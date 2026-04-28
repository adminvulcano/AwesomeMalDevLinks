# https://core-jmp.org/2026/03/crimes-against-ntdll-implementing-early-cascade-injection/

[![Crimes against NTDLL - Implementing Early Cascade Injection](https://core-jmp.org/wp-content/uploads/2026/03/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0-2026-03-14-%D0%B2-15.39.47-300x300.png)](https://core-jmp.org/2026/03/crimes-against-ntdll-implementing-early-cascade-injection/)

March 14, 2026

by[oxfemale](https://core-jmp.org/author/oxfemale/ "View all posts by oxfemale")

withno comment

[attaks](https://core-jmp.org/security/attaks/ "View all posts in attaks") [Bypassing](https://core-jmp.org/security/windows/bypassing/ "View all posts in Bypassing") [EDR](https://core-jmp.org/security/edr/ "View all posts in EDR") [Injection](https://core-jmp.org/security/windows/injection/ "View all posts in Injection") [Rust](https://core-jmp.org/security/rust/ "View all posts in Rust") [winapi](https://core-jmp.org/security/windows/winapi/ "View all posts in winapi") [winapi](https://core-jmp.org/security/winapi-2/ "View all posts in winapi") [windows](https://core-jmp.org/security/windows/ "View all posts in windows")

[Original text](https://fluxsec.red/implementing-early-cascade-injection-rust) by [fluxsec](https://fluxsec.red/)

> _Early Cascade Injection is an advanced process injection technique designed to execute payloads at the earliest stage of Windows process initialization. The method abuses internal components of the Windows loader located in **ntdll.dll**, specifically the Application Compatibility Shim Engine. By modifying undocumented global variables such as **`g_ShimsEnabled`** and the callback pointer **`g_fnSE_DllLoaded`**, an attacker can redirect the loader’s DLL-load callback to attacker-controlled shellcode._
>
> _The attack typically begins by creating a new process in a **suspended state**, injecting the payload into its memory, and patching these shim engine variables. When the process resumes, the Windows loader starts initializing modules and loading system libraries. Because the shim engine callback has been redirected, the injected shellcode executes as part of the legitimate loader workflow._
>
> _This approach is particularly stealthy because it avoids common injection indicators such as **CreateRemoteThread, APC injection, or thread context hijacking**. Instead, the payload runs during normal loader activity, often **before EDR user-mode hooks or monitoring components are initialized**, making the technique significantly harder to detect._

## Intro

You can find this implementation in my [Wyrm C2 framework on GitHub](https://github.com/0xflux/Wyrm/).

Early Cascade Injection was published by [Outflank](https://www.outflank.nl/blog/2024/10/15/introducing-early-cascade-injection-from-windows-process-creation-to-stealthy-injection/) in 2024. Full credit goes to them for discovering the technique – this post deals with the **implementation** of Early Cascade Injection in **Rust**.

I recommend reading Outflank’s blog post – however, as a quick primer, the technique allows for the **loading of fileless malware** in a foreign process without having to perform typical (and heavily monitored) process injection. This is also useful as a primitive to spawn a new sacrificial process for doing things such as **execute-assembly** in the Cobalt Strike world (Wyrm does not implement this yet with a sacrificial process but uses the **dotex** command to run dotnet code in memory).

There are two general buckets for running shellcode in foreign processes (exploits aside):

1. Process injection where the process is already running, or;
2. Spawn and inject, such as Process Hollowing, Early Bird Injection etc.

The problem with these attack surfaces, is they are very well documented and as such, likely to be detected by EDRs.

The clever trick about Early Cascade Injection, is it allows us to have code execution on our shellcode bootstrap **without creating a suspicious thread**, or using **suspicious cross process Asynchronous Procedure Calls** (APC). Instead, we create the process in a suspended state (as is the norm with early process injection techniques), and we surgically tamper with NTDLL before the first usermode thread runs.

When a new process is started, the Windows kernel performs certain actions in order to set up a process, one of those, is mapping NTDLL into memory. Importantly, after the kernel has finished setting up the scaffolding of the process, the thread will then switch into usermode and begin through **ntdll!LdrInitializeThunk**. As Outflank explains, creating a process in a suspended state with the **CREATE\_SUSPENDED** flag, the usermode thread will not run until that thread is resumed.

## The Shim Engine

I am purposefully missing out a lot of detail around how Outflank arrived here – their [blog post](https://www.outflank.nl/blog/2024/10/15/introducing-early-cascade-injection-from-windows-process-creation-to-stealthy-injection/) does an excellent job of talking about the **internals of NTDLL** and **EDR Preloading**.

However, the [Shim Engine](https://techcommunity.microsoft.com/blog/askperf/demystifying-shims---or---using-the-app-compat-toolkit-to-make-your-old-stuff-wo/374947) is a technology implemented in NTDLL which is designed as a compatibility framework intercepting API calls from older applications modifying them to work on newer versions of Windows. The machinery of the engine is implemented in NTDLL, and it is that machinery which Outflank discovered can be abused for process injection.

A global variable internal to NTDLL was discovered called **g\_pfnSE\_DllLoaded**, which is part of the Shim Engine, is a pointer which can be modified by us to point to attacker controlled shellcode. To use this variable, we need to enable a flag named **g\_ShimsEnabled**, which instructs the thread to start performing the Shim Engine routines.

Modifying these two gives us shellcode execution, however, we don’t want the full machinery of the Shim Engine to start running. Outflank chose this variable ( **g\_pfnSE\_DllLoaded**) to abuse as it is the first in a series of pointers that gets dispatched; meaning as soon as we begin executing our stub, we must disable **g\_ShimsEnabled** so that the rest of the Shim Engine doesn’t run.

Finally, in the shellcode stub which runs, we can queue up an APC in the **current thread** which is not nearly as suspicious as cross-process APCs. If you want some info on abusing cross-process APCs, check my blog post on [APC Queue Injection](https://fluxsec.red/apc-queue-injection-rust).

So, the elements we need to make this work are:

1. **Stage 0** – Initiator process (a loader, existing implant, etc) which creates the suspended process.
2. **Stage 1** – Shim engine bootstrap shellcode that gets injected into the suspended process.
3. **Stage 2** – A post-exploitation payload (such as the Wyrm C2 framework).

For the **stage 2** payload, it must be capable of performing **Reflective DLL Injection** at the start address of the queued APC, or your **stage 1** stub needs to set up the post-ex payload.

There is one complication to solve – the variables we need to modify are not exported in any way that we could link against them or somehow call them via FFI. So, how do we manipulate them? Well, the approach I took was simple pattern matching of code which uses these pointers, and then taking the address of the variable in memory. For example, the below byte patterns represent the machine code, and the comments represent the instructions:

```
const G_PFNSE_DLLLOADED_PATTERN: &[u8] = &[\
    0x48, 0x8b, 0x3d, 0xd0, 0xc3, 0x12, 0x00,   // mov  rdi, qword ptr [ntdll!g_pfnSE_DllLoaded (############)]\
    0x83, 0xe0, 0x3f,                           // and  eax, 3Fh\
    0x44, 0x2b, 0xe0,                           // sub  r12d, eax\
    0x8b, 0xc2,                                 // mov  eax, edx\
    0x41, 0x8a, 0xcc                            // mov  cl, r12b\
];

const G_SHIMS_ENABLED_PATTERN: &[u8] = &[\
    0xe8, 0x33, 0x38, 0xf5, 0xff,               // call ntdll!RtlEnterCriticalSection (7ff9ddead780)\
    0x44, 0x38, 0x2d, 0xe4, 0x84, 0x11, 0x00,   // cmp  byte ptr [ntdll!g_ShimsEnabled (7ff9de072438)], r13b\
    0x48, 0x8d, 0x35, 0x95, 0x89, 0x11, 0x00,   // lea  rsi, [ntdll!PebLdr+0x10 (7ff9de0728f0)]\
];
```

Then, using a simple function, we can scan the NTDLL module for these patterns. This is somewhat brittle as these bytes could change between builds of NTDLL. A better approach could be to wildcard the offset bytes and search pattern match on the instructions around that which likely have a better chance at being consistent between patches.

## Implementation

### Stage zero

Ok – lets start with the **stage zero** payload which is the ‘initiator’. This has a few jobs:

1. Create a process in the suspended state.
2. Inject the **stage two** post-ex payload (in this case, **Wyrm**).
3. Position the address of the **stage one** shellcode (which in this case, is included in the injected memory from step 2).
4. Encode the pointer to the shellcode with the cookie found in: **SharedUserData!Cookie** found at the constant address **0x7FFE0330**.
5. Write the 2 pointers in the NTDLL Shim Engine.
6. Resume the thread.

There is very little point in me just doing a copy-paste of the code to implement this, you can see it in the function **early\_cascade\_spawn\_child** in the Wyrm source: [src/spawn\_inject/early\_cascade.rs](https://github.com/0xflux/Wyrm/blob/master/implant/src/spawn_inject/early_cascade.rs). However, I will call out a few important things:

On step 3, I did not write separate shellcode for the bootstrap. Instead, I wrote the bootstrap in **no\_std** Rust meaning it does not rely on the standard library. The result is code that is _sufficiently_ position independent to place in memory and execute directly, effectively behaving like shellcode. This is incredibly ergonomic.

In Wyrm I provide a function called **Shim** which acts as this ‘shellcode bootstrap’ for using Early Cascade Injection, and we will take a look at that code in the **Stage One** section. So, the address we will put into **g\_pfnSE\_DllLoaded**, is the address of the Shim function – allowing the thread to start executing straight up machine code with no dependencies. **Neat!**

The **next thing** to talk about here is having to encode our pointer that we write to **g\_pfnSE\_DllLoaded**. The shim callback pointer is stored in an encoded form, so writing a raw function pointer into **g\_pfnSE\_DllLoaded** will not work. Luckily for us, the key (cookie) used for the encryption is found in **SharedUserData!Cookie**, which is at a constant address (64-bit) of **0x7FFE0330**. So, we can write a function that performs the pointer encryption, returning the encrypted copy of the pointer:

```
fn encode_system_ptr(ptr: *const c_void) -> *const c_void {
    // get pointer cookie from SharedUserData!Cookie (0x330)
    let cookie = unsafe { *(0x7FFE0330 as *const u32) };

    // rotr64
    let ptr_val = ptr as usize;
    let xored = cookie as usize ^ ptr_val;
    let rotated = xored.rotate_right((cookie & 0x3F) as u32);

    rotated as *const c_void
}
```

**Finally**, we want to talk about how to resolve the global variables we wish to write to. As stipulated we are going to pattern match usage of the pointers in NTDLL, to discover their true address based on the offset of where we found it.

To follow through in its entirety, check the source in [shared\_no\_std/src/memory.rs](https://github.com/0xflux/Wyrm/blob/master/shared_no_std/src/memory.rs).

So, we take the two patterns:

```
const G_PFNSE_DLLLOADED_PATTERN: &[u8] = &[\
    0x48, 0x8b, 0x3d, 0xd0, 0xc3, 0x12, 0x00,   // mov  rdi, qword ptr [ntdll!g_pfnSE_DllLoaded (############)]\
    0x83, 0xe0, 0x3f,                           // and  eax, 3Fh\
    0x44, 0x2b, 0xe0,                           // sub  r12d, eax\
    0x8b, 0xc2,                                 // mov  eax, edx\
    0x41, 0x8a, 0xcc                            // mov  cl, r12b\
];

const G_SHIMS_ENABLED_PATTERN: &[u8] = &[\
    0xe8, 0x33, 0x38, 0xf5, 0xff,               // call ntdll!RtlEnterCriticalSection (7ff9ddead780)\
    0x44, 0x38, 0x2d, 0xe4, 0x84, 0x11, 0x00,   // cmp  byte ptr [ntdll!g_ShimsEnabled (7ff9de072438)], r13b\
    0x48, 0x8d, 0x35, 0x95, 0x89, 0x11, 0x00,   // lea  rsi, [ntdll!PebLdr+0x10 (7ff9de0728f0)]\
];
```

And we search for their usage with this simple function where we pass the pattern as the third argument. The first and second args relate to the base address of NTDLL and its size:

```
#[inline(always)]
pub fn scan_module_for_byte_pattern(
    image_base: *const c_void,
    image_size: usize,
    pattern: &[u8],
) -> Result<*const c_void, ()> {
    // Convert the raw address pointer to a byte pointer so we can read individual bytes
    let image_base = image_base as *const u8;
    let mut cursor = image_base as *const u8;
    // End of image denotes the end of our reads, if nothing is found by that point we have not found the
    // sequence of bytes
    let end_of_image = unsafe { image_base.add(image_size) };

    while cursor != end_of_image {
        unsafe {
            let bytes = from_raw_parts(cursor, pattern.len());

            if bytes == pattern {
                return Ok(cursor as *const _);
            }

            cursor = cursor.add(1);
        }
    }

    Err(())
}
```

Then, we need to calculate the difference between the address where we found the start of the machine code, and the offset in the machine code which is where the variable lives:

```
let p_g_pfnse_dll_loaded = unsafe {
    const INSTRUCTION_LEN: isize = 7;

    // Offset by 3 bytes to get the imm, and read the imm as a 4 byte value
    let offset = read_unaligned((p_text_g_pfnse_dll_loaded as *const u8).add(3) as *const i32);
    let offset = offset as isize + INSTRUCTION_LEN;

    (p_text_g_pfnse_dll_loaded as isize + offset) as *mut c_void
};
```

And with that, we can resolve both internal variables addresses! All that is left to do is set **g\_pfnse\_dll\_loaded** to the encrypted address we dealt with earlier, and set **g\_ShimsEnabled** to **1**.

### Stage one

The **stage one** that is capable of being executed by a fresh thread is found in the **Shim** function in [implant/src/stubs/shim.rs](https://github.com/0xflux/Wyrm/blob/master/implant/src/stubs/shim.rs).

Whilst operating here we do have some restrictions – we should also assume **kernel32** and **kernelbase** are not available for use, meaning we are limited to the core library, compiler intrinsics and functions exported in NTDLL. This is fine, we can work with this for what we need.

The stage one has a few duties:

1. Resolve the address of **NtQueueApcThread** so we can launch the **stage two**.
2. Disable the **g\_ShimsEnabled** variable we enabled from stage zero.
3. Queue an APC via **NtQueueApcThread** pointing to the **stage two**.

To resolve the address of **NtQueueApcThread**, I use a variation of my [export-resolver](https://fluxsec.red/export-resolver) crate which I have embedded into Wyrm. In short, this uses [PEB walking](https://fareedfauzi.github.io/2024/07/13/PEB-Walk.html) to resolve the addresses of functions we wish to use. The variation included in Wyrm is **no\_std** compliant such that we can use it in our free standing stub.

Next, we search for **g\_ShimsEnabled** and set it to 0, in exactly the same way shown above. Again – the code I wrote to resolve the addresses is **no\_std**.

Finally, we can call **NtQueueApcThread** to queue an APC at the address of the reflective loader of Wyrm.

In order to use this function, we first must declare its prototype:

```
type NtQueueApcThread = unsafe extern "system" fn(
    thread_handle: isize,
    apc_routine: *const c_void,
    arg1: usize,
    arg2: usize,
    arg3: usize,
) -> u32;
```

And then cast the address we found via the **export-resolver** variant to the type `NtQueueApcThread`:

```
let p_nt_queue_apc_thread = resolve_address("ntdll.dll", "NtQueueApcThread", None);
let NtQueueApcThread = core::mem::transmute::<_, NtQueueApcThread>(p_nt_queue_apc_thread);
```

Then we set up our arguments which go into the function, and call it normally (where **Load** is the name of the function in Wyrm which performs reflective DLL loading):

```
let current_thread = -2isize;
let apc_routine = Load as *const c_void;
let apc_arg1 = 0usize;
let apc_arg2 = 0usize;
let apc_arg3 = 0usize;

NtQueueApcThread(current_thread, apc_routine, apc_arg1, apc_arg2, apc_arg3);
```

The eagle-eyed reader may be wondering how the queued APC is actually run – well, helpfully, when the thread starts executing in NTDLL, after our shim magic has run, NTDLL makes a call to **NtTestAlert** which causes any queued items in the APC queue to dispatch, giving us free execution without having to either wait on a prayer, or call NtTestAlert ourselves.

### Stage two

Finally, our stage two loads – in this case it’s the Wyrm reflective DLL loader. I’m not going into the internals of that here as it’s pretty complex, however you can check the source at: [implant/src/stubs/rdi.rs](https://github.com/0xflux/Wyrm/blob/master/implant/src/stubs/rdi.rs).

## References

- [https://www.outflank.nl/blog/2024/10/15/introducing-early-cascade-injection-from-windows-process-creation-to-stealthy-injection/](https://www.outflank.nl/blog/2024/10/15/introducing-early-cascade-injection-from-windows-process-creation-to-stealthy-injection/)
- [https://ntdoc.m417z.com/ntqueueapcthread](https://ntdoc.m417z.com/ntqueueapcthread)
- [https://github.com/0xNinjaCyclone/EarlyCascade/blob/main/main.c#L82](https://github.com/0xNinjaCyclone/EarlyCascade/blob/main/main.c#L82)
- [https://malwaretech.com/2024/02/bypassing-edrs-with-edr-preload.html](https://malwaretech.com/2024/02/bypassing-edrs-with-edr-preload.html)

### Share this:

- [Share on Facebook (Opens in new window)Facebook](https://core-jmp.org/2026/03/crimes-against-ntdll-implementing-early-cascade-injection/?share=facebook&nb=1)
- [Share on X (Opens in new window)X](https://core-jmp.org/2026/03/crimes-against-ntdll-implementing-early-cascade-injection/?share=x&nb=1)

### Like this:

LikeLoading...

Comments are closed.

Shopping Basket

%d