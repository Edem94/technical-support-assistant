---
id: KB-3004
title: Wi-Fi keeps disconnecting on VeloBook 14
product: VeloBook 14
category: known-issue
applies_to: VeloBook 14 with Wi-Fi driver 23.40
updated: 2026-09-25
status: published
---
# Wi-Fi keeps disconnecting on VeloBook 14

## Symptoms
Wi-Fi disconnects every few minutes, usually on 6 GHz networks, and reconnects on its own. Only VeloBook 14 models with driver 23.40 are affected (KI-127).

## Fix
Install Wi-Fi driver **23.60** or later from **Veloria Control Center > Updates**. Check the installed version in **Device Manager > Network adapters > Veloria AX7 Wireless > Driver**.

## Workaround
Connect to the 5 GHz network until you can update the driver.

## Other causes
1. Turn off **Allow the computer to turn off this device to save power** on the adapter's Power Management tab.
2. Forget the network and rejoin it.
3. Update your router's firmware.
