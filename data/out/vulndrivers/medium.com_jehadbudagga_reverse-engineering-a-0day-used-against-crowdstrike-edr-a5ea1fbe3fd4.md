# https://medium.com/@jehadbudagga/reverse-engineering-a-0day-used-against-crowdstrike-edr-a5ea1fbe3fd4

[Sitemap](https://medium.com/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40jehadbudagga%2Freverse-engineering-a-0day-used-against-crowdstrike-edr-a5ea1fbe3fd4&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

Get app

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40jehadbudagga%2Freverse-engineering-a-0day-used-against-crowdstrike-edr-a5ea1fbe3fd4&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

# Reverse Engineering a 0day used Against CrowdStrike EDR

[![Jehad Abudagga](https://miro.medium.com/v2/resize:fill:32:32/1*RDY4v701RlMMNtetLOsVYw.png)](https://medium.com/@jehadbudagga?source=post_page---byline--a5ea1fbe3fd4---------------------------------------)

[Jehad Abudagga](https://medium.com/@jehadbudagga?source=post_page---byline--a5ea1fbe3fd4---------------------------------------)

Follow

4 min read

·

Apr 5, 2026

50

4

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Da5ea1fbe3fd4&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40jehadbudagga%2Freverse-engineering-a-0day-used-against-crowdstrike-edr-a5ea1fbe3fd4&source=---header_actions--a5ea1fbe3fd4---------------------post_audio_button------------------)

Share

## Hello again…

I've been reversing kernel drivers for over a year now and last week i came across several interesting Kernel drivers that have been used in BYOVD attacks against several EDRs including the well known CrowdStrike EDR

I decided to make a blog about it and publish the POC and drivers for everyone.

Lets start.

In this picture we can see the driver and its variants (15+ variants) all have the same code inside.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*bCoSNbubNmyX2yx5QJrgjw.jpeg)

Identified Drivers

All the Drivers are signed by Microsoft and have valid signatures and not blocked or revoked by anyone.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*WfNNRtTazMxc-gxa07EsBQ.jpeg)

Drivers signed by Microsoft

When opening one of the drivers in virus total we can see that its not detected by any AV or EDR vendor.

link: [https://www.virustotal.com/gui/file/6fbaad2f00afaa94723fa7d5bd46e7ea4babb7ce478a8e7229ce7bd4b85e0f51/detection](https://www.virustotal.com/gui/file/6fbaad2f00afaa94723fa7d5bd46e7ea4babb7ce478a8e7229ce7bd4b85e0f51/detection)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*nh-ueTVZvlbcjwxYUWdFNA.jpeg)

Virus total scan of one of the drivers

## Reverse Engineering

Now for the reverse engineering part, i opened Ida pro and loaded the driver in it, Ida pro was not able to decompile the main function (DriverEntry) in the driver.

This is a known IDA issue with drivers that use non-standard stack frames or that have had their entry point obfuscated. Rather than fight it, I skipped DriverEntry and went straight for the dispatch handler which is where the interesting logic lives anyway.

![](https://miro.medium.com/v2/resize:fit:477/1*oLQy6Zdz7Xf7Y0X9zGp8KA.jpeg)

Decompilation failure in DriverEntry

The DeviceIoControlHandler function was decompiled but looked terrible, raw offsets for CurrentStackLocation fields, unnamed sub-functions, meaningless variable names.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*JdTGt_nqGIZd8nFBPeoBiw.jpeg)

DeviceIoControlHandler before fixing.

After fixing the types and names:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*b9_3xMqAyG5LBSFJ5daCBg.jpeg)

DeviceIoControlHandler after fixing.

We can see 2 IOCTL’s, the first i was too lazy to reverse but the second one (0x22E010) is leading to a function responsible for process killing i named procKiller.

When opening the procKiller decompilation code still it looks ugly and garbage, i had to fix it like i did before.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*ssUIbyatZFa2gMzY1P8YFQ.jpeg)

procKiller function before fixing

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*OxAmA7X7OeGAn9Q_sLIdRQ.jpeg)

procKiller function after fixing

The procKiller function flow is as following:

1\. The IOCTL input buffer is treated as a null-terminated ASCII string containing the decimal PID.

2\. The driver calls atoi() on it, passes the integer to TerminateProcess.

3\. Writes `"ok"` back to the output buffer on success. That's the entire interface.

## Get Jehad Abudagga’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

Inside the TerminateProcess is the true flow of killing the process:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*LBhBbllhu80SsQkyHWll0Q.jpeg)

TerminateProcess function

the TerminateProcess takes the PID and opens the process using ZwOpenProcess function to obtain a handle, then a call to ZwTerminateProcess using the obtained process handle.

This is why CrowdStrike (and other EDRs running as PPL) can be killed. In user mode, OpenProcess against a PPL process returns Access Denied. But from the kernel, ZwOpenProcess doesn’t care.

Now that we have reversed the killing part and identified the IOCTL responsable for process killing, we still miss one critical piece which is the driver’s symblolic link , without it we cant send process termination requests from usermode.

For the symbolic link hunting i decided to go for the dynamic approach which is loading the driver and seeing if any new symlinks pop up in WinObj and we were able to find the driver symbolic link:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*JxG2S1i-WAcS1k1YsKcRJg.jpeg)

Driver Symlink

Now we have all the pieces:

Driver symlink: \\\.\\{F8284233–48F4–4680-ADDD-F8284233}

Kill Process IOCTL : 0x22E010

## **Creating the POC**

First i added all driver symlink and the ioctl as variables:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*imhVBDcFgmdWtsBsrjUleQ.jpeg)

in the main function the flow is the following:

1. Opens \\\.\\{F8284233–48F4–4680-ADDD-F8284233} via CreateFileW.
2. Converts the PID to a decimal ASCII string.
3. Sends it via DeviceIoControl with IOCTL 0x22E010.
4. Process Terminated !!!

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*QkGUtWSr_Kiwgz_c71fk4A.jpeg)

main function part 1

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*AirtxPH0gvw-9cNcjftL2Q.jpeg)

main function part 2

Now its time to test the POC against CrowdStrike:

First we load the driver using OSRLOADER.

you can also load the driver using sc.exe:

```
sc.exe create PoisonX binPath="C:\Path\to\Driver.sys" type=kernel
sc.exe start PoisonX
```

![](https://miro.medium.com/v2/resize:fit:441/1*BLTVp4HaPrUoEQVfG-tMhw.jpeg)

Loading the driver using OSRLOADER

Then we run the POC against crowdstrike.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*IwVC5ncmA05lDpDhqz3T_Q.jpeg)

Before running the POC

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*zJgQ9x2aP0reYVMFrG_-Eg.png)

After running POC

For the POC and the drivers, i just published them on GitHub.

[https://github.com/j3h4ck/PoisonKiller/](https://github.com/j3h4ck/PoisonKiller/)

[Byovd](https://medium.com/tag/byovd?source=post_page-----a5ea1fbe3fd4---------------------------------------)

[Edr](https://medium.com/tag/edr?source=post_page-----a5ea1fbe3fd4---------------------------------------)

[Red Teaming](https://medium.com/tag/red-teaming?source=post_page-----a5ea1fbe3fd4---------------------------------------)

[Reverse Engineering](https://medium.com/tag/reverse-engineering?source=post_page-----a5ea1fbe3fd4---------------------------------------)

[Apt](https://medium.com/tag/apt?source=post_page-----a5ea1fbe3fd4---------------------------------------)

[![Jehad Abudagga](https://miro.medium.com/v2/resize:fill:48:48/1*RDY4v701RlMMNtetLOsVYw.png)](https://medium.com/@jehadbudagga?source=post_page---post_author_info--a5ea1fbe3fd4---------------------------------------)

[![Jehad Abudagga](https://miro.medium.com/v2/resize:fill:64:64/1*RDY4v701RlMMNtetLOsVYw.png)](https://medium.com/@jehadbudagga?source=post_page---post_author_info--a5ea1fbe3fd4---------------------------------------)

Follow

[**Written by Jehad Abudagga**](https://medium.com/@jehadbudagga?source=post_page---post_author_info--a5ea1fbe3fd4---------------------------------------)

[77 followers](https://medium.com/@jehadbudagga/followers?source=post_page---post_author_info--a5ea1fbe3fd4---------------------------------------)

· [3 following](https://medium.com/@jehadbudagga/following?source=post_page---post_author_info--a5ea1fbe3fd4---------------------------------------)

Security Researcher \| CETP \| CPTS \| CRTL \| CRTO \| CRTE \| CRTP \| eCPPT \| C-ADPenX \| CRTeamerX

Follow

## Responses (4)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40jehadbudagga%2Freverse-engineering-a-0day-used-against-crowdstrike-edr-a5ea1fbe3fd4&source=---post_responses--a5ea1fbe3fd4---------------------respond_sidebar------------------)

Cancel

Respond

See all responses

[Help](https://help.medium.com/hc/en-us?source=post_page-----a5ea1fbe3fd4---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----a5ea1fbe3fd4---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----a5ea1fbe3fd4---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----a5ea1fbe3fd4---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----a5ea1fbe3fd4---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----a5ea1fbe3fd4---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----a5ea1fbe3fd4---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----a5ea1fbe3fd4---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----a5ea1fbe3fd4---------------------------------------)

reCAPTCHA

Recaptcha requires verification.

protected by **reCAPTCHA**