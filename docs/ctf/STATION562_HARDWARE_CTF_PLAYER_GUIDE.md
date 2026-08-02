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

## MMO Rewards

The Station 562 badge is connected to the DC562 DEF CON MMO: mmo.lockboxx.org.

In the game, find the NPC named `n+1` at the house party in Act 3, if you can
make it that far. His in-game digital badge grants access to the party and
mirrors the real Station 562 badge.

To redeem a reward:

1. Recover a codeword by solving one of the badge's CTF challenges.
2. Find `n+1` at the house party in Act 3.
3. Give the recovered codeword to `n+1`.
4. Receive the associated loot.

Rewards may include equipment, cards, and other items that make your character
stronger in the MMO. Record each codeword exactly as it appears. Codewords may be case-sensitive.

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
