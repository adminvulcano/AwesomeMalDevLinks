# https://blog.talosintelligence.com/qilin-edr-killer/

[Blog](https://blog.talosintelligence.com/)

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/EDR-Killer-header-1.jpg)

# Qilin EDR killer infection chain

By [Takahiro Takeda](https://blog.talosintelligence.com/author/takahiro/),
[Holger Unterbrink](https://blog.talosintelligence.com/author/holger-unterbrink/)

Thursday, April 2, 2026 06:00


[Threat Spotlight](https://blog.talosintelligence.com/category/threat-spotlight/) [Reverse Engineering](https://blog.talosintelligence.com/category/reverse-engineering/) [malware](https://blog.talosintelligence.com/category/malware/)

- Endpoint detection and response (EDR) tools are widely deployed and far more capable than traditional antivirus. As a result, attackers use EDR killers to disable or bypass them.
- Disabling telemetry collection (process, memory, network activity) limits what defenders can see and analyze.
- As defenders improve behavioral detection, attackers increasingly target the defense layer itself as part of their initial access or early execution stages.
- This blog provides an in-depth analysis of the malicious “msimg32.dll” used in Qilin ransomware attacks, which is a multi-stage infection chain targeting EDR systems. It can terminate over 300 different EDR drivers from almost every vendor in the market.
- We present multiple techniques used by the malware to evade and ultimately disable EDR solutions, including SEH/VEH-based obfuscation, kernel object manipulation, and various API and system call bypass methods.

* * *

This blog post provides an in-depth technical analysis of the malicious dynamic-link library (DLL) “msimg32.dll”, which Cisco Talos observed being deployed in Qilin ransomware attacks. The broader activities and attacks of Qilin was previously introduced and described in the blog post [here](https://blog.talosintelligence.com/an-overview-of-ransomware-threats-in-japan-in-2025-and-early-detection-insights-from-qilin-cases).

This DLL represents the initial stage of a sophisticated, multi-stage infection chain designed to disable local endpoint detection and response (EDR) solutions present on compromised systems. Figure 1 shows a high-level diagram demonstrating the overall execution flow of this infection chain.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image1-1.jpg)Figure 1. Infection chain overview.

The first stage consists of a PE loader responsible for preparing the execution environment for the EDR killer component. This secondary payload is embedded within the loader in an encrypted form.

The loader implements advanced EDR evasion techniques. It neutralizes user-mode hooks and suppresses Event Tracing for Windows (ETW) event generation at runtime by leveraging a -like approach. Additionally, it makes extensive use of structured exception handling (SEH) and vectored exception handling (VEH) to obscure control flow and conceal API invocation patterns. This enables the EDR killer payload to be decrypted, loaded, and executed entirely in memory without triggering detection by the locally installed EDR solution.

Once active, the EDR killer component loads two helper drivers. The first driver (“rwdrv.sys”) provides access to the system’s physical memory, while the second driver (“hlpdrv.sys”) is used to terminate EDR processes. Prior to loading the second driver, the EDR killer component unregisters monitoring callbacks established by the EDR, ensuring that process termination can proceed without interference.

Overall, the malware is capable of disabling over 300 different EDR drivers across a wide range of vendors. While the campaign has been previously reported by , , and others at a higher level, this analysis focuses on previously undocumented technical details of the infection chain (e.g., the SEH/VEH tricks and the overwriting of certain kernel objects).

## PE loader section (“msimg32.dll”)

The malicious DLL is most likely side-loaded by a legitimate application that imports functions from “msimg32.dll”. To preserve expected functionality, the original API calls are forwarded to the legitimate library located in “C:\\Windows\\System32”.

The version of “msimg32.dll” deployed by the threat actor triggers its malicious logic from within its `DllMain` function. As a result, the payload is executed as soon as the legitimate application loads the DLL.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image2.png)Figure 2. Malicious version of “msimg32.dll”.

Sophos also gave some technical and historical insights into this loader in their earlier blog, in which it is referred to as Shanya.

### Initialization phase

During initialization, the loader allocates a heap buffer in process memory that acts as a slot-policy table.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image3.png)Figure 3a. Allocating buffer for slot-policy table.

The size of this buffer is computed as "ntdll.dll" `OptionalHeader.SizeOfCode` divided by 16 ( `SizeOfCode >> 4`), resulting in one byte per 16-byte code slot covering the code region as defined by `OptionalHeader.SizeOfCode` (typically the .text range). Each entry in the table corresponds to a fixed 16-byte block relative to `BaseOfCode`.

The loader then iterates over the export table of “ntdll.dll”. For each exported function whose name begins with "Nt", the virtual address of the corresponding syscall stub is resolved. From this address, a slot index is calculated as: slot\_idx = (FuncVA - BaseOfCode)/16

This index is used to mark the corresponding entry in the slot-policy table. All Nt\* stubs are assigned a default policy, while selected functions are explicitly marked with special policies, including:

- `NtTraceEvent`
- `NtTraceControl`
- `NtAlpcSendWaitReceivePort`

The result is a data-driven classification of relevant syscall stubs without modifying the executable code of “ntdll.dll”. The resulting slot-policy-table appears as follows:

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image4.png)Figure 3b. Slot-policy table.

The actual loader function is significantly more complex and incorporates additional obfuscation techniques, such as hash-based API resolution at runtime.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image5.png)Figure 4. Filling slot-policy table depending on “Nt” syscall stub functions.

After constructing the table, the sample dynamically resolves `ntdll!LdrProtectMrdata`, which will be discussed in greater detail later. It then invokes this routine to change the protection of the `.mrdata` section to writable. This section contains the exception dispatcher callback pointer along with other critical runtime data.

Once the section is writable, the loader overwrites the dispatcher slot with its own custom exception handler. As a result, its routine is executed whenever an exception is triggered.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image6.png)Figure 5. Overwriting of exception handler dispatcher slot.

### Runtime exception handling

This function primarily performs two tasks: handling breakpoint exceptions and single-step exceptions.

The handling of breakpoint exceptions (0xCC) is relatively straightforward. It simply resumes execution at the instruction immediately following the INT3 (0xCC). Talos is not certain why this approach was implemented. It may function as a lightweight anti-emulation, anti-analysis, or anti-sandbox mechanism for weak analysis systems, serve as groundwork for more advanced anti-debugging techniques, or act as preparation for future control-flow manipulation similar to the VEH-based logic observed in Stages 2 and 3.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image7.png)Figure 6. Breakpoint logic of `hook_function_ExceptionCallback` function.

The single-step portion of the function is significantly more complex and is where the previously introduced slot-policy table is utilized. `ctx->ntstub_class_map` points to the map buffer allocated during initialization.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image8.png)Figure 7. Single step logic of `hook_function_ExceptionCallback` function.

Simplified the logic of the initialization and dispatch function looks like this in pseudo code. `InitCtxAndPatchNtdllMrdataDispatch` is the initialization function and `hook_function_ExceptionCallback` is the dispatch function mentioned above.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image9.png)Figure 8. Simplified single step SEH logic.

The `find_syscall` routine shown in Figure 7 implements a syscall recovery technique. Details can be found in the picture below. It scans both backward and forward through “ntdll.dll” to locate intact syscall stubs and identify neighboring syscalls that can be repurposed.

The simplified logic is as follows:

- Indirectly determine the target syscall number by scanning forward and backward.
- Locate a clean neighbouring stub.
- Manually load the correct syscall ID into `eax`.
- Transition directly to kernel mode using the syscall instruction (i.e., a syscall instruction located inside a clean neighboring stub).

By reusing a neighboring syscall stub to invoke the desired system call, the loader bypasses EDR-hooked syscalls without modifying the hooked code itself. The Windows kernel only evaluates the syscall ID in `eax`; it does not verify which exported API function initiated the call.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image10.png)Figure 9. Halo’s Gate: `find_syscall` function.

As previously mentioned, the actual code of the malware is more complex (e.g., the aforementioned runtime resolution of `ntdll!LdrProtectMrdata`).

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image11.png)Figure 10. Resolution of `ntdll!LdrProtectMrdata` at runtime.

The loader resolves the `ntdll!LdrProtectMrdata` function in a stealthy way. Instead of resolving `LdrProtectMrdata` by name or hash, the loader instead:

- Finds the .mrdata section in the “ntdll.dll” image
- Checks whether the current dispatcher slot pointer (`dispatch_slot`) lies inside .mrdata
- If it does, it uses a known exported ntdll function (`RtlDeleteFunctionTable`, located via hash) as an anchor
- From that anchor, it scans for a CALL rel32 instruction (0xE8) and extracts its target address
- That call target is the address of `LdrProtectMrdata` and stored in `ctx->LdrProtectMrdata`

The initialization routine described earlier also incorporates several basic anti-debugging measures. For example, it verifies whether a breakpoint has been placed on `KiUserExceptionDispatcher`. If such a breakpoint is detected, the process is deliberately crashed. This check is performed before the dispatcher is overwritten, which means that the resulting exception is handled by the original, default exception handler.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image12.png)Figure 11. `KiUserExceptionDispatcher` breakpoint check.

The loader also implements geo-fencing. It excludes systems configured for languages commonly used in post-Soviet countries. This check is performed at an early stage, and the loader terminates if a locale from the exclusion list is detected.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image13.png)Figure 12. Geo-fencing function.![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image14.png)Figure 13. Geo-fencing excluded countries list.

After initializing Stage 1, the loader proceeds to unpack the subsequent stages. It creates a paging file-backed section and maps two views of this section into the process address space. This aspect was not analyzed in depth; however, creating two views of the same section is a common malware technique used to obscure a READ-WRITE-EXECUTABLE memory region. Typically, one view is configured with WRITE access only, masking the effective executable permissions of the underlying section. This shared memory region will contain subsequent malware stages after unpacking them. This also makes it more difficult to dump the memory during analysis. When a virtual memory page is not currently present in RAM (present bit cleared), accessing it triggers a page fault. The kernel then resolves the fault (e.g., by loading the page from the pagefile into physical memory).

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image15.png)Figure 14. `CreateFileMappingA` resolver function, returns the handle 0x174.![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image16.png)Figure 15. First “write only” view, `FILE_MAP_WRITE` (0x2).![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image17.png)Figure 16. Second “R-W-X” view, `0x24 = FILE_MAP_READ (0x4) | FILE_MAP_EXECUTE (0x20)`.

After creating the views, it copies and decodes bytes into this buffer. The basic block highlighted in green marks the start of this routine, while the red basic block represents the final control transfer (see Figure 17) to the decoded payload. The yellow basic block contains the decision logic that determines when execution transitions to the red basic block.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image18.png)Figure 17. Stage 2 decoding routine.

Inside the red basic block, we have the final jump into the decoded bytes of Stage 2.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image19.png)Figure 18. Call to Stage 2 in red basic block.

### Stage 2

Stage 2 (0x2470000) serves solely as a stealthy transition mechanism to transfer execution to Stage 3. As expected, all addresses referenced from this point onward, such as 0x2470000, may vary between executions of the loader, as they are dynamically allocated at runtime.

The initial part of Stage 2 is straightforward: It decodes the data stored in the memory section and then unmaps the previously mapped view. The subsequent function call constitutes the critical step: `ctx->FuncPtrHookIAT((ULONGLONG)ctx->hooking_func);`

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image20.png)Figure 19. Stage 2.![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image21.png)Figure 20. IAT hooking function.

This IAT-hooking routine overwrites the `ExitProcess` entry in the Import Address Table (IAT) of the main process (i.e., the process that loaded the malicious “msimg32.dll”).

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image22.png)Figure 21. Overwritten IAT pointer to `ExitProcess` at 0x140017138.

As shown in Figure 18, execution returns normally from Stage 2, and `DllMain` completes without any obvious anomalies. The malicious logic is triggered later, when `ExitProcess` is invoked by `exit_or_terminate_process` during process termination. Instead of terminating the process, execution is redirected to function 0x2471000, which corresponds to Stage 3.

### Stage 3

Stage 3 primarily decompresses and loads a PE image from memory that was originally embedded within the malicious “msimg32.dll”. It begins by resolving syscall stubs, which are used in subsequent code sections followed by decoding routines.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image23.png)Figure 22. Syscall resolution and execution of certain functions.

After several decoding and preparation steps, the PE image is decompressed from memory.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image24.png)Figure 23. Compressed buffer, previously unpacked.![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image25.png)Figure 24. Decompressed buffer.

After the PE image has been decompressed, the final routine responsible for preparing, loading, and ultimately executing the PE can be found at 0x24A2CE7 in this run.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image26.png)Figure 25. Final load and execution of the embedded PE.

The `fix_and_load_PE_set_VEH` function begins by mapping “shell32.dll” into the process address space using `NtCreateFile`, `NtCreateSection`, and `MapViewOfFile`. It then overwrites the in-memory contents of “shell32.dll” with the previously loaded PE image.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image27.png)Figure 26. Load “shell32.dll” into memory.

After copying the embedded and decoded PE image into memory, the code manually applies base relocations.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image28.png)Figure 27. PE relocation.

After preparing the PE for in-memory execution, the loader employs a technique similar to Stage 2, but this time leveraging a vectored exception handler (VEH). After registering the VEH, it triggers the handler by setting a hardware breakpoint on `ntdll!NtOpenSection`. To indirectly invoke `NtOpenSection`, the loader subsequently loads a fake DLL via a call to the `LdrLoadDll` API. It appears that the malware author intentionally chose a name referencing a well-known security researcher, likely as a provocative touch.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image29.png)Figure 28. Call to `LdrLoadDll`.

After several intermediate steps, this results in a call to `NtOpenSection`, which triggers the previously configured hardware breakpoint and, in turn, invokes the VEH. The first time the VEH is triggered at `NtOpenSection`, it executes the code in Figure 29.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image30.png)Figure 29. Malicious VEH, part 1: `NtOpenSection` handler.

It modifies the “shell32.dll” name in memory to “hasherezade\_\[redacted\].dll”, then adjusts RIP in the context record to point to the next `ret` instruction (0xC3) within the `NtOpenSection` stub and sets a new hardware breakpoint on `NtMapViewOfSection`. In addition, it updates the stack pointer to reference `LdrpMinimalMapModule+offset`, where the offset corresponds to an instruction immediately following a call to `NtOpenSection` inside `LdrpMinimalMapModule`. It then invokes `NtContinue`, which resumes execution at the RIP value stored in the context record (i.e., at the `ret` instruction). That `ret` instruction subsequently transfers control to the address prepared on the stack, namely `LdrpMinimalMapModule+offset`.

`cr_1->rsp = LdrpMinimalMapModule+offset
cr_1->rip = ntdll!NtOpenSection+0x14 = ret ; jumps to <rsp> when executed`

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image31.png)Figure 30. Jump destination after calling `NtOpenSection`.

During execution of `LdrpMinimalMapModule`, a call to `NtMapViewOfSection` is made, which triggers the hardware breakpoint set by the previous routine. On this occasion, the VEH executes the code in Figure 31.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image32.png)Figure 31. Malicious VEH, part 2: `NtMapViewOfSection` handler.

It deletes all HW breakpoints and then sets the stackpointer to an address which points to an address in `LdrMinimalMapModule+offset`. As expected, this is right after a call to `NtMapViewOfSection`. In other words, the registers in the context are overwritten like this:

`ctx->rsp -> ntdll!LdrpMinimalMapModule+0x23b
ctx->rip -> ntdll!NtMapViewOfSection+0x14 = ret`

When the return (ret) instruction is reached, it jumps to the address stored in the stack pointer (rsp).

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image33.png)Figure 32. Jump destination after `call NtMapViewOfSection`.

The subsequent code in `LdrpMinimalMapModule` maps the previously restored PE image into the process address space and prepares it for execution. Finally, control returns to 0x24A3C1E, the instruction immediately following the call that originally triggered the first hardware breakpoint.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image34.png)Figure 33. Instruction after the call to `LdrLoadDll`.

After several additional fix-up steps, the loader transfers execution to Stage 4 (i.e., the loaded PE image).

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image35.png)Figure 34. Final jump to loaded PE.

This PE file is an EDR killer capable of disabling over 300 different EDR drivers across a wide range of solutions. A detailed analysis of this component will be provided in the next section.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image36.png)Figure 35. Excerpt from the EDR driver list.

### PE loader summary

The first three stages of this binary implement a sophisticated and complex PE loader capable of bypassing common EDR solutions by evading user-mode hooks through carefully crafted SEH and VEH techniques. While these methods are not entirely novel, they remain effective and should be detectable by properly implemented EDR solutions.

The loader decrypts and executes an embedded PE payload in memory. In this campaign, the payload is an EDR killer capable of disabling over 300 different EDR products. This component will be analyzed in detail in the next section.

## EDR killer

### Stage 4: Extracted EDR killer PE file

Besides initialization, the first thing the extracted PE from Stage 3 does is check again if the system locale matches a list of post-Soviet countries and, if it does, it crashes. This is another indicator that former stages are just a custom PE loader, which could be used to load any PE the adversaries want. Otherwise, doing the same check again is not logical.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image37.png)Figure 36. Malware geo-fencing function.![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image38.png)Figure 37. List of blocked countries.

The malware then attempts to elevate its privileges and load a helper driver. This also implies that the process must be executed with administrative privileges.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image39.png)Figure 38. Privilege escalation and loading of helper driver.

The “rwdrv.sys” driver is a renamed version of “ThrottleStop.sys”, originally distributed by TechPowerUp LLC and signed with a valid digital certificate. It is legitimately used by tools such as GPU-Z and ThrottleStop. This is not the first observed abuse of this ; it has previously been leveraged in several malware campaigns.

Despite its benign origin, the driver exposes highly powerful functionality and can be loaded by arbitrary user-mode applications. Critically, it implements these capabilities without enforcing meaningful security checks, making it particularly attractive for abuse.

This driver exposes a low-level hardware access interface to user mode via input/output controls (IOCTLs). It allows a user-mode application to directly interact with system hardware.

The driver implements IOCTL handlers that provide the following capabilities:

- I/O port access
  - Read from hardware ports (inb/inw/ind)
  - Write to hardware ports (outb/outw/outd)
- CPU Model Specific Register (MSR) access
  - Read MSRs (\_\_readmsr)
  - Write MSRs (\_\_writemsr) with limited protection against modifying critical syscall/sysenter registers
- Physical memory/MMIO access
  - Map arbitrary physical memory into kernel space using MmMapIoSpace
  - Create a user-mode mapping of the same memory using MmMapLockedPagesSpecifyCache
  - Maintain up to 256 active mappings per driver instance
  - Provide an IOCTL to release/unmap those mappings
- Direct physical memory access
  - Read physical memory values
  - Write physical memory values
- PCI configuration space access
  - Read PCI configuration registers (HalGetBusDataByOffset)
  - Write PCI configuration registers (HalSetBusDataByOffset)

Additionally, the driver tracks the number of open handles and associates memory mappings with the calling process ID.

Overall, the driver functions as a generic kernel-mode hardware access layer, exposing primitives for port I/O, MSR access, physical memory mapping, and PCI configuration operations. Such functionality is typically used by hardware diagnostic tools, firmware utilities, or low-level system utilities, but it also provides powerful primitives that could be abused if accessible from unprivileged user-mode.

The two important functions heavily used by the sample are the ability to read and write physical memory.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image40.png)Figure 39. Read physical memory IOCTL.![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image41.png)Figure 40. Write physical memory IOCTL.

After loading the driver, the malware proceeds to determine the Windows version. To do so, it first resolves the required API function using a PEB-based lookup routine, a technique consistently employed throughout the sample.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image42.png)Figure 41. DLL resolution.![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image43.png)Figure 42. API function resolution.

The implementation parses the Process Environment Block (PEB) and locates the target module by finding the hash of its name. Then the `ResolveExportByHash` function takes the module base from the previously found DLL and parses its PE header to find the function that corresponds to the function hash. It can either provide the API function address as an PE offset or as a virtual address.

After a couple of initializations and checks, it gets the “rwdrv.sys” handle, followed by the EDR-related part of the sample — the kernel tricks which are responsible for avoiding, blinding, and disabling the EDR.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image44.png)Figure 43. Get driver handle for “rwdrv.sys”.![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image45.png)Figure 44. Overview of the EDR killer part of the sample.

However, let’s have a brief look into the details. It starts with building a vector of physical memory pages. This vector will later be used in subsequent methods.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image46.png)Figure 45. Initialization logic of the Page Frame Number (PFN) metadata list.

The `SetMemLayoutPointer`function in the if statement above leverages the `NtQuerySystemInformation` API function to gather the Superfetch information about the physical memory pages. It stores a pointer to this information in global variables (`mem_layout_v1_ptr` or `mem_layout_v2_ptr`). Which one is used depends on the version variable which is the argument handed over to the function. In our case, `1` is for calling the function the first time and `2` is for the second time. In other words, it brute-forces whichever version works for the Windows system it is running on.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image47-48-1.png)Figure 46. Superfetch structure and `NtQuerySystemInformation` call.

The `BuildSuperfetchPfnMetadataList` function is quite large and complex. Simplified, it starts by using the `mem_layout` pointer to calculate the total page count.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image49.png)Figure 47. Total Page count algorithm.

It then ends by using `NtQuerySystemInformation` again to get the physical pages and their meta data to store this information in a global vector (`g_PfnVector`).

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image50.png)Figure 48. Superfetch structure.![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image51.png)Figure 49. Build global physical memory list Vector.

Back to the block from the above, the next step blinds the EDRs by deleting their callbacks for certain operations (e.g., process creation, thread creation, and image loading events).

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image52.png)Figure 50. Deleting EDR callbacks.

The `unregister_callbacks` function iterates through a list of over 300 driver names which are stored in the sample.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image53.png)Figure 51. EDR driver name list.![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image54.png)Figure 52. `unregister_callbacks` function.

It also demonstrates the overall implementation of the malware, which is also used in several other functions. It uses a certain API function to calculate an offset to the function or object it is really using — in this case, the kernel callback `cng!CngCreateProcessNotifyRoutine`. It also does not touch this object in the process virtual address space. It uses the driver loaded earlier (“rwdrv.sys”) to get the physical memory address of it. The logic and driver communication is implemented in the `read_phy_bytes` function, and the same for overwriting memory; the `write_to_phy_mem` function is used to handle the driver communications. The `DeviceIoControlImplementation` function which talks to the driver is implemented in `write_to_phy_mem`.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image55.png)Figure 53. `DeviceIoControlImplementation` function called in `write_to_phy_mem`.

The other callback-related functions shown in Figure 44 work similarly to the one we discussed. They overwrite or unregister other EDR-specific callbacks, which were set by the EDR Mini-Filter driver.

The final part of the EDR killer begins by loading another driver (“hlpdrv.sys”).

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image56.png)Figure 54. Load and use of hlpdrv.sys.

The malware uses the driver to terminate EDR processes running on the system using the IOCTL code 0x2222008. This executes the function in the driver which is responsible for unprotecting and terminating the process.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image57.png)Figure 55. Terminate protected process function in hlpdrv.sys.

Once terminated, EDR processes such as Windows Defender no longer run, as demonstrated in Figure 56.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image58.png)Figure 56. Terminated Windows Defender process.

Additionally, it restores the `CiValidateImageHeader` callback. The `RestoreCiValidateImageHeaderCallback` function is shown in Figure 57.

![](https://storage.ghost.io/c/af/a0/afa04ee3-414f-4481-8d23-7e7c146f192e/content/images/2026/03/image59.png)Figure 57. Restoring code integrity checks.

This is accomplished using the same concept we previously saw in Figure 52:

- Resolve a known API function.
- Use this function as an anchor point to locate a specific instruction within its code.
- This instruction contains a pointer in one of its operands that points to, or near, the object of interest.
- Identify the pointer to the target object within that instruction.
- Perform a sign extension on the operand.
- Add an additional offset to compute the final address of the object being sought — in this case, the `CiValidateImageHeader` callback.
- Restore the original function pointer to `CiValidateImageHeader`.

Note that the malware had previously overwritten the callback to `CiValidateImageHeader` with the address of `ArbPreprocessEntry`, a function that always returns true. In other words, it has now restored the original Code Integrity check.

## Summary

This blog was a technical deep dive into the infection chain that is hidden in the malicious “msimg32.dll”, which has been observed during Qilin ransomware attacks. It demonstrates the sophisticated tricks the malware is employing to circumvent or completely disable modern EDR protection features on compromised systems.

It is encouraging to see how many hurdles modern malware must overcome. At the same time, this highlights that even state-of-the-art defense mechanisms can still be bypassed by determined adversaries. Defenders should never rely on a single product for protection; instead, Talos strongly recommends a multi-layered security approach. This significantly increases the difficulty for attackers to remain undetected, even if they manage to evade one line of defense.

## Coverage

The following ClamAV signatures detect and block this threat:

- Win.Malware.Bumblebee-10056548-0
- Win.Tool.EdrKiller-10059833-0
- Win.Tool.ThrottleStop-10059849-0

The following SNORT® rules (SIDs) detect and block this threat:

- Covering Snort2 SID(s): 1:66181, 1:66180
- Covering Snort3 SID(s): 1:301456

## Indicators of compromise (IOCs)

The IOCs for this threat are also available at our GitHub repository [here](https://github.com/Cisco-Talos/IOCs/blob/main/2026/04/overview-of-ransomware-threats-in-japan.txt).

msimg32.dll

MD5: 89ee7235906f7d12737679860264feaf

SHA1: 01d00d3dd8bc8fd92dae9e04d0f076cb3158dc9c

SHA256: 7787da25451f5538766240f4a8a2846d0a589c59391e15f188aa077e8b888497

rwdrv.sys

MD5: 6bc8e3505d9f51368ddf323acb6abc49

SHA1: 82ed942a52cdcf120a8919730e00ba37619661a3

SHA256: 16f83f056177c4ec24c7e99d01ca9d9d6713bd0497eeedb777a3ffefa99c97f0

hlpdrv.sys

cf7cad39407d8cd93135be42b6bd258f

ce1b9909cef820e5281618a7a0099a27a70643dc

bd1f381e5a3db22e88776b7873d4d2835e9a1ec620571d2b1da0c58f81c84a56

EDRKiller.exe (non-fixed memory dump with overlay)

MD5: 1305e8b0f9c459d5ed85e7e474fbebb1

SHA1: 84e2d2084fe08262c2c378a377963a1482b35ac5

SHA256: 12fcde06ddadf1b48a61b12596e6286316fd33e850687fe4153dfd9383f0a4a0

Time stamp: 0x684d33f0 (14. June 2025, 08:33:52 UTC)

ImpHash : 05aa031a007e2f51e3f48ae2ed1e1fcb

TLSH: T1B4647C01B7E50CF9EE77C638C9614A06EA72BC425761DADF43A04A964F237D09E3DB12

##### Share this post

- [Share this on Facebook](https://www.facebook.com/sharer.php?u=https://blog.talosintelligence.com/qilin-edr-killer/ "Share this on Facebook")
- [Post This](https://x.com/share?url=https://blog.talosintelligence.com/qilin-edr-killer/ "Post This")
- [Share this on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https://blog.talosintelligence.com/qilin-edr-killer/ "Share this on LinkedIn")
- [Reddit This](https://www.reddit/submit?url=https://blog.talosintelligence.com/qilin-edr-killer/ "Reddit This")
- [Email This](mailto:?body=Qilin%20EDR%20killer%20infection%20chainhttps://blog.talosintelligence.com/qilin-edr-killer/ "Email This")