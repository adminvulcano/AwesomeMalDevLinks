# https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus

Table of contents Exit editor mode

Ask LearnAsk LearnFocus mode

Table of contents[Read in English](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus)Add to CollectionsAdd to plan[Edit](https://github.com/MicrosoftDocs/defender-docs/blob/public/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus.md)

* * *

#### Share via

[Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fenable-cloud-protection-microsoft-defender-antivirus%3FWT.mc_id%3Dfacebook) [x.com](https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fenable-cloud-protection-microsoft-defender-antivirus%3FWT.mc_id%3Dtwitter&tw_p=tweetbutton&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fenable-cloud-protection-microsoft-defender-antivirus%3FWT.mc_id%3Dtwitter) [LinkedIn](https://www.linkedin.com/feed/?shareActive=true&text=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fenable-cloud-protection-microsoft-defender-antivirus%3FWT.mc_id%3Dlinkedin) [Email](mailto:?subject=%5BShared%20Article%5D%20Turn%20on%20cloud%20protection%20in%20Microsoft%20Defender%20Antivirus%20-%20Microsoft%20Defender%20for%20Endpoint%20%7C%20Microsoft%20Learn&body=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fenable-cloud-protection-microsoft-defender-antivirus%3FWT.mc_id%3Demail)

* * *

Copy MarkdownPrint

* * *

Note

Access to this page requires authorization. You can try [signing in](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#) or changing directories.


Access to this page requires authorization. You can try changing directories.


# Turn on cloud protection in Microsoft Defender Antivirus

- Applies to: Microsoft Defender for Endpoint Plan 1, Microsoft Defender for Endpoint Plan 2, Microsoft Defender Antivirus

Feedback

Summarize this article for me


[Cloud protection in Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-defender-antivirus) delivers accurate, real-time, and intelligent protection. Cloud protection should be enabled by default.

Note

[Tamper protection](https://learn.microsoft.com/en-us/defender-endpoint/prevent-changes-to-security-settings-with-tamper-protection) helps keep cloud protection and other security settings from being changed. As a result, when tamper protection is enabled, any changes made to [tamper-protected settings](https://learn.microsoft.com/en-us/defender-endpoint/prevent-changes-to-security-settings-with-tamper-protection#what-happens-when-tamper-protection-is-turned-on) are ignored. If you must make changes to a device and those changes are blocked by tamper protection, we recommend using [troubleshooting mode](https://learn.microsoft.com/en-us/defender-endpoint/enable-troubleshooting-mode) to temporarily disable tamper protection on the device. Note that after troubleshooting mode ends, any changes made to tamper-protected settings are reverted to their configured state.

[Section titled: Prerequistes](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#prerequistes)

## Prerequistes

[Section titled: Supported operating systems](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#supported-operating-systems)

### Supported operating systems

- Windows

[Section titled: Why cloud protection should be turned on](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#why-cloud-protection-should-be-turned-on)

## Why cloud protection should be turned on

Microsoft Defender Antivirus cloud protection helps protect against malware on your endpoints and across your network. We recommend keeping cloud protection turned on, because certain security features and capabilities in Microsoft Defender for Endpoint only work when cloud protection is enabled.

[![alt-text="Diagram showing things that depend on cloud protection](https://learn.microsoft.com/en-us/defender-endpoint/media/mde-cloud-protection.png#lightbox)](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus)

The following table summarizes the features and capabilities that depend on cloud protection:

Expand table

| Feature/Capability | Subscription requirement | Description |
| --- | --- | --- |
| **Checking against metadata in the cloud**. The Microsoft Defender Antivirus cloud service uses machine learning models as an extra layer of defense. These machine learning models include metadata, so when a suspicious or malicious file is detected, its metadata is checked. <br>To learn more, see [Blog: Get to know the advanced technologies at the core of Microsoft Defender for Endpoint next-generation protection](https://www.microsoft.com/security/blog/2019/06/24/inside-out-get-to-know-the-advanced-technologies-at-the-core-of-microsoft-defender-atp-next-generation-protection/) | Microsoft Defender for Endpoint Plan 1 or Plan 2 (Standalone or included in a plan like Microsoft 365 E3 or E5) |  |
| **[Cloud protection and sample submission](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission)**. Files and executables can be sent to the Microsoft Defender Antivirus cloud service for detonation and analysis. Automatic sample submission relies on cloud protection, although it can also be configured as a standalone setting.<br>To learn more, see [Cloud protection and sample submission in Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission). | Microsoft Defender for Endpoint Plan 1 or Plan 2 (Standalone or included in a plan like Microsoft 365 E3 or E5) |  |
| **[Tamper protection](https://learn.microsoft.com/en-us/defender-endpoint/prevent-changes-to-security-settings-with-tamper-protection)**. Tamper protection helps protect against unwanted changes to your organization's security settings. <br>To learn more, see [Protect security settings with tamper protection](https://learn.microsoft.com/en-us/defender-endpoint/prevent-changes-to-security-settings-with-tamper-protection). | Microsoft Defender for Endpoint Plan 2 (Standalone or included in a plan like Microsoft 365 E5) |  |
| **[Block at first sight](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus)**<br>Block at first sight detects new malware and blocks it within seconds. When a suspicious or malicious file is detected, block at first sight capabilities queries the cloud protection backend and applies heuristics, machine learning, and automated analysis of the file to determine whether it's a threat.<br>To learn more, see [What is "block at first sight"?](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#what-is-block-at-first-sight) | Microsoft Defender for Endpoint Plan 1 or Plan 2 (Standalone or included in a plan like Microsoft 365 E3 or E5) |  |
| **[Emergency signature updates](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-updates#security-intelligence-updates)**. When malicious content is detected, emergency signature updates and fixes are deployed. Rather than wait for the next regular update, you can receive these fixes and updates within minutes. <br>To learn more about updates, see [Microsoft Defender Antivirus security intelligence and product updates](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-updates). | Microsoft Defender for Endpoint Plan 2 (Standalone or included in a plan like Microsoft 365 E5) |  |
| **[Endpoint detection and response (EDR) in block mode](https://learn.microsoft.com/en-us/defender-endpoint/edr-in-block-mode)**. EDR in block mode provides extra protection when Microsoft Defender Antivirus isn't the primary antivirus product on a device. EDR in block mode remediates artifacts found during EDR-generated scans that the non-Microsoft, primary antivirus solution might have missed. When enabled for devices with Microsoft Defender Antivirus as the primary antivirus solution, EDR in block mode provides the added benefit of automatically remediating artifacts identified during EDR-generated scans. <br>To learn more, see [EDR in block mode](https://learn.microsoft.com/en-us/defender-endpoint/edr-in-block-mode). | Microsoft Defender for Endpoint Plan 2 (Standalone or included in a plan like Microsoft 365 E5) |  |
| **[Attack surface reduction rules](https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction)**. ASR rules are intelligent rules that you can configure to help stop malware. Certain rules require cloud protection to be turned on in order to function fully. These rules include: <br>\- Block executable files from running unless they meet a prevalence, age, or trusted list criteria <br>\- Use advanced protection against ransomware <br>\- Block untrusted programs from running from removable drives <br>To learn more, see [Use attack surface reduction rules to prevent malware infection](https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction). | Microsoft Defender for Endpoint Plan 1 or Plan 2 (Standalone or included in a plan like Microsoft 365 E3 or E5) |  |
| **[Indicators of compromise (IoCs)](https://learn.microsoft.com/en-us/defender-endpoint/indicators-overview)**. In Defender for Endpoint, IoCs can be configured to define the detection, prevention, and exclusion of entities. Examples: <br>"Allow" indicators can be used to define exceptions to antivirus scans and remediation actions.<br>"Alert and block" indicators can be used to prevent files or processes from executing. <br>To learn more, see [Create indicators](https://learn.microsoft.com/en-us/defender-endpoint/indicators-overview). | Microsoft Defender for Endpoint Plan 2 (Standalone or included in a plan like Microsoft 365 E5) |  |

[Section titled: Methods to configure cloud protection](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#methods-to-configure-cloud-protection)

## Methods to configure cloud protection

You can turn Microsoft Defender Antivirus cloud protection on or off by using one of several methods, such as:

- [Turn on cloud protection in Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#turn-on-cloud-protection-in-microsoft-defender-antivirus)
  - [Why cloud protection should be turned on](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#why-cloud-protection-should-be-turned-on)
  - [Methods to configure cloud protection](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#methods-to-configure-cloud-protection)
  - [Use Microsoft Intune to turn on cloud protection](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#use-microsoft-intune-to-turn-on-cloud-protection)
  - [Use Group Policy to turn on cloud protection](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#use-group-policy-to-turn-on-cloud-protection)
  - [Use PowerShell cmdlets to turn on cloud protection](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#use-powershell-cmdlets-to-turn-on-cloud-protection)
  - [Use Windows Management Instrumentation (WMI) to turn on cloud protection](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#use-windows-management-instruction-wmi-to-turn-on-cloud-protection)
  - [Turn on cloud protection on individual clients with the Windows Security app](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#turn-on-cloud-protection-on-individual-clients-with-the-windows-security-app)
  - [See also](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#see-also)

You can also use [Configuration Manager](https://learn.microsoft.com/en-us/mem/configmgr/protect/deploy-use/defender-advanced-threat-protection). And, you can turn cloud protection on or off on individual endpoints by using the [Windows Security app](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#turn-on-cloud-protection-on-individual-clients-with-the-windows-security-app).

For more information about the specific network-connectivity requirements to ensure your endpoints can connect to the cloud protection service, see [Configure and validate network connections](https://learn.microsoft.com/en-us/defender-endpoint/configure-network-connections-microsoft-defender-antivirus).

Note

In Windows 10 and Windows 11, there is no difference between the **Basic** and **Advanced** reporting options described in this article. This is a legacy distinction and choosing either setting results in the same level of cloud protection. There is no difference in the type or amount of information that is shared. For more information on what we collect, see the [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?linkid=521839).

[Section titled: Use Microsoft Intune to turn on cloud protection](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#use-microsoft-intune-to-turn-on-cloud-protection)

## Use Microsoft Intune to turn on cloud protection

1. Go to the Intune admin center ( [https://intune.microsoft.com](https://intune.microsoft.com/)) and sign in.

2. Choose **Endpoint security** \> **Antivirus**.

3. In the **AV policies** section, either select an existing policy, or choose **\+ Create Policy**.

Expand table




| Task | Steps |
| --- | --- |
| Create a new policy | 1\. For **Platform**, select **Windows**. <br>2\. For **Profile**, select **Microsoft Defender Antivirus**.<br>3\. On the **Basics** page, specify a name and description for the policy, and then choose **Next**.<br>4\. In the **Defender** section, find **Allow Cloud Protection**, and set it to **Allowed**.<br>5\. Scroll down to **Submit Samples Consent**, and select one of the following settings:<br>\- **Send all samples automatically**<br>\- **Send safe samples automatically**<br>6\. On the **Scope tags** step, if your organization is using [scope tags](https://learn.microsoft.com/en-us/mem/intune/fundamentals/scope-tags), select the tags you want to use, and then choose **Next**.<br>7\. On the **Assignments** step, select the groups, users, or devices that you want to apply this policy to, and then choose **Next**.<br>8\. On the **Review + create** step, review the settings for your policy, and then choose **Create**. |
| Edit an existing policy | 1\. Select the policy that you want to edit.<br>2\. Under **Configuration settings**, choose **Edit**.<br>3\. In the **Defender** section, find **Allow Cloud Protection**, and set it to **Allowed**.<br>4\. Scroll down to **Submit Samples Consent**, and select one of the following settings:<br>\- **Send all samples automatically**<br>\- **Send safe samples automatically**<br>5\. Select **Review + save**. |


Tip

To learn more about Microsoft Defender Antivirus settings in Intune, see [Antivirus policy for endpoint security in Intune](https://learn.microsoft.com/en-us/mem/intune/protect/endpoint-security-antivirus-policy).

[Section titled: Use Group Policy to turn on cloud protection](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#use-group-policy-to-turn-on-cloud-protection)

## Use Group Policy to turn on cloud protection

1. On your Group Policy management device, open the [Group Policy Management Console](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc731212(v=ws.11)), right-click the Group Policy Object you want to configure and select **Edit**.

2. In the **Group Policy Management Editor**, go to **Computer configuration**.

3. Select **Administrative templates**.

4. Expand the tree to **Windows components** \> **Microsoft Defender Antivirus > MAPS**



Note



MAPS settings are equal to cloud-delivered protection.

5. Double-click **Join Microsoft MAPS**. Ensure the option is turned on and set to **Basic MAPS** or **Advanced MAPS**. Select **OK**.

You can choose to send basic or additional information about detected software:

   - Basic MAPS: Basic membership sends basic information to Microsoft about malware and potentially unwanted software that has been detected on your device. Information includes where the software came from (like URLs and partial paths), the actions taken to resolve the threat, and whether the actions were successful.

   - Advanced MAPS: In addition to basic information, advanced membership sends detailed information about malware and potentially unwanted software, including the full path to the software, and detailed information about how the software has affected your device.
6. Double-click **Send file samples when further analysis is required**. Ensure that the first option is set to **Enabled** and that the other options are set to either:


   - **Send safe samples** (1)
   - **Send all samples** (3)

Note

The **Send safe samples** (1) option means that most samples are sent automatically. Files that are likely to contain personal information prompt the user for additional confirmation.
Setting the option to **Always Prompt** (0) lowers the protection state of the device. Setting it to **Never send** (2) means that the [Block at First Sight](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus) feature of Microsoft Defender for Endpoint won't work.

7. Select **OK**.


[Section titled: Use PowerShell cmdlets to turn on cloud protection](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#use-powershell-cmdlets-to-turn-on-cloud-protection)

## Use PowerShell cmdlets to turn on cloud protection

The following cmdlets can turn on cloud protection:

PowerShell


Copy

```powershell
Set-MpPreference -MAPSReporting Advanced
Set-MpPreference -SubmitSamplesConsent SendAllSamples
```

For more information on how to use PowerShell with Microsoft Defender Antivirus, see [Use PowerShell cmdlets to configure and run Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/use-powershell-cmdlets-microsoft-defender-antivirus) and [Microsoft Defender Antivirus cmdlets](https://learn.microsoft.com/en-us/powershell/module/defender/). [Policy CSP - Defender](https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-defender) also has more information specifically on [-SubmitSamplesConsent](https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-defender#defender-submitsamplesconsent).

Important

You can set **-SubmitSamplesConsent** to `SendSafeSamples` (the default, recommended setting), `NeverSend`, or `AlwaysPrompt`.
The `SendSafeSamples` setting means that most samples are sent automatically. Files that are likely to contain personal information result in a prompt for the user to continue, and require confirmation.
The `NeverSend` and `AlwaysPrompt` settings lower the protection level of the device. Furthermore, the `NeverSend` setting means that the [Block at First Sight](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus) feature of Microsoft Defender for Endpoint won't work.

[Section titled: Use Windows Management Instrumentation (WMI) to turn on cloud protection](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#use-windows-management-instrumentation-wmi-to-turn-on-cloud-protection)

## Use Windows Management Instrumentation (WMI) to turn on cloud protection

Use the [**Set** method of the **MSFT\_MpPreference**](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/defender/set-msft-mppreference) class for the following properties:

WMI


Copy

```wmi
MAPSReporting
SubmitSamplesConsent
```

For more information about allowed parameters, see [Windows Defender WMIv2 APIs](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/defender/windows-defender-wmiv2-apis-portal).

[Section titled: Turn on cloud protection on individual clients with the Windows Security app](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#turn-on-cloud-protection-on-individual-clients-with-the-windows-security-app)

## Turn on cloud protection on individual clients with the Windows Security app

Note

If the **Configure local setting override for reporting Microsoft MAPS** Group Policy setting is set to **Disabled**, then the **Cloud-based protection** setting in Windows Settings are greyed out and unavailable. Changes made through a Group Policy Object must first be deployed to individual endpoints before the setting is updated in Windows Settings.

1. Open the Windows Security app by selecting the shield icon in the task bar, or by searching the start menu for **Windows Security**.

2. Select the **Virus & threat protection** tile (or the shield icon on the left menu bar), and then, under **Virus & threat protection settings**, select **Manage settings**.

[![The Virus & threat protection settings](https://learn.microsoft.com/en-us/defender/media/wdav-protection-settings-wdsc.png)](https://learn.microsoft.com/en-us/defender/media/wdav-protection-settings-wdsc.png#lightbox)

3. Confirm that **Cloud-based Protection** and **Automatic sample submission** are switched to **On**.



Note



If automatic sample submission has been configured with Group Policy, then the setting is greyed out and unavailable.


[Section titled: See also](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#see-also)

## See also

- [Use Microsoft cloud protection in Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-defender-antivirus)

- [Configuration Manager: Microsoft Defender for Endpoint](https://learn.microsoft.com/en-us/mem/configmgr/protect/deploy-use/defender-advanced-threat-protection)

- [Use PowerShell cmdlets to manage Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/use-powershell-cmdlets-microsoft-defender-antivirus)


Tip

If you're looking for Antivirus related information for other platforms, see:

- [Set preferences for Microsoft Defender for Endpoint on macOS](https://learn.microsoft.com/en-us/defender-endpoint/mac-preferences)
- [Microsoft Defender for Endpoint on Mac](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint-mac)
- [macOS Antivirus policy settings for Microsoft Defender Antivirus for Intune](https://learn.microsoft.com/en-us/mem/intune/protect/antivirus-microsoft-defender-settings-macos)
- [Set preferences for Microsoft Defender for Endpoint on Linux](https://learn.microsoft.com/en-us/defender-endpoint/linux-preferences)
- [Microsoft Defender for Endpoint on Linux](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint-linux)
- [Configure Defender for Endpoint on Android features](https://learn.microsoft.com/en-us/defender-endpoint/android-configure)
- [Configure Microsoft Defender for Endpoint on iOS features](https://learn.microsoft.com/en-us/defender-endpoint/ios-configure-features)

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


[Set up Microsoft Defender for Cloud - Training](https://learn.microsoft.com/en-us/training/modules/set-up-microsoft-defender-cloud/?source=recommendations)

Discover how to leverage Microsoft Defender for Cloud through the Azure portal to ensure the security of your Azure services and workloads, offering continuous threat detection and prevention.


* * *

- Last updated on 10/20/2025

Ask Learn is an AI assistant that can answer questions, clarify concepts, and define terms using trusted Microsoft documentation.

Please sign in to use Ask Learn.

[Sign in](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus#)