# https://github.com/dadevel/xwin-starterpack?

[Skip to content](https://github.com/dadevel/xwin-starterpack?#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/dadevel/xwin-starterpack?) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/dadevel/xwin-starterpack?) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/dadevel/xwin-starterpack?) to refresh your session.Dismiss alert

{{ message }}

[dadevel](https://github.com/dadevel)/ **[xwin-starterpack](https://github.com/dadevel/xwin-starterpack)** Public template

- [Notifications](https://github.com/login?return_to=%2Fdadevel%2Fxwin-starterpack) You must be signed in to change notification settings
- [Fork\\
2](https://github.com/login?return_to=%2Fdadevel%2Fxwin-starterpack)
- [Star\\
11](https://github.com/login?return_to=%2Fdadevel%2Fxwin-starterpack)


main

[**1** Branch](https://github.com/dadevel/xwin-starterpack/branches) [**0** Tags](https://github.com/dadevel/xwin-starterpack/tags)

[Go to Branches page](https://github.com/dadevel/xwin-starterpack/branches)[Go to Tags page](https://github.com/dadevel/xwin-starterpack/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![dadevel](https://avatars.githubusercontent.com/u/57419228?v=4&size=40)](https://github.com/dadevel)[dadevel](https://github.com/dadevel/xwin-starterpack/commits?author=dadevel)<br>[add x86 and arm64 support](https://github.com/dadevel/xwin-starterpack/commit/5e25be965e5aaa107618c21094ba352b157ce1ac)<br>last monthMar 29, 2026<br>[5e25be9](https://github.com/dadevel/xwin-starterpack/commit/5e25be965e5aaa107618c21094ba352b157ce1ac) · last monthMar 29, 2026<br>## History<br>[2 Commits](https://github.com/dadevel/xwin-starterpack/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/dadevel/xwin-starterpack/commits/main/) 2 Commits |
| [.devcontainer](https://github.com/dadevel/xwin-starterpack/tree/main/.devcontainer ".devcontainer") | [.devcontainer](https://github.com/dadevel/xwin-starterpack/tree/main/.devcontainer ".devcontainer") | [add x86 and arm64 support](https://github.com/dadevel/xwin-starterpack/commit/5e25be965e5aaa107618c21094ba352b157ce1ac "add x86 and arm64 support") | last monthMar 29, 2026 |
| [.vscode](https://github.com/dadevel/xwin-starterpack/tree/main/.vscode ".vscode") | [.vscode](https://github.com/dadevel/xwin-starterpack/tree/main/.vscode ".vscode") | [add x86 and arm64 support](https://github.com/dadevel/xwin-starterpack/commit/5e25be965e5aaa107618c21094ba352b157ce1ac "add x86 and arm64 support") | last monthMar 29, 2026 |
| [include](https://github.com/dadevel/xwin-starterpack/tree/main/include "include") | [include](https://github.com/dadevel/xwin-starterpack/tree/main/include "include") | [add x86 and arm64 support](https://github.com/dadevel/xwin-starterpack/commit/5e25be965e5aaa107618c21094ba352b157ce1ac "add x86 and arm64 support") | last monthMar 29, 2026 |
| [src](https://github.com/dadevel/xwin-starterpack/tree/main/src "src") | [src](https://github.com/dadevel/xwin-starterpack/tree/main/src "src") | [add x86 and arm64 support](https://github.com/dadevel/xwin-starterpack/commit/5e25be965e5aaa107618c21094ba352b157ce1ac "add x86 and arm64 support") | last monthMar 29, 2026 |
| [.gitignore](https://github.com/dadevel/xwin-starterpack/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/dadevel/xwin-starterpack/blob/main/.gitignore ".gitignore") | [add x86 and arm64 support](https://github.com/dadevel/xwin-starterpack/commit/5e25be965e5aaa107618c21094ba352b157ce1ac "add x86 and arm64 support") | last monthMar 29, 2026 |
| [LICENSE](https://github.com/dadevel/xwin-starterpack/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/dadevel/xwin-starterpack/blob/main/LICENSE "LICENSE") | [initial commit](https://github.com/dadevel/xwin-starterpack/commit/d4be471fa596e815fa9b15194f9061ac595b69bb "initial commit") | 6 months agoOct 30, 2025 |
| [Makefile](https://github.com/dadevel/xwin-starterpack/blob/main/Makefile "Makefile") | [Makefile](https://github.com/dadevel/xwin-starterpack/blob/main/Makefile "Makefile") | [add x86 and arm64 support](https://github.com/dadevel/xwin-starterpack/commit/5e25be965e5aaa107618c21094ba352b157ce1ac "add x86 and arm64 support") | last monthMar 29, 2026 |
| [README.md](https://github.com/dadevel/xwin-starterpack/blob/main/README.md "README.md") | [README.md](https://github.com/dadevel/xwin-starterpack/blob/main/README.md "README.md") | [add x86 and arm64 support](https://github.com/dadevel/xwin-starterpack/commit/5e25be965e5aaa107618c21094ba352b157ce1ac "add x86 and arm64 support") | last monthMar 29, 2026 |
| View all files |

## Repository files navigation

# xwin-starterpack

[Permalink: xwin-starterpack](https://github.com/dadevel/xwin-starterpack?#xwin-starterpack)

> Develop and debug Windows software on Linux with the power of [Clang](https://clang.llvm.org/) and [Xwin](https://github.com/jake-shadle/xwin/).

Install LLVM and OpenSSH in a Windows VM.

```
winget install --source=winget --id=LLVM.LLVM

Add-WindowsCapability -Online -Name OpenSSH.Server
[System.IO.File]::WriteAllLines('C:\ProgramData\ssh\administrators_authroized_keys', 'YOUR SSH PUBLIC KEY HERE', (New-Object System.Text.UTF8Encoding $false))
icacls.exe C:\ProgramData\ssh\administrators_authorized_keys /inheritance:r /grant Administrators:F /grant SYSTEM:F
New-ItemProperty -Path 'HKLM:\SOFTWARE\OpenSSH' -Name DefaultShell -Value 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' -PropertyType String -Force
Set-Service -Name sshd -StartupType 'Automatic'
Restart-Service sshd
```

Forward the ports used by LLDB from your Linux machine over SSH to the Windows VM.

```
ssh -L 127.0.0.1:1234:127.0.0.1:1234 -L 127.0.0.1:2345:127.0.0.1:2345 administrator@windev
```

Start the LLDB server on Windows.

```
mkdir C:\Build
cd C:\Build
& "C:\Program Files\LLVM\bin\lldb-server.exe" platform --server --listen 1234 --gdbserver-port 2345
```

Back on Linux open this project in Visual Studio Code and confirm the _Reopen in Container_ recommendation.

```
code .
```

When you are using Podman instead of Docker you need an additional environment variable.

```
DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock code .
```

That's it.
Now you are ready to go.

References:

- [Cross compiling Windows binaries from Linux](https://jake-shadle.github.io/xwin/)
- [Introducing the Universal CRT](https://devblogs.microsoft.com/cppblog/introducing-the-universal-crt/)
- [LLDB DAP](https://github.com/llvm/vscode-lldb)

## About

Windows C/C++ development environment on Linux


### Topics

[llvm](https://github.com/topics/llvm "Topic: llvm") [vscode](https://github.com/topics/vscode "Topic: vscode") [xwin](https://github.com/topics/xwin "Topic: xwin")

### Resources

[Readme](https://github.com/dadevel/xwin-starterpack?#readme-ov-file)

### License

[MIT license](https://github.com/dadevel/xwin-starterpack?#MIT-1-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/dadevel/xwin-starterpack?).

[Activity](https://github.com/dadevel/xwin-starterpack/activity)

### Stars

[**11**\\
stars](https://github.com/dadevel/xwin-starterpack/stargazers)

### Watchers

[**0**\\
watching](https://github.com/dadevel/xwin-starterpack/watchers)

### Forks

[**2**\\
forks](https://github.com/dadevel/xwin-starterpack/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fdadevel%2Fxwin-starterpack&report=dadevel+%28user%29)

## [Releases](https://github.com/dadevel/xwin-starterpack/releases)

No releases published

## [Packages\  0](https://github.com/users/dadevel/packages?repo_name=xwin-starterpack)

No packages published

## [Contributors\  1](https://github.com/dadevel/xwin-starterpack/graphs/contributors)

- [![@dadevel](https://avatars.githubusercontent.com/u/57419228?s=64&v=4)](https://github.com/dadevel)[**dadevel** Daniel](https://github.com/dadevel)

## Languages

- [Makefile48.4%](https://github.com/dadevel/xwin-starterpack/search?l=makefile)
- [Dockerfile44.4%](https://github.com/dadevel/xwin-starterpack/search?l=dockerfile)
- [C++7.2%](https://github.com/dadevel/xwin-starterpack/search?l=c%2B%2B)

You can’t perform that action at this time.