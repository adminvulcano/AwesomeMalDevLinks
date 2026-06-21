# https://github.com/sbousseaden/EDRUnChoker

[Skip to content](https://github.com/sbousseaden/EDRUnChoker/#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/sbousseaden/EDRUnChoker/) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/sbousseaden/EDRUnChoker/) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/sbousseaden/EDRUnChoker/) to refresh your session.Dismiss alert

{{ message }}

[sbousseaden](https://github.com/sbousseaden)/ **[EDRUnChoker](https://github.com/sbousseaden/EDRUnChoker)** Public

- [Notifications](https://github.com/login?return_to=%2Fsbousseaden%2FEDRUnChoker) You must be signed in to change notification settings
- [Fork\\
3](https://github.com/login?return_to=%2Fsbousseaden%2FEDRUnChoker)
- [Star\\
40](https://github.com/login?return_to=%2Fsbousseaden%2FEDRUnChoker)


master

[**1** Branch](https://github.com/sbousseaden/EDRUnChoker/branches) [**0** Tags](https://github.com/sbousseaden/EDRUnChoker/tags)

[Go to Branches page](https://github.com/sbousseaden/EDRUnChoker/branches)[Go to Tags page](https://github.com/sbousseaden/EDRUnChoker/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![sbousseaden](https://avatars.githubusercontent.com/u/20989958?v=4&size=40)](https://github.com/sbousseaden)[sbousseaden](https://github.com/sbousseaden/EDRUnChoker/commits?author=sbousseaden)<br>[Update README.md](https://github.com/sbousseaden/EDRUnChoker/commit/6bc6866762188e46b4dca1683e8540181a84092d)<br>2 weeks agoJun 8, 2026<br>[6bc6866](https://github.com/sbousseaden/EDRUnChoker/commit/6bc6866762188e46b4dca1683e8540181a84092d) · 2 weeks agoJun 8, 2026<br>## History<br>[5 Commits](https://github.com/sbousseaden/EDRUnChoker/commits/master/) <br>Open commit details<br>[View commit history for this file.](https://github.com/sbousseaden/EDRUnChoker/commits/master/) 5 Commits |
| [.gitignore](https://github.com/sbousseaden/EDRUnChoker/blob/master/.gitignore ".gitignore") | [.gitignore](https://github.com/sbousseaden/EDRUnChoker/blob/master/.gitignore ".gitignore") | [EDRUnChoker: fileless WMI defense against EDRChoker QoS throttling](https://github.com/sbousseaden/EDRUnChoker/commit/52e684d55b3de5a8e0fdf34445c52b9ebf521078 "EDRUnChoker: fileless WMI defense against EDRChoker QoS throttling") | 2 weeks agoJun 8, 2026 |
| [Get-EdrChokerDefenseStatus.ps1](https://github.com/sbousseaden/EDRUnChoker/blob/master/Get-EdrChokerDefenseStatus.ps1 "Get-EdrChokerDefenseStatus.ps1") | [Get-EdrChokerDefenseStatus.ps1](https://github.com/sbousseaden/EDRUnChoker/blob/master/Get-EdrChokerDefenseStatus.ps1 "Get-EdrChokerDefenseStatus.ps1") | [Fix ActiveStore QoS policy detection via WbemContext PolicyStore.](https://github.com/sbousseaden/EDRUnChoker/commit/9d28f642d9de3c40b4d1b392973ed1fd318acb47 "Fix ActiveStore QoS policy detection via WbemContext PolicyStore.  Plain WMI ExecQuery missed ActiveStore policies from New-NetQosPolicy and EDRChoker; enumerate ActiveStore and GPO:localhost with SWbemNamedValueSet and align status checks with Get-NetQosPolicy.") | 2 weeks agoJun 8, 2026 |
| [Install-EdrChokerWmiDefense.ps1](https://github.com/sbousseaden/EDRUnChoker/blob/master/Install-EdrChokerWmiDefense.ps1 "Install-EdrChokerWmiDefense.ps1") | [Install-EdrChokerWmiDefense.ps1](https://github.com/sbousseaden/EDRUnChoker/blob/master/Install-EdrChokerWmiDefense.ps1 "Install-EdrChokerWmiDefense.ps1") | [Fix ActiveStore QoS policy detection via WbemContext PolicyStore.](https://github.com/sbousseaden/EDRUnChoker/commit/9d28f642d9de3c40b4d1b392973ed1fd318acb47 "Fix ActiveStore QoS policy detection via WbemContext PolicyStore.  Plain WMI ExecQuery missed ActiveStore policies from New-NetQosPolicy and EDRChoker; enumerate ActiveStore and GPO:localhost with SWbemNamedValueSet and align status checks with Get-NetQosPolicy.") | 2 weeks agoJun 8, 2026 |
| [README.md](https://github.com/sbousseaden/EDRUnChoker/blob/master/README.md "README.md") | [README.md](https://github.com/sbousseaden/EDRUnChoker/blob/master/README.md "README.md") | [Update README.md](https://github.com/sbousseaden/EDRUnChoker/commit/6bc6866762188e46b4dca1683e8540181a84092d "Update README.md") | 2 weeks agoJun 8, 2026 |
| [Uninstall-EdrChokerWmiDefense.ps1](https://github.com/sbousseaden/EDRUnChoker/blob/master/Uninstall-EdrChokerWmiDefense.ps1 "Uninstall-EdrChokerWmiDefense.ps1") | [Uninstall-EdrChokerWmiDefense.ps1](https://github.com/sbousseaden/EDRUnChoker/blob/master/Uninstall-EdrChokerWmiDefense.ps1 "Uninstall-EdrChokerWmiDefense.ps1") | [Fix ActiveStore QoS policy detection via WbemContext PolicyStore.](https://github.com/sbousseaden/EDRUnChoker/commit/9d28f642d9de3c40b4d1b392973ed1fd318acb47 "Fix ActiveStore QoS policy detection via WbemContext PolicyStore.  Plain WMI ExecQuery missed ActiveStore policies from New-NetQosPolicy and EDRChoker; enumerate ActiveStore and GPO:localhost with SWbemNamedValueSet and align status checks with Get-NetQosPolicy.") | 2 weeks agoJun 8, 2026 |
| View all files |

## Repository files navigation

# EDRUnChoker

[Permalink: EDRUnChoker](https://github.com/sbousseaden/EDRUnChoker/#edrunchoker)

**Fileless WMI remediation for [EDRChoker](https://github.com/TwoSevenOneT/EDRChoker)** counters QoS abuse (`pacer.sys`) that throttles EDR agents to near-zero network bandwidth.

Registers a permanent subscription in `root\subscription` (no files on disk). A 5-second timer runs embedded VBScript that enumerates QoS policies with **WbemContext `PolicyStore`** on **ActiveStore** and **GPO:localhost** — plain WMI `ExecQuery` misses ActiveStore policies created by `New-NetQosPolicy` / EDRChoker — and removes malicious app-path throttles targeting known security products or aggressive rates (≤ 1 Mbps).

## Scripts

[Permalink: Scripts](https://github.com/sbousseaden/EDRUnChoker/#scripts)

| Script | Purpose |
| --- | --- |
| `Install-EdrChokerWmiDefense.ps1` | Deploy subscription (elevated) |
| `Uninstall-EdrChokerWmiDefense.ps1` | Remove subscription |
| `Get-EdrChokerDefenseStatus.ps1` | Check subscription and policy count |

## Quick start

[Permalink: Quick start](https://github.com/sbousseaden/EDRUnChoker/#quick-start)

```
.\Install-EdrChokerWmiDefense.ps1
.\Get-EdrChokerDefenseStatus.ps1
```

## SOC / event log

[Permalink: SOC / event log](https://github.com/sbousseaden/EDRUnChoker/#soc--event-log)

Each successful cleanup writes a **Warning** to the **Application** log under source **EDRChokerDefense**. One event is emitted per removed policy, useful as remediation evidence and to correlate with EDRChoker activity on the host.

![image](https://private-user-images.githubusercontent.com/20989958/604354319-60001ea8-c1b5-4a93-8a4e-9facea3e51d1.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODIwNDY0MzYsIm5iZiI6MTc4MjA0NjEzNiwicGF0aCI6Ii8yMDk4OTk1OC82MDQzNTQzMTktNjAwMDFlYTgtYzFiNS00YTkzLThhNGUtOWZhY2VhM2U1MWQxLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA2MjElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNjIxVDEyNDg1NlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWEzNjA3Yzk5NmIzZjdhZmJhYzk3MzkxYzMwYzVlMDI1NGUyMTM4OGE2ZmYyMThjMTkxMjEyZmNmMjgzOWY5MDgmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRnBuZyJ9.tr7ZWp102KkGNs-al0A3Uban6X04T-Z-LG6bUJEsA8E) ![image](https://private-user-images.githubusercontent.com/20989958/604553765-283d6071-dc66-4633-a4d7-c0917c52e751.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODIwNDY0MzYsIm5iZiI6MTc4MjA0NjEzNiwicGF0aCI6Ii8yMDk4OTk1OC82MDQ1NTM3NjUtMjgzZDYwNzEtZGM2Ni00NjMzLWE0ZDctYzA5MTdjNTJlNzUxLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA2MjElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNjIxVDEyNDg1NlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWJiY2UzZGZmMDJiODI1MDU5YzU4M2M3MGY2ZjZjMGY2ZDAwMGJjNmM3ODgzYWJmODk2YzljMmFkNzUwZDBjZjAmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRnBuZyJ9.WIiVhlEcEwgRIqeGcsZ4skIZSmRgulMO79yb-aN-EeA)

| Event ID | Meaning |
| --- | --- |
| 1000 | Subscription installed |
| 1001 | Subscription removed |
| 1002 | Malicious QoS policy removed |
| 1003 | Remediation failed |

**1002 example:**`action=remediate qos_policy=02zxnnzr target=elastic-endpoint.exe throttle_bps=8 tier=tier1-known-edr store=ActiveStore`

```
Get-WinEvent -FilterHashtable @{ LogName='Application'; ProviderName='EDRChokerDefense' } -MaxEvents 50
```

Forward `ProviderName="EDRChokerDefense"` via WEF, Splunk UF, Elastic Agent, etc.

## Protect the subscription

[Permalink: Protect the subscription](https://github.com/sbousseaden/EDRUnChoker/#protect-the-subscription)

Attackers may delete or modify the WMI objects in `root\subscription` to disable defense. **Baseline** the subscription after install and alert on changes.

**Sysmon** (recommended): enable and monitor:

| Sysmon ID | What to watch |
| --- | --- |
| **19** | `WmiEventFilter` created/modified/deleted |
| **20** | `WmiEventConsumer` created/modified/deleted |
| **21** | `WmiEventFilter` ↔ consumer binding changes |

Alert on any activity involving `EDRChokerDefense_QoSFilter`, `EDRChokerDefense_QoSConsumer`, or `EDRChokerDefense_Timer`, and on **new**`ActiveScriptEventConsumer` / `CommandLineEventConsumer` instances outside your change window.

**Periodic validation** (GPO/script): `Get-WmiObject -Namespace root\subscription -Class __EventFilter | Where-Object Name -like 'EDRChokerDefense*'`

## References

[Permalink: References](https://github.com/sbousseaden/EDRUnChoker/#references)

- [EDRChoker](https://github.com/TwoSevenOneT/EDRChoker)
- [EDRChoker research](https://www.zerosalarium.com/2026/06/edrchoker-choking-telemetry-stream-block-edr.html)

## About

EDRUnChoker - fileless WMI defense that removes EDRChoker QoS throttling policies


### Resources

[Readme](https://github.com/sbousseaden/EDRUnChoker/#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/sbousseaden/EDRUnChoker/).

[Activity](https://github.com/sbousseaden/EDRUnChoker/activity)

### Stars

[**40**\\
stars](https://github.com/sbousseaden/EDRUnChoker/stargazers)

### Watchers

[**0**\\
watching](https://github.com/sbousseaden/EDRUnChoker/watchers)

### Forks

[**3**\\
forks](https://github.com/sbousseaden/EDRUnChoker/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fsbousseaden%2FEDRUnChoker&report=sbousseaden+%28user%29)

## [Releases](https://github.com/sbousseaden/EDRUnChoker/releases)

No releases published

## [Packages\  0](https://github.com/users/sbousseaden/packages?repo_name=EDRUnChoker)

No packages published

## [Contributors\  3](https://github.com/sbousseaden/EDRUnChoker/graphs/contributors)

- [![@sbousseaden](https://avatars.githubusercontent.com/u/20989958?s=64&v=4)](https://github.com/sbousseaden)[**sbousseaden**](https://github.com/sbousseaden)
- [![@Samirbous](https://avatars.githubusercontent.com/u/64742097?s=64&v=4)](https://github.com/Samirbous)[**Samirbous**](https://github.com/Samirbous)
- [![@cursoragent](https://avatars.githubusercontent.com/u/199161495?s=64&v=4)](https://github.com/cursoragent)[**cursoragent** Cursor Agent](https://github.com/cursoragent)

## Languages

- [PowerShell100.0%](https://github.com/sbousseaden/EDRUnChoker/search?l=powershell)

You can’t perform that action at this time.