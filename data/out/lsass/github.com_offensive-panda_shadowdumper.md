# https://github.com/Offensive-Panda/ShadowDumper

[Skip to content](https://github.com/Offensive-Panda/ShadowDumper#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/Offensive-Panda/ShadowDumper) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/Offensive-Panda/ShadowDumper) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/Offensive-Panda/ShadowDumper) to refresh your session.Dismiss alert

{{ message }}

[Offensive-Panda](https://github.com/Offensive-Panda)/ **[ShadowDumper](https://github.com/Offensive-Panda/ShadowDumper)** Public

- [Notifications](https://github.com/login?return_to=%2FOffensive-Panda%2FShadowDumper) You must be signed in to change notification settings
- [Fork\\
91](https://github.com/login?return_to=%2FOffensive-Panda%2FShadowDumper)
- [Star\\
572](https://github.com/login?return_to=%2FOffensive-Panda%2FShadowDumper)


Shadow Dumper is a powerful tool used to dump LSASS memory, often needed in penetration testing and red teaming. It uses multiple advanced techniques to dump memory, allowing to access sensitive data in LSASS memory.


### License

[MIT license](https://github.com/Offensive-Panda/ShadowDumper/blob/main/LICENSE)

[572\\
stars](https://github.com/Offensive-Panda/ShadowDumper/stargazers) [91\\
forks](https://github.com/Offensive-Panda/ShadowDumper/forks) [Branches](https://github.com/Offensive-Panda/ShadowDumper/branches) [Tags](https://github.com/Offensive-Panda/ShadowDumper/tags) [Activity](https://github.com/Offensive-Panda/ShadowDumper/activity)

[Star](https://github.com/login?return_to=%2FOffensive-Panda%2FShadowDumper)

[Notifications](https://github.com/login?return_to=%2FOffensive-Panda%2FShadowDumper) You must be signed in to change notification settings

# Offensive-Panda/ShadowDumper

main

[**1** Branch](https://github.com/Offensive-Panda/ShadowDumper/branches) [**2** Tags](https://github.com/Offensive-Panda/ShadowDumper/tags)

[Go to Branches page](https://github.com/Offensive-Panda/ShadowDumper/branches)[Go to Tags page](https://github.com/Offensive-Panda/ShadowDumper/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![Offensive-Panda](https://avatars.githubusercontent.com/u/76246439?v=4&size=40)](https://github.com/Offensive-Panda)[Offensive-Panda](https://github.com/Offensive-Panda/ShadowDumper/commits?author=Offensive-Panda)<br>[Update README.md](https://github.com/Offensive-Panda/ShadowDumper/commit/a2c1d97469a7a6837630168c8c0768dc23a6e2c1)<br>9 months agoMay 22, 2025<br>[a2c1d97](https://github.com/Offensive-Panda/ShadowDumper/commit/a2c1d97469a7a6837630168c8c0768dc23a6e2c1) · 9 months agoMay 22, 2025<br>## History<br>[34 Commits](https://github.com/Offensive-Panda/ShadowDumper/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/Offensive-Panda/ShadowDumper/commits/main/) 34 Commits |
| [ShadowDumper](https://github.com/Offensive-Panda/ShadowDumper/tree/main/ShadowDumper "ShadowDumper") | [ShadowDumper](https://github.com/Offensive-Panda/ShadowDumper/tree/main/ShadowDumper "ShadowDumper") | [V2.0 Launch](https://github.com/Offensive-Panda/ShadowDumper/commit/0862e31ecc6dc7066c7a00873289451ba7b420d9 "V2.0 Launch") | last yearMar 2, 2025 |
| [LICENSE](https://github.com/Offensive-Panda/ShadowDumper/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/Offensive-Panda/ShadowDumper/blob/main/LICENSE "LICENSE") | [Initial commit](https://github.com/Offensive-Panda/ShadowDumper/commit/008a825a61ae3b9f8c67564d5f74871ef18d5415 "Initial commit") | 2 years agoNov 10, 2024 |
| [README.md](https://github.com/Offensive-Panda/ShadowDumper/blob/main/README.md "README.md") | [README.md](https://github.com/Offensive-Panda/ShadowDumper/blob/main/README.md "README.md") | [Update README.md](https://github.com/Offensive-Panda/ShadowDumper/commit/a2c1d97469a7a6837630168c8c0768dc23a6e2c1 "Update README.md") | 9 months agoMay 22, 2025 |
| View all files |

## Repository files navigation

# ShadowDumper

[Permalink: ShadowDumper](https://github.com/Offensive-Panda/ShadowDumper#shadowdumper)

[![Buy Me A Coffee](https://camo.githubusercontent.com/0cf29a542375e1a46e84d8bf5805a4e5c0a6ee98b6547ccdc0c55eed49d99c69/68747470733a2f2f63646e2e6275796d6561636f666665652e636f6d2f627574746f6e732f76322f64656661756c742d79656c6c6f772e706e67)](https://www.paypal.me/OFFPAN)[![Donate with PayPal](https://camo.githubusercontent.com/59377b5c0870cdb89982c7acc993a2468389ccb9fea5889c37eabab4823d556c/68747470733a2f2f7777772e70617970616c6f626a656374732e636f6d2f7765627374617469632f6d6b74672f6c6f676f2f70705f63635f6d61726b5f3131317836392e6a7067)](https://www.paypal.me/OFFPAN)

[![Help](https://github.com/Offensive-Panda/ShadowDumper/raw/main/ShadowDumper/Assets/main.jpg)](https://github.com/Offensive-Panda/ShadowDumper/blob/main/ShadowDumper/Assets/main.jpg)

Shadow Dumper is a powerful tool used to dump LSASS (Local Security Authority Subsystem Service) memory, often needed in penetration testing and red teaming activities. It offers flexible options to users and uses multiple advanced techniques to dump memory, allowing to access sensitive data in LSASS memory.

Caution

It's important to note that this project is only for educational and research purposes, and any unauthorized use of it could lead to legal consequences.

## 🚀 Capabilities

[Permalink: 🚀 Capabilities](https://github.com/Offensive-Panda/ShadowDumper#-capabilities)

- **Unhooked Injection (Modified Mimikatz Binary)** – Utilizes unhooking to inject a modified Mimikatz binary, bypassing EDR hooks and evading detection.
- **Unhooked Injection (Direct Syscalls with MDWD)** – Implements direct syscalls for stealthy injection using MDWD, reducing the footprint left behind.
- **Simple MiniDumpWriteDump API** – Executes the straightforward MiniDumpWriteDump API method for standard LSASS memory extraction.
- **MINIDUMP\_CALLBACK\_INFORMATION Callbacks** – Uses callback functions for custom handling, offering greater control over the dumping process.
- **Process Forking Technique** – Forks the LSASS process, creating a memory clone and avoiding direct access to the target process.
- **Direct Syscalls with MiniDumpWriteDump** – Combines direct syscalls with MiniDumpWriteDump, enhancing stealth by avoiding typical API hooks.
- **Native Dump with Direct Syscalls (Offline Parsing)** – Leverages direct syscalls to create a native dump with essential streams for offline parsing, perfect for low-noise operations.

## 🛠️ Build

[Permalink: 🛠️ Build](https://github.com/Offensive-Panda/ShadowDumper#%EF%B8%8F-build)

- Clone ShadowDumper repository
- Open in Visual Studio 2019 (v142)
- C++ Language Standard ISO C++14 Standard or Higher
- Download the shellcodes **pan.bin and off.bin** from \[Resource Shellcodes\] folder, place them somewhere in your computer and change the path in ShadowDumper.rc file before compiling.
- Make sure MASM should be selected. \[Right-click on your project in solution explorer, click build dependencies, click build customization and select .masm\]
- Right click on ASM files and go to properties and make sure item type should be Microsoft Macro Assembler
- Compile project

Note

V1.0 Compatibility: Windows (x64) \[Tested with x64 build\] on Windows 10 Version 22H2 (OS build 19045.5487) with major 10.0
\[You may face issues on latest releases in some methods, this can be due to version of mimikatz\]

## ⛑️ Usage

[Permalink: ⛑️ Usage](https://github.com/Offensive-Panda/ShadowDumper#%EF%B8%8F-usage)

To run ShadowDumper, execute the compiled binary from the powershell.

**Default Mode (V1.0)**

- No Parameter Provided: Show the user friendly console with multiple options to execute

[![Help](https://github.com/Offensive-Panda/ShadowDumper/raw/main/ShadowDumper/Assets/display.png)](https://github.com/Offensive-Panda/ShadowDumper/blob/main/ShadowDumper/Assets/display.png)

**Default Mode (V2.0)**

- No Parameter Provided: Show the user friendly console with multiple options to execute

[![Help](https://github.com/Offensive-Panda/ShadowDumper/raw/main/ShadowDumper/Assets/displayv2.png)](https://github.com/Offensive-Panda/ShadowDumper/blob/main/ShadowDumper/Assets/displayv2.png)

**CommandLine Mode (V1.0)**

- Parameter: -h: Displays a help menu with all available options.

[![Help](https://github.com/Offensive-Panda/ShadowDumper/raw/main/ShadowDumper/Assets/help.png)](https://github.com/Offensive-Panda/ShadowDumper/blob/main/ShadowDumper/Assets/help.png)

**CommandLine Mode (V2.0)**

- Parameter: -h: Displays a help menu with all available options.

[![Help](https://github.com/Offensive-Panda/ShadowDumper/raw/main/ShadowDumper/Assets/helpv2.png)](https://github.com/Offensive-Panda/ShadowDumper/blob/main/ShadowDumper/Assets/helpv2.png)

```
  ShadowDumper.exe
    - Parameter: 1: To dump lsass memory using unhooking technique to inject modified mimikatz binary [Token Elevation, SAM Dumping, Vault Credentials, Lsass Hashes Dumping].

  ShadowDumper.exe
    - Parameter: 2:  To dump lsass memory using unhooking technique to inject binary using direct syscalls with MDWD.

  ShadowDumper.exe
    - Parameter: 3: To dump lsass memory using simple MiniDumpWriteDump API.

  ShadowDumper.exe
    - Parameter: 4: To dump lsass memory using MINIDUMP_CALLBACK_INFORMATION callbacks and encrypt the dumps before writing on disk as per your choice.

  ShadowDumper.exe
    - Parameter: 5: To dump lsass memory using process forking technique and encrypt the dumps before writing on disk as per your choice.

  ShadowDumper.exe
    - Parameter: 6:  To dump lsass memory using direct syscalls with MiniDumpWriteDump.

  ShadowDumper.exe
    - Parameter: 7:   To dump lsass memory using direct syscalls (native dump with needed streams for parsing offline).

   ShadowDumper.exe
    - Parameter: 8:   To decrypt the dump file before offline parsing with tools like (mimikatz or pypykatz).
```

## 💫 Demonstration

[Permalink: 💫 Demonstration](https://github.com/Offensive-Panda/ShadowDumper#-demonstration)

Demonstrates the working of ShadowDumper (V1.0).

[![Demo](https://github.com/Offensive-Panda/ShadowDumper/raw/main/ShadowDumper/Assets/D.gif)](https://github.com/Offensive-Panda/ShadowDumper/blob/main/ShadowDumper/Assets/D.gif)[![Demo](https://github.com/Offensive-Panda/ShadowDumper/raw/main/ShadowDumper/Assets/D.gif)](https://github.com/Offensive-Panda/ShadowDumper/blob/main/ShadowDumper/Assets/D.gif)[Open Demo in new window](https://github.com/Offensive-Panda/ShadowDumper/blob/main/ShadowDumper/Assets/D.gif)

Demonstrates the working of ShadowDumper (V2.0).

[![Demo](https://github.com/Offensive-Panda/ShadowDumper/raw/main/ShadowDumper/Assets/D2.gif)](https://github.com/Offensive-Panda/ShadowDumper/blob/main/ShadowDumper/Assets/D2.gif)[![Demo](https://github.com/Offensive-Panda/ShadowDumper/raw/main/ShadowDumper/Assets/D2.gif)](https://github.com/Offensive-Panda/ShadowDumper/blob/main/ShadowDumper/Assets/D2.gif)[Open Demo in new window](https://github.com/Offensive-Panda/ShadowDumper/blob/main/ShadowDumper/Assets/D2.gif)

## 🔄 Upcoming

[Permalink: 🔄 Upcoming](https://github.com/Offensive-Panda/ShadowDumper#-upcoming)

```
- Exfiltrate: Exfiltrate dump file over C2 server.

- Enhancement: Add more techniques to dump lsass memory.

Stay tuned for future releases!
```

## 🤳 Contact

[Permalink: 🤳 Contact](https://github.com/Offensive-Panda/ShadowDumper#-contact)

Have questions, ideas, or want to collaborate? Reach out to the [author](https://offensive-panda.github.io/) for a conversation, or jump right in and contribute via GitHub Issues. Let's make something great together!

## 🙏 Acknowledgment

[Permalink: 🙏 Acknowledgment](https://github.com/Offensive-Panda/ShadowDumper#-acknowledgment)

- Took help in nativedump streams from the Project by **Florinel Olteanu** called [**NtDump**](https://github.com/florylsk/NtDump).
- Injected modified mimikatz by **Benjamin DELPY** called [**Mimikatz**](https://github.com/gentilkiwi/mimikatz).

## About

Shadow Dumper is a powerful tool used to dump LSASS memory, often needed in penetration testing and red teaming. It uses multiple advanced techniques to dump memory, allowing to access sensitive data in LSASS memory.


### Resources

[Readme](https://github.com/Offensive-Panda/ShadowDumper#readme-ov-file)

### License

[MIT license](https://github.com/Offensive-Panda/ShadowDumper#MIT-1-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/Offensive-Panda/ShadowDumper).

[Activity](https://github.com/Offensive-Panda/ShadowDumper/activity)

### Stars

[**572**\\
stars](https://github.com/Offensive-Panda/ShadowDumper/stargazers)

### Watchers

[**8**\\
watching](https://github.com/Offensive-Panda/ShadowDumper/watchers)

### Forks

[**91**\\
forks](https://github.com/Offensive-Panda/ShadowDumper/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2FOffensive-Panda%2FShadowDumper&report=Offensive-Panda+%28user%29)

## [Releases\  2](https://github.com/Offensive-Panda/ShadowDumper/releases)

[LsassDumpingV2.0\\
Latest\\
\\
on Mar 2, 2025Mar 2, 2025](https://github.com/Offensive-Panda/ShadowDumper/releases/tag/LsassDumpingV2.0)

[\+ 1 release](https://github.com/Offensive-Panda/ShadowDumper/releases)

## [Packages\  0](https://github.com/users/Offensive-Panda/packages?repo_name=ShadowDumper)

No packages published

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/Offensive-Panda/ShadowDumper).

## Languages

- [C++71.6%](https://github.com/Offensive-Panda/ShadowDumper/search?l=c%2B%2B)
- [C24.0%](https://github.com/Offensive-Panda/ShadowDumper/search?l=c)
- [Assembly4.4%](https://github.com/Offensive-Panda/ShadowDumper/search?l=assembly)

You can’t perform that action at this time.