# https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/create-remote-thread.md

[Skip to content](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/create-remote-thread.md#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/create-remote-thread.md) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/create-remote-thread.md) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/create-remote-thread.md) to refresh your session.Dismiss alert

{{ message }}

[trustedsec](https://github.com/trustedsec)/ **[SysmonCommunityGuide](https://github.com/trustedsec/SysmonCommunityGuide)** Public

- [Notifications](https://github.com/login?return_to=%2Ftrustedsec%2FSysmonCommunityGuide) You must be signed in to change notification settings
- [Fork\\
184](https://github.com/login?return_to=%2Ftrustedsec%2FSysmonCommunityGuide)
- [Star\\
1.4k](https://github.com/login?return_to=%2Ftrustedsec%2FSysmonCommunityGuide)


## Collapse file tree

## Files

master

Search this repository

/

# create-remote-thread.md

Copy path

BlameMore file actions

BlameMore file actions

## Latest commit

[![darkoperator](https://avatars.githubusercontent.com/u/521246?v=4&size=40)](https://github.com/darkoperator)[darkoperator](https://github.com/trustedsec/SysmonCommunityGuide/commits?author=darkoperator)

[update to build and chapters](https://github.com/trustedsec/SysmonCommunityGuide/commit/bde5de34c30521837013b586d8de17677722fa90)

Open commit details

4 months agoNov 30, 2025

[bde5de3](https://github.com/trustedsec/SysmonCommunityGuide/commit/bde5de34c30521837013b586d8de17677722fa90) · 4 months agoNov 30, 2025

## History

[History](https://github.com/trustedsec/SysmonCommunityGuide/commits/master/chapters/create-remote-thread.md)

Open commit details

[View commit history for this file.](https://github.com/trustedsec/SysmonCommunityGuide/commits/master/chapters/create-remote-thread.md) History

167 lines (121 loc) · 6.44 KB

/

# create-remote-thread.md

Top

## File metadata and controls

- Preview

- Code

- Blame


167 lines (121 loc) · 6.44 KB

[Raw](https://github.com/trustedsec/SysmonCommunityGuide/raw/refs/heads/master/chapters/create-remote-thread.md)

Copy raw file

Download raw file

Outline

Edit and raw actions

# Create Remote Thread

[Permalink: Create Remote Thread](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/create-remote-thread.md#create-remote-thread)

Sysmon will log **EventID 8** for processes that use the Win32 API [CreateRemoteThread](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createremotethread) call. This is a **low-volume, high-value event type** that detects one of the most common process injection techniques used by malware and attackers.

## Detection Value and Why It Matters

[Permalink: Detection Value and Why It Matters](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/create-remote-thread.md#detection-value-and-why-it-matters)

CreateRemoteThread is a classic process injection technique where one process creates a thread in another process to execute code. This is used by attackers for:

**Code Injection**: Injecting malicious code into legitimate processes to evade detection and inherit the target process's privileges and context.

**Defense Evasion**: Running malicious code inside trusted processes (explorer.exe, svchost.exe) to avoid detection by security tools that trust those processes.

**Privilege Escalation**: Injecting into processes running with higher privileges.

**Persistence**: Maintaining presence by continuously injecting into long-running system processes.

**MITRE ATT&CK Mapping**:

- **T1055.001 - Process Injection: Dynamic-link Library Injection**
- **T1055.002 - Process Injection: Portable Executable Injection**
- **T1055 - Process Injection** (general)

## How CreateRemoteThread Injection Works

[Permalink: How CreateRemoteThread Injection Works](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/create-remote-thread.md#how-createremotethread-injection-works)

Process injection using CreateRemoteThread follows this pattern:

Process of use/abuse of CreateRemoteThread

- Use **OpenProcess( )** to open a target process.

- Use **VirtualAllocEx( )** allocate a chunk of memory in the process.

- Use **WriteProcessMemory( )** write the payload to the newly
allocated section.

- User **CreateRemoteThread( )** to create a new thread in the remote
process to execute the shellcode.


There are multiple Process Injection techniques, Sysmon monitors for the
most common one used. The infographic from
[http://struppigel.blogspot.com/2017/07/process-injection-info-graphic.html](http://struppigel.blogspot.com/2017/07/process-injection-info-graphic.html)

Illustrates the different techniques.

[![process injection infograph](https://github.com/trustedsec/SysmonCommunityGuide/raw/master/chapters/media/image57.png)](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/media/image57.png)

The fields for the event are:

- **RuleName**: Name of rule that triggered the event.

- **UtcTime**: Time in UTC when event was created

- **SourceProcessGuid**: Process Guid of the source process that
created a thread in another process

- **SourceProcessId**: Process ID used by the OS to identify the
source process that created a thread in another process

- **SourceImage**: File path of the source process that created a
thread in another process

- **TargetProcessGuid**: Process Guid of the target process

- **TargetProcessId**: Process ID used by the OS to identify the
target process

- **TargetImage**: File path of the target process

- **NewThreadId**: Id of the new thread created in the target process

- **StartAddress**: New thread start address

- **StartModule**: Start module determined from thread start address
mapping to PEB loaded module list

- **StartFunction**: Start function is reported if exact match to
function in image export tables


## Configuration Strategy: Log All, Exclude Known-Good

[Permalink: Configuration Strategy: Log All, Exclude Known-Good](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/create-remote-thread.md#configuration-strategy-log-all-exclude-known-good)

The number of processes that legitimately use CreateRemoteThread() in a production environment is **very low**. This makes it ideal for a **log-all approach** with minimal exclusions.

**Important Limitation**: CreateRemoteThread() is not the only API for creating remote threads. Attackers may use alternative methods like:

- NtCreateThreadEx()
- RtlCreateUserThread()
- QueueUserAPC()
- Other undocumented APIs

Sysmon only monitors CreateRemoteThread(), so this event type alone does not guarantee detection of all process injection. It should be combined with other event types (Process Access, Image Loading) for comprehensive coverage.

## What to Investigate

[Permalink: What to Investigate](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/create-remote-thread.md#what-to-investigate)

When reviewing CreateRemoteThread events, prioritize:

**1\. Unknown Source Processes**

- Any SourceImage you don't recognize or that isn't a system process
- Processes running from temp directories or user folders
- Unsigned or suspicious executables

**2\. Injection into Critical Processes**

- Threads created in explorer.exe, lsass.exe, or other critical system processes
- Especially suspicious if the source is not a system process

**3\. Unusual StartModule or StartAddress**

- StartModule not pointing to legitimate system DLLs
- StartAddress in unusual memory regions
- StartFunction that doesn't match expected behavior

**4\. Script Engines or Office Apps as Source**

- powershell.exe, cscript.exe, wscript.exe creating remote threads
- WINWORD.EXE, EXCEL.EXE injecting into other processes (very suspicious)

**5\. Correlation with Other Events**

- Cross-reference with Process Access events for the same target
- Check if the source process was recently created (staging malware)

[![process](https://github.com/trustedsec/SysmonCommunityGuide/raw/master/chapters/media/image58.png)](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/media/image58.png)

## Example Configuration: Excluding Known-Good System Processes

[Permalink: Example Configuration: Excluding Known-Good System Processes](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/create-remote-thread.md#example-configuration-excluding-known-good-system-processes)

After baselining, exclude verified legitimate uses of CreateRemoteThread:

```
<Sysmon schemaversion="4.22">
  <CheckRevocation/>
    <EventFiltering>
      <RuleGroup name="" groupRelation="or">
        <CreateRemoteThread onmatch="exclude">
          <!--The process activity of those in the list should be monitored since an-->
          <!--attacker may host his actions in one of these to bypass detection.-->
           <TargetImage condition="end with">
             Google\Chrome\Application\chrome.exe
            </TargetImage>
            <SourceImage condition="is">
              C:\Windows\System32\wbem\WmiPrvSE.exe
            </SourceImage>
            <SourceImage condition="is">
              C:\Windows\System32\svchost.exe
            </SourceImage>
            <SourceImage condition="is">
              C:\Windows\System32\wininit.exe
            </SourceImage>
            <SourceImage condition="is">
              C:\Windows\System32\csrss.exe
            </SourceImage>
            <SourceImage condition="is">
              C:\Windows\System32\services.exe
            </SourceImage>
            <SourceImage condition="is">
              C:\Windows\System32\winlogon.exe
            </SourceImage>
            <SourceImage condition="is">
              C:\Windows\System32\audiodg.exe
            </SourceImage>
            <StartModule condition="is">
              C:\windows\system32\kernel32.dll
            </StartModule>
        </CreateRemoteThread>
        </RuleGroup>
    </EventFiltering>
</Sysmon>
```

You can’t perform that action at this time.