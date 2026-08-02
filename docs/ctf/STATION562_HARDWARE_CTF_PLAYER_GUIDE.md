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

Six transmissions are hidden inside the badge. Every solved gate unlocks only
the files and instructions needed for the next gate.

The CTF welcomes AI-assisted play. Ask an AI to explain tools, command options,
binary formats, or an error message, but give it only the clue and files you
have actually unlocked. Real badge evidence is still required.

## Safety Contract

The intended path is read-only.

Allowed:

- read-only actions requested by the current recovered transmission;
- read-only copies of badge flash and files;
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

## Compatibility

You need one Station 562 badge, a USB data cable, and a computer capable of
running Python 3 and standard ESP32/BLE utilities. Linux, macOS, and Windows are
supported; no stage requires a macOS-only tool.

Install a tool or dependency only when a recovered transmission requests it.
Every custom Station 562 validator is recovered from the badge during play.
When the badge opens a physical signal window, follow its OLED prompts. The
interaction is deliberately forgiving and may be retried without penalty.

## Follow One Transmission At A Time

Use only the newest material you have legitimately recovered:

1. Read the current clue or output completely.
2. Open the exact file or path named by the newest recovered instruction.
3. Run a tool with `--help` before using it if any argument is unclear.
4. Preserve complete output and evidence files until the chain is finished.

Recovered tools operate on local copies and do not write back to the badge.

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
