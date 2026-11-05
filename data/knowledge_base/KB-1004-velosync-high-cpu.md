---
id: KB-1004
title: VeloSync uses high CPU after updating to 4.1
product: VeloSync
category: known-issue
applies_to: VeloSync 4.1.0 to 4.1.2 on Windows
updated: 2026-10-02
status: published
---
# VeloSync uses high CPU after updating to 4.1

## Symptoms
`VeloSyncService.exe` uses 40% or more CPU while idle and laptop fans run constantly. Only Windows is affected.

## Cause
The file-indexer in versions 4.1.0 to 4.1.2 rescans the whole library in a loop when the library holds more than about 100,000 files (known issue KI-118).

## Fix
Update to VeloSync **4.1.3** or later using **Settings > About > Check for updates**.

## Workaround if you cannot update
Add folders you rarely use to **Settings > Sync > Selective sync exclusions** to bring the file count below 100,000.

Do not disable the VeloSync service. Doing so stops sync silently and files will stop backing up.
