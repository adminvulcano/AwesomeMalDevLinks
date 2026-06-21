# https://github.com/mandiant/gopacket

[Skip to content](https://github.com/mandiant/gopacket#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/mandiant/gopacket) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/mandiant/gopacket) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/mandiant/gopacket) to refresh your session.Dismiss alert

{{ message }}

[mandiant](https://github.com/mandiant)/ **[gopacket](https://github.com/mandiant/gopacket)** Public

- [Notifications](https://github.com/login?return_to=%2Fmandiant%2Fgopacket) You must be signed in to change notification settings
- [Fork\\
56](https://github.com/login?return_to=%2Fmandiant%2Fgopacket)
- [Star\\
677](https://github.com/login?return_to=%2Fmandiant%2Fgopacket)


main

[**1** Branch](https://github.com/mandiant/gopacket/branches) [**0** Tags](https://github.com/mandiant/gopacket/tags)

[Go to Branches page](https://github.com/mandiant/gopacket/branches)[Go to Tags page](https://github.com/mandiant/gopacket/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![psycep](https://avatars.githubusercontent.com/u/93807253?v=4&size=40)](https://github.com/psycep)[psycep](https://github.com/mandiant/gopacket/commits?author=psycep)<br>[Merge pull request](https://github.com/mandiant/gopacket/commit/f638237f7d0fdb456b6eb10b2b9d945a08a30558) [#35](https://github.com/mandiant/gopacket/pull/35) [from ahm3dgg/allow-multiple-smb-dialects](https://github.com/mandiant/gopacket/commit/f638237f7d0fdb456b6eb10b2b9d945a08a30558)<br>Open commit details<br>2 weeks agoJun 8, 2026<br>[f638237](https://github.com/mandiant/gopacket/commit/f638237f7d0fdb456b6eb10b2b9d945a08a30558) · 2 weeks agoJun 8, 2026<br>## History<br>[55 Commits](https://github.com/mandiant/gopacket/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/mandiant/gopacket/commits/main/) 55 Commits |
| [internal/build](https://github.com/mandiant/gopacket/tree/main/internal/build "This path skips through empty directories") | [internal/build](https://github.com/mandiant/gopacket/tree/main/internal/build "This path skips through empty directories") | [Initial commit](https://github.com/mandiant/gopacket/commit/160b6a42805e2c782bfa5b929a303332944baeef "Initial commit") | 2 months agoApr 17, 2026 |
| [pkg](https://github.com/mandiant/gopacket/tree/main/pkg "pkg") | [pkg](https://github.com/mandiant/gopacket/tree/main/pkg "pkg") | [Merge pull request](https://github.com/mandiant/gopacket/commit/f638237f7d0fdb456b6eb10b2b9d945a08a30558 "Merge pull request #35 from ahm3dgg/allow-multiple-smb-dialects  Allow Multiple SMB Dialects") [#35](https://github.com/mandiant/gopacket/pull/35) [from ahm3dgg/allow-multiple-smb-dialects](https://github.com/mandiant/gopacket/commit/f638237f7d0fdb456b6eb10b2b9d945a08a30558 "Merge pull request #35 from ahm3dgg/allow-multiple-smb-dialects  Allow Multiple SMB Dialects") | 2 weeks agoJun 8, 2026 |
| [tools](https://github.com/mandiant/gopacket/tree/main/tools "tools") | [tools](https://github.com/mandiant/gopacket/tree/main/tools "tools") | [exec-tools: fix output polling for long-running commands](https://github.com/mandiant/gopacket/commit/dfe4d2ea7b83f703d588bd76d6995a4d6c807271 "exec-tools: fix output polling for long-running commands  Two compounding bugs in wmiexec / atexec / smbexec / dcomexec made the output-retrieval loop return early on any command that didn't finish within the first 100ms poll, leaking the temp file in ADMIN$ / C$. Issue #22 reports the symptom for wmiexec (systeminfo, ping); the same broken pattern existed in all four tools.  1. Wrong call site. The polling loop treated a sharing-violation    on smbClient.Cat as the signal \"command still running.\" Cat    opens with FILE_SHARE_READ-compatible access — it succeeds    against the writer on the first poll and returns the file as    it currently exists (typically empty). The conflict actually    lives on Rm: deleting the file requires DELETE access, which    conflicts with the writer's share mode. Moved the sharing-    violation check from Cat to Rm. Matches Impacket's wmiexec.py.  2. Dead string match. The check was    strings.Contains(err.Error(), \"STATUS_SHARING_VIOLATION\"). The    underlying smb2 library's NtStatus.Error() returns only the    human-readable description (\"A file cannot be opened because    the share access flags are incompatible.\") — the literal    constant name never appears in err.Error(), so the check could    never fire. Same issue for STATUS_OBJECT_NAME_NOT_FOUND in the    not-found branch (further muddled by smb2/conn.go translating    that NTSTATUS to os.ErrNotExist before wrapping).  Added typed helpers in pkg/smb (IsSharingViolation, IsNotFound) that unwrap through *os.PathError and match on *smb2.ResponseError.Code plus the os.ErrNotExist sentinel. NTSTATUS values are hardcoded since the smb2/internal/erref package can't be imported from outside the smb2 tree.  The dcomexec \"broken / connection reset / use of closed\" branch stays string-matched — those errors come from net, not smb2.  Thanks to @aimogging in #22 for the diagnosis and proof-of-concept in #29; this change applies the same Cat-vs-Rm insight across all four exec tools and replaces the err.Error() substring matching with typed-error helpers so future smb2 library changes don't silently break the check again.  Verified against GOAD winterfell: wmiexec whoami / systeminfo / ping -n 4 1.1.1.1 all return full output, exit 0, no ADMIN$ residue, both directly from the operator box and over SOCKS5H proxy.") | last monthMay 12, 2026 |
| [.gitignore](https://github.com/mandiant/gopacket/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/mandiant/gopacket/blob/main/.gitignore ".gitignore") | [Initial commit](https://github.com/mandiant/gopacket/commit/160b6a42805e2c782bfa5b929a303332944baeef "Initial commit") | 2 months agoApr 17, 2026 |
| [CONTRIBUTING.md](https://github.com/mandiant/gopacket/blob/main/CONTRIBUTING.md "CONTRIBUTING.md") | [CONTRIBUTING.md](https://github.com/mandiant/gopacket/blob/main/CONTRIBUTING.md "CONTRIBUTING.md") | [Initial commit](https://github.com/mandiant/gopacket/commit/160b6a42805e2c782bfa5b929a303332944baeef "Initial commit") | 2 months agoApr 17, 2026 |
| [KNOWN\_ISSUES.md](https://github.com/mandiant/gopacket/blob/main/KNOWN_ISSUES.md "KNOWN_ISSUES.md") | [KNOWN\_ISSUES.md](https://github.com/mandiant/gopacket/blob/main/KNOWN_ISSUES.md "KNOWN_ISSUES.md") | [kerberos, dcerpc: tunnel KDC traffic through pkg/transport](https://github.com/mandiant/gopacket/commit/8eea02943132c064aeb89372ad76777ab8213bd9 "kerberos, dcerpc: tunnel KDC traffic through pkg/transport  The embedded gokrb5/v8 library hard-coded net.DialTimeout for AS/TGS exchanges, bypassing -proxy and leaking the operator's source IP to the KDC (UDP/88 first, TCP/88 fallback). The DCERPC Kerberos auth path used a separate library (oiweiwei/gokrb5.fork/v9 via go-msrpc) that leaked the same way.  Vendor jcmturner/gokrb5/v8 in-tree at pkg/third_party/gokrb5 with a required KDCDialer first argument on every client constructor, so proxy-bypass becomes a compile error. Wire kerberos.TransportKDCDialer everywhere a gokrb5 client is built. Stamp udp_preference_limit=1 and dns_lookup_kdc/realm=false unconditionally so KRB5 is TCP-only and the OS resolver is never consulted; /etc/krb5.conf and $KRB5_CONFIG are deliberately not read.  For DCERPC: set krbConfig.KDCDialer on every krb5.Config, pass dcerpc.WithDialer(transport.ContextDialer{}) on every dcerpc.Dial, and use the \"ncacn_ip_tcp:\" StringBinding prefix on the OXID-pivot dial so go-msrpc's hard-coded pre-dial net.LookupIP is skipped (defers FQDN resolution to the SOCKS5 proxy).  Verified against a live GOAD lab: 8 Kerberos-touching tools plus 5 NTLM/password/PtH regressions all operate through SOCKS5 with zero direct packets to the AD subnet. Negative control (no -proxy) immediately emits direct SYNs to the KDC, confirming both the leak class and the fix.") | last monthMay 12, 2026 |
| [LICENSE](https://github.com/mandiant/gopacket/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/mandiant/gopacket/blob/main/LICENSE "LICENSE") | [Initial commit](https://github.com/mandiant/gopacket/commit/160b6a42805e2c782bfa5b929a303332944baeef "Initial commit") | 2 months agoApr 17, 2026 |
| [Makefile](https://github.com/mandiant/gopacket/blob/main/Makefile "Makefile") | [Makefile](https://github.com/mandiant/gopacket/blob/main/Makefile "Makefile") | [Initial commit](https://github.com/mandiant/gopacket/commit/160b6a42805e2c782bfa5b929a303332944baeef "Initial commit") | 2 months agoApr 17, 2026 |
| [NOTICE](https://github.com/mandiant/gopacket/blob/main/NOTICE "NOTICE") | [NOTICE](https://github.com/mandiant/gopacket/blob/main/NOTICE "NOTICE") | [kerberos, dcerpc: tunnel KDC traffic through pkg/transport](https://github.com/mandiant/gopacket/commit/8eea02943132c064aeb89372ad76777ab8213bd9 "kerberos, dcerpc: tunnel KDC traffic through pkg/transport  The embedded gokrb5/v8 library hard-coded net.DialTimeout for AS/TGS exchanges, bypassing -proxy and leaking the operator's source IP to the KDC (UDP/88 first, TCP/88 fallback). The DCERPC Kerberos auth path used a separate library (oiweiwei/gokrb5.fork/v9 via go-msrpc) that leaked the same way.  Vendor jcmturner/gokrb5/v8 in-tree at pkg/third_party/gokrb5 with a required KDCDialer first argument on every client constructor, so proxy-bypass becomes a compile error. Wire kerberos.TransportKDCDialer everywhere a gokrb5 client is built. Stamp udp_preference_limit=1 and dns_lookup_kdc/realm=false unconditionally so KRB5 is TCP-only and the OS resolver is never consulted; /etc/krb5.conf and $KRB5_CONFIG are deliberately not read.  For DCERPC: set krbConfig.KDCDialer on every krb5.Config, pass dcerpc.WithDialer(transport.ContextDialer{}) on every dcerpc.Dial, and use the \"ncacn_ip_tcp:\" StringBinding prefix on the OXID-pivot dial so go-msrpc's hard-coded pre-dial net.LookupIP is skipped (defers FQDN resolution to the SOCKS5 proxy).  Verified against a live GOAD lab: 8 Kerberos-touching tools plus 5 NTLM/password/PtH regressions all operate through SOCKS5 with zero direct packets to the AD subnet. Negative control (no -proxy) immediately emits direct SYNs to the KDC, confirming both the leak class and the fix.") | last monthMay 12, 2026 |
| [README.md](https://github.com/mandiant/gopacket/blob/main/README.md "README.md") | [README.md](https://github.com/mandiant/gopacket/blob/main/README.md "README.md") | [README: add author byline](https://github.com/mandiant/gopacket/commit/901986d7fda69fdd9955898f38526ae43064ac8c "README: add author byline") | last monthMay 14, 2026 |
| [go.mod](https://github.com/mandiant/gopacket/blob/main/go.mod "go.mod") | [go.mod](https://github.com/mandiant/gopacket/blob/main/go.mod "go.mod") | [go.mod: bump x/crypto to v0.45.0 to clear ssh CVEs](https://github.com/mandiant/gopacket/commit/f83dc52479e1becc12dc6834c140eefe22216e41 "go.mod: bump x/crypto to v0.45.0 to clear ssh CVEs  Clears GHSA-f6x5-jh6r-wrfv (ssh/agent OOB panic) and GHSA-j5w8-q4qc-rx2x (ssh unbounded memory). We only import x/crypto/md4 and x/crypto/pbkdf2, so neither vuln is reachable from this repo, but bumping silences the Dependabot alerts. x/net and x/text pulled forward by go mod tidy.") | last monthMay 14, 2026 |
| [go.sum](https://github.com/mandiant/gopacket/blob/main/go.sum "go.sum") | [go.sum](https://github.com/mandiant/gopacket/blob/main/go.sum "go.sum") | [go.mod: bump x/crypto to v0.45.0 to clear ssh CVEs](https://github.com/mandiant/gopacket/commit/f83dc52479e1becc12dc6834c140eefe22216e41 "go.mod: bump x/crypto to v0.45.0 to clear ssh CVEs  Clears GHSA-f6x5-jh6r-wrfv (ssh/agent OOB panic) and GHSA-j5w8-q4qc-rx2x (ssh unbounded memory). We only import x/crypto/md4 and x/crypto/pbkdf2, so neither vuln is reachable from this repo, but bumping silences the Dependabot alerts. x/net and x/text pulled forward by go mod tidy.") | last monthMay 14, 2026 |
| [install.sh](https://github.com/mandiant/gopacket/blob/main/install.sh "install.sh") | [install.sh](https://github.com/mandiant/gopacket/blob/main/install.sh "install.sh") | [install.sh: prefix cross-compile outputs with gopacket-](https://github.com/mandiant/gopacket/commit/cae9eb3c79e4fdf2a17a3a4a2d3d28030839dedb "install.sh: prefix cross-compile outputs with gopacket-  The native install already renamed each tool to gopacket-<toolname> before copying to /usr/local/bin, but the portable and windows cross- compile targets dropped raw binaries like ping.exe, net.exe, reg.exe, attrib.exe, services.exe into ./dist/. When a user copies one of those to a Windows host and runs it from the same directory, cmd.exe's PATH resolution picks up the local binary before the Windows built-in of the same name, shadowing tools users rely on. The portable target on Linux has the same risk for binaries named ping, net, etc.  Applies the same normalization (lowercase, underscores to hyphens) and gopacket- prefix the native install already uses, but at build time for the cross-compile targets. Native behavior is unchanged: ./bin/ still gets raw names so install_native can prefix on copy.") | 2 months agoApr 22, 2026 |
| View all files |

## Repository files navigation

# gopacket

[Permalink: gopacket](https://github.com/mandiant/gopacket#gopacket)

By Jacob Paullus ( [@psycep\_](https://x.com/psycep_))

A complete Go implementation of [Impacket](https://github.com/fortra/impacket) \- 63 tools and 24 library packages for Windows network protocol interaction, Active Directory enumeration, and attack execution. Built as a native Go framework so you can compile once and run anywhere without Python dependencies.

> **Beta Release - Highly Experimental.** gopacket is under active development. Core tools have been tested against Active Directory lab environments, but edge cases and protocol quirks are expected. If something isn't working, please test the same operation with Impacket side-by-side and include both outputs in your bug report. This helps us quickly identify whether it's a gopacket-specific issue or a shared protocol limitation.

## Installation

[Permalink: Installation](https://github.com/mandiant/gopacket#installation)

```
git clone https://github.com/mandiant/gopacket
cd gopacket

# Default: Linux/macOS build + install to /usr/local/bin
./install.sh

# Run with no flags and it prompts you through the choices interactively.
# Or pick a target directly:
./install.sh --target portable   # static Linux binaries in ./dist/portable/
./install.sh --target windows    # Windows .exe cross-compiles in ./dist/windows/
./install.sh --target all        # build every target in one run

# Build without installing (native only)
./install.sh --build-only

# Or build with make
make build
```

The default (`--target native`) build needs Go 1.24.13+, GCC, and libpcap
development headers (`apt install build-essential libpcap-dev` on
Debian/Ubuntu/Kali, `yum install gcc libpcap-devel` on RHEL/CentOS, or
`brew install libpcap` on macOS). The `portable` and `windows` targets only
need the Go toolchain; `sniff` and `split` become stubs in those builds
because they require libpcap. See [Platform Support](https://github.com/mandiant/gopacket#platform-support) for
the full matrix.

### Platform Support

[Permalink: Platform Support](https://github.com/mandiant/gopacket#platform-support)

gopacket builds on Linux, macOS, and Windows. The set of working tools and
available proxying paths depends on the build flags:

| Build | Tools available | Proxying |
| --- | --- | --- |
| Linux / macOS with cgo (default) | All 63 | proxychains (LD\_PRELOAD) and/or `-proxy` SOCKS5 |
| Linux with `CGO_ENABLED=0` | 61 (`sniff`, `split` become stubs) | `-proxy` only (proxychains needs the libc hook) |
| Windows (`GOOS=windows CGO_ENABLED=0`) | 60 (`sniff`, `split`, `sniffer` stubs) | `-proxy` only (no `LD_PRELOAD` on Windows) |

`sniff` and `split` depend on libpcap via cgo; `sniffer` depends on Unix raw
sockets. When a tool can't be built for the target, gopacket substitutes a
stub that prints a clear message and exits 1, so `go build ./...` always
succeeds and the install layout is consistent across platforms.

To uninstall:

```
./install.sh --uninstall
```

## Proxy Support

[Permalink: Proxy Support](https://github.com/mandiant/gopacket#proxy-support)

gopacket supports two independent proxying paths. They can also be chained.

### proxychains (LD\_PRELOAD)

[Permalink: proxychains (LD_PRELOAD)](https://github.com/mandiant/gopacket#proxychains-ld_preload)

All gopacket tools work through proxychains. Go binaries normally bypass proxychains because Go's runtime handles DNS and networking internally, skipping the `LD_PRELOAD` hooks that proxychains relies on. gopacket works around this by linking against the system C library for network operations, allowing proxychains to intercept connections normally.

```
proxychains gopacket-secretsdump 'domain/user:password@target'
proxychains gopacket-smbclient -k -no-pass 'domain/user@dc.domain.local'
```

### Internal SOCKS5 proxy (`-proxy`)

[Permalink: Internal SOCKS5 proxy (-proxy)](https://github.com/mandiant/gopacket#internal-socks5-proxy--proxy)

Every tool accepts `-proxy` to route outbound TCP through a SOCKS5 server without relying on `LD_PRELOAD`. Accepted schemes: `socks5` and `socks5h`. When `-proxy` is unset, the `ALL_PROXY` / `all_proxy` environment variables are consulted as a fallback.

```
gopacket-secretsdump -proxy socks5h://127.0.0.1:1080 'domain/user:password@target'
ALL_PROXY=socks5h://127.0.0.1:1080 gopacket-smbclient 'domain/user:password@target'
```

UDP-dependent features are **disabled** under `-proxy` rather than silently leaking packets (SOCKS5 UDP ASSOCIATE is rarely supported by proxies, and bypassing the proxy for UDP would reveal the operator's real source IP). Affected features and their workarounds are documented in [KNOWN\_ISSUES.md](https://github.com/mandiant/gopacket/blob/main/KNOWN_ISSUES.md).

**Chaining:**`-proxy` is compatible with proxychains. The TCP connection to the SOCKS5 proxy itself still goes through libc `connect()`, so `proxychains → gopacket → -proxy → target` works for nested routing scenarios.

## Documentation

[Permalink: Documentation](https://github.com/mandiant/gopacket#documentation)

See the [Library Developer Guide](https://github.com/mandiant/gopacket/wiki) for full API documentation, code examples, and architecture overview for building custom tools on top of gopacket's 24 protocol packages.

## Tools (63)

[Permalink: Tools (63)](https://github.com/mandiant/gopacket#tools-63)

### Remote Execution

[Permalink: Remote Execution](https://github.com/mandiant/gopacket#remote-execution)

| Tool | Description |
| --- | --- |
| **psexec** | Remote command execution via SMB service creation |
| **smbexec** | Remote command execution via SMB (stealthier than psexec) |
| **wmiexec** | Remote command execution via WMI |
| **dcomexec** | Remote command execution via DCOM |
| **atexec** | Remote command execution via Task Scheduler |

### Credential Dumping & DPAPI

[Permalink: Credential Dumping & DPAPI](https://github.com/mandiant/gopacket#credential-dumping--dpapi)

| Tool | Description |
| --- | --- |
| **secretsdump** | SAM/LSA/NTDS.dit extraction and DCSync (remote + offline) |
| **dpapi** | DPAPI backup key extraction |
| **esentutl** | Offline ESE database parser (NTDS.dit) |
| **registry-read** | Offline Windows registry hive parser |

### Kerberos

[Permalink: Kerberos](https://github.com/mandiant/gopacket#kerberos)

| Tool | Description |
| --- | --- |
| **getTGT** | Request a TGT with password, hash, or AES key |
| **getST** | Request a service ticket with S4U2Self/S4U2Proxy |
| **GetUserSPNs** | Kerberoasting - find and request SPNs |
| **GetNPUsers** | AS-REP roasting - find accounts without pre-auth |
| **ticketer** | Golden/silver ticket forging |
| **ticketConverter** | Convert between ccache and kirbi formats |
| **describeTicket** | Parse and decrypt Kerberos tickets |
| **getPac** | Request and parse PAC information |
| **keylistattack** | KERB-KEY-LIST-REQ attack (RODC) |
| **raiseChild** | Child-to-parent domain escalation via golden ticket |

### Active Directory Enumeration

[Permalink: Active Directory Enumeration](https://github.com/mandiant/gopacket#active-directory-enumeration)

| Tool | Description |
| --- | --- |
| **GetADUsers** | Enumerate domain users via LDAP |
| **GetADComputers** | Enumerate domain computers via LDAP |
| **GetLAPSPassword** | Read LAPS passwords via LDAP |
| **findDelegation** | Find delegation configurations |
| **lookupsid** | SID brute-forcing via LSARPC |
| **samrdump** | Enumerate users via SAMR |
| **rpcdump** | Dump RPC endpoints via epmapper |
| **rpcmap** | Scan for accessible RPC interfaces |
| **net** | net user/group/computer enumeration via SAMR/LSARPC |
| **netview** | Enumerate sessions, shares, and logged-on users |
| **CheckLDAPStatus** | Check LDAP signing and channel binding requirements |
| **DumpNTLMInfo** | Dump NTLM authentication info from SMB negotiation |
| **getArch** | Detect remote OS architecture via RPC |
| **machine\_role** | Detect machine role (DC, server, workstation) |

### Active Directory Attacks

[Permalink: Active Directory Attacks](https://github.com/mandiant/gopacket#active-directory-attacks)

| Tool | Description |
| --- | --- |
| **addcomputer** | Create/modify/delete machine accounts (SAMR + LDAP) |
| **rbcd** | Resource-Based Constrained Delegation manipulation |
| **dacledit** | Read/write DACLs on AD objects |
| **owneredit** | Read/modify object ownership |
| **samedit** | SAM account name spoofing (CVE-2021-42278/42287) |
| **badsuccessor** | BadSuccessor / backup operator escalation |
| **changepasswd** | Change/reset passwords via SAMR and LDAP |

### SMB Tools

[Permalink: SMB Tools](https://github.com/mandiant/gopacket#smb-tools)

| Tool | Description |
| --- | --- |
| **smbclient** | Interactive SMB client (shares, ls, get, put, etc.) |
| **smbserver** | SMB server for file sharing |
| **attrib** | Query/modify file attributes via SMB |
| **filetime** | Query/modify file timestamps via SMB |
| **services** | Remote service management via SVCCTL |
| **reg** | Remote registry operations via WINREG |
| **Get-GPPPassword** | Extract Group Policy Preferences passwords from SYSVOL |
| **karmaSMB** | Rogue SMB server for hash capture |

### NTLM Relay

[Permalink: NTLM Relay](https://github.com/mandiant/gopacket#ntlm-relay)

| Tool | Description |
| --- | --- |
| **ntlmrelayx** | Full NTLM relay framework with multi-protocol support |

ntlmrelayx supports:

- **Capture servers:** SMB, HTTP/HTTPS, WCF (ADWS), RAW, RPC, WinRM
- **Relay clients:** SMB, LDAP/LDAPS, HTTP/HTTPS, MSSQL, WinRM, RPC
- **Attacks:** secretsdump, smbexec, ldapdump, RBCD delegation, ACL abuse, shadow credentials, ADCS ESC8, addcomputer, DNS manipulation, and more
- **Infrastructure:** SOCKS5 proxy with protocol-aware plugins, interactive console, REST API, multi-target round-robin, WPAD serving

### SQL Server

[Permalink: SQL Server](https://github.com/mandiant/gopacket#sql-server)

| Tool | Description |
| --- | --- |
| **mssqlclient** | Interactive MSSQL client with SQL/Windows/Kerberos auth |
| **mssqlinstance** | MSSQL instance discovery via SQL Browser |

### WMI

[Permalink: WMI](https://github.com/mandiant/gopacket#wmi)

| Tool | Description |
| --- | --- |
| **wmiquery** | Interactive WMI query shell |
| **wmipersist** | WMI event subscription persistence |

### Terminal Services

[Permalink: Terminal Services](https://github.com/mandiant/gopacket#terminal-services)

| Tool | Description |
| --- | --- |
| **tstool** | Terminal Services session and process enumeration |

### Other Protocols

[Permalink: Other Protocols](https://github.com/mandiant/gopacket#other-protocols)

| Tool | Description |
| --- | --- |
| **rdp\_check** | RDP authentication check |
| **mqtt\_check** | MQTT authentication check |
| **exchanger** | Exchange Web Services client |

### Utilities

[Permalink: Utilities](https://github.com/mandiant/gopacket#utilities)

| Tool | Description |
| --- | --- |
| **ntfs-read** | Offline NTFS filesystem parser |
| **ping** / **ping6** | ICMP ping |
| **sniff** / **sniffer** | Network packet capture |
| **split** | Split large files |

## Authentication

[Permalink: Authentication](https://github.com/mandiant/gopacket#authentication)

All network tools support three authentication methods:

```
# Password
gopacket-secretsdump 'domain/user:password@target'

# NTLM hash (pass-the-hash)
gopacket-secretsdump -hashes ':nthash' 'domain/user@target'

# Kerberos (pass-the-ticket)
KRB5CCNAME=ticket.ccache gopacket-secretsdump -k -no-pass 'domain/user@target'
```

### Common Flags

[Permalink: Common Flags](https://github.com/mandiant/gopacket#common-flags)

| Flag | Description |
| --- | --- |
| `-hashes LMHASH:NTHASH` | NTLM hash authentication (LM hash can be empty) |
| `-k` | Use Kerberos authentication |
| `-no-pass` | Don't prompt for password (use with `-k` or `-hashes`) |
| `-dc-ip IP` | IP address of the domain controller |
| `-target-ip IP` | IP address of the target (when using hostname for Kerberos) |
| `-port PORT` | Target port (defaults vary by tool) |
| `-proxy URL` | Route outbound TCP through a SOCKS5 proxy (e.g. `socks5h://127.0.0.1:1080`). UDP features are disabled. |
| `-debug` | Enable debug output |

### Quick Examples

[Permalink: Quick Examples](https://github.com/mandiant/gopacket#quick-examples)

```
# Dump domain hashes via DCSync
gopacket-secretsdump 'corp.local/admin:Password1@dc01.corp.local'

# Interactive SMB shell
gopacket-smbclient -hashes ':aabbccdd...' 'corp.local/admin@fileserver'

# Kerberoast
gopacket-getuserspns 'corp.local/user:pass@dc01.corp.local'

# Golden ticket
gopacket-ticketer -nthash <krbtgt_hash> -domain-sid S-1-5-21-... -domain corp.local admin

# NTLM relay with SOCKS proxy
sudo gopacket-ntlmrelayx -t smb://target -socks

# LDAP relay for RBCD
sudo gopacket-ntlmrelayx -t ldaps://dc01.corp.local --delegate-access

# Route all outbound traffic through a SOCKS5 proxy
gopacket-secretsdump -proxy socks5h://127.0.0.1:1080 'corp.local/admin:pass@dc01.corp.local'
```

## Library

[Permalink: Library](https://github.com/mandiant/gopacket#library)

The `pkg/` directory contains 24 reusable protocol packages that can be imported independently.

| Package | Description |
| --- | --- |
| **smb** | SMB2/3 client with NTLM and Kerberos auth |
| **ldap** | LDAP client with NTLM/Kerberos bind |
| **dcerpc** | DCE/RPC client + 20 service implementations (DRSUAPI, SAMR, SVCCTL, LSARPC, WINREG, NETLOGON, DCOM, TSCH, EPMAPPER, etc.) |
| **kerberos** | Kerberos client, ticket forging (golden/silver), S4U2Self/S4U2Proxy |
| **ntlm** | NTLM authentication protocol |
| **relay** | NTLM relay framework (servers, clients, attacks, SOCKS) |
| **tds** | SQL Server TDS protocol |
| **ese** | Extensible Storage Engine parser |
| **registry** | Windows registry hive parser |
| **ntfs** | NTFS filesystem parser |
| **security** | Security descriptors, ACLs, SIDs |
| **dpapi** | DPAPI structures |
| **mqtt** | MQTT protocol client |
| **session** | Target/credential parsing (`domain/user:pass@host`) |
| **flags** | Unified CLI flag framework |

## Missing Features (vs Impacket)

[Permalink: Missing Features (vs Impacket)](https://github.com/mandiant/gopacket#missing-features-vs-impacket)

gopacket aims for full Impacket parity. The following are not yet implemented:

**Relay protocol clients:**

- IMAP relay client + attack (requires Exchange/IMAP server)
- SMTP relay client (requires SMTP server)

**Relay attack modules:**

- SCCM policies/DP attacks (requires SCCM infrastructure)

**Standalone tools:**

- `ifmap.py` (DCOM interface mapping)
- `mimikatz.py` (limited Mimikatz over RPC)
- `goldenPac.py` (MS14-068 - obsolete on patched systems)
- `smbrelayx.py` (superseded by ntlmrelayx)
- `kintercept.py` (Kerberos interception)

These gaps are low priority - most require niche infrastructure to test or are obsoleted by newer techniques.

## Known Limitations

[Permalink: Known Limitations](https://github.com/mandiant/gopacket#known-limitations)

These are protocol-level limitations shared with Impacket, not gopacket bugs:

- **SMB to LDAPS relay** fails on patched DCs due to NTLM MIC validation (post-CVE-2019-1040). Use HTTP coercion instead.
- **WinRM relay** blocked by EPA (Extended Protection for Authentication) on patched Server 2019+.
- **RPC relay attacks** (tschexec, enum-local-admins) require PKT\_INTEGRITY which is unavailable in relay sessions.
- **LDAP relay to port 389** fails on DCs requiring LDAP signing. Always relay to LDAPS (port 636).

See [KNOWN\_ISSUES.md](https://github.com/mandiant/gopacket/blob/main/KNOWN_ISSUES.md) for detailed information on each issue and workarounds.

## Reporting Issues & Contributing

[Permalink: Reporting Issues & Contributing](https://github.com/mandiant/gopacket#reporting-issues--contributing)

> This is a beta release. Bugs are expected, and contributions are welcome.

### Why we ask you to test with Impacket first

[Permalink: Why we ask you to test with Impacket first](https://github.com/mandiant/gopacket#why-we-ask-you-to-test-with-impacket-first)

Because gopacket implements the same wire protocols as Impacket, a large
fraction of "bugs" turn out to be **environmental**, not gopacket-specific -
patched DCs, LDAP signing requirements, EPA, PKT\_INTEGRITY, SMB signing,
NTLM MIC validation post-CVE-2019-1040, missing SPNs, time skew, DNS quirks,
firewall rules, and so on. Running the same operation with Impacket side by
side removes the environment from the equation:

- **If Impacket fails the same way**, the issue is almost always
environmental and is likely already documented in
[KNOWN\_ISSUES.md](https://github.com/mandiant/gopacket/blob/main/KNOWN_ISSUES.md). No bug report needed.
- **If Impacket succeeds where gopacket fails**, that's a real gopacket bug
and exactly what we want to hear about.

This single triage step saves a lot of round-trips, so please don't skip it.

### Filing a bug report

[Permalink: Filing a bug report](https://github.com/mandiant/gopacket#filing-a-bug-report)

1. Run the same operation with Impacket and note whether it succeeds or fails
2. Re-run gopacket with `-debug` and capture the full output
3. **Anonymize anything sensitive before posting.** GitHub issues are public.
Strip or replace real hostnames, IP addresses, usernames, password hashes,
Kerberos tickets, domain names, SIDs, and any output line that could be
tied back to a real engagement. Replacing `corp.internal` → `example.local`
and `dc01.corp.internal` → `dc01.example.local` is fine - keep the
structure of the data, just not the identifying values. **If in doubt,**
**redact it.**
4. Open a [GitHub issue](https://github.com/mandiant/gopacket/issues/new) and include:

   - Both outputs (gopacket and Impacket), as text not screenshots, anonymized
   - The exact command line you ran (anonymized)
   - Target OS, AD functional level, and any relevant hardening
     (signing, EPA, channel binding, patch level)
   - gopacket version / commit hash

### Feature requests

[Permalink: Feature requests](https://github.com/mandiant/gopacket#feature-requests)

Open a [GitHub issue](https://github.com/mandiant/gopacket/issues/new) describing the use case
and the Impacket equivalent (if any). If the feature is on the
"Missing Features" list above, mention which one - it helps us prioritize.

### Pull requests

[Permalink: Pull requests](https://github.com/mandiant/gopacket#pull-requests)

PRs are welcome. Before opening one:

- Run `go build ./...`, `go vet ./...`, `gofmt -l .`, and `go test ./...`
and make sure they all pass cleanly
- Match the existing code style in the package you're touching
- Keep changes focused - separate refactors from feature work
- For non-trivial changes, open an issue first to discuss the approach

## Why This Matters for Defenders

[Permalink: Why This Matters for Defenders](https://github.com/mandiant/gopacket#why-this-matters-for-defenders)

Threat actors are moving away from Python. Compiled Go and Rust tooling
(Sliver, BRC4, Geacon, and bespoke loaders) is increasingly replacing
Impacket in real-world intrusions. Most defensive tooling and detection
logic was built around Impacket's Python-based network behavior, and that
coverage is eroding as the attacker ecosystem shifts to compiled languages.

gopacket exists in part to help the security community get ahead of this
shift. By providing an open-source, readable Go implementation of the
same protocols and techniques, defenders and detection engineers can:

- **Study how Go-based tooling behaves on the wire** rather than waiting
to encounter it during an incident
- **Understand the protocol-level differences** between Go and Python
implementations that make existing signatures less effective
- **Run realistic purple team exercises** using the same compiled,
single-binary tooling that threat actors are adopting, rather than
testing exclusively against Python scripts that behave differently
at the network layer

The gap between attacker tooling and defender visibility is widest when
new tooling stays private. Open-sourcing gopacket narrows that gap.

## Notes

[Permalink: Notes](https://github.com/mandiant/gopacket#notes)

- Kerberos authentication requires a valid ccache file (TGT or service ticket)
- For Kerberos, use the FQDN hostname - not an IP address
- If `KRB5CCNAME` is not set, tools will look for `<username>.ccache` in the current directory
- All tools support both proxychains and an internal `-proxy` SOCKS5 flag (see Proxy Support)
- This project is for authorized security testing and research purposes only

## License

[Permalink: License](https://github.com/mandiant/gopacket#license)

Released under the [Apache License 2.0](https://github.com/mandiant/gopacket/blob/main/LICENSE).

gopacket is a clean Go reimplementation of [Impacket](https://github.com/fortra/impacket); see [NOTICE](https://github.com/mandiant/gopacket/blob/main/NOTICE) for full third-party acknowledgments.

## About

Gopacket is a clean Go implementation of Impacket, a library intended for working with network protocols.


### Resources

[Readme](https://github.com/mandiant/gopacket#readme-ov-file)

### License

[Apache-2.0 license](https://github.com/mandiant/gopacket#Apache-2.0-1-ov-file)

### Contributing

[Contributing](https://github.com/mandiant/gopacket#contributing-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/mandiant/gopacket).

[Activity](https://github.com/mandiant/gopacket/activity)

[Custom properties](https://github.com/mandiant/gopacket/custom-properties)

### Stars

[**677**\\
stars](https://github.com/mandiant/gopacket/stargazers)

### Watchers

[**3**\\
watching](https://github.com/mandiant/gopacket/watchers)

### Forks

[**56**\\
forks](https://github.com/mandiant/gopacket/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fmandiant%2Fgopacket&report=mandiant+%28user%29)

## [Releases](https://github.com/mandiant/gopacket/releases)

No releases published

## [Packages\  0](https://github.com/orgs/mandiant/packages?repo_name=gopacket)

No packages published

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/mandiant/gopacket).

## [Contributors\  4](https://github.com/mandiant/gopacket/graphs/contributors)

- [![@psycep](https://avatars.githubusercontent.com/u/93807253?s=64&v=4)](https://github.com/psycep)[**psycep** Jacob Paullus](https://github.com/psycep)
- [![@dependabot[bot]](https://avatars.githubusercontent.com/in/29110?s=64&v=4)](https://github.com/apps/dependabot)[**dependabot\[bot\]**](https://github.com/apps/dependabot)
- [![@Jah-yee](https://avatars.githubusercontent.com/u/166608075?s=64&v=4)](https://github.com/Jah-yee)[**Jah-yee** RoomWithOutRoof](https://github.com/Jah-yee)
- [![@ahm3dgg](https://avatars.githubusercontent.com/u/210139660?s=64&v=4)](https://github.com/ahm3dgg)[**ahm3dgg** ahmed](https://github.com/ahm3dgg)

## Languages

- [Go99.1%](https://github.com/mandiant/gopacket/search?l=go)
- Other0.9%

You can’t perform that action at this time.