# https://github.com/Tylous/Mangle

[Skip to content](https://github.com/Tylous/Mangle#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/Tylous/Mangle) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/Tylous/Mangle) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/Tylous/Mangle) to refresh your session.Dismiss alert

{{ message }}

[Tylous](https://github.com/Tylous)/ **[Mangle](https://github.com/Tylous/Mangle)** Public

forked from [optiv/Mangle](https://github.com/optiv/Mangle)

- [Notifications](https://github.com/login?return_to=%2FTylous%2FMangle) You must be signed in to change notification settings
- [Fork\\
12](https://github.com/login?return_to=%2FTylous%2FMangle)
- [Star\\
104](https://github.com/login?return_to=%2FTylous%2FMangle)


main

[**1** Branch](https://github.com/Tylous/Mangle/branches) [**0** Tags](https://github.com/Tylous/Mangle/tags)

[Go to Branches page](https://github.com/Tylous/Mangle/branches)[Go to Tags page](https://github.com/Tylous/Mangle/tags)

Go to file

Code

Open more actions menu

This branch is [1 commit behind](https://github.com/Tylous/Mangle/compare/main...optiv%3AMangle%3Amain) optiv/Mangle:main.

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![Tylous](https://avatars.githubusercontent.com/u/15052743?v=4&size=40)](https://github.com/Tylous)[Tylous](https://github.com/Tylous/Mangle/commits?author=Tylous)<br>[v1.2](https://github.com/Tylous/Mangle/commit/32bf6837192b58508b614a9f25329560b5da4df4)<br>4 years agoDec 15, 2022<br>[32bf683](https://github.com/Tylous/Mangle/commit/32bf6837192b58508b614a9f25329560b5da4df4) · 4 years agoDec 15, 2022<br>## History<br>[5 Commits](https://github.com/Tylous/Mangle/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/Tylous/Mangle/commits/main/) 5 Commits |
| [Screenshots](https://github.com/Tylous/Mangle/tree/main/Screenshots "Screenshots") | [Screenshots](https://github.com/Tylous/Mangle/tree/main/Screenshots "Screenshots") | [v1.0](https://github.com/Tylous/Mangle/commit/02759612acab9e564456ceb96fbd626cd842f09e "v1.0") | 4 years agoJun 21, 2022 |
| [LICENSE](https://github.com/Tylous/Mangle/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/Tylous/Mangle/blob/main/LICENSE "LICENSE") | [Initial commit](https://github.com/Tylous/Mangle/commit/dde0d266511f5b383fad57f20521c24f5c799020 "Initial commit") | 4 years agoJun 21, 2022 |
| [Mangle.go](https://github.com/Tylous/Mangle/blob/main/Mangle.go "Mangle.go") | [Mangle.go](https://github.com/Tylous/Mangle/blob/main/Mangle.go "Mangle.go") | [v1.2](https://github.com/Tylous/Mangle/commit/bd196daa0fac8aa3c2cfdb7694dc59d81badda54 "v1.2") | 4 years agoDec 15, 2022 |
| [README.md](https://github.com/Tylous/Mangle/blob/main/README.md "README.md") | [README.md](https://github.com/Tylous/Mangle/blob/main/README.md "README.md") | [v1.0](https://github.com/Tylous/Mangle/commit/02759612acab9e564456ceb96fbd626cd842f09e "v1.0") | 4 years agoJun 21, 2022 |
| [go.mod](https://github.com/Tylous/Mangle/blob/main/go.mod "go.mod") | [go.mod](https://github.com/Tylous/Mangle/blob/main/go.mod "go.mod") | [v1.1](https://github.com/Tylous/Mangle/commit/27bceefd4fdd73ebfeb3ef4fe796e99df03bc5b8 "v1.1") | 4 years agoOct 4, 2022 |
| [go.sum](https://github.com/Tylous/Mangle/blob/main/go.sum "go.sum") | [go.sum](https://github.com/Tylous/Mangle/blob/main/go.sum "go.sum") | [v1.1](https://github.com/Tylous/Mangle/commit/27bceefd4fdd73ebfeb3ef4fe796e99df03bc5b8 "v1.1") | 4 years agoOct 4, 2022 |
| View all files |

## Repository files navigation

# Mangle

[Permalink: Mangle](https://github.com/Tylous/Mangle#mangle)

[![](https://github.com/Tylous/Mangle/raw/main/Screenshots/logo.png)](https://github.com/Tylous/Mangle/blob/main/Screenshots/logo.png)

**Authored By Tyl0us**

**Featured at Source Zero Con 2022**

Mangle is a tool that manipulates aspects of compiled executables (.exe or DLL). Mangle can remove known Indicators of Compromise (IoC) based strings and replace them with random characters, change the file by inflating the size to avoid EDRs, and can clone code-signing certs from legitimate files. In doing so, Mangle helps loaders evade on-disk and in-memory scanners.

## Contributing

[Permalink: Contributing](https://github.com/Tylous/Mangle#contributing)

Mangle was developed in Golang.

## Install

[Permalink: Install](https://github.com/Tylous/Mangle#install)

The first step, as always, is to clone the repo. Before you compile Mangle, you'll need to install the dependencies. To install them, run the following commands:

```
go get github.com/Binject/debug/pe
```

Then build it

```
go build Mangle.go
```

## Important

[Permalink: Important](https://github.com/Tylous/Mangle#important)

While Mangle is written in Golang, a lot of the features are designed to work on executable files from other languages. At the time of release, the only feature that is Golang specific is the string manipulation part.

## Usage

[Permalink: Usage](https://github.com/Tylous/Mangle#usage)

```
./mangle -h

	   _____                        .__
	  /     \ _____    ____    ____ |  |   ____
	 /  \ /  \\__  \  /    \  / ___\|  | _/ __ \
	/    Y    \/ __ \|   |  \/ /_/  >  |_\  ___/
	\____|__  (____  /___|  /\___  /|____/\___  >
		\/     \/     \//_____/   	  \/
					(@Tyl0us)
Usage of ./Mangle:
  -C string
        Path to the file containing the certificate you want to clone
  -I string
        Path to the orginal file
  -M    Edit the PE file to strip out Go indicators
  -O string
        The new file name
  -S int
        How many MBs to increase the file by
```

## Strings

[Permalink: Strings](https://github.com/Tylous/Mangle#strings)

Mangle takes the input executable and looks for known strings that security products look for or alert on. These strings alone are not the sole point of detection. Often, these strings are in conjunction with other data points and pieces of telemetry for detection and prevention. Mangle finds these known strings and replaces the hex values with random ones to remove them. IMPORTANT: Mangle replaces the exact size of the strings it’s manipulating. It doesn’t add any more or any less, as this would create misalignments and instabilities in the file. Mangle does this using the `-M` command-line option.

Currently, Mangle only does Golang files but as time goes on other languages will be added. If you know of any for other languages, please open an issue ticket and submit them.

**Before**

[![](https://github.com/Tylous/Mangle/raw/main/Screenshots/Strings_Before.png)](https://github.com/Tylous/Mangle/blob/main/Screenshots/Strings_Before.png)

**After**

[![](https://github.com/Tylous/Mangle/raw/main/Screenshots/Strings_After.png)](https://github.com/Tylous/Mangle/blob/main/Screenshots/Strings_After.png)

## Inflate

[Permalink: Inflate](https://github.com/Tylous/Mangle#inflate)

Pretty much all EDRs can’t scan both on disk or in memory files beyond a certain size. This simply stems from the fact that large files take longer to review, scan, or monitor. EDRs do not want to impact performance by slowing down the user's productivity. Mangle inflates files by creating a padding of Null bytes (Zeros) at the end of the file. This ensures that nothing inside the file is impacted. To inflate an executable, use the `-S` command-line option along with the number of bytes you want to add to the file. Large payloads are really not an issue anymore with how fast Internet speeds are, that being said, it's not recommended to make a 2 gig file.

Based on test cases across numerous userland and kernel EDRs, it is recommended to increase the size by either 95-100 megabytes. Because vendors do not check large files, the activity goes unnoticed, resulting in the successful execution of shellcode.

### Example:

[Permalink: Example:](https://github.com/Tylous/Mangle#example)

[![](https://github.com/Tylous/Mangle/raw/main/Screenshots/Demo.gif)](https://github.com/Tylous/Mangle/blob/main/Screenshots/Demo.gif)[![Demo.gif](https://github.com/Tylous/Mangle/raw/main/Screenshots/Demo.gif)](https://github.com/Tylous/Mangle/blob/main/Screenshots/Demo.gif)[Open Demo.gif in new window](https://github.com/Tylous/Mangle/blob/main/Screenshots/Demo.gif)

## Certificate

[Permalink: Certificate](https://github.com/Tylous/Mangle#certificate)

Mangle also contains the ability to take the full chain and all attributes from a legitimate code-signing certificate from a file and copy it onto another file. This includes the signing date, counter signatures, and other measurable attributes.

While this feature may sound similar to another tool I developed, [Limelighter](https://github.com/Tylous/Limelighter), the major difference between the two is that Limelighter makes a fake certificate based off a domain and signs it with the current date and time, versus using valid attributes where the timestamp is taken from when the original file. This option can use DLL or .exe files to copy using the `-C` command-line option, along with the path to the file you want to copy the certificate from.

[![](https://github.com/Tylous/Mangle/raw/main/Screenshots/Cert_Copy.png)](https://github.com/Tylous/Mangle/blob/main/Screenshots/Cert_Copy.png)

## Credit

[Permalink: Credit](https://github.com/Tylous/Mangle#credit)

- Special thanks to Jessica of SuperNovasStore for creating the logo.
- Special thanks to Binject for his [repo](https://github.com/Binject/debug)

## About

Mangle is a tool that manipulates aspects of compiled executables (.exe or DLL) to avoid detection from EDRs


### Resources

[Readme](https://github.com/Tylous/Mangle#readme-ov-file)

### License

[MIT license](https://github.com/Tylous/Mangle#MIT-1-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/Tylous/Mangle).

[Activity](https://github.com/Tylous/Mangle/activity)

### Stars

[**104**\\
stars](https://github.com/Tylous/Mangle/stargazers)

### Watchers

[**2**\\
watching](https://github.com/Tylous/Mangle/watchers)

### Forks

[**12**\\
forks](https://github.com/Tylous/Mangle/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2FTylous%2FMangle&report=Tylous+%28user%29)

## [Releases](https://github.com/Tylous/Mangle/releases)

No releases published

## [Packages\  0](https://github.com/users/Tylous/packages?repo_name=Mangle)

No packages published

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/Tylous/Mangle).

## [Contributors\  0](https://github.com/Tylous/Mangle/graphs/contributors)

No contributors


## Languages

- Go100.0%

You can’t perform that action at this time.