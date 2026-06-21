# https://research.nasbench.dev/research/windows-processes/dllhost

[Archive](https://research.nasbench.dev/research) [Process Anatomy](https://research.nasbench.dev/research/categories/process-anatomy)

Process Anatomy

# Windows Process Internals - Dllhost Explained

A deep dive look at dllhost.exe and how it works.

Collection **Process Anatomy**

Read Time **2 min**

Created **2026-05-06**

Last Updated **2026-05-06**

windows-processeswindowswindows-internalscom

This `dllhost.exe` writeup is a continuation / revisit of my original blog from 2020 titled [What is the “DLLHOST.EXE” Process Actually Running](https://nasbench.medium.com/what-is-the-dllhost-exe-process-actually-running-ef9fe4c19c08). This time around the focus is code analysis from a reverse engineering perspective. Lets dive in!

| Default location |
| --- |
| C:\\Windows\\System32\\dllhost.exe |
| C:\\Windows\\SysWOW64\\dllhost.exe |

## Explaining Dllhost.exe's From Main [\#](https://research.nasbench.dev/research/windows-processes/dllhost\#explaining-dllhostexes-from-main)

The `dllhost.exe` binary itself is pretty small. It's just a `wWinMain` function that does the following:

1. Parse the CLI to look for a colon `:`.
2. If a colon exists and the text before it is `/ProcessID` (case insensitive), use the text after the colon.
3. Otherwise, use the command line text itself as the GUID string.
4. Pass the selected string to `IIDFromString`.
5. If GUID parsing succeeds, call `CoInitializeEx`.
6. Call `CoRegisterSurrogateEx(&processGuid, 0)`.

So the two useful command line shapes are:

- `dllhost.exe {GUID}`
- `dllhost.exe /ProcessID:{GUID}` (case insensitive `ProcessID`)

Here is a snippet from IDA pseudocode (beautified for readability) showing the initial parsing loop looking for the `:`, and `/ProcessID`:

```
currentChar = commandLineBuffer[0];
for ( optionEnd = commandLineBuffer; ; ++optionEnd )
{
  if ( !currentChar )
    goto useWholeCommandLine;

  guidTextAfterColon = optionEnd + 1;
  if ( currentChar == ':' )
    break;

  currentChar = *guidTextAfterColon;
}

*optionEnd = 0;
guidTextSource = (char *)(optionEnd + 1);

if ( !*guidTextAfterColon || (unsigned int)_o__wcsicmp(commandLineBuffer, L"/ProcessID") )
useWholeCommandLine:
  guidTextSource = (char *)commandLineBuffer;
```

The GUID is then copied into a buffer and passed to `IIDFromString`.

```
if ( IIDFromString(guidTextBuffer, &processGuid) >= 0 )
{
  ...
}
```

If that succeeds, `dllhost.exe` initializes COM and registers the process as a surrogate, and then waits :)

```
if ( CoInitializeEx(nullptr, 0) >= 0 )
{
  CoRegisterSurrogateEx(&processGuid, 0);
  CoUninitialize();
  CurrentProcess = GetCurrentProcess();
  TerminateProcess(CurrentProcess, 0);
}
```

As we can see, `dllhost.exe` is not doing much on its own. It just registers itself as a COM surrogate with the parsed GUID, and then waits for COM to do the real work of activating classes in it.

> This btw explains why it cannot be used as a direct LOLBin, since it only does the registration. So its execution is an indicator of COM surrogate activity, but it's not the one initiating that activity.

## Special GUID Policy Branch [\#](https://research.nasbench.dev/research/windows-processes/dllhost\#special-guid-policy-branch)

There is one GUID-specific policy branch before the call to `CoRegisterSurrogateEx`.

If the `COMSysAppRedirectionTrustPolicy` feature is enabled and the parsed GUID matches:

```
02d4b3f1-fd88-11d1-960d-00805fc79235
```

then `dllhost.exe` checks whether the token is elevated. If it is elevated, it applies a process mitigation policy before continuing into COM surrogate registration.

```
if ( (unsigned __int8)wil::details::FeatureImpl<__WilFeatureTraits_Feature_COMSysAppRedirectionTrustPolicy>::__private_IsEnabled(...)
  && *(_QWORD *)&processGuid.Data1 == 0x11D1FD8802D4B3F1LL
  && *(_QWORD *)processGuid.Data4 == 0x3592C75F80000D96LL )
{
  TokenInformation = 0;
  returnLength = 4;
  if ( !GetTokenInformation((HANDLE)0xFFFFFFFFFFFFFFFCLL, TokenElevation, &TokenInformation, 4u, &returnLength) )
    return wil::details::in1diag3::Win32_Return_GetLastError(...);

  if ( TokenInformation )
  {
    mitigationPolicyEnabled = 1;
    if ( !(unsigned int)SetProcessMitigationPolicy(16, &mitigationPolicyEnabled, 4) )
      return wil::details::in1diag3::Win32_Return_GetLastError(...);
  }
}
```

## Appendix: Registry Surrogate Configuration And `-Embedding` [\#](https://research.nasbench.dev/research/windows-processes/dllhost\#appendix-registry-surrogate-configuration-and--embedding)

In order to know when `dllhost.exe` will be chosen as the COM surrogate, we investigate the following registry keys:

```
HKCR\AppID\{AppID}\DllSurrogate
HKLM\SOFTWARE\Classes\AppID\{AppID}\DllSurrogate
```

Some important notes about these keys:

| AppID `DllSurrogate` value | COM behavior |
| --- | --- |
| Missing | No surrogate is selected from this value. |
| Empty string | Use the default system surrogate: `DllHost.exe /Processid:{AppID}`. |
| Non-empty string | Use that custom surrogate executable. COM builds `<surrogate path> {CLSID} -Embedding`. |

That means the GUID passed to default `dllhost.exe` is the AppID:

```
DllHost.exe /Processid:{AppID}
```

For a custom surrogate, its whatever executable + the CLSID of the class being activated + `-Embedding`:

```
<custom surrogate path> {CLSID} -Embedding
```

> I encourage you to check out, `CComProcessInfo::FinalConstruct` and `CComClassInfo::InitializeSurrogateInfo` in `combase.dll`, to see the `DllSurrogate` classification and command consturction

Here is an example of what we just talked about. The following registry configuration sets up a custom surrogate for the AppID `{1D278EEF-5C38-4F2A-8C7D-D5C13B662567}`.

```
HKCR\CLSID\{E041C90B-68BA-42C9-991E-477B73A75C90}
  AppID = {1D278EEF-5C38-4F2A-8C7D-D5C13B662567}

HKLM\SOFTWARE\Classes\AppID\{1D278EEF-5C38-4F2A-8C7D-D5C13B662567}
  DllSurrogate = \\?\C:\Windows\System32\SecurityHealth\10.0.29554.1001-0\SecurityHealthHost.exe
```

The running process shows the custom surrogate shape:

```
\\?\C:\Windows\System32\SecurityHealth\10.0.29554.1001-0\SecurityHealthHost.exe {E041C90B-68BA-42C9-991E-477B73A75C90} -Embedding
```

Related Articles

## Other threads in the archive worth reading next.

[Process Anatomy\\
**Windows Process Internals - Fondue.EXE** \\
An in-depth look at Fondue.EXE, CLI options, the "rude app" checks, the handoff to APPWIZ.CPL and a bit of DLL side-loading.](https://research.nasbench.dev/research/windows-processes/fondue) [Process Anatomy\\
**Windows Process Internals - Fsutil.EXE** \\
An in-depth look at the Fsutil.EXE utility, its functionality, and an exploration of its internal workings.](https://research.nasbench.dev/research/windows-processes/fsutil) [Process Anatomy\\
**Windows Process Internals - At.EXE** \\
An in-depth look at the At.EXE utility, its functionality, and an exploration of its internal workings.](https://research.nasbench.dev/research/windows-processes/at)