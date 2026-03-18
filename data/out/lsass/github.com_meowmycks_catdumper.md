# https://github.com/Meowmycks/catdumper

[Skip to content](https://github.com/Meowmycks/catdumper#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/Meowmycks/catdumper) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/Meowmycks/catdumper) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/Meowmycks/catdumper) to refresh your session.Dismiss alert

{{ message }}

[Meowmycks](https://github.com/Meowmycks)/ **[catdumper](https://github.com/Meowmycks/catdumper)** Public

- [Notifications](https://github.com/login?return_to=%2FMeowmycks%2Fcatdumper) You must be signed in to change notification settings
- [Fork\\
6](https://github.com/login?return_to=%2FMeowmycks%2Fcatdumper)
- [Star\\
13](https://github.com/login?return_to=%2FMeowmycks%2Fcatdumper)


main

[**1** Branch](https://github.com/Meowmycks/catdumper/branches) [**0** Tags](https://github.com/Meowmycks/catdumper/tags)

[Go to Branches page](https://github.com/Meowmycks/catdumper/branches)[Go to Tags page](https://github.com/Meowmycks/catdumper/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![Meowmycks](https://avatars.githubusercontent.com/u/45502375?v=4&size=40)](https://github.com/Meowmycks)[Meowmycks](https://github.com/Meowmycks/catdumper/commits?author=Meowmycks)<br>[Update catdumper.cpp](https://github.com/Meowmycks/catdumper/commit/f8ddaea9df76cde54318ca8169da798f29e740aa)<br>Open commit details<br>3 years agoJan 10, 2024<br>[f8ddaea](https://github.com/Meowmycks/catdumper/commit/f8ddaea9df76cde54318ca8169da798f29e740aa) · 3 years agoJan 10, 2024<br>## History<br>[44 Commits](https://github.com/Meowmycks/catdumper/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/Meowmycks/catdumper/commits/main/) 44 Commits |
| [README.md](https://github.com/Meowmycks/catdumper/blob/main/README.md "README.md") | [README.md](https://github.com/Meowmycks/catdumper/blob/main/README.md "README.md") | [Update README.md](https://github.com/Meowmycks/catdumper/commit/81756e9ef93ce41f662e02695535b5e04b328c4b "Update README.md  Removed unnecessary lines.") | 3 years agoJan 10, 2024 |
| [catdumper.cpp](https://github.com/Meowmycks/catdumper/blob/main/catdumper.cpp "catdumper.cpp") | [catdumper.cpp](https://github.com/Meowmycks/catdumper/blob/main/catdumper.cpp "catdumper.cpp") | [Update catdumper.cpp](https://github.com/Meowmycks/catdumper/commit/f8ddaea9df76cde54318ca8169da798f29e740aa "Update catdumper.cpp  Explained what \"case 16\" means on line 29.") | 3 years agoJan 10, 2024 |
| [catdumper.h](https://github.com/Meowmycks/catdumper/blob/main/catdumper.h "catdumper.h") | [catdumper.h](https://github.com/Meowmycks/catdumper/blob/main/catdumper.h "catdumper.h") | [Update catdumper.h](https://github.com/Meowmycks/catdumper/commit/2ae6cc68f427539e15466e972164edd0ba02e1fc "Update catdumper.h  Moved over lines from the `.cpp` file typically meant to be placed here.") | 3 years agoJan 10, 2024 |
| [exfil.py](https://github.com/Meowmycks/catdumper/blob/main/exfil.py "exfil.py") | [exfil.py](https://github.com/Meowmycks/catdumper/blob/main/exfil.py "exfil.py") | [Update exfil.py](https://github.com/Meowmycks/catdumper/commit/b5a4f8a2a8ff20cd9b3aebd50ead702a7a5c2162 "Update exfil.py  Added a comment explaining what to do in case of protocol errors.") | 3 years agoJan 9, 2024 |
| View all files |

## Repository files navigation

# catdumper

[Permalink: catdumper](https://github.com/Meowmycks/catdumper#catdumper)

## Disclaimer

[Permalink: Disclaimer](https://github.com/Meowmycks/catdumper#disclaimer)

Don't be evil with this. I created this tool to learn. I'm not responsible if the Feds knock on your door.

## Overview

[Permalink: Overview](https://github.com/Meowmycks/catdumper#overview)

`catdumper.exe` takes a snapshot of the LSASS process, creates a MiniDump of it, RC4 encrypts it with a randomly-generated string, and Base64 encodes it, all in-memory.

While still in-memory, the encrypted MiniDump and its key are exfiltrated over an HTTPS connection to a Python Flask server, `exfil.py` you run on your machine.

The Flask server decodes and decrypts the data locally before dropping it to the disk. After that, you can open it in Mimikatz like normal.

Compile as a VS2022 project and run as Administrator. You can figure out that part :)

## Features

[Permalink: Features](https://github.com/Meowmycks/catdumper#features)

- Uses polymorphism with compiletime RNG to always generate a unique file signature.
- Unhooks NtReadVirtualMemory to defeat EDR userland hooking.
- Also tricks heuristics by performing multiple benign Windows API functions.
- Encrypting and encoding MiniDump in-memory means AV/EDRs _shouldn't_ flag it.
- Strings that might raise flags are obfuscated (e.g "lsass.exe").
- Packet size and time between requests is randomized.

## Demo

[Permalink: Demo](https://github.com/Meowmycks/catdumper#demo)

![catdumper_demo](https://private-user-images.githubusercontent.com/45502375/295127593-2f6b5c33-de3b-4243-afdb-4ea84b017efb.gif?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzM4MjkxNjgsIm5iZiI6MTc3MzgyODg2OCwicGF0aCI6Ii80NTUwMjM3NS8yOTUxMjc1OTMtMmY2YjVjMzMtZGUzYi00MjQzLWFmZGItNGVhODRiMDE3ZWZiLmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAzMTglMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMzE4VDEwMTQyOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWFkMzg2ZDZkNmY3YjE0NWQ2M2I1NTQyYzBkZTk4NDEzNDUxMTYyM2ViMDUzZmI0YjU4YjQ2YzJlNjkyMmZjNmUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.jnAVD9qm6G5QoyV0OZfMtC4F88gZsj3SPV4gowE-ee0)![catdumper_demo](https://private-user-images.githubusercontent.com/45502375/295127593-2f6b5c33-de3b-4243-afdb-4ea84b017efb.gif?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzM4MjkxNjgsIm5iZiI6MTc3MzgyODg2OCwicGF0aCI6Ii80NTUwMjM3NS8yOTUxMjc1OTMtMmY2YjVjMzMtZGUzYi00MjQzLWFmZGItNGVhODRiMDE3ZWZiLmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAzMTglMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMzE4VDEwMTQyOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWFkMzg2ZDZkNmY3YjE0NWQ2M2I1NTQyYzBkZTk4NDEzNDUxMTYyM2ViMDUzZmI0YjU4YjQ2YzJlNjkyMmZjNmUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.jnAVD9qm6G5QoyV0OZfMtC4F88gZsj3SPV4gowE-ee0)[Open catdumper_demo in new window](https://private-user-images.githubusercontent.com/45502375/295127593-2f6b5c33-de3b-4243-afdb-4ea84b017efb.gif?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzM4MjkxNjgsIm5iZiI6MTc3MzgyODg2OCwicGF0aCI6Ii80NTUwMjM3NS8yOTUxMjc1OTMtMmY2YjVjMzMtZGUzYi00MjQzLWFmZGItNGVhODRiMDE3ZWZiLmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAzMTglMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMzE4VDEwMTQyOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWFkMzg2ZDZkNmY3YjE0NWQ2M2I1NTQyYzBkZTk4NDEzNDUxMTYyM2ViMDUzZmI0YjU4YjQ2YzJlNjkyMmZjNmUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.jnAVD9qm6G5QoyV0OZfMtC4F88gZsj3SPV4gowE-ee0)

## About

LSASS Credential Dumper that utilizes the Windows API, in-memory RC4 encryption and Base64 encoding, and HTTPS exfiltration.


### Resources

[Readme](https://github.com/Meowmycks/catdumper#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/Meowmycks/catdumper).

[Activity](https://github.com/Meowmycks/catdumper/activity)

### Stars

[**13**\\
stars](https://github.com/Meowmycks/catdumper/stargazers)

### Watchers

[**2**\\
watching](https://github.com/Meowmycks/catdumper/watchers)

### Forks

[**6**\\
forks](https://github.com/Meowmycks/catdumper/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2FMeowmycks%2Fcatdumper&report=Meowmycks+%28user%29)

## [Releases](https://github.com/Meowmycks/catdumper/releases)

No releases published

## [Packages\  0](https://github.com/users/Meowmycks/packages?repo_name=catdumper)

No packages published

## [Contributors\  1](https://github.com/Meowmycks/catdumper/graphs/contributors)

- [![@Meowmycks](https://avatars.githubusercontent.com/u/45502375?s=64&v=4)](https://github.com/Meowmycks)[**Meowmycks**](https://github.com/Meowmycks)

## Languages

- [C++89.9%](https://github.com/Meowmycks/catdumper/search?l=c%2B%2B)
- [Python10.1%](https://github.com/Meowmycks/catdumper/search?l=python)

You can’t perform that action at this time.