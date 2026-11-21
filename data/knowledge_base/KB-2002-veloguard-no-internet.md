---
id: KB-2002
title: VeloGuard is connected, but websites or internal apps do not load
product: VeloGuard VPN
category: troubleshooting
applies_to: VeloGuard 6.x
updated: 2026-08-29
status: published
---
# VeloGuard is connected, but websites or internal apps do not load

## Nothing loads
1. Disconnect and reconnect to get a new tunnel.
2. Open **Settings > Connection** and lower **MTU** from 1420 to 1280. This fixes most cases where small pages load but large ones stall.
3. On Windows, run `ipconfig /flushdns` in Command Prompt.

## Public websites load, internal apps do not (VG-2100)
Split DNS is not being applied. Common cause: another VPN client, or a local DNS filter. Remove the other client's network adapter or disable the filter, then reconnect. VeloGuard 6.2.0 had a bug that ignored split DNS on Wi-Fi 7 adapters (KI-131), fixed in 6.2.1.

## Internal apps load, public websites do not
Your organization may use full tunnel with a web filter. Contact your IT admin. Support cannot change organization network policies.
