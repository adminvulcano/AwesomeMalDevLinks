# https://learn.microsoft.com/en-us/defender-endpoint/behavioral-blocking-containment

Table of contents Exit editor mode

Ask LearnAsk LearnFocus mode

Table of contents[Read in English](https://learn.microsoft.com/en-us/defender-endpoint/behavioral-blocking-containment)Add to CollectionsAdd to plan[Edit](https://github.com/MicrosoftDocs/defender-docs/blob/public/defender-endpoint/behavioral-blocking-containment.md)

* * *

#### Share via

[Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fbehavioral-blocking-containment%3FWT.mc_id%3Dfacebook) [x.com](https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fbehavioral-blocking-containment%3FWT.mc_id%3Dtwitter&tw_p=tweetbutton&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fbehavioral-blocking-containment%3FWT.mc_id%3Dtwitter) [LinkedIn](https://www.linkedin.com/feed/?shareActive=true&text=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fbehavioral-blocking-containment%3FWT.mc_id%3Dlinkedin) [Email](mailto:?subject=%5BShared%20Article%5D%20Behavioral%20blocking%20and%20containment%20-%20Microsoft%20Defender%20for%20Endpoint%20%7C%20Microsoft%20Learn&body=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fbehavioral-blocking-containment%3FWT.mc_id%3Demail)

* * *

Copy MarkdownPrint

* * *

Note

Access to this page requires authorization. You can try [signing in](https://learn.microsoft.com/en-us/defender-endpoint/behavioral-blocking-containment#) or changing directories.


Access to this page requires authorization. You can try changing directories.


# Behavioral blocking and containment

- Applies to: Microsoft Defender for Endpoint Plan 1, Microsoft Defender for Endpoint Plan 2

Feedback

Summarize this article for me


[Section titled: Overview](https://learn.microsoft.com/en-us/defender-endpoint/behavioral-blocking-containment#overview)

## Overview

Today's threat landscape is overrun by [fileless malware](https://learn.microsoft.com/en-us/defender-endpoint/malware/fileless-threats) and that lives off the land, highly polymorphic threats that mutate faster than traditional solutions can keep up with, and human-operated attacks that adapt to what adversaries find on compromised devices. Traditional security solutions aren't sufficient to stop such attacks; you need artificial intelligence (AI) and device learning (ML) backed capabilities, such as behavioral blocking and containment, included in [Defender for Endpoint](https://learn.microsoft.com/en-us/windows/security).

Behavioral blocking and containment capabilities can help identify and stop threats, based on their behaviors and process trees even when the threat has started execution. Next-generation protection, EDR, and Defender for Endpoint components and features work together in behavioral blocking and containment capabilities.

Behavioral blocking and containment capabilities work with multiple components and features of Defender for Endpoint to stop attacks immediately and prevent attacks from progressing.

- [Next-generation protection](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows) (which includes Microsoft Defender Antivirus) can detect threats by analyzing behaviors, and stop threats that have started running.

- [Endpoint detection and response](https://learn.microsoft.com/en-us/defender-endpoint/overview-endpoint-detection-response) (EDR) receives security signals across your network, devices, and kernel behavior. As threats are detected, alerts are created. Multiple alerts of the same type are aggregated into incidents, which makes it easier for your security operations team to investigate and respond.

- [Defender for Endpoint](https://learn.microsoft.com/en-us/defender-endpoint/overview-endpoint-detection-response) has a wide range of optics across identities, email, data, and apps, in addition to the network, endpoint, and kernel behavior signals received through EDR. A component of [Microsoft Defender XDR](https://learn.microsoft.com/en-us/defender-xdr/microsoft-365-defender), Defender for Endpoint processes and correlates these signals, raises detection alerts, and connects related alerts in incidents.


With these capabilities, more threats can be prevented or blocked, even if they start running. Whenever suspicious behavior is detected, the threat is contained, alerts are created, and threats are stopped in their tracks.

The following image shows an example of an alert that was triggered by behavioral blocking and containment capabilities:

[![The Alerts page with an alert through behavioral blocking and containment](https://learn.microsoft.com/en-us/defender-endpoint/media/blocked-behav-alert.png)](https://learn.microsoft.com/en-us/defender-endpoint/media/blocked-behav-alert.png#lightbox)

[Section titled: Prerequisites](https://learn.microsoft.com/en-us/defender-endpoint/behavioral-blocking-containment#prerequisites)

## Prerequisites

[Section titled: Supported operating systems](https://learn.microsoft.com/en-us/defender-endpoint/behavioral-blocking-containment#supported-operating-systems)

### Supported operating systems

- Windows

[Section titled: Components of behavioral blocking and containment](https://learn.microsoft.com/en-us/defender-endpoint/behavioral-blocking-containment#components-of-behavioral-blocking-and-containment)

## Components of behavioral blocking and containment

- **On-client, policy-driven [attack surface reduction rules](https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction)** Predefined common attack behaviors are prevented from executing, according to your attack surface reduction rules. When such behaviors attempt to execute, they can be seen in [Microsoft Defender XDR](https://go.microsoft.com/fwlink/p/?linkid=2077139) as informational alerts. Attack surface reduction rules aren't enabled by default; you configure your policies in the [Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/microsoft-365-defender).

- **[Client behavioral blocking](https://learn.microsoft.com/en-us/defender-endpoint/client-behavioral-blocking)** Threats on endpoints are detected through machine learning, and then are blocked and remediated automatically. (Client behavioral blocking is enabled by default.)

- **[Feedback-loop blocking](https://learn.microsoft.com/en-us/defender-endpoint/feedback-loop-blocking)** (also referred to as rapid protection) Threat detections are observed through behavioral intelligence. Threats are stopped and prevented from running on other endpoints. (Feedback-loop blocking is enabled by default.)

- **[Endpoint detection and response (EDR) in block mode](https://learn.microsoft.com/en-us/defender-endpoint/edr-in-block-mode)** Malicious artifacts or behaviors that are observed through post-breach protection are blocked and contained. EDR in block mode works even if Microsoft Defender Antivirus isn't the primary antivirus solution. (EDR in block mode isn't enabled by default; you turn it on at Microsoft Defender XDR.)


Expect more to come in the area of behavioral blocking and containment, as Microsoft continues to improve threat protection features and capabilities. To see what's planned and rolling out now, visit the [Microsoft 365 roadmap](https://www.microsoft.com/microsoft-365/roadmap?filters=Microsoft%20365).

[Section titled: Examples of behavioral blocking and containment in action](https://learn.microsoft.com/en-us/defender-endpoint/behavioral-blocking-containment#examples-of-behavioral-blocking-and-containment-in-action)

## Examples of behavioral blocking and containment in action

Behavioral blocking and containment capabilities have blocked attacker techniques such as the following:

- Credential dumping from LSASS
- Cross-process injection
- Process hollowing
- User Account Control bypass
- Tampering with antivirus (such as disabling it or adding the malware as exclusion)
- Contacting Command and Control (C&C) to download payloads
- Coin mining
- Boot record modification
- Pass-the-hash attacks
- Installation of root certificate
- Exploitation attempt for various vulnerabilities

Below are two real-life examples of behavioral blocking and containment in action.

[Section titled: Example 1: Credential theft attack against 100 organizations](https://learn.microsoft.com/en-us/defender-endpoint/behavioral-blocking-containment#example-1-credential-theft-attack-against-100-organizations)

### Example 1: Credential theft attack against 100 organizations

As described in [In hot pursuit of elusive threats: AI-driven behavior-based blocking stops attacks in their tracks](https://www.microsoft.com/security/blog/2019/10/08/in-hot-pursuit-of-elusive-threats-ai-driven-behavior-based-blocking-stops-attacks-in-their-tracks), a credential theft attack against 100 organizations around the world was stopped by behavioral blocking and containment capabilities. Spear-phishing email messages that contained a lure document were sent to the targeted organizations. If a recipient opened the attachment, a related remote document was able to execute code on the user's device and load Lokibot malware, which stole credentials, exfiltrated stolen data, and waited for further instructions from a command-and-control server.

Behavior-based device-learning models in Defender for Endpoint caught and stopped the attacker's techniques at two points in the attack chain:

- The first protection layer detected the exploit behavior. Device-learning classifiers in the cloud correctly identified the threat as and immediately instructed the client device to block the attack.
- The second protection layer, which helped stop cases where the attack got past the first layer, detected process hollowing, stopped that process, and removed the corresponding files (such as Lokibot).

While the attack was detected and stopped, alerts, such as an "initial access alert," were triggered and appeared in the [Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-xdr/microsoft-365-defender).

[![Initial access alert in the Microsoft Defender portal](https://learn.microsoft.com/en-us/defender-endpoint/media/behavblockcontain-initialaccessalert.png)](https://learn.microsoft.com/en-us/defender-endpoint/media/behavblockcontain-initialaccessalert.png#lightbox)

This example shows how behavior-based device-learning models in the cloud add new layers of protection against attacks, even after they have started running.

[Section titled: Example 2: NTLM relay - Juicy Potato malware variant](https://learn.microsoft.com/en-us/defender-endpoint/behavioral-blocking-containment#example-2-ntlm-relay---juicy-potato-malware-variant)

### Example 2: NTLM relay - Juicy Potato malware variant

As described in the recent blog post, [Behavioral blocking and containment: Transforming optics into protection](https://www.microsoft.com/security/blog/2020/03/09/behavioral-blocking-and-containment-transforming-optics-into-protection), in January 2020, Defender for Endpoint detected a privilege escalation activity on a device in an organization. An alert called "Possible privilege escalation using NTLM relay" was triggered.

[![An NTLM alert for Juicy Potato malware](https://learn.microsoft.com/en-us/defender-endpoint/media/ntlmalertjuicypotato.png)](https://learn.microsoft.com/en-us/defender-endpoint/media/ntlmalertjuicypotato.png#lightbox)

The threat turned out to be malware; it was a new, not-seen-before variant of a notorious hacking tool called Juicy Potato, which is used by attackers to get privilege escalation on a device.

Minutes after the alert was triggered, the file was analyzed, and confirmed to be malicious. Its process was stopped and blocked, as shown in the following image:

[![Artifact blocked](https://learn.microsoft.com/en-us/defender-endpoint/media/artifactblockedjuicypotato.png)](https://learn.microsoft.com/en-us/defender-endpoint/media/artifactblockedjuicypotato.png#lightbox)

A few minutes after the artifact was blocked, multiple instances of the same file were blocked on the same device, preventing more attackers or other malware from deploying on the device.

This example shows that with behavioral blocking and containment capabilities, threats are detected, contained, and blocked automatically.

Tip

If you're looking for Antivirus related information for other platforms, see:

- [Set preferences for Microsoft Defender for Endpoint on macOS](https://learn.microsoft.com/en-us/defender-endpoint/mac-preferences)
- [Microsoft Defender for Endpoint on Mac](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint-mac)
- [macOS Antivirus policy settings for Microsoft Defender Antivirus for Intune](https://learn.microsoft.com/en-us/mem/intune/protect/antivirus-microsoft-defender-settings-macos)
- [Set preferences for Microsoft Defender for Endpoint on Linux](https://learn.microsoft.com/en-us/defender-endpoint/linux-preferences)
- [Microsoft Defender for Endpoint on Linux](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint-linux)
- [Configure Defender for Endpoint on Android features](https://learn.microsoft.com/en-us/defender-endpoint/android-configure)
- [Configure Microsoft Defender for Endpoint on iOS features](https://learn.microsoft.com/en-us/defender-endpoint/ios-configure-features)

[Section titled: Next steps](https://learn.microsoft.com/en-us/defender-endpoint/behavioral-blocking-containment#next-steps)

## Next steps

- [Learn more about Defender for Endpoint](https://learn.microsoft.com/en-us/defender-endpoint/overview-endpoint-detection-response)

- [Configure your attack surface reduction rules](https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction)

- [Enable EDR in block mode](https://learn.microsoft.com/en-us/defender-endpoint/edr-in-block-mode)

- [See recent global threat activity](https://www.microsoft.com/wdsi/threats)

- [Get an overview of Microsoft Defender XDR](https://learn.microsoft.com/en-us/defender-xdr/microsoft-365-defender)


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


[Microsoft Certified: Security Operations Analyst Associate - Certifications](https://learn.microsoft.com/en-us/credentials/certifications/security-operations-analyst/?source=recommendations)

Investigate, search for, and mitigate threats using Microsoft Sentinel, Microsoft Defender for Cloud, and Microsoft 365 Defender.


* * *

- Last updated on 10/20/2025

Ask Learn is an AI assistant that can answer questions, clarify concepts, and define terms using trusted Microsoft documentation.

Please sign in to use Ask Learn.

[Sign in](https://learn.microsoft.com/en-us/defender-endpoint/behavioral-blocking-containment#)