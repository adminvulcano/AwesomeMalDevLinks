# https://github.com/kimd155/WerWolf

[Skip to content](https://github.com/kimd155/WerWolf#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/kimd155/WerWolf) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/kimd155/WerWolf) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/kimd155/WerWolf) to refresh your session.Dismiss alert

{{ message }}

[kimd155](https://github.com/kimd155)/ **[WerWolf](https://github.com/kimd155/WerWolf)** Public

- [Notifications](https://github.com/login?return_to=%2Fkimd155%2FWerWolf) You must be signed in to change notification settings
- [Fork\\
0](https://github.com/login?return_to=%2Fkimd155%2FWerWolf)
- [Star\\
19](https://github.com/login?return_to=%2Fkimd155%2FWerWolf)


master

[**1** Branch](https://github.com/kimd155/WerWolf/branches) [**0** Tags](https://github.com/kimd155/WerWolf/tags)

[Go to Branches page](https://github.com/kimd155/WerWolf/branches)[Go to Tags page](https://github.com/kimd155/WerWolf/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![kimd155](https://avatars.githubusercontent.com/u/94112981?v=4&size=40)](https://github.com/kimd155)[kimd155](https://github.com/kimd155/WerWolf/commits?author=kimd155)<br>[Update README.md](https://github.com/kimd155/WerWolf/commit/8a98c122b97abcc7b77df63709562ab137c32527)<br>2 months agoApr 14, 2026<br>[8a98c12](https://github.com/kimd155/WerWolf/commit/8a98c122b97abcc7b77df63709562ab137c32527) · 2 months agoApr 14, 2026<br>## History<br>[13 Commits](https://github.com/kimd155/WerWolf/commits/master/) <br>Open commit details<br>[View commit history for this file.](https://github.com/kimd155/WerWolf/commits/master/) 13 Commits |
| [bofs](https://github.com/kimd155/WerWolf/tree/master/bofs "bofs") | [bofs](https://github.com/kimd155/WerWolf/tree/master/bofs "bofs") | [Add files via upload](https://github.com/kimd155/WerWolf/commit/60ae2d1c263a6344abeec350662a3d809253d4d9 "Add files via upload") | 2 months agoApr 14, 2026 |
| [loader](https://github.com/kimd155/WerWolf/tree/master/loader "loader") | [loader](https://github.com/kimd155/WerWolf/tree/master/loader "loader") | [Fix async WER dump: wait for WerFault to finish writing](https://github.com/kimd155/WerWolf/commit/ac1c29f3fdc84b17fabae0b72c2786a68c1a9279 "Fix async WER dump: wait for WerFault to finish writing  RtlReportSilentProcessExit is async, it sends an ALPC message and returns immediately. The loader was freeing memory and the process was exiting before WerFault finished writing the dump.  Changes:   - Add 5s delay after BOF execution before freeing VirtualAlloc memory   - Add dump file polling in main.py (waits up to 60s for lsass*.dmp)   - Print unresolved symbols visibly so missing imports are obvious") | 2 months agoApr 13, 2026 |
| [README.md](https://github.com/kimd155/WerWolf/blob/master/README.md "README.md") | [README.md](https://github.com/kimd155/WerWolf/blob/master/README.md "README.md") | [Update README.md](https://github.com/kimd155/WerWolf/commit/8a98c122b97abcc7b77df63709562ab137c32527 "Update README.md") | 2 months agoApr 14, 2026 |
| [logo.png](https://github.com/kimd155/WerWolf/blob/master/logo.png "logo.png") | [logo.png](https://github.com/kimd155/WerWolf/blob/master/logo.png "logo.png") | [Initial release of WerWolf](https://github.com/kimd155/WerWolf/commit/b35c24b7d7d54d9d31dc0ceb687358844e2f2f1c "Initial release of WerWolf  In-memory BOF implementation of the Silent Process Exit LSASS dump technique. Custom Python COFF loader executes RtlReportSilentProcessExit as a Beacon Object File, no executable on disk, no PowerShell, no AMSI.") | 2 months agoApr 13, 2026 |
| [main.py](https://github.com/kimd155/WerWolf/blob/master/main.py "main.py") | [main.py](https://github.com/kimd155/WerWolf/blob/master/main.py "main.py") | [Fix ctypes x64 pointer truncation, use proper restype/argtypes for al…](https://github.com/kimd155/WerWolf/commit/ba2c527b8b5a65dc43af1ea360eb3356972588f6 "Fix ctypes x64 pointer truncation, use proper restype/argtypes for all WinAPI calls") | 2 months agoApr 13, 2026 |
| View all files |

## Repository files navigation

# WerWolf

[Permalink: WerWolf](https://github.com/kimd155/WerWolf#werwolf)

[![WerWolf](https://github.com/kimd155/WerWolf/raw/master/logo.png)](https://github.com/kimd155/WerWolf/blob/master/logo.png)

**In-memory BOF implementation of the Silent Process Exit LSASS dump technique**

WerWolf takes the `RtlReportSilentProcessExit` technique (originally presented by Asaf Gilboa at DEF CON 30) and executes it as an in-memory Beacon Object File via a custom Python COFF loader. No executable on disk. No PowerShell. No script block logging. No AMSI.

For the full technical deep-dive, research story, and how this improves on existing implementations, read the companion article on Medium: **[WerWolf: Taking Silent Process Exit from PowerShell Script to In-Memory BOF](https://medium.com/@kimd15/werwolf-taking-silent-process-exit-from-powershell-script-to-in-memory-bof-and-why-edrs-still-978fab767c56)**

## Usage

[Permalink: Usage](https://github.com/kimd155/WerWolf#usage)

```
# Just run it (requires admin on Windows)
python main.py

# Verbose mode
python main.py -v
```

That's it. WerWolf automatically loads and executes the BOF. No arguments needed.

## Requirements

[Permalink: Requirements](https://github.com/kimd155/WerWolf#requirements)

- Python 3.8+
- Windows (tested on Windows 10/11 and Server 2016+)
- Administrator privileges

## Output

[Permalink: Output](https://github.com/kimd155/WerWolf#output)

The dump is written to `C:\Windows\Temp\`. Parse it offline:

```
pypykatz lsa minidump C:\Windows\Temp\lsass.exe_*.dmp
```

## Project Structure

[Permalink: Project Structure](https://github.com/kimd155/WerWolf#project-structure)

```
WerWolf/
├── main.py              # Entry point - just run it
├── loader/
│   ├── parser.py        # COFF format parser
│   └── loader.py        # In-memory loader & executor
└── bofs/
    ├── include/
    │   └── beacon.h     # BOF API header
    └── wer_execute.o    # The WerWolf BOF (Compiled)
    └── wer_execute.c    # The WerWolf BOF (precompiled)
```

## Prior Art

[Permalink: Prior Art](https://github.com/kimd155/WerWolf#prior-art)

- Asaf Gilboa - "LSASS Shtinkering" (DEF CON 30) - original technique discovery
- [deepinstinct/LsassSilentProcessExit](https://github.com/deepinstinct/LsassSilentProcessExit) \- C implementation
- [CompassSecurity/PowerLsassSilentProcessExit](https://github.com/CompassSecurity/PowerLsassSilentProcessExit) \- PowerShell implementation

WerWolf's contribution is the **delivery mechanism**: executing the technique as an in-memory BOF, avoiding the disk artifacts and script logging that the existing tools create.

## MITRE ATT&CK

[Permalink: MITRE ATT&CK](https://github.com/kimd155/WerWolf#mitre-attck)

| Technique | ID |
| --- | --- |
| OS Credential Dumping: LSASS Memory | T1003.001 |
| Modify Registry | T1112 |
| Signed Binary Proxy Execution | T1218 |

## Disclaimer

[Permalink: Disclaimer](https://github.com/kimd155/WerWolf#disclaimer)

For authorized security testing and research only. Obtain written authorization before testing on systems you do not own.

## License

[Permalink: License](https://github.com/kimd155/WerWolf#license)

MIT

## About

In-memory BOF implementation of Silent Process Exit LSASS dump via RtlReportSilentProcessExit


### Resources

[Readme](https://github.com/kimd155/WerWolf#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/kimd155/WerWolf).

[Activity](https://github.com/kimd155/WerWolf/activity)

### Stars

[**19**\\
stars](https://github.com/kimd155/WerWolf/stargazers)

### Watchers

[**0**\\
watching](https://github.com/kimd155/WerWolf/watchers)

### Forks

[**0**\\
forks](https://github.com/kimd155/WerWolf/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fkimd155%2FWerWolf&report=kimd155+%28user%29)

## [Releases](https://github.com/kimd155/WerWolf/releases)

No releases published

## [Packages\  0](https://github.com/users/kimd155/packages?repo_name=WerWolf)

No packages published

## [Contributors\  1](https://github.com/kimd155/WerWolf/graphs/contributors)

- [![@kimd155](https://avatars.githubusercontent.com/u/94112981?s=64&v=4)](https://github.com/kimd155)[**kimd155** Kim D](https://github.com/kimd155)

## Languages

- [Python78.5%](https://github.com/kimd155/WerWolf/search?l=python)
- [C21.5%](https://github.com/kimd155/WerWolf/search?l=c)

You can’t perform that action at this time.