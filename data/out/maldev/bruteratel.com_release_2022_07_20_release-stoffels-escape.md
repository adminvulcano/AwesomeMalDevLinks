# https://bruteratel.com/release/2022/07/20/Release-Stoffels-Escape/

## Release v1.1 - Stoffel's Escape

Brute Ratel v1.1 codename _Stoffel’s Escape_ is now available for download. This release brings several new feature additions and improvements to the Badger, Ratel Server and Commander, including a complete re-write of the badger’s core to avoid some subtle detection techniques following the [Palo Alto blog](https://unit42.paloaltonetworks.com/brute-ratel-c4-tool/#Brute-Ratel-C4-Overview). A quick summary of the changes can be found in the [release notes](https://bruteratel.com/release_notes/releases.txt). The release name (Stoffel’s Escape) gives subtle hints foreshadowing the nature of this release. This release could not have been better without the support from the blue team community. As BRc4 initially started as a personal project two years back, there were still some remnants of IOCs that needed to be changed. Palo Alto’s reversing blog came in as a surprise, but it only helped to rebuild the payload and optimize it in a certain way to avoid as many IOCs as possible. This release was focused to overcome all the IOCs listed in public or private blogs, conferences and github detections, till date, about Badger and change them to avoid attribution and detection.

## Badger

### The Core

The first major change begins with the core of the badger. The entire core was re-written to hide several traces in memory following the Palo Alto blog. Most known Command and Control Centers like CobaltStrike and Metasploit, use a reflective DLL at heart which is usually bootstrapped inside a shellcode. This shellcode acts as a loader by allocating an executable memory section in the current process and then relocating various sections of the reflective DLL to execute them. This also brings in the need for a user defined reflective loader, as the static reflective loader would actually be easy to detect and an organization would have to update it in every release to avoid IOCs. Cobalt Strike’s UDRL provides a way for operators to write their own reflective loaders for the same reason. This is however something I wanted to avoid for a long time in the badger, because it meant that every organization will need to have an in-house expertise on writing loaders which is not always the case. At the same time, writing a position independent payload is a pain as it comes with it’s set of limitations when dealing with larger payloads such as dealing with ‘\_chkstk’ and maintaining the 8kb stack limit which might generate exceptions, which cannot be caught unless you are writing a non-position-independent payload. This simply brings us back to using a reflective DLL.

However, upon further research, I did find a way to avoid using reflective loaders while also avoiding a position independent shellcode for the second stage. Make no mistake, the first stage is still position independent. This is one of the major updates to badger which avoids using several memory allocations to execute the bootstrapped stage. Badger now comes with a new shellcode, stage and wrapper to hide it’s presence in memory. Until the previous release v1.0.7, the RC4 encryption key ‘bYXJm/3#M?:XyMBF’ was hardcoded within the stageless payload which was used to decrypt the stage configuration. This was a part of the legacy code I wrote two years back when I started building BRc4. The stage itself was not encrypted as it was expected that the operators might do this. However, all of this changes with the release of v1.1. Every payload that is built starting v1.1 release will use randomly generated keys, different for both, the configuration and the badger’s stage. This key is now also hidden in order to avoid it’s extraction with regexes. Another important change made to the shellcode was to use random assembly registers to avoid YARA detections. This means, the Ratel Server will use a custom polymorphic algorithm which use random registers for shellcode allocation, and the entire code will be different, everytime a new payload is created.

### In-Memory Evasions

Until the v1.0.7 release, the badger loaded all the required DLLs (including the ones required for post-exploitation) directly during the initial execution of the payload. This is now changed in the current release, where only the required DLLs necessary to perform the core operations such as HTTP/TCP/SMB connections are loaded. The simplest example can be taken for the ‘phish\_creds’ command which requires credui.dll. The post-exploitation DLLs will not be loaded unless their respective command is executed. This change also provided a gateway for more operational security changes to the core to avoid loading any DLL into memory. When the badger is executed, it will first check the Process Environment Block (PEB) to search for DLLs already loaded by the current process. If the DLL required by the badger is already loaded, then the badger won’t call LoadLibrary or LdrLoadDll. It will simply extract the DLL’s base address directly from the PEB avoiding the need to call LoadLibrary or LdrLoadDll. This helps to avoid loading almost all of the libraries when injected into processes like Explorer or Microsoft Edge as they by default load all the minimum DLLs required by the badger to run.

Another major change made to the core was to change the way DLLs are loaded. Some EDRs usually hook LoadLibrary and LdrLoadDll to check which region is calling this function. This check is sometimes also performed by capturing EtwTI in the kernel mode. This telemetry is used to perform stack tracing to validate if the request is originating from a user allocated RX region, and if it is, the process is then killed. In order to avoid such detections, badger now uses proxy functions to avoid calling LoadLibrary or LdrLoadDll by itself. All calls to LoadLibrary and LdrLoadDll are now proxied via other legitimate functions of windows. This helps to avoid a direct call originating from the user allocated RX region which can be an IOC. This feature was added as a separate payload generation feature in Brute Ratel which is now listed as ‘stealth’ in the context menu when generating the payload via Listener or the Payload Profiler.

In the previous releases of BRc4, the badger only encrypted the RW (ReadWrite), and the RX (ReadExecute) regions of the badger due to the way sleep masking was implemented. However, it was found that there were a few strings which were left out from the ReadOnly region of the badger (.rdata) which contained strings like “AMSI Patched”. This however changes with the current release as the entire shellcode, stage and all memory regions are encrypted during the initial execution as well as during sleep. All encryption routines use different encryption keys everytime and they are used only once and dynamically generated on the fly. The current release of badger utilizes a custom heap, some portions of which are also encrypted depending on the level of it’s sensitivity, and this heap is also zeroed out before freeing it up. However we are not encrypting the entire process memory as it is known to crash the process due to the sensitive allocations by ntdll/kernel32. Catching and releasing exceptions every now and then via Vectored Exception Handler or Hardware hooks is an extremely bad software development practice as legitimate programs never do that. This becomes an easy IOC to detect and thus we wanted to avoid heap encryption for the same reason. The below video showcases the new memory evasion features.

Brute Ratel v1.1 - Memory Evasion - YouTube

Tap to unmute

[Brute Ratel v1.1 - Memory Evasion](https://www.youtube.com/watch?v=AUB4sGWnIGs) [Chetan Nayak](https://www.youtube.com/channel/UCpDI4t3oGuQNOpaX85daOrg)

![thumbnail-image](https://yt3.ggpht.com/s78j1PZDYdQ3Zlirsv6BfnTda3TzKvFmvQYVNTuD6sdFpQgj_m3fWhzC0f9vLicYVLY9BzBcBA=s68-c-k-c0x00ffffff-no-rj)

Chetan Nayak2.13K subscribers

The new badger also supports full thread stack masquerading as well as start address spoofing to make it look extremely legitimate. The sleep masking techniques are also updated which can be switched dynamically either during the creation of the payload or on the fly using the newly introduced ‘obfsleep’ command. There is also a ‘start\_address’ command which can be used to specify the spoofed start address for APC based sleep masking. The below figure should show the stack difference between badger and legitimate windows process which are none.

![](https://bruteratel.com/images/post_img/2022-07-20-Release-Stoffels-Escape/stack_0.png)

![](https://bruteratel.com/images/post_img/2022-07-20-Release-Stoffels-Escape/stack_1.png)

### Extended Syscall Support for x86 and x86 on WOW64

In the previous releases, syscalls were only supported for x64. However, starting from this release, all types of payload i.e. x86, x86 on WOW64 and x64 will get full syscall and memory evasion support. This is not just limited to indirect syscalls, but also for full sleep masking including thread stack masquerading. The commands ‘set\_malloc’ and ‘set\_threadex’ have also been updated to support indirect syscalls for x86 and x86 on Wow64 support. All staged and stageless payloads use indirect syscalls by default.

### Phantom Thread

A new thread injection technique was added to badger under the name ‘phantom\_thread’. This command when combined with the ‘threads’ command can be extremely powerful to hide remote process injection traces in memory. The ‘threads’ command returns all the running threads in the system and can be used to filter out threads that are already in an alertable state.

![](https://bruteratel.com/images/post_img/2022-07-20-Release-Stoffels-Escape/threads.png)

The ‘phantom\_thread’ command uses a ROP gadget technique alongside context hijacking for alertable threads. The rop gadgets help to redirect the execution flow to originate from a legitimate region instead of directly from the RX region. However, the gadgets required for ROP, are found only in a few DLLs of windows. In case, if the required gadget is not found, then the ‘phantom\_thread’ command falls back to perform hijacking of the thread, BUT without opening a handle to the target process which is still stealthier than most injection methods. This command uses indirect syscalls where required.

#### NOTE: Since this command requires an alertable thread, the operator needs to find a valid alertable thread which can be hijacked and alerted. C-Sharp process/Windows Apps cannot be hijacked.

![](https://bruteratel.com/images/post_img/2022-07-20-Release-Stoffels-Escape/phantom_thread.png)

### Custom Memory Hooks

The ‘memhook’ command was added to the current release which can be used to add custom hooks without using BOFs. This command can overwrite any valid region in memory with the opcodes provided by the operator, using indirect syscalls. Shown below is a simple example which prints a statement before and after calling Environment.Exit().

```
using System;
using System.Collections.Generic;
using System.Reflection;

namespace EnvExit
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Before Exit");
            Environment.Exit(0);
            Console.WriteLine("This should not print if patch failed\n");
        }
    }
}
```

Ths Environment.Exit() method resides in mscorlib.ni.dll. We can patch this method with a ‘xor rax, rax; ret’ to stop C-sharp executables from exiting when the dotnet is loaded in the current process with the ‘sharpinline’ command. The dotnet code to extract the Environment.Exit() address is available in the BRc4 package. This address can be patched with any user provided opcode. In the below example, it’s over written with opcodes to return zero in the rax register, before finally running the above dotnet code to check if the process still exits.

![](https://bruteratel.com/images/post_img/2022-07-20-Release-Stoffels-Escape/memhook.png)

As can be seen in x64dbg below, the memory location is now patched. This command is extremely powerful as you can manipulate the execution flow of functions on the fly including patching of syscalls at runtime.

![](https://bruteratel.com/images/post_img/2022-07-20-Release-Stoffels-Escape/memhook_x64dbg.png)

### Built-in Socks, Burnable Socks and Socks Over DOH

The original socks implementation (socksbridge) of Brute Ratel utilized a reflective DLL and a separate socks server (boomerang). However, this had it’s own limitations where it could not be used for nested pivoting with SMB and TCP. This command ‘socksbridge’ is now removed in replacement for the built-in socks in the badger. The built-in socks uses the current listener as a socks server, and also helps with nested pivoting. This feature also provides an option to use a burnable socks server without injection, and providing support for socks over DNS over HTTPS. The socks client in badger can be started or stopped with the ‘socks\_start’ and ‘socks\_stop’ command which will also autostart and stop the socks server on the active listener. A list of active socks server on the listener can be found by selecting ‘Server->View Active Socks’ Menu.

Pivoting Over Socks Over DNS Over HTTPS with Brute Ratel C4 - YouTube

Tap to unmute

[Pivoting Over Socks Over DNS Over HTTPS with Brute Ratel C4](https://www.youtube.com/watch?v=YY9K1iwLIDY) [Chetan Nayak](https://www.youtube.com/channel/UCpDI4t3oGuQNOpaX85daOrg)

![thumbnail-image](https://yt3.ggpht.com/s78j1PZDYdQ3Zlirsv6BfnTda3TzKvFmvQYVNTuD6sdFpQgj_m3fWhzC0f9vLicYVLY9BzBcBA=s68-c-k-c0x00ffffff-no-rj)

Chetan Nayak2.13K subscribers

The current implementaion also allows to use a burnable socks server with a different profile and sleep zero (without injection), while still making the badger’s core sleep with the operator provided sleep and jitter values. This means, if the operator does not want to use the current listener as the socks server, then the operator can start a separate socks server with an altogether different profile and request the badger to connect to the socks server using the ‘socks\_profile’ and the ‘socks\_profile\_start’ command just for pivoting. This will only route the socks traffic to the new server, while the badger’s core will still connect to the original listener with the user provided sleep and jitter values to execute commands. In short, single badger connecting to two different servers with different profiles and different sleep time. This temporary profile is auto-cleared from the memory of the badger when the ‘socks\_stop’ command is called. Note that while socks is active, the badger’s sleep masking will be disabled.

Burnable Socks Controller with Brute Ratel - YouTube

Tap to unmute

[Burnable Socks Controller with Brute Ratel](https://www.youtube.com/watch?v=psGT9ne1gT4) [Chetan Nayak](https://www.youtube.com/channel/UCpDI4t3oGuQNOpaX85daOrg)

![thumbnail-image](https://yt3.ggpht.com/s78j1PZDYdQ3Zlirsv6BfnTda3TzKvFmvQYVNTuD6sdFpQgj_m3fWhzC0f9vLicYVLY9BzBcBA=s68-c-k-c0x00ffffff-no-rj)

Chetan Nayak2.13K subscribers

### Coffexec Update

Similar to the badger’s core, Coffexec was also updated to use proxying of several function calls while loading the symbols from object files. The BOF supplied with Coffexec itself does not run in a seperated thread, but it also does not block the main thread, which means the main thread can still continue to sleep and fetch commands from the server. Three new BOF APIs were added to Coffexec - BadgerAlloc which allocates memory using badger’s custom heap, BadgerFree which also zeroes out memory before releasing it and BadgerSetdebug to enable debug privileges. More information on these can be found in [badger\_exports.h](https://bruteratel.com/assets/badger_exports.h).

### Updates to SMB and TCP Badgers

In all the previous releases every nested pivot required a new named pipe. For example, consider b-0 is your main http connection, and b-1 is your first SMB pivot connected to b-0. Now if you start a nested pivot b-2 in another system and connect to it via b-1, then you were needed to connect to the new SMB listener on b-1 via b-0. This is no longer required for nested pivots. This means if you connect to b-2 from b-1, b-1 will send all of b-2’s data directly from it’s own pipe instead of starting a new one. This reuse of existing HANDLE/Sockets not only apply to SMB, but also to TCP badgers. The TCP listeners were also updated to auto-stop listening on the listener port after a TCP connection is received while still maintaining the active TCP connection. This simply means as soon as a connection is received over TCP listener, the listener passes on the socket to a different thread and stops listening. The second thread however continues to interact with the TCP badger’s socket and maintains it till it is closed.

### Downloading Files

The ‘download’ and ‘shadowcloak’ command in the previous release used to show status of all active downloads in the terminal which was a sore to the eye. This release changes that. When a file starts downloading, it is added to a queue on the server. Thus there is no default output on the screen, unless ofcourse the download is completed. However, all downloads can be viewed using ‘list\_downloads’ command unlike earlier where the full download status was shown on screen. Downloads can be stopped with the ‘stop\_task’ command. This also applies to downloads over SMB, TCP and to the memory dump file downloaded with the Shadowcloak command.

### Other Badger Improvements

- The ‘pcinject’ command was removed as badger does not contain a reflective DLL anymore. The ‘shinject\_ex’ command was updated to provide more stealth as compared to the pcinject command
- The original keylogger implementation of Brute Ratel utilized a reflective DLL. The current release makes this code a part of badger which means no more reflective DLL
- The ‘screenshot’ command was updated to take screenshots of all desktops instead of just the main desktop
- The ‘detect’ command was renamed to ‘detect\_hooks’ which now auto detects hooks in ntdll, kernel32 and kernelbase.dll. The kernel32 and kernelbase.dll hook detections are only single jump based which might generate false positives
- The Sharpreflect and Sharpinline uses indirect syscalls where required
- The DCSync command supports syncing passwords from selected Domains using a user provided domain name
- ExitThread in SMB Badger now disconnects the SMB pipe before exiting the thread. This was an issue earlier when the SMB pipe stayed active even after the thread was exited due to which the pipe was not able to reconnect/re-link. This is now fixed
- Shellcodes can now run from any address in memory as it saves and restores original stack during return
- All tasks can now be stopped with the ‘stop\_task’ command, including stoping of socks client, tcp listeners, crisis\_monitor and all other commands

## Ratel Server

### Staging

Several changes were made to the ratel server on how the payload was built. Apart from dynamic payload encryption, the Ratel server now provides an option to build stages which are around 7-8kb depending upon the configuration of the malleable profile. These stages can be configured to autostop after a certain number of stages are downloaded from the listener, or can be stopped manually. Make note that staging is only supported over HTTP/S and all malleable profiles are supported. To enable staging, you can right click a listener and select Staging.

![](https://bruteratel.com/images/post_img/2022-07-20-Release-Stoffels-Escape/staging_0.png)

Similar to the badger, there are two types of stages that can be generated here. The default one which uses indirect syscalls and another ‘stealth’ payload which uses indirect syscalls alongside searching the PEB for loaded DLLs and proxying the loading of DLLs via other legitimate functions, if they are not found in PEB. The ‘stealth’ feature is only available for x64 payloads.

![](https://bruteratel.com/images/post_img/2022-07-20-Release-Stoffels-Escape/staging_1.png)

One of the issues found in the previous release was that the shellcode of badger returned quickly after executing the reflective DLL which caused issues with tools like Macropack. This release fixes that issue by providing three different exit methods i.e. return (default), RtlExitUserThread and WaitForSingleObject. The ‘WaitForSingleObject’ was specifically built to work alongside alertable threads where if you spawn an executable which returns quickly (eg.: werfault.exe or searchprotocolhost.exe), the shellcode doesn’t complete it’s execution. When you execute the badger’s shellcode, it spoofs the entrypoint of the stage and stack, executes the stage and then returns quickly. Only the spoofed thread runs in this case. However, if QAPC was used to execute the badger’s shellcode, and if the badger’s shellcode returned after executing the stage, QAPC resumes the main thread of the suspended process allowing it to exit. In order to avoid this issue, WaitForSingleObject was introduced which waits on the thread handle of the spoofed thread, so that the main thread does not resume when used with QAPC.

## Commander

Commander is now updated to show the active thread in which the badger is residing in a specific process. This feature was added to supplement the thread stack spoofing command so that the user knows where the badger is residing. Apart from this, several minor changes were made to the commander as follows:

- Added option to configure jitter and sleep when building a listener or a payload rather than having to depend on ‘autoruns’
- Added file download and delete option in File Explorer
- All tasked commands are shown with their respective thread ID and task ID in grey color in Commander’s Terminal. This helps to keep a track of all tasks and their threads
- The Dcsync command’s output is now automatically parsed and added to the Credentials tab
- Added option to change the text and background color of badgers. Colors are saved across sessions but are not unique per operator and will affect all Operators using Commander
- Added Several shortcut options to to the UI
  - Alt+1 : Select Listener Tab
  - Alt+2 : Select Badger Tab
  - Alt+3 : Select Credential Tab
  - Ctrl+H : Add HTTP Listener
  - Ctrl+D : Add DOH Listener
  - Ctrl+P : Add Payload Profiler
  - Alt+D : View Downloads
  - Alt+L : View Logs
  - Ctrl+1 : Show Operator Menu
  - Ctrl+2 : Show C4 Profiler Menu
  - Ctrl+3 : Show Server Menu
- Updated Process Manager to search processes in non-case-sensitive format
- Renamed ‘list\_pivot’ command to ‘list\_tcppivot’ so as to not create a confusion that it lists all pivots
- Moved Switch Profile, Process Manager, File Explorer and Clickscript options to the Arsenal menu
- Added better accessibility related settings for visibility enhancement

### End Notes

Apart from the plethora of changes made to the badger, there were also several changes made to the procedure of providing trial licenses to possible customers. To safeguard the existing customer’s interest, it was decided that trial licenses will not be updated anymore. Companies who request trial licenses will only be provided with the latest update to v1.0.x releases and only licensed users will be allowed to update. This action was taken to make sure trial users don’t upload the latest payloads to Virus Total out of immaturity.

I will close this blog with a final note to all my customers that due to the nature of the software, it is implied that it will always be a cat-and-mouse game between EDRs and BRc4. But at the same time, one important thing that Brute Ratel will always focus on, is to provide cutting edge evasion tactics within the product. It is highly recommended to upgrade to this release as this brings in several changes to the core of badger, both from the feature and the security point of view. Due to way, the core was re-developed, this brought in a myriad of possibilities to enhance how the payload looks and works in memory, and the next releases will only make it better.