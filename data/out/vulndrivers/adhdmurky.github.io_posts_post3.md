# https://adhdmurky.github.io/posts/post3/

Once I found out about this new driver exploit, I was eager to reverse engineer it and attempt to abuse it using my current (noob) skill set.

A write-up for this driver is publicly available, but I chose not to read it, as that would have taken away from the learning experience.

The original research can be found [PhantomKiller](https://git.redteamfortress.com/j3h4ck/PhantomKiller). But mine is like I said…. for dummies :D

So I decided to approach this my own way and explain it as simply as possible, they say that’s the best way to learn.

I located the driver and downloaded it to my virtual machine for analysis and used IDA to manually reverse engineer it.

![0b1f9678011749a904c0d68e58c1613f.png](https://adhdmurky.github.io/PostImages/0b1f9678011749a904c0d68e58c1613f.png)

Best way to determine whether a driver is vulnerable is by examining its function imports from ntoskrnl. We can see that we have `ZwTerminateProcess` function. Let’s check it out.

![49ffac89fee2ac9436111f55e997667e.png](https://adhdmurky.github.io/PostImages/49ffac89fee2ac9436111f55e997667e.png)

Lets use that function to see all the locations in the code that reference it.

![7ba9096f36469fb21959007d486fca35.png](https://adhdmurky.github.io/PostImages/7ba9096f36469fb21959007d486fca35.png)

We can see that `sub_14000198C` has a cross-reference at offset `0x5B`

![772306d37dfcdbf2c7660d82ba926173.png](https://adhdmurky.github.io/PostImages/772306d37dfcdbf2c7660d82ba926173.png)

If we double-click and compile the code we should see our implementation of terminate process function.

![05be071712ccd62c8d95fde40bd287c8.png](https://adhdmurky.github.io/PostImages/05be071712ccd62c8d95fde40bd287c8.png)

But…. before we jump right into it, we need to cover some basics of driver exploitation.

To write a console app for driver exploitation, one must find a few things in advance before calling the DeviceIoControl function:

- The driver’s symbolic link that user-mode can use to gain a handle to the device (SymbolicLinks are created based on DeviceName stored in Kernel Object Namespace e.g., \\\Devices\\MyDriver).
- The IOCTL code that is used in the “`IRP_MJ_DEVICE_CONTROL`” aka. “`MajorFunction[14]`” Major Function that leads to our ZwTerminateProcess function (By default, drivers have Unload, Create, and Close functions that are invoked automatically by the system: Unload when the driver is unloaded from memory, Create when user-mode calls CreateFile() to open the device, and Close when user-mode calls CloseHandle(), and none of these require IOCTL codes to invoke them.).
- The size and contents of the input/output buffer we send in the IRP packet to the driver associated with the device object.

Now that we got that covered lets go back to reversing.

In the first function we found via cross-reference (sub\_14000198C), we can see two other interesting functions besides ZwTerminateProcess: PsLookupProcessByProcessId and ObOpenObjectByPointer. PsLookupProcessByProcessId takes two arguments, and the first one is interesting because it’s the same argument passed into our “sub” function.

![0a9dbbafc92f434989c053dd2ce3fb6e.png](https://adhdmurky.github.io/PostImages/0a9dbbafc92f434989c053dd2ce3fb6e.png)

According to Microsoft documentation, PsLookupProcessByProcessId has two arguments: the first is ProcessId, and it returns a referenced pointer to the EPROCESS structure of the process we provided the ID for.

![7dc1f8096c1842e5462115f352730fae.png](https://adhdmurky.github.io/PostImages/7dc1f8096c1842e5462115f352730fae.png)

Once our Process variable is updated by PsLookupProcessByProcessId, the ObOpenObjectByPointer function will take that pointer and return a handle to that process object.

![a4e57faf80eddfd749640133b537bf3f.png](https://adhdmurky.github.io/PostImages/a4e57faf80eddfd749640133b537bf3f.png)

ZwTerminateProcess is now able to terminate a process using the handle its provided with.

So basically, this very interesting “sub” function does everything we need to terminate a process, we just need to figure out where that function is and how to pass the PID parameter to it. Again best way to do it is to find its cross-references:

![936a62e6e1bfdf37999c6373f5ee9e8c.png](https://adhdmurky.github.io/PostImages/936a62e6e1bfdf37999c6373f5ee9e8c.png)

We can see that there is a reference at offset of `0x33` of `sub_140001020` .

![9e163e531bb475d9382e2ea17b47575f.png](https://adhdmurky.github.io/PostImages/9e163e531bb475d9382e2ea17b47575f.png)

IDA does a poor job guessing some driver data types and variables. Luckily, I did wrote few of my own dumb drivers and reverse engineered them, so now I know which data types are most commonly replaced with which ones. Also, due to their values, it’s easy to recognize them.

Here is IDA wrong version:

![21c43e929f173d0721091fcde19b8be7.png](https://adhdmurky.github.io/PostImages/21c43e929f173d0721091fcde19b8be7.png)

And here is my version.

![d3cabe67f6f0e966a997fd21253110ad.png](https://adhdmurky.github.io/PostImages/d3cabe67f6f0e966a997fd21253110ad.png)

If you look closely, we can see several interesting things: First is the function we were looking for, second is the input/output buffer length, and lastly the IOCTL code used for this Major Function.

If we provide the correct IOCTL and correct buffer to the IRP, we should be able to pass the Process ID (which is, by the way, a DWORD; 4 bytes in length, as seen in the input buffer length).

But there is one thing missing: the symbolic link. The best way to find it is to, yet again, go to the cross-reference of our newly found `sub_140001020` function.

![c885824b6994b9fd20c9f9cf56e3839a.png](https://adhdmurky.github.io/PostImages/c885824b6994b9fd20c9f9cf56e3839a.png)

And finally we are at our DriverEntry function or I would call it the main function for drivers. Here we see our MajorFunction\[14\] aka. IRP\_MJ\_DEVICE\_CONTROL that gets executed once DeviceIoControl is called by user-mode (very important for our console app later).

And a bit lower we can see DeviceName of our driver “BootRepair”. The driver created a symbolic link in the object manager under the MS‑DOS device namespace as “\\\DosDevices\\\BootRepair”, and user‑mode opens the corresponding DosDevices entry by using the Win32 device path prefix “\\\.” (so CreateFile("\\\.\\BootRepair") resolves to \\DosDevices\\BootRepair). And voilà! we have all we need to build our console app.

![f6837b5e517c2474054008ceed3b68db.png](https://adhdmurky.github.io/PostImages/f6837b5e517c2474054008ceed3b68db.png)

Onto our Console app we go, and no I didn’t vibe-code this.

We use header that we need for all the functions used to interact with driver, and one of the important stuff is that we define IOCTL code we need for our driver Major Function call.

Our app will take the ProcessID as its only argument, and since we need it as the buffer for the DeviceIoControl function, we also calculate its size.

Keep in mind that we already know what we need to provide in the input buffer and the buffer size, as mentioned earlier during reversing process.

To gain a handle to our device, we need to provide the symbolic link name because this is a user-mode application, along with the minimum required access and other parameters that are not worth mentioning (due to skill issue).

![77eb2eb46c11143a0e039ba7f7365925.png](https://adhdmurky.github.io/PostImages/77eb2eb46c11143a0e039ba7f7365925.png)

Lastly our DeviceIoControl function that requires our already obtained device handle, IOCTL code, and input buffer and its size. Since driver doesn’t write anything back output buffer argument is NULL and size is 0.

![bde22fc92bb51649a3e3b23ac288f657.png](https://adhdmurky.github.io/PostImages/bde22fc92bb51649a3e3b23ac288f657.png)

Sadly I don’t have any EDR to terminate in my VM, but I will demonstrate with simple notepad.exe running as Local Administrator. We can see that our lowpriv user can’t meddle with process that has higher integrity then his own:

![7ea83cef6191cd8904485c8e8f3a046b.png](https://adhdmurky.github.io/PostImages/7ea83cef6191cd8904485c8e8f3a046b.png)

Now we load our Lenovo driver, and as you can see in the bottom right part Test Mode is not turned on.

![1789b231f5a621a705df886f99134557.png](https://adhdmurky.github.io/PostImages/1789b231f5a621a705df886f99134557.png)

Because Test Mode is not enabled, this is what happens when you try to create a service for your own unsigned driver, it gets blocked by Driver Signature Enforcement. Unless you have a valid code-signing certificate to sign your driver, are abusing an already-signed legitimate driver (as in BYOVD), the only remaining option is to disable DSE but that is not the point in this blog.

![4bb031b82ee1585a8f65ee87a2f810f9.png](https://adhdmurky.github.io/PostImages/4bb031b82ee1585a8f65ee87a2f810f9.png)

And finally, we can see our console app in action successfully terminating a highly elevated process by abusing a Lenovo driver.

![ebf614da3878ed6ce640ba620c410af2.png](https://adhdmurky.github.io/PostImages/ebf614da3878ed6ce640ba620c410af2.png)

[Go to top](https://adhdmurky.github.io/posts/post3/# "Go to top")