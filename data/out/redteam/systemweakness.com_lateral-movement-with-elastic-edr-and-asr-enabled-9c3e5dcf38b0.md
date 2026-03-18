# https://systemweakness.com/lateral-movement-with-elastic-edr-and-asr-enabled-9c3e5dcf38b0

[Sitemap](https://systemweakness.com/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fsystemweakness.com%2Flateral-movement-with-elastic-edr-and-asr-enabled-9c3e5dcf38b0&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

Get app

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fsystemweakness.com%2Flateral-movement-with-elastic-edr-and-asr-enabled-9c3e5dcf38b0&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

[**System Weakness**](https://systemweakness.com/?source=post_page---publication_nav-f20a9840e177-9c3e5dcf38b0---------------------------------------)

·

Follow publication

[![System Weakness](https://miro.medium.com/v2/resize:fill:76:76/1*gncXIKhx5QOIX0K9MGcVkg.jpeg)](https://systemweakness.com/?source=post_page---post_publication_sidebar-f20a9840e177-9c3e5dcf38b0---------------------------------------)

System Weakness is a publication that specialises in publishing upcoming writers in cybersecurity and ethical hacking space. Our security experts write to make the cyber universe more secure, one vulnerability at a time.

Follow publication

# Bypassing Elastic EDR to Perform Lateral Movement

[![Ibad Altaf](https://miro.medium.com/v2/resize:fill:64:64/1*eTswarm8T0kTcSQgRzfz9Q.jpeg)](https://ibady01.medium.com/?source=post_page---byline--9c3e5dcf38b0---------------------------------------)

[Ibad Altaf](https://ibady01.medium.com/?source=post_page---byline--9c3e5dcf38b0---------------------------------------)

Follow

4 min read

·

Jul 5, 2024

36

1

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D9c3e5dcf38b0&operation=register&redirect=https%3A%2F%2Fsystemweakness.com%2Flateral-movement-with-elastic-edr-and-asr-enabled-9c3e5dcf38b0&source=---header_actions--9c3e5dcf38b0---------------------post_audio_button------------------)

Share

So, I have just recently started playing around with EDRs. As this would have been my first time testing an EDR, I wanted an open-source EDR solution, hence the reason for Elastic.

The preface of this article is to avoid EDR detections and perform lateral movement to another machine.

The lab setup is from Zeropointsecurity’s CRTO II course. So before we dig into that, there were some setups to the Cobalt Strike malleable profile, most of the configurations to evade Cobalt Strike related EDR detections were done using the techniques mentioned in the following [article](https://www.cobaltstrike.com/blog/cobalt-strike-and-yara-can-i-have-your-signature). There were some additional configurations apart from this as well, however, for the sake of the article’s title, I’ll avoid going into details.

Before explaining the evasion techniques, I’ll explain the scenario. So, we have 2 machines, WKSTN-1 and WKSTN-2. Both the machines have EDR agents deployed and WKSTN-2 has ASR enabled. A user has access to WKSTN-1 and is a local administrator on WKSTN-2. I need to perform lateral movement.

So first of all, I have to transfer my P2P beacon over SMB, which generates the following alert: [Potential Lateral Tool Transfer via SMB Share](https://www.elastic.co/guide/en/security/current/potential-lateral-tool-transfer-via-smb-share.html).

If we look at the rule query, we see that we can evade this rule by changing the magic bytes of our loader as well as the extension of it.

```
(file.Ext.header_bytes : "4d5a*" or file.extension : ("exe", "scr", "pif", "com", "dll"))] by process.entity_id
```

We can modify how the PE is loaded in the memory from our malleable C2 profile.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*XDe9I44gfbu7g9EWde1bcw.png)

Secondly, we’ll change the extension of our loader to .png. This way we can avoid this alert and transfer our loader from WKSTN-1 to WKSTN-2.

After transferring the file, if we were to change the extension of the file from .png to .exe, an alert will be generated: [Remote Execution via File Shares](https://www.elastic.co/guide/en/security/current/remote-execution-via-file-shares.html)

If we look at the query for this alert, we’ll hit the following ruleset

```
 process.pid == 4 and (file.extension : "exe" or file.Ext.header_bytes : "4d5a*")] by host.id, file.path
```

To evade this alert, what we can do is change the extension from .png to .scr. “.scr” is essentially an executable file used by Microsoft for screensavers.

After changing the extension, we can use SharpWMI to remotely execute WMI commands on the machine and try to execute this payload, however, another alert is generated: [WMI Incoming Lateral Movement](https://www.elastic.co/guide/en/security/current/wmi-incoming-lateral-movement.html).

After researching evasion techniques, I found another way to execute remote commands without the use of WMI. I won’t go into the details of this method, but you can read up on it [here](https://github.com/Mr-Un1k0d3r/SCShell). I loaded the scshell BOF in Cobalt Strike and executed the remote command, however, another new alert was generated: [System Shells via Services](https://www.elastic.co/guide/en/security/current/system-shells-via-services.html).

```
scshell 10.10.120.102 XblAuthManager "C:\windows\system32\cmd.exe /c C:\windows\CLSMBL.scr"
```

Reading upon this alert, it was clear that it was detected because the cmd.exe process was being executed remotely as a SYSTEM user.

```
  process.name : ("cmd.exe", "powershell.exe", "pwsh.exe", "powershell_ise.exe")
```

This alert was pretty easy to evade, and just directly executing the payload was enough.

```
scshell 10.10.120.102 XblAuthManager "C:\windows\CLSMBL.scr"
```

However, not all was well, yet another alert was generated: [Suspicious Execution via Windows Services](https://github.com/elastic/protections-artifacts/blob/main/behavior/rules/privilege_escalation_suspicious_execution_via_windows_services.toml).

## Get Ibad Altaf’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

After reviewing the ruleset for this alert, I noticed this exclusion:

![](https://miro.medium.com/v2/resize:fit:603/1*Sm9nDQ3VJKEH7JMFVKIZFA.png)

I changed the file path of where my loader was stored to _C:\\ProgramData\\Microsoft\\Search,_ executed the loader from there and got a Beacon. :D

## **Exploit Chain**

1. Verifying access to WKSTN-2

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*eHVr6eGEey-oPFSUiNPWpA.png)

2\. Upload the .png file to the **excluded** directory

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*CTGEjajZdqPbvT6m5EkCYQ.png)

3\. Cobalt Strike uses “fork and run” to execute commands, which gets detected by Elastic, so to avoid that I’m using an invariant unmanaged runspace PowerShell to change the extension to .scr. Since this will load “System.Management.Automation.dll”, we need to use a process that is known to load this DLL, which is why I have chosen msiexec.exe in my example.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*WrmeM2AUyzqfvSBf12QdJQ.png)

4\. Executing the remote file with scshell

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*ySDpX6fvn6MGebygRQqTZw.png)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*_GxuNDyywGB7g6UuZZzH1g.png)

5\. Connecting to the Beacon

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*zlxKFxkEG7s7kQ2b-Ad5CA.png)

### **Conclusion**

We were able to evade EDR alerts and perform lateral movement from WKSTN-1 to WKSTN-2.

## References

1. [https://www.cobaltstrike.com/blog/cobalt-strike-and-yara-can-i-have-your-signature](https://www.cobaltstrike.com/blog/cobalt-strike-and-yara-can-i-have-your-signature)
2. [https://securityintelligence.com/x-force/defining-cobalt-strike-reflective-loader/](https://securityintelligence.com/x-force/defining-cobalt-strike-reflective-loader/)
3. [https://www.elastic.co/guide/en/security/current/potential-lateral-tool-transfer-via-smb-share.html](https://www.elastic.co/guide/en/security/current/potential-lateral-tool-transfer-via-smb-share.html)
4. [https://www.elastic.co/guide/en/security/current/remote-execution-via-file-shares.html](https://www.elastic.co/guide/en/security/current/remote-execution-via-file-shares.html)
5. [https://www.elastic.co/guide/en/security/current/wmi-incoming-lateral-movement.html](https://www.elastic.co/guide/en/security/current/wmi-incoming-lateral-movement.html)
6. [https://www.elastic.co/guide/en/security/current/system-shells-via-services.html](https://www.elastic.co/guide/en/security/current/system-shells-via-services.html)
7. [https://github.com/elastic/protections-artifacts/blob/main/behavior/rules/privilege\_escalation\_suspicious\_execution\_via\_windows\_services.toml](https://github.com/elastic/protections-artifacts/blob/main/behavior/rules/privilege_escalation_suspicious_execution_via_windows_services.toml)
8. [https://github.com/Mr-Un1k0d3r/SCShell](https://github.com/Mr-Un1k0d3r/SCShell)
9. [https://www.elastic.co/guide/en/security/current/suspicious-powershell-engine-imageload.html](https://www.elastic.co/guide/en/security/current/suspicious-powershell-engine-imageload.html)

[Cybersecurity](https://medium.com/tag/cybersecurity?source=post_page-----9c3e5dcf38b0---------------------------------------)

[Elastic](https://medium.com/tag/elastic?source=post_page-----9c3e5dcf38b0---------------------------------------)

[Red Team](https://medium.com/tag/red-team?source=post_page-----9c3e5dcf38b0---------------------------------------)

[Endpoint Security](https://medium.com/tag/endpoint-security?source=post_page-----9c3e5dcf38b0---------------------------------------)

[Penetration Testing](https://medium.com/tag/penetration-testing?source=post_page-----9c3e5dcf38b0---------------------------------------)

[![System Weakness](https://miro.medium.com/v2/resize:fill:96:96/1*gncXIKhx5QOIX0K9MGcVkg.jpeg)](https://systemweakness.com/?source=post_page---post_publication_info--9c3e5dcf38b0---------------------------------------)

[![System Weakness](https://miro.medium.com/v2/resize:fill:128:128/1*gncXIKhx5QOIX0K9MGcVkg.jpeg)](https://systemweakness.com/?source=post_page---post_publication_info--9c3e5dcf38b0---------------------------------------)

Follow

[**Published in System Weakness**](https://systemweakness.com/?source=post_page---post_publication_info--9c3e5dcf38b0---------------------------------------)

[10.4K followers](https://systemweakness.com/followers?source=post_page---post_publication_info--9c3e5dcf38b0---------------------------------------)

· [Last published 1 day ago](https://systemweakness.com/how-reconnaissance-leads-to-your-first-real-vulnerability-5131477e3320?source=post_page---post_publication_info--9c3e5dcf38b0---------------------------------------)

System Weakness is a publication that specialises in publishing upcoming writers in cybersecurity and ethical hacking space. Our security experts write to make the cyber universe more secure, one vulnerability at a time.

Follow

[![Ibad Altaf](https://miro.medium.com/v2/resize:fill:96:96/1*eTswarm8T0kTcSQgRzfz9Q.jpeg)](https://ibady01.medium.com/?source=post_page---post_author_info--9c3e5dcf38b0---------------------------------------)

[![Ibad Altaf](https://miro.medium.com/v2/resize:fill:128:128/1*eTswarm8T0kTcSQgRzfz9Q.jpeg)](https://ibady01.medium.com/?source=post_page---post_author_info--9c3e5dcf38b0---------------------------------------)

Follow

[**Written by Ibad Altaf**](https://ibady01.medium.com/?source=post_page---post_author_info--9c3e5dcf38b0---------------------------------------)

[148 followers](https://ibady01.medium.com/followers?source=post_page---post_author_info--9c3e5dcf38b0---------------------------------------)

· [5 following](https://medium.com/@ibady01/following?source=post_page---post_author_info--9c3e5dcf38b0---------------------------------------)

Penetration tester and a red teamer. Love to learn techniques to bypass various security solutions. Find me at [linkedin.com/in/ibad-altaf](http://linkedin.com/in/ibad-altaf)

Follow

## Responses (1)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fsystemweakness.com%2Flateral-movement-with-elastic-edr-and-asr-enabled-9c3e5dcf38b0&source=---post_responses--9c3e5dcf38b0---------------------respond_sidebar------------------)

Cancel

Respond

[![Ahmed Nosir](https://miro.medium.com/v2/resize:fill:32:32/1*_vhWOCwLWpPNZ2S82PrWcQ.jpeg)](https://medium.com/@egycondor?source=post_page---post_responses--9c3e5dcf38b0----0-----------------------------------)

[Ahmed Nosir](https://medium.com/@egycondor?source=post_page---post_responses--9c3e5dcf38b0----0-----------------------------------)

[Dec 6, 2024](https://medium.com/@egycondor/great-article-ae98959a429b?source=post_page---post_responses--9c3e5dcf38b0----0-----------------------------------)

Zeropointsecurity’s CRTO II course

```
Great article
```

Reply

## More from Ibad Altaf and System Weakness

[See all from Ibad Altaf](https://ibady01.medium.com/?source=post_page---author_recirc--9c3e5dcf38b0---------------------------------------)

[See all from System Weakness](https://systemweakness.com/?source=post_page---author_recirc--9c3e5dcf38b0---------------------------------------)

## Recommended from Medium

[See more recommendations](https://medium.com/?source=post_page---read_next_recirc--9c3e5dcf38b0---------------------------------------)

[Help](https://help.medium.com/hc/en-us?source=post_page-----9c3e5dcf38b0---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----9c3e5dcf38b0---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----9c3e5dcf38b0---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----9c3e5dcf38b0---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----9c3e5dcf38b0---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----9c3e5dcf38b0---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----9c3e5dcf38b0---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----9c3e5dcf38b0---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----9c3e5dcf38b0---------------------------------------)