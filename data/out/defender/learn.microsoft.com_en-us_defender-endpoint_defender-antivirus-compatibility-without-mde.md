# https://learn.microsoft.com/en-us/defender-endpoint/defender-antivirus-compatibility-without-mde

Table of contents Exit editor mode

Ask LearnAsk LearnFocus mode

Table of contents[Read in English](https://learn.microsoft.com/en-us/defender-endpoint/defender-antivirus-compatibility-without-mde)Add to CollectionsAdd to plan[Edit](https://github.com/MicrosoftDocs/defender-docs/blob/public/defender-endpoint/defender-antivirus-compatibility-without-mde.md)

* * *

#### Share via

[Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fdefender-antivirus-compatibility-without-mde%3FWT.mc_id%3Dfacebook) [x.com](https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fdefender-antivirus-compatibility-without-mde%3FWT.mc_id%3Dtwitter&tw_p=tweetbutton&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fdefender-antivirus-compatibility-without-mde%3FWT.mc_id%3Dtwitter) [LinkedIn](https://www.linkedin.com/feed/?shareActive=true&text=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fdefender-antivirus-compatibility-without-mde%3FWT.mc_id%3Dlinkedin) [Email](mailto:?subject=%5BShared%20Article%5D%20Microsoft%20Defender%20Antivirus%20and%20non-Microsoft%20antivirus%2Fantimalware%20solutions%20Antivirus%20protection%20without%20Defender%20for%20Endpoint%20-%20Microsoft%20Defender%20for%20Endpoint%20%7C%20Microsoft%20Learn&body=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fdefender-antivirus-compatibility-without-mde%3FWT.mc_id%3Demail)

* * *

Copy MarkdownPrint

* * *

Note

Access to this page requires authorization. You can try [signing in](https://learn.microsoft.com/en-us/defender-endpoint/defender-antivirus-compatibility-without-mde#) or changing directories.


Access to this page requires authorization. You can try changing directories.


# Microsoft Defender Antivirus and non-Microsoft antivirus solutions without Defender for Endpoint

- Applies to: Microsoft Defender for Endpoint Plan 1, Microsoft Defender for Individuals

Feedback

Summarize this article for me


This section describes what happens when you use Microsoft Defender Antivirus alongside non-Microsoft antivirus/antimalware products on endpoints that aren't onboarded to Defender for Endpoint Plan 2.

Microsoft Defender Antivirus doesn't run in passive mode on devices that aren't onboarded to Defender for Endpoint Plan 2.

The following table summarizes what to expect:

Expand table

| Windows version | Primary antivirus/antimalware solution | Microsoft Defender Antivirus state |
| --- | --- | --- |
| Windows 11 and Windows 10 | Microsoft Defender Antivirus | Active mode |
| Windows 11 and Windows 10 | A non-Microsoft antivirus solution | Disabled mode (happens automatically). |
| Windows server 2016 and later. <br> Windows Server version 1803 or newer. <br> Azure Stack HCI OS, version 23H2 and later. | Microsoft Defender Antivirus | Active mode |
| Windows server 2016 and later. <br> Windows Server version 1803 or newer. <br> Azure Stack HCI OS, version 23H2 and later. | A non-Microsoft antivirus solution | Disabled (set manually; see the note that follows this table) |

Note

Defender for Endpoint support for Windows Server 2025 is rolling out, beginning in February 2025 and over the next several weeks.
On Windows Server, if you're running a non-Microsoft antivirus product, you can uninstall Microsoft Defender Antivirus by using the following PowerShell cmdlet (as an administrator): `Uninstall-WindowsFeature Windows-Defender`. Restart your server to finish removing Microsoft Defender Antivirus. On Windows Server 2016, you might see _Windows Defender Antivirus_ instead of _Microsoft Defender Antivirus_. If you uninstall your non-Microsoft antivirus product, make sure that Microsoft Defender Antivirus is re-enabled. See **[Re-enable Microsoft Defender Antivirus on Windows Server if it was disabled](https://learn.microsoft.com/en-us/defender-endpoint/enable-update-mdav-to-latest-ws)**.

Check the services and filter drivers for Microsoft Defender Antivirus by using the following command:

PowerShell


Copy

```powershell

gsv WinDefend, WdBoot, WdFilter, WdNisSvc, WdNisDrv | ft -auto DisplayName, Name, StartType, Status
```

Expand table

| Display Name | Name | StartType | Status when Microsoft Defender Antivirus is enabled | Status when Microsoft Defender Antivirus is disabled | Comments |
| --- | --- | --- | --- | --- | --- |
| Microsoft Defender Antivirus Boot Driver | `WdBoot` | Boot | Stopped (`0x0 Boot_start`) | Stopped (`0x3 Demand_start`) | It's normal to be stopped after boot. |
| Microsoft Defender Antivirus Mini-Filter Driver | `WdFilter` | Manual | Running (`0x0 Boot_start`) | Stopped (`0x3 Demand_start`) | If a non-Microsoft antivirus solution is installed, expect the status to be stopped. |
| Microsoft Defender Antivirus Network Inspection System Driver | `WdNisDrv` | Manual | Running (`0x3 Demand_start`) | Stopped (`0x3 Demand_start`) | If a non-Microsoft antivirus solution is installed, expect the status to be stopped. |
| Microsoft Defender Antivirus Network Inspection Service | `WdNisSvc` | Manual | Running (`0x3 Demand_start`) | Stopped (`0x3 Demand_start`) | If a non-Microsoft antivirus solution is installed, expect the status to be stopped. |
| Microsoft Defender Antivirus Service | `WinDefend` | Automatic | Running (`0x2 Auto_start`) | Stopped (`0x3 Demand_start`) | If a non-Microsoft antivirus solution is installed, expect the status to be stopped. |

[Section titled: Frequently Asked Questions (FAQ)](https://learn.microsoft.com/en-us/defender-endpoint/defender-antivirus-compatibility-without-mde#frequently-asked-questions-faq)

### Frequently Asked Questions (FAQ)

**Q:** Can I update Microsoft Defender Antivirus components such as "Security intelligence update" or "Engine update" or "Platform update" when Microsoft Defender Antivirus is disabled?

**A:** No. When Microsoft Defender Antivirus is disabled, since the services and drivers aren't running, you won't be able to update the components such as "Security intelligence update" or "Engine update" or "Platform update".

Tip

If you are migrating to Microsoft Defender for Endpoint Plan 2, when onboarded, Microsoft Defender Antivirus goes into passive mode automatically on Windows clients, and can be set to passive mode using a registry key on Windows Server. You can update the different components of Microsoft Defender Antivirus.

**Q:** Can I manually change the start type of the services and drivers for Microsoft Defender Antivirus?

**A:** We don't support the manual modification of the start type of the services and drivers for Microsoft Defender Antivirus in Windows images. On Windows clients, the supported method is by your non-Microsoft antivirus registering in Windows Security Center (WSC) api. Or, on Windows Server, you can uninstall the Microsoft Defender Antivirus feature by using roles and features MMC or by running the following PowerShell command (as an administrator):

Windows Server 2019 and newer

PowerShell


Copy

```powershell

Uninstall-WindowsFeature Windows-Defender
```

Windows Server 2016

PowerShell


Copy

```powershell

Uninstall-WindowsFeature Windows-Defender
Uninstall-WindowsFeature Windows-Defender-Gui
```

**Q:** Can I use Microsoft Defender Antivirus in passive mode without onboarding to Microsoft Defender for Endpoint?

**A:** No. Passive mode is a functionality in Microsoft Defender for Endpoint Plan 1, Microsoft Defender for Endpoint Plan 2 and Microsoft Defender for Business.

**Q:** Can I use [EDR in block mode](https://learn.microsoft.com/en-us/defender-endpoint/edr-in-block-mode) without onboarding to Microsoft Defender for Endpoint?

**A:** No. EDR in block mode is a functionality in Microsoft Defender for Endpoint Plan 2.

**Q:** Can I use indicators, such as file hashes, IP addresses, URLs, or certificates with Microsoft Defender Antivirus (in active mode) with my Microsoft 365 E3/A3 license?

**A:** Yes. See [Tech Community Blog: Microsoft Defender for Endpoint Plan 1 Now Included in Microsoft 365 E3/A3 Licenses](https://techcommunity.microsoft.com/blog/microsoftdefenderatpblog/microsoft-defender-for-endpoint-plan-1-now-included-in-m365-e3a3-licenses/3060639) and [Overview of Microsoft Defender for Endpoint Plan 1](https://learn.microsoft.com/en-us/defender-endpoint/defender-endpoint-plan-1).

[Section titled: See also](https://learn.microsoft.com/en-us/defender-endpoint/defender-antivirus-compatibility-without-mde#see-also)

## See also

- [Use Microsoft Defender for Endpoint Security Settings Management to manage Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/mde-security-settings-management)

- [Microsoft Intune securely manages identities, manages apps, and manages devices](https://learn.microsoft.com/en-us/mem/intune/fundamentals/what-is-intune)

  - [Defender CSP](https://learn.microsoft.com/en-us/windows/client-management/mdm/defender-csp)

  - [Policy CSP - Defender](https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-defender)
- [How to create and deploy antimalware policies for Endpoint Protection in Configuration Manager](https://learn.microsoft.com/en-us/mem/configmgr/protect/deploy-use/endpoint-antimalware-policies)

- [Use Group Policy settings to configure and manage Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/use-group-policy-microsoft-defender-antivirus)

- [Use PowerShell cmdlets to configure and manage Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/use-powershell-cmdlets-microsoft-defender-antivirus)

- [Exclusions overview](https://learn.microsoft.com/en-us/defender-endpoint/navigate-defender-endpoint-antivirus-exclusions)

- [Address false positives/negatives in Microsoft Defender for Endpoint](https://learn.microsoft.com/en-us/defender-endpoint/defender-endpoint-false-positives-negatives)

- [Troubleshoot Microsoft Defender Antivirus settings](https://learn.microsoft.com/en-us/defender-endpoint/troubleshoot-settings)

- [Run the client analyzer on Windows](https://learn.microsoft.com/en-us/defender-endpoint/run-analyzer-windows)

- [Performance analyzer for Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/tune-performance-defender-antivirus)


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


[Implement endpoint protection by using Microsoft Defender for Endpoint - Training](https://learn.microsoft.com/en-us/training/modules/implement-endpoint-protection-use-microsoft-defender-endpoint/?source=recommendations)

This module examines how Microsoft Defender for Endpoint helps enterprise networks prevent, detect, investigate, and respond to advanced threats by using endpoint behavioral sensors, cloud security analytics, and threat intelligence. MS-102


Certification


[Microsoft 365 Certified: Endpoint Administrator Associate - Certifications](https://learn.microsoft.com/en-us/credentials/certifications/modern-desktop/?source=recommendations)

Plan and execute an endpoint deployment strategy, using essential elements of modern management, co-management approaches, and Microsoft Intune integration.


* * *

- Last updated on 01/15/2026

Ask Learn is an AI assistant that can answer questions, clarify concepts, and define terms using trusted Microsoft documentation.

Please sign in to use Ask Learn.

[Sign in](https://learn.microsoft.com/en-us/defender-endpoint/defender-antivirus-compatibility-without-mde#)