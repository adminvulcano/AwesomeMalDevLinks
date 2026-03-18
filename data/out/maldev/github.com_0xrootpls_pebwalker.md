# https://github.com/0xROOTPLS/PEBwalker

[Skip to content](https://github.com/0xROOTPLS/PEBwalker#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/0xROOTPLS/PEBwalker) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/0xROOTPLS/PEBwalker) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/0xROOTPLS/PEBwalker) to refresh your session.Dismiss alert

{{ message }}

[0xROOTPLS](https://github.com/0xROOTPLS)/ **[PEBwalker](https://github.com/0xROOTPLS/PEBwalker)** Public

- [Notifications](https://github.com/login?return_to=%2F0xROOTPLS%2FPEBwalker) You must be signed in to change notification settings
- [Fork\\
0](https://github.com/login?return_to=%2F0xROOTPLS%2FPEBwalker)
- [Star\\
0](https://github.com/login?return_to=%2F0xROOTPLS%2FPEBwalker)


main

[**1** Branch](https://github.com/0xROOTPLS/PEBwalker/branches) [**0** Tags](https://github.com/0xROOTPLS/PEBwalker/tags)

[Go to Branches page](https://github.com/0xROOTPLS/PEBwalker/branches)[Go to Tags page](https://github.com/0xROOTPLS/PEBwalker/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![0xROOTPLS](https://avatars.githubusercontent.com/u/104942265?v=4&size=40)](https://github.com/0xROOTPLS)[0xROOTPLS](https://github.com/0xROOTPLS/PEBwalker/commits?author=0xROOTPLS)<br>[Delete peb.exe](https://github.com/0xROOTPLS/PEBwalker/commit/c1429face6f8e51d1578f7af907dfb29145f4783)<br>2 years agoNov 4, 2024<br>[c1429fa](https://github.com/0xROOTPLS/PEBwalker/commit/c1429face6f8e51d1578f7af907dfb29145f4783) · 2 years agoNov 4, 2024<br>## History<br>[5 Commits](https://github.com/0xROOTPLS/PEBwalker/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/0xROOTPLS/PEBwalker/commits/main/) 5 Commits |
| [Cargo.toml](https://github.com/0xROOTPLS/PEBwalker/blob/main/Cargo.toml "Cargo.toml") | [Cargo.toml](https://github.com/0xROOTPLS/PEBwalker/blob/main/Cargo.toml "Cargo.toml") | [Add files via upload](https://github.com/0xROOTPLS/PEBwalker/commit/f53e606dede01a494570ad2928b1bbf39f4e3476 "Add files via upload") | 2 years agoNov 4, 2024 |
| [README.md](https://github.com/0xROOTPLS/PEBwalker/blob/main/README.md "README.md") | [README.md](https://github.com/0xROOTPLS/PEBwalker/blob/main/README.md "README.md") | [Update README.md](https://github.com/0xROOTPLS/PEBwalker/commit/748a9726d8ebc3a6abcd6fee7f9377ed65f48ebc "Update README.md") | 2 years agoNov 4, 2024 |
| [main.rs](https://github.com/0xROOTPLS/PEBwalker/blob/main/main.rs "main.rs") | [main.rs](https://github.com/0xROOTPLS/PEBwalker/blob/main/main.rs "main.rs") | [Update main.rs](https://github.com/0xROOTPLS/PEBwalker/commit/5574a5c324f94bdd1206ab88b575a526aad17814 "Update main.rs  critical [ALWAYS TRUE] logic flaw corrected") | 2 years agoNov 4, 2024 |
| View all files |

## Repository files navigation

# PEBwalker

[Permalink: PEBwalker](https://github.com/0xROOTPLS/PEBwalker#pebwalker)

A PEB walker that resolves function addresses via runtime hash comparison, avoiding static imports.

## Flow

[Permalink: Flow](https://github.com/0xROOTPLS/PEBwalker#flow)

1. Calculates hash for target module & function
2. Access process environment block (PEB)
3. Walk loaded module list
4. Match module via hash
5. Parses module exports
6. Resolves functions via hash
7. Returns function pointer of target
8. Profit

## Detections

[Permalink: Detections](https://github.com/0xROOTPLS/PEBwalker#detections)

_At the time of writing, no engines detect this code snippet as malicious, as it is really not by itself._

## Example Usage

[Permalink: Example Usage](https://github.com/0xROOTPLS/PEBwalker#example-usage)

```
//Create UTF-16 hash for module
let target_lib: Vec<u16> = "ntdll.dll".encode_utf16().collect();
let lib_sum = calc_wide_checksum(&target_lib);

//Create hash for target function
let target_func = calc_checksum(b"NtAllocateVirtualMemory");

//Resolve func pointer
let routine_ptr = find_routine(lib_sum, target_func);
```

## About

A PEB walker that resolves function addresses via runtime checksum comparison, avoiding static imports.


### Resources

[Readme](https://github.com/0xROOTPLS/PEBwalker#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/0xROOTPLS/PEBwalker).

[Activity](https://github.com/0xROOTPLS/PEBwalker/activity)

### Stars

[**0**\\
stars](https://github.com/0xROOTPLS/PEBwalker/stargazers)

### Watchers

[**1**\\
watching](https://github.com/0xROOTPLS/PEBwalker/watchers)

### Forks

[**0**\\
forks](https://github.com/0xROOTPLS/PEBwalker/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2F0xROOTPLS%2FPEBwalker&report=0xROOTPLS+%28user%29)

## [Releases](https://github.com/0xROOTPLS/PEBwalker/releases)

No releases published

## [Packages\  0](https://github.com/users/0xROOTPLS/packages?repo_name=PEBwalker)

No packages published

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/0xROOTPLS/PEBwalker).

## [Contributors\  1](https://github.com/0xROOTPLS/PEBwalker/graphs/contributors)

- [![@0xROOTPLS](https://avatars.githubusercontent.com/u/104942265?s=64&v=4)](https://github.com/0xROOTPLS)[**0xROOTPLS** 0xROOTPLS](https://github.com/0xROOTPLS)

## Languages

- [Rust100.0%](https://github.com/0xROOTPLS/PEBwalker/search?l=rust)

You can’t perform that action at this time.