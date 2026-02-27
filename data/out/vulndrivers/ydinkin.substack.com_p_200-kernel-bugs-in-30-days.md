# https://ydinkin.substack.com/p/200-kernel-bugs-in-30-days

# [Yaron Dinkin](https://ydinkin.substack.com/)

SubscribeSign in

![User's avatar](https://substackcdn.com/image/fetch/$s_!qwjj!,w_64,h_64,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdf93ffd0-bc34-47dc-bef5-f67364a7cd9a_144x144.png)

Discover more from Yaron Dinkin

Subscribe

By subscribing, you agree Substack's [Terms of Use](https://substack.com/tos), and acknowledge its [Information Collection Notice](https://substack.com/ccpa#personal-data-collected) and [Privacy Policy](https://substack.com/privacy).

Already have an account? Sign in

# 100+ Kernel Bugs in 30 Days

### High-Scale Driver Vulnerability Research with Agent Swarms

[![Yaron Dinkin's avatar](https://substackcdn.com/image/fetch/$s_!qwjj!,w_36,h_36,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdf93ffd0-bc34-47dc-bef5-f67364a7cd9a_144x144.png)](https://substack.com/@ydinkin)[![Eyal Kraft's avatar](https://substackcdn.com/image/fetch/$s_!Ht_h!,w_36,h_36,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05827702-49bc-4ffe-8d86-657d8d1341b2_144x144.png)](https://substack.com/@eyalkraft)

[Yaron Dinkin](https://substack.com/@ydinkin) and [Eyal Kraft](https://substack.com/@eyalkraft)

Feb 23, 2026

9

2

4

Share

#### TL;DR

**We used AI agents to reverse engineer Windows kernel drivers to find zero-days. It worked better than expected. Which is bad.**

[![BSOD chaos in toyland](https://substackcdn.com/image/fetch/$s_!69zh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb80bdc16-283c-4636-acee-50b2a1ee40a6_1536x1024.png)](https://substackcdn.com/image/fetch/$s_!69zh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb80bdc16-283c-4636-acee-50b2a1ee40a6_1536x1024.png)

_(This blog post was written by hand, and edited with AI assistance.)_

Frontier LLMs have already proven themselves for security audits of open source projects. AI-powered researchers found tens _(maybe hundreds?)_ of critical CVEs human researchers missed for years.

[Eyal Kraft](https://open.substack.com/users/465243607-eyal-kraft?utm_source=mentions) and I had an even bigger concern: what about all those targets no one has _ever_ looked at? There are literally TBs of binaries running on millions of machines across the world no human researcher has ever bothered to look at. Most likely no one ever will.

We decided to put agent swarms to the test by building a simple harness to perform binary zero-day research at scale. We targeted Windows Kernel Drivers. Thousands of third-party `.sys` files ship on every OEM machine, each one cryptographically signed by both its vendor and MSFT, with questionable code quality.

To date, most security research and mitigation efforts around Windows drivers focused on intentionally malicious or rootkit-style drivers, binaries that expose unsafe APIs like `MmMapIoSpace` or raw MSR/port I/O as a deliberate backdoor. Microsoft’s [vulnerable driver blocklist](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/microsoft-recommended-driver-block-rules) and community projects like [LOLDrivers](https://www.loldrivers.io/) catalog these known-bad drivers and prevent them from being loaded. But this misses an entire class of vulnerabilities: unintentional memory corruption bugs inside otherwise legitimate drivers. These aren’t backdoors, but rather your garden-variety bugs written by legitimate vendors. No blocklist catches them because no one has ever audited their code, and preventing them from loading will prevent you from using your GPU, keyboard, or webcam.

To do this in a cost-effective manner, we built an autonomous platform that scrapes drivers from all over the internet, catalogs and labels them, decompiles them, and uses agent swarms to identify memory corruption vulnerabilities with minimal token use and maximum plain-old-python. By using SLMs for much of the analysis, the entire project cost us only **$600 USD**, roughly **$3 per analyzed target**.

From a dataset of over **1,873 binaries**, we found **521 potential vulnerabilities** across **158 unique driver binaries** from dozens of vendors. Of those, we manually confirmed and reported 15 to vendors including **Lenovo, Fujitsu, IBM, Intel, AMD, Silicom, NVIDIA, and Dell**. They were, unsurprisingly, unresponsive. Despite most confirming the vulnerability exists (screenshots and/or video proof was always provided), to date, only one vulnerability was patched and assigned a CVE ( [CVE-2025-65001](https://nvd.nist.gov/vuln/detail/CVE-2025-65001), we’d like to thank Fujitsu PSIRT for their handling of our submission).

It’s also important to note none of the PSIRTs saw it as their responsibility to alert MSFT of these vulnerable drivers to add them to the [vulnerable driver blocklist](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/design/microsoft-recommended-driver-block-rules) or revoke their certificate.

After 90+ days of responsibly waiting for a fix on all submissions, we are publishing the full set of analyzed driver hashes so defenders can check whether affected binaries are present in their environments. If you’re a vendor, customer, or security professional interested in more details, you’re welcome to contact us at [hi@hexaplex.ai](mailto:hi@hexaplex.ai).

### Methodology

Our flow runs a five-stage pipeline:

1. **Scrape:** We covered both the [MSFT update catalog](https://www.catalog.update.microsoft.com/), OEM sites, and public driver repositories. Overall, we collected **1,654 different drivers** across **1,873 unique binary versions**.


2. **Preprocess:** CAB extraction, PE metadata analysis, and catalog signature parsing. This stage computes hashes, identifies driver entry points, and ranks targets by attack surface indicators (IOCTL dispatch complexity, number of device objects, presence of `METHOD_NEITHER` handlers). To focus our analysis, we filtered out drivers requiring complex setups (mostly non USB/PCIe devices) and old versions (Sorry, WinXP users...).


3. **Analyze:** The core loop. For each target, we launch an audit harness _(today, we’d probably just use ClaudeCode / OpenClaw with custom skills)_. A council of LLM agents then iteratively audit the binary:


1. **Decompilation Agent** renames unnamed functions, deduces functionality, recovers dynamic calls, using contextual inference so auditors can follow the logic

2. **Attack Surface Agent** identifies functions worth auditing based on the decompiled code

3. **Code Audit Agent** inspects each target function for memory corruption bugs, walking the recovered call graph to understand data flow


Findings are written as structured JSON with bug type, severity, confidence, impact assessment, and the decompiled code path.

We used a mix of models via OpenRouter, optimizing for vulnerabilities per token rather than per-model accuracy. On average, each target costs roughly $3 in API calls.

4. **Virtualize:** _(This became the bottleneck once we had a queue of 100+ findings)._ We created a custom VM-based harness for loading drivers on kernel-debugged Windows machines controlled by agents. Some drivers require custom USB/PCIe devices we obviously don’t have on hand. We customized QEMU to expose virtual devices, and used LLMs to virtualize enough of the initialization handshake for drivers to load and expose their IOCTL interfaces.

5. **Validate:** Using our harness, we can iteratively create Python PoC scripts per finding, effectively performing guided fuzzing until the machine crashes. The BSOD crash dump is then analyzed to confirm the vulnerability indeed triggered correctly (we found many hallucinated reports where the fuzzer successfully caused a crash, without actually exploiting the finding - causing a sneaky false positive we had to debug manually).

6. **Report:** We manually validated the automated report, running our PoC script on a “real” Windows 11 machine and ensuring the vulnerability description is comprehensive and factually correct. We then submitted it to the PSIRT ourselves. Note that we did not actually weaponize most vulnerabilities into full LPE exploits, but instead gauged the likelihood of it being exploitable in real-world scenarios based on our experience.


Of the 1,654 drivers in our dataset, we selected **202 high-risk drivers** for full analysis based on preprocessing heuristics. The remaining drivers are queued for future passes.

### Results

#### Dataset overview

- Total binaries collected: 1,873

- Total unique drivers: 1,654

- Binaries analyzed: 202

- Total findings: 521

- Unique binaries with findings: 158

- Findings manually confirmed and reported: 15

- Vendors notified: 8

- CVEs assigned: 1 ( [CVE-2025-65001](https://nvd.nist.gov/vuln/detail/CVE-2025-65001))

- Total project cost: ~$600

- Cost per target: ~$3

- Cost per bug: ~$4


#### Bug type distribution

- Arbitrary Read: 144 (27.6%)

- Heap Overflow: 111 (21.3%)

- Other: 82 (15.7%)

- Integer Overflow: 33 (6.3%)

- Stack Overflow: 26 (5.0%)

- Arbitrary Write: 92 (17.7%)

- Use-After-Free: 22 (4.2%)

- Type Confusion: 11 (2.1%)


Arbitrary memory access bugs (read + write) account for **45.3%** of all findings, unsurprising given that IOCTL handlers routinely copy data between user and kernel buffers with no bounds checking. Most of those stem from either heap buffer mishandling or faulty deserialization logic.

#### Severity and confidence

- Critical: 149 (28.6%)

- High: 220 (42.2%)

- Medium: 149 (28.6%)

- Low: 3 (0.6%)


The agent provided severity and confidence ratings. **70.8%** of findings are rated High or Critical, with **78.7%** of findings having High confidence, 19.6% Medium, and only 1.7% Low.

#### False positive rate

After manual analysis, we estimate the false positive rate at approximately **60%** **of critical/high confidence findings**. Most are real code patterns where the bug exists but exploitation is impractical (e.g., an OOB read that can only leak padding bytes, or a write that requires special system conditions). Adjusting for this, we estimate **over 100 of the 521 findings** **represent genuinely exploitable user→kernel local privilege escalation** on current Windows 11 x64 systems.

#### Impact themes

To reduce hallucination rate, the agent was asked to propose maximum impact of vulnerability exploitation for each reported finding. The most common impact categories across findings (categories overlap, a single finding can cause both DoS and privilege escalation):

- **Denial of Service:** System crash via kernel bugcheck (BSOD). The dominant impact across nearly all findings, since any kernel memory corruption is at minimum a reliability issue.

- **Information Disclosure:** Kernel memory leak via uninitialized buffers or OOB reads, often sufficient for KASLR bypass.

- **Privilege Escalation:** Arbitrary kernel read/write primitives enabling token manipulation or kernel code execution.

- **Code Execution**: Heap overflow or use-after-free conditions exploitable for arbitrary kernel code execution via pool shaping.


#### Notable Vulnerability Patterns

As an example, AMD’s Crash Defender driver (`amdfendr.sys`) exposes a world-writable device that supports sending IOCTLs with proprietary operation codes. Those operations on the device access internal transport queue descriptors without proper size validations, allowing heap corruption. With pool grooming, this is a path to arbitrary kernel data access, or even kernel code execution. Even without it, it’s a reliable BSOD from any user account.

The driver ships on Windows AMD systems, including AWS EC2 Windows AMIs with AMD instances. meaning the attack surface extends to cloud workloads.

[![](https://substackcdn.com/image/fetch/$s_!TV9H!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fed217d79-22cd-45b3-adeb-5276c935546c_1192x266.png)](https://substackcdn.com/image/fetch/$s_!TV9H!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fed217d79-22cd-45b3-adeb-5276c935546c_1192x266.png)

The same common binary exploitation patterns account for the majority of findings. It is unclear whether it is because driver dev teams skip modern security tooling entirely, or because the highly polymorphic nature of both WDK and KMDF makes pre-LLM static analysis unfeasible.

#### Reported Vulnerabilities

We manually confirmed and reported 15 vulnerabilities to 8 vendors, all with CVSS ratings of 7+. All have been under disclosure for over 90 days.

**Average CVSS across reported findings: 8.2 (High)**

Most bugs are exploitable from a standard, unprivileged user account. Most require nothing more than opening the device handle (often world-accessible) and sending a sequence of `DeviceIoControl` calls. Windows drivers are MSFT-signed, meaning they can be side-loaded on any Windows machine via Bring Your Own Vulnerable Driver (BYOVD) attacks even if the associated product was never installed (requiring admin privileges and therefore making the LPE a more restrictive admin→kernel).

### PSIRT response

Response from vendor PSIRTs has been disappointing. Several vendors rejected our reports outright despite video proof-of-concept demonstrations of exploitation. Others acknowledged that the products containing these drivers have reached End-of-Life, but have not revoked the driver signing certificates, leaving the BYOVD attack surface intact on every Windows machine.

To date, only **Fujitsu PSIRT** has successfully patched and assigned a CVE ( [CVE-2025-65001](https://nvd.nist.gov/vuln/detail/CVE-2025-65001)). We continue to monitor and will update if additional CVEs are assigned.

### Takeaways

1. **Agent-assisted binary vulnerability research works, and it’s cheap.** $600 and a few weeks produced an agentic loop that would take a human team years of focused reverse engineering. The per-bug cost of $4 means any motivated attacker can afford to scan the entire Windows driver ecosystem.

2. **Agentic flows require closed loops.** Although we performed this research before Opus-4.6 and GPT-5.3, the biggest performance leap was achieved by “closing the loop” and giving the agent direct feedback on exploitation success using our VM-based kernel-debugging harness. Agents that can try to bugcheck the machine over-and-over again are tomorrow’s fuzzers, and **with enough compute they’re 100x more dangerous in the wrong hands.**

3. **The Windows kernel driver ecosystem is in worse shape than most people assume.** Third-party kernel drivers remain one of the last bastions of C code running in kernel-mode with minimal security review. Code signing guarantees authenticity, not security. Our 60% false positive rate still leaves over 100 likely-exploitable privilege escalation bugs across mainstream vendor drivers from companies like AMD, Intel, NVIDIA, Dell, Lenovo, and IBM.

4. **PSIRT processes are not built for this volume.** Most vendor security teams are structured to handle a handful of reports per quarter from human researchers. When an automated system produces dozens of valid findings across multiple product lines simultaneously, the existing intake processes fail. Reports get rejected, misrouted, or deprioritized. The gap between discovery rate and remediation rate will only widen as these tools improve.

5. **We’re publishing our hash list for customers to defend themselves.** We’re past responsible disclosure timelines, so we’re making IOCs publicly available in a safe manner. If you’re a PSIRT, CERT, or security team that needs more information, contact us at [hi@hexaplex.ai](mailto:hi@hexaplex.ai) and we’ll figure it out.


### Appendix: Driver Hashes (IOCs)

The hashes below are “double-hashed”, each value is `SHA256(SHA256(file_bytes))`. We publish them this way so attackers can’t use this list to look up and download vulnerable binaries from VirusTotal or similar services. If you have a driver file on disk, you can check it against this list locally. We will provide comprehensive IOCs directly to PSIRTs, CERTs, and security teams upon request. Contact us at [hi@hexaplex.ai](mailto:hi@hexaplex.ai).

To check a driver on your system:

```
# Linux / macOS
sha256sum driver.sys | awk ‘{print $1}’ | tr -d ‘\n’ | sha256sum | awk ‘{print $1}’

# PowerShell
$h = (Get-FileHash driver.sys -Algorithm SHA256).Hash.ToLower(); $b = [System.Text.Encoding]::UTF8.GetBytes($h); $s = [System.Security.Cryptography.SHA256]::Create(); $d = $s.ComputeHash($b); ($d | ForEach-Object { $_.ToString(”x2”) }) -join “”
```

Full list:

```
f5518872b73ee8df067ab93a5a3f3e50474d619b26207da65ca6329e6553a8c0
bff265e5e5bc595057c734126ce2b3605bf2cf4ce129b223174f809d4f4c3dbe
0001c402add3ecfaf03cd70b9cacc1c9b679ebf51630264c6157fd6fac432918
1740e9ad3f9e29d59b75acee49288e9a2f5cb20f787a1be230f9c94091850cbc
3db22ada94df04f003ce92a936510f1265e0ccc5d751d5d620d2734da0e0f3d5
69f62eb881ff203acc0969911cb4c51c3f57539b999cc95560daeb96105680a4
43122f13e27189408a9366f890d15fd6e69dfc3f1a6a0a7afb53be292947335d
2e2497d54f1894f8e692cc294f9871ab57f148db69aed4270fc02c038be38193
f848b02daccf967907697bc9e251c8e523c003e3d3c70a00666c629dd7896168
8bf115e6814b4918a4c28c96975c9a274e259fab6eeb0abac6c99ab578db3622
b641de06167ab0ace9a9486fccecbe54ef3bbc7dcb25dbd74d69059d83fc872e
8f418bafa65d6a35023132bc9ca306a1aa7fc85cc64385e5b2c16f7f82f9e36f
167585faabac13f7a43c6660651fece580ae5b8d19d3583e6774060c92fc636c
7b564f798c818414f4ef0bf111df6695ba96e77f079e3b7fab330a590181404c
263cc8ffcde041af197761bf439cc30f62c162d2160a54bf5eafb07b840063cb
a4e1020c079124beeff920bf14e7e88dcb1a32a84296e088f6fdaf8a54c3bbcf
6b3284100f4a94d487fe76cb062ec404ed96bf03da5ca63bae64cf357e06df9c
e2b82a29494e628b416862ac85556266723e862f605198c9a647b4c68be8e67b
14180c0ad1278dc68bcd1d2bd5c090953f251c31735fd813ecdf48653f393c31
f33f51590913e9c1b384e11824190934fe5ce1bed2c816340673255abd5b1c7e
fd92d31c1daa8849f10f00ded6746f52128d321c96c5cdec2fab48a3566f353a
dfa97b9b8a4257627a3081540098eda93a6939f4726b8a33764286431561783a
61ea52ca06e7c714d13361f8fedef0e6db0134eb41c182858379a69c559c0118
6e207b2399c8545819bd2a3f0361bdc3b81f8964d40875541f10988cd83a8961
d7a05e9b3d9ad28ffe7dd4297972b1b513ddf3a1463d733bf70d2a721e87266b
30d968cc95df5a4f20cffa0b461bba411f888caed09813fe773f73cf97c69d17
d75ee2ec08266737ff776970fec1af4ad33a6e1a5c503087879cb914ea6c2ba0
eac89c954b31577e5bf429f40aafb74a6482ed59d7e341034d9248ba0a6a43e8
d8b9276c00a5232d242d1294773d9df1ba15366ec7fca96d937437a09e42c68d
f8735230e2c9192e02b5b7ad1c95509cb69562c7a1388330896c7a1d3d6565c8
726d74c97e437a674e42d1bcbacd433e467529678619d0d3b3840a097c9293d6
ddddb96dffbc5cfaad5847112996d2bfc50d75d088ac29c2d4a2bb02695e673b
13a1bb718618b221153a309e167e941133cccb5d27c54766d08b91eeaffa91d9
d9e3b5bf65de9a6cd12837f7904b8d5a3ffaf346a899b57154fe382c86e3ae5e
8f030fe5541b3f1a4f0e6738decb6baca52b7fdca27241928addad2fb386dc86
eecf03717f35c05eff82546a828fe658c81ab85b5781aef6c1770a7b46731a22
064e28cc2e3cb07db853cb98d968f00f67fbd7070afb56c723f6661c74edb6bf
52cd8365be18992213f45d563474cfc8cb584566ac3e33cd136cb1ceff16820e
4b18e765bcf2435894a6055958c8d150f302d998e1d846c4808b85a95f32fda6
03acd199834846b016b04e604496788100f8f90c2a50e5db55aaf44705218cd6
bca6885b24498cacbc259f5c6fc65bab5691c3b3be0f1d162cfcfeea19d82a7a
1b47869ac08a94888a256e418a615aa3cbb6698d19748b528a7917cf3c91e76b
76fc2ea6378ded4a84d7565af278b6055ffab52de9c27d2a80fb0493e5de6cbf
3fd21ea96af68f88cc86421ac98379a24ef1c7661ee8aba3475704a37a366753
2630fd79567406e9ca9bddfa2c03ee9b4c8cf475090a8567cf1efa6a287c785e
d28adf2219a6684f10a9c287a974b998a58893682ae26824330a32d0985d47f4
6dc7398197418d3caa51441599e7b15fdba119af8766f23f4409862567b11bd9
2fab7bc7ef6423f1ea08fc1ad947c9cefe4199ab641802e77777c03c97fa1321
e1ef1c9568b3722d30580429efcbf6ce8e7e3d61c4d972a3c8ea161caff016fc
ff91351f33b683f8612ce9bdd6a402a9344300a83b869347d5390a2106c856b6
f827900e8ada4bc97eb24959f26ebc9ed4794cb67cb218af49d13e6ee19685a1
94aaaaf6854ea08c122c9b60d8245ae0cc7ededec74846c79bd7e7924e26f6f8
9f6901adeb0750eae4634e6d0c8539d5d7338b306d6bc7dd55be00994631f595
2f5248763ae1af1d58cc4a9a6486f3d06a42cc1f9980c0cbb709ae1a7fc1ddee
63aaac65243ac25e24ba733e3961a0d545b23323ceb26721290247df2854f399
c2d6f6b6177431ca7ea2ba511dfd6c5f5fb04a84b6b519c1c7a7740749185ceb
f5070463de6a1d06d4bfa99267df265819d80089a89c61843450d171ef5270f9
c74c38036737b9aa867309765ef8d1b29ac4219bc21d2242d9656851c72f1f13
dbbdd1ea3246e04c7b80f8966e502dc7e891a36700f08bbbcd3b94a2cc6c94df
44641b4c1362b3f57fd36685dc59668416422696ca7f8e8a164a2e034174e3a0
afbf7fc92861087b857f3340e2b3aa4a423701cb53e7cf70c2fecd6f458e49a0
b05689300c51a95224d2dd9722f4b66482f750c7f4f7280598a1a9174b98060d
2f0389c4e5fc28c80a882a3232343a25f7f7b01121dfc4d609db42cff6de6faf
11c5d708eee5d09054d453b89b67eee5423e779ac8772bc4af0d99b7736cd4dd
066337bf10204c1dfe29d99ccd4c2cd9cb0d5091038a4518819aa5b735e7533d
7a67749b345da15af072b109541469d0c9b94c9e0f77abb3e38618f6130b03db
54b54ce4a35148708a17b4060cec53db85d2740baf3b0ddb14f6052e3be2a339
a86effaf5796fadbbdff31d0666697a27ff6d7de84eefe3d09bfb71e39302ea4
882922c05adc4e54b29002e039b09e3054267050c2e2acddf2a30fee8b363594
736bbabb5d15cd335f319e58192140e340b031834cc88652201de6c3815dafb5
a1fc19e554fa5ce739f9de3eec5809a8719886b65f7caa4e382d2f31f3f14c35
bb14a75ac4bbc6d0e470b7adf98f2cca40539e5a560a52151b391c635ff1c1d7
581d477d118bf87f1aafd1be937ab9db71c3a594216c910413c2e8c171fb69ab
c01d45f5691b4d08adb461b34237f9ef995e37443a74eb5ffbedcdf00ffe5243
c9fde1bed82f51b9a63b299af7bd2551833d53cd5fcc4325da9df97602810405
45bc2bf7c77a2e68f7971f14ab526f8864ad975f330f46f086add8976ff391a5
6c7af8c9d28fb1260a354a4b9e3b9f0dcd61c1b7b5b74a52607aba9578708c6d
36aac1cff790804b5dba09576b00c351ec9a3a55487de629dabebce7b524c204
2ac47f11582786861dd2e21e3166d0df257098e6793d783a7f5c1953102c7a42
defebc60860dd33553c10e3e0a89d3c7489a5c6c6048759d2b4bd6252b3aa9bd
9a19b927a781f7bcd6ce45d2861e3cfeb9a2cb540151c52cac35781d06d80f38
794392a5bf4c5bbe055c7a464b31939894ad2dc8d2685c9e170683144c2a650b
cc7db83737f52f3942ffb3f5b3230b9ce70dddd8fb71f563306175149b8912e1
7dcf02e1efc4040d0c8eab9b48993b47dc4d016cbf5a0555a6727c0c180bf3ba
d4f8ca287ff2ca574e0e61bc0440c3899a7b7508dc6cfa4644ee0429c2816030
a222156ad96181ed3c7e5b8f96ebe4942dd88adb3bbb1c494f0e2a24e1f946a5
d0e67b68747b11d47d77c4d96ae33107f8bc9174f73023bc4fe2398620962fe0
672556b9545bbb8403e3c3af40313a26a658b18731e27478c220691057aa4053
89a3e2b734714c3ceb0589949c8932af9e2dcb4b427fe97b78ac3ecc2a930e69
90a7120991391b4be3fb5c774cdd83ce4d5266900b385b4fc97e40772274cf4d
ce94839da4a2a92151c7e1a81475de847fc7b840472d9eebd8c9d2f1f7ed33db
545cb7f66b7de34411f8d4c0eaca30678b3eef8cda34a190d44fb6097be9eb59
a6ebc4553a83d91fbcb57168f9cf0bd06acefde0a9c6f0b21112a6a314a3bf6e
20a8f132946e6c40208e8797e4214a3c35fb2ad3506c287679ef3b421460a99a
7583260faba805fd08a156088df0000f463777fc6e9f98271f1f9824c02c4481
f7286ae800bf46dd3c876617aa3d6f3345a4d00138bccae05ee3b3dfcccfd368
a1c4d865419ff619ea4ca2a3304757426590b05b6b909f3d1d0dc5093232a014
b5bb1adff986dc603a21d7f95dd14b7a0e2cdc87e9be756306ed1d0ef48e1796
f700ce792ca57b74563e34207a1be2d866c9df74510cd6a9462e62d62dc2ee8f
3456b5ad6c936f60d7e76eb9b7116b2491ae6e5748d30e0d90451da3f0c0a9e2
5a9b580375cb3ae51656b0729783434d7ffb2133e6696971c66bcd4ed1fb9d3d
473201c93b0eeaea7560ea067c6273ec1ebc94d6bf4e7667b69b93cd834b00dd
5a0d5649b886b52d77dc275fbd6e583e8627b149e48338d612cae82b1e7fcd3d
bcd1418282d998071a822c873e29d47461d2916ab906bdf693e8800a7e280110
cc3d1df5f1a0d7f9d50678a7b02968842af4ffbf957f0837c5632df0562d71d5
4a99f768b598ca64918f796a4cf0b1ac4eb484cee616652e49ffe8b53d2c0e7d
c1f4f0e0e303b203994b660794f0fefcb5b23fa4a5af8ab72100f0e9ecad7c5a
302e5791f74462c16048551e55e085743f4cae1de1b468c856f2e33e52794a1a
7aa27d7a8f8d214df71c1d0331e570144e3136ded18382f62dbef3c8ae04b72c
886fabaad2357cb8df6ba79ed32e5644455826f4d73c1889a74ffbe344aa20de
142550e835d6839eb53645501671ffa1aaf3dd119c98d87ab19570b572cdc30e
3de1bfefa2a6fd28237ed1acae053081ebe9832aa337e8d6356bc86ddc905b18
a3b5daf9b74b4c9fd6de8e01c5751dc20e1dfd1ddf887d9b2029d1edac2a6155
a02acdd074b5bfeaa841c34834a1f433ad5768bbac2a59f4f89b835f80840bc2
37a4f94e4e811af5b320a5eb9b4c717abdb31ddc3356e68905da2c73086ac4e9
6288822f04f8abe45f7c1145efaed90220d08a9f602c486499459599de8b5606
7c0cc1790fc5f5c3e09c7b88b0800d3b60016d69976a5646a3bdd43284415f29
daa7c2ffac63f52e0cc5360a24b9d686fb9fdfe24e5d3a89a6b53751690e41e7
119cd51bd88c85f2babc441a2ad23fdefcbff3137bb20fa5e316f737ddbca969
4a4506e4c5ae5d618e7402c4cdf1742143316055247f8b6c396508323dd5bd07
aa95e38abb02f9130f7151f188913b0a07b1bda647b9166b9ac6671c96a012be
1f5907b03eb16e2ca64e253b5e93785937e35d5394bb21102335f85f0ffbe532
34c7ad67417737df93c486645d92ac3b6cdd4a89962369dea4d07603dc0770eb
a37215f7c178bb0b71f4219c54a7a2aec4252b1a4bdbd5fc533035708e52dd0c
e60afb30b323ac44f935589921cdbb6d8082afb6fe69e85eac8964f28d063e08
6a6be30cd89c2276d4a5320803de6d7f8d075d85b9f628f71b33bcd7642b2f0f
121cedbdf3fc308f6734be53fde698ca9158ba46fc118064238f38324c68d559
094b6d64c792ad3ce638e525bbcd045e13680026e1cebde2dc1e0f335c834e16
8fffdd3cd4ef6e98926334c9c1b59cf30c27f0b1b0376ee7e8d13ca7a3635463
5f1af0018fcbb599f115d62531b1b1c5df7935f6a1de57c9628d57035a3c241b
11b63161b5e5f3a37dea4c16725ea4214b4b89e137b8c550758828f26d6e5063
70bb9000831e00b37e36bb337e4064a852ace3528409202626ed1e39a3fba0a9
1671191ff7b876b2fbdf2fc63a8e8566d21d29e1134f51b65cee9a3c18b08026
756ddb9181dd991074bbd68a8df7c48ead8e0cb950bcb2342eca024fbbfe24ef
c0bf8afc8d061e3da5b8593dc24bc1cfe86e138b87cab3674d39981196815d29
0c7d181e350328b9e7d0e7e57e75f2905b2cd7c3f0a950103b81ba5203e93d6c
7f3b8b4fec4138490e59f5529a9e63bc7aeb2d0c840bf8a19e1b7ba05f14f623
7b3137e5962c729903d5c80815e09600489d989db854b5d1244a2bb6ed4efaf8
192f70a0e34f8e10c4871494a5c4157e20d437f240eced81dca0a9508dea8222
a266dde07e0cfccd48aacb4737582c7855dc5430142a8c93fb18940406733294
480c835cce8a4589d02da3104aabd21dd205fc13c09b579250f2fa838cf59c1f
5415f7f1d27b044ee2508c33f9130389b4c813ba8aff1159446b7878f98bfea9
851552076ed14bc9e92968df9937d55bc4536a348f7bd49f24df3705ea3bb296
77eb25431bb9813a4355c733f10b02e2e38a4426a26ddfce3931a4fa1cb412c0
02db103174351f58b7f4a30205eece3acc5d4fd134200d17638a811750e217e4
60df4d36f4ee4c2c8e360d5606ef8c56c33d08a85a9c24ce7b4285e4121b441f
b2069a78812d01e63388db34bbf0174ac787996f76ee7ef2210fa7b8c5c2edd3
94be5699f73227d3170de3c16fe9654241a054e28e6dc7952f409a6602bc148e
616d2015e428ddadebdffea571d5e384dd2ceb25fa36b63ffbedcd734b7dd861
55713fbb9eecf735f25b23e1cb9c28b8c36cdc0193906f1cf41d91f701f2fe5f
cfc81ad7402dd137baf7b53058af9c8d372b5e9149480abb43757e4a568a2958
4735d2db86a7c27565b0463948f506463b5cdb11a8dd9a89adee91552b071c20
9e2b6e6792e56c4ce14011c365963b80449aa8245fc08790b4c9b5cfea856e19
5262442d370ce096a706eaf43181b3e2ca77625085b3e831d881565e0b7633e6
062ed83ffc3b8ac543914d58826b6de6d62e92d098f0774cce924f44e0800eae
c03a63e11b7ee84aae78aae0cc7073c94457e7ecbe9732966f97e761780338f3
7aeff559b2ae04d30eb1dc173dbced58b01d56e62001b3a60fdc0e01cdb681a3
a7e7ff920364f6307b92955acaf5b4e097b9a9f7cd90f94b8439c48ba0e414cd
```

Thanks for reading! Subscribe for free to receive new posts and updates.

Subscribe

[![dagelf's avatar](https://substackcdn.com/image/fetch/$s_!t9lZ!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb874903-cb5a-43ed-b520-34e01ec12d99_144x144.png)](https://substack.com/profile/1071876-dagelf)[![PatchMeIfUCan's avatar](https://substackcdn.com/image/fetch/$s_!f9QU!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3d04d88c-d6c7-4b97-b0cf-bfb8e760decc_144x144.png)](https://substack.com/profile/433817627-patchmeifucan)[![Phù Thủy Máy Tính's avatar](https://substackcdn.com/image/fetch/$s_!1kkV!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff45120a8-2a9b-4b9f-84cc-4b6852545216_144x144.png)](https://substack.com/profile/268496432-phu-thuy-may-tinh)[![Gibran Iqbal's avatar](https://substackcdn.com/image/fetch/$s_!FkLd!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F4c68ecc7-b673-4836-90d6-f62b969f3a90_144x144.png)](https://substack.com/profile/7366447-gibran-iqbal)[![AnythingComputery's avatar](https://substackcdn.com/image/fetch/$s_!LERE!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80a7cfac-d76e-4109-8368-f50f56ee550d_480x360.png)](https://substack.com/profile/222028251-anythingcomputery)

9 Likes∙

[4 Restacks](https://substack.com/note/p-188916866/restacks?utm_source=substack&utm_content=facepile-restacks)

9

2

4

Share

|     |     |
| --- | --- |
| [![Eyal Kraft's avatar](https://substackcdn.com/image/fetch/$s_!Ht_h!,w_52,h_52,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05827702-49bc-4ffe-8d86-657d8d1341b2_144x144.png)](https://substack.com/@eyalkraft?utm_source=byline) | A guest post by

|     |     |
| --- | --- |
| [Eyal Kraft](https://substack.com/@eyalkraft?utm_campaign=guest_post_bio&utm_medium=web)<br>AI & Cybersecurity | [Subscribe to Eyal](https://eyalkraft.substack.com/subscribe?) | |

#### Discussion about this post

CommentsRestacks

![User's avatar](https://substackcdn.com/image/fetch/$s_!TnFC!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack.com%2Fimg%2Favatars%2Fdefault-light.png)

[![sase's avatar](https://substackcdn.com/image/fetch/$s_!chgW!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdf5c78e1-8d30-4115-9e18-01c5cb611a34_144x144.png)](https://substack.com/profile/468051257-sase?utm_source=comment)

[sase](https://substack.com/profile/468051257-sase?utm_source=substack-feed-item)

[20h](https://substack.com/note/c-220136536 "Feb 26, 2026, 1:18 PM")

which model bro ? no mention

Like

Reply

Share

[![dagelf's avatar](https://substackcdn.com/image/fetch/$s_!t9lZ!,w_32,h_32,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb874903-cb5a-43ed-b520-34e01ec12d99_144x144.png)](https://substack.com/profile/1071876-dagelf?utm_source=comment)

[dagelf](https://substack.com/profile/1071876-dagelf?utm_source=substack-feed-item)

[2d](https://substack.com/note/c-219599615 "Feb 25, 2026, 11:44 AM")

Phew no hits.

Like

Reply

Share

### Ready for more?

Subscribe