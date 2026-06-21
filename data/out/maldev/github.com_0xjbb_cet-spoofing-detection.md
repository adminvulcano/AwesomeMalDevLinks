# https://github.com/0xjbb/cet-spoofing-detection

[Skip to content](https://github.com/0xjbb/cet-spoofing-detection#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/0xjbb/cet-spoofing-detection) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/0xjbb/cet-spoofing-detection) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/0xjbb/cet-spoofing-detection) to refresh your session.Dismiss alert

{{ message }}

[0xjbb](https://github.com/0xjbb)/ **[cet-spoofing-detection](https://github.com/0xjbb/cet-spoofing-detection)** Public

- [Notifications](https://github.com/login?return_to=%2F0xjbb%2Fcet-spoofing-detection) You must be signed in to change notification settings
- [Fork\\
4](https://github.com/login?return_to=%2F0xjbb%2Fcet-spoofing-detection)
- [Star\\
37](https://github.com/login?return_to=%2F0xjbb%2Fcet-spoofing-detection)


master

[**1** Branch](https://github.com/0xjbb/cet-spoofing-detection/branches) [**0** Tags](https://github.com/0xjbb/cet-spoofing-detection/tags)

[Go to Branches page](https://github.com/0xjbb/cet-spoofing-detection/branches)[Go to Tags page](https://github.com/0xjbb/cet-spoofing-detection/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>![author](https://github.githubassets.com/images/gravatars/gravatar-user-420.png?size=40)<br>0xjbb<br>[Fix for](https://github.com/0xjbb/cet-spoofing-detection/commit/ca660ca8b75e1e6fb89ce62221b7c4694c526fcc) [#1](https://github.com/0xjbb/cet-spoofing-detection/issues/1)<br>last monthMay 22, 2026<br>[ca660ca](https://github.com/0xjbb/cet-spoofing-detection/commit/ca660ca8b75e1e6fb89ce62221b7c4694c526fcc) · last monthMay 22, 2026<br>## History<br>[3 Commits](https://github.com/0xjbb/cet-spoofing-detection/commits/master/) <br>Open commit details<br>[View commit history for this file.](https://github.com/0xjbb/cet-spoofing-detection/commits/master/) 3 Commits |
| [screenshots](https://github.com/0xjbb/cet-spoofing-detection/tree/master/screenshots "screenshots") | [screenshots](https://github.com/0xjbb/cet-spoofing-detection/tree/master/screenshots "screenshots") | [Initial commit](https://github.com/0xjbb/cet-spoofing-detection/commit/e0efd5e9043262a4753c8adb7f6c410b5e4a8b8e "Initial commit") | last monthMay 14, 2026 |
| [.gitignore](https://github.com/0xjbb/cet-spoofing-detection/blob/master/.gitignore ".gitignore") | [.gitignore](https://github.com/0xjbb/cet-spoofing-detection/blob/master/.gitignore ".gitignore") | [Initial commit](https://github.com/0xjbb/cet-spoofing-detection/commit/e0efd5e9043262a4753c8adb7f6c410b5e4a8b8e "Initial commit") | last monthMay 14, 2026 |
| [CMakeLists.txt](https://github.com/0xjbb/cet-spoofing-detection/blob/master/CMakeLists.txt "CMakeLists.txt") | [CMakeLists.txt](https://github.com/0xjbb/cet-spoofing-detection/blob/master/CMakeLists.txt "CMakeLists.txt") | [Initial commit](https://github.com/0xjbb/cet-spoofing-detection/commit/e0efd5e9043262a4753c8adb7f6c410b5e4a8b8e "Initial commit") | last monthMay 14, 2026 |
| [README.md](https://github.com/0xjbb/cet-spoofing-detection/blob/master/README.md "README.md") | [README.md](https://github.com/0xjbb/cet-spoofing-detection/blob/master/README.md "README.md") | [readme update](https://github.com/0xjbb/cet-spoofing-detection/commit/980893fab8e27595b3d56187b1ed490d09a6ce73 "readme update") | last monthMay 14, 2026 |
| [main.cpp](https://github.com/0xjbb/cet-spoofing-detection/blob/master/main.cpp "main.cpp") | [main.cpp](https://github.com/0xjbb/cet-spoofing-detection/blob/master/main.cpp "main.cpp") | [Initial commit](https://github.com/0xjbb/cet-spoofing-detection/commit/e0efd5e9043262a4753c8adb7f6c410b5e4a8b8e "Initial commit") | last monthMay 14, 2026 |
| [util.cpp](https://github.com/0xjbb/cet-spoofing-detection/blob/master/util.cpp "util.cpp") | [util.cpp](https://github.com/0xjbb/cet-spoofing-detection/blob/master/util.cpp "util.cpp") | [Fix for](https://github.com/0xjbb/cet-spoofing-detection/commit/ca660ca8b75e1e6fb89ce62221b7c4694c526fcc "Fix for https://github.com/0xjbb/cet-spoofing-detection/issues/1") [#1](https://github.com/0xjbb/cet-spoofing-detection/issues/1) | last monthMay 22, 2026 |
| [util.h](https://github.com/0xjbb/cet-spoofing-detection/blob/master/util.h "util.h") | [util.h](https://github.com/0xjbb/cet-spoofing-detection/blob/master/util.h "util.h") | [Initial commit](https://github.com/0xjbb/cet-spoofing-detection/commit/e0efd5e9043262a4753c8adb7f6c410b5e4a8b8e "Initial commit") | last monthMay 14, 2026 |
| View all files |

## Repository files navigation

# CET Spoofing Detection

[Permalink: CET Spoofing Detection](https://github.com/0xjbb/cet-spoofing-detection#cet-spoofing-detection)

This tool is a proof of concept aimed to detect stackspoofing within CET processes. It does this by comparing the shadow stack to the userstack and looks for missing frames.
There are some false positives when a process uses .NET.

### Compilation

[Permalink: Compilation](https://github.com/0xjbb/cet-spoofing-detection#compilation)

- assumes clang/++, cmake and ninja are in your path
- untested with MSVC.

## Build

[Permalink: Build](https://github.com/0xjbb/cet-spoofing-detection#build)

```
cmake -B build -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -G Ninja
cmake --build build
```

```
PS C:\Users\dev\CLionProjects\CETSpoofingDetection> cmake -B build -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -G Ninja
-- The C compiler identification is Clang 22.1.2 with GNU-like command-line
-- The CXX compiler identification is Clang 22.1.2 with GNU-like command-line
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: C:/Program Files/LLVM/bin/clang.exe - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: C:/Program Files/LLVM/bin/clang++.exe - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done (4.7s)
-- Generating done (0.0s)
-- Build files have been written to: C:/Users/dev/CLionProjects/CETSpoofingDetection/build
PS C:\Users\dev\CLionProjects\CETSpoofingDetection> cmake --build build
[6/6] Linking CXX executable CETSpoofingDetection.exe
PS C:\Users\dev\CLionProjects\CETSpoofingDetection>
```

### Usage

[Permalink: Usage](https://github.com/0xjbb/cet-spoofing-detection#usage)

Just run the application inside a terminal, it will take a snapshot of threads and iterate through, extract CET processes and them check the stacks of those.

Below is an example of using it against the BOYUD project : [https://github.com/klezVirus/BYOUD](https://github.com/klezVirus/BYOUD)

[![](https://github.com/0xjbb/cet-spoofing-detection/raw/master/screenshots/udinject.jpg)](https://github.com/0xjbb/cet-spoofing-detection/blob/master/screenshots/udinject.jpg)

The spoofed callstack

[![](https://github.com/0xjbb/cet-spoofing-detection/raw/master/screenshots/callstack.jpg)](https://github.com/0xjbb/cet-spoofing-detection/blob/master/screenshots/callstack.jpg)

Detection from the tool.

[![](https://github.com/0xjbb/cet-spoofing-detection/raw/master/screenshots/alert.jpg)](https://github.com/0xjbb/cet-spoofing-detection/blob/master/screenshots/alert.jpg)

## About

Stack spoofing Detection for CET processes by comparing shadow and user stacks.


### Topics

[engineering](https://github.com/topics/engineering "Topic: engineering") [stack](https://github.com/topics/stack "Topic: stack") [detection](https://github.com/topics/detection "Topic: detection") [cet](https://github.com/topics/cet "Topic: cet") [spoofing](https://github.com/topics/spoofing "Topic: spoofing") [shadow](https://github.com/topics/shadow "Topic: shadow") [soc](https://github.com/topics/soc "Topic: soc") [red-team](https://github.com/topics/red-team "Topic: red-team") [shadowstack](https://github.com/topics/shadowstack "Topic: shadowstack") [unwind](https://github.com/topics/unwind "Topic: unwind") [blue-team](https://github.com/topics/blue-team "Topic: blue-team") [redteam](https://github.com/topics/redteam "Topic: redteam") [shadow-stack](https://github.com/topics/shadow-stack "Topic: shadow-stack") [stack-spoofing](https://github.com/topics/stack-spoofing "Topic: stack-spoofing") [intel-cet](https://github.com/topics/intel-cet "Topic: intel-cet") [stackspoofing](https://github.com/topics/stackspoofing "Topic: stackspoofing")

### Resources

[Readme](https://github.com/0xjbb/cet-spoofing-detection#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/0xjbb/cet-spoofing-detection).

[Activity](https://github.com/0xjbb/cet-spoofing-detection/activity)

### Stars

[**37**\\
stars](https://github.com/0xjbb/cet-spoofing-detection/stargazers)

### Watchers

[**0**\\
watching](https://github.com/0xjbb/cet-spoofing-detection/watchers)

### Forks

[**4**\\
forks](https://github.com/0xjbb/cet-spoofing-detection/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2F0xjbb%2Fcet-spoofing-detection&report=0xjbb+%28user%29)

## [Contributors\  0](https://github.com/0xjbb/cet-spoofing-detection/graphs/contributors)

No contributors


## Languages

- [C++98.2%](https://github.com/0xjbb/cet-spoofing-detection/search?l=c%2B%2B)
- [CMake1.8%](https://github.com/0xjbb/cet-spoofing-detection/search?l=cmake)

You can’t perform that action at this time.