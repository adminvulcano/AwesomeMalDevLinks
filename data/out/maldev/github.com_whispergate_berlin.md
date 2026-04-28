# https://github.com/Whispergate/berlin

[Skip to content](https://github.com/Whispergate/berlin#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/Whispergate/berlin) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/Whispergate/berlin) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/Whispergate/berlin) to refresh your session.Dismiss alert

{{ message }}

[Whispergate](https://github.com/Whispergate)/ **[berlin](https://github.com/Whispergate/berlin)** Public

- [Notifications](https://github.com/login?return_to=%2FWhispergate%2Fberlin) You must be signed in to change notification settings
- [Fork\\
3](https://github.com/login?return_to=%2FWhispergate%2Fberlin)
- [Star\\
45](https://github.com/login?return_to=%2FWhispergate%2Fberlin)


main

[**1** Branch](https://github.com/Whispergate/berlin/branches) [**0** Tags](https://github.com/Whispergate/berlin/tags)

[Go to Branches page](https://github.com/Whispergate/berlin/branches)[Go to Tags page](https://github.com/Whispergate/berlin/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![serexp](https://avatars.githubusercontent.com/u/160177873?v=4&size=40)](https://github.com/serexp)[serexp](https://github.com/Whispergate/berlin/commits?author=serexp)<br>[Fix preprocessor directive for CPU support checkInitial commit, push …](https://github.com/Whispergate/berlin/commit/c1c4f9af737dbfb9f05781882bfa331c750fe15e)<br>Open commit details<br>2 months agoFeb 28, 2026<br>[c1c4f9a](https://github.com/Whispergate/berlin/commit/c1c4f9af737dbfb9f05781882bfa331c750fe15e) · 2 months agoFeb 28, 2026<br>## History<br>[3 Commits](https://github.com/Whispergate/berlin/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/Whispergate/berlin/commits/main/) 3 Commits |
| [berlin.c](https://github.com/Whispergate/berlin/blob/main/berlin.c "berlin.c") | [berlin.c](https://github.com/Whispergate/berlin/blob/main/berlin.c "berlin.c") | [Initial commit, push CPU code](https://github.com/Whispergate/berlin/commit/c3c36235223a7a9c4b8c0a86bbcd58f4a4073ee2 "Initial commit, push CPU code") | 2 months agoFeb 28, 2026 |
| [berlin.h](https://github.com/Whispergate/berlin/blob/main/berlin.h "berlin.h") | [berlin.h](https://github.com/Whispergate/berlin/blob/main/berlin.h "berlin.h") | [Fix preprocessor directive for CPU support checkInitial commit, push …](https://github.com/Whispergate/berlin/commit/c1c4f9af737dbfb9f05781882bfa331c750fe15e "Fix preprocessor directive for CPU support checkInitial commit, push CPU code  Replaced non-standard #pragma error with standard #error directive.") | 2 months agoFeb 28, 2026 |
| [poc.c](https://github.com/Whispergate/berlin/blob/main/poc.c "poc.c") | [poc.c](https://github.com/Whispergate/berlin/blob/main/poc.c "poc.c") | [Initial commit, push CPU code](https://github.com/Whispergate/berlin/commit/c3c36235223a7a9c4b8c0a86bbcd58f4a4073ee2 "Initial commit, push CPU code") | 2 months agoFeb 28, 2026 |
| [readme.txt](https://github.com/Whispergate/berlin/blob/main/readme.txt "readme.txt") | [readme.txt](https://github.com/Whispergate/berlin/blob/main/readme.txt "readme.txt") | [Initial ommit, push CPU code](https://github.com/Whispergate/berlin/commit/9f3b7cbb94584f1ca991fdd0668178fd9856a03c "Initial ommit, push CPU code") | 2 months agoFeb 28, 2026 |
| View all files |

## Repository files navigation

```
------------------------------------------------------------------
| ▀█████████▄     ▄████████    ▄████████  ▄█        ▄█  ███▄▄▄▄    |
|   ███    ███   ███    ███   ███    ███ ███       ███  ███▀▀▀██▄  |
|   ███    ███   ███    █▀    ███    ███ ███       ███▌ ███   ███  |
|  ▄███▄▄▄██▀   ▄███▄▄▄      ▄███▄▄▄▄██▀ ███       ███▌ ███   ███  |
| ▀▀███▀▀▀██▄  ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   ███       ███▌ ███   ███  |
|   ███    ██▄   ███    █▄  ▀███████████ ███       ███  ███   ███  |
|   ███    ███   ███    ███   ███    ███ ███▌    ▄ ███  ███   ███  |
| ▄█████████▀    ██████████   ███    ███ █████▄▄██ █▀    ▀█   █▀   |
|                             ███    ███ ▀                         |
------------------------------------------------------------------

.........A


  /$$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$  /$$   /$$  /$$$$$$
 /$$_____/ /$$__  $$ /$$__  $$ /$$__  $$|  $$ /$$/ /$$__  $$
|  $$$$$$ | $$$$$$$$| $$  \__/| $$$$$$$$ \  $$$$/ | $$  \ $$
 \____  $$| $$_____/| $$      | $$_____/  >$$  $$ | $$  | $$
 /$$$$$$$/|  $$$$$$$| $$      |  $$$$$$$ /$$/\  $$| $$$$$$$/
|_______/  \_______/|__/       \_______/|__/  \__/| $$____/
                                                  | $$
                                                  | $$
                                                  |__/
......... PRODUCTION................................................

                Berlin: a cross-platform CPU-based
    virtual machine detection framework for modern offensive security.

=== LAYER II ====== RESEARCH...........................................

We introduce the notion that virtual machines have a general best-effort
manner as to the emulation of CPU features.
CPUs interpret programs instruction by instruction, decoding them and
executing them one by one after performing checks on them. One of these
checks is the verification of the instruction against a list of "vmexit
instruction", instructions that cannot reliably be executed on virtual
machines and require the host CPU to execute. These are notably slower
to execute, because instead of being executed in a virtualized CPU and
taking at most a few nanoseconds, vmexit instructions need to exit
virtualization, leading to some of them taking hundred of milliseconds
depending on device and configuration.
In our work, we introduce a CPU-agnostic framework for the identification
of virtual machines through the use of vmexit instructions and use
timing attacks to identify virtualization.
We offer a single entry point with a parameter:
int isVM(int threshold);

Once the threshold is reached OR surpassed, we deem that we are running
in a virtualized machine and therefore return true (aka 1). In case we
suffer from an error, we return true (1). Otherwise, false is returned,
testifying that we have made adequate testing and think we are running
on genuine bare metal.

=== LAYER III ====== ENGINEERING.........................................
The birth of this library is due to me being very bored of rewriting the
same code for VM detection in my offensive tooling and deciding to evolve
not to use third-party means of identification, such as registry keys on
Windows, because they only introduce additional IOCs and overhead while
being very easily fakeable.

These methods are all best-effort. It is entirely possible to build a
machine that can fool Berlin. It however requires what I deem significant
effort (patching kvm, qemu and more), and is enough to twart moderately-
motivated adversaries. You cannot win against a determined adversary,
anyway.

To make this library portable, I have decided to abstract OS-specific
dependencies and make the library and its POC entirely freestanding,
not requiring the C (or C++) runtime.

You may and should tune the thresholds for your target's hardware if
it is known. Default thresholds work well on my bare metal machine and
a VM, but my CPU is not the same as yours or your target's.

Compile with optimizations to reduce the size of some loops, which
makes them run faster and makes detections more accurate.

=== LAYER IV ====== Compilation........................................
Compilation is very simple:
    clang poc.c berlin.c -DDEBUG -O3

=== LAYER V ====== LICENSE.............................................
Proprietary software.
    All rights reserved to Serexp.
    No license granted.
Contact for commercial use.
```

## About

Cross-platform CPU-based virtual machine detection framework for modern offensive security.


[serexp.lain.la](https://serexp.lain.la/ "https://serexp.lain.la")

### Resources

[Readme](https://github.com/Whispergate/berlin#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/Whispergate/berlin).

[Activity](https://github.com/Whispergate/berlin/activity)

[Custom properties](https://github.com/Whispergate/berlin/custom-properties)

### Stars

[**45**\\
stars](https://github.com/Whispergate/berlin/stargazers)

### Watchers

[**1**\\
watching](https://github.com/Whispergate/berlin/watchers)

### Forks

[**3**\\
forks](https://github.com/Whispergate/berlin/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2FWhispergate%2Fberlin&report=Whispergate+%28user%29)

## [Releases](https://github.com/Whispergate/berlin/releases)

No releases published

## [Packages\  0](https://github.com/orgs/Whispergate/packages?repo_name=berlin)

No packages published

## [Contributors\  1](https://github.com/Whispergate/berlin/graphs/contributors)

- [![@serexp](https://avatars.githubusercontent.com/u/160177873?s=64&v=4)](https://github.com/serexp)[**serexp**](https://github.com/serexp)

## Languages

- [C100.0%](https://github.com/Whispergate/berlin/search?l=c)

You can’t perform that action at this time.