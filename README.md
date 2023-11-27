
TLS-PROXY
=========

New Chrome/Chromium versions have removed TLS1.0 support arround verions 98.

But sometimes you have to connect to devices that are not yet upgraded or upgradeable to TLS 1.2
Google won't let you log into these devices, e.g. to upgrade those devices. Instead of asking
you they lock you out of these devices.

This simple small proxy is a TCP proxy that lets you connect via HTTP to this HTTPS devices
as long as your python3 libraries let you connetct to ths HTTPS ciphers used by the device.

Usage:

```
   python3 tls-proxy.py -p 9999 -d target.server:443
```

then open your browser and conenct to this server :9999

