# https://github.com/kapla0011/InsomniacUnwinding

[Skip to content](https://github.com/kapla0011/InsomniacUnwinding#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/kapla0011/InsomniacUnwinding) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/kapla0011/InsomniacUnwinding) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/kapla0011/InsomniacUnwinding) to refresh your session.Dismiss alert

{{ message }}

[kapla0011](https://github.com/kapla0011)/ **[InsomniacUnwinding](https://github.com/kapla0011/InsomniacUnwinding)** Public

- [Notifications](https://github.com/login?return_to=%2Fkapla0011%2FInsomniacUnwinding) You must be signed in to change notification settings
- [Fork\\
6](https://github.com/login?return_to=%2Fkapla0011%2FInsomniacUnwinding)
- [Star\\
45](https://github.com/login?return_to=%2Fkapla0011%2FInsomniacUnwinding)


main

[**1** Branch](https://github.com/kapla0011/InsomniacUnwinding/branches) [**0** Tags](https://github.com/kapla0011/InsomniacUnwinding/tags)

[Go to Branches page](https://github.com/kapla0011/InsomniacUnwinding/branches)[Go to Tags page](https://github.com/kapla0011/InsomniacUnwinding/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![kapla0011](https://avatars.githubusercontent.com/u/114022035?v=4&size=40)](https://github.com/kapla0011)[kapla0011](https://github.com/kapla0011/InsomniacUnwinding/commits?author=kapla0011)<br>[first commit](https://github.com/kapla0011/InsomniacUnwinding/commit/c02774cdd681ad47e1374c63a35edd825af84e47)<br>last monthMar 30, 2026<br>[c02774c](https://github.com/kapla0011/InsomniacUnwinding/commit/c02774cdd681ad47e1374c63a35edd825af84e47) · last monthMar 30, 2026<br>## History<br>[1 Commit](https://github.com/kapla0011/InsomniacUnwinding/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/kapla0011/InsomniacUnwinding/commits/main/) 1 Commit |
| [InsomniacUnwinding](https://github.com/kapla0011/InsomniacUnwinding/tree/main/InsomniacUnwinding "InsomniacUnwinding") | [InsomniacUnwinding](https://github.com/kapla0011/InsomniacUnwinding/tree/main/InsomniacUnwinding "InsomniacUnwinding") | [first commit](https://github.com/kapla0011/InsomniacUnwinding/commit/c02774cdd681ad47e1374c63a35edd825af84e47 "first commit") | last monthMar 30, 2026 |
| [.gitignore](https://github.com/kapla0011/InsomniacUnwinding/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/kapla0011/InsomniacUnwinding/blob/main/.gitignore ".gitignore") | [first commit](https://github.com/kapla0011/InsomniacUnwinding/commit/c02774cdd681ad47e1374c63a35edd825af84e47 "first commit") | last monthMar 30, 2026 |
| [DeadBeefSignature.yar](https://github.com/kapla0011/InsomniacUnwinding/blob/main/DeadBeefSignature.yar "DeadBeefSignature.yar") | [DeadBeefSignature.yar](https://github.com/kapla0011/InsomniacUnwinding/blob/main/DeadBeefSignature.yar "DeadBeefSignature.yar") | [first commit](https://github.com/kapla0011/InsomniacUnwinding/commit/c02774cdd681ad47e1374c63a35edd825af84e47 "first commit") | last monthMar 30, 2026 |
| [InsomniacUnwinding.sln](https://github.com/kapla0011/InsomniacUnwinding/blob/main/InsomniacUnwinding.sln "InsomniacUnwinding.sln") | [InsomniacUnwinding.sln](https://github.com/kapla0011/InsomniacUnwinding/blob/main/InsomniacUnwinding.sln "InsomniacUnwinding.sln") | [first commit](https://github.com/kapla0011/InsomniacUnwinding/commit/c02774cdd681ad47e1374c63a35edd825af84e47 "first commit") | last monthMar 30, 2026 |
| [README.md](https://github.com/kapla0011/InsomniacUnwinding/blob/main/README.md "README.md") | [README.md](https://github.com/kapla0011/InsomniacUnwinding/blob/main/README.md "README.md") | [first commit](https://github.com/kapla0011/InsomniacUnwinding/commit/c02774cdd681ad47e1374c63a35edd825af84e47 "first commit") | last monthMar 30, 2026 |
| View all files |

## Repository files navigation

# InsomniacUnwinding

[Permalink: InsomniacUnwinding](https://github.com/kapla0011/InsomniacUnwinding#insomniacunwinding)

Surgical UNWIND\_INFO preservation for sleep masking without call stack spoofing.

**Blog Post:** [Unwind Data Can't Sleep - Introducing InsomniacUnwinding](https://lorenzomeacci.com/unwind-data-cant-sleep-introducing-insomniacunwinding)

## Overview

[Permalink: Overview](https://github.com/kapla0011/InsomniacUnwinding#overview)

Traditional sleep masking encrypts the entire payload image, breaking stack unwinding. This implementation is based on Ekko created by (@C5pider) and surgically preserve only the UNWIND\_INFO structures needed for stack walking (~250 bytes vs ~6KB full `.rdata`), the PE Headers and the .pdata section.

## How It Works

[Permalink: How It Works](https://github.com/kapla0011/InsomniacUnwinding#how-it-works)

The timer chain is extended to patch back preserved regions after encryption:

01. `VirtualProtect` → RW
02. `SystemFunction032` → Encrypt entire image
03. `RtlCopyMemory` → Restore PE headers
04. `RtlCopyMemory` → Restore .pdata
05. `RtlCopyMemory` × N → Restore each UNWIND\_INFO region
06. `WaitForSingleObject` → Sleep
07. `SystemFunction032` → Decrypt
08. `RtlCopyMemory` → Restore PE headers (XOR'd to garbage)
09. `RtlCopyMemory` → Restore .pdata
10. `RtlCopyMemory` × N → Restore each UNWIND\_INFO region
11. `VirtualProtect` → RX
12. `SetEvent` → Signal completion

## Usage

[Permalink: Usage](https://github.com/kapla0011/InsomniacUnwinding#usage)

1. Build in Visual Studio (x64 Release)

2. Run:


```
.\InsomniacUnwinding.exe
```

3. Attach a debugger and inspect the main thread's call stack during sleep. It should resolve correctly through `BaseThreadInitThunk` and `RtlUserThreadStart`.

## YARA Testing

[Permalink: YARA Testing](https://github.com/kapla0011/InsomniacUnwinding#yara-testing)

Test signatures are embedded in `.rdata` and `.data`:

```
.\yara64.exe DeadBeefSignature.yar <pid>
```

Expected results:

- **Awake:** 2 hits
- **Sleeping:** 0 hits (both encrypted, only UNWIND\_INFO preserved)

## Key Insight

[Permalink: Key Insight](https://github.com/kapla0011/InsomniacUnwinding#key-insight)

Call stack spoofing is an architectural consequence of unbacked sleepmask memory, not a fundamental requirement. When the sleepmask executes from backed memory, spoofing becomes unnecessary.

## Acknowledgments

[Permalink: Acknowledgments](https://github.com/kapla0011/InsomniacUnwinding#acknowledgments)

Thanks to Alex Reid (@Octoberfest73) for catching a mistake in the initial research that led to this improved implementation.

## About

A sleepmask based on Ekko that preserves unwind data at sleep time.


[lorenzomeacci.com/unwind-data-cant-sleep-introducing-insomniacunwinding](https://lorenzomeacci.com/unwind-data-cant-sleep-introducing-insomniacunwinding "https://lorenzomeacci.com/unwind-data-cant-sleep-introducing-insomniacunwinding")

### Resources

[Readme](https://github.com/kapla0011/InsomniacUnwinding#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/kapla0011/InsomniacUnwinding).

[Activity](https://github.com/kapla0011/InsomniacUnwinding/activity)

### Stars

[**45**\\
stars](https://github.com/kapla0011/InsomniacUnwinding/stargazers)

### Watchers

[**0**\\
watching](https://github.com/kapla0011/InsomniacUnwinding/watchers)

### Forks

[**6**\\
forks](https://github.com/kapla0011/InsomniacUnwinding/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fkapla0011%2FInsomniacUnwinding&report=kapla0011+%28user%29)

## [Releases](https://github.com/kapla0011/InsomniacUnwinding/releases)

No releases published

## [Packages\  0](https://github.com/users/kapla0011/packages?repo_name=InsomniacUnwinding)

No packages published

## [Contributors\  1](https://github.com/kapla0011/InsomniacUnwinding/graphs/contributors)

- [![@kapla0011](https://avatars.githubusercontent.com/u/114022035?s=64&v=4)](https://github.com/kapla0011)[**kapla0011** kapla](https://github.com/kapla0011)

## Languages

- [C98.6%](https://github.com/kapla0011/InsomniacUnwinding/search?l=c)
- [YARA1.4%](https://github.com/kapla0011/InsomniacUnwinding/search?l=yara)

You can’t perform that action at this time.