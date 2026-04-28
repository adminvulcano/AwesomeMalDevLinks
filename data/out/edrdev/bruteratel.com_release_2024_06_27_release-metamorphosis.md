# https://bruteratel.com/release/2024/06/27/Release-Metamorphosis/

## Release v2.0 - Everything Everywhere All At Once

Brute Ratel v2.0 \[codename Metamorphosis\] is now available for download. This release introduces significant changes compared to previous versions, so it’s strongly recommended to review this blog, the private videos, and the documentation before using it. The Badger component has undergone extensive rewrites, featuring major updates in evasion tactics and new functionalities. The server has been optimized for speed and efficiency, with significant improvements to the licensing algorithm, ensuring each license is linked to a specific host to prevent misuse. However, the license can still be transfered from one host to another while deactivating the previous one. Additionally, several minor updates have been made to the Commander, which operators will notice during operation.

**NOTE: This release is not compatible with any older releases. Neither the server, badger or the commander will be compatible. It is important to note the changes in this release before deploying them in production.**

## Strategic Changes

Before we dive into the various changes in this release, let us first understand why the changes were required. It is common knowledge that with the rising popularity of Brute Ratel, several organizations, large and small are inclined to purchase the product for red teams. As much as this is beneficial to Dark Vortex, this also brings in a few licensing problems. Several measures were taken to tackle this issue.

### Strengthening Licensing Enforcement in Brute Ratel v2.0

A single Brute Ratel license permits use by only one user. According to the EULA, this license allows deployment on up to three servers: two public-facing servers and one for a local test-dev environment. This arrangement is based on my experience during red team assessments, where typically, a short haul server, a long haul server, and a test server configured to match the target infrastructure are sufficient for a single red team operation. If multiple red teams are being performed by an organization with multiple people, then multiple licenses would need to be purchased. However, it has been observed that some organizations were purchasing a single-user license and deploying it on a large scale, allowing multiple users to connect and operate on the server. To address this, the latest release of Brute Ratel strengthens the licensing algorithm to tie each license to the specific host on which it is activated. This is enforced through hardware checks on the host, ensuring that a license activated on one host cannot be copied to another. To activate Brute Ratel on a new host, the downloaded package must be transferred to the new host and activated there. This measure prevents the activation of the package on one host and its subsequent transfer to multiple other hosts. We recognize that this change poses a challenge for offline usage of the package. However, with this release, we are moving away from supporting offline activation due to potential misuse. Brute Ratel is designed for use by red teams, and not for offline penetration testing or use on HackTheBox machines, as has been observed with some customers. We remain committed to this intended use.

### Brute Ratel Usage Policy

Another strategic change in the sale of Brute Ratel is the decision to identify and sell the product only to organizations with experience in Red Team operations or a solid understanding of Windows internals. This change is due to instances where users lacked the necessary skills to effectively use Brute Ratel, expecting it to be a point-and-shoot tool, thereby compromising the integrity of the implants and ending up providing samples with zero opsec to security organisations. Brute Ratel IS NOT and WILL NEVER BE a point-and-shoot tool. Such tools are not suitable for Red Teams. While Brute Ratel includes official support for evasion and each release incorporates new evasion techniques tested with over 10 EDR software solutions, it is essential to understand that the operator is responsible for writing the loader, selecting the appropriate configurations, utilizing its malleability, configuring the stomped module, and stack configurations (described below), among other tasks. Brute Ratel offers the necessary options for configurations and builds shellcode based on these configurations, but safely executing the shellcode remains the operator’s responsibility. In light of this, we have decided to cease renewals and reject sales to organizations where operators lack knowledge or the willingness to learn about Red Teams (more emphasis on willingness to learn), and instead seek a tool that performs all tasks with a single click.

## Badger

### Core Updates

The majority of the badger has been rewritten in this release to enhance evasion capabilities and update the architecture. Here are some of the key changes without delving too deeply into the internals:

1. Introduced new sleep masking mechanisms that keep the badger’s stack-chain valid regardless of its sleep status.
2. Sleep masking mechanisms can now be configured in a separate OpSec tab while creating a listener or payload profile.
3. New options are available in the OpSec tab to configure the badger’s entry point, offset, core-thread execution method, and to build custom stack frames. If an operator does not configure any stack chain, a random legitimate looking stack is built depending on the process in which the badger is residing
4. Significant updates to the SOCKS proxy have increased its speed and stability.
5. All libraries can now be loaded with a custom stack chain defined by the operator.

A more detailed version of the updates and their usage is available in the offline documentation.

### Other Improvements:

1. \[QOL\] The ‘ls’ command now works without requiring a slash at the end of the directory.
2. \[QOL\] The ‘ls’ command on an empty directory now returns a message indicating that the directory is empty, instead of returning no data.
3. Added new commands: **get winrm\_config**, **set winrm\_config**, **clear winrm\_config** and **pivot\_winrm**, which use COM objects and WinRM for lateral movement.
4. \[QOL\] The ‘rm’ command now enforces secure delete, making ‘rm -rf’ unnecessary.
5. The default SOCKS 4a/5 timeout is now set to 3 minutes.
6. Fixed the “Invalid architecture” bug in x86 BOFs.
7. \[QOL\] Data in the listener input boxes are now trimmed for newlines and spaces.
8. \[QOL\] Fixed the ‘timeloop’ command bug.
9. \[QOL\] Improved the quality of screenshot captures.

## Ratel Server

The core changes mentioned in the strategic policies above apply to the Ratel Server. Apart from these, several user requested features have been added.

1. During a red team operation, having hundreds of badgers can slow down the Commander startup because it has to synchronize the badger tables with the server. This issue arises particularly when there are several inactive badgers that do not require interaction. Ideally, an operator can remove information about a dead badger from the Commander and Server using the context menu (right-click on the badger in the table). This action does not delete any command logs or entries; these are retained in the **logs** directory. However, problems occur if a removed badger checks in again. For example, if a badger goes offline because a phished system has gone to sleep, and the operator removes it from the Commander thinking it’s dead, it may come back when the system resumes from sleep. Since badgers use authenticated tokens, they cannot interact with the server if they have been removed, and they appear in the **deauth.log**. This release addresses this issue by enabling the import of badger profiles from the Commander in JSON format. An operator can create a badger profile or use one from the automatically generated **autosave.profile**, and import this JSON file into the server. If the server needs to be shut down during an engagement, this badger profile can also be used to import badgers along with a **badger\_counter**. Additionally, if an operator fails to save the badger’s profile before removal, they can extract the badger ID and its token from old logs, and use random information for the rest of the JSON profile. This allows the badger to authenticate, and once authenticated, the operator can update the server with the correct information.
2. Added badger\_counter to autosave.profile. The counter increases with each newly added or connected badger.
3. Updated service and DLL executable shellcodes to remove static detections.
4. The Brute Ratel server binary now requires the operator to run the server as a root user.
5. Removed redundant functions from various Go programs.
6. Major updates to DNS Over HTTPS comms making it faster and more stable for heavy downloads.

## Commander

The latest release of Commander focuses primarily on quality of life (QoL) enhancements. Below are the key updates:

1. New Listener and Payload Profile Options:
   - Added options to streamline the creation and editing of Listener and Payload profiles
2. Enhanced Badger Profile Management:
   - Introduced a button in the “Server Config” menu to import badger profiles for resurrected badgers
   - This feature is useful for re-adding ‘removed badgers’ using their metadata. For example, if an operator removes a badger and it checks back in after a few days, it typically appears in the ‘deauth.log’ file. The data from ‘deauth.log’ or the initial access log can be used to retrieve the badger’s token and reintegrate it into the server.
3. Improved Command Help Output:
   - Updated the help output for commands that require special double quotes to properly escape single double quotes
4. Text Formatting Enhancements:
   - All data fields in Commander now have automatic space and newline truncation to prevent copy-paste errors

These updates aim to enhance the overall user experience by simplifying processes and reducing potential errors.