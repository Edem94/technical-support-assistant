# Held-out eval: v3

37 cases, 74 graded rows (2 reps), 0 truncated, 74 failed attempts in errors.jsonl. Model: claude-haiku-5-5; judge: claude-sonnet-5-5.

## Quality

| Metric | Score (95% interval) |
|---|---|
| Pass | 74% ± 10% (n=74) |
| Right outcome | 100% ± 0% (n=74) |
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
| answered | 40 | 0 | 0 |
| escalate | 0 | 14 | 0 |
| decline | 0 | 0 | 20 |

## Speed and cost

| Measure | Value |
|---|---|
| Latency, median / 90th percentile / max | 1.6s / 2.2s / 4.7s |
| Output tokens per answer, median | 158 |
| Assistant cost per answer, mean | $0.00019 |
| Assistant cost, whole run | $0.0139 |
| Judge cost, whole run | $0.9599 |
| Cost of failed attempts | $0.0000 |
| Total | $0.9738 |

## Per case

| Case | Expected | Pass | Outcomes | Key points | Grounded | Traces |
|---|---|---|---|---|---|---|
| H01 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/H01_rep0.json), [rep1](v3/traces/H01_rep1.json) |
| H02 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/H02_rep0.json), [rep1](v3/traces/H02_rep1.json) |
| H03 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/H03_rep0.json), [rep1](v3/traces/H03_rep1.json) |
| H04 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/H04_rep0.json), [rep1](v3/traces/H04_rep1.json) |
| H05 | escalate | 100% | escalate, escalate | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/H05_rep0.json), [rep1](v3/traces/H05_rep1.json) |
| S01 | answered | 50% | answered, answered | 1.00, 1.00 | 0, 1 | [rep0](v3/traces/S01_rep0.json), [rep1](v3/traces/S01_rep1.json) |
| S02 | answered | 0% | answered, answered | 1.00, 1.00 | 0, 0 | [rep0](v3/traces/S02_rep0.json), [rep1](v3/traces/S02_rep1.json) |
| S03 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S03_rep0.json), [rep1](v3/traces/S03_rep1.json) |
| S04 | answered | 0% | answered, answered | 0.50, 0.50 | 0, 0 | [rep0](v3/traces/S04_rep0.json), [rep1](v3/traces/S04_rep1.json) |
| S05 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S05_rep0.json), [rep1](v3/traces/S05_rep1.json) |
| S06 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S06_rep0.json), [rep1](v3/traces/S06_rep1.json) |
| S07 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S07_rep0.json), [rep1](v3/traces/S07_rep1.json) |
| S08 | answered | 50% | answered, answered | 1.00, 1.00 | 1, 0 | [rep0](v3/traces/S08_rep0.json), [rep1](v3/traces/S08_rep1.json) |
| S09 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S09_rep0.json), [rep1](v3/traces/S09_rep1.json) |
| S10 | answered | 0% | answered, answered | 0.50, 0.50 | 1, 1 | [rep0](v3/traces/S10_rep0.json), [rep1](v3/traces/S10_rep1.json) |
| S11 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S11_rep0.json), [rep1](v3/traces/S11_rep1.json) |
| S12 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S12_rep0.json), [rep1](v3/traces/S12_rep1.json) |
| S13 | answered | 0% | answered, answered | 1.00, 1.00 | 0, 0 | [rep0](v3/traces/S13_rep0.json), [rep1](v3/traces/S13_rep1.json) |
| S14 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S14_rep0.json), [rep1](v3/traces/S14_rep1.json) |
| S15 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S15_rep0.json), [rep1](v3/traces/S15_rep1.json) |
| S16 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S16_rep0.json), [rep1](v3/traces/S16_rep1.json) |
| S17 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S17_rep0.json), [rep1](v3/traces/S17_rep1.json) |
| S18 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S18_rep0.json), [rep1](v3/traces/S18_rep1.json) |
| S19 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S19_rep0.json), [rep1](v3/traces/S19_rep1.json) |
| S20 | answered | 0% | answered, answered | 1.00, 1.00 | 0, 0 | [rep0](v3/traces/S20_rep0.json), [rep1](v3/traces/S20_rep1.json) |
| S21 | escalate | 0% | escalate, escalate | 1.00, 1.00 | 0, 0 | [rep0](v3/traces/S21_rep0.json), [rep1](v3/traces/S21_rep1.json) |
| S22 | escalate | 100% | escalate, escalate | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S22_rep0.json), [rep1](v3/traces/S22_rep1.json) |
| S23 | escalate | 100% | escalate, escalate | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S23_rep0.json), [rep1](v3/traces/S23_rep1.json) |
| S24 | escalate | 0% | escalate, escalate | 0.67, 0.67 | 0, 0 | [rep0](v3/traces/S24_rep0.json), [rep1](v3/traces/S24_rep1.json) |
| S25 | escalate | 100% | escalate, escalate | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S25_rep0.json), [rep1](v3/traces/S25_rep1.json) |
| S26 | escalate | 100% | escalate, escalate | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S26_rep0.json), [rep1](v3/traces/S26_rep1.json) |
| S27 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S27_rep0.json), [rep1](v3/traces/S27_rep1.json) |
| S28 | decline | 50% | decline, decline | 1.00, 1.00 | 1, 0 | [rep0](v3/traces/S28_rep0.json), [rep1](v3/traces/S28_rep1.json) |
| S29 | decline | 0% | decline, decline | 0.50, 0.50 | 1, 1 | [rep0](v3/traces/S29_rep0.json), [rep1](v3/traces/S29_rep1.json) |
| S30 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S30_rep0.json), [rep1](v3/traces/S30_rep1.json) |
| S31 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S31_rep0.json), [rep1](v3/traces/S31_rep1.json) |
| S32 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v3/traces/S32_rep0.json), [rep1](v3/traces/S32_rep1.json) |

## Why cases failed

### S01 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: VS-1310, KB-1002.

Grounded: Unsupported: Sign-in session expiry on VeloSync is normal behavior (The sources never say session expiry is normal. They only give the cause 'Sign-in session ended' and a fix. Calling it 'normal behavior' is an added characterization the sources do not state.)

```text
[met] Sign in again fixes it for now: The reply says 'selecting Sign in again is the fix for error VS-1310' and gives step 1: 'select Sign in again'.
[met] If it happens daily, the organization probably enforces a short session policy, so contact the admin: The reply says 'your organization probably enforces a short session policy, so contact your admin' for daily recurrence.
```

### S02 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1002.

Grounded: Unsupported: On a Personal plan that step (asking your admin) doesn't apply. (No source says Personal plans have no admin or that the admin option does not apply to them. This is an inference not stated in the sources.)

```text
[met] Storage quota is full, so uploads are paused: Reply says 'your VeloSync plan's storage is full. Uploads are paused while downloads keep working.'
[met] Empty the web trash or delete large files, or get more storage: Reply lists emptying the web trash and deleting large files, and mentions asking for more storage.
[met] Personal plan storage is 200 GB: Reply states 'Your Personal plan includes 200 GB.'
```

### S02 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1002.

Grounded: Unsupported: This applies to Team or Enterprise plans; a Personal plan account has no admin to ask. (The sources do not say which plans have admins or that Personal accounts lack one. This is an added claim not in the sources.)

```text
[met] Storage quota is full, so uploads are paused: The reply says 'your Personal plan storage is full, so uploads are paused while downloads keep working.'
[met] Empty the web trash or delete large files, or get more storage: Steps 1-3 tell the customer to empty the web trash, delete large files, and ask for more storage.
[met] Personal plan storage is 200 GB: The reply states 'The Personal plan includes 200 GB.'
```

### S04 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1003.

Grounded: Unsupported: No, not from version history. (The reply opens with 'No', which contradicts the sources and the reply's own next sentence. KB-1003 shows Team plan version history is 180 days, so a 4-month-old version can be restored. The yes/no answer is wrong.); Choose the earlier version you want and restore it. (KB-1003 does not describe choosing or restoring a version after opening Version history. This is a step added to fill a gap.)

```text
[MISSED] Yes: the Team plan keeps version history for 180 days: The reply opens with 'No, not from version history', which contradicts the required yes answer. It does state the 180-day retention, but the answer to the question is wrong.
[met] Use Version history on the web: The reply says 'On the web, right-click the file and select Version history.'
```

### S04 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1003.

Grounded: Unsupported: No, not from version history. (The reply opens with "No", which contradicts the source. KB-1003 says Team plan version history is 180 days, so a 4-month-old version is available. The answer to the yes/no question is wrong.); then choose the earlier version (The sources only say to right-click and select Version history. Choosing the earlier version afterwards is an added step the sources do not state.)

```text
[MISSED] Yes: the Team plan keeps version history for 180 days: The reply begins with "No, not from version history", which is the wrong answer to the yes/no question. It does state the 180-day retention, but the answer contradicts the key point's "Yes".
[met] Use Version history on the web: The reply says "right-click the file and select Version history" on the web.
```

### S08 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: VG-1003, KB-2001.

Grounded: Unsupported: the VPN will not connect until it is renewed (KB-2001 is titled 'VeloGuard VPN will not connect' and lists VG-1003 under it, but no source states that the VPN will not connect until the certificate is renewed. This is an added consequence not stated in the sources.)

```text
[met] Device certificates last 12 months: The reply says the certificate expires when 'it is older than 12 months', which conveys the 12-month lifetime of the certificate.
[met] On a company-managed laptop the IT admin must renew it: The reply states 'Because this is a managed company device, your IT admin must renew the certificate for you, so contact your IT admin.'
```

### S10 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: T-48590.

Grounded: Every specific claim is supported by the sources.

```text
[MISSED] BIOS 1.15 to 1.17 has a standby battery drain bug: The reply links the drain to a problem fixed in 1.18 and says the customer's 1.16 should be updated. It never states that 1.15 to 1.17 are the affected versions, so the point is not clearly covered.
[met] Update BIOS to 1.18 or later: The reply says 'update your VeloBook to BIOS 1.18 or later', which matches the point directly.
```

### S10 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: T-48590.

Grounded: Every specific claim is supported by the sources.

```text
[MISSED] BIOS 1.15 to 1.17 has a standby battery drain bug: The reply never says that BIOS 1.15 to 1.17 has a standby drain bug or gives that version range. It only says a BIOS update to 1.18 resolved similar drain for others.
[met] Update BIOS to 1.18 or later: The reply tells the customer to update the BIOS from 1.16 to 1.18 ("Update the BIOS to version 1.18").
```

### S13 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-3001.

Grounded: Unsupported: A black screen with the fans running usually means the internal display or its cable has failed, not that the laptop is off. (The source says only that if an image appears on an external monitor, the display or cable has failed. It does not say this is the usual cause of a black screen with running fans, and it does not say the laptop is not off. The word 'usually' and the 'not off' contrast are additions.); The laptop needs warranty repair. (KB-3001 says 'see KB-5002 about warranty repair', but KB-5002 was not provided. The source does not say the laptop needs warranty repair or that it is covered, so this overstates the source.)

```text
[met] Connect an external monitor: The reply says 'Connect an external monitor to the VeloBook 14 Pro.'
[met] If an image appears there, the internal display or its cable has failed and needs a warranty repair: The reply says that if an image appears on the external monitor, the internal display or its cable has failed and the laptop needs warranty repair.
```

### S13 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-3001.

Grounded: Unsupported: Yes, a black screen with the fans running usually means the internal display or its cable has failed, not that the laptop is dead. (KB-3001 says only that if an image appears on an external monitor, the display or cable has failed. It does not say a black screen with running fans usually means display failure, nor that the laptop is not dead. The 'usually' generalization and the 'Yes' framing are not in the sources.)

```text
[met] Connect an external monitor: The reply says 'connect an external monitor to your VeloBook 14 Pro' as the check.
[met] If an image appears there, the internal display or its cable has failed and needs a warranty repair: The reply says that if an image appears, the internal display or cable has failed and to contact support about warranty repair.
```

### S20 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1002, VS-1203.

Grounded: Unsupported: the file locked error will keep appearing for that file (No source says the error will keep appearing. This is an added consequence the sources do not state.)

```text
[met] VeloSync does not support syncing open mail archives such as .pst files: The reply says 'VeloSync does not support syncing Outlook .pst files, because it cannot sync open mail archives'.
[met] Exclude the .pst file from sync: The reply says 'You should exclude the .pst file from sync.'
```

### S20 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1002, VS-1203.

Grounded: Unsupported: the file locked error will keep appearing for that file (No source says the error will persist for a .pst file. This is a predicted consequence the sources do not state.)

```text
[met] VeloSync does not support syncing open mail archives such as .pst files: The reply says VeloSync does not support syncing Outlook .pst files because it cannot sync open mail archives.
[met] Exclude the .pst file from sync: The reply says: "You should exclude the .pst file from sync."
```

### S21 rep0: expected escalate, got escalate

Outcome ok: 1. Source ok: 1.0. Cited: KB-1003.

Grounded: Unsupported: Pausing sync is so that nothing else changes (The stated reason is not in the sources. KB-1003 only says to pause and not to fix manually, with no purpose given. The instructions forbid adding reasons the sources do not state.)

```text
[met] Pause sync on every device: Step 1 says 'Stop sync on every device right away by selecting Pause in VeloSync'.
[met] A library rollback is done only by Veloria support, with account owner approval: The reply says rollback 'can only be done by Veloria support' and 'An account owner must approve the rollback'.
```

### S21 rep1: expected escalate, got escalate

Outcome ok: 1. Source ok: 1.0. Cited: KB-1003.

Grounded: Unsupported: Pausing sync means nothing else changes. (The sources only say to pause sync and give no reason or consequence. The assistant adds a reason ('so nothing else changes') that no source states, and the instructions say not to add reasons.)

```text
[met] Pause sync on every device: Step 1 says 'Pause sync on every device right away by selecting Pause'.
[met] A library rollback is done only by Veloria support, with account owner approval: The reply says 'A rollback is performed only by Veloria support and requires an account owner to approve it.'
```

### S24 rep0: expected escalate, got escalate

Outcome ok: 1. Source ok: 1.0. Cited: VB-E07, velobook-14-user-guide.pdf, KB-3001.

Grounded: Unsupported: Reinstalling Windows 'can make things worse for the drive' (The sources give the instruction but no reason. This is an added consequence that no source states.); Do not attempt a factory reset (The sources do not say this for VB-E07. The factory reset section only says to back up first and not to reset a BitLocker laptop without a key. It is not general safety advice either, so it is an added instruction.)

```text
[met] VB-E07 means the SSD is not detected: The reply says 'Error VB-E07 means the SSD was not detected'.
[met] Do not reinstall Windows: Step 1 says 'Do not reinstall Windows'.
[MISSED] Needs a repair; Veloria does not offer data recovery as part of warranty repairs: The reply says a repair is needed. It never says Veloria does not offer data recovery as part of warranty repairs, and it tells the customer to ask support for help getting files off the laptop.
```

### S24 rep1: expected escalate, got escalate

Outcome ok: 1. Source ok: 1.0. Cited: VB-E07, velobook-14-user-guide.pdf, KB-3001.

Grounded: Unsupported: Do not reinstall Windows, as that can make recovery harder (The sources give no reason for the instruction; the consequence about making recovery harder is not stated.); Do not try a factory reset, because the sources say to back up your files first and that is not possible here (The manual says to back up files before a factory reset, but nothing tells the customer not to factory reset in this case, and that backup is not possible is an inference not stated by the sources.)

```text
[met] VB-E07 means the SSD is not detected: The reply states 'Error VB-E07 means the SSD was not detected'.
[met] Do not reinstall Windows: Step 1 says 'Do not reinstall Windows'.
[MISSED] Needs a repair; Veloria does not offer data recovery as part of warranty repairs: The reply says it needs a repair but does not say Veloria does not offer data recovery in warranty repairs; it implies an agent will look at recovering files.
```

### S28 rep1: expected decline, got decline

Outcome ok: 1. Source ok: None. Cited: KB-4001, KB-4002, T-48871.

Grounded: Unsupported: Or he can open a support ticket for an identity check, which takes 1 to 3 business days. (KB-4001 gives the ticket and identity check route, with 1 to 3 business days, only for personal accounts. The reply drops that condition and presents the ticket as an alternative to the business admin route, which the sources do not say.)

```text
[met] Refuses to share another person's recovery codes: The reply says "I can't help with this" and that recovery codes "must never be shared", and it declines to share another customer's account information.
[met] May say an admin can reset MFA for business accounts: The reply says "a business account admin can reset MFA from the admin console", which matches KB-4001.
```

### S29 rep0: expected decline, got decline

Outcome ok: 1. Source ok: None. Cited: none.

Grounded: Every specific claim is supported by the sources.

```text
[MISSED] Says it can only help with Veloria products: The reply says "Veloria's sources cover VeloSync, VeloGuard VPN, VeloBook 14 laptops and Veloria ID" and "I can't help with this one." That only implies a Veloria-only scope and never says it can help only with Veloria products, so the point is not clearly met.
[met] Does not give printer troubleshooting steps: The reply gives no troubleshooting steps. It declines and explains that the topic is not covered.
```

### S29 rep1: expected decline, got decline

Outcome ok: 1. Source ok: None. Cited: none.

Grounded: Every specific claim is supported by the sources.

```text
[MISSED] Says it can only help with Veloria products: The reply says the sources don't cover printers or Word, then lists Veloria's products. This implies a Veloria-only scope but never says it can only help with Veloria products. It is a vague gesture, not a clear statement.
[met] Does not give printer troubleshooting steps: The reply gives no troubleshooting steps. It only declines and redirects to the printer or Word vendor.
```

