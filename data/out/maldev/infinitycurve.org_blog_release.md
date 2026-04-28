# https://www.infinitycurve.org/blog/release

[Havoc Professional](https://www.infinitycurve.org/blog/tag/havoc%20professional) [Kaine-kit](https://www.infinitycurve.org/blog/tag/kaine-kit) [release](https://www.infinitycurve.org/blog/tag/release)

# Havoc Professional Release

The initial release of the long awaited Havoc Professional and the Kaine-kit is finally here and new team member.

![Paul Ungur](https://www.infinitycurve.org/_next/image?url=%2Fimages%2FPaul.png&w=48&q=75)Paul Ungur

February 20, 2026

![Havoc Professional Release](https://www.infinitycurve.org/_next/image?url=%2Fimages%2Fblog%2Frelease%2Fbanner.png&w=3840&q=75)

### Introduction

Since our last introduction blog post of the Havoc Professional framework and the kaine-kit, we have refined the framework behind the scenes, added many necessary features that operators depend on to navigate hardened environments, while matching the capabilities of numerous current competing vendors.

Another major announcement is that we have a new team member joining us: [Iker M.](https://x.com/avx128), who has been developing exciting new technologies and techniques for us since last year september (Evasion Tactics, Allure, and more). We're going to cover some of these features in this post!

### Enhanced User Interface and Design Philosophy

The user interface has undergone a significant redesign, particularly with the default theme. We've moved away from the Dracula theme used in the older Havoc Framework client, opting instead for a custom aesthetic that reflects our new direction and identity.

![Switching of C2 Listener configuration at runtime](https://www.infinitycurve.org/images/blog/release/lookfeel-1.png)![Switching of C2 Listener configuration at runtime](https://www.infinitycurve.org/images/blog/release/lookfeel-2.png)![Switching of C2 Listener configuration at runtime](https://www.infinitycurve.org/images/showcase-5.png)

The client features a flexible docking system that allows widgets to be freely repositioned according to operator preference, or set to float independently.

### Encrypted DNS - DoH and DoT Support

Kaine supports traditional DNS but now also DNS over HTTPS (DoH) and DNS over TLS (DoT) protocols, expanding the arsenal of covert communication channels available to operators. These protocols leverage standard HTTPS (port 443) and TLS-encrypted DNS (port 853) services commonly provided by major DNS providers such as Google, Cloudflare, and Quad9.

![DNS (DNS over TLS) Listener](https://www.infinitycurve.org/images/blog/release/dns-over-tls.png)

This multi protocol approach enables a layered operational strategy where DNS-based channels serve as the initial, low signature entry point for establishing persistence and conducting reconnaissance.

### Runtime Channel Switching

A feature has been introduced to kaine that allows operators to dynamically update a session's listener configuration at runtime.

![Switching of C2 Listener configuration at runtime](https://www.infinitycurve.org/images/blog/release/switch-c2-config.png)

This capability enables operators to reconfigure an existing session to connect to a new listener with updated parameters, allowing for seamless transitions to fresh infrastructure and profiles that utilize clean domains, effectively pivoting away from compromised or burned infrastructure without disrupting the session.

![Switching of C2 channel protocols](https://www.infinitycurve.org/images/blog/release/switch-c2-channel.png)

Additionally, sessions can switch between entirely different listener protocols at runtime, such as transitioning from HTTP to SMB or vice versa, regardless of whether the listener is configured as P2P or Direct. This provides operators with the flexibility to adapt their communication channels based on operational requirements and environmental constraints, all without spawning a new agent session on the host.

Runtime channel switching also extends to DNS-based protocols, allowing operators to seamlessly upgrade implants between traditional DNS, DNS over HTTPS (DoH), and DNS over TLS (DoT) based on network conditions and stealth requirements. This flexibility enables tactical transitions, such as establishing initial low-profile communication over DNS before switching to HTTP for bandwidth-intensive operations like file downloads or SOCKS proxy tunneling.

### Async Beacon Object Files

Kaine provides full support for Asynchronous Beacon Object Files, a recent enhancement to the BOF ecosystem introduced through collaboration between Outflank, MDSec, and Fortra. If you are not aware, Async BOFs allow object files to run in the background as persistent monitoring tasks, enabling long-running operations without blocking the agent's main execution thread.

For a comprehensive understanding of Async BOF design and implementation, refer to the official Outflank blog post: [Async BOFs – "Wake Me Up, Before You Go Go"](https://www.outflank.nl/blog/2025/07/16/async-bofs-wake-me-up-before-you-go-go/). In short, async BOFs run in the background and can trigger the core beacon to wake up from its sleep to send back an event to the TeamServer or client that issued the async BOF.

![Async BOF](https://www.infinitycurve.org/images/blog/release/async-bof.png)

The agent can be woken up through the `BeaconWakeup` API, while the operator can issue a stop signal to the async BOF to halt execution and shut down safely while cleaning up any resources it has allocated during its runtime by simply checking whether the returned event handle from `BeaconGetStopJobEvent` has been signaled.

The scripting capability of Havoc allows operators to capture any events triggered and received from the async beacon object file to properly react to them.

![Process Notify](https://www.infinitycurve.org/images/blog/release/capture-event.png)

The `notify_callback` has been registered by the Havoc client to capture any beacon output from the async object file, while also capturing the associated output types, the task-id, and the callback-uuid associated with the output being redirected from the TeamServer to the client.

![Process Notify](https://www.infinitycurve.org/images/blog/release/process-notify.png)

We have released several example Async BOFs demonstrating real-world applications:

- [process-notify](https://github.com/InfinityCurveLabs/process-notify): Monitors and notifies on specific process creations and executions
- [userlogon-notify](https://github.com/InfinityCurveLabs/userlogon-notify): Monitors and notifies on user logon events

These examples showcase how Async BOFs enable proactive monitoring and event-driven operations. Since they are based on the standardized format from Outflank, Fortra, and MDSec, Async BOFs written for those platforms can be run under Havoc as well without spending much time porting the code (as far as we assume and are aware).

### Adaptive Beacon Object Files

Another capability that the Kaine object file loader provides is the proxying and execution of Win32 APIs without requiring any callstack spoofing functions to be used directly within the Beacon Object File. This allows existing object files from TrustedSec, Outflank, and other developers to naturally run with the agent's current applied evasion capabilities.

![Object Execute](https://www.infinitycurve.org/images/blog/release/object-execute.png)![Object Function Call Spoof](https://www.infinitycurve.org/images/blog/release/object-spoof.png)

The object file loader also utilizes additional extensions that modify or change the way payload memory is allocated, allowing external extensions to define how executable memory is allocated for features and Beacon Object Files. This gives operators control over every step and behavior of the execution process.

### Backwards Compatible and Stable

One of our strongest focuses has been maintaining robust backwards compatibility while ensuring stability across Windows versions without instability or crashes. The agent has been tested across numerous Windows versions, starting from Windows XP and legacy Windows Servers to modern systems such as Windows 11 and current Windows Server releases, with tests against Endpoint Security Products to ensure stability and low detection rates.

Each of our features has been tested on multiple versions to ensure stability while offering broad support, including legacy Windows systems, in case operators receive a callback from systems such as Windows XP within a network.

![Backwards Compatible](https://www.infinitycurve.org/images/blog/release/backwards-xp.png)

### Extensions - Embedded and Dynamically Loaded

A key advantage of the kaine-kit is its collection of extensions that alter the agent's behavior by applying evasion capabilities at runtime or extending the agent with additional commands and features such as SOCKS proxy, process management, filesystem interaction, and more. These extensions can be loaded at any time during runtime or statically linked into the binary at build time, giving operators full control over which features are available in the agent at any given moment.

Extensions can be embedded directly into the agent binary during compilation, ensuring critical capabilities are available from the moment of execution.

![Statically Link Extension](https://www.infinitycurve.org/images/blog/release/extension-static.png)

Extensions can also be loaded dynamically during any active agent session, allowing operators to upgrade sessions with additional features and commands such as stack spoofing or filesystem management without redeployment.

![Dynamically Loaded Extension](https://www.infinitycurve.org/images/blog/release/extension-dynamic.png)

### PowerShell? I like it (Power)Safe!

Another feature introduced to the kaine-kit collection is PowerSafe, a modern approach to performing unmanaged PowerShell execution. Unlike traditional implementations such as PowerPick, which rely on loading a .NET assembly to execute PowerShell scripts.

PowerSafe takes a different approach entirely, executing PowerShell fully natively by resolving all necessary PowerShell execution environments, objects, and classes to prepare the execution environment, while disabling all security features: Antimalware Scan Interface (AMSI), Script Block Logging, Module Logging, Transcription, Execution Policy, and Constrained Language Mode (CLM).

![PowerSafe execution demonstration](https://www.infinitycurve.org/images/blog/release/powersafe.png)

This feature is based upon the [PowerChell](https://github.com/scrt/PowerChell) project by [itm4n](https://itm4n.github.io/), which we recommend checking out for further technical details.

### Firebeam Preview

In our last post, we mentioned a new feature called Firebeam. Since that announcement, we have made numerous iterations to ensure it is as easy to work with as possible. Our future goal is to port existing tooling over to Firebeam without any modifications or recompilations from source. While we work toward this objective, we have ensured that development for the Firebeam VM is as straightforward as possible.

![Firebeam Compile with LLVM bitcode](https://www.infinitycurve.org/images/blog/release/firebeam-compile.png)

The process of taking a generated executable and transpiling it to bytecode follows the steps illustrated below:

![Firebeam Diagram](https://www.infinitycurve.org/images/blog/release/firebeam-steps.png)

Once the bytecode has been generated and executed on the Firebeam VM, additional features such as runtime Win32 proxying are applied depending on the installed extensions and features. In this case, Firebeam utilizes function proxy execution through the registered Stack Spoofing Extension.

![Firebeam Function Proxying](https://www.infinitycurve.org/images/blog/release/firebeam-proxy.png)![Firebeam Bytecode Execution](https://www.infinitycurve.org/images/blog/release/firebeam-execute.png)

The output generated by the Firebeam bytecode is printed to the console after execution completes.

Now that we have developed a closer look at Firebeam and established a properly scalable solution for ourselves and our customers, we will continue working on it to make development and debugging easier and more streamlined.

### Extensive Support For Existing Tooling

We want to emphasize in this blog post that we value the R&D time spent by red teams and understand that not many have the privilege to either outsource it or have an internal team. Hence, we have made it our mission to add extensive support for existing tools and will continue adding support for vendor-specific features and tooling in the future by taking advantage of our own modular architecture. For example, we provide additional support for Beacon Object Files on older Windows systems without the need to recompile them from source with the necessary patches to function in legacy environments such as Windows XP.

![Whoami BOF on Windows XP](https://www.infinitycurve.org/images/blog/release/winxp-whoami.png)![TrustedSec Warning](https://www.infinitycurve.org/images/blog/release/trustedsec-warning.png)

Numerous publicly available and existing Beacon Object Files from Outflank, Cobalt Strike (Fortra), and TrustedSec work without any issues or recompilations, as we utilize the "standardized" Beacon API. The only necessary change is ensuring a proper Python script is written for the Havoc client to understand how to pack the arguments and invoke the BOF.

We have already started porting some customer favorites and well-known beacon object files under our GitHub organization and plan to continue adding kaine-specific scripts to public and popular BOF repositories:

- [CS-Situational-Awareness-BOF](https://github.com/InfinityCurveLabs/CS-Situational-Awareness-BOF)
- [CS-Remote-OPs-BOF](https://github.com/InfinityCurveLabs/CS-Remote-OPs-BOF)
- [nanodump](https://github.com/InfinityCurveLabs/nanodump)
- [No-Consolation](https://github.com/InfinityCurveLabs/No-Consolation)
- [C2-Tool-Collection](https://github.com/InfinityCurveLabs/C2-Tool-Collection)
- [UAC-BOF-Bonanza](https://github.com/InfinityCurveLabs/UAC-BOF-Bonanza)

and more! Please have a look, and thanks a lot to [Iker M.](https://x.com/avx128) for porting some of those BOFs to the Kaine agent by providing required python scripts.

### Callstack Spoofing Extension

As mentioned in previous sections, one of the most significant feature requests and now a requirement in modern evasion tactics for operating against modern defenses is callstack spoofing. We designed our core implant with the idea that any function can be proxied, hooked, or altered at runtime by external extensions, which the Callstack Spoofing extension utilizes to spoof Win32 functions at runtime.

![Callstack Spoofing configuration](https://www.infinitycurve.org/images/blog/release/spoofing-config.png)

Currently, the extension supports two modes of callstack spoofing. The first is Desync, which desynchronizes the unwinding from real control flow, completely hiding the original callstack and restoring the original stack afterwards. The second is Synthetic, which generates a legitimate-looking call stack by truncating the real call stack and inserting a fabricated stack frame chain.

Operators can configure the method, gadget location, and user-defined callstack that are applied while calling any Win32 function API.

![Callstack Spoofing configuration](https://www.infinitycurve.org/images/blog/release/spoofing-action.png)

As displayed, these techniques not only apply configured callstack frames but have also been properly tested across various Windows versions and legacy systems such as Windows XP.

We plan to add additional callstack spoofing-related features to allow fine-tuning and to enable inserting function entries into the callstack of the current process to simulate a more normal function execution flow that typically occurs.

### ALLURE - A bin2bin obfuscator

Last year, we had been thinking of a way to address future static detections of our tradecraft. This was a problem worth solving to us because it seemed the status quo was still sleepmasks, or in some circles, byte replacements - two fundamentally flawed approaches.

One approach that seemed obvious at the time was to simply write our own LLVM based obfuscator (there are many open source projects and examples of how LLVM can be leveraged for obfuscation), however we found it to be quite limiting. It simply isn't suited for our goals and ambitions; LLVM operates behind layers of abstractions that have no real concept of the final binary layout such as relocations, offsets or the final addressing within the binary. These limitations on what can be done from within a pass will for the most part directly trickle down into a need for external scripts to patch things in. All in all, we felt LLVM wasn't the right foundation, so we decided to go with a custom bin2bin approach.

The main focus was raising the effort of writing static detections, without compromising on size, stability, or runtime. Unlike commercial grade protectors, hindering analysis was secondary. Preserving the semantics of the original code was a hard requirement; as even the slightest mistake can snowball into undefined behavior.

![Showcasing obfuscation done by allure](https://www.infinitycurve.org/images/blog/release/allure-showcase-1.png)

#### Call To Security Product Vendors

We are actively working to establish collaborative partnerships with security product vendors to ensure our products cannot be misused by threat actors or malicious groups, protecting organizations from potential harm.

If you are a security product vendor and a rogue license and or implant is found in the wild with the strong assumption that it is not a red team but rather getting abused by an Threat Actor, then we kindly ask to [contact us](https://www.infinitycurve.org/contact-us) immediately and report the binaries so we can revoked and invalidate the license associated with the binaries to avoid further damage being caused.

### History, Future Plans, and Closing Thoughts

With this official release, we will be archiving the Havoc Framework project on GitHub. Similar to how Armitage served as a stepping stone in the evolution of Cobalt Strike, Havoc Framework began as a sandbox project that rapidly evolved over time. However, due to its limited design architecture, we recognized the need for a complete rewrite from the ground up to address modern operational use cases and meet the high demand from red teams requiring more reliable and sophisticated tooling in an ever-changing threat landscape.

We have implemented only half of the features on our roadmap, and this marks just the beginning. The modular and plugin-driven architecture of the entire framework enables us to rapidly deploy new features through our ICPM updater (InfinityCurve Package Manager) and address bugs in a streamlined manner.

Havoc Professional and the Kaine-kit are sold under a [single license](https://www.infinitycurve.org/pricing). Our products are exclusively available to established red team companies with a minimum of four years of experience and operational history, ensuring our solutions are in the hands of seasoned professionals. We intentionally limit the number of client slots to maintain the low detection rates our customers depend on, preserving the integrity and effectiveness of our tools. This selective approach also allows us to allocate our internal resources toward continuous research and development.

If your organization is interested in acquiring Havoc Professional licenses, [contact us](https://www.infinitycurve.org/contact-us).