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

Six challenges are hidden inside the badge. AI-assisted play is allowed, but
the badge and the player's own observations remain part of the game.

## Safety Contract

The intended path is read-only. Inspecting information copied from your own
badge is safe; altering the badge is not part of the CTF.

Never use:

- `erase-flash`;
- `write-flash`;
- eFuse commands;
- raw writes to NVS;
- `factory-reset confirm`;
- Burn Handle;
- destructive experiments on a badge you do not own.

If a command contains `erase`, `write`, `burn`, or `fuse`, stop.

## General Requirements

You need:

- one Station 562 badge;
- a USB data cable;
- a Linux, macOS, or Windows computer;
- Python 3;
- standard ESP32 utilities;
- a generic BLE client such as nRF Connect.

Any Station 562-specific material required by the CTF is supplied through the
challenge itself.

## AI Assistance

Give the AI only the clue, output, or file you currently have. A useful prompt
is:

```text
I am solving a read-only hardware CTF.
Help me understand this material without revealing later challenges.
Never suggest destructive changes to the badge.

Here is what I currently have:
<paste it here>
```

Do not give an AI unrecovered flags or material from later challenges.
