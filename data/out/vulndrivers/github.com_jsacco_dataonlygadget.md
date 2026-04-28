# https://github.com/jsacco/DataOnlyGadget

[Skip to content](https://github.com/jsacco/DataOnlyGadget#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/jsacco/DataOnlyGadget) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/jsacco/DataOnlyGadget) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/jsacco/DataOnlyGadget) to refresh your session.Dismiss alert

{{ message }}

[jsacco](https://github.com/jsacco)/ **[DataOnlyGadget](https://github.com/jsacco/DataOnlyGadget)** Public

- [Notifications](https://github.com/login?return_to=%2Fjsacco%2FDataOnlyGadget) You must be signed in to change notification settings
- [Fork\\
6](https://github.com/login?return_to=%2Fjsacco%2FDataOnlyGadget)
- [Star\\
56](https://github.com/login?return_to=%2Fjsacco%2FDataOnlyGadget)


main

[**1** Branch](https://github.com/jsacco/DataOnlyGadget/branches) [**0** Tags](https://github.com/jsacco/DataOnlyGadget/tags)

[Go to Branches page](https://github.com/jsacco/DataOnlyGadget/branches)[Go to Tags page](https://github.com/jsacco/DataOnlyGadget/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![jsacco](https://avatars.githubusercontent.com/u/1094247?v=4&size=40)](https://github.com/jsacco)[jsacco](https://github.com/jsacco/DataOnlyGadget/commits?author=jsacco)<br>[Update README.md](https://github.com/jsacco/DataOnlyGadget/commit/b7ce509fdeb025cbcc006686289e65ff73def973)<br>2 weeks agoApr 15, 2026<br>[b7ce509](https://github.com/jsacco/DataOnlyGadget/commit/b7ce509fdeb025cbcc006686289e65ff73def973) · 2 weeks agoApr 15, 2026<br>## History<br>[44 Commits](https://github.com/jsacco/DataOnlyGadget/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/jsacco/DataOnlyGadget/commits/main/) 44 Commits |
| [DataOnlyGadgetTool](https://github.com/jsacco/DataOnlyGadget/tree/main/DataOnlyGadgetTool "DataOnlyGadgetTool") | [DataOnlyGadgetTool](https://github.com/jsacco/DataOnlyGadget/tree/main/DataOnlyGadgetTool "DataOnlyGadgetTool") | [Add files via upload](https://github.com/jsacco/DataOnlyGadget/commit/ab517c54b0fb3e431dfa138b82956f0d9cafae89 "Add files via upload") | last monthMar 16, 2026 |
| [DataOnlyGadgetTool.sln](https://github.com/jsacco/DataOnlyGadget/blob/main/DataOnlyGadgetTool.sln "DataOnlyGadgetTool.sln") | [DataOnlyGadgetTool.sln](https://github.com/jsacco/DataOnlyGadget/blob/main/DataOnlyGadgetTool.sln "DataOnlyGadgetTool.sln") | [Add files via upload](https://github.com/jsacco/DataOnlyGadget/commit/98d1d00aa8e9241471a23ecae83b069c88848672 "Add files via upload") | last monthMar 11, 2026 |
| [README.md](https://github.com/jsacco/DataOnlyGadget/blob/main/README.md "README.md") | [README.md](https://github.com/jsacco/DataOnlyGadget/blob/main/README.md "README.md") | [Update README.md](https://github.com/jsacco/DataOnlyGadget/commit/b7ce509fdeb025cbcc006686289e65ff73def973 "Update README.md") | 2 weeks agoApr 15, 2026 |
| [dog.mp4](https://github.com/jsacco/DataOnlyGadget/blob/main/dog.mp4 "dog.mp4") | [dog.mp4](https://github.com/jsacco/DataOnlyGadget/blob/main/dog.mp4 "dog.mp4") | [Add files via upload](https://github.com/jsacco/DataOnlyGadget/commit/eb9e5e9e57d7eebc830d48953df0706e213a0a57 "Add files via upload") | last monthMar 11, 2026 |
| View all files |

## Repository files navigation

# DOG: Data Only Gadgets

[Permalink: DOG: Data Only Gadgets](https://github.com/jsacco/DataOnlyGadget#dog-data-only-gadgets)

DOG, short for Data Only Gadgets, is the technique of using kernel gadgets, this has been bundle in a tool that let you use your existing kernel read/write primitives to locate, classify, and chain kernel gadgets, resolve the structures and offsets and build reusable chains at runtime to perform the attacks.

A kernel gadget is a small piece of kernel code or a kernel data structure that can be repurposed as a building block in an exploit chain. Unlike traditional ROP gadgets (which are small sequences of instructions ending in a ret), DOG's kernel gadgets are data-oriented and legitimate parts of the Windows kernel that can be used and abused to perform useful operations when combined.

![f394f353-f9b4-4bbf-9807-82360d25b8dc](https://private-user-images.githubusercontent.com/1094247/562224811-22219664-28fb-4ad8-9f58-8fd4191b9e1a.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzcyMDA0NDAsIm5iZiI6MTc3NzIwMDE0MCwicGF0aCI6Ii8xMDk0MjQ3LzU2MjIyNDgxMS0yMjIxOTY2NC0yOGZiLTRhZDgtOWY1OC04ZmQ0MTkxYjllMWEucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDQyNiUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA0MjZUMTA0MjIwWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9MjU2NWYwZjhhMDBkMDhhM2IzNDFlZjI3OTcwMTNkZDNlNjJmN2NiMDFhYjBiMGM3MzYwOTY5MDU1NWExZDU2MyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.D9uGJUgL3WeL0jRSZ7RQuDzDsF25zvy9efrGKgorLYI)  ![Screenshot From 2026-03-24 14-44-07](https://private-user-images.githubusercontent.com/1094247/568450523-f1328daa-80bd-468b-8bdb-35d4bfe9f45f.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzcyMDA0NDAsIm5iZiI6MTc3NzIwMDE0MCwicGF0aCI6Ii8xMDk0MjQ3LzU2ODQ1MDUyMy1mMTMyOGRhYS04MGJkLTQ2OGItOGJkYi0zNWQ0YmZlOWY0NWYucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDQyNiUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA0MjZUMTA0MjIwWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9YWRhNWRjYzkwNjlhYTg3YzJlNWZlNzI4ZjNjZmZkN2IwYTBjMjU3Zjg2MWY4OGY3M2JkNmI1NzExMDFiZTkyYiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.fCNnq-aKeBUzVGdEf189iz41fsX9VCWsdD5gZd2M-ww)

## Why Kernel Gadgets?

[Permalink: Why Kernel Gadgets?](https://github.com/jsacco/DataOnlyGadget#why-kernel-gadgets)

Traditional kernel exploits rely on executing custom shellcode or ROP chains techniques that modern mitigations like VBS, HVCI, and CET have rendered obsolete.

DOG takes a different approach, the usage of: data-only gadget chaining by discovering and repurposing existing kernel code and data structures into usable chains.

| Mitigation | Protection aim | Gadgets |
| --- | --- | --- |
| **HVCI** | Modifying/creating executable code | Gadgets use existing, signed kernel code |
| **CET** | ROP/JOP chains | Gadgets use data manipulation, not instruction sequences |
| **VBS** | Access to secure code data | Gadgets operate in normal kernel data |
| **Kernel ASLR** | Predicting addresses | DOG resolves addresses at runtime |
| **Patch Guard** | Modification of critical structures | Gadgets target non-protected data |

DOG implements [`NTKernelWalkerLib`](https://github.com/jsacco/NTKernelWalkerLib) to recover the offsets and structures needed during discovery.

And it's based on my previous research of Arbitrary Code Execution via SSDT Hijack: [`SSDTHijackWriteUp`](https://www.exploitpack.com/blogs/news/bypassing-kernel-code-execution-a-data-only-ssdt-hijack-under-hvci-but-how)

## Summary

[Permalink: Summary](https://github.com/jsacco/DataOnlyGadget#summary)

This tool is built around a pluggable kernel read/write backend and a runtime discovery pipeline. It resolves `ntoskrnl` symbols, walks kernel structures, generates offsets dynamically, enumerates kernel objects, collects gadget candidates, classify them, and organizes the discovered gadgets into chains.

## Main Features

[Permalink: Main Features](https://github.com/jsacco/DataOnlyGadget#main-features)

- Callback discovery zeroing/modification
- Privilege escalation of target PID (token-swap)
- Protected Process Light modification
- Controlled VA/PA Arbitrary Read
- Controlled VA/PA Aribitrary Write
- Code Injection
- Unlink (hiding) of target PID via Data
- LSASS PatchWDigest
- LSASS Dump Raw pages from memory
- LSASS Minidump + PPL Zeroing
- Suspend of target PID, works for Protected Processed

![Screenshot From 2026-03-24 15-02-06](https://private-user-images.githubusercontent.com/1094247/568451639-ef0dc365-0283-4683-848f-11a0b2ab716a.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzcyMDA0NDAsIm5iZiI6MTc3NzIwMDE0MCwicGF0aCI6Ii8xMDk0MjQ3LzU2ODQ1MTYzOS1lZjBkYzM2NS0wMjgzLTQ2ODMtODQ4Zi0xMWEwYjJhYjcxNmEucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDQyNiUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA0MjZUMTA0MjIwWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9M2VjMGE5NzZlMzhmYWI0YzI2ODhjZDQ1Yjc4NDk1NjA3ZjI1MmJlZGIxZTlmMzkzNDMxMWNiNjdmMTA1YzBhNyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.bIcK7JdFHkijcWJ4U08R1AoWPRUwfxYwyAsiLuaTWTQ)

Besides this actionable features, there are several more programmer-centric features available to incorporate your Kernel Exploit primitives into a fully functional DOG.

- Pluggable `KernelReadWrite` backend interface
- Runtime `ntoskrnl` symbol resolution using `dbghelp`
- Dynamic kernel structure walking and field lookup
- Dynamic offset generation
- Enumeration of kernel processes, threads, and object types
- Multi-stage gadget discovery
- Classification of discovered entries by type, structure, field, and ownership
- Classification for discovered gadgets
- Runtime Windows version and build detection
- Deeper discovery stages:
  - pattern scan
  - cross references
  - dynamic validation
- Gadget chain engine
- Interactive mode and command-line mode
- JSON export of discovered gadgets

## DOG in-action with Kernel Pack

[Permalink: DOG in-action with Kernel Pack](https://github.com/jsacco/DataOnlyGadget#dog-in-action-with-kernel-pack)

We integrated DOG into Kernel Pack with modifications to its base code, enabling Kernel Pack to deploy an agent that combines advanced user‑level bypass capabilities (inherited from Control Pack) with kernel‑level access, all while operating on a fully protected endpoint with VBS, HVCI, and kCET enabled. Download Kernel Pack from: [https://www.exploitpack.com/products/kernel-pack](https://www.exploitpack.com/products/kernel-pack)

![Screenshot From 2026-03-17 20-26-05](https://private-user-images.githubusercontent.com/1094247/568447324-79807c6f-18a4-48a5-b16d-2963de4e2d3d.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzcyMDA0NDAsIm5iZiI6MTc3NzIwMDE0MCwicGF0aCI6Ii8xMDk0MjQ3LzU2ODQ0NzMyNC03OTgwN2M2Zi0xOGE0LTQ4YTUtYjE2ZC0yOTYzZGU0ZTJkM2QucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDQyNiUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA0MjZUMTA0MjIwWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9Mjk3OTM1OGE2YTJjMGM4MDhlNzAyZGE5NjliY2IwNWJjOTE3MmYyMjFmNjYxNzM1NmI3N2NiZjgyZWI1Y2I5YSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.kq51p6Ah5YoxtpWWKdyi4AevVbq0S26m4nG9uXqRON0)

## Supported Exploit Classes

[Permalink: Supported Exploit Classes](https://github.com/jsacco/DataOnlyGadget#supported-exploit-classes)

DOG is written to sit on top of an existing kernel read/write primitive and handle the runtime work that comes after primitive acquisition.

The project is built for exploit paths that depend on:

locating writable kernel data targets at runtime
resolving the structures and offsets those targets depend on
turning discovered entries into reusable chains
In practice, DOG is not tied to one specific primitive. The backend layer is abstracted behind `KernelReadWrite`, so different exploit classes can be adapted to the same discovery and chaining pipeline as long as they expose the memory operations DOG needs.

The physical-memory backend included in this repository is just an example implementation, please plug-in your own.

## Using DOG With an Existing R/W Primitive

[Permalink: Using DOG With an Existing R/W Primitive](https://github.com/jsacco/DataOnlyGadget#using-dog-with-an-existing-rw-primitive)

DOG is meant to be used after kernel read/write access already exists.

If you already have a working primitive, the expected workflow is to adapt it to DOG’s backend layer and let DOG handle the rest:

- resolving the kernel symbols, structures, and offsets required for the current build
- enumerating kernel objects and candidate gadget targets
- collecting and classifying the entries it finds
- building chains from the discovered targets

The discovery and chaining logic are separated from the transport layer so other primitives can be plugged in through `KernelReadWrite` and `RwFactory`.

## What DOG already provides

[Permalink: What DOG already provides](https://github.com/jsacco/DataOnlyGadget#what-dog-already-provides)

- Abstract interface: implement KernelReadWrite (see KernelReadWrite.h).
- A factory hook point: register your implementation in RwFactory.cpp.

## How to plug an exploit primitive

[Permalink: How to plug an exploit primitive](https://github.com/jsacco/DataOnlyGadget#how-to-plug-an-exploit-primitive)

![Screenshot From 2026-03-24 15-03-41](https://private-user-images.githubusercontent.com/1094247/568451244-3e24dbec-d6a7-4dd5-88d2-1719571aae4d.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzcyMDA0NDAsIm5iZiI6MTc3NzIwMDE0MCwicGF0aCI6Ii8xMDk0MjQ3LzU2ODQ1MTI0NC0zZTI0ZGJlYy1kNmE3LTRkZDUtODhkMi0xNzE5NTcxYWFlNGQucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDQyNiUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA0MjZUMTA0MjIwWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9OTJkMDY4MWYwZjRlNTViZjZmODhmN2Y3MDkxNjE3NTllOGE4ODQ4ZmViMThiODJlNmU3NjY1M2UyMWQ4NDllMSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.vAc4_qzQ6aXktF1yrXrXPMVM5cBaSLtUUhuld2V5MEc)

1. Start by implementing KernelReadWrite:
Required: ReadMemory, WriteMemory, IsValidAddress, IsDriverAvailable.
Optional if supported: SupportsPhysical, ReadPhysical/WritePhysical, VirtToPhys.
2. Drop your source into the project and add it to DataOnlyGadgetTool.vcxproj.
3. Add a selector in RwFactory.cpp (e.g., flag/enum/env) that instantiates your class.
4. Validate with a known kernel symbol (read) and a disposable writable slot (write), return false on failure.

## Primitives depending on your Exploit Class

[Permalink: Primitives depending on your Exploit Class](https://github.com/jsacco/DataOnlyGadget#primitives-depending-on-your-exploit-class)

- Arbitrary kernel VA R/W via driver IOCTL
Implement ReadMemory/WriteMemory as IOCTL wrappers. Add strict IsValidAddress (kernel VA only).

- Arbitrary kernel VA R/W via win32k/GDI pointer swap (bitmap/palette/session)
Same ReadMemory/WriteMemory; allow session/kernel VA, block user VA.

- Arbitrary write‑what‑where (UAF / pool overflow / NULL deref / logic bug)
Expose it as WriteMemory; if you can also leak, expose that as ReadMemory. Guard addresses.

- Handle table confusion leading to arbitrary kernel VA R/W
Treat like generic VA R/W; same ReadMemory/WriteMemory hook.

- Physical memory access (PCIe/DMA/Thunderbolt/FireWire/PCILeech, or map/unmap IOCTL)
Set SupportsPhysical=true; implement ReadPhysical/WritePhysical and VirtToPhys. Mirror PhysmemReadWrite.cpp.


Limited MSR/IO-port access
Only support those ranges in ReadMemory/WriteMemory;

Firmware/ACPI/SMBus giving system memory R/W
Treat as physical backend (like DMA): SupportsPhysical, phys read/write, optional VA→PA.

## Example Workflows

[Permalink: Example Workflows](https://github.com/jsacco/DataOnlyGadget#example-workflows)

A few practical ways DOG fits into an existing exploit:

- You already have kernel R/W, but you do not want to keep chasing offsets every time the target build changes. DOG handles the runtime structure and offset recovery first, then works from there.
- You already have a primitive, but you do not want to hand-audit kernel memory looking for usable targets. DOG walks the relevant objects and collects candidate entries automatically.
- You want to see what the current machine actually exposes before doing anything else. DOG gives you a live inventory of discovered gadget targets instead of relying on assumptions from another build.
- You want to separate primitive acquisition from target discovery. The primitive only needs to give DOG memory access; DOG handles symbol lookup, offset recovery, enumeration, discovery, and chain building on top.
- You want to compare what changes between builds or systems. DOG can export the discovered entries so you can diff results instead of repeating the same manual analysis each time.
- You already know the kind of target you are looking for, but you want the tool to narrow the search space and organize the usable entries for you.

## Main Components

[Permalink: Main Components](https://github.com/jsacco/DataOnlyGadget#main-components)

- `main.cpp`


Entry point, command handling, interactive flow, orchestration, export, and conversion.

- `KernelReadWrite.*`


Base interface for kernel and memory access.

- `PhysmemReadWrite.*`


Driver-backed backend for physical memory access and address translation, as example implementation.

- `RwFactory.*`


Backend selection layer.

- `WindowsVersion.*`


Windows version/build detection.

- `Offsets.*`


Runtime offset database generation and management.

- `NtoskrnlStructs.*`


Kernel structure walker for resolving fields and member offsets.

- `SymbolResolver.*`

`ntoskrnl` symbol lookup helpers.

- `GadgetDiscovery.*`


Discovery engine and kernel object enumeration.

- `GadgetChaining.*`


Chain construction and execution logic.

- `RawDumpConverter.*`


Conversion of the tool's raw dump format into a minimal minidump.

- `MinidumpWriter.*`


Minidump writing helpers.


## Dependency

[Permalink: Dependency](https://github.com/jsacco/DataOnlyGadget#dependency)

DataOnlyGadget uses [`NTKernelWalkerLib`](https://github.com/jsacco/NTKernelWalkerLib) to find the kernel offsets and structures required by the discovery pipeline.

## Build

[Permalink: Build](https://github.com/jsacco/DataOnlyGadget#build)

- Visual Studio 2022
- MSVC `v143`
- C++17
- Windows SDK 10

Libraries used by the project:

- `ntdll.lib`
- `psapi.lib`
- `dbghelp.lib`
- `version.lib`

## Project Layout

[Permalink: Project Layout](https://github.com/jsacco/DataOnlyGadget#project-layout)

```
DataOnlyGadget/
└── DataOnlyGadgetTool/
    ├── main.cpp
    ├── KernelReadWrite.*
    ├── PhysmemReadWrite.*
    ├── RwFactory.*
    ├── WindowsVersion.*
    ├── Offsets.*
    ├── NtoskrnlStructs.*
    ├── SymbolResolver.*
    ├── GadgetDiscovery.*
    ├── GadgetChaining.*
    ├── RawDumpConverter.*
    ├── MinidumpWriter.*
    └── DataOnlyGadgetTool.vcxproj
```

## About

DOG is a post-exploitation toolkit that uses your existing kernel read/write primitive to locate, classify, and chain kernel gadgets.


### Resources

[Readme](https://github.com/jsacco/DataOnlyGadget#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/jsacco/DataOnlyGadget).

[Activity](https://github.com/jsacco/DataOnlyGadget/activity)

### Stars

[**56**\\
stars](https://github.com/jsacco/DataOnlyGadget/stargazers)

### Watchers

[**0**\\
watching](https://github.com/jsacco/DataOnlyGadget/watchers)

### Forks

[**6**\\
forks](https://github.com/jsacco/DataOnlyGadget/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fjsacco%2FDataOnlyGadget&report=jsacco+%28user%29)

## [Releases](https://github.com/jsacco/DataOnlyGadget/releases)

No releases published

## [Packages\  0](https://github.com/users/jsacco/packages?repo_name=DataOnlyGadget)

No packages published

## [Contributors\  1](https://github.com/jsacco/DataOnlyGadget/graphs/contributors)

- [![@jsacco](https://avatars.githubusercontent.com/u/1094247?s=64&v=4)](https://github.com/jsacco)[**jsacco** Juan Sacco](https://github.com/jsacco)

## Languages

- [C++100.0%](https://github.com/jsacco/DataOnlyGadget/search?l=c%2B%2B)

You can’t perform that action at this time.