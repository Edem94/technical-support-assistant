---
id: KB-1002
title: VeloSync is stuck on "Syncing" or shows an error
product: VeloSync
category: troubleshooting
applies_to: VeloSync 4.x
updated: 2026-09-03
status: published
---
# VeloSync is stuck on "Syncing" or shows an error

Open the tray or menu bar icon and select **Activity** to see which file is blocking the queue and which error code it shows.

## VS-1042: Path too long
The full path exceeds 260 characters on Windows. Shorten folder names or move the file closer to the root of the VeloSync folder. On Windows 11 you can instead enable long paths under **Settings > Advanced > Long path support** (VeloSync 4.0 or later).

## VS-1107: Storage quota exceeded
Your plan's storage is full and uploads are paused. Downloads continue. Empty the VeloSync web trash, delete large files, or ask your admin for more storage. Plan storage is: Personal 200 GB, Team 2 TB per user, Enterprise 5 TB per user.

## VS-1203: File locked
Another application has the file open. Close it and sync resumes within 60 seconds. For Outlook `.pst` files, exclude them from sync: VeloSync does not support syncing open mail archives.

## VS-1310: Session expired
Select **Sign in again**. If it recurs daily, your organization probably enforces a short session policy; contact your admin.

## VS-1618: Unsupported characters
Rename files containing `< > : " | ? *`, or ending in a space or period.

## If no error is shown
1. Pause sync and resume it.
2. Quit VeloSync and reopen it.
3. Check status.veloria.example for an outage.
4. Run **Settings > Advanced > Rebuild local index**. This takes up to an hour for large libraries and does not delete files.
