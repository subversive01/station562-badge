# STATION 562 // BADGE RELEASES

```text
+--------------------------------------------------------+
| [ CONTROL ROOM ]                         [STATION 562] |
|========================================================|
|                                                        |
| OP-A     +--------+  +--------+  +--------+      OP-B  |
|  o       | CH 562 |  | TX >>> |  | RX ... |       o    |
| /|\      +--------+  +--------+  +--------+      /|\   |
| / \       [..::..]    [######]    [..::..]       / \   |
|========================================================|
| CH ACTIVE      SIGNAL LOCKED      TX BURST       S562  |
+--------------------------------------------------------+
```

Binary releases, owner documentation, and safe self-flashing tools for the
Station 562 badge.

**Current production release: `V6.3.0`**

## Start Here

- [Quick Start](docs/user/STATION562_QUICK_START.md)
- [Advanced Owner Guide](docs/user/STATION562_ADVANCED_OWNER_GUIDE.md)
- [Terminal and BLE Reference](docs/user/STATION562_TERMINAL_AND_BLE_REFERENCE.md)
- [Hardware Pinout](docs/HARDWARE_PINOUT.md)
- [Self-Flash Guide](docs/SELF_FLASH_GUIDE.md)
- [Hardware CTF Player Guide](docs/ctf/STATION562_HARDWARE_CTF_PLAYER_GUIDE.md)
- [AI-Assisted CTF Play](docs/ctf/STATION562_HARDWARE_CTF_AI_PLAY.md)
- [V6.3.0 Release Notes](docs/firmware/V6.3.0_RELEASE_NOTES.md)

## Supported Badges

The updater detects the ESP32 family and selects the correct build:

| Badge | Processor | Release image |
| --- | --- | --- |
| CodeCell | ESP32-C3 | CodeCell V6.3.0 update bundle |
| Seeed Studio XIAO | ESP32-C6 | XIAO V6.3.0 update bundle |

Never manually swap the two update bundles.

The [Hardware Pinout](docs/HARDWARE_PINOUT.md) is also included for owners who
want to write independent firmware and repurpose the badge for another project.
Custom firmware is separate from the supported Station 562 release and should
be developed with care around the existing flash layout and 3.3 V hardware.

## Flash V6.3.0

You need Python 3, a USB data cable, and the badge.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/flash_station562.py --list
python tools/flash_station562.py --port YOUR_PORT
```

On Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python tools\flash_station562.py --list
python tools\flash_station562.py --port COM5
```

The normal update installs one target-specific production bundle containing the
firmware and matching CTF. It preserves the badge's handle, team, career,
settings, keypair, and ROOT certificate.

## The CTF

The complete signed six-stage hardware CTF is included in the release image.
Flashing through this repository installs it automatically.

The public documentation explains safe play and how to begin. It does not
publish answers or skip the chain. Every later custom tool and instruction is
recovered from the badge only after the preceding gate is solved.

Start with the [Hardware CTF Player Guide](docs/ctf/STATION562_HARDWARE_CTF_PLAYER_GUIDE.md).

## Important Safety Rules

- Do not run `erase-flash` for an ordinary update.
- Do not run `factory-reset confirm` unless you intentionally want to erase the
  owner identity and Signal Clash career.
- Do not use eFuse commands.
- Do not unplug the badge while a write is active.
- Close serial terminals, Arduino monitors, and BLE tools before flashing.
- The updater verifies the selected bundle before and after writing.

## Release Integrity

Public V6.3.0 update-bundle hashes:

```text
CodeCell bundle  3d1069d8d82cd5b670ef0365bf212832db94a24af1092e8eff2a4ea1cfa60703
XIAO bundle      7fc2f5db7cb560ffbe3789f769cd161b7c57936d0778f7d2706a920c539c0da7
```

The complete image manifest is at
[`firmware/v6.3.0/manifest.json`](firmware/v6.3.0/manifest.json).
