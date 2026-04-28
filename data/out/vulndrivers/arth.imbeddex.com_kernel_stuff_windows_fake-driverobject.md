# https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/

█

[Skip to main content](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/#__docusaurus_skipToContent_fallback)

On this page

A manually mapped driver without a `DRIVER_OBJECT` is deaf and mute. It can run internal threads and manipulate memory, but it cannot safely interact with standard Windows I/O subsystems. Crafting a structurally perfect fake driver object is the bridge that allows a ghost module to use standard, powerful Windows APIs without crashing the system or triggering immediate detection. This technique is used in my project [YetAnotherReflectiveLoader](https://github.com/Oorth/YetAnotherReflectiveLoader), I have intentionally not uploaded this specific code for security reasons, but we will talk about the logic here in this blog.

C++

IDA Pro

WinDbg

## Setup [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/\#setup "Direct link to Setup")

Everything which we are going to talk about is done on latest Windows and defender versions, which at the time of writing this blog are -

#### Windows OS

- **Edition:** Windows 11 Pro
- **Version:**`25H2`
- **OS Build:**`26200.7840`

#### Defender Engine

- **Client:**`4.18.26010.5`
- **Engine:**`1.1.26010.1`
- **AV / AS:**`1.445.222.0`

#### Environment

Everything is created and built to test modern security with security features:

✓ Real-time protection

✓ Tamper Protection

✓ Memory integrity

✓ Memory access protection

✗ Microsoft Vulnerable Driver Blocklist

Warning

This is some serious work, hence should be used with care and made just for education and research purposes.

## What is a Driver Object [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/\#what-is-a-driver-object "Direct link to What is a Driver Object")

A `DRIVER_OBJECT` is the Windows kernel’s official representation of a loaded driver. Whenever the OS loads a legitimate .sys file into memory, the I/O Manager allocates and initializes this structure to act as the brain for that driver. The `DRIVER_OBJECT` structure looks like:

```cpp
//0x150 bytes (sizeof)
struct _DRIVER_OBJECT
{
    SHORT Type;                                                             //0x0
    SHORT Size;                                                             //0x2
    struct _DEVICE_OBJECT* DeviceObject;                                    //0x8
    ULONG Flags;                                                            //0x10
    VOID* DriverStart;                                                      //0x18
    ULONG DriverSize;                                                       //0x20
    VOID* DriverSection;                                                    //0x28
    struct _DRIVER_EXTENSION* DriverExtension;                              //0x30
    struct _UNICODE_STRING DriverName;                                      //0x38
    struct _UNICODE_STRING* HardwareDatabase;                               //0x48
    struct _FAST_IO_DISPATCH* FastIoDispatch;                               //0x50
    LONG (*DriverInit)(struct _DRIVER_OBJECT* arg1, struct _UNICODE_STRING* arg2); //0x58
    VOID (*DriverStartIo)(struct _DEVICE_OBJECT* arg1, struct _IRP* arg2);  //0x60
    VOID (*DriverUnload)(struct _DRIVER_OBJECT* arg1);                      //0x68
    LONG (*MajorFunction[28])(struct _DEVICE_OBJECT* arg1, struct _IRP* arg2); //0x70
};
```

Microsoft learn also provides a very nice [documentation](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/ns-wdm-_driver_object) EXTERNAL LINK TOhttps://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/ns-wdm-\_driver\_object![Website Preview](https://api.microlink.io/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fwindows-hardware%2Fdrivers%2Fddi%2Fwdm%2Fns-wdm-_driver_object&embed=image.url), which you can have a look at.
The `DRIVER_OBJECT` structure contains dozens of fields, but four primary components dictate how a driver actually interacts with the Windows Operating System:

The Dispatch Table

MajorFunction Array

This is the most important part of the structure. It is an array of up to 28 function pointers (`IRP_MJ_CREATE`, `IRP_MJ_READ`, `IRP_MJ_DEVICE_CONTROL`).

When a user-mode application calls `DeviceIoControl` or `ReadFile`, the Windows I/O Manager packages that request into an **IRP**, looks up this array in the target's `DRIVER_OBJECT`, and jumps to the function pointer registered there.

The Device Anchor

DeviceObject Linked List

A single driver can manage multiple devices (for example, a single disk driver managing three different hard drives).

The `DRIVER_OBJECT` contains a pointer to the very first `DEVICE_OBJECT` it created. Each device then points to the next one, creating a linked list. When the driver is unloaded, the OS uses this list to ensure all child devices are cleanly destroyed.

Lifecycle Management

Routine Pointers

The structure holds pointers to functions that dictate the driver's lifecycle:

• `DriverUnload`: The function the OS calls when it's time to safely remove the driver from memory.

• `DriverStartIo`: Used for serializing hardware I/O requests.

• `AddDevice`: Used heavily by Plug-and-Play (PnP) drivers when new hardware is plugged in.

Identity & Namespace

DriverName String

The structure holds a `UNICODE_STRING` pointing to the driver's location in the Windows Object Manager namespace.

(e.g., `\Driver\kbdclass` or `\Driver\Tcp`).

This is how the OS and other drivers locate it by name.

## Reversing `IoCreateDriver` [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/\#reversing-iocreatedriver "Direct link to reversing-iocreatedriver")

Before making a fake Driver\_Object we must see how the OS does it. For this we can look at `IoCreateDriver` inside IDA

If you want to review the complete, unedited logic of `IoCreateDriver`, you can expand the block below to switch between the raw IDA disassembly and the generated HexRays pseudocode.

Expand to view the complete `MiLockVadTree` function

- IDA Pro Assembly
- HexRays Pseudocode

IoCreateDriver (Assembly)

```nasm
PAGE:0000000140AACA20 ; Exported entry 876. IoCreateDriver
PAGE:0000000140AACA20
PAGE:0000000140AACA20 ; =============== S U B R O U T I N E =======================================
PAGE:0000000140AACA20
PAGE:0000000140AACA20 ; Attributes: bp-based frame fpd=70h
PAGE:0000000140AACA20
PAGE:0000000140AACA20 ; __int64 __fastcall IoCreateDriver(_OWORD *, __int64)
PAGE:0000000140AACA20                 public IoCreateDriver
PAGE:0000000140AACA20 IoCreateDriver  proc near               ; CODE XREF: HaliInitPnpDriver+25↑p
PAGE:0000000140AACA20                                         ; CmpBuildMachineHiveCache+27↑p ...
PAGE:0000000140AACA20
PAGE:0000000140AACA20 Object          = qword ptr -150h
PAGE:0000000140AACA20 HandleInformation= qword ptr -148h
PAGE:0000000140AACA20 var_140         = qword ptr -140h
PAGE:0000000140AACA20 var_138         = dword ptr -138h
PAGE:0000000140AACA20 var_130         = qword ptr -130h
PAGE:0000000140AACA20 var_128         = qword ptr -128h
PAGE:0000000140AACA20 Src             = qword ptr -120h
PAGE:0000000140AACA20 Handle          = qword ptr -110h
PAGE:0000000140AACA20 var_108         = qword ptr -108h
PAGE:0000000140AACA20 var_100         = qword ptr -100h
PAGE:0000000140AACA20 var_F8          = xmmword ptr -0F8h
PAGE:0000000140AACA20 var_E8          = dword ptr -0E8h
PAGE:0000000140AACA20 var_E4          = dword ptr -0E4h
PAGE:0000000140AACA20 var_E0          = qword ptr -0E0h
PAGE:0000000140AACA20 var_D8          = qword ptr -0D8h
PAGE:0000000140AACA20 var_D0          = dword ptr -0D0h
PAGE:0000000140AACA20 var_CC          = dword ptr -0CCh
PAGE:0000000140AACA20 var_C8          = xmmword ptr -0C8h
PAGE:0000000140AACA20 pszDest         = word ptr -0B0h
PAGE:0000000140AACA20 var_30          = qword ptr -30h
PAGE:0000000140AACA20 var_20          = byte ptr -20h
PAGE:0000000140AACA20 arg_10          = qword ptr  20h
PAGE:0000000140AACA20 arg_18          = qword ptr  28h
PAGE:0000000140AACA20
PAGE:0000000140AACA20 ; __unwind { // __GSHandlerCheck
PAGE:0000000140AACA20                 mov     [rsp-8+arg_10], rbx
PAGE:0000000140AACA25                 mov     [rsp-8+arg_18], rsi
PAGE:0000000140AACA2A                 push    rbp
PAGE:0000000140AACA2B                 push    rdi
PAGE:0000000140AACA2C                 push    r12
PAGE:0000000140AACA2E                 push    r14
PAGE:0000000140AACA30                 push    r15
PAGE:0000000140AACA32                 lea     rbp, [rsp-50h]
PAGE:0000000140AACA37                 sub     rsp, 150h
PAGE:0000000140AACA3E                 mov     rax, cs:RtlCopyFromUser_$fo$
PAGE:0000000140AACA45                 xor     rax, rsp
PAGE:0000000140AACA48                 mov     [rbp+70h+var_30], rax
PAGE:0000000140AACA4C                 xor     r15d, r15d
PAGE:0000000140AACA4F                 xorps   xmm0, xmm0
PAGE:0000000140AACA52                 mov     [rbp+70h+var_E4], r15d
PAGE:0000000140AACA56                 xorps   xmm1, xmm1
PAGE:0000000140AACA59                 mov     [rbp+70h+var_CC], r15d
PAGE:0000000140AACA5D                 mov     rsi, rdx
PAGE:0000000140AACA60                 mov     [rsp+170h+var_100], r15
PAGE:0000000140AACA65                 mov     [rsp+170h+Handle], r15
PAGE:0000000140AACA6A                 lea     r12d, [r15+2]
PAGE:0000000140AACA6E                 mov     [rsp+170h+var_108], r15
PAGE:0000000140AACA73                 movups  xmmword ptr [rsp+170h+Src], xmm0
PAGE:0000000140AACA78                 movups  [rsp+170h+var_F8], xmm1
PAGE:0000000140AACA7D                 test    rcx, rcx
PAGE:0000000140AACA80                 jnz     loc_140AACB16
PAGE:0000000140AACA86                 lea     r9d, [r15+1]
PAGE:0000000140AACA8A                 lock xadd cs:IopUniqueDriverObjectNumber, r9d
PAGE:0000000140AACA93                 lea     ebx, [rcx+3Ch]
PAGE:0000000140AACA96                 inc     r9d
PAGE:0000000140AACA99                 mov     edx, ebx        ; cchDest
PAGE:0000000140AACA9B                 lea     r8, aDriver08u  ; "\\Driver\\%08u"
PAGE:0000000140AACAA2                 lea     rcx, [rbp+70h+pszDest] ; pszDest
PAGE:0000000140AACAA6                 call    RtlStringCchPrintfW
PAGE:0000000140AACAAB                 lea     rax, [rbp+70h+pszDest]
PAGE:0000000140AACAAF                 mov     edi, ebx
PAGE:0000000140AACAB1
PAGE:0000000140AACAB1 loc_140AACAB1:                          ; CODE XREF: IoCreateDriver+9E↓j
PAGE:0000000140AACAB1                 cmp     [rax], r15w
PAGE:0000000140AACAB5                 jz      short loc_140AACAC0
PAGE:0000000140AACAB7                 add     rax, r12
PAGE:0000000140AACABA                 sub     rdi, 1
PAGE:0000000140AACABE                 jnz     short loc_140AACAB1
PAGE:0000000140AACAC0
PAGE:0000000140AACAC0 loc_140AACAC0:                          ; CODE XREF: IoCreateDriver+95↑j
PAGE:0000000140AACAC0                 mov     rax, rdi
PAGE:0000000140AACAC3                 mov     rcx, rdi
PAGE:0000000140AACAC6                 neg     rax
PAGE:0000000140AACAC9                 sbb     eax, eax
PAGE:0000000140AACACB                 sub     rbx, rdi
PAGE:0000000140AACACE                 not     eax
PAGE:0000000140AACAD0                 and     eax, 0C000000Dh
PAGE:0000000140AACAD5                 neg     rcx
PAGE:0000000140AACAD8                 sbb     rdx, rdx
PAGE:0000000140AACADB                 and     rdx, rbx
PAGE:0000000140AACADE                 test    rdi, rdi
PAGE:0000000140AACAE1                 jz      loc_140AACD38
PAGE:0000000140AACAE7                 cmp     rdx, 0FFFFh
PAGE:0000000140AACAEE                 jbe     short loc_140AACAFA
PAGE:0000000140AACAF0                 mov     eax, 80000005h
PAGE:0000000140AACAF5                 jmp     loc_140AACD38
PAGE:0000000140AACAFA ; ---------------------------------------------------------------------------
PAGE:0000000140AACAFA
PAGE:0000000140AACAFA loc_140AACAFA:                          ; CODE XREF: IoCreateDriver+CE↑j
PAGE:0000000140AACAFA                 add     dx, dx
PAGE:0000000140AACAFD                 lea     rax, [rbp+70h+pszDest]
PAGE:0000000140AACB01                 mov     word ptr [rsp+170h+Src], dx
PAGE:0000000140AACB06                 add     dx, r12w
PAGE:0000000140AACB0A                 mov     word ptr [rsp+170h+Src+2], dx
PAGE:0000000140AACB0F                 mov     [rsp+170h+Src+8], rax
PAGE:0000000140AACB14                 jmp     short loc_140AACB1F
PAGE:0000000140AACB16 ; ---------------------------------------------------------------------------
PAGE:0000000140AACB16
PAGE:0000000140AACB16 loc_140AACB16:                          ; CODE XREF: IoCreateDriver+60↑j
PAGE:0000000140AACB16                 movups  xmm0, xmmword ptr [rcx]
PAGE:0000000140AACB19                 movdqu  xmmword ptr [rsp+170h+Src], xmm0
PAGE:0000000140AACB1F
PAGE:0000000140AACB1F loc_140AACB1F:                          ; CODE XREF: IoCreateDriver+F4↑j
PAGE:0000000140AACB1F                 mov     rdx, cs:IoDriverObjectType
PAGE:0000000140AACB26                 lea     rax, [rsp+170h+Src]
PAGE:0000000140AACB2B                 mov     [rsp+170h+var_128], r15
PAGE:0000000140AACB30                 lea     r8, [rbp+70h+var_E8]
PAGE:0000000140AACB34                 mov     [rbp+70h+var_D8], rax
PAGE:0000000140AACB38                 xorps   xmm0, xmm0
PAGE:0000000140AACB3B                 lea     rax, [rsp+170h+var_100]
PAGE:0000000140AACB40                 mov     [rbp+70h+var_E8], 30h ; '0'
PAGE:0000000140AACB47                 mov     [rsp+170h+var_130], rax
PAGE:0000000140AACB4C                 mov     edi, 1A8h
PAGE:0000000140AACB51                 mov     [rsp+170h+var_138], r15d
PAGE:0000000140AACB56                 xor     r9d, r9d
PAGE:0000000140AACB59                 mov     dword ptr [rsp+170h+var_140], r15d
PAGE:0000000140AACB5E                 xor     ecx, ecx
PAGE:0000000140AACB60                 mov     dword ptr [rsp+170h+HandleInformation], edi
PAGE:0000000140AACB64                 mov     [rbp+70h+var_E0], r15
PAGE:0000000140AACB68                 mov     [rbp+70h+var_D0], 250h
PAGE:0000000140AACB6F                 movdqu  [rbp+70h+var_C8], xmm0
PAGE:0000000140AACB74                 call    ObCreateObjectEx
PAGE:0000000140AACB79                 test    eax, eax
PAGE:0000000140AACB7B                 js      loc_140AACD38
PAGE:0000000140AACB81                 mov     rbx, [rsp+170h+var_100]
PAGE:0000000140AACB86                 mov     r8d, edi        ; Size
PAGE:0000000140AACB89                 mov     rcx, rbx        ; void *
PAGE:0000000140AACB8C                 xor     edx, edx        ; Val
PAGE:0000000140AACB8E                 call    memset_0
PAGE:0000000140AACB93                 lea     rax, [rbx+150h]
PAGE:0000000140AACB9A                 mov     ecx, 4
PAGE:0000000140AACB9F                 mov     [rbx+30h], rax
PAGE:0000000140AACBA3                 lea     rdi, [rbx+70h]
PAGE:0000000140AACBA7                 mov     [rax], rbx
PAGE:0000000140AACBAA                 lea     rdx, [rsp+170h+var_108]
PAGE:0000000140AACBAF                 mov     dword ptr [rbx], 1500004h
PAGE:0000000140AACBB5                 lea     rax, IopInvalidDeviceRequest
PAGE:0000000140AACBBC                 mov     [rbx+10h], ecx
PAGE:0000000140AACBBF                 mov     ecx, 1Ch
PAGE:0000000140AACBC4                 rep stosq
PAGE:0000000140AACBC7                 mov     rcx, rsi
PAGE:0000000140AACBCA                 mov     [rbx+58h], rsi
PAGE:0000000140AACBCE                 call    RtlPcToFileHeader
PAGE:0000000140AACBD3                 mov     rax, [rsp+170h+var_108]
PAGE:0000000140AACBD8                 mov     ecx, 100h       ; BugCheckParameter3
PAGE:0000000140AACBDD                 mov     [rbx+18h], rax
PAGE:0000000140AACBE1                 mov     r8d, 334E6F49h
PAGE:0000000140AACBE7                 movzx   edx, word ptr [rsp+170h+Src]
PAGE:0000000140AACBEC                 add     rdx, r12
PAGE:0000000140AACBEF                 call    ExAllocatePool2
PAGE:0000000140AACBF4                 mov     qword ptr [rbp+70h+var_F8+8], rax
PAGE:0000000140AACBF8                 mov     r14, rax
PAGE:0000000140AACBFB                 test    rax, rax
PAGE:0000000140AACBFE                 jz      loc_140AACD21
PAGE:0000000140AACC04                 movzx   edx, word ptr [rsp+170h+Src]
PAGE:0000000140AACC09                 mov     word ptr [rsp+170h+var_F8], dx
PAGE:0000000140AACC0E                 mov     edi, edx
PAGE:0000000140AACC10                 mov     r8d, edx        ; Size
PAGE:0000000140AACC13                 lea     ecx, [r12+rdx]
PAGE:0000000140AACC17                 mov     rdx, [rsp+170h+Src+8] ; Src
PAGE:0000000140AACC1C                 mov     word ptr [rsp+170h+var_F8+2], cx
PAGE:0000000140AACC21                 mov     rcx, rax        ; void *
PAGE:0000000140AACC24                 call    memmove
PAGE:0000000140AACC29                 movups  xmm0, [rsp+170h+var_F8]
PAGE:0000000140AACC2E                 xor     r9d, r9d
PAGE:0000000140AACC31                 shr     rdi, 1
PAGE:0000000140AACC34                 xor     edx, edx        ; AccessState
PAGE:0000000140AACC36                 mov     rcx, rbx        ; Object
PAGE:0000000140AACC39                 mov     [r14+rdi*2], r15w
PAGE:0000000140AACC3E                 lea     r8d, [r9+1]
PAGE:0000000140AACC42                 mov     rax, [rbx+30h]
PAGE:0000000140AACC46                 movdqu  xmmword ptr [rax+18h], xmm0
PAGE:0000000140AACC4B                 lea     rax, [rsp+170h+Handle]
PAGE:0000000140AACC50                 mov     [rsp+170h+var_140], rax ; __int64
PAGE:0000000140AACC55                 mov     [rsp+170h+HandleInformation], r15 ; __int64
PAGE:0000000140AACC5A                 mov     dword ptr [rsp+170h+Object], r15d ; int
PAGE:0000000140AACC5F                 call    ObInsertObjectEx
PAGE:0000000140AACC64                 mov     edi, eax
PAGE:0000000140AACC66                 test    eax, eax
PAGE:0000000140AACC68                 js      loc_140AACD36
PAGE:0000000140AACC6E                 mov     r8, cs:IoDriverObjectType ; ObjectType
PAGE:0000000140AACC75                 lea     rax, [rsp+170h+var_108]
PAGE:0000000140AACC7A                 mov     rcx, [rsp+170h+Handle] ; Handle
PAGE:0000000140AACC7F                 xor     r9d, r9d        ; AccessMode
PAGE:0000000140AACC82                 mov     [rsp+170h+HandleInformation], r15 ; HandleInformation
PAGE:0000000140AACC87                 xor     edx, edx        ; DesiredAccess
PAGE:0000000140AACC89                 mov     [rsp+170h+Object], rax ; Object
PAGE:0000000140AACC8E                 mov     [rsp+170h+var_108], r15
PAGE:0000000140AACC93                 call    ObReferenceObjectByHandle
PAGE:0000000140AACC98                 mov     rbx, [rsp+170h+var_108]
PAGE:0000000140AACC9D                 mov     edi, eax
PAGE:0000000140AACC9F                 mov     rcx, [rsp+170h+Handle] ; Handle
PAGE:0000000140AACCA4                 test    eax, eax
PAGE:0000000140AACCA6                 jns     short loc_140AACCB9
PAGE:0000000140AACCA8                 call    ZwMakeTemporaryObject
PAGE:0000000140AACCAD                 mov     rcx, [rsp+170h+Handle] ; Handle
PAGE:0000000140AACCB2                 call    ZwClose
PAGE:0000000140AACCB7                 jmp     short loc_140AACD36
PAGE:0000000140AACCB9 ; ---------------------------------------------------------------------------
PAGE:0000000140AACCB9
PAGE:0000000140AACCB9 loc_140AACCB9:                          ; CODE XREF: IoCreateDriver+286↑j
PAGE:0000000140AACCB9                 call    ZwClose
PAGE:0000000140AACCBE                 movzx   edx, word ptr [rsp+170h+Src+2]
PAGE:0000000140AACCC3                 mov     ecx, 40h ; '@'  ; BugCheckParameter3
PAGE:0000000140AACCC8                 mov     r8d, 334E6F49h
PAGE:0000000140AACCCE                 call    ExAllocatePool2
PAGE:0000000140AACCD3                 mov     [rbx+40h], rax
PAGE:0000000140AACCD7                 test    rax, rax
PAGE:0000000140AACCDA                 jz      short loc_140AACD02
PAGE:0000000140AACCDC                 movzx   eax, word ptr [rsp+170h+Src+2]
PAGE:0000000140AACCE1                 mov     [rbx+3Ah], ax
PAGE:0000000140AACCE5                 movzx   eax, word ptr [rsp+170h+Src]
PAGE:0000000140AACCEA                 mov     [rbx+38h], ax
PAGE:0000000140AACCEE                 movzx   r8d, word ptr [rsp+170h+Src+2] ; Size
PAGE:0000000140AACCF4                 mov     rdx, [rsp+170h+Src+8] ; Src
PAGE:0000000140AACCF9                 mov     rcx, [rbx+40h]  ; void *
PAGE:0000000140AACCFD                 call    memmove
PAGE:0000000140AACD02
PAGE:0000000140AACD02 loc_140AACD02:                          ; CODE XREF: IoCreateDriver+2BA↑j
PAGE:0000000140AACD02                 xor     edx, edx
PAGE:0000000140AACD04                 mov     rcx, rbx
PAGE:0000000140AACD07                 mov     rax, rsi
PAGE:0000000140AACD0A                 call    _guard_dispatch_icall_no_overrides
PAGE:0000000140AACD0F                 mov     edi, eax
PAGE:0000000140AACD11                 test    eax, eax
PAGE:0000000140AACD13                 js      short loc_140AACD26
PAGE:0000000140AACD15                 lea     rcx, [rsp+170h+Src]
PAGE:0000000140AACD1A                 call    EtwTiLogDriverObjectLoad
PAGE:0000000140AACD1F                 jmp     short loc_140AACD36
PAGE:0000000140AACD21 ; ---------------------------------------------------------------------------
PAGE:0000000140AACD21
PAGE:0000000140AACD21 loc_140AACD21:                          ; CODE XREF: IoCreateDriver+1DE↑j
PAGE:0000000140AACD21                 mov     edi, 0C000009Ah
PAGE:0000000140AACD26
PAGE:0000000140AACD26 loc_140AACD26:                          ; CODE XREF: IoCreateDriver+2F3↑j
PAGE:0000000140AACD26                 mov     rcx, rbx        ; Object
PAGE:0000000140AACD29                 call    ObMakeTemporaryObject
PAGE:0000000140AACD2E                 mov     rcx, rbx        ; Object
PAGE:0000000140AACD31                 call    ObfDereferenceObject
PAGE:0000000140AACD36
PAGE:0000000140AACD36 loc_140AACD36:                          ; CODE XREF: IoCreateDriver+248↑j
PAGE:0000000140AACD36                                         ; IoCreateDriver+297↑j ...
PAGE:0000000140AACD36                 mov     eax, edi
PAGE:0000000140AACD38
PAGE:0000000140AACD38 loc_140AACD38:                          ; CODE XREF: IoCreateDriver+C1↑j
PAGE:0000000140AACD38                                         ; IoCreateDriver+D5↑j ...
PAGE:0000000140AACD38                 mov     rcx, [rbp+70h+var_30]
PAGE:0000000140AACD3C                 xor     rcx, rsp        ; StackCookie
PAGE:0000000140AACD3F                 call    __security_check_cookie
PAGE:0000000140AACD44                 lea     r11, [rsp+170h+var_20]
PAGE:0000000140AACD4C                 mov     rbx, [r11+40h]
PAGE:0000000140AACD50                 mov     rsi, [r11+48h]
PAGE:0000000140AACD54                 mov     rsp, r11
PAGE:0000000140AACD57                 pop     r15
PAGE:0000000140AACD59                 pop     r14
PAGE:0000000140AACD5B                 pop     r12
PAGE:0000000140AACD5D                 pop     rdi
PAGE:0000000140AACD5E                 pop     rbp
PAGE:0000000140AACD5F                 retn
PAGE:0000000140AACD5F ; ---------------------------------------------------------------------------
PAGE:0000000140AACD60                 db 0CCh
PAGE:0000000140AACD60 ; } // starts at 140AACA20
PAGE:0000000140AACD60 IoCreateDriver  endp
```

IoCreateDriver (Decompiled)

```cpp
__int64 __fastcall IoCreateDriver(_OWORD *a1, __int64 a2)
{
  wchar_t *v3; // rax
  __int64 v4; // rdi
  __int64 result; // rax
  unsigned __int64 v6; // rdx
  char *v7; // rbx
  _WORD *Pool2; // rax
  _WORD *v9; // r14
  unsigned __int64 v10; // rdi
  __int128 v11; // xmm0
  int inserted; // edi
  NTSTATUS v13; // eax
  __int64 v14; // rax
  __int64 v15; // r8
  __int64 v16; // r9
  void *Src[2]; // [rsp+50h] [rbp-B0h] BYREF
  HANDLE Handle; // [rsp+60h] [rbp-A0h] BYREF
  PVOID Object; // [rsp+68h] [rbp-98h] BYREF
  PVOID v20; // [rsp+70h] [rbp-90h]
  __int128 v21; // [rsp+78h] [rbp-88h]
  _DWORD v22[2]; // [rsp+88h] [rbp-78h] BYREF
  __int64 v23; // [rsp+90h] [rbp-70h]
  void **v24; // [rsp+98h] [rbp-68h]
  int v25; // [rsp+A0h] [rbp-60h]
  int v26; // [rsp+A4h] [rbp-5Ch]
  __int128 v27; // [rsp+A8h] [rbp-58h]
  wchar_t pszDest[64]; // [rsp+C0h] [rbp-40h] BYREF

  v22[1] = 0;
  v26 = 0;
  v20 = 0LL;
  Handle = 0LL;
  Object = 0LL;
  *(_OWORD *)Src = 0LL;
  v21 = 0LL;
  if ( a1 )
  {
    *(_OWORD *)Src = *a1;
    goto LABEL_10;
  }
  RtlStringCchPrintfW(
    pszDest,
    0x3CuLL,
    L"\\Driver\\%08u",
    (unsigned int)_InterlockedIncrement(&IopUniqueDriverObjectNumber));
  v3 = pszDest;
  v4 = 60LL;
  do
  {
    if ( !*v3 )
      break;
    ++v3;
    --v4;
  }
  while ( v4 );
  result = v4 == 0 ? 0xC000000D : 0;
  v6 = (60 - v4) & -(__int64)(v4 != 0);
  if ( v4 )
  {
    if ( v6 > 0xFFFF )
      return 2147483653LL;
    LOWORD(Src[0]) = 2 * v6;
    WORD1(Src[0]) = 2 * v6 + 2;
    Src[1] = pszDest;
LABEL_10:
    v24 = Src;
    v22[0] = 48;
    v23 = 0LL;
    v25 = 592;
    v27 = 0LL;
    result = ObCreateObjectEx(0, (_DWORD)IoDriverObjectType, (unsigned int)v22, 0);
    if ( (int)result < 0 )
      return result;
    v7 = (char *)v20;
    memset_0(v20, 0, 0x1A8uLL);
    *((_QWORD *)v7 + 6) = v7 + 336;
    *((_QWORD *)v7 + 42) = v7;
    *(_DWORD *)v7 = 0x1500004;
    *((_DWORD *)v7 + 4) = 4;
    memset64(v7 + 112, (unsigned __int64)&IopInvalidDeviceRequest, 0x1CuLL);
    *((_QWORD *)v7 + 11) = a2;
    RtlPcToFileHeader(a2, &Object);
    *((_QWORD *)v7 + 3) = Object;
    Pool2 = (_WORD *)ExAllocatePool2(0x100uLL);
    *((_QWORD *)&v21 + 1) = Pool2;
    v9 = Pool2;
    if ( Pool2 )
    {
      LOWORD(v21) = Src[0];
      v10 = LOWORD(Src[0]);
      WORD1(v21) = LOWORD(Src[0]) + 2;
      memmove(Pool2, Src[1], LOWORD(Src[0]));
      v11 = v21;
      v9[v10 >> 1] = 0;
      *(_OWORD *)(*((_QWORD *)v7 + 6) + 24LL) = v11;
      inserted = ObInsertObjectEx(v7, 0LL, 0, 0LL, (__int64)&Handle);
      if ( inserted < 0 )
        return (unsigned int)inserted;
      Object = 0LL;
      v13 = ObReferenceObjectByHandle(Handle, 0, IoDriverObjectType, 0, &Object, 0LL);
      v7 = (char *)Object;
      inserted = v13;
      if ( v13 < 0 )
      {
        ZwMakeTemporaryObject(Handle);
        ZwClose(Handle);
        return (unsigned int)inserted;
      }
      ZwClose(Handle);
      v14 = ExAllocatePool2(0x40uLL);
      *((_QWORD *)v7 + 8) = v14;
      if ( v14 )
      {
        *((_DWORD *)v7 + 14) = Src[0];
        memmove(*((void **)v7 + 8), Src[1], WORD1(Src[0]));
      }
      inserted = guard_dispatch_icall_no_overrides(v7, 0LL, v15, v16);
      if ( inserted >= 0 )
      {
        EtwTiLogDriverObjectLoad(Src);
        return (unsigned int)inserted;
      }
    }
    else
    {
      inserted = -1073741670;
    }
    ObMakeTemporaryObject(v7);
    ObfDereferenceObject(v7);
    return (unsigned int)inserted;
  }
  return result;
}
```

### `ObCreateObject` parameters [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/\#obcreateobject-parameters "Direct link to obcreateobject-parameters")

To start our analysis, we will need to find how the OS allocates memory for the `DRIVER_OBJECT`. For this lets look at how `ObCreateObjectEx` is called:

```nasm
PAGE:0000000140AACB1F loc_140AACB1F:                 ; CODE XREF: IoCreateDriver+F4↑j
PAGE:0000000140AACB1F             mov     rdx, cs:IoDriverObjectType
PAGE:0000000140AACB26             lea     rax, [rsp+170h+Src]
PAGE:0000000140AACB2B             mov     [rsp+170h+var_128], r15
PAGE:0000000140AACB30             lea     r8, [rbp+70h+var_E8]
PAGE:0000000140AACB34             mov     [rbp+70h+var_D8], rax
PAGE:0000000140AACB38             xorps   xmm0, xmm0
PAGE:0000000140AACB3B             lea     rax, [rsp+170h+var_100]
PAGE:0000000140AACB40             mov     [rbp+70h+var_E8], 30h ; '0'
PAGE:0000000140AACB47             mov     [rsp+170h+var_130], rax
PAGE:0000000140AACB4C             mov     edi, 1A8h
PAGE:0000000140AACB51             mov     [rsp+170h+var_138], r15d
PAGE:0000000140AACB56             xor     r9d, r9d
PAGE:0000000140AACB59             mov     dword ptr [rsp+170h+var_140], r15d
PAGE:0000000140AACB5E             xor     ecx, ecx
PAGE:0000000140AACB60             mov     dword ptr [rsp+170h+HandleInformation], edi
PAGE:0000000140AACB64             mov     [rbp+70h+var_E0], r15
PAGE:0000000140AACB68             mov     [rbp+70h+var_D0], 250h
PAGE:0000000140AACB6F             movdqu  [rbp+70h+var_C8], xmm0
PAGE:0000000140AACB74             call    ObCreateObjectEx
```

In x64 assembly, the first four arguments go into `RCX`, `RDX`, `R8`, `R9`, and the remaining arguments are pushed to the Stack (RSP) starting at offset \[`rsp+20h`\]. Lets look at the parameters

Assembly TraceParameter Analysis

Arg 1: RCX (ProbeMode)

xor ecx, ecx

`ecx` (the lower 32 bits of `rcx`) is zeroed out.

`0` equals **KernelMode**.

Arg 2: RDX (ObjectType)

mov rdx, cs:IoDriverObjectType

Loads the global pointer for the Driver Object Type into `rdx`.

Arg 3: R8 (ObjectAttributes)

lea r8,\[rbp+70h+var\_E8\]

Loads the address of the local `OBJECT_ATTRIBUTES` structure into `r8`.

Arg 4: R9 (Ownership)

xor r9d, r9d

`r9` is completely zeroed out.

\-\-\- FASTCALL REGISTERS EXHAUSTED. MOVING TO STACK ---

Arg 6: Stack (ObjectBodySize)

mov edi, 1A8h

movdword ptr \[rsp+170h+...\], edi

**The Size:**`0x1A8` is 424 in decimal. It loads it into `edi`, and then pushes it onto the stack space for the 6th argument.

Arg 9: Stack (OUT Object)

lea rax,\[rsp+170h+var\_100\]

mov\[rsp+170h+var\_130\], rax

**The v20:**`var_100` is the `v20` in the pseudocode. The `lea` instruction grabs its address, puts it in `rax`, and then moves it onto the stack as the 9th argument.

From this we can see the function allocates a block of size `0x1A8` Bytes which is a big clue. In WinDg checking for sizes of `DRIVER_OBJECT` and `DRIVER_EXTENSION` it reveals:

![DriverObject_DriverExtension_size](https://arth.imbeddex.com/img/FakeDriverObject/DriverObject_DriverExtension_size.png)

`_Driver_Object` and `_Driver_Extension` sizes

We can see that Size of `_Driver_Object` is `0x150` bytes and `_Driver_Extension` is `0x58` bytes and both together `0x150 + 0x58 = 0x1A8` which is exactly what the `ObCreateObjectEx` uses.

### `DRIVER_EXTENSION` initialization [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/\#driver_extension-initialization "Direct link to driver_extension-initialization")

Our Findings are verified again by looking at the Pseudocode of `IoCreateDriver` further:

IoCreateDriver Pseudocode

```cpp
    v7 = (char *)v20;
    memset_0(v20, 0, 0x1A8uLL);
```

Here, the OS zeros out `0x1A8` bytes. So, we do know that the OS allocated `DRIVER_OBJECT` and `DRIVER_EXTENSION` as one contiguous chunk. Further looking at the pseudocode, we can see the OS interacting with the `_DRIVER_EXTENSION`

IoCreateDriver Pseudocode

```cpp
// The Pointer Math (DriverExtension)
*((_QWORD *)v7 + 6) = v7 + 0x150;
```

`v7` is cast as a 64-bit pointer (`_QWORD*`), so adding 6 moves the offset by `6 * 8 = 48 bytes (0x30)`. Offset `0x30` in a `DRIVER_OBJECT` is the DriverExtension pointer, which we can actually see:

struct\_DRIVER\_EXTENSION

```cpp
//0x28 bytes (sizeof)
struct _DRIVER_EXTENSION
{
    struct _DRIVER_OBJECT* DriverObject;                                    //0x0
    LONG (*AddDevice)(struct _DRIVER_OBJECT* arg1, struct _DEVICE_OBJECT* arg2); //0x8
    ULONG Count;                                                            //0x10
    struct _UNICODE_STRING ServiceKeyName;                                  //0x18
};
```

and `v7 + 0x150` is the base address plus the exact size of the `DRIVER_OBJECT`. Which means `DRIVER_EXTENSION` sits just below the `DRIVER_OBJECT` yet another confirmation. We can also see the OS setting up a back pointer to the `_DRIVER_OBJECT` here:

IoCreateDriver Pseudocode

```cpp
// The Back-Pointer
*((_QWORD *)v7 + 42) = v7;
```

Adding 42 to a `_QWORD*` moves the offset by `42 * 8 = 336 bytes (0x150)` and what is at offset `0x150` The very first member of `DRIVER_EXTENSION` which is `struct _DRIVER_OBJECT* DriverObject;` the back-pointer.

### `Type` and `Size` Initialization [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/\#type-and-size-initialization "Direct link to type-and-size-initialization")

The decompiler shows this strange line of code:

```cpp
*(_DWORD *)v7 = 0x1500004;
```

This is a classic compiler optimization trick. Offset `0` of the `DRIVER_OBJECT` struct holds two consecutive 16-bit (`SHORT`) values: `Type` and `Size`. Instead of writing them separately, the compiler packed them into a single 32-bit `DWORD` write using **Little-Endian** formatting.

Memory Bit-Packing
0x01500004

01 50Upper 16-bits

00 04Lower 16-bits

↓

↓

DriverObject->Size336 bytes

DriverObject->Type4 (IO\_TYPE\_DRIVER)

## The `IoDriverObjectType` [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/\#the-iodriverobjecttype "Direct link to the-iodriverobjecttype")

In the Windows kernel, `IoDriverObjectType` is an exported global variable which points to an `_OBJECT_TYPE` structure.

THE OOP ANALOGY:

Think of the Windows Kernel in terms of Object-Oriented Programming. An `*ObjectType` variable (like `IoDriverObjectType` or `PsThreadType`) acts as a **Class Definition**.

The Object Manager needs these "Class Blueprints" to know exactly what kind of **Instance** it is dealing with, how to secure it, and how to safely destroy it. By passing `IoDriverObjectType` into `ObCreateObject`, we are giving the Object Manager the blueprint it needs to work with this raw memory.

`IoDriverObjectType` is am exported variable which we can verify in ida:

![Exported_IoDriverObjectType](https://arth.imbeddex.com/img/FakeDriverObject/Exported_IoDriverObjectType.png)

IoDriverObjectType Variable

As it is a globally exported variable we can me the compiler statically link it to our driver but this will leave a suspicious looking import in our Driver's PE.

```cpp
extern POBJECT_TYPE IoDriverObjectType;
```

### Dynamic Resolution [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/\#dynamic-resolution "Direct link to Dynamic Resolution")

We can dynamically resolve `IoDriverObjectType` by looking at another loaded driver, specifically by targeting a built-in Windows device that is guaranteed to always be present, such as `\Device\Tcp`.

Step 1Get device object pointer

ResolveIoDriverObjectType.cpp

```cpp
PDEVICE_OBJECT pTcpDeviceObject = NULL;

UNICODE_STRING tcpDeviceName;
RtlInitUnicodeString(&tcpDeviceName, L"\\Device\\Tcp");

// Get the device object pointer
PFILE_OBJECT pTcpFileObject = NULL;
status = IoGetDeviceObjectPointer(&tcpDeviceName, FILE_ANY_ACCESS, &pTcpFileObject, &pTcpDeviceObject);
if(!NT_SUCCESS(status))
{
  LOG_W("[ResolveIoDriverObjectType] [-] Failed to get TCP device object pointer: 0x%X\n", status);
  return nullptr;
}
```

`IoGetDeviceObjectPointer` doesn't just return the device object; it returns a FILE\_OBJECT representing our open handle to the device, and a pointer to the target DEVICE\_OBJECT itself.

Step 2Get Driver Object

ResolveIoDriverObjectType.cpp

```cpp
// Get the driver object pointer
PDRIVER_OBJECT pTcpDriverObject = pTcpDeviceObject->DriverObject;
if(!pTcpDriverObject)
{
  LOG_W("[ResolveIoDriverObjectType] [-] TCP device has a NULL driver object.\n");

  ObDereferenceObject(pTcpFileObject);
  return nullptr;
}
```

Once we have the TCP device object, we simply dereference it to find its master driver object

Step 3Query the Object Manager

ResolveIoDriverObjectType.cpp

```cpp
POBJECT_TYPE pDriverObjectType = pObGetObjectType(pTcpDriverObject);
if(!pDriverObjectType)
{
  LOG_W("[ResolveIoDriverObjectType] [-] pIoDriverObjectType is 0x%p\n", pDriverObjectType);

  ObDereferenceObject(pTcpFileObject);
  return nullptr;
}
```

The Object Manager looks at the object header of the TCP driver, extracts the pointer to its class definition (`IoDriverObjectType`), and hands it right back to us.

Step 4Cleanup

ResolveIoDriverObjectType.cpp

```cpp
ObDereferenceObject(pTcpFileObject);
```

Because `IoGetDeviceObjectPointer` increments the reference count on the `FILE_OBJECT` we must call `ObDereferenceObject` when we are done. If we don't, we cause a memory leak and prevent the TCP driver from ever cleanly unloading.

## Finally [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/\#finally "Direct link to Finally")

Now we have all the stuff that is required to make ourselves a fake `DriverObject` which the OS will have no issues interacting with. We now know how the OS creates a driver using `IoCreateDriver` how it uses ObCreateObject to create `DriverObject` a and whatever it does with the `_DRIVER_EXTENSION` structure, and the initializations. We will replicate the behaviour of ` IoCreateDriver`.

### Create `DriverObject` [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/\#create-driverobject "Direct link to create-driverobject")

We begin by setting up an `OBJECT_ATTRIBUTES` structure. By providing `NULL` for the name and specifying the `OBJ_KERNEL_HANDLE` flag, we ensure our driver object remains anonymous (invisible to standard namespace directory queries) and strictly isolated from user-mode access.

```cpp
OBJECT_ATTRIBUTES objAttributes;
InitializeObjectAttributes(&objAttributes, NULL, OBJ_KERNEL_HANDLE, NULL, NULL);

PDRIVER_OBJECT pFakeDriverObject = nullptr;

NTSTATUS status = pObCreateObject(KernelMode, pDriverObjectType, &objAttributes, KernelMode, (PVOID)NULL, sizeof(_DRIVER_OBJECT) + sizeof(_DRIVER_EXTENSION), 0, 0, (PVOID*)&pFakeDriverObject);
if(!NT_SUCCESS(status) || pFakeDriverObject == NULL)
{
  LOG_W("[CreateFakeDriverObject] [-] ObCreateObject failed. Status: 0x%X\n", status);
  return nullptr;
}
```

By passing `sizeof(_DRIVER_OBJECT) + sizeof(_DRIVER_EXTENSION)`, we are mathematically replicating the exact `0x1A8` (424 byte) size we uncovered during our assembly trace of `IoCreateDriver`

### Setup `Type` and `Size` [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/\#setup-type-and-size "Direct link to setup-type-and-size")

We saw `IoCreateDriver` setting up the Type and Size fields inside the `_DRIVER_OBJECT` structure, So we do the same which is very simple:

```cpp
pFakeDriverObject->Type = 4; // 4 == IO_TYPE_DRIVER
pFakeDriverObject->Size = sizeof(_DRIVER_OBJECT);
```

### Setup `_DRIVER_EXTENSION` [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/\#setup-_driver_extension "Direct link to setup-_driver_extension")

And Inside the `_DRIVER_EXTENSION` structure we need to populate the backpointer

```cpp
pFakeDriverObject->DriverExtension = (PDRIVER_EXTENSION)(pFakeDriverObject + 1);

RtlZeroMemory(pFakeDriverObject->DriverExtension, sizeof(DRIVER_EXTENSION));
pFakeDriverObject->DriverExtension->DriverObject = pFakeDriverObject;
```

POINTER MATH TRICK

We set the extension pointer using `pFakeDriverObject + 1`. Because `pFakeDriverObject` is typed as a `PDRIVER_OBJECT`, adding `1` tells the C++ compiler to physically jump forward in memory by exactly `sizeof(DRIVER_OBJECT)` bytes

We do this because when we reverse engineered `IoCreateDriver` earlier, we saw that the OS allocates the `DRIVER_OBJECT` and the `DRIVER_EXTENSION` together as one massive, contiguous chunk of memory.

## The End [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/\#the-end "Direct link to The End")

We have successfully reverse engineered the Windows Kernel and forged a completely independent `DRIVER_OBJECT` from scratch.
Until next time, keep testing boundaries and stay stealthy.

## References [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/\#references "Direct link to References")

[![icon](https://www.google.com/s2/favicons?domain=learn.microsoft.com&sz=64)\\
\\
DRIVER\_OBJECT structuremicrosoft\\
\\
›](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/ns-wdm-_driver_object) [![icon](https://www.google.com/s2/favicons?domain=osr.com&sz=64)\\
\\
ObCreateObjectosr\\
\\
›](https://community.osr.com/t/obcreateobject/1569) [![icon](https://www.google.com/s2/favicons?domain=j00ru.vexillium.org&sz=64)\\
\\
Fun facts: Windows kernel and Device Extension Sizej00ru\\
\\
›](https://j00ru.vexillium.org/2012/09/fun-facts-windows-kernel-and-device-extension-size/)

- [Setup](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/#setup)
- [What is a Driver Object](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/#what-is-a-driver-object)
- [Reversing `IoCreateDriver`](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/#reversing-iocreatedriver)
  - [`ObCreateObject` parameters](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/#obcreateobject-parameters)
  - [`DRIVER_EXTENSION` initialization](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/#driver_extension-initialization)
  - [`Type` and `Size` Initialization](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/#type-and-size-initialization)
- [The `IoDriverObjectType`](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/#the-iodriverobjecttype)
  - [Dynamic Resolution](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/#dynamic-resolution)
- [Finally](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/#finally)
  - [Create `DriverObject`](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/#create-driverobject)
  - [Setup `Type` and `Size`](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/#setup-type-and-size)
  - [Setup `_DRIVER_EXTENSION`](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/#setup-_driver_extension)
- [The End](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/#the-end)
- [References](https://arth.imbeddex.com/Kernel_stuff/Windows/Fake-DriverObject/#references)

VISITOR

\[CONNECTED\] \_

Your IP: 194.26.202.98\|LOC: Centreville, US\|ISP: Cox Communications Inc.\|CPU: 32 Cores\|RAM: 8Gb\|PWR: 100% \[Charging\]\|DOC: \[==========\]   0%\|00:00:00