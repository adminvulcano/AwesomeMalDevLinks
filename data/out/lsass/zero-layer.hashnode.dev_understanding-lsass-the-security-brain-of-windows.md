# https://zero-layer.hashnode.dev/understanding-lsass-the-security-brain-of-windows

## Command Palette

Search for a command to run...

[![Sravan](https://cdn.hashnode.com/res/hashnode/image/upload/v1771408246446/45f6b326-8c15-4709-a29e-f532f4fb8a85.jpeg?w=500&h=500&fit=crop&crop=entropy&auto=compress,format&format=webp&auto=compress,format&format=webp)](https://hashnode.com/@Sravan-)

[Sravan](https://hashnode.com/@Sravan-)

### **Introduction – What This LSASS Article Will Cover**

In this article, we will take a deep dive into LSASS — not from a tool perspective, but from an architectural and internal understanding standpoint. LSASS is often mentioned in the context of credential dumping or red team operations, but very few discussions focus on how it actually works internally and why it is such a central component of Windows security.

The goal of this article is to understand LSASS as a session-based authentication authority inside Windows. We will explore how LSASS manages multiple logon sessions simultaneously, how user identities are isolated within memory, how authentication packages such as Kerberos and NTLM integrate into LSASS, and how access tokens are generated and maintained. Rather than viewing LSASS as a static credential vault.

We will also examine how Kerberos tickets are stored in memory, how they are scoped per logon session, and how Windows enables single sign-on by caching cryptographic material inside LSASS.

This understanding is essential for both offensive research and defensive engineering, because modern attacks increasingly focus on manipulating authentication tickets and access tokens directly in memory, rather than performing traditional disk-based credential dumping.

### What Is LSASS ?

On every modern Windows system, there is one process that quietly sits at the center of all authentication, authorization, and identity decisions: **LSASS**, the Local Security Authority Subsystem Service. While it is often mentioned casually in security discussions as “the process that holds credentials,” that description barely scratches the surface of what LSASS actually represents inside the Windows operating system.

LSASS is not just a credential store. It is an enforcement engine of Windows security policy. Every time a user logs on OR a service starts OR a scheduled task runs OR a network resource is accessed, LSASS is involved in deciding _who_ is making the request, _what identity_ they are using, and _what they are allowed to do_. Because of this role, LSASS runs as **SYSTEM**, making it one of the most privileged user-mode processes on the machine.

At higher level, LSASS is responsible for Creating Access Tokens, validating credentials, maintaining authentication state for all active logon sessions.

This design allows Windows to support features such as single sign-on, background service authentication, and seamless access to domain resources without repeatedly prompting users for their passwords.

### Internal Structure of LSASS ?

When most people think of LSASS, they imagine a single block of memory containing password hashes and Kerberos tickets. In reality, LSASS is structured more like a compartmentalized security container, carefully organizing authentication material into isolated logical sections called **logon sessions**.

![](https://cloudmate-test.s3.us-east-1.amazonaws.com/uploads/covers/6995899a1a3e7d78226cd5f9/91a04c25-472e-463e-a5ef-fab35922de45.png)

To truly understand LSASS, we must stop thinking of it as a single memory container and instead view it as a structured, session-oriented security architecture. The diagram above illustrates this concept: LSASS does not store credentials globally. Instead, it maintains multiple independent logon sessions inside a single protected process.

Every time a security principal authenticates on a Windows system — whether that is an interactive user, an RDP session, a scheduled task, or a service account — LSASS creates a dedicated logon session. These sessions coexist within LSASS memory but remain logically separated from one another.

This separation is fundamental to Windows security design.

Inside each session, LSASS loads authentication package state. In a domain environment, this primarily includes Kerberos structures. These structures contain long-term encryption keys, Ticket Granting Tickets (TGTs), service tickets (TGS), session keys, and ticket metadata such as lifetime and renewability flags.

The critical concept shown in the diagram is that Kerberos tickets are not global to the machine. They are bound to the specific logon session that requested them.

For example if User Dave accesses a file share such as `\\web04\backup`, the domain controller issues a TGS for the CIFS service on web04. That TGS is stored inside Dave’s logon session. If User Jen logs in to the same machine but has not accessed that resource, her logon session will not contain that TGS. Even though both users share the same physical system and LSASS process, their authentication material remains isolated.

This is why LSASS can safely support multiple concurrent identities without cross-contaminating credentials.

Beyond Kerberos, LSASS also supports other authentication mechanisms. If Kerberos is unavailable or not applicable, NTLM authentication material may be stored within the same logon session. This can include NT hashes or cached challenge-response data. LSASS therefore acts as a multi-protocol credential vault rather than a single-purpose Kerberos store.

From a security standpoint, access to LSASS memory is heavily restricted. Since LSASS runs as SYSTEM, a process typically requires administrative privileges combined with SeDebugPrivilege to open it for memory access. Recognizing the historical abuse of LSASS for credential extraction, Microsoft introduced LSA Protection in 2012, allowing LSASS to run as a Protected Process Light (PPL). This significantly restricts unauthorized memory access even from administrative processes.

### In-Memory Kerberos Ticket Transfer

In a normal Kerberos authentication flow, the client does not directly authenticate to a service using a password. Instead, it follows a structured exchange with the domain controller. First, the client sends an AS-REQ and receives an AS-REP, which results in a Ticket Granting Ticket (TGT). Next, the client requests access to a specific service using a TGS-REQ and receives a TGS-REP, which contains a service ticket. Finally, that service ticket is presented to the target system to establish authenticated access.

When this flow completes successfully, the issued tickets are delivered back to the client and stored inside LSASS under the user’s logon session.

LSASS then holds the TGT, any issued TGS tickets, and the associated session keys. From that point forward, Windows can transparently access services without prompting the user again. This is the foundation of **single sign-on.**

![](https://cloudmate-test.s3.us-east-1.amazonaws.com/uploads/covers/6995899a1a3e7d78226cd5f9/17aec0ca-86be-4351-ab09-56caa565df7d.png)

The important architectural detail is this: once a TGS has been issued, the domain controller is no longer involved in validating every subsequent access. The service trusts the ticket because it is cryptographically signed by the KDC. As long as the ticket is valid and unexpired, it can be presented directly to the service.

**This is where in-memory ticket transfer concepts emerge**.

Pass-the-Ticket does not involve passwords or NTLM hashes. Instead, it relies on the reuse of an already-issued Kerberos service ticket. The ticket itself becomes the credential. If an entity gains access to that ticket while it is resident in LSASS memory, and if it can be placed into another logon session, then authentication to the target service can occur without performing the original AS-REQ or TGS-REQ exchanges again.

Conceptually, the flow changes from:

AS-REQ → AS-REP

TGS-REQ → TGS-REP

Use ticket

to simply: Use existing ticket

From a structural perspective inside LSASS, a service ticket is stored under the logon session associated with a specific LUID. If that ticket is somehow transferred into another session, the receiving session can present it as if it were legitimately obtained. The service does not know the difference, because it only verifies the ticket’s cryptographic validity and target service name.

![](https://cloudmate-test.s3.us-east-1.amazonaws.com/uploads/covers/6995899a1a3e7d78226cd5f9/070ccdd5-8181-49dc-92eb-b21505ad5f89.png)

Consider a simplified scenario. A machine is domain-joined. Two users are logged in: Jen and Dave. Dave has already accessed a sensitive file share and therefore has a valid CIFS service ticket cached inside his LSASS logon session. Jen does not.

If an entity gains administrative control of the machine, it now has the capability to interact with LSASS at a privileged level. At this point, the question becomes: what does Dave have access to? If Dave is a domain administrator, reuse of his service tickets may allow authentication to highly privileged services. Even if Dave is not a domain admin, he may have access to resources that contain sensitive material — backups, configuration files, scripts, or service account credentials — that can later be leveraged for escalation.

The critical idea here is that the value of a Kerberos ticket is not inherent in the ticket itself. Its value is determined entirely by the privileges of the identity to which it belongs.

Modern research has shown that ticket acquisition can occur through different approaches. One approach involves directly reading LSASS memory, which requires high privilege and is heavily monitored by modern EDR solutions. Another approach interacts with Windows authentication interfaces and LSA mechanisms in ways that avoid raw memory scraping. From a detection standpoint, these approaches differ significantly in telemetry footprint.

This evolution is important. Older techniques focused on dumping LSASS and extracting all credentials at once. Modern stealth-oriented techniques attempt to minimize direct memory access and instead blend into legitimate Kerberos behavior patterns. When this happens, detection becomes less about spotting memory access and more about identifying anomalous ticket usage patterns across the network.

**From a defensive perspective**, Pass-the-Ticket is not about breaking Kerberos. It is about abusing trust in already-issued credentials. Detecting it therefore requires visibility into ticket issuance events, unusual service access patterns, cross-host ticket reuse, and logon session inconsistencies.

**The takeaway is this: LSASS does not just store tickets — it enables the reuse of tickets as long as they remain valid. That architectural reality is what makes Kerberos both powerful and, when misused, dangerous.**

[#windows](https://zero-layer.hashnode.dev/tag/windows) [#cybersecurity](https://zero-layer.hashnode.dev/tag/cybersecurity) [#lsass](https://zero-layer.hashnode.dev/tag/lsass) [#kerberos](https://zero-layer.hashnode.dev/tag/kerberos) [#redteaming](https://zero-layer.hashnode.dev/tag/redteaming) [#blueteam](https://zero-layer.hashnode.dev/tag/blueteam) [#edr](https://zero-layer.hashnode.dev/tag/edr) [#active-directory](https://zero-layer.hashnode.dev/tag/active-directory) [#windowsinternals](https://zero-layer.hashnode.dev/tag/windowsinternals)

280 views

Contents