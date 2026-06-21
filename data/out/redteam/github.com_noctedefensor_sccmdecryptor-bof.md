# https://github.com/NocteDefensor/SCCMDecryptor-BOF

[Skip to content](https://github.com/NocteDefensor/SCCMDecryptor-BOF#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/NocteDefensor/SCCMDecryptor-BOF) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/NocteDefensor/SCCMDecryptor-BOF) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/NocteDefensor/SCCMDecryptor-BOF) to refresh your session.Dismiss alert

{{ message }}

[NocteDefensor](https://github.com/NocteDefensor)/ **[SCCMDecryptor-BOF](https://github.com/NocteDefensor/SCCMDecryptor-BOF)** Public

- [Notifications](https://github.com/login?return_to=%2FNocteDefensor%2FSCCMDecryptor-BOF) You must be signed in to change notification settings
- [Fork\\
4](https://github.com/login?return_to=%2FNocteDefensor%2FSCCMDecryptor-BOF)
- [Star\\
57](https://github.com/login?return_to=%2FNocteDefensor%2FSCCMDecryptor-BOF)


main

[**1** Branch](https://github.com/NocteDefensor/SCCMDecryptor-BOF/branches) [**0** Tags](https://github.com/NocteDefensor/SCCMDecryptor-BOF/tags)

[Go to Branches page](https://github.com/NocteDefensor/SCCMDecryptor-BOF/branches)[Go to Tags page](https://github.com/NocteDefensor/SCCMDecryptor-BOF/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![NocteDefensor](https://avatars.githubusercontent.com/u/103839834?v=4&size=40)](https://github.com/NocteDefensor)[NocteDefensor](https://github.com/NocteDefensor/SCCMDecryptor-BOF/commits?author=NocteDefensor)<br>[Update README.md](https://github.com/NocteDefensor/SCCMDecryptor-BOF/commit/6852596531a7035a18bef555d7cf5b49932031d2)<br>last yearJun 28, 2025<br>[6852596](https://github.com/NocteDefensor/SCCMDecryptor-BOF/commit/6852596531a7035a18bef555d7cf5b49932031d2) · last yearJun 28, 2025<br>## History<br>[16 Commits](https://github.com/NocteDefensor/SCCMDecryptor-BOF/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/NocteDefensor/SCCMDecryptor-BOF/commits/main/) 16 Commits |
| [README.md](https://github.com/NocteDefensor/SCCMDecryptor-BOF/blob/main/README.md "README.md") | [README.md](https://github.com/NocteDefensor/SCCMDecryptor-BOF/blob/main/README.md "README.md") | [Update README.md](https://github.com/NocteDefensor/SCCMDecryptor-BOF/commit/6852596531a7035a18bef555d7cf5b49932031d2 "Update README.md") | last yearJun 28, 2025 |
| [SCCMDecryptor.c](https://github.com/NocteDefensor/SCCMDecryptor-BOF/blob/main/SCCMDecryptor.c "SCCMDecryptor.c") | [SCCMDecryptor.c](https://github.com/NocteDefensor/SCCMDecryptor-BOF/blob/main/SCCMDecryptor.c "SCCMDecryptor.c") | [Create SCCMDecryptor.c](https://github.com/NocteDefensor/SCCMDecryptor-BOF/commit/d6eb3e71ef382dd8afca50ed1bb62b89a64c6ef6 "Create SCCMDecryptor.c") | last yearFeb 15, 2025 |
| [beacon.h](https://github.com/NocteDefensor/SCCMDecryptor-BOF/blob/main/beacon.h "beacon.h") | [beacon.h](https://github.com/NocteDefensor/SCCMDecryptor-BOF/blob/main/beacon.h "beacon.h") | [Create beacon.h](https://github.com/NocteDefensor/SCCMDecryptor-BOF/commit/d2c137cd394714aa357fdd2f3a624357f1789faf "Create beacon.h") | last yearFeb 15, 2025 |
| [makefile](https://github.com/NocteDefensor/SCCMDecryptor-BOF/blob/main/makefile "makefile") | [makefile](https://github.com/NocteDefensor/SCCMDecryptor-BOF/blob/main/makefile "makefile") | [Create makefile](https://github.com/NocteDefensor/SCCMDecryptor-BOF/commit/3ceb87247edd21acc85bbd929e1d699c5cfc9dde "Create makefile") | last yearFeb 15, 2025 |
| [sccmdecrypt.cna](https://github.com/NocteDefensor/SCCMDecryptor-BOF/blob/main/sccmdecrypt.cna "sccmdecrypt.cna") | [sccmdecrypt.cna](https://github.com/NocteDefensor/SCCMDecryptor-BOF/blob/main/sccmdecrypt.cna "sccmdecrypt.cna") | [Update sccmdecrypt.cna](https://github.com/NocteDefensor/SCCMDecryptor-BOF/commit/4affc32e248639c12df21a750bedbf389bef6b30 "Update sccmdecrypt.cna") | last yearFeb 15, 2025 |
| View all files |

## Repository files navigation

# SCCMDecryptor BOF

[Permalink: SCCMDecryptor BOF](https://github.com/NocteDefensor/SCCMDecryptor-BOF#sccmdecryptor-bof)

A Beacon Object File (BOF) implementation of Adam Chester's [@xpn's](https://x.com/_xpn_) [c# tool](https://gist.github.com/xpn/5f497d2725a041922c427c3aaa3b37d1) for decrypting SCCM encrypted password blobs retrieved from the site DB. This tool needs to be run on an SCCM server containing the "Microsoft Systems Management Server" CSP.
![image](https://private-user-images.githubusercontent.com/103839834/413583716-a39dbf72-a8f7-4428-b337-6c5f7bcf41e2.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODIwNDY2NTUsIm5iZiI6MTc4MjA0NjM1NSwicGF0aCI6Ii8xMDM4Mzk4MzQvNDEzNTgzNzE2LWEzOWRiZjcyLWE4ZjctNDQyOC1iMzM3LTZjNWY3YmNmNDFlMi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNjIxJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDYyMVQxMjUyMzVaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1kYjBjYzg5Y2E3ZGZkZmZkY2RlNGJkZjRlMTZlOTI3N2NjOTY1MGRhMWU2MzJhMjIzNTVlNGQ3ZTBmN2VkY2IzJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.m7oNvqvxdH539q3bHK_SHTB6jCSF0rTt-sAep7hqM6M)

## Building

[Permalink: Building](https://github.com/NocteDefensor/SCCMDecryptor-BOF#building)

Requirements:

- MinGW-w64 (for cross-compilation)
- Make

To build both x64 and x86 versions:

```
make
```

## Usage

[Permalink: Usage](https://github.com/NocteDefensor/SCCMDecryptor-BOF#usage)

2. In a beacon running in local administrator context on an SCCM server, use the command:

```
beacon> sccmdecrypt <hex_string>
```

where hex\_string is the encrypted credential blob retrieved from the SCCM database.
Example:

![image](https://private-user-images.githubusercontent.com/103839834/414550500-ecb681a8-04d5-4f7e-b2d2-84ac321a2002.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODIwNDY2NTUsIm5iZiI6MTc4MjA0NjM1NSwicGF0aCI6Ii8xMDM4Mzk4MzQvNDE0NTUwNTAwLWVjYjY4MWE4LTA0ZDUtNGY3ZS1iMmQyLTg0YWMzMjFhMjAwMi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNjIxJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDYyMVQxMjUyMzVaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0xZDcwNDQwNDYyMmU5NGYwMjNhYTYyNWNmZjUxODQxNmRlMTBjMDg2NzBhNDc3ZDE1ZGFkYjFmYTRlM2EwMzljJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.t8hjwUm4e9bjyUcEuPEQOdkQDhrFiiLnldj23MZMF5I)

## Credits

[Permalink: Credits](https://github.com/NocteDefensor/SCCMDecryptor-BOF#credits)

This is a BOF implementation of the original C# SCCM decryptor tool created by [@ _xpn_](https://gist.github.com/xpn/5f497d2725a041922c427c3aaa3b37d1).

- [Misconfiguration Manager Cred-5](https://github.com/subat0mik/Misconfiguration-Manager/blob/main/attack-techniques/CRED/CRED-5/cred-5_description.md)

## About

No description, website, or topics provided.


### Resources

[Readme](https://github.com/NocteDefensor/SCCMDecryptor-BOF#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/NocteDefensor/SCCMDecryptor-BOF).

[Activity](https://github.com/NocteDefensor/SCCMDecryptor-BOF/activity)

### Stars

[**57**\\
stars](https://github.com/NocteDefensor/SCCMDecryptor-BOF/stargazers)

### Watchers

[**1**\\
watching](https://github.com/NocteDefensor/SCCMDecryptor-BOF/watchers)

### Forks

[**4**\\
forks](https://github.com/NocteDefensor/SCCMDecryptor-BOF/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2FNocteDefensor%2FSCCMDecryptor-BOF&report=NocteDefensor+%28user%29)

## [Releases](https://github.com/NocteDefensor/SCCMDecryptor-BOF/releases)

No releases published

## [Packages\  0](https://github.com/users/NocteDefensor/packages?repo_name=SCCMDecryptor-BOF)

No packages published

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/NocteDefensor/SCCMDecryptor-BOF).

## [Contributors\  1](https://github.com/NocteDefensor/SCCMDecryptor-BOF/graphs/contributors)

- [![@NocteDefensor](https://avatars.githubusercontent.com/u/103839834?s=64&v=4)](https://github.com/NocteDefensor)[**NocteDefensor**](https://github.com/NocteDefensor)

## Languages

- [C96.9%](https://github.com/NocteDefensor/SCCMDecryptor-BOF/search?l=c)
- [Makefile3.1%](https://github.com/NocteDefensor/SCCMDecryptor-BOF/search?l=makefile)

You can’t perform that action at this time.