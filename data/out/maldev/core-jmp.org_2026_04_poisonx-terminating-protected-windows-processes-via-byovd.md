# https://core-jmp.org/2026/04/poisonx-terminating-protected-windows-processes-via-byovd/

[![PoisonX: Terminating Protected Windows Processes via BYOVD](https://core-jmp.org/wp-content/uploads/2026/04/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0-2026-04-07-%D0%B2-14.39.13-300x300.png)](https://core-jmp.org/2026/04/poisonx-terminating-protected-windows-processes-via-byovd/)

April 7, 2026

by[oxfemale](https://core-jmp.org/author/oxfemale/ "View all posts by oxfemale")

withno comment

[BYOUD](https://core-jmp.org/security/byoud/ "View all posts in BYOUD") [BYOVD](https://core-jmp.org/security/byovd/ "View all posts in BYOVD") [Exploit Development](https://core-jmp.org/security/exploit-development/ "View all posts in Exploit Development") [exploitation](https://core-jmp.org/security/exploitation/ "View all posts in exploitation") [PPL](https://core-jmp.org/security/windows/ppl/ "View all posts in PPL") [winapi](https://core-jmp.org/security/windows/winapi/ "View all posts in winapi") [winapi](https://core-jmp.org/security/winapi-2/ "View all posts in winapi") [windows](https://core-jmp.org/security/windows/ "View all posts in windows")

### Introduction

**PoisonX** is a research tool demonstrating the **Bring Your Own Vulnerable Driver (BYOVD)** technique to terminate any Windows process — including **Protected Processes (PP)** and **Protected Process Light (PPL)** such as modern **EDR and antivirus services** (for example, CrowdStrike Falcon).

The tool uses a **Microsoft-signed kernel driver** that exposes a vulnerable **IOCTL interface**. Because the driver is signed by the **Microsoft Windows Hardware Compatibility Publisher**, Windows allows it to load normally without triggering code-integrity protections. Once loaded, the driver accepts commands from user-mode software and can terminate arbitrary processes at the kernel level.

This project is designed for **security research, red-team experimentation, and defensive testing** to demonstrate how vulnerable but trusted drivers can be abused to bypass endpoint security mechanisms.

![](https://core-jmp.org/wp-content/uploads/2026/04/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0-2026-04-07-%D0%B2-14.39.13.png)

[https://github.com/oxfemale/PoisinX](https://github.com/oxfemale/PoisinX)

## Driver Properties

| Property | Value |
| --- | --- |
| Device path | `\\.\{F8284233-48F4-4680-ADDD-F8284233}` |
| IOCTL code | `0x22E010` |
| Signer | Microsoft Windows Hardware Compatibility Publisher |
| Sign date | 2025-03-25 |

Because the driver is **officially signed**, it bypasses standard driver-loading restrictions enforced by **Windows Code Integrity**. This allows attackers or researchers to interact with the driver through a stable device interface exposed via a fixed GUID.

* * *

## How PoisonX Works

PoisonX operates as a user-mode controller that interacts with the vulnerable kernel driver.

```
PoisonX.exe
   │
   ├─ Checks administrator privileges
   ├─ Attempts to enable SeDebugPrivilege
   │
   ├─ [--extract]           Extract embedded driver variants
   ├─ [--driver-install]    Install driver using SCM
   ├─ [--driver-uninstall]  Remove driver service
   ├─ [--pid-list]          Enumerate processes and protection levels
   └─ [--poison-pid]        Send IOCTL_KILL → target process terminated
```

When the **–poison-pid** command is used and no driver is currently installed, PoisonX performs automatic deployment:

1. Iterates through up to **18 embedded driver variants** (`PoisonX1.sys … PoisonX18.sys`)
2. Extracts the first available driver next to the executable
3. Installs the driver as a **kernel-mode service** using the Service Control Manager
4. Sends a kill request to the driver via **DeviceIoControl**
5. The driver terminates the specified process

The process identifier is transmitted to the driver as an **ASCII payload**, which the driver parses and uses to locate the target process.

* * *

## Architecture

The PoisonX codebase is organized into several modular components.

```
PoisinX/
 ├─ PoisinX.cpp       Entry point and CLI dispatcher
 ├─ poison.cpp/h      IOCTL communication with the driver
 ├─ service.cpp/h     Kernel driver install/uninstall via SCM
 ├─ extract.cpp/h     Embedded resource extraction
 ├─ proclist.cpp/h    Process enumeration and PP/PPL detection
 ├─ admin.cpp/h       Privilege checks and SeDebugPrivilege
 ├─ banner.cpp/h      Console banner display
 ├─ log.cpp/h         Thread-safe logging system
 ├─ resource.h        Resource definitions
 └─ resources.rc      Embedded driver binaries
```

## Module Responsibilities

| Module | Description |
| --- | --- |
| poison | Opens the device interface and sends `DeviceIoControl(IOCTL_KILL)` |
| service | Handles kernel driver service lifecycle via SCM |
| extract | Extracts driver binaries embedded as Win32 resources |
| proclist | Enumerates processes and displays protection levels |
| admin | Verifies administrator privileges and enables debugging rights |
| log | Provides configurable logging with multiple verbosity levels |

The **proclist module** is particularly useful for researchers, as it displays each running process along with its **PP/PPL protection type and signer information**.

* * *

## Usage

### Basic commands

```
PoisonX.exe --driver-install   <driver_name>
PoisonX.exe --driver-uninstall <driver_name>
PoisonX.exe --extract          <resource_number>
PoisonX.exe --pid-list
PoisonX.exe --poison-pid       <pid>
```

![](https://core-jmp.org/wp-content/uploads/2026/04/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0-2026-04-07-%D0%B2-14.39.45.png)

* * *

### Options

| Flag | Description |
| --- | --- |
| `--log-level <0-3>` | Set verbosity level |
| `--write-log <file>` | Save console output to UTF-8 log file |

* * *

### Examples

List all running processes and their protection status:

```
PoisonX.exe --pid-list
```

![](https://core-jmp.org/wp-content/uploads/2026/04/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0-2026-04-07-%D0%B2-14.40.00-1024x733.png)

Terminate process PID 1234 (auto-deploy driver if needed):

```
PoisonX.exe --poison-pid 1234
```

Extract the first driver variant:

```
PoisonX.exe --extract 1
```

Install or uninstall driver manually:

```
PoisonX.exe --driver-install PoisonX1
PoisonX.exe --driver-uninstall PoisonX1
```

Verbose execution with logging:

```
PoisonX.exe --poison-pid 1234 --log-level 3 --write-log C:\Temp\poisonx.log
```

* * *

## Building the Project

| Requirement | Version |
| --- | --- |
| Visual Studio | 2019 or newer |
| Toolset | v143 |
| C++ Standard | C++14 |
| Target | x64 |

To build the project:

1. Open `PoisinX.vcxproj` in Visual Studio
2. Select **Release configuration**
3. Build the project

Before building, ensure that the **embedded driver binaries** are present in `resources.rc` as Win32 resources with IDs **101–118**.

* * *

## Logging System

PoisonX includes a flexible logging system that supports multiple verbosity levels.

| Level | Flag | Output |
| --- | --- | --- |
| 0 | MINIMAL | Only critical results |
| 1 | INFO | Operational steps |
| 2 | ERROR | Windows error messages |
| 3 | VERBOSE | Full internal tracing |

Logs can optionally be mirrored to a **UTF-8 file** for analysis.

* * *

## Security Implications

PoisonX highlights a critical weakness in modern endpoint defenses: **trusted but vulnerable drivers**.

Because these drivers:

- are **digitally signed**
- run with **kernel privileges**
- expose unsafe **IOCTL handlers**

they can be abused to bypass **process protection mechanisms** implemented by Windows and endpoint security products.

BYOVD attacks have become increasingly common in **ransomware campaigns, red-team operations, and advanced malware**, where attackers disable monitoring tools before deploying further payloads.

* * *

## Conclusion

PoisonX demonstrates how a **signed vulnerable driver can undermine core Windows security protections**. By exposing a kernel-level process termination primitive, the tool illustrates the risks posed by trusted drivers with unsafe interfaces.

For defenders, this research reinforces the importance of:

- maintaining **driver blocklists**
- monitoring **kernel driver loading**
- detecting suspicious **DeviceIoControl interactions**

Understanding these techniques is essential for improving modern endpoint protection and preventing kernel-level abuse.

### Share this:

- [Share on Facebook (Opens in new window)Facebook](https://core-jmp.org/2026/04/poisonx-terminating-protected-windows-processes-via-byovd/?share=facebook&nb=1)
- [Share on X (Opens in new window)X](https://core-jmp.org/2026/04/poisonx-terminating-protected-windows-processes-via-byovd/?share=x&nb=1)

### Like this:

LikeLoading…

Comments are closed.

Shopping Basket

![AI Engine Chatbot](https://core-jmp.org/wp-content/plugins/ai-engine/images/chat-traditional-1.svg)

AI:

Hi! How can I help you?

%d