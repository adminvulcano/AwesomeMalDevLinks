# https://github.com/0xROOTPLS/Cicada

[Skip to content](https://github.com/0xROOTPLS/Cicada#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/0xROOTPLS/Cicada) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/0xROOTPLS/Cicada) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/0xROOTPLS/Cicada) to refresh your session.Dismiss alert

{{ message }}

[0xROOTPLS](https://github.com/0xROOTPLS)/ **[Cicada](https://github.com/0xROOTPLS/Cicada)** Public

- [Notifications](https://github.com/login?return_to=%2F0xROOTPLS%2FCicada) You must be signed in to change notification settings
- [Fork\\
0](https://github.com/login?return_to=%2F0xROOTPLS%2FCicada)
- [Star\\
5](https://github.com/login?return_to=%2F0xROOTPLS%2FCicada)


main

[**1** Branch](https://github.com/0xROOTPLS/Cicada/branches) [**0** Tags](https://github.com/0xROOTPLS/Cicada/tags)

[Go to Branches page](https://github.com/0xROOTPLS/Cicada/branches)[Go to Tags page](https://github.com/0xROOTPLS/Cicada/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![0xROOTPLS](https://avatars.githubusercontent.com/u/104942265?v=4&size=40)](https://github.com/0xROOTPLS)[0xROOTPLS](https://github.com/0xROOTPLS/Cicada/commits?author=0xROOTPLS)<br>[Enhance README with sleep obfuscation details](https://github.com/0xROOTPLS/Cicada/commit/c308ec8fe62d62237d4212d61d1c78a4ffabb971)<br>Open commit details<br>3 months agoDec 13, 2025<br>[c308ec8](https://github.com/0xROOTPLS/Cicada/commit/c308ec8fe62d62237d4212d61d1c78a4ffabb971) · 3 months agoDec 13, 2025<br>## History<br>[6 Commits](https://github.com/0xROOTPLS/Cicada/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/0xROOTPLS/Cicada/commits/main/) 6 Commits |
| [README.md](https://github.com/0xROOTPLS/Cicada/blob/main/README.md "README.md") | [README.md](https://github.com/0xROOTPLS/Cicada/blob/main/README.md "README.md") | [Enhance README with sleep obfuscation details](https://github.com/0xROOTPLS/Cicada/commit/c308ec8fe62d62237d4212d61d1c78a4ffabb971 "Enhance README with sleep obfuscation details  Updated sleep obfuscation details and clarified timer chain steps.") | 3 months agoDec 13, 2025 |
| [cicada.c](https://github.com/0xROOTPLS/Cicada/blob/main/cicada.c "cicada.c") | [cicada.c](https://github.com/0xROOTPLS/Cicada/blob/main/cicada.c "cicada.c") | [Refactor protected\_sleep for enhanced security](https://github.com/0xROOTPLS/Cicada/commit/6736154d3d66cc3e44e9d11a0ae300f112856f38 "Refactor protected_sleep for enhanced security  Refactor protected_sleep function with enhanced encryption and decryption processes for shellcode, heap, and stack. Update timer chain logic to improve security and maintainability.") | 3 months agoDec 13, 2025 |
| View all files |

## Repository files navigation

# Cicada PIC Stager

[Permalink: Cicada PIC Stager](https://github.com/0xROOTPLS/Cicada#cicada-pic-stager)

**For security research and educational purposes only.**

## Features

[Permalink: Features](https://github.com/0xROOTPLS/Cicada#features)

- **Position-Independent Code (PIC)** \- No relocations, runs from any memory address
- **HTTPS Stage Fetching** \- Retrieves stage via WinHTTP with certificate validation bypass (self signed OK)
- **Sleep Obfuscation** \- RC4 encrypts shellcode + heap + stack during sleep via encrypted timer chain
- **Timer-Based Execution** \- Stage executed via `NtContinue` context switching
- **Self-Destruction** \- Stager memory freed after stage handoff
- **No String Literals** \- All strings built on stack
- **PEB Walking** \- Dynamic API resolution without `GetProcAddress` imports

## Execution Flow

[Permalink: Execution Flow](https://github.com/0xROOTPLS/Cicada#execution-flow)

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. API RESOLUTION                                               │
│    PEB walk → kernel32 → LoadLibraryA                           │
│    Load: ntdll, advapi32, winhttp                               │
├─────────────────────────────────────────────────────────────────┤
│ 2. PROTECTED SLEEP (11-step encrypted timer chain)              │
│    Timer 0:  Decrypt timer chain body                           │
│    Timer 1:  VirtualProtect(RW)                                 │
│    Timer 2-4: RC4 encrypt shellcode, heap, stack                │
│    Timer 5:  WaitForSingleObject (sleep)                        │
│    Timer 6-8: RC4 decrypt stack, heap, shellcode                │
│    Timer 9:  VirtualProtect(RX)                                 │
│    Timer 10: SetEvent (wake)                                    │
├─────────────────────────────────────────────────────────────────┤
│ 3. FETCH STAGE                                                  │
│    WinHTTP GET /stage → raw shellcode bytes                     │
│    VirtualAlloc(RWX) → copy stage                               │
├─────────────────────────────────────────────────────────────────┤
│ 4. EXECUTE + ZERO                                               │
│    Timer 1 (T+0):    NtContinue → execute stage                 │
│    Timer 2 (T+100ms): VirtualFree(stager) → self-destruct       │
└─────────────────────────────────────────────────────────────────┘
```

## Build Requirements

[Permalink: Build Requirements](https://github.com/0xROOTPLS/Cicada#build-requirements)

**WSL or Linux with MinGW cross-compiler:**

```
sudo apt install gcc-mingw-w64-x86-64 binutils
```

## Building

[Permalink: Building](https://github.com/0xROOTPLS/Cicada#building)

```
# Compile to flat binary
x86_64-w64-mingw32-gcc-win32 -c payload.c -o payload.o \
    -Os -fPIC -nostdlib -nostartfiles -ffreestanding \
    -fno-asynchronous-unwind-tables -fno-ident \
    -fno-stack-protector -mno-stack-arg-probe -e start -s

# Link to raw shellcode (requires linker script)
ld -T linker.ld payload.o -o payload.bin
```

**Linker script (`linker.ld`):**

```
OUTPUT_FORMAT("binary");
SECTIONS {
    . = 0x00;
    .text : {
        *(.text)
        *(.func)
    }
}
```

## Configuration

[Permalink: Configuration](https://github.com/0xROOTPLS/Cicada#configuration)

Edit `payload.c` before building:

| Constant | Location | Description |
| --- | --- | --- |
| `INITIAL_SLEEP_MS` | Line ~490 | Initial sleep delay (default: 300000ms) |
| `server[]` | Line ~600 | C2 server address (default: 127.0.0.1) |
| Port 443 | `WinHttpConnect` call | HTTPS port |
| `/stage` | `http_get_stage` | Stage endpoint path |

## Server Requirements

[Permalink: Server Requirements](https://github.com/0xROOTPLS/Cicada#server-requirements)

The stager expects:

- HTTPS server on configured host:port
- `GET /stage` returns raw shellcode bytes
- Self-signed certificates accepted (validation bypassed)

## Sleep Obfuscation Details

[Permalink: Sleep Obfuscation Details](https://github.com/0xROOTPLS/Cicada#sleep-obfuscation-details)

Timer chain data is split into two regions:

| Region | Contents | During Sleep |
| --- | --- | --- |
| **Header** (~1.3KB) | Timer 0 CONTEXT, Key B, body descriptor | Exposed |
| **Body** (~14KB) | 10 ROP CONTEXTs, Key A, region descriptors | Encrypted |

**Protected during sleep:**

- Shellcode (encrypted with Key A)
- Heap (encrypted with Key A)
- Stack (encrypted with Key A)
- Timer chain body (encrypted with Key B)

**Exposed during sleep:**

- Timer 0 CONTEXT (reveals: "call SystemFunction032 on body region")
- Key B (chain decryption key, different from main Key A)

This minimizes exposure - an analyst sees only that _something_ decrypts _something_, not the actual ROP chain, targets, or main encryption key.

## Entry Point

[Permalink: Entry Point](https://github.com/0xROOTPLS/Cicada#entry-point)

```
int start(PVOID shellcode_base, DWORD shellcode_size);
```

The loader must pass:

- `shellcode_base` \- Address where stager is loaded (for self-reference during sleep encryption)
- `shellcode_size` \- Size of stager shellcode

## Size

[Permalink: Size](https://github.com/0xROOTPLS/Cicada#size)

~5400 bytes (varies with compiler optimization)

## References

[Permalink: References](https://github.com/0xROOTPLS/Cicada#references)

- [Ekko Sleep Obfuscation](https://github.com/Cracked5pider/Ekko) \- Timer-based sleep encryption

## About

Cicada is a position-independent Windows shellcode stager featuring sleep obfuscation and remote HTTPS staging


### Resources

[Readme](https://github.com/0xROOTPLS/Cicada#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/0xROOTPLS/Cicada).

[Activity](https://github.com/0xROOTPLS/Cicada/activity)

### Stars

[**5**\\
stars](https://github.com/0xROOTPLS/Cicada/stargazers)

### Watchers

[**0**\\
watching](https://github.com/0xROOTPLS/Cicada/watchers)

### Forks

[**0**\\
forks](https://github.com/0xROOTPLS/Cicada/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2F0xROOTPLS%2FCicada&report=0xROOTPLS+%28user%29)

## [Releases](https://github.com/0xROOTPLS/Cicada/releases)

No releases published

## [Packages\  0](https://github.com/users/0xROOTPLS/packages?repo_name=Cicada)

No packages published

## [Contributors\  1](https://github.com/0xROOTPLS/Cicada/graphs/contributors)

- [![@0xROOTPLS](https://avatars.githubusercontent.com/u/104942265?s=64&v=4)](https://github.com/0xROOTPLS)[**0xROOTPLS** 0xROOTPLS](https://github.com/0xROOTPLS)

## Languages

- [C100.0%](https://github.com/0xROOTPLS/Cicada/search?l=c)

You can’t perform that action at this time.