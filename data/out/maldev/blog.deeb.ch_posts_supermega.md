# https://blog.deeb.ch/posts/supermega/

# Supermega

A shellcode loader laboratory for RedTeaming to experiment bypassing EDR.

## Intro

I needed a framework to implement my EXE-Injection technique
Cordyceps. It should be able to:

- Have a list of **input shellcodes** (e.g. start calc, show MessageBox start CobaltStrike)
- Have a list of **input EXE’s**
- Different **loader implementations** with individual techniques
- Allows rapid prototyping, development, and testing

The solution was to use [From C Project, through assembly, to shellcode](https://github.com/vxunderground/VXUG-Papers/blob/main/From%20a%20C%20project%20through%20assembly%20to%20shellcode.pdf) by hasharezade, for Vxunderground

This blog article focuses on the function of SuperMega, without going
too much into details of Cordyceps. Cordyceps attempts to integrate the
payload as much as possible into nonmalicious EXE .text section to thwart detection.

This is part of a three article series:

- [Supermega](https://blog.deeb.ch/posts/supermega) for an introduction on how to use the SuperMega loader laboratory (this)
- See [How EDR works](https://blog.deeb.ch/posts/how-edr_works) for a discussion of EDR detection principles
- See [Cordyceps EXE Injection](https://blog.deeb.ch/posts/exe-injection) for a discussion of Cordyceps approaches

I published the source code at [github.com/dobin/SuperMega](https://github.com/dobin/SuperMega).

## SuperMega Cordyceps injection

Cordyceps injects shellcode into an existing executable.

```
                  Injectable EXE
                  ┌─────────────┐
                  │             │
Shellcode         │             │
┌───────┐         │             │
│       │         │             │
│       ├────────►│             │
│       │         │             │
└───────┘         │             │
                  │             │
                  └─────────────┘
```

The input is a Payload (Shellcode, like CobaltStrike), and a non-malicious EXE file. The payload will be inserted somewhere in the injectable exe, and executed by the carrier (loader). The carrier is located somewhere in the .text section.

There are many techniques and options on where to insert the payload
and carrier, and how the carrier
loads, decodes (decrypt), and invokes the payload.

Here the carrier is injected into .text, and the payload into .rdata. The carrier
references the payload:

```
                        Injectable EXE
┌───────────┐           ┌─────────────┐
│           │           │             │
│ Carrier   ├──────────►│  .text      │
│           │           │             │
└────┬──────┘           │             │
     │                  │             │
┌────▼──────┐           │             │
│           │           │             │
│           │           │             │
│ Payload   ├──────────►│  .rdata     │
│           │           │             │
│           │           │             │
└───────────┘           │             │
                        └─────────────┘
```

## The GUI

![SuperMega GUI](https://blog.deeb.ch/supermega/supermega-gui.png)

After selecting all the options, click “Build” to generate the infected executable.

Once the infected exe is generated, it can be started locally
by clicking “Start”. If a avred-server is configured, it can
be executed remotely on that server instead (e.g. with an enabled, or different, EDR).

## Compile C To Shellcode

The document “From C Project, through assembly, to shellcode” explains how to generate shellcode from C source code.
It involves several steps:

- Write C code “normally”
- Compile that C into assembler-text
- Modify the assembler-text
  - Fixup string references
  - Clean / remove all external dependencies
- Assemble modified assembler-text into an EXE
- Extract the .code section from the EXE
- Result is a runnable shellcode

```
┌───────────┐   ┌──────────┐   ┌───────────┐   ┌──────────┐   ┌───────────┐   ┌────────────┐
│  .C       │   │ .C       │   │ .ASM      │   │ .ASM     │   │ .EXE      │   │ .BIN       │
│  Loader   │   │ Loader   │   │ Loader    │   │ Loader   │   │ .text     │   │ Shellcode  │
│           ├──►│          ├──►│           ├──►│          ├──►│           ├──►│            │
│  Template │   │ Rendered │   │ Assembled │   │ Cleaned  │   │ Compiled  │   │ Shellcode  │
│           │   │          │   │           │   │ Fixed    │   │           │   │            │
└───────────┘   └──────────┘   └───────────┘   └──────────┘   └───────────┘   └────────────┘
```

The reuslt of the individual phases are stored in log files in the project
folder `projects/<project name>/`, starting with `log-*`.

![Logfiles Overview](https://blog.deeb.ch/supermega/logfiles-overview.png)

- `supermega.log`: All log entries from SuperMega (the main log file)
- `cmdoutput.log`: The output of externally executed programs (e.g. C compiler, linker, assembler)
- `main_c_*`: C template, and its rendered counterpart
- `carrier_*`: The assembly-text before- and after fixup and cleanup

### Example loader code (.c Template)

The C source code is jinja2 templated, so i can integrate different carrier,
without depending on `#ifdef`.

`log-0-main_c_template.txt`:

```c
#include <Windows.h>
#include <time.h>

char *supermega_payload;

int main()
{
    // Alloc
    char *dest = VirtualAlloc(NULL, {{PAYLOAD_LEN}}, 0x3000, p_RW);

    // Decode
    {{ plugin_decoder }}

    // Permissions
	MyVirtualProtect(dest, {{PAYLOAD_LEN}}, p_RX, &result);

    // Execute
    (*(void(*)())(dest))();
}
```

With `plugin_decoder` for example being a 2-byte XOR decoder:

```c
    char *key = "{{XOR_KEY2}}";
    for ( int i = 0; i < {{PAYLOAD_LEN}}; i++ ) {
        dest[i] = supermega_payload[i] ^ key[i % 2];
    }
```

### Rendered .c Template

`log-1-main_c_rendered.txt`:

```c
    // Alloc
    char *dest = VirtualAlloc(NULL, 433, 0x3000, p_RW);

    // Decode
    char *key = "\xc1\x68";
    for ( int i = 0; i < 433; i++ ) {
        dest[i] = supermega_payload[i] ^ key[i % 2];
    }

    // Permissions
	MyVirtualProtect(dest, 433, p_RX, &result);

    // Execute
    (*(void(*)())(dest))();
```

### .asm Assembled

`log-2-carrier_asm_orig.txt`:

```
	mov	r9d, 4
	mov	r8d, 12288				; 00003000H
	mov	edx, 433				; 000001b1H
	xor	ecx, ecx
	call	QWORD PTR __imp_VirtualAlloc
	mov	QWORD PTR dest$[rsp], rax

...

	movsxd	rax, DWORD PTR i$1[rsp]
	mov	rcx, QWORD PTR supermega_payload
	movsx	eax, BYTE PTR [rcx+rax]
```

### .asm Cleanup

`log-2-carrier_asm_final.txt`:

```
	mov	r9d, 4
	mov	r8d, 12288				; 00003000H
	mov	edx, 433				; 000001b1H
	xor	ecx, ecx
	DB 0f8H, 0d8H, 0f3H, 0c5H, 075H, 085H ; IAT Reuse for VirtualAlloc
	mov	QWORD PTR dest$[rsp], rax

...

	movsxd	rax, DWORD PTR i$1[rsp]
	DB 099H, 04eH, 08bH, 0c3H, 015H, 02eH, 092H ; supermega_payload Payload
	movsx	eax, BYTE PTR [rcx+rax]
```

### Injection, IAT-reuse and .rdata insert

## SuperMega Options

![Logfiles Overview](https://blog.deeb.ch/supermega/supermega-options.png)

Input:

- Payload: The shellcode (or DLL) to execute
- Injectable: Non-malicious EXE we use to inject ourselves into

Options:

- Carrier: Which of the different carrier implementations to use
  - alloc\_rw\_rx: Alloc a RW region, copy shellcode, make it RX
  - alloc\_rw\_rwx: Alloc a RW region, copy shellcode, make it RWX (for shikata-ga-nai)
  - dll\_loader\_alloc: For DLL payload, alloc new region
  - dll\_loader\_change: For DLL payload, change .text
  - peb\_walk: Oldschool, for testing
- Carrier invoke:
  - change Entrypoint: Make PE entry-point point to our carrier (opsec unsafe)
  - backdoor Entrypoint: Backdoor the function which is pointed to by the PE entry-point
- Payload location:
  - .text
  - .rdata
- Add missing IAT entries: If you dont want to adjust shellcode based on imports of target EXE

And lastly, the carrier Opotions:

- Encode: How to encrypt payload
- Guardrails: Execution Guardrails (edit it first)
- AntiEmulation: Anti AV emulation
- Decoy: start a program to show the user
- VirtualProtect: Special VirtualProtect implementations

## Using Cordyceps for EXE Injection

```
      ┌─────────────┐
      │             │
      │             │            Memory Section
      ├─────────────┤            ┌──────────┐
┌─────┤  Carrier    ├────────────►          │
│     │             │ Alloc      │ Payload  │
│     ├─────────────┤ Copy       │ Usable   │
│     │             │ Jump       │          │
│     │             │            │          │
│     ├─────────────┤            │          │
└────►│  Payload    │            └──────────┘
      │  Encrypted  │
      ├─────────────┤
      │             │
      │             │
      └─────────────┘
```

The carrier (-shellcode) loads and executes the payload (-shellcode) into memory. In the case
of exe’s, the carrier will be stored in the middle of the .text section.
There are two options to jump to the carrier when the exe starts:

- `change Entrypoint`: Overwrite the entry point address in the PE header, and point it to the new location
- `hijack Main`: Use an existing jump inside the `main()` function

```
 Change Entrypoint                                    Backdoor Main

┌─────────────────┐                                  ┌─────────────────┐
│                 │ Header                           │                 │ Header
│                 │                                  │                 │
│    EntryPoint   ├────────────┐                     │    EntryPoint   │
│                 │            │                     │                 │
├─────────────────┤            │                     ├─────────────────┤
├─────────────────┤            │                     ├─────────────────┤
│                 │ main()     │                     │                 │ main()
│                 │            │                     │                 │
│                 │            │                     │                 ├────────────┐
├─────────────────┤            │                     ├─────────────────┤            │
│                 │            │                     │                 │            │
│                 │            │                     │                 │            │
├─────────────────┤            │                     ├─────────────────┤            │
│Carrier Shellcode│◄───────────┘                     │Carrier Shellcode│◄───────────┘
├─────────────────┤                                  ├─────────────────┤
│                 │                                  │                 │
│                 │                                  │                 │
│                 │                                  │                 │
│                 │                                  │                 │
│                 │                                  │                 │
└─────────────────┘                                  └─────────────────┘
```

`hijack Main` is way more opsec safe, and the original entry point of the
exe is preserved. Also, the jump to the carrier is not located conveniently at a
specific location where it can be scanned, but basically randomly inside `main()`, where it first needs to be found.

Then a carrier implementation can be selected.

| Name | Properties |
| --- | --- |
| peb\_walk | Text |
| alloc\_rw\_rwx | Title |
| alloc\_rw\_rx | Text |
| change\_rwx\_rx | Text |
| dll\_loader\_alloc | Text |
| dll\_loader\_change | Text |

There are different carrier implementations,
each using a different technique.

### alloc rw->rwx and alloc rw->rx

For example, the `alloc rw->rx` carrier
will allocate memory with `VirtualAlloc` as read-write, copy over
the shellcode, set it to read-execute, and jump to the shellcode.
The copying can of course also involve a decoding routine for the
shellcode, for example XOR. The payload can be stored in either
.text or .rdata section.

```
┌───────────────────┐
│      Hdr          │
├───────────────────┤
│                   │
│                   │
├───────────────────┤
│     .text         │
│                   ├─────────────┐
│                   │             │  VirtualAlloc RW
│                   │             │
│                   │             │  Copy
├───────────────────┤             │
│     .data         │             │  VirtualProtect RX / RWX
│                   │             │
├───────────────────┤             │  Jump
│                   │             │
│                   │             │
│                   │             │
├───────────────────┤             │
│     Shellcode     │◄────────────┘
│                   │
├───────────────────┤
│                   │
└───────────────────┘
```

This is the common `VirtualAlloc -> Copy -> VirtualProtect -> jump`
technique to start a shellcode. As all these calls come within an
IMAGE section, it should be kinda trusted (OPSEC good). But the payload will
then, as always, live in a PRIVATE section (OPSEC bad).

### change rwx->rx

There is the carrier called `change rwx->rx`, which will change the
permission of the shellcode to `read-write-exec`, decode it, and
then set it to `read-exec`. This will modify part of either the
.text or .rdata section, wherever the payload is stored.

```
┌───────────────────┐
│      Hdr          │
├───────────────────┤
│                   │
│                   │
├───────────────────┤                    VirtualProtect(.text, rwx)
│     .text         ├─────────────────┐
│                   │                 │  Copy
│                   │                 │
├───────────────────┤                 │  VirtualProtect(.text, rx)
│     .text: Changed│  ◄──────────────┘
├───────────────────┤
│                   │                    shellcode decoded! still image
│                   │
├───────────────────┤
│                   │
│                   │
└───────────────────┘
```

This can make the payload look like it’s living in an IMAGE section,
which is OPSEC good. Scanners that compare .text section of
memory and the origin file, like in the search for module stompers,
will detect modified .text reliably. This takes some performance tho.

As Cordyceps re-uses the IAT, if the carrier uses methods of DLL’s
that not imported by the injectable exe, one possibility is
to just patch the IAT. This allows the carrier to run on exe’s
even if not all of its needed functions are available.
Setting this option is OPSEC bad.

## Using Cordyceps for DLL Injection

If the injectable is a DLL, there are several ways to invoke the
carrier:

- Overwriting the entry point will exec it on DLL Load (instead DllMain)
- Putting it into DllMain() with code backdooring
- Putting it into an exported function with code backdooring
- Overwrite an exported function with the actual shellcode

## Using Cordyceps to load a DLL

It is possible to use the carrier `dll_loader`, and then select
a DLL as payload (NOT as injectable!).

The problem with loading shellcode is that the functionality never really exists
as shellcode itself: The shellcode will just allocate another memory section and
somehow load the actual functionality there, e.g. as (reflective) DLL.
This memory region is PRIVATE, which is OPSEC-bad.

The implemented DLL loader can be configured so that the payload stays in the
.text section as IMAGE after decoding it, which should be OPSEC-good.

This works by pre-loading the DLL into its in-memory form (considering RVA’s, and page aligning), and injecting that into a .text section.
When the EXE starts, it will
change the memory protection of the payload-DLL in-memory,
perform relocations and IAT loading, and executes
the DLL.

```

┌──────────────┐               ┌──────────────┐              ┌──────────────┐
│              │               │              │              │              │
├──────────────┤               ├──────────────┤              ├──────────────┤
│  .text       │               │  .text       │              │  .text       │
│              │               │              │              │              │
│              │               │              │              │              │
│              │               ├──────────────┤              ├──────────────┤
│              │               │ DLL .text    │              │ DLL .text    │
│              │               ├──────────────┤              ├──────────────┤
│              │ ────────────► │ DLL .rdata   │ ───────────► │ DLL .rdata   │
│              │ inject        ├──────────────┤  IAT load    ├──────────────┤
│              │ DLL preloaded │ DLL .data    │  Relocations │ DLL .data    │
│              │               │              │              │              │
├──────────────┤               ├──────────────┤              ├──────────────┤
│              │               │              │              │              │
│              │               │              │              │              │
│              │               │              │              │              │
│              │               │              │              │              │
│              │               │              │              │              │
└──────────────┘               └──────────────┘              └──────────────┘
    PE File                       PE File                       Process

```

## Testing

I try to test common usecases as integration tests.
This is extremely important, as stuff can break very easily
when refactoring, or working on core concepts.

It works by just using a shellcode as carrier which creates
the file `c:\temp\a`. The python script verifies after each
invocation of the infected executable that this file exists.
If not, something went wrong. That often means x64dbg time.

![tester.py log output showing all works](https://blog.deeb.ch/supermega/testerpy.png)

## SuperMega / Cordyceps Anti Detection Properties

- file scanning:
  - Hard to signature
  - payload encrypted
  - loader written in C, easiy modifiable
  - no loading of payload
  - bypass!
- Memory scanning:
  - carrier: bypass (same as file scanning)
  - payload: no protection (has to protect itself)
- behaviour:
  - carrier will use native DLL functions
    - from IMAGE (“trusted”)
    - clean call stack
      - no AceLdr, TitanLdr, ThreadStackSpoofer, CallStackMasker, MoonWalking needed
    - it may not trigger memory scanning?
  - payload: no protection (is on its own)
- no new threads (all origin from IMAGE)
- Machine learning bypass