# https://github.com/0xRoam/LoadReload

[Skip to content](https://github.com/0xRoam/LoadReload#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/0xRoam/LoadReload) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/0xRoam/LoadReload) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/0xRoam/LoadReload) to refresh your session.Dismiss alert

{{ message }}

[0xRoam](https://github.com/0xRoam)/ **[LoadReload](https://github.com/0xRoam/LoadReload)** Public

- [Notifications](https://github.com/login?return_to=%2F0xRoam%2FLoadReload) You must be signed in to change notification settings
- [Fork\\
0](https://github.com/login?return_to=%2F0xRoam%2FLoadReload)
- [Star\\
22](https://github.com/login?return_to=%2F0xRoam%2FLoadReload)


main

[**1** Branch](https://github.com/0xRoam/LoadReload/branches) [**0** Tags](https://github.com/0xRoam/LoadReload/tags)

[Go to Branches page](https://github.com/0xRoam/LoadReload/branches)[Go to Tags page](https://github.com/0xRoam/LoadReload/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>![author](https://github.githubassets.com/images/gravatars/gravatar-user-420.png?size=40)<br>Roam<br>[cleanup](https://github.com/0xRoam/LoadReload/commit/6192a5fa7a45679b82d8cd01131e29981e69c98f)<br>last weekJun 13, 2026<br>[6192a5f](https://github.com/0xRoam/LoadReload/commit/6192a5fa7a45679b82d8cd01131e29981e69c98f) · last weekJun 13, 2026<br>## History<br>[1 Commit](https://github.com/0xRoam/LoadReload/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/0xRoam/LoadReload/commits/main/) 1 Commit |
| [LoadReload](https://github.com/0xRoam/LoadReload/tree/main/LoadReload "LoadReload") | [LoadReload](https://github.com/0xRoam/LoadReload/tree/main/LoadReload "LoadReload") | [cleanup](https://github.com/0xRoam/LoadReload/commit/6192a5fa7a45679b82d8cd01131e29981e69c98f "cleanup") | last weekJun 13, 2026 |
| [.gitignore](https://github.com/0xRoam/LoadReload/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/0xRoam/LoadReload/blob/main/.gitignore ".gitignore") | [cleanup](https://github.com/0xRoam/LoadReload/commit/6192a5fa7a45679b82d8cd01131e29981e69c98f "cleanup") | last weekJun 13, 2026 |
| [LoadReload.sln](https://github.com/0xRoam/LoadReload/blob/main/LoadReload.sln "LoadReload.sln") | [LoadReload.sln](https://github.com/0xRoam/LoadReload/blob/main/LoadReload.sln "LoadReload.sln") | [cleanup](https://github.com/0xRoam/LoadReload/commit/6192a5fa7a45679b82d8cd01131e29981e69c98f "cleanup") | last weekJun 13, 2026 |
| [README.md](https://github.com/0xRoam/LoadReload/blob/main/README.md "README.md") | [README.md](https://github.com/0xRoam/LoadReload/blob/main/README.md "README.md") | [cleanup](https://github.com/0xRoam/LoadReload/commit/6192a5fa7a45679b82d8cd01131e29981e69c98f "cleanup") | last weekJun 13, 2026 |
| View all files |

## Repository files navigation

# LoadReload

[Permalink: LoadReload](https://github.com/0xRoam/LoadReload#loadreload)

Shellcode Loader for Master Thesis, designed for Sliver-Shellcode (smaller than 25MB....).

Note

**Features:**

- Multibyte-XOR Decryption of Payload
- Fetches Payload locally
- Anti-Emulation by BusySleep-Function via KUSER\_SHARED\_DATA
- RW-RX-Loop for EDR-Deconditioning / Wasting Resources for Memory-Scanners
- Preloading of Network-DLLs against behaviour alerts like "Network Module from Stomped Module"
- Module Overloading of Decoy-DLL chosen by Operator (currently edgehtml.dll)
- IAT Obfuscation by API-Hashing and Dynamic API-Resolution
- Shellcode Execution via LdrCallenclave

**References & Thanks**

I couldnt have achieved anything in this thesis without the awesome work of other people and the great support of my thesis supervisor. So I wanna thank each of these persons guiding me and helping me grow.

- [https://github.com/eversinc33](https://github.com/eversinc33)
- [https://github.com/dobin](https://github.com/dobin)
- [https://github.com/S3cur3Th1sSh1t](https://github.com/S3cur3Th1sSh1t)
- and many more...

The Features listed above where inspired by:

- [https://maldevacademy.com](https://maldevacademy.com/)
- [https://blog.deeb.ch/posts/how-edr-works/](https://blog.deeb.ch/posts/how-edr-works/)
- [https://github.com/dobin/SuperMega/blob/main/data/source/antiemulation/sirallocalot.c](https://github.com/dobin/SuperMega/blob/main/data/source/antiemulation/sirallocalot.c)
- [https://github.com/dobin/SuperMega/blob/main/data/source/antiemulation/timeraw.c](https://github.com/dobin/SuperMega/blob/main/data/source/antiemulation/timeraw.c)
- [https://gist.github.com/whokilleddb/ef1f8c33947f6ceb90664ce38d3dcf04](https://gist.github.com/whokilleddb/ef1f8c33947f6ceb90664ce38d3dcf04)
- [https://github.com/tlsbollei/KittyLoader](https://github.com/tlsbollei/KittyLoader)

Caution

**Disclaimer & Legal Notice**

This repository, **LoadReload**, and all associated code, techniques, and information are provided strictly for **educational and academic research purposes**.

This sample and its methodologies are actively used to research attack patterns, develop detection capabilities, and enhance security products.

You are required to use this knowledge and these tools **only on systems you own or have explicit, written permission to test**.

Any unauthorized use against systems you do not own is **illegal and strictly prohibited**.

This tool was created to advance the field of defensive cybersecurity. The author, _0xRoam_, assumes **no liability** and is not responsible for any misuse or damage caused by this software.

By accessing this repository, you acknowledge that you understand its purpose is to learn about **modern malware techniques, evasion tactics**, and ultimately to **improve our collective ability to defend against them**.

## About

Shellcode Loader for Master Thesis


### Resources

[Readme](https://github.com/0xRoam/LoadReload#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/0xRoam/LoadReload).

[Activity](https://github.com/0xRoam/LoadReload/activity)

### Stars

[**22**\\
stars](https://github.com/0xRoam/LoadReload/stargazers)

### Watchers

[**0**\\
watching](https://github.com/0xRoam/LoadReload/watchers)

### Forks

[**0**\\
forks](https://github.com/0xRoam/LoadReload/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2F0xRoam%2FLoadReload&report=0xRoam+%28user%29)

## [Releases](https://github.com/0xRoam/LoadReload/releases)

No releases published

## [Packages\  0](https://github.com/users/0xRoam/packages?repo_name=LoadReload)

No packages published

## [Contributors\  1](https://github.com/0xRoam/LoadReload/graphs/contributors)

- [![@0xRoam](https://avatars.githubusercontent.com/u/90392515?s=64&v=4)](https://github.com/0xRoam)[**0xRoam** 0xRoam](https://github.com/0xRoam)

## Languages

- [C++88.0%](https://github.com/0xRoam/LoadReload/search?l=c%2B%2B)
- [C12.0%](https://github.com/0xRoam/LoadReload/search?l=c)

You can’t perform that action at this time.