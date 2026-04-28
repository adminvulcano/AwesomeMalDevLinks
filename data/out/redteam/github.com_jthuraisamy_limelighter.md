# https://github.com/jthuraisamy/Limelighter

[Skip to content](https://github.com/jthuraisamy/Limelighter#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/jthuraisamy/Limelighter) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/jthuraisamy/Limelighter) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/jthuraisamy/Limelighter) to refresh your session.Dismiss alert

{{ message }}

[jthuraisamy](https://github.com/jthuraisamy)/ **[Limelighter](https://github.com/jthuraisamy/Limelighter)** Public

forked from [Tylous/Limelighter](https://github.com/Tylous/Limelighter)

- [Notifications](https://github.com/login?return_to=%2Fjthuraisamy%2FLimelighter) You must be signed in to change notification settings
- [Fork\\
2](https://github.com/login?return_to=%2Fjthuraisamy%2FLimelighter)
- [Star\\
2](https://github.com/login?return_to=%2Fjthuraisamy%2FLimelighter)


master

[**1** Branch](https://github.com/jthuraisamy/Limelighter/branches) [**0** Tags](https://github.com/jthuraisamy/Limelighter/tags)

[Go to Branches page](https://github.com/jthuraisamy/Limelighter/branches)[Go to Tags page](https://github.com/jthuraisamy/Limelighter/tags)

Go to file

Code

Open more actions menu

This branch is [4 commits ahead of](https://github.com/jthuraisamy/Limelighter/compare/Tylous%3ALimelighter%3Amaster...master) Tylous/Limelighter:master.

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![jthuraisamy](https://avatars.githubusercontent.com/u/5413071?v=4&size=40)](https://github.com/jthuraisamy)[jthuraisamy](https://github.com/jthuraisamy/Limelighter/commits?author=jthuraisamy)<br>[Update Limelighter.go](https://github.com/jthuraisamy/Limelighter/commit/cd405113e5805a204be77cf98361e2a43295f3db)<br>3 years agoDec 29, 2023<br>[cd40511](https://github.com/jthuraisamy/Limelighter/commit/cd405113e5805a204be77cf98361e2a43295f3db) · 3 years agoDec 29, 2023<br>## History<br>[21 Commits](https://github.com/jthuraisamy/Limelighter/commits/master/) <br>Open commit details<br>[View commit history for this file.](https://github.com/jthuraisamy/Limelighter/commits/master/) 21 Commits |
| [Screenshots](https://github.com/jthuraisamy/Limelighter/tree/master/Screenshots "Screenshots") | [Screenshots](https://github.com/jthuraisamy/Limelighter/tree/master/Screenshots "Screenshots") | [Version 1.2](https://github.com/jthuraisamy/Limelighter/commit/2c5ba9de5e7aae98bdad0838b2d194fe5afd223a "Version 1.2") | 5 years agoMar 17, 2021 |
| [.gitignore](https://github.com/jthuraisamy/Limelighter/blob/master/.gitignore ".gitignore") | [.gitignore](https://github.com/jthuraisamy/Limelighter/blob/master/.gitignore ".gitignore") | [Initial commit](https://github.com/jthuraisamy/Limelighter/commit/bb8c6019c47a66d64c50979254eaa2adb19d05d1 "Initial commit") | 6 years agoAug 19, 2020 |
| [LICENSE](https://github.com/jthuraisamy/Limelighter/blob/master/LICENSE "LICENSE") | [LICENSE](https://github.com/jthuraisamy/Limelighter/blob/master/LICENSE "LICENSE") | [Initial commit](https://github.com/jthuraisamy/Limelighter/commit/bb8c6019c47a66d64c50979254eaa2adb19d05d1 "Initial commit") | 6 years agoAug 19, 2020 |
| [Limelighter.go](https://github.com/jthuraisamy/Limelighter/blob/master/Limelighter.go "Limelighter.go") | [Limelighter.go](https://github.com/jthuraisamy/Limelighter/blob/master/Limelighter.go "Limelighter.go") | [Update Limelighter.go](https://github.com/jthuraisamy/Limelighter/commit/cd405113e5805a204be77cf98361e2a43295f3db "Update Limelighter.go") | 3 years agoDec 29, 2023 |
| [README.md](https://github.com/jthuraisamy/Limelighter/blob/master/README.md "README.md") | [README.md](https://github.com/jthuraisamy/Limelighter/blob/master/README.md "README.md") | [Update README.md](https://github.com/jthuraisamy/Limelighter/commit/be930a0bb1cfbfcc6f3d1de8036eb515efd80f0b "Update README.md") | 3 years agoDec 29, 2023 |
| View all files |

## Repository files navigation

# LimeLighter

[Permalink: LimeLighter](https://github.com/jthuraisamy/Limelighter#limelighter)

A tool which creates a spoof code signing certificates and sign binaries and DLL files to help evade EDR products and avoid MSS and sock scruitney. LimeLighter can also use valid code signing certificates to sign files. Limelighter can use a fully qualified domain name such as `acme.com`.

## Contributing

[Permalink: Contributing](https://github.com/jthuraisamy/Limelighter#contributing)

LimeLighter was developed in golang.

Make sure that the following are installed on your OS

```
openssl
osslsigncode
```

The first step as always is to clone the repo. Before you compile LimeLighter you'll need to install the dependencies. To install them, run following commands:

```
git clone https://github.com/Tylous/Limelighter
cd LimeLighter
go mod init github.com/Tylous/Limelighter
go get github.com/fatih/color
```

Then build it

```
go build Limelighter.go
```

## Usage

[Permalink: Usage](https://github.com/jthuraisamy/Limelighter#usage)

```
./LimeLighter -h

        .____    .__               .____    .__       .__     __
        |    |   |__| _____   ____ |    |   |__| ____ |  |___/  |_  ___________
        |    |   |  |/     \_/ __ \|    |   |  |/ ___\|  |  \   __\/ __ \_  __ \
        |    |___|  |  Y Y  \  ___/|    |___|  / /_/  >   Y  \  | \  ___/|  | \/
        |_______ \__|__|_|  /\___  >_______ \__\___  /|___|  /__|  \___  >__|
                \/        \/     \/        \/ /_____/      \/          \/
                                                        @Tyl0us

[*] A Tool for Code Signing... Real and fake
Usage of ./LimeLighter:
  -Domain string
        Domain you want to create a fake code sign for
  -I string
        Unsiged file name to be signed
  -O string
        Signed file name
  -Password string
        Password for real  certificate
  -Real string
        Path to a valid .pfx certificate file
  -Verify string
        Verifies a file's code sign certificate
  -debug
        Print debug statements
```

To sign a file you can use the command option `Domain` to generate a fake code signing certificate.

[![Signing](https://github.com/jthuraisamy/Limelighter/raw/master/Screenshots/Signing.png)](https://github.com/jthuraisamy/Limelighter/blob/master/Screenshots/Signing.png)

to sign a file with a valid code signing certificate use the `Real` and `Password` to sign a file with a valid code signing certificate.

To verify a signed file use the `verify` command.

[![Verifying](https://github.com/jthuraisamy/Limelighter/raw/master/Screenshots/Verifing.png)](https://github.com/jthuraisamy/Limelighter/blob/master/Screenshots/Verifing.png)[![WindowsVerifying](https://github.com/jthuraisamy/Limelighter/raw/master/Screenshots/WindowsVerifying.png)](https://github.com/jthuraisamy/Limelighter/blob/master/Screenshots/WindowsVerifying.png)

## About

Slightly modified Limelighter


### Resources

[Readme](https://github.com/jthuraisamy/Limelighter#readme-ov-file)

### License

[MIT license](https://github.com/jthuraisamy/Limelighter#MIT-1-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/jthuraisamy/Limelighter).

[Activity](https://github.com/jthuraisamy/Limelighter/activity)

### Stars

[**2**\\
stars](https://github.com/jthuraisamy/Limelighter/stargazers)

### Watchers

[**0**\\
watching](https://github.com/jthuraisamy/Limelighter/watchers)

### Forks

[**2**\\
forks](https://github.com/jthuraisamy/Limelighter/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fjthuraisamy%2FLimelighter&report=jthuraisamy+%28user%29)

## [Releases](https://github.com/jthuraisamy/Limelighter/releases)

No releases published

## [Packages\  0](https://github.com/users/jthuraisamy/packages?repo_name=Limelighter)

No packages published

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/jthuraisamy/Limelighter).

## [Contributors\  0](https://github.com/jthuraisamy/Limelighter/graphs/contributors)

No contributors


## Languages

- Go100.0%

You can’t perform that action at this time.