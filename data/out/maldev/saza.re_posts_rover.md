# https://saza.re/posts/rover/

## Contents

# Project ROVER

[lldre](https://github.com/lldre "Author")

June 14, 2026 2664 words
13 minutes

Contents

# A Different Approach to Red Team Tool Design

Over the past three years, I’ve been working on a red team C2 framework. Not because I needed it for red team operations, but because I wanted to explore a different design philosophy than what I was seeing in commercial red team tools. I ended up spending about 1200 hours building the backing framework before writing a single line of actual red team or c2 server functionality. Because in my mind, for malware: longevity > immediate gain and obfuscation > functionality.

Over the past 12 years I’ve looked extensively at a wide range of malware. Fancy APT backdoors, bootkits, ransomware and some good old commercial red team tools like Cobalt Strike, Nighthawk, Brute Ratel, Havoc, etc. Each malware had their own defining features and characteristics, things they did well and things they did… less well. One thing that recently started to stand out to me however, was how the design philosophy behind the commercial red team tools and commercial malware were completely opposite, while one would think they face some of the same _existential_ problems.

Malware developers building malware for infecting systems at scale design their malware to withstand detection for at least a day or two. This usually gives enough time to execute a campaign. Additionally, they design it in a way that they can effortlessly scramble their malware so it is undetected again for the next campaign. This design is the mold into which they have to fit their malware’s functionality.

Commercial red team tooling, however, seem to all take a different approach. They’re almost enterprise-software-like in their design. They look like they’re a bunch of scripts being held together with 500 bandaids. Bandaids that are reactions to the ever increasing scrutiny of their tools and the resulting detections that happen. Eventually they’re more occupied with building evasion than with building functionality. I can’t help but think these tools all started out as a collection of internally developed tools for their own red team exercises and were eventually packaged for sale. When tools are used by a total of 3 red team operators, the toolset isn’t likely to be scrutinized by researchers, but when you start selling your tools and hundreds, or even thousands, of red team operators are starting to use your tool, you most definitely will start hitting some holes in the road.

These origins would explain the difference in design between commercial malware and commercial red team tools. But in the end, they’re both built to deliver undetected intrusion functionality, so why the discrepancy? This is what I set out to figure out, what if we develop a red team tool designed with a stealth first approach. Built to automatically evade where 90% of detections happen so we can focus on building functionality and beating the remaining 10%.

Now I want to say that I don’t hate on these tools, they’re selling like hot cakes for a reason. They do the job and they do it well, and that is all that counts. But the malware researcher in me can’t help but wonder, what it would look like if we took the malware development approach to a red team tool?

_no llms were used during the development of this tool. just endless suffering by myself_

## The Design

When considering the design I wanted to reverse engineer back from the endpoint detection system (EDR). How do we consistently and effortlessly evade EDR (that’s definitely a question that hasn’t been asked before)? Well, to figure that out I had to tap into some previous research I did with Northwave (of which the technical details might release soon). We spent a few years researching how to effectively redeploy existing malware for [Adversary Emulation](https://northwave-cybersecurity.com/articles/combining-red-team-simulations-with-adversary-emulation). During this research, one of the key problems we ran into, naturally, was the malware being detected by EDR. The problem with EDR detections is that they have dozens of moving parts that are all fairly black-box. So, in order for us to figure out why our existing malware was being detected, we had to to find a way to isolate the different parts. The methodology we came up with uses techniques that enable or disable different parts of the detection chain.

- First check all static signatures, by smartly disabling the emulator. Then, knowing it will pass the static signature check, we can verify the emulator detection by smartly disabling the step after emulation. This way, if we get a detection hit, we know it has to have happened during emulation. Lastly, for each different step, there are specific ways of isolation exactly where that step triggered a detection rule. For on-system malware detection (only related to the file and code, not to how the operator uses it) you get roughly the following steps that are important:

1. Static
a. The second an unknown file presents itself to the system or flies over the network, several different types of static signatures and rules are applied to it to check for known bad. These signatures could be hashes, metadata based, function signatures, string signatures, etc. They’re applied to the file while it is not yet running.
2. Emulation
a. If the file is executable and unknown, the file likely enters one of the AV’s emulators. The binary is started, given a virtualized and sandboxed environment (file system, memory, etc) to run in. These emulators are usually given small amounts of time and resources to perform their task. Their task is to get the malware in a running state and see if any of their static or dynamic signatures hit, without having to run it on the actual system. When a certain maliciousness threshold is hit, or if certain settings are set, the malware gets sent off to a cloud sandbox where more resources are given to perform the same task. If the maliciousness score is too high, it gets blocked outright.
3. Dynamic
a. If we pass those checks we are allowed to run the file on the actual system, but the EDR’s task doesn’t stop here. The endpoint protection will now perform things like runtime API hooking, running inspections on newly created RWX memory, ETW monitoring, etc. While the ETW and API hooking is dynamic, static signatures are also still applied in the dynamic state. When malware runs, new memory regions are created to which static signatures can be applied. This is (probably) why sleep masks were created!
4. And beyond
a. Then we get some machine learning stuff, SOC monitoring and other stuff which I don’t really consider in scope for this blog.

During this research we made some important realisations. First off we realised how pretty much all APT malware is detected only during the static step. Change a byte here or there and entire APT malware chains become undetected again. Then, we also realised how, in general, malware is by far mostly detected by static bytepattern signatures, hashes, string signatures and signatures applied to memory when new executable memory is created without a backing file. Consequently, when building stealthy malware, it is these things that need to be a high priority target for effortless evasion in the malware’s design.

There are other detection points related to behavioral analysis and specific API call patterns, but those tend to be more about what you do with the tool rather than the tool itself. That’s (mostly) something for the operator to deal with.

When I based the design on these detection realities rather than on operational requirements, I came up with the following core principles:

- **Minimize signaturable surface area**: The visible implant code should use minimal to no visible API calls and contain no strings.

- **Per-compile “polymorphism”**: Every build should be completely different at the binary level. All keys, identifiers, numeric constants, some strings and even the layout of each function in assembly should get completely changed with each compile. Jinja+++++

- **Non-executable memory component execution**: As created executable memory is a detection hotspot, we should be using as little of it as possible. This should greatly reduce exposure of the dynmically loaded malicious components like BOFs and most built-in functionality.

- **Position independence**: Everything needs to be position independent code so it can be run or injected anywhere without modification or relocation.

- **Platform Agnostic**: The implant’s base code should be platform agnostic, running on anything from Windows to Mac to edge devices.

- **Extensive Coupling**: Implant code and configuration data live in separate files. Modules and BOF code should also have separatable code and data. These two files should be extensively coupled, so that one cannot be used without the other from the same compile. Then, decryption keys should be build specific and be split between the server, data and code files. Requiring all three from the same build to run the malware. Coupling of data and code makes it harder to analyze individual components in isolation. A code file dump uploaded to virustotal won’t function with another data file found from a different compile. Getting code and data files from an attack while not having the encryption key part from the server, would still make it near impossible to perform analysis (if the crypto is implemented correctly….).

- **AI-aware design**: This was speculative, but I wanted to avoid patterns that would be common in malware training datasets consumed by the big LLMs. Most malware in public datasets consists of C/C++ code targeting x86/x64 Windows, so I made some architectural choices to deviate from that norm where possible.


## Building and Testing

The implementation design included a custom BOF execution system with no RWX memory, the “polymorphic” compilation system, and the advanced coupling of binaries, modules and servers.

For BOFs specifically, I wanted to drop the whole embedded BOF loader that other tools use, as this is unnecessary additional attack surface. I also wanted to have each BOF be completely encrypted in memory, always, without the use of sleep masks (which add additional detection attack surface). Lastly, the design for the BOF system should remove any limitations that the current BOF implementation has, which makes development a hassle. Ideally you just have AI generate some bofslop and it all magically works without being detected.

Building the tool this way meant I could hopefully more easily add features later without worrying much about detection. After 3 years, the project ended up being about 15,000 lines of code across five different programming languages. I used different languages for different parts based on what each language handles well.

Building the foundation was extremely challenging. The tool, by design, has many interconnected components that all need to work together in tandem. When I needed to modify one part, it often meant updating several other parts to maintain compatibility. All the while adhering to my design principles like reducing attack surface. I’ve spent weeks implementing one thing in one system only to realize some foundational changes needed to be made in other systems. In addition to that, debugging across multiple languages relying on each other, and often using some dirty techniques, was also not easy. I’ve probably written 70000 lines of code to end up at the 15000 lines of the pure weaponized curiosity that I have right now. On the contrary, the interconnectedness of the parts that made development troublesome, should translate to greatly increased difficulty when analysing the tool.

Recently I finally reached a few major milestones:

- **Non-executable memory execution**: Executing BOF files without allocating executable memory, while keeping the BOF files fully encrypted at all parts of of its lifetime

- **Compile-time binding**: All the components from a single build are cryptographically bound together so they only work with each other. If someone got one file and uploaded it to VirusTotal, they wouldn’t be able to analyze it without all the other files from that exact same build. Additionally, recompiling should make a significant amount of previous malware analysis automation work done on the tool obsolete.

- **Actual functionality**: And most recently getting the whole system to actually produce useful red team functionality. This was the first satisfying moment after 3 years of development, as it was the first time I had anything to show for my time. It moved from being a theoretical exercise to something that could potentially be used for actual work.


Throughout, because of the design, the tool couldn’t really be tested at all against AV. Not until all the pieces were completed and working together. This meant that I went on three years of development with no real validation that my design philosophu would work..

### Testing

When everything was finally ready, it was time to put my 3 year old theory to the test against a system running Microsoft Defender for Endpoint. I didn’t have very high expectations. This was the first build and had no additional obfuscation applied beyond what was built into the design.

I started the implant and connected it back to the C2 server. No alerts appeared and no entries showed up in the MDE timeline.

I used my custom shell to navigate the file system. Still no alerts or timeline entries.

Then, I started firing off BOFs (small excerpt below), one after the other. No alerts. No timeline entries. Is this thing even on?

Then, finally, the only detection event I was able to trigger was a single timeline entry for local account enumeration when I ran a `netuser` BOF. I have to assume this was behavioral matching done through ETW monitoring, as the same timeline entry showed up for many other legitimate processes. And in the end that’s just detecting what the operator does, not really the implant itself. The implant kept running normally and I could execute more BOFs afterward.

MDE timeline:

![/images/rover/image.png](https://saza.re/svg/loading.min.svg)

So, the non-executable memory BOF execution worked as designed. That was really encouraging, though it was just one test against one endpoint protection system. More future testing would be needed to draw broader conclusions.

Pretty cool to see it all come together after 3 years of isolated development in my free time.

## Conclusion

I’ve worked back from the problem at hand for deploying a red team tool at scale: detection. Others have worked forward from solving their immediate problem at hand: I need this functionality. Will their tools remain reliable in 2 years, when their user base grows further and their malware comes under more scrutiny? When they need to increase license prices by 20% a year to pay for the extra engineers to solve their detection issues? Who knows, maybe they will. I feel like with the advent of AI, we will see an increased reliance on advanced tools like this. And in the age of AI those tools will see a lot more usage (leading to more data for the defenders) and a lot more scrutiny, which again will be performed by AI. That’s why I was motivated to engineer something that was designed with that problem in mind, not focused on the functionality.

After a promising (three-year-long) first step, I’m not sure what I’m gonna do next yet.
**Would you be interested in a tool that has non executable memory BOF execution and the other features listed above?**
Or, are you content with what you currently use? **Let me know!**

## Small excerpt of tool output

```
>> ls
./
../
x.exe
>> cd ..
>> ls
./
../
DefenderDeploymentTool_Onboard_[redacted]/
DefenderDeploymentTool_Onboard_[redacted].zip
desktop.ini
folder/

>> bof_invoke ipconfig
BOF Response (1252 bytes):

Windows IP Configuration

   Host Name . . . . . . . . . . . . : [redacted]
   Primary Dns Suffix  . . . . . . . :
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No

Ethernet adapter Ethernet:

   Connection-specific DNS Suffix  . : [redacted]
   Description . . . . . . . . . . . : Microsoft
   Hyper-V Network Adapter
   Physical Address. . . . . . . . . : 38
```

Updated on June 14, 2026

Back \| [Home](https://saza.re/)

[Exception Hijacking](https://saza.re/posts/exception_hijack/ "Exception Hijacking")

[Back to Top](https://saza.re/posts/rover/# "Back to Top")[View Comments](https://saza.re/posts/rover/# "View Comments")