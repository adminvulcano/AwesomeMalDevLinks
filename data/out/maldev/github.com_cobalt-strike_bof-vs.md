# https://github.com/Cobalt-Strike/bof-vs

[Skip to content](https://github.com/Cobalt-Strike/bof-vs#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/Cobalt-Strike/bof-vs) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/Cobalt-Strike/bof-vs) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/Cobalt-Strike/bof-vs) to refresh your session.Dismiss alert

{{ message }}

[Cobalt-Strike](https://github.com/Cobalt-Strike)/ **[bof-vs](https://github.com/Cobalt-Strike/bof-vs)** Public

- [Notifications](https://github.com/login?return_to=%2FCobalt-Strike%2Fbof-vs) You must be signed in to change notification settings
- [Fork\\
38](https://github.com/login?return_to=%2FCobalt-Strike%2Fbof-vs)
- [Star\\
276](https://github.com/login?return_to=%2FCobalt-Strike%2Fbof-vs)


main

[**1** Branch](https://github.com/Cobalt-Strike/bof-vs/branches) [**6** Tags](https://github.com/Cobalt-Strike/bof-vs/tags)

[Go to Branches page](https://github.com/Cobalt-Strike/bof-vs/branches)[Go to Tags page](https://github.com/Cobalt-Strike/bof-vs/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>![author](https://github.githubassets.com/images/gravatars/gravatar-user-420.png?size=40)<br>Henri Nurmi (Cobalt Strike)<br>[Merge branch 'feat/update-readme' into 'main'](https://github.com/Cobalt-Strike/bof-vs/commit/c9b3ae2276cced9335cdc73cd4956b8a9b3b0708)<br>Open commit details<br>5 months agoNov 20, 2025<br>[c9b3ae2](https://github.com/Cobalt-Strike/bof-vs/commit/c9b3ae2276cced9335cdc73cd4956b8a9b3b0708) · 5 months agoNov 20, 2025<br>## History<br>[24 Commits](https://github.com/Cobalt-Strike/bof-vs/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/Cobalt-Strike/bof-vs/commits/main/) 24 Commits |
| [BOF-Template](https://github.com/Cobalt-Strike/bof-vs/tree/main/BOF-Template "BOF-Template") | [BOF-Template](https://github.com/Cobalt-Strike/bof-vs/tree/main/BOF-Template "BOF-Template") | [Update template with 4.12 changes](https://github.com/Cobalt-Strike/bof-vs/commit/dd6addd1f9b4bc637b63247d67552709f0c59ddf "Update template with 4.12 changes") | 6 months agoOct 30, 2025 |
| [media](https://github.com/Cobalt-Strike/bof-vs/tree/main/media "media") | [media](https://github.com/Cobalt-Strike/bof-vs/tree/main/media "media") | [Update README.md](https://github.com/Cobalt-Strike/bof-vs/commit/f89828347d83f3cfea56fb91297b505d1e59c49e "Update README.md  Update README.md with link to the latest release  Add files via upload  Delete videos/Setup BOF-VS.mp4  Update README.md  Update README.md  Add files via upload  Update README.md") | 5 months agoNov 20, 2025 |
| [.gitignore](https://github.com/Cobalt-Strike/bof-vs/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/Cobalt-Strike/bof-vs/blob/main/.gitignore ".gitignore") | [Initial commit](https://github.com/Cobalt-Strike/bof-vs/commit/b1973774899304b894228a567f9c5cc0f44b49d1 "Initial commit") | 3 years agoSep 19, 2023 |
| [BOF-Template.sln](https://github.com/Cobalt-Strike/bof-vs/blob/main/BOF-Template.sln "BOF-Template.sln") | [BOF-Template.sln](https://github.com/Cobalt-Strike/bof-vs/blob/main/BOF-Template.sln "BOF-Template.sln") | [Add sleepmask support](https://github.com/Cobalt-Strike/bof-vs/commit/855a33afacd6efad3eaceebe42c5ece4a435d91d "Add sleepmask support") | 2 years agoJun 20, 2024 |
| [LICENSE](https://github.com/Cobalt-Strike/bof-vs/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/Cobalt-Strike/bof-vs/blob/main/LICENSE "LICENSE") | [Add sleepmask support](https://github.com/Cobalt-Strike/bof-vs/commit/855a33afacd6efad3eaceebe42c5ece4a435d91d "Add sleepmask support") | 2 years agoJun 20, 2024 |
| [README.md](https://github.com/Cobalt-Strike/bof-vs/blob/main/README.md "README.md") | [README.md](https://github.com/Cobalt-Strike/bof-vs/blob/main/README.md "README.md") | [Update README.md](https://github.com/Cobalt-Strike/bof-vs/commit/f89828347d83f3cfea56fb91297b505d1e59c49e "Update README.md  Update README.md with link to the latest release  Add files via upload  Delete videos/Setup BOF-VS.mp4  Update README.md  Update README.md  Add files via upload  Update README.md") | 5 months agoNov 20, 2025 |
| View all files |

## Repository files navigation

# Beacon Object File Visual Studio Template

[Permalink: Beacon Object File Visual Studio Template](https://github.com/Cobalt-Strike/bof-vs#beacon-object-file-visual-studio-template)

[This repository](https://github.com/Cobalt-Strike/bof-vs) contains the Beacon Object File Visual Studio (BOF-VS) template project.
You can read more about rationale and design decisions from this blog [post](https://www.cobaltstrike.com/blog/simplifying-bof-development).

## Quick Start Guide

[Permalink: Quick Start Guide](https://github.com/Cobalt-Strike/bof-vs#quick-start-guide)

To get started, use the instructions provided below.

### Video Walkthrough

[Permalink: Video Walkthrough](https://github.com/Cobalt-Strike/bof-vs#video-walkthrough)

Setup.BOF-VS.mp4

### Prerequisites:

[Permalink: Prerequisites:](https://github.com/Cobalt-Strike/bof-vs#prerequisites)

- An x64 Windows 10/11 development machine (without a security solution)
- Visual Studio Community/Pro/Enterprise 2022 (Desktop Development with C++ installed)
- Python 3 for the BOF linter (optional)

### Template Installation

[Permalink: Template Installation](https://github.com/Cobalt-Strike/bof-vs#template-installation)

Download the latest [release](https://github.com/Cobalt-Strike/bof-vs/releases/latest/download/bof-vs.zip),
and copy the `bof-vs.zip` archive under the
`%USERPROFILE%\Documents\Visual Studio 2022\Templates\ProjectTemplates` folder.
The template is accessible through Visual Studio's new project dialog,
where you can locate it by searching with the keyword `BOF`. Be certain
to have `All languages` chosen as the language filter.

If Visual Studio does not recognize the template, then reset the project template cache by
deleting the following file: `%localappdata%\Microsoft\VisualStudio\<VS vesrion>\ProjectTemplatesCache_{<GUID>}\cache.bin`

If you need a BOF-VS template for a previous version of Cobalt Strike, you can find it under the [tags](https://github.com/Cobalt-Strike/bof-vs/tags).

### Debug Build

[Permalink: Debug Build](https://github.com/Cobalt-Strike/bof-vs#debug-build)

The `Debug` target builds your BOF to an executable, which allows
you to benefit from the convenience of debugging your BOF code directly within
Visual Studio's built-in debugger. This will enable you to work at the source
code level without running the BOF through a Beacon.

### Release Build

[Permalink: Release Build](https://github.com/Cobalt-Strike/bof-vs#release-build)

The Release target compiles a release object file of your BOF,
which is designed to be used directly with Cobalt Strike.

## Dynamic Function Resolution

[Permalink: Dynamic Function Resolution](https://github.com/Cobalt-Strike/bof-vs#dynamic-function-resolution)

The project template includes two macro definitions to facilitate Dynamic
Function Resolution (DFR) declarations. These macros provide a robust mechanism
for efficiently resolving Win32 API functions in BOFs and simplify the
development process significantly.

### DFR Macro

[Permalink: DFR Macro](https://github.com/Cobalt-Strike/bof-vs#dfr-macro)

The `DFR` macro can automatically extract the function type and generate
the required function declaration.

```
DFR(KERNEL32, OpenProcess)
```

The above `DFR` macro statement expands to the following declaration.

```
DECLSPEC_IMPORT decltype(OpenProcess) KERNEL32$OpenProcess;
```

A common practice is to map the `KERNEL32$OpenProcess` function to OpenProcess
using the following macro definition. This mapping enables you to call the
OpenProcess function directly, eliminating the need for the `KERNEL32$` prefix.

```
#define OpenProcess KERNEL32$OpenProcess
```

#### Example Usage

[Permalink: Example Usage](https://github.com/Cobalt-Strike/bof-vs#example-usage)

```
DFR(KERNEL32, OpenProcess)
#define OpenProcess KERNEL32$OpenProcess

void func1() {
    OpenProcess(...);
}

void func2() {
    OpenProcess(...);
}
```

### DFR\_LOCAL Macro

[Permalink: DFR_LOCAL Macro](https://github.com/Cobalt-Strike/bof-vs#dfr_local-macro)

The `DFR_LOCAL(module, function)` macro allows you to define a local function
pointer variable that directly references the `module$function` function. One
of the main advantages of using this macro compared to the `DFR` macro is
the elimination of the need for the additional `OpenProcess` -\> `KERNEL32$OpenProcess`
mapping. This streamlines the code and makes it more concise. However, it's
important to note that the function pointer created with the `DFR_LOCAL` macro
has a limited scope and can only be accessed within the function where it is defined.
Consequently, if you plan to use the required WINAPI functions in multiple
functions throughout your BOF, you will need to define the function pointer
using the DFR\_LOCAL macro in each of those functions.

#### Example Usage

[Permalink: Example Usage](https://github.com/Cobalt-Strike/bof-vs#example-usage-1)

```
void func1() {
    DFR_LOCAL(KERNEL32, OpenProcess);
    OpenProcess(...);
}

void func2() {
    DFR_LOCAL(KERNEL32, OpenProcess);
    OpenProcess(...);
}
```

## Mocked APIs

[Permalink: Mocked APIs](https://github.com/Cobalt-Strike/bof-vs#mocked-apis)

The template includes a mocked version of the Beacon API for Debug builds,
enabling BOF debugging without a running Beacon instance. When you select
either the Debug or UnitTest configuration, the mocked API is automatically
included into the project.

### Argument Packer

[Permalink: Argument Packer](https://github.com/Cobalt-Strike/bof-vs#argument-packer)

The BofData class implements an argument packer to replicate the argument
packing behavior of the bof\_pack aggressor function. This enables us to
call BOF's entry point with custom arguments without Beacon.

```
bof::mock::BofData data;
// the pack function takes one or more arguments
data.pack<int, short, int, const char*>(6502, 80, 68010, "Hello World");

// alternatively, the << operator can be used to construct the arguments buffer
data << 0xdeadface << L"Hello World";

// raw buffers can be added too
const char buf[] = { 0x41, 0x42, 0x43, 0x44 };
data.addData(buf, sizeof(buf));

go(data.get(), data.size());
```

### Beacon API

[Permalink: Beacon API](https://github.com/Cobalt-Strike/bof-vs#beacon-api)

The template also provides a mocked implementation of the Data Parser, Output,
and Format APIs. The mocked functions within the Output API print the output
to the standard output, ensuring the results are visible. Moreover, all returned
output is stored for future examination and analysis.

Furthermore, the Internal API functions (such as BeaconUseToken,
BeaconInjectProcess, etc.) are declared. However, it is important to note that
these functions lack the real implementation and only display an error message
on the standard error if called.

## Unit Tests

[Permalink: Unit Tests](https://github.com/Cobalt-Strike/bof-vs#unit-tests)

The project template offers an additional build target called `UnitTest`,
specifically designed to build BOFs with the GoogleTest framework. Furthermore,
the mock library provides a convenient `runMocked` function that handles
the argument packing, execution of the BOF's entry point, and capturing all
generated outputs.

Install the GoogleTest framework:

1. Right-click the project name in Solution Explorer.
2. Select `Manage NuGet Packages`.
3. Ensure that the `Microsoft.googletest.v140.windesktop.msvcstl.static.rt-static` package is installed.

### Example Usage

[Permalink: Example Usage](https://github.com/Cobalt-Strike/bof-vs#example-usage-2)

```
extern "C" {
    #include "beacon.h"

    void go(char* args, int len) {
        datap parser;
        BeaconDataParse(&parser, args, len);
        int number = BeaconDataInt(&parser);
        BeaconPrintf(CALLBACK_OUTPUT, "Hello: %i", number);
    }
}

TEST(ExampleBofTest, TestCase1) {
    std::vector<bof::output::OutputEntry> actual =
        bof::runMocked<int>(go, 6502);

    std::vector<bof::output::OutputEntry> expected = {
        {CALLBACK_OUTPUT, "Hello: 6502"}
    };

    ASSERT_EQ(expected, actual);
}
```

## Sleepmask

[Permalink: Sleepmask](https://github.com/Cobalt-Strike/bof-vs#sleepmask)

In addition to supporting standard Beacon Object Files, the template also includes
functionality for developing Sleepmask BOFs. Beacon's Sleepmask can be used to apply
runtime masking to its PE sections and Heap allocations. Therefore, this template
creates a "mock Beacon" as part of the call to runMockedSleepMask() to replicate
the layout of Beacon in memory during debugging. This function also makes it possible
to apply malleable C2 settings to the "mock Beacon".

```
// Mock up Beacon and run the sleep mask once
bof::runMockedSleepMask(sleep_mask);

// Mock up Beacon with the specific .stage C2 profile
bof::runMockedSleepMask(sleep_mask,
    {
        .allocator = bof::profile::Allocator::VirtualAlloc,
        .obfuscate = bof::profile::Obfuscate::False,
        .useRWX = bof::profile::UseRWX::True,
        .module = "",
    },
    {
        .sleepTimeMs = 5000,
        .runForever = false,
    }
);
```

## Multiple BOFs

[Permalink: Multiple BOFs](https://github.com/Cobalt-Strike/bof-vs#multiple-bofs)

The template supports multiple BOFs within separate files, enabling each .cpp
file to be compiled into an individual BOF. This approach eliminates the need
for multiple projects and allows grouping similar BOFs under one Visual Studio
project. When it comes to debugging, since each BOF is compiled into its own
debug executable, it is important to adjust the debug command accordingly.
This can be done through the project properties: `Configuration Properties -> Debugging -> Command`.

## BOF Linter

[Permalink: BOF Linter](https://github.com/Cobalt-Strike/bof-vs#bof-linter)

To help identify potential BOF issues, the template integrates the `boflint`
tool, which runs during the release build to analyze the BOF for common errors
and shows them in the Error List of Visual Studio. This linter detects several
key issues, including:

- **Relocation types**: Ensures only supported relocation types are used.
- **Entry point validation**: Verifies the presence of the mandatory `go` or `sleep_mask` function.
- **Import resolution**: Flags undefined or unresolvable imports.
- **Large stack variables**: Detects large stack variable usage that results in an unresolvable import for stack probing.
- **Exception handling**: Warns against the use of exception handling, which is unsupported in BOFs.

`boflint` is only executed if Python 3 is detected on the system. If Python 3
is not installed, you can get it from:

- [Microsoft Store](https://apps.microsoft.com/detail/9ncvdn91xzqp?hl=en-us&gl=US)
- [Official Python release](https://www.python.org/downloads/windows/)

You can also run the linter manually:

```
python ./utils/boflint.py --loader cs x64/Release/bof.x64.o
```

## About

A Beacon Object File (BOF) template for Visual Studio


### Resources

[Readme](https://github.com/Cobalt-Strike/bof-vs#readme-ov-file)

### License

[Apache-2.0 license](https://github.com/Cobalt-Strike/bof-vs#Apache-2.0-1-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/Cobalt-Strike/bof-vs).

[Activity](https://github.com/Cobalt-Strike/bof-vs/activity)

[Custom properties](https://github.com/Cobalt-Strike/bof-vs/custom-properties)

### Stars

[**276**\\
stars](https://github.com/Cobalt-Strike/bof-vs/stargazers)

### Watchers

[**4**\\
watching](https://github.com/Cobalt-Strike/bof-vs/watchers)

### Forks

[**38**\\
forks](https://github.com/Cobalt-Strike/bof-vs/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2FCobalt-Strike%2Fbof-vs&report=Cobalt-Strike+%28user%29)

## [Releases\  4](https://github.com/Cobalt-Strike/bof-vs/releases)

[CS 4.12\\
Latest\\
\\
on Nov 25, 2025Nov 25, 2025](https://github.com/Cobalt-Strike/bof-vs/releases/tag/cs-4.12)

[\+ 3 releases](https://github.com/Cobalt-Strike/bof-vs/releases)

## [Packages\  0](https://github.com/orgs/Cobalt-Strike/packages?repo_name=bof-vs)

No packages published

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/Cobalt-Strike/bof-vs).

## [Contributors\  1](https://github.com/Cobalt-Strike/bof-vs/graphs/contributors)

- [![@zurro](https://avatars.githubusercontent.com/u/52583?s=64&v=4)](https://github.com/zurro)[**zurro** Pablo A. Zurro](https://github.com/zurro)

## Languages

- [C++49.8%](https://github.com/Cobalt-Strike/bof-vs/search?l=c%2B%2B)
- [Python29.4%](https://github.com/Cobalt-Strike/bof-vs/search?l=python)
- [C19.1%](https://github.com/Cobalt-Strike/bof-vs/search?l=c)
- [Makefile1.7%](https://github.com/Cobalt-Strike/bof-vs/search?l=makefile)

You can’t perform that action at this time.