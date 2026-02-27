# https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission

Table of contents Exit editor mode

Ask LearnAsk LearnFocus mode

Table of contents[Read in English](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission)Add to CollectionsAdd to plan[Edit](https://github.com/MicrosoftDocs/defender-docs/blob/public/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission.md)

* * *

#### Share via

[Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fcloud-protection-microsoft-antivirus-sample-submission%3FWT.mc_id%3Dfacebook) [x.com](https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fcloud-protection-microsoft-antivirus-sample-submission%3FWT.mc_id%3Dtwitter&tw_p=tweetbutton&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fcloud-protection-microsoft-antivirus-sample-submission%3FWT.mc_id%3Dtwitter) [LinkedIn](https://www.linkedin.com/feed/?shareActive=true&text=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fcloud-protection-microsoft-antivirus-sample-submission%3FWT.mc_id%3Dlinkedin) [Email](mailto:?subject=%5BShared%20Article%5D%20Cloud%20protection%20and%20sample%20submission%20at%20Microsoft%20Defender%20Antivirus%20-%20Microsoft%20Defender%20for%20Endpoint%20%7C%20Microsoft%20Learn&body=%0A%0D%0Ahttps%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fdefender-endpoint%2Fcloud-protection-microsoft-antivirus-sample-submission%3FWT.mc_id%3Demail)

* * *

Copy MarkdownPrint

* * *

Note

Access to this page requires authorization. You can try [signing in](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission#) or changing directories.


Access to this page requires authorization. You can try changing directories.


# Cloud protection and sample submission at Microsoft Defender Antivirus

- Applies to: Microsoft Defender for Endpoint Plan 1, Microsoft Defender for Endpoint Plan 2

Feedback

Summarize this article for me


Microsoft Defender Antivirus uses many intelligent mechanisms for detecting malware. One of the most powerful capabilities is the ability to apply the power of the cloud to detect malware and perform rapid analysis. Cloud protection and automatic sample submission work together with Microsoft Defender Antivirus to help protect against new and emerging threats.

If a suspicious or malicious file is detected, a sample is sent to the cloud service for analysis while Microsoft Defender Antivirus blocks the file. As soon as a determination is made, which happens quickly, the file is either released or blocked by Microsoft Defender Antivirus.

This article provides an overview of cloud protection and automatic sample submission at Microsoft Defender Antivirus. To learn more about cloud protection, see [Cloud protection and Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-defender-antivirus).

[Section titled: Prerequisites](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission#prerequisites)

## Prerequisites

[Section titled: Supported operating systems](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission#supported-operating-systems)

### Supported operating systems

- Windows
- macOS
- Linux
- Windows Server

[Section titled: How cloud protection and sample submission work together](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission#how-cloud-protection-and-sample-submission-work-together)

## How cloud protection and sample submission work together

To understand how cloud protection works together with sample submission, it can be helpful to understand how Defender for Endpoint protects against threats. The Microsoft Intelligent Security Graph monitors threat data from a vast network of sensors. Microsoft layers cloud-based machine-learning models that can assess files based on signals from the client and the vast network of sensors and data in the Intelligent Security Graph. This approach gives Defender for Endpoint the ability to block many never-before-seen threats.

The following image depicts the flow of cloud protection and sample submission with Microsoft Defender Antivirus:

[![Cloud-delivered protection flow](https://learn.microsoft.com/en-us/defender-endpoint/media/cloud-protection-flow.png)](https://learn.microsoft.com/en-us/defender-endpoint/media/cloud-protection-flow.png#lightbox)

Microsoft Defender Antivirus and cloud protection automatically block most new, never-before-seen threats at first sight by using the following methods:

1. Lightweight client-based machine-learning models, blocking new and unknown malware.

2. Local behavioral analysis, stopping file-based and file-less attacks.

3. High-precision antivirus, detecting common malware through generic and heuristic techniques.

4. Advanced cloud-based protection is provided for cases when Microsoft Defender Antivirus running on the endpoint needs more intelligence to verify the intent of a suspicious file.

1. In the event Microsoft Defender Antivirus can't make a clear determination, file metadata is sent to the cloud protection service. Often within milliseconds, the cloud protection service can determine based on the metadata as to whether the file is malicious or not a threat.

      - The cloud query of file metadata can be a result of behavior, mark of the web, or other characteristics where a clear verdict isn't determined.
      - A small metadata payload is sent, with the goal of reaching a verdict of malware or not a threat. The metadata doesn't include personal data, such as personally identifiable information (PII). Information such as filenames, are hashed.
      - Can be synchronous or asynchronous. For synchronous, the file doesn't open until the cloud renders a verdict. For asynchronous, the file opens while cloud protection performs its analysis.
      - Metadata can include PE attributes, static file attributes, dynamic and contextual attributes, and more (see [Examples of metadata sent to the cloud protection service](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission#examples-of-metadata-sent-to-the-cloud-protection-service)).
2. After examining the metadata, if Microsoft Defender Antivirus cloud protection can't reach a conclusive verdict, it can request a sample of the file for further inspection. This request honors the setting configuration for sample submission, as described in the following table:

      Expand table




      | Setting | Description |
      | --- | --- |
      | **Send safe samples automatically** | \- Safe samples are samples considered to not commonly contain PII data. Examples include `.bat`, `.scr`, `.dll`, and `.exe`. <br>\- If file is likely to contain PII, the user gets a request to allow file sample submission.<br>\- This option is the default configuration on Windows, macOS, and Linux. |
      | **Always Prompt** | \- If configured, the user is always prompted for consent before file submission<br>\- This setting isn't available in macOS and Linux cloud protection |
      | **Send all samples automatically** | \- If configured, all samples are sent automatically<br>\- If you would like sample submission to include macros embedded in Word docs, you must choose **Send all samples automatically**<br>\- "Send all samples automatically" is the equivalent to the "Enable" setting in macOS policy |
      | **Do not send** | \- Prevents "block at first sight" based on file sample analysis<br>\- "Don't send" is the equivalent to the "Disabled" setting in macOS policy and "None" setting in Linux policy.<br>\- Metadata is sent for detections even when sample submission is disabled |

3. After files are submitted to cloud protection, the submitted files can be **scanned**, **detonated**, and processed through **big data analysis** **machine-learning** models to reach a verdict. Turning off cloud-delivered protection limits analysis to only what the client can provide through local machine-learning models, and similar functions.

Important

[Block at first sight (BAFS)](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus) provides detonation and analysis to determine whether a file or process is safe. BAFS can delay the opening of a file momentarily until a verdict is reached. If you disable sample submission, BAFS is also disabled, and file analysis is limited to metadata only. We recommend keeping sample submission and BAFS enabled. To learn more, see [What is "block at first sight"?](https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus#what-is-block-at-first-sight)

[Section titled: Cloud protection levels](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission#cloud-protection-levels)

## Cloud protection levels

Cloud protection is enabled by default at Microsoft Defender Antivirus. We recommend that you keep cloud protection enabled, although you can configure the protection level for your organization. See [Specify the cloud-delivered protection level for Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/specify-cloud-protection-level-microsoft-defender-antivirus).

[Section titled: Sample submission settings](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission#sample-submission-settings)

## Sample submission settings

In addition to configuring your cloud protection level, you can configure your sample submission settings. You can choose from several options:

- **Send safe samples automatically** (the default behavior)
- **Send all samples automatically**
- **Do not send samples**

Tip

Using the `Send all samples automatically` option provides for better security, because phishing attacks are used for a high amount of [initial access attacks](https://attack.mitre.org/tactics/TA0001/).
For information about configuration options using Intune, Configuration Manager, Group Policy, or PowerShell, see [Turn on cloud protection at Microsoft Defender Antivirus](https://learn.microsoft.com/en-us/defender-endpoint/enable-cloud-protection-microsoft-defender-antivirus).

[Section titled: Examples of metadata sent to the cloud protection service](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission#examples-of-metadata-sent-to-the-cloud-protection-service)

## Examples of metadata sent to the cloud protection service

[![The examples of metadata sent to cloud protection in the Microsoft Defender Antivirus portal](https://learn.microsoft.com/en-us/defender-endpoint/media/cloud-protection-metadata-sample.png)](https://learn.microsoft.com/en-us/defender-endpoint/media/cloud-protection-metadata-sample.png#lightbox)

The following table lists examples of metadata sent for analysis by cloud protection:

Expand table

| Type | Attribute |
| --- | --- |
| Machine attributes | `OS version`<br>`Processor`<br>`Security settings` |
| Dynamic and contextual attributes | **Process and installation**<br>`ProcessName`<br>`ParentProcess`<br>`TriggeringSignature`<br>`TriggeringFile`<br>`Download IP and url`<br>`HashedFullPath`<br>`Vpath`<br>`RealPath`<br>`Parent/child relationships`<br>**Behavioral**<br>`Connection IPs`<br>`System changes`<br>`API calls`<br>`Process injection`<br>**Locale**<br>`Locale setting`<br>`Geographical location` |
| Static file attributes | **Partial and full hashes**<br>`ClusterHash`<br>`Crc16`<br>`Ctph`<br>`ExtendedKcrcs`<br>`ImpHash`<br>`Kcrc3n`<br>`Lshash`<br>`LsHashs`<br>`PartialCrc1`<br>`PartialCrc2`<br>`PartialCrc3`<br>`Sha1`<br>`Sha256`<br>**File properties**<br>`FileName`<br>`FileSize`<br>**Signer information**<br>`AuthentiCodeHash`<br>`Issuer`<br>`IssuerHash`<br>`Publisher`<br>`Signer`<br>`SignerHash` |

[Section titled: Samples are treated as customer data](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission#samples-are-treated-as-customer-data)

## Samples are treated as customer data

If you're wondering what happens with sample submissions, Defender for Endpoint treats all file samples as customer data. Microsoft honors both the geographical and data retention choices your organization selected when onboarding to Defender for Endpoint.

In addition, Defender for Endpoint received multiple compliance certifications, demonstrating continued adherence to a sophisticated set of compliance controls:

- ISO 27001
- ISO 27018
- SOC I, II, III
- PCI

For more information, see the following resources:

- [Azure Compliance Offerings](https://learn.microsoft.com/en-us/azure/storage/common/storage-compliance-offerings)
- [Service Trust Portal](https://servicetrust.microsoft.com/)
- [Microsoft Defender for Endpoint data storage and privacy](https://learn.microsoft.com/en-us/defender-endpoint/data-storage-privacy)

[Section titled: Other file sample submission scenarios](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission#other-file-sample-submission-scenarios)

## Other file sample submission scenarios

There are two more scenarios where Defender for Endpoint might request a file sample that isn't related to the cloud protection at Microsoft Defender Antivirus. These scenarios are described in the following table:

Expand table

| Scenario | Description |
| --- | --- |
| Manual file sample collection in the Microsoft Defender portal | When onboarding devices to Defender for Endpoint, you can configure settings for [endpoint detection and response (EDR)](https://learn.microsoft.com/en-us/defender-endpoint/overview-endpoint-detection-response). For example, there's a setting to enable sample collections from the device, which can easily be confused with the sample submission settings described in this article. <br>The EDR setting controls file sample collection from devices when requested through the Microsoft Defender portal, and is subject to the roles and permissions already established. This setting can allow or block file collection from the endpoint for features such as deep analysis in the Microsoft Defender portal. If this setting isn't configured, the default is to enable sample collection. <br>Learn about Defender for Endpoint configuration settings, see [Onboard Windows and Mac client devices to Microsoft Defender for Endpoint](https://learn.microsoft.com/en-us/defender-endpoint/onboard-client) |
| Automated investigation and response content analysis | When [automated investigations](https://learn.microsoft.com/en-us/defender-endpoint/automated-investigations) are running on devices (when configured to run automatically in response to an alert or manually run), files that are identified as suspicious can be collected from the endpoints for further inspection. If necessary, the file content analysis feature for automated investigations can be disabled in the Microsoft Defender portal. <br> The file extension names can also be modified to add or remove extensions for other file types that are automatically submitted during an automated investigation. <br> To learn more, see [Manage automation file uploads](https://learn.microsoft.com/en-us/defender-endpoint/manage-automation-file-uploads). |

[Section titled: See also](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission#see-also)

## See also

- [Next-generation protection overview](https://learn.microsoft.com/en-us/defender-endpoint/next-generation-protection)
- [Microsoft Defender for Endpoint on Linux](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint-linux)
- [Microsoft Defender for Endpoint on Mac](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint-mac)
- [Microsoft Defender for Endpoint - Mobile Threat Defense](https://learn.microsoft.com/en-us/defender-endpoint/mtd)
- [Configure remediation for Microsoft Defender Antivirus detections](https://learn.microsoft.com/en-us/defender-endpoint/configure-remediation-microsoft-defender-antivirus)

* * *

## Feedback

Was this page helpful?


YesNoNo

Need help with this topic?


Want to try using Ask Learn to clarify or guide you through this topic?


Ask LearnAsk Learn

Suggest a fix?

* * *

## Additional resources

Training


Module


[Set up Microsoft Defender for Cloud - Training](https://learn.microsoft.com/en-us/training/modules/set-up-microsoft-defender-cloud/?source=recommendations)

Discover how to leverage Microsoft Defender for Cloud through the Azure portal to ensure the security of your Azure services and workloads, offering continuous threat detection and prevention.


Certification


[Microsoft Certified: Security Operations Analyst Associate - Certifications](https://learn.microsoft.com/en-us/credentials/certifications/security-operations-analyst/?source=recommendations)

Investigate, search for, and mitigate threats using Microsoft Sentinel, Microsoft Defender for Cloud, and Microsoft 365 Defender.


* * *

- Last updated on 10/20/2025

Ask Learn is an AI assistant that can answer questions, clarify concepts, and define terms using trusted Microsoft documentation.

Please sign in to use Ask Learn.

[Sign in](https://learn.microsoft.com/en-us/defender-endpoint/cloud-protection-microsoft-antivirus-sample-submission#)