# https://aff-wg.org/2026/04/13/small-pic-energy/

[Skip to content](https://aff-wg.org/2026/04/13/small-pic-energy/#content)

I have a challenge for you:

How much beaconing agent functionality can you fit into 4KB PIC? How do you do it? This isn’t a shellcode golf challenge. It’s about elegant ways to build common agent stuff in C. I was able to get a WinINet loop, a light command kernel, and a BOF runner in mine. To do this, I relied on BOF inversions (discussed in this post). I did fudge a bit and rely on GCC’s ( [discouraged](https://aff-wg.org/2026/01/13/keeping-bin2bin-out-of-the-bin/)) -Os to shrink some modules. I didn’t want to though! One caution: if you start on this problem, you might get obsessed, and stop doing other work. That’s what happened to me. You’re warned.

The above is a form of “small PIC” energy. And, with this [Tradecraft Garden](https://tradecraftgarden.org/) and Crystal Palace release, I’m hoping to invite this energy into your projects.

The rest of this post is more thought exercise in nature. But, up front, here are the new features:

- It’s now OK to merge a [shared library](https://tradecraftgarden.org/docs.html#lib) into a project multiple times. Crystal Palace will ignore follow-on merges.
- We now have a [Simple BOF runner](https://tradecraftgarden.org/simplebof.html) in the Tradecraft Garden.
- And Crystal Palace is now accessible in a language agnostic way thanks to a new [JSON-over-HTTP sidecar](https://tradecraftgarden.org/sidecar.html) service

### Modular PIC Agents, Redux

I’m seeing [some experimentation](https://tradecraftgarden.org/references.html) with Crystal Palace for both capability development (e.g., PIC C2 agents) and as a composition kernel in some projects too. If I were baking Crystal Palace into a C2, here’s what I would do:

**(1) Separate the concerns**

I would separate the capability (e.g., a C2 agent) assembly and tradecraft combination as concerns

**(2) Assemble the capability**

To assemble the capability, I would use a .spec file to merge COFFs, patch in configuration, and (possibly) dynamically merge user-selected features \[or variant implementations\] in the capability.

This capability .spec would:

- output a COFF (make coff)
- merge any libraries the capability depends on

This capability.spec would NOT:

- use +optimize, +mutate, ised, or other code transformation things
- use linkfunc (the bin2bin may error out re-processing PIC in (3))
- use dfr, fixbss, fixptrs, etc. — these are time-of-use tradecraft choices

**(3) Pair Tradecraft with the Capability** To pair tradecraft with a capability, let the user choose a tradecraft .spec file. The .spec accepts a COFF, decides how to turn it into PIC (e.g., apply a [PIC services module](https://tradecraftgarden.org/simplepic.html) or pair it with a [PICO loader](https://tradecraftgarden.org/simpleobj.html)), brings in any runtime tradecraft, and outputs shellcode. This is also where +optimize, +mutate, ised, and other stuff should happen.

Take the above as a thought exercise rather than a prescriptive. My thought is that this is a logical way to separate concerns, delegate tradecraft to a single .spec (which may orchestrate multiple components), and keep the integration and UX simple.

### BOF Inversions

One of the ideas I’m excited about is using Crystal Palace to apply tradecraft to [Beacon Object Files](https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/content/topics/beacon-object-files_main.htm) before they’re passed to a C2 agent. Daniel Duggan’s [BOF Cocktails](https://rastamouse.me/bof-cocktails/) shares the details.

I love this, because it feeds the use-case agnostic capability and tradecraft separation this project is after.

Pairing research tradecraft directly to BOFs skips C2 entirely for the development, test, and demonstration of that tradecraft. This opens up room for [detection science](https://www.elastic.co/security-labs/detonating-beacons-to-illuminate-detection-gaps) that treats naked BOFs as a control and tradecraft-paired BOFs as variables. This separation frees research to thrive alongside but culturally separate from operations.

[C2 operators](https://www.youtube.com/watch?v=26PedM_-zRo) benefit too, as it means their BOFs are self-protecting and not dependent on the agent or C2 to bring evasion. And, for C2 engineers—this delegates another piece of your problem set to the BOFs themselves.

**The Chicken and Egg Problem** This ideal has a chicken and egg problem though. It makes little sense to integrate Crystal Palace directly or create hooks to intercept and edit BOFs, if there’s no eco-system of BOF cocktails. And, there’s not much incentive to write BOF cocktails, if there’s nowhere to use them yet.

**The Solution: BOF Inversions** I have a value proposition for C2 engineers that opens up the door for BOF cocktails and makes it much easier to support BOFs with minimal weight. I call it BOF inversions, as in—we’re inverting the implementation responsibility for BOFs and their API from the agent and into the linker and the BOF itself.

Here’s the idea:

1. A hypothetical C2 passes every BOF through a user-specified Crystal Palace .spec file
2. The .spec file [turns the BOF into a PICO](https://tradecraftgarden.org/simplebof.html?file=loader.spec) (via make object).
3. The .spec file also [merges](https://tradecraftgarden.org/simplebof.html?file=bofprep.spec) (most of) a [BOF API implementation](https://tradecraftgarden.org/simplebof.html?file=bofapi.c) into the BOF.
4. The agent receives the PICO and uses a [simple PICO runner](https://tradecraftgarden.org/simplebof.html?file=loader.c) to execute it.

To support the above, the agent needs a PICO runner function and an implementation of any BOF APIs that must live in the agent. In Tradecraft Garden’s [Simple BOF runner](https://tradecraftgarden.org/simplebof.html), I just needed BeaconOutput and that was it.

The fun of this scheme is that the agent no longer has to implement the Beacon API. These functions live inside of the BOF itself. And, thanks to +optimize, any APIs that aren’t needed are removed before the PICO is shipped to the agent.

Now, let the user configure or edit the .spec responsible for turning BOFs into PICOs and you have a natural integration point for [BOF cocktails](https://rastamouse.me/bof-cocktails/) too.

### Linker Sidecar Service and API

Using Crystal Palace as a capability composition kernel or implementing BOF inversions requires low latency time-of-use access to Crystal Palace. Prior to this release, that was only possible via the [Java API](https://tradecraftgarden.org/docs.html#javaapi). To open this project up to other language stacks, I’ve added a [Linker Sidecar](https://tradecraftgarden.org/sidecar.html) server to Crystal Palace. The new linkserve command starts this process.

The Linker Sidecar is a localhost-only [JSON-over-HTTP server](https://tradecraftgarden.org/sidecar.html) to use Crystal Palace.

The API follows the CLI’s concepts closely. The server accepts a JSON object with parameters and gives back a JSON object with base64 encoded output, yara rules, and messages from the linker. It’s a stateless one transaction POST request.

Here’s a [Python script](https://tradecraftgarden.org/download/client.py.txt) to act like ./link:

|     |
| --- |
| `import``sys`<br>`import``base64`<br>`import``requests`<br>`from``pathlib``import``Path`<br>`# Handle our arguments`<br>`if``len``(sys.argv) !``=``4``:`<br>```print``(``"Usage: python client.py <spec_file> <file.dll|.o> <output_file>"``)`<br>```sys.exit(``1``)`<br>`spec_file``=``str``( Path(sys.argv[``1``]).resolve() )`<br>`capab_file``=``str``( Path(sys.argv[``2``]).resolve() )`<br>`out_file``=``sys.argv[``3``]`<br>`url``=``"http://127.0.0.1:60060/link"`<br>`# Populate our arguments`<br>`linkargs``=``{`<br>```"action"``:``"link"``,`<br>```"params"``: {`<br>```"spec"``: spec_file,`<br>```"file"``: capab_file`<br>```}`<br>`}`<br>`# Make a request to the Sidecar`<br>`try``:`<br>```response``=``requests.post(url, json``=``linkargs)`<br>```response.raise_for_status()`<br>```data``=``response.json()`<br>```if``data.get(``"success"``)``is``True``:`<br>```print``(``"[*] Success"``)`<br>```if``data.get(``"message"``) !``=``"":`<br>```print``(data.get(``"message"``))`<br>```raw_binary``=``base64.b64decode(data[``"output_b64"``])`<br>```with``open``(out_file,``"wb"``) as f:`<br>```f.write(raw_binary)`<br>```else``:`<br>```print``(f``"[-] Failure {data.get('context')}:\n{data.get('message')}"``)`<br>`except``requests.exceptions.RequestException as e:`<br>```print``(f``"[-] HTTP Connection Error: {e}"``)` |

The [Linker Sidecar documentation](https://tradecraftgarden.org/sidecar.html) has the API details and example JSON for you. I put special care into the error messages, to make sure you’re not pulling your hair out if there’s a bad or missing parameter. I’m looking forward to seeing what you do with this.

### Migration Notes

None

### Closing Thoughts

I want to close by sharing how our small PIC is a response to another “Small PIC energy”. These thoughts get to the heart of how I see code and individual behavior as our agency to influence culture.

One of the occupational hazards of offensive security is ego. When I say ego, I’m not referring to a “my work speaks for itself” pride. But, instead, a missing something that drives some in the field to disparage other efforts, play word games to erase others’ contributions, and in the worst cases—drive chat and private conference whisper campaigns to stigmatize peers until their very name is irresistible safe red meat.

All of these things come from a zero-sum approach to participation in the profession. That is, if anyone who threatens their self-image continues to exist or worse–gets acknowledgement, it’s a game they’ve somehow lost. Commercial product interests have made these tendencies much worse. These insecure and ego-driven behaviors are “Small PIC energy”.

This passive-aggressive cruelty can look like bold thought leadership because it’s loud and because community leaders and established peers pretend it’s something else. This looks like permission, but it’s discomfort and fear to act when their “friends” throw the punches. In these situations, tribal cliques form that mix uncomfortable participants, eager followers, partners who sell the tribe’s virtue, and loud leaders that bully “others”. To outsiders, it looks like consensus. To the collective profession, this unchecked dynamic is contagious, divisive, and destructive.

There’s another way. I believe code can shape communities. The secret is to see the ready potential in others. Genuinely want their success. And, work to create space and opportunity for that success. This requires a belief that our success comes with theirs. In this playbook, the collective improvement of our peers and ourselves is [the product](https://www.cobaltstrike.com/blog/raphaels-transition). Not the technology. I ~~was~~ [am](https://lorenzomeacci.com/bypassing-edr-in-a-crystal-clear-way) proud to see people [build](https://aff-wg.org/2025/04/10/post-ex-weaponization-an-oral-history/) on things I put out there and grateful to learn from them as they do. I remain awed that our niche profession drove the industry’s [real](https://aff-wg.org/2025/09/26/analysis-of-a-ransomware-breach/) [technical conversation](https://aff-wg.org/2025/03/13/the-security-conversation/) in a way no one else could. Tradecraft Garden is an effort to revive this in a ‘now’ considered way. small PIC > “Small PIC energy”.

To see what’s new, check out the [release notes](https://tradecraftgarden.org/releasenotes.txt).

- [Subscribe](https://aff-wg.org/2026/04/13/small-pic-energy/) [Subscribed](https://aff-wg.org/2026/04/13/small-pic-energy/)








  - [![](https://aff-wg.org/wp-content/uploads/2024/08/cropped-affwgsiteimage_nowreath.png?w=50) Adversary Fan Fiction Writers Guild](https://aff-wg.org/)

Join 105 other subscribers

Sign me up

  - Already have a WordPress.com account? [Log in now.](https://wordpress.com/log-in?redirect_to=https%3A%2F%2Fr-login.wordpress.com%2Fremote-login.php%3Faction%3Dlink%26back%3Dhttps%253A%252F%252Faff-wg.org%252F2026%252F04%252F13%252Fsmall-pic-energy%252F)


- - [![](https://aff-wg.org/wp-content/uploads/2024/08/cropped-affwgsiteimage_nowreath.png?w=50) Adversary Fan Fiction Writers Guild](https://aff-wg.org/)
  - [Subscribe](https://aff-wg.org/2026/04/13/small-pic-energy/) [Subscribed](https://aff-wg.org/2026/04/13/small-pic-energy/)
  - [Sign up](https://wordpress.com/start/)
  - [Log in](https://wordpress.com/log-in?redirect_to=https%3A%2F%2Fr-login.wordpress.com%2Fremote-login.php%3Faction%3Dlink%26back%3Dhttps%253A%252F%252Faff-wg.org%252F2026%252F04%252F13%252Fsmall-pic-energy%252F)
  - [Copy shortlink](https://wp.me/pfXSCG-s7)
  - [Report this content](https://wordpress.com/abuse/?report_url=https://aff-wg.org/2026/04/13/small-pic-energy/)
  - [View post in Reader](https://wordpress.com/reader/blogs/235916366/posts/1743)
  - [Manage subscriptions](https://subscribe.wordpress.com/)
  - [Collapse this bar](https://aff-wg.org/2026/04/13/small-pic-energy/)