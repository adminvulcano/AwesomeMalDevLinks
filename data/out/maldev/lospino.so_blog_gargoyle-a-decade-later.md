# https://lospino.so/blog/gargoyle-a-decade-later/

[Skip to content](https://lospino.so/blog/gargoyle-a-decade-later/#main)

Security research \| May 13, 2026

# Gargoyle, a decade later

A reflective retrospective on Gargoyle, temporal memory state, the 2026 refresh, and what better validation teaches defenders.

![A restrained technical diagram of memory regions, stack frames, and control flow for Gargoyle.](https://lospino.so/images/projects/gargoyle-editorial.webp)

- [GitHub **JLospinoso/gargoyle**](https://github.com/JLospinoso/gargoyle)
- [article **Earlier article**](https://lospino.so/security/assembly/c/cpp/developing/software/2017/03/04/gargoyle-memory-analysis-evasion.html)

Nearly a decade later, I found myself back inside an old Windows proof of
concept that I had not expected to keep mattering.

Gargoyle began as a small 32-bit Windows research demo. I published it in 2017
with a blog post titled [“gargoyle, a memory scanning evasion\\
technique”](https://lospino.so/security/assembly/c/cpp/developing/software/2017/03/04/gargoyle-memory-analysis-evasion.html).
The visible behavior was deliberately boring: every so often, it displayed a
MessageBox. The interesting part was not the window. It was the state transition
around the window. A code region could spend most of its life in non-executable
memory, briefly become executable during a small work window, and then return to
a dormant non-executable state.

At the time, I framed the idea around memory scanning. That was the right
historical frame, but it is not the cleanest one I would use now. The part that
survived is simpler and more general: memory state is temporal. A point-in-time
scanner can report something true and still miss a state transition that happens
before or after it looks.

That is the reason I came back to the repository. The refreshed
[Gargoyle repo](https://github.com/JLospinoso/gargoyle) keeps the original
Win32 proof of concept as the canonical historical design, but it wraps the idea
in better tooling, better architecture coverage, and better evidence language.
It adds sibling demonstrations for x64, ARM64, and ARM64EC. It documents the
build and validation paths. It fixes a timer/APC semantic weakness that I should
have been more precise about years ago. It also says, much more plainly than the
original article did, what the proof of concept does not claim.

Gargoyle is not an invisibility machine. It is not a loader. It is not an
operator workflow. It is a compact research artifact about time, state, and
measurement.

There is a particular kind of discomfort in revisiting your own old systems
code. You recognize the thought process immediately, including the parts you
would still defend. You also notice the assumptions that felt obvious at the
time because the demo worked and because the surrounding ecosystem had not yet
forced better questions. Returning to Gargoyle was like that. I did not want to
preserve the project in amber, and I did not want to turn it into something
larger and louder. I wanted to make it legible.

That may sound less dramatic than the original title. I think it is more useful.

## The actual idea was time

The best modern description of Gargoyle is the one in the refreshed docs:
[temporal memory state](https://github.com/JLospinoso/gargoyle/blob/master/docs/concepts/temporal-memory-state.md).

A memory page can have one security-relevant state when an observer looks and
another state when the program later does work. If a scanner asks only “which
private pages are executable right now?”, then a region that is dormant and
non-executable at that instant may fall outside the scanner’s predicate. That
does not mean the memory is gone. It does not mean a defender has no evidence.
It means the observation was time-bound.

That distinction matters because “hiding” is an easy word to overuse. It
suggests absence. It invites the wrong kind of argument about whether something
was or was not seen in the abstract. Gargoyle is better understood as a
measurement problem. What state did the observer measure? At what time? At what
layer? What changed before and after that observation? What other artifacts did
the state machine leave behind?

The original proof challenged a narrow but important scanner assumption. If
live memory analysis focuses on pages that are executable at scan time, then a
program that spends most of its dormant life in non-executable memory can expose
a blind spot. The scanner may be doing exactly what it was designed to do. The
problem is that “currently executable” and “capable of becoming executable
again” are different questions.

That lesson aged well. It pushes defenders toward stateful observation:
allocation history, protection transitions, timer state, callback context, stack
provenance, page-table evidence, CFG bitmap residue, endpoint telemetry, and
whatever else helps turn a snapshot into a timeline. A single memory map can be
useful. It is still a slice.

The refreshed
[responsible-use docs](https://github.com/JLospinoso/gargoyle/blob/master/docs/responsible-use.md)
try to keep that boundary visible. The project is a benign research and
education artifact. It should be run in owned or explicitly permitted labs. It
should stay small, observable, and boring on purpose. If the artifact stops
being boring, it probably stops being useful for the kind of teaching I want it
to support.

## The compact Win32 proof

The original Win32 design still has a certain compactness that I like.

At a high level, the proof assembled four ideas: a waitable timer, APC
delivery, a protection transition through `VirtualProtectEx`, and an x86
stack-pivot shape. The setup code displayed the benign MessageBox, changed the
setup region back to a dormant non-executable state, and arranged for later
re-entry. When the timer path fired, the stack-pivot path restored execute
permission and returned to the setup code so the loop could continue.

The details were very 2017 and very 32-bit Windows. The original article walked
through the stack trampoline, the ROP gadget shape, the use of a gadget in
`mshtml.dll`, and the way the callback argument could point at a crafted stack.
The current
[Win32 architecture page](https://github.com/JLospinoso/gargoyle/blob/master/docs/architectures/win32-original.md)
keeps that implementation as the canonical historical proof. The root
`main.cpp`, `setup.nasm`, and `gadget.nasm` are still the source of truth for
that version.

I am intentionally describing this at the level of state and evidence rather
than as a recipe. The point of the proof was never the specific gadget. The
point was that a tiny program could make memory protection a time-dependent
property and force a scanner to be honest about what it measured.

That compactness is why Gargoyle remained a useful reference. A reader could
hold the whole idea in their head: show a harmless marker, go dormant, wait for
timer/APC re-entry, briefly restore execute permission, repeat. It was small
enough to teach, small enough to inspect, and small enough to be criticized.

The criticism matters. The original proof did not show that memory disappears.
It did not say anything universal about modern endpoint products. It did not
generalize cleanly across architectures. It did not establish every internal
transition with the kind of validation language I would now prefer. It was a
good small proof, not a theory of everything.

That is the first lesson of revisiting old research: keep the idea, shrink the
mythology around it.

## What aged well, and what did not

The idea aged better than the artifact.

The idea was temporal memory state. That still feels like the right abstraction.
It shows up in lots of later conversations: protection cycling, short work
windows, sleep obfuscation, timer-driven re-entry, callback-driven execution,
and defensive attempts to recover state history from telemetry and forensic
artifacts. Not all of that work descends from Gargoyle. Some of it is adjacent.
Some of it is convergent. But it lives in the same neighborhood: security tools
often need snapshots, while programs are state machines.

The artifact was narrower. It was x86. It used a historical stack-pivot/ROP
shape. Its validation was mostly live and visible. It was written for a Windows
toolchain and operating-system reality that has changed. In hindsight, the
original phrase “memory scanning evasion” also carried more swagger than was
necessary. It named the scanner assumption, but it could invite readers to turn
a narrow proof into a broader claim.

That is one reason the refresh is deliberately conservative. The current README
describes Gargoyle as a historical Windows research proof of concept for
temporal memory-state evasion. The original Win32 implementation remains
central. The newer architecture work is framed as sibling demonstrations, not
as a claim that the old x86 mechanism was transparently portable.

The biggest thing that did not age well was the validation story around timer
APC delivery. The old mental model could blur two separate facts: a timer handle
can become signaled, and an APC completion routine can be dispatched when the
thread enters an alertable wait. Those facts are related, but not identical. If
the research claim is about APC completion, the proof should bind to alertable
APC dispatch, not merely to a wait returning.

That is the part of the refresh I value most now. It does not make the demo more
spectacular. It makes the claim cleaner.

## From MessageBox to measurement

The MessageBox is funny to me now because it did exactly what I needed and also
made the proof too easy to summarize badly.

It was a perfect demo marker. You could run the program, see a harmless window,
close it, wait, and see it again. There is pedagogical value in that. Systems
work can disappear into traces and memory maps so quickly that a small visible
marker helps readers stay oriented. The window says: the benign path ran here.
It says nothing more mystical than that.

But the temptation is to let the visible marker stand in for the whole
mechanism. That is where demos get slippery. A UI event is not a callback trace.
A returning wait is not a proof of APC dispatch. A page state observed in a
memory viewer is not a complete history of every transition. The MessageBox was
useful because it made the loop tangible; it was insufficient if treated as the
entire evidence story.

That is the biggest difference between how I would present Gargoyle now and how
I presented it in 2017. I would still use the small visible marker. I would
still keep the proof compact. I would still explain the Win32 mechanics because
the original design is interesting. But I would lead readers more carefully from
marker to mechanism to evidence. I would be explicit about which parts are
directly observed, which parts are inferred from a controlled run, and which
parts require optional manual inspection or stronger instrumentation.

This is not just an editorial preference. In security research, a demo can
become a story faster than the author expects. A good story helps the idea
travel; a loose story lets the idea drift. The refresh is partly an attempt to
keep the story attached to the measurements.

## The refresh: making the old thing measurable

The 2026 refresh was not an attempt to turn Gargoyle into a bigger runtime. It
was an attempt to make the old research artifact easier to build, easier to
teach, and harder to misread.

The build stayed Windows-native. That was the right kind of boring. Gargoyle is
not a cross-platform library; its interesting semantics are Windows semantics:
waitable timers, APCs, alertable waits, page protections, calling conventions,
and Windows-on-Arm behavior. The refreshed
[build docs](https://github.com/JLospinoso/gargoyle/blob/master/docs/implementation/build-system.md)
therefore describe a Visual Studio/MSBuild-centered solution with `just`
recipes around the repeatable checks. I briefly considered whether a more
abstract build system would make the project feel tidier. It would mostly have
made the wrong thing look important.

That is a small example of a larger theme in the refresh: choose the dull tool
when the dull tool tells the truth. Gargoyle is Windows-specific, so MSBuild is
not an embarrassment to hide behind another layer. NASM is part of the x86/x64
story. ARMASM and COFF extraction are part of the ARM story. The `just` recipes
are there to make the work repeatable, not to pretend the project has become a
portable framework. A good refresh should reduce accidental friction without
changing the nature of the artifact.

The other major change is the acceptance harness. The
[harness docs](https://github.com/JLospinoso/gargoyle/blob/master/docs/implementation/acceptance-harness.md)
split validation into modes: artifacts, architecture reports, headless runs,
and live MessageBox validation. That gives the project a vocabulary for
evidence. Artifact validation checks that expected files exist and that PE
machine metadata is compatible with the requested platform. Architecture mode
records runtime identity facts. Headless mode exercises local benign rounds
without UI where the native runtime supports it. Live mode validates the visible
desktop MessageBox path.

Those are not interchangeable proofs. They are smaller claims that fit
together.

The refresh also made the tooling stricter. The Python acceptance package is
typed, linted, tested, and documented. The native checks include build coverage,
MSVC analysis, and sanitizer-oriented validation where appropriate. The CI docs
separate the ordinary Windows x64 gate from the hosted Windows-on-Arm smoke
path. That hosted ARM path is one of the pleasant modern surprises: ARM64 and
ARM64EC are now feasible to build and smoke-test in CI rather than remaining
“would be nice someday” architecture notes.

That Windows-on-Arm point changed the shape of the work. Without hosted ARM
coverage, ARM64 and ARM64EC would have been easy to describe and hard to trust.
With it, they could become sibling demonstrations with real automated evidence:
builds, PE-machine compatibility checks, architecture reports, and headless
timer/APC rounds. CI still cannot replace a desktop lab, and it does not claim
to. But it can keep architecture support from being aspirational prose.

The docs changed just as much as the code. The refreshed documentation is
layered: concepts first, reproducible lab steps next, then architecture pages,
implementation internals, validation semantics, research context, and
maintainer guidance. That structure is not just organization for its own sake.
It lets a reader learn the idea without being handed an adaptation guide. It
also lets maintainers talk about evidence boundaries in one place instead of
sprinkling caveats randomly through a long README.

That was the mood of the refresh: less cleverness, more accounting.

## The docs are part of the artifact

For a project like Gargoyle, documentation is not a wrapper around the proof of
concept. It is part of the proof of concept.

That sounds grander than I mean it. I do not mean that prose can substitute for
working code. I mean that a research artifact teaches through the path it gives
readers. If the only path is “read the source and infer the story,” then the
most confident readers will infer too much and the most cautious readers will
have to do archaeology. Neither outcome is ideal.

The refreshed docs are layered because the audience is layered. A curious reader
should be able to understand the temporal-state idea before seeing a build
command. A defender should be able to find the validation limits without reading
assembly. A maintainer should be able to see how the PIC artifacts are produced,
which harness modes collect which evidence, and why architecture-specific claims
are worded so carefully. A future contributor should also see the guardrails:
do not turn a benign demo into an operator workflow; do not add features that
make the research artifact less safe to reproduce; do not let “future work”
become a euphemism for expanding capability.

That is why the docs spend so much time on claim language. “Proves” is reserved
for evidence the harness or manual observation directly supports. “Suggests” is
for consistent evidence that still leaves gaps. “Does not prove” is not a
defensive crouch; it is an engineering courtesy. It tells the reader where the
edge of the observation is.

This is also why the original Win32 story stays central. It would be tempting to
flatten the architecture pages into a compatibility matrix and let the newer
siblings feel like replacements. That would erase the historical shape of the
work. The x64, ARM64, and ARM64EC versions are useful precisely because they sit
beside the original rather than pretending the old stack-pivot design was
architecture-neutral all along.

## The `SleepEx` correction

The most important technical correction is easy to state and easy to
underestimate.

Microsoft’s
[`SetWaitableTimer` documentation](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-setwaitabletimer)
distinguishes the timer becoming signaled from the APC completion routine being
called. When a completion routine is supplied, the APC is queued to the thread
that set the timer. That routine runs when the thread enters an alertable wait.
Microsoft’s
[`SleepEx` documentation](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-sleepex)
describes that alertable wait behavior directly.

The weak model is:

1. Set a waitable timer.
2. Wait on the timer handle.
3. Observe that the wait returned.
4. Infer that the completion routine ran.

The corrected model is:

1. Set a waitable timer with a completion routine.
2. Enter an alertable wait with `SleepEx(INFINITE, TRUE)`.
3. Let the timer due time queue the APC.
4. Dispatch the completion routine while the thread is alertable.
5. Interpret later re-entry evidence according to what the validation path
   actually observed.

The refreshed
[timer/APC docs](https://github.com/JLospinoso/gargoyle/blob/master/docs/concepts/timer-apc-sleepex.md)
make that correction explicit. The thread that configured the timer enters an
alertable `SleepEx` wait, giving the queued APC a documented dispatch point.

This is a good humility moment because the wrong proof can look a lot like the
right proof. A timer can become signaled. A UI marker can appear later. A page
can have the protection you expect when you inspect it. But if the claim is
about a specific asynchronous path, the validation has to connect to that path.

The refreshed
[validation overview](https://github.com/JLospinoso/gargoyle/blob/master/docs/validation/overview.md)
therefore uses narrower language. On x86 and x64, live validation closes two
benign MessageBoxes. The first validates initial handoff into the setup path.
The later one validates controlled re-entry into the benign path after the
alertable wait. That is consistent with the intended timer/APC behavior, but it
does not independently establish callback identity or capture every protection
transition.

ARM64 and ARM64EC headless validation is stronger for callback delivery because
the native runtime records completed-round and callback-round counters. That
still does not prove every possible memory-forensics claim. It does give a more
direct local signal that the callback body ran than the x86/x64 live window
check provides.

I like that distinction. It is fussy in the way good engineering is fussy.

## Canonical, sibling, sibling, sibling

The architecture story is deliberately asymmetric.

Win32/x86 is the canonical historical proof. It is the original shape:
`main.cpp`, `setup.nasm`, `gadget.nasm`, the stack trampoline, the system-DLL
gadget search, and the fallback `gadget.pic`. It is the reference story because
that is what Gargoyle was in 2017.

x64 is a sibling demonstration, not a transparent port of the x86 design. This
is a subtle but important boundary. The x64 version has a comparable teaching
goal, but it does not implement a corollary `mshtml.dll` trampoline path. The
[x64 docs](https://github.com/JLospinoso/gargoyle/blob/master/docs/architectures/x64-sibling.md)
describe separate `setup_x64.pic` and `reentry_x64.pic` artifacts. The re-entry
PIC remains executable while the setup PIC is parked, enters
`SleepEx(INFINITE, TRUE)`, and handles the restore shape around timer/APC
re-entry. That validates a sibling temporal-state demonstration under x64 ABI
constraints. It is not the old stack-pivot chain dressed up in 64-bit clothes.

ARM64 is another sibling demonstration. It exists because Windows-on-Arm is now
practical enough to care about in a maintenance story. The ARM64 version uses
ARMASM and COFF `.text` extraction for PIC generation, follows ARM64 calling
conventions, supports architecture reports and headless validation, and records
the completed/callback counters that make the non-interactive evidence more
specific. The
[ARM64 docs](https://github.com/JLospinoso/gargoyle/blob/master/docs/architectures/arm64-sibling.md)
are careful about the lab boundary: hosted CI can build and smoke-test the
headless path, while live desktop validation still requires an appropriate ARM64
Windows desktop.

ARM64EC is the sibling with the most interesting caveat. ARM64EC has special
rules for dynamic code. Microsoft’s
[ARM64EC ABI documentation](https://learn.microsoft.com/en-us/windows/arm/arm64ec-abi)
describes the distinction between ordinary executable dynamic memory and
ARM64EC dynamic code. The Gargoyle ARM64EC runtime uses the EC-code allocation
path needed by this demo, and the
[ARM64EC docs](https://github.com/JLospinoso/gargoyle/blob/master/docs/architectures/arm64ec-sibling.md)
say exactly that. It validates build identity, runtime identity, the demo’s
EC-code allocation behavior, and benign timer/APC semantics. It does not
demonstrate mixed x64 DLL interop. It is not a general proof for every ARM64EC
dynamic-code pattern.

This architecture language is less catchy than “now ported everywhere.” Good.
“Ported everywhere” would be wrong.

## The decade around Gargoyle

One of the stranger parts of revisiting Gargoyle was seeing the idea refracted
through other people’s work.

The first conversation was declared relationship. WithSecure’s
[`dotnet-gargoyle`](https://github.com/WithSecureLabs/dotnet-gargoyle)
describes itself as a spiritual .NET equivalent. YouMayPasser describes itself
as an [x64 implementation of\\
Gargoyle](https://github.com/waldo-irc/YouMayPasser). DeepSleep describes
itself as a [Gargoyle-like x64\\
variant](https://github.com/thefLink/DeepSleep). I treat those as declared
relationships, not because their mechanics are identical, but because the
sources say so.
[ShellcodeFluctuation](https://github.com/mgeeky/ShellcodeFluctuation) is close
but different: it explicitly says Gargoyle introduced the author to
memory-protection flipping, while changing the mechanics enough that I would
describe it as explicitly inspired and mechanically adjacent rather than a
literal continuation.

The second conversation was the broader sleep-obfuscation family.
[Ekko](https://github.com/Cracked5pider/Ekko),
[Cronos](https://github.com/Idov31/Cronos), FOLIAGE-related analysis, timer
queues, context restoration, dormant-state changes, and stack-spoofing
discussions all live near the same problem: these techniques make
security-relevant state brief, delayed, or distributed across ordinary-looking
mechanisms. MDSec’s
[How I Met Your Beacon](https://www.mdsec.co.uk/2022/07/part-1-how-i-met-your-beacon-overview/)
series places several of these ideas in a broader page-protection and
event-driven sleep-obfuscation family. WithSecure’s
[timer-queue hunting work](https://labs.withsecure.com/publications/hunting-for-timer-queue-timers)
shows how quickly the defensive question becomes mechanism-specific: a waitable
timer/APC proof and a timer-queue family may rhyme, but they do not leave the
same evidence. I read these sources as family mapping, not proof of common
descent.

The third conversation was defensive and academic, and it is the one I find most
encouraging. Elastic’s
[Hunting In Memory](https://www.elastic.co/security-labs/hunting-memory) placed
Gargoyle in a memory-resident technique taxonomy and pointed at threads and user
APCs as part of the evidence surface. F-Secure/Countercept work, later visible
through public Volatility plugin artifacts and summaries, turned the idea into
timer/APC and ROP-chain analysis questions; the
[Volatility Foundation contest summary](https://volatilityfoundation.org/results-from-the-2018-volatility-contests-are-in/)
describes the plugin’s timer APC inspection, emulation, ROP-chain following, and
`VirtualProtectEx` argument analysis. The public
[WithSecureLabs Volatility plugin](https://github.com/WithSecureLabs/volatility-plugins/blob/master/gargoyle.py)
is a nice artifact of that response.

Academic work sharpened the distinction further.
[PTE-aware memory-forensics research](https://dfrws.org/wp-content/uploads/2019/06/2019_USA_paper-windows_memory_forensics_detecting_unintentionally_hidden_injected_code_by_examining_page_table_entries.pdf)
asked what page-table evidence can reveal when higher-level views are
incomplete.
[Later memory-subversion work](https://dfrws.org/wp-content/uploads/2020/10/2020_USA_paper-hiding_process_memory_via_anti-forensic_techniques.pdf)
compared Gargoyle-style protection cycling with stronger approaches that
manipulate memory-management structures more deeply.
[Black Hat Asia 2023 work on transient implant-state footprints](https://i.blackhat.com/Asia-23/AS-23-Uhlmann-You-Can-Run-But-You-Cant-Hide.pdf)
discussed the residue left by pages that were executable earlier in a process
lifetime, including CFG bitmap evidence. That is exactly the defender-friendly
future I hoped the refresh would point toward: the old proof teaches a state
machine, and newer tools ask what the state machine leaves behind.

Category discipline matters here. Citation is not derivation. Similarity is not
lineage. Defensive analysis is not an endorsement of misuse. Stronger
anti-forensics are not “Gargoyle but better”; they are a different class of
problem. The refreshed
[lineage docs](https://github.com/JLospinoso/gargoyle/blob/master/docs/research/lineage.md)
try to keep those categories separate because folklore is the enemy of useful
history.

There is another reason to be careful with lineage: influence is not the only
interesting thing. Sometimes the useful lesson is convergence. If several
projects end up exploring timers, callbacks, protection transitions, dormant
state changes, or stack provenance, that does not necessarily mean they all come
from one root. It may mean the defensive pressure created a set of obvious
design tensions. For a retrospective, that is at least as interesting as a
family tree.

## What defenders can take from it now

The first defensive takeaway is to treat memory state as a time series.

A snapshot can be valuable, but it is still a slice. If a private region was
executable, is now non-executable, and may become executable again, the
interesting question is not only “what protection does this page have?” It is
“what sequence of events led here, and what evidence did those events leave?”

The second takeaway is to correlate mechanisms that are individually ordinary.
Timers are ordinary. APCs are ordinary. Alertable waits are ordinary. Memory
protection changes can be ordinary. Private memory can be ordinary. The signal
comes from the relationship: repeated private-region protection transitions,
callback or timer state, stack provenance, memory content history, and runtime
context forming a coherent state machine.

The third takeaway is to use more than one memory abstraction. VADs, PTEs, PFNs,
CFG bitmaps, thread stacks, timer objects, user-mode API traces, ETW, kernel
telemetry, and endpoint histories all answer different questions. If those
answers disagree, the disagreement may be the point. Gargoyle’s old scanner
assumption was narrow enough to make that lesson visible. Modern defensive work
has many more places to look.

This is where the field feels meaningfully different from 2017. The old proof
was interesting because it exposed a gap in a simple point-in-time predicate.
Modern defenders are much less confined to that predicate. They can ask whether
a region was executable earlier, whether a callback target is plausible, whether
a sleeping thread’s stack tells a coherent story, whether page-table evidence
matches a higher-level memory map, whether endpoint telemetry recorded a
protection change, and whether benign software in the environment produces
similar patterns. None of those signals is magic. Together they make the old
snapshot assumption feel much less lonely.

The fourth takeaway is to build benign corpora. A safe, documented, intentionally
boring program that exercises temporal memory-state behavior can help defenders
test assumptions without importing an operator workflow. The refreshed Gargoyle
repo should be useful as a teaching object and validation target precisely
because it refuses to become larger than that.

Benign corpora are underrated in this space. It is easy to benchmark a detector
against dramatic artifacts and then learn the wrong lesson. Real environments
have browsers, JIT runtimes, security products, game anti-cheat, DRM,
instrumentation frameworks, packed software, developer tools, and all sorts of
perfectly legitimate reasons for memory to look strange. A good research corpus
should help measure false positives as well as misses. Gargoyle can only be one
small case in that corpus, but it is useful because the intended state machine
is labeled and explainable.

The fifth takeaway is to keep evidence language honest. A live MessageBox
validates a visible benign action. A second live MessageBox validates later
controlled re-entry into the benign path. ARM64/ARM64EC completed-round and
callback-round counters give stronger callback-delivery evidence. An artifact
check validates files and PE metadata. An architecture report validates runtime
identity facts. A memory-map observation can support the temporal-state model
during sampled windows. None of those statements should inflate into a product
claim.

The defensive version of Gargoyle is not a trick. It is a measurement exercise.

## Safe reproduction

The safest way to approach the refreshed repository is to start with the docs,
not the source.

The [docs home](https://github.com/JLospinoso/gargoyle/blob/master/docs/index.md)
lays out reader paths. The
[quickstart](https://github.com/JLospinoso/gargoyle/blob/master/docs/quickstart.md)
gives the shortest safe build and validation path. The
[lab setup](https://github.com/JLospinoso/gargoyle/blob/master/docs/lab-setup.md)
page explains the Windows desktop assumptions. The
[validation limitations](https://github.com/JLospinoso/gargoyle/blob/master/docs/validation/limitations.md)
page is the guardrail: the project does not establish product evasion, general
stealth, durable footholds, deployment behavior, or broad operational capability.

For local automated validation, use the acceptance harness modes. Artifacts mode
checks expected outputs and PE metadata. Architecture mode records runtime
identity facts. ARM64 and ARM64EC headless mode exercises benign local rounds
and checks completed/callback counters. Live mode is the desktop MessageBox path
for an interactive lab.

For x86/x64 live validation, interpret the result narrowly. The first MessageBox
validates initial handoff. The later MessageBox validates controlled re-entry
into the benign path after the alertable wait. That is meaningful. It is also
scoped.

For ARM64/ARM64EC, the headless counters are the more interesting validation
artifact. They make callback delivery more directly observable in a CI-safe
way. The ARM64EC path adds its own caveat: it exercises the EC-code allocation
behavior used by the demo, not mixed x64 DLL interop and not general ARM64EC
dynamic-code behavior.

The right reproduction goal is modest: understand the state machine, run the
benign validation path appropriate to the architecture, and compare the observed
evidence to the claim being made.

That restraint is what keeps the project useful.

## The old new thing

The most interesting thing about Gargoyle in 2026 is not simply that an old
research idea still teaches something. It is that the old idea can now be held
to a better standard.

In 2017, I cared about demonstrating a clever mismatch between point-in-time
executable-memory scanning and time-varying execution state. That mismatch was
real. It remains useful. But revisiting the project made me care just as much
about the discipline around it.

What did the demo actually show? What did it merely suggest? Which claims were
architecture-specific? Which observations were available to defenders? Which
later projects were really descendants, and which were adjacent work solving a
related problem? Which parts of the original proof were durable, and which parts
belonged to the particular Windows/x86 moment in which I wrote it?

Those are healthier questions than “does the demo still work?”

Gargoyle is a small Windows research artifact about temporal memory state. The
refresh keeps the original Win32 proof recognizable, adds sibling demonstrations
for modern architecture realities, corrects an important APC validation
semantic, and documents the result with clearer boundaries. It does not make
Gargoyle more operational. It makes Gargoyle more legible.

That is a good ending for an old proof of concept: not that a hiding technique
won, but that measurement got better.

## Further reading

- Original article:
  [“gargoyle, a memory scanning evasion technique”](https://lospino.so/security/assembly/c/cpp/developing/software/2017/03/04/gargoyle-memory-analysis-evasion.html)
- Refreshed repo:
  [JLospinoso/gargoyle](https://github.com/JLospinoso/gargoyle)
- Key refreshed docs:
  [temporal memory state](https://github.com/JLospinoso/gargoyle/blob/master/docs/concepts/temporal-memory-state.md),
  [timer/APC and SleepEx](https://github.com/JLospinoso/gargoyle/blob/master/docs/concepts/timer-apc-sleepex.md),
  [architecture comparison](https://github.com/JLospinoso/gargoyle/blob/master/docs/architectures/comparison.md),
  [validation overview](https://github.com/JLospinoso/gargoyle/blob/master/docs/validation/overview.md),
  and [research references](https://github.com/JLospinoso/gargoyle/blob/master/docs/research/references.md)
- Windows API references:
  [`SetWaitableTimer`](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-setwaitabletimer),
  [`SleepEx`](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-sleepex),
  [waitable timers with APCs](https://learn.microsoft.com/en-us/windows/win32/sync/using-a-waitable-timer-with-an-asynchronous-procedure-call),
  [`VirtualProtectEx`](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualprotectex),
  and [ARM64EC ABI documentation](https://learn.microsoft.com/en-us/windows/arm/arm64ec-abi)
- Defensive and research context:
  [Elastic, “Hunting In Memory”](https://www.elastic.co/security-labs/hunting-memory),
  [WithSecureLabs Volatility plugin](https://github.com/WithSecureLabs/volatility-plugins/blob/master/gargoyle.py),
  [Volatility Foundation 2018 plugin contest summary](https://volatilityfoundation.org/results-from-the-2018-volatility-contests-are-in/),
  [WithSecure, “Hunting for timer-queue timers”](https://labs.withsecure.com/publications/hunting-for-timer-queue-timers),
  [MDSec, “How I Met Your Beacon”](https://www.mdsec.co.uk/2022/07/part-1-how-i-met-your-beacon-overview/),
  [PTE-aware memory-forensics research](https://dfrws.org/wp-content/uploads/2019/06/2019_USA_paper-windows_memory_forensics_detecting_unintentionally_hidden_injected_code_by_examining_page_table_entries.pdf),
  [memory-subversion anti-forensics research](https://dfrws.org/wp-content/uploads/2020/10/2020_USA_paper-hiding_process_memory_via_anti-forensic_techniques.pdf),
  and [Black Hat Asia 2023, “You Can Run But You Can’t Hide”](https://i.blackhat.com/Asia-23/AS-23-Uhlmann-You-Can-Run-But-You-Cant-Hide.pdf)

## Related

- [writing **C Constructs That Still Don’t Work in C++ — and a Few That Changed** _A language-mode-aware update on the C constructs that still break or change meaning in modern C++._](https://lospino.so/blog/c-constructs-that-still-dont-work-in-cpp/)
- [writing **The Function Signature Is a Lie** _Hidden result storage shows why the source signature is not the whole call._](https://lospino.so/blog/abi-series/the-function-signature-is-a-lie/)
- [writing **C++ Crash Course** _A reflection on modern C++, technical books, and the work of teaching systems programming clearly._](https://lospino.so/c/c++/programming/developing/software/2019/07/28/cpp-crash-course.html)
- [notes **Common x86 Calling Conventions** _A practical guide to cdecl, stdcall, and fastcall on x86, with stack layouts and NASM examples._](https://lospino.so/assembly/c/developing/software/2015/04/04/common-x86-calling-conventions.html)
- [writing **C Constructs That Don't Work in C++** _C idioms that fail or change meaning in C++, from pointer conversions to prototypes._](https://lospino.so/c/c++/programming/developing/software/2019/04/28/c-constructs-that-dont-work-in-cpp.html)