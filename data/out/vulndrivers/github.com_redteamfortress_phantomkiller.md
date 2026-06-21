# https://github.com/redteamfortress/PhantomKiller

[Skip to content](https://github.com/redteamfortress/PhantomKiller#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/redteamfortress/PhantomKiller) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/redteamfortress/PhantomKiller) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/redteamfortress/PhantomKiller) to refresh your session.Dismiss alert

{{ message }}

[redteamfortress](https://github.com/redteamfortress)/ **[PhantomKiller](https://github.com/redteamfortress/PhantomKiller)** Public

- [Notifications](https://github.com/login?return_to=%2Fredteamfortress%2FPhantomKiller) You must be signed in to change notification settings
- [Fork\\
53](https://github.com/login?return_to=%2Fredteamfortress%2FPhantomKiller)
- [Star\\
277](https://github.com/login?return_to=%2Fredteamfortress%2FPhantomKiller)


main

[**1** Branch](https://github.com/redteamfortress/PhantomKiller/branches) [**1** Tag](https://github.com/redteamfortress/PhantomKiller/tags)

[Go to Branches page](https://github.com/redteamfortress/PhantomKiller/branches)[Go to Tags page](https://github.com/redteamfortress/PhantomKiller/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![redteamfortress](https://avatars.githubusercontent.com/u/285915761?v=4&size=40)](https://github.com/redteamfortress)[redteamfortress](https://github.com/redteamfortress/PhantomKiller/commits?author=redteamfortress)<br>[Update README.md](https://github.com/redteamfortress/PhantomKiller/commit/1b38661279bdf941656a6768640d36afd1cc54dd)<br>last monthMay 19, 2026<br>[1b38661](https://github.com/redteamfortress/PhantomKiller/commit/1b38661279bdf941656a6768640d36afd1cc54dd) · last monthMay 19, 2026<br>## History<br>[5 Commits](https://github.com/redteamfortress/PhantomKiller/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/redteamfortress/PhantomKiller/commits/main/) 5 Commits |
| [PhantomKiller](https://github.com/redteamfortress/PhantomKiller/tree/main/PhantomKiller "PhantomKiller") | [PhantomKiller](https://github.com/redteamfortress/PhantomKiller/tree/main/PhantomKiller "PhantomKiller") | [Add files via upload](https://github.com/redteamfortress/PhantomKiller/commit/142309d20f7e6085aa47d79b482996956f4ef85f "Add files via upload") | last monthMay 19, 2026 |
| [x64/Release](https://github.com/redteamfortress/PhantomKiller/tree/main/x64/Release "This path skips through empty directories") | [x64/Release](https://github.com/redteamfortress/PhantomKiller/tree/main/x64/Release "This path skips through empty directories") | [Add files via upload](https://github.com/redteamfortress/PhantomKiller/commit/142309d20f7e6085aa47d79b482996956f4ef85f "Add files via upload") | last monthMay 19, 2026 |
| [PhantomKiller.slnx](https://github.com/redteamfortress/PhantomKiller/blob/main/PhantomKiller.slnx "PhantomKiller.slnx") | [PhantomKiller.slnx](https://github.com/redteamfortress/PhantomKiller/blob/main/PhantomKiller.slnx "PhantomKiller.slnx") | [Add files via upload](https://github.com/redteamfortress/PhantomKiller/commit/142309d20f7e6085aa47d79b482996956f4ef85f "Add files via upload") | last monthMay 19, 2026 |
| [PhantomKiller.sys](https://github.com/redteamfortress/PhantomKiller/blob/main/PhantomKiller.sys "PhantomKiller.sys") | [PhantomKiller.sys](https://github.com/redteamfortress/PhantomKiller/blob/main/PhantomKiller.sys "PhantomKiller.sys") | [Add files via upload](https://github.com/redteamfortress/PhantomKiller/commit/c0be3a96eb5483d050c890eb4116506bc4434355 "Add files via upload") | last monthMay 19, 2026 |
| [README.md](https://github.com/redteamfortress/PhantomKiller/blob/main/README.md "README.md") | [README.md](https://github.com/redteamfortress/PhantomKiller/blob/main/README.md "README.md") | [Update README.md](https://github.com/redteamfortress/PhantomKiller/commit/1b38661279bdf941656a6768640d36afd1cc54dd "Update README.md") | last monthMay 19, 2026 |
| View all files |

## Repository files navigation

# PhantomKiller

[Permalink: PhantomKiller](https://github.com/redteamfortress/PhantomKiller#phantomkiller)

weaponizing a signed lenovo kernel driver to terminate any process — including EDR/AV protected processes.

## overview

[Permalink: overview](https://github.com/redteamfortress/PhantomKiller#overview)

PhantomKiller abuses `BootRepair.sys`, a legitimate lenovo driver shipped with Lenovo PC Manager. the driver exposes a device object (`\\.\BootRepair`) with no DACL restrictions and a single IOCTL (`0x222014`) that takes a 4-byte PID and calls `ZwTerminateProcess`, no access checks, no caller validation, no protection.

**full writeup:** [Phantom Killer — Reverse Engineering and Weaponizing a Lenovo Driver to Terminate EDR Processes](https://medium.com/@jehadbudagga/phantom-killer-reverse-engineering-and-weaponizing-a-lenovo-driver-to-terminate-edr-processes-9191cd06374f)

## driver details

[Permalink: driver details](https://github.com/redteamfortress/PhantomKiller#driver-details)

| field | value |
| --- | --- |
| file name | `BootRepair.sys` |
| sha256 | `5ab36c116767eaae53a466fbc2dae7cfd608ed77721f65e83312037fbd57c946` |
| signer | LENOVO (Symantec Class 3 SHA256 Code Signing CA) |
| compiled | 2018-01-03 |
| arch | x64 |
| VT detections | 0/71 at time of discovery |

## vulnerability summary

[Permalink: vulnerability summary](https://github.com/redteamfortress/PhantomKiller#vulnerability-summary)

- device object created without secure DACL — any user can open a handle
- `IRP_MJ_CREATE` (MajorFunction\[0\]) has no access checks
- `IRP_MJ_DEVICE_CONTROL` (MajorFunction\[14\]) accepts IOCTL `0x222014`
- input: 4-byte `DWORD` (target PID)
- internally calls `PsLookupProcessByProcessId` → `ObOpenObjectByPointer` → `ZwTerminateProcess`
- kills any process including PPL-protected AV/EDR processes

## attack scenarios

[Permalink: attack scenarios](https://github.com/redteamfortress/PhantomKiller#attack-scenarios)

**driver already loaded:** any low-privileged user can open the device and terminate any process on the system.

**BYOVD:** an attacker loads the signed driver via `sc.exe` or similar, then uses it to kill EDR processes before deploying post-exploitation tools.

## usage

[Permalink: usage](https://github.com/redteamfortress/PhantomKiller#usage)

```
sc.exe create PhantomKiller binPath="C:\Path\to\BootRepair.sys" type=kernel
sc.exe start PhantomKiller
```

```
PhantomKiller.exe <pid>
```

## disclaimer

[Permalink: disclaimer](https://github.com/redteamfortress/PhantomKiller#disclaimer)

this project is for **educational and authorized security research purposes only**. do not use this against systems you do not own or have explicit permission to test. the author is not responsible for any misuse.

## author

[Permalink: author](https://github.com/redteamfortress/PhantomKiller#author)

**j3h4ck** — [@j3h4ck](https://twitter.com/j3h4ck) \| [linkedin](https://www.linkedin.com/in/jehadabudagga/) \| [medium](https://medium.com/@jehadbudagga)

## About

Another BYOVD process killer. works on all EDR's. fully signed.


[medium.com/@jehadbudagga/phantom-killer-reverse-engineering-and-weaponizing-a-lenovo-driver-to-terminate-edr-processes-9191cd06374f](https://medium.com/@jehadbudagga/phantom-killer-reverse-engineering-and-weaponizing-a-lenovo-driver-to-terminate-edr-processes-9191cd06374f "https://medium.com/@jehadbudagga/phantom-killer-reverse-engineering-and-weaponizing-a-lenovo-driver-to-terminate-edr-processes-9191cd06374f")

### Topics

[redteaming](https://github.com/topics/redteaming "Topic: redteaming") [edr](https://github.com/topics/edr "Topic: edr") [edr-bypass](https://github.com/topics/edr-bypass "Topic: edr-bypass") [edr-evasion](https://github.com/topics/edr-evasion "Topic: edr-evasion") [byovd](https://github.com/topics/byovd "Topic: byovd")

### Resources

[Readme](https://github.com/redteamfortress/PhantomKiller#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/redteamfortress/PhantomKiller).

[Activity](https://github.com/redteamfortress/PhantomKiller/activity)

### Stars

[**277**\\
stars](https://github.com/redteamfortress/PhantomKiller/stargazers)

### Watchers

[**2**\\
watching](https://github.com/redteamfortress/PhantomKiller/watchers)

### Forks

[**53**\\
forks](https://github.com/redteamfortress/PhantomKiller/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fredteamfortress%2FPhantomKiller&report=redteamfortress+%28user%29)

## [Releases\  1](https://github.com/redteamfortress/PhantomKiller/releases)

[Driver & compiled POC\\
Latest\\
\\
on May 19May 19, 2026](https://github.com/redteamfortress/PhantomKiller/releases/tag/v1.0.0)

## [Packages\  0](https://github.com/users/redteamfortress/packages?repo_name=PhantomKiller)

No packages published

## [Contributors\  1](https://github.com/redteamfortress/PhantomKiller/graphs/contributors)

- [![@redteamfortress](https://avatars.githubusercontent.com/u/285915761?s=64&v=4)](https://github.com/redteamfortress)[**redteamfortress** Red Team Fortress](https://github.com/redteamfortress)

## Languages

- [C++100.0%](https://github.com/redteamfortress/PhantomKiller/search?l=c%2B%2B)

You can’t perform that action at this time.