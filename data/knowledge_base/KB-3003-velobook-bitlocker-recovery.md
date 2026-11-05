---
id: KB-3003
title: BitLocker recovery key prompt after a BIOS update
product: VeloBook 14
category: troubleshooting
applies_to: VeloBook 14 and VeloBook 14 Pro with Windows 11 Pro
updated: 2026-10-14
status: published
---
# BitLocker recovery key prompt after a BIOS update

After a BIOS update Windows may ask for a 48-digit BitLocker recovery key. This is a security feature: the device measurements changed.

## Find the key
- **Personal devices:** sign in to your Microsoft account on another device and look under devices and BitLocker recovery keys.
- **Work devices:** contact your IT admin. Veloria support does not hold BitLocker keys.

## After entering the key
Windows usually starts normally and does not prompt again.

## If you cannot find the key
Do not reinstall Windows or reset the laptop: this permanently erases the encrypted data. Without the key, nobody can recover the drive, including Veloria support. Escalate through KB-5001 so an agent can review options with you.

## Avoiding this
Before a BIOS update, suspend BitLocker from **Control Panel > BitLocker Drive Encryption > Suspend protection**. It resumes after restart.
