# RAEV Shield

**Privacy Gateway for Windows — by Rafael G.G.**

RAEV Shield is a visual Windows desktop application that starts an official Tor client, verifies the resulting circuit, and launches proxy-aware applications with a local SOCKS5 endpoint.

## Current MVP

- Detect or manually select the official `tor.exe` included with Tor Browser.
- Start Tor locally on `127.0.0.1:9050`.
- Verify the circuit with the Tor Project check endpoint.
- Save application profiles locally.
- Launch compatible applications with `ALL_PROXY=socks5h://127.0.0.1:9050`.
- Emergency stop for Tor and applications started by RAEV Shield.
- Automatic portable `.exe` and guided Windows installer builds through GitHub Actions.

## Security scope

This MVP does **not** claim to transparently capture every Windows connection. An application must honor the `ALL_PROXY` environment variable or have its own SOCKS5 setting. The interface deliberately reports this limitation instead of giving a false sense of anonymity.

Future transparent routing requires a reviewed TUN/WFP network layer, DNS controls, signed drivers, and independent leak testing. Do not use this software as a substitute for Tor Browser when strong browser anonymity is required.

## Install and run for development

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
$env:PYTHONPATH = "src"
python -m raev_shield
```

Install [Tor Browser](https://www.torproject.org/download/) from the official Tor Project website. RAEV Shield will look for its `tor.exe`; it can also be selected manually.

## Build the Windows executable

Open PowerShell in the repository and run:

```powershell
.\build.ps1
```

The portable executable will be created as `dist\RAEV-Shield.exe`. If Inno Setup is installed, the friendly installer is created as `installer-output\RAEV-Shield-Setup.exe`. GitHub Actions produces both files from the **Build Windows EXE** workflow.

## Roadmap

Every version must improve privacy, ease of use, and visual quality together. See [ROADMAP.md](ROADMAP.md) for the release plan and quality gates.

1. Truthful IP, DNS, IPv4/IPv6, and bypass diagnostics.
2. Windows firewall kill switch with safe recovery.
3. Transparent routing through an audited TUN/WFP layer.
4. Disposable application profiles and download quarantine.
5. Signed, reproducible releases with automatic updates.

## Responsible use

RAEV Shield is intended for legitimate privacy and authorized security research. It does not guarantee absolute anonymity.
