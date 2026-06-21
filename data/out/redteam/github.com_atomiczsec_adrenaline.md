# https://github.com/atomiczsec/Adrenaline

[Skip to content](https://github.com/atomiczsec/Adrenaline#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/atomiczsec/Adrenaline) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/atomiczsec/Adrenaline) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/atomiczsec/Adrenaline) to refresh your session.Dismiss alert

{{ message }}

[atomiczsec](https://github.com/atomiczsec)/ **[Adrenaline](https://github.com/atomiczsec/Adrenaline)** Public

- [Notifications](https://github.com/login?return_to=%2Fatomiczsec%2FAdrenaline) You must be signed in to change notification settings
- [Fork\\
34](https://github.com/login?return_to=%2Fatomiczsec%2FAdrenaline)
- [Star\\
308](https://github.com/login?return_to=%2Fatomiczsec%2FAdrenaline)


main

[**4** Branches](https://github.com/atomiczsec/Adrenaline/branches) [**30** Tags](https://github.com/atomiczsec/Adrenaline/tags)

[Go to Branches page](https://github.com/atomiczsec/Adrenaline/branches)[Go to Tags page](https://github.com/atomiczsec/Adrenaline/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![atomiczsec](https://avatars.githubusercontent.com/u/75549184?v=4&size=40)](https://github.com/atomiczsec)[atomiczsec](https://github.com/atomiczsec/Adrenaline/commits?author=atomiczsec)<br>[Merge pull request](https://github.com/atomiczsec/Adrenaline/commit/c1e34aea28fa0390143db148a264f59322abea8f) [#6](https://github.com/atomiczsec/Adrenaline/pull/6) [from atomiczsec/devin/1781148812-fix-cloud-meta…](https://github.com/atomiczsec/Adrenaline/commit/c1e34aea28fa0390143db148a264f59322abea8f)<br>Open commit details<br>last weekJun 10, 2026<br>[c1e34ae](https://github.com/atomiczsec/Adrenaline/commit/c1e34aea28fa0390143db148a264f59322abea8f) · last weekJun 10, 2026<br>## History<br>[111 Commits](https://github.com/atomiczsec/Adrenaline/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/atomiczsec/Adrenaline/commits/main/) 111 Commits |
| [.github/workflows](https://github.com/atomiczsec/Adrenaline/tree/main/.github/workflows "This path skips through empty directories") | [.github/workflows](https://github.com/atomiczsec/Adrenaline/tree/main/.github/workflows "This path skips through empty directories") | [fix: security hardening — GHA injection, wrong constant, invalid JSON](https://github.com/atomiczsec/Adrenaline/commit/045126c9afe0eb489cc832822edd0cb5a321deea "fix: security hardening — GHA injection, wrong constant, invalid JSON  - .github/workflows/release.yml: Fix script injection by moving   user-controlled inputs (module_path, tag_suffix) to env vars instead   of direct ${{ }} interpolation in shell blocks. Pin   softprops/action-gh-release to SHA (v2.6.2). Add explicit   permissions: contents: read to the detect job.  - collection/ai_surface/ai_surface.c: Replace INVALID_FILE_ATTRIBUTES   with the correct (DWORD)0xFFFFFFFF for GetFileSize error check.   Both happen to be 0xFFFFFFFF but the former is semantically wrong.  - discovery/wallpaper_enum/metadata.json: Remove trailing comma that   made the file invalid JSON.  Co-Authored-By: Devin AI <158243242+devin-ai-integration[bot]@users.noreply.github.com>") | last weekJun 10, 2026 |
| [Assets](https://github.com/atomiczsec/Adrenaline/tree/main/Assets "Assets") | [Assets](https://github.com/atomiczsec/Adrenaline/tree/main/Assets "Assets") | [upload existing repo to github](https://github.com/atomiczsec/Adrenaline/commit/da6987054aef08d965cffd46c86113000bcdd2e5 "upload existing repo to github") | 8 months agoOct 29, 2025 |
| [collection](https://github.com/atomiczsec/Adrenaline/tree/main/collection "collection") | [collection](https://github.com/atomiczsec/Adrenaline/tree/main/collection "collection") | [Merge pull request](https://github.com/atomiczsec/Adrenaline/commit/d21f77ef45e31cd59318f07cd987c64df4c7383d "Merge pull request #5 from atomiczsec/devin/1781148087-improve-error-handling  Fix silent error swallowing and improve error propagation across BOFs") [#5](https://github.com/atomiczsec/Adrenaline/pull/5) [from atomiczsec/devin/1781148087-improve-error-…](https://github.com/atomiczsec/Adrenaline/commit/d21f77ef45e31cd59318f07cd987c64df4c7383d "Merge pull request #5 from atomiczsec/devin/1781148087-improve-error-handling  Fix silent error swallowing and improve error propagation across BOFs") | last weekJun 10, 2026 |
| [community](https://github.com/atomiczsec/Adrenaline/tree/main/community "community") | [community](https://github.com/atomiczsec/Adrenaline/tree/main/community "community") | [Improve error handling: fix silent failures and add error diagnostics](https://github.com/atomiczsec/Adrenaline/commit/e1e8b82368e244f164ef22ffad81e7689e680586 "Improve error handling: fix silent failures and add error diagnostics  - applications_enum.c: Remove RegCloseKey on uninitialized handle when   RegOpenKeyExA fails (undefined behavior bug) - window_handles_enum.c: Report errors when GetClipboardData or   GlobalLock fail in TestClipboardAccess instead of silently ignoring - powershell_history.c: Add error codes to file open/seek/read failures   in read_snippet_ascii_at for diagnosability - notepad_grab.c: Report error when CreateToolhelp32Snapshot fails   in FindNotepadProcesses - process_tokens_list.c: Report specific failure reason in   EnableSeDebugPrivilege (OpenProcessToken vs LookupPrivilegeValue) - wevt_logon_enum.c: Report which wevtapi function failed to resolve   instead of generic failure message  Co-Authored-By: Devin AI <158243242+devin-ai-integration[bot]@users.noreply.github.com>") | last weekJun 10, 2026 |
| [credential\_access](https://github.com/atomiczsec/Adrenaline/tree/main/credential_access "credential_access") | [credential\_access](https://github.com/atomiczsec/Adrenaline/tree/main/credential_access "credential_access") | [Merge pull request](https://github.com/atomiczsec/Adrenaline/commit/c1e34aea28fa0390143db148a264f59322abea8f "Merge pull request #6 from atomiczsec/devin/1781148812-fix-cloud-metadata-bugs  Fix bugs in cloud_metadata_check: select() error fd, O(n²) cred path, redundant URL build") [#6](https://github.com/atomiczsec/Adrenaline/pull/6) [from atomiczsec/devin/1781148812-fix-cloud-meta…](https://github.com/atomiczsec/Adrenaline/commit/c1e34aea28fa0390143db148a264f59322abea8f "Merge pull request #6 from atomiczsec/devin/1781148812-fix-cloud-metadata-bugs  Fix bugs in cloud_metadata_check: select() error fd, O(n²) cred path, redundant URL build") | last weekJun 10, 2026 |
| [discovery](https://github.com/atomiczsec/Adrenaline/tree/main/discovery "discovery") | [discovery](https://github.com/atomiczsec/Adrenaline/tree/main/discovery "discovery") | [Merge pull request](https://github.com/atomiczsec/Adrenaline/commit/d21f77ef45e31cd59318f07cd987c64df4c7383d "Merge pull request #5 from atomiczsec/devin/1781148087-improve-error-handling  Fix silent error swallowing and improve error propagation across BOFs") [#5](https://github.com/atomiczsec/Adrenaline/pull/5) [from atomiczsec/devin/1781148087-improve-error-…](https://github.com/atomiczsec/Adrenaline/commit/d21f77ef45e31cd59318f07cd987c64df4c7383d "Merge pull request #5 from atomiczsec/devin/1781148087-improve-error-handling  Fix silent error swallowing and improve error propagation across BOFs") | last weekJun 10, 2026 |
| [execution](https://github.com/atomiczsec/Adrenaline/tree/main/execution "execution") | [execution](https://github.com/atomiczsec/Adrenaline/tree/main/execution "execution") | [Improve error handling: fix silent failures and add error diagnostics](https://github.com/atomiczsec/Adrenaline/commit/e1e8b82368e244f164ef22ffad81e7689e680586 "Improve error handling: fix silent failures and add error diagnostics  - applications_enum.c: Remove RegCloseKey on uninitialized handle when   RegOpenKeyExA fails (undefined behavior bug) - window_handles_enum.c: Report errors when GetClipboardData or   GlobalLock fail in TestClipboardAccess instead of silently ignoring - powershell_history.c: Add error codes to file open/seek/read failures   in read_snippet_ascii_at for diagnosability - notepad_grab.c: Report error when CreateToolhelp32Snapshot fails   in FindNotepadProcesses - process_tokens_list.c: Report specific failure reason in   EnableSeDebugPrivilege (OpenProcessToken vs LookupPrivilegeValue) - wevt_logon_enum.c: Report which wevtapi function failed to resolve   instead of generic failure message  Co-Authored-By: Devin AI <158243242+devin-ai-integration[bot]@users.noreply.github.com>") | last weekJun 10, 2026 |
| [.gitignore](https://github.com/atomiczsec/Adrenaline/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/atomiczsec/Adrenaline/blob/main/.gitignore ".gitignore") | [add service\_control BOF + gitignore for no bloat](https://github.com/atomiczsec/Adrenaline/commit/e57ed1e5d0a0a24de8cf0aeebd1c80f91832728b "add service_control BOF + gitignore for no bloat") | last monthMay 18, 2026 |
| [LICENSE](https://github.com/atomiczsec/Adrenaline/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/atomiczsec/Adrenaline/blob/main/LICENSE "LICENSE") | [Initial commit](https://github.com/atomiczsec/Adrenaline/commit/76a3ca40778ba1de1da2baf1edb7931f719b7891 "Initial commit") | 8 months agoOct 29, 2025 |
| [README.md](https://github.com/atomiczsec/Adrenaline/blob/main/README.md "README.md") | [README.md](https://github.com/atomiczsec/Adrenaline/blob/main/README.md "README.md") | [Add cloud\_metadata\_check BOF entry to README](https://github.com/atomiczsec/Adrenaline/commit/56363bb91786faf1f5d5bb879d6153ed2b18f98e "Add cloud_metadata_check BOF entry to README  Included a new entry for the cloud_metadata_check BOF, detailing its functionality in probing cloud-local metadata services for AWS, Azure, and GCP.") | 3 weeks agoMay 29, 2026 |
| View all files |

## Repository files navigation

# Adrenaline BOF Kit

[Permalink: Adrenaline BOF Kit](https://github.com/atomiczsec/Adrenaline#adrenaline-bof-kit)

[![](https://github.com/atomiczsec/Adrenaline/raw/main/Assets/ADRENALINE.jpg)](https://github.com/atomiczsec/Adrenaline/blob/main/Assets/ADRENALINE.jpg)

_A C2-agnostic collection of Beacon Object Files (BOFs) for red team and offensive security operations. BOFs are organized by attack chain phase and designed to be small, modular, and automation-friendly for use in reconnaissance, enumeration, and post-exploitation workflows._

## Table of Contents (MITRE taxonomy)

[Permalink: Table of Contents (MITRE taxonomy)](https://github.com/atomiczsec/Adrenaline#table-of-contents-mitre-taxonomy)

[Collection](https://github.com/atomiczsec/Adrenaline#collection)

[Community](https://github.com/atomiczsec/Adrenaline#community)

[Credential Access](https://github.com/atomiczsec/Adrenaline#credential-access)

[Discovery](https://github.com/atomiczsec/Adrenaline#discovery)

[Execution](https://github.com/atomiczsec/Adrenaline#execution)

## Collection

[Permalink: Collection](https://github.com/atomiczsec/Adrenaline#collection)

| **BOF** | **Use** |
| --- | --- |
| **[ai\_surface](https://github.com/atomiczsec/Adrenaline/blob/main/collection/ai_surface)** | Maps AI tooling on Windows developer endpoints and highlights their configuration artifacts that may expose server definitions, commands, arguments, and embedded credentials. |
| **[clipboard\_grab](https://github.com/atomiczsec/Adrenaline/blob/main/collection/clipboard_grab)** | Retrieves text data from the Windows clipboard using Win32 APIs and returns the contents to the callback. Original Code Credits: [@rvrsh3ll](https://github.com/rvrsh3ll/BOF_Collection) |
| **[powershell\_history](https://github.com/atomiczsec/Adrenaline/blob/main/collection/powershell_history)** | Collects PowerShell history artifacts from default PSReadLine and transcript locations. Useful for locating credentials or infrastructure. |
| **[window\_handles\_enum](https://github.com/atomiczsec/Adrenaline/blob/main/collection/window_handles_enum)** | Enumerates window handles across all system processes and uses a legitimate window handle to access the clipboard. |

## Community

[Permalink: Community](https://github.com/atomiczsec/Adrenaline#community)

| **BOF** | **Use** |
| --- | --- |
| **[notepad\_grab](https://github.com/atomiczsec/Adrenaline/blob/main/community/notepad_grab)** | Extracts and returns plain text directly from open Notepad windows by reading memory, allowing operators to recover unsaved or in-memory notes. Useful for data collection from live endpoints. Original Source: [NoteThief](https://github.com/trainr3kt/NoteThief) |
| **[schtask\_enum](https://github.com/atomiczsec/Adrenaline/blob/main/community/schtask_enum)** | Enumerates scheduled tasks on Windows systems using the Task Scheduler COM interface. Provides a summary of tasks including their state, schedule, and configuration without overwhelming the beacon with XML data. Original Source: [TrustedSec CS-Situational-Awareness-BOF](https://github.com/trustedsec/CS-Situational-Awareness-BOF) |
| **[net\_use](https://github.com/atomiczsec/Adrenaline/blob/main/community/net_use)** | Add, list, or remove mapped drives via MPR (Modernized to manage memory properly, avoiding crashing) Original Source: [TrustedSec CS-Situational-Awareness-BOF](https://github.com/trustedsec/CS-Situational-Awareness-BOF) |
| **[session\_view](https://github.com/atomiczsec/Adrenaline/blob/main/community/session_view)** | Enumerates Windows Terminal Services sessions, displaying session IDs, usernames, domains, connection states, and session LUIDs. Original Source: [SessionView](https://github.com/lsecqt/SessionView) by lsecqt |

## Credential Access

[Permalink: Credential Access](https://github.com/atomiczsec/Adrenaline#credential-access)

| **BOF** | **Use** |
| --- | --- |
| **[certstore\_loot](https://github.com/atomiczsec/Adrenaline/blob/main/credential_access/certstore_loot)** | Enumerates local certificate stores to find certificates with exportable private keys and provides you with the path to export them. |
| **[cloud\_metadata\_check](https://github.com/atomiczsec/Adrenaline/blob/main/credential_access/cloud_metadata_check)** | Probes cloud-local metadata services for AWS, Azure, and GCP from the current process, reporting provider identity, instance context, and bounded credential snippets when reachable. |
| **[process\_tokens\_list](https://github.com/atomiczsec/Adrenaline/blob/main/credential_access/process_tokens_list)** | Enumerates accessible tokens from running processes, showing user context, token type (primary/impersonation), and impersonation level. Supports optional filtering by PID or process name. SeDebugPrivilege is disabled by default for OPSEC. |

## Discovery

[Permalink: Discovery](https://github.com/atomiczsec/Adrenaline#discovery)

| **BOF** | **Use** |
| --- | --- |
| **[amsi\_etw\_detect](https://github.com/atomiczsec/Adrenaline/blob/main/discovery/amsi_etw_detect)** | Checks for AMSI and ETW presence in the current process by detecting loaded DLLs and ETW-related exports. Useful for picking targets with less security activity when applied broadly. |
| **[app\_count](https://github.com/atomiczsec/Adrenaline/blob/main/discovery/app_count)** | Counts the number of installed applications via the registry, de-duplicates, and prints. Applied to a large number of beacons, allows us to infer things about a device based on app count differences. |
| **[applocker\_policy](https://github.com/atomiczsec/Adrenaline/blob/main/discovery/applocker_policy)** | Enumerates AppLocker policy configurations, rule collections, and enforcement modes by scanning the relevant registry keys. |
| **[asr\_status](https://github.com/atomiczsec/Adrenaline/blob/main/discovery/asr_status)** | Enumerates Windows Defender Attack Surface Reduction (ASR) rules from registry locations to identify which ASR rules are configured, their enforcement state (Block/Audit/Warn/Disabled), and the policy source (Intune/MDM vs Group Policy). |
| **[bitlocker\_status](https://github.com/atomiczsec/Adrenaline/blob/main/discovery/bitlocker_status)** | Enumerates BitLocker encryption status, policy configurations, and recovery key backup locations by scanning registry keys. |
| **[mdm\_policy\_artifacts](https://github.com/atomiczsec/Adrenaline/blob/main/discovery/mdm_policy_artifacts)** | Uses a scoring model to assess MDM enrollment posture on Windows systems by evaluating indicators including join state, scheduled tasks, policy configuration, and enrollment artifacts. |
| **[netjoin\_query](https://github.com/atomiczsec/Adrenaline/blob/main/discovery/netjoin_query)** | Queries Windows domain join information and workstation details, identifying if the system is domain-joined or in a workgroup. |
| **[power\_state](https://github.com/atomiczsec/Adrenaline/blob/main/discovery/power_state)** | Identifies host form factor as Laptop, Desktop, Tablet, Server, Embedded, or Unknown using SMBIOS chassis data with a power-status fallback. |
| **[proxy\_enum](https://github.com/atomiczsec/Adrenaline/blob/main/discovery/proxy_enum)** | Enumerates Windows proxy configuration state across WinINET, WinHTTP, policy keys, environment variables, WPAD indicators, Chrome settings, and .NET `defaultProxy` values. |
| **[user\_idle](https://github.com/atomiczsec/Adrenaline/blob/main/discovery/user_idle)** | Gets user idle time since last input and GUI resource usage (GDI/USER handles) in the current process for timing intelligence. |
| **[wallpaper\_enum](https://github.com/atomiczsec/Adrenaline/blob/main/discovery/wallpaper_enum)** | Enumerates the current desktop wallpaper path for each attached monitor using the modern IDesktopWallpaper COM interface. Centralized wallpapers are sometimes on internal SMB shares or imaging servers, revealing network paths, domain trusts, and policy enforcement without touching disk or the network. |
| **[wef\_detect](https://github.com/atomiczsec/Adrenaline/blob/main/discovery/wef_detect)** | Detects Windows Event Forwarding (WEF) configuration, which indicates centralized logging. If found, indicates security events are being forwarded to a central server. |
| **[window\_list](https://github.com/atomiczsec/Adrenaline/blob/main/discovery/window_list)** | Enumerates the titles of all visible windows on the current user's desktop, optionally including Process IDs (PIDs). |
| **[wsc\_status](https://github.com/atomiczsec/Adrenaline/blob/main/discovery/wsc_status)** | Queries Windows Security Center health status, including Anti-Virus, Firewall, Anti-Spyware, WSC Service, Auto-Update, Internet Settings, and User Account Control. |
| **[win\_version](https://github.com/atomiczsec/Adrenaline/blob/main/discovery/win_version)** | This BOF queries the registry and system APIs to provide a concise but detailed overview of the Windows installation. |

## Execution

[Permalink: Execution](https://github.com/atomiczsec/Adrenaline#execution)

| **BOF** | **Use** |
| --- | --- |
| **[com\_probe](https://github.com/atomiczsec/Adrenaline/blob/main/execution/com_probe)** | Probe whether a COM object can be instantiated from a given CLSID. |
| **[firewall\_rule](https://github.com/atomiczsec/Adrenaline/blob/main/execution/firewall_rule)** | Add, remove, or query Windows Firewall rules via the COM API (`INetFwPolicy2`) without spawning `netsh.exe` or `cmd.exe`. Useful for pivoting inside networks. |
| **[service\_control](https://github.com/atomiczsec/Adrenaline/blob/main/execution/service_control)** | Manages local Windows services via SCM: query (capped list or single service), create, start, stop, delete, and configure failure actions. Elevated rights usually required for changes. |
| **[wevt\_logon\_enum](https://github.com/atomiczsec/Adrenaline/blob/main/execution/wevt_logon_enum)** | Enumerates recent Security log (successful/failed) logon events (Event IDs 4624,4625,4672) via the wevtapi API and prints remote workstation name/IP plus the target username. |

* * *

### Connect with me:

[Permalink: Connect with me:](https://github.com/atomiczsec/Adrenaline#connect-with-me)

[![](https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/github.svg)](https://github.com/atomiczsec)[![](https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg)](https://instagram.com/atomiczsec)[![](https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/twitter.svg)](https://x.com/atomiczsec)[![](https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/medium.svg)](https://medium.com/@atomiczsec)[![](https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/youtube.svg)](https://youtube.com/@atomiczsec)

* * *

**DISCLAIMER:** The creators and contributors of this repository accept no liability for any loss, damage, or consequences resulting from the use of the information or code contained in this repo. By utilizing this repo, you acknowledge and accept full responsibility for your actions. Use at your own risk.

## About

C2-agnostic BOF collection, categorized by attack chain phase. Designed to be small and modular, allowing for quick execution and automation.


[www.atomiczsec.net/projects](https://www.atomiczsec.net/projects "https://www.atomiczsec.net/projects")

### Topics

[windows](https://github.com/topics/windows "Topic: windows") [bof](https://github.com/topics/bof "Topic: bof")

### Resources

[Readme](https://github.com/atomiczsec/Adrenaline#readme-ov-file)

### License

[MIT license](https://github.com/atomiczsec/Adrenaline#MIT-1-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/atomiczsec/Adrenaline).

[Activity](https://github.com/atomiczsec/Adrenaline/activity)

### Stars

[**308**\\
stars](https://github.com/atomiczsec/Adrenaline/stargazers)

### Watchers

[**1**\\
watching](https://github.com/atomiczsec/Adrenaline/watchers)

### Forks

[**34**\\
forks](https://github.com/atomiczsec/Adrenaline/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fatomiczsec%2FAdrenaline&report=atomiczsec+%28user%29)

## [Releases\  30](https://github.com/atomiczsec/Adrenaline/releases)

[Release credential\_access-cloud\_metadata\_check-2026-05-29-145430-56363bb\\
Latest\\
\\
3 weeks agoMay 29, 2026](https://github.com/atomiczsec/Adrenaline/releases/tag/credential_access-cloud_metadata_check-2026-05-29-145430-56363bb)

[\+ 29 releases](https://github.com/atomiczsec/Adrenaline/releases)

## [Packages\  0](https://github.com/users/atomiczsec/packages?repo_name=Adrenaline)

No packages published

## [Contributors\  3](https://github.com/atomiczsec/Adrenaline/graphs/contributors)

- [![@atomiczsec](https://avatars.githubusercontent.com/u/75549184?s=64&v=4)](https://github.com/atomiczsec)[**atomiczsec** Gavin K](https://github.com/atomiczsec)
- [![@devin-ai-integration[bot]](https://avatars.githubusercontent.com/in/811515?s=64&v=4)](https://github.com/apps/devin-ai-integration)[**devin-ai-integration\[bot\]**](https://github.com/apps/devin-ai-integration)
- [![@cursoragent](https://avatars.githubusercontent.com/u/199161495?s=64&v=4)](https://github.com/cursoragent)[**cursoragent** Cursor Agent](https://github.com/cursoragent)

## Languages

- [C95.3%](https://github.com/atomiczsec/Adrenaline/search?l=c)
- [Makefile4.7%](https://github.com/atomiczsec/Adrenaline/search?l=makefile)

You can’t perform that action at this time.