# https://insinuator.net/2026/04/windows-early-boot-configuration-the-cmcontrolvector-and-pspsystemmitigationoptions/

While investigating how process mitigation settings are initialized, I encountered the global variable `PspSystemMitigationOptions`. Tracing how this value is populated led me to the `CmControlVector`. In this blog post, we take a look at the Windows kernel land configuration manager, especially its global `CmControlVector` variable. Quick note: the kernel’s configuration manager is not related to Microsoft Intune’s [Configuration Manager](https://learn.microsoft.com/en-us/intune/configmgr/core/understand/introduction). In short, the configuration manager is responsible for managing and implementing the registry. However, it is also responsible for setting up parts of the system during early boot.

This blog post is structured as follows:

- First, a bit of background on how I encountered the `CmControlVector`. It was of course via a detour.
- Next, we discuss when and how the `CmControlVector` is processed by the kernel’s configuration manager.
- Finally, we take a peek into the `CmControlVector` variable and extract some insights.

Recently, a question regarding a process’s `MitigationFlags` came up. These flags encode the exploit mitigations the kernel (or process itself) applies to a process. The information regarding enabled mitigations are stored in the process’s `_EPROCESS` structure. Many exploit mitigations already play a role during process initialization. In the past (see, for example, our work on the [Application Compatibility Infrastructure](https://insinuator.net/2024/04/bsi-publishes-windows-10-sisyphus-reports-application-compatibility-infrastructure-microsoft-defender-antivirus-etw-usage-and-device-setup-manager-service/)), we often had to debug the process creation procedure under Windows. And so from time to time, we had already stumbled across the `PspSystemMitigationOptions` global variable. This one is prominently used in `PspAllocateProcess` when a newly created process is allocated.

To make a long story short, the global `PspSystemMitigationOptions` is combined with per-process (more precisely, per-image) settings stored in the registry. These are known as `Image File Execution Options` (`IFEO`). Together, they form the effective `MitigationFlags`, which are then transformed and stored in a process’s `_EPROCESS` structure. For this blog post, we don’t need to dive deep into this setup and merging procedure. But in broad strokes, the process is as follows: the system-wide and per-image settings are combined into the effective mitigation settings. They are then transformed into the three `MitigationOptions` of the `_EPROCESS` structure. This transformation consists mostly of rearranging the bit order and applying some additional checks and lookups. In the `_EPROCESS` they are called `MitigationOptions`, `MitigationOptions2` and `MitigationOptions3`. The `MitigationOptions` have evolved over time, and with new releases of Windows and new mitigations that are implemented there are now three 64-bit values that encode the `MitigationOptions`.

Both, the per-image and system-wide settings are stored in the registry. The `IFEO` options are set as the name suggests, per-image. This registry key can be used to configure more than only mitigation options and is [partially documented](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/xperf/image-file-execution-options). I typically use the `IFEO` options to attach a debugger (preferably a time-travel debugger) when a process launches. The `MitigationOptions` value are located for each image under:

- `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\<ImageName.exe>`

The system-wide mitigation settings are stored under:

- `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\kernel`

This can easily be identified by changing the so-called [“Exploit protection”](https://learn.microsoft.com/en-us/defender-endpoint/enable-exploit-protection) settings and using Procmon to trace registry usage. However, this gives the location where the settings are stored, and via the stack trace which code is responsible for setting them. But we don’t know the component that is responsible for reading them in. For the `IFEO``MitigationOptions`, it was quite clear that they are read during process allocation in `PspAllocateProcess`. The procedure for reading the system-wide mitigation settings from the registry is not that obvious right away. While investigating, I also read a bit about what [others](https://www.orangecyberdefense.com/global/blog/cybersecurity/fairy-law) had to say about the `PspSystemMitigationOptions`. While skimming the article, some points stood out, such as that the settings are “populated from boot-time registry configuration” and that “changes to MitigationOptions made at runtime are therefore ignored until the next reboot”. This is indeed the case, and Windows notifies a user when the system-wide “Exploit Mitigation” settings are changed that a reboot is required for the changes to take effect.

The referenced article also mentions when system-wide mitigation settings are read from the registry; however, I skimmed over this part. Instead, I choose to investigate, again, with Procmon. I set up a boot trace with Procmon, rebooted the system, and to my initial surprise, the registry value was never read. So, I repeated the process, again, with the same outcome. This suggests that the value is referenced before Procmon has started! In parallel, I did some light reversing. The `PspSystemMitigationOptions` themselves are not referenced during initialization. Cross-references always expected them to be set and read them directly. But I soon found out that the `PspSystemMitigationOptions` are referenced in a larger structure, the `CmControlVector`, which is used in `nt!CmpGetSystemControlValues`. To be sure, I decided to verify my expectations from my static reversing by placing a data breakpoint on `PspSystemMitigationOptions`. Indeed, as expected, I got a hit on my breakpoint, and `nt!CmpGetSystemControlValues` was prominently located in the call stack as shown below:

```
kd> k
 # Child-SP          RetAddr               Call Site
00 fffff802`8107b258 fffff802`ef23dacc     nt!memcpy+0x32
01 fffff802`8107b260 fffff802`ef239bd2     nt!CmpGetBootValueData+0x210
02 fffff802`8107b2d0 fffff802`ef239184     nt!CmpGetSystemControlValues+0x38a
03 fffff802`8107b590 fffff802`ef1fbef0     nt!CmInitSystem0+0x1c
04 fffff802`8107b5c0 fffff802`ef14a156     nt!InitBootProcessor+0x268
05 fffff802`8107b7d0 fffff802`ef13c623     nt!KiInitializeKernel+0x816
06 fffff802`8107bab0 00000000`00000000     nt!KiSystemStartup+0x283
```

Now that we have confirmed what we already expected, we need to put it into context. We are indeed dealing with configuration manager code inside the kernel. This means that we are still in phase zero of the kernel initialization. In general, the Windows kernel initialization has two phases: Phase 0 and Phase 1.

- Phase 0 performs early, low-level setup using minimal resources, initializing core components like memory management, interrupts, and the hardware abstraction layer while the system is still single-threaded. This is also where the registry is set up and the `CmControlVector` is read.
- Phase 1 continues with full system initialization, enabling multitasking, and initializing device drivers and system services.

This explains why Procmon never captured the registry access: the `CmControlVector` is processed during Phase 0, before drivers and user-land tooling is available.

Now the interesting question: What is the `CmControlVector`, and how is it processed? Essentially, it is an array of type `CM_CONTROL_VECTOR`. The following list provides an overview and shows the values for the `PspSystemMitigationOptions`

- `pKeyPath`: a unicode string with a registry path. In this case: `Session Manager\Kernel`
- `pValueName`: a unicode string with a value name. In this case: `MitigationOptions`
- `pTargetBuffer`: a pointer to a target buffer. Potentially, there is a default value. In this case: `PspSystemMitigationOptions`, with no default value.
- `pSizeOptional`: a pointer to the size of the expected data. In this case: `PspSystemMitigationOptionsLength` which is `0x18`.
- `typeOptional`: an optional type. Which is not set in this case.
- `flagsOptional`: optional flags. Which is also not set in this case.

During kernel initialization, the `CmControlVector` is iterated entry by entry. Each entry is used to read a value from the registry. The result is then stored in the corresponding target buffer. For our case, this would be the `PspSystemMitigationOptions`. This also confirms that this registry value is indeed only read once during early boot and then stored in the global variable `PspSystemMitigationOptions`. Afterwards this global variable is then only read, but not modified anymore. However, the `PspSystemMitigationOptions` are only a small portion of the `CmControlVector`. Considering Windows 11 LTSC 24H2, the `CmControlVector` contains 563 entries.

To gain some insight into `CmControlVector`, I created a small IDA script to extract the information. While some target buffers (like `PspSystemMitigationOptions`) are referenced by a symbol, others are anonymous. To gain more insight, the script also collects cross-references for each target buffer. This helps identify which kernel component uses a given configuration entry. It is indeed only a small portion that has no symbol, and mostly related to the memory manager. This is obvious on the one hand from the registry location, and the function that uses the variable.

The script to extract the data is available [here](https://github.com/ernw/insinuator-snippets/blob/master/CmControlVector/extractBootValues.py), and a list of all results is available [here](https://github.com/ernw/insinuator-snippets/blob/master/CmControlVector/CmControlVectorData.json). And finally, I collected some more or less interesting information [here](https://github.com/ernw/insinuator-snippets/blob/master/CmControlVector/Stats.txt). This one lists statistics on whether entries have an option size, type, or flags set, and finally, which kernel component uses the variables. This one is based on the function prefix. Note that it lists the private and non-private prefixes separately, i.e., `Etw` and `Etwp`. I did not normalize these prefixes, as some cases (e.g., `PnP`) make automated grouping ambiguous. Furthermore, with other parts, the private or internal part is referenced instead with an `i`, for example, in the case of the memory manager that uses the `Mi` prefix.

* * *

In case you’re interested, here are other recent Windows internals contributions from [ERNW](https://ernw.de/):

- [Windows Hell No for Business](https://blackhat.com/us-25/briefings/schedule/#windows-hell-no-for-business-45865)@ Black Hat USA 2025

  - Related blog post: [Windows Hello for Business – Faceplant: Planting Biometric Templates](https://insinuator.net/2025/08/windows-hello-for-buiness-faceplant-planting-biometric-templates/)
  - Related blog post: [Windows Hello for Business – The Face Swap](https://insinuator.net/2025/07/windows-hello-for-business-the-face-swap/)
  - Related blog post: [Windows Hello for Business – Past and Present Attacks](https://insinuator.net/2025/06/windows-hello-for-business-past-and-present-attacks/)
- [WinpMem: Volatility’s driver that lets malware volatilize](https://www.youtube.com/watch?v=hZjPvYSxDdM)@ Recon 2025

  - Related [white paper release](https://insinuator.net/2025/10/white-paper-73-analyzing-winpmem-driver-vulnerabilities/)
- [Jigsaw RDPuzzle: Piecing Attacker Actions Together](https://insinuator.net/2025/01/jigsaw-rdpuzzle/)

### Leave a Reply [Cancel reply](https://insinuator.net/2026/04/windows-early-boot-configuration-the-cmcontrolvector-and-pspsystemmitigationoptions/\#respond)

Your email address will not be published.Required fields are marked \*

Comment \*

Name \*

Email \*

Website

Δ