---
id: KB-1001
title: Install VeloSync and sign in for the first time
product: VeloSync
category: getting-started
applies_to: VeloSync 4.x on Windows 10/11 and macOS 13+
updated: 2026-08-12
status: published
---
# Install VeloSync and sign in for the first time

## Requirements
- Windows 10 22H2 or later, Windows 11, or macOS 13 or later.
- At least 2 GB of free disk space, plus room for any files kept offline.
- A Veloria ID. Business users sign in with their work email.

## Steps
1. Download the installer from the VeloSync page in your Veloria account portal.
2. Run the installer. Administrator rights are only needed for the "All users" option.
3. When the app opens, select **Sign in** and complete sign-in in your browser.
4. Choose a local folder. The default is `C:\Users\<name>\VeloSync` on Windows and `~/VeloSync` on macOS.
5. Choose **Online-only** (saves disk space) or **Keep offline** (full local copy).

The folder must be on an internal NTFS or APFS drive. Network shares and exFAT drives are not supported.

## If sign-in fails
- If the browser never returns to the app, set your default browser again and retry.
- For error VS-1310, see KB-1002.
- For Veloria ID errors starting with `ID-`, see KB-4002.
