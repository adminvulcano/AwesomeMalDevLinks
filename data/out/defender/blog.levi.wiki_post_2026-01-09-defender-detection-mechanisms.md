# https://blog.levi.wiki/post/2026-01-09-defender-detection-mechanisms

# Defender's different Detection Mechanisms

This post is based on the observations from my [EDRi Framework](https://github.com/cailllev/EDR-Introspection).

TL;DL: EDRi attaches itself to the Antimalware and Kernel ETW traces, and hooks ntdll of MsMpEng.exe, to supervise all actions MDE takes against my attack.exe

Start [here](https://blog.levi.wiki/post/2025-12-04-defender-detection-engines) if you do not know about heuristic scans, emulations, memory scans or behaviour tracking.

## EDRi Log Analysis

The output of the EDRi framework is analysed and interpreted, given these four attacks:

- [CobaltStrike loader, no bypass](https://github.com/cailllev/EDR-Introspection/blob/d1c16c36e0e7a16cbd474df7331a3c7b5b6fec27/EDRi/dumps/events/MDE-vs-ProcInject-standard.csv)
- [CobaltStrike loader, obfuscated](https://github.com/cailllev/EDR-Introspection/blob/d1c16c36e0e7a16cbd474df7331a3c7b5b6fec27/EDRi/dumps/events/MDE-vs-ProcInject-obfuscation.csv)
- [Lsass dumper, no bypass](https://github.com/cailllev/EDR-Introspection/blob/d1c16c36e0e7a16cbd474df7331a3c7b5b6fec27/EDRi/dumps/events/MDE-vs-LsassReader-standard.csv)
- [Lsass dumper, deconditioning](https://github.com/cailllev/EDR-Introspection/blob/d1c16c36e0e7a16cbd474df7331a3c7b5b6fec27/EDRi/dumps/events/MDE-vs-LsassReader-deconditioning.csv)

The logs are also available as nicely formatted and pre-filtered Google sheets [here](https://drive.google.com/drive/folders/17SLAfnBD9_jk4VrKUqm-2ZQ_pcJcnw-Z?usp=sharing).

The goal of the EDRi framework is to observe what the EDR does, therefore 2 undetected and 2 detected attacks are analysed further.

Try to guess which attacks are undetected, source code is [here](https://github.com/cailllev/EDR-Introspection/tree/master/attacks).

- CobaltStrike loader (obfuscated) is detected as a generic loader (Trojan/Bearfoos) when storing on disk.
- Lsass dumper (no bypass) can be executed but is frozen after the lsass process is opened and MiniDumpWriteDump is called.
- Generating a CobaltStrike loader (with default config) as raw bytes, storing the shellcode as an array, allocating memory, writing and invoking the shellcode still worked in 2025. Who would've guessed?
- The lsass dumper also works, when using deconditioning. This is still a bit of magic, more [here](https://blog.levi.wiki/post/2025-12-05-decondition-everything).

## Observed Mechanisms

The listed mechanisms below can be found in the Microsoft-Antimalware-Engine ETW trace, as individual events.

The mechanisms are named after the event operation, task or message. There is no systematic way Microsoft labeled these.

The EDRi framework is [my master's thesis](https://github.com/cailllev/EDR-Introspection/blob/master/paper/EDR-Introspection.pdf), the analysis of the logs is a part of it and took substantial amount of time and nerves.

The table below is based on the analysis over all 4 EDRi logs, and the mechanisms are observed in all logs and in the same ordering.

| Mechanism | Event ID | Assumed Objective(s) |
| --- | --- | --- |
| stream scan | 32 | This represents the heuristics step (engine), gets static information |
| MetaStore insert | 44 | Stores extracted identifiers from heuristics and emulations |
| MetaStore query | 44 | Gets identifiers, used to decide what further analysis must be done |
| scan | 1 | This represents the complete emulation step (engine) |
| MOAC lookup | 36 | Used to check if a file should be emulated or not |
| UfsScanFile | 30 | The actual emulation of the file |
| UfsScanProc | 32 | The actual emulation (of a process?) |
| GetHashes | 43 | Extracts identifiers (cryptographic hashes) after an emulation, sometimes for retrieval of info in heuristics phase (stream scan) |
| UfsScanProc | 32 | Scans the loaded modules in a process |
| SpyNet report | 43 | Bundles identifiers, submits them to Microsoft’s cloud to request a verdict (or simply Microsoft’s data collection of known executables) |

### Data only in Threat-Intelligence

AllocVM and ProtectVM events indicate memory allocation or memory permission changes (to RW, then to RX) inside MsMpEng itself.

This is always linked to an emulation of your executable. Either sequence of events may _preceed_ such an emulation:

- UfsScanFileTask start, NtCreateFile your.exe with access=0x120081, NtCreate your.exe with access=0x120089 (read data, read attr, read EA, read control, sync)
- UfsScaProcTask start, NtOpenProcess your.exe with access=0x418 (ProcVmOperation, ProcVmRead, ProcQueryInfo)

### Memory Reads

All memory reads by MsMpEng are preceeded by a NtOpenProcess system call. This system call is also logged in the **Microsoft-Windows-Kernel-Audit-API-Calls** ETW trace.

The event log also includes the desiredaccess field, indicating what operation will be done. Observed use-cases:

| desired access | rights | observed time | subsequent actions | interpretation |
| --- | --- | --- | --- | --- |
| 0x410 | ProcVmRead,ProcQueryInfo | after behaviour trigger | NtQueryInformationProcess InfoClass=Basic | extensive memory scan |
| 0x418 | ProcVmOperation,ProcVmRead,ProcQueryInfo | proc start | NtQueryInformationProcess InfoClass=Session,Basic | get loaded modules via LDR + pointer in ntdll |
| 0x600 | ProcSetInfo,ProcQueryInfo | proc start | NtQueryInformationProcess InfoClass=Logging | get logging info |
| 0x1000 | ProcQueryLimitedInfo | various | NtQueryInformationProcess InfoClass=Session,ThreadPagePrio | cache lookup helper? |
| 0x1010 | ProcVmRead,ProcQueryLimitedInfo | various | NtQueryInformationProcess InfoClass=Session,Basic | after file read of attack.exe? |
| 0x1410 | ProcVmRead,ProcQuery(Limited)Info | various | NtQueryInformationProcess InfoClass=Session,Basic,Wow64 | may get first module in LDR + pointer in ntdll |
| 0x101000 | Sync,ProcQueryLimitedInfo | around scan request | NtQueryInformationProcess InfoClass=Session,ImageFileName | get exe name |

## Conclusion

It should be able to predict MDE's (MsMpEng's) actions with just observing the **Microsoft-Windows-Kernel-Audit-API-Calls** ETW trace.

The **desiredaccess** field from the event **PsOpenProcess**, eventID 5, can be combined with the above observations.

It is then possible to create **AURA** malware, in the sense of **Access-based, Unintentionally Revealed Actions**.

Alternative name: **BITE** malware, Behavioural Intent Tracking via ETW

## Future Work

- do [more attacks](https://github.com/cailllev/EDR-Introspection/tree/master?tab=readme-ov-file#create-own-attack)
- analyse more logs
- verify above findings
- develop [EDRi Core](https://blog.levi.wiki/post/Link%20follows)
- create **AURA** malware, test hypothesis