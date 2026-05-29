# https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/

Mar 25, 2026HARD· 4 MIN READ

# Call Stack Spoofing: Defeating EDR Stack Telemetry

Advanced techniques for spoofing thread call stacks to evade EDR behavioral detection - covering return address spoofing, synthetic frames, and thread stack manipulation.

#stack-spoofing#edr-evasion#call-stack#return-address#windows-internals

On this page

01. [Why Call Stacks Matter to EDR](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#why-call-stacks-matter-to-edr)
02. [Technique 1: Return Address Spoofing](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#technique-1-return-address-spoofing)
03. [Concept](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#concept)
04. [Implementation](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#implementation)
05. [The Problem](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#the-problem)
06. [Solution: Frame Spoofing with Desync](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#solution-frame-spoofing-with-desync)
07. [Technique 2: Synthetic Stack Frames](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#technique-2-synthetic-stack-frames)
08. [Concept](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#concept-1)
09. [Implementation with SilentMoonwalk](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#implementation-with-silentmoonwalk)
10. [Challenges](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#challenges)
11. [Technique 3: Thread Stack Spoofing (Sleep-Time)](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#technique-3-thread-stack-spoofing-sleep-time)
12. [Concept](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#concept-2)
13. [CallStackMasker Approach](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#callstackmasker-approach)
14. [Combined with Sleep Obfuscation](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#combined-with-sleep-obfuscation)
15. [Technique 4: Hardware Breakpoint-Based Spoofing](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#technique-4-hardware-breakpoint-based-spoofing)
16. [Concept](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#concept-3)
17. [Flow](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#flow)
18. [Advantages](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#advantages)
19. [Detection and Counter-Detection](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#detection-and-counter-detection)
20. [How EDR Detects Spoofing](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#how-edr-detects-spoofing)
21. [Counter-Detection](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#counter-detection)
22. [Comparison](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/#comparison)

## Why Call Stacks Matter to EDR [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#why-call-stacks-matter-to-edr)

When your implant calls `NtAllocateVirtualMemory` via indirect syscalls, the syscall itself might bypass userland hooks. But modern EDR products don’t just hook - they inspect the **call stack** of the calling thread via kernel callbacks or ETW stack walking.

A legitimate call to `VirtualAlloc` from `kernel32.dll` has a predictable call stack:

```
ntdll!NtAllocateVirtualMemory
kernelbase!VirtualAlloc
kernel32!VirtualAllocStub
application!SomeFunction
application!main
ntdll!RtlUserThreadStart
Copy
```

But when your implant calls the same syscall, the stack shows:

```
ntdll!NtAllocateVirtualMemory
<UNKNOWN MODULE>     ← Your implant (unbacked memory)
<UNKNOWN MODULE>     ← More implant code
ntdll!RtlUserThreadStart
Copy
```

The presence of return addresses pointing to **unbacked memory** (not backed by a file on disk) is a strong indicator of malicious in-memory execution. This is what call stack spoofing defeats.

## Technique 1: Return Address Spoofing [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#technique-1-return-address-spoofing)

### Concept [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#concept)

Before making a sensitive API call, overwrite the return address on the stack to point to a legitimate module (like `kernel32.dll`), make the call, then restore the original return address.

### Implementation [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#implementation)

```
; Save real return address
pop rax                    ; Pop real return address into RAX
mov [saved_ret], rax       ; Save it

; Push fake return address (points into kernel32)
mov rcx, [kernel32_gadget] ; Address of 'ret' instruction in kernel32.dll
push rcx                   ; Fake return address on stack

; Make the API call
; When EDR walks the stack, it sees kernel32 as the caller
call target_api

; The 'ret' in kernel32 will return to... nowhere useful
; So we need to handle the return ourselves
Copynasm
```

### The Problem [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#the-problem)

Simple return address spoofing breaks the return flow. When the API returns, it `ret`s to your fake address (a `ret` gadget in kernel32), which then `ret`s to whatever is next on the stack - likely crashing.

### Solution: Frame Spoofing with Desync [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#solution-frame-spoofing-with-desync)

Use a more sophisticated approach where you construct a full fake frame and use a trampoline to redirect execution after the API call returns:

```
// 1. Save current RSP and RBP
// 2. Set up a fake stack frame that looks legitimate
// 3. Make the API call from this fake frame
// 4. API returns to your trampoline gadget
// 5. Trampoline restores the real RSP/RBP
// 6. Execution continues normally
Copyc
```

## Technique 2: Synthetic Stack Frames [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#technique-2-synthetic-stack-frames)

### Concept [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#concept-1)

Instead of just spoofing one return address, construct an entire fake call stack that mimics a legitimate execution path. The stack looks like a normal chain of kernel32 → kernelbase → ntdll calls.

### Implementation with SilentMoonwalk [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#implementation-with-silentmoonwalk)

The SilentMoonwalk technique (by KlezVirus) constructs synthetic frames by:

1. **Finding ROP gadgets** in legitimate modules (`add rsp, X; ret` sequences)
2. **Building a fake frame chain** where each return address points to a gadget that adjusts RSP and returns to the next fake frame
3. **The final gadget** returns to your real code

```
// Desired fake call stack:
// kernel32!BaseThreadInitThunk+0x14
// ntdll!RtlUserThreadStart+0x21

// Find the right gadgets
PVOID k32_gadget = FindGadget("kernel32.dll", "add rsp, 0x38; ret");
PVOID ntdll_gadget = FindGadget("ntdll.dll", "add rsp, 0x28; ret");

// Construct frames on the stack
*(PVOID*)(fake_stack + 0x00) = api_to_call;
*(PVOID*)(fake_stack + 0x38) = k32_gadget;   // After API returns
*(PVOID*)(fake_stack + 0x70) = ntdll_gadget;  // After k32 gadget
*(PVOID*)(fake_stack + 0x98) = real_return;    // Back to our code
Copyc
```

### Challenges [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#challenges)

- Gadget addresses change across Windows versions
- Stack alignment must be maintained (16-byte on x64)
- Some EDRs validate frame pointer chains (RBP linkage)
- Fake frames must have plausible local variable space

## Technique 3: Thread Stack Spoofing (Sleep-Time) [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#technique-3-thread-stack-spoofing-sleep-time)

### Concept [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#concept-2)

During sleep, spoof the entire thread’s call stack. When EDR scans sleeping threads (Hunt-Sleeping-Beacons), it sees a normal-looking stack instead of your implant.

### CallStackMasker Approach [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#callstackmasker-approach)

1. Before sleep, capture the current thread context
2. Overwrite the stack with a legitimate-looking chain:





```
ntdll!NtWaitForSingleObject
ntdll!RtlpTpWaitCallback
ntdll!TppWorkerThread
kernel32!BaseThreadInitThunk
ntdll!RtlUserThreadStart
Copy
```

3. Enter sleep
4. After waking, restore the real stack

### Combined with Sleep Obfuscation [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#combined-with-sleep-obfuscation)

The most effective approach combines stack spoofing with memory encryption:

```
1. Encrypt implant memory (Ekko/Foliage)
2. Spoof the call stack (CallStackMasker)
3. Sleep
   → EDR scans: memory is encrypted, stack looks normal
4. Wake → Restore stack → Decrypt memory → Execute
Copy
```

## Technique 4: Hardware Breakpoint-Based Spoofing [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#technique-4-hardware-breakpoint-based-spoofing)

### Concept [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#concept-3)

Use hardware breakpoints and a Vectored Exception Handler (VEH) to intercept execution at the point of the API call and modify the stack in the exception handler - before EDR can inspect it.

### Flow [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#flow)

```
// 1. Set hardware breakpoint on NtAllocateVirtualMemory
SetHardwareBreakpoint(0, NtAllocateVirtualMemory, DR_EXECUTE);

// 2. Register VEH
AddVectoredExceptionHandler(1, SpoofHandler);

// 3. When the API is called, breakpoint fires → VEH executes
LONG SpoofHandler(EXCEPTION_POINTERS* ex) {
    if (ex->ExceptionRecord->ExceptionCode == EXCEPTION_SINGLE_STEP) {
        // Modify the stack to look legitimate
        SpoofCallStack(ex->ContextRecord);
        // Continue execution
        return EXCEPTION_CONTINUE_EXECUTION;
    }
}
Copyc
```

### Advantages [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#advantages)

- No inline assembly required
- Works with indirect syscalls
- Can be applied selectively to specific API calls
- Hardware breakpoints don’t modify code memory

## Detection and Counter-Detection [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#detection-and-counter-detection)

### How EDR Detects Spoofing [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#how-edr-detects-spoofing)

1. **Frame pointer validation** \- Check if RBP chains are consistent
2. **Return address validation** \- Verify each return address is preceded by a `call` instruction
3. **Stack size analysis** \- Fake frames often have unusual gaps
4. **Module backing** \- Check if return addresses are in legitimate, file-backed modules

### Counter-Detection [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#counter-detection)

1. **Use real call instructions** \- Ensure each fake return address is preceded by a valid `call` in the module
2. **Maintain RBP chains** \- Link frame pointers correctly
3. **Match frame sizes** \- Use the real function’s expected frame size
4. **Vary your spoofing** \- Don’t always use the same fake chain

## Comparison [\#](https://robinx0.github.io/blogs/edr-bypass/stack-spoofing-techniques/\#comparison)

| Technique | Complexity | Stealth | Covers Sleep | Performance |
| --- | --- | --- | --- | --- |
| Return Address Spoof | Low | Medium | No | Minimal |
| Synthetic Frames | High | High | No | Low |
| Thread Stack Spoof | High | Very High | Yes | Moderate |
| HW Breakpoint Based | Medium | High | No | Minimal |
| Combined (all) | Very High | Maximum | Yes | Moderate |

> Call stack telemetry is the next frontier in the EDR arms race. Indirect syscalls bypass hooks, sleep obfuscation defeats memory scanning, and stack spoofing completes the trifecta by defeating behavioral analysis. Master all three for modern red team operations.

Continue · Edr bypass

[Apr 17, 2026The Userland EDR Bypass Stack: Unhooking, Syscalls, ETW/AMSI, and Kernel CallbacksA comprehensive guide to the layered techniques that make up modern userland EDR evasio...ELITE](https://robinx0.github.io/blogs/edr-bypass/userland-edr-bypass-stack/) [Apr 14, 2026Hardware Breakpoint Hooking: Bypassing Inline EDR Hooks Without Touching MemoryA practical C++ guide to using x86-64 debug registers (DR0-DR7) for user-mode API hooki...ELITE](https://robinx0.github.io/blogs/edr-bypass/hardware-breakpoint-hooking/) [Mar 29, 2026Sleep Obfuscation Deep Dive: Ekko, Zilean, and FoliageAdvanced sleep obfuscation techniques that encrypt implant memory during sleep cycles t...HARD](https://robinx0.github.io/blogs/edr-bypass/sleep-obfuscation-techniques/)

[← Home](https://robinx0.github.io/) [More Edr bypass →](https://robinx0.github.io/writeups?cat=Edr+bypass)

×‹›