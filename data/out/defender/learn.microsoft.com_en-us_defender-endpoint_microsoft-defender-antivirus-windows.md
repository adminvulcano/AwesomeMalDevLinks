# https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows

Table of contents Exit editor mode

Ask LearnAsk LearnFocus mode

Table of contents[Read in English](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows)Add to CollectionsAdd to plan[Edit](https://github.com/MicrosoftDocs/defender-docs/blob/public/defender-endpoint/microsoft-defender-antivirus-windows.md)

* * *

#### Share via

[Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fmicrosoft-defender-antivirus-windows%3FWT.mc_id%3Dfacebook) [x.com](https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fmicrosoft-defender-antivirus-windows%3FWT.mc_id%3Dtwitter&tw_p=tweetbutton&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fmicrosoft-defender-antivirus-windows%3FWT.mc_id%3Dtwitter) [LinkedIn](https://www.linkedin.com/feed/?shareActive=true&text=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fmicrosoft-defender-antivirus-windows%3FWT.mc_id%3Dlinkedin) [Email](mailto:?subject=%5BShared%20Article%5D%20Microsoft%20Defender%20Antivirus%20in%20Windows%20Overview%20-%20Microsoft%20Defender%20for%20Endpoint%20%7C%20Microsoft%20Learn&body=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fmicrosoft-defender-antivirus-windows%3FWT.mc_id%3Demail)

* * *

Copy MarkdownPrint

* * *

Note

Access to this page requires authorization. You can try [signing in](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows#) or changing directories.


Access to this page requires authorization. You can try changing directories.


# Microsoft Defender Antivirus in Windows Overview

- Applies to: Microsoft Defender for Business, Microsoft Defender Antivirus

Feedback

Summarize this article for me


Microsoft Defender Antivirus is available in Windows 10 and Windows 11, and in versions of Windows Server.

Microsoft Defender Antivirus is a major component of your next-generation protection in Microsoft Defender for Endpoint. This protection brings together machine learning, big-data analysis, in-depth threat resistance research, and the Microsoft cloud infrastructure to protect devices (or endpoints) in your organization. Microsoft Defender Antivirus is built into Windows, and it works with Microsoft Defender for Endpoint to provide protection on your device and in the cloud.

Tip

As a companion to this article, see our [Security Analyzer setup guide](https://go.microsoft.com/fwlink/p/?linkid=2268522) to review best practices and learn to fortify defenses, improve compliance, and navigate the cybersecurity landscape with confidence. For a customized experience based on your environment, you can access [the Security Analyzer automated setup guide](https://go.microsoft.com/fwlink/p/?linkid=2268615) in the Microsoft 365 admin center.

[Section titled: Prerequisites](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows#prerequisites)

## Prerequisites

[Section titled: Supported operating systems](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows#supported-operating-systems)

### Supported operating systems

- Windows

[Section titled: Microsoft Defender Antivirus capabilities](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows#microsoft-defender-antivirus-capabilities)

## Microsoft Defender Antivirus capabilities

Microsoft Defender Antivirus provides anomaly detection, a layer of protection for malware that doesn't fit any predefined pattern. Anomaly detection monitors for process creation events or files that are downloaded from the internet. Through machine learning and cloud-delivered protection, Microsoft Defender Antivirus can stay one step ahead of attackers. Anomaly detection is on by default and can help block attacks such as [3CX Security Alert for Electron Windows App](https://www.3cx.com/blog/news/desktopapp-security-alert/). Microsoft Defender Antivirus started blocking this malware four days before the attack was registered in VirusTotal.

Modern malware requires modern solutions. In 2015, Microsoft Defender Antivirus moved away from using a static signature-based engine to a model that uses predictive technologies--such as machine learning, applied science, and artificial intelligence--as this switch is what's necessary to keep you and your organizations safe from the complexity of today's ever-evolving malware landscape.

Microsoft Defender Antivirus can block almost all malware at first sight, in milliseconds.

We designed our antivirus solution to work in both online and offline scenarios. For offline scenarios, the latest dynamic intelligence from the Intelligence Security Graph is provisioned to the endpoint regularly throughout the day. When connected to the cloud, real-time intelligence gets fed from the [Intelligent Security Graph](https://www.microsoft.com/security/blog/2018/04/17/connect-to-the-intelligent-security-graph-using-a-new-api/).

Microsoft Defender Antivirus can also stop threats based on their behaviors and process trees even when the threat has started execution. A common example of these kinds of attacks is fileless malware. Microsoft's Next-generation protection features work together to identify and block malware based on abnormal behavior. To learn more, see [Behavioral blocking and containment](https://learn.microsoft.com/en-us/defender-endpoint/behavioral-blocking-containment).

[Section titled: Compatibility with other antivirus products](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows#compatibility-with-other-antivirus-products)

## Compatibility with other antivirus products

If you're using a non-Microsoft antivirus/anti-malware product on your device, you might be able to run Microsoft Defender Antivirus in passive mode alongside the non-Microsoft antivirus solution. It depends on the operating system used and whether your device is onboarded to Defender for Endpoint. To learn more, see [Microsoft Defender Antivirus compatibility](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-compatibility).

[Section titled: Microsoft Defender Antivirus processes and services](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows#microsoft-defender-antivirus-processes-and-services)

## Microsoft Defender Antivirus processes and services

The following table summarizes Microsoft Defender Antivirus processes and services. You can view them in Task Manager in Windows.

Expand table

| Process or service | Where to view its status |
| --- | --- |
| **Microsoft Defender Antivirus Core service**<br>(`MdCoreSvc`) | \- **Processes** tab: `Antimalware Core Service`<br>\- **Details** tab: `MpDefenderCoreService.exe`<br>\- **Services** tab: `Microsoft Defender Core Service` |
| **Microsoft Defender Antivirus service**<br>(`WinDefend`) | \- **Processes** tab: `Antimalware Service Executable`<br>\- **Details** tab: `MsMpEng.exe`<br>\- **Services** tab: `Microsoft Defender Antivirus` |
| **Microsoft Defender Antivirus Network Realtime Inspection service**<br>(`WdNisSvc`) | \- **Processes** tab: `Microsoft Network Realtime Inspection Service`<br>\- **Details** tab: `NisSrv.exe`<br>\- **Services** tab: `Microsoft Defender Antivirus Network Inspection Service` |
| **Microsoft Defender Antivirus command-line utility** | \- **Processes** tab: N/A <br>\- **Details** tab: `MpCmdRun.exe`<br>\- **Services** tab: N/A |
| **Microsoft Security Client Policy Configuration Tool** | \- **Processes** tab: N/A <br>\- **Details** tab: `ConfigSecurityPolicy.exe`<br>\- **Services** tab: N/A |

To learn more about the Microsoft Defender Core service, visit [Microsoft Defender Core service overview](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-core-service-overview).

For [Microsoft Endpoint Data Loss Prevention](https://learn.microsoft.com/en-us/purview/endpoint-dlp-getting-started) (Endpoint DLP), the following table summarizes processes and services. You can view them in Task Manager in Windows.

Expand table

| Process or service | Where to view its status |
| --- | --- |
| **Microsoft Endpoint DLP service**<br>(`MDDlpSvc`) | \- **Processes** tab: `MpDlpService.exe`<br>\- **Details** tab: `MpDlpService.exe`<br>\- **Services** tab: `Microsoft Data Loss Prevention Service` |
| **Microsoft Endpoint DLP command-line utility** | \- **Processes** tab: N/A <br>\- **Details** tab: `MpDlpCmd.exe`<br>\- **Services** tab: N/A |

[Section titled: Comparing active mode, passive mode, and disabled mode](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows#comparing-active-mode-passive-mode-and-disabled-mode)

## Comparing active mode, passive mode, and disabled mode

The following table describes what to expect when Microsoft Defender Antivirus is in active mode, passive mode, or disabled.

Expand table

| Mode | What happens |
| --- | --- |
| Active mode | In active mode, Microsoft Defender Antivirus is used as the primary antivirus app on the device. Files are scanned, threats are remediated, and detected threats are listed in your organization's security reports and in your Windows Security app. |
| Passive mode | In passive mode, Microsoft Defender Antivirus isn't used as the primary antivirus app on the device. Files are scanned, and detected threats are reported, but threats aren't remediated by Microsoft Defender Antivirus. <br>**IMPORTANT**: Microsoft Defender Antivirus can run in passive mode only on endpoints that are onboarded to Microsoft Defender for Endpoint. See [Requirements for Microsoft Defender Antivirus to run in passive mode](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-compatibility#requirements-for-microsoft-defender-antivirus-to-run-in-passive-mode). |
| Disabled or uninstalled | When disabled or uninstalled, Microsoft Defender Antivirus isn't used. Files aren't scanned, and threats aren't remediated. In general, we don't recommend disabling or uninstalling Microsoft Defender Antivirus. |

To learn more, see [Microsoft Defender Antivirus compatibility](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-compatibility).

[Section titled: Check the state of Microsoft Defender Antivirus on your device](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows#check-the-state-of-microsoft-defender-antivirus-on-your-device)

## Check the state of Microsoft Defender Antivirus on your device

You can use one of several methods, such as the Windows Security app or Windows PowerShell, to check the state of Microsoft Defender Antivirus on your device.

Important

Beginning with [platform version 4.18.2208.0 and later](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint-releases#microsoft-defender-antivirus-releases): If a server has been onboarded to Microsoft Defender for Endpoint, the "Turn off Windows Defender" [group policy](https://learn.microsoft.com/en-us/defender-endpoint/configure-endpoints-gp#update-endpoint-protection-configuration) setting will no longer completely disable Windows Defender Antivirus on Windows Server 2012 R2 and later. Instead, it will place it into passive mode. In addition, the [tamper protection](https://learn.microsoft.com/en-us/defender-endpoint/prevent-changes-to-security-settings-with-tamper-protection) feature will allow a switch to active mode but not to passive mode.

- If "Turn off Windows Defender" is already in place before onboarding to Microsoft Defender for Endpoint, there will be no change and Defender Antivirus will remain disabled.
- To switch Defender Antivirus to passive mode, even if it was disabled before onboarding, you can apply the [ForceDefenderPassiveMode configuration](https://learn.microsoft.com/en-us/defender-endpoint/switch-to-mde-phase-2#manually-set-microsoft-defender-antivirus-to-passive-mode-on-windows-server) with a value of `1`. To place it into active mode, switch this value to `0` instead.

Note the modified logic for `ForceDefenderPassiveMode` when tamper protection is enabled: Once Microsoft Defender Antivirus is toggled to active mode, tamper protection will prevent it from going back into passive mode even when `ForceDefenderPassiveMode` is set to `1`.

[Section titled: Use the Windows Security app to check the status of Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows#use-the-windows-security-app-to-check-the-status-of-microsoft-defender-antivirus)

### Use the Windows Security app to check the status of Microsoft Defender Antivirus

1. On your Windows device, select the **Start** menu, and begin typing `Security`. Then open the Windows Security app in the results.

2. Select **Virus & threat protection**.

3. Under **Who's protecting me?**, choose **Manage Providers**.


You'll see the name of your antivirus/anti-malware solution on the security providers page.

[Section titled: Use PowerShell to check the status of Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows#use-powershell-to-check-the-status-of-microsoft-defender-antivirus)

### Use PowerShell to check the status of Microsoft Defender Antivirus

1. Select the **Start** menu, and begin typing `PowerShell`. Then open Windows PowerShell in the results.

2. Type `Get-MpComputerStatus`.

3. In the list of results, look at the **AMRunningMode** row.

   - **Normal** means Microsoft Defender Antivirus is running in active mode.

   - **Passive mode** means Microsoft Defender Antivirus running, but isn't the primary antivirus/anti-malware product on your device. Passive mode is only available for devices that are onboarded to Microsoft Defender for Endpoint and that meet certain requirements. To learn more, see [Requirements for Microsoft Defender Antivirus to run in passive mode](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-compatibility#requirements-for-microsoft-defender-antivirus-to-run-in-passive-mode).

   - **EDR Block Mode** means Microsoft Defender Antivirus is running and [Endpoint detection and response (EDR) in block mode](https://learn.microsoft.com/en-us/defender-endpoint/edr-in-block-mode), a capability in Microsoft Defender for Endpoint, is enabled. Check the **ForceDefenderPassiveMode** registry key. If its value is 0, it's running in normal mode; otherwise, it's running in passive mode.

   - **SxS Passive Mode** means Microsoft Defender Antivirus is running alongside another antivirus/anti-malware product, and [limited periodic scanning is used](https://learn.microsoft.com/en-us/defender-endpoint/limited-periodic-scanning-microsoft-defender-antivirus).

Tip

To learn more about the Get-MpComputerStatus PowerShell cmdlet, see the reference article [Get-MpComputerStatus](https://learn.microsoft.com/en-us/powershell/module/defender/get-mpcomputerstatus).

Tip

**Performance tip** Due to a variety of factors (examples listed below) Microsoft Defender Antivirus, like other antivirus software, can cause performance issues on endpoint devices. In some cases, you might need to tune the performance of Microsoft Defender Antivirus to alleviate those performance issues. Microsoft's **Performance analyzer** is a PowerShell command-line tool that helps determine which files, file paths, processes, and file extensions might be causing performance issues; some examples are:

- Top paths that impact scan time
- Top files that impact scan time
- Top processes that impact scan time
- Top file extensions that impact scan time
- Combinations – for example:
  - top files per extension
  - top paths per extension
  - top processes per path
  - top scans per file
  - top scans per file per process

You can use the information gathered using Performance analyzer to better assess performance issues and apply remediation actions.
See: [Performance analyzer for Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/tune-performance-defender-antivirus).

[Section titled: Get your antivirus/anti-malware platform updates](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows#get-your-antivirusanti-malware-platform-updates)

## Get your antivirus/anti-malware platform updates

It's important to keep Microsoft Defender Antivirus (or any antivirus/anti-malware solution) up to date. Microsoft releases regular updates to help ensure that your devices have the latest technology to protect against new malware and attack techniques. To learn more, see [Manage Microsoft Defender Antivirus updates and apply baselines](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-updates).

Tip

If you're looking for Antivirus related information for other platforms, see:

- [Set preferences for Microsoft Defender for Endpoint on macOS](https://learn.microsoft.com/en-us/defender-endpoint/mac-preferences)
- [Microsoft Defender for Endpoint on Mac](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint-mac)
- [macOS Antivirus policy settings for Microsoft Defender Antivirus for Intune](https://learn.microsoft.com/en-us/mem/intune/protect/antivirus-microsoft-defender-settings-macos)
- [Set preferences for Microsoft Defender for Endpoint on Linux](https://learn.microsoft.com/en-us/defender-endpoint/linux-preferences)
- [Microsoft Defender for Endpoint on Linux](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint-linux)
- [Configure Defender for Endpoint on Android features](https://learn.microsoft.com/en-us/defender-endpoint/android-configure)
- [Configure Microsoft Defender for Endpoint on iOS features](https://learn.microsoft.com/en-us/defender-endpoint/ios-configure-features)

Note

After installing the latest Microsoft Defender Antivirus platform or engine update, certain registry entries may not update automatically. To ensure the registry reflects the current version, administrators should manually verify and update the relevant keys using **Registry Editor (regedit)** or a supported deployment script.

[Section titled: See also](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows#see-also)

## See also

- [Performance analyzer for Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/tune-performance-defender-antivirus)
- [Microsoft Defender Antivirus management and configuration](https://learn.microsoft.com/en-us/defender-endpoint/configuration-management-reference-microsoft-defender-antivirus)
- [Evaluate Microsoft Defender Antivirus protection](https://learn.microsoft.com/en-us/defender-endpoint/evaluate-microsoft-defender-antivirus)
- [Exclusions for Microsoft Defender for Endpoint and Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/defender-endpoint-antivirus-exclusions)

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


[MD-102 3-Manage Microsoft Defender in Windows client - Training](https://learn.microsoft.com/en-us/training/modules/manage-defender-windows-client/?source=recommendations)

This module explains the built-in security features of Windows clients and how to implement them using policies.


Certification


[Microsoft 365 Certified: Endpoint Administrator Associate - Certifications](https://learn.microsoft.com/en-us/credentials/certifications/modern-desktop/?source=recommendations)

Plan and execute an endpoint deployment strategy, using essential elements of modern management, co-management approaches, and Microsoft Intune integration.


* * *

- Last updated on 10/20/2025

Ask Learn is an AI assistant that can answer questions, clarify concepts, and define terms using trusted Microsoft documentation.

Please sign in to use Ask Learn.

[Sign in](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows#)