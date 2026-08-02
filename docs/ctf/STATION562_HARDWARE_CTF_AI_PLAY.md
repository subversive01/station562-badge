# AI-Assisted Station 562 CTF Play

Audience: player-facing.

AI assistance is allowed and expected. The challenge is designed so an AI can
teach the underlying engineering without replacing the physical player.

## Good AI Prompt

```text
I am solving a read-only hardware CTF on an ESP32-C3/C6 badge.
Help me understand each command before I run it.

Hard safety rules:
- Never propose erase-flash, write-flash, eFuse writes, factory reset,
  Burn Handle, or live NVS modification.
- Prefer read-flash and offline parsing.
- Explain offsets, lengths, endianness, checksums, and cryptography.
- Do not invent sensor values or BLE packets.
- Ask me to provide the real output from my badge before continuing.

Here is my current clue/output:
<paste it here>
```

## What AI Can Help With

- finding and opening a serial port;
- explaining the current clue's standard hardware tool or data format;
- reviewing command options before the player runs them;
- interpreting read-only evidence already recovered from the badge;
- explaining cryptographic verification without revealing a solution;
- diagnosing a failed validator without destructive commands.

## What The Human Must Supply

- a real badge and USB connection;
- every physical action requested by an unlocked stage;
- every live hardware or radio observation requested by an unlocked stage;
- exact read-only files copied from the player's target badge.

AI should be a patient engineering partner, not a flag oracle.
Give it only the newest clue and files the player has legitimately unlocked;
do not provide unrecovered clues, flags, or future-stage material.
