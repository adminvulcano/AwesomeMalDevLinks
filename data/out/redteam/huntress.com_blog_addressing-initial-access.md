# https://www.huntress.com/blog/addressing-initial-access

![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F9f33356fc04f46a2ac4a68753ba41658)

[Home](https://www.huntress.com/)![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F779e332a141048329fb98c924119138a) [Blog](https://www.huntress.com/blog) ![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F779e332a141048329fb98c924119138a)

Addressing Initial Access

Published:

[March 16, 2023](https://www.huntress.com/)

# Addressing Initial Access

By:

[![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Ffa69b31eae1e4264b7c12bcfa5e0f9a5)\\
Harlan Carvey](https://www.huntress.com/authors/harlan-carvey)

[![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F96ce13bf128a4d35ae6cc645eb2cbb0d)\\
Dray Agha](https://www.huntress.com/authors/dray-agha)

Contributors:

Special thanks to our Contributors:

[Team Huntress](https://www.huntress.com/authors/team-huntress)

![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fbe999d11243f4569929bf0e05f7d8b70)

![Share icon](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fe499a4a7ecac4052ab9e5c194b638f16)

![Glitch effect](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fc2118b00ed614bbf83f96f25de0beaf8)![Glitch effect](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fc2118b00ed614bbf83f96f25de0beaf8)![Glitch effect](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F0658aac7c84b4f7e9a7c7b2a5b519b28)

See Huntress in action.

## Engineering Defence

In February 2022, Microsoft announced that due to how pervasive the use of “weaponized” documents were, they were going to block macros in MS Office documents downloaded from the Internet by default.

Following this announcement, some threat actors sought alternate means for gaining **initial access \[** [**TA0001**](https://attack.mitre.org/tactics/TA0001/) **\]** to systems through **phishing** campaigns, and several settled on the use of **disk image files**(i.e., files with ISO, IMG, VHD, or VHDX extensions) as, at the time, malware delivered via this means bypassed security restrictions. Then, towards the end of 2022, we started seeing malware, such as **Qakbot,** delivered via malicious **OneNote** files.

However, much like the “changes” Microsoft sought to implement, there are settings that organizations can make, via Group Policy Objects (GPOs) or directly via the Windows Registry, to protect themselves, and to significantly inhibit or even obviate attempts to gain initial access. In this short Huntress article, **we share some PowerShell one-liners you can deploy with ease to engineer these defences via the Registry.** _You can copy/paste the PowerShell code provided in this blog post with no modifications_, we’ve done all the hard work for you.

## Disrupt OneNote Malware

With respect to OneNote files, an option for protecting your infrastructure is simply to remove the OneNote application from endpoints if there is no business use for this application.

If OneNote is required, however, then there are two settings that can be made to endpoints to enhance the security posture and repudiate attacks via files embedded within OneNote files:

|     |     |
| --- | --- |
|  | #Run as Administrator, copy/paste the below |
|  |  |
|  | # Mount HKU |
|  | mount -PSProvider Registry -Name HKU -Root HKEY\_USERS; |
|  |  |
|  | # Loop through each HKU/user's HKCU, AND deploy OneNote defences |
|  | (gci -path "HKU:\\\*\\Software\\Microsoft\\Office\\\*\\OneNote\\Options\").PsPath \| |
|  | Foreach-Object {New-ItemProperty-Path $\_-Name "disableembeddedfiles"-Value 1-type DWORD -verbose}; |
|  |  |
|  | (gci -path "HKU:\\\*\\Software\\Microsoft\\Office\\\*\\OneNote\\Options\").PsPath \| |
|  | Foreach-Object {New-Item-Path "$\_\\embeddedfileopenoptions"-verbose}; |
|  |  |
|  | (gci -path "HKU:\\\*\\Software\\Microsoft\\Office\\\*\\OneNote\\Options\").PsPath \| |
|  | Foreach-Object {New-ItemProperty-Path "$\_\\embeddedfileopenoptions"-Name "blockedextensions"-type string -value ".js;.exe;.bat;.vbs;.com;.scr;.cmd;.ps1"-verbose} |

[view raw](https://gist.github.com/Purp1eW0lf/ef9371d317e268d40a769d143128652a/raw/bf63fe0629c745e90b9c3cc742364b084b2aa809/Deny_OneNote_Malware.ps1) [Deny\_OneNote\_Malware.ps1](https://gist.github.com/Purp1eW0lf/ef9371d317e268d40a769d143128652a#file-deny_onenote_malware-ps1)
hosted with ❤ by [GitHub](https://github.com/)

Deploying the suggested defences above **denies the user the ability to interact with the OneNote malware,** raising a dialog box with an error message to contact the IT team (sorry, helpdesk folk), as illustrated in figure 1.

![image3-1](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F65884369aeed4baf8d01c348efc25ef3)

**_Fig. 1: Error Message Triggered On User Interaction With Malicious OneNote File After Registry Modification_**

## Prevent Automatic Mounting

When threat actors shifted to deploying malware via disk image (ISO, IMG, VHD, VHDX) files, part of the reason they did so was because users could double-click and automatically mount those files, allowing them to immediately access and launch files embedded within those disk image files. Figure 2 illustrates what it looks like when a user automatically mounts a disk image file by double-clicking it, allowing them to execute the contents of the drive, detonating the malware.

![image2-1](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F11e2dd91af2a4502a94eacb6d84de262)

**_Fig. 2: Disk Image File Automatically Mounted_**

However, settings can be made to prevent users from accessing disk image files in this way, while still allowing them to access disk image files programmatically.  The commands to enable those settings are:

|     |     |
| --- | --- |
|  | #run as Administrator, copy/paste the below |
|  |  |
|  | New-ItemProperty-Path "HKLM:\\SOFTWARE\\Classes\\Windows.IsoFile\\shell\\mount"-Name "ProgrammaticAccessOnly"-type string -verbose; |
|  |  |
|  | New-ItemProperty-Path "HKLM:\\SOFTWARE\\Classes\\Windows.VhdFile\\shell\\mount"-Name "ProgrammaticAccessOnly"-type string -verbose |

[view raw](https://gist.github.com/Purp1eW0lf/59de9a6ace3bb96246fcdf1e80345774/raw/b516206b9d1ea0af176793546f5256e19aaf5e15/Deny_Mounting.ps1) [Deny\_Mounting.ps1](https://gist.github.com/Purp1eW0lf/59de9a6ace3bb96246fcdf1e80345774#file-deny_mounting-ps1)
hosted with ❤ by [GitHub](https://github.com/)

With the Registry change implemented, **automatically mounting the disk image file via double-clicking** is no longer an option, and as such, the image file contents are not automatically available to the user. Instead, the innocuous ‘Disc Image Burner’ is the default option, as illustrated in figure 3, neutralizing the opportunity for the malware to enroll the user in its execution.

![image5-1](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F84110f91c3c34716ba8ac0495c7094b6)

**_Fig. 3: Default Option Following Recommended Defensive Registry Modifications_**

## Block Macros

Macros embedded in MS Office files can be a tricky subject. Some organizations embed macros in Word documents and Excel spreadsheets, and share them via the Internet as part of their legitimate business processes. However, threat actors have used, and continue to use this functionality to gain initial access into enterprise environments. The change in default behavior that Microsoft announced in February 2022 could be implemented as a GPO, or a Registry modification.

In order to **disable** **macros** from executing within MS Office (Excel, PowerPoint, Word) files **downloaded from the Internet**, you can use the below Powershell code to enable the necessary setting. Our suggested PowerShell code will loop through all users and applications, as illustrated in figure 4.

|     |     |
| --- | --- |
|  | #run as Administrator, copy/paste the below |
|  |  |
|  | # Mount HKU |
|  | mount -PSProvider Registry -Name HKU -Root HKEY\_USERS; |
|  |  |
|  | # Loop through each HKU/user's HKCU, loop though each Office version and application, and implement defences |
|  | (gci -path "HKU:\\\*\\Software\\Microsoft\\Office\\\*\\\*\\Security\").PsPath \| |
|  | Foreach-Object {Set-ItemProperty-path $\_-name "blockcontentexecutionfrominternet"-value 1-Type DWord -verbose} |

[view raw](https://gist.github.com/Purp1eW0lf/28776631fd731fa2418e80d96ab7f52d/raw/712888fc520ed051e41884f05377a78bbae47b50/Deny_MOTW_Files.ps1) [Deny\_MOTW\_Files.ps1](https://gist.github.com/Purp1eW0lf/28776631fd731fa2418e80d96ab7f52d#file-deny_motw_files-ps1)
hosted with ❤ by [GitHub](https://github.com/)

![image4](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F59048062d84e41dd9a13b9144e28018c)

**_Fig. 4: PowerShell Wildcard For Loop Through Each Office Application_**

## Conclusion: Engineering Hostility

Threat actors are well-known for leveraging default behaviors of systems and users to gain access to systems, obtain a foothold and then progress on from there, moving laterally or selling access to other threat actors.

However, **the suggested changes in this Huntress article** will help make your environment **hostile to adversarial attempts for initial access**. We have shared and curated some simple steps that you can take that are free, and will serve to transparently increase your security posture, and to significantly frustrate if not halt these attack chains.

### Notes on our PowerShell Methods

Elsewhere on the internet there is the suggestion that Office 365 Group Policy templates must specifically be downloaded and imported on a machine, to successfully administer a number of GPO changes to reduce your attack surface here.

On investigation \[ [1](https://www.microsoft.com/en-us/download/details.aspx?id=49030), [2](https://github.com/iothacker/Microsoft-Office-365-Business-Group-Policy-ADMX-Templates/blob/master/onent16-365.admx)\], these templates have the GPO point to specific Registry locations anyway, as shown in figure 5. Therefore, it saves time and overhead to directly write these Registry values ourselves and skip importing the templates, cutting out the middle-man as it were.

![image1](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fb9d946621fa24922a8a3bb755056099f)

**_Fig. 5: OneNote Group Policy .admx Template Lists Direct Registry Key_**

Moreover, by using PowerShell we gain a number of advantages. **First** is that we can leverage wildcards to fill in the blanks - meaning we needn’t know or ‘hard-code’ specific Office version numbers or even Office applications. **Second**, by using PowerShell we do not need every user’s Registry hives to be mounted (as “HKEY\_CURRENT\_USER”, or “HKCU”) and can instead access each user’s hive via a ‘for loop’ to make the necessary changes. **Third** and final, by leveraging PowerShell the way we have minimizes the administrator’s effort and maximizes ROI; simply run the PowerShell commands offered to make your environment more hostile to threat actors attempting to gain initial access.

**\\*\\*\\***

**Thanks to the contributors of this blog,** [**Harlan Carvey**](https://www.huntress.com/authors/harlan-carvey) **and** [**Dray Agha**](https://www.huntress.com/authors/dray-agha) **.**

1 [https://www.bleepingcomputer.com/news/microsoft/microsoft-plans-to-kill-malware-delivery-via-office-macros/](https://www.bleepingcomputer.com/news/microsoft/microsoft-plans-to-kill-malware-delivery-via-office-macros/)

2 [https://learn.microsoft.com/en-us/deployoffice/security/internet-macros-blocked](https://learn.microsoft.com/en-us/deployoffice/security/internet-macros-blocked)

3 [https://www.bleepingcomputer.com/news/security/how-to-prevent-microsoft-onenote-files-from-infecting-windows-with-malware/](https://www.bleepingcomputer.com/news/security/how-to-prevent-microsoft-onenote-files-from-infecting-windows-with-malware/)

4 [https://support.huntress.io/hc/en-us/articles/11477430445587](https://support.huntress.io/hc/en-us/articles/11477430445587)

5 [https://www.secureworks.com/research/the-curious-case-of-mia-ash](https://www.secureworks.com/research/the-curious-case-of-mia-ash)

6 [https://www.bleepingcomputer.com/news/microsoft/how-to-auto-block-macros-in-microsoft-office-docs-from-the-internet/](https://www.bleepingcomputer.com/news/microsoft/how-to-auto-block-macros-in-microsoft-office-docs-from-the-internet/)

![Glitch effect](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F97d1ebf9f67945c9af2c6341e585bc21)

## You Might Also Like

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fa24761509a8f4363840a74e944c546af?format=webp)\\
\\
**Brute Force or Something More? Ransomware Initial Access Brokers Exposed** \\
\\
Discover how a seemingly simple brute force attack led to the uncovering of a suspected ransomware-as-a-service operation. This ecosystem appears to be leveraged by initial access brokers, driving an illicit and complex network of cybercrime.\\
\\
Learn More](https://www.huntress.com/blog/brute-force-or-something-more-ransomware-initial-access-brokers-exposed)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F71736a89bd5a497b93e17c2f6ba5cd39)\\
\\
**ClickFix Gets Creative: Malware Buried in Images** \\
\\
Huntress uncovered an attack utilizing a ClickFix lure to initiate a multi-stage malware execution chain. This analysis reveals how threat actors use steganography to conceal infostealers like LummaC2 and Rhadamanthys within seemingly harmless PNGs.\\
\\
Learn More](https://www.huntress.com/blog/clickfix-malware-buried-in-images)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F0f1958b8347f4e10acaef1c39a35263d)\\
\\
**Supply Chain Compromise of axios npm Package** \\
\\
An NPM supply chain attack struck the ubiquitous open-source axios library and Huntress has observed over a hundred affected devices.\\
\\
Learn More](https://www.huntress.com/blog/supply-chain-compromise-axios-npm-package)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fe08f13bc961c434ca082024b58a4bf77)\\
\\
**defendnot? Defend YES! Detecting Malicious Security Product Bypass Techniques**\\
\\
"defendnot" bypasses Windows Defender using undocumented APIs. Learn detection strategies and robust defenses against this sophisticated evasion technique.\\
\\
Learn More](https://www.huntress.com/blog/defendnot-detecting-malicious-security-product-bypass-techniques)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fb4ebc0447fc34db1a4ca274e87f1ca92)\\
\\
**You Can Run, but You Can’t Hide: Defender Exclusions** \\
\\
Understand Windows Defender AntiVirus exclusions and how adversaries might leverage this capability to bypass scans.\\
\\
Learn More](https://www.huntress.com/blog/you-can-run-but-you-cant-hide-defender-exclusions)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F7e7c649ebb684f77b166569f03be9b08)\\
\\
**How OAuth 2.0 Device Code Phishing Works in Azure and Google** \\
\\
All OAuth 2.0 implementations are equal. Some are just more equal than others. This blog covers device code phishing and compares OAuth implementations between Google and Azure. Does OAuth implementation impact the efficacy of hacker tradecraft? Find out here!\\
\\
Learn More](https://www.huntress.com/blog/oh-auth-2-0-device-code-phishing-in-google-cloud-and-azure)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F64080726eb2c4eab87e38430974405e2)\\
\\
**Best Practices to Reduce Your Attack Surface** \\
\\
Read expert insights on how to strengthen your cybersecurity strategy with asset inventory and attack surface reduction.\\
\\
Learn More](https://www.huntress.com/blog/best-practices-to-reduce-your-attack-surface)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F63bc16db8b0d4d94ab28499cbb537a68)\\
\\
**Rapid Response: Microsoft Office RCE - “Follina” MSDT Attack** \\
\\
A new attack vector enables hackers to more easily compromise users with malicious Microsoft Office documents.\\
\\
Learn More](https://www.huntress.com/blog/microsoft-office-remote-code-execution-follina-msdt-bug)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fa24761509a8f4363840a74e944c546af?format=webp)\\
\\
**Brute Force or Something More? Ransomware Initial Access Brokers Exposed** \\
\\
Discover how a seemingly simple brute force attack led to the uncovering of a suspected ransomware-as-a-service operation. This ecosystem appears to be leveraged by initial access brokers, driving an illicit and complex network of cybercrime.\\
\\
Learn More](https://www.huntress.com/blog/brute-force-or-something-more-ransomware-initial-access-brokers-exposed)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F71736a89bd5a497b93e17c2f6ba5cd39)\\
\\
**ClickFix Gets Creative: Malware Buried in Images** \\
\\
Huntress uncovered an attack utilizing a ClickFix lure to initiate a multi-stage malware execution chain. This analysis reveals how threat actors use steganography to conceal infostealers like LummaC2 and Rhadamanthys within seemingly harmless PNGs.\\
\\
Learn More](https://www.huntress.com/blog/clickfix-malware-buried-in-images)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F0f1958b8347f4e10acaef1c39a35263d)\\
\\
**Supply Chain Compromise of axios npm Package** \\
\\
An NPM supply chain attack struck the ubiquitous open-source axios library and Huntress has observed over a hundred affected devices.\\
\\
Learn More](https://www.huntress.com/blog/supply-chain-compromise-axios-npm-package)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fe08f13bc961c434ca082024b58a4bf77)\\
\\
**defendnot? Defend YES! Detecting Malicious Security Product Bypass Techniques**\\
\\
"defendnot" bypasses Windows Defender using undocumented APIs. Learn detection strategies and robust defenses against this sophisticated evasion technique.\\
\\
Learn More](https://www.huntress.com/blog/defendnot-detecting-malicious-security-product-bypass-techniques)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fb4ebc0447fc34db1a4ca274e87f1ca92)\\
\\
**You Can Run, but You Can’t Hide: Defender Exclusions** \\
\\
Understand Windows Defender AntiVirus exclusions and how adversaries might leverage this capability to bypass scans.\\
\\
Learn More](https://www.huntress.com/blog/you-can-run-but-you-cant-hide-defender-exclusions)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F7e7c649ebb684f77b166569f03be9b08)\\
\\
**How OAuth 2.0 Device Code Phishing Works in Azure and Google** \\
\\
All OAuth 2.0 implementations are equal. Some are just more equal than others. This blog covers device code phishing and compares OAuth implementations between Google and Azure. Does OAuth implementation impact the efficacy of hacker tradecraft? Find out here!\\
\\
Learn More](https://www.huntress.com/blog/oh-auth-2-0-device-code-phishing-in-google-cloud-and-azure)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F64080726eb2c4eab87e38430974405e2)\\
\\
**Best Practices to Reduce Your Attack Surface** \\
\\
Read expert insights on how to strengthen your cybersecurity strategy with asset inventory and attack surface reduction.\\
\\
Learn More](https://www.huntress.com/blog/best-practices-to-reduce-your-attack-surface)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F63bc16db8b0d4d94ab28499cbb537a68)\\
\\
**Rapid Response: Microsoft Office RCE - “Follina” MSDT Attack** \\
\\
A new attack vector enables hackers to more easily compromise users with malicious Microsoft Office documents.\\
\\
Learn More](https://www.huntress.com/blog/microsoft-office-remote-code-execution-follina-msdt-bug)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fa24761509a8f4363840a74e944c546af?format=webp)\\
\\
**Brute Force or Something More? Ransomware Initial Access Brokers Exposed** \\
\\
Discover how a seemingly simple brute force attack led to the uncovering of a suspected ransomware-as-a-service operation. This ecosystem appears to be leveraged by initial access brokers, driving an illicit and complex network of cybercrime.\\
\\
Learn More](https://www.huntress.com/blog/brute-force-or-something-more-ransomware-initial-access-brokers-exposed)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F71736a89bd5a497b93e17c2f6ba5cd39)\\
\\
**ClickFix Gets Creative: Malware Buried in Images** \\
\\
Huntress uncovered an attack utilizing a ClickFix lure to initiate a multi-stage malware execution chain. This analysis reveals how threat actors use steganography to conceal infostealers like LummaC2 and Rhadamanthys within seemingly harmless PNGs.\\
\\
Learn More](https://www.huntress.com/blog/clickfix-malware-buried-in-images)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F0f1958b8347f4e10acaef1c39a35263d)\\
\\
**Supply Chain Compromise of axios npm Package** \\
\\
An NPM supply chain attack struck the ubiquitous open-source axios library and Huntress has observed over a hundred affected devices.\\
\\
Learn More](https://www.huntress.com/blog/supply-chain-compromise-axios-npm-package)

- [![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fe08f13bc961c434ca082024b58a4bf77)\\
\\
**defendnot? Defend YES! Detecting Malicious Security Product Bypass Techniques**\\
\\
"defendnot" bypasses Windows Defender using undocumented APIs. Learn detection strategies and robust defenses against this sophisticated evasion technique.\\
\\
Learn More](https://www.huntress.com/blog/defendnot-detecting-malicious-security-product-bypass-techniques)


![Green arrow left](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F7931d9d4a9f04879807e4aa007bab741)![Green arrow right](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fa287ab8ec0524100bdb223e1623f44d8)

![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fe4c269018ce94700a59e351c5b9edb99)![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F1aa59311842f4ca6bda70300ff181cf9)![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2F9ad6bcb77d1842b98142269ef70c4f47)

## Sign Up for Huntress Updates

Get insider access to Huntress tradecraft, killer events, and the freshest blog updates.

Business Email\*

[Privacy](https://www.cloudflare.com/privacypolicy/) • [Terms](https://www.cloudflare.com/website-terms/)

Submit

By submitting this form, you accept our [Terms of Service](https://www.huntress.com/terms-of-use)& [Privacy Policy](https://www.huntress.com/privacy-policy)

![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fcb5efa5143804ba59d530a903d29fe5f)

![](https://cdn.builder.io/api/v1/pixel?apiKey=3eb6f92aedf74f109c7b4b0897ec39a8)

Keep me in the loop![](https://cdn.builder.io/api/v1/image/assets%2F3eb6f92aedf74f109c7b4b0897ec39a8%2Fd90a8ce3aab44183b0b10892ebab15c1)

a5179843176824832.cdn.optimizely.com

# a5179843176824832.cdn.optimizely.com is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)

Qualified