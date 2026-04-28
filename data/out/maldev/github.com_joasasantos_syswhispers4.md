# https://github.com/JoasASantos/SysWhispers4

[Skip to content](https://github.com/JoasASantos/SysWhispers4#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/JoasASantos/SysWhispers4) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/JoasASantos/SysWhispers4) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/JoasASantos/SysWhispers4) to refresh your session.Dismiss alert

{{ message }}

[JoasASantos](https://github.com/JoasASantos)/ **[SysWhispers4](https://github.com/JoasASantos/SysWhispers4)** Public

- [Notifications](https://github.com/login?return_to=%2FJoasASantos%2FSysWhispers4) You must be signed in to change notification settings
- [Fork\\
61](https://github.com/login?return_to=%2FJoasASantos%2FSysWhispers4)
- [Star\\
461](https://github.com/login?return_to=%2FJoasASantos%2FSysWhispers4)


main

[**1** Branch](https://github.com/JoasASantos/SysWhispers4/branches) [**0** Tags](https://github.com/JoasASantos/SysWhispers4/tags)

[Go to Branches page](https://github.com/JoasASantos/SysWhispers4/branches)[Go to Tags page](https://github.com/JoasASantos/SysWhispers4/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![JoasASantos](https://avatars.githubusercontent.com/u/34966120?v=4&size=40)](https://github.com/JoasASantos)[JoasASantos](https://github.com/JoasASantos/SysWhispers4/commits?author=JoasASantos)<br>[Merge pull request](https://github.com/JoasASantos/SysWhispers4/commit/da74852278bbf945fcde237f74a6ffdac25d7f8c) [#1](https://github.com/JoasASantos/SysWhispers4/pull/1) [from Whispergate/main](https://github.com/JoasASantos/SysWhispers4/commit/da74852278bbf945fcde237f74a6ffdac25d7f8c)<br>last monthMar 7, 2026<br>[da74852](https://github.com/JoasASantos/SysWhispers4/commit/da74852278bbf945fcde237f74a6ffdac25d7f8c) · last monthMar 7, 2026<br>## History<br>[7 Commits](https://github.com/JoasASantos/SysWhispers4/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/JoasASantos/SysWhispers4/commits/main/) 7 Commits |
| [core](https://github.com/JoasASantos/SysWhispers4/tree/main/core "core") | [core](https://github.com/JoasASantos/SysWhispers4/tree/main/core "core") | [Fixed prefix generator and nested comments in codebase](https://github.com/JoasASantos/SysWhispers4/commit/5547228e32721629d83866812499b0f392cab145 "Fixed prefix generator and nested comments in codebase") | last monthMar 7, 2026 |
| [data](https://github.com/JoasASantos/SysWhispers4/tree/main/data "data") | [data](https://github.com/JoasASantos/SysWhispers4/tree/main/data "data") | [feat: add advanced evasion techniques and new SSN resolution methods](https://github.com/JoasASantos/SysWhispers4/commit/01c6530084a34e2ca47f9a789294e1c24e4e6951 "feat: add advanced evasion techniques and new SSN resolution methods  New SSN Resolution Methods: - SyscallsFromDisk: load clean ntdll from \KnownDlls to bypass ALL hooks - RecycledGate: FreshyCalls + opcode cross-validation (most resilient) - HW Breakpoint: hardware breakpoints + VEH to extract SSN  New Evasion Techniques: - AMSI bypass (--amsi-bypass): patches AmsiScanBuffer - ntdll unhooking (--unhook-ntdll): remaps clean .text from KnownDlls - Anti-debugging (--anti-debug): PEB, timing, heap flags, debug port,   instrumentation callback checks - Sleep encryption (--sleep-encrypt): Ekko-style XOR .text during sleep  Enhanced Obfuscation: - 14 junk instruction variants (up from 4) - Compile-time string encryption helpers - Random variable name generation - CRC32 and FNV-1a hash alternatives  New Presets: - stealth: maximum evasion combo (32 functions) - file_ops: NT file I/O operations (7 functions) - transaction: process doppelganging support (7 functions)  New NT Functions (64 total, up from 48): - NtOpenSection, NtCreateTransaction, NtRollbackTransaction,   NtCommitTransaction, NtSetInformationVirtualMemory, NtCreateEvent,   NtSetEvent, NtResetEvent, NtCreateTimer, NtSetTimer, NtTestAlert,   NtAlertResumeThread, NtAlertThread, NtWriteFile, NtReadFile,   NtDeleteFile  Other improvements: - SSN decryption now properly handled in ASM stubs - Enhanced Tartarus' Gate with short JMP (EB) hook detection - FindSection helper for PE section parsing - GetOwnImageBase helper for self-referencing operations  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>") | last monthMar 4, 2026 |
| [examples](https://github.com/JoasASantos/SysWhispers4/tree/main/examples "examples") | [examples](https://github.com/JoasASantos/SysWhispers4/tree/main/examples "examples") | [Initial release: SysWhispers4 — advanced Windows syscall stub generator](https://github.com/JoasASantos/SysWhispers4/commit/562c115e6c0e09d1d777c9118a01be2aba35259c "Initial release: SysWhispers4 — advanced Windows syscall stub generator  - 5 SSN resolution methods: Static, FreshyCalls, Hell's Gate, Halo's Gate, Tartarus' Gate - 4 invocation methods: Embedded (direct), Indirect, Randomized (RDTSC entropy), Egg hunt - Architecture support: x64, x86, WoW64, ARM64 (SVC #0 / w8) - Compiler support: MSVC (MASM ml64.exe), MinGW (GAS inline asm), Clang - XOR SSN encryption at rest (randomized key per generation) - ETW user-mode bypass (ntdll!EtwEventWrite patch) - Call-stack spoofing trampoline (ntdll return address) - PEB-walk ntdll resolution (no Win32 API calls) - EAT parsing with DJB2 compile-time hashes (no string comparisons) - Fix: rdtsc clobbers rdx (arg2) in randomized stub — save rdx→r11 before rdtsc - 48 NT functions across 5 presets (common, injection, evasion, token, all) - j00ru syscall table update script (26 Windows builds Win7–Win11 24H2) - Comprehensive README with SW1/SW2/SW3/SW4 feature comparison matrix  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>") | 2 months agoFeb 22, 2026 |
| [scripts](https://github.com/JoasASantos/SysWhispers4/tree/main/scripts "scripts") | [scripts](https://github.com/JoasASantos/SysWhispers4/tree/main/scripts "scripts") | [fix(update\_syscall\_table): handle j00ru's human-readable CSV header f…](https://github.com/JoasASantos/SysWhispers4/commit/300ce4b597fc1f64ceff133274b82910a04ec297 "fix(update_syscall_table): handle j00ru's human-readable CSV header format  j00ru/windows-syscalls updated both x64 and x86 CSVs to use human-readable column headers (\"Windows 10 (1903)\", \"Windows NT 4.0 (SP3)\") instead of the dotted version strings (\"10.0.19041.1\") the script assumed.  Changes: - Replace _version_to_build() with _parse_header_col() that handles both   the human-readable format and legacy dotted strings as a fallback - Add VER_MAP: unified label→(build_key, display_label) covering all 82   columns across x64 (XP SP1 → Win11 25H2) and x86 (NT 3.1 → Win10 22H2) - Win10/Win11 columns use actual build numbers (19041, 22000, 26100…) for   cross-arch consistency; legacy columns use descriptive keys (xp_sp2, 7_sp1) - Add data/syscalls_nt_x86.json (513 Nt* functions, NT 3.1 → Win10 22H2) - Refresh data/syscalls_nt_x64.json (506 functions, XP SP1 → Win11 25H2)   with correct Win11 / Server 2022/2025 build keys  Fixes: ValueError: invalid literal for int() with base 10: 'Windows NT 3'  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>") | 2 months agoFeb 22, 2026 |
| [.gitignore](https://github.com/JoasASantos/SysWhispers4/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/JoasASantos/SysWhispers4/blob/main/.gitignore ".gitignore") | [Fixed prefix generator and nested comments in codebase](https://github.com/JoasASantos/SysWhispers4/commit/5547228e32721629d83866812499b0f392cab145 "Fixed prefix generator and nested comments in codebase") | last monthMar 7, 2026 |
| [README.md](https://github.com/JoasASantos/SysWhispers4/blob/main/README.md "README.md") | [README.md](https://github.com/JoasASantos/SysWhispers4/blob/main/README.md "README.md") | [docs: comprehensive README update for v4.1 features](https://github.com/JoasASantos/SysWhispers4/commit/a827940811f4e6ec2d1b35a50d27787b35c4f6b2 "docs: comprehensive README update for v4.1 features  - Document 3 new SSN resolution methods (SyscallsFromDisk, RecycledGate, HW Breakpoint) - Document 5 new evasion techniques (AMSI bypass, ntdll unhooking, anti-debug,   sleep encryption, enhanced obfuscation) - Add recommended configurations section (red team, CTF, heavy EDR) - Update feature comparison matrix with all new capabilities - Update function count (48 → 64) and preset list (5 → 8) - Add evasion techniques deep dive section - Add project structure overview - Add integration example with full evasion chain  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>") | last monthMar 4, 2026 |
| [syswhispers.py](https://github.com/JoasASantos/SysWhispers4/blob/main/syswhispers.py "syswhispers.py") | [syswhispers.py](https://github.com/JoasASantos/SysWhispers4/blob/main/syswhispers.py "syswhispers.py") | [Fixed prefix generator and nested comments in codebase](https://github.com/JoasASantos/SysWhispers4/commit/5547228e32721629d83866812499b0f392cab145 "Fixed prefix generator and nested comments in codebase") | last monthMar 7, 2026 |
| View all files |

## Repository files navigation

# SysWhispers4

[Permalink: SysWhispers4](https://github.com/JoasASantos/SysWhispers4#syswhispers4)

> **AV/EDR evasion via direct and indirect system calls**
> Windows NT 3.1 through Windows 11 24H2 · x64 · x86 · WoW64 · ARM64

SysWhispers4 is a Python-based syscall stub generator that produces C/ASM code for invoking NT kernel functions directly, bypassing user-mode hooks placed by AV/EDR products on `ntdll.dll`.

Built on the lineage of [SysWhispers](https://github.com/jthuraisamy/SysWhispers) → [SysWhispers2](https://github.com/jthuraisamy/SysWhispers2) → [SysWhispers3](https://github.com/klezVirus/SysWhispers3), this version adds the most comprehensive set of SSN resolution strategies, invocation methods, and evasion capabilities to date.

* * *

## Evolution: SysWhispers 1 → 4

[Permalink: Evolution: SysWhispers 1 → 4](https://github.com/JoasASantos/SysWhispers4#evolution-syswhispers-1--4)

### Feature Comparison Matrix

[Permalink: Feature Comparison Matrix](https://github.com/JoasASantos/SysWhispers4#feature-comparison-matrix)

| Feature | SW1 | SW2 | SW3 | **SW4** |
| --- | :-: | :-: | :-: | :-: |
| **SSN Resolution** |  |  |  |  |
| Static embedded table | ✅ | ✅ | ✅ | ✅ |
| Hell's Gate (runtime ntdll parse) | ❌ | ✅ | ✅ | ✅ |
| Halo's Gate (hook-neighbor scan) | ❌ | ❌ | ✅ | ✅ |
| Tartarus' Gate (near+far JMP) | ❌ | ❌ | Partial | ✅ |
| FreshyCalls (sort-by-VA) | ❌ | ❌ | ❌ | **✅ New** |
| SyscallsFromDisk (clean ntdll from KnownDlls) | ❌ | ❌ | ❌ | **✅ New** |
| RecycledGate (FreshyCalls + opcode validation) | ❌ | ❌ | ❌ | **✅ New** |
| HW Breakpoint (DR registers + VEH) | ❌ | ❌ | ❌ | **✅ New** |
| Static + dynamic fallback | ❌ | ❌ | ❌ | **✅ New** |
| **Invocation Methods** |  |  |  |  |
| Embedded (direct `syscall`) | ✅ | ✅ | ✅ | ✅ |
| Indirect (jmp to ntdll gadget) | ❌ | ❌ | ✅ | ✅ |
| Randomized indirect (per-call entropy) | ❌ | ❌ | Partial† | **✅ Fixed** |
| Egg hunt (no static `0F 05` on disk) | ❌ | ❌ | ✅ | ✅ |
| **Architecture** |  |  |  |  |
| x64 | ✅ | ✅ | ✅ | ✅ |
| x86 (32-bit sysenter) | ❌ | ❌ | ✅ | ✅ |
| WoW64 (Heaven's Gate) | ❌ | ❌ | ✅ | ✅ |
| ARM64 (`SVC #0`, `w8`) | ❌ | ❌ | ❌ | **✅ New** |
| **Compiler Support** |  |  |  |  |
| MSVC (MASM) | ✅ | ✅ | ✅ | ✅ |
| MinGW / GCC (GAS inline) | ❌ | ❌ | ✅ | ✅ |
| Clang (GAS inline) | ❌ | ❌ | ✅ | ✅ |
| **Evasion / Obfuscation** |  |  |  |  |
| Function name hashing | ❌ | ✅ | ✅ | ✅ (DJB2) |
| Stub ordering randomization | ❌ | ❌ | ❌ | **✅ New** |
| Junk instruction injection (14 variants) | ❌ | ❌ | ❌ | **✅ New** |
| XOR-encrypted SSN at rest | ❌ | ❌ | ❌ | **✅ New** |
| Gadget pool (up to 64 gadgets) | ❌ | ❌ | ❌ | **✅ New** |
| Call stack spoof helper | ❌ | ❌ | ❌ | **✅ New** |
| User-mode ETW bypass | ❌ | ❌ | ❌ | **✅ New** |
| AMSI bypass | ❌ | ❌ | ❌ | **✅ New** |
| ntdll unhooking (remap from KnownDlls) | ❌ | ❌ | ❌ | **✅ New** |
| Anti-debugging (6 checks) | ❌ | ❌ | ❌ | **✅ New** |
| Sleep encryption (Ekko-style) | ❌ | ❌ | ❌ | **✅ New** |
| **Syscall Table** |  |  |  |  |
| Windows XP → Win10 20H2 | ✅ | ✅ | ✅ | ✅ |
| Windows 11 21H2–24H2 | ❌ | ❌ | Partial | **✅ Full** |
| Windows Server 2022/2025 | ❌ | ❌ | ❌ | **✅ New** |
| Auto-update from j00ru | ❌ | ❌ | ❌ | **✅ New** |
| **Tool** |  |  |  |  |
| Supported NT functions | ~12 | ~12 | ~35 | **64** |
| Python version | 2/3 | 3 | 3 | **3.10+** |
| Type annotations | ❌ | ❌ | Partial | **✅ Full** |

> † SW3's randomized method had a register-corruption bug — `RDTSC` overwrites `edx` (arg2). SW4 correctly saves `rdx → r11` before `rdtsc` and restores it without touching the stack.

* * *

## What's New in v4.1

[Permalink: What's New in v4.1](https://github.com/JoasASantos/SysWhispers4#whats-new-in-v41)

### New SSN Resolution Methods

[Permalink: New SSN Resolution Methods](https://github.com/JoasASantos/SysWhispers4#new-ssn-resolution-methods)

#### SyscallsFromDisk (`--resolve from_disk`)

[Permalink: SyscallsFromDisk (--resolve from_disk)](https://github.com/JoasASantos/SysWhispers4#syscallsfromdisk---resolve-from_disk)

Maps a **clean copy** of ntdll from `\KnownDlls\ntdll.dll` and reads SSNs from the unhooked `.text` section. Completely bypasses **all** inline hooks — the EDR never sees the read.

```
// Flow: NtOpenSection → NtMapViewOfSection → read clean SSNs → NtUnmapViewOfSection
// SSNs come from the on-disk image, guaranteed hook-free
SW4_SyscallsFromDisk(pNtdll);
```

#### RecycledGate (`--resolve recycled`)

[Permalink: RecycledGate (--resolve recycled)](https://github.com/JoasASantos/SysWhispers4#recycledgate---resolve-recycled)

Combines the reliability of FreshyCalls (sort-by-VA) with opcode validation from Hell's Gate. For each function:

1. Get candidate SSN from sorted position (FreshyCalls)
2. If stub is clean, verify SSN matches opcode (double-check)
3. If stub is hooked, trust the sorted-index SSN (hook-resistant)

**The most resilient method available** — even if hooks reorder stubs or modify opcodes, the VA-sort gives the correct SSN.

#### HW Breakpoint (`--resolve hw_breakpoint`)

[Permalink: HW Breakpoint (--resolve hw_breakpoint)](https://github.com/JoasASantos/SysWhispers4#hw-breakpoint---resolve-hw_breakpoint)

Uses **debug registers** (DR0–DR3) and a Vectored Exception Handler (VEH) to extract SSNs without reading the (potentially hooked) function bytes:

1. Set DR0 = address of `syscall` instruction in ntdll stub
2. Register VEH handler
3. Call into the stub — VEH catches `EXCEPTION_SINGLE_STEP`
4. At breakpoint, EAX contains the SSN — capture it
5. Clear DR0, skip the syscall, continue

Works even when hooks redirect execution, because the breakpoint fires after `mov eax, <SSN>`.

### New Evasion Techniques

[Permalink: New Evasion Techniques](https://github.com/JoasASantos/SysWhispers4#new-evasion-techniques)

#### AMSI Bypass (`--amsi-bypass`)

[Permalink: AMSI Bypass (--amsi-bypass)](https://github.com/JoasASantos/SysWhispers4#amsi-bypass---amsi-bypass)

Patches `amsi.dll!AmsiScanBuffer` to return `E_INVALIDARG`, making AMSI think scan arguments are invalid. If `amsi.dll` isn't loaded, returns success (nothing to patch).

```
SW4_PatchAmsi();  // Call early, before any suspicious operations
```

#### ntdll Unhooking (`--unhook-ntdll`)

[Permalink: ntdll Unhooking (--unhook-ntdll)](https://github.com/JoasASantos/SysWhispers4#ntdll-unhooking---unhook-ntdll)

Maps a clean copy of ntdll from `\KnownDlls\` and **overwrites the hooked `.text` section** with the clean bytes:

```
// Call BEFORE SW4_Initialize() for best results
SW4_UnhookNtdll();     // Remove ALL inline hooks from ntdll
SW4_Initialize();       // Now FreshyCalls/Hell's Gate reads clean stubs
```

This completely removes all inline hooks from ntdll, making subsequent NT API calls go through original code paths.

#### Anti-Debugging (`--anti-debug`)

[Permalink: Anti-Debugging (--anti-debug)](https://github.com/JoasASantos/SysWhispers4#anti-debugging---anti-debug)

Performs 6 checks to detect debugger/analysis presence:

| Check | Technique | Detects |
| --- | --- | --- |
| 1 | `PEB.BeingDebugged` | Standard debugger attachment |
| 2 | `NtGlobalFlag` (0x70) | Heap debug flags set by debuggers |
| 3 | `RDTSC` timing delta | Single-stepping / tracing |
| 4 | `NtQueryInformationProcess(ProcessDebugPort)` | Kernel debug port |
| 5 | Heap flags analysis | Debug heap indicators |
| 6 | Instrumentation callback detection | EDR instrumentation hooks |

```
if (!SW4_AntiDebugCheck()) {
    // Debugger detected — bail out or take evasive action
    ExitProcess(0);
}
```

#### Sleep Encryption (`--sleep-encrypt`)

[Permalink: Sleep Encryption (--sleep-encrypt)](https://github.com/JoasASantos/SysWhispers4#sleep-encryption---sleep-encrypt)

**Ekko-style** memory encryption during sleep to evade periodic memory scanners:

1. Generate random XOR key via `RDTSC`
2. XOR-encrypt own `.text` section
3. Set waitable timer + queue APC to decrypt
4. Sleep in alertable state
5. Timer fires → APC decrypts `.text` → execution resumes

```
// Instead of Sleep(5000), use:
SW4_SleepEncrypt(5000);  // .text is encrypted during the entire sleep
```

Defeats:

- Memory scanners during sleep (code is encrypted gibberish)
- Periodic module scans (signatures won't match)
- YARA/signature scans on in-memory PE

* * *

## All Features (Existing + New)

[Permalink: All Features (Existing + New)](https://github.com/JoasASantos/SysWhispers4#all-features-existing--new)

### SSN Resolution Methods (8 total)

[Permalink: SSN Resolution Methods (8 total)](https://github.com/JoasASantos/SysWhispers4#ssn-resolution-methods-8-total)

| Method | Flag | Hook Resistance | Speed | Notes |
| --- | --- | :-: | :-: | --- |
| Static | `--resolve static` | None | Fastest | Embedded j00ru table, no runtime parsing |
| Hell's Gate | `--resolve hells_gate` | Low | Fast | Reads opcode bytes — fails if hooked |
| Halo's Gate | `--resolve halos_gate` | Medium | Fast | Neighbor scan (±8 stubs) |
| Tartarus' Gate | `--resolve tartarus` | High | Fast | Detects E9/FF25/EB/CC hooks, ±16 neighbors |
| FreshyCalls | `--resolve freshycalls` | **Very High** | Medium | Sort by VA — doesn't read function bytes |
| SyscallsFromDisk | `--resolve from_disk` | **Maximum** | Slow | Maps clean ntdll from disk |
| RecycledGate | `--resolve recycled` | **Maximum** | Medium | FreshyCalls + opcode cross-validation |
| HW Breakpoint | `--resolve hw_breakpoint` | **Maximum** | Slow | DR registers + VEH |

### Invocation Methods (4 total)

[Permalink: Invocation Methods (4 total)](https://github.com/JoasASantos/SysWhispers4#invocation-methods-4-total)

| Method | Flag | RIP in ntdll | Syscall on Disk | Random per Call |
| --- | --- | :-: | :-: | :-: |
| Embedded | `--method embedded` | ❌ | ✅ | ❌ |
| Indirect | `--method indirect` | ✅ | ❌ | ❌ |
| Randomized | `--method randomized` | ✅ | ❌ | ✅ (64 gadgets) |
| Egg Hunt | `--method egg` | ❌ | ❌ | ❌ |

### Evasion Options (8 total)

[Permalink: Evasion Options (8 total)](https://github.com/JoasASantos/SysWhispers4#evasion-options-8-total)

| Feature | Flag | Description |
| --- | --- | --- |
| Obfuscation | `--obfuscate` | Stub reordering + 14 junk instruction variants |
| SSN Encryption | `--encrypt-ssn` | XOR with random compile-time key |
| Stack Spoofing | `--stack-spoof` | Synthetic return address from ntdll |
| ETW Bypass | `--etw-bypass` | Patch `EtwEventWrite` to return ACCESS\_DENIED |
| AMSI Bypass | `--amsi-bypass` | Patch `AmsiScanBuffer` to return E\_INVALIDARG |
| ntdll Unhooking | `--unhook-ntdll` | Remap clean `.text` from `\KnownDlls\` |
| Anti-Debug | `--anti-debug` | 6 detection checks (PEB, timing, heap, etc.) |
| Sleep Encryption | `--sleep-encrypt` | Ekko-style XOR `.text` during sleep |

* * *

## Quick Start

[Permalink: Quick Start](https://github.com/JoasASantos/SysWhispers4#quick-start)

```
git clone https://github.com/CyberSecurityUP/SysWhispers4
cd SysWhispers4

# Optional: update syscall table from j00ru (for --resolve static)
python scripts/update_syscall_table.py

# Common preset — FreshyCalls + direct syscall (recommended start)
python syswhispers.py --preset common

# Injection preset — indirect via Tartarus' Gate
python syswhispers.py --preset injection --method indirect --resolve tartarus

# Maximum evasion: all techniques combined
python syswhispers.py --preset stealth \
    --method randomized --resolve recycled \
    --obfuscate --encrypt-ssn --stack-spoof \
    --etw-bypass --amsi-bypass --unhook-ntdll \
    --anti-debug --sleep-encrypt

# Clean ntdll from disk — bypasses ALL hooks
python syswhispers.py --preset injection \
    --method indirect --resolve from_disk \
    --unhook-ntdll

# Hardware breakpoint SSN extraction
python syswhispers.py --functions NtAllocateVirtualMemory,NtCreateThreadEx \
    --resolve hw_breakpoint

# Egg hunt (no syscall opcode on disk)
python syswhispers.py \
    --functions NtAllocateVirtualMemory,NtWriteVirtualMemory,NtCreateThreadEx \
    --method egg --resolve halos_gate

# ARM64 (Windows on ARM)
python syswhispers.py --preset common --arch arm64

# x86 / WoW64
python syswhispers.py --preset injection --arch x86

# MinGW / Clang (GAS inline assembly)
python syswhispers.py --preset common --compiler mingw
```

* * *

## Command-Line Reference

[Permalink: Command-Line Reference](https://github.com/JoasASantos/SysWhispers4#command-line-reference)

```
python syswhispers.py [OPTIONS]

Function selection (at least one required):
  -p, --preset PRESET      common | injection | evasion | token | stealth |
                           file_ops | transaction | all
  -f, --functions FUNCS    NtAllocateVirtualMemory,NtCreateThreadEx,...

Target:
  -a, --arch ARCH          x64 (default) | x86 | wow64 | arm64
  -c, --compiler COMPILER  msvc (default) | mingw | clang

Techniques:
  -m, --method METHOD      embedded (default) | indirect | randomized | egg
  -r, --resolve RESOLVE    freshycalls (default) | static | hells_gate |
                           halos_gate | tartarus | from_disk | recycled |
                           hw_breakpoint

Evasion / Obfuscation:
  --obfuscate              Randomize stub order + inject junk instructions
  --encrypt-ssn            XOR-encrypt SSN table at rest
  --stack-spoof            Include synthetic call stack frame helper
  --etw-bypass             Include user-mode ETW patch function
  --amsi-bypass            Include AMSI bypass (AmsiScanBuffer patch)
  --unhook-ntdll           Include ntdll unhooking (remap from KnownDlls)
  --anti-debug             Include anti-debugging checks (6 techniques)
  --sleep-encrypt          Include Ekko-style sleep encryption

Output:
  --prefix PREFIX          Symbol prefix (default: SW4)
  -o, --out-file OUTFILE   Output filename base (default: SW4Syscalls)
  --out-dir OUTDIR         Output directory (default: .)

Info:
  --list-functions         Print all 64 supported NT functions and exit
  --list-presets           Print all preset definitions and exit
  -v, --verbose            Verbose output / traceback on error
```

* * *

## Generated Files

[Permalink: Generated Files](https://github.com/JoasASantos/SysWhispers4#generated-files)

| File | Purpose |
| --- | --- |
| `SW4Syscalls_Types.h` | NT type definitions — structures, enums, typedefs |
| `SW4Syscalls.h` | Function prototypes + `SW4_Initialize()` \+ evasion API declarations |
| `SW4Syscalls.c` | Runtime SSN resolution + helper functions + evasion implementations |
| `SW4Syscalls.asm` | MASM syscall stubs (MSVC) |
| `SW4Syscalls_stubs.c` | GAS inline assembly stubs (MinGW / Clang) |

* * *

## Integration (MSVC)

[Permalink: Integration (MSVC)](https://github.com/JoasASantos/SysWhispers4#integration-msvc)

1. Add all 4 files to your Visual Studio project
2. Enable MASM: **Project → Build Customizations → masm (.targets)**
3. Call initialization functions at startup

```
#include "SW4Syscalls.h"

int main(void) {
    // Step 1 (optional): Remove ALL hooks from ntdll
    // Call BEFORE Initialize for best results
    SW4_UnhookNtdll();

    // Step 2: Resolve SSNs (required for all dynamic methods)
    if (!SW4_Initialize()) return 1;

    // Step 3 (optional): Evasion patches
    SW4_PatchEtw();    // Suppress user-mode ETW events
    SW4_PatchAmsi();   // Bypass AMSI scanning

    // Step 4 (optional): Verify clean environment
    if (!SW4_AntiDebugCheck()) {
        // Debugger detected — take evasive action
        return 0;
    }

    // Use NT functions directly — all via syscall, no API hooks
    PVOID base = NULL;
    SIZE_T size = 0x1000;
    NTSTATUS st = SW4_NtAllocateVirtualMemory(
        GetCurrentProcess(), &base, 0, &size,
        MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE
    );

    // Use encrypted sleep instead of Sleep()
    // SW4_SleepEncrypt(5000);  // .text encrypted during sleep

    return NT_SUCCESS(st) ? 0 : 1;
}
```

### Integration (MinGW/Clang)

[Permalink: Integration (MinGW/Clang)](https://github.com/JoasASantos/SysWhispers4#integration-mingwclang)

```
x86_64-w64-mingw32-gcc -masm=intel \
    example.c SW4Syscalls.c SW4Syscalls_stubs.c \
    -o example.exe -lntdll
```

* * *

## SSN Resolution Techniques

[Permalink: SSN Resolution Techniques](https://github.com/JoasASantos/SysWhispers4#ssn-resolution-techniques)

### Static

[Permalink: Static](https://github.com/JoasASantos/SysWhispers4#static)

Embeds syscall numbers from the bundled j00ru table at generation time. No runtime ntdll parsing — fastest and simplest. An embedded table is a detection signal; use dynamic methods for stealth.

### FreshyCalls _(default — recommended)_

[Permalink: FreshyCalls (default — recommended)](https://github.com/JoasASantos/SysWhispers4#freshycalls-default--recommended)

Sorts all `Nt*` exports from ntdll by virtual address. Sorted index = SSN. Works even if **every**`Nt*` stub is hooked — reads only VAs, not function bytes.

### Hell's Gate

[Permalink: Hell's Gate](https://github.com/JoasASantos/SysWhispers4#hells-gate)

Reads the `mov eax, <SSN>` opcode directly from each ntdll stub:

```
4C 8B D1 B8 [SSN_lo] [SSN_hi] 00 00
```

Fails when the stub's first bytes are overwritten by an EDR hook.

### Halo's Gate

[Permalink: Halo's Gate](https://github.com/JoasASantos/SysWhispers4#halos-gate)

Extends Hell's Gate: when a stub is hooked, scans neighboring stubs (±8) in the sorted export list and infers the SSN by ±offset arithmetic.

### Tartarus' Gate

[Permalink: Tartarus' Gate](https://github.com/JoasASantos/SysWhispers4#tartarus-gate)

Extends Halo's Gate to detect **all** EDR hook patterns:

- `E9 xx xx xx xx` — near relative JMP
- `FF 25 xx xx xx xx` — far absolute JMP via memory
- `EB xx` — short JMP
- `CC` — int3 breakpoint
- `E8 xx xx xx xx` — call (rare)

Scans up to 16 neighbors in both directions.

### SyscallsFromDisk _(bypasses ALL hooks)_

[Permalink: SyscallsFromDisk (bypasses ALL hooks)](https://github.com/JoasASantos/SysWhispers4#syscallsfromdisk-bypasses-all-hooks)

Maps a completely clean copy of ntdll from `\KnownDlls\ntdll.dll` and reads SSNs from the pristine `.text` section. The EDR hooks are irrelevant — we never read from the hooked copy.

### RecycledGate _(most resilient)_

[Permalink: RecycledGate (most resilient)](https://github.com/JoasASantos/SysWhispers4#recycledgate-most-resilient)

Combines FreshyCalls and Hell's Gate for maximum confidence:

- Primary: sorted-by-VA index (FreshyCalls)
- Validation: opcode cross-check if stub is clean
- Fallback: trust VA sort if stub is hooked

Even if an EDR modifies both hooks AND export table entries, the VA-sort still provides the correct SSN.

### HW Breakpoint _(advanced)_

[Permalink: HW Breakpoint (advanced)](https://github.com/JoasASantos/SysWhispers4#hw-breakpoint-advanced)

Uses CPU debug registers (DR0–DR3) to set hardware breakpoints on syscall instructions inside ntdll. A Vectored Exception Handler (VEH) catches the breakpoint and reads the SSN from EAX at that point. Does not read any potentially-tampered bytes.

* * *

## Invocation Methods

[Permalink: Invocation Methods](https://github.com/JoasASantos/SysWhispers4#invocation-methods)

### Embedded — Direct Syscall

[Permalink: Embedded — Direct Syscall](https://github.com/JoasASantos/SysWhispers4#embedded--direct-syscall)

`syscall` lives in your stub. At kernel entry, RIP points into your PE — detectable by EDRs checking non-ntdll RIP.

### Indirect

[Permalink: Indirect](https://github.com/JoasASantos/SysWhispers4#indirect)

Jumps to a pre-located `syscall;ret` gadget **inside ntdll.dll**. At kernel entry, RIP appears to be inside ntdll — identical to a legitimate API call.

### Randomized Indirect

[Permalink: Randomized Indirect](https://github.com/JoasASantos/SysWhispers4#randomized-indirect)

Like Indirect, but selects a **random** gadget from a pool of up to 64 on every call. Defeats EDR heuristics that whitelist specific ntdll gadget addresses. Uses `RDTSC` for entropy — no API call needed.

```
SW4_NtAllocateVirtualMemory PROC
    mov  r10, rcx          ; arg1 → r10 (syscall ABI)
    mov  r11, rdx          ; SAVE rdx — rdtsc trashes edx!
    rdtsc                   ; eax:edx = TSC (clobbers edx)
    xor  eax, edx           ; mix
    and  eax, 63            ; pool index (0..63)
    lea  rcx, [SW4_GadgetPool]
    mov  rcx, QWORD PTR [rcx + rax*8]   ; random gadget
    mov  rdx, r11           ; RESTORE rdx
    mov  eax, DWORD PTR [SW4_SsnTable + N*4]
    jmp  rcx               ; → random ntdll syscall;ret
SW4_NtAllocateVirtualMemory ENDP
```

### Egg Hunt

[Permalink: Egg Hunt](https://github.com/JoasASantos/SysWhispers4#egg-hunt)

Stubs contain an 8-byte random egg marker in place of `syscall`. `SW4_HatchEggs()` scans the `.text` section at startup and replaces each egg with `0F 05 90 90 90 90 90 90`. **No `syscall` opcode appears in the binary on disk.**

* * *

## EDR Detection Landscape

[Permalink: EDR Detection Landscape](https://github.com/JoasASantos/SysWhispers4#edr-detection-landscape)

| Detection Vector | Embedded | Indirect | Randomized | Egg |
| --- | :-: | :-: | :-: | :-: |
| User-mode hook bypass | ✅ | ✅ | ✅ | ✅ |
| RIP inside ntdll at syscall | ❌ | ✅ | ✅ | ❌ |
| No `0F 05` in binary on disk | ✅¹ | ✅ | ✅ | **✅** |
| Random gadget per call | ❌ | ❌ | **✅** | ❌ |
| Clean call stack | with `--stack-spoof` | with `--stack-spoof` | with `--stack-spoof` | with `--stack-spoof` |
| Memory scan evasion during sleep | with `--sleep-encrypt` | with `--sleep-encrypt` | with `--sleep-encrypt` | with `--sleep-encrypt` |
| Kernel ETW-Ti bypass | ❌ | ❌ | ❌ | ❌ |

¹ The `syscall` opcode is in your PE's `.text` section — at your code address, not ntdll.

> **ETW-Ti** (`Microsoft-Windows-Threat-Intelligence`) fires inside the kernel regardless of invocation method. No user-mode technique bypasses it without kernel access.

* * *

## Evasion Techniques Deep Dive

[Permalink: Evasion Techniques Deep Dive](https://github.com/JoasASantos/SysWhispers4#evasion-techniques-deep-dive)

### XOR-Encrypted SSN Table (`--encrypt-ssn`)

[Permalink: XOR-Encrypted SSN Table (--encrypt-ssn)](https://github.com/JoasASantos/SysWhispers4#xor-encrypted-ssn-table---encrypt-ssn)

SSN values are stored XOR'd with a random compile-time key. Decrypted in the ASM stub just before the syscall — no plaintext SSN appears in the binary at rest.

```
#define SW4_XOR_KEY  0xDEADF00DU
// In SSN table: encrypted value
SW4_SsnTable[fi] = sortedIndex ^ SW4_XOR_KEY;
```

```
; In stub: decrypt before syscall
mov eax, DWORD PTR [SW4_SsnTable + N*4]  ; encrypted
xor eax, SW4_XOR_KEY                      ; decrypt
syscall
```

### Call Stack Spoofing (`--stack-spoof`)

[Permalink: Call Stack Spoofing (--stack-spoof)](https://github.com/JoasASantos/SysWhispers4#call-stack-spoofing---stack-spoof)

A trampoline that replaces the visible return address on the stack with a pointer into ntdll, making the call chain appear legitimate to stack-walking EDRs.

```
SW4_CallWithSpoofedStack PROC
    pop  r11               ; save real return address
    push [SW4_SpoofReturnAddr]  ; push ntdll address instead
    push r11               ; real address below (unreachable by walker)
    jmp  rax               ; execute target
SW4_CallWithSpoofedStack ENDP
```

### ETW Bypass (`--etw-bypass`)

[Permalink: ETW Bypass (--etw-bypass)](https://github.com/JoasASantos/SysWhispers4#etw-bypass---etw-bypass)

Patches `ntdll!EtwEventWrite` to return `STATUS_ACCESS_DENIED` immediately, suppressing user-mode ETW event delivery.

> This does **not** bypass kernel-mode ETW-Ti callbacks. Use only in authorized engagements.

### ntdll Unhooking (`--unhook-ntdll`)

[Permalink: ntdll Unhooking (--unhook-ntdll)](https://github.com/JoasASantos/SysWhispers4#ntdll-unhooking---unhook-ntdll-1)

Maps a clean ntdll from `\KnownDlls\` and `memcpy`'s the clean `.text` section over the hooked one:

```
Flow: NtOpenSection → NtMapViewOfSection → FindSection(".text") →
      VirtualProtect(RWX) → memcpy(clean→hooked) → VirtualProtect(RX) → cleanup
```

Call **before**`SW4_Initialize()` to ensure SSN resolution reads clean stubs.

### Junk Instructions (`--obfuscate`)

[Permalink: Junk Instructions (--obfuscate)](https://github.com/JoasASantos/SysWhispers4#junk-instructions---obfuscate)

14 different harmless x64 instruction variants injected between stub instructions:

```
nop                          ; classic NOP
xchg ax, ax                  ; 2-byte NOP
lea r11, [r11]               ; no-op LEA
nop DWORD PTR [rax]          ; multi-byte NOP
xchg r11, r11                ; register swap (no-op)
test r11d, 0ABh              ; flags-only, result discarded
push 042h / pop r11          ; push-pop noise
fnop                         ; FPU no-op
lea rsp, [rsp + 00h]         ; stack identity LEA
; ... and more
```

* * *

## Supported Functions (64)

[Permalink: Supported Functions (64)](https://github.com/JoasASantos/SysWhispers4#supported-functions-64)

```
python syswhispers.py --list-functions
```

| Category | Functions |
| --- | --- |
| **Memory** | `NtAllocateVirtualMemory` · `NtAllocateVirtualMemoryEx` · `NtFreeVirtualMemory` · `NtWriteVirtualMemory` · `NtReadVirtualMemory` · `NtProtectVirtualMemory` · `NtQueryVirtualMemory` · `NtSetInformationVirtualMemory` |
| **Section/Mapping** | `NtCreateSection` · `NtOpenSection` · `NtMapViewOfSection` · `NtUnmapViewOfSection` |
| **Process** | `NtOpenProcess` · `NtCreateProcess` · `NtCreateProcessEx` · `NtCreateUserProcess` · `NtTerminateProcess` · `NtSuspendProcess` · `NtResumeProcess` · `NtQueryInformationProcess` · `NtSetInformationProcess` |
| **Thread** | `NtCreateThreadEx` · `NtOpenThread` · `NtTerminateThread` · `NtSuspendThread` · `NtResumeThread` · `NtGetContextThread` · `NtSetContextThread` · `NtQueueApcThread` · `NtQueueApcThreadEx` · `NtQueryInformationThread` · `NtSetInformationThread` · `NtAlertThread` · `NtAlertResumeThread` · `NtTestAlert` |
| **Handle/Sync** | `NtClose` · `NtDuplicateObject` · `NtWaitForSingleObject` · `NtWaitForMultipleObjects` · `NtSignalAndWaitForSingleObject` · `NtCreateEvent` · `NtSetEvent` · `NtResetEvent` · `NtCreateTimer` · `NtSetTimer` |
| **File** | `NtCreateFile` · `NtOpenFile` · `NtWriteFile` · `NtReadFile` · `NtDeleteFile` |
| **Token** | `NtOpenProcessToken` · `NtOpenThreadToken` · `NtQueryInformationToken` · `NtAdjustPrivilegesToken` · `NtDuplicateToken` · `NtImpersonateThread` |
| **Transaction** | `NtCreateTransaction` · `NtRollbackTransaction` · `NtCommitTransaction` |
| **Misc** | `NtDelayExecution` · `NtQuerySystemInformation` · `NtQueryObject` · `NtFlushInstructionCache` · `NtContinue` |

* * *

## Presets

[Permalink: Presets](https://github.com/JoasASantos/SysWhispers4#presets)

| Preset | Functions | Use Case |
| --- | :-: | --- |
| `common` | 25 | General process/thread/memory operations |
| `injection` | 20 | Shellcode injection, APC injection, section mapping |
| `evasion` | 15 | AV/EDR evasion, process querying, memory manipulation |
| `token` | 6 | Token manipulation, impersonation, privilege escalation |
| `stealth` | 32 | **Maximum evasion**: injection + evasion + unhooking support |
| `file_ops` | 7 | File I/O via NT syscalls |
| `transaction` | 7 | Process doppelganging / transaction rollback |
| `all` | 64 | Every supported function |

* * *

## Recommended Configurations

[Permalink: Recommended Configurations](https://github.com/JoasASantos/SysWhispers4#recommended-configurations)

### Minimum Detection Footprint (Red Team)

[Permalink: Minimum Detection Footprint (Red Team)](https://github.com/JoasASantos/SysWhispers4#minimum-detection-footprint-red-team)

```
python syswhispers.py --preset stealth \
    --method randomized --resolve recycled \
    --obfuscate --encrypt-ssn --stack-spoof \
    --unhook-ntdll --etw-bypass --amsi-bypass \
    --anti-debug --sleep-encrypt
```

### Fast & Simple (CTF / Quick Testing)

[Permalink: Fast & Simple (CTF / Quick Testing)](https://github.com/JoasASantos/SysWhispers4#fast--simple-ctf--quick-testing)

```
python syswhispers.py --preset common
```

### Bypass Heavily Hooked EDR

[Permalink: Bypass Heavily Hooked EDR](https://github.com/JoasASantos/SysWhispers4#bypass-heavily-hooked-edr)

```
python syswhispers.py --preset injection \
    --method indirect --resolve from_disk \
    --unhook-ntdll --encrypt-ssn
```

### Process Doppelganging

[Permalink: Process Doppelganging](https://github.com/JoasASantos/SysWhispers4#process-doppelganging)

```
python syswhispers.py --preset transaction \
    --method indirect --resolve freshycalls
```

* * *

## Syscall Table Coverage

[Permalink: Syscall Table Coverage](https://github.com/JoasASantos/SysWhispers4#syscall-table-coverage)

Updated via `scripts/update_syscall_table.py` from [j00ru/windows-syscalls](https://github.com/j00ru/windows-syscalls):

| OS | Builds Covered |
| --- | --- |
| Windows 7 | SP1 (7601) |
| Windows 8 / 8.1 | RTM (9200, 9600) |
| Windows 10 | 1507 → 22H2 (10240 → 19045, 14 builds) |
| Windows 11 | 21H2 → 24H2 (22000 → 26100, 4 builds) |
| Windows Server | 2022 (20348), 2025 (26100) |

* * *

## Architecture Support

[Permalink: Architecture Support](https://github.com/JoasASantos/SysWhispers4#architecture-support)

| Arch | Syscall Instruction | SSN Register | Methods Supported |
| --- | :-: | :-: | --- |
| x64 | `syscall` | `eax` | All (embedded, indirect, randomized, egg) |
| x86 | `sysenter` | `eax` | Embedded + Egg |
| WoW64 | `syscall` (64-bit) | `eax` | All (x64 stubs from 32-bit PE) |
| ARM64 | `svc #0` | `w8` | Embedded |

* * *

## Project Structure

[Permalink: Project Structure](https://github.com/JoasASantos/SysWhispers4#project-structure)

```
SysWhispers4/
├── syswhispers.py              # CLI entry point
├── core/
│   ├── models.py               # Enums, dataclasses (8 resolution, 4 invocation methods)
│   ├── generator.py            # Code generation engine (~1900 lines)
│   ├── obfuscator.py           # Obfuscation: junk, eggs, XOR, string encryption
│   └── utils.py                # Hashes (DJB2, CRC32, FNV-1a), data loading
├── data/
│   ├── prototypes.json         # 64 NT function signatures
│   ├── presets.json            # 8 function presets
│   ├── syscalls_nt_x64.json   # x64 SSN table (Win7–Win11 24H2)
│   └── syscalls_nt_x86.json   # x86 SSN table
├── scripts/
│   └── update_syscall_table.py # Auto-fetch latest j00ru table
└── examples/
    └── example_injection.c     # Reference integration example
```

* * *

## Security Notice

[Permalink: Security Notice](https://github.com/JoasASantos/SysWhispers4#security-notice)

SysWhispers4 is a security research and authorized penetration testing tool. Use only:

- On systems you own or have explicit written authorization to test
- In CTF competitions
- For defensive research (understanding offensive techniques to improve detection)
- For developing security product signatures

Unauthorized use against systems you do not own is illegal in most jurisdictions.

* * *

## References & Credits

[Permalink: References & Credits](https://github.com/JoasASantos/SysWhispers4#references--credits)

| Resource | Author(s) |
| --- | --- |
| [SysWhispers](https://github.com/jthuraisamy/SysWhispers) | Jackson T. (jthuraisamy) |
| [SysWhispers2](https://github.com/jthuraisamy/SysWhispers2) | Jackson T. (jthuraisamy) |
| [SysWhispers3](https://github.com/klezVirus/SysWhispers3) | klezVirus |
| [SysWhispers3 fork](https://github.com/RWXstoned/SysWhispers3) | RWXstoned |
| [Windows Syscall Tables](https://github.com/j00ru/windows-syscalls) | j00ru |
| [Hell's Gate](https://github.com/am0nsec/HellsGate) | am0nsec, RtlMclovin |
| [Halo's Gate](https://sektor7.net/) | SEKTOR7 |
| [Tartarus' Gate](https://github.com/trickster0/TartarusGate) | trickster0 |
| [FreshyCalls](https://github.com/crummie5/FreshyCalls) | crummie5 |
| [RecycledGate](https://github.com/thefLink/RecycledGate) | thefLink |
| [Ekko Sleep Obfuscation](https://github.com/Cracked5pider/Ekko) | C5pider |
| [LayeredSyscall](https://whiteknightlabs.com/2024/07/31/layeredsyscall-abusing-veh-to-bypass-edrs/) | White Knight Labs |
| [Call Stack Spoofing](https://labs.withsecure.com/publications/spoofing-call-stacks-to-confuse-edrs) | WithSecure Labs |
| [SysWhispers Evolution Analysis](https://sudosiddharths.medium.com/analyzing-the-evolution-and-execution-of-syswhispers-1-3-74cbbcdaf397) | Siddharth S. |

* * *

## License

[Permalink: License](https://github.com/JoasASantos/SysWhispers4#license)

This project is released for educational and authorized security testing purposes.

## About

AV/EDR evasion via direct and indirect system calls Windows NT 3.1 through Windows 11 24H2 · x64 · x86 · WoW64 · ARM64


### Topics

[av-evasion](https://github.com/topics/av-evasion "Topic: av-evasion") [edr-evasion](https://github.com/topics/edr-evasion "Topic: edr-evasion") [syswhispers](https://github.com/topics/syswhispers "Topic: syswhispers") [syswhispers4](https://github.com/topics/syswhispers4 "Topic: syswhispers4")

### Resources

[Readme](https://github.com/JoasASantos/SysWhispers4#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/JoasASantos/SysWhispers4).

[Activity](https://github.com/JoasASantos/SysWhispers4/activity)

### Stars

[**461**\\
stars](https://github.com/JoasASantos/SysWhispers4/stargazers)

### Watchers

[**5**\\
watching](https://github.com/JoasASantos/SysWhispers4/watchers)

### Forks

[**61**\\
forks](https://github.com/JoasASantos/SysWhispers4/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2FJoasASantos%2FSysWhispers4&report=JoasASantos+%28user%29)

## [Releases](https://github.com/JoasASantos/SysWhispers4/releases)

No releases published

## [Packages\  0](https://github.com/users/JoasASantos/packages?repo_name=SysWhispers4)

No packages published

## [Contributors\  3](https://github.com/JoasASantos/SysWhispers4/graphs/contributors)

- [![@claude](https://avatars.githubusercontent.com/u/81847?s=64&v=4)](https://github.com/claude)[**claude** Claude](https://github.com/claude)
- [![@JoasASantos](https://avatars.githubusercontent.com/u/34966120?s=64&v=4)](https://github.com/JoasASantos)[**JoasASantos** Joas A Santos](https://github.com/JoasASantos)
- [![@Lavender-exe](https://avatars.githubusercontent.com/u/32195948?s=64&v=4)](https://github.com/Lavender-exe)[**Lavender-exe** Lav](https://github.com/Lavender-exe)

## Languages

- [Python100.0%](https://github.com/JoasASantos/SysWhispers4/search?l=python)

You can’t perform that action at this time.