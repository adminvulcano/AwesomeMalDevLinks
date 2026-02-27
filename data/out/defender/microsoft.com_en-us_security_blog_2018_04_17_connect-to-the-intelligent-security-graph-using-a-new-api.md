# https://www.microsoft.com/en-us/security/blog/2018/04/17/connect-to-the-intelligent-security-graph-using-a-new-api/

[Skip to content](https://www.microsoft.com/en-us/security/blog/2018/04/17/connect-to-the-intelligent-security-graph-using-a-new-api/#wp--skip-link--target)

 [Skip to content](https://www.microsoft.com/en-us/security/blog/2018/04/17/connect-to-the-intelligent-security-graph-using-a-new-api/#wp--skip-link--target)

![](https://www.microsoft.com/en-us/security/blog/wp-content/themes/security-blog-2025/dist/images/single-bg.jpg)

![](https://www.microsoft.com/en-us/security/blog/wp-content/themes/security-blog-2025/dist/images/single-bg-dark.jpg)

* * *

## Share

- [Link copied to clipboard!](https://www.microsoft.com/en-us/security/blog/2018/04/17/connect-to-the-intelligent-security-graph-using-a-new-api/)
- [Share on Facebook](https://www.facebook.com/sharer/sharer.php?u=https://www.microsoft.com/en-us/security/blog/2018/04/17/connect-to-the-intelligent-security-graph-using-a-new-api/)
- [Share on X](https://twitter.com/intent/tweet?url=https://www.microsoft.com/en-us/security/blog/2018/04/17/connect-to-the-intelligent-security-graph-using-a-new-api/&text=Connect+to+the+Intelligent+Security+Graph+using+a+new+API)
- [Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https://www.microsoft.com/en-us/security/blog/2018/04/17/connect-to-the-intelligent-security-graph-using-a-new-api/)

## Content types

- [News](https://www.microsoft.com/en-us/security/blog/content-type/news/)

## Topics

- [Incident response](https://www.microsoft.com/en-us/security/blog/topic/incident-response/)
- [Security operations](https://www.microsoft.com/en-us/security/blog/topic/security-operations/)

Most organizations deal with high volumes of security data and have dozens of security solutions in their enterprise, making the task of integrating various products and services daunting and complex. The cost, time, and resources necessary to connect systems, enable correlation of alerts, and provide access to contextual data is extremely high. These challenges hinder the ability for organizations to move quickly when detecting and remediating threats in a world of fast-moving, disruptive attacks.

By connecting security data and systems, we can gain an advantage over today’s adversaries. At Microsoft, our security products are powered by the Intelligent Security Graph which synthesizes massive amounts of threat intelligence and security signals from across Microsoft products, services, and partners using advanced analytics to identify and mitigate cyberthreats. This week at the RSA conference, we announced the public preview of a Security API that empowers customers and partners to build on the Intelligent Security Graph. By connecting security solutions and integrating with existing workflows, alerts and contextual information from multiple solutions can be easily consolidated and correlated to inform threat detection, and actions can be taken to streamline incident response. The unified API will make these connections easier by providing a standard interface and uniform schema to integrate and correlate security alerts from multiple sources, enrich investigations with contextual data, and automate security operations for greater efficiency.

The Security API is part of the Microsoft Graph, which is a unified rest API for integrating data and intelligence from Microsoft products and services. Using Microsoft Graph, developers can rapidly build solutions that authenticate once and use a single API call to access or act on security insights from multiple security solutions. Additional value is uncovered when you explore the other Microsoft Graph entities (Office 365, Azure Active Directory, Intune, and more) to tie business context with your security insights.

This public preview supports API access of Alerts from Azure Security Center and Azure Active Directory Identity Protection with Intune and Azure Information Protection coming soon. We are also announcing support for high volume streaming of alerts to a SIEM through Security API integration with Azure Monitor. This will enable seamless ingestion of alerts from multiple sources directly into a SIEM. Over the coming months, we’ll add many more Microsoft and partner security solutions integrations as data providers. We will also add new capabilities that unlock new security context through _Security Inventory_ and take _Actions_ to automation security operations through the same Security API.

![A data architecture diagram ](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2018/04/Microsoft-Graph-Security-API-1024x516.png)

## Enabling ecosystem partners

The Security API opens up new possibilities for [integration partners](https://www.microsoft.com/en-us/security/association) to build with the Intelligent Security Graph. Partners can not only consume security insights from the Graph but they can allow their alerts, context, and automation to be enabled in the Graph at peer level with integrated Microsoft products. By forming a connected, extended ecosystem of security technologies, Microsoft and partners can deliver better protections for our customers. Some partners have already onboarded to the Security APIs and many other integrations are in progress:

**Anomali** [integrates](http://www.anomali.com/learn/microsoft-isg) with the Security API to correlate alerts from Microsoft Graph with threat intelligence, providing earlier detection and response to cyber threats.

> The Security Graph API allows us to receive not only actionable alert information but allows security analysts to pivot and enrich alerts with asset and user information. – **Colby DeRodeff, Co-founder and Chief Strategy Officer of Anomali**

**Palo Alto Networks** can [enrich alerts](https://researchcenter.paloaltonetworks.com/2018/04/see-graph-security-api-action-rsa-conference-2018/) from Microsoft Graph Security with threat intelligence speeding up detection and prevention of cyberattacks for our shared customers.

> The adoption of public clouds is accelerating, but so is the threat level to the applications and data inside organizations. Today’s announcement of the Microsoft Graph Security API sets the stage for expanding the built-in security features we can offer our joint customers and to help organizations safely embrace the cloud. – **Andy Horwitz, Vice President, Business and Corporate Development, Palo Alto Networks**

**PwC** uses alerts and context from Microsoft Graph in its [Secure Terrain](https://www.pwc.com/us/en/cybersecurity/secure-terrain.html) solution to deliver improved visibility and protection.

> The integration with Secure Terrain offers users a streamlined way to investigate Microsoft Graph alerts in the context of the broader enterprise and perform threat hunting investigations. – **Christopher Morris, Principal at PricewaterhouseCoopers**

## Building intelligent security applications

Customers, managed service providers, and technology partners, can leverage the Security APIs to build and integrate a variety of applications. Some examples include:

- **Custom security dashboards**. Surface rich alerts in your custom Security Operations Center dashboards – streamline alerts and add contextual information about related entities
- **Security operations tools**. Manage alerts in your ticketing, security or IT management system – keep alert status and assignments in sync, automate common tasks
- **Threat protection solutions**. Correlate alerts and contextual information for improved detections, take action on threats – block an IP on firewall or run an AV scan
- **Other applications**. Add security functionality to non-security applications – HR, financial, and healthcare apps

## Get started today:

Join us at the Microsoft booth, N3501 in the north expo hall, at RSA Conference 2018 in San Francisco. You’ll get the chance to speak to experts and see how our partners are using the API.

To learn more and get started today with using the Microsoft Graph Security API, check out the following resources:

- Visit the [Microsoft Secure site](https://aka.ms/graphsecurityapi) to learn more
- Read the Microsoft Graph [documentation](https://aka.ms/graphsecuritydocs)
- Download the sample code in [ASP.Net](https://aka.ms/graphsecurityaspnet) and [Python](https://aka.ms/graphsecuritypython)
- Follow the discussion on [Stack Overflow](https://stackoverflow.com/questions/tagged/microsoft-graph-security)

![Microsoft](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2023/04/microsoft_logo-300x300.png)

## Microsoft Security Team

[See Microsoft Security Team posts](https://www.microsoft.com/en-us/security/blog/author/microsoft-secure-blog-staff/)

## Related posts

- ![Graphic illustrating Microsoft Incident Response.](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2023/06/MS_SecurityExperts_Cyberattacks_Cover-Image-1200x900_Final.jpg)









  - June 29, 2023
  - 3 min read

### [Patch me if you can: Cyberattack Series](https://www.microsoft.com/en-us/security/blog/2023/06/29/patch-me-if-you-can-cyberattack-series/)

The Microsoft Incident Response team takes swift action to help contain a ransomware attack and regain positive administrative control of the customer environment.

- ![Man in sweater inside a secure room who is looking at data and a geographic area displayed on a large monitor which is behind glass walls with reflections.](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2023/06/SEC20_Security_041.jpg)









  - June 26, 2023
  - 7 min read

### [Why endpoint management is key to securing an AI-powered future](https://www.microsoft.com/en-us/security/blog/2023/06/26/why-endpoint-management-is-key-to-securing-an-ai-powered-future/)

With the coming wave of AI, this is precisely the time for organizations to prepare for the future.

- ![Graphic depicting phishing risks and other cybersecurity threats.](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2023/05/1200x800_MSFTInsider_BlogHeader_CyberSignals4.png)









  - May 19, 2023
  - 3 min read

### [Cyber Signals: Shifting tactics fuel surge in business email compromise](https://www.microsoft.com/en-us/security/blog/2023/05/19/cyber-signals-shifting-tactics-fuel-surge-in-business-email-compromise/)

Business email operators seek to exploit the daily sea of email traffic to lure victims into providing financial and other sensitive business information.

![](https://www.microsoft.com/en-us/security/blog/wp-content/themes/security-blog-2025/dist/images/bg-footer.png)

![](https://www.microsoft.com/en-us/security/blog/wp-content/themes/security-blog-2025/dist/images/bg-footer.png)

## Get started with Microsoft Security

Protect your people, data, and infrastructure with AI-powered, end-to-end security from Microsoft.

[Learn how](https://www.microsoft.com/en-us/security?wt.mc_id=AID730391_QSG_BLOG_319247&ocid=AID730391_QSG_BLOG_319247)

![](https://www.microsoft.com/en-us/security/blog/wp-content/themes/security-blog-2025/dist/images/footer-promotional.jpg)

Connect with us on social

- [X](https://twitter.com/msftsecurity)
- [YouTube](https://www.youtube.com/channel/UC4s3tv0Qq_OSUBfR735Jc6A)
- [LinkedIn](https://www.linkedin.com/showcase/microsoft-security/)