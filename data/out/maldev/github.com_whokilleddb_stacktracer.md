# https://github.com/whokilleddb/stacktracer

[Skip to content](https://github.com/whokilleddb/stacktracer#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/whokilleddb/stacktracer) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/whokilleddb/stacktracer) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/whokilleddb/stacktracer) to refresh your session.Dismiss alert

{{ message }}

[whokilleddb](https://github.com/whokilleddb)/ **[stacktracer](https://github.com/whokilleddb/stacktracer)** Public

- [Notifications](https://github.com/login?return_to=%2Fwhokilleddb%2Fstacktracer) You must be signed in to change notification settings
- [Fork\\
1](https://github.com/login?return_to=%2Fwhokilleddb%2Fstacktracer)
- [Star\\
45](https://github.com/login?return_to=%2Fwhokilleddb%2Fstacktracer)


main

[**1** Branch](https://github.com/whokilleddb/stacktracer/branches) [**0** Tags](https://github.com/whokilleddb/stacktracer/tags)

[Go to Branches page](https://github.com/whokilleddb/stacktracer/branches)[Go to Tags page](https://github.com/whokilleddb/stacktracer/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>![author](https://github.githubassets.com/images/gravatars/gravatar-user-420.png?size=40)<br>DB<br>[Added tracer](https://github.com/whokilleddb/stacktracer/commit/8eebd7fd0de868becb378fd833e1e098d12c73bb)<br>last weekMar 8, 2026<br>[8eebd7f](https://github.com/whokilleddb/stacktracer/commit/8eebd7fd0de868becb378fd833e1e098d12c73bb) · last weekMar 8, 2026<br>## History<br>[4 Commits](https://github.com/whokilleddb/stacktracer/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/whokilleddb/stacktracer/commits/main/) 4 Commits |
| [.cargo](https://github.com/whokilleddb/stacktracer/tree/main/.cargo ".cargo") | [.cargo](https://github.com/whokilleddb/stacktracer/tree/main/.cargo ".cargo") | [Initial commit](https://github.com/whokilleddb/stacktracer/commit/1c18c58b21d923abd5cc986d67be57e701b6c3e1 "Initial commit") | 2 weeks agoMar 7, 2026 |
| [src](https://github.com/whokilleddb/stacktracer/tree/main/src "src") | [src](https://github.com/whokilleddb/stacktracer/tree/main/src "src") | [Update README](https://github.com/whokilleddb/stacktracer/commit/45c76ad2f5c9f36e0bd3c5dbfd36f07e870a828c "Update README") | last weekMar 8, 2026 |
| [.gitignore](https://github.com/whokilleddb/stacktracer/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/whokilleddb/stacktracer/blob/main/.gitignore ".gitignore") | [Initial commit](https://github.com/whokilleddb/stacktracer/commit/1c18c58b21d923abd5cc986d67be57e701b6c3e1 "Initial commit") | 2 weeks agoMar 7, 2026 |
| [Cargo.lock](https://github.com/whokilleddb/stacktracer/blob/main/Cargo.lock "Cargo.lock") | [Cargo.lock](https://github.com/whokilleddb/stacktracer/blob/main/Cargo.lock "Cargo.lock") | [Added tracer](https://github.com/whokilleddb/stacktracer/commit/8eebd7fd0de868becb378fd833e1e098d12c73bb "Added tracer") | last weekMar 8, 2026 |
| [Cargo.toml](https://github.com/whokilleddb/stacktracer/blob/main/Cargo.toml "Cargo.toml") | [Cargo.toml](https://github.com/whokilleddb/stacktracer/blob/main/Cargo.toml "Cargo.toml") | [Added tracer](https://github.com/whokilleddb/stacktracer/commit/8eebd7fd0de868becb378fd833e1e098d12c73bb "Added tracer") | last weekMar 8, 2026 |
| [README.md](https://github.com/whokilleddb/stacktracer/blob/main/README.md "README.md") | [README.md](https://github.com/whokilleddb/stacktracer/blob/main/README.md "README.md") | [Added tracer](https://github.com/whokilleddb/stacktracer/commit/8eebd7fd0de868becb378fd833e1e098d12c73bb "Added tracer") | last weekMar 8, 2026 |
| View all files |

## Repository files navigation

# StackTracer

[Permalink: StackTracer](https://github.com/whokilleddb/stacktracer#stacktracer)

[!["Buy Me A Coffee"](https://camo.githubusercontent.com/9f44ce2dc3b3eecdd02598900866ffc518801df1932849703dae1e5ce5031070/68747470733a2f2f7777772e6275796d6561636f666665652e636f6d2f6173736574732f696d672f637573746f6d5f696d616765732f6f72616e67655f696d672e706e67)](https://www.buymeacoffee.com/whokilleddb)

The goal of this project is find valid stack frames which you can replicate in your payloads. In C2s like BRC4, you can specify a stack frame which looks legit - and this can help in increasing the evasiveness of your shellcode. Using this tool you can examine legit processes for their stack frames and copy them over.

## Building

[Permalink: Building](https://github.com/whokilleddb/stacktracer#building)

Building this tool is as easy as rust makes it:

```
$ cargo build --release
```

Note that you might need to install the `x86_64-pc-windows-gnu` toolchain

## Usage:

[Permalink: Usage:](https://github.com/whokilleddb/stacktracer#usage)

To view a detailed usage guide, you can pass the `--help` flag:

```
Z:\> stacktracer.exe --help
  _____ _             _ _______
 / ____| |           | |__   __|
| (___ | |_ __ _  ___| | _| |_ __ __ _  ___ ___ _ __
 \___ \| __/ _` |/ __| |/ / | '__/ _` |/ __/ _ \ '__|
 ____) | || (_| | (__|   <| | | | (_| | (_|  __/ |
|_____/ \__\__,_|\___|_|\_\_|_|  \__,_|\___\___|_|
                                      DB @whokilleddb

A rust program to print the stack trace of a given thread

Usage: stacktracer.exe [OPTIONS] --pid <pid>

Options:
      --pid <pid>    Process ID
      --tid <tid>    Thread ID (defaults to 0) [default: 0]
      --hide-banner  Hide the banner
  -h, --help         Print help
  -V, --version      Print version
```

The only required option is the `--pid` flag. To enumerate a process without targetting a particular thread, you go like:

```
Z:\> stacktracer.exe --pid 1234
```

To enumerate a specific thread, you can specify the ThreadID using the `--tid` flag:

```
Z:\>.\stacktracer.exe --pid 3688 --tid 7336
  _____ _             _ _______
 / ____| |           | |__   __|
| (___ | |_ __ _  ___| | _| |_ __ __ _  ___ ___ _ __
 \___ \| __/ _` |/ __| |/ / | '__/ _` |/ __/ _ \ '__|
 ____) | || (_| | (__|   <| | | | (_| | (_|  __/ |
|_____/ \__\__,_|\___|_|\_\_|_|  \__,_|\___\___|_|
                                      DB @whokilleddb

PID     | TID   | STACK FRAME
3688    | 7336  | win32u.dll!NtUserWaitMessage+0x14,USER32.DLL!IsDialogMessageA+0x3ba,USER32.DLL!Ordinal2635+0x267,USER32.DLL!SoftModalMessageBox+0x5b6,USER32.DLL!MessageBoxIndirectA+0x562,USER32.DLL!MessageBoxTimeoutW+0x18f,USER32.DLL!MessageBoxTimeoutA+0x100,USER32.DLL!MessageBoxA+0x45,0x25c70680050,KERNEL32.DLL+0x0
```

_Hope this helps!_

## About

Print the stack trace


### Resources

[Readme](https://github.com/whokilleddb/stacktracer#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/whokilleddb/stacktracer).

[Activity](https://github.com/whokilleddb/stacktracer/activity)

### Stars

[**45**\\
stars](https://github.com/whokilleddb/stacktracer/stargazers)

### Watchers

[**0**\\
watching](https://github.com/whokilleddb/stacktracer/watchers)

### Forks

[**1**\\
fork](https://github.com/whokilleddb/stacktracer/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fwhokilleddb%2Fstacktracer&report=whokilleddb+%28user%29)

## [Releases](https://github.com/whokilleddb/stacktracer/releases)

No releases published

## [Packages\  0](https://github.com/users/whokilleddb/packages?repo_name=stacktracer)

No packages published

## [Contributors\  0](https://github.com/whokilleddb/stacktracer/graphs/contributors)

No contributors


## Languages

- [Rust100.0%](https://github.com/whokilleddb/stacktracer/search?l=rust)

You can’t perform that action at this time.