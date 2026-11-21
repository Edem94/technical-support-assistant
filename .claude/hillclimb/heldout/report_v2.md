# Held-out eval: v2

37 cases, 74 graded rows (2 reps), 0 truncated, 0 failed attempts in errors.jsonl. Model: claude-haiku-5-5; judge: claude-sonnet-5-5.

## Quality

| Metric | Score (95% interval) |
|---|---|
| Pass | 78% ± 9% (n=74) |
| Right outcome | 100% ± 0% (n=74) |
| Right source | 100% ± 0% (n=50) |
| Grounded | 81% ± 9% (n=74) |
| Key points | 97% ± 3% (n=74) |

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
| Latency, median / 90th percentile / max | 1.5s / 2.1s / 4.0s |
| Output tokens per answer, median | 154 |
| Assistant cost per answer, mean | $0.00019 |
| Assistant cost, whole run | $0.0139 |
| Judge cost, whole run | $0.9536 |
| Cost of failed attempts | $0.0000 |
| Total | $0.9674 |

## Per case

| Case | Expected | Pass | Outcomes | Key points | Grounded | Traces |
|---|---|---|---|---|---|---|
| H01 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/H01_rep0.json), [rep1](v2/traces/H01_rep1.json) |
| H02 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/H02_rep0.json), [rep1](v2/traces/H02_rep1.json) |
| H03 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/H03_rep0.json), [rep1](v2/traces/H03_rep1.json) |
| H04 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/H04_rep0.json), [rep1](v2/traces/H04_rep1.json) |
| H05 | escalate | 100% | escalate, escalate | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/H05_rep0.json), [rep1](v2/traces/H05_rep1.json) |
| S01 | answered | 50% | answered, answered | 1.00, 1.00 | 0, 1 | [rep0](v2/traces/S01_rep0.json), [rep1](v2/traces/S01_rep1.json) |
| S02 | answered | 50% | answered, answered | 1.00, 1.00 | 1, 0 | [rep0](v2/traces/S02_rep0.json), [rep1](v2/traces/S02_rep1.json) |
| S03 | answered | 0% | answered, answered | 1.00, 1.00 | 0, 0 | [rep0](v2/traces/S03_rep0.json), [rep1](v2/traces/S03_rep1.json) |
| S04 | answered | 50% | answered, answered | 1.00, 1.00 | 0, 1 | [rep0](v2/traces/S04_rep0.json), [rep1](v2/traces/S04_rep1.json) |
| S05 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S05_rep0.json), [rep1](v2/traces/S05_rep1.json) |
| S06 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S06_rep0.json), [rep1](v2/traces/S06_rep1.json) |
| S07 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S07_rep0.json), [rep1](v2/traces/S07_rep1.json) |
| S08 | answered | 50% | answered, answered | 1.00, 1.00 | 1, 0 | [rep0](v2/traces/S08_rep0.json), [rep1](v2/traces/S08_rep1.json) |
| S09 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S09_rep0.json), [rep1](v2/traces/S09_rep1.json) |
| S10 | answered | 0% | answered, answered | 0.50, 0.50 | 1, 1 | [rep0](v2/traces/S10_rep0.json), [rep1](v2/traces/S10_rep1.json) |
| S11 | answered | 50% | answered, answered | 1.00, 1.00 | 0, 1 | [rep0](v2/traces/S11_rep0.json), [rep1](v2/traces/S11_rep1.json) |
| S12 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S12_rep0.json), [rep1](v2/traces/S12_rep1.json) |
| S13 | answered | 50% | answered, answered | 0.50, 1.00 | 0, 1 | [rep0](v2/traces/S13_rep0.json), [rep1](v2/traces/S13_rep1.json) |
| S14 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S14_rep0.json), [rep1](v2/traces/S14_rep1.json) |
| S15 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S15_rep0.json), [rep1](v2/traces/S15_rep1.json) |
| S16 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S16_rep0.json), [rep1](v2/traces/S16_rep1.json) |
| S17 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S17_rep0.json), [rep1](v2/traces/S17_rep1.json) |
| S18 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S18_rep0.json), [rep1](v2/traces/S18_rep1.json) |
| S19 | answered | 100% | answered, answered | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S19_rep0.json), [rep1](v2/traces/S19_rep1.json) |
| S20 | answered | 0% | answered, answered | 1.00, 1.00 | 0, 0 | [rep0](v2/traces/S20_rep0.json), [rep1](v2/traces/S20_rep1.json) |
| S21 | escalate | 50% | escalate, escalate | 1.00, 1.00 | 0, 1 | [rep0](v2/traces/S21_rep0.json), [rep1](v2/traces/S21_rep1.json) |
| S22 | escalate | 100% | escalate, escalate | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S22_rep0.json), [rep1](v2/traces/S22_rep1.json) |
| S23 | escalate | 100% | escalate, escalate | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S23_rep0.json), [rep1](v2/traces/S23_rep1.json) |
| S24 | escalate | 0% | escalate, escalate | 0.67, 0.67 | 0, 0 | [rep0](v2/traces/S24_rep0.json), [rep1](v2/traces/S24_rep1.json) |
| S25 | escalate | 100% | escalate, escalate | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S25_rep0.json), [rep1](v2/traces/S25_rep1.json) |
| S26 | escalate | 100% | escalate, escalate | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S26_rep0.json), [rep1](v2/traces/S26_rep1.json) |
| S27 | decline | 50% | decline, decline | 1.00, 1.00 | 0, 1 | [rep0](v2/traces/S27_rep0.json), [rep1](v2/traces/S27_rep1.json) |
| S28 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S28_rep0.json), [rep1](v2/traces/S28_rep1.json) |
| S29 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S29_rep0.json), [rep1](v2/traces/S29_rep1.json) |
| S30 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S30_rep0.json), [rep1](v2/traces/S30_rep1.json) |
| S31 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S31_rep0.json), [rep1](v2/traces/S31_rep1.json) |
| S32 | decline | 100% | decline, decline | 1.00, 1.00 | 1, 1 | [rep0](v2/traces/S32_rep0.json), [rep1](v2/traces/S32_rep1.json) |

## Why cases failed

### S01 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: VS-1310, KB-1002.

Grounded: Unsupported: Yes, this is a known issue (The sources never describe this as a 'known issue'. They give an error code and its fix, but nothing labels it a known issue. The reply also opens with 'Yes' although the customer did not ask a yes/no question.)

```text
[met] Sign in again fixes it for now: The reply says 'To fix it, select Sign in again.'
[met] If it happens daily, the organization probably enforces a short session policy, so contact the admin: The reply says 'If it keeps happening every day, your organization probably enforces a short session policy, so contact your admin about it.'
```

### S02 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1002.

Grounded: Unsupported: (this applies if the account is managed by an organization) (The sources do not say that asking an admin applies only to organization-managed accounts. This is an added condition not stated in the sources.)

```text
[met] Storage quota is full, so uploads are paused: The reply says 'your VeloSync plan's storage is full, so uploads are paused while downloads continue.'
[met] Empty the web trash or delete large files, or get more storage: The reply lists emptying the web trash, deleting large files, and asking admin for more storage.
[met] Personal plan storage is 200 GB: The reply states 'The Personal plan includes 200 GB.'
```

### S03 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1003.

Grounded: Unsupported: The Sam's conflicted copy is Sam's version. (KB-1003 never says the name in the renamed file identifies who made that version. The reply infers this from the naming pattern, and the sources do not state it.)

```text
[met] VeloSync kept both versions because both were edited offline: The reply says 'VeloSync keeps both versions when two people edit a file offline.'
[met] Compare the two, merge the changes, then delete the copy no longer needed: The reply says 'compare the two files, merge your changes... and then delete the copy you no longer need.'
```

### S03 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1003.

Grounded: Unsupported: so the file you see is Sam's version (No source says the name in the conflicted copy is the name of the person who made that version. The reply also assumes which person's edits ended up in which file, and the sources do not state that.)

```text
[met] VeloSync kept both versions because both were edited offline: The reply says "VeloSync keeps both versions when two people edit a file offline", which explains why the conflicted copy exists.
[met] Compare the two, merge the changes, then delete the copy no longer needed: The reply says "Compare the two versions, merge your changes, and then delete the copy you no longer need."
```

### S04 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1003.

Grounded: Unsupported: then choose the earlier version to restore (KB-1003 only says to right-click and select Version history under 'Restoring an earlier version'. It does not describe choosing a version to restore from the list; this extra step is not in the sources.)

```text
[met] Yes: the Team plan keeps version history for 180 days: Reply starts with 'Yes' and states the Team plan's version history is 180 days, covering 4 months.
[met] Use Version history on the web: Reply says 'On the web, right-click the file and select Version history'.
```

### S08 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: VG-1003, KB-2001.

Grounded: Unsupported: Managed devices cannot be renewed from the error dialog. (Sources say to select Renew certificate in the error dialog and that managed devices must be renewed by the IT admin. They do not state that the dialog cannot be used on managed devices; this is an added inference about what will or won't work.)

```text
[met] Device certificates last 12 months: The reply says the error occurs when a device certificate is older than 12 months, which conveys the 12-month lifetime, though it does not literally say 'last 12 months'.
[met] On a company-managed laptop the IT admin must renew it: The reply states 'your IT admin needs to renew the certificate' for the company laptop and tells the customer to contact their IT admin.
```

### S10 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: T-48590.

Grounded: Every specific claim is supported by the sources.

```text
[MISSED] BIOS 1.15 to 1.17 has a standby battery drain bug: The reply never says which BIOS versions are affected. It only says a BIOS update fixed a similar drain and tells the customer to move from 1.16 to 1.18. It does not state the 1.15 to 1.17 range.
[met] Update BIOS to 1.18 or later: The reply says 'Update your VeloBook 14 BIOS from 1.16 to 1.18 or later.'
```

### S10 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: T-48590.

Grounded: Every specific claim is supported by the sources.

```text
[MISSED] BIOS 1.15 to 1.17 has a standby battery drain bug: The reply only says a similar case was fixed by updating to 1.18. It never says versions 1.15 to 1.17 have a standby drain bug, so this is not stated.
[met] Update BIOS to 1.18 or later: The reply says 'Your BIOS is 1.16, so update to 1.18', which clearly advises updating to 1.18.
```

### S11 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-5002.

Grounded: Unsupported: VeloCare Plus offers 'protection against accidents like this in future' (i.e. spills) (The sources only say VeloCare Plus adds one accidental damage repair per year. They list accidental damage and liquid damage separately as excluded from the standard warranty, and never say VeloCare Plus covers liquid damage. Suggesting it protects against a coffee spill is an unsupported implication.)

```text
[met] Standard warranty is 2 years: The reply says 'a standard warranty of 2 years from purchase, covering manufacturing defects'.
[met] Liquid damage is not covered by the standard warranty: The reply says 'No, spilling coffee is not covered by the standard warranty, because liquid damage is excluded.'
[met] VeloCare Plus adds one accidental damage repair per year, with a USD 49 fee: Step 1 says VeloCare Plus 'adds one accidental damage repair per year for a USD 49 service fee'.
```

### S13 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-3001.

Grounded: Unsupported: Yes, this usually means the internal display or its cable has failed rather than the laptop being off. (KB-3001 says only that if an image appears on an external monitor, the internal display or cable has failed. It does not say a black screen with fans 'usually' means display failure, nor that the laptop is not off. The 'usually' generalization is an added claim. Also, the question was not yes/no, so 'Yes' is inappropriate.)

```text
[met] Connect an external monitor: The reply says 'Connect an external monitor to the VeloBook 14 Pro.'
[MISSED] If an image appears there, the internal display or its cable has failed and needs a warranty repair: The reply says the internal display or cable has failed and refers to warranty repair info in KB-5002, but only says 'you can look at' it rather than stating that it needs a warranty repair; this is a vague gesture.
```

### S20 rep0: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1002, VS-1203.

Grounded: Unsupported: the file lock you are seeing is expected for this file type (The sources do not say the lock is expected for .pst files. KB-1002 says only that VS-1203 means another app has the file open and that .pst files should be excluded because open mail archives are unsupported. 'Expected' is an inference the sources do not state.)

```text
[met] VeloSync does not support syncing open mail archives such as .pst files: The reply states 'VeloSync does not support syncing Outlook .pst files, because it does not support syncing open mail archives'.
[met] Exclude the .pst file from sync: The reply says 'Exclude the .pst file from sync instead.'
```

### S20 rep1: expected answered, got answered

Outcome ok: 1. Source ok: 1.0. Cited: KB-1002, VS-1203.

Grounded: Unsupported: the file locked error will keep occurring for that file (No source says the error will keep recurring. This is an added consequence beyond what KB-1002 or VS-1203 state.)

```text
[met] VeloSync does not support syncing open mail archives such as .pst files: The reply states 'VeloSync does not support syncing Outlook .pst files, because it cannot sync open mail archives'.
[met] Exclude the .pst file from sync: The reply says 'Exclude the .pst file from sync instead.'
```

### S21 rep0: expected escalate, got escalate

Outcome ok: 1. Source ok: 1.0. Cited: KB-1003.

Grounded: Unsupported: Pausing sync means "nothing else changes." (The sources give no reason for pausing and do not say that nothing else will change. This is an added reason or consequence.)

```text
[met] Pause sync on every device: The reply says "Stop sync on every device right away by selecting Pause in VeloSync".
[met] A library rollback is done only by Veloria support, with account owner approval: The reply says a rollback "only Veloria support can perform and which requires an account owner to approve".
```

### S24 rep0: expected escalate, got escalate

Outcome ok: 1. Source ok: 1.0. Cited: VB-E07, velobook-14-user-guide.pdf.

Grounded: Unsupported: because this can make recovery harder (No source gives a reason for the instruction not to reinstall Windows. This is an added consequence.); Your files are on the SSD (No source says where the customer's files are stored. This is an assumption.)

```text
[met] VB-E07 means the SSD is not detected: The reply says 'Error VB-E07 means the SSD is not detected'.
[met] Do not reinstall Windows: The reply says 'Do not reinstall Windows'.
[MISSED] Needs a repair; Veloria does not offer data recovery as part of warranty repairs: The reply mentions a repair request, but it never says Veloria does not offer data recovery as part of warranty repairs. It says a human agent will handle 'any data recovery', which implies the opposite.
```

### S24 rep1: expected escalate, got escalate

Outcome ok: 1. Source ok: 1.0. Cited: VB-E07, velobook-14-user-guide.pdf, KB-3001.

Grounded: Unsupported: Do not try to reset the laptop (The sources say do not reinstall Windows, and the manual says back up files before a factory reset, but nothing says not to reset for VB-E07. Resetting would wipe files, but that consequence is not stated for this error. This is an added instruction beyond the sources.)

```text
[met] VB-E07 means the SSD is not detected: The reply states 'Error VB-E07 means the SSD was not detected'.
[met] Do not reinstall Windows: The reply says 'Do not reinstall Windows' and repeats it in step 1.
[MISSED] Needs a repair; Veloria does not offer data recovery as part of warranty repairs: The reply says to request a repair, but it says nothing about Veloria not offering data recovery under warranty repairs. It instead implies support will help recover the files.
```

### S27 rep0: expected decline, got decline

Outcome ok: 1. Source ok: None. Cited: KB-2001.

Grounded: Unsupported: VeloGuard VPN is a client app that runs on your devices to connect them through a Veloria tunnel; it is not software installed on a router. (The sources say VeloGuard 6 uses the VeloTunnel protocol and mention the app's Settings, but nothing states it is a client app running on devices or that it is not installed on routers. The claim is not in the sources or the instructions, which only list VeloGuard VPN as a product.)

```text
[met] Says the sources do not cover a Linux router version: The reply says "The sources I have do not describe a VeloGuard version for Linux routers or any other router, so I cannot confirm whether one is available."
[met] Does not invent installation steps: The reply gives no installation steps or instructions; it only states a lack of source coverage.
```

