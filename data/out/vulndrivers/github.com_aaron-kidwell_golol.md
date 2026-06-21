# https://github.com/aaron-kidwell/goLoL

[Skip to content](https://github.com/aaron-kidwell/goLoL#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/aaron-kidwell/goLoL) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/aaron-kidwell/goLoL) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/aaron-kidwell/goLoL) to refresh your session.Dismiss alert

{{ message }}

[aaron-kidwell](https://github.com/aaron-kidwell)/ **[goLoL](https://github.com/aaron-kidwell/goLoL)** Public

- [Notifications](https://github.com/login?return_to=%2Faaron-kidwell%2FgoLoL) You must be signed in to change notification settings
- [Fork\\
7](https://github.com/login?return_to=%2Faaron-kidwell%2FgoLoL)
- [Star\\
59](https://github.com/login?return_to=%2Faaron-kidwell%2FgoLoL)


main

[**1** Branch](https://github.com/aaron-kidwell/goLoL/branches) [**4** Tags](https://github.com/aaron-kidwell/goLoL/tags)

[Go to Branches page](https://github.com/aaron-kidwell/goLoL/branches)[Go to Tags page](https://github.com/aaron-kidwell/goLoL/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![aaron-kidwell](https://avatars.githubusercontent.com/u/82623017?v=4&size=40)](https://github.com/aaron-kidwell)[aaron-kidwell](https://github.com/aaron-kidwell/goLoL/commits?author=aaron-kidwell)<br>[updated README.md to reflect the new driver scanning capability](https://github.com/aaron-kidwell/goLoL/commit/1b3b42cdc2ef072e3fafb75da58756a394fa92b8)<br>last monthMay 27, 2026<br>[1b3b42c](https://github.com/aaron-kidwell/goLoL/commit/1b3b42cdc2ef072e3fafb75da58756a394fa92b8) · last monthMay 27, 2026<br>## History<br>[25 Commits](https://github.com/aaron-kidwell/goLoL/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/aaron-kidwell/goLoL/commits/main/) 25 Commits |
| [docs](https://github.com/aaron-kidwell/goLoL/tree/main/docs "docs") | [docs](https://github.com/aaron-kidwell/goLoL/tree/main/docs "docs") | [add screenshot to README](https://github.com/aaron-kidwell/goLoL/commit/be38317a3ea53c50c0671efe8617ecb5a28b159f "add screenshot to README") | last monthMay 21, 2026 |
| [internal](https://github.com/aaron-kidwell/goLoL/tree/main/internal "internal") | [internal](https://github.com/aaron-kidwell/goLoL/tree/main/internal "internal") | [goLoL initial commit](https://github.com/aaron-kidwell/goLoL/commit/96cf6f02c4077f0aa24ed82396af076ea3fabe81 "goLoL initial commit") | last monthMay 21, 2026 |
| [.gitignore](https://github.com/aaron-kidwell/goLoL/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/aaron-kidwell/goLoL/blob/main/.gitignore ".gitignore") | [included executable](https://github.com/aaron-kidwell/goLoL/commit/c777e031daef8e1c85442d911b08a9fdb5bcf383 "included executable") | last monthMay 22, 2026 |
| [README.md](https://github.com/aaron-kidwell/goLoL/blob/main/README.md "README.md") | [README.md](https://github.com/aaron-kidwell/goLoL/blob/main/README.md "README.md") | [updated README.md to reflect the new driver scanning capability](https://github.com/aaron-kidwell/goLoL/commit/1b3b42cdc2ef072e3fafb75da58756a394fa92b8 "updated README.md to reflect the new driver scanning capability") | last monthMay 27, 2026 |
| [go.mod](https://github.com/aaron-kidwell/goLoL/blob/main/go.mod "go.mod") | [go.mod](https://github.com/aaron-kidwell/goLoL/blob/main/go.mod "go.mod") | [updated README.md and main.go](https://github.com/aaron-kidwell/goLoL/commit/a949d5620233b0db65e583d9657ff7337bb4913b "updated README.md and main.go") | last monthMay 21, 2026 |
| [go.sum](https://github.com/aaron-kidwell/goLoL/blob/main/go.sum "go.sum") | [go.sum](https://github.com/aaron-kidwell/goLoL/blob/main/go.sum "go.sum") | [goLoL initial commit](https://github.com/aaron-kidwell/goLoL/commit/96cf6f02c4077f0aa24ed82396af076ea3fabe81 "goLoL initial commit") | last monthMay 21, 2026 |
| [goLoL.exe](https://github.com/aaron-kidwell/goLoL/blob/main/goLoL.exe "goLoL.exe") | [goLoL.exe](https://github.com/aaron-kidwell/goLoL/blob/main/goLoL.exe "goLoL.exe") | [added ability to scan local drivers against the LOLDrivers catalog](https://github.com/aaron-kidwell/goLoL/commit/95bc3abcd7a7e492b23abb6254dc9b9b63ac76b6 "added ability to scan local drivers against the LOLDrivers catalog") | last monthMay 27, 2026 |
| [main.go](https://github.com/aaron-kidwell/goLoL/blob/main/main.go "main.go") | [main.go](https://github.com/aaron-kidwell/goLoL/blob/main/main.go "main.go") | [added ability to scan local drivers against the LOLDrivers catalog](https://github.com/aaron-kidwell/goLoL/commit/95bc3abcd7a7e492b23abb6254dc9b9b63ac76b6 "added ability to scan local drivers against the LOLDrivers catalog") | last monthMay 27, 2026 |
| View all files |

## Repository files navigation

# goLoL

[Permalink: goLoL](https://github.com/aaron-kidwell/goLoL#golol)

**goLoL** is a Windows host scanner with dual support for **[LOLBAS](https://lolbas-project.github.io/)** binaries and **[LOLDrivers](https://www.loldrivers.io/)**. It lists LOLBAS techniques runnable at your current privilege level (with MITRE ATT&CK mappings) and can scan local `.sys` files for vulnerable/malicious LOLDrivers hash matches.
**Note:** This is not an OPSEC safe tool.
**Author:** Aaron Kidwell

```
                   █████                █████
                  ░░███                ░░███
  ███████  ██████  ░███         ██████  ░███
 ███░░███ ███░░███ ░███        ███░░███ ░███
░███ ░███░███ ░███ ░███       ░███ ░███ ░███
░███ ░███░███ ░███ ░███      █░███ ░███ ░███      █
░░███████░░██████  ███████████░░██████  ███████████
 ░░░░░███ ░░░░░░  ░░░░░░░░░░░  ░░░░░░  ░░░░░░░░░░░
 ███ ░███
░░██████
 ░░░░░░
```

[![goLoL interactive terminal output](https://github.com/aaron-kidwell/goLoL/raw/main/docs/screenshot.png)](https://github.com/aaron-kidwell/goLoL/blob/main/docs/screenshot.png)

## Features

[Permalink: Features](https://github.com/aaron-kidwell/goLoL#features)

- **Live LOLBAS catalog** — pulls the latest entries from [lolbas-project.github.io](https://lolbas-project.github.io/api/lolbas.json)
- **On-disk detection** — resolves documented paths to local `%WINDIR%`, `%ProgramFiles%`, `%USERPROFILE%`, and WindowsApps locations
- **Privilege-aware filtering** — shows only techniques runnable at your current tier
- **MITRE ATT&CK labels** — technique IDs mapped to readable names (e.g. `T1003.003: NTDS`)
- **Flexible sorting** — group by binary, privilege tier, or ATT&CK technique
- **Driver mode** — hashes local `.sys` files and matches against the live [LOLDrivers](https://www.loldrivers.io/) JSON catalog
- **Plain output mode** — ASCII-only output for telnet, reverse shells, and other unstable terminals
- **Lightweight scanning** — filesystem checks via Go APIs; admin-group detection uses `net localgroup` (one child process on Windows)

## Privilege tiers

[Permalink: Privilege tiers](https://github.com/aaron-kidwell/goLoL#privilege-tiers)

| Your context | What you see |
| --- | --- |
| Standard user | User-tier techniques |
| Member of local **Administrators** | User-tier + admin-tier techniques |
| **NT AUTHORITY\\SYSTEM** | User-tier + admin-tier + SYSTEM-tier techniques |

Admin-tier commands may still require an elevated shell even if your account is in the Administrators group. SYSTEM-tier entries are hidden unless the process token is SYSTEM (`S-1-5-18`).

## Requirements

[Permalink: Requirements](https://github.com/aaron-kidwell/goLoL#requirements)

- **Windows** (primary target; non-Windows builds stub out privilege checks)
- **Go 1.21+** (project uses Go 1.26.2)
- **Network access** to fetch LOLBAS/LOLDrivers catalogs on each run (not cached offline)

## Install

[Permalink: Install](https://github.com/aaron-kidwell/goLoL#install)

**Remote install** (requires a tagged release on GitHub, e.g. `v0.1.0`):

```
go install github.com/aaron-kidwell/goLoL@latest
```

The binary is placed in your `GOPATH/bin` (or `~/go/bin`). On Windows, ensure that directory is on your `PATH`.

**Clone and build:**

```
git clone https://github.com/aaron-kidwell/goLoL.git
cd goLoL
go build -ldflags="-s -w" -trimpath -o golol.exe .
```

## Usage

[Permalink: Usage](https://github.com/aaron-kidwell/goLoL#usage)

`goLoL` supports two scan modes:

- **LOLBAS mode (default)** for living-off-the-land binaries and privilege-filtered techniques
- **LOLDrivers mode** via `-driver` for vulnerable/malicious driver hash matches

Run from the module root (required for `internal/` packages):

```
go run .
```

Build a binary (recommended.. strips debug info, ~30% smaller):

```
go build -ldflags="-s -w" -trimpath -o golol.exe .
.\golol.exe
```

`-s -w` removes the symbol table and DWARF debug data. A default `go build` on this project is ~9.5 MB; with those flags it drops to ~6.4 MB.

### Flags

[Permalink: Flags](https://github.com/aaron-kidwell/goLoL#flags)

| Flag | Description |
| --- | --- |
| `-h`, `-help` | Show help |
| `-driver` | Scan local drivers and list known vulnerable/malicious matches from LOLDrivers |
| `-plain` | ASCII-only output — no colors, Unicode, or cursor control |
| `-s`, `-search` | Show one binary by name (`certutil` or `certutil.exe`); reports if not on disk |
| `-sort` | Sort results: `binary` (default), `privilege`, or `attack` |

Sort aliases: `b`, `priv` / `p`, `mitre` / `a`. Invalid values print an error and show help.

### Examples

[Permalink: Examples](https://github.com/aaron-kidwell/goLoL#examples)

```
# Default — grouped by binary name (A–Z)
go run .

# Driver mode (scan local .sys files against LOLDrivers hashes)
go run . -driver

# Look up a single binary
go run . -s certutil
.\golol.exe -s certutil.exe

# Admin tier first, then user tier (SYSTEM tier first when running as SYSTEM)
go run . -sort privilege

# Sorted by MITRE ATT&CK ID
go run . -sort attack

# Reverse shell / telnet friendly output
go run . -plain

# Combine flags
go run . -plain -sort attack
```

### Example output

[Permalink: Example output](https://github.com/aaron-kidwell/goLoL#example-output)

Counts and binaries vary by host. The screenshot at the top of this README shows interactive mode (colored terminal, grouped by binary).

**Plain mode** (`-plain`):

```
[*] Checking process token...
[*] Fetching LOLBAS catalog...
[+] Found 147 binaries, 299 techniques

==============================================================
Role:        administrator
Sort:        binary
Binaries:    147
Techniques:  299
==============================================================

  [1] Esentutl.exe
  Path:          C:\Windows\System32\esentutl.exe
  ...
```

## How it works

[Permalink: How it works](https://github.com/aaron-kidwell/goLoL#how-it-works)

1. Detects the current process privilege context (standard user, local admin group member, or SYSTEM).
2. In default mode, downloads and parses the LOLBAS JSON catalog.
3. For each LOLBAS entry, remaps documented paths to the local filesystem and checks whether the binary exists.
4. Filters commands by privilege tier and deduplicates by resolved on-disk path.
5. In `-driver` mode, downloads the LOLDrivers JSON catalog, hashes local `.sys` files, and reports hash matches.
6. Prints results with paths, ATT&CK technique, use case, and example command (or driver match metadata in `-driver` mode).

| Component | Location |
| --- | --- |
| LOLBAS catalog | `https://lolbas-project.github.io/api/lolbas.json` |
| LOLDrivers catalog | `https://www.loldrivers.io/api/drivers.json` |
| Privilege detection | `internal/privileges` |
| MITRE technique names | `internal/mitre` |
| Path resolution & output | `main.go` |

## Project layout

[Permalink: Project layout](https://github.com/aaron-kidwell/goLoL#project-layout)

```
.
├── docs/
│   └── screenshot.png            # README screenshot
├── main.go
├── internal/
│   ├── mitre/
│   │   └── names.go              # MITRE ATT&CK ID → label map
│   └── privileges/
│       ├── privileges_windows.go # Token / Administrators group checks
│       └── privileges_stub.go    # Non-Windows stub
├── go.mod
└── go.sum
```

## Disclaimer

[Permalink: Disclaimer](https://github.com/aaron-kidwell/goLoL#disclaimer)

For **authorized** security testing, lab use, and education only. Only run against systems you own or have explicit permission to assess. LOLBAS entries describe techniques that may be abused by attackers — use responsibly. The author is not responsible for misuse.

Technique and metadata are sourced from the [LOLBAS Project](https://github.com/LOLBAS-Project/LOLBAS) and [LOLDrivers](https://github.com/magicsword-io/LOLDrivers). goLoL is not affiliated with or endorsed by either project.

## License

[Permalink: License](https://github.com/aaron-kidwell/goLoL#license)

MIT

## About

goLoL is a Windows host scanner with dual support for LOLBAS binaries and LOLDrivers. It lists LOLBAS techniques runnable at your current privilege level (with MITRE ATT&CK mappings) and can scan local .sys files for vulnerable/malicious LOLDrivers hash matches.


### Topics

[go](https://github.com/topics/go "Topic: go") [golang](https://github.com/topics/golang "Topic: golang") [ctf-tools](https://github.com/topics/ctf-tools "Topic: ctf-tools") [living-off-the-land](https://github.com/topics/living-off-the-land "Topic: living-off-the-land") [penetration-testing-tools](https://github.com/topics/penetration-testing-tools "Topic: penetration-testing-tools") [lolbas](https://github.com/topics/lolbas "Topic: lolbas") [cybersecurity-tools](https://github.com/topics/cybersecurity-tools "Topic: cybersecurity-tools")

### Resources

[Readme](https://github.com/aaron-kidwell/goLoL#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/aaron-kidwell/goLoL).

[Activity](https://github.com/aaron-kidwell/goLoL/activity)

### Stars

[**59**\\
stars](https://github.com/aaron-kidwell/goLoL/stargazers)

### Watchers

[**2**\\
watching](https://github.com/aaron-kidwell/goLoL/watchers)

### Forks

[**7**\\
forks](https://github.com/aaron-kidwell/goLoL/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Faaron-kidwell%2FgoLoL&report=aaron-kidwell+%28user%29)

## [Releases\  4](https://github.com/aaron-kidwell/goLoL/releases)

[goLoL 1.2\\
Latest\\
\\
last monthMay 27, 2026](https://github.com/aaron-kidwell/goLoL/releases/tag/1.2)

[\+ 3 releases](https://github.com/aaron-kidwell/goLoL/releases)

## [Contributors\  1](https://github.com/aaron-kidwell/goLoL/graphs/contributors)

- [![@aaron-kidwell](https://avatars.githubusercontent.com/u/82623017?s=64&v=4)](https://github.com/aaron-kidwell)[**aaron-kidwell** Aaron Kidwell](https://github.com/aaron-kidwell)

## Languages

- [Go100.0%](https://github.com/aaron-kidwell/goLoL/search?l=go)

You can’t perform that action at this time.