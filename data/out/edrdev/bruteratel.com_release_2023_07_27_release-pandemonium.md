# https://bruteratel.com/release/2023/07/27/Release-Pandemonium/

## Release v1.7 - Pandemonium

![](https://bruteratel.com/images/post_img/2023-07-27-Release-Pandemonium/badger.jpg)

Brute Ratel v1.7 \[codename Pandemonium\] is now available for download. This release is an entire overhaul of the Badger, Ratel Server and Commander to provide support for Yara evasions and Apple Silicon. Customers using v1.6 release should note that the Badger, Ratel server and Commander of **v1.6 will not support v1.7**. Do not upgrade to this release if you are in an active engagement. Operators should read this blog or the release notes section to understand the changes before upgrading. A quick summary of changes can be found in the [release notes](https://bruteratel.com/release_notes/releases.txt).

## Feature Additions:Ratel Server/Badger

### Fallback C2 Strategy

During a red team engagement, an operator is usually limited to a few rotational hosts and one malleable profile. This allows the operator to switch back and forth between various hosts such as Azure, Fastly, Cloudfront or other fronted domains and redirectors. However, using the same profile to connect to multiple different domains can be suspicious over time. This release introduces ‘Fallback Strategy’ feature using which an operator can use multiple fallback malleable profiles for badger. Each fallback profile can contain another subset of fallback profiles enabling autonomous switching of profiles if one or more of your profiles/domains get blocked. Make note that each profile can still contain multiple rotational host for even more evasion. This can be mapped as follows:

![](https://bruteratel.com/images/post_img/2023-07-27-Release-Pandemonium/fallback_profile.png)

Each profile can contain an encrypted fallback profile metadata and the fallback profile can contain another profile and so on. The fallback profile is just another HTTP or DOH profile. This option can be configured either from Commander or via a C2 profile such as:

```
{
    "listeners": {
        "primary-c2": {
            // ... your primary profile data
            "fallback": "fallback-c2",
            "fallback_counter": 10
        },
        "fallback-c2": {
            // .. fallback profile 1 data
            "fallback": "fallback-c2-2",
            "fallback_counter": 5
        }
        "fallback-c2-2": {
            // .. fallback profile 2 data
        }
    }
}
```

A detailed demonstration of the fallback strategy can be found in the below video:

Brute Ratel v1.7 - C2 Fallback Strategy - YouTube

Tap to unmute

[Brute Ratel v1.7 - C2 Fallback Strategy](https://www.youtube.com/watch?v=YVhP2kFvMfY) [Chetan Nayak](https://www.youtube.com/channel/UCpDI4t3oGuQNOpaX85daOrg)

![thumbnail-image](https://yt3.ggpht.com/s78j1PZDYdQ3Zlirsv6BfnTda3TzKvFmvQYVNTuD6sdFpQgj_m3fWhzC0f9vLicYVLY9BzBcBA=s68-c-k-c0x00ffffff-no-rj)

Chetan Nayak2.13K subscribers

[Watch on](https://www.youtube.com/watch?v=YVhP2kFvMfY)

### Module Stomping for ‘memexec’ and ‘coffexec’

The v1.5 release of Brute Ratel introduced an Advanced Module Stomping technique for the badger wherein the stomped module’s PEB data is patched to make it look like a generically loaded module. This technique also restores the original buffer of the stomped DLL when the badger goes to sleep, so that tools like Pe-Sieve does not detect it as malicious by comparing the in-memory DLL buffer to disk. This release extends the module stomping technique to ‘memexec’ and BOF executions.

Before you execute a BOF (coffexec) or a PE (memexec) in memory, you can configure a separate module to stomp using the ‘set module\_stomp’ command. This module name can be fetched or cleared using ‘get module\_stomp’ or ‘clear module\_stomp’ command. Once a module has been configured, you can proceed to run your BOFs or PE, and they will be automatically mapped to the stomped module region. This region’s original DLL content is also restored once the BOF or the PE has completed execution. Make note that the module selected for stomping must have a ‘.text’ section larger than or equal to, the size of the PE or the BOF, else the stomping will fail with error ‘ERROR\_ILLEGAL\_DLL\_RELOCATION’. ‘Coffexec’ and ‘memexec’ will also check if the module stomped is required by the PE or the BOF’s IAT. If it is, then the stomping again fails and prevents the badger from crashing as stomping a module required by your PE or object file is dangerous.

Brute Ratel v1.7 - Post-Ex Evasions - YouTube

Tap to unmute

[Brute Ratel v1.7 - Post-Ex Evasions](https://www.youtube.com/watch?v=L6gHusqUQW4) [Chetan Nayak](https://www.youtube.com/channel/UCpDI4t3oGuQNOpaX85daOrg)

Chetan Nayak2.13K subscribers

[Watch on](https://www.youtube.com/watch?v=L6gHusqUQW4)

### Screen Recording

This release brings in a screen recording feature which becomes extremely important if you often perform Red Team engagements in a banking environment. Recently during one of our red team engagements for a bank, one of the objectives was to gain access to the SWIFT server and perform a few activities on the SWIFT banking software. Due to limited knowledge and little internet information on how a SWIFT server works, the best idea was to monitor the day-to-day activities of a SWIFT operator and understand the software. This is why the screen recording feature was added. The ‘record\_screen’ command can take arguments as quality (low/medium/high) and number of minutes to record the target’s screen. The recording can also be stopped before the timer completes by using the ‘stop\_task’ command.

![](https://bruteratel.com/images/post_img/2023-07-27-Release-Pandemonium/recording.png)

### Full Unicode Support

This release provides full support for Unicode characters, both on the badger as well as on the Commander’s end. Unicode characters involving russian, latin, chinese and others are all supported by the below commands:

- cd
- ls
- File Explorer (GUI)
- Ldap Sentinel (GUI)
- runas
- impersonate
- vault\_remove
- make\_token
- cp
- mv
- mkdir
- rmdir
- rm
- download
- preview
- fileinfo
- acl

Due to changes to these commands, some commands need escaped slashes unlike before. These commands are ‘cp’, ‘mv’ and ‘download’. More information can be found in the ‘help’ section within the badger’s terminal for each command.

### Memexec Profiler

This release also extends the ability to add ‘memexec’ as a built-in command via ‘register\_exe’ profile. A sample command profile for ‘register\_exe’ would look like:

```
{
    "register_exe": {
        "handles": {
            "arch" : "x64",
            "file_path": "server_confs/sample_profile_pe/handle64.exe",
            "description": "Lists all handles from all processes. Uses sysinternal's handle64.exe executable to run in memory",
            "artifact": "WINAPI",
            "mainArgs": "NA",
            "optionalArg": "NA",
            "example": "handles",
            "minimumArgCount": 1
        }
    }
}
```

The set, clear and get commands are now clubbed under a singular title for ease of access. Previously, the configuration commands were separate, for eg.: ‘set\_child’ or ‘set\_parent’ etc. This led to an increased number of commands just to configure various aspects of the badger. With this release, the set, clear and get commands are clubbed into each of their respective titles.

## Feature Additions:Commander

This release adds official support for Commander for Apple Silicon’s ARM architecture and Windows 11. Each Commander (linux/mac and windows) is built individually to support their respective operating system such as path auto completion, fonts and other user interface widgets. Linux uses the ‘Monospace’ font by default, Windows 10/11 uses ‘Courier New’ and MacOS uses ‘Monaco’ for the entire GUI. However, this release also provides the ability for the operator to change the theme and font dynamically at runtime as well as store them in a local json file, so that the configuration of the Commander can be auto-read during startup. Operators can also write stylesheets for themes and preview them dynamically by Selecting the ‘Commander’ menu and then selecting the ‘Settings’ option. This means there is no need to start and stop the commander to apply themes anymore.

![](https://bruteratel.com/images/post_img/2023-07-27-Release-Pandemonium/settings.png)

To ease the life of an operator, the option to upload profiles for Listener, Commands, Autoruns and Clickscripts are now added to Commander. Operators can select the “Load json profile” button in the respective ‘Add HTTP Listener’ or ‘Add DOH Listener’ dialog, or select the Upload option in the ‘C4 Profilers’ section.

![](https://bruteratel.com/images/post_img/2023-07-27-Release-Pandemonium/profiler.png)

Various samples for each of these profiles are provided in the profiles directory within the brute ratel package. A quick example to upload the profiles can be found in the video below:

Brute Ratel v1.7 - Dynamic Profilers - YouTube

Tap to unmute

[Brute Ratel v1.7 - Dynamic Profilers](https://www.youtube.com/watch?v=2xPtBxoXszw) [Chetan Nayak](https://www.youtube.com/channel/UCpDI4t3oGuQNOpaX85daOrg)

Chetan Nayak2.13K subscribers

[Watch on](https://www.youtube.com/watch?v=2xPtBxoXszw)

A notification smiley has been added to the top right side of Commander to display the online and offline status. Depending upon how your badger connects, this is updated frequently. If your badger is configured to sleep zero, it will show up as (o\_o), for terminated connection with Server, it shows up as (X\_X), else it will show up as idle.

![](https://bruteratel.com/images/post_img/2023-07-27-Release-Pandemonium/status_1.png)

![](https://bruteratel.com/images/post_img/2023-07-27-Release-Pandemonium/status_2.png)

![](https://bruteratel.com/images/post_img/2023-07-27-Release-Pandemonium/status_3.png)

Some other changes include:

1. The ‘clear’ command (to clear the badger’s command queue) is renamed to ‘clearq’ as ‘clear’ command is used to clear various other command configurations for the badger
2. The Pivot, Mitre and Team Graphs are now directly exported to html for reporting purposes instead of rendering them within Commander
3. The Bulk query runs as a standalone dialogue instead of being docked within Commander
4. Added option to wordwrap badger’s terminal
5. Updates to light and shady theme
6. Removed the word ‘auto-‘ from listener and auto profile generation

Various other changes were made to Brute Ratel, to make it more evasive and smoother to operate across various operating systems. Users will observe those changes as they migrate from v1.6 to v1.7 Commander. More detailed information on the changes are mentioned in the release notes. The upcoming weeks will also see a few more blogs on the roadmap of Brute Ratel and how it is going to provide users with a heavy customization option when dealing with various EDRs ;)

Apart from these updates, Dark Vortex will be conducting free Seminars every month on the usage of Brute Ratel which should help customers understand the core of the product and why it is more successful and evasive than any other C2s in the current market. The current BRc4 Seminar is scheduled for 31st July 7 AM UK (GMT +1:00). Stay tuned and Happy Hacking :)