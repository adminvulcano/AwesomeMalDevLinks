# https://www.microsoft.com/en-us/security/blog/2019/06/24/inside-out-get-to-know-the-advanced-technologies-at-the-core-of-microsoft-defender-atp-next-generation-protection/

[Skip to content](https://www.microsoft.com/en-us/security/blog/2019/06/24/inside-out-get-to-know-the-advanced-technologies-at-the-core-of-microsoft-defender-atp-next-generation-protection/#wp--skip-link--target)

 [Skip to content](https://www.microsoft.com/en-us/security/blog/2019/06/24/inside-out-get-to-know-the-advanced-technologies-at-the-core-of-microsoft-defender-atp-next-generation-protection/#wp--skip-link--target)

![](https://www.microsoft.com/en-us/security/blog/wp-content/themes/security-blog-2025/dist/images/single-bg.jpg)

![](https://www.microsoft.com/en-us/security/blog/wp-content/themes/security-blog-2025/dist/images/single-bg-dark.jpg)

* * *

## Share

- [Link copied to clipboard!](https://www.microsoft.com/en-us/security/blog/2019/06/24/inside-out-get-to-know-the-advanced-technologies-at-the-core-of-microsoft-defender-atp-next-generation-protection/)
- [Share on Facebook](https://www.facebook.com/sharer/sharer.php?u=https://www.microsoft.com/en-us/security/blog/2019/06/24/inside-out-get-to-know-the-advanced-technologies-at-the-core-of-microsoft-defender-atp-next-generation-protection/)
- [Share on X](https://twitter.com/intent/tweet?url=https://www.microsoft.com/en-us/security/blog/2019/06/24/inside-out-get-to-know-the-advanced-technologies-at-the-core-of-microsoft-defender-atp-next-generation-protection/&text=Inside+out%3A+Get+to+know+the+advanced+technologies+at+the+core+of+Microsoft+Defender+ATP+next+generation+protection)
- [Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https://www.microsoft.com/en-us/security/blog/2019/06/24/inside-out-get-to-know-the-advanced-technologies-at-the-core-of-microsoft-defender-atp-next-generation-protection/)

## Content types

- [Research](https://www.microsoft.com/en-us/security/blog/content-type/research/)

## Products and services

- [Microsoft Defender](https://www.microsoft.com/en-us/security/blog/product/microsoft-defender/)
- [Microsoft Defender for Endpoint](https://www.microsoft.com/en-us/security/blog/product/microsoft-defender-for-endpoint/)

## Topics

- [Threat intelligence](https://www.microsoft.com/en-us/security/blog/topic/threat-intelligence/)

more

While Windows Defender Antivirus makes catching [5 billion threats on devices every month](https://www.microsoft.com/en-us/security/blog/2019/05/14/executing-vision-microsoft-threat-protection/) look easy, multiple advanced detection and prevention technologies work under the hood to make this happen.

Windows Defender Antivirus is the [next-generation protection](https://docs.microsoft.com/windows/security/threat-protection/windows-defender-antivirus/windows-defender-antivirus-in-windows-10) component of Microsoft Defender Advanced Threat Protection ( [Microsoft Defender ATP](https://www.microsoft.com/en-us/WindowsForBusiness/windows-atp?ocid=cx-blog-mmpc)), Microsoft’s unified endpoint security platform. Much like how Microsoft Defender ATP integrates multiple capabilities to address the complex security challenges in modern enterprises, Windows Defender Antivirus uses multiple engines to detect and stop a wide range of threats and attacker techniques at multiple points.

These next-generation protection engines provide [industry-best](https://docs.microsoft.com/windows/security/threat-protection/intelligence/top-scoring-industry-antivirus-tests) detection and blocking capabilities. Many of these engines are built into the client and provide advanced protection against majority of threats in real-time. When the client encounters unknown threats, it sends metadata or the file itself to the cloud protection service, where more advanced protections examine new threats on the fly and integrate signals from multiple sources.

![Microsoft Defender ATP next generation protection engines](https://www.microsoft.com/en-us/security/blog//wp-content/uploads/2019/06/microsoft-defender-atp-next-generation-protection-engines.png)

These next-generation protection engines ensure that protection is:

- **Accurate**: Threats both common and sophisticated, a lot of which are designed to try and slip through protections, are detected and blocked
- **Real-time**: Threats are prevented from getting on to devices, stopped in real-time at first sight, or detected and remediated in the least possible time (typically within a few milliseconds)
- **Intelligent**: Through the power of the cloud, machine learning (ML), and Microsoft’s industry-leading optics, protection is enriched and made even more effective against new and unknown threats

My team continuously enhances each of these engines to be increasingly effective at catching the latest strains of malware and attack methods. These enhancements show up in consistent [top scores in industry tests](https://docs.microsoft.com/windows/security/threat-protection/intelligence/top-scoring-industry-antivirus-tests), but more importantly, translate to [threats and malware outbreaks](https://www.microsoft.com/en-us/security/blog/2018/03/07/behavior-monitoring-combined-with-machine-learning-spoils-a-massive-dofoil-coin-mining-campaign/) stopped and [more customers protected](https://www.microsoft.com/en-us/security/blog/2018/03/22/why-windows-defender-antivirus-is-the-most-deployed-in-the-enterprise/).

Here’s a rundown of the many components of the next generation protection capabilities in Microsoft Defender ATP:

In the cloud:

- **Metadata-based ML engine** – Specialized ML models, which include file type-specific models, feature-specific models, and adversary-hardened [monotonic models](https://www.microsoft.com/en-us/security/blog/2019/07/25/new-machine-learning-model-sifts-through-the-good-to-unearth-the-bad-in-evasive-malware/), analyze a featurized description of suspicious files sent by the client. Stacked ensemble classifiers combine results from these models to make a real-time verdict to allow or block files pre-execution.
- **Behavior-based ML engine** – Suspicious behavior sequences and advanced attack techniques are monitored on the client as triggers to analyze the process tree behavior using real-time cloud ML models. Monitored attack techniques span the attack chain, from exploits, elevation, and persistence all the way through to lateral movement and exfiltration.
- **AMSI-paired ML engine** – Pairs of client-side and cloud-side models perform advanced analysis of scripting behavior pre- and post-execution to catch advanced threats like fileless and in-memory attacks. These models include a pair of models for each of the scripting engines covered, including PowerShell, JavaScript, VBScript, and Office VBA macros. Integrations include both dynamic content calls and/or behavior instrumentation on the scripting engines.
- **File classification ML engine** – Multi-class, deep neural network classifiers examine full file contents, provides an additional layer of defense against attacks that require additional analysis. Suspicious files are held from running and submitted to the cloud protection service for classification. Within seconds, full-content deep learning models produce a classification and reply to the client to allow or block the file.
- **Detonation-based ML engine** – Suspicious files are detonated in a sandbox. Deep learning classifiers analyze the observed behaviors to block attacks.
- **Reputation ML engine** – Domain-expert reputation sources and models from across Microsoft are queried to block threats that are linked to malicious or suspicious URLs, domains, emails, and files. Sources include Windows Defender SmartScreen for URL reputation models and Office 365 ATP for email attachment expert knowledge, among other Microsoft services through the Microsoft Intelligent Security Graph.
- **Smart rules engine** – Expert-written smart rules identify threats based on researcher expertise and collective knowledge of threats.

On the client:

- **ML engine** – A set of light-weight machine learning models make a verdict within milliseconds. These include specialized models and features that are built for specific file types commonly abused by attackers. Examples include models built for portable executable (PE) files, PowerShell, Office macros, JavaScript, PDF files, and more.
- **Behavior monitoring engine** – The behavior monitoring engine monitors for potential attacks post-execution. It observes process behaviors, including behavior sequence at runtime, to identify and block certain types of activities based on predetermined rules.
- **Memory scanning engine** – This engine scans the memory space used by a running process to expose malicious behavior that may be hiding through code obfuscation.
- **AMSI integration engine** – Deep in-app integration engine enables detection of fileless and in-memory attacks through Antimalware Scan Interface ( [AMSI](https://docs.microsoft.com/en-us/windows/desktop/AMSI/antimalware-scan-interface-portal)), defeating code obfuscation. This integration blocks malicious behavior of scripts client-side.
- **Heuristics engine** – Heuristic rules identify file characteristics that have similarities with known malicious characteristics to catch new threats or modified versions of known threats.
- **Emulation engine** – The emulation engine dynamically unpacks malware and examines how they would behave at runtime. The dynamic emulation of the content and scanning both the behavior during emulation and the memory content at the end of emulation defeat malware packers and expose the behavior of polymorphic malware.
- **Network engine** – Network activities are inspected to identify and stop malicious activities from threats.

Together with [attack surface reduction](https://docs.microsoft.com/windows/security/threat-protection/microsoft-defender-atp/overview-attack-surface-reduction)—composed of advanced capabilities like hardware-based isolation, application control, exploit protection, network protection, controlled folder access, attack surface reduction rules, and network firewall—these [next-generation protection](https://docs.microsoft.com/windows/security/threat-protection/windows-defender-antivirus/windows-defender-antivirus-in-windows-10) engines deliver Microsoft Defender ATP’s pre-breach capabilities, stopping attacks before they can infiltrate devices and compromise networks.

As part of Microsoft’s defense-in-depth solution, the superior performance of these engines accrues to the [Microsoft Defender ATP](https://www.microsoft.com/en-us/WindowsForBusiness/windows-atp?ocid=cx-blog-mmpc) unified endpoint protection, where antivirus detections and other next-generation protection capabilities enrich endpoint detection and response, automated investigation and remediation, advanced hunting, threat and vulnerability management, managed threat hunting service, and other capabilities.

These protections are further amplified through [Microsoft Threat Protection](https://www.microsoft.com/en-us/security/technology/threat-protection), Microsoft’s comprehensive, end-to-end security solution for the modern workplace. Through [signal-sharing and orchestration of remediation across Microsoft’s security technologies](https://techcommunity.microsoft.com/t5/Security-Privacy-and-Compliance/Announcing-Microsoft-Threat-Protection/ba-p/262783), Microsoft Threat Protection secures identities, endpoints, email and data, apps, and infrastructure.

![A diagram showing the enormous evolution of Microsoft Defender ATP's next generation protection](https://www.microsoft.com/en-us/security/blog//wp-content/uploads/2019/06/microsoft-defender-atp-ngp-microsoft-threat-protection.png)

The enormous evolution of Microsoft Defender ATP’s next generation protection follows the same upward trajectory of innovation across Microsoft’s security technologies, which the industry recognizes, and customers benefit from. We will continue to improve and lead the industry in evolving security.

**_Tanmay Ganacharya ( [@tanmayg](https://twitter.com/tanmayg))_**

_Principal Director, Microsoft Defender ATP Research_

* * *

## Talk to us

Questions, concerns, or insights on this story? Join discussions at the [Microsoft Defender ATP community](https://techcommunity.microsoft.com/t5/Windows-Defender-Advanced-Threat/ct-p/WindowsDefenderAdvanced).

Follow us on Twitter [**@MsftSecIntel**](https://twitter.com/MsftSecIntel).

![](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2018/01/tanmay-ganacharya-300x300.png)

## Tanmay Ganacharya

Vice President, Security Research, Microsoft Defender

[See Tanmay Ganacharya posts](https://www.microsoft.com/en-us/security/blog/author/tanmay-ganacharya/)

## Related posts

- ![A man sitting at a desk using a laptop](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2025/06/Featured-image-RIFT-809x455.webp)









  - June 27, 2025
  - 12 min read

### [Unveiling RIFT: Enhancing Rust malware analysis through pattern matching](https://www.microsoft.com/en-us/security/blog/2025/06/27/unveiling-rift-enhancing-rust-malware-analysis-through-pattern-matching/)

As threat actors are adopting Rust for malware development, RIFT, an open-source tool, helps reverse engineers analyze Rust malware, solving challenges in the security industry.

- ![A graphic showing a store with a window and numbers.](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2025/04/MSFT_CyberSignals_9thEdition_MicrositeCoverImageSecurityReport.png)









  - April 16, 2025
  - 12 min read

### [Cyber Signals Issue 9 \| AI-powered deception: Emerging fraud threats and countermeasures](https://www.microsoft.com/en-us/security/blog/2025/04/16/cyber-signals-issue-9-ai-powered-deception-emerging-fraud-threats-and-countermeasures/)

Microsoft maintains a continuous effort to protect its platforms and customers from fraud and abuse.

- ![A woman using a laptop](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2025/04/Node-js-malware-featured.png)









  - April 15, 2025
  - 10 min read

### [Threat actors misuse Node.js to deliver malware and other malicious payloads](https://www.microsoft.com/en-us/security/blog/2025/04/15/threat-actors-misuse-node-js-to-deliver-malware-and-other-malicious-payloads/)

Since October 2024, Microsoft Defender Experts has observed and helped multiple customers address campaigns leveraging Node.

![](https://www.microsoft.com/en-us/security/blog/wp-content/themes/security-blog-2025/dist/images/bg-footer.png)

![](https://www.microsoft.com/en-us/security/blog/wp-content/themes/security-blog-2025/dist/images/bg-footer.png)

## Get started with Microsoft Security

Protect your people, data, and infrastructure with AI-powered, end-to-end security from Microsoft.

[Learn how](https://www.microsoft.com/en-us/security?wt.mc_id=AID730391_QSG_BLOG_319247&ocid=AID730391_QSG_BLOG_319247)

![](https://www.microsoft.com/en-us/security/blog/wp-content/themes/security-blog-2025/dist/images/footer-promotional.jpg)

Connect with us on social

- [X](https://twitter.com/msftsecurity)
- [YouTube](https://www.youtube.com/channel/UC4s3tv0Qq_OSUBfR735Jc6A)
- [LinkedIn](https://www.linkedin.com/showcase/microsoft-security/)