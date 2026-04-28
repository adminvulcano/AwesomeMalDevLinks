# https://github.com/WKL-Sec/slack-udc2

[Skip to content](https://github.com/WKL-Sec/slack-udc2#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/WKL-Sec/slack-udc2) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/WKL-Sec/slack-udc2) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/WKL-Sec/slack-udc2) to refresh your session.Dismiss alert

{{ message }}

[WKL-Sec](https://github.com/WKL-Sec)/ **[slack-udc2](https://github.com/WKL-Sec/slack-udc2)** Public

- [Notifications](https://github.com/login?return_to=%2FWKL-Sec%2Fslack-udc2) You must be signed in to change notification settings
- [Fork\\
9](https://github.com/login?return_to=%2FWKL-Sec%2Fslack-udc2)
- [Star\\
69](https://github.com/login?return_to=%2FWKL-Sec%2Fslack-udc2)


main

[**1** Branch](https://github.com/WKL-Sec/slack-udc2/branches) [**0** Tags](https://github.com/WKL-Sec/slack-udc2/tags)

[Go to Branches page](https://github.com/WKL-Sec/slack-udc2/branches)[Go to Tags page](https://github.com/WKL-Sec/slack-udc2/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![WKL-Sec](https://avatars.githubusercontent.com/u/97109724?v=4&size=40)](https://github.com/WKL-Sec)[WKL-Sec](https://github.com/WKL-Sec/slack-udc2/commits?author=WKL-Sec)<br>[Update README.md](https://github.com/WKL-Sec/slack-udc2/commit/05f7fc278c1587aa171ae66b3349d6b39a1be166)<br>3 months agoJan 5, 2026<br>[05f7fc2](https://github.com/WKL-Sec/slack-udc2/commit/05f7fc278c1587aa171ae66b3349d6b39a1be166) · 3 months agoJan 5, 2026<br>## History<br>[3 Commits](https://github.com/WKL-Sec/slack-udc2/commits/main/) <br>Open commit details<br>[View commit history for this file.](https://github.com/WKL-Sec/slack-udc2/commits/main/) 3 Commits |
| [client](https://github.com/WKL-Sec/slack-udc2/tree/main/client "client") | [client](https://github.com/WKL-Sec/slack-udc2/tree/main/client "client") | [File upload](https://github.com/WKL-Sec/slack-udc2/commit/86261d8de5b6db8ea4046514a5fc1e4f61f3e62c "File upload") | 3 months agoJan 5, 2026 |
| [server](https://github.com/WKL-Sec/slack-udc2/tree/main/server "server") | [server](https://github.com/WKL-Sec/slack-udc2/tree/main/server "server") | [File upload](https://github.com/WKL-Sec/slack-udc2/commit/86261d8de5b6db8ea4046514a5fc1e4f61f3e62c "File upload") | 3 months agoJan 5, 2026 |
| [LICENSE](https://github.com/WKL-Sec/slack-udc2/blob/main/LICENSE "LICENSE") | [LICENSE](https://github.com/WKL-Sec/slack-udc2/blob/main/LICENSE "LICENSE") | [Initial commit](https://github.com/WKL-Sec/slack-udc2/commit/2e66a497e5b238053bcbbf1e1d284ed52d7454b0 "Initial commit") | 3 months agoJan 5, 2026 |
| [README.md](https://github.com/WKL-Sec/slack-udc2/blob/main/README.md "README.md") | [README.md](https://github.com/WKL-Sec/slack-udc2/blob/main/README.md "README.md") | [Update README.md](https://github.com/WKL-Sec/slack-udc2/commit/05f7fc278c1587aa171ae66b3349d6b39a1be166 "Update README.md") | 3 months agoJan 5, 2026 |
| View all files |

## Repository files navigation

# Slack UDC2 BOF

[Permalink: Slack UDC2 BOF](https://github.com/WKL-Sec/slack-udc2#slack-udc2-bof)

A Beacon Object File (BOF) implementation that provides an UDC2 channel that uses Slack API requests.

## Overview

[Permalink: Overview](https://github.com/WKL-Sec/slack-udc2#overview)

The Slack UDC2 BOF acts as a communication proxy that encapsulates Beacon traffic within Slack API requests.

![image-6](https://private-user-images.githubusercontent.com/97109724/532110066-99410863-bcbc-4d0e-b6e3-15b54c6ff7c6.jpg?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzcyMDAzOTEsIm5iZiI6MTc3NzIwMDA5MSwicGF0aCI6Ii85NzEwOTcyNC81MzIxMTAwNjYtOTk0MTA4NjMtYmNiYy00ZDBlLWI2ZTMtMTViNTRjNmZmN2M2LmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA0MjYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNDI2VDEwNDEzMVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWZlODQzY2U3ZWI4ZTAxODcwNDJlZDg4ZTEyNTdmNzU0MWFmMjE2OGYxMDUwYjMyMGM3NzZiYmIxNGZkZWRhYWYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRmpwZWcifQ.Hp-cMV7ee_bTBog6lwdi6TLsO9QPldoobCqGcLv0ITY)

## Features

[Permalink: Features](https://github.com/WKL-Sec/slack-udc2#features)

### BOF Compliance

[Permalink: BOF Compliance](https://github.com/WKL-Sec/slack-udc2#bof-compliance)

- **No MSVCRT Dependencies**: Uses only Windows API functions
- **Minimal Footprint**: Optimized for in-memory execution

## Slack UDC2 Release Example Quick Start Guide

[Permalink: Slack UDC2 Release Example Quick Start Guide](https://github.com/WKL-Sec/slack-udc2#slack-udc2-release-example-quick-start-guide)

To quickly get the Slack UDC2 Release BOF built and usable within Cobalt Strike, follow the instructions below. Note that you should have the `Release` solution configuration selected for this.

1. In the slack\_udc2\_bof.cpp file, find the following line:

```
        gUdc2State.botToken = "xoxb-TOKEN-HERE"; // SET THIS TO YOUR BOT TOKEN
        gUdc2State.clientchannelId = "CLIENT-CHANNEL-TOKEN-HERE"; // SET THIS TO YOUR SLACK CLIENT CHANNEL ID
        gUdc2State.serverchannelId = "SERVER-CHANNEL-TOKEN-HERE"; // SET THIS TO YOUR SLACK SERVER CHANNEL ID
```

2. Change the values to your configurations.

3. Make sure the "Release" configuration is selected in Visual Studio and choose the architecture you wish to build the BOF for (x64 or x86)

4. From the Build menu in Visual Studio, click Build Solution

5. Once the BOF has been successfully built, open the Cobalt Strike client and open the listeners page. Create a new UDC2 listener. Give it a name like udc2-slack-x64 or udc2-slack-x86 and choose a port for the UDC2 listener to listen on. For the UDC2 BOF field, click on the open-file dialog option and select the Slack UDC2 BOF that you just built in the previous step. Ensure that the "Debug only" checkbox is **NOT** checked. If you want to apply guard rails, apply them, and finally click Save.

6. For specific usage instructions of the Slack UDC2 server python script, refer to the documentation in the server\\README.md file. In the interim, run the python script with the following options: `python3 slack_udc2_server.py --ts-addr YOUR_TS_UDC2_LISTENER_IP --ts-port YOUR_TS_UDC2_LISTENER_PORT`

7. Before running the server, make sure to replace the following values as well (line 24-26):


```
    slack_token: str = 'xoxb-TOKEN-HERE'
    slack_client_channel: str = 'REPLACE-TOKEN'
    slack_server_channel: str = 'REPLACE-TOKEN'
```

7. From the Cobalt Strike client, export a payload as you would normally, but choose the new UDC2 listener you created in step 5.
8. Your payload is now ready to execute with the Slack UDC2 BOF stomped into it. Run the payload and you should see Slack API requests being sent to your python UDC2 server which will extract the Beacon frame data from them and forward it on to the UDC2 listener on the Team Server.
9. You should now see a new Beacon registered in the Cobalt Strike client.

## Architecture

[Permalink: Architecture](https://github.com/WKL-Sec/slack-udc2#architecture)

### Core Components

[Permalink: Core Components](https://github.com/WKL-Sec/slack-udc2#core-components)

#### Global State Management

[Permalink: Global State Management](https://github.com/WKL-Sec/slack-udc2#global-state-management)

```
typedef struct {
    BOOL    initialized;
    UINT32  beaconId; // not used
    const char* botToken;
    const char* clientchannelId;
    const char* serverchannelId;
} UDC2_STATE;
```

## API Reference

[Permalink: API Reference](https://github.com/WKL-Sec/slack-udc2#api-reference)

### Core Functions

[Permalink: Core Functions](https://github.com/WKL-Sec/slack-udc2#core-functions)

#### `int udc2Proxy(const char* sendBuf, int sendBufLen, char* recvBuf, int recvBufMaxLen)`

[Permalink: int udc2Proxy(const char* sendBuf, int sendBufLen, char* recvBuf, int recvBufMaxLen)](https://github.com/WKL-Sec/slack-udc2#int-udc2proxyconst-char-sendbuf-int-sendbuflen-char-recvbuf-int-recvbufmaxlen)

Main proxy function for relaying Beacon traffic. This is where the Slack communication happens.

**Parameters:**

- `sendBuf`: Points to Beacon frame data that needs to be sent out
- `sendBufLen`: The total length of the frame data
- `recvBuf`: Points to Beacon memory that you should copy response frame data to
- `recvBufMaxLen`: The max size of the recv buffer

**Returns:** Number of bytes received on success, negative error code on failure

#### `void udc2Close()`

[Permalink: void udc2Close()](https://github.com/WKL-Sec/slack-udc2#void-udc2close)

Cleanup function for session termination.

#### `int sendSlackPackets(sendBuf, sendBufLen);`

[Permalink: int sendSlackPackets(sendBuf, sendBufLen);](https://github.com/WKL-Sec/slack-udc2#int-sendslackpacketssendbuf-sendbuflen)

Send data via Slack so the server will relay it to Teamserver.

**Parameters:**

- `buffer`: Data buffer to send
- `length`: Length of data

## Error Handling

[Permalink: Error Handling](https://github.com/WKL-Sec/slack-udc2#error-handling)

### Error Codes

[Permalink: Error Codes](https://github.com/WKL-Sec/slack-udc2#error-codes)

```
#define UDC2_SUCCESS                 0   // Operation successful
#define UDC2_ERROR_INVALID_PARAM    -1   // Invalid parameter
#define UDC2_ERROR_MEMORY_ALLOC     -2   // Memory allocation failure
#define UDC2_ERROR_NETWORK          -3   // Network operation failure
#define UDC2_ERROR_TIMEOUT          -4   // Operation timeout
#define UDC2_ERROR_PROTOCOL         -5   // Protocol violation
#define UDC2_ERROR_FRAGMENTATION    -6   // Fragmentation error
```

## Dependencies

[Permalink: Dependencies](https://github.com/WKL-Sec/slack-udc2#dependencies)

### Windows APIs

[Permalink: Windows APIs](https://github.com/WKL-Sec/slack-udc2#windows-apis)

- **KERNEL32.dll**: Memory management (`HeapAlloc`, `HeapFree`, `GetProcessHeap`)
- **WS2\_32.dll**: Network utilities (`inet_addr`)
- **Wininet.dll**: network utilities (`InternetOpenA`, `InternetConnectA`, `HttpOpenRequestA`, `HttpSendRequestA`, `InternetReadFile`, `InternetCloseHandle`)

## Limitations

[Permalink: Limitations](https://github.com/WKL-Sec/slack-udc2#limitations)

This project is intentionally simplified for educational purposes to help others learn how the UDC2 framework operates. As such, it has the following limitations:

- **No Fragmentation Support**: Unlike the original Slack implementation, this BOF does not support fragmented transfers. Slack has a limitation of approximately 40,000 characters per message. Attempting to transfer data exceeding this limit will result in an error or unintentional behavior, which may cause the Beacon to crash.
- **Single Beacon Support**: There is currently no beaconId validation/routing logic implemented in the transport layer. This project supports only one active UDC2 Beacon at a time. Note: While child beacons (SMB/TCP) can be established through the initial Slack-linked beacon, the Slack channel itself cannot distinguish between multiple primary UDC2 beacons.
- **Infrastructure**: Further development is required for use in a full-scale Red Team engagement, specifically data fragmentation, and multi-beacon management.

## References

[Permalink: References](https://github.com/WKL-Sec/slack-udc2#references)

- [ICMP Bof Github](https://github.com/Cobalt-Strike/icmp-udc2)
- [Cobalt Strike Documentation](https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/content/topics/welcome_main.htm)
- [BOF Development Guide](https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/content/topics/beacon-object-files_main.htm)

## Author

[Permalink: Author](https://github.com/WKL-Sec/slack-udc2#author)

Kleiton Kurti ( [@kleiton0x00](https://github.com/kleiton0x00))

## About

Cobalt Strike UDC2 implementation that provides an Slack C2 channel


### Resources

[Readme](https://github.com/WKL-Sec/slack-udc2#readme-ov-file)

### License

[MIT license](https://github.com/WKL-Sec/slack-udc2#MIT-1-ov-file)

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/WKL-Sec/slack-udc2).

[Activity](https://github.com/WKL-Sec/slack-udc2/activity)

### Stars

[**69**\\
stars](https://github.com/WKL-Sec/slack-udc2/stargazers)

### Watchers

[**1**\\
watching](https://github.com/WKL-Sec/slack-udc2/watchers)

### Forks

[**9**\\
forks](https://github.com/WKL-Sec/slack-udc2/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2FWKL-Sec%2Fslack-udc2&report=WKL-Sec+%28user%29)

## [Releases](https://github.com/WKL-Sec/slack-udc2/releases)

No releases published

## [Packages\  0](https://github.com/users/WKL-Sec/packages?repo_name=slack-udc2)

No packages published

## [Contributors\  1](https://github.com/WKL-Sec/slack-udc2/graphs/contributors)

- [![@WKL-Sec](https://avatars.githubusercontent.com/u/97109724?s=64&v=4)](https://github.com/WKL-Sec)[**WKL-Sec** White Knight Labs](https://github.com/WKL-Sec)

## Languages

- [Python69.7%](https://github.com/WKL-Sec/slack-udc2/search?l=python)
- [C++17.0%](https://github.com/WKL-Sec/slack-udc2/search?l=c%2B%2B)
- [C10.8%](https://github.com/WKL-Sec/slack-udc2/search?l=c)
- [Makefile2.5%](https://github.com/WKL-Sec/slack-udc2/search?l=makefile)

You can’t perform that action at this time.