# https://specterops.io/blog/2026/03/04/offensive-dpapi-with-nemesis/

![Revisit consent button](https://cdn-cookieyes.com/assets/images/revisit.svg)

We value your privacy

We use cookies to enhance your browsing experience, serve personalized ads or content, and analyze our traffic. By clicking "Accept All", you consent to our use of cookies.

CustomizeReject AllAccept All

Customize Consent Preferences![](https://cdn-cookieyes.com/assets/images/close.svg)

NecessaryAlways Active

Necessary cookies are required to enable the basic features of this site, such as providing secure log-in or adjusting your consent preferences. These cookies do not store any personally identifiable data.

- Cookie

\_cfuvid

- Duration

session

- Description

Calendly sets this cookie to track users across sessions to optimize user experience by maintaining session consistency and providing personalized services


- Cookie

\_GRECAPTCHA

- Duration

6 months

- Description

Google Recaptcha service sets this cookie to identify bots to protect the website against malicious spam attacks.


- Cookie

cookieyes-consent

- Duration

1 year

- Description

CookieYes sets this cookie to remember users' consent preferences so that their preferences are respected on subsequent visits to this site. It does not collect or store any personal information about the site visitors.


Functional

Functional cookies help perform certain functionalities like sharing the content of the website on social media platforms, collecting feedback, and other third-party features.

- Cookie

li\_gc

- Duration

6 months

- Description

Linkedin set this cookie for storing visitor's consent regarding using cookies for non-essential purposes.


- Cookie

lidc

- Duration

1 day

- Description

LinkedIn sets the lidc cookie to facilitate data center selection.


- Cookie

yt-remote-device-id

- Duration

Never Expires

- Description

YouTube sets this cookie to store the user's video preferences using embedded YouTube videos.


- Cookie

ytidb::LAST\_RESULT\_ENTRY\_KEY

- Duration

Never Expires

- Description

The cookie ytidb::LAST\_RESULT\_ENTRY\_KEY is used by YouTube to store the last search result entry that was clicked by the user. This information is used to improve the user experience by providing more relevant search results in the future.


- Cookie

yt-remote-connected-devices

- Duration

Never Expires

- Description

YouTube sets this cookie to store the user's video preferences using embedded YouTube videos.


- Cookie

yt-remote-session-app

- Duration

session

- Description

The yt-remote-session-app cookie is used by YouTube to store user preferences and information about the interface of the embedded YouTube video player.


- Cookie

yt-remote-cast-installed

- Duration

session

- Description

The yt-remote-cast-installed cookie is used to store the user's video player preferences using embedded YouTube video.


- Cookie

yt-remote-session-name

- Duration

session

- Description

The yt-remote-session-name cookie is used by YouTube to store the user's video player preferences using embedded YouTube video.


- Cookie

yt-remote-fast-check-period

- Duration

session

- Description

The yt-remote-fast-check-period cookie is used by YouTube to store the user's video player preferences for embedded YouTube videos.


Analytics

Analytical cookies are used to understand how visitors interact with the website. These cookies help provide information on metrics such as the number of visitors, bounce rate, traffic source, etc.

- Cookie

pardot

- Duration

past

- Description

The pardot cookie is set while the visitor is logged in as a Pardot user. The cookie indicates an active session and is not used for tracking.


- Cookie

ajs\_anonymous\_id

- Duration

1 year

- Description

This cookie is set by Segment to count the number of people who visit a certain site by tracking if they have visited before.


- Cookie

ajs\_user\_id

- Duration

Never Expires

- Description

This cookie is set by Segment to help track visitor usage, events, target marketing, and also measure application performance and stability.


- Cookie

uid

- Duration

1 year 1 month 4 days

- Description

This is a Google UserID cookie that tracks users across various website segments.


- Cookie

sid

- Duration

1 year 1 month 4 days

- Description

The sid cookie contains digitally signed and encrypted records of a user’s Google account ID and most recent sign-in time.


- Cookie

\_ga

- Duration

1 year 1 month 4 days

- Description

Google Analytics sets this cookie to calculate visitor, session and campaign data and track site usage for the site's analytics report. The cookie stores information anonymously and assigns a randomly generated number to recognise unique visitors.


- Cookie

\_ga\_\*

- Duration

1 year 1 month 4 days

- Description

Google Analytics sets this cookie to store and count page views.


- Cookie

\_gcl\_au

- Duration

3 months

- Description

Google Tag Manager sets the cookie to experiment advertisement efficiency of websites using their services.


Performance

Performance cookies are used to understand and analyze the key performance indexes of the website which helps in delivering a better user experience for the visitors.

No cookies to display.

Advertisement

Advertisement cookies are used to provide visitors with customized advertisements based on the pages you visited previously and to analyze the effectiveness of the ad campaigns.

- Cookie

bcookie

- Duration

1 year

- Description

LinkedIn sets this cookie from LinkedIn share buttons and ad tags to recognize browser IDs.


- Cookie

visitor\_id\*

- Duration

1 year 1 month 4 days

- Description

Pardot sets this cookie to store a unique user ID.


- Cookie

visitor\_id\*-hash

- Duration

1 year 1 month 4 days

- Description

Pardot sets this cookie to store a unique user ID.


- Cookie

YSC

- Duration

session

- Description

Youtube sets this cookie to track the views of embedded videos on Youtube pages.


- Cookie

VISITOR\_INFO1\_LIVE

- Duration

6 months

- Description

YouTube sets this cookie to measure bandwidth, determining whether the user gets the new or old player interface.


- Cookie

VISITOR\_PRIVACY\_METADATA

- Duration

6 months

- Description

YouTube sets this cookie to store the user's cookie consent state for the current domain.


- Cookie

yt.innertube::requests

- Duration

Never Expires

- Description

YouTube sets this cookie to register a unique ID to store data on what videos from YouTube the user has seen.


- Cookie

yt.innertube::nextId

- Duration

Never Expires

- Description

YouTube sets this cookie to register a unique ID to store data on what videos from YouTube the user has seen.


Uncategorised

Other uncategorized cookies are those that are being analyzed and have not been classified into a category as yet.

- Cookie

\_zitok

- Duration

1 year

- Description

Description is currently not available.


- Cookie

lpv603731

- Duration

1 hour

- Description

Description is currently not available.


- Cookie

\_\_Secure-ROLLOUT\_TOKEN

- Duration

6 months

- Description

Description is currently not available.


Reject AllSave My PreferencesAccept All

Powered by [![Cookieyes logo](https://cdn-cookieyes.com/assets/images/poweredbtcky.svg)](https://www.cookieyes.com/product/cookie-consent/?ref=cypbcyb&utm_source=cookie-banner&utm_medium=powered-by-cookieyes)

[Introducing BloodHound Scentry: Accelerate your APM practice. Learn More](https://specterops.io/bloodhoundscentry/)

[Back to Blog](https://specterops.io/blog)

[Research & Tradecraft](https://specterops.io/blog/category/research/)

Offensive DPAPI With Nemesis

Author

[Will Schroeder](https://specterops.io/blog/author/will-schroeder/), [Lee Chagolla-Christensen](https://specterops.io/blog/author/lchristensenspecterops-io/)

Read Time

16 mins

Published

Mar 4, 2026

##### Share

_**TL;DR**: Nemesis 2.2 automates the entire DPAPI decryption chain – from SYSTEM/user masterkeys through CNG keys to Chromium’s latest App-Bound Encryption – with robust forward as well as retroactive decryption._

The Windows Data Protection API, or DPAPI, is the fun little technology that just won’t disappear from offensive operations. I first talked about abusing DPAPI on operations in my 2018 post [Operational Guidance for Offensive User DPAPI Abuse](https://specterops.io/blog/2018/08/22/operational-guidance-for-offensive-user-dpapi-abuse/). Some things have changed since then, but plenty stayed the same. SpecterOps has touched on using DPAPI in specific use cases over the last several years, from [Slack](https://specterops.io/blog/2023/11/09/abusing-slack-for-offensive-operations-part-2/), to capturing [custom entropy](https://specterops.io/blog/2022/05/18/entropycapture-simple-extraction-of-dpapi-optional-entropy/), and even how it factors into protections for [certificates and CA private keys](https://specterops.io/blog/2021/06/17/certified-pre-owned/), but the major systems and tool(s) we used for abuse didn’t majorly change until [Nemesis 1.0.0](https://specterops.io/blog/2023/08/09/hacking-with-your-nemesis/) (and then with my colleague [Andrew Gomez’](https://github.com/KingOfTheNOPs/) [cookie-monster](https://github.com/KingOfTheNOPs/cookie-monster/) project for Chrome v1.37+).

During our recent Nemesis 2.2 development sprint, we turned our eyes to DPAPI yet again and heavily revamped how we use and abuse DPAPI. This post will summarize the major new DPAPI features, how everything works internally, and will give you everything you need to get started analyzing and abusing DPAPI in Nemesis!

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_072325.png?w=1024)_Nemesis Is a Cookie Monster_

**_Note:_** _What we’re talking about here will not touch on TPM usage. We’re handling purely file and memory based approaches._

**_Another note_** **:** In case it isn’t obvious, DPAPI applies to only Windows, so while there is some overlap in how Chrome/Chromium protects secrets on other platforms like macOS. We’re only going to focus on the Windows side of the house today.

# DPAPI Background

Every DPAPI post has to begin with a quick (or no-so-quick) primer on DPAPI. As I listed a number of DPAPI references in the introduction, I’m going to make this on the quicker side. This diagram explains the current state of Windows DPAPI protection, specifically in relation to Chromium Cookie and Login Data protection:

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_c4d419.png?w=1024)_Chromium DPAPI Decryption_

Definitely not complicated. Nope. Not at all.

While things have gotten more complicated with Google Chromium’s App-Bound Encryption (ABE) approach, particularly with the Chromium 137+ update that introduced the Cryptography API: Next Generation ( [CNG](https://learn.microsoft.com/en-us/windows/win32/seccng/about-cng)) wrinkle, the base of everything else is heavily the same.

There are a lot of interconnected files here that link forward and backward, something you can certainly decrypt manually piece by piece, or now have Nemesis automate everything for you!

**To note:** Nemesis doesn’t do anything particularly novel here. We just adapted public code and information to automate the DPAPI + Chromium decryption processes as much as we could. The rest of this post will break down specific subcomponents and show how Nemesis handles them. Shoutout to these awesome projects that we built on top of: [pypykatz](https://github.com/skelsec/pypykatz/), [Impacket](https://github.com/fortra/impacket), [DPAPIck3](https://github.com/tijldeneut/DPAPIck3). Also shoutout to these awesome projects that helped work out the newest version of Chromium’s app-bound-encryption approach: [chrome\_v20\_decryption](https://github.com/runassu/chrome_v20_decryption/), [cookie-monster](https://github.com/KingOfTheNOPs/cookie-monster/), and [DIANA](https://github.com/tijldeneut/diana/).

# SYSTEM DPAPI Masterkeys

The DPAPI masterkeys for a particular system are treated a bit differently than domain user keys. They’re located at _C:\\Windows\\System32\\Microsoft\\Protect\\S-1-5-18\\User\_ and are encrypted with the DPAPI\_SYSTEM LSA secret (specifically, the user key) and has no domain backup key component. There are three ways we know of to get the decrypted key material for these:

- Use offline copies of the SYSTEM (for the bootkey) and SECURITY (for the LSA secrets) hives to extract the DPAPI\_SYSTEM LSA secret to then decrypt the system masterkey file (thanks [pypykatz](https://github.com/skelsec/pypykatz/blob/c7b8fc92b58851bb3df827794a1eab2bc898382c/pypykatz/dpapi/dpapi.py)!)
- Use existing LSA Secret extractors live on the host to extract the DPAPI\_SYSTEM LSA secret to then decrypt the system masterkey file
- Extract the decrypted keys from an LSASS dump

We wanted Nemesis to support all the current options.

If you are submitting offline registry hive files extracted from a system, the registry\_hive file enrichment module will extract the DPAPI\_SYSTEM key from SYSTEM/SECURITY hives and store it for system masterkey decryption. Additionally, the dpapi\_masterkey file enrichment module will attempt decryption for any new SYSTEM masterkey files that come in using available DPAPI\_SYSTEM keys.

If you’re able to extract the DPAPI\_SYSTEM LSA secret via other methods, we have the option to submit this via the Nemesis **Chrome/DPAPI** -\> **Submit Credential Material** tab with the **DPAPI\_SYSTEM Secret** credential type:

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_cb5bcd.png?w=1024)_Submitting a DPAPI\_SYSTEM Secret_

And finally, the lsass\_dump file enrichment module will scrape any system (and user) plaintext masterkeys and GUIDs and save them in the backend for later blob/file decryption.

These SYSTEM masterkeys are linked to a particular SOURCE ID (i.e., a host name) that’s used to correlate the files with others that are needed for decryption. We’ll show how these keys are used later to decrypt CNG files and Chromium Local State encryption keys.

# User DPAPI Masterkeys

User keys are located at _%APPDATA%\\Microsoft\\Protect\\<user\_sid>\\<guid>_ and are a bit more complicated for us attackers, but also grant us a number of different options for decryption. User DPAPI masterkeys have the final blob key protected twice, via two different methods.

Firstly, the key is protected with an intermediate key derived from the user’s password. This key can be derived from a user’s plaintext password or their NTLM hash, as shown in this diagram from our [Adversary Tactics: Red Team Operations](https://specterops.io/training/red-team-operations/) training:

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_c1b7cf.png?w=1024)_The DPAPI Key Derivation Process_

This ultimately results in what Microsoft refers to as a [credential key](https://github.com/EvanMcBroom/lsa-whisperer/wiki/msv1_0#credential-key) (a.k.a., pre-key) which you can _also_ retrieve from LSASS via [lsa-whisperer](https://github.com/EvanMcBroom/lsa-whisperer/wiki/msv1_0#getcredentialkey) via the msv1\_0 GetCredentialKey or msv1\_0 GetStrongCredentialKey (from a SYSTEM context on the host) and used with [SharpDPAPI](https://github.com/GhostPack/SharpDPAPI/):

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_51040e.png?w=1024)_Using lsa-whisperer to Retrieve the DPAPI Credential Key and Decrypting Masterkeys_

Secondly, the blob key is protected with the public key component of the domain DPAPI backupkey (described in more detail in the **Scenario 4: Elevated Domain Access** section of the [original DPAPI post](https://specterops.io/blog/2018/08/22/operational-guidance-for-offensive-user-dpapi-abuse/)). If you can retrieve the private key component of this keypair from a domain controller (DC), you can decrypt any domain user’s DPAPI masterkey blobs in the past or future:

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_9fcded.png?w=1024)

Twitter Embed

[Visit this post on X](https://twitter.com/gentilkiwi/status/609890409830064129?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E609890409830064129%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F)

[![](https://pbs.twimg.com/profile_images/1643733784196440064/2YlqbAR6_normal.jpg)](https://twitter.com/gentilkiwi?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E609890409830064129%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F)

[![🥝](https://abs-0.twimg.com/emoji/v2/svg/1f95d.svg)![🏳️‍🌈](https://abs-0.twimg.com/emoji/v2/svg/1f3f3-fe0f-200d-1f308.svg) Benjamin Delpy](https://twitter.com/gentilkiwi?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E609890409830064129%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F)

[@gentilkiwi](https://twitter.com/gentilkiwi?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E609890409830064129%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F)

·

[Follow](https://twitter.com/intent/follow?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E609890409830064129%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F&screen_name=gentilkiwi)

[View on X](https://twitter.com/gentilkiwi/status/609890409830064129?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E609890409830064129%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F)

Decrypt \*all\* keys of DPAPI Masterkeys files!
> [https://github.com/gentilkiwi/mimikatz/releases…](https://github.com/gentilkiwi/mimikatz/releases)
Moar keys! Including RSA domain backup decrypt

[![Image](https://pbs.twimg.com/media/CHbEGHsUsAAWpKj?format=png&name=small)](https://x.com/gentilkiwi/status/609890409830064129/photo/1)

[![Image](https://pbs.twimg.com/media/CHbEGHJUMAAwY14?format=png&name=360x360)](https://x.com/gentilkiwi/status/609890409830064129/photo/1)

[1:09 AM · Jun 14, 2015](https://twitter.com/gentilkiwi/status/609890409830064129?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E609890409830064129%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F)

[X Ads info and privacy](https://help.twitter.com/en/twitter-for-websites-ads-info-and-privacy)

[62](https://twitter.com/intent/like?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E609890409830064129%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F&tweet_id=609890409830064129) [Reply](https://twitter.com/intent/tweet?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E609890409830064129%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F&in_reply_to=609890409830064129)

Copy link

[Read more on X](https://twitter.com/explore?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E609890409830064129%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F)

**Side note:** We noticed during our dev that, on the most recent versions of Windows, the structure of the decrypted master key changed. [We accounted for this](https://github.com/SpecterOps/Nemesis/blob/fc307d1df16d11f81c1c8bf40bd8fcb9cd0644e7/libs/nemesis_dpapi/nemesis_dpapi/core.py#L740-L748), but existing DPAPI libraries we tested (dpapick3 and Impacket) were broken as of the drafting of this post (late 2025). We have test data in the repo for anyone interested!

You can also use the [BackupKey Remote Protocol](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-bkrp/90b08be4-5175-4177-b4ce-d920d797e3a8) (\[MS-BKRP\]), famously implemented in Mimikatz, from a list system (from the target user’s context) to retrieve a user DPAPI masterkey:

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_39fbc0.png?w=1024)

Twitter Embed

[Visit this post on X](https://twitter.com/gentilkiwi/status/604408115090591744?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E604408115090591744%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F)

[![](https://pbs.twimg.com/profile_images/1643733784196440064/2YlqbAR6_normal.jpg)](https://twitter.com/gentilkiwi?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E604408115090591744%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F)

[![🥝](https://abs-0.twimg.com/emoji/v2/svg/1f95d.svg)![🏳️‍🌈](https://abs-0.twimg.com/emoji/v2/svg/1f3f3-fe0f-200d-1f308.svg) Benjamin Delpy](https://twitter.com/gentilkiwi?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E604408115090591744%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F)

[@gentilkiwi](https://twitter.com/gentilkiwi?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E604408115090591744%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F)

·

[Follow](https://twitter.com/intent/follow?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E604408115090591744%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F&screen_name=gentilkiwi)

[View on X](https://twitter.com/gentilkiwi/status/604408115090591744?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E604408115090591744%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F)

Get Domain DPAPI backup keys \*remotely\* with a Golden Ticket !
[#mimikatz](https://twitter.com/hashtag/mimikatz?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E604408115090591744%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F&src=hashtag_click) loves RPC <3
\> [https://github.com/gentilkiwi/mimikatz/releases…](https://github.com/gentilkiwi/mimikatz/releases)

[![Image](https://pbs.twimg.com/media/CGNJ-kUU4AEU65h?format=png&name=small)](https://x.com/gentilkiwi/status/604408115090591744/photo/1)

[10:04 PM · May 29, 2015](https://twitter.com/gentilkiwi/status/604408115090591744?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E604408115090591744%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F)

[X Ads info and privacy](https://help.twitter.com/en/twitter-for-websites-ads-info-and-privacy)

[26](https://twitter.com/intent/like?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E604408115090591744%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F&tweet_id=604408115090591744) [Reply](https://twitter.com/intent/tweet?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E604408115090591744%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F&in_reply_to=604408115090591744)

Copy link

[Read more on X](https://twitter.com/explore?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E604408115090591744%7Ctwgr%5E461a44ce4c8a38245d89aa27715d5af9319466c2%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fspecterops.io%2Fblog%2F2026%2F03%2F04%2Foffensive-dpapi-with-nemesis%2F)

Sidenote for those who weren’t aware, you can also do this with [SharpDPAPI](https://github.com/GhostPack/SharpDPAPI)!

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_5e3f43.png?w=1024)_Retrieving User Masterkeys With \[MS-BKRP\] via SharpDPAPI_

However, with Nemesis, as it’s a file-enrichment platform without direct implant interaction, we’re confined to file based methods for retrieval. To execute this, Nemesis will try to parse any GUID-named file as a DPAPI masterkey file, storing the encrypted sections into the storage backend. Any parsed user/system masterkey files are then displayed in the **DPAPI** page (on the left navigator) under **Master Keys**:

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_d67c89.png?w=1024)_Nemesis DPAPI Masterkey Display_

If you have a user password, NTLM hash, or lsa-whisperer credential key, you can submit these through the **Chrome/DPAPI -> Submit Credential Material** tab. This will retroactively decrypt any existing encrypted masterkeys, but not any in the future (more on this at the end of this section). However, if you submit a domain DPAPI backupkey, these not only decrypt existing domain user masterkeys, but backup keys are stored in the Nemesis backend and will decrypt any newly linked user masterkeys that come in.

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_9fbdb0.png?w=1024)_Submitting DPAPI Credential Material_

And as mentioned, similarly to SYSTEM DPAPI masterkeys, we automatically scrape user DPAPI masterkeys from any LSASS dumps submitted as well.

_However_, to note: while we store DPAPI domain backup keys, masterkeys, and chromium cookie/login data (more on this in the next section) in the schema, we do not currently store user passwords, NTLM hashes, or secure credential keys persistently. We decided on this approach as we wanted to greatly simplify the old data model. We may add back in individual DPAPI blob tracking at some point but for now we opted for simplicity. This means that if you do _not_ have a domain DPAPI backup key, in order to decrypt any NEW masterkeys submitted, you need to resubmit a user password/NTLM hash/secure credential key as each submission will only attempt to decrypt masterkeys currently present in the database.

# DPAPI Blobs

Nemesis 2.0, unlike Nemesis 1.0.0, does not extract and store every single DPAPI carved DPAPI blob in the backend database as first-class citizens. This was part of our schema simplification and general performance optimization with the Nemesis 2.0 rewrite. _However_, every file is still scanned for DPAPI and up to 100 DPAPI blobs are carved and directly stored with a file’s enrichments. This data is exposed in a few tabs for files with discovered DPAPI blobs.

First, a finding is created if DPAPI data is found in a file, along with the unique set of masterkey GUIDs for the discovered blob:

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_3d1757.png?w=1024)

Second, a _.csv_ transform is created for **_all_** carved DPAPI blobs, which contains the masterkey guid, the blob offset and length, whether the blob is decrypted, and if the blob is less than 1000 bytes and was decrypted a base64 encoded string of the decrypted bytes is included:

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_450ed2.png?w=1024)_Downloading the DPAPI Carved Blob .csv_

Finally, Nemesis creates a separate Markdown transform for all **_decrypted_** DPAPI blobs, which again displays the masterkey guid/blob offset/blob length but will display any <=1000 byte decrypted blobs as a hex dump for easier triage:

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_2d5594.png?w=1024)_DPAPI Blob Carving and Hexdump Display_

# Chromium Cookies and Login Data

On to the main event, one of the main targets people have when trying to abuse DPAPI: Chromium browser cookies and saved logins. Here’s where things get a bit more complicated.

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_56703b.png?w=1024)_You, likely after this section_

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_7100d4.jpeg)_Me, during this section_

Back in the ancient days, the Chromium code base protected its cookie and saved login values the old fashioned way: by calling the CryptProtectData/CryptUnprotectData DPAPI functions on the secret values directly for storage and retrieval. And things were… good for us attackers at least 🙂 All it took was code execution within a user’s context to decrypt sensitive values.

With Chrome 80’s release on February 4, 2020, Chrome changed their protection approach to mirror the one used on macOS. The **Local State** file for a user’s Chrome/Chromium instance contained a key at encrypted\_key that was also DPAPI encrypted. This key was then used to protect cookie values and login entries. Offensively for us, this made little difference, as code execution in a user’s context gave us the single decryption key needed for all sensitive entries. And (attacker) life was good.

But alas, the development team at Chrome is crafty and infostealer malware authors are not nice people. On July 30, 2024, the Chrome team released the awesome (for defenders, not us attackers) “ [Improving the security of Chrome cookies on Windows](https://security.googleblog.com/2024/07/improving-security-of-chrome-cookies-on.html)” blog. In this post, they detail their new **Application-Bound (App-Bound) Encryption** primitives to store sensitive Chromium data such as cookie values and login passwords. My colleague Andrew Gomez goes into this in more detail in “ [Dough No! Revisiting Cookie Theft](https://specterops.io/blog/2025/08/27/dough-no-revisiting-cookie-theft/)”, but to summarize: the app\_bound\_encrypted\_key entry in the **Local State** file was now protected first with a SYSTEM DPAPI masterkey, and the decrypted bundle was then decrypted with the user’s DPAPI masterkey. As Andrew describes, “ _In order to use the user’s and SYSTEM’s master key for protecting the App-Bound key, Chromium browsers utilize an elevation service to perform privileged operations such as EncryptData and DecryptData via the iElevator COM interface._”

This absolutely raised the bar for attackers, but hasn’t stopped them completely. Given SYSTEM execution, [cookie-monster](https://github.com/KingOfTheNOPs/cookie-monster/) will allow you to decrypt the **encrypted\_aes\_key** in a Chromium’s **Local State** file. [Andrew’s post](https://specterops.io/blog/2025/08/27/dough-no-revisiting-cookie-theft/) goes into details on how this is possible, and this screenshot from his post shows the Beacon object file (BOF) in action:

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_1c636c.png?w=1024)_Obtain Chrome App-Bound Key as SYSTEM on Domain-Joined Host_

You can actually submit this decrypted app-bound-encryption key directly to Nemesis via the Nemesis **Chrome/DPAPI** -\> **Submit Credential Material** tab with the **Chromium App-Bound-Encryption Key** credential type. The **Source** field is required, so we can link this key to the appropriate host:

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_9cd605.png?w=1024)_Submitting a Chromium App-Bound-Encryption Key_

I want to emphasize that I am NOT ragging on the developers of this system in any way whatsoever; it’s an extremely clever solution to the constraints Chrome operates under on Windows systems. Preventing user secret retrieval when an attacker has code execution in a user’s context is a nearly impossible task. As the Chrome team states in the original “ [Chrome app-bound encryption Service](https://drive.google.com/file/d/1xMXmA0UJifXoTHjHWtVir2rb94OsxXAI/view)” design document:

_IMPORTANT: The aim is not to prevent an attacker who is running at a higher privilege than Chrome from performing these operations – e.g. Administrator, SYSTEM, an enterprise admin, a rootkit, or a kernel driver. This is just to prevent an attacker with the same privilege as Chrome from trivially calling the APIs._

ABE obviously complicated our lives as attackers and I tip my hat to the Chrome development team. 👏

This ABE function/approach changed several times (specifically with some of the encryption algorithm specifics) up to the drafting of this post, with the most recent version being released in Chrome 137+. Specifically now, after decrypting with the SYSTEM and user DPAPI keys/functions, the final app-bound key is THEN decrypted with the **Google Chromekey1** key from the Cryptography API: Next Generation Key Storage Provider (KSP). My best guess as to why they did this is that CNG keys can be stored on TPMs, which would prevent their retrieval (if configured correctly).

So, are we out of luck? Well, if the target is using software-based storage for the KSP, these files are stored in _C:\\ProgramData\\Microsoft\\Crypto\\SystemKeys\\<hash>\_<machineGuid>_ where the <hash> is calculated [with this function](https://gist.github.com/leechristensen/40acb67ff5b788d6b78d81443b66b444) and results in the value 7096db7aeb75c0d3497ecd56d355a695. In this case, the private keys from these files are protected with a SYSTEM DPAPI masterkey as well: a class of files we’re already handling. Given the proper keys, we can decrypt this CNG file, extract the “chromekey” needed, and decrypt the final app-bound encryption key needed to decrypt our cookies and logins. And Nemesis can handle just this!

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_017a00.png?w=1024)_Decrypted Chromium Local State Key_

# Retroactive Decryption

So now, with all of these files linked together, you’re probably feeling like a meme I totally don’t overuse in my posts:

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_e1e4b1.png)_Pepe…. DPAPIvia? I’ll see myself out._

If our ultimate goal is, say, Chromium Login Data decryption for a modern browser based purely off of file decryption (i.e., no code execution directly on host), the files we’ll need to review are:

- The Chromium **Login Data** file itself
- The Chromium **Local State** file from the same Chromium install (Chrome, Edge, etc.)
- The user masterkey key blob from:
  - The specific user masterkey file + Domain DPAPI backup key, user password, NTLM hash, etc.
  - Raw carved user masterkey from an LSASS dump
- The SYSTEM masterkey key blob from:
  - SECURITY + SYSTEM hive carving of the DPAPI\_SYSTEM secret, along with the specific SYSTEM masterkey file to decrypt
  - Raw carved SYSTEM masterkey blob from an LSASS dump
- The **Google Chromekey1** CNG file from _C:\\ProgramData\\Microsoft\\Crypto\\SystemKeys\\<hash>\_<machineGuid>_

Here’s the previous graphic showing these files interacting:

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_296afc.png?w=1024)_Chromium DPAPI Decryption_

This is a lot of files, and there is an element of state-dependency here as well. For example, the **Local State** file needs the linked user and system decrypted masterkeys, as well as the decrypted chromekey, before it can be decrypted and _then_ used to decrypt **Login Data** entries.

We didn’t want users to have to use some kind of state diagram to determine an exact order all of these files need to be submitted in, so we built in robust retroactive decryption for this process. TL;DR no matter what order you submit all of these files in, decryption of specific parts will be used to decrypt future and retroactive linked files (with the only exception being the submission of user password/NTLM/credkey entries to decrypt user masterkeys). This is because we don’t currently store and track individual credentials in the Nemesis backend, though this may be something we add in the future. Decrypted masterkeys, Chromekeys, Chromium local state keys, and domain backup keys are all tracked and linked (where possible) in the backend.

For example, if you submit Chromium **Login Data** and **Local State** files, and the **Google Chromekey1** CNG file, and _then_ submit an LSASS dump containing plaintext DPAPI user/system keys, everything will retroactively decrypt down to the **Login Data** entries. This will work even if the files have non-standard names and download locations, _as long as the SOURCE (host) field is the same for each file!_

![](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_11ef7b.jpeg?w=1024)_Nemesis Chromium DPAPI Decryption Process_

# Wrapup

Nemesis has come a long way since its 1.0.0 release, and has progressed even more since its 2.0 release this year. DPAPI functionality is something we care deeply about and have been working on for nearly 10 years, and we’re excited that Nemesis can function as part of the next generation of DPAPI analysis tools.

All of these changes are live in the main branch of [Nemesis](https://github.com/SpecterOps/Nemesis/)! Join us in the [#nemesis-chat](https://bloodhoundhq.slack.com/archives/C05KN15CCGP) channel in the [BloodHound Slack](https://ghst.ly/BHSlack) for any questions or feedback, and _please_ [report any issues on GitHub](https://github.com/SpecterOps/Nemesis/issues).

Post Views:4,470

[Will Schroeder](https://specterops.io/blog/author/will-schroeder/)

Principal Security Researcher

Will Schroeder (@harmj0y) is a Principal Security Researcher at SpecterOps specializing in machine learning and offensive development. He has co-authored numerous projects ranging from BloodHound to the “Certified Pre-Owned” white paper.

[Lee Chagolla-Christensen](https://specterops.io/blog/author/lchristensenspecterops-io/)

Principal Security Researcher

Lee Chagolla-Christensen is a Principal Security Researcher at SpecterOps, developing new offensive tradecraft and techniques across security and artificial intelligence.

Ready to get started?

[Book a Demo](https://specterops.io/get-a-demo/)

You might also be interested in

[![The Nemesis 2.X Development Guide](https://specterops.io/wp-content/uploads/sites/3/2026/03/nemesis_codex.png?w=300)\\
\\
Research & Tradecraft\\
\\
The Nemesis 2.X Development Guide\\
\\
TL;DR: Nemesis 2.X makes it easy to extend the platform – this guide walks through creating new file enrichment modules… \\
\\
By: \\
Will Schroeder, Lee Chagolla-Christensen \\
\\
16 mins](https://specterops.io/blog/2026/03/10/the-nemesis-2-x-development-guide/)

[![Nemesis 2.2](https://specterops.io/wp-content/uploads/sites/3/2026/02/image_242e30.png?w=300)\\
\\
Research & Tradecraft\\
\\
Nemesis 2.2\\
\\
TL;DR: Nemesis 2.2 introduces a number of powerful new features focusing on large container processing, data processing agents, enhanced DPAPI… \\
\\
By: \\
Will Schroeder, Lee Chagolla-Christensen \\
\\
22 mins](https://specterops.io/blog/2026/02/25/nemesis-2-2/)

[![Mapping Deception Solutions With BloodHound OpenGraph  – Configuration Manager](https://specterops.io/wp-content/uploads/sites/3/2026/02/Screenshot-2026-02-09-at-11.46.45-AM-2.png?w=300)\\
\\
Research & Tradecraft\\
\\
Mapping Deception Solutions With BloodHound OpenGraph  – Configuration Manager\\
\\
TL;DR: At SpecterOps, we look at Attack Path Management from multiple perspectives, including those of identifying areas to implement quality… \\
\\
By: \\
Joshua Prager \\
\\
20 mins](https://specterops.io/blog/2026/02/19/mapping-deception-solutions-with-bloodhound-opengraph-configuration-manager/)

![](<Base64-Image-Removed>)

[Previous image](https://specterops.io/blog/2026/03/04/offensive-dpapi-with-nemesis/)[Next image](https://specterops.io/blog/2026/03/04/offensive-dpapi-with-nemesis/)

Twitter Widget Iframe