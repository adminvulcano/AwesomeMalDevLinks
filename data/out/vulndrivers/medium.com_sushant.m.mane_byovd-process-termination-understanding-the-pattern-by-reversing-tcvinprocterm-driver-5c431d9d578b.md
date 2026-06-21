# https://medium.com/@sushant.m.mane/byovd-process-termination-understanding-the-pattern-by-reversing-tcvinprocterm-driver-5c431d9d578b

[Sitemap](https://medium.com/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40sushant.m.mane%2Fbyovd-process-termination-understanding-the-pattern-by-reversing-tcvinprocterm-driver-5c431d9d578b&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

Get app

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40sushant.m.mane%2Fbyovd-process-termination-understanding-the-pattern-by-reversing-tcvinprocterm-driver-5c431d9d578b&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![Unknown user](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

# BYOVD & Process Termination: Understanding The Pattern By Reversing TCVINProcTerm Driver

[![Sushant M Mane | The Cyber Veda IN](https://miro.medium.com/v2/resize:fill:32:32/1*oFq5g7toWmW-JTlNQHotKQ.png)](https://medium.com/@sushant.m.mane?source=post_page---byline--5c431d9d578b---------------------------------------)

[Sushant M Mane \| The Cyber Veda IN](https://medium.com/@sushant.m.mane?source=post_page---byline--5c431d9d578b---------------------------------------)

Follow

13 min read

·

May 24, 2026

1

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D5c431d9d578b&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40sushant.m.mane%2Fbyovd-process-termination-understanding-the-pattern-by-reversing-tcvinprocterm-driver-5c431d9d578b&source=---header_actions--5c431d9d578b---------------------post_audio_button------------------)

Share

> _Author — Sushant Mane_
>
> _LinkedIn —_ [https://www.linkedin.com/in/sushantmmane/](https://www.linkedin.com/in/sushantmmane/)
>
> Website — [https://thecyberveda.in/](https://thecyberveda.in/)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*w36VYv24Nb7ZRlMBYyFnhw.png)

## Introduction

Incident reports and malware analysis reports often mention **BYOVD**( _Bring Your Own Vulnerable Driver_) in the same breath as process termination, EDR interfaces, or “kernel-level” kills. The term is easy to look up but hard to connect to a concrete mechanism if you have never traced a driver IOCTL path.

This article walks through the full picture in one place:

- What BYOVD means in practice ?
- How a kernel driver exposes process termination to user mode ?
- How to reverse a minimal reference driver — **TCVINProcTerm.sys**( _The Cyber Veda India Process Terminator Driver_) to recover it’s device name, IOCTL, and input format ?
- How to validate that analysis in an isolated VM ?

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1000/1*Am65xSC2EaxYfYXQaMQ39Q.png)

**Disclaimer:** The driver was built for education: it accepts a process ID (PID) via an IOCTL and terminates the target using **ZwOpenProcess** and **ZwTerminateProcess.** We do not distribute known-vulnerable third-party drivers or IOCTL tables for them. The goal is to understand the **pattern** attackers use or defenders see in the field, using a binary that can be safely analyzed.

## **What BYOVD Is ?**

**Bring Your Own Vulnerable Driver** describes a technique where an attacker loads a **legitimately signed** kernel driver that exposes dangerous functionality, often through an IOCTL and invokes that functionality from user mode.

The steps are consistent across many cases:

1. **Load** a kernel driver (.sys) onto the system.
2. **Open** the driver’s user mode device path (\\\.\\DeviceName).
3. **Send an IOCTL** with a small input buffer (for terminators, often a PID).
4. The driver’s **dispatch routine** runs in kernel mode and performs a privileged action.

For process-termination families, that action is typically opening the target process with terminate access and calling **ZwTerminateProcess.**

This is distinct from:

- **Exploiting a kernel memory bug** in the OS itself.
- **Loading an unsigned driver** on a system that enforces signing (normal production configurations block that).

BYOVD abuses **trust in a signed module** and **weakness in its design or access control** (overly powerful IOCTL, permissive device ACL, no caller verification). In short not necessarily a classic memory corruption vulnerability.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*cd8zMbCnAa8J0PxsWIvE2A.png)

## User Mode & Kernel Mode

Windows runs code in **user mode** (Ring 3)and **kernel mode**(Ring 0).

**User mode** hosts most applications. Each process has its own virtual address space. A crash usually affects only that process. Security products commonly monitor user-mode APIs related to process operations (for example, **OpenProcess, TerminateProcess** ).

**Kernel mode** hosts the operating system core and drivers. Drivers can invoke kernel APIs such as **ZwOpenProcess** and **ZwTerminateProcess.** Errors in kernel code can destabilize the entire system.

User-mode programs do not call ZwTerminateProcess directly. They can communicate with drivers through **device objects:** open a handle with **CreateFile** on \\\.\\DeviceName, then use **DeviceIoControl** to send IOCTLs. The I/O manager delivers those requests to the driver as **IRPs (I/O Request Packets).**

That boundary: User Client → Device → IOCTL → Driver → Kernel API, is the structure you should internalize before opening a disassembler.

## The Attack Pipeline

The following flow applies to **TCVINProcTerm** and many process-terminator drivers described in threat intelligence.

```
1. LOAD
   .sys installed/loaded → DriverEntry
   Creates \Device\TCVINProcTerm and symlink \\.\TCVINProcTerm

2. OPEN (user mode)
   CreateFile("\\\\.\\TCVINProcTerm")

3. IOCTL (user mode)
   DeviceIoControl(IOCTL, input buffer, ...)
   Input: ULONG ProcessId (4 bytes)

4. DISPATCH (kernel)
   I/O Manager → IRP_MJ_DEVICE_CONTROL → DeviceControl()

5. ACT (kernel)
   ZwOpenProcess → ZwTerminateProcess → ZwClose
```

**User mode** controls steps 2–3. **Kernel mode** executes steps 1,4–5. BYOVD reports usually emphasize that step 1 used a **signed non-Microsoft driver** and that step 3 was available to a process that should not have had that capability.

## Driver Structure ( What You Will See In The Binary )

You do not need to write a driver to reverse one, but understanding driver code and internals would help a lot. These componenets map directly to what appears in **TCVINProcTerm.sys.**

### Driver and Service

A driver is a **.sys** image loaded into kernel memory, often via the Service Control Manager ( **sc create**/ **sc start** with **type= kernel**).

From an analyst perspective, a new kernel module plus a new device name is a meaningful event.

### Device Object & Symlink

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*MQll37ihhwI7NCLShdZqHg.png)

The kernel creates an internal device object; the symlink exposes a Win32 path. If the client opens the wrong name or the driver is not loaded, **CreateFile** fails — commonly with error 2 ( **ERROR\_FILE\_NOT\_FOUND).**

In static analysis, search the **strings** list for **\\Device\** and **\\DosDevices\** (or **\\??\**) and follow cross-references into initialization code.

### DriverEntry

On load, Windows calls **DriverEntry.** Typical responsibilities:

- **IoCreateDevice —** create **\\Device\\TCVINProcTerm**
- **IoCreateSymbolicLink —** map the user-visible name
- Assign **DriverObject →MajorFunction\[\]** handlers
- Set device flags (this driver uses **buffered I/O** for IOCTLs)
- Clear **DO\_DEVICE\_INITIALIZING**

In a decompiler, look for calls to **IoCreateDevice** and **IoCreateSymbolicLink,** then a series of writes to the major function table.

### **IRPs and Completion**

Each **CreateFile** or **DeviceIoControl** operation becomes an I/O Request Packet **(IRP).**

> **Definition:** An I/O Request Packet (IRP) is a fundamental core-mode data structure used by the Windows operating system to manage and route hardware and software I/O operations. Whenever an application requests to read/write a file, communicate with a USB device, or send network packets, the I/O Manager creates an IRP to represent that request as it travels through a layered stack of device drivers.
>
> **Reference:** [https://learn.microsoft.com/en-us/windows-hardware/drivers/gettingstarted/i-o-request-packets](https://learn.microsoft.com/en-us/windows-hardware/drivers/gettingstarted/i-o-request-packets)

The driver must set **Irp →IoStatus.Status**, optionally **Irp →IoStatus.Information**, and call **IoCompleteRequest** on every code path. Missing completion can hang callers or contribute to instability.

To see more about the IRP structure, you can refer [https://www.vergiliusproject.com/.](https://www.vergiliusproject.com/)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*LGBWGiYwToAg5xoSdEEZrg.png)

### Major Function Table

Handlers are indexed by IRP major function code. The ones that matter here:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*WXfKTt7ecIuoYM6hhy0bEw.png)

For reversal: locate **DriverEntry**, find the write to **MajorFunction\[14\]**, and analyze that function as **DeviceControl**. Create/close handlers usually only complete the IRP with success.

### DeviceControl

**DeviceControl** reads the IOCTL code and buffer lengths from the IRP stack, validates input, performs work, and completes the IRP. For terminators, the work is a helper that opens the process by PID and terminates it.

## IOCTLs and the termination contract

An IOCTL is a 32-bit control code passed to **DeviceIoControl**. It is constructed with the **CTL\_CODE** macro from device type, function index, transfer method, and required access.

**TCVINProcTerm** defines:

- **Name:** IOCTL\_TCVIN\_PROCESS\_TERMINATE. ( Just a name given to the corresponding IOCTL during development).
- **Transfer Method:** **METHOD\_BUFFERED** — the I/O manager copies input from user space into a system buffer exposed as **Irp →AssociatedIrp.SystemBuffer**
- **Input:** a single **ULONG ProcessId** (minimum length 4 bytes)

There is no complex structure — only a PID. That simplicity is common in terminator drivers.

When you reverse the binary, the IOCTL appears as a **numeric constant** compared against **Parameters.DeviceIoControl.IoControlCode** in **DeviceControl.** Record that hex value.

## How Kernel Based Process Termination Work ?

### User Mode Equivalent

```
OpenProcess(PROCESS_TERMINATE, ..., pid)
TerminateProcess(handle, exitCode)
CloseHandle(handle)
```

Security rools and policies often focus on this path.

### Kernel Path (TCVINProcTerm)

```
ZwOpenProcess(&handle, DesiredAccess, ObjectAttributes, ClientId)
ZwTerminateProcess(handle, ExitStatus)
ZwClose(handle)
```

**PID versus handle:** the IOCTL carries a **PID**. The driver must open a kernel handle with appropriate access before terminating.

### Access Mask

**ZwOpenProcess** takes an **ACCESS\_MASK** as **DesiredAccess.** The syntax is shown below —

```
NTSYSAPI NTSTATUS ZwOpenProcess(
  [out]          PHANDLE            ProcessHandle,
  [in]           ACCESS_MASK        DesiredAccess,
  [in]           POBJECT_ATTRIBUTES ObjectAttributes,
  [in, optional] PCLIENT_ID         ClientId
);
```

For termination, the driver requests process-specific termination rights:

```
PROCESS_TERMINATE = 0x0001
```

This is not the same as standard object rights like **DELETE** or **SYNCHRONIZE** described in the generic access-mask documentation. Those apply to all object types; **PROCESS\_TERMINATE** applies to process objects. In disassembly, the access argument to **ZwOpenProcess** is often the immediate value 1.

**InitializeObjectAttributes** is used with **OBJ\_KERNEL\_HANDLE** so the handle is stored in the kernel handle table.

**CLIENT\_ID:** set **UniqueProcess** to the PID (as a handle-valued integer) and **UniqueThread** to NULL.

**NTSTATUS values to expect**

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*AyVJAs-OM8PFiciVM9SXXA.png)

Kernel code does not guarantee success against all targets. **Protected Process Light (PPL)** and other policies still apply. We will try killing both Notepad.exe and LSASS.exe which is a PPL Protected process.

### Pseudocode Aligned With The Binary

Below is the pseudocode of the driver and now we can relate to the code as we have covered a lot of basics and theory behing it.

```
DeviceControl:
  if IoControlCode != IOCTL_TCVIN_PROCESS_TERMINATE
      return STATUS_INVALID_DEVICE_REQUEST

  if InputBufferLength < sizeof(ULONG)
      return STATUS_BUFFER_TOO_SMALL

  pid = *(ULONG*)SystemBuffer
  return TerminateProcessByPid(pid)

TerminateProcessByPid(pid):
  ZwOpenProcess(..., PROCESS_TERMINATE, ..., pid)
  ZwTerminateProcess(...)
  ZwClose(...)
```

## Reversing TCVINProcTerm.sys ( Our Process Termination Driver )

**Tools**

- Ghidra or IDA Free/Pro (x64) — I will be using Ghidra here.

### Step 1: Strings

> Open the strings view and locate:
>
> `1. \Device\TCVINProcTerm`
>
> `2. \DosDevices\TCVINProcTerm`

Follow cross-references into the initialization path. This confirms the sample and shows where the device is registered.

## Get Sushant M Mane \| The Cyber Veda IN’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

After importing the driver in Ghidra and analyzing it in the code browser, we can search for **strings.**

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*5poU_NAHHYclX_E0rlyCEQ.png)

We can see the strings —

```
DEFINED 1400019c0 u_\DosDevices\TCVINProcTerm_1400019c0 unicode u"\\DosDevices\\TCVINProcTerm" u"\\DosDevices\\TCVINProcTerm" unicode 52 true
DEFINED 140001a00 u_\Device\TCVINProcTerm_140001a00 unicode u"\\Device\\TCVINProcTerm" u"\\Device\\TCVINProcTerm" unicode 44 true
```

Under **X-Refs** .i.e. the **Cross-References** we can see the **function** where this string is referred.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*Fa5X9Atj2_X-St-CfelQbg.png)

In the decompiler window, we can see the pseudo-code where the string is being used.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*m4wgrV0xIVtm61OcQZ7z5A.png)

### Step 2: DriverEntry

> Go to the PE entry point. Identify `DriverEntry` by the pattern:
>
> `1. IoCreateDevice`
>
> `2. IoCreateSymbolicLink`
>
> Writes to `MajorFunction` array

Checking for the **Cross References** for FUN\_140001230, it takes us to the **DriverEntry** function.

![](https://miro.medium.com/v2/resize:fit:690/1*oePbP5DY1LFG5EzL5FKHJw.png)

Below is the actual source code which you can refer to understand more about the pseudocode generated.

```
// Driver Entry
NTSTATUS DriverEntry(
 _In_ PDRIVER_OBJECT DriverObject,
 _In_ PUNICODE_STRING RegistryPath
) {
 NTSTATUS status;
 UNICODE_STRING deviceName;
 UNICODE_STRING symlinkName;

 UNREFERENCED_PARAMETER(RegistryPath);

 RtlInitUnicodeString(&deviceName, DEVICE_NAME);
 RtlInitUnicodeString(&symlinkName, SYMLINK_NAME);

 status = IoCreateDevice(
  DriverObject,
  0,
  &deviceName,
  FILE_DEVICE_UNKNOWN,
  0,
  FALSE,
  &g_DeviceObject
 );

 if (!NT_SUCCESS(status)) {
  return status;
 }

 status = IoCreateSymbolicLink(&symlinkName, &deviceName);

 if (!NT_SUCCESS(status)) {
  IoDeleteDevice(g_DeviceObject);
  g_DeviceObject = NULL;
  return status;
 }

 // Major Functions
 DriverObject->MajorFunction[IRP_MJ_CREATE] = CreateClose;
 DriverObject->MajorFunction[IRP_MJ_CLOSE] = CreateClose;
 DriverObject->MajorFunction[IRP_MJ_DEVICE_CONTROL] = DeviceControl;
 DriverObject->DriverUnload = DriverUnload;

 return STATUS_SUCCESS;

}
```

Based on this we can rename and redefine the types of the variable properly.

But the main things we found here is:

1. **Device Name — “\\\.\\TCVINProcTerm”**

![](https://miro.medium.com/v2/resize:fit:649/1*RxA9Qt70GcWLkFqWPtYXVg.png)

### Step 3: Locate DeviceControl

> From `DriverEntry`, find the handler stored at `MajorFunction[0x0E]` (index 14). Rename it `DeviceControl`.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:645/1*4tBNxdrokNPpg1cz9ygsGg.png)

### Step 4: Recover IOCTL and Input

> In `DeviceControl`, look for:
>
> \- Comparison of `IoControlCode` to a constant → record IOCTL (hex)
>
> \- Check that `InputBufferLength >= 4`
>
> \- Read `*(ULONG*)` from `Irp->AssociatedIrp.SystemBuffer`
>
> Fill in a short worksheet:

```
Symlink / device strings:     (from step 1)
IOCTL (hex):                  ___________
Minimum input size:           4 bytes
Input layout:                 ULONG ProcessId at offset 0
ZwOpenProcess present:        yes / no    Access mask: 0x1
ZwTerminateProcess present:   yes / no
All IRP paths complete:       verify IoCompleteRequest on branches
```

Observing the DeviceControl function we can find the IOCTL ( Hex Number ) being present over there.

![](https://miro.medium.com/v2/resize:fit:699/1*TpxKPc8NlbGogt_c0qD88Q.png)

which calls the function FUN\_1400012e0, which upon observation is our function which contains the **ZwTerminateProcess**

![](https://miro.medium.com/v2/resize:fit:607/1*F4YIIHP5uoWycR60ADCyQw.png)

Therefore, the IOCTL is 0x222000, which takes us to the ZwTerminateProcess API.

Filling the above worksheet —

```
Symlink / device strings:     \\.\TCVINProcTerm
IOCTL (hex):                  0x222000
Minimum input size:           4 bytes
Input layout:                 ULONG ProcessId at offset 0
ZwOpenProcess present:        yes | Access mask: 0x1
ZwTerminateProcess present:   yes
```

### Step 5: Termination Helper

> Follow the call from `DeviceControl` into the helper that invokes `ZwOpenProcess`, `ZwTerminateProcess`, and `ZwClose`. Rename the helper (e.g. `TerminateProcessByPid`).

If we see the syntax/documentation for ZwTerminateProcess, we can see that the first argument is the ProcessHandle to be terminated.

```
NTSYSAPI NTSTATUS ZwTerminateProcess(
  [in, optional] HANDLE   ProcessHandle,
  [in]           NTSTATUS ExitStatus
);
```

ProcessHandle is passed to ZwTerminateProcess by ZwOpenProcess which has the following syntax —

```
NTSYSAPI NTSTATUS ZwOpenProcess(
  [out]          PHANDLE            ProcessHandle,
  [in]           ACCESS_MASK        DesiredAccess,
  [in]           POBJECT_ATTRIBUTES ObjectAttributes,
  [in, optional] PCLIENT_ID         ClientId
);
```

A better pseudocode generated from IDA using symbols is shown below , read it, take your time and relate the concepts —

```
__int64 __fastcall DriverEntry(_DRIVER_OBJECT *DriverObject, _UNICODE_STRING *RegistryPath)
{
  int status; // [rsp+40h] [rbp-38h]
  int statusa; // [rsp+40h] [rbp-38h]
  _UNICODE_STRING deviceName; // [rsp+48h] [rbp-30h] BYREF
  _UNICODE_STRING symlinkName; // [rsp+58h] [rbp-20h] BYREF

  RtlInitUnicodeString(&deviceName, L"\\Device\\TCVINProcTerm");
  RtlInitUnicodeString(&symlinkName, L"\\DosDevices\\TCVINProcTerm");
  status = IoCreateDevice(DriverObject, 0, &deviceName, 0x22u, 0, 0, &g_DeviceObject);
  if ( status >= 0 )
  {
    statusa = IoCreateSymbolicLink(&symlinkName, &deviceName);
    if ( statusa >= 0 )
    {
      DriverObject->MajorFunction[0] = CreateClose;
      DriverObject->MajorFunction[2] = CreateClose;
      DriverObject->MajorFunction[14] = DeviceControl;
      DriverObject->DriverUnload = DriverUnload;
      return 0i64;
    }
    else
    {
      _mm_lfence();
      IoDeleteDevice(g_DeviceObject);
      g_DeviceObject = 0i64;
      return (unsigned int)statusa;
    }
  }
  else
  {
    _mm_lfence();
    return (unsigned int)status;
  }
}
```

```
__int64 __fastcall DeviceControl(_DEVICE_OBJECT *DeviceObject, _IRP *Irp)
{
  unsigned int status; // [rsp+20h] [rbp-38h]
  unsigned int ioctlCode; // [rsp+24h] [rbp-34h]
  unsigned int inLen; // [rsp+28h] [rbp-30h]
  _IO_STACK_LOCATION *irpSp; // [rsp+30h] [rbp-28h]
  unsigned int *buffer; // [rsp+38h] [rbp-20h]

  status = -1073741808;
  irpSp = IoGetCurrentIrpStackLocation(Irp);
  ioctlCode = irpSp->Parameters.Read.ByteOffset.LowPart;
  buffer = (unsigned int *)Irp->AssociatedIrp.MasterIrp;
  inLen = irpSp->Parameters.Create.Options;
  Irp->IoStatus.Information = 0i64;
  if ( ioctlCode == 2236416 )
  {
    if ( inLen >= 4ui64 && buffer )
      status = TerminateProcessByPid(*buffer);
    else
      status = -1073741789;
  }
  Irp->IoStatus.Status = status;
  IofCompleteRequest(Irp, 0);
  return status;
}
```

```
__int64 __fastcall TerminateProcessByPid(unsigned int ProcessId)
{
  int status; // [rsp+20h] [rbp-58h]
  void *processHandle; // [rsp+28h] [rbp-50h] BYREF
  _CLIENT_ID clientId; // [rsp+30h] [rbp-48h] BYREF
  _OBJECT_ATTRIBUTES objectAttributes; // [rsp+40h] [rbp-38h] BYREF

  processHandle = 0i64;
  objectAttributes.Length = 48;
  objectAttributes.RootDirectory = 0i64;
  objectAttributes.Attributes = 512;
  objectAttributes.ObjectName = 0i64;
  objectAttributes.SecurityDescriptor = 0i64;
  objectAttributes.SecurityQualityOfService = 0i64;
  clientId.UniqueProcess = (void *)ProcessId;
  clientId.UniqueThread = 0i64;
  status = ZwOpenProcess(&processHandle, 1u, &objectAttributes, &clientId);
  if ( status >= 0 )
  {
    status = ZwTerminateProcess(processHandle, 0);
    ZwClose(processHandle);
  }
  else
  {
    _mm_lfence();
  }
  return (unsigned int)status;
}
```

So, by reversing the driver we have found the device name and the IOCTL for Process Terminaton using ZwTerminateProcess. These 2 things are must for a minimal PoC to create the client and killing process.

## Demo

Run only on a disposable VM you control, with test signing enabled and a snapshot taken before loading the driver.

### Enable Test Signing

Elevated command prompt on the VM, enter the following line:

```
bcdedit /set testsigning on
```

Reboot. A “Test Mode” watermark indicates test signing is on. Do not use production systems.

![](https://miro.medium.com/v2/resize:fit:201/1*r50VeB0DmECixB_NO2icBg.png)

### Install & Start The Driver

Copying the TCVINProcTerm.sys to VM.

Using the following commands to load and start the driver.

```
sc create TCVINProcTerm type= kernel binPath= C:\<Path>\TCVINProcTerm.sys
sc start TCVINProcTerm
sc query TCVINProcTerm
```

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*dOfernOcgvfxm1efjLCGsA.png)

### Successful Termination

> 1\. Start Notepad and note its PID.
>
> 2\. Use a small client (or your own script) to:
>
> `- CreateFile(L"\\\\.\\TCVINProcTerm", ...)`
>
> `- DeviceIoControl` with the IOCTL recovered from reversal, passing a 4-byte PID
>
> 3\. Confirm Notepad exits.

The following is the code of our client, which is then compiled into an exe.

```
/*
@Author - Sushant Mane
@Description - Userland client to interact with the driver.
@Date - 24th May 2026
*/

#include <Windows.h>
#include <stdio.h>
#include "Process_Terminator.h"

int main(int argc, char** argv) {

 HANDLE hDevice;
 PROCESS_TERMINATE_REQUEST req;
 DWORD bytesReturned;
 BOOL ok;
 ULONG pid;

 if (argc < 2) {
  printf("Usage: %s <pid>\n", argv[0]);
  return 1;
 }

 pid = (ULONG)strtoul(argv[1], NULL, 10);
 req.ProcessId = pid;

 hDevice = CreateFileW(
  L"\\\\.\\TCVINProcTerm",
  GENERIC_READ | GENERIC_WRITE,
  0,
  NULL,
  OPEN_EXISTING,
  FILE_ATTRIBUTE_NORMAL,
  NULL
 );

 if (hDevice == INVALID_HANDLE_VALUE) {
  printf("CreateFile FAILED: %lu\n", GetLastError());
  return 1;
 }

 ok = DeviceIoControl(
  hDevice,
  IOCTL_TCVIN_PROCESS_TERMINATE,
  &req,
  sizeof(req),
  NULL,
  0,
  &bytesReturned,
  NULL
 );

 CloseHandle(hDevice);

 if (!ok) {
  printf("DeviceIoControl FAILED: %lu\n", GetLastError());
  return 1;
 }

 printf("IOCTL send for PID %lu\n", pid);

 return 0;
}
```

If the IOCTL, device name, or input size from your analysis is wrong, the process will remain running, this is a useful check that static analysis matched the binary.

In ProcessHacker we can observe the PID of Notepad.exe, and using our script we can kill it.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*oxs3FvYUSlKPVINlrC_Tdg.png)

Now after execution, we can see the process is killed, Notepad.exe with PID 4244 doesn’t exist.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*4z4_IHOzmIFwrvLKPndqCA.png)

### Cleanup

Close any open handles to the device, then:

```
sc stop TCVINProcTerm
sc delete TCVINProcTerm
```

Restore the VM snapshot if you want a clean state.

## Comparison with real-world BYOVD

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*mlwpcNTO3q59vKcHt_ywPA.png)

The mechanics are the same: signed (or lab test-signed) module, device object, IOCTL, kernel primitive. Defenders prioritize driver load, handle to `\\.\` devices, and correlation with process termination. Microsoft’s vulnerable driver blocklist and policies such as WDAC target known-abusable drivers at scale.

This article does not publish IOCTL values or binaries for known malicious drivers. The skill is recovering the contract from any sample you are authorized to analyze.

## Summary

After working through this article, you should be able to:

1. Explain BYOVD as signed driver + device + IOCTL + kernel action.
2. Trace the path from `CreateFile` on `\\.\TCVINProcTerm` to `DeviceControl` and `ZwTerminateProcess`.
3. Reverse `TCVINProcTerm.sys` to recover the device strings, IOCTL code, and 4-byte PID input.
4. Validate the analysis in a test-signed VM with success and failure cases.
5. Relate the pattern to detection and driver hardening in real environments.

TCVINProcTerm is a deliberate teaching sample. The same analysis steps apply to suspicious drivers in incident response — without requiring you to build a driver from scratch.

## Follow Us

**At The Cyber Veda India**, we cover major cyber events, share actionable knowledge, and deliver practical training online.

**Where to find us:**

- [**LinkedIn**](https://www.linkedin.com/company/the-cyber-veda-india) **:** Follow for in-depth articles on cybersecurity and electronic warfare
- [**YouTube**](https://www.youtube.com/@TheCyberVedaIN) **:** Watch technical breakdowns and training sessions on cyber defense
- [**Instagram**](https://www.instagram.com/thecyberveda_india/) **:** Quick insights on cybersecurity trends and incident analysis
- [**The Cyber Veda India**](https://thecyberveda.in/) **:** Our edutech platform offering cybersecurity training and workshops

If you found this breakdown useful, **follow along** for more content that keeps you informed about the latest in cybersecurity and electronic warfare.

**Stay secure. Stay informed.**

[Windows](https://medium.com/tag/windows?source=post_page-----5c431d9d578b---------------------------------------)

[Offensive Security](https://medium.com/tag/offensive-security?source=post_page-----5c431d9d578b---------------------------------------)

[Cybersecurity](https://medium.com/tag/cybersecurity?source=post_page-----5c431d9d578b---------------------------------------)

[Device Drivers](https://medium.com/tag/device-drivers?source=post_page-----5c431d9d578b---------------------------------------)

[Kernel](https://medium.com/tag/kernel?source=post_page-----5c431d9d578b---------------------------------------)

[![Sushant M Mane | The Cyber Veda IN](https://miro.medium.com/v2/resize:fill:48:48/1*oFq5g7toWmW-JTlNQHotKQ.png)](https://medium.com/@sushant.m.mane?source=post_page---post_author_info--5c431d9d578b---------------------------------------)

[![Sushant M Mane | The Cyber Veda IN](https://miro.medium.com/v2/resize:fill:64:64/1*oFq5g7toWmW-JTlNQHotKQ.png)](https://medium.com/@sushant.m.mane?source=post_page---post_author_info--5c431d9d578b---------------------------------------)

Follow

[**Written by Sushant M Mane \| The Cyber Veda IN**](https://medium.com/@sushant.m.mane?source=post_page---post_author_info--5c431d9d578b---------------------------------------)

[45 followers](https://medium.com/@sushant.m.mane/followers?source=post_page---post_author_info--5c431d9d578b---------------------------------------)

· [71 following](https://medium.com/@sushant.m.mane/following?source=post_page---post_author_info--5c431d9d578b---------------------------------------)

Follow

[Help](https://help.medium.com/hc/en-us?source=post_page-----5c431d9d578b---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----5c431d9d578b---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----5c431d9d578b---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----5c431d9d578b---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----5c431d9d578b---------------------------------------)

[Store](https://medium.com/store)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----5c431d9d578b---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----5c431d9d578b---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----5c431d9d578b---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----5c431d9d578b---------------------------------------)

reCAPTCHA

Recaptcha requires verification.

protected by **reCAPTCHA**