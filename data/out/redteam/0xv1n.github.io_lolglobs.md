# https://0xv1n.github.io/LOLGlobs/

\*?

# LOLGlobs

Process execution through wildcard pattern evasion

4 platforms·11 categories

`/`

`@linux``@macos``@powershell``@windows-cmd` — filter by platform·`/discovery``/download``/execution` — filter by category·`T1059` — search by MITRE ID

AllLinuxmacOSWindows CMDPowerShell

All CategoriesDiscoveryDownloadExecutionUploadPersistenceLateral MovementExfiltrationCredential AccessEncode/DecodeCompileReconnaissance

66 entries

| Command | Description | Platform | Wildcards | Category | MITRE |
| --- | --- | --- | --- | --- | --- |
| [Add-Type](https://0xv1n.github.io/LOLGlobs/globs/powershell/add-type/) | Compile and load C# or other .NET language code at runtime. Enables direct Wi... | PowerShell | \*?\[c-e\] | execution | [T1059.001](https://attack.mitre.org/techniques/T1059/001/) |
| [Copy-Item](https://0xv1n.github.io/LOLGlobs/globs/powershell/copy-item/) | Copy files and directories. Used for staging payloads, copying sensitive data... | PowerShell | \*?\[n-p\]-match | exfiltration | [T1048](https://attack.mitre.org/techniques/T1048/) |
| [Get-Content](https://0xv1n.github.io/LOLGlobs/globs/powershell/get-content/) | Read file contents. Equivalent to cat on Linux. Used to read sensitive files,... | PowerShell | \*?\[d-f\] | discovery | [T1005](https://attack.mitre.org/techniques/T1005/) |
| [Import-Module](https://0xv1n.github.io/LOLGlobs/globs/powershell/import-module/) | Load PowerShell modules from disk, UNC paths, or the module store. Used to lo... | PowerShell | \*?\[l-n\] | execution | [T1059.001](https://attack.mitre.org/techniques/T1059/001/) |
| [Invoke-Command](https://0xv1n.github.io/LOLGlobs/globs/powershell/invoke-command/) | Run commands on local or remote computers. Enables lateral movement via Power... | PowerShell | \*\[d-f\]? | lateral-movement | [T1021.006](https://attack.mitre.org/techniques/T1021/006/) |
| [Invoke-Expression](https://0xv1n.github.io/LOLGlobs/globs/powershell/invoke-expression/) | Execute arbitrary strings as PowerShell commands. The most direct code execut... | PowerShell | \*?\[d-f\]-match | execution | [T1059.001](https://attack.mitre.org/techniques/T1059/001/) |
| [Invoke-RestMethod](https://0xv1n.github.io/LOLGlobs/globs/powershell/invoke-restmethod/) | Send HTTP/HTTPS requests and receive structured responses. Used for C2 commun... | PowerShell | \*\[d-f\]?-match | download | [T1105](https://attack.mitre.org/techniques/T1105/) |
| [Invoke-WebRequest](https://0xv1n.github.io/LOLGlobs/globs/powershell/invoke-webrequest/) | Download files or interact with web services. PowerShell's built-in HTTP clie... | PowerShell | \*?\[d-f\]-match | download | [T1105](https://attack.mitre.org/techniques/T1105/) |
| [New-Object](https://0xv1n.github.io/LOLGlobs/globs/powershell/new-object/) | Creates .NET or COM objects. Used to instantiate WebClient for downloads, cre... | PowerShell | \*?\[d-f\]-clike | download | [T1105](https://attack.mitre.org/techniques/T1105/) |
| [Out-File](https://0xv1n.github.io/LOLGlobs/globs/powershell/out-file/) | Send pipeline output to a file. Alternative to Set-Content with pipeline supp... | PowerShell | \*?\[t-v\] | execution | [T1059.001](https://attack.mitre.org/techniques/T1059/001/) |
| [Remove-Item](https://0xv1n.github.io/LOLGlobs/globs/powershell/remove-item/) | Delete files, directories, registry keys, or other PowerShell provider items.... | PowerShell | \*?\[d-f\]-match | execution | [T1070.004](https://attack.mitre.org/techniques/T1070/004/) |
| [Set-Content](https://0xv1n.github.io/LOLGlobs/globs/powershell/set-content/) | Write content to a file. Used to drop payloads, modify system files, or write... | PowerShell | \*?\[d-f\] | execution | [T1059.001](https://attack.mitre.org/techniques/T1059/001/) |
| [Start-Process](https://0xv1n.github.io/LOLGlobs/globs/powershell/start-process/) | Start one or more processes. Can launch executables with specific arguments, ... | PowerShell | \*?\[s-u\]-match | execution | [T1059.001](https://attack.mitre.org/techniques/T1059/001/) |
| [Test-Connection](https://0xv1n.github.io/LOLGlobs/globs/powershell/test-connection/) | Send ICMP echo requests (ping). Used for host discovery and network reconnais... | PowerShell | \*?\[d-f\] | reconnaissance | [T1018](https://attack.mitre.org/techniques/T1018/) |
| [awk](https://0xv1n.github.io/LOLGlobs/globs/linux/awk/) | Text processing utility. Can be used to extract credential data, process file... | Linux | ?\*\[\] | execution | [T1059](https://attack.mitre.org/techniques/T1059/) |
| [base64](https://0xv1n.github.io/LOLGlobs/globs/linux/base64/) | Encode or decode base64 data. Widely used to obfuscate payloads, bypass conte... | Linux | \*?\[\] | encode-decode | [T1140](https://attack.mitre.org/techniques/T1140/) |
| [bash](https://0xv1n.github.io/LOLGlobs/globs/linux/bash/) | GNU Bourne Again Shell. Executing bash with -i or -c allows spawning interact... | Linux | ?\*\[\]{}+() | execution | [T1059.004](https://attack.mitre.org/techniques/T1059/004/) |
| [bitsadmin](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/bitsadmin/) | Background Intelligent Transfer Service admin tool. Can download or upload fi... | Windows CMD | \*? | download | [T1197](https://attack.mitre.org/techniques/T1197/) |
| [cat](https://0xv1n.github.io/LOLGlobs/globs/linux/cat/) | Concatenate and display file contents. Used for reading sensitive files like ... | Linux | ?\*\[\] | discovery | [T1083](https://attack.mitre.org/techniques/T1083/) |
| [certutil](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/certutil/) | Certificate management utility. Widely abused for base64 encoding/decoding an... | Windows CMD | \*? | download | [T1105](https://attack.mitre.org/techniques/T1105/) |
| [chmod](https://0xv1n.github.io/LOLGlobs/globs/linux/chmod/) | Change file permissions. Used post-exploitation to make dropped payloads exec... | Linux | ?\*\[\] | execution | [T1222.002](https://attack.mitre.org/techniques/T1222/002/) |
| [chown](https://0xv1n.github.io/LOLGlobs/globs/linux/chown/) | Change file owner and group. Used to reassign ownership of files, directories... | Linux | ?\*\[\] | persistence | [T1222.002](https://attack.mitre.org/techniques/T1222/002/) |
| [cmd](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/cmd/) | Windows Command Processor. Spawning cmd.exe is a common technique for executi... | Windows CMD | ?\* | execution | [T1059.003](https://attack.mitre.org/techniques/T1059/003/) |
| [cscript](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/cscript/) | Windows Script Host console runner for JScript and VBScript. Executes script ... | Windows CMD | ?\* | execution | [T1059.005](https://attack.mitre.org/techniques/T1059/005/) |
| [curl](https://0xv1n.github.io/LOLGlobs/globs/linux/curl/) | Transfer data to or from a server. Commonly used for downloading payloads, ex... | Linux | ?\*\[\]{} | download | [T1105](https://attack.mitre.org/techniques/T1105/) |
| [curl](https://0xv1n.github.io/LOLGlobs/globs/macos/curl/) | Transfer data from servers. macOS ships with curl by default. Used for C2, pa... | macOS | ?\*\[\] | download | [T1105](https://attack.mitre.org/techniques/T1105/) |
| [dd](https://0xv1n.github.io/LOLGlobs/globs/linux/dd/) | Convert and copy files or block devices. Used for disk imaging, raw data exfi... | Linux | ? | exfiltration | [T1005](https://attack.mitre.org/techniques/T1005/) |
| [esentutl](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/esentutl/) | Extensible Storage Engine utility. Can copy locked or in-use files (e.g., NTD... | Windows CMD | \*? | download | [T1105](https://attack.mitre.org/techniques/T1105/) |
| [expand](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/expand/) | Expands compressed CAB archive files. Can extract payloads from CAB container... | Windows CMD | ?\* | execution | [T1140](https://attack.mitre.org/techniques/T1140/) |
| [extrac32](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/extrac32/) | CAB extraction utility bundled with Internet Explorer. Less monitored than ex... | Windows CMD | \*? | execution | [T1218](https://attack.mitre.org/techniques/T1218/) |
| [find](https://0xv1n.github.io/LOLGlobs/globs/linux/find/) | Search for files in directory hierarchy. Pivotal for discovery — finding SUID... | Linux | ?\*\[\] | discovery | [T1083](https://attack.mitre.org/techniques/T1083/) |
| [finger](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/finger/) | Legacy user info protocol client. Can retrieve arbitrary text from an attacke... | Windows CMD | \*? | download | [T1105](https://attack.mitre.org/techniques/T1105/) |
| [forfiles](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/forfiles/) | Execute a command for each file matching a wildcard mask. The /m flag accepts... | Windows CMD | \*? | execution | [T1059.003](https://attack.mitre.org/techniques/T1059/003/) |
| [gdb](https://0xv1n.github.io/LOLGlobs/globs/linux/gdb/) | GNU debugger. Can execute arbitrary shell commands via the 'shell' command, c... | Linux | ?\[\] | execution | [T1059](https://attack.mitre.org/techniques/T1059/) |
| [id](https://0xv1n.github.io/LOLGlobs/globs/linux/id/) | Print user and group information. Confirms current user UID, GID, and group m... | Linux | \[\]?\* | discovery | [T1033](https://attack.mitre.org/techniques/T1033/) |
| [mshta](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/mshta/) | Microsoft HTML Application host. Executes HTA files or inline VBScript/JScrip... | Windows CMD | \*? | execution | [T1218.005](https://attack.mitre.org/techniques/T1218/005/) |
| [nc](https://0xv1n.github.io/LOLGlobs/globs/linux/nc/) | Netcat — the TCP/IP Swiss army knife. Used for port scanning, reverse shells,... | Linux | ?\[\]\* | execution | [T1059.004](https://attack.mitre.org/techniques/T1059/004/) |
| [nmap](https://0xv1n.github.io/LOLGlobs/globs/linux/nmap/) | Network mapper and port scanner. Used for network reconnaissance, host discov... | Linux | ?\*\[\] | reconnaissance | [T1046](https://attack.mitre.org/techniques/T1046/) |
| [node](https://0xv1n.github.io/LOLGlobs/globs/linux/node/) | Node.js JavaScript runtime. Can execute arbitrary JavaScript, spawn reverse s... | Linux | ?\*\[\] | execution | [T1059](https://attack.mitre.org/techniques/T1059/) |
| [open](https://0xv1n.github.io/LOLGlobs/globs/macos/open/) | Open files, URLs, or applications. Can launch applications, execute scripts v... | macOS | ?\*\[\] | execution | [T1218](https://attack.mitre.org/techniques/T1218/) |
| [openssl](https://0xv1n.github.io/LOLGlobs/globs/linux/openssl/) | Cryptography toolkit and TLS client. Can encrypt/decrypt data, create reverse... | Linux | \*? | encode-decode | [T1573](https://attack.mitre.org/techniques/T1573/) |
| [osascript](https://0xv1n.github.io/LOLGlobs/globs/macos/osascript/) | Execute AppleScript or JavaScript for Automation (JXA). Can control applicati... | macOS | \*?\[\] | execution | [T1059.002](https://attack.mitre.org/techniques/T1059/002/) |
| [perl](https://0xv1n.github.io/LOLGlobs/globs/linux/perl/) | Perl interpreter. Supports arbitrary code execution, file I/O, network operat... | Linux | ?\*\[\] | execution | [T1059](https://attack.mitre.org/techniques/T1059/) |
| [php](https://0xv1n.github.io/LOLGlobs/globs/linux/php/) | PHP CLI interpreter. Can execute arbitrary PHP code, spawn reverse shells, re... | Linux | ?\[\] | execution | [T1059](https://attack.mitre.org/techniques/T1059/) |
| [pip](https://0xv1n.github.io/LOLGlobs/globs/linux/pip/) | Python package installer. Installing packages with malicious setup.py execute... | Linux | ?\[\] | execution | [T1059.006](https://attack.mitre.org/techniques/T1059/006/) |
| [powershell.exe](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/powershell-exe/) | PowerShell executable launched from CMD. Bypasses CMD-level restrictions by d... | Windows CMD | \*? | execution | [T1059.001](https://attack.mitre.org/techniques/T1059/001/) |
| [python3](https://0xv1n.github.io/LOLGlobs/globs/linux/python3/) | Python 3 interpreter. Enables arbitrary code execution, file operations, netw... | Linux | ?\*\[\] | execution | [T1059.006](https://attack.mitre.org/techniques/T1059/006/) |
| [python3](https://0xv1n.github.io/LOLGlobs/globs/macos/python3/) | Python 3 interpreter on macOS. Available via Xcode CLI tools or Homebrew. Ena... | macOS | ?\*\[\] | execution | [T1059.006](https://attack.mitre.org/techniques/T1059/006/) |
| [regsvr32](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/regsvr32/) | Registers and unregisters OLE controls. Can execute remote scriptlets (scrobj... | Windows CMD | ?\* | execution | [T1218.010](https://attack.mitre.org/techniques/T1218/010/) |
| [replace](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/replace/) | Replaces (copies) files from a source to a destination directory. Can be used... | Windows CMD | \*? | execution | [T1105](https://attack.mitre.org/techniques/T1105/) |
| [rsync](https://0xv1n.github.io/LOLGlobs/globs/linux/rsync/) | Fast, versatile file copying tool. Supports remote file sync over SSH — usefu... | Linux | ?\*\[\] | exfiltration | [T1048](https://attack.mitre.org/techniques/T1048/) |
| [ruby](https://0xv1n.github.io/LOLGlobs/globs/linux/ruby/) | Ruby interpreter. Can be used for arbitrary code execution, reverse shells, a... | Linux | ?\*\[\] | execution | [T1059](https://attack.mitre.org/techniques/T1059/) |
| [rundll32](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/rundll32/) | Loads and runs DLLs. Used to execute malicious DLL exports directly, bypassin... | Windows CMD | ?\* | execution | [T1218.011](https://attack.mitre.org/techniques/T1218/011/) |
| [scp](https://0xv1n.github.io/LOLGlobs/globs/linux/scp/) | Secure Copy Protocol. Used for file transfer between hosts over SSH — exfiltr... | Linux | ?\*\[\] | exfiltration | [T1048.002](https://attack.mitre.org/techniques/T1048/002/) |
| [screen](https://0xv1n.github.io/LOLGlobs/globs/linux/screen/) | Terminal multiplexer. Can create persistent sessions that survive logout, run... | Linux | ?\*\[\] | execution | [T1059.004](https://attack.mitre.org/techniques/T1059/004/) |
| [sed](https://0xv1n.github.io/LOLGlobs/globs/linux/sed/) | Stream editor for filtering and transforming text. Can read arbitrary files, ... | Linux | ?\*\[\] | execution | [T1059](https://attack.mitre.org/techniques/T1059/) |
| [socat](https://0xv1n.github.io/LOLGlobs/globs/linux/socat/) | Multipurpose relay tool. More powerful than netcat — supports SSL, UDP, and c... | Linux | ?\*\[\] | execution | [T1059](https://attack.mitre.org/techniques/T1059/) |
| [ssh](https://0xv1n.github.io/LOLGlobs/globs/linux/ssh/) | Secure Shell client. Used for lateral movement, remote command execution, tun... | Linux | ?\*\[\] | lateral-movement | [T1021.004](https://attack.mitre.org/techniques/T1021/004/) |
| [strace](https://0xv1n.github.io/LOLGlobs/globs/linux/strace/) | System call tracer. Can monitor running processes, extract secrets from memor... | Linux | \*?\[\] | discovery | [T1057](https://attack.mitre.org/techniques/T1057/) |
| [tar](https://0xv1n.github.io/LOLGlobs/globs/linux/tar/) | Archive utility. Used to compress and exfiltrate data, or extract attacker-co... | Linux | ?\*\[\] | exfiltration | [T1560.001](https://attack.mitre.org/techniques/T1560/001/) |
| [vim](https://0xv1n.github.io/LOLGlobs/globs/linux/vim/) | Vi Improved text editor. Can execute shell commands via :!cmd, spawn interact... | Linux | ?\[\] | execution | [T1059](https://attack.mitre.org/techniques/T1059/) |
| [wget](https://0xv1n.github.io/LOLGlobs/globs/linux/wget/) | Non-interactive network downloader. Used to fetch files from HTTP/FTP servers... | Linux | ?\*\[\]{} | download | [T1105](https://attack.mitre.org/techniques/T1105/) |
| [whoami](https://0xv1n.github.io/LOLGlobs/globs/linux/whoami/) | Prints the current user's username. Useful for confirming privilege level aft... | Linux | ?\*\[\]{}@() | discovery | [T1033](https://attack.mitre.org/techniques/T1033/) |
| [wmic](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/wmic/) | WMI command-line interface. Used for system information gathering, remote exe... | Windows CMD | ?\* | execution | [T1047](https://attack.mitre.org/techniques/T1047/) |
| [wscript](https://0xv1n.github.io/LOLGlobs/globs/windows-cmd/wscript/) | Windows Script Host GUI runner for JScript and VBScript. Executes scripts wit... | Windows CMD | ?\* | execution | [T1059.005](https://attack.mitre.org/techniques/T1059/005/) |
| [xxd](https://0xv1n.github.io/LOLGlobs/globs/linux/xxd/) | Hex dump and reverse hex dump utility. Can convert binaries to hex and recons... | Linux | ?\[\]\* | encode-decode | [T1140](https://attack.mitre.org/techniques/T1140/) |

No entries match your search. [Clear filters](https://0xv1n.github.io/LOLGlobs/#)

`ESC`

`↑↓` navigate`↵` open`esc` close