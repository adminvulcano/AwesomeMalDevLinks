# https://www.microsoft.com/en-us/security/blog/2018/03/07/behavior-monitoring-combined-with-machine-learning-spoils-a-massive-dofoil-coin-mining-campaign/

[Skip to content](https://www.microsoft.com/en-us/security/blog/2018/03/07/behavior-monitoring-combined-with-machine-learning-spoils-a-massive-dofoil-coin-mining-campaign/#wp--skip-link--target)

 [Skip to content](https://www.microsoft.com/en-us/security/blog/2018/03/07/behavior-monitoring-combined-with-machine-learning-spoils-a-massive-dofoil-coin-mining-campaign/#wp--skip-link--target)

![](https://www.microsoft.com/en-us/security/blog/wp-content/themes/security-blog-2025/dist/images/single-bg.jpg)

![](https://www.microsoft.com/en-us/security/blog/wp-content/themes/security-blog-2025/dist/images/single-bg-dark.jpg)

* * *

## Share

- [Link copied to clipboard!](https://www.microsoft.com/en-us/security/blog/2018/03/07/behavior-monitoring-combined-with-machine-learning-spoils-a-massive-dofoil-coin-mining-campaign/)
- [Share on Facebook](https://www.facebook.com/sharer/sharer.php?u=https://www.microsoft.com/en-us/security/blog/2018/03/07/behavior-monitoring-combined-with-machine-learning-spoils-a-massive-dofoil-coin-mining-campaign/)
- [Share on X](https://twitter.com/intent/tweet?url=https://www.microsoft.com/en-us/security/blog/2018/03/07/behavior-monitoring-combined-with-machine-learning-spoils-a-massive-dofoil-coin-mining-campaign/&text=Behavior+monitoring+combined+with+machine+learning+spoils+a+massive+Dofoil+coin+mining+campaign)
- [Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https://www.microsoft.com/en-us/security/blog/2018/03/07/behavior-monitoring-combined-with-machine-learning-spoils-a-massive-dofoil-coin-mining-campaign/)

## Content types

- [Research](https://www.microsoft.com/en-us/security/blog/content-type/research/)

## Topics

- [Threat intelligence](https://www.microsoft.com/en-us/security/blog/topic/threat-intelligence/)

**Update:** Further analysis of this campaign points to a poisoned update for a peer-to-peer (P2P) application. For more information, read **[Poisoned peer-to-peer app kicked off Dofoil coin miner outbreak](https://cloudblogs.microsoft.com/microsoftsecure/2018/03/13/poisoned-peer-to-peer-app-kicked-off-dofoil-coin-miner-outbreak/)**. To detect and respond to Dofoil in corporate networks, read [**Hunting down Dofoil with Windows Defender ATP**](https://cloudblogs.microsoft.com/microsoftsecure/2018/04/04/hunting-down-dofoil-with-windows-defender-atp/).

Just before noon on March 6 (PST), Windows Defender Antivirus blocked more than 80,000 instances of several sophisticated trojans that exhibited advanced cross-process injection techniques, persistence mechanisms, and evasion methods. Behavior-based signals coupled with cloud-powered machine learning models uncovered this new wave of infection attempts. The trojans, which are new variants of Dofoil (also known as Smoke Loader), carry a [coin miner](https://cloudblogs.microsoft.com/microsoftsecure/2018/03/13/invisible-resource-thieves-the-increasing-threat-of-cryptocurrency-miners/) payload. Within the next 12 hours, more than 400,000 instances were recorded, 73% of which were in Russia. Turkey accounted for 18% and Ukraine 4% of the global encounters.

![Figure 1: Windows Defender ATP machine timeline view with Windows Defender Exploit Guard event](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2018/03/dofoil.png)

_Figure 1: Geographic distribution of the Dofoil attack components_

Windows Defender AV initially flagged the attack’s unusual persistence mechanism through behavior monitoring, which immediately sent this behavior-based signal to our cloud protection service.

1. Within milliseconds, multiple metadata-based machine learning models in the cloud started blocking these threats at first sight.
2. Seconds later, our sample-based and detonation-based machine learning models also verified the malicious classification. Within minutes, detonation-based models chimed in and added additional confirmation.
3. Within minutes, an anomaly detection alert notified us about a new potential outbreak.
4. After analysis, our response team updated the classification name of this new surge of threats to the proper malware families. People affected by these infection attempts early in the campaign would have seen blocks under machine learning names like Fuery, Fuerboos, Cloxer, or Azden. Later blocks show as the proper family names, Dofoil or Coinminer.

Windows 10, Windows 8.1, and Windows 7 users running Windows Defender AV or Microsoft Security Essentials are all protected from this latest outbreak.

![Figure 2. Layered machine learning defenses in Windows Defender AV](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2018/03/dofoil-ml.png)

_Figure 2. Layered machine learning defenses in Windows Defender AV_

Artificial intelligence and behavior-based detection in Windows Defender AV has become one of the mainstays of our defense system. The AI-based pre-emptive protection provided against this attack is similar to how layered machine learning defenses stopped an [Emotet outbreak](https://cloudblogs.microsoft.com/microsoftsecure/2018/02/14/how-artificial-intelligence-stopped-an-emotet-outbreak/) last month.

## Code injection and coin mining

Dofoil is the latest malware family to incorporate coin miners in attacks. Because the value of Bitcoin and other cryptocurrencies continues to grow, malware operators see the opportunity to include coin mining components in their attacks. For example, exploit kits are now delivering coin miners instead of ransomware. Scammers are adding coin mining scripts in tech support scam websites. And certain banking trojan families added coin mining behavior.

![Figure 3. Windows Defender ATP detection for process hollowing](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2018/03/1-process-hollowing-5aa05c09f3fe0-1024x531.png)

The Dofoil campaign we detected on March 6 started with a trojan that performs [process hollowing](https://cloudblogs.microsoft.com/microsoftsecure/2017/07/12/detecting-stealthier-cross-process-injection-techniques-with-windows-defender-atp-process-hollowing-and-atom-bombing/) on _explorer.exe._ Process hollowing is a code injection technique that involves spawning a new instance of legitimate process (in this case _c:\\windows\\syswow64\\explorer.exe_) and then replacing the legitimate code with malware.

_Figure 3. Windows Defender ATP detection for process hollowing (SHA-256: d191ee5b20ec95fe65d6708cbb01a6ce72374b309c9bfb7462206a0c7e039f4d, detected by Windows Defender AV_ _a_ _s [TrojanDownloader:Win32/Dofoil.AB](https://www.microsoft.com/en-us/wdsi/threats/malware-encyclopedia-description?Name=TrojanDownloader:Win32/Dofoil.AB)_)

The hollowed explorer.exe process then spins up a second malicious instance, which drops and runs a coin mining malware masquerading as a legitimate Windows binary, wuauclt.exe.

![Figure 4. Windows Defender ATP detection for coin mining malware ](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2018/03/2-coin-mining-5aa05cb75752d-1024x553.png)

_Figure 4. Windows Defender ATP detection for coin mining malware (SHA-256: 2b83c69cf32c5f8f43ec2895ec9ac730bf73e1b2f37e44a3cf8ce814fb51f120, detected by Windows Defender AV_ _as_ [_Trojan:Win32/CoinMiner.D_](https://www.microsoft.com/en-us/wdsi/threats/malware-encyclopedia-description?Name=Trojan:Win32/CoinMiner.D))

Even though it uses the name of a legitimate Windows binary, it’s running from the wrong location. The command line is anomalous compared to the legitimate binary. Additionally, the network traffic from this binary is suspicious.

![Windows Defender ATP alert process tree showing anomalous IP communications](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2018/03/3-IP-comms.png)

_Figure 5. Windows Defender ATP alert process tree showing anomalous IP communications_

![Windows Defender ATP showing suspicious network activity ](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2018/03/dofoil-suspicious-network-activity.png)

_Figure 6. Windows Defender ATP showing suspicious network activity_

![Windows Defender ATP alert process tree](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2018/03/Figure-7.png)

_Figure 7. Windows Defender ATP alert process tree showing hollowed explorer.exe process making suspicious connections_

Dofoil uses a customized mining application. Based on its code, the coin miner supports NiceHash, which means it can mine different cryptocurrencies. The samples we analyzed mined Electroneum coins.

## Persistence

For coin miner malware, persistence is key. These types of malware employ various techniques to stay undetected for long periods of time in order to mine coins using stolen computer resources.

To stay hidden, Dofoil modifies the registry. The hollowed _explorer.exe_ process creates a copy of the original malware in the Roaming AppData folder and renames it to _ditereah.exe_. It then creates a registry key or modifies an existing one to point to the newly created malware copy. In the sample we analyzed, the malware modified the OneDrive Run key.

![Figure 8. Windows Defender ATP alert process tree showing creation of new malware process](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2018/03/3-persistence-1.png)![Windows Defender ATP alert process tree showing creation of new malware process ](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2018/03/5-persistence-one-drive.png)

_Figure 8. Windows Defender ATP alert process tree showing creation of new malware process (SHA-256: d191ee5b20ec95fe65d6708cbb01a6ce72374b309c9bfb7462206a0c7e039f4d) and registry modification_

## Command-and-control communication

Dofoil is an enduring family of trojan downloaders. These connect to command and control (C&C) servers to listen for commands to download and install malware. In the March 6 campaign, Dofoil’s C&C communication involves the use of the decentralized [Namecoin](https://www.namecoin.org/) network infrastructure .

The hollowed _explorer.exe_ process writes and runs another binary, _D1C6.tmp.exe_ ( _SHA256: 5f3efdc65551edb0122ab2c40738c48b677b1058f7dfcdb86b05af42a2d8299c_) into the _Temp_ folder.  _D1C6.tmp.exe_ then drops and executes a copy of itself named _lyk.exe_. Once running, _lyk.exe_ connects to IP addresses that act as DNS proxy servers for the Namecoin network. It then attempts to connect to the C&C server _vinik.bit_ inside the NameCoin infrastructure. The C&C server commands the malware to connect or disconnect to an IP address; download a file from a certain URL and execute or terminate the specific file; or sleep for a period of time.

![ Windows Defender ATP alert process tree showing creation of the temporary file, D1C6.tmp.exe](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2018/03/dofoil-explorer.png)![Figure 9. Windows Defender ATP alert process tree showing creation of the temporary file, D1C6.tmp.exe ](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2018/03/dofoil-d1c6.png)

_Figure 9. Windows Defender ATP alert process tree showing creation of the temporary file, D1C6.tmp.exe (SHA256: 5f3efdc65551edb0122ab2c40738c48b677b1058f7dfcdb86b05af42a2d8299c)_ _Figure 10. Windows Defender ATP alert process tree showing lyk.exe connecting to IP addresses_

## Stay protected with Windows 10

With the rise in valuation of cryptocurrencies, cybercriminal groups are launching more and more attacks to infiltrate networks and quietly mine for coins.

[Windows Defender AV](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-antivirus/windows-defender-antivirus-in-windows-10?ocid=cx-blog-mmpc)’s layered approach to security, which uses behavior-based detection algorithms, generics, and heuristics, as well as machine learning models in both the client and the cloud, provides real-time protection against new threats and outbreaks.

As demonstrated, Windows Defender Advanced Threat Protection ( [Windows Defender ATP](https://www.microsoft.com/en-us/WindowsForBusiness/windows-atp?ocid=cx-blog-mmpc)) flags malicious behaviors related to installation, code injection, persistence mechanisms, and coin mining activities. Security operations can use the rich detection libraries in Windows Defender ATP to detect and respond to anomalous activities in the network. Windows Defender ATP also integrates protections from Windows Defender AV, Windows Defender Exploit Guard, and Windows Defender Application Guard, providing a seamless security management experience.

To test how Windows Defender ATP can help your organization detect, investigate, and respond to advanced attacks, **[sign up for a free trial](https://www.microsoft.com/en-us/windowsforbusiness/windows-atp?ocid=cx-blog-mmpc)**.

[Windows 10 S](https://www.microsoft.com/en-us/windows/windows-10-s?ocid=cx-blog-mmpc), a special configuration of Windows 10, helps protect against coin miners and other threats. Windows 10 S works exclusively with apps from the Microsoft Store and uses Microsoft Edge as the default browser, providing Microsoft verified security.

_Windows Defender Research_

* * *

## **Talk to us**

Questions, concerns, or insights on this story? Join discussions at the [Microsoft community](https://answers.microsoft.com/en-us/protect) and [Windows Defender Security Intelligence](https://www.microsoft.com/en-us/wdsi).

Follow us on Twitter [@WDSecurity](https://twitter.com/WDSecurity) and Facebook [Windows Defender Security Intelligence](https://www.facebook.com/MsftWDSI/).

![](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2018/01/windows-defender-security-intelligence-300x300.png)

## Microsoft Defender Security Research Team

[See Microsoft Defender Security Research Team posts](https://www.microsoft.com/en-us/security/blog/author/windows-defender-research/)

## Related posts

- ![A woman sitting at a desk using a laptop](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2025/04/Threat-landscape-containers-featured.png)









  - April 23, 2025
  - 14 min read

### [Understanding the threat landscape for Kubernetes and containerized assets](https://www.microsoft.com/en-us/security/blog/2025/04/23/understanding-the-threat-landscape-for-kubernetes-and-containerized-assets/)

The dynamic nature of containers can make it challenging for security teams to detect runtime anomalies or pinpoint the source of a security incident, presenting an opportunity for attackers to stay undetected.

- ![Operations manager working at standing desk.](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2024/04/OpenMetadata-exploitation.png)









  - April 17, 2024
  - 4 min read

### [Attackers exploiting new critical OpenMetadata vulnerabilities on Kubernetes clusters](https://www.microsoft.com/en-us/security/blog/2024/04/17/attackers-exploiting-new-critical-openmetadata-vulnerabilities-on-kubernetes-clusters/)

Microsoft recently uncovered an attack that exploits new critical vulnerabilities in OpenMetadata to gain access to Kubernetes workloads and leverage them for cryptomining activity.

- ![Two male engineers sitting in front of a computer screen.](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2023/12/MSC16_slalom_014.jpg)









  - December 12, 2023
  - 16 min read

### [Threat actors misuse OAuth applications to automate financially driven attacks](https://www.microsoft.com/en-us/security/blog/2023/12/12/threat-actors-misuse-oauth-applications-to-automate-financially-driven-attacks/)

Microsoft Threat Intelligence presents cases of threat actors misusing OAuth applications as automation tools in financially motivated attacks.

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