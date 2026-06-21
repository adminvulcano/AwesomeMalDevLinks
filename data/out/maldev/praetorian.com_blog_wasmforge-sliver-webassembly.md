# https://www.praetorian.com/blog/wasmforge-sliver-webassembly/

[Skip to content](https://www.praetorian.com/blog/wasmforge-sliver-webassembly/#content)

- [AI Offensive Security](https://www.praetorian.com/category/ai-security/ai-offensive-security/), [Labs](https://www.praetorian.com/category/labs/), [Offensive Security](https://www.praetorian.com/category/offensive-security/)

# Enter the WasmForge: Compiling Sliver into WebAssembly

- [Michael Weber](https://www.praetorian.com/author/michael-weber/)
- [June 4, 2026](https://www.praetorian.com/blog/2026/06/04/)

![](https://www.praetorian.com/wp-content/uploads/2026/06/Part-2-Enter-the-WasmForge-blog-hero-1.webp)

In [our last post](https://www.praetorian.com/blog/llm-edr-signature-reduction/) we used a Claude skill to systematically beat down VirusTotal detection rates on offensive security tools, with a brief mention of a new loader we’d been using to apply those techniques in bulk. This post is about that loader, which we call WasmForge.

WasmForge is, from the user’s perspective, a build wrapper. You point it at a Go project and you get back a Windows or macOS binary that runs your tool but doesn’t look anything like it. Internally it’s a lot more. It’s a Go-to-WebAssembly compiler, a custom [Wazero](https://github.com/tetratelabs/wazero) fork, around eighty host shim functions for MacOS and Windows APIs, and a healthy amount of evasion techniques from our previously discussed skill. The whole pipeline exists to solve one specific problem: take an existing offensive security tool, change **_zero lines_** of its source code, and produce a binary you can actually drop on a hardened endpoint.

# The Tool Authors Won, Then The Tool Authors Lost

Many red team engagements can be completed using the same handful of established tools. [Sliver](https://github.com/bishopfox/sliver) for C2 traffic that’s been hardened by years of community work. [Chisel](https://github.com/jpillora/chisel) for the umpteenth time someone wants an HTTP-tunneled SOCKS proxy. A [Mythic](https://github.com/its-a-feature/mythic) beacon when the engagement scope or detection model rules out Sliver. None of these tools are exotic.

The trouble, of course, is that every one of these tools has been signatured to hell and back. Every major Endpoint Detection and Response (EDR) vendor has a YARA rule with the project name in its title, sometimes literally. By the time you’re ready to drop your tool on the endpoint, you’ve already already lost the static-analysis battle before you can run the binary.

This leads to the same set of frustrating options. Fork the source and start renaming things. Piece together some evasion tips scattered across a few disparate blogs. Rewrite the tool from scratch. Wrap the tool in a custom loader you’ve then got to maintain forever (as crazy as it sounds, we prefer this option). The state of the practice is essentially “spend a few days hardening a known-good tool before every engagement.” Security practitioners can do better.

We wanted a loader that handled this part for us, and we wanted it to be aggressively **_transparent_** – you should not have to touch the tool’s source, you should not have to know how the loader works internally, and the resulting binary should be opsec-safe enough to drop into a real engagement without further modification.

## Why WebAssembly, Of All Things

WebAssembly is not the first thing that comes to mind when you’re hiding malware. It’s a language of the modern web with **wasm32** modules running in browser sandboxes, mostly compiled from Rust, Go, or C++ via well-known toolchains. It is **_NOT_** normally expected to be running a full implant. That last property is an interesting one from our perspective.

There are two reasons WASM ended up being the right substrate.

The first reason is precedent. We’ve had a lot of success in the past hiding malicious behavior inside WebAssembly running in browser extensions (see [ChromeAlone](https://github.com/praetorian-inc/chromealone) for the long version of that argument). Defensive tooling for WASM analysis is significantly less developed than for native PE analysis. Most static analyzers know how to chew on a Go **gopclntab** but very few of them know what to do with a 30,000 instruction WASM module that’s been compiled from the same Go source. The instruction set is unfamiliar, the type system is unfamiliar, and the binary format is unfamiliar enough that most heuristic engines just give up and make their decision entirely based on the outer container.

![](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201024%20368'%3E%3C/svg%3E)**I love this image too much not to re-use it**

The second reason is portability. We wanted to write the loader once and target Windows and macOS from it. WebAssembly’s whole pitch is “compile once, run anywhere,” with a relatively well-defined system interface ( [WASI](https://wasi.dev/)) bridging the gap between the WASM module and the host. WASI Preview 1 isn’t a complete substitute for native syscalls, but it’s a really useful starting point. **fd\_read**, **fd\_write**, **path\_open**, **clock\_time\_get**, and other functions you’d need for any basic program. The pieces that **_aren’t_** covered by WASI (like network sockets that work, raw sockets, Win32 APIs, or macOS frameworks) are exactly what we have to bridge ourselves, and nobody expects WASM to be able to do that.

The combination of “defenders’ analysis tooling is weaker here” and “we can target both major OSes from one source” was enough to commit. The tradeoffs of binary size, a **_weird_** debug experience, and having to implement a runtime were considered acceptable in a world where we can use LLMs to prompt our way to success.

# Architecture

WasmForge has three stages. The first prepares a patched copy of the Go standard library that compiles cleanly for the **wasip1** target. The second runs the Go compiler against that patched **stdlib** to produce a **.wasm** module. The third generates an outer Go binary containing a [Wazero](https://github.com/wazero/wazero) runtime, embeds the encrypted WASM module into the binary’s PE sections, and applies “polymorphism” (quotes intentional as it’s largely just a lot of automatic renaming) and signing passes we’ll get to in a minute.

![](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201024%20544'%3E%3C/svg%3E)**The rough flow for building a WasmForge’d binary**

The transparency property comes out of the first two stages. The patched GOROOT handles all the parts of Go’s standard library that don’t natively work under WASI like **net.Dial**, **net.Listen**, **net/http**, **os/exec**, **os.Pipe**, and friends by inserting **//go:wasmimport** shims that delegate the actual work to host functions. From the guest’s perspective, **net.Dial(“tcp”, “10.1.2.3:443”)** looks like it works the same way it does on any other platform. The guest binary doesn’t know it’s running in WebAssembly, which is the entire point.

The third stage is where most of our opsec engineering lives. This is where we got to spend time using the [skill from our previous blog post](https://github.com/praetorian-inc/reduce-golang-detections-skill). We’ll come back to it after we talk about how the guest side actually executes.

## The Guest Side: WASI, Wazero, and a Lot of Shims

WASI Preview 1 doesn’t get you very far on its own. It gets you a couple dozen syscall analogues that look enough like Linux to be useful and stop well short of being useful enough. There are no real sockets. There is no **LoadLibrary**. There is no **mach\_vm\_write**. The whole point of an offensive security tool is in the part WASI doesn’t ship.

Wazero is the embeddable Go WASM runtime we use as the engine. It’s pure Go (no CGO), it supports defining your own host module with arbitrary function imports, and it gives us enough control over execution to actually do the things we need. We forked it because we needed to make changes the upstream maintainers reasonably don’t want, like randomizing the WASM opcode table per build, renaming a lot of internal package paths, and swapping out the cache magic bytes. Fundamentally though, at the runtime level it’s an unmodified Wazero from the guest’s perspective.

The interesting work is in the host module. WasmForge defines an **env** namespace with roughly eighty host functions: socket lifecycle ( **sock\_open, sock\_bind, sock\_connect, sock\_read**), **os** proxies ( **os\_hostname**, **os\_exec**, **os\_pipe**), Win32 wrappers ( **win32\_load\_library**, **win32\_get\_proc\_address**, **win32\_syscalln**, **win32\_create\_process**, the registry quartet, along with several dozen others), and macOS framework calls ( **fw\_load**, **fw\_sym**, **fw\_call**). Almost every one of these is a thin wrapper that converts WASM linear-memory pointers into real host addresses, calls into Go’s **syscall** or **x/sys/windows** package, and writes results back into the guest’s memory.

Walking through a single call **net.Dial(“tcp”, “10.1.2.3:443”)** from the guest, a call looks like this:

![](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20942%201024'%3E%3C/svg%3E)**We need to jump through several hoops to let the guest program run without requiring logic changes**

Every other host function, all eighty-odd of them, follow the same shape. Pointer arguments get translated to invoke the host, who does the real work, and then the return values get written back into the guest’s linear memory at known offsets.

That pointer-translation step sounds innocuous and is in fact the most load-bearing piece of code in the whole project. WASM linear memory is, from the guest’s perspective, a contiguous byte array starting at offset zero. WASM pointers are 32-bit offsets into that array. Pass one of those offsets directly to a Win32 API and you get an access violation in about half a millisecond. **0x2a39b3a** is not a valid kernel-mode address, no matter how good your call looks otherwise. Before every host-side syscall we walk the argument list and apply a simple range heuristic: anything ≥ **0x10000** but less than the WASM module’s allocated memory size is **_probably_** a linear-memory pointer, and gets rewritten to its host equivalent ( **wasmMemBase + offset**). The **0x10000** floor exists to distinguish real pointers from small scalar values that the guest sometimes passes in pointer-shaped positions, like flag bitmasks, small handles, or nil. After the call returns, we sometimes have to do the reverse: COM interfaces and several Win32 APIs write **host** pointers back into the **guest’s** output parameter, which the guest then expects to dereference. We mirror those host pointers into WASM memory, with a small reverse-lookup table tracking which mirrored copy corresponds to which host original, and patch the output buffer to point at the mirror instead.

The range heuristic catches most cases but isn’t perfect on its own. Plenty of Win32 APIs take parameters that the function signature types as **PVOID** but at runtime are actually larger handles, session IDs, or kernel objects that **happen** to fall inside the WASM-pointer range by coincidence, and translating those by mistake produces some entertaining crashes. For those, we lean on a per-API pointer-mask table generated at build time from [win32json](https://github.com/marlersoft/win32json), Andy Marler’s JSON serialization of Microsoft’s own [win32metadata](https://github.com/microsoft/win32metadata). This is the same machine-readable Win32 API surface that [CsWin32](https://github.com/microsoft/cswin32) and Rust’s **windows-sys** use to know which parameter is which. We have a small **gen-ptrmasks** codegen step that walks every API entry in the metadata and emits a bitmask saying “arg\[0\] is a real pointer, arg\[1\] is a handle, arg\[2\] is a size\_t,” and the host shim consults that mask before deciding which arguments to translate. The metadata covers something like 80,000 API entry points across kernel32, advapi32, user32, ntdll, and the rest, which means we get exact pointer semantics essentially for free across the entire Windows API surface the guest can touch. The handful of cases where the metadata is **_wrong_**, most notably the cross-process memory APIs where a **PointerTo(Void)** is actually a remote-process address, not a local one, are dealt with via a few hand-curated overrides. While you would expect that the mask table would be sufficient to handle this problem entirely, we’ve found that it’s necessary to use the mask table in conjunction with the heuristic to get the most stable output from WasmForge.

This is enough to make most APIs work. COM is the API that taught us the most about where the model breaks. **CLRCreateInstance** returns an **ICLRMetaHost** pointer in an output parameter. The guest reads that pointer, jumps through it to get a vtable, reads function pointers out of the vtable, calls them, and expects them to do the right thing. Every one of those pointers like the interface, the vtable, and the methods themselves live in host memory. Mirroring just the top-level pointer doesn’t work, we have to mirror the vtable too, and we have to recognize that vtable entries are **_function_** pointers that live in **MEM\_IMAGE** regions (i.e., the DLLs themselves), which we **do not** want to copy into linear memory because the guest can’t execute them anyway. The right behavior, which is to mirror data while leaving executable pointers as opaque tokens and recursively follow non-image pointers one level deeper, turned out to be about a week of small bugs and a few “helpful” **0xc0000005s** before it converged. Many tokens were burned running down a “good enough” solution for this issue.

Note that not all APIs are supported with this approach. In the current version there’s no support for callback thunks, so calls to functions like **EnumWindows** or **SetWindowsHookEx** are unsupported for now. In practice this appears to be less of a limitation that one would expect since there are often alternate APIs we can use to perform the same enumeration without dealing with the host calling a function in the guest memory directly.

## Hide and Seek with Several Hundred Function Names

By the time we have a working WASM module embedded inside a Go binary that runs Wazero, we’re maybe sixty percent of the way to a usable loader. The remaining forty percent is making sure the **outer** binary, the Go executable that hosts the runtime, doesn’t itself look like a piece of obvious malware.

We identified three important changes here.

**Randomized WASM virtual machines on every compile.** Wazero, like most WASM runtimes, has an internal table mapping WASM opcodes to runtime behavior. We [Fisher-Yates](https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle) that table at build time. Every compiled binary has a different mapping from opcode bytes to instructions, and we rewrite the embedded WASM module to match. The result is that two binaries built five minutes apart from the same source contain the **_same_** WASM payload structurally, but with completely different byte representations. No two WasmForge binaries have the same WASM bytecode, which makes signaturing the payload at a static level genuinely hard. Analysts will have to derive the mapping by analyzing the host layer or else none of their tooling to analyze the WASM blob will work at all.

We do the same thing to the WASM section IDs and to the magic header bytes. There’s no **\\0asm** header in a WasmForge-built binary, just a random four-byte sequence specific to that build, and the runtime knows which one to look for because we encoded that into its initialization data at compile time.

![](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201024%20489'%3E%3C/svg%3E)**A diagram illustrating the difference between a standard WASM build and WasmForge build**

**Ghost profiles**. This is what we walked through in the [previous post](https://www.praetorian.com/blog/llm-edr-signature-reduction/). The short version: a vanilla Go binary’s **gopclntab** is mostly empty space and runtime symbols, which looks suspicious to ML classifiers expecting real software’s symbol density. We harvest symbol tables from real Go projects (consul, caddy, terraform, and others) and splice them into the host binary so the **gopclntab** looks like the **gopclntab** of a real signed enterprise tool. The skill from the previous post is what we used to figure out which profiles actually moved the detection numbers and which ones didn’t.

**Randomized DLL imports, signing identity, and PE metadata.** Since our base host binary only uses kernel32, its base import list looks suspicious. The host binary needs to import enough Windows DLLs to look plausible (a binary that only links kernel32 is its own red flag) but not so many that ML notices a “kitchen sink” pattern. We rotate a small pool of plausible imports like crypt32, iphlpapi, advapi32, and others between builds. We do something similar with the PE VERSIONINFO product and file-version strings which cycle through a curated pool of legitimate-sounding enterprise software names. The Authenticode signing pipeline picks a random certificate identity per build from a pool of plausible signers, with random subject/issuer/description/URL strings. This is the exact fix that killed the AhnLab **Trojan/Win.Sliver** rule cold in the previous post.

None of these are individually clever. The clever part is the measurement loop. Each of these knobs has a “natural” setting that you’d guess at, and an “empirically correct” setting that using VT as an adversarial oracle eventually narrows you down to. The skill from the previous post is how we got from the first to the second on every one of these.

# But Does It Actually Work?

As most readers will have guessed, this entire project was built with heavy LLM assistance. A tool with this much surface area ranging across the three-stage build pipeline, ~80 host functions, custom Wazero fork, mirror table, shadow memory, and the whole macOS/Windows split would normally take several months of dedicated engineering effort. Ours took a few weeks of work. Most of the boring bridging code (the eightieth Win32 wrapper, the fourth darwin framework helper, the umpteenth socket-options translator) was written by Claude under fairly close supervision.

Two validation questions mattered:

1\. **Does it actually compile real Go projects without modification?**

2\. **Do those compiled binaries actually work at runtime?**

We have a test suite for the basics. Echo TCP servers, UDP, HTTP clients, DNS resolution, Win32 registry round-trips, and macOS framework loading. These run in our continuous integration and catch most regressions. They’re not, however, representative of the load you put on a runtime when you point it at a real red team tool. Real red team tools do things like spin up 30 goroutines that block on **WaitForSingleObject** while a parent goroutine runs a separate HTTP server while a third goroutine waits on a named pipe. Our synthetic tests didn’t tend to catch these interesting edge cases.

So the best validation was running real tooling through it. The list, in roughly the order we tried them:

**Sliver**– We tested beacon and session implants for both Windows and macOS. Full beacon to session upgrade, file I/O, process listing, token manipulation, SOCKS5 proxying, **execute-assembly** against Seatbelt and Rubeus, BOF loading via **goffloader**. We tested against [Game of Active Directory](https://github.com/Orange-Cyberdefense/GOAD) labs to confirm that things like Kerberos extraction actually worked end to end.

**Tribunus** – A custom internal Mythic implant we’ve written for Windows. We tested standard commands like **shell, ps, netstat, whoami**.

**gogokatz** – An internal (for now) Go port of mimikatz we wrote for exactly this kind of workflow. This lets us try to execute full LSASS memory dumps without special privileges beyond what the real mimikatz needs.

**Chisel** – We used this for testing HTTP-tunneled SOCKS. It was a nice bandwidth/jitter stress test for the socket bridge.

**goffloader** – We used this for explicit COFF/BOF loading. Eight-phase test exercising VirtualAlloc, memory writes, PE parsing, relocations, IAT resolution, execution, output capture, and cleanup.

The first time we got Sliver fully running through WasmForge on a real Windows endpoint was the moment we decided the project was worth shipping. Watching **execute-assembly Rubeus.exe kerberoast** complete successfully against a domain controller, through a WASM-bridged COM call into the CLR running a loaded Rubeus assembly, was significantly more rewarding and hilarious than it had any right to be.

The macOS side took separate validation. Sliver on Darwin uses a different code path than Sliver on Windows (no token manipulation, different syscall conventions, completely different framework loading), and our darwin host module is structurally similar to the Windows one but ends up being much smaller because there’s no shadow memory, no mirror table, and no COM. We’ve validated the same beacon-then-session flow on macOS, including SOCKS5 proxying and full TLS networking with automatic CA cert detection.

The resulting binaries from this process have been used on engagements against hardened clients, on both Windows and macOS targets, without modification of the underlying tool source. Which is the whole reason WasmForge exists.

You can see a full ASCIInema run through of the compilation process and testing here:

![](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201192%20901'%3E%3C/svg%3E)**WasmForge in action. Note that labctl is**

**just a helper function to run binaries in our lab.**

# What’s Next

The thing about a WebAssembly-based loader is that “compiles to WebAssembly” is a much bigger tent than “is written in Go.” Anything with a WASM compilation target gets to live inside the same runtime once the host shims exist. We’ve been doing increasingly serious work on the .NET side, specifically using the NativeAOT-LLVM toolchain with WASI SDK, to compile [GhostPack](https://github.com/GhostPack)-style C# tooling like Seatbelt, Rubeus, and SharpDPAPI into WASM that our same loader can host.

That work is far enough along that the next post is going to be about it specifically. We will simultaneously open-source WasmForge along the final blogpost in this series describing the C#-to-WASM build pipeline. Watch this space, the tool is dropping soon and we’re excited to get it into the hands of the security community.

## About the Authors

![Michael Weber](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%200%200'%3E%3C/svg%3E)

### [Michael Weber](https://www.praetorian.com/author/michael-weber/)

Michael has worked in security as a malware reverse engineer, penetration tester, and offensive security developer for over a decade.

## Catch the Latest

Catch our latest exploits, news, articles, and events.

- [Offensive Security](https://www.praetorian.com/category/offensive-security/), [Vulnerability Research](https://www.praetorian.com/category/vulnerability-research/)

- June 19, 2026

## [GhostPack Necromancy: Reforging C\# Tools with WasmForge](https://www.praetorian.com/blog/wasmforge-csharp-ghostpack-edr-evasion/)

[Read More](https://www.praetorian.com/blog/wasmforge-csharp-ghostpack-edr-evasion/)

- [Offensive Security](https://www.praetorian.com/category/offensive-security/), [Vulnerability Research](https://www.praetorian.com/category/vulnerability-research/)

- June 17, 2026

## [FreeBSoD: Leveraging Language Models to Find and Exploit Kernel Bugs (Part 1 of 2)](https://www.praetorian.com/blog/ai-vulnerability-research-freebsd-kernel/)

[Read More](https://www.praetorian.com/blog/ai-vulnerability-research-freebsd-kernel/)

- [Uncategorized](https://www.praetorian.com/category/uncategorized/)

- June 16, 2026

## [Sharing is Caring: SMB Secret Scanning with Sulla](https://www.praetorian.com/blog/sharing-is-caring-smb-secret-scanning-with-sulla/)

[Read More](https://www.praetorian.com/blog/sharing-is-caring-smb-secret-scanning-with-sulla/)

## Ready to Discuss Your Next Continuous Threat Exposure Management Initiative?

Praetorian’s Offense Security Experts are Ready to Answer Your Questions

[Get Started](https://www.praetorian.com/contact-us/)