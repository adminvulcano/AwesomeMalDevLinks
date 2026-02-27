# https://blog.levi.wiki/post/2025-12-02-defender-temporal-detections

# Temporal-Behavioural Detections & Whitelists

While playing around with attacks and bypasses for my [EDRi](https://github.com/cailllev/EDRi) project, I noticed very strange behaviour in Defenders detections.

Defender for Individuals (and MDE) appear to store “known bad” behavior of processes and classify further executions of similar attacks the same, meaning other bypass strategies of the same attack are classified just as the first attack variant.

Conversely, the inverse also seems to hold. Non-malicious behaviour is also stored temporarily, presumably to increase system performance. Shortly after the initial successful attack with the deconditioning strategy, the standard (null) strategy also works.

## Notes

1) In the following tests the \\EDR-Introspection\ folder is excluded from Defender, meaning known bad files are not deleted after detection, and only malicious behaviour at runtime is blocked, not the initial execution.

2) The source code for the tests is available here [EDRi/attacks/LsassReader](https://github.com/cailllev/EDR-Introspection/blob/4eb8966fd3a23752b078f4f6724aa4a83caff140/attacks/LsassReader/read-lsass.cpp)

3) standard.exe means no bypasses, deconditioning.exe uses string-obfuscation, anti-emulation and deconditioning (by dumping non critical processes first)

## Tests

![LsassReader deconditioning works](https://blog.levi.wiki/static/defender-temporal-detections/LsassReader-deconditioning-works.png)

_First run of LsassReader-deconditioning.exe is successful._

![LsassReader standard works](https://blog.levi.wiki/static/defender-temporal-detections/LsassReader-standard-works.png)

_Now the LsassReader-standard.exe also does not raise behavioural alerts._

Only after LsassReader-standard.exe raises an alert, for example by copying it to a non-excluded directory (1), future executions of the standard strategy are behaviourally detected and blocked. The file hash still matches (2). When the standard variant is executed _now_ (3), the system eventually hangs before the attack is able to dump the lsass process (4). The system hang can also be seen by the large time difference - 20 seconds instead of 5 seconds - marked in the red square top left.

![LsassReader standard detected](https://blog.levi.wiki/static/defender-temporal-detections/LsassReader-standard-detected.png)

_After a triggered alert, the temporal behavioral detections are reset for LsassReader-(x).exe._

And because of the now “known bad” behaviour of LsassReader-(x).exe, the deconditioning strategy is also behaviourally detected and the system hangs before the attack can dump the lsass process, see again the red square top left.

![LsassReader deconditioning detected](https://blog.levi.wiki/static/defender-temporal-detections/LsassReader-deconditioning-detected.png)

_After a triggered alert, all LsassReader-(x).exe variants are blocked._

## Solution?

Disable "send samples to Microsoft" and wait for about an hour after testing one variant, then the cached behavioural detection will be deleted again and Defender operates "as usual".

## A note on Cloud Delivered Protection

Projects like [Detonator](https://github.com/dobin/DetonatorAgent) use newly set-up VMs to conduct tests.

However, as described in "Microsoft Defender for Endpoint in Depth" (978-1804615461), suspicious executions can get flagged and compared to known bad files (metadata of files) on Microsofts cloud.

Even when "Cloud Delivered Protection" is turned off, there are 4 local stages to this protection, meaning metadata is stored locally after a detection and can be retrieved for future runs of similar malware files.

## Conclusion

- When conducting tests on one system without resetting it, wait 1h after an attack was detected.
- When conducting tests on multiple systems or with resets between runs, make sure "Cloud Delivered Protection" is off, so the metadata of detected files is not stored in the cloud.