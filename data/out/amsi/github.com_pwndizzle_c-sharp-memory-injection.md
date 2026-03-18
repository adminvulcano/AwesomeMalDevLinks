# https://github.com/pwndizzle/c-sharp-memory-injection

[Skip to content](https://github.com/pwndizzle/c-sharp-memory-injection#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/pwndizzle/c-sharp-memory-injection) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/pwndizzle/c-sharp-memory-injection) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/pwndizzle/c-sharp-memory-injection) to refresh your session.Dismiss alert

{{ message }}

[pwndizzle](https://github.com/pwndizzle)/ **[c-sharp-memory-injection](https://github.com/pwndizzle/c-sharp-memory-injection)** Public

- [Notifications](https://github.com/login?return_to=%2Fpwndizzle%2Fc-sharp-memory-injection) You must be signed in to change notification settings
- [Fork\\
80](https://github.com/login?return_to=%2Fpwndizzle%2Fc-sharp-memory-injection)
- [Star\\
321](https://github.com/login?return_to=%2Fpwndizzle%2Fc-sharp-memory-injection)


master

[**1** Branch](https://github.com/pwndizzle/c-sharp-memory-injection/branches) [**0** Tags](https://github.com/pwndizzle/c-sharp-memory-injection/tags)

[Go to Branches page](https://github.com/pwndizzle/c-sharp-memory-injection/branches)[Go to Tags page](https://github.com/pwndizzle/c-sharp-memory-injection/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![pwndizzle](https://avatars.githubusercontent.com/u/2359033?v=4&size=40)](https://github.com/pwndizzle)[pwndizzle](https://github.com/pwndizzle/c-sharp-memory-injection/commits?author=pwndizzle)<br>[Update iat-injection.cs](https://github.com/pwndizzle/c-sharp-memory-injection/commit/99b1657c41dccc889996158e4aacff0ec51533cf)<br>9 years agoNov 5, 2017<br>[99b1657](https://github.com/pwndizzle/c-sharp-memory-injection/commit/99b1657c41dccc889996158e4aacff0ec51533cf) · 9 years agoNov 5, 2017<br>## History<br>[24 Commits](https://github.com/pwndizzle/c-sharp-memory-injection/commits/master/) <br>Open commit details<br>[View commit history for this file.](https://github.com/pwndizzle/c-sharp-memory-injection/commits/master/) 24 Commits |
| [README.md](https://github.com/pwndizzle/c-sharp-memory-injection/blob/master/README.md "README.md") | [README.md](https://github.com/pwndizzle/c-sharp-memory-injection/blob/master/README.md "README.md") | [Update README.md](https://github.com/pwndizzle/c-sharp-memory-injection/commit/4dfab3bec70b3b9f2f47ac69a17128a78e2d729a "Update README.md") | 9 years agoNov 5, 2017 |
| [apc-injection-any-process.cs](https://github.com/pwndizzle/c-sharp-memory-injection/blob/master/apc-injection-any-process.cs "apc-injection-any-process.cs") | [apc-injection-any-process.cs](https://github.com/pwndizzle/c-sharp-memory-injection/blob/master/apc-injection-any-process.cs "apc-injection-any-process.cs") | [Create apc-injection-any-process.cs](https://github.com/pwndizzle/c-sharp-memory-injection/commit/7a6e0131fbbe0f06d64b520c2d46c6a6f298f6f1 "Create apc-injection-any-process.cs") | 9 years agoOct 4, 2017 |
| [apc-injection-new-process.cs](https://github.com/pwndizzle/c-sharp-memory-injection/blob/master/apc-injection-new-process.cs "apc-injection-new-process.cs") | [apc-injection-new-process.cs](https://github.com/pwndizzle/c-sharp-memory-injection/blob/master/apc-injection-new-process.cs "apc-injection-new-process.cs") | [Rename apc-inject-new-process.cs to apc-injection-new-process.cs](https://github.com/pwndizzle/c-sharp-memory-injection/commit/4845f22874806904f71160b8e5bd52748ac2a636 "Rename apc-inject-new-process.cs to apc-injection-new-process.cs") | 9 years agoOct 4, 2017 |
| [iat-injection.cs](https://github.com/pwndizzle/c-sharp-memory-injection/blob/master/iat-injection.cs "iat-injection.cs") | [iat-injection.cs](https://github.com/pwndizzle/c-sharp-memory-injection/blob/master/iat-injection.cs "iat-injection.cs") | [Update iat-injection.cs](https://github.com/pwndizzle/c-sharp-memory-injection/commit/99b1657c41dccc889996158e4aacff0ec51533cf "Update iat-injection.cs") | 9 years agoNov 5, 2017 |
| [process-dll-injection.cs](https://github.com/pwndizzle/c-sharp-memory-injection/blob/master/process-dll-injection.cs "process-dll-injection.cs") | [process-dll-injection.cs](https://github.com/pwndizzle/c-sharp-memory-injection/blob/master/process-dll-injection.cs "process-dll-injection.cs") | [Update process-dll-injection.cs](https://github.com/pwndizzle/c-sharp-memory-injection/commit/9e549f3ac109a6362a6acdeefdd64d6dbc7bb02f "Update process-dll-injection.cs") | 9 years agoOct 1, 2017 |
| [thread-hijack.cs](https://github.com/pwndizzle/c-sharp-memory-injection/blob/master/thread-hijack.cs "thread-hijack.cs") | [thread-hijack.cs](https://github.com/pwndizzle/c-sharp-memory-injection/blob/master/thread-hijack.cs "thread-hijack.cs") | [Create thread-hijack.cs](https://github.com/pwndizzle/c-sharp-memory-injection/commit/225a2c8999b3ae3b6d98e7a190fdb2b5373bb116 "Create thread-hijack.cs") | 9 years agoSep 30, 2017 |
| View all files |

## Repository files navigation

# C\# Memory Injection Examples

[Permalink: C# Memory Injection Examples](https://github.com/pwndizzle/c-sharp-memory-injection#c-memory-injection-examples)

A set of scripts that demonstrate how to perform memory injection.

I've tried to make these techniques as simple and opsec safe as possible, avoiding unnecessary memory modifications, process or file creation. I'm no C# expert or memory injection guru so use these examples at your own risk :)

The shellcode used in the examples can be found below (there are also dll/exe versions too):

[https://github.com/peterferrie/win-exec-calc-shellcode](https://github.com/peterferrie/win-exec-calc-shellcode)

### Contents

[Permalink: Contents](https://github.com/pwndizzle/c-sharp-memory-injection#contents)

- apc-injection-any-process.cs - APC injection using QueueAPC into a currently running remote process. This method relies on the threads within the process entering an alertable state.

- apc-injection-new-process.cs - APC injection using QueueAPC into a newly created process. As the threads of a newly created process will be alertable its easier to trigger APC usage with this technique, although you will generate a new process.

- iat-injection.cs - Modify a specific import pointer for a target function within a specific process to point to shellcode before continuing to execute the legitimate function.

- process-dll-injection.cs - Classic dll injection where the path to a dll on disk is injected in a running process and then loaded with a call to CreateRemoteThread passing LoadLibrary and the dll path.

- thread-hijack.cs - This example suspends a thread within a running process, injects shellcode in the process and redirects execution of an existing thread to the shellcode. Once the shellcode is executed the thread will continue as before.


## About

A set of scripts that demonstrate how to perform memory injection in C#


### Resources

[Readme](https://github.com/pwndizzle/c-sharp-memory-injection#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/pwndizzle/c-sharp-memory-injection).

[Activity](https://github.com/pwndizzle/c-sharp-memory-injection/activity)

### Stars

[**321**\\
stars](https://github.com/pwndizzle/c-sharp-memory-injection/stargazers)

### Watchers

[**11**\\
watching](https://github.com/pwndizzle/c-sharp-memory-injection/watchers)

### Forks

[**80**\\
forks](https://github.com/pwndizzle/c-sharp-memory-injection/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fpwndizzle%2Fc-sharp-memory-injection&report=pwndizzle+%28user%29)

## [Releases](https://github.com/pwndizzle/c-sharp-memory-injection/releases)

No releases published

## [Packages\  0](https://github.com/users/pwndizzle/packages?repo_name=c-sharp-memory-injection)

No packages published

## [Contributors\  1](https://github.com/pwndizzle/c-sharp-memory-injection/graphs/contributors)

- [![@pwndizzle](https://avatars.githubusercontent.com/u/2359033?s=64&v=4)](https://github.com/pwndizzle)[**pwndizzle** Alex Davies](https://github.com/pwndizzle)

## Languages

- [C#100.0%](https://github.com/pwndizzle/c-sharp-memory-injection/search?l=c%23)

You can’t perform that action at this time.