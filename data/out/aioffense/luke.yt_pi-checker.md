# https://luke.yt/pi-checker/

[←](https://luke.yt/)

# PI Checker

Prompt Injection Checker - Eight categories of prompt injection tests. Pick a category, run the test levels, and check each response against the vulnerable if criteria on the card. Summarization includes a baseline page - run that first to see what a clean response looks like.

**For research and educational use only. These tests do not guarantee that your AI tool is safe against prompt injection attacks.**

Most test pages are a fictional sushi restaurant called "Evil Sushi". The financial sector demo uses a separate fictional company, Arcturus Capital Holdings - see category 8 below for full context on the financial attack surface.

[Methodology & reference →](https://luke.yt/pi-checker/wiki.html)

## [1\. Summarization Poisoning](https://luke.yt/pi-checker/summarization/)

7 levels + baseline

Feed each "Evil Sushi" page URL to your AI tool and ask it to summarize the page. Each level uses a different technique to hide the injection.

[View tests →](https://luke.yt/pi-checker/summarization/)

## [2\. RAG / Document Poisoning](https://luke.yt/pi-checker/rag/)

3 levels

Feed a poisoned document into your agent's knowledge base or RAG pipeline and ask it a question about the contents.

[View tests →](https://luke.yt/pi-checker/rag/)

## [3\. CLI / Agentic](https://luke.yt/pi-checker/cli/)

2 levels

Feed a poisoned file to an AI coding assistant or agent with file system access and see whether it follows the embedded instructions.

[View tests →](https://luke.yt/pi-checker/cli/)

## [4\. Multi-step / Chained Injection](https://luke.yt/pi-checker/chained/)

2 pages

Page 1 is clean. The payload is on page 2, linked from page 1. Tests whether an injection encountered late in a session can corrupt the agent's entire report.

[View tests →](https://luke.yt/pi-checker/chained/)

## [5\. Fictional / Narrative Injection](https://luke.yt/pi-checker/narrative/)

3 levels

Payloads wrapped in character dialogue or story formatting. Spans text-extraction and raw-HTML pipelines. Tests whether your AI follows instructions framed as fiction or hidden in markup.

[View tests →](https://luke.yt/pi-checker/narrative/)

## [6\. Translation Attacks](https://luke.yt/pi-checker/translation/)

4 languages

Evil Sushi recreated in French, German, Japanese, and Italian. Tests whether injections embedded in foreign-language content survive translation into English.

[View tests →](https://luke.yt/pi-checker/translation/)

## [7\. Jailbreak Attacks](https://luke.yt/pi-checker/jailbreak/)

3 levels

Payloads that attempt to convince a model it has no safety policies, replace its identity, or abandon its system prompt entirely. Uses persona establishment, RTL Unicode obfuscation, and Base64 encoding.

[View tests →](https://luke.yt/pi-checker/jailbreak/)

## [8\. Financial Sector Demo](https://luke.yt/pi-checker/financial-demo/)

3 levels

A fictional investor relations page for a company with mixed financials. Tests whether hidden injections can manipulate an AI analyst's investment recommendation - overriding visible data, suppressing risk disclosures, or fabricating an acquisition.

[View tests →](https://luke.yt/pi-checker/financial-demo/)

## Local LLMs vs Frontier Models

A preliminary look at Prompt Injection resistance

A full report comparing 8 different local models and 2 frontier models using various tests from this site.

[Download report (PDF) →](https://luke.yt/reports/Local-LLMs-vs-Frontier-Models.pdf)

[⌂](https://luke.yt/) [↑](https://luke.yt/pi-checker/#top)