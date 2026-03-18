# https://github.com/0xROOTPLS/WaveGate

[Skip to content](https://github.com/0xROOTPLS/WaveGate#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/0xROOTPLS/WaveGate) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/0xROOTPLS/WaveGate) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/0xROOTPLS/WaveGate) to refresh your session.Dismiss alert

{{ message }}

[0xROOTPLS](https://github.com/0xROOTPLS)/ **[WaveGate](https://github.com/0xROOTPLS/WaveGate)** Public

- [Notifications](https://github.com/login?return_to=%2F0xROOTPLS%2FWaveGate) You must be signed in to change notification settings
- [Fork\\
0](https://github.com/login?return_to=%2F0xROOTPLS%2FWaveGate)
- [Star\\
2](https://github.com/login?return_to=%2F0xROOTPLS%2FWaveGate)


main

[**1** Branch](https://github.com/0xROOTPLS/WaveGate/branches) [**1** Tag](https://github.com/0xROOTPLS/WaveGate/tags)

[Go to Branches page](https://github.com/0xROOTPLS/WaveGate/branches)[Go to Tags page](https://github.com/0xROOTPLS/WaveGate/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![0xROOTPLS](https://avatars.githubusercontent.com/u/104942265?v=4&size=40)](https://github.com/0xROOTPLS)[0xROOTPLS](https://github.com/0xROOTPLS/WaveGate/commits?author=0xROOTPLS)<br>[Revise disclaimer in README.md for clarity](https://github.com/0xROOTPLS/WaveGate/commit/e1671cb8d8e81f476c7bd8b114def6f5c6585c69)<br>Open commit details<br>3 months agoDec 10, 2025<br>[e1671cb](https://github.com/0xROOTPLS/WaveGate/commit/e1671cb8d8e81f476c7bd8b114def6f5c6585c69) · 3 months agoDec 10, 2025<br>## History<br>[6 Commits](https://github.com/0xROOTPLS/WaveGate/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/0xROOTPLS/WaveGate/commits/main/) 6 Commits |
| [WaveGate](https://github.com/0xROOTPLS/WaveGate/tree/main/WaveGate "WaveGate") | [WaveGate](https://github.com/0xROOTPLS/WaveGate/tree/main/WaveGate "WaveGate") | [Add files via upload](https://github.com/0xROOTPLS/WaveGate/commit/12954d068b65eaf9439c4a55d825799c62abb7fc "Add files via upload") | 3 months agoDec 9, 2025 |
| [client](https://github.com/0xROOTPLS/WaveGate/tree/main/client "client") | [client](https://github.com/0xROOTPLS/WaveGate/tree/main/client "client") | [Refactor VM check documentation and comments](https://github.com/0xROOTPLS/WaveGate/commit/3e9e5abba58800b86b1351aa1993dc4e02ccb3c0 "Refactor VM check documentation and comments  Removed outdated comments and simplified function documentation.") | 3 months agoDec 10, 2025 |
| [shared](https://github.com/0xROOTPLS/WaveGate/tree/main/shared "shared") | [shared](https://github.com/0xROOTPLS/WaveGate/tree/main/shared "shared") | [Add files via upload](https://github.com/0xROOTPLS/WaveGate/commit/12954d068b65eaf9439c4a55d825799c62abb7fc "Add files via upload") | 3 months agoDec 9, 2025 |
| [ui](https://github.com/0xROOTPLS/WaveGate/tree/main/ui "ui") | [ui](https://github.com/0xROOTPLS/WaveGate/tree/main/ui "ui") | [Add files via upload](https://github.com/0xROOTPLS/WaveGate/commit/12954d068b65eaf9439c4a55d825799c62abb7fc "Add files via upload") | 3 months agoDec 9, 2025 |
| [Cargo.toml](https://github.com/0xROOTPLS/WaveGate/blob/main/Cargo.toml "Cargo.toml") | [Cargo.toml](https://github.com/0xROOTPLS/WaveGate/blob/main/Cargo.toml "Cargo.toml") | [Add files via upload](https://github.com/0xROOTPLS/WaveGate/commit/12954d068b65eaf9439c4a55d825799c62abb7fc "Add files via upload") | 3 months agoDec 9, 2025 |
| [README.md](https://github.com/0xROOTPLS/WaveGate/blob/main/README.md "README.md") | [README.md](https://github.com/0xROOTPLS/WaveGate/blob/main/README.md "README.md") | [Revise disclaimer in README.md for clarity](https://github.com/0xROOTPLS/WaveGate/commit/e1671cb8d8e81f476c7bd8b114def6f5c6585c69 "Revise disclaimer in README.md for clarity  Updated disclaimer to emphasize potential bugs and incomplete features.") | 3 months agoDec 10, 2025 |
| View all files |

## Repository files navigation

# WaveGate

[Permalink: WaveGate](https://github.com/0xROOTPLS/WaveGate#wavegate)

WaveGate is an "advanced", visually appealing remote access tool with a plethora of features for the operator.

# Disclaimer

[Permalink: Disclaimer](https://github.com/0xROOTPLS/WaveGate#disclaimer)

- WaveGate is in very early stages of development (1.0) - **Please expect potentialy catestrophic bugs aand/or incomplete feature implementation**. I did my best to ensure each module works, but the codebase got so large its hard to keep all the gears working together.
- WaveGate clients were not designed to be evasive. It is probably very signaturable.
- WaveGate was made for the community, and for those who want a great resource for offensive Rust-based RAT features.

# Features

[Permalink: Features](https://github.com/0xROOTPLS/WaveGate#features)

- **Remote Shell**: Interactive streamed shell sessions with input/output forwarding.
- **Remote Execution**: Including web downloads and local file execution, with output capture.
- **File Manager**: Full custom interactive Windows file manager with browsing, upload/download, delete, rename, and directory creation capabilities.
- **Registry Editor**: Full custom registry editor with key/value listing, getting/setting/deleting values, creating/deleting keys (with recursive delete option).
- **Process Manager**: Process listing and killing.
- **Startup Manager**: Management of startup items, including adding/removing entries.
- **Services Manager**: Service listing, starting, stopping, and configuration.
- **Task Scheduler Manager**: Task listing, creation, deletion, and execution.
- **Clipboard Manager**: Clipboard monitoring with history, content retrieval, setting, and regex-based replacement.
- **WMI Console**: WMI query execution with pre-built commands for system information and management.
- **Remote Desktop**: Interactive remote desktop with mouse/keyboard control, supporting H.264 encoding, tile-based DXGI capture at up to 30 FPS, or JPEG BitBlt fallback.
- **Remote Webcam/Media Stream**: Remote webcam and audio streaming with configurable video/audio devices, FPS, quality, and resolution; uses direct MPEG encoding.
- **Screenshot**: On-demand screenshot capture.
- **GUI User Chat**: Interactive chat window for communicating with the end user, with event polling and forwarding.
- **Open URL**: Ability to open specified URLs in the default browser.
- **Credential Recovery**: Recovery of stored credentials, browser cookies (Chromium v10, v11, and v20).
- **TCP Connections Manager**: Listing and management of active TCP connections.
- **Hosts File Manager**: Editing and management of the hosts file for DNS redirection.
- **Cached DNS Manager/Poisoner**: DNS cache management, including poisoning for MITM attacks.
- **Lateral Movement Module**: Token creation/impersonation; jumping to remote hosts via SCShell, PExec, and SMB pipes; remote execution via WMI, WinRM, and SMB; pivoting capabilities.
- **Active Directory Enumeration**: Full AD enumeration including users, machines, groups, domain info, and trusts.
- **Kerberos Module**: Listing, purging, and enumerating Kerberos tickets; requesting and managing service tickets.
- **Reverse Proxy**: SOCKS5-style reverse proxy for tunneling, with support for SMB/named pipe proxies; handles connect, data, and close messages.
- **Primary/Backup Hosts**: Connection attempts to primary host first, falling back to backup if configured.
- **Domain Fronting**: Supported via custom SNI hostname overriding.
- **Custom DNS Support**: System DNS or custom primary/backup DNS servers for resolution, with manual query handling.
- **UAC Bypass**: Built-in UAC bypass for elevation, with relaunch on demand.
- **Proxy Aware**: Supports HTTP or SOCKS5 proxies for outbound connections, with optional username/password authentication.
- **Persistence Methods**: 4 methods including registry run keys, task scheduler, startup folder, and service installation.
- **Zone ID Clearing**: Automatic clearing of Zone.Identifier ADS to bypass MOTW.
- **Auto System Sleep Prevention**: Configurable prevention of system sleep/idle.
- **Startup/Connect/Reconnect Delays**: Configurable delays for run start, initial connect, and reconnect attempts.
- **Auto Uninstall Triggers**: Triggers based on hostname, date, environment, with full cleanup.
- **Anti-VM Detection**: Detection via WMI queries to exit if in VM.
- **Configuration Security**: Config is encrypted and brute-forced at runtime (no key stored), then zeroed out in memory.
- **Communication Modes**: Regular TLS stream or HTTP upgrade to WebSocket for comms, with framing support.
- **Geolocation Fetching**: One-time geolocation fetch from ip-api.com at startup, cached for system info.
- **Single-Instance Enforcement**: Uses named mutex and lock file to ensure only one instance runs, with retry for restarts.
- **Disclosure Dialog**: Optional user disclosure dialog at startup, exiting if declined.
- **VM/Environment Checks**: Additional environment checks beyond anti-VM, including install location enforcement.
- **System Info Gathering**: Comprehensive info including hardware (CPU, GPU, RAM, motherboard, drives via WMI and sysinfo), usage (CPU/RAM percent), network (IPs, country), and real-time updates (active window, uptime).
- **Persistent UID**: Generated from machine GUID + build ID for unique identification.
- **Protocol Handling**: Binary protocol with length-prefixing, message types (register, ping/pong, commands, responses, info updates, media/RD frames, proxy messages), and WebSocket wrapping.
- **Panic Protection**: Command execution wrapped in panic catching for stability.
- **Cleanup on Disconnect**: Automatic cleanup of active sessions (shell, media, RD, proxy) on disconnect.

# Images

[Permalink: Images](https://github.com/0xROOTPLS/WaveGate#images)

### Main Client Area

[Permalink: Main Client Area](https://github.com/0xROOTPLS/WaveGate#main-client-area)

![Main Client Area](https://camo.githubusercontent.com/30caaefe518a85ddaa3d096e98b37d67097bc242b84279b942ec6466d0365471/68747470733a2f2f66696c65732e636174626f782e6d6f652f73776e6261612e504e47)

### Context Menu

[Permalink: Context Menu](https://github.com/0xROOTPLS/WaveGate#context-menu)

![Context Menu](https://camo.githubusercontent.com/2854629c3eb8f808890c4ec0fc944ccb67c96d82697f0b7b5b1ef3ee7ddaba21/68747470733a2f2f66696c65732e636174626f782e6d6f652f7978776c69652e504e47)

### File Manager

[Permalink: File Manager](https://github.com/0xROOTPLS/WaveGate#file-manager)

![File Manager](https://camo.githubusercontent.com/e0073b92e9a4d0aee6e2cb1b7ae80040bef7cc2e28e08d0dcb3e6ba7959d5138/68747470733a2f2f66696c65732e636174626f782e6d6f652f7138763931652e504e47)

### Remote Shell

[Permalink: Remote Shell](https://github.com/0xROOTPLS/WaveGate#remote-shell)

![Remote Shell](https://camo.githubusercontent.com/fc0457b65e8cb827b5ce69d37a313f8ff5ff31256b5fe3ea0ea27281ef8d738a/68747470733a2f2f66696c65732e636174626f782e6d6f652f76346e306e632e504e47)

### Registry Editor

[Permalink: Registry Editor](https://github.com/0xROOTPLS/WaveGate#registry-editor)

![Registry Editor](https://camo.githubusercontent.com/cd7998d241cf9584b6e93da74ecd05fc0b8830526dd226eb29ca5015f2d67f66/68747470733a2f2f66696c65732e636174626f782e6d6f652f7866317469782e504e47)

### WMI Console

[Permalink: WMI Console](https://github.com/0xROOTPLS/WaveGate#wmi-console)

![WMI Console](https://camo.githubusercontent.com/3a17865e018cf2fd40708c3d16de29f470a43a6066e2fc309cf4bc43d1c5591d/68747470733a2f2f66696c65732e636174626f782e6d6f652f31386f3177642e504e47)

### User Chat

[Permalink: User Chat](https://github.com/0xROOTPLS/WaveGate#user-chat)

![User Chat](https://camo.githubusercontent.com/53178de952f9f1c298b893d43f306950341c1c73ccb32873086330222dcaa985/68747470733a2f2f66696c65732e636174626f782e6d6f652f7838333873352e504e47)

### Credential Recovery

[Permalink: Credential Recovery](https://github.com/0xROOTPLS/WaveGate#credential-recovery)

![Credential Recovery](https://camo.githubusercontent.com/0fbc516d33eb551ad2a1d6d019ca4f4fbca46fc36333266d8890fe301e9597af/68747470733a2f2f66696c65732e636174626f782e6d6f652f656e7a3461732e504e47)

### Lateral Movement — Tokens

[Permalink: Lateral Movement — Tokens](https://github.com/0xROOTPLS/WaveGate#lateral-movement--tokens)

![Lateral Movement — Tokens](https://camo.githubusercontent.com/42d524718e9035fc545b4b04c65551e06c3d3418bdda0d9ab090e40f4716be2e/68747470733a2f2f66696c65732e636174626f782e6d6f652f7761377a306f2e504e47)

### Lateral Movement — Jump

[Permalink: Lateral Movement — Jump](https://github.com/0xROOTPLS/WaveGate#lateral-movement--jump)

![Lateral Movement — Jump](https://camo.githubusercontent.com/1b32a63f0575e88447aebbf0075ddc475e55c045a5ed5863f1f6ddefa101c78d/68747470733a2f2f66696c65732e636174626f782e6d6f652f666f746879792e504e47)

### Lateral Movement — Pivots

[Permalink: Lateral Movement — Pivots](https://github.com/0xROOTPLS/WaveGate#lateral-movement--pivots)

![Lateral Movement — Pivots](https://camo.githubusercontent.com/4cbfbb598e16326dde9d73653fd35e456fb98295d651d3592f1ebe8e174a36ac/68747470733a2f2f66696c65732e636174626f782e6d6f652f7663796e64362e504e47)

### Lateral Movement — Remote Exec

[Permalink: Lateral Movement — Remote Exec](https://github.com/0xROOTPLS/WaveGate#lateral-movement--remote-exec)

![Lateral Movement — Remote Exec](https://camo.githubusercontent.com/29a214815863b8cf305acfcd8496f8866d5b7c625961d161f95d7eda0f25809a/68747470733a2f2f66696c65732e636174626f782e6d6f652f6169397a78612e504e47)

### Lateral Movement — AD

[Permalink: Lateral Movement — AD](https://github.com/0xROOTPLS/WaveGate#lateral-movement--ad)

![Lateral Movement — AD](https://camo.githubusercontent.com/a1291f8a94814b3163b21dc55d9460ea6138b32dcb0eb18bb4f49f2c34929fe6/68747470733a2f2f66696c65732e636174626f782e6d6f652f7475316e7a762e504e47)

### Lateral Movement — Kerberos

[Permalink: Lateral Movement — Kerberos](https://github.com/0xROOTPLS/WaveGate#lateral-movement--kerberos)

![Lateral Movement — Kerberos](https://camo.githubusercontent.com/3bc9493bd420ed27de8ec8191b51acc711a8dd2396bd8a392aa6031c1d9f1930/68747470733a2f2f66696c65732e636174626f782e6d6f652f63726e396f632e504e47)

### Builder Part 1

[Permalink: Builder Part 1](https://github.com/0xROOTPLS/WaveGate#builder-part-1)

![Builder Part 1](https://camo.githubusercontent.com/4093c506f0876be016a2cfa4ad10726b4764c60ff5b8b0c76d55730aa91b4407/68747470733a2f2f66696c65732e636174626f782e6d6f652f6664373668722e504e47)

### Builder Part 2

[Permalink: Builder Part 2](https://github.com/0xROOTPLS/WaveGate#builder-part-2)

![Builder Part 2](https://camo.githubusercontent.com/a92bd5f3b315e27cc7877fe82feb29e64eb0936b56090f251d75b771b3c2f149/68747470733a2f2f66696c65732e636174626f782e6d6f652f756f663077702e504e47)

### Server Config

[Permalink: Server Config](https://github.com/0xROOTPLS/WaveGate#server-config)

![Server Config](https://camo.githubusercontent.com/443226782162c572c4a503952956e3e645ada800cdf34f9e5ea21e522007b931/68747470733a2f2f66696c65732e636174626f782e6d6f652f7469746338342e504e47)

### Logs

[Permalink: Logs](https://github.com/0xROOTPLS/WaveGate#logs)

![Logs](https://camo.githubusercontent.com/54411893c615c32cbdefaed2d8b46c581d331eac60f56708bb153a15ef57bcd0/68747470733a2f2f66696c65732e636174626f782e6d6f652f6f6677386c6b2e504e47)

### General Settings 1

[Permalink: General Settings 1](https://github.com/0xROOTPLS/WaveGate#general-settings-1)

![General Settings 1](https://camo.githubusercontent.com/6888d7190ae843598110de4b0f4f2cf50f6a7c47328c8d0bfdfa7c0c4f2624d6/68747470733a2f2f66696c65732e636174626f782e6d6f652f3063386935692e504e47)

### General Settings 2

[Permalink: General Settings 2](https://github.com/0xROOTPLS/WaveGate#general-settings-2)

![General Settings 2](https://camo.githubusercontent.com/959ff0136826774d102cbd6a3b916465d04f599e1686ac44948e897c538b157a/68747470733a2f2f66696c65732e636174626f782e6d6f652f6b303137756c2e504e47)

## About

WaveGate is a Tauri/Rust based RAT written for fun =D


### Resources

[Readme](https://github.com/0xROOTPLS/WaveGate#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/0xROOTPLS/WaveGate).

[Activity](https://github.com/0xROOTPLS/WaveGate/activity)

### Stars

[**2**\\
stars](https://github.com/0xROOTPLS/WaveGate/stargazers)

### Watchers

[**0**\\
watching](https://github.com/0xROOTPLS/WaveGate/watchers)

### Forks

[**0**\\
forks](https://github.com/0xROOTPLS/WaveGate/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2F0xROOTPLS%2FWaveGate&report=0xROOTPLS+%28user%29)

## [Releases\  1](https://github.com/0xROOTPLS/WaveGate/releases)

[WaveGate 1.0 Release\\
Latest\\
\\
on Dec 9, 2025Dec 10, 2025](https://github.com/0xROOTPLS/WaveGate/releases/tag/Release)

## [Packages\  0](https://github.com/users/0xROOTPLS/packages?repo_name=WaveGate)

No packages published

## [Contributors\  1](https://github.com/0xROOTPLS/WaveGate/graphs/contributors)

- [![@0xROOTPLS](https://avatars.githubusercontent.com/u/104942265?s=64&v=4)](https://github.com/0xROOTPLS)[**0xROOTPLS** 0xROOTPLS](https://github.com/0xROOTPLS)

## Languages

- [Rust63.6%](https://github.com/0xROOTPLS/WaveGate/search?l=rust)
- [JavaScript29.0%](https://github.com/0xROOTPLS/WaveGate/search?l=javascript)
- [CSS4.1%](https://github.com/0xROOTPLS/WaveGate/search?l=css)
- [HTML3.3%](https://github.com/0xROOTPLS/WaveGate/search?l=html)

You can’t perform that action at this time.