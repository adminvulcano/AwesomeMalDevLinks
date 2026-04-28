# https://sudosiddharths.medium.com/analyzing-the-evolution-and-execution-of-syswhispers-1-3-74cbbcdaf397

[Sitemap](https://sudosiddharths.medium.com/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fsudosiddharths.medium.com%2Fanalyzing-the-evolution-and-execution-of-syswhispers-1-3-74cbbcdaf397&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

Get app

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fsudosiddharths.medium.com%2Fanalyzing-the-evolution-and-execution-of-syswhispers-1-3-74cbbcdaf397&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

# **Analyzing the Evolution and Execution of SysWhispers (1–3)**

[![Siddharth Avi Singh](https://miro.medium.com/v2/resize:fill:32:32/1*KyDwOby0liwb3TnHGhDQ4g.jpeg)](https://sudosiddharths.medium.com/?source=post_page---byline--74cbbcdaf397---------------------------------------)

[Siddharth Avi Singh](https://sudosiddharths.medium.com/?source=post_page---byline--74cbbcdaf397---------------------------------------)

Follow

7 min read

·

Jan 14, 2026

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D74cbbcdaf397&operation=register&redirect=https%3A%2F%2Fsudosiddharths.medium.com%2Fanalyzing-the-evolution-and-execution-of-syswhispers-1-3-74cbbcdaf397&source=---header_actions--74cbbcdaf397---------------------post_audio_button------------------)

Share

![](https://miro.medium.com/v2/resize:fit:460/1*58e3ShdYaW6lgtqs41NF-A.jpeg)

Icon for the SysWhispers repository on Github

## Origins of SysWhispers

SysWhispers originated as an experiment or requirement of bypassing User-land hooks placed by AV/EDR softwares to monitor the system calls made to the kernel land by applications, for malicious activity and blocking basis the same.

Kernel land and user land is the division created by Windows to separate the level of access provided to an application, as a safeguard against excessive permissions and unauthorized actions. Here “syscall” is an actual instruction that is visible in WinDBG and marks the shift from User-mode to kernel-mode. Once the kernel routines are finished, the program flow returns back to the user-mode and the “return address” value from the kernel API call.

As pointed out before, AV/EDR place their hooks in user-mode or user-land itself in some specific instructions, which means that bypassing this check is the main goal of the attacker to operate undetected. There are a few methods to perform the same, however, each comes with their own limitations.

### First Step: Using Syscalls Directly

- Syscall numbers can be obtained via multiple methods, some static, some dynamic
- Syscall numbers, however, change between OS versions and can even change between service packs
- Google Project Zero has an online “system calls table” which contains a list; this is what is utilized in the first version of SysWhispers
- Using a fixed table required pulling the OS version from the machine on which the malware is being run, for this the Native API “RtlGetVersion” is used; the OS version obtained from this is fed back to the functions keeping an index of the syscall numbers and from there the correct syscalls are used

### Second Step: Restoring the hooked API calls with direct syscalls

- A little detail about the method using which the the API calls is hooked is that the first 5 bytes of the “NtReadVirtualMemory” function is edited, the first instruction is a JMP (jump) instruction to an address elsewhere in the memory
- This memory is of their own module where it checks for malicious activity; if the check fails: it returns to the function with an error code, having never executed the payload and never entering the kernel; if the check succeeds: the function returns normally and proceeds with execution to kernel mode
- There are two ways to take it from here:
- **Re-patch the patch**— How this works is that the malware stores the correct/original assembly instructions which it overwrites in the system call functions (“ZwProtectVirtualMemory” & “ZwWriteVirtualMemory”) by overwriting the first 5 bytes (including the system call number)
- **Ntdll IAT (Import Address Table) hook** — Here we create a copy of the function elsewhere; walk the ntdll import address table and swap out the pointer for NtReadVirtualMemory to our version which does not contain the EDR hook. The advantage of this version is that the EDR’s hook both looks clean and remains unchanged; it is never called leaving minimal forensic trail on the same

Using the methods above we have finally achieved a bypass for EDR hooking into syscalls which can prevent the timely execution of stealth malware on Windows Machines. Out of the methodologies mentioned above, the following sequence is followed by SysWhispers:

SysWhispers provides red teamers the ability to generate header/ASM pairs for any system call in the core kernel image (ntoskrnl.exe) across any Windows version starting from XP. The headers will also include the necessary type definitions; what’s different is that instead of using “RtlGetVersion” {to detect which a threat hunting query can be created}, instead it detects the same in the assembly by querying the PEB directly. This allows for a single function in the code to handle syscall addresses for each different type of windows systems and OS.

## **SysWhispers2 — The Evolution of SysWhispers**

The major evolutionary advantage of SysWhispers2 is to change the way that syscall numbers are obtained. While earlier, a static table for the same was being used while the Windows OS version and Service Pack number was obtained by querying the PEB and thus the correct syscall number was mapped accordingly; now the syscall number is obtained dynamically by using existing libraries and files, thus allowing for smaller syscall stubs.

How this came to be and was achieved is summarised below:

The first inspiration for this kind of evolution was developed from the method published on EvilSocket:

Instead of loading the ntdll library using the LoadLibrary() function, we can manually inspect its contents like a portable executable; to do we same: we open ntdll.dll, inspect its export directory, obtain the RVA and raw offset of NtCreateFile and then check the first bytes of opcodes. We’ve to expect the first byte to be B8h which is a MOV EAX, IMM32 so we can take the four next bytes and have our syscall number.

Thus, we get a table with each syscall number, RVA (Relative Virtual Address) and relative API name.

## Get Siddharth Avi Singh’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

Inspired by this, another version is written which resulted in the availability of a tool called freshycalls which became the original variation of what has finally been executed in SysWhispers2.

The modern method or the method finally included in SysWhispers2 which became the basis for the new version being released follows a methodology where it does not need to take any of the aforementioned steps to obtain the correct syscall number or address for functions. It doesn’t even need to load ntdll.dll. What it instead does is it analyzes the ntdll.dll’s Export Address Table (EAT) and enumerates all exported functions prefixed with “Zw”; replaces them with the prefix “Nt”, hashes the resulting names and records their function addresses. Since the stub layout in Windows is consistent, sorting the address of the Zw\* (or Nt\*) functions in memory effectively sorts them in order of their syscall numbers. So the index in the sorted list is the syscall number.

These entries are then sorted in ascending order by address, and their index in the sorted list becomes the syscall number (SSN).

This approach is resilient to user-mode hooks, doesn’t require OS version checks or external syscall tables, and relies on consistent internal ordering of system calls in memory — making it both stealthy and reliable for bypassing EDR detection.

With this final change in how syscall numbers are obtained, SysWhispers2 achieves dynamic execution with a much smaller stub.

## **SysWhisper3 — A Widened Fork of SysWhispers2**

An important thing to note here is that the recent changes made to SysWhispers2 (notably the modern methods of obtaining SSN) were implemented around the same time in a fork at the time of its release which would later become SysWhispers3; hence additional capabilities added to SysWhispers3 are limited. We have covered the later enhancements from SysWhisper2 to SysWhispers3 below:

While SysWhispers2 pioneered runtime syscall resolution by parsing the EAT of ntdll.dll, SysWhispers3 fully eliminates the need for traditional syscall stubs altogether. Instead of embedding instructions like mov eax, SSN; syscall, which can be statically analyzed and detected, SysWhispers3 retrieves function addresses from ntdll.dll and performs indirect jumps into legitimate syscall stubs already residing in memory. This makes detection through signature-based scanning or heuristic pattern-matching significantly more difficult, since no custom syscall stub exists for a scanner to latch onto.

The implementation relies heavily on a dispatcher pattern, where a central function maps hashed syscall names to function pointers resolved at runtime. This not only reduces binary size and static footprint but also enables support for WoW64 and other system variants without needing separate handling logic. The use of indirect syscalls means the control flow mimics genuine Windows behavior, further complicating detection for security solutions. In essence, while SysWhispers2 introduced dynamic resolution, SysWhispers3 focuses on execution invisibility — removing known syscall signatures, resisting API hooking, and blending malware behavior into the noise of legitimate system activity.

## **Detection Pattern Documentation**

SysWhispers3 is designed to avoid triggering common detection patterns used by AV/EDR and SIEM tools. Since it doesn’t use typical high-level Windows API functions and instead jumps directly to system call instructions inside ntdll.dll, the usual API monitoring won’t catch these calls. There are no IAT hooks, no VirtualAlloc, WriteProcessMemory, or CreateRemoteThread APIs involved, which are commonly monitored. It also avoids static syscall stubs, meaning that signature-based tools don’t typically catch anything suspicious. The result is a significant reduction in static, behavioral, and memory-based detection opportunities.

Another detection challenge comes from the fact that the syscall sequence originates from legitimate memory inside ntdll.dll, making it blend in with normal activity. Even advanced heuristics that flag “unusual syscall chains” might miss it because there is no violation of expected memory permissions or executable regions.

## **Evasion Technique Analysis**

SysWhispers3 uses multiple techniques to stay hidden:

- **Indirect syscalls:** Instead of creating new syscall instructions, it jumps into existing syscall stubs in ntdll.dll, avoiding detection from tools that look for suspicious syscall instruction patterns.
- **No hardcoded syscall numbers:** It calculates syscall indexes dynamically by sorting exported Zw\* function addresses, making it compatible with multiple OS versions without relying on OS version checks or hardcoded tables.

Together, these techniques make SysWhispers3 harder to detect both statically (through file scanning) and dynamically (through behavior analysis or memory forensics). It also makes forensic attribution harder since the “attack chain” appears clean when reviewing logs and memory snapshots.

## **References:**

1. [https://github.com/klezVirus/SysWhispers3](https://github.com/klezVirus/SysWhispers3)
2. [https://web.archive.org/web/20220814091544/https://www.crummie5.club/freshycalls/](https://web.archive.org/web/20220814091544/https://www.crummie5.club/freshycalls/)
3. [https://www.evilsocket.net/2014/02/11/On-Windows-syscall-mechanism-and-syscall-numbers-extraction-methods/](https://www.evilsocket.net/2014/02/11/On-Windows-syscall-mechanism-and-syscall-numbers-extraction-methods/)
4. [https://klezvirus.github.io/posts/NoSysWhispers/](https://klezvirus.github.io/posts/NoSysWhispers/)
5. [https://www.outflank.nl/blog/2019/06/19/red-team-tactics-combining-direct-system-calls-and-srdi-to-bypass-av-edr/](https://www.outflank.nl/blog/2019/06/19/red-team-tactics-combining-direct-system-calls-and-srdi-to-bypass-av-edr/)
6. [https://medium.com/@fsx30/bypass-edrs-memory-protection-introduction-to-hooking-2efb21acffd6](https://medium.com/@fsx30/bypass-edrs-memory-protection-introduction-to-hooking-2efb21acffd6)
7. [https://silentbreaksecurity.com/srdi-shellcode-reflective-dll-injection/](https://silentbreaksecurity.com/srdi-shellcode-reflective-dll-injection/)
8. [https://www.mdsec.co.uk/2019/03/silencing-cylance-a-case-study-in-modern-edrs/](https://www.mdsec.co.uk/2019/03/silencing-cylance-a-case-study-in-modern-edrs/)

[Syswhispers](https://medium.com/tag/syswhispers?source=post_page-----74cbbcdaf397---------------------------------------)

[Cybersecurity](https://medium.com/tag/cybersecurity?source=post_page-----74cbbcdaf397---------------------------------------)

[Edr Bypass](https://medium.com/tag/edr-bypass?source=post_page-----74cbbcdaf397---------------------------------------)

[Threat Research](https://medium.com/tag/threat-research?source=post_page-----74cbbcdaf397---------------------------------------)

[![Siddharth Avi Singh](https://miro.medium.com/v2/resize:fill:48:48/1*KyDwOby0liwb3TnHGhDQ4g.jpeg)](https://sudosiddharths.medium.com/?source=post_page---post_author_info--74cbbcdaf397---------------------------------------)

[![Siddharth Avi Singh](https://miro.medium.com/v2/resize:fill:64:64/1*KyDwOby0liwb3TnHGhDQ4g.jpeg)](https://sudosiddharths.medium.com/?source=post_page---post_author_info--74cbbcdaf397---------------------------------------)

Follow

[**Written by Siddharth Avi Singh**](https://sudosiddharths.medium.com/?source=post_page---post_author_info--74cbbcdaf397---------------------------------------)

[4 followers](https://sudosiddharths.medium.com/followers?source=post_page---post_author_info--74cbbcdaf397---------------------------------------)

· [3 following](https://sudosiddharths.medium.com/following?source=post_page---post_author_info--74cbbcdaf397---------------------------------------)

Threat Researcher, Malware Analyst and Ex-Red Teamer and Pentester.

Follow

## No responses yet

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fsudosiddharths.medium.com%2Fanalyzing-the-evolution-and-execution-of-syswhispers-1-3-74cbbcdaf397&source=---post_responses--74cbbcdaf397---------------------respond_sidebar------------------)

Cancel

Respond

[Help](https://help.medium.com/hc/en-us?source=post_page-----74cbbcdaf397---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----74cbbcdaf397---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----74cbbcdaf397---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----74cbbcdaf397---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----74cbbcdaf397---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----74cbbcdaf397---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----74cbbcdaf397---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----74cbbcdaf397---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----74cbbcdaf397---------------------------------------)

reCAPTCHA

Recaptcha requires verification.

protected by **reCAPTCHA**