# https://github.com/raskolnikov90/Beatrice.py

[Skip to content](https://github.com/raskolnikov90/Beatrice.py#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/raskolnikov90/Beatrice.py) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/raskolnikov90/Beatrice.py) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/raskolnikov90/Beatrice.py) to refresh your session.Dismiss alert

{{ message }}

[raskolnikov90](https://github.com/raskolnikov90)/ **[Beatrice.py](https://github.com/raskolnikov90/Beatrice.py)** Public

- [Notifications](https://github.com/login?return_to=%2Fraskolnikov90%2FBeatrice.py) You must be signed in to change notification settings
- [Fork\\
27](https://github.com/login?return_to=%2Fraskolnikov90%2FBeatrice.py)
- [Star\\
201](https://github.com/login?return_to=%2Fraskolnikov90%2FBeatrice.py)


main

[**1** Branch](https://github.com/raskolnikov90/Beatrice.py/branches) [**0** Tags](https://github.com/raskolnikov90/Beatrice.py/tags)

[Go to Branches page](https://github.com/raskolnikov90/Beatrice.py/branches)[Go to Tags page](https://github.com/raskolnikov90/Beatrice.py/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![raskolnikov90](https://avatars.githubusercontent.com/u/44821234?v=4&size=40)](https://github.com/raskolnikov90)[raskolnikov90](https://github.com/raskolnikov90/Beatrice.py/commits?author=raskolnikov90)<br>[Pro Edition Update](https://github.com/raskolnikov90/Beatrice.py/commit/29b39f057e7a4986b24600240289f99596c7033c)<br>last monthMay 9, 2026<br>[29b39f0](https://github.com/raskolnikov90/Beatrice.py/commit/29b39f057e7a4986b24600240289f99596c7033c) · last monthMay 9, 2026<br>## History<br>[10 Commits](https://github.com/raskolnikov90/Beatrice.py/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/raskolnikov90/Beatrice.py/commits/main/) 10 Commits |
| [README.md](https://github.com/raskolnikov90/Beatrice.py/blob/main/README.md "README.md") | [README.md](https://github.com/raskolnikov90/Beatrice.py/blob/main/README.md "README.md") | [Pro Edition Update](https://github.com/raskolnikov90/Beatrice.py/commit/29b39f057e7a4986b24600240289f99596c7033c "Pro Edition Update") | last monthMay 9, 2026 |
| [beatrice.py](https://github.com/raskolnikov90/Beatrice.py/blob/main/beatrice.py "beatrice.py") | [beatrice.py](https://github.com/raskolnikov90/Beatrice.py/blob/main/beatrice.py "beatrice.py") | [Avoid self add cases](https://github.com/raskolnikov90/Beatrice.py/commit/6fb71f61244055b095fab149778695cd986586dd "Avoid self add cases") | 2 months agoApr 25, 2026 |
| [requirements.txt](https://github.com/raskolnikov90/Beatrice.py/blob/main/requirements.txt "requirements.txt") | [requirements.txt](https://github.com/raskolnikov90/Beatrice.py/blob/main/requirements.txt "requirements.txt") | [Add files via upload](https://github.com/raskolnikov90/Beatrice.py/commit/5f1529b2481fb1764d7d0ff23cb954ca3162fe69 "Add files via upload") | 2 months agoApr 16, 2026 |
| View all files |

## Repository files navigation

# Beatrice.py

[Permalink: Beatrice.py](https://github.com/raskolnikov90/Beatrice.py#beatricepy)

To bypass detection methods like YARA rules that look for certain bytes and memory scanners Beatrice.py patches machine code in binaries with alternative x64 assembly opcodes of the same size. This tool was also designed to modify machine code of executables or complex binaries that contain strings and other data, it will strictly match machine code to avoid breaking binaries.

![image](https://camo.githubusercontent.com/4269de5392c1322d0bf7e83353af22ca6ab04cdf5837e7760c59bb5c8906f091/68747470733a2f2f692e696d6775722e636f6d2f4254756e4c73532e676966)![image](https://camo.githubusercontent.com/4269de5392c1322d0bf7e83353af22ca6ab04cdf5837e7760c59bb5c8906f091/68747470733a2f2f692e696d6775722e636f6d2f4254756e4c73532e676966)[Open image in new window](https://camo.githubusercontent.com/4269de5392c1322d0bf7e83353af22ca6ab04cdf5837e7760c59bb5c8906f091/68747470733a2f2f692e696d6775722e636f6d2f4254756e4c73532e676966)

# Usage

[Permalink: Usage](https://github.com/raskolnikov90/Beatrice.py#usage)

```
python3 beatrice.py

@@@@@@@   @@@@@@@@   @@@@@@   @@@@@@@  @@@@@@@   @@@   @@@@@@@  @@@@@@@@       @@@@@@@   @@@ @@@
@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@  @@@@@@@@  @@@  @@@@@@@@  @@@@@@@@       @@@@@@@@  @@@ @@@
@@!  @@@  @@!       @@!  @@@    @@!    @@!  @@@  @@!  !@@       @@!            @@!  @@@  @@! !@@
!@   @!@  !@!       !@!  @!@    !@!    !@!  @!@  !@!  !@!       !@!            !@!  @!@  !@! @!!
@!@!@!@   @!!!:!    @!@!@!@!    @!!    @!@!!@!   !!@  !@!       @!!!:!         @!@@!@!    !@!@!
!!!@!!!!  !!!!!:    !!!@!!!!    !!!    !!@!@!    !!!  !!!       !!!!!:         !!@!!!      @!!!
!!:  !!!  !!:       !!:  !!!    !!:    !!: :!!   !!:  :!!       !!:            !!:         !!:
:!:  !:!  :!:       :!:  !:!    :!:    :!:  !:!  :!:  :!:       :!:       :!:  :!:         :!:
 :: ::::   :: ::::  ::   :::     ::    ::   :::   ::   ::: :::   :: ::::  :::   ::          ::
:: : ::   : :: ::    :   : :     :      :   : :  :     :: :: :  : :: ::   :::   :           :

Usage: beatrice.py <binary>
-h for usage and flags
-v for Verbose mode
-s for Safer mode, normal mode already mostly safe but still may break some binaries
```

# What this tool does

[Permalink: What this tool does](https://github.com/raskolnikov90/Beatrice.py#what-this-tool-does)

### It will:

[Permalink: It will:](https://github.com/raskolnikov90/Beatrice.py#it-will)

- Generate patterns of simple assembly x64 instructions and their alternative instructions, turn them into machine code and patch the machine code if it matches.
- Build different lists of assembly instructions that contain immediate values and other instructions that can’t be easily turned into patterns and apply appropriate changes to them.
- Apply alternative ways to encode instructions whenever possible.
- Create an identical binary functionality wise but with the above patches applied that will help evade YARA rules and some Antivirus solutions.

### It will NOT:

[Permalink: It will NOT:](https://github.com/raskolnikov90/Beatrice.py#it-will-not)

- Be a one size fits all solution.
- Modify strings, only on the Pro Edition
- Modify imports or calls to Windows API functions that can be detected by some AVs and EDRs.
- Completely evade behavior based detection. While this modifies the machine code enough to sometimes trick behavior based detection it won’t change the core functionality leading to still possibilities for detection.

While this tool can make some binaries evade AVs on its own, it is best used combined with other evasion techniques (Examples: Modify shellcode to be used with a loader, help with custom or modified tooling)

# Pro Edition

[Permalink: Pro Edition](https://github.com/raskolnikov90/Beatrice.py#pro-edition)

A paid version of this tool is available at: [https://buymeacoffee.com/lainkusanagi/e/531266](https://buymeacoffee.com/lainkusanagi/e/531266)

### Pro Edition features:

[Permalink: Pro Edition features:](https://github.com/raskolnikov90/Beatrice.py#pro-edition-features)

- Rewritten and improved alternative encodings for assembly instructions.
- Parse bytes from YARA rules and DefenderCheck output and use them to generate more patches.
- Parse strings from YARA rules to modify strings on binaries and executable.
- Obfuscate Import Address Table.
- Generate new potential detection bytes that can be used to create YARA rules.
- Includes a PDF showing how the tool can be used for Antivirus and EDR evasion as well as how to use it to test and create detection rules.

# Tests against Windows Defender and Elastic YARA rules ( April 2026 Public Version )

[Permalink: Tests against Windows Defender and Elastic YARA rules ( April 2026 Public Version )](https://github.com/raskolnikov90/Beatrice.py#tests-against-windows-defender-and-elastic-yara-rules--april-2026-public-version-)

### Executables (.exe)

[Permalink: Executables (.exe)](https://github.com/raskolnikov90/Beatrice.py#executables-exe)

**Mimikatz with obfuscated strings** → [Evades Defender, see my Medium article.](https://medium.com/@luisgerardomoret_69654/modifying-mimikatz-to-evade-defender-2026-dc701000289d)

**Metasploit** stageless reverse shell tcp → Inconsistent results against Defender sometimes it evades Defender sometimes it’s detected, evades Elastic YARA rules.

**Havoc** payload with default profile and no modification → Evades Defender (shown on gif above), detected by Elastic YARA due to default hashing and default profile.

**Sliver** payload using its default obfuscation → Detected by Defender due to using Garble for obfuscation, evades Elastic YARA Rules.

**Sliver** with skip-symbols option → Detected by both Defender and Elastic YARA due to strings.

**AdaptixC2** payload with IAT Hiding → Already evasive against Defender but tool may help if Microsoft creates more signatures, evades Elastic YARA rules.

**CobaltStrike** stageless payload → Bypassed detection bytes but still detected by few strings.

### Raw binaries / Shellcode (.bin)

[Permalink: Raw binaries / Shellcode (.bin)](https://github.com/raskolnikov90/Beatrice.py#raw-binaries--shellcode-bin)

Using [DefenderYara](https://github.com/roadwy/DefenderYara/tree/main/Trojan/Win64), [defender2yara](https://github.com/t-tani/defender2yara/tree/yara-rules/Win64/Trojan) and [Elastic rules](https://github.com/elastic/protections-artifacts) to test.

**Metasploit** stageless reverse shell tcp → Evades YARA rules.

**Havoc** payload with custom profile and no modification → Evades Defender YARA rules, detected by Elastic YARA due to default hashing and default profile.

**Sliver** payload using its default obfuscation → Evades YARA rules.

**Sliver** with skip-symbols option → Detected by both Defender and Elastic YARA due to strings.

**AdaptixC2** payload with IAT Hiding → Evades YARA rules.

**CobaltStrike** stageless payload → Bypassed detection bytes but still detected by few strings.

**Donut** shellcode → Evades YARA rules.

Notes on Havoc: Ran on Docker to solve compiler compatibility issues so payloads compile as they originally do before using the tool.

Notes on CobaltStrike: I don’t own license, I have access to a course that provides labs and includes CobaltStrike.

# Known Issues

[Permalink: Known Issues](https://github.com/raskolnikov90/Beatrice.py#known-issues)

Golang compiled binaries that use Garble for obfuscation may break.

Despite working most of the time some binaries may still break, that’s why safe mode was added as an option to just use the most basic features.

## About

Modify machine code in binaries with alternative x64 assembly opcodes for AV evasion


### Resources

[Readme](https://github.com/raskolnikov90/Beatrice.py#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/raskolnikov90/Beatrice.py).

[Activity](https://github.com/raskolnikov90/Beatrice.py/activity)

### Stars

[**201**\\
stars](https://github.com/raskolnikov90/Beatrice.py/stargazers)

### Watchers

[**1**\\
watching](https://github.com/raskolnikov90/Beatrice.py/watchers)

### Forks

[**27**\\
forks](https://github.com/raskolnikov90/Beatrice.py/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fraskolnikov90%2FBeatrice.py&report=raskolnikov90+%28user%29)

## [Releases](https://github.com/raskolnikov90/Beatrice.py/releases)

No releases published

## [Packages\  0](https://github.com/users/raskolnikov90/packages?repo_name=Beatrice.py)

No packages published

## [Contributors\  1](https://github.com/raskolnikov90/Beatrice.py/graphs/contributors)

- [![@raskolnikov90](https://avatars.githubusercontent.com/u/44821234?s=64&v=4)](https://github.com/raskolnikov90)[**raskolnikov90** Luis G Moret](https://github.com/raskolnikov90)

## Languages

- [Python100.0%](https://github.com/raskolnikov90/Beatrice.py/search?l=python)

You can’t perform that action at this time.