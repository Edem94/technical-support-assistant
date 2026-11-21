---
id: KB-2001
title: VeloGuard VPN will not connect
product: VeloGuard VPN
category: troubleshooting
applies_to: VeloGuard 6.x
updated: 2026-09-18
status: published
---
# VeloGuard VPN will not connect

VeloGuard 6 uses the WireGuard-based **VeloTunnel** protocol on UDP 51820, with fallback to TLS on TCP 443. Legacy L2TP is no longer supported.

## VG-619: Tunnel could not be established
A firewall is blocking UDP 51820. In the app, go to **Settings > Connection** and set **Protocol** to **TLS 443**. This is slower but works on most restricted networks, such as hotels.

## VG-691: Credentials rejected
Your Veloria ID password or MFA code was rejected. Sign out of VeloGuard and sign in again. If that fails, see KB-4002.

## VG-809: NAT or firewall interference
Common on home routers with SIP ALG or strict NAT. Restart the router, disable SIP ALG if available, or switch to **TLS 443**.

## VG-1003: Device certificate expired
Device certificates last 12 months. Select **Renew certificate** in the error dialog. Managed devices must be renewed by your IT admin.

## General checks
1. Confirm the internet works with the VPN off.
2. Update to VeloGuard 6.2.1 or later.
3. Pause third-party antivirus firewalls and test again.
4. Try a different network, such as a phone hotspot.
5. Run **Help > Export diagnostics** and attach the file to a support ticket.
