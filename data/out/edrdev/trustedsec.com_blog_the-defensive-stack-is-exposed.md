# https://trustedsec.com/blog/the-defensive-stack-is-exposed

![Revisit consent button](https://cdn-cookieyes.com/assets/images/revisit.svg)

We value your privacy

We use cookies to enhance your browsing experience, serve personalised ads or content, and analyse our traffic. By clicking "Accept All", you consent to our use of cookies.

CustomiseReject AllAccept All

Customise Consent Preferences![Close](https://cdn-cookieyes.com/assets/images/close.svg)

We use cookies to help you navigate efficiently and perform certain functions. You will find detailed information about all cookies under each consent category below.

The cookies that are categorised as "Necessary" are stored on your browser as they are essential for enabling the basic functionalities of the site. ... Show more

NecessaryAlways Active

Necessary cookies are required to enable the basic features of this site, such as providing secure log-in or adjusting your consent preferences. These cookies do not store any personally identifiable data.

- Cookie

\_\_cf\_bm

- Duration

1 hour

- Description

This cookie, set by Cloudflare, is used to support Cloudflare Bot Management.


- Cookie

\_\_hssrc

- Duration

session

- Description

This cookie is set by Hubspot whenever it changes the session cookie. The \_\_hssrc cookie set to 1 indicates that the user has restarted the browser, and if the cookie does not exist, it is assumed to be a new session.


- Cookie

\_\_hssc

- Duration

1 hour

- Description

HubSpot sets this cookie to keep track of sessions and to determine if HubSpot should increment the session number and timestamps in the \_\_hstc cookie.


- Cookie

\_cfuvid

- Duration

session

- Description

Calendly sets this cookie to track users across sessions to optimize user experience by maintaining session consistency and providing personalized services


Functional

Functional cookies help perform certain functionalities like sharing the content of the website on social media platforms, collecting feedback, and other third-party features.

- Cookie

lidc

- Duration

1 day

- Description

LinkedIn sets the lidc cookie to facilitate data center selection.


- Cookie

li\_gc

- Duration

6 months

- Description

Linkedin set this cookie for storing visitor's consent regarding using cookies for non-essential purposes.


Analytics

Analytical cookies are used to understand how visitors interact with the website. These cookies help provide information on metrics such as the number of visitors, bounce rate, traffic source, etc.

- Cookie

\_gcl\_au

- Duration

3 months

- Description

Google Tag Manager sets the cookie to experiment advertisement efficiency of websites using their services.


- Cookie

\_ga\_\*

- Duration

1 year 1 month 4 days

- Description

Google Analytics sets this cookie to store and count page views.


- Cookie

\_ga

- Duration

1 year 1 month 4 days

- Description

Google Analytics sets this cookie to calculate visitor, session and campaign data and track site usage for the site's analytics report. The cookie stores information anonymously and assigns a randomly generated number to recognise unique visitors.


- Cookie

\_\_hstc

- Duration

6 months

- Description

Hubspot set this main cookie for tracking visitors. It contains the domain, initial timestamp (first visit), last timestamp (last visit), current timestamp (this visit), and session number (increments for each subsequent session).


- Cookie

hubspotutk

- Duration

6 months

- Description

HubSpot sets this cookie to keep track of the visitors to the website. This cookie is passed to HubSpot on form submission and used when deduplicating contacts.


Performance

Performance cookies are used to understand and analyse the key performance indexes of the website which helps in delivering a better user experience for the visitors.

- Cookie

session\_id

- Duration

1 year

- Description

This cookie is used to get or set the session id for the current session.


Advertisement

Advertisement cookies are used to provide visitors with customised advertisements based on the pages you visited previously and to analyse the effectiveness of the ad campaigns.

- Cookie

sa-user-id

- Duration

1 year

- Description

StackAdapt sets this cookie as a third party advertising cookie to record information about a user's website activity, such as the pages visited and the locations viewed, to enable us to provide users with interest-based content and personalised advertisements on external websites.


- Cookie

sa-user-id-v2

- Duration

1 year

- Description

StackAdapt sets this cookie as a third party advertising cookie to record information about a user's website activity, such as the pages visited and the locations viewed, to enable us to provide users with interest-based content and personalised advertisements on external websites.


- Cookie

bcookie

- Duration

1 year

- Description

LinkedIn sets this cookie from LinkedIn share buttons and ad tags to recognize browser IDs.


- Cookie

IDE

- Duration

1 year 24 days

- Description

Google DoubleClick IDE cookies store information about how the user uses the website to present them with relevant ads according to the user profile.


- Cookie

test\_cookie

- Duration

15 minutes

- Description

doubleclick.net sets this cookie to determine if the user's browser supports cookies.


Uncategorised

Other uncategorised cookies are those that are being analysed and have not been classified into a category as yet.

- Cookie

sa-user-id-v3

- Duration

1 year

- Description

Description is currently not available.


- Cookie

calltrk\_nearest\_tld

- Duration

1 year 1 month 4 days

- Description

Description is currently not available.


- Cookie

calltrk\_referrer

- Duration

6 months

- Description

This is a functionality cookie set by the CallRail. This cookie is used to store the referring URL. It helps to accurately attribute the visitor source when displaying a tracking phone number.


- Cookie

calltrk\_landing

- Duration

6 months

- Description

This is a functionality cookie set by the CallRail. This cookie is used to store the landing page URL. It helps to accurately attribute the visitor source when displaying a tracking phone number.


- Cookie

frontend\_lang

- Duration

1 year

- Description

No description available.


- Cookie

libsyn-paywall-s

- Duration

1 day

- Description

Description is currently not available.


Reject AllSave My PreferencesAccept All

Powered by [![Cookieyes logo](https://cdn-cookieyes.com/assets/images/poweredbtcky.svg)](https://www.cookieyes.com/product/cookie-consent/?ref=cypbcyb&utm_source=cookie-banner&utm_medium=powered-by-cookieyes)

- [Blog](https://trustedsec.com/blog)
- [The Defensive Stack is Exposed: LLMs, Reverse Engineering, and the End of Opaque Defense](https://trustedsec.com/blog/the-defensive-stack-is-exposed)

May 05, 2026

# The Defensive Stack is Exposed: LLMs, Reverse Engineering, and the End of Opaque Defense

Written by
Justin Elze


Artificial Intelligence (AI)

![](https://trusted-sec.transforms.svdcdn.com/production/images/Blog-Covers/TheDefensiveStackisExposed_WebHero.jpg?w=320&h=320&q=90&auto=format&fit=crop&dm=1777923976&s=f9839c3296af123ead771511a744689e)

Table of contents

- [Universal Approaches, Universal Problems](https://trustedsec.com/blog/the-defensive-stack-is-exposed#Universal)
- [The Security Through Obscurity Collapse](https://trustedsec.com/blog/the-defensive-stack-is-exposed#Collapse)
- [What This Actually Means](https://trustedsec.com/blog/the-defensive-stack-is-exposed#Means)
- [Where This Goes Next](https://trustedsec.com/blog/the-defensive-stack-is-exposed#Next)
- [What Defenders Should Actually Do](https://trustedsec.com/blog/the-defensive-stack-is-exposed#WhatDo)
- [Opaque was Never Durable](https://trustedsec.com/blog/the-defensive-stack-is-exposed#Durable)

Share

- [Share URL](https://trustedsec.com/blog/the-defensive-stack-is-exposed "Share URL")
- [Share via Email](mailto:?subject=Check%20out%20this%20article%20from%20TrustedSec%21&body=The%20Defensive%20Stack%20is%20Exposed%3A%20LLMs%2C%20Reverse%20Engineering%2C%20and%20the%20End%20of%20Opaque%20Defense%3A%20https%3A%2F%2Ftrustedsec.com%2Fblog%2Fthe-defensive-stack-is-exposed "Share via Email")
- [Share on Facebook](https://www.facebook.com/sharer.php?u=https%3A%2F%2Ftrustedsec.com%2Fblog%2Fthe-defensive-stack-is-exposed "Share on Facebook")
- [Share on X](https://twitter.com/share?text=The%20Defensive%20Stack%20is%20Exposed%3A%20LLMs%2C%20Reverse%20Engineering%2C%20and%20the%20End%20of%20Opaque%20Defense%3A%20https%3A%2F%2Ftrustedsec.com%2Fblog%2Fthe-defensive-stack-is-exposed "Share on X")
- [Share on LinkedIn](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Ftrustedsec.com%2Fblog%2Fthe-defensive-stack-is-exposed&mini=true "Share on LinkedIn")

Share

- [Share URL](https://trustedsec.com/blog/the-defensive-stack-is-exposed "Share URL")
- [Share via Email](mailto:?subject=Check%20out%20this%20article%20from%20TrustedSec%21&body=The%20Defensive%20Stack%20is%20Exposed%3A%20LLMs%2C%20Reverse%20Engineering%2C%20and%20the%20End%20of%20Opaque%20Defense%3A%20https%3A%2F%2Ftrustedsec.com%2Fblog%2Fthe-defensive-stack-is-exposed "Share via Email")
- [Share on Facebook](https://www.facebook.com/sharer.php?u=https%3A%2F%2Ftrustedsec.com%2Fblog%2Fthe-defensive-stack-is-exposed "Share on Facebook")
- [Share on X](https://twitter.com/share?text=The%20Defensive%20Stack%20is%20Exposed%3A%20LLMs%2C%20Reverse%20Engineering%2C%20and%20the%20End%20of%20Opaque%20Defense%3A%20https%3A%2F%2Ftrustedsec.com%2Fblog%2Fthe-defensive-stack-is-exposed "Share on X")
- [Share on LinkedIn](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Ftrustedsec.com%2Fblog%2Fthe-defensive-stack-is-exposed&mini=true "Share on LinkedIn")

Everyone is talking about LLMs finding zero days. That is not the only story. The story is what happens when you point these models at the defensive tools organizations depend on for first line defense. AI is changing the economics of understanding systems, including the systems built to stop attackers.

## The Wrong Conversation

While security Twitter argues about LLM-generated exploits, autonomous bug hunting, and whether a model can replace a red team, LLMs are already useful for something more immediately practical: systematically understanding and reverse engineering the defensive products themselves.

Across five commercial endpoint products we evaluated internally, workflows that previously took skilled reverse engineers weeks of focused effort now took days. The model handled the mapping, summarization, and cross-version comparison that used to dominate the timeline, and a human spent their attention on validation and judgment calls. The same approaches transferred across AV products, EDR platforms, appliances, and other defensive tooling with only minor steering. Outputs still require validation, but the timeline compression is real.

The acquisition problem everyone thought was the hard part was never the hard part. Defensive products end up on university download sites, customer trials, VirusTotal submissions, GitHub repositories, misconfigured S3 buckets, and random places. Minimum-seat requirements and "we do not sell to researchers" policies slow down independent researchers and small labs, but they do not stop anyone. In some cases they make the ecosystem worse by limiting legitimate scrutiny while doing little to reduce adversary access. Once the product, configuration, update package, or endpoint artifact is available, the real question is not whether an attacker can get it. The real question is how long it takes them to understand it. That is the part LLMs are changing.

## Universal Approaches, Universal Problems

Here is what testing showed: the same core analysis workflows work across vendors with minor steering. That is not a coincidence. It says something fundamental about the state of defensive tooling.

These products share architectural patterns, rely on similar frameworks, and make comparable design decisions driven by the same business pressures. They face the same trade-off between comprehensive detection and false positives. They need some form of local policy, rules, signatures, scoring logic, scripted engine, or ML model to make decisions on the host. Tuning choices made under those constraints create predictable behavioral patterns.

That extends well beyond traditional signatures. A modern defensive product is usually a mix of YARA-style rules, behavioral logic, allowlists, prefilters, cloud lookups, scripted engines, and local ML classifiers. Some vendors use decision trees or neural models. Others ship hundreds of behavioral rules as readable Lua source after one decryption pass. Most do all of the above. There is lots of decision logic on or near the host, and decision logic can be studied.

The prompt is not magic. The workflow is what matters: give the model enough context to map the system, identify the decision points, separate confirmed behavior from hypotheses, and help the operator focus their manual validation. What used to require deep product expertise and long manual analysis can now be accelerated by someone who knows what questions to ask.

## The Security Through Obscurity Collapse

A large amount of defensive tooling was built around the assumption that its internal logic would remain opaque to attackers. Detection algorithms, rule structures, behavioral models, policy formats, scoring thresholds, and tuning decisions were protected mostly through access restrictions, product complexity, and lack of attacker time.

That assumption is breaking.

When defensive products operate on endpoints, their rules, configurations, policies, logs, update packages, and model artifacts become accessible somewhere. Maybe not cleanly. Maybe not completely. Maybe not in a format the vendor intended anyone to read. Enough of it exists for an attacker to study, however.

This is especially true for local detection logic. If a product needs to make a decision on the host, some part of that decision path has to exist on or near the host. That could be a rule pack, a feature extractor, a scoring threshold, a scripted behavioral engine, a prefilter, an exclusion list, or a local model that decides whether something is clean, suspicious, or malicious. The same is true for the policy that selects which of those engines run, with what thresholds, and against which paths and processes, and that policy is often readable on the endpoint itself, sometimes literally world-readable in the registry.

Complexity used to be part of the protection. It is a smaller barrier now, because LLMs are good at helping humans move through complex systems. They do not need to perfectly reverse engineer everything. They only need to reduce the time required to find useful seams.

This is not saying defensive tools are worthless. It is saying the old model of "attackers will not understand how this works" is no longer a safe assumption. If a product only works because its internal logic is hard to inspect, that is not durable security. That is temporary friction.

## What This Actually Means

Organizations are making security purchasing decisions based on a threat model that assumed attackers would not be able to study how their defensive products actually work. Obfuscation, proprietary formats, encrypted configurations, and the sheer expertise required for product-specific reverse engineering were treated as durable barriers. Procurement evaluates products against static test cases, compliance checkboxes, and MITRE mappings on the assumption that whatever the attacker brings will not include a working understanding of the product's internal decision logic. That assumption is what is failing. The barriers still exist, but LLMs collapse the time and skill required to get past them, which means the threat model the purchase was made under is not the threat model the product is now operating in.

The reality is different.

**Rule Extraction:** YARA rules, behavioral signatures, detection conditions, and related logic can be extracted, reconstructed, or inferred from on-disk artifacts and observed behavior.

**Model Analysis:** Local ML models, feature extraction logic, scoring thresholds, and verdict boundaries can often be studied enough to understand what the product values and what it ignores.

**Scripted Engine Analysis:** Embedded interpreters expose how behavioral events are matched, scored, suppressed, or escalated, and the rules they execute are usually shipped to the host.

**Policy and Exclusion Mining:** A surprising amount of effective policy is readable on the endpoint. Trusted paths, process allowlists, signer rules, command line exclusions, file-type masks, and per-rule silencing flags let an attacker pick the least-monitored path before doing anything noisy.

**Gap Analysis:** Blind spots become easier to identify when rules, models, prefilters, exclusions, trust paths, and management states can be analyzed together rather than one at a time.

**Version Comparison:** Updates expose what the vendor changed, what they fixed quietly, and what suddenly became important enough to modify.

**Vulnerability Discovery:** The same analysis that maps detection logic also surfaces product-specific vulnerabilities. Parsing routines, IPC interfaces, kernel callbacks, update mechanisms, local services running at SYSTEM, and tamper-protection logic all become inspectable. LLM-assisted review accelerates the hunt for memory corruption, logic flaws, privilege escalation paths, unsafe deserialization, and signed-driver abuse in the very products meant to stop them. More lines of code means more problems, and defensive products ship a lot of code.

This is not theoretical. It is the operational reality of reducing the cost of analysis. Skilled operators already did this kind of work. LLMs make it faster, more repeatable, and more accessible to people who do not have years of product-specific reverse engineering experience.

This also changes how defenders should think about detection confidence. A quiet endpoint product does not automatically mean nothing happened. It may mean the activity fell below a threshold, hit a prefilter, matched an exclusion, hit a cached clean verdict keyed by path rather than content, or occurred while the sensor was in maintenance, recovery, or a degraded cloud-disconnected state. Several products we looked at had legitimate operational states that relax tamper protection or drop telemetry, and the conditions to reach them are visible to anyone who reads the agent.

## Where This Goes Next

The defensive stack is becoming part of the attack surface. The same capabilities being applied to endpoint products will move outward to SIEM correlation rules and alert pipelines, cloud policy and identity relationships, WAF and runtime application controls, and any other defensive surface that ships its decision logic close to the asset it protects.

The pattern repeats anywhere defensive tooling relies on complexity, access restrictions, or hidden logic for protection. If the control makes decisions, those decisions can eventually be studied. If the decision logic can be studied, LLMs compress the time required to understand it. One fair counterpoint vendors can use the same tools to find and fix the seams faster, and pointing a model at their own product gives them every advantage, including source code, build artifacts, telemetry, and test infrastructure. The asymmetry is not technical. It is procedural. Attackers ship findings the moment they are useful. Vendors ship findings through triage queues, regression testing, customer pilots, staged rollouts, and support contracts. The defender's analysis is not slower because the AI is slower, it is slower because the path from "we found something" to "every customer is protected" is measured in weeks or quarters, while the path from "we found something" to "we used it on an engagement" is measured in days. Until that gap closes, the attacker side of this curve will keep moving faster than the defender side, regardless of who has better tooling.

## What Defenders Should Actually Do

Most defenders will never reverse engineer their EDR, and they should not have to. The point is simpler: assume the attacker has, and assume they know which techniques your product misses, ignores, or silently routes around. That changes which controls you should be leaning on.

The lesson is not "fix your EDR." It is "stop carrying the weight on a single layer the attacker can study." Put real budget and attention into the layers that do not depend on opaque endpoint logic.

### 1\. Harden the host so the techniques attackers know are gaps cannot land cleanly.

These controls work whether the EDR has a rule for the technique. They raise the floor under everything else.

- Application control. WDAC, AppLocker, or a third-party equivalent in enforcement mode (not audit), with a signer-and-path policy that blocks unsigned binaries from user-writable directories. This kills a large fraction of "EDR did not have a rule for it" payloads outright.
- LSA Protection (RunAsPPL), Credential Guard, and removing cached credentials where feasible. Mimikatz-class techniques become noisy and partial regardless of EDR coverage.
- ASR rules in block mode for the well-known initial access and execution paths (Office child processes, obfuscated scripts, LSASS access, executable content from email/web).
- PowerShell script block logging and module logging on, shipped to the SIEM. Cheap, high signal, independent of the EDR.
- Local admin separation (LAPS), tiered admin model, no domain admin sessions on workstations. Limits what a successful bypass is worth.

If app control and ASR are off, the EDR is doing work that should have been prevented one layer down.

### 2\. Build SIEM detections that do not rely on the EDR's verdict.

The EDR ships you events even when it does not alert on them. Your SIEM is where you turn those raw events into detections the vendor did not write, and where you correlate across sources the EDR cannot see.

- Ingest raw process, file, registry, network, and module-load telemetry from the endpoint, plus Windows Security, PowerShell, Sysmon, DNS, and proxy logs. Do not depend on the EDR's alert stream alone.
- Write correlation rules for the gaps reverse engineering tends to expose: signed-binary execution from unusual paths, LOLBin chains, WMI/COM lateral movement, service creation outside change windows, scheduled task creation by interactive users, anomalous parent-child process relationships.
- Run purple team exercises that explicitly assume the EDR is silent on the initial access host. The SIEM rule is what has to fire.

### 3\. Put weight on identity detection.

Identity is where most modern intrusions actually move, and it is the layer least dependent on endpoint product internals. It also tends to survive when the endpoint layer is bypassed.

- Sign-in risk and user risk policies in Entra ID (or equivalent), with Conditional Access enforcing MFA, device compliance, and location/risk-based blocks.
- Detect impossible travel, atypical sign-in locations, MFA fatigue patterns, legacy auth attempts, and PRT anomalies.
- Detect token theft indicators: refresh tokens used from a different device or IP address than they were issued to, session cookies replayed from unexpected locations.
- Detect service principal and OAuth app abuse: new consents to high-privilege scopes, app registrations created outside change processes, service principals authenticating from new IP addresses.
- Watch directory-side actions: privileged group changes, role assignments, Conditional Access policy edits, federation/trust changes, certificate-based auth additions.
- For on-premises AD: Kerberoasting, AS-REP roasting, DCSync, ticket anomalies, and changes to, ACLs on tier-zero objects.

These detections fire on IdP and directory telemetry, not on the EDR's view of the endpoint. They keep working when the endpoint layer does not.

### 4\. Treat the EDR as one signal among many.

Defense in depth was always the right model. It becomes load-bearing when the first line is predictable. Practical checks:

- Map your high-severity alerts back to their source. If most come from a single product, the other layers are decorative.
- Add canary files, accounts, services, and credentials. They detect the techniques rules miss because they detect intent, not pattern.
- Pay attention to network egress: beaconing, DNS anomalies, unexpected outbound destinations, traffic to fresh domains. These are independent of any endpoint verdict.

### 5\. Treat this as an architectural problem, not a vendor problem.

The issue is not that one product is bad. The broader defensive model leaned on opaque logic, product complexity, and access friction, and those assumptions are aging out. Update procurement, architecture review, and tabletop scenarios to reflect a world where the internal logic of any defensive product can be studied by a motivated attacker, then make sure the layers that do not depend on that opacity (host hardening, SIEM correlation, identity detection) are doing real work.

## Opaque was Never Durable

InfoSec will continue to fixate on the dramatic parts of AI security threats while missing the operational reality. We will keep talking about autonomous exploit generation while attackers use the same tools to map defensive capabilities, understand product behavior, and reduce the cost of bypass development.

The organizations that adapt their security architecture to account for inspectable defensive tooling will be in a much better position. The ones that do not will eventually discover that their security stack was providing less protection than they thought.

The difference this time is speed and scale. What used to take specialized teams months can now take capable operators days. What used to require deep product expertise now increasingly requires the right workflow, the right artifacts, and the right prompts.

Sample EDR Skill - [https://gist.github.com/HackingLZ/8956b015a55412522d22a88e0dd284fc](https://gist.github.com/HackingLZ/8956b015a55412522d22a88e0dd284fc)

Sample EDR Large Prompt - [https://gist.github.com/HackingLZ/a9f71c8ea7bd6d867765bda0af2460f6](https://gist.github.com/HackingLZ/a9f71c8ea7bd6d867765bda0af2460f6)

Share

- [Share URL](https://trustedsec.com/blog/the-defensive-stack-is-exposed "Share URL")
- [Share via Email](mailto:?subject=Check%20out%20this%20article%20from%20TrustedSec%21&body=The%20Defensive%20Stack%20is%20Exposed%3A%20LLMs%2C%20Reverse%20Engineering%2C%20and%20the%20End%20of%20Opaque%20Defense%3A%20https%3A%2F%2Ftrustedsec.com%2Fblog%2Fthe-defensive-stack-is-exposed "Share via Email")
- [Share on Facebook](https://www.facebook.com/sharer.php?u=https%3A%2F%2Ftrustedsec.com%2Fblog%2Fthe-defensive-stack-is-exposed "Share on Facebook")
- [Share on X](https://twitter.com/share?text=The%20Defensive%20Stack%20is%20Exposed%3A%20LLMs%2C%20Reverse%20Engineering%2C%20and%20the%20End%20of%20Opaque%20Defense%3A%20https%3A%2F%2Ftrustedsec.com%2Fblog%2Fthe-defensive-stack-is-exposed "Share on X")
- [Share on LinkedIn](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Ftrustedsec.com%2Fblog%2Fthe-defensive-stack-is-exposed&mini=true "Share on LinkedIn")

CloseShow Transcript