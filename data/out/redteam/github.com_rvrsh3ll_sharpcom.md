# https://github.com/rvrsh3ll/sharpcom

[Skip to content](https://github.com/rvrsh3ll/sharpcom#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/rvrsh3ll/sharpcom) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/rvrsh3ll/sharpcom) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/rvrsh3ll/sharpcom) to refresh your session.Dismiss alert

{{ message }}

[rvrsh3ll](https://github.com/rvrsh3ll)/ **[SharpCOM](https://github.com/rvrsh3ll/SharpCOM)** Public

- [Notifications](https://github.com/login?return_to=%2Frvrsh3ll%2FSharpCOM) You must be signed in to change notification settings
- [Fork\\
29](https://github.com/login?return_to=%2Frvrsh3ll%2FSharpCOM)
- [Star\\
136](https://github.com/login?return_to=%2Frvrsh3ll%2FSharpCOM)


master

[**1** Branch](https://github.com/rvrsh3ll/SharpCOM/branches) [**0** Tags](https://github.com/rvrsh3ll/SharpCOM/tags)

[Go to Branches page](https://github.com/rvrsh3ll/SharpCOM/branches)[Go to Tags page](https://github.com/rvrsh3ll/SharpCOM/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![ktlmsney](https://avatars.githubusercontent.com/u/49543676?v=4&size=40)](https://github.com/ktlmsney)[ktlmsney](https://github.com/rvrsh3ll/SharpCOM/commits?author=ktlmsney)<br>[Update Program.cs](https://github.com/rvrsh3ll/SharpCOM/commit/b8c2bfa817153c94a99b15e5b5da75b290d55c18)<br>7 years agoSep 16, 2019<br>[b8c2bfa](https://github.com/rvrsh3ll/SharpCOM/commit/b8c2bfa817153c94a99b15e5b5da75b290d55c18) · 7 years agoSep 16, 2019<br>## History<br>[5 Commits](https://github.com/rvrsh3ll/SharpCOM/commits/master/) <br>Open commit details<br>[View commit history for this file.](https://github.com/rvrsh3ll/SharpCOM/commits/master/) 5 Commits |
| [SharpCOM](https://github.com/rvrsh3ll/SharpCOM/tree/master/SharpCOM "SharpCOM") | [SharpCOM](https://github.com/rvrsh3ll/SharpCOM/tree/master/SharpCOM "SharpCOM") | [Update Program.cs](https://github.com/rvrsh3ll/SharpCOM/commit/b8c2bfa817153c94a99b15e5b5da75b290d55c18 "Update Program.cs") | 7 years agoSep 16, 2019 |
| [packages](https://github.com/rvrsh3ll/SharpCOM/tree/master/packages "packages") | [packages](https://github.com/rvrsh3ll/SharpCOM/tree/master/packages "packages") | [Initial Commit](https://github.com/rvrsh3ll/SharpCOM/commit/c26e6bed3c4d1d0f84d26253011c63030de07646 "Initial Commit") | 8 years agoDec 13, 2018 |
| [.gitattributes](https://github.com/rvrsh3ll/SharpCOM/blob/master/.gitattributes ".gitattributes") | [.gitattributes](https://github.com/rvrsh3ll/SharpCOM/blob/master/.gitattributes ".gitattributes") | [Initial commit](https://github.com/rvrsh3ll/SharpCOM/commit/aeeab7d39b252f2ea075cfaa7f33a68e9981ae6d "Initial commit") | 8 years agoDec 13, 2018 |
| [.gitignore](https://github.com/rvrsh3ll/SharpCOM/blob/master/.gitignore ".gitignore") | [.gitignore](https://github.com/rvrsh3ll/SharpCOM/blob/master/.gitignore ".gitignore") | [Initial Commit](https://github.com/rvrsh3ll/SharpCOM/commit/c26e6bed3c4d1d0f84d26253011c63030de07646 "Initial Commit") | 8 years agoDec 13, 2018 |
| [LICENSE](https://github.com/rvrsh3ll/SharpCOM/blob/master/LICENSE "LICENSE") | [LICENSE](https://github.com/rvrsh3ll/SharpCOM/blob/master/LICENSE "LICENSE") | [Initial commit](https://github.com/rvrsh3ll/SharpCOM/commit/aeeab7d39b252f2ea075cfaa7f33a68e9981ae6d "Initial commit") | 8 years agoDec 13, 2018 |
| [README.md](https://github.com/rvrsh3ll/SharpCOM/blob/master/README.md "README.md") | [README.md](https://github.com/rvrsh3ll/SharpCOM/blob/master/README.md "README.md") | [Update README.md](https://github.com/rvrsh3ll/SharpCOM/commit/842166dfcff9cb374363fcfebf86ebee0fdc91a5 "Update README.md") | 8 years agoDec 13, 2018 |
| [SharpCOM.sln](https://github.com/rvrsh3ll/SharpCOM/blob/master/SharpCOM.sln "SharpCOM.sln") | [SharpCOM.sln](https://github.com/rvrsh3ll/SharpCOM/blob/master/SharpCOM.sln "SharpCOM.sln") | [Initial Commit](https://github.com/rvrsh3ll/SharpCOM/commit/c26e6bed3c4d1d0f84d26253011c63030de07646 "Initial Commit") | 8 years agoDec 13, 2018 |
| View all files |

## Repository files navigation

# SharpCOM

[Permalink: SharpCOM](https://github.com/rvrsh3ll/sharpcom#sharpcom)

SharpCOM is a c# port of [Invoke-DCOM](https://github.com/rvrsh3ll/Misc-Powershell-Scripts/blob/master/Invoke-DCOM.ps1)

Major credit to @cobbr\_io for the initial conversion of Invoke-DCOM to c# in [SharpSploit](https://github.com/cobbr/SharpSploit/blob/master/SharpSploit/LateralMovement/DCOM.cs)

This version is meant to be a "weaponized" port of the SharpSploit DCOM lateral movement module.

As an example, one could execute SharpCOM.exe through Cobalt Strike's Beacon "execute-assembly" module.

#### Example usage

[Permalink: Example usage](https://github.com/rvrsh3ll/sharpcom#example-usage)

beacon>execute-assembly /root/SharpCOM/SharpCOM.exe --Method ShellWindows --ComputerName hosta.example.local --Command "calc.exe"

## About

CSHARP DCOM Fun


### Resources

[Readme](https://github.com/rvrsh3ll/sharpcom#readme-ov-file)

### License

[BSD-3-Clause license](https://github.com/rvrsh3ll/sharpcom#BSD-3-Clause-1-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/rvrsh3ll/sharpcom).

[Activity](https://github.com/rvrsh3ll/SharpCOM/activity)

### Stars

[**136**\\
stars](https://github.com/rvrsh3ll/SharpCOM/stargazers)

### Watchers

[**5**\\
watching](https://github.com/rvrsh3ll/SharpCOM/watchers)

### Forks

[**29**\\
forks](https://github.com/rvrsh3ll/SharpCOM/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Frvrsh3ll%2FSharpCOM&report=rvrsh3ll+%28user%29)

## [Releases](https://github.com/rvrsh3ll/SharpCOM/releases)

No releases published

## [Packages\  0](https://github.com/users/rvrsh3ll/packages?repo_name=SharpCOM)

No packages published

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/rvrsh3ll/sharpcom).

## [Contributors\  2](https://github.com/rvrsh3ll/SharpCOM/graphs/contributors)

- [![@rvrsh3ll](https://avatars.githubusercontent.com/u/6186835?s=64&v=4)](https://github.com/rvrsh3ll)[**rvrsh3ll** Steve Borosh](https://github.com/rvrsh3ll)
- [![@ktlmsney](https://avatars.githubusercontent.com/u/49543676?s=64&v=4)](https://github.com/ktlmsney)[**ktlmsney**](https://github.com/ktlmsney)

## Languages

- [C#100.0%](https://github.com/rvrsh3ll/SharpCOM/search?l=c%23)

You can’t perform that action at this time.