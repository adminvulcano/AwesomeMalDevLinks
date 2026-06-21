# https://titansoftwork.com/insight/doing_what_edrs_wont/

Insights

Blackbird: Doing What EDRs Won't.

There's a reason security products avoid kernel hooking. They are fragile, build-sensitive, and BSOD prone. Advanced malware analysis demands the visibility they provide. This post delves into the hook engine behind Blackbird and the struggle developing it.

[20-05-2026 • 8damon\\
\\
8 min read\\
\\
**K2: Detecting Syscalls** \\
\\
SysWhispers, HellsGate, HeavensGate, SidewaysGate, SpoofGate, TFGate, DoomGate, whatever gate your tool is being detected before the initial handle fully opens. How do EDR's detect & deny direct and indirect syscalls?\\
\\
Read article](https://titansoftwork.com/insight/detecting_syscalls/)[20-04-2026 • 8damon\\
\\
13 min read\\
\\
**Blackbird: Defeating Anti-Virtualization Technologies** \\
\\
How does Blackbird make Windows lie to malware's faces? Most anti-analysis checks trust the kernel because they have no choice. Blackbird weaponizes this by modifying syscall, timing & registry return data, erasing VM-identifiers and much, much more.\\
\\
Read article](https://titansoftwork.com/insight/defeating_antivirtualization/)[13-03-2026 • 8damon\\
\\
9 min read\\
\\
**Blackbird: Doing What EDRs Won't.** \\
\\
There's a reason security products avoid kernel hooking. They are fragile, build-sensitive, and BSOD prone. Advanced malware analysis demands the visibility they provide. This post delves into the hook engine behind Blackbird and the struggle developing it.\\
\\
Read article](https://titansoftwork.com/insight/doing_what_edrs_wont/)[05-02-2026 • 8damon\\
\\
16 min read\\
\\
**ActiveBreach Engine: Rethinking Syscall Execution Under EDR** \\
\\
Modern defensive tooling doesn’t need to see payloads to stop you, it only needs to see the call path. This post breaks down how Windows system calls are intercepted, how syscall stubs became signatures, and why ActiveBreach takes a fundamentally different approach.\\
\\
Read article](https://titansoftwork.com/insight/syscall_execution/)

TITAN INSIGHTS

13-03-2026 • 8damon

9 min read

# Blackbird: Doing What EDRs Won't.

## Intro

Fair warning, this blogpost gets quite technical, goodluck!

Kernel hooking is not difficult because a jump is difficult, that's easy.

So why do **EDR** avoid kernel hooks? In itself they sound great, telemetry directly from the routines themselves, no callbacks required, full control over kernel components. It's not that easy.

Controlling _all_ of the conditions around kernel routines well enough so that the target routine still behaves exactly as it did before is extremely difficult. That means respecting instruction boundaries, patchguard, register state, paged pools, IRQL constraints, memory protections, SMP visibility, handler lifetime, unload sequencing, performance and failure atomicity. Miss any one of those and bugcheck!

Sadly, EDRs also have to behave, since they are deployed on thousands, even millions of corporate and consumer systems. They can't afford to BSOD. [Blackbird](https://github.com/8damon/Blackbird-Platform) has no such problem;

This post covers the [Blackbirds Kernel Hook Engine](https://github.com/8damon/Blackbird-Platform/tree/stable/kernel) AKA the most challenging component I've ever built.

The paths under instrumentation are:

- `NtQuerySystemInformation(Ex)`
- `NtQueryInformationProcess`
- `NtWriteVirtualMemory`
- `NtProtectVirtualMemory`
- `NtCreateSection`
- `NtMapViewOfSection`
- `NtAllocateVirtualMemory`
- `NtQuerySystemInformationEx`

Flow:

- if Blackbird is disarmed, pass through immediately
- if Blackbird is armed, only continue instrumentation when the caller PID is in the monitored set
- keep the instrument path safe under kernel execution constraints
- never violate the original routines execution semantics(!)

Sounds simple right?

* * *

## The Goal

Blackbird needed lightweight telemetry on a narrow set of kernel-facing APIs that tend to matter for memory manipulation, section activity, and process inspection, I wanted this because Ob\* & Ps\* callbacks provide too little information.

![BK_HOOK_NTALLOC](https://titansoftwork.com/content/insights/media/blackbird/NtAllocateVirtualMemoryBkHook.png)

This, is the goal. That's a clean, working, hooked `ntoskrnl.exe!NtAllocateVirtualMemory`.

## Problems, Complexities & Problems

The original hook logic inherited too much user-mode thinking.

Usermode hooking is easy, especially `NtXxx` calls, as they all follow the same exact stub, with differing SSN's. Kernel? Not so much, did chatgpt just tell you to hook the SSDT? Bugcheck!

The assumptions were:

- overwrite enough bytes to fit the hook
- build a trampoline and jump back
- if installation fails, free state and move on
- if the patch disassembles cleanly, the hook is probably fine

That includes:

- complete instruction boundaries
- correct register state
- correct cross-core patch visibility
- failure handling that restores executable state before freeing anything

This was NOT considered early on.

## What Actually Broke

There were three real failure classes.

### 1\. Truncated Prologues

The first issue was boundary selection.

Some overwrite lengths cut through live instructions, which meant the trampoline replayed instruction fragments instead of complete instructions. Control flow then returned into a function that was already semantically poisoned.

First major lesson was that just because it covers the hook length doesn't mean it doesn't slice the kernel routine mid-instruction.

The logs that made this obvious were the live prologue dumps from install.

A one-byte miss was enough to Bugcheck!

This happened a lot.

### 2\. Register-Clobbering Hook Shape

The second issue was the hook encoding itself.

A `mov rax, imm64; jmp rax` style redirect is convenient, but it mutates `RAX`. That is not automatically safe just because it is common. A lot of targets care.

`NtAllocateVirtualMemory` was the clearest case. Early routine state was sensitive enough that clobbering `RAX` would destroy the kernel routine itself. The jump worked. The routine itself did not.

### 3 Unsafe Rollback

The third issue was failure handling.

One install failure path could leave the target routine patched while the trampoline state was already being torn down. That is a stale live entry point into freed executable memory, which is exactly the kind of bug that turns debugging into archaeology. Now if install fails, original bytes must be restored before anything else is released.

* * *

## How the Hook Engine Works Now

The engine is descriptor driven. Each hook target is described up front by `BLACKBIRD_NTAPI_HOOK_DESCRIPTOR`:

```c
typedef struct _BLACKBIRD_NTAPI_HOOK_DESCRIPTOR
{
    PCSTR ApiName;
    PCWSTR Name0;
    PCWSTR Name1;
    PCWSTR Name2;
    PVOID HookFunction;
    ULONG OverwriteLength;
    BOOLEAN Required;
    ULONGLONG FallbackNtosOffset;
    UCHAR FallbackSignature[8];
    ULONG FallbackSignatureSize;
} BLACKBIRD_NTAPI_HOOK_DESCRIPTOR;
```

That descriptor specs:

- the logical API name
- the export names to try
- the hook entry point
- the overwrite length validated for that target
- whether the hook is required
- optional fallback signature metadata if export resolution fails

Runtime state is stored in `BLACKBIRD_NTAPI_HOOK`:

```c
typedef struct _BLACKBIRD_NTAPI_HOOK
{
    BLACKBIRD_NTAPI_HOOK_DESCRIPTOR Descriptor;
    PVOID RoutineAddress;
    PVOID Trampoline;
    UCHAR OriginalPatch[BLACKBIRD_NTAPI_MAX_OVERWRITE];
    BOOLEAN Installed;
} BLACKBIRD_NTAPI_HOOK;
```

### Resolving the Target Routine

Install begins by resolving the target export using `MmGetSystemRoutineAddress`, trying up to three names:

```c
Hook->RoutineAddress =
    BLACKBIRDNtApiResolveAddress(
        Hook->Descriptor.Name0,
        Hook->Descriptor.Name1,
        Hook->Descriptor.Name2
    );
```

If export resolution misses, the engine can fall back to SSDT/signature-based resolution.

That fallback exists because `MmGetSystemRoutineAddress` ignores certain symbols.

```c
if (!BLACKBIRDNtApiIsKernelPointer(Hook->RoutineAddress))
{
    return STATUS_PROCEDURE_NOT_FOUND;
}
```

### Capturing the Prologue

Once the routine is resolved, the engine copies the original bytes from the target prologue into `OriginalPatch`:

```c
RtlCopyMemory(Hook->OriginalPatch, Hook->RoutineAddress, overwriteLength);
```

Debug printing. Even in the kernel, I found myself spamming `DbgPrintEx` everywhere to see what WinDbg would pick up on, if you run Blackbird with a KdDebugger attached you'll see exactly what I mean.

* * *

## The Final Hook

![BLACKBIRD_HOOK](https://titansoftwork.com/content/capabilities/blackbird/BlackbirdHookDisassembly.png)

The hook now uses a RIP-indirect absolute jump generated by `BLACKBIRDNtApiBuildJump`:

```c
VOID BLACKBIRDNtApiBuildJump(UCHAR *Patch, PVOID Destination)
{
    ULONGLONG destination64;
    ULONG displacement = 0;

    destination64 = (ULONGLONG)(ULONG_PTR)Destination;
    Patch[0] = 0xFF;
    Patch[1] = 0x25;
    RtlCopyMemory(&Patch[2], &displacement, sizeof(displacement));
    RtlCopyMemory(&Patch[6], &destination64, sizeof(destination64));
}
```

Which produces:

```x86asm
FF 25 00 00 00 00
<8-byte absolute target>
```

Patch size is 14 bytes.

The hook no longer needs to burn a general-purpose register just to redirect control flow. No `mov rax, imm64; jmp rax`, which caused huge problems before. The patch bytes after the jump are padded with NOPs out to the validated overwrite length.

### Building the Trampoline

The trampoline is allocated from `NonPagedPoolExecute` and contains:

- the stolen prologue bytes
- a jump back to `RoutineAddress + overwriteLength`

`BLACKBIRDNtApiHookInstall`:

```c
trampoline =
    ExAllocatePoolWithTag(
        NonPagedPoolExecute,
        overwriteLength + BLACKBIRD_NTAPI_PATCH_SIZE,
        BLACKBIRD_NTAPI_HOOK_TAG
    );

RtlCopyMemory(trampoline, Hook->OriginalPatch, overwriteLength);
BLACKBIRDNtApiBuildJump(
    trampolineJump,
    (PVOID)((PUCHAR)Hook->RoutineAddress + overwriteLength)
);
RtlCopyMemory(
    (PUCHAR)trampoline + overwriteLength,
    trampolineJump,
    BLACKBIRD_NTAPI_PATCH_SIZE
);
```

The trampoline is then stored as the "original" function pointer for that hook target. Every hook handler calls through that trampoline, not through some reconstructed fantasy of the original routine.

### Writing Into Read-Only Kernel Text

You may be wondering, how?

Yeah me too.

The engine remaps the target through an MDL and temporarily gives that mapping executable read-write protection.

What's an MDL?

> An [MDL (Memory Descriptor List)](https://medium.com/@WaterBucket/understanding-memory-descriptor-lists-mdls-for-windows-vulnerability-research-exploit-7de8729caee7) describes physical pages and allows the kernel to map them with different protections. Here it's used to temporarily create a writable mapping of normally read-only kernel code.

```c
mdl = IoAllocateMdl(Destination, (ULONG)Size, FALSE, FALSE, NULL);
MmProbeAndLockPages(mdl, KernelMode, IoReadAccess);
mappedAddress = MmMapLockedPagesSpecifyCache(
    mdl,
    KernelMode,
    MmCached,
    NULL,
    FALSE,
    NormalPagePriority
);
MmProtectMdlSystemAddress(mdl, PAGE_EXECUTE_READWRITE);
```

Worth noting the cache type here: `MmCached`, not `MmNonCached`. I originally used `MmNonCached` and it caused problems. Creating overlapping UC and WB aliases to the same physical page is undefined behaviour per [Intel Vol. 3A §11.12.4](https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-vol-3a-part-1-manual.pdf), and it means the write can bypass the L1/L2 cache entirely, leaving remote CPU icaches stale in a way that MFENCE alone can't fix. With `MmCached` the store goes through the normal WB cache hierarchy and the IPI-forced serialisation on each remote CPU is enough.

Then came another problem... Cores! Yes, the CPU ones. Turns out writing directly to kernel memory without any sort of synchronization causes problems. I've had to learn what [IPI's](https://en.wikipedia.org/wiki/Inter-processor_interrupt) are.

Basically, in usermode when you write to memory, the kernel memory handler will automatically do this for you, when working in kernel space it's on you. An IPI ( [Inter-Processor Interrupt](https://en.wikipedia.org/wiki/Inter-processor_interrupt)) is exactly what it sounds like: an [interrupt](https://en.wikipedia.org/wiki/Interrupt) sent from one CPU to the others. It forces all processors to rendezvous so they can observe the same memory state before continuing execution. Without this, one CPU could execute invalid kernel memory, bugcheck!

```c
KeIpiGenericCall(BLACKBIRDNtApiBroadcastWrite, (ULONG_PTR)&patchContext);
```

Inside the broadcast callback, one core performs the write while the rest rendezvous under the generic call mechanism:

```c
if (InterlockedCompareExchange(&patchContext->Applied, 1, 0) == 0)
{
    // Commit bytes 1..Size-1 first, byte 0 last.
    // Byte 0 is 0xFF, the JMP opcode. Writing the tail first means any
    // concurrent observer reading the hook site before we're done still
    // sees the original byte 0, so the site stays in a valid pre-hook
    // state until the final store makes the jump live.
    for (i = 1; i < patchContext->Size; ++i)
    {
        patchContext->Destination[i] = patchContext->Source[i];
    }
    patchContext->Destination[0] = patchContext->Source[0];

    KeMemoryBarrier();
    {
        int cpuInfo[4];
        __cpuid(cpuInfo, 0);
    }
}
```

`KeMemoryBarrier()` issues an MFENCE but it isn't a serialising instruction, so it doesn't flush the instruction cache on remote processors. Self-modifying code on x86-64 needs a serialising instruction on the writing CPU after the stores complete. `CPUID` is the lightest one available in ring 0 on both Intel and AMD. The IPI delivery already forced a serialising interrupt on every remote CPU before they resumed, so the `CPUID` here only covers the writing core itself.

### Verification and Rollback

After the patch is applied, the engine immediately re-reads the modified bytes and compares them against the expected patch.

```c
RtlCopyMemory(verifyPatch, Hook->RoutineAddress, overwriteLength);

if (RtlCompareMemory(verifyPatch, patch, overwriteLength) != overwriteLength)
{
    BLACKBIRDNtApiRollbackPatchOnInstallFailure(Hook, overwriteLength);
    return STATUS_DATA_ERROR;
}
```

If verification fails, rollback restores the original prologue bytes before anything else is freed:

```c
rollbackStatus = BLACKBIRDNtApiWriteReadonlyMemory(
    Hook->RoutineAddress,
    Hook->OriginalPatch,
    OverwriteLength
);
```

* * *

## Hook Execution

Each hook follows the same broad structure:

1. increment the in-flight counter
2. validate the original trampoline pointer
3. call the original routine
4. sanitize or observe output if needed
5. check whether logging should occur
6. emit ETW telemetry
7. release rundown protection
8. decrement the in-flight counter

For example, `BLACKBIRDNtWriteVirtualMemoryHook`:

```c
BLACKBIRDNtApiHookEnter();

if (g_OriginalNtWriteVirtualMemory == NULL)
{
    status = STATUS_INVALID_DEVICE_STATE;
    goto Exit;
}

status = g_OriginalNtWriteVirtualMemory(
    ProcessHandle,
    BaseAddress,
    Buffer,
    BufferSize,
    NumberOfBytesWritten
);

if (!BLACKBIRDNtApiShouldLog(&callerPid))
{
    goto Exit;
}

observedWritten = BLACKBIRDNtApiReadSizeTSafe(NumberOfBytesWritten);
BLACKBIRDNtApiLog(
    "NtWriteVirtualMemory",
    callerPid,
    (UINT64)(ULONG_PTR)ProcessHandle,
    (UINT64)(ULONG_PTR)BaseAddress,
    (UINT64)(ULONG_PTR)Buffer,
    (UINT64)BufferSize,
    (UINT64)observedWritten,
    0, 0, 0,
    status
);
```

### Why `NtAllocateVirtualMemory` Gets Special Treatment

`NtAllocateVirtualMemory` is not hooked through the same plain C path as the rest. The hook descriptor points to `BLACKBIRDNtAllocateVirtualMemoryHookStub` instead of a normal C handler.

`NtAllocateVirtualMemory` was one of the routines that proved especially sensitive to ABI and entry-state assumptions. Using a dedicated stub path reduces how much glue code gets to interfere with the call state before execution reaches the original trampoline.

There is also a pre-log path, `BLACKBIRDNtAllocateVirtualMemoryPreLog`, which records arguments only after the same gating logic is satisfied:

```c
observedBase = BLACKBIRDNtApiReadPointerSafe(BaseAddress);
observedRegionSize = BLACKBIRDNtApiReadSizeTSafe(RegionSize);

BLACKBIRDNtApiLog(
    "NtAllocateVirtualMemory",
    callerPid,
    (UINT64)(ULONG_PTR)ProcessHandle,
    (UINT64)(ULONG_PTR)observedBase,
    (UINT64)observedRegionSize,
    (UINT64)ZeroBits,
    (UINT64)AllocationType,
    (UINT64)Protect,
    0, 0,
    STATUS_SUCCESS
);
```

### In-Flight Tracking & Unloads

Every hook entry increments `g_NtApiHookInFlight`:

```c
VOID BLACKBIRDNtApiHookEnter(VOID)
{
    InterlockedIncrement(&g_NtApiHookInFlight);
}
```

Every exit decrements it and corrects underflow if anything goes wrong:

```c
remaining = InterlockedDecrement(&g_NtApiHookInFlight);
if (remaining < 0)
{
    InterlockedExchange(&g_NtApiHookInFlight, 0);
}
```

During uninitialize, Blackbird does not immediately free trampolines. It first:

1. marks the monitor unloading
2. deactivates all hooks by restoring original bytes
3. waits for rundown release
4. waits for in-flight hook entries to drain
5. only then frees trampoline state

```c
for (i = 0; i < BLACKBIRD_HOOK_COUNT; ++i)
{
    BLACKBIRDNtApiHookDeactivate(&g_Hooks[i]);
}

ExWaitForRundownProtectionRelease(&g_NtApiRundown);
BLACKBIRDNtApiWaitForInFlightCalls();

for (i = 0; i < BLACKBIRD_HOOK_COUNT; ++i)
{
    BLACKBIRDNtApiHookFreeTrampoline(&g_Hooks[i]);
}
```

### Performance

Drivers have to be fast. Very fast. [IRQL](https://en.wikipedia.org/wiki/IRQL)'s must be cleared very quickly. If you've ever opened [SystemInformer](https://systeminformer.sourceforge.io/) and watched the _System Calls Delta_ stat you'll see that hundreds and thousands of syscalls execute every delta cycle. Now imagine a extra routine (a hook), on a lot of the core kernel functions, doing a bunch of processing and copying in that extremely critical path. Sounds slow right? It is.

I don't want to slow the system to a crawl, so I use a very simple state machine;

If the driver is not armed, the path exits quickly.

If the PID is not monitored, the path exits quickly.

If the current IRQL is wrong, the path exits quickly.

The hook engine still exists in the function entry path, but if the driver isnt armed, and if the PID the syscall is coming from isn't in the drivers armed list, it ignores it.

## Conclusion

I see why people dislike kernel development. The amount of variables to constantly consider, reconsider and recheck again and again cause huge cognitive load. The debugging mechanisms being WinDbg, printing and `analyze -v` on bugchecks is extremely frustrating and causes slow debugging.

I also see how powerful it is, and why AntiCheats & EDRs live down here. There's a lot of misconcepts about Patchguard (KPP), people seem to think it protects the whole kernel, it does not. It is a telemetry goldmine, unfortunately any sophisticated EDR will make it almost impossible for userland malware to stay undetected, unless their heuristics are off. Not even getting started on the Hypervisors being brought in.

After spending significant time developing Blackbird to first of all detect my _own_ frameworks, I realized what a large misconception a large part of the "maldev" community has surrounding EDRs. My project **ActiveBreach** is effective yes, until it faces a real EDR. That project is seen as "modern" and **SysWhispers5** just released, still with the same misconcepts it had 5 years ago. Stackwalking and spoofing is one thing, but your allocations, threads, queries, handles, _every_ single thing is monitored.