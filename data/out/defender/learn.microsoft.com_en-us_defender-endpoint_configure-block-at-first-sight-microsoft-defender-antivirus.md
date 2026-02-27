# https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus

Table of contents Exit editor mode

Ask LearnAsk LearnFocus mode

Table of contents[Read in English](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus)Add to CollectionsAdd to plan[Edit](https://github.com/MicrosoftDocs/defender-docs/blob/public/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus.md)

* * *

#### Share via

[Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fconfigure-block-at-first-sight-microsoft-defender-antivirus%3FWT.mc_id%3Dfacebook) [x.com](https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fconfigure-block-at-first-sight-microsoft-defender-antivirus%3FWT.mc_id%3Dtwitter&tw_p=tweetbutton&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fconfigure-block-at-first-sight-microsoft-defender-antivirus%3FWT.mc_id%3Dtwitter) [LinkedIn](https://www.linkedin.com/feed/?shareActive=true&text=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fconfigure-block-at-first-sight-microsoft-defender-antivirus%3FWT.mc_id%3Dlinkedin) [Email](mailto:?subject=%5BShared%20Article%5D%20Enable%20block%20at%20first%20sight%20to%20detect%20malware%20in%20seconds%20-%20Microsoft%20Defender%20for%20Endpoint%20%7C%20Microsoft%20Learn&body=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fconfigure-block-at-first-sight-microsoft-defender-antivirus%3FWT.mc_id%3Demail)

* * *

Copy MarkdownPrint

* * *

Note

Access to this page requires authorization. You can try [signing in](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#) or changing directories.


Access to this page requires authorization. You can try changing directories.


# Turn on block at first sight

- Applies to: Microsoft Defender for Endpoint Plan 1, Microsoft Defender for Endpoint Plan 2

Feedback

Summarize this article for me


This article describes an antivirus/antimalware feature known as "block at first sight", and describes how to enable block at first sight for your organization.

Tip

This article is intended for enterprise admins and IT Pros who manage security settings for organizations. If you aren't an enterprise admin or IT Pro but you have questions about block at first sight, see the [Not an enterprise admin or IT Pro?](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#not-an-enterprise-admin-or-it-pro) section.

[Section titled: Prerequisites](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#prerequisites)

## Prerequisites

[Section titled: Supported operating systems](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#supported-operating-systems)

### Supported operating systems

- Windows

[Section titled: What is "block at first sight"?](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#what-is-block-at-first-sight)

## What is "block at first sight"?

Block at first sight is a threat protection feature of next-generation protection that detects new malware and blocks it within seconds. Block at first sight is enabled when certain security settings are enabled:

- [Cloud protection](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-defender-antivirus) is turned on;
- [Sample submission](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission) is configured for samples to be sent automatically; and
- [Microsoft Defender Antivirus is up to date](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-updates) on devices.

In most enterprise organizations, the settings needed to enable block at first sight are configured with Microsoft Defender Antivirus deployments. See [Turn on cloud protection in Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus).

[Section titled: How it works](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#how-it-works)

## How it works

When Microsoft Defender Antivirus encounters a suspicious but undetected file, it queries our cloud protection backend. The cloud backend applies heuristics, machine learning, and automated analysis of the file to determine whether the files are malicious or not a threat.

Microsoft Defender Antivirus uses multiple detection and prevention technologies to deliver accurate, intelligent, and real-time protection.

[![The list of Microsoft Defender Antivirus engines](https://learn.microsoft.com/en-us/defender-endpoint/media/microsoft-defender-atp-next-generation-protection-engines.png)](https://learn.microsoft.com/en-us/defender-endpoint/media/microsoft-defender-atp-next-generation-protection-engines.png#lightbox)

Tip

To learn more, see [(Blog) Get to know the advanced technologies at the core of Microsoft Defender for Endpoint next-generation protection](https://www.microsoft.com/security/blog/2019/06/24/inside-out-get-to-know-the-advanced-technologies-at-the-core-of-microsoft-defender-atp-next-generation-protection/).

[Section titled: A few things to know about block at first sight](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#a-few-things-to-know-about-block-at-first-sight)

## A few things to know about block at first sight

- Block at first sight can block nonportable executable files (such as JS, VBS, or macros) and executable files, running the [latest Defender antimalware platform](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-updates) on Windows or Windows Server.

- Block at first sight only uses the cloud protection backend for executable files and nonportable executable files that are downloaded from the Internet, or that originate from the Internet zone. A hash value of the `.exe` file is checked via the cloud backend to determine if the file is a previously undetected file.

- If the cloud backend is unable to make a determination, Microsoft Defender Antivirus locks the file and uploads a copy to the cloud. The cloud performs more analysis to reach a determination before it either allows the file to run or blocks it in all future encounters, depending on whether it determines the file to be malicious or not a threat.

- In many cases, this process can reduce the response time for new malware from hours to seconds.

- You can [specify how long a file should be prevented from running](https://learn.microsoft.com/en-us/defender-endpoint/configure-cloud-block-timeout-period-microsoft-defender-antivirus) while the cloud-based protection service analyzes the file. And, you can [customize the message displayed on users' desktops](https://learn.microsoft.com/en-us/windows/security/threat-protection/windows-defender-security-center/wdsc-customize-contact-information) when a file is blocked. You can change the company name, contact information, and message URL.


[Section titled: Turn on block at first sight with Microsoft Intune](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#turn-on-block-at-first-sight-with-microsoft-intune)

## Turn on block at first sight with Microsoft Intune

1. In the Microsoft Intune admin center ( [https://intune.microsoft.com](https://intune.microsoft.com/)), go to **Endpoint security** \> **Antivirus**.

2. Select an existing policy, or create a new policy using the **Microsoft Defender Antivirus** profile type. In our example, we selected **Windows 10, Windows 11, or Windows Server** for the platform.

[![Screenshot of new MDAV policy creation in Intune.](https://learn.microsoft.com/en-us/defender-endpoint/media/intune-mdav-policy.png)](https://learn.microsoft.com/en-us/defender-endpoint/media/intune-mdav-policy.png#lightbox)

3. Set **Allow cloud protection** to **Allowed. Turns on Cloud Protection**.
![Screenshot of Cloud Protection set to allowed in Intune.](https://learn.microsoft.com/en-us/defender-endpoint/media/intune-mdav-cpallowed.png)

4. Scroll down to **Submit Samples Consent**, and select one of the following settings:

   - **Send all samples automatically**
   - **Send safe samples automatically**
5. Apply the Microsoft Defender Antivirus profile to a group, such as **All users**, **All devices**, or **All users and devices**.


[Section titled: Turn on block at first sight with Group Policy](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#turn-on-block-at-first-sight-with-group-policy)

## Turn on block at first sight with Group Policy

Note

We recommend using Intune or Microsoft Configuration Manager to turn on block at first sight.

1. On your Group Policy management computer, open the [Group Policy Management Console](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc731212(v=ws.11)), right-click the Group Policy Object you want to configure and select **Edit**.

2. Using the **Group Policy Management Editor** go to **Computer configuration** \> **Administrative templates** \> **Windows Components** \> **Microsoft Defender Antivirus** \> **MAPS**.

3. In the MAPS section, double-click **Configure the 'Block at First Sight' feature**, and set it to **Enabled**, and then select **OK**.



Important



Setting to **Always prompt (0)** lowers the protection state of the device. Setting to **Never send (2)** means block at first sight won't function.

4. In the MAPS section, double-click **Send file samples when further analysis is required**, and set it to **Enabled**. Under **Send file samples when further analysis is required**, select **Send all samples**, and then select **OK**.

5. Redeploy your Group Policy Object across your network as you usually do.


[Section titled: Confirm block at first sight is enabled on individual client devices](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#confirm-block-at-first-sight-is-enabled-on-individual-client-devices)

## Confirm block at first sight is enabled on individual client devices

You can confirm that block at first sight is enabled on individual client devices using the Windows Security app. Block at first sight is automatically enabled as long as **Cloud-delivered protection** and **Automatic sample submission** are both turned on.

1. Open the Windows Security app.

2. Select **Virus & threat protection**, and then, under **Virus & threat protection settings**, select **Manage Settings**.

[![The Virus & threat protection settings label in the Windows Security app](https://learn.microsoft.com/en-us/defender/media/wdav-protection-settings-wdsc.png)](https://learn.microsoft.com/en-us/defender/media/wdav-protection-settings-wdsc.png#lightbox)

3. Confirm that **Cloud-delivered protection** and **Automatic sample submission** are both turned on.


Note

- If the prerequisite settings are configured and deployed using Group Policy, the settings described in this section are greyed-out and unavailable for use on individual endpoints.
- Changes made through a Group Policy Object must first be deployed to individual endpoints before the setting gets updated in Windows Settings.

[Section titled: Turn off block at first sight](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#turn-off-block-at-first-sight)

## Turn off block at first sight

Caution

Turning off block at first sight lowers the protection state of your devices and your network. We don't recommend disabling block at first sight protection permanently.

[Section titled: Turn off block at first sight with Microsoft Intune](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#turn-off-block-at-first-sight-with-microsoft-intune)

### Turn off block at first sight with Microsoft Intune

1. Go to the Microsoft Intune admin center ( [https://intune.microsoft.com](https://intune.microsoft.com/)) and sign in.

2. Go to **Endpoint security** \> **Antivirus**, and then select your Microsoft Defender Antivirus policy.

3. Under **Manage**, choose **Properties**.

4. Next to **Configuration settings**, choose **Edit**.

5. Set **Allow cloud protection** to **Not allowed. Turns off Cloud Protection**.

6. Review and save your settings.


[Section titled: Turn off block at first sight with Group Policy](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#turn-off-block-at-first-sight-with-group-policy)

### Turn off block at first sight with Group Policy

1. On your Group Policy management computer, open the [Group Policy Management Console](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc731212(v=ws.11)), right-click the Group Policy Object you want to configure, and then select **Edit**.

2. Using the **Group Policy Management Editor**, go to **Computer configuration** and select **Administrative templates**.

3. Expand the tree through **Windows components** \> **Microsoft Defender Antivirus** \> **MAPS**.

4. Double-click **Configure the 'Block at First Sight' feature** and set the option to **Disabled**.



Note



Disabling block at first sight doesn't disable or alter the prerequisite group policies.


[Section titled: Not an enterprise admin or IT Pro?](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#not-an-enterprise-admin-or-it-pro)

## Not an enterprise admin or IT Pro?

If you aren't an enterprise admin or an IT Pro, but you have questions about block at first sight, this section is for you. Block at first sight is a threat protection feature that detects and blocks malware within seconds. Although there isn't a specific setting called "Block at first sight," the feature is enabled when certain settings are configured on your device.

[Section titled: How to manage block at first sight on or off on your own device](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#how-to-manage-block-at-first-sight-on-or-off-on-your-own-device)

### How to manage block at first sight on or off on your own device

If you have a personal device that isn't managed by an organization, you might be wondering how to turn block at first sight on or off. You can use the Windows Security app to manage block at first sight.

1. On your Windows 10 or Windows 11 computer, open the Windows Security app.

2. Select **Virus & threat protection**.

3. Under **Virus & threat protection settings**, select **Manage settings**.

4. Take one of the following steps:

   - To enable block at first sight, make sure that both **Cloud-delivered protection** and **Automatic sample submission** are both turned on.

   - To disable block at first sight, turn off **Cloud-delivered protection** or **Automatic sample submission**.



     Caution



     Turning off block at first sight lowers the level of protection for your device. We don't recommend permanently disabling block at first sight.

[Section titled: See also](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#see-also)

## See also

- [Microsoft Defender Antivirus in Windows](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows)
- [Enable cloud-delivered protection](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus)
- [Stay protected with Windows Security](https://support.microsoft.com/windows/stay-protected-with-windows-security-2ae0363d-0ada-c064-8b56-6a39afb6a963)
- [Onboard to Microsoft Defender for Endpoint](https://learn.microsoft.com/en-us/defender-endpoint/onboarding)

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


Certification


[Microsoft 365 Certified: Endpoint Administrator Associate - Certifications](https://learn.microsoft.com/en-us/credentials/certifications/modern-desktop/?source=recommendations)

Plan and execute an endpoint deployment strategy, using essential elements of modern management, co-management approaches, and Microsoft Intune integration.


* * *

- Last updated on 10/20/2025

Ask Learn is an AI assistant that can answer questions, clarify concepts, and define terms using trusted Microsoft documentation.

Please sign in to use Ask Learn.

[Sign in](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#)