# Station 562 Hardware CTF

Release: Station 562 `V6.3.0`.

```text
STATION 562 // FIRST CONTACT

A NUMBER STATION IS WAITING.
ITS FIRST TRANSMISSION IS NOT ON THE AIR.
FOLLOW THE WIRE.
ASK WHAT THE STATION CAN DO.
TUNE IT TO THE NUMBER IT WEARS.
```

Six transmissions are hidden inside the badge. The trail begins with ordinary
USB serial discovery. Every solved gate unlocks only the files and instructions
needed for the next gate.

The CTF welcomes AI-assisted play. Ask an AI to explain tools, command options,
binary formats, or an error message, but give it only the clue and files you
have actually unlocked. Real badge evidence is still required.

## Safety Contract

The intended path is read-only.

Allowed:

- USB serial commands;
- `esptool read-flash`;
- offline inspection of copied files;
- one read-only BLE connection-state check when a recovered instruction
  requests it;
- read-only Station 562 validators recovered from the badge.

Never use:

- `erase-flash`;
- `write-flash`;
- eFuse commands;
- raw writes to NVS;
- `factory-reset confirm`;
- Burn Handle;
- destructive experiments on a badge you do not own.

If a command contains `erase`, `write`, `burn`, or `fuse`, stop.

## Initial Tools

You need:

- one Station 562 badge and a USB data cable;
- Python 3;
- a serial terminal;
- Espressif `esptool`;
- nRF Connect or another BLE client for the later live-link stage.

Create a working directory and Python environment:

```bash
mkdir station562-ctf
cd station562-ctf
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install esptool pyserial
```

On Windows PowerShell, activate with
`.venv\Scripts\Activate.ps1` and use `py -3` instead of `python3` if needed.

Later stages may identify another standard tool or dependency. Install it only
when the current recovered instructions request it. Every custom Station 562
validator is recovered from the badge during play.

## Find The Badge

List likely USB ports:

```bash
# macOS
ls /dev/cu.usbmodem*

# Linux
ls /dev/ttyACM* /dev/ttyUSB*

# Windows PowerShell
[System.IO.Ports.SerialPort]::GetPortNames()
```

If several ports appear, compare the list before and after reconnecting the
badge. The new port is normally the badge.

Open a cross-platform terminal at 115200 baud:

```bash
python3 -m serial.tools.miniterm PORT 115200
```

Press Enter, type `help`, and read the full command list. Exit miniterm with
`Ctrl+]`.

The opening transmission tells you what kind of command to look for and what
value belongs in it. When the badge opens a physical signal window, follow its
OLED and terminal prompts. The interaction is deliberately forgiving and may
be retried without penalty.

## Follow One Transmission At A Time

Use only the newest material you have legitimately recovered:

1. Read the current terminal output completely.
2. Open the exact file or path named by the newest recovered instruction.
3. Run a tool with `--help` before using it if any argument is unclear.
4. Preserve complete output and evidence files until the chain is finished.

Recovered tools operate on local copies and do not write back to the badge.

## USB Port Conflicts

Only one program can normally own the serial port. Close the serial terminal
before using `esptool`. Reopen the terminal after `esptool` finishes and the
badge reboots.

If a port is busy on macOS or Linux:

```bash
lsof PORT
```

Close only the process that owns that badge port.

## Ask For Help Without Skipping The Game

A useful AI or help-desk request is:

```text
I am solving a read-only ESP32 hardware CTF.
Explain this clue or command before I run it.
Do not suggest erase-flash, write-flash, eFuse writes, factory reset,
Burn Handle, or live NVS modification.
Here is the latest material I have unlocked:
<paste it here>
```

The challenge is the engineering path, not wrestling with undocumented file
names or hidden command syntax. Each accepted stage supplies the operational
details for the next one.
