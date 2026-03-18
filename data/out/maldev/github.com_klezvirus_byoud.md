# https://github.com/klezVirus/BYOUD

[Skip to content](https://github.com/klezVirus/BYOUD#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/klezVirus/BYOUD) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/klezVirus/BYOUD) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/klezVirus/BYOUD) to refresh your session.Dismiss alert

{{ message }}

[klezVirus](https://github.com/klezVirus)/ **[BYOUD](https://github.com/klezVirus/BYOUD)** Public

- [Notifications](https://github.com/login?return_to=%2FklezVirus%2FBYOUD) You must be signed in to change notification settings
- [Fork\\
8](https://github.com/login?return_to=%2FklezVirus%2FBYOUD)
- [Star\\
82](https://github.com/login?return_to=%2FklezVirus%2FBYOUD)


master

[**1** Branch](https://github.com/klezVirus/BYOUD/branches) [**0** Tags](https://github.com/klezVirus/BYOUD/tags)

[Go to Branches page](https://github.com/klezVirus/BYOUD/branches)[Go to Tags page](https://github.com/klezVirus/BYOUD/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![klezVirus](https://avatars.githubusercontent.com/u/8959898?v=4&size=40)](https://github.com/klezVirus)[klezVirus](https://github.com/klezVirus/BYOUD/commits?author=klezVirus)<br>[feat: initial public release](https://github.com/klezVirus/BYOUD/commit/848fbba512b56a21a3d302b4abfdbc4cf8993cfb)<br>3 days agoMar 14, 2026<br>[848fbba](https://github.com/klezVirus/BYOUD/commit/848fbba512b56a21a3d302b4abfdbc4cf8993cfb) · 3 days agoMar 14, 2026<br>## History<br>[1 Commit](https://github.com/klezVirus/BYOUD/commits/master/) <br>Open commit details<br>[View commit history for this file.](https://github.com/klezVirus/BYOUD/commits/master/) 1 Commit |
| [byoud](https://github.com/klezVirus/BYOUD/tree/master/byoud "byoud") | [byoud](https://github.com/klezVirus/BYOUD/tree/master/byoud "byoud") | [feat: initial public release](https://github.com/klezVirus/BYOUD/commit/848fbba512b56a21a3d302b4abfdbc4cf8993cfb "feat: initial public release") | 3 days agoMar 14, 2026 |
| [udinject](https://github.com/klezVirus/BYOUD/tree/master/udinject "udinject") | [udinject](https://github.com/klezVirus/BYOUD/tree/master/udinject "udinject") | [feat: initial public release](https://github.com/klezVirus/BYOUD/commit/848fbba512b56a21a3d302b4abfdbc4cf8993cfb "feat: initial public release") | 3 days agoMar 14, 2026 |
| [.gitignore](https://github.com/klezVirus/BYOUD/blob/master/.gitignore ".gitignore") | [.gitignore](https://github.com/klezVirus/BYOUD/blob/master/.gitignore ".gitignore") | [feat: initial public release](https://github.com/klezVirus/BYOUD/commit/848fbba512b56a21a3d302b4abfdbc4cf8993cfb "feat: initial public release") | 3 days agoMar 14, 2026 |
| [LICENSE](https://github.com/klezVirus/BYOUD/blob/master/LICENSE "LICENSE") | [LICENSE](https://github.com/klezVirus/BYOUD/blob/master/LICENSE "LICENSE") | [feat: initial public release](https://github.com/klezVirus/BYOUD/commit/848fbba512b56a21a3d302b4abfdbc4cf8993cfb "feat: initial public release") | 3 days agoMar 14, 2026 |
| [README.md](https://github.com/klezVirus/BYOUD/blob/master/README.md "README.md") | [README.md](https://github.com/klezVirus/BYOUD/blob/master/README.md "README.md") | [feat: initial public release](https://github.com/klezVirus/BYOUD/commit/848fbba512b56a21a3d302b4abfdbc4cf8993cfb "feat: initial public release") | 3 days agoMar 14, 2026 |
| [byoud.sln](https://github.com/klezVirus/BYOUD/blob/master/byoud.sln "byoud.sln") | [byoud.sln](https://github.com/klezVirus/BYOUD/blob/master/byoud.sln "byoud.sln") | [feat: initial public release](https://github.com/klezVirus/BYOUD/commit/848fbba512b56a21a3d302b4abfdbc4cf8993cfb "feat: initial public release") | 3 days agoMar 14, 2026 |
| View all files |

## Repository files navigation

# BYOUD — Bring Your Own Unwind Data

[Permalink: BYOUD — Bring Your Own Unwind Data](https://github.com/klezVirus/BYOUD#byoud--bring-your-own-unwind-data)

BYOUD is a framework for x64 stack spoofing on Windows. It tackles a complete opposite approach from classic stack spoofing, manipulating unwind metadata to hide arbitrary chunks of the call chain in debuggers and EDRs.

For a full technical breakdown of how it works, see the [blog post](https://klezvirus.github.io/posts/Byoud).

* * *

## Techniques

[Permalink: Techniques](https://github.com/klezVirus/BYOUD#techniques)

| # | Name | Description |
| --- | --- | --- |
| 1 | `UNWIND_DATA_TAMPER` | Modifies the target function's `UNWIND_INFO` in place to expand the frame size |
| 2 | `UNWIND_DATA_HIJACK` | Replaces the `UnwindData` RVA of the target's `RUNTIME_FUNCTION` with a donor's |
| 3 | `RT_FUNCTION_HIJACK` | Hijacks an existing `.pdata` entry to cover the shellcode's address range |
| 4 | `RT_FUNCTION_INJECT` | Appends a new `RUNTIME_FUNCTION` and `UNWIND_INFO` to the module's exception directory |
| 5 | `RTFI_JIT_SYSINFORMER` | Registers a dynamic `RUNTIME_FUNCTION` via `RtlAddFunctionTable` with cache bypass — visible to SystemInformer |
| 6 | `RTFI_JIT_WINDBG` | Same as above with additional `LdrpInvertedFunctionTable` manipulation — visible to WinDbg |
| 7 | `RTFI_JIT_NORMAL_VA` | Registers a dynamic `RUNTIME_FUNCTION` for shellcode in a plain `VirtualAlloc`'d region |

Techniques 1–4 and 7 work correctly regardless of `/GS` compilation settings. Techniques 5 and 6 have known issues when the calling DLL is compiled with stack cookies. Compile with `/GS-` to avoid this.

* * *

## Components

[Permalink: Components](https://github.com/klezVirus/BYOUD#components)

**`byoud.dll`** — the framework. Exposes `ShieldedExecution` (runs a technique end-to-end) and `CallGate` (the assembly stub copied into target modules).

**`udinject.exe`** — test harness for exercising the framework, inspecting stack traces, and validating unwind behavior across techniques.

* * *

For everything else, see the [blog post](https://klezvirus.github.io/posts/Byoud/).

## References and Acknowledgements

[Permalink: References and Acknowledgements](https://github.com/klezVirus/BYOUD#references-and-acknowledgements)

- [namazso](https://x.com/namazso) because his original work on stack spoofing has laid the groundwork for all current research on the topic
- [Gabriel Landau](https://x.com/GabrielLandau) for the shadow stack analysis research
- [Alex Ionescu](https://x.com/aionescu) and [Yarden Shafir](https://x.com/yarden_shafir) for their CET internals work

## About

Bring your own Unwind Data Framework


### Resources

[Readme](https://github.com/klezVirus/BYOUD#readme-ov-file)

### License

[GPL-3.0 license](https://github.com/klezVirus/BYOUD#GPL-3.0-1-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/klezVirus/BYOUD).

[Activity](https://github.com/klezVirus/BYOUD/activity)

### Stars

[**82**\\
stars](https://github.com/klezVirus/BYOUD/stargazers)

### Watchers

[**0**\\
watching](https://github.com/klezVirus/BYOUD/watchers)

### Forks

[**8**\\
forks](https://github.com/klezVirus/BYOUD/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2FklezVirus%2FBYOUD&report=klezVirus+%28user%29)

## [Releases](https://github.com/klezVirus/BYOUD/releases)

No releases published

## [Packages\  0](https://github.com/users/klezVirus/packages?repo_name=BYOUD)

No packages published

## [Contributors\  1](https://github.com/klezVirus/BYOUD/graphs/contributors)

- [![@klezVirus](https://avatars.githubusercontent.com/u/8959898?s=64&v=4)](https://github.com/klezVirus)[**klezVirus**](https://github.com/klezVirus)

## Languages

- [C++82.2%](https://github.com/klezVirus/BYOUD/search?l=c%2B%2B)
- [C14.6%](https://github.com/klezVirus/BYOUD/search?l=c)
- [Assembly3.2%](https://github.com/klezVirus/BYOUD/search?l=assembly)

You can’t perform that action at this time.