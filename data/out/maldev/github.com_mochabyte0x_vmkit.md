# https://github.com/mochabyte0x/vmkit

[Skip to content](https://github.com/mochabyte0x/vmkit#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/mochabyte0x/vmkit) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/mochabyte0x/vmkit) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/mochabyte0x/vmkit) to refresh your session.Dismiss alert

{{ message }}

[mochabyte0x](https://github.com/mochabyte0x)/ **[vmkit](https://github.com/mochabyte0x/vmkit)** Public

- [Notifications](https://github.com/login?return_to=%2Fmochabyte0x%2Fvmkit) You must be signed in to change notification settings
- [Fork\\
0](https://github.com/login?return_to=%2Fmochabyte0x%2Fvmkit)
- [Star\\
26](https://github.com/login?return_to=%2Fmochabyte0x%2Fvmkit)


main

[**1** Branch](https://github.com/mochabyte0x/vmkit/branches) [**0** Tags](https://github.com/mochabyte0x/vmkit/tags)

[Go to Branches page](https://github.com/mochabyte0x/vmkit/branches)[Go to Tags page](https://github.com/mochabyte0x/vmkit/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![mochabyte0x](https://avatars.githubusercontent.com/u/115954804?v=4&size=40)](https://github.com/mochabyte0x)[mochabyte0x](https://github.com/mochabyte0x/vmkit/commits?author=mochabyte0x)<br>[Enhance README with comprehensive project details](https://github.com/mochabyte0x/vmkit/commit/0960e27f1f1db6368260fce97b73f34920f1ecd0)<br>Open commit details<br>last monthMay 10, 2026<br>[0960e27](https://github.com/mochabyte0x/vmkit/commit/0960e27f1f1db6368260fce97b73f34920f1ecd0) · last monthMay 10, 2026<br>## History<br>[3 Commits](https://github.com/mochabyte0x/vmkit/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/mochabyte0x/vmkit/commits/main/) 3 Commits |
| [example](https://github.com/mochabyte0x/vmkit/tree/main/example "example") | [example](https://github.com/mochabyte0x/vmkit/tree/main/example "example") | [Add files via upload](https://github.com/mochabyte0x/vmkit/commit/19a5e162a087194caad09dd0f2fc003c56914b86 "Add files via upload") | last monthMay 10, 2026 |
| [.gitignore](https://github.com/mochabyte0x/vmkit/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/mochabyte0x/vmkit/blob/main/.gitignore ".gitignore") | [Initial commit](https://github.com/mochabyte0x/vmkit/commit/3786f0773d47742bc542014105a621f8b71118d4 "Initial commit") | last monthMay 10, 2026 |
| [LICENSE](https://github.com/mochabyte0x/vmkit/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/mochabyte0x/vmkit/blob/main/LICENSE "LICENSE") | [Initial commit](https://github.com/mochabyte0x/vmkit/commit/3786f0773d47742bc542014105a621f8b71118d4 "Initial commit") | last monthMay 10, 2026 |
| [Makefile](https://github.com/mochabyte0x/vmkit/blob/main/Makefile "Makefile") | [Makefile](https://github.com/mochabyte0x/vmkit/blob/main/Makefile "Makefile") | [Add files via upload](https://github.com/mochabyte0x/vmkit/commit/19a5e162a087194caad09dd0f2fc003c56914b86 "Add files via upload") | last monthMay 10, 2026 |
| [README.md](https://github.com/mochabyte0x/vmkit/blob/main/README.md "README.md") | [README.md](https://github.com/mochabyte0x/vmkit/blob/main/README.md "README.md") | [Enhance README with comprehensive project details](https://github.com/mochabyte0x/vmkit/commit/0960e27f1f1db6368260fce97b73f34920f1ecd0 "Enhance README with comprehensive project details  Expanded README with detailed sections on motivation, usage, and technical explanations.") | last monthMay 10, 2026 |
| [compile\_flags.txt](https://github.com/mochabyte0x/vmkit/blob/main/compile_flags.txt "compile_flags.txt") | [compile\_flags.txt](https://github.com/mochabyte0x/vmkit/blob/main/compile_flags.txt "compile_flags.txt") | [Add files via upload](https://github.com/mochabyte0x/vmkit/commit/19a5e162a087194caad09dd0f2fc003c56914b86 "Add files via upload") | last monthMay 10, 2026 |
| [vm\_loader.hpp](https://github.com/mochabyte0x/vmkit/blob/main/vm_loader.hpp "vm_loader.hpp") | [vm\_loader.hpp](https://github.com/mochabyte0x/vmkit/blob/main/vm_loader.hpp "vm_loader.hpp") | [Add files via upload](https://github.com/mochabyte0x/vmkit/commit/19a5e162a087194caad09dd0f2fc003c56914b86 "Add files via upload") | last monthMay 10, 2026 |
| View all files |

## Repository files navigation

# vmkit

[Permalink: vmkit](https://github.com/mochabyte0x/vmkit#vmkit)

A header-only, freestanding C++20 template for IR-bytecode VM loaders. The
whole point is to spin up a new loader without rewriting the same dispatch /
decode / decrypt plumbing every single time.

## TOC

[Permalink: TOC](https://github.com/mochabyte0x/vmkit#toc)

- [vmkit](https://github.com/mochabyte0x/vmkit#vmkit)
  - [Motivation](https://github.com/mochabyte0x/vmkit#motivation)
  - [What this is](https://github.com/mochabyte0x/vmkit#what-this-is)
  - [What it deliberately leaves to you](https://github.com/mochabyte0x/vmkit#what-it-deliberately-leaves-to-you)
  - [Layout](https://github.com/mochabyte0x/vmkit#layout)
  - [Quickstart](https://github.com/mochabyte0x/vmkit#quickstart)
  - [Building the example](https://github.com/mochabyte0x/vmkit#building-the-example)
  - [How the round-trip works](https://github.com/mochabyte0x/vmkit#how-the-round-trip-works)
  - [Configuration flags](https://github.com/mochabyte0x/vmkit#configuration-flags)
  - [Adding a new opcode](https://github.com/mochabyte0x/vmkit#adding-a-new-opcode)
  - [Compile flags for production loaders](https://github.com/mochabyte0x/vmkit#compile-flags-for-production-loaders)
- [Technical explanation](https://github.com/mochabyte0x/vmkit#technical-explanation)
  - [The dispatch table](https://github.com/mochabyte0x/vmkit#the-dispatch-table)
  - [Why specialization beats a switch](https://github.com/mochabyte0x/vmkit#why-specialization-beats-a-switch)
  - [Opcode randomization](https://github.com/mochabyte0x/vmkit#opcode-randomization)
  - [Bytecode encryption at rest](https://github.com/mochabyte0x/vmkit#bytecode-encryption-at-rest)
  - [Per-operation context encryption](https://github.com/mochabyte0x/vmkit#per-operation-context-encryption)
  - [Why everything is `if constexpr`](https://github.com/mochabyte0x/vmkit#why-everything-is-if-constexpr)
  - [Why C++20 specifically](https://github.com/mochabyte0x/vmkit#why-c20-specifically)
  - [Reinterpret-cast on the bytecode](https://github.com/mochabyte0x/vmkit#reinterpret-cast-on-the-bytecode)
  - [Op layout and alignment](https://github.com/mochabyte0x/vmkit#op-layout-and-alignment)
  - [Constraints worth knowing](https://github.com/mochabyte0x/vmkit#constraints-worth-knowing)
  - [Going beyond the template](https://github.com/mochabyte0x/vmkit#going-beyond-the-template)

## Motivation

[Permalink: Motivation](https://github.com/mochabyte0x/vmkit#motivation)

Two pieces of prior art kicked this whole thing off.

The first was [_RISCy Business_](https://secret.club/2023/12/24/riscy-business.html)
on secret.club. It's about embedding a full RISC-V interpreter to execute
LLVM-retargeted Windows code as RISC-V bytecode. Pretty neat. The second
was the **Firebeam VM** in Havoc Pro, which applies that same VM-as-loader
idea inside a production C2.

Most of the value here isn't in inventing some clever ISA: it's in having
a small, embeddable, hardenable execution layer between your bytecode and
the host. So I wanted to come at it from a loader-first angle and trade ISA
fidelity for simplicity. RISC-V gives you a real toolchain, but at the cost
of carrying an interpreter and a CRT shim.

For a loader the bytecode rarely needs to do more than _allocate, write,_
_decrypt, jump_. A custom IR with fixed-size ops covers that surface in a
fraction of the code, and the obfuscation primitives that actually matter
(opcode randomization, bytecode encryption at rest, per-op state
encryption) port across cleanly. They're properties of the dispatch loop,
not the instruction set.

So this template is the dispatch / decode / decrypt skeleton I wished I had
on hand when starting fresh: in "modern" C++, freestanding-friendly, with
everything Windows-specific left as a clearly marked extension point. Drop
in a `Handler<>` specialization per opcode and you've got a working loader.

## What this is

[Permalink: What this is](https://github.com/mochabyte0x/vmkit#what-this-is)

A single header (`vm_loader.hpp`) that gives you:

- A fixed-size IR `Op` record and a typed `Vm<...>` dispatcher
- Compile-time per-opcode validation through `Handler<Op>` template specialization
- A 256-entry `constexpr` jump table built at compile time (zero runtime cost on dispatch)
- Three opt-in obfuscation hooks that cost _nothing_ when disabled:

  - opcode randomization (per-build randomized bytecode opcodes)
  - bytecode XOR encryption at rest
  - per-operation context encryption
- A `consteval` Jenkins-OAAT API hash, in case you want it for dynamic resolution

The runnable example is a real shellcode loader, not a MessageBox stand-in.
`example_builder.cpp` reads `example/payload.bin` (raw shellcode), XOR-encrypts
both the IR bytecode and the payload, and emits `example/embedded.h` with two
encrypted blobs inside. `example_loader.cpp``#include`s that header and runs
the classic 5-op pipeline: `AllocRegion` → `WritePayload` (encrypted bytes
into the region) → `DecryptRegion` (XOR in place) → `ProtectRX` → `ExecRegion`
(cast to fn ptr and jump). Same shape a production loader uses; the only
thing you have to bring is the payload.

## What it deliberately leaves to you

[Permalink: What it deliberately leaves to you](https://github.com/mochabyte0x/vmkit#what-it-deliberately-leaves-to-you)

- Memory primitives (`VirtualAlloc` / `NtAllocateVirtualMemory`)
- Execution methods (fibers, threadpool, indirect syscalls, …)
- Anti-analysis checks
- Syscall resolution and API hash tables
- Payload encryption

The template covers the VM core. The rest is wired in through `Handler<>`
bodies on your side.

## Layout

[Permalink: Layout](https://github.com/mochabyte0x/vmkit#layout)

```
template/
  vm_loader.hpp           the entire VM
  Makefile                builds the example loader and builder
  compile_flags.txt       clangd config (C++20, freestanding-friendly)
  example/
    example_loader.cpp    Windows loader that runs encrypted shellcode via the VM
    example_builder.cpp   matching builder that consumes payload.bin + emits embedded.h
    payload.bin           raw shellcode you drop in (NOT committed)
    embedded.h            generated by the builder, consumed by the loader
```

Four moving parts inside `vm_loader.hpp`:

| Type | Role |
| --- | --- |
| `vmkit::Op<Opcode>` | Fixed-size operation record |
| `vmkit::Handler<Op>` | Per-opcode behavior, you specialize this |
| `vmkit::OpcodeList<Ops...>` | Pack of opcodes the VM should dispatch |
| `vmkit::Vm<Opcode, Ctx, Cfg, OpcodeList>` | The dispatcher |

## Quickstart

[Permalink: Quickstart](https://github.com/mochabyte0x/vmkit#quickstart)

```
#include "vm_loader.hpp"

// 1. Define your opcodes (must fit in uint8_t).
enum class MyOp : std::uint8_t { Alloc = 0, Write = 1, Exec = 2 };

// 2. Define your loader's mutable state.
struct MyContext { void* regions[8]; };

// 3. Specialize Handler<> for each opcode.
template <> struct vmkit::Handler<MyOp::Alloc> {
    static void execute(MyContext& ctx, const vmkit::Op<MyOp>& op) noexcept {
        ctx.regions[op.u32[0]] = my_virtual_alloc(op.u64[0]);
    }
};
// ... Write, Exec ...

// 4. Pick a config (or roll your own by inheriting from DefaultConfig).
struct MyCfg : vmkit::DefaultConfig {
    static constexpr bool bytecode_xor_encrypted = true;
    static void decrypt_bytecode(std::span<std::uint8_t> blob,
                                 std::uint32_t seed) noexcept {
        // your in-place XOR / chacha / aes routine here
    }
};

// 5. Run.
vmkit::Vm<MyOp, MyContext, MyCfg, vmkit::OpcodeList<MyOp::Alloc, MyOp::Write, MyOp::Exec>> vm;
vm.execute(blob_span, ctx, seed);
```

## Building the example

[Permalink: Building the example](https://github.com/mochabyte0x/vmkit#building-the-example)

You need to drop a raw shellcode binary at `example/payload.bin` first,
otherwise `make` will refuse with `No rule to make target 'example/payload.bin'`.
Anything that's a valid x64 entry point works. Then:

```
make             # build everything (builder -> embedded.h -> loader)
make run-loader  # build + run the loader (executes the shellcode)
make run-builder # build + run the builder on its own (prints to stdout)
make clean
```

The build chain is: builder compiles first, then runs against `payload.bin`
to generate `example/embedded.h`, then the loader compiles against it. Swap
out `payload.bin` and re-run `make` and the whole thing rebuilds with the
new payload baked in.

`make CXX=g++` or `make CXXFLAGS="-std=c++20 -O3"` if you want to override
the defaults.

## How the round-trip works

[Permalink: How the round-trip works](https://github.com/mochabyte0x/vmkit#how-the-round-trip-works)

A walk through what actually happens between `make` and the shellcode running:

1. **Builder side.**`example_builder.cpp` reads `example/payload.bin` (raw
shellcode), builds a 5-op `OpT program[]` whose `(size, src_off)` fields
reference the payload, encodes each opcode through a forward map (real
opcode → randomized byte), and XOR-encrypts both the bytecode and the
payload with a 32-byte key derived from a fixed seed (`0xC0FFEE`). It
prints a self-contained C++ header with `#pragma once` and four `inline constexpr` symbols: `g_ir_blob`, `g_ir_seed`, `g_ir_payload`, and
`g_ir_payload_size`.
2. **Make.** The Makefile redirects the builder's stdout into
`example/embedded.h`. If `payload.bin` is missing, Make stops cold; if
it changes, embedded.h regenerates and the loader rebuilds.
3. **Loader side.**`example_loader.cpp``#include`s `embedded.h`, copies
`g_ir_blob` into a stack-local mutable buffer (since `execute()`
decrypts in place), and hands it off to `vm.execute(blob, ctx, g_ir_seed)`.
4. **Execute.**The VM:

   - calls `LoaderConfig::decrypt_bytecode` once (XOR the bytecode with the
     derived key),
   - reads each `Op`, looks up its randomized opcode byte in
     `LoaderConfig::opcode_reverse_map`,
   - dispatches through the `constexpr` 256-entry table to the matching
     `Handler<Op>::execute`.
5. **The pipeline runs.** Five ops: `AllocRegion(PAGE_READWRITE)`,
`WritePayload` (copies still-encrypted bytes from `g_ir_payload`),
`DecryptRegion` (XOR in place using the same derived key),
`ProtectRX` (`VirtualProtect` to `PAGE_EXECUTE_READ`), `ExecRegion`
(cast to fn ptr and jump). The shellcode starts running at the end of
step 5.

If the builder's forward map and the loader's reverse map drift, or the
two `derive_key` implementations disagree on a single byte, the whole
thing falls apart immediately: either the bytecode dispatches into
`unknown_op`, or the decrypted shellcode is garbage and the `ExecRegion`
jump dies. That's the contract this example is testing for you ^^.

## Configuration flags

[Permalink: Configuration flags](https://github.com/mochabyte0x/vmkit#configuration-flags)

`vmkit::DefaultConfig` exposes three flags. Override the ones you want,
leave the rest alone:

| Flag | Effect when `true` |
| --- | --- |
| `opcode_randomization` | Decode each opcode through `opcode_reverse_map[...]` |
| `bytecode_xor_encrypted` | Calls `Cfg::decrypt_bytecode(blob, seed)` once before dispatch |
| `per_op_context_encryption` | Wraps each op with `decrypt_context` / `encrypt_context` |

When a flag is `false`, the corresponding hook is **never instantiated**.
No overhead, no symbols, no dead code in the binary. Pretty nice ^^.

## Adding a new opcode

[Permalink: Adding a new opcode](https://github.com/mochabyte0x/vmkit#adding-a-new-opcode)

```
enum class MyOp : std::uint8_t { /* existing... */, NewThing = 7 };

template <> struct vmkit::Handler<MyOp::NewThing> {
    static void execute(MyContext& ctx, const vmkit::Op<MyOp>& op) noexcept {
        // your logic
    }
};

// Then add it to the OpcodeList. Forget this and your opcode silently no-ops at runtime.
// Forget the Handler specialization and the build dies with a static_assert.
vmkit::Vm<MyOp, MyContext, MyCfg, vmkit::OpcodeList</* existing... */, MyOp::NewThing>> vm;
```

## Compile flags for production loaders

[Permalink: Compile flags for production loaders](https://github.com/mochabyte0x/vmkit#compile-flags-for-production-loaders)

The header itself is plain C++20. For an actual loader the typical flag set
looks like:

```
-std=c++20 -O2 -ffreestanding -fno-exceptions -fno-rtti -nostdlib++
```

On MSVC: `/std:c++20 /EHs-c- /GR- /kernel` (or hand-tune; `/kernel` implies
no-exceptions + no-RTTI anyway).

* * *

# Technical explanation

[Permalink: Technical explanation](https://github.com/mochabyte0x/vmkit#technical-explanation)

This part is for anyone who wants to understand _how_ it works, not just
how to use it. Feel free to skip if you only need the API.

## The dispatch table

[Permalink: The dispatch table](https://github.com/mochabyte0x/vmkit#the-dispatch-table)

The classic IR interpreter pattern is one giant `switch` on the opcode
byte. That works, sure, but every new opcode means editing the switch,
and a missing `case` is a silent runtime no-op (which is exactly when you
don't want to find out, btw).

`vmkit` flips that. The `Vm<>` class holds a single static member:

```
static constexpr std::array<Dispatcher, 256> dispatch_table = build_table();
```

`build_table()` is a `constexpr` function that:

1. Initializes all 256 slots to `&unknown_op` (a no-op).
2. For every opcode `Op` listed in `OpcodeList<Ops...>`, sets
`dispatch_table[Op] = &dispatch_to<Op>`.
3. `dispatch_to<Op>` is a `static_assert`-guarded thunk that calls
`Handler<Op>::execute(ctx, op)`.

Step 2 is a fold expression over the parameter pack, built entirely at
compile time:

```
((t[static_cast<std::size_t>(Ops)] = &dispatch_to<Ops>), ...);
```

The result: dispatch is a single indirect call through a table the compiler
already knows about. Modern compilers will frequently devirtualize and
inline it. There's no runtime registration step, no virtual table, no hash
lookup.

## Why specialization beats a switch

[Permalink: Why specialization beats a switch](https://github.com/mochabyte0x/vmkit#why-specialization-beats-a-switch)

`Handler<Op>` is a primary template that's deliberately undefined. When you
write `template<> struct vmkit::Handler<MyOp::Alloc> { ... }`, you're
filling in one slot of a compile-time registry.

The kicker is in `dispatch_to<Op_>`:

```
static_assert(HasHandler<Op_, Ctx, OpType>, "vmkit: missing Handler<Op> specialization for a listed opcode");
Handler<Op_>::execute(ctx, op);
```

`HasHandler` is a concept that probes for `Handler<Op>::execute(ctx, op)`.
If you list an opcode in `OpcodeList<...>` without specializing `Handler<>`
for it, `dispatch_to<Op>` fails to instantiate and the build dies with a
clear message. With a `switch`, that exact same mistake compiles cleanly
and silently no-ops at runtime. Which, again, is _not_ when you want to
find out about it.

## Opcode randomization

[Permalink: Opcode randomization](https://github.com/mochabyte0x/vmkit#opcode-randomization)

By default, the bytecode opcode byte _is_ the real opcode. With
`opcode_randomization = true`, the byte stored in the bytecode is a
randomized encoding instead, and the runtime maps it back through a
256-byte reverse table:

```
std::uint8_t raw = static_cast<std::uint8_t>(op.opcode);
if constexpr (Cfg::opcode_randomization) {
    raw = Cfg::opcode_reverse_map[raw];
}
dispatch_table[raw](ctx, op);
```

There are two halves to this:

- **Builder side** (forward map): real opcode → randomized byte. Each build
picks a fresh permutation seeded from a config value, so identical IR
programs produce different bytecode across builds.
- **Runtime side** (reverse map): randomized byte → real opcode. Embedded
as a `constexpr std::array` in the binary.

The two maps are inverses of each other. The example demonstrates a tiny
hand-rolled permutation; a real builder would produce a random shuffle
keyed off the build seed.

What this buys you: static signatures based on opcode byte sequences become
useless, since every build has a different alphabet. What it doesn't buy
you: protection against execution-trace analysis or symbolic execution.

## Bytecode encryption at rest

[Permalink: Bytecode encryption at rest](https://github.com/mochabyte0x/vmkit#bytecode-encryption-at-rest)

`bytecode_xor_encrypted = true` makes `execute()` call
`Cfg::decrypt_bytecode(blob, seed)` once before the dispatch loop starts.
The header _intentionally_ doesn't ship a crypto routine (that'd be one
more recognizable signature), so you wire in whatever transform matches
your builder.

The `xor_codec::apply` helper in the header is provided for convenience: a
minimal in-place XOR with a key span. For real loaders you'll probably
want at least a seed-derived key, ideally a stream cipher (sry, no
shortcuts here).

`blob` is `std::span<std::uint8_t>`, mutable on purpose, since the
decryption happens in place. If you keep an encrypted copy elsewhere, copy
before calling `execute()`.

## Per-operation context encryption

[Permalink: Per-operation context encryption](https://github.com/mochabyte0x/vmkit#per-operation-context-encryption)

`per_op_context_encryption = true` adds two calls around each opcode:

```
for (i = 0; i < count; ++i) {
    if (i > 0) Cfg::decrypt_context(ctx, i);
    /* dispatch */
    Cfg::encrypt_context(ctx, i + 1);
}
if (count > 0) Cfg::decrypt_context(ctx, count);
```

The pattern is: the loader's mutable state (region pointers, syscall
table, exec method, …) lives _encrypted_ in memory between operations. A
memory dump captured between two ops shows ciphertext, not pointers. Each
op transitions through plaintext for the duration of `Handler<>::execute`,
and gets re-encrypted right after.

The op index gets fed into the encryption hook, so the key can rotate per
op and make static dump analysis even harder.

This is mostly useful against passive memory forensics, btw. Anything
actively hooking your handlers will see plaintext.

## Why everything is `if constexpr`

[Permalink: Why everything is if constexpr](https://github.com/mochabyte0x/vmkit#why-everything-is-if-constexpr)

Each obfuscation feature is gated on a `static constexpr bool`:

```
if constexpr (Cfg::bytecode_xor_encrypted) {
    Cfg::decrypt_bytecode(blob, seed);
}
```

This is _not_ a runtime branch. If the flag is `false`, the entire branch
gets discarded at compile time. `decrypt_bytecode` is never even
instantiated and contributes zero bytes to the binary. A loader that uses
no obfuscation features compiles down to literally the dispatch loop,
nothing else.

Compare with `#ifdef`: this gives you the same dead-code elimination, but
with template-argument granularity. You can have two `Vm<>` instances in
the same binary running different configs, which is something `#ifdef`
just can't do.

## Why C++20 specifically

[Permalink: Why C++20 specifically](https://github.com/mochabyte0x/vmkit#why-c20-specifically)

Three features the design genuinely needs:

1. **`auto` non-type template parameters.** Lets `Handler<MyOp::Alloc>`
work regardless of whether the underlying enum is `int` or `uint8_t`.
Pre-C++17 this would need a template-template wrapper or a macro, neither
of which is fun to read.
2. **Concepts.**`HasHandler` is the cleanest way to say "this opcode has
a valid handler" and produce a diagnostic that's actually readable.
3. **`constexpr std::array` member init via lambda.** The
`opcode_reverse_map` in the example is built by an immediately-invoked
`constexpr` lambda. C++17 could do it via a helper function; C++20 just
lets you write it inline.

The header pulls in only `<array>`, `<cstddef>`, `<cstdint>`, and `<span>`.
All header-only, no allocators, freestanding-compatible.

## Reinterpret-cast on the bytecode

[Permalink: Reinterpret-cast on the bytecode](https://github.com/mochabyte0x/vmkit#reinterpret-cast-on-the-bytecode)

```
const auto* ops = reinterpret_cast<const OpType*>(blob.data());
```

Strict-aliasing pedants will recoil. The real-world story tho:

- The bytecode _is_ an array of `OpType`, just delivered as bytes.
- `OpType` is trivially copyable and standard-layout.
- `std::uint8_t` is allowed to alias other types in practice on every
compiler that ships a Windows loader.

Real loaders get built with `-fno-strict-aliasing` anyway. If you're
targeting something where this genuinely matters, use `std::memcpy` into a
stack-local `OpType` per iteration and the optimizer will collapse it.

## Op layout and alignment

[Permalink: Op layout and alignment](https://github.com/mochabyte0x/vmkit#op-layout-and-alignment)

```
template <typename Opcode, std::size_t U32 = 8, std::size_t U64 = 4>
struct alignas(8) Op { Opcode opcode; std::uint32_t u32[U32]; std::uint64_t u64[U64]; };
```

- `alignas(8)` guarantees the bytecode array is 8-byte aligned, so `u64[]`
reads are aligned without per-op shuffling.
- The slot counts are template parameters, not hardcoded. Bump them up if
your handlers need more operands per op; bump them down if the defaults
are wasteful for your use case.
- All ops in a single `Vm<>` instance are the same size. If you need
variable-length operands (large strings, payload chunks…), put them in a
side table and reference them by offset. `WritePayload` in the example
shows the pattern.

* * *

## Constraints worth knowing

[Permalink: Constraints worth knowing](https://github.com/mochabyte0x/vmkit#constraints-worth-knowing)

- The opcode enum's underlying type must fit in a byte (0..255). Dispatch
table is exactly 256 entries; anything wider doesn't fit.
- `Op<Opcode>` is fixed-size. Variable-length operands go in side tables
referenced by offset.
- `execute()` takes a _mutable_`std::span` because in-place bytecode
decryption rewrites it. Copy first if you want to keep the encrypted form
around.
- Unknown opcodes silently no-op. That's by design. Easy to drop in junk
opcodes for control-flow obfuscation. Replace `unknown_op` in
`vm_loader.hpp` with a trap if you'd rather hard-fail.

## Going beyond the template

[Permalink: Going beyond the template](https://github.com/mochabyte0x/vmkit#going-beyond-the-template)

The template covers the VM core. Production loaders typically build out:

- Real Win32 / NTAPI hooks for alloc / protect / exec
- Indirect syscalls (Hell's gate variants and friends)
- API hashing tables and dynamic resolution
- Anti-analysis checks
- Callstack spoofing
- Multiple execution methods
- Payload encryption
- Transport obfuscation
- Section-entropy padding and PE checksum patching

All of those slot in either as `Handler<>` bodies, as overrides on a
custom `Cfg`, or as builder-side preprocessing. None of them require
touching the VM core in `vm_loader.hpp`. As always, feel free to bend the
template to your use case ^^.

# Credits

[Permalink: Credits](https://github.com/mochabyte0x/vmkit#credits)

```
Secret Club: https://secret.club/2023/12/24/riscy-business.html
Infinity Curve: https://infinitycurve.org/products/havoc-professional
```

## About

A header-only, freestanding C++20 template for IR-bytecode VM loaders


### Resources

[Readme](https://github.com/mochabyte0x/vmkit#readme-ov-file)

### License

[BSD-2-Clause license](https://github.com/mochabyte0x/vmkit#BSD-2-Clause-1-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/mochabyte0x/vmkit).

[Activity](https://github.com/mochabyte0x/vmkit/activity)

### Stars

[**26**\\
stars](https://github.com/mochabyte0x/vmkit/stargazers)

### Watchers

[**0**\\
watching](https://github.com/mochabyte0x/vmkit/watchers)

### Forks

[**0**\\
forks](https://github.com/mochabyte0x/vmkit/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fmochabyte0x%2Fvmkit&report=mochabyte0x+%28user%29)

## [Releases](https://github.com/mochabyte0x/vmkit/releases)

No releases published

## [Packages\  0](https://github.com/users/mochabyte0x/packages?repo_name=vmkit)

No packages published

## [Contributors\  1](https://github.com/mochabyte0x/vmkit/graphs/contributors)

- [![@mochabyte0x](https://avatars.githubusercontent.com/u/115954804?s=64&v=4)](https://github.com/mochabyte0x)[**mochabyte0x** MochaByte](https://github.com/mochabyte0x)

## Languages

- [C++91.8%](https://github.com/mochabyte0x/vmkit/search?l=c%2B%2B)
- [Makefile8.2%](https://github.com/mochabyte0x/vmkit/search?l=makefile)

You can’t perform that action at this time.