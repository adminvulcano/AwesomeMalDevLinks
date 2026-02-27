# https://tlsh.org/

# TLSH - A Locality Sensitive Hash

## Introduction

TLSH is a fuzzy matching program and library.
Given a file (min 50 bytes), TLSH generates a hash value which can be used for similarity comparisons.
Similar files will have similar hash values which allows for the detection of similar objects by comparing their hash values

TLSH has been adopted by a range of bodies and malware repositories including:

- VirusTotal ( [https://developers.virustotal.com/v3.0/reference#files-tlsh](https://developers.virustotal.com/v3.0/reference#files-tlsh))

- Malware Bazaar ( [https://bazaar.abuse.ch/](https://bazaar.abuse.ch/))

- MISP ( [https://www.misp-project.org/](https://www.misp-project.org/))

- STIX: TLSH is a part of the STIX 2.1 standard ( [https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html](https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html)).


TLSH is becoming a standard choice for threat hunting and related security processing because of 2 key properties:

- Speed and Scalability.


We have added further explanation about fast search and scalable clustering on the
[Technical Overview](https://tlsh.org/papers.html#fast_search) page.

- TLSH is significantly more difficult to attack and evade than other similarity digests such as SSDEEP and SDHASH.


We have an overview on [Robustness to Attack here](https://tlsh.org/papers.html#robustness).


## News

- 13/4/2021: Notes on Function Re-ordering
Commentary on a recently published paper on the [blog](https://tlsh.org/blog.html).

- 22/10/2021: Presented [Designing the Elements of a Fuzzy Hashing Scheme](https://tlsh.org/papersDir/Design_TLSH_2021.pdf)
at EUC/Trustcom 2021.

- 15/11/2021: Presented "TLSH for the SOC" at the Australian Cyber Conference.
Related technical material can be found at [Fast Clustering of High Dimensional Data\\
Clustering the Malware Bazaar Dataset](https://tlsh.org/papersDir/n21_opt_cluster.pdf).