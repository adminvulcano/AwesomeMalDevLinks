# https://learn.microsoft.com/en-us/defender-endpoint/amsi-on-mdav

Table of contents Exit editor mode

Ask LearnAsk LearnFocus mode

Table of contents[Read in English](https://learn.microsoft.com/en-us/defender-endpoint/amsi-on-mdav)Add to CollectionsAdd to plan[Edit](https://github.com/MicrosoftDocs/defender-docs/blob/public/defender-endpoint/amsi-on-mdav.md)

* * *

#### Share via

[Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Famsi-on-mdav%3FWT.mc_id%3Dfacebook) [x.com](https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Famsi-on-mdav%3FWT.mc_id%3Dtwitter&tw_p=tweetbutton&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Famsi-on-mdav%3FWT.mc_id%3Dtwitter) [LinkedIn](https://www.linkedin.com/feed/?shareActive=true&text=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Famsi-on-mdav%3FWT.mc_id%3Dlinkedin) [Email](mailto:?subject=%5BShared%20Article%5D%20Anti-malware%20Scan%20Interface%20(AMSI)%20integration%20with%20Microsoft%20Defender%20Antivirus%20-%20Microsoft%20Defender%20for%20Endpoint%20%7C%20Microsoft%20Learn&body=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Famsi-on-mdav%3FWT.mc_id%3Demail)

* * *

Copy MarkdownPrint

* * *

Note

Access to this page requires authorization. You can try [signing in](https://learn.microsoft.com/en-us/defender-endpoint/amsi-on-mdav#) or changing directories.


Access to this page requires authorization. You can try changing directories.


# Anti-malware Scan Interface (AMSI) integration with Microsoft Defender Antivirus

- Applies to: Microsoft Defender for Endpoint Plan 1, Microsoft Defender for Endpoint Plan 2, Microsoft Defender for Business, Microsoft Defender for Individuals

Feedback

Summarize this article for me


Microsoft Defender for Endpoint utilizes the anti-malware Scan Interface (AMSI) to enhance protection against fileless malware, dynamic script-based attacks, and other nontraditional cyber threats. This article describes the benefits of AMSI integration, the types of scripting languages it supports, and how to enable AMSI for improved security.

[Section titled: What is fileless malware?](https://learn.microsoft.com/en-us/defender-endpoint/amsi-on-mdav#what-is-fileless-malware)

## What is fileless malware?

Fileless malware plays a critical role in modern cyberattacks, using stealthy techniques to avoid detection. Several major ransomware outbreaks used fileless methods as part of their kill chains.

Fileless malware uses existing tools that are already present on a compromised device, such as PowerShell.exe or wmic.exe. Malware can infiltrate a process, executing code within its memory space, and invoking these built-in tools. Attackers significantly reduce their footprint and evade traditional detection mechanisms.

Because memory is volatile, and fileless malware doesn't place files on disk, establishing persistence by using fileless malware can be tricky. One example of how fileless malware achieved persistence was to create a registry run key that launches a "one-liner" PowerShell cmdlet. This command launched an obfuscated PowerShell script that was stored in the registry BLOB. The obfuscated PowerShell script contained a reflective portable executable (PE) loader that loaded a Base64-encoded PE from the registry. The script stored in the registry ensured the malware persisted.

Attackers use several fileless techniques that can make malware implants stealthy and evasive. These techniques include:

- **Reflective DLL injection**: Reflective DLL injection involves the manual loading of malicious DLLs into a process memory without the need for said DLLs to be on disk. The malicious DLL can be hosted on a remote attacker-controlled machine and delivered through a staged network channel (for example, Transport Layer Security (TLS) protocol), or embedded in obfuscated form inside infection vectors, like macros and scripts. This configuration results in the evasion of the OS mechanism that monitors and keeps track of loading executable modules. An example of malware that uses Reflective DLL injection is `HackTool:Win32/Mikatz!dha`.

- **Memory exploits**: Adversaries use fileless memory exploits to run arbitrary code remotely on victim machines. For example, the UIWIX threat uses the EternalBlue exploit, which was used by both Petya and WannaCry, to install the DoublePulsar backdoor, and lives entirely in the kernel's memory (SMB Dispatch Table). Unlike Petya and Wannacry, UIWIX doesn't drop any files on disk.

- **Script-based techniques**: Scripting languages provide powerful means for delivering memory-only executable payloads. Script files can embed encoded shell codes or binaries that they can decrypt on the fly at run time and execute via .NET objects or directly with APIs without requiring them to be written to disk. The scripts themselves can be hidden in the registry, read from network streams, or run manually in the command-line by an attacker, without ever touching the disk.



Note



Do not disable PowerShell as a means to block fileless malware. PowerShell is a powerful and secure management tool and is important for many system and IT functions. Attackers use malicious PowerShell scripts as post-exploitation technique that can only take place after an initial compromise has already occurred. Its misuse is a symptom of an attack that begins with other malicious actions like software exploitation, social engineering, or credential theft. The key is to prevent an attacker from getting into the position where they can misuse PowerShell.





Tip



Reducing the number of unsigned Powershell scripts in your environment helps with increasing your security posture.
Here are instructions on how you could add signing to the Powershell scripts used in your environment
[Hey, Scripting Guy! How Can I Sign Windows PowerShell Scripts with an Enterprise Windows PKI? (Part 2 of 2) \| Scripting Blog](https://devblogs.microsoft.com/scripting/hey-scripting-guy-how-can-i-sign-windows-powershell-scripts-with-an-enterprise-windows-pki-part-2-of-2/)

- **WMI persistence**: Some attackers use the Windows Management Instrumentation (WMI) repository to store malicious scripts that are then invoked periodically using WMI bindings.
Microsoft Defender Antivirus blocks most malware using generic, heuristic, and behavior-based detections, as well as local and cloud-based machine learning models. Microsoft Defender Antivirus protects against fileless malware through these capabilities:

  - Detecting script-based techniques by using AMSI, which provides the capability to inspect PowerShell and other script types, even with multiple layers of obfuscation
  - Detecting and remediating WMI persistence techniques by scanning the WMI repository, both periodically and whenever anomalous behavior is observed
  - Detecting reflective DLL injection through enhanced memory scanning techniques and behavioral monitoring

[Section titled: Prerequisites](https://learn.microsoft.com/en-us/defender-endpoint/amsi-on-mdav#prerequisites)

## Prerequisites

[Section titled: Supported operating systems](https://learn.microsoft.com/en-us/defender-endpoint/amsi-on-mdav#supported-operating-systems)

### Supported operating systems

- Windows 10 and later
- Windows Server 2016 and later

[Section titled: Supported Scripting Languages](https://learn.microsoft.com/en-us/defender-endpoint/amsi-on-mdav#supported-scripting-languages)

### Supported Scripting Languages

- PowerShell
- Jscript
- VBScript
- Windows Script Host (wscript.exe and cscript.exe)
- .NET Framework 4.8 or newer (scanning of all assemblies)
- Windows Management Instrumentation (WMI)

If you use Microsoft 365 Apps, AMSI also supports JavaScript, VBA, and XLM.

AMSI doesn't currently support Python or Perl.

[Section titled: Why AMSI?](https://learn.microsoft.com/en-us/defender-endpoint/amsi-on-mdav#why-amsi)

## Why AMSI?

AMSI provides a deeper level of inspection for malicious software that employs obfuscation and evasion techniques on Windows' built-in scripting hosts. By integrating AMSI, Microsoft Defender for Endpoint offers extra layers of protection against advanced threats.

[Section titled: Enabling AMSI](https://learn.microsoft.com/en-us/defender-endpoint/amsi-on-mdav#enabling-amsi)

### Enabling AMSI

To enable AMSI, you need to enable script scanning. See [Configure scanning options for Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/configure-advanced-scan-types-microsoft-defender-antivirus).

Also see [Defender Policy CSP - Windows Client Management](https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-defender).

[Section titled: AMSI resources](https://learn.microsoft.com/en-us/defender-endpoint/amsi-on-mdav#amsi-resources)

### AMSI resources

[Anti-malware Scan Interface (AMSI) APIs](https://learn.microsoft.com/en-us/windows/win32/amsi/antimalware-scan-interface-portal) are available for developers and antivirus vendors to implement.

Other Microsoft products such as [Exchange](https://techcommunity.microsoft.com/t5/exchange-team-blog/more-about-amsi-integration-with-exchange-server/ba-p/2572371) and [Sharepoint](https://techcommunity.microsoft.com/t5/microsoft-sharepoint-blog/cyberattack-protection-by-default-and-other-enhancements-to/ba-p/3925641) also use AMSI
integration.

[Section titled: More resources to protect against fileless attacks](https://learn.microsoft.com/en-us/defender-endpoint/amsi-on-mdav#more-resources-to-protect-against-fileless-attacks)

## More resources to protect against fileless attacks

- [Windows Defender Application Control and AppLocker](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/windows-defender-application-control/wdac-and-applocker-overview). Enforces strong code Integrity policies and to allow only trusted applications to run. In the context of fileless malware, WDAC locks down PowerShell to Constrained Language Mode, which limits the extended language features that can lead to unverifiable code execution, such as direct .NET scripting, invocation of Win32 APIs via the Add-Type cmdlet, and interaction with COM objects. This essentially mitigates PowerShell-based reflective DLL injection attacks.

- [Attack surface reduction](https://learn.microsoft.com/en-us/defender-endpoint/overview-attack-surface-reduction) helps admins protect against common attack vectors.

- [Enable virtualization-based protection of code integrity](https://learn.microsoft.com/en-us/windows/security/hardware-security/enable-virtualization-based-protection-of-code-integrity). Mitigates kernel-memory exploits through Hypervisor Code Integrity (HVCI), which makes it difficult to inject malicious code using kernel-mode software vulnerabilities.


**Note:** The author created this article with assistance from AI. [Learn more](https://learn.microsoft.com/principles-for-ai-generated-content)

* * *

## Feedback

Was this page helpful?


YesNoNo

Need help with this topic?


Want to try using Ask Learn to clarify or guide you through this topic?


Ask LearnAsk Learn

Suggest a fix?

* * *

## Additional resources

Training


Module


[Implement Windows security enhancements with Microsoft Defender for Endpoint - Training](https://learn.microsoft.com/en-us/training/modules/implement-windows-10-security-enhancements-with-microsoft-defender-for-endpoint/?source=recommendations)

Implement Windows security enhancements with Microsoft Defender for Endpoint


Certification


[Microsoft Certified: Security Operations Analyst Associate - Certifications](https://learn.microsoft.com/en-us/credentials/certifications/security-operations-analyst/?source=recommendations)

Investigate, search for, and mitigate threats using Microsoft Sentinel, Microsoft Defender for Cloud, and Microsoft 365 Defender.


* * *

- Last updated on 10/20/2025

Ask Learn is an AI assistant that can answer questions, clarify concepts, and define terms using trusted Microsoft documentation.

Please sign in to use Ask Learn.

[Sign in](https://learn.microsoft.com/en-us/defender-endpoint/amsi-on-mdav#)