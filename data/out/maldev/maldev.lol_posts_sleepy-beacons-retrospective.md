# https://maldev.lol/posts/sleepy-beacons-retrospective/

[← research library](https://maldev.lol/posts)

# Sleepy Beacons: A retrospective on how implants take naps

I’ve been deep in research-mode for a long-running side project (\* _caugh_\\* _implant_ \* _caugh_\*), and as part of that work I needed to get some beacon-sleep tech working. Since I haven’t been evading EDRs for a day job for a while (2+ years at this point?), I wanted to get back up to date with the latest and greatest, and shake off the rust I’ve accumulated from being away from low-level _things_ for too long.

They say the best way to (re-)learn something is to teach it. What follows is my attempt at that: a (hopefuly noob friendly) walkthrough of beacon-sleep-tech through the ages.

But first…

## Why sleep matters

Modern implants spend >95% of their life sleeping. You can consider them narcoleptic: they wake up, check in for any work items, do them, return the result, then go right back to sleep. Back in the days when Meterpreter ruled the buffers, we only had _sessions_: realtime interactive reverse shells that were allways ‘awake’. We don’t really do that anymore unless for very specefic reasons, and even for those we are starting to see the wider adoption of [async-bofs](https://www.outflank.nl/blog/2025/07/16/async-bofs-wake-me-up-before-you-go-go/) which can run long running code COFF-style, allowing the main implant to sleep while the async BOF continues to run.

So why is sleep so important?

## Just `Sleep()`

Consider the naive approach: call `Sleep(sleep_ms)` in a loop. The implant thread is descheduled for `sleep_ms` milliseconds, then wakes up, does its thing, and goes back to sleep. The CPU is happy, but so are defenders - your implant is just _sitting there, ominiously…_ in memory available at anypoint for a scan or memory dump. The implant thread’s call stack points at `ntdll!NtDelayExecution` or `ntdll!NtWaitForSingleObjectEx` (depending on how you implement the sleep), and its heap allocations are unprotected. It’s a sitting duck, waiting for a new yara rule to make a joke of all your nights and weekends spent writing your custom implant.

## Protection from scanners with Gargoyle

Enter [Gargoyle](https://lospino.so/security/assembly/c/cpp/developing/software/2017/03/04/gargoyle-memory-analysis-evasion.html). This dusty technique (2017 - a millenia in malware years) introduced the concept of protection cycling (from R-X to RW- and back again) to evade memory scanners that only spend their precious CPU cycles inspecting executable memory regions. No encryption yet, but the next few techniques we will discuss all build on the same protection-cycling introduced by Gargoyle.

Gargoyle uses `SetWaitableTimer` which takes (among other things) the callback function pointer (to the stack pivot below), `lpArgToCompletionRoutine` ( [“a pointer to a struct that is passed to the completion routine”](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-setwaitabletimer)), and `lPeriod` (how often the the timer is signaled).

`lpArgToCompletionRoutine` is set to point to an attacker-crafted ‘stack’-like struct on-heap, the callback function is set to:

```
mshtml!gadget:
  pop ecx
  pop esp ; stack pivot to attacker-controlled "stack" in `lpArgToCompletionRoutine`
  ret
```

This carefully selected gadget pops the `lpArgToCompletionRoutine` pointer into `esp`. The “stack” looks something like this:

```
 Offset  Bytes (DWORDs)               Role at runtime
 ──────  ─────────────────────────    ─────────────────────────────────────────
 +0x00   &VirtualProtectEx            ← ret target #1 (jump into VPE)
 +0x04   &payload_entry               ← VPE's "return address" → jumps into payload
 +0x08   GetCurrentProcess() (= -1)   ← VPE arg1: hProcess
 +0x0C   &payload_page                ← VPE arg2: lpAddress
 +0x10   payload_size (e.g. 0x1000)   ← VPE arg3: dwSize
 +0x14   PAGE_EXECUTE_READ  (= 0x20)  ← VPE arg4: flNewProtect
 +0x18   &Workspace.old_protect       ← VPE arg5: lpflOldProtect
 +0x1C   <slot for next "ret">        ← payload's "return address" → next stage
 +0x20   &Workspace.config            ← payload arg1 (whatever the payload needs)
```

At this point it should be clear: Gargoyles original ROP based technique only works for x86 `__stdcall` wherby all arguments are passed on the stack. The later ‘refreshed’ version of Gargoyle and other similar techniques switch from a ROP-based approach to using `NtContinue` with crafted `CONTEXT` structures which allow setting registers directly. Generaly more flexible, though as we’ll see `CONTEXT` structs in memory will be leveraged by defenders for detection…

## NtContinue-ing the journey with Ekko and Foliage

This big happy family of techniques all share the same core idea: use a system primitive (timer callback, APC, thread context) to drive a chain of `NtContinue` calls with carefully crafted `CONTEXT` structs that cycle the implant’s `.text` between `RX` and `RW`, encrypt/decrypt the code in-place, and sleep in between.

As this is a retrospective, some history: this usage of timers for queueing ‘NtContinue’ calls was first done in the closed source [NightHawk](https://www.mdsec.co.uk/) implant, and [written up by Austin Hudson](https://web.archive.org/web/20220505170100/https://suspicious.actor/2022/05/05/mdsec-nighthawk-study.html). Austin released the first public implementation attempt [Foliage](https://github.com/y11en/FOLIAGE), later superseeded by [C5pider’s Ekko](https://github.com/Cracked5pider/Ekko).

### Ekko

We’ll start with Ekko since its actualy the simpler to understand of the two. Ekko works by creating seven `CONTEXT` structs on the stack. Without too much detail, `CONTEXT` structs basicaly hold the entire CPU state (registers, flags, etc.) in a structand can be ‘activated’ with `NtContinue` to jump to arbitrary code with an arbitrary register state. Ekko uses timer-queue callbacks to execute the time-ordered NtContinue calls with a set of crafted `CONTEXT` structs.

To do this correctly, Ekko first runs a timer-queue callback set to run `RtlCaptureContext` (not `NtContinue`). This captures the timer-queue-worker’s thread `CONTEXT`, which is subsequently copied 6 times and modified to point ESP at the appropriate functions (VirtProtect, SysFunc032, WaitForSingleObjectEx, etc).

When those contexts are all created, the main ekko thread carefully sets up timers with staggered times pointing `NtContinue` at the appropriate `CONTEXT` struct for each stage of the sleep chain. The implant thread is parked the whole time, and the ephemeral timer-worker threads are the ones actually executing the callbacks and riding the chain. The last callback in the chain sets an event that wakes up the main implant thread, which can then do whatever evil stuff you have tasked for it before going back to sleep.

The chain of calls after the contexts are created looks like this:

1. `VirtualProtect(.text, RW)`
2. `SystemFunction032(.text, key)` (RC4 in-place encrypt)
3. `WaitForSingleObjectEx(hEvent, sleep_ms, TRUE)`
4. `VirtualProtect(.text, RW)`
5. `SystemFunction032(.text, key)` (RC4 in-place decrypt)
6. `SetEvent(hEvent)` (wake up the main implant thread)

In a sentence: encrypt the code, sleep, decrypt the code, wake up. Rinse and repeat.

### Foliage

Foliage is a bit more complex, but the core idea is the same: use `NtContinue` with crafted `CONTEXT` structs to drive the same protection-cycling + encrypt/sleep/decrypt pattern. The main difference is that instead of using timer-queue callbacks to execute the `NtContinue` calls, Foliage uses a helper thread with queued APCs calling `NtContinue`, the neat trick here is that the `NtContinue` calls are chained together by configuring the call to `ret` to `NtTestAlert` which is a syscall that will immediately run any APCs queued to the thread. This allows chaining the CONTEXTs together with APCs, instead of timers like Ekko.

Step-by-step, Foliage does the following:

1. Create a suspended helper thread
2. Create a synchro event for the helper thread to wait on between stages of the sleep chain.
3. Capture the yet-suspended helper thread’s `CONTEXT` and create 6 modified copies for each stage of the sleep chain (similar to Ekko)
4. Build 9 CONTEXTs:

```
  - `NtWaitForSingleObjectEx` (Synchro event)
  - `NtProtectVirtualMemory` (`.text` to RW)
  - `NtDeviceIoControlFile` (call `KsecDD` driver's `IOCTL_KSEC_ENCRYPT_MEMORY` to encrypt `.text` in-place)
  - `NtGetContextThread` (capture main thread context to heap)
  - `NtSetContextThread` (set main thread context to something spoofed for stack evasion)
  - `NtDelayExecution` (sleep)
  - `NtDeviceIoControlFile` (call `KsecDD` driver's `IOLCT_KSEC_DECRYPT_MEMORY` to decrypt `.text` in-place)
  - `NtSetContextThread` (restore main thread context to real one for wake)
  - `NtProtectVirtualMemory` (`.text` to RX)
  - `ExitThread` (helper thread cleanup)
```

For each CONTEXT, the `RSP` is set to `NtTestAlert` which is a syscall that will immediately run any APCs queued to the thread. This allows chaining the CONTEXTs together with APCs, instead of timers like Ekko.
5\. For each CONTEXT, queue an APC to the helper thread for ‘NtContinue(&CONTEXT)’. The APCs are queued in the order of the sleep chain, but they won’t execute until the helper thread is running and alertable.
6\. Resume the helper thread. It wakes up, executes the first APC which calls `NtWaitForSingleObjectEx` on the synchro event, and goes to sleep.
7\. The main thread now calls `NtSignalAndWaitForSingleObject` alerting the Synchro event and waiting on the helper thread handle. The event signal wakes up the helper thread and allows it to execute the next APC in the chain. The main thread is now waiting on the thread handle. Notice the CONTEXT chain, when the final APC executes the helper thread commits seppuku and the main thread is woken up.

Thats the full flow. A bit dense of an explanation but summarized as best I could. Its worth noting that I personaly was not aware of the use of `KsecDD` IOCTLs for in-place encryption before doing this deep dive on Foliage, and I think its a pretty clever way to get the encrypt/decrypt done without the commonly abused SystemFunction032/3 or userland crypto APIs.

Also of note, the original Ekko poc does not do any stack spoofing via `NtSetContext` or otherwise, the Havoc implementation of Ekko does leverage the `NtSetContextThread` approach to get the main thread’s context into a fake one for stack evasion during sleep, as well as replacing the TIB stack bounds with the helper thread’s to defeat RSP/TEB checks.

## Variations on the same idea

- [DeathSleep](https://github.com/janoglezcampos/DeathSleep) — All this worry about callstack spoofing the main thread, why not just kill it? DeathSleep captures the current main thread `CONTEXT`, calculates and copies the live part of the stack, queues thread-pool workers to do the sleep-encryption and start a new ‘resurrection’ thread, then calls `ExitThread`. After all the sleep-stuff, the resurection timer creates a fresh thread whose entrypoint restores the saved stack, fixes the saved `Rsp` to the new stack location, and uses `NtContinue` to resume at the instruction after `DeathSleep()`. Neat trick, with a trade-off: the sleeping thread really dies, so thread create/exit telemetry becomes part of the signature.
- [Cronos](https://github.com/Idov31/Cronos) — APCs with timers. Replaces Ekko’s timer-queue callbacks with waitable timers that queue APC routines. A dummy waitable timer first runs `RtlCaptureContext` inside the APC delivery path; Cronos clones that valid callback-thread context into four staged contexts: `VirtualProtect(RW)`, `SystemFunction032` encrypt, `SystemFunction032` decrypt, `VirtualProtect(RWX)`. Those timers are scheduled at `0`, `1`, `sleepTime - 1`, and `sleepTime`, then the implant has to enter an alertable wait for the APCs to run. Cronos uses a small stack-helper stub that sets up the stack such as to shepherd the main thread through four SleepEx(infinite) calls - every time an APC completes the main thread wakes, returns to some pre-defined ROP gadget which goes back to the SleepEx(infinite) call exactly the right amount of times, finaly returning `.text` after final APC runs. Because cronos is using timers for queing the APCs, Foliage’s `RSP->NtTestAlert` would not work for it as the next APCs in the chain may not have been queued by the timers yet. Worth reading the [writeup](https://idov31.github.io/posts/cronos-sleep-obfuscation) if interested.

## The userland cat-and-mouse: callstack hunting and the spoofing arms race

### What defenders started looking at

Once Ekko/Foliage/Cronos became the de-facto pattern, the defenders did what defenders do: they looked at what made these techniques visible and stand out from the crowd of normal process threads. It turns out a sleeping beacon, even one that has carefully encrypted its `.text`, can leave a lot of evidence in its memory and thread state. A whole generation of open-source scanners spun up around this - [Hunt-Sleeping-Beacons](https://github.com/thefLink/Hunt-Sleeping-Beacons), [BeaconHunter](https://www.mdsec.co.uk/2022/07/part-1-how-i-met-your-beacon-overview/), [Moneta](https://www.forrest-orr.net/post/masking-malicious-memory-artifacts-part-ii-insights-from-moneta), [Patriot](https://github.com/joe-desimone/patriot), [pe-sieve](https://github.com/hasherezade/pe-sieve) \- each one targeting a slightly different detective surface.

Heres a quick rundown of no-no’s for your sleeping implant malwarez:

- **`KiUserApcDispatcher` on the stack** sitting underneath a blocking call like `NtWaitForSingleObject` or `NtDelayExecution` is a dead giveaway for an APC-driven sleep mask. That’s Cronos, that’s Foliage, that’s anything that queues an APC to drive the chain. Legitimate code rarely sits in a blocking syscall with an APC frame below it.
- **`RtlpTpTimerCallback` on the stack** is the same idea for the timer-queue variant - that’s Ekko’s fingerprint. The OS itself put that frame there, and you can’t easily make it not be there.
- **Timer queue enumeration** is even more direct. `NtQueryInformationWorkerFactory` lets a scanner walk `FULL_TP_POOL.TimerQueue` and inspect every `PFULL_TP_TIMER` in the process. Any callback pointing at `NtContinue` or `VirtualProtect` is a detection opportunity.
- **In-memory `CONTEXT` scanning**: To feed `NtContinue` for the ROP chain, Ekko / Foliage / Cronos all pre-build `CONTEXT` structs (typically on the stack or heap) where `Rip` is set to `VirtualProtect` / `NtProtectVirtualMemory`. Joe Desimone’s [Patriot](https://github.com/joe-desimone/patriot) just scans memory for these structures and flags the sus ones. Defeating it means either not pre-building CONTEXTs (move to a different sleep primitive entirely) or somehow obfuscating/unobfuscating them in place during the sleep chain, both of which complicate the design considerably.
- **Unbacked-memory return addresses** \- if a frame on the stack points back into a `MEM_PRIVATE` page that isn’t backed by any loaded module, that’s your reflectively-loaded implant’s own `.text` (or some other private executable allocation) waving hello. Real code returns into module-backed memory.
- **RSP outside TEB stack bounds** \- every thread’s TEB records the legitimate stack range. If the thread’s current `RSP` is outside that range, somebody is up to something (typically, somebody pivoted to a fake stack and forgot to update the bounds).
- **Shallow ROP-style stacks** \- a legitimate sleeping thread has a deep chain of frames from `BaseThreadInitThunk` down through whatever wait function it’s parked in. A naive ROP-driven sleep often produces 2-3 frames total.
- **Obviously cloned thread contexts** \- when Foliage (or anything Foliage-shaped) copies a helper thread’s `CONTEXT` to spoof the main thread’s stack, you end up with two threads claiming the same TIB Stack Base / Stack Limit. Trivial to spot if you enumerate threads.
- **DeathSleep-specific** \- terminating and re-creating the implant thread on every sleep cycle generates a steady stream of thread-create/thread-exit events that any kernel callback (`PsSetCreateThreadNotifyRoutine`) will pick up. Pretty easy to detect based on repititive thread birth/death.

### Quick tangent for stack/frame spoofing

So defenders can read your sleeping thread’s stack. The obvious counter is: don’t let them read a stack that incriminates you. This is a whole sub-rabbit-hole of its own with a long lineage, but the through-line for our purposes is short.

Worth a quick distinction first: stack spoofing historicaly comes in two flavors. **Active** spoofing happens _during_ your hooked syscalls — you doctor the return address right before calling `Nt*` so the call-site looks like it came from `kernelbase` instead of your reflective DLL. **Passive** (or sleep-time) spoofing is what we care about here — you spoof the _parked_ stack while the implant is asleep, so a scanner walking it sees nothing interesting. Most modern sleep masks do both; the techniques below are the passive variants.

The lineage starts with [Namazso’s 2018 trick](https://www.unknowncheats.me/forum/anti-cheat-bypass/268039-x64-return-address-spoofing-source-explanation.html) for anti-cheat bypass: stash your real return address in `rbx`, push the address of a `jmp [rbx]` gadget living in a legit signed DLL, and let the called function `ret` into the gadget which then bounces you home. To a stack walker, the topmost frame points at signed code instead of your unbacked memory. One frame of cover - simple and effective for a single hop. Basic ROP.

[Kyle Avery’s AceLdr](https://github.com/kyleavery/AceLdr) (DEF CON 30) was the first (that I’m aware) to wire this directly into a Cobalt Strike user-defined-reflective-loader, including the sleep loop. The topmost frame of a sleeping AceLdr beacon no longer points at unbacked memory - it points at a `jmp [rbx]` gadget in `ntdll`. [WithSecure’s CallStackSpoofer (a.k.a. VulcanRaven)](https://github.com/WithSecureLabs/CallStackSpoofer) extended the idea from one frame to a multi-frame chain using a different approach: precomputed call stacks installed onto a target thread via `GetThreadContext` / `SetThreadContext` / `CreateThread`.

[klezVirus’s SilentMoonwalk](https://github.com/klezVirus/SilentMoonwalk) is the next iteration of that idea, and the one I recently went down a rabbit hole on (maybe we’ll dive into that in another post…) TLDR; instead of precomputing a stack, you build one dynamically that the Windows unwinder will follow on its own. The trick is that `RtlVirtualUnwind` is a _static_ unwinder - it reads `UNWIND_INFO` records out of `.pdata` and chases them. So if you carefully select four frames from `kernelbase` whose `UNWIND_INFO` mechanically fits together (F₁ does `UWOP_SET_FPREG`, F₂ does `UWOP_PUSH_NONVOL(RBP)`, F₃ contains a `JMP [RBX]` desync gadget, F₄ is an `ADD RSP, X; RET` conceal/pivot), the unwinder follows the breadcrumbs and reports a clean stack of `kernelbase!*` frames. The CPU never executed those functions - the `JMP [RBX]` in F₃ diverts real execution to your restore routine, while the static unwinder just _thinks_ the frames were there.

[Moonwalk++](https://klezvirus.github.io/posts/Moonwalk-plus-plus/) takes this further by exploiting a structural property of the moonwalk layout: every stack frame sitting between `BaseThreadInitThunk` and F₁ is _invisible_ to the reconstructed call stack. Anything you put in there is hidden from anyone walking from the top down. M++ uses that concealed region to stash a full ROP chain (`R_D`) that decrypts the shellcode in-place. Moonwalk++ and SilentMoonwalk are complicated, and I don’t intend to fully explain them in gory details here in this post. You can and should read the source and accompanying posts from klezVirus if you want to understand the full mechanics.

### The ticking clock - CET

Stack spoofing on the parked thread isn’t free anymore either. Specifically, the most common pattern - capture a random spoof thread’s full `CONTEXT` via `GetThreadContext`, slap it onto the sleeping main thread via `SetThreadContext` breaks on any modern target with Intel CET Shadow Stack enabled. That means Windows 11 22H2+ on Intel 12th-gen+ or AMD Zen 3+. The process image must be compiled with CET support, and on windows HVCI must be enabled. This is pretty rare today but its coming…

Why it breaks: with CET, the kernel routine [`KiVerifyContextIpForUserCet`](https://github.com/yardenshafir/cet-research/blob/master/src/KiVerifyContextIpForUserCet.c) runs on every `NtSetContextThread` call and iterates the target thread’s shadow stack looking for the new `Rip`. The spoof thread’s `Rip` was pushed onto _its own_ shadow stack by a `call` in _its_ execution - not the sleeping thread’s. So when the kernel walks the sleeping thread’s shadow stack looking for it, it isn’t there, and the syscall returns `STATUS_SET_CONTEXT_DENIED`. Your implant sleeps with its real, unspoofed call stack hanging out for any scanner to walk.

One apparent caveat: Windows supports a `UserCetSetContextIpValidationRelaxedMode` process mitigation flag that lets older binaries without an `EH_CONTINUATION_TABLE` skip this check entirely for compatibility - see Yarden Shafir’s writeups: [R.I.P ROP](https://windows-internals.com/cet-on-windows/) and [CET on Xanax](https://windows-internals.com/cet-updates-cet-on-xanax/). Anything new enough to actually matter is strict, though. These research posts are quite old and I have not personally validated the claims against modern CET behavior.

## What killed the whole family — ETW Threat Intelligence (the kernel ceiling)

Bad news. Everything we’ve covered so far - the timer dispatch, the APC chains, the stack spoofing - is _userland_ engineering. And every single one of these techniques calls `NtProtectVirtualMemory` to cycle the implant’s `.text` between `RX` and `RW` (and sometimes `NOACCESS` in between). That syscall is what gets you killed on a modern endpoint, and it doesn’t matter how clean your call stack looks while you’re doing it.

The mechanism is the `Microsoft-Windows-Threat-Intelligence` (ETW-Ti) provider — Microsoft doesn’t publish docs for it (it’s only consumable by anti-malware-PPL processes) but the [official manifest dump](https://github.com/jdu2600/Windows10EtwEvents/blob/master/manifest/Microsoft-Windows-Threat-Intelligence.tsv) by @jdu2600 spells out every event. It’s a kernel-mode ETW provider that fires `KERNEL_THREATINT_TASK_PROTECTVM` events from _inside_ the `NtProtectVirtualMemory` syscall implementation - meaning by the time the event fires, you’re already executing in `nt!NtProtectVirtualMemory` in ring 0. Each event carries:

- the new protection mask
- the previous protection mask
- the target VAD type (`IMAGE`, `MAPPED`, `PRIVATE`)
- the base address of the affected region
- a **kernel-captured** call stack from the kernel-side call site

Defender (and any antimalware-signed sensor with provider access) consumes these events and scores patterns. The scoring is heuristic but the pattern that lights it up is well understood:

> `RX → RW → NOACCESS|READONLY → RW → RX` on the same `BaseAddress`, on an `IMAGE` VAD, repeated on a periodic schedule, with call-stack origin inside the same `.text` range → high-confidence sleep mask.

The IOC is the _shape_, not the specific values. Substituting `READONLY` for `NOACCESS` doesn’t help. Removing the middle protection change doesn’t help. Stretching the period out doesn’t help once you’ve done enough cycles to be visible. The kernel sees a chunk of IMAGE-backed memory whose protections are oscillating in a pattern that has no legitimate use case, and you get killed within seconds. This is **Image-VAD protection cycliing**.

The only method I know of to evade this is to not call `NtProtectVirtualMemory` at all. You can do that with dual-section mapping (`MEM_MAPPED`, `SEC_COMMIT`) or by setting up RWX permissions at load and never touching them again. Dual-section mapping does not work for IMAGE VADs, so thats kind of a non-starter. MockingJay style writable image sections seem like the only path forward here. If you at home reading this have got this far (congrats!) and have any other ideas, please let me know. I’m also always on the hunt for signed ‘mockingjay’ DLLs with fat sections for… you know, science.

If you want to read more on the kernel side of this, the best public references is John Uhlmann’s [BlackHat Asia 2023 talk](https://i.blackhat.com/Asia-23/AS-23-Uhlmann-You-Can-Run-But-You-Cant-Hide.pdf) and the accompanying PoC ETW consumer, [EtwTi-FluctuationMonitor](https://github.com/jdu2600/EtwTi-FluctuationMonitor).

## Where this leaves us

Every public technique is DoA out of the box - thats to be expected. There are evasive combinations of the techniques above that may still be viable depending on your EDR of choice, but the bar is pretty high. The major comonality of tech here is the CONTEXT structures and those can be carved out from memory and inspected if your process has drawn the ire of the sensor (See Patriot). The trick seems to be to limit your exposure to scanning in the first place - the less you look like a sleeping beacon, the less likely you are to be scanned for. So I guess ‘act normal’ is the best advice I can give you… for now ;)

Cheers. Ping me if I screwed something up in any of the above or if you have any cool ideas for new techniques or defenses. Always happy to chat about this stuff.

## Resources

**Sleep masks**

- [Ekko — C5pider](https://github.com/Cracked5pider/Ekko)
- [Foliage — SecIdiot](https://github.com/y11en/FOLIAGE)
- [Cronos — Idov31](https://github.com/Idov31/Cronos)
- [DeathSleep — janoglezcampos](https://github.com/janoglezcampos/DeathSleep)
- [Adaptix StealthPalace (Ekko v2 + Kraken Mask) — Maor Sabag](https://github.com/MaorSabag/Adaptix-StealthPalace)

**Stack spoofing**

- [Namazso 2018 return-address spoofing](https://www.unknowncheats.me/forum/anti-cheat-bypass/268039-x64-return-address-spoofing-source-explanation.html)
- [AceLdr — Kyle Avery](https://github.com/kyleavery/AceLdr)
- [VulcanRaven — WithSecure](https://github.com/WithSecureLabs/CallStackSpoofer)
- [SilentMoonwalk — klezVirus](https://github.com/klezVirus/SilentMoonwalk)
- [Moonwalk++ post](https://klezvirus.github.io/posts/Moonwalk-plus-plus/)
- [Sleeping Beauty II — CFG + CET + TIB-swap (Maor Sabag)](https://maorsabag.github.io/posts/adaptix-stealthpalace/sleeping-beauty-ii/)

**Detection side**

- [MDSec — How I Met Your Beacon](https://www.mdsec.co.uk/2022/07/part-1-how-i-met-your-beacon-overview/)
- [BH Asia 2023 — John Uhlmann](https://i.blackhat.com/Asia-23/AS-23-Uhlmann-You-Can-Run-But-You-Cant-Hide.pdf)
- [Forrest Orr — Moneta](https://www.forrest-orr.net/post/masking-malicious-memory-artifacts-part-ii-insights-from-moneta)
- [PoolParty — Alon Leviev / SafeBreach](https://www.safebreach.com/blog/process-injection-using-windows-thread-pools)
- [Fibratus — thread-pool telemetry](https://fibratus.io/blog/thread-pool-telemetry-sleeping-beacon-detection)
- [Binary Defense — Understanding Sleep Obfuscation](https://binarydefense.com/resources/blog/understanding-sleep-obfuscation/)
- [Hunt-Sleeping-Beacons — thefLink](https://github.com/thefLink/Hunt-Sleeping-Beacons)