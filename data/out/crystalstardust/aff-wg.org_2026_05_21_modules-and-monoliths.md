# https://aff-wg.org/2026/05/21/modules-and-monoliths/

[Skip to content](https://aff-wg.org/2026/05/21/modules-and-monoliths/#content)

Last week, memN0ps published [DoublePulsar: A User-defined Reflective Loader in the Crystal Palace and Tradecraft Garden Era](https://memn0ps.github.io/doublepulsar-a-user-defined-reflective-loader-in-the-crystal-palace-and-tradecraft-garden-era/). It’s a lengthy blog post, about 50 printed pages. And, most of those are devoted to memN0ps’ fantastic deep-dive into evasion mechanics and conquering the challenges of building a [monolithic UDRL](https://github.com/memN0ps/doublepulsar-rs) using Rust’s nightly toolchain.

memN0ps devoted significant space to contrasting monolithic UDRL development to my [Crystal Palace](https://tradecraftgarden.org/crystalpalace.html) and Daniel Duggan’s [Crystal Kit](https://github.com/rasta-mouse/Crystal-Kit). The post spends time on Crystal Kit’s deviations from evasive loader best practice. And, memN0ps celebrates bespoke loader development as a higher-skill, more [fundamentals-informed](https://vimeo.com/1100089433?share=copy&fl=sv&fe=ci) path. The post’s assertions are turn-key operations focused, imply a lack of agency for folks who don’t build monoliths, and don’t represent [Tradecraft Garden](https://tradecraftgarden.org/) as I see it.

Daniel didn’t release [Crystal Kit](https://github.com/rasta-mouse/Crystal-Kit) as an exemplar trend-conforming evasion cocktail. It started as [an exploration](https://rastamouse.me/crystal-kit/) of Crystal Palace’s C2 agnostic claim, by adding evasion to [Cobalt Strike](https://www.cobaltstrike.com/) without Cobalt Strike’s specific interfaces. It’s also an open source modular foundation for students in Daniel’s [CRTL course](https://www.zeropointsecurity.co.uk/course/red-team-ops-ii). Its default state provides room to apply specific techniques to push back on specific observables. Relevant: a [Crystal Kit fork](https://github.com/nickswink/Crystal-Kit-Xenon) for the [Xenon Mythic agent](https://github.com/MythicAgents/Xenon) exists too.

Tradecraft Garden’s mission is to separate tradecraft and capability. I solved [time-of-use composition](https://aff-wg.org/2026/04/13/small-pic-energy/) with a linker because linkers compose programs. Going further, I’m breaking the post-exploitation tradecraft chain into discrete components. I’m doing this to encourage folks to conduct new research, write code, and publish defense guidance or document truth on those stand-alone components.

LibTCG and loaders like Crystal Kit are part of an effort to find best practice dividing lines between post-exploitation tradecraft components. For example, [LibTCG](https://tradecraftgarden.org/libtcg.html) uses a direct PEB walk. But, let’s say someone has a module lookup [technique](https://tradecraftgarden.org/simplepatch.html) that does something else: Crystal Palace’s [services module](https://tradecraftgarden.org/simplepic.html) pattern can bring that technique into a loader or capability without modification. In this scheme, I didn’t take away PEB walking control from a researcher. I’ve componentized it and made it something that can get swapped out. In doing this, I’m creating space for deep study and experimentation on this one piece of the puzzle. This specialization is how things move forward.

The synergy of this model is showing up. Last year, Daniel Duggan published [LibTP](https://github.com/rasta-mouse/LibTP) for [proxying NT API calls via the Threadpool](https://0xdarkvortex.dev/proxying-dll-loads-for-hiding-etwti-stack-tracing/). SAERXCIT published [a blog post](https://offsec.almond.consulting/evading-elastic-callstack-signatures.html) on how to evade callstack signatures with call gadgets. And, to prove it out SAERXCIT published a [LibTP-compatible](https://github.com/SAERXCIT/LibTP_Gadget) Crystal Palace [shared library](https://tradecraftgarden.org/docs.html#lib) to drop-in demonstrate their primitive. None of this demonstration involved weaponization with a C2.

What I see is the red teaming “advanced tradecraft” (Win32) meta is nearly a checklist right now. By breaking down the post-exploitation tradecraft problem set, I’m hoping more [ideas](https://bigbingus.com/posts/stop-being-weird/) and [approaches](https://github.com/boku7/Loki) emerge. Where my project is courting red teaming-aligned researchers (and it is, [leverage](https://vimeo.com/1170068618) is the candy), it’s an effort to bring their research energy into this ground truth model.

This ground truth model is not about outputs to deliberately “best” EDR X today. I strongly believe that research isn’t for turn-key circumvention of specific security products. It’s higher impact to seek and explain possibilities, blindspots, and areas where whole classes of security technology are weak (e.g., [categorical techniques](https://www.cobaltstrike.com/blog/pushing-back-on-userland-hooks-with-cobalt-strike) are in scope). Tradecraft Garden’s model encourages componentization, [de-escalated release](https://aff-wg.org/2026/02/02/the-islands-of-invariance/), and favors impact demonstration through [system events and properties](https://www.cobaltstrike.com/blog/in-memory-evasion) if possible. Where security exercise use is desired—this use-agnostic model empowers, but also expects, the red team to choose, adapt, and validate before they deploy.

[My goal](https://vimeo.com/1074106659#t=4556) is to platform systems security research, separate from the edit and recompile evasion treadmill, and create an outcome where red and blue efforts [may](https://www.youtube.com/watch?v=09A5qds1Zss&list=RD09A5qds1Zss&start_radio=1) benefit from these fundamental outputs at the same time.

I want to thank [memN0ps](https://github.com/memn0ps) for publishing their [Rust loader](https://github.com/memN0ps/doublepulsar-rs) and sharing their process with us. As a fellow researcher, passionate about the craft, I appreciate what a gift of labor and creativity their work is. Further, I appreciate their blog post as a mirror of some project messaging gaps I needed to address.

- [Subscribe](https://aff-wg.org/2026/05/21/modules-and-monoliths/) [Subscribed](https://aff-wg.org/2026/05/21/modules-and-monoliths/)








  - [![](https://aff-wg.org/wp-content/uploads/2024/08/cropped-affwgsiteimage_nowreath.png?w=50) Adversary Fan Fiction Writers Guild](https://aff-wg.org/)

Join 105 other subscribers

Sign me up

  - Already have a WordPress.com account? [Log in now.](https://wordpress.com/log-in?redirect_to=https%3A%2F%2Fr-login.wordpress.com%2Fremote-login.php%3Faction%3Dlink%26back%3Dhttps%253A%252F%252Faff-wg.org%252F2026%252F05%252F21%252Fmodules-and-monoliths%252F)


- - [![](https://aff-wg.org/wp-content/uploads/2024/08/cropped-affwgsiteimage_nowreath.png?w=50) Adversary Fan Fiction Writers Guild](https://aff-wg.org/)
  - [Subscribe](https://aff-wg.org/2026/05/21/modules-and-monoliths/) [Subscribed](https://aff-wg.org/2026/05/21/modules-and-monoliths/)
  - [Sign up](https://wordpress.com/start/)
  - [Log in](https://wordpress.com/log-in?redirect_to=https%3A%2F%2Fr-login.wordpress.com%2Fremote-login.php%3Faction%3Dlink%26back%3Dhttps%253A%252F%252Faff-wg.org%252F2026%252F05%252F21%252Fmodules-and-monoliths%252F)
  - [Copy shortlink](https://wp.me/pfXSCG-wi)
  - [Report this content](https://wordpress.com/abuse/?report_url=https://aff-wg.org/2026/05/21/modules-and-monoliths/)
  - [View post in Reader](https://wordpress.com/reader/blogs/235916366/posts/2002)
  - [Manage subscriptions](https://subscribe.wordpress.com/)
  - [Collapse this bar](https://aff-wg.org/2026/05/21/modules-and-monoliths/)