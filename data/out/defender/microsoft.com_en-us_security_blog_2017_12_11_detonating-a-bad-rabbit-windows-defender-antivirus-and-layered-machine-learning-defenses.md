# https://www.microsoft.com/en-us/security/blog/2017/12/11/detonating-a-bad-rabbit-windows-defender-antivirus-and-layered-machine-learning-defenses/

[Skip to content](https://www.microsoft.com/en-us/security/blog/2017/12/11/detonating-a-bad-rabbit-windows-defender-antivirus-and-layered-machine-learning-defenses/#wp--skip-link--target)

 [Skip to content](https://www.microsoft.com/en-us/security/blog/2017/12/11/detonating-a-bad-rabbit-windows-defender-antivirus-and-layered-machine-learning-defenses/#wp--skip-link--target)

![](https://www.microsoft.com/en-us/security/blog/wp-content/themes/security-blog-2025/dist/images/single-bg.jpg)

![](https://www.microsoft.com/en-us/security/blog/wp-content/themes/security-blog-2025/dist/images/single-bg-dark.jpg)

* * *

## Share

- [Link copied to clipboard!](https://www.microsoft.com/en-us/security/blog/2017/12/11/detonating-a-bad-rabbit-windows-defender-antivirus-and-layered-machine-learning-defenses/)
- [Share on Facebook](https://www.facebook.com/sharer/sharer.php?u=https://www.microsoft.com/en-us/security/blog/2017/12/11/detonating-a-bad-rabbit-windows-defender-antivirus-and-layered-machine-learning-defenses/)
- [Share on X](https://twitter.com/intent/tweet?url=https://www.microsoft.com/en-us/security/blog/2017/12/11/detonating-a-bad-rabbit-windows-defender-antivirus-and-layered-machine-learning-defenses/&text=Detonating+a+bad+rabbit%3A+Windows+Defender+Antivirus+and+layered+machine+learning+defenses)
- [Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https://www.microsoft.com/en-us/security/blog/2017/12/11/detonating-a-bad-rabbit-windows-defender-antivirus-and-layered-machine-learning-defenses/)

## Content types

- [Research](https://www.microsoft.com/en-us/security/blog/content-type/research/)

## Products and services

- [Microsoft Defender](https://www.microsoft.com/en-us/security/blog/product/microsoft-defender/)

## Topics

- [Threat intelligence](https://www.microsoft.com/en-us/security/blog/topic/threat-intelligence/)

Windows Defender Antivirus uses a layered approach to protection: tiers of advanced automation and machine learning models evaluate files in order to reach a verdict on suspected malware. While [Windows Defender AV](https://www.microsoft.com/en-us/windows/windows-defender?ocid=cx-blog-mmpc) detects a vast majority of new malware files at first sight, we always strive to further close the gap between malware release and detection.

In a [previous blog post](https://blogs.technet.microsoft.com/mmpc/2017/07/18/windows-defender-antivirus-cloud-protection-service-advanced-real-time-defense-against-never-before-seen-malware?ocid=cx-blog-mmpc), we looked at a real-world case study showing how Windows Defender Antivirus cloud protection service leverages [next-gen security technologies](https://blogs.technet.microsoft.com/mmpc/2017/05/08/antivirus-evolved?ocid=cx-blog-mmpc) to save “patient zero” from new malware threats in real-time. In that case study, a new Spora ransomware variant was analyzed and blocked within seconds using a deep neural network (DNN) machine learning classifier in the cloud. In this blog post we’ll look at how additional automated analysis and machine learning models can further protect customers within minutes in rare cases where initial classification is inconclusive.

## Layered machine learning models

In Windows Defender AV’s layered approach to defense, if the first layer doesn’t detect a threat, we move on to the next level of inspection. As we move down the layers, the amount of time required increases. However, we catch the vast majority of malware at the first (fastest) protection layers and only need to move on to a more sophisticated (but slower) level of inspection for rarer/more advanced threats.

For example, the vast majority of scanned objects are evaluated by the local Windows Defender client machine learning models, behavior-based detection algorithms, generic and heuristic classifications, and more. This helps ensure that users get the best possible performance. In rare cases where local intelligence can’t reach a definitive verdict, Windows Defender AV will use the cloud for deeper analysis.

## Detonation-based machine learning classification

We use a variety of machine learning models that use different algorithms to predict whether a certain file is malware. Some of these algorithms are binary classifiers that give a strict clean-or-malware verdict (0 or 1), while others are multi-class classifiers that provide a probability for each classification (malware, clean, potentially unwanted application, etc). Each machine learning model is trained against a set of different features (often thousands, sometimes hundreds of thousands) to learn to distinguish between different kinds of programs.

For the fastest classifiers in our layered stack, the features may include static attributes of the file combined with events (for example, API calls or behaviors) seen while the scanning engine emulates the file using dynamic translation. If the results from these models are inconclusive, we’ll take an even more in-depth look at what the malware does by actually executing it in a sandbox and observing its run-time behavior. This is known as dynamic analysis, or detonation, and happens automatically whenever we receive a new suspected malware sample.

The activities seen in the sandbox machine (for example, registry changes, file creation/deletion, process injection, network connections, and so forth) are recorded and provided as features to our ML models. These models can then combine both the static features obtained from scanning the file with the dynamic features observed during detonation to arrive at an even stronger prediction.

### Ransom:Win32/Tibbar.A – _Protection in 14 minutes_

On October 24, 2017, in the wake of recent ransomware outbreaks such as Wannacry and NotPetya, [news broke](https://www.bleepingcomputer.com/news/security/bad-rabbit-ransomware-outbreak-hits-eastern-europe/) of a new threat spreading, primarily in Ukraine and Russia: Ransom:Win32/Tibbar.A (popularly known as Bad Rabbit).

This threat is a good example of how detonation-based machine learning came into play to protect Windows Defender AV customers. First though, let’s look at what happened to patient zero.

At 11:17 a.m. local time on October 24, a user running Windows Defender AV in St. Petersburg, Russia was tricked into downloading a file named _FlashUtil.exe_ from a malicious website. Instead of a Flash update, the program was really the just-released Tibbar ransomware.

Windows Defender AV scanned the file and determined that it was suspicious. A query was sent to the cloud protection service, where several metadata-based machine learning models found the file suspicious, but not with a high enough probability to block. The cloud protection service requested that Windows Defender AV client to lock the file, upload it for processing, and wait for a decision.

Within a few seconds the file was processed, and sample-analysis-based ML models returned their conclusions. In this case, a multi-class deep neural network (DNN) machine learning classifier correctly classified the Tibbar sample as malware, but with only an 81.6% probability score. In order to avoid false positives, cloud protection service is configured by default to require at least 90% probability to block the malware (these thresholds are continually evaluated and fine-tuned to find the right balance between blocking malware while avoiding the blocking of legitimate programs). In this case, the ransomware was allowed to run.

### Detonation chamber

In the meantime, while patient zero and eight other unfortunate victims (in Ukraine, Russia, Israel, and Bulgaria) contemplated whether to pay the ransom, the sample was detonated and details of the system changes made by the ransomware were recorded.

As soon as the detonation results were available, a multi-class deep neural network (DNN) classifier that used both static and dynamic features evaluated the results and classified the sample as malware with 90.7% confidence, high enough for the cloud to start blocking.

When a tenth Windows Defender AV customer in the Ukraine was tricked into downloading the ransomware at 11:31 a.m. local time, 14 minutes after the first encounter, cloud protection service used the detonation-based malware classification to immediately block the file and protect the customer.

At this point the cloud protection service had “learned” that this file was malware. It now only required metadata from the client with the hash of the file to issue blocking decisions and protect customers. As the attack gained momentum and began to spread, Windows Defender AV customers with cloud protection enabled were protected. Later, a more specific detection was released to identify the malware as Ransom:Win32/Tibbar.A.

## Closing the gap

While we feel good about Windows Defender AV’s layered approach to protection, digging deeper and deeper with automation and machine learning in order to finally reach a verdict on suspected malware, we are continually seeking to close the gap even further between malware release and protection. The cases where we cannot block at first sight are increasingly rare, but there is so much to be done. As our machine learning models are continuously updated and retrained, we are able to make better predictions over time. Yet malware authors will not rest, and the ever-changing threat landscape requires continuous investment in new and better technologies to detect new threats, but also to effectively differentiate the good from the bad.

What about systems that do get infected while detonation and classification are underway? One area that we’re actively investing in is advanced remediation techniques that will let us reach back out to those systems in an organization that were vulnerable and, if possible, get them back to a healthy state.

If you are organization that is willing to accept a higher false positive risk in exchange for stronger protection, you can [configure the cloud protection level](https://docs.microsoft.com/en-us/windows/client-management/mdm/policy-csp-defender#defender-cloudblocklevel) to tell the Windows Defender AV cloud protection service to take a more aggressive stance towards suspicious files, such as blocking at lower machine learning probability thresholds. In the Tibbar example above, for example, a configuration like this could have protected patient zero using the initial 81% confidence score, and not wait for the higher confidence (detonation-based) result that came later. You can also [configure the cloud extended timeout](https://docs.microsoft.com/en-us/windows/client-management/mdm/policy-csp-defender#defender-cloudextendedtimeout) to give the cloud protection service more time to evaluate a first-seen threat.

As another layer of real-time protection against ransomware, [enable Controlled folder access](https://blogs.technet.microsoft.com/mmpc/2017/10/23/stopping-ransomware-where-it-counts-protecting-your-data-with-controlled-folder-access/), which is one of the features of the new [Windows Defender Exploit Guard](https://blogs.technet.microsoft.com/mmpc/2017/10/23/windows-defender-exploit-guard-reduce-the-attack-surface-against-next-generation-malware?ocid=cx-blog-mmpc). Controlled folder access protects files from tampering by locking folders so that ransomware and other unauthorized apps can’t access them.

For enterprises, Windows Defender Exploit Guard’s other features (Attack Surface Reduction, Exploit protection, and Network protection) further protect networks from advanced attacks. [Windows Defender Advanced Threat Protection](https://www.microsoft.com/en-us/WindowsForBusiness/windows-atp?ocid=cx-blog-mmpc) can also alert security operations personnel about malware activities in the network so that personnel can promptly investigate and respond to attacks.

To test how Windows Defender ATP can help your organization detect, investigate, and respond to advanced attacks, **[sign up for a free trial](https://www.microsoft.com/en-us/windowsforbusiness/windows-atp?ocid=cx-blog-mmpc)**.

For users running [Windows 10 S](https://www.microsoft.com/en-us/windows/windows-10-s?ocid=cx-blog-mmpc), malware like Tibbar simply won’t run. Windows 10 S provides advanced levels of security by exclusively running apps from the Microsoft Store. Threats such as Tibbar are non-issues for Windows 10 S users. [Learn more about Windows 10 S](https://support.microsoft.com/en-us/help/4020089/windows-10-s-faq).

New machine learning and AI techniques, in combination with both static and dynamic analysis, gives Windows Defender AV the ability to block more and more malware threats at first sight and, if that fails, learn as quickly as possible that something is bad and start blocking it. Using a layered approach, with different ML models at each layer, gives us the ability to target a wide variety of threats quickly while maintaining low false positive rates. As we gather more data about a potential threat, we can provide predictions with higher and higher confidence and take action accordingly. It is an exciting time to be in the fray.

**_Randy Treit_**

_Senior Security Researcher, Windows Defender Research_

* * *

## **Talk to us**

Questions, concerns, or insights on this story? Join discussions at the [Microsoft community](https://answers.microsoft.com/en-us/protect) and [Windows Defender Security Intelligence](https://www.microsoft.com/en-us/wdsi).

Follow us on Twitter [@WDSecurity](https://twitter.com/WDSecurity) and Facebook [Windows Defender Security Intelligence](https://www.facebook.com/MsftWDSI/).

![](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2018/01/windows-defender-security-intelligence-300x300.png)

## Microsoft Defender Security Research Team

[See Microsoft Defender Security Research Team posts](https://www.microsoft.com/en-us/security/blog/author/windows-defender-research/)

## Related posts

- ![Side profile of a woman wearing a dark shirt in a dim office reaching up and working on a Microsoft Surface Studio.](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2026/02/Threat-Modeling-AI-Applications--809x455.webp)









  - February 26
  - 8 min read

### [Threat modeling AI applications](https://www.microsoft.com/en-us/security/blog/2026/02/26/threat-modeling-ai-applications/)

AI threat modeling helps teams identify misuse, emergent risk, and failure modes in probabilistic and agentic AI systems.

- ![A colorful graphic showing a radar scanning icon representing new detection and hunting guidance.](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2026/02/MS_Actional-Insights_Detection-hunting-809x455.webp)









  - February 24
  - 14 min read

### [Developer-targeting campaign using malicious Next.js repositories](https://www.microsoft.com/en-us/security/blog/2026/02/24/c2-developer-targeting-campaign/)

A developer-targeting campaign leveraged malicious Next.

- ![](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2026/02/Running-OpenClaw-safely-identity-isolation-and-runtime-risk-809x455.webp)









  - February 19
  - 12 min read

### [Running OpenClaw safely: identity, isolation, and runtime risk](https://www.microsoft.com/en-us/security/blog/2026/02/19/running-openclaw-safely-identity-isolation-runtime-risk/)

Self-hosted agents execute code with durable credentials and process untrusted input.

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