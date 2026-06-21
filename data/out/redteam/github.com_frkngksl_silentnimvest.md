# https://github.com/frkngksl/SilentNimvest

[Skip to content](https://github.com/frkngksl/SilentNimvest#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/frkngksl/SilentNimvest) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/frkngksl/SilentNimvest) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/frkngksl/SilentNimvest) to refresh your session.Dismiss alert

{{ message }}

[frkngksl](https://github.com/frkngksl)/ **[SilentNimvest](https://github.com/frkngksl/SilentNimvest)** Public

- [Notifications](https://github.com/login?return_to=%2Ffrkngksl%2FSilentNimvest) You must be signed in to change notification settings
- [Fork\\
13](https://github.com/login?return_to=%2Ffrkngksl%2FSilentNimvest)
- [Star\\
106](https://github.com/login?return_to=%2Ffrkngksl%2FSilentNimvest)


main

[**1** Branch](https://github.com/frkngksl/SilentNimvest/branches) [**0** Tags](https://github.com/frkngksl/SilentNimvest/tags)

[Go to Branches page](https://github.com/frkngksl/SilentNimvest/branches)[Go to Tags page](https://github.com/frkngksl/SilentNimvest/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![frkngksl](https://avatars.githubusercontent.com/u/26549173?v=4&size=40)](https://github.com/frkngksl)[frkngksl](https://github.com/frkngksl/SilentNimvest/commits?author=frkngksl)<br>[Update README.md](https://github.com/frkngksl/SilentNimvest/commit/8ab73458e90593a8da05900442f3d0f8f82558fe)<br>2 months agoApr 4, 2026<br>[8ab7345](https://github.com/frkngksl/SilentNimvest/commit/8ab73458e90593a8da05900442f3d0f8f82558fe) · 2 months agoApr 4, 2026<br>## History<br>[9 Commits](https://github.com/frkngksl/SilentNimvest/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/frkngksl/SilentNimvest/commits/main/) 9 Commits |
| [.gitignore](https://github.com/frkngksl/SilentNimvest/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/frkngksl/SilentNimvest/blob/main/.gitignore ".gitignore") | [Upload files before refactor](https://github.com/frkngksl/SilentNimvest/commit/5512ec6b383235c80335c21090ef6cdb374a0276 "Upload files before refactor") | 3 months agoMar 31, 2026 |
| [Crypto.nim](https://github.com/frkngksl/SilentNimvest/blob/main/Crypto.nim "Crypto.nim") | [Crypto.nim](https://github.com/frkngksl/SilentNimvest/blob/main/Crypto.nim "Crypto.nim") | [Upload files before refactor](https://github.com/frkngksl/SilentNimvest/commit/5512ec6b383235c80335c21090ef6cdb374a0276 "Upload files before refactor") | 3 months agoMar 31, 2026 |
| [LICENSE](https://github.com/frkngksl/SilentNimvest/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/frkngksl/SilentNimvest/blob/main/LICENSE "LICENSE") | [Create LICENSE](https://github.com/frkngksl/SilentNimvest/commit/7c5e413cfc784dd17ca678c6c4bdad9183cc2edf "Create LICENSE") | 2 months agoApr 3, 2026 |
| [Main.nim](https://github.com/frkngksl/SilentNimvest/blob/main/Main.nim "Main.nim") | [Main.nim](https://github.com/frkngksl/SilentNimvest/blob/main/Main.nim "Main.nim") | [Add banner](https://github.com/frkngksl/SilentNimvest/commit/47fd607de184f8e81d5b99f9d4d06cb708cb2c03 "Add banner") | 2 months agoApr 2, 2026 |
| [README.md](https://github.com/frkngksl/SilentNimvest/blob/main/README.md "README.md") | [README.md](https://github.com/frkngksl/SilentNimvest/blob/main/README.md "README.md") | [Update README.md](https://github.com/frkngksl/SilentNimvest/commit/8ab73458e90593a8da05900442f3d0f8f82558fe "Update README.md") | 2 months agoApr 4, 2026 |
| [Structs.nim](https://github.com/frkngksl/SilentNimvest/blob/main/Structs.nim "Structs.nim") | [Structs.nim](https://github.com/frkngksl/SilentNimvest/blob/main/Structs.nim "Structs.nim") | [Upload files before refactor](https://github.com/frkngksl/SilentNimvest/commit/5512ec6b383235c80335c21090ef6cdb374a0276 "Upload files before refactor") | 3 months agoMar 31, 2026 |
| [Utility.nim](https://github.com/frkngksl/SilentNimvest/blob/main/Utility.nim "Utility.nim") | [Utility.nim](https://github.com/frkngksl/SilentNimvest/blob/main/Utility.nim "Utility.nim") | [Add banner](https://github.com/frkngksl/SilentNimvest/commit/47fd607de184f8e81d5b99f9d4d06cb708cb2c03 "Add banner") | 2 months agoApr 2, 2026 |
| View all files |

## Repository files navigation

# SilentNimvest

[Permalink: SilentNimvest](https://github.com/frkngksl/SilentNimvest#silentnimvest)

Basically, SilentNimvest is a SAM and Security Hives parser written in Nim. SilentNimvest reads keys under these hives by using the Silent Harvest technique. With this technique, rather than a SYSTEM-level privilege, a plain Administrator account who enables `SeBackupPrivilege` (thanks to `NtOpenKeyEx` flags) can dump the Local users' hashes, cached domain logon information, LSA Secrets, and other secrets that can be obtained from these hives
by using a less EDR-alerted registry read API which is `RegQueryMultipleValuesW`.
The whole project is based on [sud0ru's research](https://sud0ru.ghost.io/silent-harvest-extracting-windows-secrets-under-the-radar/).

# Compilation

[Permalink: Compilation](https://github.com/frkngksl/SilentNimvest#compilation)

You can directly compile the source code with the following command:

`nim c -d:release -o:SilentNimvest.exe Main.nim`

In case you get the error "cannot open file", you should also install the required dependencies:

`nimble install winim nimcrypto checksums des`

# Usage

[Permalink: Usage](https://github.com/frkngksl/SilentNimvest#usage)

SilentNimvest can be executed directly without any required parameters from an elevated Administrator terminal.

```
PS C:\Users\test\Desktop\SilentNimvest> .\SilentNimvest.exe
 __ _ _            _       __ _                         _
/ _(_) | ___ _ __ | |_  /\ \ (_)_ __ _____   _____  ___| |_
\ \| | |/ _ \ '_ \| __|/  \/ / | '_ ` _ \ \ / / _ \/ __| __|
_\ \ | |  __/ | | | |_/ /\  /| | | | | | \ V /  __/\__ \ |_
\__/_|_|\___|_| |_|\__\_\ \/ |_|_| |_| |_|\_/ \___||___/\__|

                         @R0h1rr1m

[!] Trying to parse SAM Related Credentials (Local Users)

[*] Local User RID: 500 - Administrator - aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0
[*] Local User RID: 501 - Guest - aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0
[*] Local User RID: 503 - DefaultAccount - aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0
[*] Local User RID: 504 - WDAGUtilityAccount - aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0
[*] Local User RID: 1001 - zoro - aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0

[!] Trying to parse Security Related Credentials (Cached Domain Logon Info, Machine Account and LSA Secrets)

[*] DPAPI Keys: dpapi_machinekey: ea31d6cfe0d16ae931b73c59d7e0c089c037b & dpapi_userkey: 44431d6cfe0d16ae931b73c59d7e0c089c0d0
[*] NL$KM: 1f31d6cfe0d16ae931b73c59d7e0c089c031d6cfe0d16ae931b73c59d7e0c089c031d6cfe0d16ae931b73c59d7e0c089c0c01
[*] Plaintext User from _SC_Backupservice: .\zoro:SilentNimvest
```

# References

[Permalink: References](https://github.com/frkngksl/SilentNimvest#references)

- [https://sud0ru.ghost.io/silent-harvest-extracting-windows-secrets-under-the-radar/](https://sud0ru.ghost.io/silent-harvest-extracting-windows-secrets-under-the-radar/)
- [https://github.com/GhostPack/SharpDump](https://github.com/GhostPack/SharpDump)
- [https://cocomelonc.github.io/malware/2024/06/01/malware-cryptography-28.html](https://cocomelonc.github.io/malware/2024/06/01/malware-cryptography-28.html)

# Disclaimer

[Permalink: Disclaimer](https://github.com/frkngksl/SilentNimvest#disclaimer)

For authorized security testing only. Misuse of this tool against systems without explicit permission is illegal.

## About

Nim implementation for sud0Ru's Credential Dumping from SAM/SECURITY Hives Method (a.k.a. SilentHarvest)


### Resources

[Readme](https://github.com/frkngksl/SilentNimvest#readme-ov-file)

### License

[MIT license](https://github.com/frkngksl/SilentNimvest#MIT-1-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/frkngksl/SilentNimvest).

[Activity](https://github.com/frkngksl/SilentNimvest/activity)

### Stars

[**106**\\
stars](https://github.com/frkngksl/SilentNimvest/stargazers)

### Watchers

[**0**\\
watching](https://github.com/frkngksl/SilentNimvest/watchers)

### Forks

[**13**\\
forks](https://github.com/frkngksl/SilentNimvest/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Ffrkngksl%2FSilentNimvest&report=frkngksl+%28user%29)

## [Releases](https://github.com/frkngksl/SilentNimvest/releases)

No releases published

## [Packages\  0](https://github.com/users/frkngksl/packages?repo_name=SilentNimvest)

No packages published

## [Contributors\  1](https://github.com/frkngksl/SilentNimvest/graphs/contributors)

- [![@frkngksl](https://avatars.githubusercontent.com/u/26549173?s=64&v=4)](https://github.com/frkngksl)[**frkngksl** Furkan Göksel](https://github.com/frkngksl)

## Languages

- [Nim100.0%](https://github.com/frkngksl/SilentNimvest/search?l=nim)

You can’t perform that action at this time.