# https://github.com/0xROOTPLS/Doppel

[Skip to content](https://github.com/0xROOTPLS/Doppel#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/0xROOTPLS/Doppel) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/0xROOTPLS/Doppel) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/0xROOTPLS/Doppel) to refresh your session.Dismiss alert

{{ message }}

[0xROOTPLS](https://github.com/0xROOTPLS)/ **[Doppel](https://github.com/0xROOTPLS/Doppel)** Public

- [Notifications](https://github.com/login?return_to=%2F0xROOTPLS%2FDoppel) You must be signed in to change notification settings
- [Fork\\
0](https://github.com/login?return_to=%2F0xROOTPLS%2FDoppel)
- [Star\\
8](https://github.com/login?return_to=%2F0xROOTPLS%2FDoppel)


main

[**1** Branch](https://github.com/0xROOTPLS/Doppel/branches) [**0** Tags](https://github.com/0xROOTPLS/Doppel/tags)

[Go to Branches page](https://github.com/0xROOTPLS/Doppel/branches)[Go to Tags page](https://github.com/0xROOTPLS/Doppel/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![0xROOTPLS](https://avatars.githubusercontent.com/u/104942265?v=4&size=40)](https://github.com/0xROOTPLS)[0xROOTPLS](https://github.com/0xROOTPLS/Doppel/commits?author=0xROOTPLS)<br>[Update README.md](https://github.com/0xROOTPLS/Doppel/commit/5ed3332edfeb1624b88e4558b13e05fc794f1414)<br>2 years agoAug 29, 2024<br>[5ed3332](https://github.com/0xROOTPLS/Doppel/commit/5ed3332edfeb1624b88e4558b13e05fc794f1414) · 2 years agoAug 29, 2024<br>## History<br>[8 Commits](https://github.com/0xROOTPLS/Doppel/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/0xROOTPLS/Doppel/commits/main/) 8 Commits |
| [Doppel](https://github.com/0xROOTPLS/Doppel/tree/main/Doppel "Doppel") | [Doppel](https://github.com/0xROOTPLS/Doppel/tree/main/Doppel "Doppel") | [Update Doppel.cpp](https://github.com/0xROOTPLS/Doppel/commit/8b41adea08846df678989935d0cc3bd18af272c6 "Update Doppel.cpp") | 2 years agoAug 27, 2024 |
| [Flow.png](https://github.com/0xROOTPLS/Doppel/blob/main/Flow.png "Flow.png") | [Flow.png](https://github.com/0xROOTPLS/Doppel/blob/main/Flow.png "Flow.png") | [Add files via upload](https://github.com/0xROOTPLS/Doppel/commit/81b16a71433a7fc70c6b558f9e3a9aefdb914b44 "Add files via upload") | 2 years agoJul 12, 2024 |
| [README.md](https://github.com/0xROOTPLS/Doppel/blob/main/README.md "README.md") | [README.md](https://github.com/0xROOTPLS/Doppel/blob/main/README.md "README.md") | [Update README.md](https://github.com/0xROOTPLS/Doppel/commit/5ed3332edfeb1624b88e4558b13e05fc794f1414 "Update README.md") | 2 years agoAug 29, 2024 |
| View all files |

## Repository files navigation

![Alt text](https://camo.githubusercontent.com/efeb76894f8ea2b207e5e7fcb452eb05008f1f1767aa51319e99f49abcf9d739/68747470733a2f2f692e706f7374696d672e63632f7a66334e596a52762f646f7070656c2e6a7067)

# Introductory

[Permalink: Introductory](https://github.com/0xROOTPLS/Doppel#introductory)

Döppel is a program that was developed sporadically over two weeks, so please understand it may not be perfect. It is developed to return -1 and exit if any errors occur in it’s flow, so if this happens then either something went wrong, or it detected something it doesn’t want to run on. Please enjoy reversing this program, and I hope some of the parts I worked hard on might make you smile.

# A Disclaimer

[Permalink: A Disclaimer](https://github.com/0xROOTPLS/Doppel#a-disclaimer)

I made this program as a PoC (Proof of Concept) for a small competition. In no way is this program, or the payload it runs meant for harm or use on non-virtual machines. Please be responsible with the payload, and give it due respect as if it were a wild sample. Please note that this program does not cause ANY harm to the system it runs on, it purely allows for remote control via a C2 server. Please use this example for educational purposes, and enjoy!

# Important Features

[Permalink: Important Features](https://github.com/0xROOTPLS/Doppel#important-features)

I wanted Döppel to be different, so I included some non-standard things within it’s execution flow.

- Runs 8 individual virtual machine checks, querying mouse info, hardware specs, and recent activity.
- Is able to unhook ntdll.dll, and also patch ETW logging.
- Enables persistence in a non-standard fashion, using a debugger global flag attached to wuauclt.exe
- Dynamically resolves several core calls from Kernel32.dll to avoid detection.
- Decrypts the shellcode payload (XOR) ‘just in time’ within a loop, decrypting and injecting 10 chunks total to explorer.exe
- Sets the remote thread’s context to be within the MEM\_IMAGE flag containing region to evade detection (For example, evades ‘get-injectedthreads.ps1 by Lee Christensen)
- Utilizes RC4 encrypted TCP connection to the stager server, to retrieve the main payload.
- Main payload communicates using reverse-HTTPs to the C2 server.
- Utilizes unique obfuscation patterns + packing to evade RE, but probably not static analysis.
- Makes use of the 'gargoyle' technique to evade in-memory scanning of executable memory.
- Can he modified to inject any shellcode payload you'd like.
- Is easily customizable.

_If you like this, check out my UPXPatcher repo, which was made specifically for this PoC!_

## About

An Advanced, Evasive, Persistent, Shellcode Loader and Executor for Windows


### Resources

[Readme](https://github.com/0xROOTPLS/Doppel#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/0xROOTPLS/Doppel).

[Activity](https://github.com/0xROOTPLS/Doppel/activity)

### Stars

[**8**\\
stars](https://github.com/0xROOTPLS/Doppel/stargazers)

### Watchers

[**1**\\
watching](https://github.com/0xROOTPLS/Doppel/watchers)

### Forks

[**0**\\
forks](https://github.com/0xROOTPLS/Doppel/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2F0xROOTPLS%2FDoppel&report=0xROOTPLS+%28user%29)

## [Releases](https://github.com/0xROOTPLS/Doppel/releases)

No releases published

## [Packages\  0](https://github.com/users/0xROOTPLS/packages?repo_name=Doppel)

No packages published

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/0xROOTPLS/Doppel).

## [Contributors\  1](https://github.com/0xROOTPLS/Doppel/graphs/contributors)

- [![@0xROOTPLS](https://avatars.githubusercontent.com/u/104942265?s=64&v=4)](https://github.com/0xROOTPLS)[**0xROOTPLS** 0xROOTPLS](https://github.com/0xROOTPLS)

## Languages

- [C++100.0%](https://github.com/0xROOTPLS/Doppel/search?l=c%2B%2B)

You can’t perform that action at this time.