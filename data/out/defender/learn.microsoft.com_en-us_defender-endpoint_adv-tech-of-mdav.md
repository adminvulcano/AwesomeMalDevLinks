# https://learn.microsoft.com/en-us/defender-endpoint/adv-tech-of-mdav

Table of contents Exit editor mode

Ask LearnAsk LearnFocus mode

Table of contents[Read in English](https://learn.microsoft.com/en-us/defender-endpoint/adv-tech-of-mdav)Add to CollectionsAdd to plan[Edit](https://github.com/MicrosoftDocs/defender-docs/blob/public/defender-endpoint/adv-tech-of-mdav.md)

* * *

#### Share via

[Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fadv-tech-of-mdav%3FWT.mc_id%3Dfacebook) [x.com](https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fadv-tech-of-mdav%3FWT.mc_id%3Dtwitter&tw_p=tweetbutton&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fadv-tech-of-mdav%3FWT.mc_id%3Dtwitter) [LinkedIn](https://www.linkedin.com/feed/?shareActive=true&text=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fadv-tech-of-mdav%3FWT.mc_id%3Dlinkedin) [Email](mailto:?subject=%5BShared%20Article%5D%20Advanced%20technologies%20at%20the%20core%20of%20Microsoft%20Defender%20Antivirus%20-%20Microsoft%20Defender%20for%20Endpoint%20%7C%20Microsoft%20Learn&body=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fadv-tech-of-mdav%3FWT.mc_id%3Demail)

* * *

Copy MarkdownPrint

* * *

Note

Access to this page requires authorization. You can try [signing in](https://learn.microsoft.com/en-us/defender-endpoint/adv-tech-of-mdav#) or changing directories.


Access to this page requires authorization. You can try changing directories.


# Advanced technologies at the core of Microsoft Defender Antivirus

- Applies to: Microsoft Defender for Endpoint Plan 1, Microsoft Defender for Endpoint Plan 2, Microsoft Defender for Business, Microsoft Defender for Individuals

Feedback

Summarize this article for me


Microsoft Defender Antivirus and the multiple engines that lead to the advanced detection and prevention technologies under the hood to detect and stop a wide range of threats and attacker techniques at multiple points, as depicted in the following diagram:

![Diagram depicting next generation protection engines and how they work between the cloud and the client device.](https://learn.microsoft.com/en-us/defender-endpoint/media/next-gen-protection-engines.png)

Many of these engines are built into the client and provide advanced protection against most threats in real time.

These next-generation protection engines provide [industry-best](https://learn.microsoft.com/en-us/windows/security/threat-protection/intelligence/top-scoring-industry-antivirus-tests) detection and blocking capabilities and ensure that protection is:

- **Accurate**: Threats both common and sophisticated, many which are designed to try to slip through protections, are detected and blocked.
- **Real-time**: Threats are prevented from getting on to devices, stopped in real-time at first sight, or detected and remediated in the least possible time (typically within a few milliseconds).
- **Intelligent**: Through the power of the cloud, machine learning (ML), and Microsoft's industry-leading optics, protection is enriched and made even more effective against new and unknown threats.

[Section titled: Hybrid detection and protection](https://learn.microsoft.com/en-us/defender-endpoint/adv-tech-of-mdav#hybrid-detection-and-protection)

## Hybrid detection and protection

Microsoft Defender Antivirus does hybrid detection and protection. What this means is, detection and protection occur on the client device first, and works with the cloud for newly developing threats, which results in faster, more effective detection and protection.

When the client encounters unknown threats, it sends metadata or the file itself to the cloud protection service, where more advanced protections examine new threats on the fly and integrate signals from multiple sources.

Expand table

| On the client | In the cloud |
| --- | --- |
| **Machine learning (ML) engine**<br> A set of light-weight machine learning models make a verdict within milliseconds. These models include specialized models and features that are built for specific file types commonly abused by attackers. Examples include models built for portable executable (PE) files, PowerShell, Office macros, JavaScript, PDF files, and more. | **Metadata-based ML engine**<br> Specialized ML models, which include file type-specific models, feature-specific models, and adversary-hardened [monotonic models](https://www.microsoft.com/security/blog/2019/07/25/new-machine-learning-model-sifts-through-the-good-to-unearth-the-bad-in-evasive-malware/), analyze a featurized description of suspicious files sent by the client. Stacked ensemble classifiers combine results from these models to make a real-time verdict to allow or block files pre-execution. |
| **Behavior monitoring engine**<br> The behavior monitoring engine monitors for potential attacks post-execution. It observes process behaviors, including behavior sequence at runtime, to identify and block certain types of activities based on predetermined rules. | **Behavior-based ML engine**<br> Suspicious behavior sequences and advanced attack techniques are monitored on the client as triggers to analyze the process tree behavior using real-time cloud ML models. Monitored attack techniques span the attack chain, from exploits, elevation, and persistence all the way through to lateral movement and exfiltration. |
| **Memory scanning engine**<br> This engine scans the memory space used by a running process to expose malicious behavior that could be hiding through code obfuscation. | **Antimalware Scan Interface (AMSI)-paired ML engine**<br> Pairs of client-side and cloud-side models perform advanced analysis of scripting behavior pre- and post-execution to catch advanced threats like fileless and in-memory attacks. These models include a pair of models for each of the scripting engines covered, including PowerShell, JavaScript, VBScript, and Office VBA macros. Integrations include both dynamic content calls and/or behavior instrumentation on the scripting engines. |
| **AMSI integration engine**<br> Deep in-app integration engine enables detection of fileless and in-memory attacks through [AMSI](https://learn.microsoft.com/en-us/windows/desktop/AMSI/antimalware-scan-interface-portal), defeating code obfuscation. This integration blocks malicious behavior of scripts client-side. | **File classification ML engine**<br> Multi-class, deep neural network classifiers examine full file contents, provides an extra layer of defense against attacks that require more analysis. Suspicious files are held from running and submitted to the cloud protection service for classification. Within seconds, full-content deep learning models produce a classification and reply to the client to allow or block the file. |
| **Heuristics engine**<br> Heuristic rules identify file characteristics that have similarities with known malicious characteristics to catch new threats or modified versions of known threats. | **Detonation-based ML engine**<br> Suspicious files are detonated in a sandbox. Deep learning classifiers analyze the observed behaviors to block attacks. |
| **Emulation engine**<br> The emulation engine dynamically unpacks malware and examines how they would behave at runtime. The dynamic emulation of the content and scanning both the behavior during emulation and the memory content at the end of emulation defeat malware packers and expose the behavior of polymorphic malware. | **Reputation ML engine**<br> Domain-expert reputation sources and models from across Microsoft are queried to block threats that are linked to malicious or suspicious URLs, domains, emails, and files. Sources include Windows Defender SmartScreen for URL reputation models and Defender for Office 365 for email attachment expert knowledge, among other Microsoft services through the Microsoft Intelligent Security Graph. |
| **Network engine**<br> Network activities are inspected to identify and stop malicious activities from threats. | **Smart rules engine**<br> Expert-written smart rules identify threats based on researcher expertise and collective knowledge of threats. |
| **CommandLine scanning engine**<br> This engine scans the commandlines of all processes before they execute. If the commandline for a process is found to be malicious it is blocked from execution. | **CommandLine ML engine**<br> Multiple advanced ML models scan the suspicious commandlines in the cloud. If a commandline is found to be malicious, cloud sends a signal to the client to block the corresponding process from starting. |

For more information, see [Microsoft 365 Defender demonstrates 100 percent protection coverage in the 2023 MITRE Engenuity ATT&CK® Evaluations: Enterprise](https://www.microsoft.com/security/blog/2023/09/20/microsoft-365-defender-demonstrates-100-percent-protection-coverage-in-the-2023-mitre-engenuity-attck-evaluations-enterprise/).

[Section titled: How next-generation protection works with other Defender for Endpoint capabilities](https://learn.microsoft.com/en-us/defender-endpoint/adv-tech-of-mdav#how-next-generation-protection-works-with-other-defender-for-endpoint-capabilities)

## How next-generation protection works with other Defender for Endpoint capabilities

Together with [attack surface reduction](https://learn.microsoft.com/en-us/defender-endpoint/overview-attack-surface-reduction), which includes advanced capabilities like hardware-based isolation, application control, exploit protection, network protection, controlled folder access, attack surface reduction rules, and network firewall, [next-generation protection](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows) engines deliver Microsoft Defender for Endpoint's prebreach capabilities, stopping attacks before they can infiltrate devices and compromise networks.

As part of Microsoft's defense-in-depth solution, the superior performance of these engines accrues to the [Microsoft Defender for Endpoint](https://www.microsoft.com/security/business/endpoint-security/microsoft-defender-endpoint) unified endpoint protection, where antivirus detections and other next-generation protection capabilities enrich endpoint detection and response, automated investigation and remediation, advanced hunting, threat and vulnerability management, managed threat hunting service, and other capabilities.

These protections are further amplified through [Microsoft Defender XDR](https://www.microsoft.com/security/business/siem-and-xdr/microsoft-defender-xdr), Microsoft's comprehensive, end-to-end security solution for the modern workplace. Through [signal-sharing and orchestration of remediation across Microsoft's security technologies](https://techcommunity.microsoft.com/t5/Security-Privacy-and-Compliance/Announcing-Microsoft-Threat-Protection/ba-p/262783), Microsoft Defender XDR secures identities, endpoints, email and data, apps, and infrastructure.

[Section titled: Memory protection and memory scanning](https://learn.microsoft.com/en-us/defender-endpoint/adv-tech-of-mdav#memory-protection-and-memory-scanning)

## Memory protection and memory scanning

Microsoft Defender Antivirus (MDAV) provides memory protection with different engines:

Expand table

| Client | Cloud |
| --- | --- |
| Behavior Monitoring | Behavior-based Machine Learning |
| Antimalware Scan Interface(AMSI) integration | AMSI-paired Machine Learning |
| Emulation | Detonation-based Machine Learning |
| Memory scanning | N/A |

An additional layer to help prevent memory-based attacks is to use the Attack Surface Reduction (ASR) rule – **Block Office applications from injecting code into other processes**. For more information see, [Block Office applications from injecting code into other processes](https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-reference#block-office-applications-from-injecting-code-into-other-processes).

[Section titled: Frequently asked questions](https://learn.microsoft.com/en-us/defender-endpoint/adv-tech-of-mdav#frequently-asked-questions)

## Frequently asked questions

[Section titled: How many malware threats does Microsoft Defender Antivirus block per month?](https://learn.microsoft.com/en-us/defender-endpoint/adv-tech-of-mdav#how-many-malware-threats-does-microsoft-defender-antivirus-block-per-month)

### How many malware threats does Microsoft Defender Antivirus block per month?

[Five billion threats on devices every month](https://www.microsoft.com/security/blog/2019/05/14/executing-vision-microsoft-threat-protection/).

[Section titled: How does Microsoft Defender Antivirus memory protection help?](https://learn.microsoft.com/en-us/defender-endpoint/adv-tech-of-mdav#how-does-microsoft-defender-antivirus-memory-protection-help)

### How does Microsoft Defender Antivirus memory protection help?

See [Detecting reflective DLL loading with Windows Defender for Endpoint](https://www.microsoft.com/security/blog/2017/11/13/detecting-reflective-dll-loading-with-windows-defender-atp/) to learn about one way Microsoft Defender Antivirus memory attack protection helps.

[Section titled: Do you all focus your detections/preventions in one specific geographic area?](https://learn.microsoft.com/en-us/defender-endpoint/adv-tech-of-mdav#do-you-all-focus-your-detectionspreventions-in-one-specific-geographic-area)

### Do you all focus your detections/preventions in one specific geographic area?

No, we are in all the geographical regions (Americas, EMEA, and APAC).

[Section titled: Do you all focus on specific industries?](https://learn.microsoft.com/en-us/defender-endpoint/adv-tech-of-mdav#do-you-all-focus-on-specific-industries)

### Do you all focus on specific industries?

We focus on every industry.

[Section titled: Do your detection/protection require a human analyst?](https://learn.microsoft.com/en-us/defender-endpoint/adv-tech-of-mdav#do-your-detectionprotection-require-a-human-analyst)

### Do your detection/protection require a human analyst?

When you're pen-testing, you should demand where no human analysts are engaged on detect/protect, to see how the actual antivirus engine (prebreach) efficacy truly is, and a separate one where human analysts are engaged. You can add [Microsoft Defender Experts for XDR](https://learn.microsoft.com/en-us/defender-xdr/dex-xdr-overview) a managed extended detection and response service to augment your SOC.

The _**continuous iterative enhancement**_ each of these engines to be increasingly effective at catching the latest strains of malware and attack methods. These enhancements show up in consistent [top scores in industry tests](https://learn.microsoft.com/en-us/defender-xdr/top-scoring-industry-tests), but more importantly, translate to [threats and malware outbreaks](https://www.microsoft.com/security/blog/2018/03/07/behavior-monitoring-combined-with-machine-learning-spoils-a-massive-dofoil-coin-mining-campaign/) stopped and [more customers protected](https://www.microsoft.com/security/blog/2018/03/22/why-windows-defender-antivirus-is-the-most-deployed-in-the-enterprise/).

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

- Last updated on 01/24/2025

Ask Learn is an AI assistant that can answer questions, clarify concepts, and define terms using trusted Microsoft documentation.

Please sign in to use Ask Learn.

[Sign in](https://learn.microsoft.com/en-us/defender-endpoint/adv-tech-of-mdav#)