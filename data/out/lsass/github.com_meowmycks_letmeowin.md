# https://github.com/Meowmycks/LetMeowIn

[Skip to content](https://github.com/Meowmycks/LetMeowIn#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/Meowmycks/LetMeowIn) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/Meowmycks/LetMeowIn) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/Meowmycks/LetMeowIn) to refresh your session.Dismiss alert

{{ message }}

[Meowmycks](https://github.com/Meowmycks)/ **[LetMeowIn](https://github.com/Meowmycks/LetMeowIn)** Public

- [Notifications](https://github.com/login?return_to=%2FMeowmycks%2FLetMeowIn) You must be signed in to change notification settings
- [Fork\\
75](https://github.com/login?return_to=%2FMeowmycks%2FLetMeowIn)
- [Star\\
444](https://github.com/login?return_to=%2FMeowmycks%2FLetMeowIn)


main

[**1** Branch](https://github.com/Meowmycks/LetMeowIn/branches) [**0** Tags](https://github.com/Meowmycks/LetMeowIn/tags)

[Go to Branches page](https://github.com/Meowmycks/LetMeowIn/branches)[Go to Tags page](https://github.com/Meowmycks/LetMeowIn/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![Meowmycks](https://avatars.githubusercontent.com/u/45502375?v=4&size=40)](https://github.com/Meowmycks)[Meowmycks](https://github.com/Meowmycks/LetMeowIn/commits?author=Meowmycks)<br>[Update README.md](https://github.com/Meowmycks/LetMeowIn/commit/4dff7d989852169ae5963be0e863c06a5bbea798)<br>2 years agoJul 8, 2024<br>[4dff7d9](https://github.com/Meowmycks/LetMeowIn/commit/4dff7d989852169ae5963be0e863c06a5bbea798) · 2 years agoJul 8, 2024<br>## History<br>[26 Commits](https://github.com/Meowmycks/LetMeowIn/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/Meowmycks/LetMeowIn/commits/main/) 26 Commits |
| [src](https://github.com/Meowmycks/LetMeowIn/tree/main/src "src") | [src](https://github.com/Meowmycks/LetMeowIn/tree/main/src "src") | [Update includes.h](https://github.com/Meowmycks/LetMeowIn/commit/217392893c5b7be4c87681e5a7b2ce127861ce39 "Update includes.h  Added missing \"#include\" line") | 2 years agoApr 19, 2024 |
| [README.md](https://github.com/Meowmycks/LetMeowIn/blob/main/README.md "README.md") | [README.md](https://github.com/Meowmycks/LetMeowIn/blob/main/README.md "README.md") | [Update README.md](https://github.com/Meowmycks/LetMeowIn/commit/4dff7d989852169ae5963be0e863c06a5bbea798 "Update README.md") | 2 years agoJul 8, 2024 |
| [restoresig.py](https://github.com/Meowmycks/LetMeowIn/blob/main/restoresig.py "restoresig.py") | [restoresig.py](https://github.com/Meowmycks/LetMeowIn/blob/main/restoresig.py "restoresig.py") | [Add files via upload](https://github.com/Meowmycks/LetMeowIn/commit/628d4bf775ad32de829721fe0ca879243f1c21bb "Add files via upload") | 2 years agoApr 9, 2024 |
| View all files |

## Repository files navigation

# LetMeowIn

[Permalink: LetMeowIn](https://github.com/Meowmycks/LetMeowIn#letmeowin)

A sophisticated, covert LSASS dumper using C++ and MASM x64.

As seen on [Binary Defense](https://www.binarydefense.com/resources/blog/letmeowin-analysis-of-a-credential-dumper/) and [Cyber Security News](https://cybersecuritynews.com/researchers-detailed-letmeowin-credentials/)

## Disclaimer

[Permalink: Disclaimer](https://github.com/Meowmycks/LetMeowIn#disclaimer)

Don't be evil with this. I created this tool to learn. I'm not responsible if the Feds knock on your door.

* * *

Historically was able to (and may presently still) bypass

- Windows Defender
- Malwarebytes Anti-Malware
- CrowdStrike Falcon EDR (Falcon Complete + OverWatch)
- Palo Alto Cortex xDR _(When combined with strong initial access methods)_

![image](https://private-user-images.githubusercontent.com/45502375/322916182-fb99f6e3-abb4-4beb-9130-dfbc550e1abe.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzM4MjkxNjYsIm5iZiI6MTc3MzgyODg2NiwicGF0aCI6Ii80NTUwMjM3NS8zMjI5MTYxODItZmI5OWY2ZTMtYWJiNC00YmViLTkxMzAtZGZiYzU1MGUxYWJlLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAzMTglMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMzE4VDEwMTQyNlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTY3Yzc2NjQ1YTMzMjViZDJkNDQ2MmNhY2YwNjQ1N2IwMmIzYzk0ZjM0ZDFmM2YzMDI2NzgwNGZlMDY0YjQwNmUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.FVAKzzFnqWTN3pYOmQxGEbWoyu58aYJ0NHfvkcUDNVc)

## Features

[Permalink: Features](https://github.com/Meowmycks/LetMeowIn#features)

Avoids detection by using various means, such as:

- Manually implementing NTAPI operations through indirect system calls
- ~~Disabling~~ Breaking telemetry features (i.e ETW)
- Polymorphism through compile-time hash generation
- Obfuscating API function names and pointers
- Duplicating existing LSASS handles instead of opening new ones
- Creating offline copies of the LSASS process to perform memory dumps on
- Corrupting the `MDMP` signature of dropped files
- Probably other stuff I forgot to mention here

## Negatives

[Permalink: Negatives](https://github.com/Meowmycks/LetMeowIn#negatives)

- Only works on x64 architecture
- Relies on there being [existing opened LSASS handles](https://itm4n.github.io/lsass-runasppl/#technique-3--python--katz) on target systems
- Don't expect this to be undetectable forever 🙂

## About

A sophisticated, covert Windows-based credential dumper using C++ and MASM x64.


### Resources

[Readme](https://github.com/Meowmycks/LetMeowIn#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/Meowmycks/LetMeowIn).

[Activity](https://github.com/Meowmycks/LetMeowIn/activity)

### Stars

[**444**\\
stars](https://github.com/Meowmycks/LetMeowIn/stargazers)

### Watchers

[**11**\\
watching](https://github.com/Meowmycks/LetMeowIn/watchers)

### Forks

[**75**\\
forks](https://github.com/Meowmycks/LetMeowIn/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2FMeowmycks%2FLetMeowIn&report=Meowmycks+%28user%29)

## [Releases](https://github.com/Meowmycks/LetMeowIn/releases)

No releases published

## [Packages\  0](https://github.com/users/Meowmycks/packages?repo_name=LetMeowIn)

No packages published

## [Contributors\  1](https://github.com/Meowmycks/LetMeowIn/graphs/contributors)

- [![@Meowmycks](https://avatars.githubusercontent.com/u/45502375?s=64&v=4)](https://github.com/Meowmycks)[**Meowmycks**](https://github.com/Meowmycks)

## Languages

- [C++69.1%](https://github.com/Meowmycks/LetMeowIn/search?l=c%2B%2B)
- [C20.0%](https://github.com/Meowmycks/LetMeowIn/search?l=c)
- [Assembly9.6%](https://github.com/Meowmycks/LetMeowIn/search?l=assembly)
- [Python1.3%](https://github.com/Meowmycks/LetMeowIn/search?l=python)

You can’t perform that action at this time.