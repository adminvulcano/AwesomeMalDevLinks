# https://rastamouse.me/bof-cocktails-in-cobalt-strike/

In a previous post, I wrote about [BOF Cocktails](https://rastamouse.me/bof-cocktails/) \- an execution pattern to merge tradecraft into postex BOFs so they didn't have to rely on an agent/loader for their evasion. That post outlines the problem areas more fully, so I encourage you to read that first.

At the time, Cobalt Strike did not have a nice way to intercept BOF execution, so we had to hack around it using `alias_clear` to override commands exposed by other Aggressor scripts. Fortunately, as was announced in the CS 4.13 release party [webinar](https://www.cobaltstrike.com/resources/videos/cobalt-strike-technical-walkthrough), Cobalt Strike has a new Aggressor hook called [**BEACON\_INLINE\_EXECUTE**](https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/content/topics_aggressor-scripts/as-resources_hooks.htm#BEACON_INLINE_EXECUTE). Thank you for reading my blog CS team 😄.

This hook is fired whenever Beacon is instructed to execute a BOF and presents the opportunity for operators to perform actions/processing on it before it's sent to Beacon.

The hook receives the original BOF in raw bytes, `$1`, and expects us to return a modified BOF, also in raw bytes. When using Crystal Palace, we process it through a specification file and return the transformed object.

```perl
import crystalpalace.spec.* from: crystalpalace.jar;
import java.util.HashMap;

# $1 - raw BOF bytes
set BEACON_INLINE_EXECUTE
{
    local( '$bof $spec_path $spec $capability $final' );

    $bof = $1;

    $spec_path  = script_resource( "cocktail.spec" );
    $spec       = [ LinkSpec Parse: $spec_path ];
    $capability = [ Capability Parse: cast( $bof, 'b' ) ];
    $final      = [ $spec run: $capability, [ new HashMap ] ];

    return $final;
}
```

cocktail.cna

You're free to do anything you want in the spec file. The following is a simple example of instrumenting calls to OpenProcessToken.

```text
x86:
    push $OBJECT              # grab the bof
        make coff +optimize   # turn it into a coff-exporter object

    load "bin/hooks.x86.o"    # grab the hooks
        merge                 # merge with the bof

    mergelib "libtcg.x86.zip" # merge the tcg library

    attach "ADVAPI32$OpenProcessToken" "__OpenProcessToken"  # add a hook

    export  # export the merged bof

x64:
    push $OBJECT
        make coff +optimize

    load "bin/hooks.x64.o"
        merge

    mergelib "libtcg.x64.zip"

    attach "ADVAPI32$OpenProcessToken" "_OpenProcessToken"

    export
```

cocktail.spec

```c
#include <windows.h>
#include "tcg.h"

DECLSPEC_IMPORT BOOL WINAPI ADVAPI32$OpenProcessToken( HANDLE, DWORD, PHANDLE );

BOOL WINAPI _OpenProcessToken( HANDLE ProcessHandle, DWORD DesiredAccess, PHANDLE TokenHandle )
{
    dprintf( "[*] _OpenProcessToken\n" );
    dprintf( "  -> ProcessHandle: 0x%p\n", ProcessHandle );
    dprintf( "  -> DesiredAccess: %d\n", DesiredAccess );

    return ADVAPI32$OpenProcessToken( ProcessHandle, DesiredAccess, TokenHandle );
}
```

hooks.c

![](https://storage.ghost.io/c/36/91/36918caa-651a-469a-9d4d-1ba06e2217bf/content/images/2026/06/image-1.png)

There's no much else to say other than thanks for the feature 👍

### You might also like...

26


May


## Module Stomping PIC

4 min read


[Module Stomping PIC](https://rastamouse.me/module-stomping-pic/)

25


Apr


## Atomic BOFs

5 min read


[Atomic BOFs](https://rastamouse.me/atomic-bofs/)

09


Apr


## Crystal Mask

8 min read


[Crystal Mask](https://rastamouse.me/crystal-mask/)

04


Mar


## Islands of Invariance

6 min read


[Islands of Invariance](https://rastamouse.me/islands-of-invariance/)

03


Jan


## BOF Cocktails

5 min read


[BOF Cocktails](https://rastamouse.me/bof-cocktails/)