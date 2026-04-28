# https://bruteratel.com/release/2023/03/19/Release-Nightmare/

## Release v1.5 (Nightmare) - Ghosts From The Past

![](https://bruteratel.com/images/post_img/2023-03-07-Release-Nightmare/badger.png)

Brute Ratel v1.5 codename Nightmare is now available for download. This release brings in new evasion techniques and user experience updates (QOL) requested by the BRc4 community. A quick summary of the changes can be found in the [release notes](https://bruteratel.com/release_notes/releases.txt). This release also brings several changes to the licensing server which now provides support for backward compatibility. More on this at the end of the blog.

## Feature Additions

### Revamping Module Stomping

The highlight of this release is module stomping. _Nightmare_, the name of the release is what I went through, in order to get this feature working. Module stomping, in itself is not a new feature. This was introduced several years back in Cobaltstrike, however the technique we are going to discuss today is very different from anything publicly available. Module Stomping is pretty handy as it overwrites the ‘.text’ section of a DLL. This means all calls originating from our shellcode/reflective DLL will be backed by a file on disk. Thus, there is no need for call stack spoofing and it provides easy evasion from ETW and similar detections. However one has to be careful on how it is implemented, else it becomes evidently [easy to detect, as is the case of Cobaltstrike](https://github.com/slaeryan/DetectCobaltStomp). Lets split our technique into 3 sections and walkthrough through it in detail. If you dont want to read through this below, you can go through [this youtube video](https://youtu.be/nPmcFKSHyvg) here wherein I explain the same things below.

#### 1\. The Curious Case of LoadLibraryEx

Cobaltstrike and most other module stomping techniques use LoadLibraryEx to load a DLL into memory. LoadLibraryEx does not call the entrypoint (Dllmain) of the loaded DLL and it does not resolve IAT. If we use _LoadLibrary_ instead of _LoadLibraryEx_, the windows loader calls Dllmain and links our DLL into PEB. This is not suitable for module stomping as our stomped DLL might load other DLLs, which can start some threads. Thus if we overwrite this region with our shellcode/rdll, we might end up crashing as there might be threads which are already running via DllMain. Thus _LoadLibraryEx_ ends up being the perfect choice of API for module stomping, which takes in a third parameter ‘ _DONT\_RESOLVE\_DLL\_REFERENCES_’. This means our DLL will be loaded from disk and mapped into memory, but the windows loader wont call its entrypoint. Another important thing to note here is that since the loader is not calling the entrypoint, it will change some Flags in the \_LDR\_DATA\_TABLE\_ENTRY which is critical for module stomping detection. For the defenders, here are a list of things to monitor:

- Entrypoint of the stomped DLL is null. This means the DLL does not have an entrypoint. Thus whenever there are “PROCESS ATTACH/THREAD ATTACH” events within the process, this Dllmain will not be called
- ImageDLL flag is marked as false. This means DLL was loaded as an Exe and not DLL
- LoadNotificationsSent flag is marked as false. This means the DLL’s load notification was not sent
- ProcessStaticImport will be false. This means the import of the DLL is not processed

![](https://bruteratel.com/images/post_img/2023-03-07-Release-Nightmare/non_spoofed.png)

The above anomalies are usually enough to detect Cobaltstrike or other module stomping techniques. Another easy way to detect module stomping is to check the ‘.text’ region of the DLL on disk and the one in the memory of the process.

#### 2\. Full PEB Linking and Entrypoint Patching

Linking PEB flags are not as hard as it is to spoof the entrypoint. In case of LoadLibraryEx, we can see in the image above, that it is set to null. The reason being that whenever any new DLL gets loaded, the loader walks this PEB and calls the Dllmain of all the DLLs in memory. This is the design implementation of microsoft wherein the Dllmain accepts 3 arguments. The second argument is provided by the loader to the Dllmain whenever there are PROCESS ATTACH, DLL THREAD ATTACH, DLL THREAD DETACH AND DLL PROCESS DETACH events. Thus, if an entrypoint added to the PEB is invalid, our process will crash. If we keep it to null, the windows loader ignores it. This means we have to make sure the correct entrypoint of the DLL is added added here.

![](https://bruteratel.com/images/post_img/2023-03-07-Release-Nightmare/dllattached.png)

NOTE: Image is from [microsoft website](https://learn.microsoft.com/en-us/windows/win32/dlls/dllmain)

#### 3\. Control Flow Guard

If you have succesfully linked the PEB and avoided generic detections like that of Cobaltstrike, we have another problem at hand. In the Windows 8.1 Update KB3000850, microsoft introduced [Control Flow Guard](https://learn.microsoft.com/en-us/windows/win32/secbp/control-flow-guard) which blocked any indirect calls originating from an invalid function start address. This means all indirect calls should be called from a valid start address and not from the middle of any code from any ‘.text’ region. This information about the valid function locations are stored as the _Characteristics_ of each section in the PE which can be read using a CFF explorer by doing bitflag checks. However this is a bit trickier than expected. Ideally, if we just copy our code to the entrypoint of a stomped DLL, it should work because entrypoint is a valid start of a function. Lets take an example of staged metasploit shellcode which is of 512 bytes. If our entrypoint code (in DLL) is of, say only 1000 bytes, and our shellcode that we copied is of 512 bytes (metasploit), our staged code will simply allocate new memory, copy reflective DLLs to the newly allocated region and execute them. This is not operationally safe, because we are indirectly allocating a new region. Thus most POCs you see with metasploit will work (as POC only), but does not do any benefit in terms of evasion for the final stage. Because unlike POCs, to perform proper evasion, we have to make sure our full PE code is backed by a valid `.text` section on disk. This means we cannot use staged code, and our reflective DLL or second stage should be within the .text region and it should start from a valid call target to avoid CFG.

All C2s use some sort of PE or reflective DLL for stageless payloads and these are usually more than 150-200kb as they might contain several post-exploitation code unlike staged code. So what happens if our `.text` region is say 300kb, entrypoint code is of, say only 1000 bytes, and our shellcode that we copied is of 200 kb reflective DLL? This means we end up overwriting another function in the ‘.text’ region. Now if we perform any type of threaded calls from this region, especially if the process is a CFG-enabled process (which most of the windows processes are), then we will end up calling `ntdll!LdrpDispatchUserCallTarget` which will check the indirect call location and the bitflags enabled for that location. The `ntdll!LdrpDispatchUserCallTarget` is an internal function of ntdll.dll (notice the p in Ldrp) which takes an argument in the RCX register. This argument is the address region which needs to be vetted for invalid call targets. If the region from where the call is originating invalid, `ntdll!LdrpDispatchUserCallTarget` calls _RtlFailFast2_ with a _STATUS\_STACK\_BUFFER\_OVERRUN_ exception which kills our process instantly. More details on this error can be found in this [blog](https://devblogs.microsoft.com/oldnewthing/20190108-00/?p=100655). This means, if we want to evade CFG, we have to disable CFG on our stomped DLL’s executable region. A detailed workflow on CFG can be found in [this blog written by Trend Micro](https://documents.trendmicro.com/assets/wp/exploring-control-flow-guard-in-windows10.pdf). Below is the callstack for a thread which called _LdrpDispatchUserCallTarget_.

![](https://bruteratel.com/images/post_img/2023-03-07-Release-Nightmare/ldrpcallstack.png)

### Advanced Module Stomping Evasion

Badger overcomes all the above anomalies in two ways:

1. Badger deletes all of its region from the memory of the process while sleeping and restores the original DLL’s buffer till the sleep is complete. This is done alongside stack spoofing, stack encryption and heap encryption to avoid all traces of the badger and it’s data while sleeping. Thus if anyone scans the stomped module to perform a comparison of on-disk and in-memory regions while the badger is sleeping, it would look the same. When the badger is not sleeping, all of the evasions still work except the .text region of the DLL contains the badger’s .text region.
2. The PEB LDR module uses a custom hook to reflect the necessary changes to avoid detections for entrypoint and DLL Flags which can also be seen in the above youtube video.

For people interested in using their own custom module stomping technique, I have added commands `cfg_disable` and `cfg_enable` to disable or enable Control Flow Guard. This is not required for the badger, but if you want to create a process and perform module stomping injections with your own post exploitation toolkit, then CFG can be enabled to disabled using these commands.

Make note that even with all these evasions, its an operator who has to be careful with what module they want to stomp. Overwriting sections of bad DLLs can lead to a process crash, especially if the DLL you stomped is being utilized by some other module/code in your process. The module stomping feature can be enabled via Payload Profiles or during Listener creation. Make note that module stomping is disabled for DLLs generated by the Commander. Reason being if a DLL loads a module and calls its DllMain, this Dllmain (now badger) will call LoadLibrary to load other DLLs. But since this Dllmain will be under loader lock, you cannot load other DLLs. Thus module stomping will not work with DLLs or DLL sideloads. Staging also supports module stomping. This means you can stomp a stage yourself, and let the stage stomp your stageless code into another stomped module.

### Process Injection via Remote Procedure Call

This release brings in a new undocumented injection technique via remote procedure call. This can be enabled on the fly for remote process injections via _set\_threadex_ command similar to other process injection techniques. The ID for this technique is 12. Make note that your target process needs to be in an alertable state to perform this injection.

![](https://bruteratel.com/images/post_img/2023-03-07-Release-Nightmare/rpc.png)

### Pass The Hash

This feature addition is a result of several user requests for a built-in Pass The Hash functionality. You can choose to spawn a new process from an ntlm hash or simply impersonate a token from it. This pth is an improvised version of Mimikatz’s PTH functionality with more built-in OpSec.

![](https://bruteratel.com/images/post_img/2023-03-07-Release-Nightmare/pth.png)

Apart from the major updates above, several changes were made to the shellcode, badger’s core and Commander. Below is a quick list of those changes

- Webhook forwards the command name alongside the output received from the badger. This can be use to actively track various command outputs via API without having to use ‘greedy’ parsing when data is forwarded to logstash or elasticsearch
- Replaced RtlRegWait function for proxy calling of Windows API and NTAPI to a new undocumented function
- Improved http header parsing for the badger. Commas can be used in the http headers now. Applies for Stage Zero too
- Improved post request/response parsing for badger. Any values can be used in the http requests/responses now
- Updated _memexec_ hooks for ETW evasion
- Added module stomping option to listeners and payload profilers in Commander
- Added color option to highlight the double clicked folder in File Explorer
- Listing files in File Explorer now also displays files in the terminal
- Improved Commander terminal for stop and go scrolling. Users can scroll to the top without the scroll being autoreset to the latest output when a new output is added by the server
- Process Managers and File Explorers UI for every badger are now locked to a single instance
- Fixed HTTP Edit Listener option to overwrite existing malleable requests instead of showing the same one when loaded

Brute Ratel’s download page now also supports downloading an older version of the package. You can select the latest package or one release (main) behind the current release. This previous release will be the last major release of the previous version. Since v1.5 is now released, v1.4.5 will stay active as the previous package till v1.6 is released. Thus, if v1.5.1 or v1.5.2 gets released, the older version will still stay v1.4.5 as these releases are minor releases of v1.5.

Several other changes were made to the backend to optimize how the server handles the badger data and the shellcode generation. This release more or less likely, covers up the much needed post-exploitation techniques within the badger. There are a few more scheduled releases for the upcoming month which introduce some brand new ways of evasion for BRc4. Stay tuned and Happy Hacking :)