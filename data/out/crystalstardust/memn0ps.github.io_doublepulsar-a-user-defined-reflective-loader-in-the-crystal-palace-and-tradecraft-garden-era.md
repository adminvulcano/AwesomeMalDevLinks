# https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/

# [DoublePulsar: A User-Defined Reflective Loader in the Crystal Palace and Tradecraft Garden Era](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/)

2026-04-1444 min read (9320 words)

# [doublepulsar](https://memn0ps.github.io/tags/doublepulsar/)
# [user-defined-reflective-loader](https://memn0ps.github.io/tags/user-defined-reflective-loader/)
# [udrl](https://memn0ps.github.io/tags/udrl/)
# [cobalt-strike](https://memn0ps.github.io/tags/cobalt-strike/)
# [crystal-palace](https://memn0ps.github.io/tags/crystal-palace/)
# [crystal-kit](https://memn0ps.github.io/tags/crystal-kit/)
# [tradecraft-garden](https://memn0ps.github.io/tags/tradecraft-garden/)
# [shellcode-reflective-dll-injection](https://memn0ps.github.io/tags/shellcode-reflective-dll-injection/)
# [srdi](https://memn0ps.github.io/tags/srdi/)
# [shellcode](https://memn0ps.github.io/tags/shellcode/)
# [loader](https://memn0ps.github.io/tags/loader/)
# [rust](https://memn0ps.github.io/tags/rust/)
# [position-independent-code](https://memn0ps.github.io/tags/position-independent-code/)
# [pic](https://memn0ps.github.io/tags/pic/)
# [injection](https://memn0ps.github.io/tags/injection/)

**Disclaimer:** This post is a technical walkthrough of DoublePulsar, an open source User-Defined Reflective Loader I built and maintain on my personal GitHub. None of the techniques discussed are novel, they have been publicly known and documented by the security research community for many years, and credit is given throughout to the researchers and projects that developed them. The post is not an evaluation, comparison, or critique of any endpoint security product or commercial C2 framework, and it does not reverse engineer proprietary software. All debugger output, memory dumps, call stacks, and static analysis shown in this post are of the DoublePulsar UDRL itself. Beacon is treated as an opaque encrypted payload throughout and is never inspected, disassembled, or reverse engineered. References to specific products, detection rules, or research are included to credit existing public work, not to rank vendors or imply any product is insufficient. The goal is to shed light on these techniques and raise security awareness equally for everyone, offensive tool builders and defensive detection engineers alike.

## Summary [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#summary)

Adversaries and red teams load their tools directly into a computer’s memory without writing files to disk, making them invisible to traditional file-based security products. The component that controls this in-memory loading is called a reflective loader. Cobalt Strike, one of the most widely used adversary simulation frameworks, allows operators to replace its default loader with a custom one called a User-Defined Reflective Loader (UDRL), giving them full control over how the implant loads and hides in memory.

DoublePulsar is a UDRL written in Rust that adds multiple layers of concealment: it hides the implant inside a legitimate system module’s memory, encrypts it while idle, fakes its call history to look like normal system activity, and isolates its memory allocations from the rest of the process. For defenders, signature-based detection alone is not enough. This post provides detection strategies, YARA rules, and a MITRE ATT&CK mapping to help security teams identify this class of threat.

## Background and Context [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#background-and-context)

Reflective DLL Injection, first published by Stephen Fewer in 2008, introduced a technique for loading a DLL entirely in memory without using the Windows loader. The key innovation was compiling the loading logic directly into the DLL itself as an exported function called `ReflectiveLoader()`. A small shellcode stub in the DOS header directed execution to this export, which then allocated memory, mapped PE sections, resolved imports, applied relocations, and called the entry point. This made the DLL self-loading and position-independent.

In 2017, Nick Landers released Shellcode Reflective DLL Injection (sRDI), which took the concept further by separating the loader from the DLL entirely. Instead of embedding the loader as an export, sRDI prepended position-independent loader shellcode before the target DLL. This allowed any arbitrary DLL to be converted into injectable shellcode without modifying the DLL itself. The same year, an analysis of the DoublePulsar user-mode injector, an implant developed by the NSA’s [Equation Group](https://en.wikipedia.org/wiki/Equation_Group) and leaked by the [Shadow Brokers](https://en.wikipedia.org/wiki/DoublePulsar), revealed a similar prepended loader architecture. DoublePulsar takes its name from this implant.

Cobalt Strike adopted reflective loading early and later introduced the User-Defined Reflective Loader (UDRL) API in version 4.4 (2021) to give operators full control over how Beacon loads into memory. The UDRL replaces Cobalt Strike’s default `ReflectiveLoader()` with operator-supplied code, either embedded inside the Beacon DLL or prepended in front of it. Robert Bearsby’s [Revisiting the UDRL](https://www.cobaltstrike.com/blog/revisiting-the-udrl-part-1-simplifying-development) blog series documents both approaches and provides the UDRL-VS development kit.

![Prepended vs Embedded Reflective Loader](https://memn0ps.github.io/DoublePulsar-A-User-Defined-Reflective-Loader-in-the-Crystal-Palace-and-Tradecraft-Garden-Era/figure1_prepended_vs_embedded_loader.png)

**Figure 1:** _Prepended vs embedded reflective loader architecture (diagram from [Revisiting the UDRL Part 1](https://www.cobaltstrike.com/blog/revisiting-the-udrl-part-1-simplifying-development) by Robert Bearsby / Cobalt Strike)_

The value of a custom UDRL over the default Cobalt Strike loader is control. Without one, the default reflective loader creates a fresh memory allocation using whatever settings are in the Malleable C2 profile, potentially undoing any evasion work the shellcode runner did to get the payload into memory in the first place. This “nesting doll” problem is what pushes most operators toward writing custom UDRLs. The default loader’s behavior is well documented, signatured, and detectable. A UDRL controls memory allocation strategy, section permissions, import resolution, and can inject evasion primitives at every stage of the loading pipeline. Public UDRLs like [TitanLdr](https://github.com/benheise/TitanLdr) by Austin Hudson, [AceLdr](https://github.com/kyleavery/AceLdr/) by Kyle Avery, and [BokuLoader](https://github.com/boku7/BokuLoader) by Bobby Cooke demonstrated that operators could build loaders with module stomping, return address spoofing, heap isolation, and sleep obfuscation. The IBM X-Force [analysis of reflective loaders](https://www.ibm.com/think/x-force/defining-cobalt-strike-reflective-loader) covers the foundational concepts. Lorenzo Meacci’s [EDR evasion research](https://lorenzomeacci.com/bypassing-edr-in-a-crystal-clear-way) built on [Crystal Palace](https://tradecraftgarden.org/crystalpalace.html) and RastaMouse’s [Crystal-Kit](https://github.com/rasta-mouse/Crystal-Kit) demonstrated advanced techniques including module overloading with `.pdata` registration, `NtContinue` entry transfer, and sleep masking. Crystal Kit hooks `BEACON_RDLL_GENERATE` (making it a UDRL) and uses PICOs (Position-Independent Code Objects) to run evasion tradecraft alongside the loader, with support for post-exploitation DLL loading via `POSTEX_RDLL_GENERATE`.

### Crystal Palace, Tradecraft Garden, and the UDRL [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#crystal-palace-tradecraft-garden-and-the-udrl)

The most recent development in Cobalt Strike’s loading ecosystem is [Crystal Palace](https://tradecraftgarden.org/crystalpalace.html), an open source PIC linker and linker script language maintained by Raphael Mudge. The [Tradecraft Garden](https://tradecraftgarden.org/) provides example loaders and a shared library (`libtcg`) for DLL loading, PICO running, and debug output. RastaMouse’s [Crystal-Kit](https://github.com/rasta-mouse/Crystal-Kit) packages these into a ready-to-use Cobalt Strike evasion kit.

The architecture is quite different from traditional UDRLs like TitanLdr, AceLdr, and DoublePulsar. Traditional UDRLs are compiled to a PE, have their `.text` section extracted as raw shellcode via `objcopy`, and handle everything in one monolithic binary: PE loading, import resolution, relocations, hooking, and evasion. Crystal Palace takes a modular approach. Operators write C source files that compile to COFF object files (`.o`), not DLLs. Crystal Palace then links these objects together via specification files (`.spec`) that control how components are combined, what functions are resolved, and what hooks are installed. The `MODULE$Function` pattern (e.g., `KERNEL32$VirtualAlloc`) handles dynamic function resolution at link time, so operators never need to write PEB walking or hash-based API resolution code. Crystal Palace also provides link-time optimizations (`+optimize`), code mutations (`+mutate`), and function reordering (`+disco`).

The key architectural concept is the PICO (Position-Independent Code Object). A PICO is Crystal Palace’s convention for running COFF objects in memory, similar to a BOF but without the Beacon-specific API. In Crystal Kit, the evasion tradecraft (IAT hooking, call stack spoofing, sleep masking) lives in a PICO that runs alongside the loader rather than being embedded in it. The loader loads the Beacon DLL and the PICO, calls the PICO’s setup functions (e.g., `setup_hooks`, `setup_memory`), and the PICO patches Beacon’s imports at load time via the `addhook` directive in the spec file. This separation means operators can swap evasion components without rewriting the loader itself.

Crystal Palace lowers the barrier to PIC development. Operators who previously needed to understand linker scripts, section ordering, PIC string handling, and manual API resolution can now focus on writing C code and let Crystal Palace handle the position-independence constraints. The shared `libtcg` library provides DLL loading and import resolution out of the box. This accessibility has made it the most popular approach for new Cobalt Strike loader development.

However, the evasion capability depends on what the operator builds with it. Crystal Kit, as shipped, allocates Beacon memory via `VirtualAlloc` (producing unbacked private memory), uses XOR-based sleep masking with a 128-byte key, and resolves APIs through kernel32 (`LoadLibraryA`/`GetProcAddress`). These are effective starting points, though operators can build more advanced tradecraft on top of Crystal Palace as Lorenzo Meacci demonstrated.

Crystal Palace does not prevent operators from writing advanced evasion. Lorenzo Meacci’s work demonstrated that module overloading, `.pdata` registration for stack unwinding, and `NtContinue` entry transfer are achievable within the Crystal Palace framework. However, these techniques are not part of the public Crystal Kit release. Crystal Palace as a linker can support them, they just require significant additional development beyond what ships out of the box.

A purpose-built UDRL like DoublePulsar takes the monolithic approach: everything is compiled into a single position-independent binary that handles PE loading, import resolution, relocations, module stomping, NtContinue-based sleep obfuscation, heap isolation, CFG bypass, and synthetic call stack construction from `.pdata` unwind information. The tradeoff is development effort: Crystal Kit gets an operator running quickly with modular components, while a monolithic UDRL requires writing and maintaining all of it.

There is also a third approach worth considering: frameworks like [Havoc Professional](https://infinitycurve.org/products/havoc-professional) where the C2 framework itself handles evasion through a modular extension system, removing the loader development burden from the operator entirely. More on this below.

### Choosing Between a UDRL and Crystal Kit [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#choosing-between-a-udrl-and-crystal-kit)

Both a purpose-built UDRL and Crystal Kit achieve the same end result: Beacon loaded into memory with evasion tradecraft applied. Neither approach is inherently superior. They solve the same problem with different tradeoffs, and the right choice depends on who is building it, how much time they have, and what level of control they need.

|  | Purpose-Built UDRL | Crystal Kit / Crystal Palace |
| --- | --- | --- |
| **Architecture** | Monolithic. Everything in one binary: loader, hooks, sleep, spoofing | Modular. Loader + separate PICOs for tradecraft, linked via spec files |
| **Compilation** | Compiled to a PE, `.text` section extracted as shellcode via `objcopy` | C source compiled to COFF `.o` files, linked by Crystal Palace |
| **API Resolution** | Manual PEB walking, DJB2/ROR13 hash resolution written by the developer | Handled by Crystal Palace via `MODULE$Function` DFR pattern and `libtcg` |
| **PE Loading** | Developer writes or adapts: `ParseDLL`, `LoadDLL`, `ProcessImports`, relocations | Provided by `libtcg` shared library out of the box |
| **Evasion Tradecraft** | Built directly into the loader binary | Lives in a separate PICO, loaded alongside the loader |
| **Swapping Techniques** | Change source code, recompile | Swap PICO in spec file, relink without touching the loader |
| **Link-Time Features** | Bring your own. Compile-time obfuscation (opaque predicates, control-flow flattening), custom VM-based obfuscators, or any toolchain the operator controls | `+optimize` (dead code removal), `+mutate` (code mutations), `+disco` (function reordering), provided by Crystal Palace |
| **Toolchain** | Rust/C compiler + linker script + objcopy | MinGW GCC + Crystal Palace JAR (Java) + spec files |
| **Post-Ex Loader** | Write a separate loader or reuse the same one | `POSTEX_RDLL_GENERATE` hook with shared PICO tradecraft |
| **Learning Curve** | High. Must understand PIC constraints, PE format, Windows internals | Lower. Crystal Palace abstracts PIC constraints, `libtcg` handles PE loading |
| **Control** | Total. Every byte is yours | Partial. Crystal Palace controls linking, DFR, and code layout |
| **Detection Response** | Patch the exact code path, recompile, done | May need to modify PICO, loader, or spec file depending on what was detected |
| **Team Scalability** | Difficult. The person who wrote it is the person who maintains it | Good. Senior dev builds loader, junior operators swap PICOs per engagement |

**A purpose-built UDRL is the right fit if:**

- You are a solo operator or small team with deep Windows internals knowledge
- You need full control over every aspect of the loading process, from memory allocation strategy to exact API call sequences
- You want to respond to new detection rules quickly by patching the exact code path that was flagged, without waiting for upstream tooling updates
- You are building private tooling that extends beyond loading (custom sleep chains, custom call stack spoofing, heap isolation strategies that are specific to your operational needs)
- You do not want to depend on an external toolchain (Crystal Palace is a Java application) or someone else’s linking conventions
- You are comfortable writing and maintaining PIC code, manual API resolution, PE parsing, and relocation processing

**Crystal Kit and Crystal Palace are the right fit if:**

- You are part of a team with varying skill levels and need operators to deploy evasion tradecraft without understanding PIC internals
- You are time-boxed on an engagement and need a working loader quickly without writing PE loading and import resolution from scratch
- You want to experiment with different evasion techniques by swapping PICOs (hooks, sleep masking, call stack spoofing) without rewriting the loader
- You want link-time optimizations (`+optimize` removes unused code, `+mutate` provides polymorphism, `+disco` randomizes function order) without implementing them yourself
- You need both a Beacon loader (`BEACON_RDLL_GENERATE`) and a post-exploitation loader (`POSTEX_RDLL_GENERATE`) that share the same tradecraft components
- You want to use the Tradecraft Garden’s example loaders as a starting point rather than building from scratch
- You are more comfortable writing C than dealing with the constraints of PIC shellcode development (no `.data` section, no string literals, no CRT)

**The tradeoff in practice:** Crystal Kit gets an operator running in hours with modular components. A purpose-built UDRL takes weeks or months to build but gives the developer total ownership of the code. When a new detection rule drops (like Elastic’s call stack pattern rule that appeared the same month as DoublePulsar), the UDRL developer can patch the specific gadget source, the specific frame layout, or the specific byte pattern in their own code and recompile. The Crystal Kit operator may need to wait for an upstream PICO update or write a new PICO themselves, which requires the same PIC development skills the framework was supposed to abstract away.

Both produce working, evasive loaders. The choice is about who you are and what you need.

Integrated frameworks like [Havoc Professional](https://infinitycurve.org/products/havoc-professional) represent a third path: the C2 developer handles evasion at the framework level, reducing the need for operators to build or maintain a separate loader. This addresses the operational reality that consultancies are time-boxed, C2 licenses are expensive, and writing a custom loader on top of an already expensive framework is additional R&D that not every team can afford. This does not eliminate all custom work, operators may still need to handle specific scenarios, but it removes the loader development burden from the operator entirely.

DoublePulsar is written entirely in Rust, making it among the first public proof-of-concept UDRLs written in Rust with this level of evasion capability. The same techniques and primitives apply regardless of language. PIC development in Rust is less commonly documented and remains rare in public offensive tooling, but the barrier is one of familiarity, not capability.

DoublePulsar uses the prepended loader architecture. The Aggressor CNA script (`Titan.cna`) takes the compiled loader shellcode, RC4-encrypts the Beacon with a random key, and appends the encrypted payload after the loader code. At runtime, the loader decrypts the Beacon and maps it into memory.

## DoublePulsar Architecture [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#doublepulsar-architecture)

The loader executes as a linear pipeline: assembly bootstrap, thread creation, Beacon decryption, module stomping, PE mapping, and Beacon execution.

![DoublePulsar Loader Pipeline](https://memn0ps.github.io/DoublePulsar-A-User-Defined-Reflective-Loader-in-the-Crystal-Palace-and-Tradecraft-Garden-Era/figure2_loader_pipeline.png)

**Figure 2:** _DoublePulsar loader pipeline overview_

**Entry and Bootstrap.** The assembly entry point in `start.asm` (section `.text$A`) aligns the stack, allocates shadow space, and transfers control to Rust. This bootstrap pattern is similar to [Stardust](https://github.com/Cracked5pider/Stardust) by C5pider:

```asm
Start:
    push   rsi
    mov    rsi, rsp
    and    rsp, 0FFFFFFFFFFFFFFF0h    ; align stack to 16 bytes
    sub    rsp, 020h                  ; shadow space
    call   Entry                      ; transfer to Rust
    mov    rsp, rsi
    pop    rsi
    ret
```

A custom linker script, similar to the approach used in [TitanLdr](https://github.com/benheise/TitanLdr) and [AceLdr](https://github.com/kyleavery/AceLdr/), merges everything into a single `.text` section in a specific order. This is what makes the entire binary position-independent, everything lives in `.text` and `objcopy` extracts it as raw shellcode:

```
SECTIONS
{
    .text :
    {
        *( .text$A );    /* Assembly entry (Start) */
        *( .text$B );    /* Rust loader code (Entry, ace, loader) */
        *( .text$C );    /* STUB metadata structure */
        *( .text$D );    /* IAT hooks, sleep obfuscation */
        *( .text$E );    /* Utilities, crypto, API wrappers */
        *( .rdata* );    /* Read-only data */
        *( .data* );     /* Mutable data */
        KEEP( *(.text$ZZ) );  /* GetIp marker (end of loader) */
    }

    /DISCARD/ : { *(.pdata); *(.xdata); *(.debug*); }
}
```

Position-independent address calculation relies on two assembly helpers in `misc.asm`. `GetIp()` uses the classic call/pop/sub-5 pattern to return the current instruction pointer, and `StubAddr()` uses RIP-relative addressing to return the runtime address of the STUB metadata:

```asm
[SECTION .text$ZZ]
GetIp:
    call    get_ret_ptr
get_ret_ptr:
    pop    rax
    sub    rax, 5
    ret

[SECTION .text$C]
StubAddr:
    lea    rax, [rel Stub]
    ret
```

The Rust `OFFSET()` macro combines these to convert any compile-time symbol address to its runtime equivalent without relocations.

**Thread Creation via ACE.** The `ace()` function creates a suspended thread, hijacks its RIP to point at the `loader()` function, and resumes it. This approach is based on [AceLdr](https://github.com/kyleavery/AceLdr/):

```rust
let addr = (api.ntdll.RtlUserThreadStart_ptr as *mut u8).offset(0x21);
let start_address: PUSER_THREAD_START_ROUTINE = transmute(addr);

api.ntdll.RtlCreateUserThread(
    -1isize as HANDLE, null_mut(), suspended,
    0, 0, 0, start_address, null_mut(), thread, null_mut(),
);

let mut ctx: CONTEXT = core::mem::zeroed();
ctx.ContextFlags = CONTEXT_CONTROL;
api.ntdll.NtGetContextThread(thread, &mut ctx);

ctx.Rip = loader as *const () as u64;
api.ntdll.NtSetContextThread(thread, &mut ctx);
api.ntdll.NtResumeThread(thread, null_mut());

api.kernel32.WaitForSingleObject(thread, 0xFFFFFFFF);
```

This isolates the loader’s execution context from the original thread and produces a clean call stack. `NtSetContextThread` on a suspended thread is heavily monitored by EDR products like Microsoft Defender for Endpoint and CrowdStrike, as this pattern is primarily associated with debuggers and process injection. This is a known tradeoff.

**CNA Script and CONFIG Layout.** The `Titan.cna` script, adapted from [titanldr-ng](https://github.com/klezVirus/titanldr-ng)’s CNA integration, runs inside the Cobalt Strike client. When Beacon shellcode is generated, the script generates a random 16-character ASCII string as the RC4 key, encrypts the Beacon payload, and constructs a CONFIG structure: a 4-byte big-endian length field followed by the 16-byte key, followed by the encrypted Beacon. This CONFIG is appended directly after the loader code at the address returned by `G_END()`.

**Loader Pipeline.** The `loader()` function handles the full loading sequence, following a similar approach to [TitanLdr](https://github.com/benheise/TitanLdr) and [AceLdr](https://github.com/kyleavery/AceLdr/). The first stage extracts the CONFIG structure appended by the CNA script, which contains the Beacon size (big-endian) and 16-byte RC4 key, then allocates a temporary RW buffer for decryption:

```rust
let cfg = G_END() as *const Config;
let beacon_size = u32::from_be_bytes((*cfg).rc4_len) as SIZE_T;
let key_ptr = (*cfg).key_buf.as_ptr();
let encrypted_beacon = (cfg as usize + core::mem::size_of::<Config>()) as *const u8;

let mut dec_buffer: PVOID = null_mut();
let mut alloc_size = beacon_size;

api.ntdll.NtAllocateVirtualMemory(
    -1isize as HANDLE, &mut dec_buffer, 0,
    &mut alloc_size, MEM_COMMIT, PAGE_READWRITE,
);
```

The encrypted Beacon is RC4-decrypted into the temporary buffer, and the PE headers are parsed to calculate the memory layout (stub size + Beacon image size, both aligned to 4KB):

```rust
crate::crypto::decrypt_beacon(key_ptr, encrypted_beacon, dec_buffer as *mut u8, beacon_size);

reg.dos = dec_buffer as *mut IMAGE_DOS_HEADER;
reg.nt = (dec_buffer as usize + (*reg.dos).e_lfanew as usize) as *mut IMAGE_NT_HEADERS;

calculate_regions(&mut reg);
```

Next, a sacrificial DLL is loaded for module stomping. The DLL is `d3d10.dll` by default (changeable in source to any DLL with a `.text` section large enough to fit the Beacon). `DONT_RESOLVE_DLL_REFERENCES` maps it without executing `DllMain` or resolving imports:

```rust
let module_base = api.kernel32.LoadLibraryExA(
    b"d3d10.dll\0".as_ptr() as LPCSTR,
    null_mut(),
    DONT_RESOLVE_DLL_REFERENCES,
);
```

The loader verifies the Beacon fits within the stomped module’s `.text` section, changes the region to RW, and copies the STUB metadata and loader code into it:

```rust
if reg.full > text_size {
    return;
}

api.ntdll.NtProtectVirtualMemory(
    -1isize as HANDLE, &mut memory_buffer,
    &mut reg.full, PAGE_READWRITE, &mut old_protection,
);

copy_stub(memory_buffer as _);
```

Each Beacon PE section is then mapped to its virtual address offset inside the stomped region:

```rust
let map = copy_beacon_sections(memory_buffer, &reg);
```

An isolated heap is created for all Beacon allocations. This heap is separate from the process default heap, which is what makes heap isolation and per-heap encryption possible during sleep:

```rust
let beacon_heap = api.ntdll.RtlCreateHeap(
    HEAP_GROWABLE, null_mut(), 0, 0, null_mut(), null_mut(),
);
```

The STUB metadata is filled with runtime state (region bounds, heap handle, section info) and the resolved `Api` struct is copied into inline storage within the STUB region. From this point on, hooks access `Api` through the STUB rather than the stack:

```rust
fill_stub(memory_buffer, beacon_heap, &mut reg, &api);

let api = &mut *(*(memory_buffer as PSTUB)).api;
```

Import resolution and base relocations follow standard manual PE mapping. These are well-documented techniques, so the implementation is not covered in detail here:

```rust
resolve_imports(api, map as _, import_dir_addr);
rebase_image(map as _, reloc_dir_addr, image_base);
```

What makes DoublePulsar’s loading stage different is the IAT hooking that happens after import resolution. Over 30 IAT entries are patched to redirect Beacon’s API calls through hook functions inside the stomped module, giving the loader control over Beacon’s runtime behavior (heap isolation, sleep obfuscation, call stack spoofing, network call handling). The hook set is fully customizable, adding or removing a hook is a single `hook_iat()` call with the target function’s DJB2 hash:

```rust
install_hooks(map, memory_buffer, reg.nt);
```

The stub region is set to RX and per-section permissions are applied based on each section’s characteristics flags:

```rust
api.ntdll.NtProtectVirtualMemory(
    -1isize as HANDLE, &mut stub_base,
    &mut stub_size, PAGE_EXECUTE_READ, &mut stub_old_prot,
);

fix_section_permissions(api, memory_buffer, &reg);
```

The temporary decrypt buffer is zeroed and freed so the decrypted Beacon is not left in memory:

```rust
memzero(dec_buffer as *mut u8, beacon_size as u32);
api.ntdll.NtFreeVirtualMemory(
    -1isize as HANDLE, &mut dec_buffer, &mut free_size, MEM_RELEASE,
);
```

Note that DoublePulsar does not call `NtFlushInstructionCache` before executing the entry point. Standard practice after modifying executable memory is to flush the instruction cache to ensure stale cached instructions are not executed, though in practice this is rarely an issue on x64 where the instruction cache is coherent with data writes.

Execution then transfers to Beacon’s entry point, called twice following AceLdr’s convention: first with `DLL_PROCESS_ATTACH` to initialize Beacon, then with reason code `0x4` (which starts Beacon’s main loop and never returns) passing the loader’s base address. Note that `stage.cleanup` has known limitations with module stomping and may not free the loader properly in this configuration:

```rust
let Ent: DLLMAIN = core::mem::transmute(entry);

Ent(OFFSET(Start as *const () as usize) as *mut c_void, 1, core::ptr::null_mut());
Ent(OFFSET(Start as *const () as usize) as *mut c_void, 4, core::ptr::null_mut());
```

The entire loader compiles to approximately 65KB of position-independent shellcode extracted from the `.text` section via `objcopy --dump-section`.

**Debug Output.** With debug logging enabled, the full loader sequence looks like this at runtime:

```
[ACE] Started
[ACE] RtlUserThreadStart+0x21: 00007FFE3F32AA71
[ACE] RtlCreateUserThread: 0
[ACE] Thread created: 00000000000001EC
[ACE] RIP -> loader: 00007FFDA5B15CB0
[ACE] Thread resumed, waiting
[LDR] Started
[LDR] Allocated RW buffer: 0000025F47F60000
[LDR] Beacon decrypted
[LDR] DOS header: 0000025F47F60000
[LDR] reg.full: 0000000000067000, reg.exec: 0000000000010000
[LDR] Stomp target: 00007FFDBE7E1000
[LDR] Changed to RW
[LDR] Stub copied
[LDR] Beacon sections copied: 00007FFDBE7F1000
[LDR] Heap created: 0000025F48180000
[LDR] Stub filled (Api embedded in STUB)
[LDR] Imports resolved
[LDR] Hooks installed
[LDR] Relocations applied
[LDR] Stub set to RX
[LDR:FIX_PERM] buffer: 00007FFDBE7E1000, exec: 0000000000010000, sections: 5
[LDR:FIX_PERM] [0] base: 00007FFDBE7F2000, prot: 4 -> 20
[LDR:FIX_PERM] [1] base: 00007FFDBE822000, prot: 4 -> 2
[LDR:FIX_PERM] [2] base: 00007FFDBE832000, prot: 4 -> 4
[LDR:FIX_PERM] [3] base: 00007FFDBE844000, prot: 4 -> 2
[LDR:FIX_PERM] [4] base: 00007FFDBE847000, prot: 4 -> 2
[LDR] Section permissions set
[LDR] Entry RVA: 0000000000020F6C
[LDR] Temp buffer freed
[LDR] Executing DllMain
[HOOK:Sleep] ms: 5000
[HOOK:Sleep] ms: 5000
[HOOK:Sleep] ms: 60000
[EKKO] ekko: enter
[COMMON] frame sizes resolved
[COMMON] jmp_rbx gadget found
[EKKO] context captured
[EKKO] scheduling 10 timer callbacks
[EKKO] signaling chain start, waiting for completion
[EKKO] chain complete, cleaning up
[EKKO] ekko done
```

Addresses, thread IDs, and module base addresses shown in the debug output above and in the figures that follow vary across runs due to ASLR. Not every figure in this post was captured in the same debugging session, so values will not align across every figure.

## Evasion Techniques Deep Dive [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#evasion-techniques-deep-dive)

This section walks through each evasion technique, why it exists, and how defenders can catch it.

### Module Stomping [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#module-stomping)

**Detection vector.** Memory scanners flag unbacked executable memory, regions marked `MEM_PRIVATE` with `PAGE_EXECUTE_READ` or `PAGE_EXECUTE_READWRITE` that are not associated with any file on disk. This is the most reliable indicator of reflective injection.

**Implementation.** DoublePulsar loads a sacrificial DLL (`d3d10.dll` by default, changeable in source) using `LoadLibraryExA` with the `DONT_RESOLVE_DLL_REFERENCES` flag, which maps the DLL into memory without executing its `DllMain` or resolving its imports. The loader parses the module’s PE headers to find the `.text` section, verifies the Beacon fits within it, changes the section permissions to `PAGE_READWRITE` via `NtProtectVirtualMemory`, copies the STUB metadata and loader code first (`copy_stub`), then copies each Beacon PE section to its virtual address offset (`copy_beacon_sections`). After mapping, per-section protections are restored: `.text` gets `PAGE_EXECUTE_READ`, `.rdata` gets `PAGE_READONLY`, `.data` gets `PAGE_READWRITE`.

All region sizes are aligned to 4KB page boundaries, and the total is verified to fit within the target module’s `.text` section before any writes occur.

The System Informer memory view below shows the stomped `d3d10.dll` module’s regions. During sleep, the `.text` section is flipped to RW and encrypted. When awake, it returns to RX with per-section permissions restored:

![Module Stomp - Sleep RW](https://memn0ps.github.io/DoublePulsar-A-User-Defined-Reflective-Loader-in-the-Crystal-Palace-and-Tradecraft-Garden-Era/figure3_module_stomp_sleep_rw.png)![Module Stomp - Awake RX](https://memn0ps.github.io/DoublePulsar-A-User-Defined-Reflective-Loader-in-the-Crystal-Palace-and-Tradecraft-Garden-Era/figure3_module_stomp_awake_rx.png)

**Figure 3:** _d3d10.dll memory regions during sleep (RW, encrypted) vs awake (RX, executable)_

Module stomping is preferred over call stack spoofing as the primary defense against memory scanners. Module stomping makes the memory itself backed by a legitimate module on disk (`MEM_IMAGE`), so scanners checking memory type will see a known DLL rather than suspicious private executable memory (`MEM_PRIVATE`). Call stack spoofing only fakes the thread’s call stack but does not change the memory backing, the executable region is still private and unbacked. Module stomping addresses the root cause while call stack spoofing addresses a symptom. Module stomping is also simpler and more stable operationally since it does not depend on ROP gadget availability or `.pdata` parsing. If done correctly, calling APIs from within a backed module means the return addresses on the call stack already point into a legitimate DLL, making call stack spoofing unnecessary in many cases. DoublePulsar enables both by default as defense in depth.

The shellcode loader or injector that delivers the UDRL can also module stomp the UDRL itself into a legitimate module’s memory space before the UDRL executes. This creates a two-layer stomping chain: the injector stomps the UDRL into one backed module, and the UDRL then stomps the Beacon into another. Both the loader and the Beacon end up residing in memory backed by legitimate modules on disk. When combined with DLL side-loading from a signed executable, this becomes particularly effective. If the signed executable is trusted by Windows Defender Application Control (WDAC) or AppLocker, the initial execution is permitted by policy, and both the UDRL and the Beacon occupy backed memory from that point forward.

When Beacon’s code lives inside a legitimate module’s address range, memory scanners see backed memory associated with a known DLL on disk. The default choice of `d3d10.dll` as the sacrificial module is deliberate: it is a Microsoft-signed DLL with a large `.text` section, commonly present on Windows systems with DirectX support. The target module can be changed in the source to any DLL with a `.text` section large enough to hold the loader and Beacon. A more operationally robust approach would be to randomly select from several candidate DLLs at runtime, reducing the predictability of which module gets stomped across deployments.

The same region is visible from a debugger. Attaching WinDbg to the beacon process mid-sleep:

![WinDbg Stomp and Sleep](https://memn0ps.github.io/DoublePulsar-A-User-Defined-Reflective-Loader-in-the-Crystal-Palace-and-Tradecraft-Garden-Era/figure4_stomp_and_sleep.png)

**Figure 4:** _WinDbg mid-sleep. `!address` shows `MEM_IMAGE` backed by `d3d10.dll` but currently `PAGE_READWRITE`, the NtContinue chain has flipped it for RC4 encryption._

**Detection.** Tools like PE-sieve and Moneta can compare in-memory module content against the on-disk original, detecting section hash mismatches. The stomped module’s `.text` section will not match its disk counterpart. Even with module stomping, the overwritten pages become private (copy-on-write), so scanners that check working set entries for private pages within a module’s address range can still detect the stomping regardless of whether the memory appears backed. More advanced implementations can back up the original module content before stomping, [restore it during sleep by temporarily relocating the implant, and re-stomp on wake](https://dtsec.us/2023-11-04-ModuleStompin/), limiting content-comparison detection to the awake window only. A module loaded with `DONT_RESOLVE_DLL_REFERENCES` leaves anomalous flags in its `LDR_DATA_TABLE_ENTRY` in the PEB (such as `DontCallForThreads` and other condition flags that differ from a normally loaded DLL), its imports will not be resolved, and its entry point will not be set. These are observable IoCs that defensive tools can check. A more advanced approach would be to use plain `LoadLibrary` and patch the `LDR_DATA_TABLE_ENTRY` during the load process to zero out the entry point and TLS callbacks, avoiding these flag-based detections entirely.

### Synthetic Call Stack Spoofing via uwd [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#synthetic-call-stack-spoofing-via-uwd)

**Detection vector.** ETW-based telemetry and call stack inspection tools examine thread call stacks for return addresses pointing into unbacked or suspicious memory regions. A legitimate Windows thread’s call stack traces through well-known system functions in a consistent pattern.

**Implementation.** DoublePulsar’s call stack spoofing implementation is based on the [SilentMoonwalk](https://github.com/klezVirus/SilentMoonwalk) concept by klezVirus, trickster0, and waldo-irc, with [uwd](https://github.com/joaoviictorti/uwd) by Joao Victor as a Rust reference. The code was substantially rewritten as position-independent with significant changes required to evade modern EDR call stack inspection. It parses `.pdata` exception directory entries from ntdll, kernel32, and kernelbase to extract `RUNTIME_FUNCTION` entries. For each function, it walks the `UNWIND_INFO` and `UNWIND_CODE` arrays to calculate exact stack frame sizes, handling all 11 unwind opcodes including `UWOP_PUSH_NONVOL`, `UWOP_ALLOC_LARGE`, `UWOP_ALLOC_SMALL`, `UWOP_SET_FPREG`, and chained unwind info (`UNW_FLAG_CHAININFO`). It then scans module code for ROP gadgets: `jmp [rbx]` (`FF 23`) and `add rsp, 0x58; ret` (`48 83 C4 58 C3`), each validated against their containing function’s `RUNTIME_FUNCTION` entry to ensure a valid frame size.

The `build_config()` function populates a `Config` struct with frame sizes for `RtlUserThreadStart`, `BaseThreadInitThunk`, two intermediate spoofed frames, and both gadgets. A `FramePool` stores up to 8 candidates per slot, and `rotate_config()` selects different candidates before each call using `rdtsc` as a per-call entropy source. Every API call presents a different intermediate call stack to the unwinder.

The `SpoofSynthetic` assembly stub in `synthetic.asm` constructs the fake stack bottom-up, laying down `RtlUserThreadStart+0x21` and `BaseThreadInitThunk+0x14` as the thread root frames, the two rotated intermediate frames with RBP linking for the unwinder, and the `jmp [rbx]` and `add rsp, 0x58; ret` gadgets that handle control flow after the target function returns. The target function is called via `jmp r11` rather than `call`, so no return address from the real caller is pushed onto the stack.

WinDbg’s `.fnent` command dumps the exact unwind metadata that the Rust uwd port parses at runtime:

![uwd Unwind Metadata](https://memn0ps.github.io/DoublePulsar-A-User-Defined-Reflective-Loader-in-the-Crystal-Palace-and-Tradecraft-Garden-Era/figure5_uwd_unwind_metadata.png)

**Figure 5:** _`.fnent kernel32!BaseThreadInitThunk` showing the UNWIND\_CODE entries that uwd parses to compute frame sizes when building the synthetic stack._

**Detection.** [Thread start address analysis](https://www.elastic.co/security-labs/get-injectedthreadex-detection-thread-creation-trampolines) can identify threads whose call stack does not match expected initialization patterns. [Kernel ETW call stack telemetry](https://www.elastic.co/security-labs/doubling-down-etw-callstacks) can capture call stacks at the point of API calls and flag anomalous return addresses pointing into unexpected memory regions. [Return address validation](https://www.elastic.co/security-labs/call-stacks-no-more-free-passes-for-malware) can check whether each return address on the stack is preceded by a `CALL` instruction, which synthetic frames constructed from gadget addresses will fail.

### Sleep Obfuscation [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#sleep-obfuscation)

The sleep cycle is the highest-risk window for Beacon detection. During sleep, Beacon’s code and data sit in memory in cleartext, giving memory scanners a large time window to find signatures.

Cobalt Strike’s standard architecture handles sleep obfuscation through a separate Sleepmask BOF and BeaconGate API proxy. DoublePulsar does not use either. Instead, it replaces the entire Sleepmask mechanism by hooking `Sleep` and `NtWaitForSingleObject` in the IAT, giving the loader direct control over the obfuscation chain without depending on Cobalt Strike’s built-in sleep infrastructure.

DoublePulsar implements four sleep obfuscation techniques, selectable via Cargo feature flags:

| Technique | Dispatch Mechanism | Encryption | NtContinue Chain | Fiber Support | Default |
| --- | --- | --- | --- | --- | --- |
| Ekko | TpAllocTimer / TpSetTimer | RC4 (SystemFunction040/041) | 10-step | Yes | Yes |
| FOLIAGE | NtQueueApcThread | RC4 (SystemFunction040/041) | 10-step | Yes | No |
| Zilean | TpAllocWait / TpSetWait | RC4 (SystemFunction040/041) | 10-step | Yes | No |
| XOR | Plain Sleep call | 128-byte repeating XOR | None | No | No |

During sleep, call stacks are spoofed so that no thread shows any reference to `d3d10.dll` or any address that would indicate injected code. The screenshots below were captured from System Informer while the Beacon was sleeping. Every frame points into legitimate system DLLs.

The spoofed call stack constructed by `spoof_stack_layout()` makes the thread look like a normal Win32 callback, with `EnumDateFormatsExA+0x17` as the callback frame:

![Spoofed Call Stack](https://memn0ps.github.io/DoublePulsar-A-User-Defined-Reflective-Loader-in-the-Crystal-Palace-and-Tradecraft-Garden-Era/figure6_spoofed_callstack.png)

**Figure 6:** _Spoofed call stack showing EnumDateFormatsExA+0x17, BaseThreadInitThunk+0x14, RtlUserThreadStart+0x21_

The sleep thread’s context is replaced by `spoof_context()` to look like an idle thread pool worker waiting on `NtWaitForWorkViaWorkerFactory`:

![Spoofed Sleep Thread](https://memn0ps.github.io/DoublePulsar-A-User-Defined-Reflective-Loader-in-the-Crystal-Palace-and-Tradecraft-Garden-Era/figure7_spoofed_sleep_thread.png)

**Figure 7:** _Sleep thread spoofed by `spoof_context()` to look like an idle worker waiting on `NtWaitForWorkViaWorkerFactory`._

From a debugger, the spoofed beacon thread can be compared against real thread pool workers in the same process:

![Spoofed vs Real Worker](https://memn0ps.github.io/DoublePulsar-A-User-Defined-Reflective-Loader-in-the-Crystal-Palace-and-Tradecraft-Garden-Era/figure8_spoofed_vs_real_worker.png)

**Figure 8:** _WinDbg `~*k`. Thread 5’s stack is forged by `hypnus::spoof_context` via `NtSetContextThread`. Threads 6 and 7 are genuine idle thread pool workers spawned to service Ekko’s timer queue. The only distinguishing frame is `RtlAcquireSRWLockExclusive+0x17` vs `TppWorkerThread+0x2ee`._

The three chain-based techniques (Ekko, FOLIAGE, Zilean) share the same 10-step `NtContinue` context chain, differing only in how they dispatch callback execution:

00. `NtWaitForSingleObject` on a gate event (blocks until main thread signals)
01. `NtProtectVirtualMemory` changes the entire region to `PAGE_READWRITE`
02. `SystemFunction040` RC4-encrypts the image in place
03. `NtGetContextThread` saves the real main thread context to a backup
04. `NtSetContextThread` replaces the main thread context with a spoofed idle context (RIP pointing at `ZwWaitForWorkViaWorkerFactory`, fake stack chain through `RtlAcquireSRWLockExclusive`, `BaseThreadInitThunk`, and `RtlUserThreadStart`)
05. `WaitForSingleObject` performs the actual sleep for the configured duration
06. `SystemFunction041` RC4-decrypts the image
07. `NtProtectVirtualMemory` restores `PAGE_EXECUTE_READ`
08. `NtSetContextThread` restores the real main thread context from backup
09. Signal completion (`NtSetEvent` for Ekko/Zilean, `RtlExitUserThread` for FOLIAGE)

Each context in the chain is configured with JMP gadget indirection: `ctx.Rip` is set to a `jmp <reg>` gadget found in ntdll, kernel32, or kernelbase, and the actual NT function address is placed in the corresponding register. Seven gadget patterns are scanned across three system DLLs (21 possible candidates), and one is randomly selected per run using `rdtsc`. This prevents static signatures on the chain’s RIP values.

Each chain context also gets a spoofed call stack via `spoof_stack_layout()`. The fake return address chain looks like a normal Win32 callback thread: `EnumDateFormatsExA+0x17` as the callback frame, `BaseThreadInitThunk+0x14`, `RtlUserThreadStart+0x21`, and a null terminator. The `jmp [rbx]` and `add rsp, 0x58; ret` gadgets handle control flow between chain steps, with a `mov rsp, rbp; ret` stub restoring the real stack pointer after each step completes.

Control Flow Guard (CFG) bypass is handled by `set_valid_call_targets()`, which queries `NtQueryInformationProcess` for CFG enforcement status and calls `SetProcessValidCallTargets` to register all NT function pointers used in the chain as valid indirect call targets.

Each chain-based technique runs inside a dedicated fiber. Fibers are lightweight, user-mode execution contexts with their own stack, scheduled cooperatively rather than preemptively. The chain needs to manipulate RSP, write fake return addresses, and plant RBP links, all of which would corrupt the Beacon thread’s real stack if done in place. Running on a fiber’s isolated 1MB stack (`ConvertThreadToFiber`, `CreateFiber`, `SwitchToFiber`) keeps the Beacon thread’s stack intact. After the chain completes, execution switches back and the fiber is deleted.

The Ekko, FOLIAGE, and Zilean implementations in DoublePulsar are not direct ports of the original techniques. The original implementations were flagged by top-tier EDRs out of the box. Getting them to work in a real engagement environment required modifications to the chain construction, callback dispatch, and stack layout that are specific to this loader. Ekko is the default because timer-based dispatch via `TpAllocTimer`/`TpSetTimer` is operationally reliable and does not require creating a dedicated thread (unlike FOLIAGE’s `NtCreateThreadEx` and `NtQueueApcThread` approach). Zilean uses `TpAllocWait`/`TpSetWait` with the process pseudo-handle (`-1`) as the wait target, which never signals, so the timeout fires the callback.

The XOR technique is simpler: it applies a 128-byte repeating XOR key to each Beacon section (making sections writable first, XORing, then restoring permissions) and XORs all busy heap allocations via `RtlWalkHeap`. It calls `Sleep` directly through the real kernel32 function with no context chain or fiber isolation. Sometimes simpler is better, fewer moving parts means fewer IoCs, and in environments where the NtContinue chain itself is the detection signal, XOR with a clean `Sleep` call can be the quieter option.

The `Sleep_Hook` wires all of this together. The NtContinue chain encrypts the entire STUB region (step 2 of the chain), and the `Api` struct lives inside that region. If the hook tried to read `Api` from STUB during or after encryption, it would be reading encrypted garbage. So `Api` is copied to the stack first, which is outside the encrypted region:

```rust
pub unsafe extern "C" fn Sleep_Hook(dw_milliseconds: DWORD) {
    let stub_ptr = StubAddr() as PSTUB;

    // Copy Api to stack - the STUB region gets encrypted during the chain
    let mut api: Api = core::ptr::read((*stub_ptr).api);

    // Set up sleep context from STUB fields
    api.sleep.dw_milliseconds = dw_milliseconds;
    api.sleep.buffer = (*stub_ptr).stub_beacon_address as _;
    api.sleep.length = (*stub_ptr).stub_beacon_size as _;
    api.sleep.heap = (*stub_ptr).beacon_heap_handle;

    // Dispatch to the selected sleep technique (compile-time feature flag)
    generate_encryption_key(&mut api);
    encrypt_heap_rc4(&mut api);

    #[cfg(feature = "sleep-ekko")]
    ekko::ekko_with_fiber(&mut api);

    #[cfg(feature = "sleep-foliage")]
    foliage::foliage_with_fiber(&mut api);

    #[cfg(feature = "sleep-zilean")]
    zilean::zilean_with_fiber(&mut api);

    restore_section_protections(&mut api);
    encrypt_heap_rc4(&mut api);

    // Zero the stack copy so key material does not persist
    api.zero();
}
```

The pattern is the same across all chain-based techniques: generate a random RC4 key, encrypt the isolated heap, run the NtContinue chain inside a fiber, restore per-section permissions after the chain flips everything to RX, then decrypt the heap. Only one technique is compiled in at a time, selected by Cargo feature flag.

**Detection.** The NtContinue chain creates observable patterns. [Elastic’s kernel call stack detections](https://www.elastic.co/security-labs/doubling-down-etw-callstacks) can identify [suspicious memory permission transitions and callback-based evasion](https://www.elastic.co/security-labs/upping-the-ante-detecting-in-memory-threats-with-kernel-call-stacks) such as rapid RX to RW to RX flips on the same region. For Ekko specifically, [WithSecure’s research on hunting timer-queue timers](https://labs.withsecure.com/publications/hunting-for-timer-queue-timers) demonstrates that finding multiple unique timer-queue timers in a process is already highly anomalous on a default Windows installation. FOLIAGE’s use of `NtQueueApcThread` can be detected by checking threads in a `Wait:UserRequest` state whose call stack includes `KiUserApcDispatcher`. Monitoring `SetProcessValidCallTargets` calls can reveal CFG bypass attempts. Tools like [Hunt-Sleeping-Beacons](https://github.com/theFLINK/Hunt-Sleeping-Beacons) enumerate queued timer callbacks and flag those pointing at `NtContinue`, detect abnormal intermodular calls (ntdll timer callbacks invoking kernel32/kernelbase APIs), and identify non-executable pages in thread call stacks during the sleep window when permissions are flipped to RW. [Patriot](https://github.com/JoeDesimone/patriot) scans for CONTEXT structures in memory whose `Rip` points at `VirtualProtect` or related APIs, targeting the NtContinue chain contexts directly. DoublePulsar’s JMP gadget indirection mitigates several of these by ensuring neither timer callbacks nor CONTEXT `Rip` values point directly at NT functions. Fiber-based execution remains a visibility gap for most endpoint telemetry since fiber switching occurs entirely in user mode without generating kernel callbacks. On hardware with Intel Control Flow Enforcement Technology (CET) and Shadow Stack enabled, ROP-based sleep obfuscation chains (Ekko, FOLIAGE, Zilean) will not work, as the hardware shadow stack detects return address manipulation that does not correspond to a matching CALL instruction.

### Return Address Spoofing [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#return-address-spoofing)

The call stack spoofing described above is not limited to the sleep obfuscation chain. Every API call made through the `Api` wrappers uses the same `SpoofSynthetic` stub. The dispatch is controlled by feature flags: when `spoof-uwd` is enabled (default), all calls go through `spoof_uwd!`. When `spoof-syscall` is also enabled, ntdll functions resolve the SSN and dispatch via the `syscall` instruction directly. When neither is enabled, calls are made directly.

This means every hooked API call (`InternetConnectA`, `NtWaitForSingleObject`, `RtlAllocateHeap`, `WinHttpOpen`, `WSASocketA`, and others) gets a fresh synthetic call stack with rotated intermediate frames. The detection opportunities are the same as described in the call stack spoofing section above.

### IAT Hooking [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#iat-hooking)

After Beacon’s imports are resolved, DoublePulsar patches 30+ IAT entries to redirect API calls through hook functions that live inside the stomped module’s `.text$D` section. Each hook is matched by DJB2 hash, so adding or removing hooks is as simple as adding or removing a `hook_iat()` call with the target function’s hash. The set of hooked APIs is fully customizable by the operator.

The default hook set covers heap management (`GetProcessHeap`, `RtlAllocateHeap`, `HeapAlloc`), sleep (`Sleep`, `NtWaitForSingleObject`), the complete WinINet and WinHTTP API surfaces, DNS, Winsock, wait functions, memory management (`NtProtectVirtualMemory`), thread context manipulation (`NtGetContextThread`, `NtSetContextThread`, `NtContinue`), and cryptography (`SystemFunction032`). External module hooks resolve their target at call time by walking the PEB and dispatch through call stack spoofing.

The hook chain is observable at runtime by setting WinDbg breakpoints on two APIs, one in Beacon’s patched IAT (`Sleep`) and one that is only called by the Ekko chain (`SystemFunction040`):

![WinDbg Hook Chain](https://memn0ps.github.io/DoublePulsar-A-User-Defined-Reflective-Loader-in-the-Crystal-Palace-and-Tradecraft-Garden-Era/figure9_windbg_hook_chain.png)

**Figure 9:** _Two WinDbg breakpoints in the beacon process. `KERNELBASE!Sleep` fires from a winhttp thread pool callback on thread 11, not from beacon’s own `Sleep` call, which is IAT-hooked and redirected into `Sleep_Hook` and the Ekko chain. `CRYPTBASE!SystemFunction040` (called only by Ekko) fires on thread 2 with the synthetic stack from `spoof_stack_layout()`: `EnumDateFormatsExA+0x17`, `BaseThreadInitThunk+0x14`, `RtlUserThreadStart+0x21`._

**Detection.** IAT entries should point into the address range of the module that exports them. An entry for `GetProcessHeap` pointing into the stomped module instead of `kernel32.dll` is a clear indicator. Tools that enumerate IAT entries and validate them against the PEB module list can automate this.

### Heap Isolation [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#heap-isolation)

Beacon’s heap allocations are redirected to a dedicated heap created by `RtlCreateHeap(HEAP_GROWABLE)` during the loader’s initialization. The handle is stored in `STUB.beacon_heap_handle`. The `GetProcessHeap_Hook` returns this isolated heap handle instead of the process default heap, and `RtlAllocateHeap_Hook`/`HeapAlloc_Hook` route allocations through the spoofed API wrappers. During sleep obfuscation, `encrypt_heap_rc4()` walks the isolated heap via `RtlWalkHeap`, encrypting each busy entry (`RTL_PROCESS_HEAP_ENTRY_BUSY` flag) in place using `SystemFunction032` with a randomly generated 16-byte alphanumeric key.

The isolated heap is trivially visible from a debugger via `!heap -s`:

![Beacon Heap Isolation](https://memn0ps.github.io/DoublePulsar-A-User-Defined-Reflective-Loader-in-the-Crystal-Palace-and-Tradecraft-Garden-Era/figure10_beacon_heap_isolation.png)

**Figure 10:** _WinDbg `!heap -s`. The fourth heap `0000025f48180000` is the beacon’s isolated heap from `RtlCreateHeap`, matching the `[LDR] Heap created: 0000025F48180000` line in the debug output. Every beacon allocation routes through it via `GetProcessHeap_Hook`._

**Detection.** Heap enumeration can reveal an unusual number of process heaps. A process with an extra heap that was not created by any of its loaded modules is suspicious, because most applications only create heaps during CRT initialization or through well-known allocation patterns. The aggregate behavior around sleep cycles is also characteristic: a burst of heap allocation reads followed by `SystemFunction032` calls, memory permission changes, and a sleep forms a detectable behavioral sequence even though individual `RtlWalkHeap` calls do not produce direct ETW telemetry.

### Optional Syscall Dispatch [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#optional-syscall-dispatch)

The `spoof-syscall` feature flag enables direct syscall execution with SSN resolution. The `syscall.rs` module implements three resolution strategies:

**Hell’s Gate** reads the SSN directly from an unhooked ntdll stub by matching the byte pattern `4C 8B D1 B8 XX XX 00 00` (mov r10, rcx; mov eax, SSN).

![Clean ntdll Stub](https://memn0ps.github.io/DoublePulsar-A-User-Defined-Reflective-Loader-in-the-Crystal-Palace-and-Tradecraft-Garden-Era/figure11_clean_ntdll_stub.png)

**Figure 11:** _`u ntdll!NtAllocateVirtualMemory` on an unhooked system. The bytes `4C 8B D1 B8 18 00 00 00` are the Hell’s Gate pattern, with `0x18` as the SSN._

**Halo’s Gate** handles stubs where the first byte is `0xE9` (JMP), indicating an EDR hook. It scans neighbor stubs at 32-byte intervals (up to 255 positions in both directions), finds an unhooked neighbor, reads its SSN, and adjusts by the distance.

**Tartarus Gate** handles partial hooks where the JMP is at byte offset 3 rather than byte 0, using the same neighbor-scanning logic.

The `get_syscall_address()` function scans forward from the function address for the `0F 05 C3` byte sequence (`syscall; ret`) to find the indirect syscall target address.

Direct and indirect syscalls introduce additional IoCs that are not required in most scenarios. Even when user-mode hooks are present, unhooking is an option. Calling functions normally from backed memory with a clean call stack is preferable to direct syscalls in most operational contexts. The feature is optional and disabled by default for this reason.

**Detection.** Syscall instructions executed from non-ntdll memory are detectable via ETW kernel telemetry. SSN validation can compare the SSN used against the expected value for the target function. Direct syscall patterns from user-mode code that is not ntdll are an increasingly reliable detection signal.

## Detection Engineering [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#detection-engineering)

An important caveat before getting into specifics: detection always depends on how the shellcode loader is executed and how it loads the UDRL itself. The UDRL is just the reflective loader. The initial shellcode injection, whether through process injection, DLL side-loading, or another delivery mechanism, is a separate detection surface with its own visibility. A UDRL that evades every memory scanner is still only as stealthy as the loader that put it there.

**ETW Threat Intelligence (ETWTI).** The Microsoft-Windows-Threat-Intelligence provider (ETWTI, requires a Protected Process Light consumer) surfaces memory permission changes (`NtProtectVirtualMemory` calls transitioning RX to RW and back), thread creation and context manipulation, and APC queuing (`NtQueueApcThread`). This is kernel-level telemetry, not regular ETW that any process can subscribe to. Thread pool timer and wait object creation (`TpAllocTimer`, `TpAllocWait`) can be observed through kernel-level telemetry and thread pool callback monitoring. The sleep obfuscation chain produces a distinctive burst of memory protection change events in rapid sequence, which is reliable because legitimate code rarely flips the same region between RX and RW multiple times within milliseconds.

**Call Stack Analysis.** Threads whose start address points into a stomped module’s `.text` section are suspicious. The synthetic call stacks always terminate with `RtlUserThreadStart+0x21` and `BaseThreadInitThunk+0x14` at fixed offsets, which may differ from naturally occurring thread initialization patterns. [Elastic’s kernel call stack detections](https://www.elastic.co/security-labs/doubling-down-etw-callstacks) and [return address validation](https://www.elastic.co/security-labs/call-stacks-no-more-free-passes-for-malware) are directly applicable here. Notably, Elastic’s [API Call from a Suspicious Stack](https://github.com/elastic/protections-artifacts/blob/278054cb0e90dca20d6fe06f63cce6600902d50d/behavior/rules/windows/defense_evasion_api_call_from_a_suspicious_stack.toml) rule appeared in the same month as the DoublePulsar public release and appears highly targeted, matching the exact call stack summary pattern produced by SilentMoonwalk-based spoofing implementations like uwd. Their [API Call via Jump ROP Gadget](https://github.com/elastic/protections-artifacts/blob/1f3f563a9e6982c057c553c6e79c2419b4fe1738/behavior/rules/windows/defense_evasion_api_call_via_jump_rop_gadget.toml) rule detects JMP/CALL register gadget patterns (such as `jmp [rbx]` / `FF 23`) in the return chain by inspecting trailing bytes at each return address. This rule existed prior to DoublePulsar’s release but appears to have become more effective following a recent Elastic agent update that enhanced its ability to flag ROP patterns within loaded module images. Together, these rules represent strong behavioral detection for this class of call stack spoofing and would catch the public DoublePulsar release as shipped, after release.

**Memory Scanning.** PE-sieve compares in-memory module sections against their on-disk originals and flags content mismatches. Moneta detects memory permission anomalies and unbacked executable regions. Module stomping defeats unbacked-memory detection but not content-comparison scanning. The stomped module’s `.text` section will not match its disk counterpart.

![PE-sieve Detection](https://memn0ps.github.io/DoublePulsar-A-User-Defined-Reflective-Loader-in-the-Crystal-Palace-and-Tradecraft-Garden-Era/figure12_pesieve_detection.png)

**Figure 12:** _PE-sieve detecting the stomped d3d10.dll module_

**YARA Rules.** DoublePulsar ships with two YARA rules in `doublepulsar.yar`:

The first rule (`DoublePulsar_UDRL_Loader`) matches the assembly entry point bytes at file offset 0, requires both `udrl.dll` and `Entry` export strings, `SystemFunction032`, heap management strings (`RtlCreateHeap`, `RtlWalkHeap`), at least one sleep technique indicator (timer APIs, wait APIs, APC APIs, or fiber APIs), and network/CFG strings, within a 50KB-200KB file size range.

The second rule (`DoublePulsar_UDRL_Strings`) targets the unique combination of string artifacts: `udrl.dll`, all three SystemFunction variants (032/040/041), thread pool APIs (`TpAllocTimer` or `TpAllocWait`), `TpAllocPool`, heap APIs, `EnumDateFormatsExA` (used as the spoofed callback frame source), and `SetProcessValidCallTargets` (the CFG bypass API).

These rules detect the **loader itself**, not the Beacon payload. All matched strings (`udrl.dll`, `SystemFunction032`, `TpAllocTimer`, `EnumDateFormatsExA`, etc.) are from the loader’s code. Both rules match against the raw `Titan.x64.bin` shellcode binary before any Beacon is appended. At runtime, these strings are present in the stomped module’s memory during the awake window, but during sleep the entire region is RC4-encrypted and the strings will not be in cleartext. In practice, a shellcode loader would also encrypt or encode the UDRL payload before injection, preventing the YARA rules from matching on disk or in transit. The primary value of these rules is scanning process memory during the awake window or analyzing extracted shellcode samples.

**Validation Testing.** DoublePulsar was tested on Windows 10 (Build 19045) and Windows 11 (Build 22631) against Elastic 9.0.1 in prevention mode with aggressive settings and multiple integrations enabled. The YARA rules provided in the repository are designed to detect the loader’s artifacts.

**Detection Surface.** The COFF loader or shellcode injector that delivers the UDRL shellcode into the target process is the initial detection surface, not the UDRL payload itself. The UDRL shellcode only executes after injection has already occurred. Focusing detection on the injection mechanism, process injection APIs, thread creation patterns, memory allocation sequences, and the initial write of shellcode into the target process provides an earlier interception point than scanning for the loaded Beacon. In a typical deployment, a Beacon Object File (BOF) or a standalone injector writes the UDRL shellcode into a target process and starts a thread. The BOF/injector is where the initial execution chain is most visible to endpoint telemetry, and where behavioral rules have the highest signal-to-noise ratio.

In the test case captured for this blog, the beacon was delivered via DLL side-loading: a signed third-party executable loads a shellcode loader DLL from its install directory, and that loader runs the UDRL in memory. WinDbg `~0k` on the main thread shows the full delivery chain:

![DLL Sideload Chain](https://memn0ps.github.io/DoublePulsar-A-User-Defined-Reflective-Loader-in-the-Crystal-Palace-and-Tradecraft-Garden-Era/figure13_dll_sideload_chain.png)

**Figure 13:** _WinDbg `~0k`. Reading bottom up: `LdrInitializeThunk` -\> `LdrpInitializeInternal` -\> `_LdrpInitialize` -\> `NtTestAlert` -\> `KiUserApcDispatch` -\> `<loader>!DllMain` -\> `WaitForSingleObjectEx`. The shellcode loader DLL is side-loaded by a signed third-party binary during process initialization and runs the UDRL in memory. This is the delivery surface, not the UDRL itself._

**Module Load Behavioral Analysis.** When the sacrificial DLL is loaded via `LoadLibraryExA`, it generates a module load event (Sysmon Event ID 7, ETW `Microsoft-Windows-Kernel-Process` ImageLoad). If a DLL like `d3d10.dll` is loaded into a process that would not normally use DirectX, such as a non-graphical service or command-line tool, this is a behavioral anomaly worth flagging. The module will also appear in the PEB loader data structures with anomalous metadata compared to a normally initialized DLL.

![Process Monitor d3d10 Load](https://memn0ps.github.io/DoublePulsar-A-User-Defined-Reflective-Loader-in-the-Crystal-Palace-and-Tradecraft-Garden-Era/figure14_procmon_d3d10_load.png)

**Figure 14:** _Process Monitor capturing the `Load Image` event for `C:\Windows\System32\d3d10.dll` with the kernel-side stack trace on the right. Frames 16-17 (`GetCurrentPackageInfo3+0x565`, `DiscardVirtualMemory+0x99`) are not normal callers of `LoadLibraryExA`, they are spoofed intermediate frames planted by the UDRL’s `SpoofSynthetic` rotation and survive into kernel-side stack capture._

**Private Pages Within Backed Memory.** Module stomping makes memory appear backed by a legitimate module on disk, but the actual physical pages become private (copy-on-write is triggered when the loader overwrites the `.text` section). Advanced scanners can check working set entries to determine if pages within a module’s virtual address range are still shared (file-backed) or have become private (modified), which reveals stomped sections even when the virtual address range appears legitimate.

**Thread Context Manipulation.** The ACE technique in `ace.rs` creates a thread suspended at `RtlUserThreadStart+0x21` and then modifies its RIP register before resuming. This pattern, creating a thread at a known offset within an NT function and immediately changing its context, is a well-documented injection technique. Monitoring `NtSetContextThread` calls on newly created suspended threads, particularly when the new RIP points outside the module that was specified as the thread start address, is a reliable detection signal.

**API String Artifacts.** The loader resolves all APIs by DJB2 hash at runtime, avoiding static imports in the IAT. Function names resolved through `hash_str!` macros compile to constant hash values, not plaintext strings. However, some plaintext strings do appear in the binary: the module stomp target name (changeable in source) and the API name strings used for PEB-based export resolution in hook functions, such as `InternetConnectA`, `WinHttpOpen`, `DnsExtractRecordsFromMessage_UTF8`, and `WSASocketA`. Their presence as a cluster is a strong static indicator, which is why the YARA rules target these string combinations.

**MITRE ATT&CK Mapping**

| Technique ID | Name | DoublePulsar Component |
| --- | --- | --- |
| T1620 | Reflective Code Loading | Core loader pipeline, sRDI-style prepended loader |
| T1055.001 | Dynamic-link Library Injection | Module stomping via LoadLibraryExA into a sacrificial DLL |
| T1027.013 | Encrypted/Encoded File | RC4 Beacon encryption via Titan.cna |
| T1140 | Deobfuscate/Decode Files or Information | Runtime RC4 decryption in loader |
| T1497.003 | Time Based Checks | Sleep obfuscation (Ekko, FOLIAGE, Zilean, XOR) |
| T1106 | Native API | PEB walking, direct NT API calls, DJB2 hash resolution |
| T1036.005 | Match Legitimate Resource Name or Location | Beacon mapped into a legitimate module’s memory space |
| T1055.012 | Process Hollowing | ACE thread RIP hijack via NtSetContextThread |
| T1562.001 | Disable or Modify Tools | IAT hooking to intercept Beacon API calls |
| T1027.007 | Dynamic API Resolution | DJB2 hash-based function resolution from PEB |

## Why Rust for Offensive Tooling [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#why-rust-for-offensive-tooling)

The same techniques and primitives that exist in C apply in Rust. The language does not change what is possible, only how it is expressed.

DoublePulsar compiles with `#![no_std]` and `#![no_main]`, producing a binary with no runtime library dependency and no stack unwinding. A custom linker script orders sections so assembly code comes first, loader code follows, then hooks and utilities. After compilation, `objcopy --dump-section .text` extracts the entire `.text` section as raw shellcode. Inline assembly provides `GetIp()` and `StubAddr()` for RIP-relative addressing that Rust cannot safely express.

The project is composed of three internal crates: `api` (Windows API resolution and typed wrappers), `uwd` (call stack spoofing), and `hypnus` (sleep obfuscation), plus a shared `ntdef` types crate for Windows type definitions. Each crate compiles as `no_std` PIC code and can be developed and tested independently. Cargo feature flags (`sleep-ekko`, `spoof-uwd`, `spoof-syscall`) control which techniques are compiled in, keeping the binary size minimal for each configuration.

Writing PIC in Rust is less commonly attempted because the tooling and patterns are not as well established as they are in C. The nightly toolchain is required, and the compiler can introduce unexpected relocations that break position-independence if the linker configuration is not precise. Solvable problems, but the initial learning curve is steeper.

## Future Directions [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#future-directions)

DoublePulsar as released is intentionally unobfuscated and carries a number of known IoCs by design. Despite being one of the few advanced, stable UDRLs publicly available with this depth of evasion capability, the public release prioritizes demonstrating the techniques over operational stealth. The natural next step for tooling like this is string obfuscation to kill the plaintext API name clusters that the YARA rules target, tightening the module stomping implementation so it does not leave the `DONT_RESOLVE_DLL_REFERENCES` flag residue or private pages within a shared image range, randomizing the sacrificial module selection across deployments, and then a custom VM-based obfuscator on top of all of it, with opaque predicates, control-flow flattening, mixed Boolean-arithmetic (MBA) expressions, and VM handler hardening, making static analysis, symbolic execution, and reverse engineering significantly harder. The YARA rules in this repository, for example, rely on recognizable API strings and entry point bytes that a hardened virtualization layer would break.

The public research represented by DoublePulsar and the broader portfolio on [GitHub](https://github.com/memN0ps), including work on Windows kernel rootkits, UEFI bootkits, hypervisors, and shellcode injection, forms the foundation for more advanced private capability. As stated in a recent post: the building blocks are public, what sits on top of them is not. The language does not matter. The primitives are the same. Rust happens to be the one I enjoy working with. It covers every layer of the stack I need, from UEFI bootkits and kernel rootkits to Type-1 and Type-2 hypervisors, Hyper-V hijacking frameworks, reflective loaders, and full command-and-control infrastructure including the server, database, networking, and GUI. There is no layer where I need to switch to another language, and everything integrates naturally within the same ecosystem.

Every technique in this post has a detection opportunity. The YARA rules and MITRE ATT&CK mapping are there for defenders to use.

## Credits and References [\#](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/\#credits-and-references)

DoublePulsar builds on the work of many researchers and projects. Credit is given generously.

- [Austin Hudson](https://github.com/realoriginal) for [TitanLdr](https://github.com/benheise/TitanLdr) (the original UDRL that inspired AceLdr and DoublePulsar), [FOLIAGE](https://github.com/benheise/FOLIAGE) (APC-based sleep obfuscation), and [titanldr-ng](https://github.com/klezVirus/titanldr-ng) (CNA integration, RC4 beacon encryption/decryption, additional IAT hooks), and for reviewing this blog
- [Kyle Avery](https://github.com/kyleavery) for [AceLdr](https://github.com/kyleavery/AceLdr/), which built on Austin Hudson’s TitanLdr design and merged FOLIAGE sleep obfuscation with return address spoofing and heap isolation, and for reviewing this blog
- [Arash Parsa (waldo-irc)](https://github.com/waldo-irc) for [Bypassing PE-sieve and Moneta](https://www.arashparsa.com/bypassing-pesieve-and-moneta-the-easiest-way-i-could-find/), [Hook heaps and live free](https://www.arashparsa.com/hook-heaps-and-live-free/), [MalMemDetect](https://github.com/waldo-irc/MalMemDetect), detection engineering and evasion advice, and for reviewing this blog
- [C5pider](https://github.com/Cracked5pider) for [Stardust](https://github.com/Cracked5pider/Stardust) (PIC framework), [Ekko](https://github.com/Cracked5pider/Ekko) sleep obfuscation (originally discovered by Peter Winter-Smith, implemented in MDSec’s Nighthawk), Zilean sleep obfuscation, [Havoc Professional](https://infinitycurve.org/products/havoc-professional) / [InfinityCurve](https://infinitycurve.org/), and for reviewing this blog
- [klezVirus](https://github.com/klezVirus), [Arash Parsa (waldo-irc)](https://github.com/waldo-irc), and [trickster0](https://github.com/trickster0) for [SilentMoonwalk](https://github.com/klezVirus/SilentMoonwalk) (call stack spoofing) and [Tartarus Gate](https://github.com/trickster0/TartarusGate)
- [Joao Victor](https://github.com/joaoviictorti) for [uwd](https://github.com/joaoviictorti/uwd) and [hypnus](https://github.com/joaoviictorti/hypnus), used as reference for a complete rewrite as position-independent code
- [Forrest Orr](https://www.forrest-orr.net/) for [Masking malicious memory artifacts](https://www.forrest-orr.net/post/masking-malicious-memory-artifacts-part-ii-insights-from-moneta)
- [Raphael Mudge](https://www.cobaltstrike.com/profile/raphael-mudge) for creating [Cobalt Strike](https://www.cobaltstrike.com/) and [Crystal Palace](https://tradecraftgarden.org/crystalpalace.html)
- [RastaMouse](https://github.com/rasta-mouse) / [Zero Point Security](https://www.zeropointsecurity.co.uk/) for [Red Team Ops II](https://www.zeropointsecurity.co.uk/course/red-team-ops-ii) and [Crystal-Kit](https://github.com/rasta-mouse/Crystal-Kit)
- [Alex Reid](https://www.zeropointsecurity.co.uk/program/bof-udrl-sleepmask-dev) / [Zero Point Security](https://www.zeropointsecurity.co.uk/) for [BOF, UDRL & Sleepmask Development](https://www.zeropointsecurity.co.uk/program/bof-udrl-sleepmask-dev)
- [namazso](https://github.com/namazso) for the original [x64 return address spoofing](https://www.unknowncheats.me/forum/anti-cheat-bypass/268039-x64-return-address-spoofing-source-explanation.html) technique
- IBM X-Force for [Defining the Cobalt Strike Reflective Loader](https://www.ibm.com/think/x-force/defining-cobalt-strike-reflective-loader)
- [Bobby Cooke](https://github.com/boku7) for [BokuLoader](https://github.com/boku7/BokuLoader)
- [Robert Bearsby](https://www.cobaltstrike.com/blog/revisiting-the-udrl-part-1-simplifying-development) / Cobalt Strike for the Revisiting the UDRL blog series and the prepended loader architecture diagram
- [Lorenzo Meacci](https://lorenzomeacci.com/bypassing-edr-in-a-crystal-clear-way) for Crystal Kit / Tradecraft Garden EDR evasion research
- [Dylan Tran](https://dtsec.us/) for [Module Stomping research](https://dtsec.us/2023-11-04-ModuleStompin/)
- [Stephen Fewer](https://github.com/stephenfewer) for [Reflective DLL Injection](https://github.com/stephenfewer/ReflectiveDLLInjection) (2008)
- [Nick Landers](https://github.com/monoxgas) for [sRDI](https://github.com/monoxgas/sRDI) (Shellcode Reflective DLL Injection)
- [J. Lospinoso](https://github.com/JLospinoso) for [Gargoyle](https://github.com/JLospinoso/gargoyle) (timer-based code execution)
- [F-Secure](https://blog.f-secure.com/) for [Hunting for Gargoyle](https://blog.f-secure.com/hunting-for-gargoyle-memory-scanning-evasion/)
- [Elastic](https://www.elastic.co/) for [Detecting Cobalt Strike with memory signatures](https://www.elastic.co/blog/detecting-cobalt-strike-with-memory-signatures)
- [MDSec Nighthawk study](https://web.archive.org/web/20220625003531/https://suspicious.actor/2022/05/05/mdsec-nighthawk-study.html) for Ekko sleep obfuscation research
- [am0nsec](https://github.com/am0nsec) for [Hell’s Gate](https://github.com/am0nsec/HellsGate)

**Naming.** DoublePulsar is named after the [DoublePulsar](https://en.wikipedia.org/wiki/DoublePulsar) implant developed by the NSA’s [Equation Group](https://en.wikipedia.org/wiki/Equation_Group), leaked by the Shadow Brokers in 2017. The original DoublePulsar demonstrated a prepended loader architecture for reflective injection, which inspired the approach used in this project.

Read other posts

* * *

[\[Hypervisors for Memory Introspection and Reverse Engineering\] >](https://memn0ps.github.io/hypervisors-for-memory-introspection-and-reverse-engineering/)