# https://bruteratel.com/release/2022/11/17/Release-Resurgence/

## Release v1.3 (Resurgence) - No Strings Attached

Brute Ratel v1.3 codename _Resurgence_ is now available for download. This release brings in various changes to evasion techniques, improvements to Badger, user experience (QOL) and several features requested by the BRc4 community. Since this is a major release, I’ve divided the blog into various segments which can be directly accessed with the links below. A quick summary of the changes can be found in the [release notes](https://bruteratel.com/release_notes/releases.txt).

- [Features Additions](https://bruteratel.com/release/2022/11/17/Release-Resurgence/#feature-additions)

- [Improvements](https://bruteratel.com/release/2022/11/17/Release-Resurgence/#improvements)

- [Ethics And Social Responsibility](https://bruteratel.com/release/2022/11/17/Release-Resurgence/#social-responsibility)


## Feature Additions

### A Quick Note on Detections

This release brings in several changes to Brute Ratel which not only helps with the size optimization of the shellcode, but also helps to avoid further detections. The major improvement to the core starts with the removal of strings and changes to the hashing algorithm which were earlier embedded within the payload. As the release v1.2.2 was leaked by MdSec on Virustotal, it was imminent that several EDR organizations would download and extract telemetry from the payload and build detections from it. This was observed heavily with detections from Microsoft’s Defender/ATP, Crowdstrike and Elastic. Before we understand the changes in the Badger, it’s trivial to understand how the static detections take place. Static detections are built on the following artefacts:

- Initial Yara Scans on Disk
  - This detection is usually performed by searching selective opcodes within sections of the payload, or by trying to match opcodes for a hashing algorithm within a file. Some EDRs/AVs also tend to scan for strings embedded within a payload unique to the payload to attribute the payload to a given C2
- Yara Scans during Code Injection
  - Injection techniques usually use QAPC or CreateThread/CreateRemoteThread API calls. Most EDR vendors will try to hook QAPC, if they don’t have the threat intelligence from the Etw (kernel TI). They can also capture this from the Kernel Callback such as **PsSetCreateThreadNotifyRoutine**. Thus, EDRs can hook the threads, capture it’s telemetry such as the region where the thread is starting from, and also perform Yara scans on these memory regions. Thus if your payload does not have a custom encryption stub, this can be detected. Even if you encrypt your shellcode, you have to either decrypt it before you execute the thread, or you also have to write a self-decryption routine to decrypt itself on the fly, copy the code to an RX region and execute the decrypted code. What this means is that your code to decrypt as well as the code to run NtProtectVirtualMemory (even syscalls/indirect) can be signatured by Yara. Thus most EDR vendors will try to either signature strings in unencrypted payloads, decryption routine or most importantly the hashing algorithm used to find the function pointers such as NtProtectVirtualMemory from ntdll.dll. There are also other cases of PEB hooking and tracing stack telemetry which I’ve discussed in the previous [blog](https://bruteratel.com/release/2022/08/18/Release-Scandinavian-Defense/).
- Tracking Known Sideloads/LolBins
  - This is probably the most known way of detection to track known signed exectuables and track them by performing full process scans and checking anomalous behaviours in their network connections.
- Network Detections
  - Network packet detections solely rely on the fact of having either a known signature in the buffer that you send across over a network or just a bad certificate. Thus it’s important to use valid certificates so that your connections don’t get killed, and also make sure you are using malleable profile which has custom request/responses and request and response headers.
  - Other network detections usually fall onto having known bad IPs/Uncategorized domains etc..
- Behavioural Detections
  - If you are able to avoid all of the above, you still have to deal with behavioural detections such as detections on telemetry captured by the EDRs which utilize machine learning. In case of machine learning, there are a bunch of traps which are laid out and a score is provided on the captured telemetry sometimes ranging from 0 to 10 or 0 to 100. This behaviour is defined on the basis of process commandline arguments mostly used for fork and run, it’s parent-child anomalies, network connections, frequency of execution of a process, uncommon DLLs loaded in the process, the user under which the process was executed and similar other artefacts.

All the said detections here are what I’ve seen during my tenure as a detection engineer with various EDR organizations, building detections when I started my career as a threat hunter, or when I started reversing the EDRs to understand it’s behaviour. Now that we know how the detections are usually handled, lets see where BRc4 lacked till v1.2.9. Till the previous release, Brute Ratel was encrypted using RC4 and was also using the default ror13 algorithm for calculating hashes for various API calls. The loader of the stage contained the decryption routine which also contained encrypted information about the server and it’s metadata as to where it needs to connect to. Thus the strings embedded within the core were not susceptible to detections as they were encrypted, but since they were in base64, it was itself an anomaly. Similarly, when the payload is running in memory, then during sleep, it will encrypt itself and decrypt occasionally to connect to the Ratel Server and fetch commands to execute. However, a threat hunter can simply use a debugger to add breakpoints and extract the decrypted data from the payload and run Yara against it for attribution. Apart from these, Brute Ratel only had malleable profile in the post request, but not in post response from the server. It also did not support response headers. Statistics are laid out using all these telemetry and a malicious score is provided by the EDR’s algorithm which is either allowed to run or be killed depending on the score.

### Complete Malleability

In case of BRc4, the core detection built by several EDRs were on the hashing algorithm, strings when not encrypted, the encryption routine and on the response received from the server as the response was not malleable. This release brings changes to all of these.

With this release, Badger provides extended malleability with custom response types and headers. Ratel Server can be configured to respond differently when a command needs to be sent, and a different response when there is no command in queue. Thus when the Badger checks in and there is no command in queue, the server can just send the configured response without having to send anything else, If there is a command in queue, then that can have a different malleable profile as well. Custom response headers can also be added alongside request headers. The requests/responses and headers are fully compatible with information extracted from Burpsuite. The ‘X-forwarded-for’ headers for authenticated Badgers are now written in the web.log file. Since response headers were added, the original key in the profile ‘extra\_headers’ is now renamed to ‘request\_headers’. The user interface was also changed along with a built-in help option in the “Add Listener/Add DOH Listener/Add Payload Profile” dialog.

![](https://bruteratel.com/images/post_img/2022-11-16-Release-Resurgence/listener.gif)

Another malleability update was ‘DNS interval’ for DNS Over HTTPS. DOH requests allows a maximum of 64 bytes per request. This means, if you execute a command where the response is more than 64 bytes, then the response would be split into multiple chunks. When the sleep is complete and Badger decides to check in, it encrypts the chunks available, and then sends the chunks without sleeping till all the chunks are sent. Once all the chunks are sent, it will fetch command from the c2, execute them, store their response in chunks and then go to sleep while hiding itself and also the responses in heap. DNS interval, in this case would be the time interval between various chunks it needs to send for a single request. During this interval Badger does not hide itself. It will just wait for a few seconds before sending the next chunk of data. Once all the chunks are sent, a single request is complete and then it will mask itself and sleep. Badger’s sleep and DNS interval are two different things. Badger can’t hide itself when performing any type of operation because the thread needs to actively read the RX region or read the RW code. However if the badger has zero threads active, then the Badger will encrypt itself, stack, heap and everything related to it. Thus DNS Interval allows to change the frequency at which packets of DNS for a single request is sent to the server.

### New Shellcode and Core

Badger has always been fully multi-threaded since it’s first release. This meant every new command was run in a seperate thread. This is changed now to avoid multiple thread creations. Badger is still multi-threaded, but it won’t run every command in a thread. Only a few selected commands which might block the main if run as function, is now run as a seperate thread. Everything else is run inline as a function. Several changes were also made to how a local thread was created following some detections from Elastic EDR, as unlike any other EDR, Elastic also monitors local threads. There’s also a major update to the Badger’s shellcode and it was rewritten to avoid detections from the previous releases. Earlier, the shellcode stored the server’s configuration in encrypted base64 which is now fully binary. Since the shellcode was further optimized, it was found that there is no use of the ‘ret’ based shellcodes, so that has been removed. Only RtlExitUserThread and WaitForSingleObject exists now. Default Rc4 key ‘bYXJm/3#M?:XyMBF’ was removed from the shellcode earlier, but it still stayed within the core to decrypt DLL names when DLL loading was required. This is also now removed. All ror13 hashes along with it’s hashing algorithm was removed from stage/stageless and the core payloads including all strings from the Badger’s memory. All command output received from the Badger is now tracked, parsed and formatted directly by the Ratel server. This helped lower down the size from the earlier 240kb to 210kb now, even after adding all the new features.

### Reverse Port Forwarding

Another major feature request by several users was reverse port forwarding. Reverse port forwarding can be extremely useful when you want to bring in your own custom C2 or tooling, or for moving laterally. The Badger now comes equipped with the ‘rportfwd’ command which can be used to forward a port on Badger’s host directly to the Ratel server, and the Ratel server will handle the task of forwarding it wherever requested. The below video shows a quick demonstration of reverse port forwarding for metasploit’s meterpreter.

Reverse Port Forwarding With Brute Ratel C4 - YouTube

Tap to unmute

[Reverse Port Forwarding With Brute Ratel C4](https://www.youtube.com/watch?v=7GS_HBHIvWo) [Chetan Nayak](https://www.youtube.com/channel/UCpDI4t3oGuQNOpaX85daOrg)

Chetan Nayak2.13K subscribers

## Improvements

### Ratel Server and Badger

Several other improvements were added to the existing commands as requested by the users. The below list should highlight most if not all.

1. Added dns resolver for ‘icmp\_ping’ and ‘portscan’ command. Both these commands accept a hostname instead of just IP address like it used to earlier
2. Full server profile is now autosaved to disk. The supplied profile is not overwritten anymore. This means you can kill the server anytime in between engagements, update the server/make changes as required and restore the server again without losing anything with the “-r” command line option
3. Socks is now faster than ever before. Socks encrypted data uses less rounds of encryption and a seperate thread to work asynchronously with the main thread
4. After impersonating a user, the ‘userinfo’ command shows information about the impersonated token instead of the process token
5. New encryption algorithm for badger and licensing server

### Commander

Several minor improvements were added to the user interface for QOL as requested by the users. The below list should highlight most if not all.

01. Added local path tab completion support
02. Added edit option in the ‘Listener Actions’ context menu to edit DOH and HTTPS listeners
03. File Explorer Updates:
    - Adde search option in file explorer to quick search file or folders and upload/download/delete them, or create new folders in them
    - Added folder icons
    - Added option to select multiple files and either download or delete them
    - Copy file/folder name option with the right click
04. Downloads tab is now a part of the main UI next to the creds tab and autoupdates itself on every downloaded chunk unlike earlier where the user had to refresh this manually. Commander shows active download status while files are being downloaded from the server
05. Multiple files can be directly downloaded from the downloads tab irrespective of their size unlike earlier where the size was limited to 50mb from server to commander. The active download status and progress bar is also shown in the UI.
06. Updated Addlistener, AddDOHListener and AddPayloadProfiler UI to show seperate tabs for malleability and help options
07. The Commander and Ratel server versions are now synced. If different versions are used, an error pops up displaying the warning.
08. Internal IP address of the Badger’s host is also added to the in the Badger’s table in Commander
09. Updated watchlist to show full server logs with colored output
10. Core server logs are now stored in logs/watchlist.log unlike earlier where it was stored under date basis. Added detailed tracking for logs
11. Added last check-in timer in Badger’s table for Commander. Removed Badger checkin in the status bar at the bottom of commander
12. Updated formatting for all command output in Commander’s terminal for better visbility
13. All active TCP listeners are shown in ‘Commander->Server->View Badger TCP Listener’ context menu
14. The ‘socks\_profile’ command validates a profile before sending the profile information to the Badger. It auto adds ‘auto-‘ if not supplied by the user
15. Logs exported by Operator activity also adds the target hostname and username to the csv

Several other bugs were fixed along with improvements which can be found in the [release notes](https://bruteratel.com/release_notes/releases.txt).

## Ethics And Social Responsibility

When you sell a product which falls under ‘Dual Use’, you will eventually reach a scenario of ethics and how the product needs to be used. I’ve been asked this question several times both in person and on social media on how do I verify the party purchasing the product. Brute Ratel is a product of Dark Vortex, the headquarters of which is located in Mumbai, India. India, like most of the countries have to follow the “Wassenaar Arrangement” which imposes export controls over any product which is to be sold internationally and falls under the category of “Dual Use”. In novice words, since Brute Ratel serves as a command and control, which can be used for assessing the strength of an organization, and also for military use, it comes under “Dual Use”. Thus every party, to whom the product is to be sold will have to be vetted thoroughly, else there is a heavy risk of the criminal implications. Dark Vortex assesses a purchaser in two different ways. The first and foremost is the background verification (BGV). BGV as in, when the company was formed, in which country the company is located in, who is the director of the company, whether the company faced any type of criminal charges and so on and so forth. We also force the party to interact with us only with the official business email ID and also verify the domain from where the email originated from. We do not entertain generic emails such as gmail/outlook/yahoo etc or newly purchased websites. We also check the registration of the company/incorporation and under what type, was the company registered as, whether it’s an infosec/IT company/Banking or anything else to validate we are not selling the product to a newly started company which might also be very suspicious. The BGV is fairly easy when vetting a financial organization or an infosec/IT company as most of the time these companies have usually existed for a good number of years and have a decent reputation. We take heavy precaution when a restaurant or fast food organizations try to buy the product (yes, ironically that happens). The BGV is conducted via a third party company from US and also by me (OSINT much?) to make sure that we are only dealing with legitimate and registered companies. Once this first verification process is complete, then we proceed with the second step of verification which is to make sure the payment is over a wire transfer and the transfer comes from the same company which we verified earlier. The licenses are shared only post the verification of payment and thankfully SWIFT transactions provide a detailed tracking information as to where the payment originated from. At the time of writing this blog, Dark Vortex has around 500+ customers spread mainly across US and Europe. We do not sell the product to sanctioned countries or especially to countries where there is civil unrest.

However, inspite of all the precautions, there are still chances of the product being leaked by an employee of the organization, re-sold or cracked in this instance. There’s nothing more I hate, than the use of Brute Ratel for malicious activities. BRc4 contains heavy trackers and can be traced down if anyone tries to use if for malicious purpose. The tracker is encrypted with a master key which is not shared with anyone. Also the trackers can’t be removed as these trackers are not only a part of the payload/package, but this tracker is also used for encrypting some other parts of the payload. This means if the tracker is removed or modified, the payload will stop working. Lately, I was informed about the leak of Brute Ratel v1.2.2 and v1.2.5 by an anonymous individual along with a video showcasing that Dom Chell from MdSec, and Austin Hudson from Guide Point Security were sharing the samples to selected parties. Upon further investigating the brute ratel’s licensing server logs, it was found that various brute force attempts to crack the licensing algorithm were made. All of this happened before the v1.2.2 was leaked on Virus Total. The time of brute force in the server logs matched the date when the sharing happened in the Austin Hudson’s (@Mumbai in discord) video. The video shows Dom Chell and Austin Hudson responding to having the latest release and at the same day several attempts were made to upgrade an older version of v1.2.2 to v1.2.4 as they mentioned they had the softwares. On the same day, I released a version v1.2.5 which I asked the individual to check if mdsec/austin had the new release. Surprisingly only the anonymous individual, Dom and Austin knew about this release and I saw attempts to upgrade to v1.2.5 sent via burpsuite.

discord1 from Paranoid Ninja on Vimeo

![video thumbnail](https://i.vimeocdn.com/video/1548386191-adde43cfe8c50922aa53d264f8369ad40f69aec702c590e5e41cebbb426cc8bc-d?mw=80&q=85)

Playing in picture-in-picture

Like

Add to Watch Later

Share

Play

00:00

00:04

Settings

QualityAuto

SpeedNormal

Picture-in-PictureFullscreen

[Watch on Vimeo](https://vimeo.com/771485613?fl=pl&fe=vl)

discord2 from Paranoid Ninja on Vimeo

![video thumbnail](https://i.vimeocdn.com/video/1548387551-c4916bf34be075995301edd5be99aeaf0265746fbb15ba39c621f177d27f758d-d?mw=80&q=85)

Playing in picture-in-picture

Like

Add to Watch Later

Share

Play

00:00

00:02

Settings

QualityAuto

SpeedNormal

Picture-in-PictureFullscreen

[Watch on Vimeo](https://vimeo.com/771485659?fl=pl&fe=vl)

During this time, I decided to change the licensing algo to make it more difficult to crack, following which I noticed that since Dom/Austin could not crack the software, they decided to upload the package to Virustotal, so that someone else might crack it. Unfortunately it did not take long for the infosec community to share this uploaded version among various telegram channels and discord. This was later cracked by a russian group known as ‘The Molecules Crew’ by reversing the algorithm, patching it and sharing it in various underground channels. I was informed that the cracked versions are being utilized by some of the threat actors and I have already provided help to several organizations in need. Thus, I am actively sharing the yara rules to detect stager and the stageless payloads of Brute Ratel. Make note that these won’t affect the v1.3 release as the payload is entirely changed in this release.

Now, there is no sufficient proof apart from the video, server logs and chats from various discord channels that the mentioned individuals shared the product on VT without license keys. However, Dark Vortex has already shared the evidence with various agencies to help them track down the malicious abuse of the product by threat actors. Any agency/company who need help to track down threat actors using BRc4 can contact us at [support@bruteratel.com](mailto:support@bruteratel.com) and we will be more than happy to help track down the Brute Ratel servers, reverse the payload and find more attribution information from the attack. Since I’ve already discussed the core parts of detections above, I’ve added the Yara rules to [github here](https://github.com/paranoidninja/Brute-Ratel-C4-Community-Kit/blob/main/deprecated/brc4.yara) for further detecting malicious usage of the product including various other open source detections for BRc4 all at one place.

## End Note

All in all, this release is going to be the last release for this year, ofcourse if there are any bug-fixes, that will be attended. But the next major release will be in January which will introduce a new type of payload, new lateral movement and staging techniques. Also, the API documentation for v1.3 will be available for use by this weekend. Stay tuned for more interesting releases.