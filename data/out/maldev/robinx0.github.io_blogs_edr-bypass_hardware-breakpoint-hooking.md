# https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/

Apr 14, 2026ELITE· 5 MIN READ

# Hardware Breakpoint Hooking: Bypassing Inline EDR Hooks Without Touching Memory

A practical C++ guide to using x86-64 debug registers (DR0-DR7) for user-mode API hooking - how EDRs are blind to hardware breakpoints, when HWBPs beat patching, and how to build a minimal HWBP engine.

#edr-bypass#hardware-breakpoints#hooking#windows#c++

On this page

01. [Why Hardware Breakpoints](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/#why-hardware-breakpoints)
02. [The Debug Register Model](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/#the-debug-register-model)
03. [Installation](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/#installation)
04. [Handling the Exception](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/#handling-the-exception)
05. [Where This Beats Patching](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/#where-this-beats-patching)
06. [The Detection Vectors You Must Think About](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/#the-detection-vectors-you-must-think-about)
07. [1\. Reading DR Registers](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/#1-reading-dr-registers)
08. [2\. Single-step Events via ETW](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/#2-single-step-events-via-etw)
09. [3\. NtContinue / SetThreadContext frequency](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/#3-ntcontinue--setthreadcontext-frequency)
10. [Minimal Working Example - Blocking CreateRemoteThread Injection](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/#minimal-working-example---blocking-createremotethread-injection)
11. [Pairing with Other Techniques](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/#pairing-with-other-techniques)
12. [Summary](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/#summary)

## Why Hardware Breakpoints [\#](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/\#why-hardware-breakpoints)

Most EDRs hook user-mode APIs by patching the first few bytes of the function in `ntdll.dll` / `kernelbase.dll` with a `jmp` to telemetry code. This is **inline hooking**. Everything unhooks this eventually - restore bytes from a fresh disk copy, map a clean ntdll, direct syscalls - but all of those _modify memory_, which is itself a signal.

Hardware breakpoints are different. The CPU has four **debug registers** (DR0-DR3) that hold addresses to break on. When execution reaches that address, the CPU raises `EXCEPTION_SINGLE_STEP` \- regardless of what bytes are at that location. No memory is modified. No `VirtualProtect` call. No `WriteProcessMemory`. Just an MSR write.

If you install a vectored exception handler that filters on the breakpoint address and rewrites the CPU context to redirect execution, you have a **hook** that leaves zero memory footprint.

## The Debug Register Model [\#](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/\#the-debug-register-model)

```
DR0-DR3  - breakpoint linear addresses
DR6      - status (which DR triggered)
DR7      - control (enable / len / rw bits)
Copy
```

Four HWBPs per thread. They’re **per-thread**, not process-wide, which is both a feature (stealth - only the threads you install on break) and a constraint (you must hook every relevant thread, including ones spawned after).

DR7 layout - the interesting bits:

| Bits | Purpose |
| --- | --- |
| 0,2,4,6 (L0-L3) | Local enable for DR0-DR3 |
| 16-17 (R/W0) | 00=exec, 01=write, 11=rw |
| 18-19 (LEN0) | 00=1 byte, 01=2, 11=4 |

For an execution breakpoint on DR0 at `NtOpenProcess`:

```
ctx.Dr0 = (DWORD64)target_fn;
ctx.Dr7 = (1 << 0);  // L0 = 1, RW0 = 00 (exec), LEN0 = 00 (1 byte)
Copyc
```

## Installation [\#](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/\#installation)

`SetThreadContext` with `CONTEXT_DEBUG_REGISTERS` is the clean way:

```
#include <windows.h>

bool SetHwBp(HANDLE hThread, void* addr, int slot) {
    CONTEXT ctx = { .ContextFlags = CONTEXT_DEBUG_REGISTERS };
    if (!GetThreadContext(hThread, &ctx)) return false;

    switch (slot) {
        case 0: ctx.Dr0 = (DWORD64)addr; break;
        case 1: ctx.Dr1 = (DWORD64)addr; break;
        case 2: ctx.Dr2 = (DWORD64)addr; break;
        case 3: ctx.Dr3 = (DWORD64)addr; break;
        default: return false;
    }

    // Clear the two control bits for this slot, then enable L and set exec+1byte
    ctx.Dr7 &= ~(0b11ULL << (slot * 2));
    ctx.Dr7 |=  (0b01ULL << (slot * 2));          // L_i = 1
    ctx.Dr7 &= ~(0b1111ULL << (16 + slot * 4));   // RW_i=00, LEN_i=00

    return SetThreadContext(hThread, &ctx);
}
Copycpp
```

`GetCurrentThread()` returns a pseudo-handle; for current-thread use, that’s fine.

## Handling the Exception [\#](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/\#handling-the-exception)

Register a **vectored exception handler** early. When the CPU hits the breakpoint, Windows walks the VEH chain before the SEH chain, so you see it first:

```
LONG CALLBACK VehHandler(EXCEPTION_POINTERS* ex) {
    if (ex->ExceptionRecord->ExceptionCode != EXCEPTION_SINGLE_STEP)
        return EXCEPTION_CONTINUE_SEARCH;

    auto addr = ex->ExceptionRecord->ExceptionAddress;

    // Is this our hook?
    if (addr == g_ntOpenProcess) {
        // RCX = first arg on x64, RDX = second, R8 = third, R9 = fourth
        HANDLE* phProc    = (HANDLE*)   ex->ContextRecord->Rcx;
        ACCESS_MASK mask  = (ACCESS_MASK)ex->ContextRecord->Rdx;

        // Sanitize: drop PROCESS_VM_WRITE / PROCESS_CREATE_THREAD so injection chains fail
        ex->ContextRecord->Rdx = mask & ~(PROCESS_VM_WRITE | PROCESS_CREATE_THREAD);

        // Re-arm: set the Resume Flag so we don't re-trigger on the same instruction
        ex->ContextRecord->EFlags |= 0x10000;
        return EXCEPTION_CONTINUE_EXECUTION;
    }

    return EXCEPTION_CONTINUE_SEARCH;
}

AddVectoredExceptionHandler(1, VehHandler);
Copycpp
```

The **Resume Flag (RF, bit 16 of EFlags)** is critical: it tells the CPU to skip the breakpoint check for the _next_ instruction, so you don’t loop forever on your own hook.

## Where This Beats Patching [\#](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/\#where-this-beats-patching)

Scenarios where HWBP hooking wins over inline patching:

1. **EDR inline-hook integrity checks.** Some mature EDRs (SentinelOne, CrowdStrike) compute hashes of hot functions every few seconds. If you’ve overwritten the first 5 bytes, they’ll detect it. HWBPs leave those bytes untouched.
2. **PatchGuard-friendly (kernel analog).** In kernel work, writing to SSDT or syscall handlers trips PatchGuard. DR-based kernel hooking via `KeSetAffinityThread` \+ IPI dance can evade.
3. **Self-healing telemetry.** EDRs that monitor `NtProtectVirtualMemory` and `NtWriteVirtualMemory` will flag any `VirtualProtect(PAGE_EXECUTE_READWRITE)` in `ntdll`. HWBPs don’t touch either.

## The Detection Vectors You Must Think About [\#](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/\#the-detection-vectors-you-must-think-about)

HWBP hooking is not invisible. It’s just **differently** visible.

### 1\. Reading DR Registers [\#](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/\#1-reading-dr-registers)

EDRs can call `GetThreadContext` on their own threads (or inject a probe thread) and check if DR0-DR3 are non-zero. Unusual, but Elastic’s endpoint agent does this in some configurations.

**Mitigation**: only install HWBPs on the thread actually making the call, clear them immediately after, and avoid installing on EDR-owned threads you can identify via `NtQueryInformationThread(ThreadBasicInformation).ClientId.UniqueProcess`.

### 2\. Single-step Events via ETW [\#](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/\#2-single-step-events-via-etw)

`Microsoft-Windows-Kernel-Power` and `Microsoft-Windows-Threat-Intelligence` expose single-step exceptions to ETW consumers. A high rate of single-step from a non-debugger process is weird.

**Mitigation**: batch your hooks, avoid tight loops that re-trigger, and consider pairing with ETW patching (`EtwEventWrite` NOP) to quiet the telemetry channel entirely.

### 3\. `NtContinue` / `SetThreadContext` frequency [\#](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/\#3-ntcontinue--setthreadcontext-frequency)

`SetThreadContext` on another thread’s handle from user-mode is rare in benign applications. Call-pattern detection (Elastic ML rules) picks this up.

**Mitigation**: self-context only. If you need to hook another thread, use `NtQueueApcThread` to have _it_ install its own HWBPs.

## Minimal Working Example - Blocking CreateRemoteThread Injection [\#](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/\#minimal-working-example---blocking-createremotethread-injection)

A full PoC that prevents the current process from being injected into:

```
#include <windows.h>
#include <cstdio>

static void* g_ntCreateThreadEx = nullptr;

LONG CALLBACK Veh(EXCEPTION_POINTERS* ex) {
    if (ex->ExceptionRecord->ExceptionCode != EXCEPTION_SINGLE_STEP)
        return EXCEPTION_CONTINUE_SEARCH;

    if (ex->ExceptionRecord->ExceptionAddress == g_ntCreateThreadEx) {
        // NtCreateThreadEx(HANDLE* ThreadHandle, ACCESS_MASK, POBJECT_ATTRIBUTES,
        //                  HANDLE ProcessHandle, ...)
        // RCX = thread handle ptr, R8 = attributes, R9 = process handle
        HANDLE hTargetProc = (HANDLE)ex->ContextRecord->R9;

        // Deny if target isn't our own process
        if (hTargetProc != (HANDLE)-1) {
            ex->ContextRecord->Rax = 0xC0000022;  // STATUS_ACCESS_DENIED
            // Skip the function body - return to caller
            ex->ContextRecord->Rip = *(DWORD64*)ex->ContextRecord->Rsp;
            ex->ContextRecord->Rsp += 8;
            ex->ContextRecord->EFlags |= 0x10000;
            return EXCEPTION_CONTINUE_EXECUTION;
        }
        ex->ContextRecord->EFlags |= 0x10000;
    }
    return EXCEPTION_CONTINUE_SEARCH;
}

int main() {
    HMODULE nt = GetModuleHandleA("ntdll.dll");
    g_ntCreateThreadEx = GetProcAddress(nt, "NtCreateThreadEx");

    AddVectoredExceptionHandler(1, Veh);

    CONTEXT ctx = { .ContextFlags = CONTEXT_DEBUG_REGISTERS };
    GetThreadContext(GetCurrentThread(), &ctx);
    ctx.Dr0 = (DWORD64)g_ntCreateThreadEx;
    ctx.Dr7 = 1;  // L0=1, RW0=00, LEN0=00
    SetThreadContext(GetCurrentThread(), &ctx);

    printf("HWBP installed. Try to inject now.\n");
    Sleep(INFINITE);
}
Copycpp
```

Run it, then try `process hollowing` or `CreateRemoteThread` from another process - the injection syscall returns `STATUS_ACCESS_DENIED` without the target process ever losing context.

## Pairing with Other Techniques [\#](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/\#pairing-with-other-techniques)

HWBP hooking really shines in combination:

- **HWBP + indirect syscalls**: the HWBP hooks your own stub before it hits the syscall - useful for telemetry spoofing (lie about `NtOpenProcess` args before the real syscall fires).
- **HWBP + stack spoofing**: mask the call stack _and_ avoid inline hook detection. Two independent detection vectors blinded at once.
- **HWBP + module stomping**: load a legit signed DLL, stomp its `.text` with your code, install HWBPs to redirect its imports. No `VirtualAlloc(RWX)` ever.

## Summary [\#](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/\#summary)

Hardware breakpoints trade a small detection surface (DR register snooping, single-step ETW) for a huge benefit: **no memory modifications**. For operators facing mature EDRs that baseline module hashes, they’re one of the cleanest primitives available.

The reference implementation above is deliberately minimal. Production-quality HWBP engines handle thread creation callbacks, exception chaining conflicts, WOW64 compatibility, and slot allocation across multiple concurrent hooks - but the core is 40 lines of code.

> Inline hooking changes the program. Hardware breakpoints change the CPU’s interpretation of the program. Defenders instrumented for the former still mostly miss the latter.

Continue · Edr bypass

[Apr 17, 2026The Userland EDR Bypass Stack: Unhooking, Syscalls, ETW/AMSI, and Kernel CallbacksA comprehensive guide to the layered techniques that make up modern userland EDR evasio...ELITE](https://robinx0.github.io/blogs/edr-bypass/userland-edr-bypass-stack/) [Mar 29, 2026Sleep Obfuscation Deep Dive: Ekko, Zilean, and FoliageAdvanced sleep obfuscation techniques that encrypt implant memory during sleep cycles t...HARD](https://robinx0.github.io/blogs/edr-bypass/sleep-obfuscation-techniques/) [Mar 25, 2026Call Stack Spoofing: Defeating EDR Stack TelemetryAdvanced techniques for spoofing thread call stacks to evade EDR behavioral detection -...HARD](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/)

[← Home](https://robinx0.github.io/) [More Edr bypass →](https://robinx0.github.io/writeups?cat=Edr+bypass)

×‹›