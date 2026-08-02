# Station 562 Self-Flash Guide

This guide installs official Station 562 firmware and the matching hardware CTF
with the supplied updater.

## What The Normal Update Preserves

The default updater writes one target-specific release bundle containing the
official firmware and included CTF.

It does not erase or write the NVS region that stores the owner handle, Signal
Clash career, team, settings, keypair, or ROOT certificate.

`factory-reset confirm` and Setup **BURN HANDLE** are separate destructive
actions. They are never issued by this updater.

## Requirements

- macOS, Linux, or Windows;
- Python 3.9 or newer;
- a USB data cable;
- one connected Station 562 badge;
- this repository downloaded or cloned locally.

## 1. Prepare Python

From the repository folder, create an isolated environment.

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2. Find The Badge Port

Close every serial monitor first, then run:

```bash
python tools/flash_station562.py --list
```

Typical ports:

- macOS: `/dev/cu.usbmodem...`
- Linux: `/dev/ttyACM0` or `/dev/ttyUSB0`
- Windows: `COM5`

If several appear, disconnect the badge, list again, reconnect it, and use the
new entry.

## 3. Run A Normal Update

```bash
python tools/flash_station562.py --port YOUR_PORT
```

Examples:

```bash
python tools/flash_station562.py --port /dev/cu.usbmodem1101
```

```powershell
python tools\flash_station562.py --port COM5
```

The updater will:

1. verify every bundled file against the release manifest;
2. ask Espressif's ROM loader whether the badge is ESP32-C3 or ESP32-C6;
3. select the matching CodeCell or XIAO application;
4. show the exact write plan;
5. ask for confirmation;
6. write the selected update bundle without erasing NVS;
7. verify the installed bundle;
8. reboot the badge.

Do not unplug the badge during steps 6 or 7.

## 4. Confirm The Version

Open a terminal at 115200 baud:

```bash
python -m serial.tools.miniterm YOUR_PORT 115200
```

Press Enter and run:

```text
version
```

Expected fields include:

```text
"firmware":"V6.3.0"
"hardware":"CODECELL_ESP32C3"
```

or:

```text
"firmware":"V6.3.0"
"hardware":"XIAO_ESP32C6"
```

Exit miniterm with `Ctrl+]`.

## Platform Recovery

The public updater deliberately does not replace bootloader or partition-table
data. Use the hardware-specific ROM bootloader procedure below if the normal
update cannot connect. Do not run a full-chip erase or mix files from another
target.

### XIAO ESP32-C6

1. Disconnect USB and switch off or disconnect the battery.
2. Press and hold **BOOT**.
3. Reconnect the USB data cable while continuing to hold **BOOT**.
4. Release **BOOT** after the computer detects the device.
5. Run `python tools/flash_station562.py --list`, then flash the detected port.

With USB already connected, the equivalent sequence is to hold **BOOT**, press
and release **RESET**, then release **BOOT**.

### CodeCell ESP32-C3

CodeCell normally enters download mode automatically. If it is stuck in a
reset loop or cannot be detected:

1. Disconnect USB and switch off or disconnect the battery.
2. With the badge unpowered, connect CodeCell **SCL** to **GND** with a jumper.
   On CodeCell, SCL is ESP32-C3 GPIO9, the ROM boot strap pin.
3. Reconnect USB while leaving the jumper in place.
4. Run `python tools/flash_station562.py --list`, then flash the detected port.
5. After the updater finishes, disconnect USB, remove the SCL-to-GND jumper,
   and restore normal power.

If the ESP32 ROM loader still does not appear after the applicable procedure,
this updater cannot recover the badge.

## Dry Run

To verify the package, detect the target, and print the plan without writing:

```bash
python tools/flash_station562.py --port YOUR_PORT --dry-run
```

## Troubleshooting

### Port Busy

Close Arduino Serial Monitor, `screen`, miniterm, nRF Connect, and any program
that may own the badge port.

### No Serial Port

- confirm the cable supports data;
- reconnect the badge;
- avoid unpowered hubs;
- try another USB port;
- rerun `--list`.

### Wrong Target

The updater refuses unknown ESP32 families. Do not rename or manually exchange
CodeCell and XIAO images.

### Interrupted Update

Reconnect the badge and rerun the same command. If the updater can no longer
identify the target through the ESP32 ROM loader, use **Platform Recovery**
above. If the ROM loader remains unavailable, this updater cannot recover the
badge.

### Identity Appears Missing

Stop before issuing any reset command. The updater does not erase NVS. Record
the exact updater output. Reflashing cannot reconstruct owner data that was
previously erased.

## CTF Safety

The CTF is installed automatically and its intended path is read-only. Never
improvise writes, erases, eFuse changes, Burn Handle, or factory reset while
playing.
