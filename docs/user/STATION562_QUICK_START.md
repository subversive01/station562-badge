# Station 562 V6.3.0 Quick Start

Station 562 is a proximity-controlled badge with a BLE number-station puzzle,
a red-versus-blue proximity game, an autonomous social/dance mode, an
expressive BLE MIDI instrument, a tamper-evident mode, a Setup menu, and an
optional hardware CTF.

Your badge is delivered flashed and functional. It does not need a phone for
normal use, Signal Clash, or DeFUNKd.

## Mode Names In Plain English

The badge uses themed names on its OLED and over BLE. Here is what each one
actually does:

| On-screen name | Plain-language purpose |
| --- | --- |
| **STATION 562** | Default number-station puzzle transmitter |
| **CONTROL ROOM** | Alternate animated face for the same puzzle transmitter |
| **SIGNAL CLASH** | Persistent RED-versus-BLUE proximity game |
| **DeFUNKd** | Autonomous social/dance mode that reacts to nearby badges |
| **MIDI CONTROLLER** | Touchless Bluetooth instrument for a synth, DAW, or app |
| **DEFUNKT562** | Tamper-evident blackout/alert mode |
| **SERVICE CHANNEL** | Owner Setup menu |

**DeFUNKd and DEFUNKT562 are different modes.** DeFUNKd is the casual
autonomous social mode. DEFUNKT562 is the intentionally harder-to-exit
tamper-evident mode.

## First Minute

1. Power the badge and wait for the **STATION 562** screen.
2. Keep the sensor clear while the badge starts.
3. Hold a hand over the top sensor for about two seconds.
4. Release when the screen changes to **CONTROL ROOM**.
5. Repeat the same two-second hold to return.

The badge normally advertises over BLE as `STATION_562`. The OLED shows puzzle
clue IDs; the complete rotating puzzle payload is transmitted over BLE.

## Sensor Gestures

The proximity and light sensor is near the top of the badge.

- **Hold:** move a hand close and keep it steady.
- **Swipe:** move far to close, then completely away.
- **Double swipe:** perform two separate far-close-far swipes.

Fully uncover the sensor between swipes. Deliberate gestures are more reliable
than extremely fast passes.

## Main Hold Ladder

Start from the normal Station 562 or Control Room face. Keep the sensor covered
and watch each loading screen. Release at the desired completed step.

| Hold time | Selection |
| ---: | --- |
| 2 seconds | Switch Station 562 / Control Room face |
| 4 seconds | Signal Clash, then double swipe |
| 6 seconds | DeFUNKd autonomous social mode |
| 8 seconds | MIDI Controller, then double swipe |
| 10 seconds | DEFUNKT562 tamper mode, then double swipe |
| 12 seconds | Setup / Service Channel, then double swipe |

If a confirmation appears by mistake, move your hand away and let it time out.

## Signal Clash

Signal Clash is the persistent red-versus-blue roaming game. Enter at the
four-second hold cue and double swipe when asked.

On first entry, the badge creates a persistent player identity, automatic
hacker handle, signing keypair, and initial team. That career survives reboots
and ordinary firmware updates.

### Objective

Find a nearby opposing badge, attack it, defend your own team, earn REP, and
capture unique opponents. A successful capture converts the target to the
attacker's team.

### Roaming Screen

The display rotates through:

1. handle and rank;
2. REP, unique captures, discipline, and Heat;
3. team and rank.

After one minute without gameplay, it settles on the identity screen and uses
two faint team-color LED pulses every five seconds. The radio and sensor remain
active. On XIAO hardware, white LEDs represent the BLUE team.

### Attack

The badge automatically locks the strongest qualified opposing signal.

1. Wait for a target screen.
2. Move your hand far to close, then pull it completely away.
3. Watch the large success or failure result.

Three acknowledged Port Scan attacks charge **0.DAY**, the stronger attack.
Extremely close, stable opponents automatically qualify the same gesture as
**Covert Intrusion**, which awards bonus REP when credited.

### Defend

When an attack arrives, the OLED asks you to choose:

- **FIREWALL:** move close and hold steady while aligning the ring guide.
- **EVADE:** swipe once to start the timing marker, then swipe once more to
  commit its position.

The result screen clearly reports success or failure.

### Exit

1. Hold very close for five seconds.
2. The full-screen **KEEP HOLD** progress appears after three seconds.
3. Release when asked.
4. Double swipe within four seconds.

Signal Clash always returns to normal Station 562 operation after a confirmed
exit.

## DeFUNKd: Autonomous Social Mode

Release at the six-second cue. DeFUNKd is the badge's automatic social/dance
mode: it notices nearby badges and changes its group animation without pairing
or user setup. No phone or internet connection is required. It works alone in
SOLO and becomes more social as other DeFUNKd badges appear:

| Stable badges nearby, including yours | State |
| ---: | --- |
| 1 | SOLO |
| 2 | BATTLE |
| 3 | CYPHER |
| 4 | DJ / HYPE CREW |
| 5 or more | DANCE FLOOR |

Changes are intentionally stabilized, so joining or leaving can take several
seconds. Hold the sensor for about three seconds to exit DeFUNKd.

### Clock And Signal Party

A Station 562 badge in MIDI Controller Mode can receive MIDI Clock and
broadcast its beat to nearby DeFUNKd badges. Clock alone only synchronizes the
existing OLED and LED animations.

An operator may deliberately transmit **SIGNAL HACKED**. Eligible followers
show **SIGNAL HACKED / CURIOUS?**:

- double swipe to accept the synchronized party experience;
- ignore it to remain in normal DeFUNKd.

The same conductor can send **SIGNAL RESTORED** to return accepted followers to
DeFUNKd SOLO while the clock continues.

### Operator: Trigger The Party With nRF Connect

nRF Connect can send the event command, but it does **not** create MIDI Clock.
Before using nRF Connect, the conductor badge must already be in MIDI
Controller Mode with a BLE MIDI host sending Clock Out, transport running, and
a nonzero BPM. Put the follower badges in DeFUNKd.

1. In nRF Connect, connect to the conductor named `S562_MIDI`.
2. Open the Station 562 config service ending in `5620`.
3. Enable notifications on the result characteristic ending in `5625`.
4. Choose **Write** on command characteristic `5624` and select UTF-8/text.
5. Send:

```json
{"schema":"station562.badge.config.command.v1","seq":1,"command":"signal hacked"}
```

6. Look for a matching `seq:1` result with `invitation_started` or
   `invitation_active`.
7. To end the accepted party while clock continues, use a fresh sequence:

```json
{"schema":"station562.badge.config.command.v1","seq":2,"command":"signal restored"}
```

8. Look for matching `seq:2` with `restoration_started` or
   `restoration_active`.

These two commands are public and do not open **ACCESS REQUEST**. Do not reuse
the same sequence number for consecutive writes on one connection. A
`clock_required` result means Clock Out or host transport is not currently
running. The complete UUIDs and troubleshooting codes are in the
[Terminal And BLE Command Reference](STATION562_TERMINAL_AND_BLE_REFERENCE.md).

## MIDI Controller

1. Release at the eight-second cue.
2. Double swipe to confirm.
3. In a Bluetooth MIDI connection panel, connect to `S562_MIDI`.
4. Select it as the MIDI input for a synth, DAW, sampler, or companion app.
5. Move your hand through the sensor range to perform.

The badge sends MIDI; it does not contain a sound engine.

The factory preset is **Carrier**:

- approach speed controls Note On velocity;
- strike depth selects pitch;
- held proximity sends filter, movement, expression, and pressure data;
- withdrawal speed shapes release expression before Note Off.

Carrier uses ordinary MIDI 1.0 messages. A receiving instrument must map or
respond to those controls for every expressive lane to be audible.

The default musical map is C3 through C4 in C minor on MIDI channel 1. The
advanced guide explains presets, transposition, tuning, scenes, and terminal
commands.

If the host disconnects, the badge allows 45 seconds to reconnect before
offering an exit:

- double swipe within four seconds to exit;
- hold close for about 1.5 seconds to stay.

With no host and no activity, MIDI Controller exits after about two minutes.

## DEFUNKT562: Tamper-Evident Mode

DEFUNKT562 is a deliberate tamper-evident blackout mode, not an everyday
display mode and not the DeFUNKd autonomous social mode.

1. Release at the ten-second cue.
2. Double swipe to confirm.
3. Leave the badge undisturbed during its 30-second placement calibration.

The badge is BLE silent while calibrating and armed. A qualifying proximity or
light disturbance triggers the alert identity `562_ALERT!`.

The protected owner-recovery sequence is in the advanced guide.

## Setup

1. Release at the twelve-second cue.
2. Double swipe to enter.
3. Short swipe to move through items or choices.
4. Hold for two seconds to select or save.

Setup can contain:

1. LED BRIGHTNESS
2. STATION 562 LED
3. CONTROL ROOM LED
4. SIGNAL CLASH TEAM
5. REQUEST INDUCTION, when the player is ROOT-eligible
6. ROOT INDUCTION, when the ROOT badge can sponsor or witness
7. RESTORE DEFAULTS
8. REBOOT BADGE
9. BURN HANDLE
10. RETURN TO STATION

Conditional ROOT items appear only when they apply.

**RESTORE DEFAULTS** resets ordinary LED preferences. **BURN HANDLE** is the
whole-badge player reset: it erases Setup and MIDI preferences plus the Signal
Clash handle, career, keypair, team, and ROOT certificate, then reboots. It does
not change the immutable hardware badge ID or erase the CTF archive.

## Software Standby

From a normal Station 562 face, perform five short swipes within nine seconds.
The OLED and BLE turn off; one faint red heartbeat flashes for about 40 ms
every ten seconds. Repeat the five-swipe gesture to wake.

This is software standby, not a hardware power switch or ESP deep sleep. It
still consumes battery.

## BLE Names

| Mode | Advertised name or state |
| --- | --- |
| Station 562 puzzle | `STATION_562` |
| Signal Clash | `SIGNAL_CLASH` |
| DeFUNKd | `DEFUNKD_562` |
| MIDI Controller | `S562_MIDI` |
| ROOT induction | `S562 INDUCTION` |
| DEFUNKT562 armed | BLE silent |
| DEFUNKT562 alert | `562_ALERT!` |
| Software standby | BLE off |

Changing modes changes BLE ownership. A badge that disappears under one name
may have reappeared under another.

## Optional Hardware CTF

The badge also contains a six-stage, read-only hardware CTF. The event opening
statement leads players to the USB terminal and the first transmission. The
safe starting guide is
[Station 562 Hardware CTF Player Guide](../ctf/STATION562_HARDWARE_CTF_PLAYER_GUIDE.md).

The CTF never requires erasing or writing player flash. Do not run destructive
flash commands.

## Quick Troubleshooting

- **A gesture is missed:** fully uncover the sensor, pause, and repeat more
  deliberately.
- **No MIDI sound:** connect through the app's Bluetooth MIDI panel, select
  `S562_MIDI` as an input, and arm an audible instrument.
- **Clock is present but BPM is blank:** stop and restart host transport after
  connecting.
- **nRF returns `clock_required`:** nRF sent the command correctly, but the
  conductor is not receiving active MIDI Clock. Start Clock Out and host
  transport first.
- **nRF shows no command result:** enable notifications on `5625`, write
  UTF-8/text to `5624`, and match the notification sequence to the sequence
  you sent.
- **No DeFUNKd peer appears:** confirm every participating badge is actually in
  DeFUNKd and allow several seconds for stabilization.
- **No Signal Clash target appears:** the other badge must be in Signal Clash,
  on the opposing team, and within radio range.
- **ACCESS REQUEST appears:** a connected app requested protected
  configuration. Double swipe only if you trust it; disconnecting revokes
  authorization.
- **The badge seems stuck:** use the current mode's exit gesture. MIDI can also
  exit through the USB command `midi exit`.
- **Battery drains in standby:** expected. Software standby is not power-off.

For complete Signal Clash mechanics, MIDI configuration, BLE services, terminal
access, persistence, and recovery, continue with the
[Advanced Owner Guide](STATION562_ADVANCED_OWNER_GUIDE.md) and
[Terminal And BLE Command Reference](STATION562_TERMINAL_AND_BLE_REFERENCE.md).
