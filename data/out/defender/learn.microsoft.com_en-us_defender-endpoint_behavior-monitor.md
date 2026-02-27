# https://learn.microsoft.com/en-us/defender-endpoint/behavior-monitor

Table of contents Exit editor mode

Ask LearnAsk LearnFocus mode

Table of contents[Read in English](https://learn.microsoft.com/en-us/defender-endpoint/behavior-monitor)Add to CollectionsAdd to plan[Edit](https://github.com/MicrosoftDocs/defender-docs/blob/public/defender-endpoint/behavior-monitor.md)

* * *

#### Share via

[Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fbehavior-monitor%3FWT.mc_id%3Dfacebook) [x.com](https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fbehavior-monitor%3FWT.mc_id%3Dtwitter&tw_p=tweetbutton&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fbehavior-monitor%3FWT.mc_id%3Dtwitter) [LinkedIn](https://www.linkedin.com/feed/?shareActive=true&text=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fbehavior-monitor%3FWT.mc_id%3Dlinkedin) [Email](mailto:?subject=%5BShared%20Article%5D%20Behavior%20monitoring%20in%20Microsoft%20Defender%20Antivirus%20-%20Microsoft%20Defender%20for%20Endpoint%20%7C%20Microsoft%20Learn&body=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fbehavior-monitor%3FWT.mc_id%3Demail)

* * *

Copy MarkdownPrint

* * *

Note

Access to this page requires authorization. You can try [signing in](https://learn.microsoft.com/en-us/defender-endpoint/behavior-monitor#) or changing directories.


Access to this page requires authorization. You can try changing directories.


# Behavior monitoring in Microsoft Defender Antivirus

- Applies to: Microsoft Defender for Endpoint Plan 1, Microsoft Defender for Endpoint Plan 2, Microsoft Defender for Business, Microsoft Defender for Individuals

Feedback

Summarize this article for me


Behavior monitoring is a critical detection and protection functionality of Microsoft Defender Antivirus.

Monitors process behavior to detect and analyze potential threats based on the behavior of applications, services, and files. Rather than relying solely on signature-based detection (which identifies known malware patterns), behavior monitoring focuses on observing how software behaves in real-time. Here's what it entails:

1. Real-Time Threat Detection:

   - Continuously observe processes, file system activities, and interactions within the system.
   - Defender Antivirus can identify patterns associated with malware or other threats. For example, it looks for processes making unusual changes to existing files, modifying or creating automatic startup registry (ASEP) keys, and other alterations to the file system or structure.
2. Dynamic Approach:


- Unlike static, signature-based detection, behavior monitoring adapts to new and evolving threats.

- Microsoft Defender Antivirus uses predefined patterns, and observes how software behaves during execution. For malware that doesn't fit any predefined pattern, Microsoft Defender Antivirus uses anomaly detection.

- If a program shows suspicious behavior (for example, attempting to modify critical system files), Microsoft Defender Antivirus can take action to prevent further harm, and revert some previous malware actions.


Behavior monitoring enhances Defender Antivirus's ability to proactively detect emerging threats by focusing on real-time actions and behaviors rather than relying solely on known signatures.

The following features depend on behavior monitoring.

**Anti-malware**:

- Indicators, File hash, allow/block

**Network Protection**:

- Indicators, IP address/URL, allow/block
- Web Content Filtering, allow/block

Note

Behavior monitoring is protected by tamper protection.

To temporarily disable behavior monitoring in order to remove it out of the picture, you want to first enable Troubleshooting mode, disable Tamper Protection, and then disable behavior monitoring.

[Section titled: Change the behavior monitoring policy](https://learn.microsoft.com/en-us/defender-endpoint/behavior-monitor#change-the-behavior-monitoring-policy)

## Change the behavior monitoring policy

The following table shows the different ways to configure behavior monitoring.

Expand table

| Management tool | Name | Links |
| --- | --- | --- |
| Security Settings Management | Allow behavior monitoring | This article |
| Intune | Allow behavior monitoring | [Windows Antivirus policy settings for Microsoft Defender Antivirus for Intune](https://learn.microsoft.com/en-us/mem/intune/protect/antivirus-microsoft-defender-settings-windows#real-time-protection) |
| CSP | AllowBehaviorMonitoring | [Defender Policy CSP](https://learn.microsoft.com/en-us/mem/intune/protect/antivirus-microsoft-defender-settings-windows#real-time-protection) |
| Configuration Manager Tenant Attach | Turn on behavior monitoring | [Windows Antivirus policy settings from Microsoft Defender Antivirus for tenant attached devices](https://learn.microsoft.com/en-us/mem/intune/protect/antivirus-microsoft-defender-settings-windows-tenant-attach#real-time-protection) |
| Group Policy | Turn on behavior monitoring | [Download Group Policy Settings Reference Spreadsheet for Windows 11 2023 Update (23H2)](https://www.microsoft.com/download/details.aspx?id=105668) |
| PowerShell | Set-MpPreference -DisableBehaviorMonitoring | [Set-MpPreference](https://learn.microsoft.com/en-us/powershell/module/defender/set-mppreference#-disablebehaviormonitoring) |
| WMI | boolean DisableBehaviorMonitoring; | [MSFT\_MpPreference class](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/defender/msft-mppreference) |

If you use Microsoft Defender for Business, see [Review or edit your next-generation protection policies in Microsoft Defender for Business](https://learn.microsoft.com/en-us/defender-business/mdb-next-generation-protection).

[Section titled: Modify the behavior monitoring settings by using PowerShell](https://learn.microsoft.com/en-us/defender-endpoint/behavior-monitor#modify-the-behavior-monitoring-settings-by-using-powershell)

## Modify the behavior monitoring settings by using PowerShell

Use the following command to modify the behavior monitoring settings:

PowerShell


Copy

```powershell
Set-MpPreference -DisableBehaviorMonitoring <true | false>
```

- `True` disables Behavior monitoring.
- `False` enables Behavior monitoring.

For more information, see [Set-MpPreference](https://learn.microsoft.com/en-us/powershell/module/defender/set-mppreference#-disablebehaviormonitoring).

[Section titled: Query the behavior monitoring status from PowerShell](https://learn.microsoft.com/en-us/defender-endpoint/behavior-monitor#query-the-behavior-monitoring-status-from-powershell)

## Query the behavior monitoring status from PowerShell

PowerShell


Copy

```powershell
Get-MpComputerStatus | Format-Table BehaviorMonitorEnabled
```

If the value returned is `true`, behavior monitoring is enabled.

[Section titled: Query the behavior monitoring status by using Advanced Hunting](https://learn.microsoft.com/en-us/defender-endpoint/behavior-monitor#query-the-behavior-monitoring-status-by-using-advanced-hunting)

## Query the behavior monitoring status by using Advanced Hunting

You can use Advanced Hunting (AH) to query the status of behavior monitoring.

Requires Microsoft Defender XDR, Microsoft Defender for Endpoint Plan 2, or Microsoft Defender for Business.

Kusto


Copy

```kusto
let EvalTable = DeviceTvmSecureConfigurationAssessment
| where ConfigurationId in ("scid-91")
| summarize arg_max(Timestamp,IsCompliant, IsApplicable) by DeviceId, ConfigurationId,tostring(Context)
| extend Test = case(
ConfigurationId == "scid-91" , "BehaviorMonitoring",
"N/A"),
Result = case(IsApplicable == 0,"N/A",IsCompliant == 1 , "Enabled", "Disabled")
| extend packed = pack(Test,Result)
| summarize Tests = make_bag(packed) by DeviceId
| evaluate bag_unpack(Tests);
let DefUpdate = DeviceTvmSecureConfigurationAssessment
| where ConfigurationId == "scid-2011"
// | where isnotnull(Context)
| extend Definition = parse_json(Context[0][0])
| extend LastUpdated = parse_json(Context[0][2])
| project DeviceId,Definition,LastUpdated;
let DeviceInformation = DeviceInfo
| where isnotempty(OSPlatform)
| summarize arg_max(Timestamp,*) by DeviceId, DeviceName
| project DeviceId, DeviceName, MachineGroup;
let withNames = EvalTable
| join kind = inner DeviceInformation on DeviceId
| project-away DeviceId1
| project-reorder DeviceName, MachineGroup;
withNames | join kind = fullouter DefUpdate on DeviceId
| project-away DeviceId1
| sort by BehaviorMonitoring asc
```

[Section titled: Troubleshooting high CPU usage](https://learn.microsoft.com/en-us/defender-endpoint/behavior-monitor#troubleshooting-high-cpu-usage)

## Troubleshooting high CPU usage

Detections related to behavior monitoring start with " [Behavior](https://learn.microsoft.com/en-us/unified-secops-platform/malware-naming#type)".

When investigating high CPU usage in `MsMpEng.exe`, you can temporarily disable behavior monitoring to see if the issues continue.

You can use Performance analyzer for Microsoft Defender Antivirus to find **\\path\\process**, **process** and/or **file extensions** that are contributing to the high cpu utilization. You can then add these items to [Contextual Exclusion](https://learn.microsoft.com/en-us/defender-endpoint/configure-contextual-file-folder-exclusions-microsoft-defender-antivirus).

For more information, see [Performance analyzer for Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/tune-performance-defender-antivirus).

If you're seeing high CPU usage caused by behavior monitoring, continue troubleshooting the issue by reverting each of the following items in order. Re-enable behavior monitoring after reverting each item to identify where the problem might be.

1. **platform update**
2. **engine update**
3. **security intelligence update**.

If you're still encountering high CPU usage issues, contact Microsoft support and have your Client Analyzer data ready.

If behavior monitoring isn't causing the issue, use [Performance analyzer for Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/tune-performance-defender-antivirus) to collect log information. Collect two different logs using `a -c` and `a -a`. Have this information ready when you contact Microsoft support.

For more information, see [Data collection for advanced troubleshooting on Windows](https://learn.microsoft.com/en-us/defender-endpoint/data-collection-analyzer).

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


[Perform device investigations in Microsoft Defender for Endpoint - Training](https://learn.microsoft.com/en-us/training/modules/perform-device-investigations-microsoft-defender-for-endpoints/?source=recommendations)

Perform device investigations in Microsoft Defender for Endpoint


Certification


[Microsoft Certified: Security Operations Analyst Associate - Certifications](https://learn.microsoft.com/en-us/credentials/certifications/security-operations-analyst/?source=recommendations)

Investigate, search for, and mitigate threats using Microsoft Sentinel, Microsoft Defender for Cloud, and Microsoft 365 Defender.


* * *

- Last updated on 09/29/2025

Ask Learn is an AI assistant that can answer questions, clarify concepts, and define terms using trusted Microsoft documentation.

Please sign in to use Ask Learn.

[Sign in](https://learn.microsoft.com/en-us/defender-endpoint/behavior-monitor#)