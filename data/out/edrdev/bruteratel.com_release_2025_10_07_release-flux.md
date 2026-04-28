# https://bruteratel.com/release/2025/10/07/Release-Flux/

## Release v2.3 - Flux

Brute Ratel v2.3 (codename Flux) is now available for download. A key focus of this release was complete redevelopment of the Badger implant using a custom-built compiler, designed to improve operational security (OpSec) and significantly reduce its memory footprint. During development, I noticed several limitations in the existing MinGW and Clang toolchains, particularly in how they handle certain memory regions and stack layouts. To address these issues, the MinGW/Clang compiler provided limited support, as ideally, these are not options that a general developer would ideally want to mess with. But the built-in optimizations were a tad bit problematic when dealing with my stealth requirements. Thus, I ended up creating a tailored variant, capable of optimizing the Badger’s compilation process to meet the required stealth requirements. As a result, the size of the full Badger implant has been reduced by 30% in this release, with further reductions expected to reach around 60% in the next iteration — all while retaining the full feature set.

Due to the extended development cycle and the one-month delay already incurred, not all optimizations from the new compiler could be fully integrated into this release, however they are scheduled for inclusion in the upcoming version. It is strongly recommended to review the accompanying blog post and documentation before deploying the new release.

## Badger

### Safe HTTP Requests

A new option called **_safe\_http_** has been added under the **_OpSec_** tab in listener and payload profiles. When enabled, this feature uses an extremely lightweight 2–3 Kilobyte PIC stub to send HTTP requests backed by a valid stack designed by the operator, while keeping the Badger’s entire code and heap encrypted. In practice, this means that during the request, neither the Badger nor its thread actually exists in memory until the HTTP transaction is fully parsed and completed. When the HTTP request is made, everything related to the badger is encrypted, making it extremely difficult to have yara detections as the PIC stub doesn’t have anything in it, that can be used to build a detection on. This approach helps mitigate certain detection techniques, particularly from EDRs that leverage ETW-based memory scans triggered by network activity through wininet or winhttp libraries. Do note that **_safe\_http_** does not work with **_disable\_http\_telemetry_** option, since that feature is not required when **_safe\_http_** is enabled.

### Advanced Async BOF (AAB)

BOF execution in Brute Ratel has always been asynchronous, but until now it lacked a way to hide the Badger while the BOF ran. This release overhauls BOF behavior. Thanks to the custom compiler I developed, I was able to rewrite the BOF loader from the ground up to support new BOF APIs and a redesigned BOF loader.

We’ve added a new command, **_coffexec\_async_**, which is separate from the existing **_coffexec_**. **_coffexec\_async_** runs independently of the Badger and exposes new APIs that enable the BOF to operate while the Badger remains hidden. The updated BOF APIs also provide improved stealth controls and sleep-masking interaction with the Badger. Advanced async BOFs can even run concurrently i.e. multiple BOFs can execute while the Badger stays masked and dormant.

The core logic of the AAB would be:

```
Badger Main Thread {
    coffexec_async {
        void coffee(...) {
            BadgerForceSleep(dispatch, 60);                 // induce forced sleep for 60 seconds
            BadgerDispatch(dispatch, "Hello World 1");      // print hello world 1
            BadgerDispatch(dispatch, "Hello World 2");      // print hello world 2
            BadgerWakeupAndSend(dispatch);                  // send buffered data instantly before proceeding ahead
            BadgerWakeupAndExit(dispatch);                  // Wake up the badger interrupting the above forced sleep and return to badger's main thread
        }
    }
}
```

//
To clarify the pseudo code above, when the Badger executes an asynchronous BOF, the operator can invoke the **_BadgerForceSleep_** API to place the Badger into sleep masking mode. This allows any sensitive tasks to be executed entirely without the Badger being present in memory. Once the task is complete, the operator can terminate the async BOF using **_BadgerWakeupAndExit_**.

Another API, _**BadgerWakeupAndSend**_, can be used in both **_coffexec_** and **_coffexec\_async_** to pause BOF execution midway and send any buffered content queued via **_BadgerDispatch_**. However, calling **_BadgerWakeupAndSend_** within **_coffexec\_async_** will wake the Badger and break its sleep mask, so it should be used carefully.

A few additional notes:

- Asynchronous BOFs function differently from regular BOFs, and as of this release, **_BadgerSpoofStackFrame_** API is not yet supported within async BOFs. However, a working implementation has been identified and will be included in version 2.4.
- Async Badger functionality requires sleep masking to be enabled. If the Badger’s sleep value is set to zero and coffexec\_async is invoked, a minimum 1-second sleep interval will automatically be applied before executing the async BOF.

Further details on the new BOF APIs are provided below.

#### BadgerForceSleep (async only API):

```
DECLSPEC_IMPORT BOOL BadgerForceSleep(WCHAR** dispatch, DWORD seconds);
```

This API instructs the Badger to encrypt and conceal itself in memory. It returns TRUE if masking is successfully initiated, and FALSE otherwise. Masking only occurs when no other active tasks are running within the Badger. For example, if an asynchronous task such as **_sharpinline_** is active, invoking this API will not trigger sleep masking — the **_sharpinline_** thread must return to its designated execution context, and therefore, its executable region cannot be encrypted. The API accepts a parameter specifying the number of sleep seconds, independent of the Badger’s configured sleep/jitter settings. Once invoked, masking remains in effect until either the specified time expires or one of the wakeup APIs — **_BadgerWakeupAndExit_** or **_BadgerWakeupAndSend_** — is called. If this API is not executed within **_coffexec\_async_**, the Badger will continue using its standard sleep masking behavior as defined by the operator’s **_sleep/jitter_** configuration. Essentially, this API overrides the existing sleep mask configuration and enforces a forced sleep state.

#### BadgerWakeupAndExit (async only API):

```
DECLSPEC_IMPORT VOID BadgerWakeupAndExit(WCHAR** dispatch);
```

This API terminates the Badger’s sleep mask and returns control from the BOF to the Badger’s main thread. It is critical to invoke this API at the end of every asynchronous BOF you implement. Failing to call this API at the end of the **_coffee_** function will cause the Badger to terminate.

#### BadgerWakeupAndSend:

```
DECLSPEC_IMPORT VOID BadgerWakeupAndSend(WCHAR** dispatch);
```

This API is compatible with both **_coffexec_** and **_coffexec\_async_** commands. It takes the data buffered by **_BadgerDispatch_** and instructs the Badger’s main thread to immediately transmit it to the Ratel server. If the Badger is currently in a sleep-masked state, invoking this API will temporarily break the sleep mask to allow the buffered content to be sent.

#### BadgerStopTask:

```
DECLSPEC_IMPORT BOOL BadgerStopTask(WCHAR** dispatch);
```

This API is supported by both **_coffexec_** and **_coffexec\_async_** commands. It allows a BOF to check whether the operator has issued a **_stop\_task_** command. By integrating this API into your code, you can detect when a stop request has been made—if the function returns TRUE, you can gracefully exit your routine or perform any necessary cleanup operations. This approach gives the operator greater control over task management without forcefully terminating a BOF thread, which could otherwise lead to memory leaks and compromise both OpSec and overall stability.

#### BadgerDownloadBuffer:

```
DECLSPEC_IMPORT BOOL BadgerDownloadBuffer(WCHAR** dispatch, CHAR *fileName, PVOID fileBuffer, unsigned long long fileSize);
```

This API is compatible with both **_coffexec_** and **_coffexec\_async_** commands. It accepts multiple arguments — primarily the filename, the complete file buffer, and the actual file size to be uploaded to the Ratel server. The data is transmitted using the Badger’s main HTTP thread and is automatically sent once the BOF execution completes.

#### BadgerSetToken:

```
DECLSPEC_IMPORT VOID BadgerSetToken(WCHAR** dispatch, HANDLE hToken);
```

This API is supported by both **_coffexec_** and **_coffexec\_async_** commands. While **_BadgerSetToken_** is not a new API, this release introduces a minor update — it now expects two arguments: the first being **_dispatch_**, and the second the token value. This adjustment was implemented to ensure compatibility with the **_coffexec\_async_** command. If you’re using this API in BOFs built with earlier BRc4 versions, it is recommended to update your code to reflect this change.

### Features Ported To Async BOF

With the introduction of the new Async BOF framework, it made sense to make certain Badger features more autonomous. After gathering feedback and discussing ideas with our customers in the Discord channel, I decided to transition several commands to run as Async BOFs. This allows them to operate independently while the Badger remains in its sleep-masked state.

- crisis\_monitor
- portscan
- samdump
- pth
- dcsync
- shadowcloak

When executing any of the above commands, it’s recommended to configure the Badger with a sleep interval of at least 30 to 60 seconds. This ensures you gain the full benefit of the sleep masking feature during their execution. And in order to make it easy to understand how Async BOFs work, there is an example BOF present in the sample\_config directory in the brc4 package named **_async\_bof\_test.c_**, which might be more helpful to operators.

### Other QOL Updates:

- Added a new b\_count key to the Badger profile, which tracks the total number of connections the Badger has made to the server.
- Added the **_dump\_sharpinline_** command to retrieve output from partially completed **_sharpInline_** executions.
- Added the **_stop\_sharpinline_** command to terminate an active .NET task initiated by **_sharpInline_**.
- Updated **_sharpinline_** to support running multiple versions of dotnet to run simultaneously within the same Badger instance.
- Updated the **_samdump_** command so it no longer impersonates SYSTEM by default. Operators without ‘SYSTEM’ privileges can use **_get\_system_** or their own privilege escalation methods before running samdump.
- Improved error handling — GetLastError, HRESULT, and NTSTATUS codes are now parsed by the Ratel server and displayed directly in the Badger terminal, instead of showing generic error messages.
- Updated command history behavior — the Badger terminal now logs invalid commands as well, instead of storing only successfully executed ones.
- Optimized memory usage for screen recording ( **_record\_screen_**) functionality
- Updated the Badger and Ratel server download mechanisms — when downloading a file with an existing name in the downloads directory, the old file is now deleted and replaced with the new one. Downloads are also performed on the main thread instead of a separate one.
- Added a validation check to detect if a BOF is already using a stomped module; if so, any concurrently executed BOF will skip the stomping process.
- Merged the **_memdump_** and **_shadowcloak_** commands — both functionalities are now available under **_shadowcloak_**.
- Simplified the **_impersonate_** command to accept only the token ID, rather than both username and ID.
- Improved the version mismatch dialog in Commander to make it less intrusive and more informative.
- Fixed an issue with **_net group_** where group names containing spaces were not accepted.
- Fixed a hardware breakpoint handling bug in **_coffexec_**.
- Fixed a **_schtquery_** issue where full task names containing spaces were not being read properly.
- Fixed a token parsing bug that required a double backslash.
- Resolved a rare DNS mutex issue that occurred when the server was terminated and restarted.
- Fixed a UI issue where the Process Manager and File Explorer windows, sometimes would not close properly.
- Removed ‘0.0.0.0’ from the internal IP list displayed in the Badger tab.
- Removed argument spoofing and lock screen features.
- Removed YARA rules from Litterbox.
- Removed legacy DLL and service executable detection logic.

While this post highlights many of the major updates in the Flux release, several additional changes have intentionally been left out to keep certain features away from EDRs. A significant portion of this update also involved deep backend improvements that strengthen stability, performance (for socks/rportfwd), and OpSec capabilities.

The next release will push things even further — with the new compiler framework designed to push Badger’s stealth and resilience against modern EDRs to an entirely new level. It’s going to be a crazy one.