---
id: KB-3002
title: VeloBook battery drains quickly
product: VeloBook 14
category: troubleshooting
applies_to: VeloBook 14 and VeloBook 14 Pro on Windows 11
updated: 2026-05-11
status: published
---
# VeloBook battery drains quickly

Expected battery life is up to 12 hours for the VeloBook 14 and up to 10 hours for the 14 Pro at 150 nits brightness.

## Check battery health
Open **Veloria Control Center > Battery**. If **Full charge capacity** is below 80% of design capacity within warranty, see KB-5002.

## Reduce drain
1. Open **Settings > System > Power & battery > Battery usage** and find the top apps.
2. Switch the display from 120 Hz to 60 Hz.
3. Update BIOS to 1.18 or later, which fixes a standby drain problem (KI-124).
4. If VeloSync is using a lot of CPU, see KB-1004.

## Battery Care mode
Battery Care mode limits charging to 80% to extend battery lifespan. It is on by default for Enterprise devices. If your laptop stops charging at 80%, this is expected, not a fault. Turn it off in **Veloria Control Center > Battery**.
