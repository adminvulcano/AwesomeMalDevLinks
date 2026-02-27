# https://learn.microsoft.com/en-us/defender-endpoint/client-behavioral-blocking

Table of contents Exit editor mode

Ask LearnAsk LearnFocus mode

Table of contents[Read in English](https://learn.microsoft.com/en-us/defender-endpoint/client-behavioral-blocking)Add to CollectionsAdd to plan[Edit](https://github.com/MicrosoftDocs/defender-docs/blob/public/defender-endpoint/client-behavioral-blocking.md)

* * *

#### Share via

[Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fclient-behavioral-blocking%3FWT.mc_id%3Dfacebook) [x.com](https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fclient-behavioral-blocking%3FWT.mc_id%3Dtwitter&tw_p=tweetbutton&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fclient-behavioral-blocking%3FWT.mc_id%3Dtwitter) [LinkedIn](https://www.linkedin.com/feed/?shareActive=true&text=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fclient-behavioral-blocking%3FWT.mc_id%3Dlinkedin) [Email](mailto:?subject=%5BShared%20Article%5D%20Client%20behavioral%20blocking%20-%20Microsoft%20Defender%20for%20Endpoint%20%7C%20Microsoft%20Learn&body=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fclient-behavioral-blocking%3FWT.mc_id%3Demail)

* * *

Copy MarkdownPrint

* * *

Note

Access to this page requires authorization. You can try [signing in](https://learn.microsoft.com/en-us/defender-endpoint/client-behavioral-blocking#) or changing directories.


Access to this page requires authorization. You can try changing directories.


# Client behavioral blocking

- Applies to: Microsoft Defender for Endpoint Plan 1, Microsoft Defender for Endpoint Plan 2

Feedback

Summarize this article for me


**Platform**

- Windows

[Section titled: Overview](https://learn.microsoft.com/en-us/defender-endpoint/client-behavioral-blocking#overview)

## Overview

Client behavioral blocking is a component of [behavioral blocking and containment capabilities](https://learn.microsoft.com/en-us/defender-endpoint/behavioral-blocking-containment) in Defender for Endpoint. As suspicious behaviors are detected on devices (also referred to as clients or endpoints), artifacts (such as files or applications) are blocked, checked, and remediated automatically.

[![Cloud and client protection](https://learn.microsoft.com/en-us/defender-endpoint/media/pre-execution-and-post-execution-detection-engines.png)](https://learn.microsoft.com/en-us/defender-endpoint/media/pre-execution-and-post-execution-detection-engines.png#lightbox)

Antivirus protection works best when paired with cloud protection.

[Section titled: How client behavioral blocking works](https://learn.microsoft.com/en-us/defender-endpoint/client-behavioral-blocking#how-client-behavioral-blocking-works)

## How client behavioral blocking works

[Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows) can detect suspicious behavior, malicious code, fileless and in-memory attacks, and more on a device. When suspicious behaviors are detected, Microsoft Defender Antivirus monitors and sends those suspicious behaviors and their process trees to the cloud protection service. Machine learning differentiates between malicious applications and good behaviors within milliseconds, and classifies each artifact. In almost real time, as soon as an artifact is found to be malicious, it's blocked on the device.

Whenever a suspicious behavior is detected, an [alert](https://learn.microsoft.com/en-us/defender-endpoint/alerts-queue) is generated and is visible while the attack was detected and stopped; alerts, such as an "initial access alert," are triggered and appear in the [Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/microsoft-365-defender).

Client behavioral blocking is effective because it not only helps prevent an attack from starting, it can help stop an attack that has begun executing. And, with [feedback-loop blocking](https://learn.microsoft.com/en-us/defender-endpoint/feedback-loop-blocking) (another capability of behavioral blocking and containment), attacks are prevented on other devices in your organization.

[Section titled: Behavior-based detections](https://learn.microsoft.com/en-us/defender-endpoint/client-behavioral-blocking#behavior-based-detections)

## Behavior-based detections

Behavior-based detections are named according to the [MITRE ATT&CK Matrix for Enterprise](https://attack.mitre.org/matrices/enterprise). The naming convention helps identify the attack stage where the malicious behavior was observed:

Expand table

| Tactic | Detection threat name |
| --- | --- |
| Initial Access | `Behavior:Win32/InitialAccess.*!ml` |
| Execution | `Behavior:Win32/Execution.*!ml` |
| Persistence | `Behavior:Win32/Persistence.*!ml` |
| Privilege Escalation | `Behavior:Win32/PrivilegeEscalation.*!ml` |
| Defense Evasion | `Behavior:Win32/DefenseEvasion.*!ml` |
| Credential Access | `Behavior:Win32/CredentialAccess.*!ml` |
| Discovery | `Behavior:Win32/Discovery.*!ml` |
| Lateral Movement | `Behavior:Win32/LateralMovement.*!ml` |
| Collection | `Behavior:Win32/Collection.*!ml` |
| Command and Control | `Behavior:Win32/CommandAndControl.*!ml` |
| Exfiltration | `Behavior:Win32/Exfiltration.*!ml` |
| Impact | `Behavior:Win32/Impact.*!ml` |
| Uncategorized | `Behavior:Win32/Generic.*!ml` |

Tip

To learn more about specific threats, see **[recent global threat activity](https://www.microsoft.com/wdsi/threats)**.

[Section titled: Configuring client behavioral blocking](https://learn.microsoft.com/en-us/defender-endpoint/client-behavioral-blocking#configuring-client-behavioral-blocking)

## Configuring client behavioral blocking

If your organization is using Defender for Endpoint, client behavioral blocking is enabled by default. However, to benefit from all Defender for Endpoint capabilities, including [behavioral blocking and containment](https://learn.microsoft.com/en-us/defender-endpoint/behavioral-blocking-containment), make sure the following features and capabilities of Defender for Endpoint are enabled and configured:

- [Defender for Endpoint baselines](https://learn.microsoft.com/en-us/defender-endpoint/configure-machines-security-baseline)
- [Devices onboarded to Defender for Endpoint](https://learn.microsoft.com/en-us/defender-endpoint/onboard-configure)
- [EDR in block mode](https://learn.microsoft.com/en-us/defender-endpoint/edr-in-block-mode)
- [Attack surface reduction](https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction)
- [Next-generation protection](https://learn.microsoft.com/en-us/defender-endpoint/configure-microsoft-defender-antivirus-features) (antivirus, antimalware, and other threat protection capabilities)

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


[Perform device investigations in Microsoft Defender for Endpoint - Training](https://learn.microsoft.com/en-us/training/modules/perform-device-investigations-microsoft-defender-for-endpoints/?source=recommendations)

Perform device investigations in Microsoft Defender for Endpoint


Certification


[Microsoft Certified: Security Operations Analyst Associate - Certifications](https://learn.microsoft.com/en-us/credentials/certifications/security-operations-analyst/?source=recommendations)

Investigate, search for, and mitigate threats using Microsoft Sentinel, Microsoft Defender for Cloud, and Microsoft 365 Defender.


* * *

- Last updated on 09/29/2025

Ask Learn is an AI assistant that can answer questions, clarify concepts, and define terms using trusted Microsoft documentation.

Please sign in to use Ask Learn.

[Sign in](https://learn.microsoft.com/en-us/defender-endpoint/client-behavioral-blocking#)