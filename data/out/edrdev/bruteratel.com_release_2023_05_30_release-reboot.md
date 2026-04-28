# https://bruteratel.com/release/2023/05/30/Release-Reboot/

## Release v1.6 - Reboot

![](https://bruteratel.com/images/post_img/2023-05-30-Release-Reboot/badger.png)

Brute Ratel v1.6 codename Reboot is now available for download. This release brings in several updates to existing evasion techniques, support for Windows Commander, Hi-DPI scaling and various heavy user experience updates (QOL) requested by the BRc4 community. A quick summary of the changes can be found in the [release notes](https://bruteratel.com/release_notes/releases.txt).

## Feature Additions:Ratel Server/Badger

### LDAP Sentinel

This release brings in support for sleep and jitter for LDAP Sentinel with the ‘sentinel\_sleep’ command. Using this, operators can provide an interval between every single LDAP request to the Domain Controller. Unlike previous releases, this version of LDAP Sentinel supports SASL authentication with a fallback mechanism to the default kerberos authentication. The SASL authentication consists of encrypted messages inside the LDAP “bind” requests and responses. The “bind” request contains the distinguished name of the directory object that Badger wishes to authenticate as either with an impersonated token or directly. This feature was added to support forced Certificate SASL authentication within some environments. Interestingly, this also provides better evasion against network based IDS which build detections against known LDAP queries from unencrypted data or by tracking multiple LDAP queries originating from one source and then tagging it as an anomaly. Due to the encrypted nature of the SASL authentication, it becomes difficult for various detection systems which do not handle SASL. Apart from these changes, LDAP Sentinel also supports attribute filtering. An operator can now provide multiple attribute filters within LDAP filters to limit search output to requested attributes. The below example shows attribute filters (name, distinguishedName, lastlogon and objectSid) added to the LDAP query to search user objects.

![](https://bruteratel.com/images/post_img/2023-05-30-Release-Reboot/ldap_sleep.png)

This feature when coupled with [BofHound](https://github.com/fortalice/bofhound) makes it easier to build custom bloodhound compatible json files.

### ACL Enumeration

The [GetSecurityDescriptorDacl](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-getsecuritydescriptordacl) API provides a way to enumerate a Discretionary Access Control List for an object. Brute Ratel uses this API with the newly added ‘acl’ command to enumerate permissions of a file or folder similar to the ‘cacls.exe’ executable.

![](https://bruteratel.com/images/post_img/2023-05-30-Release-Reboot/acl_enum.png)

### Environment Variables

During a red team engagement, a network service process or an IIS Server process, when exploited, might not have proper environment variables. In one of the previous releases, we introduced the ‘getenv’ command to enumerate the process environment variables. This release extends this functionality to add custom environment variables for the current process using the ‘setenv’ command.

![](https://bruteratel.com/images/post_img/2023-05-30-Release-Reboot/setenv.png)

### Curl Request

A miniature ‘curl’ functionality was added to this release to perform http/https requests to a given site and url. This command can send a GET request to HTTP/S server on a given port and URI and receive html output in raw format. This can be extremely handy to search and enumerate internal web applications without the need to start Socks proxy every now and then, or to check if your backup C2 channel is reachable from within the organizational environment.

![](https://bruteratel.com/images/post_img/2023-05-30-Release-Reboot/curl_request.png)

### Secure Deletion Of Files

Another anti-forensic feature that was requested by the community was to securely delete the files so that it cannot be extracted by the blue team using EnCase and Autopsy. This is an optional feature added to the ‘rm’ command which accepts the ‘rf’ argument. When this command is executed, the requested file is overwritten with garbage and zeroes out every bit multiple times before deletion. This makes recovery of files extremely difficult. Make note that large files will take more time for secure deletion, as more bytes are written to disk.

![](https://bruteratel.com/images/post_img/2023-05-30-Release-Reboot/secure_delete.png)

### DLL Load Telemtry Capture In Userland

An interesting feature observed with an EDR was tracking of DLL loads in userland. Most EDRs monitor DLL loads in the kernel via the [PsSetLoadImageNotifyRoutineEx](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntddk/nf-ntddk-pssetloadimagenotifyroutineex) callback. However, for unknown reasons it was observed that some EDRs capture this information in the userland by hooking LoadLibrary events. One theory behind this would be that kernel callbacks provide a limited amount of information such as the [IMAGE\_INFO](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntddk/ns-ntddk-_image_info) structure. Userland Hooking can provide an EDR more leverage to quickly perform remediations without having to use Kernel CPU time. This release of BRc4 disables userland DLL notifications by default.

### Everyone ACL For SMB Badger

Another community request was to modify the way SMB payload handled authentication from remote systems. Usually it’s a good idea to allow only authenticated users to connect to the named pipe. However, this isn’t feasible when the SMB shellcode is executed via IIS server exploitation which you do not have tokens or passwords of. Thus, the only way to connect to the named pipe is by changing the DACL of the named pipe. This release disables SMB authentication on the named pipes and allows all users to connect to the Badger’s named pipe.

### Updates To The Core

Various changes were made to the Ratel Server and Badger architecture for evasion, stability and usability. The following list includes a few of the major changes:

- The staged shellcode supports malleability data for response data (request malleability already existed). Both staged and stageless payloads transfer data in encrypted context using a custom encryption algorithm. However, having encrypted data over the network increases the entropy of the network data. It was observed that Crowdstrike, Defender ATP and a few other EDRs strip the SSL encrypted data by installing root user certificates and checking the network data entropy. Various changes were made to how the data is being sent over the network, in order to lower the entropy. The previous releases of Badger had an entropy of the value of 7.4/10 which was on a higher side. This release brings down the network entropy to 4/10 for both staged and stageless payloads, which can be lowered further by adding malleable data.
- There was a major race condition when module stomping was used alongside sleep obfuscation. This is now fixed and helps to avoid detections from Elastic EDR and FortiEDR which check the RX region of selected API calls for anomalies.
- Sleep interval for file downloads now change with the sleeping schedule configured for the main thread.
- Updated entire DNS comms with a more robust backend server rewritten from scratch for enhanced logging, fast and stable communication.

## Feature Additions:Commander

One of the most requested features of Commander was support for custom themes. What better way to support this, if not via stylesheets. Operators can now write custom stylesheets and change every aspect of the Commander, adding different fonts, colors and font-size for every widget and dialog box. The default theme is Dark, however ‘light’ and ‘shady’ themed stylesheets are provided in the package. Operators can use them as a reference to write their own stylesheet. The generated stylesheet file can be passed as a command line argument to the shellscript ‘commander-runme.sh’.

### Dark Theme With Solarized Terminal (default)

![](https://bruteratel.com/images/post_img/2023-05-30-Release-Reboot/brc4_dark.png)

### Shady Theme

![](https://bruteratel.com/images/post_img/2023-05-30-Release-Reboot/brc4_shady.png)

### Light Theme

![](https://bruteratel.com/images/post_img/2023-05-30-Release-Reboot/brc4_light.png)

Starting from this release, official support is provided for Commander to be run on Windows 10. The package includes the ‘commander-runme.bat’ file which loads up all dependencies and executes the main Commander executable. Make note that Pivot and MITRE graphs are not supported in windows due to some limitations of the chromium library used to render graphs in linux. Entire backend of the Commander was rewritten for a better user experience. Some of the highlights include:

- Support for Hi-DPI Scaling on Windows and Linux
- Added ‘back’ and ‘forward’ buttons to search backward and forward in the Badger’s terminal
- Commander’s ‘disconnected’ dialog is replaced by a simplified green circle at the extreme top right location (check the above Commander figure). This area shows whether Commander is connected (green circle) or disconnected (in red).
- Added info-pane to Badger’s Terminal which shows additional info of the Badger (check the Badger’s terminal in the above figure)
  - User name
  - Current working directory
  - Last sleep time and jitter
  - Active sleep obfuscation
  - Active socks proxy
  - Active rportfwd
- Removing badgers from the Commander perma-deletes dead badgers. DO NOT REMOVE active badgers. Deleting badgers will delete their authentication information from the server making them unable to authenticate anymore if they check in later. Logs will not be deleted.
- Commander shows active Rportfwds and TCP listeners in the “Server” drop down menu
- The download tab supports perma-delete of downloaded files. Files can now be downloaded or deleted using multi-selection.

There were various other improvements made to the Ratel Server’s backend, Badger commands and Commander, some of which are listed in the release notes. Various other evasion updates have also been added which are not added to the release notes to keep it away from the hands of defenders. There are a few more post-exploitation feature releases scheduled for the upcoming month, which were supposed to be added in this release (as mentioned in the discord channel), but were not added due to their stability issues. However, they will be pushed as a part of minor release once stable. Users are requested to update to this release as it provides several QOL over the previous release. Stay tuned and Happy Hacking :)