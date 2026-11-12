# Held-out eval: v1

37 cases, 74 graded rows (2 reps), 0 truncated, 0 failed attempts in errors.jsonl. Model: claude-haiku-5-5; judge: claude-sonnet-5-5.

## Quality

| Metric | Score (95% interval) |
|---|---|
| Pass | 72% ± 10% (n=74) |
| Right outcome | 97% ± 4% (n=74) |
| Right source | 100% ± 0% (n=50) |
| Grounded | 80% ± 9% (n=74) |
| Key points | 95% ± 3% (n=74) |

## Escalation

| Measure | Value |
|---|---|
| Recall (should escalate, did) | 100% (14/14) |
| Precision (escalated, should have) | 100% (14/14) |
| False escalation rate (should not, did) | 0% (0/60) |

## Outcomes (rows: expected, columns: actual)

| Expected | answered | escalate | decline |
|---|---|---|---|
| answered | 38 | 0 | 2 |
| escalate | 0 | 14 | 0 |
| decline | 0 | 0 | 20 |

## Speed and cost

| Measure | Value |
|---|---|
| Latency, median / 90th percentile / max | 1.7s / 2.4s / 3.7s |
| Output tokens per answer, median | 164 |
| Assistant cost per answer, mean | $0.00019 |
| Assistant cost, whole run | $0.0138 |
| Judge cost, whole run | $0.9404 |
| Cost of failed attempts | $0.0000 |
| Total | $0.9542 |

## Per case

| Case | Expected | Pass | Outcomes | Key points | Grounded | Traces |
|---|---|---|---|---|---|---|
| H01 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/H01_rep0.json), [rep1](v1/traces/H01_rep1.json) |
| H02 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/H02_rep0.json), [rep1](v1/traces/H02_rep1.json) |
| H03 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/H03_rep0.json), [rep1](v1/traces/H03_rep1.json) |
| H04 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/H04_rep0.json), [rep1](v1/traces/H04_rep1.json) |
| H05 | escalate | 50% | escalate, escalate | 1.00, 1.00 | 0, 1 | [rep0](v1/traces/H05_rep0.json), [rep1](v1/traces/H05_rep1.json) |
| S01 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S01_rep0.json), [rep1](v1/traces/S01_rep1.json) |
| S02 | answered | 0% | answered, answered | 1.00, 1.00 | 0, 0 | [rep0](v1/traces/S02_rep0.json), [rep1](v1/traces/S02_rep1.json) |
| S03 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S03_rep0.json), [rep1](v1/traces/S03_rep1.json) |
| S04 | answered | 0% | decline, decline | 0.50, 0.50 | 1, 1 | [rep0](v1/traces/S04_rep0.json), [rep1](v1/traces/S04_rep1.json) |
| S05 | answered | 50% | answered, answered | 1.00, 1.00 | 0, 1 | [rep0](v1/traces/S05_rep0.json), [rep1](v1/traces/S05_rep1.json) |
| S06 | answered | 50% | answered, answered | 1.00, 1.00 | 0, 1 | [rep0](v1/traces/S06_rep0.json), [rep1](v1/traces/S06_rep1.json) |
| S07 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S07_rep0.json), [rep1](v1/traces/S07_rep1.json) |
| S08 | answered | 50% | answered, answered | 1.00, 0.50 | 1, 1 | [rep0](v1/traces/S08_rep0.json), [rep1](v1/traces/S08_rep1.json) |
| S09 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S09_rep0.json), [rep1](v1/traces/S09_rep1.json) |
| S10 | answered | 0% | answered, answered | 0.50, 0.50 | 0, 1 | [rep0](v1/traces/S10_rep0.json), [rep1](v1/traces/S10_rep1.json) |
| S11 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S11_rep0.json), [rep1](v1/traces/S11_rep1.json) |
| S12 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S12_rep0.json), [rep1](v1/traces/S12_rep1.json) |
| S13 | answered | 0% | answered, answered | 1.00, 1.00 | 0, 0 | [rep0](v1/traces/S13_rep0.json), [rep1](v1/traces/S13_rep1.json) |
| S14 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S14_rep0.json), [rep1](v1/traces/S14_rep1.json) |
| S15 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S15_rep0.json), [rep1](v1/traces/S15_rep1.json) |
| S16 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S16_rep0.json), [rep1](v1/traces/S16_rep1.json) |
| S17 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S17_rep0.json), [rep1](v1/traces/S17_rep1.json) |
| S18 | answered | 50% | answered, answered | 1.00, 1.00 | 0, 1 | [rep0](v1/traces/S18_rep0.json), [rep1](v1/traces/S18_rep1.json) |
| S19 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S19_rep0.json), [rep1](v1/traces/S19_rep1.json) |
| S20 | answered | 0% | answered, answered | 1.00, 1.00 | 0, 0 | [rep0](v1/traces/S20_rep0.json), [rep1](v1/traces/S20_rep1.json) |
| S21 | escalate | 100% | escalate, escalate | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S21_rep0.json), [rep1](v1/traces/S21_rep1.json) |
| S22 | escalate | 100% | escalate, escalate | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S22_rep0.json), [rep1](v1/traces/S22_rep1.json) |
| S23 | escalate | 100% | escalate, escalate | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S23_rep0.json), [rep1](v1/traces/S23_rep1.json) |
| S24 | escalate | 0% | escalate, escalate | 0.67, 0.67 | 0, 1 | [rep0](v1/traces/S24_rep0.json), [rep1](v1/traces/S24_rep1.json) |
| S25 | escalate | 50% | escalate, escalate | 1.00, 1.00 | 0, 1 | [rep0](v1/traces/S25_rep0.json), [rep1](v1/traces/S25_rep1.json) |
| S26 | escalate | 100% | escalate, escalate | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S26_rep0.json), [rep1](v1/traces/S26_rep1.json) |
| S27 | decline | 0% | decline, decline | 1.00, 1.00 | 0, 0 | [rep0](v1/traces/S27_rep0.json), [rep1](v1/traces/S27_rep1.json) |
| S28 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S28_rep0.json), [rep1](v1/traces/S28_rep1.json) |
| S29 | decline | 50% | decline, decline | 1.00, 0.50 | 1, 1 | [rep0](v1/traces/S29_rep0.json), [rep1](v1/traces/S29_rep1.json) |
| S30 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S30_rep0.json), [rep1](v1/traces/S30_rep1.json) |
| S31 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S31_rep0.json), [rep1](v1/traces/S31_rep1.json) |
| S32 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v1/traces/S32_rep0.json), [rep1](v1/traces/S32_rep1.json) |

## Why cases failed

### H05 rep0: expected escalate, got escalate

Outcome ok: 1. Source ok: 1.0. Cited: VB-E09, velobook-14-user-guide.pdf, KB-3001.

Grounded: Unsupported: Stop using the laptop now to avoid further damage. (Stopping use is supported by the source and is safety advice, but 'to avoid further damage' is an added reason/consequence the sources do not state.)

```text
[met] Identifies VB-E09 as a fan or thermal fault: The reply says 'VB-E09 is a fan or thermal fault, which means the fan has failed or the laptop is overheating.'
[met] Tells the customer to stop using the laptop: The reply says 'Stop using the laptop now'.
[met] Says a repair request or support agent is needed: The reply says 'this error needs a repair, please contact support at support.veloria.example so a human agent can help you'.
```

### S02 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1002.

Grounded: Unsupported: Since you are on a Personal plan, freeing up space by emptying the web trash or deleting large files is the option that applies to you. (The sources do not say the admin option is inapplicable to Personal plans. This is an inference that the sources do not state, so it is unsupported.)

```text
[met] Storage quota is full, so uploads are paused: The reply says 'Error VS-1107 means your plan's storage is full, so uploads are paused while downloads keep working.'
[met] Empty the web trash or delete large files, or get more storage: The reply lists emptying the VeloSync web trash, deleting large files, or asking your admin for more storage.
[met] Personal plan storage is 200 GB: The reply says 'Your Personal plan includes 200 GB.'
```

### S02 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1002.

Grounded: Unsupported: If you are on your own personal plan, the first two steps are the ones you can take yourself. (The sources do not say which steps a personal-plan user can do themselves versus needing an admin. This is an inference not stated in the sources.)

```text
[met] Storage quota is full, so uploads are paused: The reply says 'your VeloSync plan's storage is full, so uploads are paused while downloads keep working.'
[met] Empty the web trash or delete large files, or get more storage: The reply lists emptying the VeloSync web trash, deleting large files, or asking your admin for more storage.
[met] Personal plan storage is 200 GB: The reply states 'On the Personal plan, storage is 200 GB.'
```

### S04 rep0: expected answered, got decline

Outcome ok: 0. Source ok: 1.0. Cited: KB-1003.

Grounded: Every specific claim is supported by the sources.

```text
[MISSED] Yes: the Team plan keeps version history for 180 days: The reply states 180 days and implies it should fall in the window, but it opens with 'I can't confirm that' and declines rather than starting with yes, so it does not clearly answer yes.
[met] Use Version history on the web: The reply says 'To restore it on the web, right-click the file and select Version history.'
```

### S04 rep1: expected answered, got decline

Outcome ok: 0. Source ok: 1.0. Cited: KB-1003.

Grounded: Every specific claim is supported by the sources.

```text
[MISSED] Yes: the Team plan keeps version history for 180 days: The reply states 180 days and says the 4-month version should be within the window, but it opens with 'I can't confirm' and declines rather than starting with yes, so it does not clearly give a yes.
[met] Use Version history on the web: The reply says 'Version history is accessed on the web by right-clicking the file and selecting Version history.'
```

### S05 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: VG-619, T-48277, KB-2001.

Grounded: Unsupported: which hotel networks often do (KB-2001 says TLS 443 works on restricted networks such as hotels, but no source states that hotel networks often block UDP 51820. This is an added generalization.)

```text
[met] Switch Protocol to TLS 443 under Settings > Connection: The reply says 'go to Settings > Connection, then set Protocol to TLS 443'.
[met] Yes, TLS 443 is slower, but works on most restricted networks: The reply states 'Yes, TLS 443 is slower, but it works on most restricted networks such as hotels.'
```

### S06 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: T-48644, KB-2002.

Grounded: Unsupported: You can also run ipconfig /flushdns in Command Prompt on Windows. (KB-2002 lists this command only under the 'Nothing loads' section. No source says it helps when public sites load but internal apps do not, so offering it for this wiki problem is a step the sources do not support.)

```text
[met] Split DNS is not being applied: The reply says 6.2.0 'ignored split DNS on Wi-Fi 7 adapters', which identifies split DNS not being applied as the cause.
[met] Version 6.2.0 has a known bug with Wi-Fi 7 adapters, fixed by updating to 6.2.1: The reply says this matches a known issue with 6.2.0 on Wi-Fi 7 adapters and tells the customer to update to 6.2.1 or later, which fixes it.
```

### S08 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: VG-1003, KB-2001.

Grounded: Every specific claim is supported by the sources.

```text
[MISSED] Device certificates last 12 months: The reply states the certificate is 'older than 12 months', which conveys the 12-month lifetime but does not explicitly say certificates last 12 months. It is only implied through the expiry cause.
[met] On a company-managed laptop the IT admin must renew it: The reply says 'managed devices must be renewed by your IT admin, so please ask your IT admin to renew the certificate' for the company laptop.
```

### S10 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: T-48590.

Grounded: Unsupported: Yes, this matches a known standby battery drain issue on VeloBook laptops. (T-48590 describes a battery empty after a weekend asleep, resolved by a BIOS update to 1.18 for standby drain. But calling it a 'known issue' on VeloBook laptops generalizes from a single past ticket; no known-issue source exists. Also the ticket does not say which product/model.); Update the BIOS to version 1.18 or later, which resolved the drain for another customer. (T-48590 says BIOS update to 1.18 resolved standby drain. 'or later' is a slight extension but the update to 1.18 is supported; 'or later' is not stated.)

```text
[MISSED] BIOS 1.15 to 1.17 has a standby battery drain bug: The reply never says that versions 1.15 to 1.17 are affected; it only says the customer's 1.16 should be updated, and calls it a general known issue without naming the affected range.
[met] Update BIOS to 1.18 or later: The reply says 'Update the BIOS to version 1.18 or later' and calls the update the fix to apply.
```

### S10 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: T-48590, T-48302.

Grounded: Every specific claim is supported by the sources.

```text
[MISSED] BIOS 1.15 to 1.17 has a standby battery drain bug: The reply says only that a 1.18 update stopped the drain and that the customer is on 1.16. It never states that 1.15 to 1.17 is an affected range or names a bug in those versions.
[met] Update BIOS to 1.18 or later: The reply says "please update your BIOS to 1.18", which matches the point.
```

### S13 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-3001, velobook-14-user-guide.pdf.

Grounded: Unsupported: A black screen with the fans running usually means the internal display or its cable has failed, not that the laptop is off. (KB-3001 says the display or cable has failed only if an image appears on an external monitor. It does not say this is the usual cause, and it does not say the laptop is not off. The 'usually' framing is an unsupported addition.); Because the laptop's display is the likely problem, contact support at support.veloria.example to arrange warranty repair. (The sources do not say the display is the likely problem before the monitor test, and they do not say support arranges the repair. The support address appears in the instructions, but this claim presents a repair route and a diagnosis the sources do not state.)

```text
[met] Connect an external monitor: The reply says 'Connect an external monitor to your VeloBook 14 Pro.'
[met] If an image appears there, the internal display or its cable has failed and needs a warranty repair: The reply says that if an image appears, the internal display or its cable has failed and the customer can ask about warranty repair. It also says to contact support to arrange warranty repair.
```

### S13 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-3001.

Grounded: Unsupported: Your VeloBook 14 Pro is still running (the fans are on), which usually means the internal display or its cable may have failed. (KB-3001 only says that if an image appears on an external monitor, the display or cable has failed. It does not say that fans running 'usually means' a display failure, so this is an unsupported inference about likelihood.); The laptop may be covered under warranty repair. (KB-3001 refers to KB-5002 about warranty repair, but there is no source on warranty coverage. Saying the laptop 'may be covered' is a coverage claim the sources do not make.)

```text
[met] Connect an external monitor: The reply says 'connect an external monitor to the laptop' as the check to perform.
[met] If an image appears there, the internal display or its cable has failed and needs a warranty repair: The reply says the internal screen or its cable has failed if an image appears, and tells the customer to contact support for warranty repair options. It hedges on coverage ('may be covered') but still points to warranty repair.
```

### S18 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1004, T-48213.

Grounded: Unsupported: Your CPU should return to normal once the file count is lower. (No source states this outcome of the workaround. KB-1004 only says to bring the file count below 100,000. The reply adds a promise about what will happen, which the instructions forbid unless a source says so.)

```text
[met] Do not disable the service, because sync would silently stop: The reply says 'please don't turn off the VeloSync service. Turning it off stops sync silently and your files will stop backing up.'
[met] Update to VeloSync 4.1.3 or later: The reply says 'Updating to 4.1.3 has resolved this... so updating VeloSync is the recommended fix.'
```

### S20 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1002, VS-1203.

Grounded: Unsupported: That is why you see the file locked message. (The sources link VS-1203 to another application having the file open, and the .pst advice sits under the VS-1203 heading. Outlook holding the file open is a reasonable reading, but the sources never say that this is the cause here. It is a mild causal inference.)

```text
[met] VeloSync does not support syncing open mail archives such as .pst files: The reply says 'VeloSync does not support syncing Outlook .pst files, because it does not support syncing open mail archives.'
[met] Exclude the .pst file from sync: The reply says 'To fix this, exclude the .pst file from sync in VeloSync.'
```

### S20 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1002, VS-1203.

Grounded: Unsupported: the file lock will keep happening with that file (Sources do not say the lock will recur. This is an added consequence not stated in any source.); Once the file is no longer in the sync queue, the lock error should stop (No source states this consequence of excluding the file; it is an inferred outcome.)

```text
[met] VeloSync does not support syncing open mail archives such as .pst files: The reply says "VeloSync does not support syncing open Outlook .pst mail archives".
[met] Exclude the .pst file from sync: The reply states "The supported fix is to exclude the .pst file from sync" and repeats "Then exclude the .pst file from sync."
```

### S24 rep0: expected escalate, got escalate

Outcome ok: 1. Source ok: 1.0. Cited: VB-E07, velobook-14-user-guide.pdf, KB-3001.

Grounded: Unsupported: ...because that can make recovery harder (No source gives a reason for not reinstalling Windows; this consequence is invented.); Please do not try to reset the laptop either (Sources say to back up before a factory reset and not to reset a BitLocker-protected laptop without a key, but do not say not to reset in this situation. This is an added instruction not found in the sources.)

```text
[met] VB-E07 means the SSD is not detected: The reply says 'VB-E07 means the SSD is not detected'.
[met] Do not reinstall Windows: The reply says 'Do not reinstall Windows'.
[MISSED] Needs a repair; Veloria does not offer data recovery as part of warranty repairs: The reply says the recommended fix is a repair request, but it never says that Veloria does not offer data recovery as part of warranty repairs. It says data recovery needs a human agent, which does not convey that.
```

### S24 rep1: expected escalate, got escalate

Outcome ok: 1. Source ok: 1.0. Cited: VB-E07, velobook-14-user-guide.pdf.

Grounded: Every specific claim is supported by the sources.

```text
[met] VB-E07 means the SSD is not detected: The reply states 'VB-E07 means the SSD was not detected.'
[met] Do not reinstall Windows: The reply says 'Do not reinstall Windows'.
[MISSED] Needs a repair; Veloria does not offer data recovery as part of warranty repairs: The reply says to request a repair, but it never says Veloria does not offer data recovery as part of warranty repairs. It says a human agent is needed for recovery, which is a different statement.
```

### S25 rep0: expected escalate, got escalate

Outcome ok: 1. Source ok: 1.0. Cited: KB-4002, KB-5001, T-48538.

Grounded: Unsupported: Veloria ID will lock the requests for 15 minutes after too many attempts. (KB-4002 says to wait 15 minutes for ID-429 (too many MFA attempts). It does not say the system locks the requests for 15 minutes. The sources do not state this mechanism, and the customer did not report an ID-429 error.)

```text
[met] Do not approve the requests: The reply says "Please do not approve any of these login requests."
[met] Reset the password right away: The reply says "reset your password right away."
[met] Possible account compromise, so contact support: The reply names a possible account compromise as the escalation reason and tells the customer to contact support at support.veloria.example.
```

### S27 rep0: expected decline, got decline

Outcome ok: 1. Source ok: None. Cited: KB-2001.

Grounded: Unsupported: VeloGuard is Veloria's VPN app for computers and devices, not software that runs on a Linux router (Sources never say which platforms VeloGuard supports or that it is an app for computers and devices. The assertion that it is not software that runs on a Linux router is not stated anywhere and contradicts the reply's own admission that it cannot confirm. Instructions only list VeloGuard VPN as a product, nothing about platforms.)

```text
[met] Says the sources do not cover a Linux router version: The reply says "the sources I have do not cover installing it on a router" and "I can't confirm whether a router version exists."
[met] Does not invent installation steps: The reply gives no installation steps; it only mentions the protocol details from KB-2001.
```

### S27 rep1: expected decline, got decline

Outcome ok: 1. Source ok: None. Cited: KB-2001.

Grounded: Unsupported: VeloGuard is an app for computers and devices, not a program that runs on a router (No source says which platforms VeloGuard runs on or that it cannot run on a router. This is an unsupported assertion, and it also conflicts with the reply's own statement that it cannot confirm availability.)

```text
[met] Says the sources do not cover a Linux router version: The reply states: 'The sources I have do not list a VeloGuard version for Linux routers, so I can't confirm whether one is available'.
[met] Does not invent installation steps: The reply gives no installation steps and says it cannot confirm how to install.
```

### S29 rep1: expected decline, got decline

Outcome ok: 1. Source ok: None. Cited: none.

Grounded: Every specific claim is supported by the sources.

```text
[MISSED] Says it can only help with Veloria products: The reply says the printer and Word are not Veloria products and that the sources don't cover printing. It then lists Veloria's products, which implies its scope, but it never states outright that it can only help with Veloria products.
[met] Does not give printer troubleshooting steps: The reply only declines and points to the manufacturer or an IT administrator. It gives no troubleshooting steps.
```

