# Station 562 V6.3.0 Advanced Owner Guide

This guide documents the complete owner-facing behavior of Station 562 firmware
V6.3.0: physical interaction, operating modes, Signal Clash, DeFUNKd, BLE MIDI,
instrument tuning, persistence, Setup, terminal and GATT access, recovery, the
optional hardware CTF, and known hardware limits.

It does not disclose puzzle answers, CTF flags, private operator keys, or hidden
easter-egg unlock sequences. Manufacturing and developer-only material is kept
outside this repository.

## 1. What Station 562 Is

Station 562 combines several separate systems in one badge:

- the normal Station 562 puzzle transmitter and OLED faces,
- the persistent Signal Clash red-versus-blue roaming game,
- DeFUNKd autonomous social/dance behavior between nearby badges,
- a standard MIDI 1.0 controller over Bluetooth Low Energy,
- clock-synchronized DeFUNKd timing and SIGNAL HACKED party visuals,
- DEFUNKT562 tamper-evident blackout/alert behavior,
- a protected physical Setup menu,
- software standby,
- terminal and protected Config GATT maintenance surfaces,
- an optional six-stage read-only hardware CTF.

These are separate operating modes. BLE ownership changes between them so the
puzzle advertiser, DeFUNKd scanner, BLE MIDI service, and DEFUNKT562 radio state
do not compete with one another.

The badge does not contain a sound engine. MIDI Controller sends musical
control data to a synth, DAW, sampler, or companion app that creates the sound.

### Mode Names In Plain English

| Firmware/display name | What an owner should expect |
| --- | --- |
| Station 562 | Default number-station puzzle transmitter |
| Control Room | Alternate animated face for the same puzzle |
| Signal Clash | Persistent RED-versus-BLUE proximity game |
| DeFUNKd | Autonomous social/dance mode driven by nearby badge count |
| MIDI Controller | Touchless BLE MIDI performance instrument |
| DEFUNKT562 | Tamper-evident blackout and alert mode |
| Service Channel | Physical Setup menu |

DeFUNKd and DEFUNKT562 are intentionally styled names for unrelated modes.
DeFUNKd is casual and social; DEFUNKT562 is a protected tamper mode.

## 2. Hardware Variants

The same production sketch supports two physical targets, but it compiles to a
different binary for each target.

| Feature | CodeCell ESP32-C3 | XIAO ESP32-C6 |
| --- | --- | --- |
| Hand/light sensor | CodeCell light/proximity system | VCNL4040 proximity, ambient, and white-light sensor |
| LEDs | 16 addressable RGB LEDs | 5 PWM red/white LED channels mapped from a 16-position logical layout |
| Default MIDI note proximity | 30-410 | 30-550 |
| Default MIDI expression proximity | 0-420 | 30-410 |
| Default MIDI gate enter/exit | 100/80 | 50/24 |
| `white` expression source | Ambient-light fallback | VCNL4040 white-light reading |

The user-facing hold times, mode order, OLED flow, BLE contracts, MIDI features,
and saved-setting behavior are intended to match across both targets. Sensor
ranges and LED rendering differ because the hardware differs.

## 3. Sensor Language

Station 562 has no conventional menu button. The hand sensor is the control.

- **Cover:** place a hand in the active sensor range.
- **Hold:** keep the sensor covered without leaving the range.
- **Swipe:** cover briefly, then fully uncover.
- **Double swipe:** perform two deliberate cover-and-release swipes, leaving a
  short clear gap between them.

Short swipes normally select or confirm. Long holds normally enter, save, or
advance through the main hold ladder. A cover longer than the allowed swipe
duration is not counted as a swipe.

If a gesture is missed:

1. Move your hand completely away.
2. Pause briefly.
3. Repeat with a slower, deliberate cover and release.

## 4. Normal Station 562 Operation

After boot, the badge enters the **STATION 562** face and advertises as
`STATION_562`.

The normal BLE advertisement contains rotating puzzle information. The clue
changes every 30 seconds. The OLED deliberately shows only the clue ID, not the
full transmitted clue payload.

The two normal OLED faces are:

- **STATION 562:** station name, channel status, TX/RX activity, and moving clue
  ID.
- **CONTROL ROOM:** an animated operator/control-room view with the same channel
  and clue activity.

Cover the sensor for about two seconds to switch faces, then release.

## 5. Main Hold Ladder

The hold ladder begins only from normal Station 562 or Control Room operation.
The OLED loading sequence is the timing guide.

| Elapsed hold | Loaded selection | Release behavior |
| --- | --- | --- |
| 0-2 seconds | Transmission detected | No mode entry |
| 2-4 seconds | Face switch completed | Remain on the newly selected face |
| 4-6 seconds | Signal Clash | Open the Signal Clash double-swipe confirmation |
| 6-8 seconds | DeFUNKd autonomous social mode | Enter DeFUNKd immediately |
| 8-10 seconds | MIDI Controller Mode | Open the MIDI double-swipe confirmation |
| 10-12 seconds | DEFUNKT562 tamper mode | Open the DEFUNKT562 double-swipe confirmation |
| 12 seconds or longer | Service Channel | Open the Setup double-swipe confirmation |

The release selects the latest fully loaded item. The two-second face switch may
occur while you continue holding toward a deeper mode; this is expected.

Confirmation windows time out safely if no valid swipes are received.

## 6. DeFUNKd Autonomous Social Mode

### Enter And Exit

Enter by releasing between six and eight seconds on the main hold ladder.
DeFUNKd is an automatic social/dance mode: the badge changes its OLED and LED
behavior according to how many nearby badges are also in DeFUNKd. It requires
no phone, pairing, internet access, or user configuration.

Exit by holding the sensor continuously for about three seconds. The badge
returns to normal Station 562 behavior.

### How Nearby Badges Interact

DeFUNKd is advertisement-only: each badge repeatedly broadcasts a small
Station 562 packet and listens for the same packet from nearby badges. The
badges do not pair and do not open direct GATT connections to one another.

| Stable badges in range, including self | State |
| ---: | --- |
| 1 | SOLO |
| 2 | BATTLE |
| 3 | CYPHER |
| 4 | DJ |
| 5 or more | DANCE FLOOR |

Transitions are intentionally stabilized. New peers must remain close long
enough to qualify, and a departed peer is not removed instantly. Visible state
changes can therefore take several seconds. When a larger gathering collapses
to one badge, AFTER PARTY and COOLDOWN can play before SOLO.

The firmware tracks at most ten nearby peer records. Very large-room behavior
remains best-effort because advertisement loss, radio congestion, and slightly
different peer visibility are unavoidable in a crowded venue.

### External Clock, SIGNAL HACKED, And SIGNAL RESTORED

While DeFUNKd is active, it can detect Station 562 clock advertisements from a
MIDI Controller badge receiving standard MIDI Clock. A current, running clock
changes only the visual time base: existing OLED and LED motion follows the
beat while the normal DeFUNKd state machine continues unchanged. Clock packets
alone never request Party entry.

The conductor can deliberately transmit a tokenized `signal hacked` event.
While DeFUNKd is in SOLO, BATTLE, CYPHER, DJ, or DANCE FLOOR, that event opens
the existing prompt. AFTER PARTY and COOLDOWN remain ineligible.

When detected, the badge alternates **SIGNAL HACKED** and **CURIOUS?** prompts.

- Double swipe within five seconds to accept the current prompt.
- Ignore it to remain in normal DeFUNKd.
- A prompt can remain available for up to one minute.

Ignored prompts back off to reduce annoyance: about two minutes after the first
dismissal, five minutes after the second, then one hour after repeated
dismissals.

After acceptance, the cyberpunk OLED animation and LED accents follow the
conductor's clock. A matching `signal restored` event from the same conductor
immediately ends the accepted Party visual path and returns the badge to
DeFUNKd SOLO without stopping the clock. The event also clears an unaccepted
prompt owned by that conductor. Restoration events from another source, or
events without a valid token, are ignored.

If validated sync is absent long enough, the badge exits the visual submode and
returns to DeFUNKd SOLO as a fallback. The source loss threshold is 15 seconds;
the visible return can vary slightly with packet timing and animation
boundaries. Outside accepted Party, stale clock data simply restores the
existing local visual timing and does not force a DeFUNKd state transition.

## 7. Signal Clash

Signal Clash is a first-class operating mode. It takes complete ownership of
the game radio, OLED, LEDs, and sensor while active. It does not depend on
DeFUNKd, a phone, a referee, or MIDI Clock.

Source and protocol identifiers still use `WARGAMES` or `SIGNAL WAR` in some
places for compatibility. The user-facing mode is **Signal Clash**.

### Enter And Exit

Enter:

1. Start from Station 562 or Control Room.
2. Release after the four-second Signal Clash loading step completes.
3. Perform two deliberate swipes during the confirmation screen.
4. Keep the sensor clear while entry settles.

The entry handoff suppresses attacks for 2.5 seconds and suppresses the exit
detector for ten seconds. A lingering hand must also clear before gameplay
input begins. These guardrails prevent entry swipes from becoming attacks.

Exit:

1. Hold very close for five continuous seconds.
2. For the first three seconds, normal gameplay remains visible.
3. From three to five seconds, the full-screen **KEEP HOLD** progress appears.
4. Release when asked.
5. Perform two swipes within four seconds.

The exit path is available from ordinary roaming and may interrupt idle
presentation. Active higher-priority combat and authorization screens retain
their own bounded interaction windows.

### Identity, Handle, And Team

On first Signal Clash initialization, the badge:

- reads its immutable hardware-derived badge ID;
- creates a random identity epoch;
- generates its own P-256 player keypair;
- generates an automatic themed handle;
- starts at PROSPECT;
- stores the complete career atomically in redundant NVS records.

The private player key remains on that badge. Normal firmware uploads and
reboots preserve the identity. **BURN HANDLE / FACTORY RESET** erases it.

Teams are RED and BLUE. CodeCell renders both colors directly. XIAO uses red
for RED and white for the logical BLUE team.

The default `AUTO` preference chooses a deterministic initial team from the
hardware badge ID. This is convenient, not a guaranteed event-wide 50/50
allocator. The owner can choose AUTO, RED, or BLUE in Setup before entering.
Changing team preference does not erase the career.

### Roaming Objective

The ordinary all-day game loop is:

1. enter Signal Clash;
2. find a nearby opposing badge;
3. attack or defend using the sensor and OLED cues;
4. convert captured opponents to your team;
5. earn REP and unique-capture credit;
6. advance through the career ranks;
7. remain available while roaming through the venue.

The game selects the strongest qualified opposing peer already visible over
BLE. It does not require entering a target ID. A locked target receives a
generous loss grace so normal packet gaps do not constantly switch the OLED
between peers.

The regular attack qualification threshold is approximately `-70 dBm`. Covert
Intrusion requires an extremely close, stable peer around `-52 dBm` plus
several confirming observations. RSSI is environmental evidence, not a
guaranteed physical distance; bodies, cases, walls, orientation, and radio
congestion affect it.

### Port Scan

Port Scan is the standard attack.

1. Wait for a valid opposing target.
2. Begin with your hand clear.
3. Move far to close.
4. Pull fully away.

The accepted cover is deliberately broad, roughly 40-1000 ms in the gesture
model. Motion quality is classified STANDARD, CLEAN, or PRECISE. Better quality
raises the compromise probability:

- base chance: 45%;
- CLEAN: +8 percentage points;
- PRECISE: +15 percentage points.

The final chance is clamped to 25-90% after all active modifiers.

### 0.DAY

Three acknowledged Port Scan attacks charge 0.DAY. When ready, the OLED shows
the circular depth guide:

1. move into the target depth band;
2. hold steadily for about 0.9-3.5 seconds;
3. release.

0.DAY has a 70% base compromise chance before quality, discipline, Heat, ally,
payload, and target modifiers. A stored offensive 0.DAY payload can also add
20 percentage points where the combat path permits it.

### Covert Intrusion

Covert Intrusion is an automatic high-risk upgrade of Port Scan. It uses the
same far-close-far gesture but requires sustained, extremely close target
evidence. A credited capture earns 5 bonus REP.

No separate mode or hidden gesture is required. If the radio evidence does not
meet the close-range rule, the same action remains a Port Scan.

### Attack Modifiers

Current modifiers include:

- BREAKER discipline: +6 percentage points;
- nearby HANDLER ally: +6;
- Fork Advantage: +8;
- exposed H3 target: +8;
- offensive 0.DAY payload: +20;
- failed attack TRACE: +10 per stack, maximum two stacks.

TRACE lasts about 18 seconds. It rewards repeated pressure without making a
single failed attempt permanent.

The target commits its new team before sending an acknowledgment. The attacker
increments capture counters only after receiving that acknowledgment. A
captured badge receives about 3.5 seconds of protection.

### Incoming Defense

An incoming attack opens a full-screen choice:

- hold for FIREWALL;
- swipe for EVADE.

The interaction windows are intentionally human-scale. A missed/no-input
attempt retains its bounded window; a decisive successful gesture resolves
immediately.

#### Firewall

Move close and hold steady. The ring guide shows live depth against the target
ring.

- about one second establishes the hold;
- about two additional seconds judge stability;
- PRECISE automatically patches the attack;
- CLEAN reduces compromise chance by 20 percentage points.

#### Evade

Evade is a two-action timing defense:

1. the first far-close-far swipe selects EVADE and starts the moving marker;
2. the second swipe commits the marker's current position.

There is exactly one committed attempt. PRECISE automatically evades. CLEAN
reduces compromise chance by 15 percentage points. A GHOST may also receive an
automatic 6% evade.

#### PATCH

A defensive PATCH blocks one otherwise successful attack and is consumed.
CIPHER can regenerate one roaming PATCH after 90 seconds without one.

### Heat And Exposure

Aggressive activity raises Heat from H0 through H3. Heat decays every 15
seconds during ordinary roaming; GHOST cools every nine seconds. At H3, the
badge is exposed and a successful opposing hack can award bonus REP.

### REP And Progression

| Rank | Automatic requirement |
| --- | --- |
| PROSPECT | Starting rank |
| OPERATOR | 50 REP and 1 unique captured badge |
| SPECIALIST | 100 REP and 3 unique captured badges |
| MADE | 150 REP and 5 unique captured badges |
| CELL_LEADER | 250 REP, 10 unique captured badges, and 3 combined successful defenses, evasions, or assists |
| ROOT eligible | 250 REP and 10 unique captured badges |
| ROOT | Successful three-badge physical induction |

ROOT eligibility deliberately depends only on REP and unique captures,
regardless of the current automatic rank. ROOT itself is never granted by
statistics alone.

Current REP awards:

| Event | REP |
| --- | ---: |
| Confirmed capture | 10 |
| Covert Intrusion bonus | 5 |
| Successful Firewall or Evade | 4 |
| HANDLER assist | 4 |
| Successful hack of an exposed H3 target | 5 |
| Referee round win, experimental | 10 |
| Referee match win, experimental | 25 |

Capture and defense REP uses a ten-minute per-opponent anti-farm window.
Lifetime event counters still update when repeat REP is suppressed. Unique
capture credit is, by definition, granted only once per hardware badge ID.

Rank promotion, five and ten unique captures, ROOT eligibility, and successful
ROOT induction receive interruptible OLED/LED celebrations. If one result
unlocks several milestones, the highest-value event wins:

`ROOT INDUCTED > ROOT ELIGIBLE > RANK UP > 10 UNIQUE > 5 UNIQUE`.

### Disciplines

Discipline selection unlocks at SPECIALIST. The choice is permanent for that
persona; Burn Handle is required to choose again.

| Discipline | Current power |
| --- | --- |
| BREAKER | Adds 6 percentage points to compromise probability |
| GHOST | Approximately 6% automatic evade and Heat cools every 9 seconds |
| CIPHER | Regenerates one missing PATCH after 90 seconds |
| HANDLER | Nearby teammates gain +6 attack chance; confirmed supported captures award the Handler an assist and 4 REP |

The OLED selection screen includes a short description. The USB command
`wg disciplines` prints the complete reference.

### Payloads

Reaching OPERATOR grants a 0.DAY offensive payload and a defensive PATCH when
the corresponding slots are empty. Every five unique opponents may refill one
missing payload, alternating the preferred slot. Payloads are part of the
persistent career.

### ROOT Induction

An eligible player can request induction from Setup. Earned ROOT requires three
physical badges:

1. the eligible candidate;
2. a ROOT sponsor;
3. an independent ROOT witness.

The candidate chooses **REQUEST INDUCTION**. The two ROOT players choose
**ROOT INDUCTION**, then select SPONSOR or WITNESS. Each participant follows
the hold confirmation shown on its own OLED.

The ceremony uses temporary `S562 INDUCTION` BLE discovery and a dedicated
connected GATT exchange. It does not require a computer, phone, offline signing
key, or matching teams. The sponsor consumes one of two lifetime sponsorship
slots. Witnessing consumes no slot.

Founder or disaster-recovery ROOT provisioning is a separate operator process
and is not an owner workflow.

### ROOT Combat

A non-ROOT player cannot capture ROOT through an ordinary single strong attack:

- normal non-ROOT attacks become raid hits;
- five unique non-ROOT attackers must land accepted hits within 90 seconds;
- a non-ROOT 0.DAY does not bypass the ROOT guard;
- ROOT-versus-ROOT 0.DAY follows the normal strong-attack path.

This preserves ROOT as a rare earned identity without making it invulnerable.

### Network Owned And Network Fork

When all locally visible players share one team, combat naturally pauses and
the badges display **NETWORK OWNED**.

After five continuous minutes without a hostile signal, a 60-second
**NETWORK FORK** offer opens on each badge:

- double swipe to **BREAK CONSENSUS** and defect;
- do nothing to remain with the winning team.

Each badge decides independently. Multiple players may volunteer; one player's
choice does not remove the option from the others. A defector receives a
15-second capture shield and Fork Advantage. If nobody volunteers, the network
remains owned and another offer follows after the next domination interval.

### Roaming Display And Battery Behavior

The normal display rotates every six seconds:

1. large `[HANDLE]` and rank;
2. large REP and UNIQ with discipline and Heat;
3. large team and rank (`ROOT:~#` for ROOT).

After 60 seconds without gameplay or user input, the OLED stays on an
identity-centered standby page with subtle pixel shifting. LEDs reduce to two
faint team-color pulses every five seconds. BLE scanning, advertising, peer
events, attacks, forks, and the sensor remain active. A meaningful sensor or
game event wakes the full display without consuming that gesture as an attack.

### Referee Operations Boundary

V6.3.0 contains an operator/referee match engine and diagnostic commands from
development. It can stage temporary balanced teams, timed rounds, sudden death,
and best-of-three scoring. Full release acceptance was deliberately deferred
because multi-badge roster convergence was not as reliable as roaming play.

Ordinary owners should treat roaming Signal Clash as the supported V6.3.0 game.
Referee Operations are experimental/operator-only and must not be used as a
production event promise. Persistent roaming teams and careers remain the
authoritative player state.

## 8. MIDI Controller Mode

### Enter

1. Start from a normal Station 562 face.
2. Hold until the eight-second MIDI Controller loading step completes and
   release before the ten-second DEFUNKT562 step.
3. Double swipe within the confirmation window.
4. The badge starts BLE MIDI advertising as `S562_MIDI`.

MIDI Controller is deliberately separate from DeFUNKd and the puzzle radio.

### Connect A Host

Use the host app's Bluetooth MIDI connection panel, not only the phone's normal
Bluetooth settings. After connecting, select `S562_MIDI` as the MIDI input
for the desired synth or instrument track.

The badge can report **connected** when an app has a direct BLE/GATT connection
even if that app has not routed the MIDI data to a synth. Connection confirms a
BLE client; audible output also requires a valid MIDI route and an armed
instrument.

### OLED And LED Feedback

At rest, the MIDI OLED shows readiness information such as host state, channel,
clock/BPM, and proximity. During an attack, the current note name becomes the
main performance feedback. This lets the player see the quantized pitch selected
by the current proximity range.

MIDI LEDs remain dark at rest and accent hand attacks or incoming clock beats.
This avoids implying activity when no performance signal exists and reduces
continuous LED load.

### Playing Notes

The sensor is theremin-like but scale-quantized:

1. Moving from far to close selects positions across the configured scale.
2. Crossing the note-on threshold begins an attack.
3. Proximity selects the scale degree or fixed note behavior.
4. Releasing the sensor ends or schedules the note according to gate settings.
5. Optional expression tracks proximity or light and sends CC, Pitch Bend, or
   Channel Pressure.

The factory Carrier musical range is C3 through C4 in C minor, eight scale
degrees, on MIDI channel 1.
Default note centers are target-specific because the sensors have different
physical response ranges.

### MIDI Output And Clock Input

V6.3.0 implements:

- MIDI 1.0 Note On and Note Off,
- Control Change,
- 14-bit Pitch Bend,
- Channel Pressure,
- MIDI Clock receive at 24 pulses per quarter note,
- MIDI Start, Continue, and Stop receive,
- batched BLE MIDI realtime-byte decoding,
- panic/all-notes cleanup,
- channels 1 through 16.

It does not implement onboard audio, MIDI 2.0/UMP, full MPE, USB MIDI, or a
custom multi-badge audio sequencer.

If a host clock was running before the BLE connection was established, some
apps do not resend Start. If BPM/transport does not become active, stop and
restart the clock in the host app. This is host-dependent behavior.

### Disconnect And Exit Behavior

While a host remains connected, MIDI Controller does not display inactivity
exit prompts.

After a real disconnect:

1. A 45-second reconnect grace period begins.
2. If still disconnected and idle, the exit prompt appears.
3. Double swipe within four seconds to exit.
4. Hold close for about 1.5 seconds to dismiss the prompt and stay in MIDI Mode.
5. With no host and no activity, automatic exit occurs after about two minutes.

The terminal/config command `midi exit` requests an immediate clean exit.

## 9. Musical Configuration

### Presets

| Preset | Intended behavior |
| --- | --- |
| `lead` | Fast scale playing with proximity velocity and free gate |
| `pluck` | Settled/plucked attack, shorter clock-aware gate, stronger attack range |
| `pad` | Long gate, fixed softer velocity, smoothed expression from light |
| `run` | Fast retriggering with filter expression and quick tracking |
| `hybrid` | Chooses lead, pluck, pad, or run attack feel for each new sensor attack while preserving your musical mapping |
| `carrier` | Opt-in touchless instrument: strike speed controls velocity, strike depth selects pitch, and the held gesture drives several coordinated expressive controls |

Applying `lead`, `pluck`, `pad`, or `run` loads that preset's complete profile.
It can therefore replace previously edited scale, gate, velocity, expression,
range, and dwell values. Selecting `hybrid` starts with the Lead attack
personality without replacing the current instrument map; each later attack
varies only articulation, gate, retrigger, and dwell. Your channel, key, scale,
octave, note range/tuning, velocity, expression, thresholds, and performance
modifiers remain stable while Hybrid is active.
Carrier is the factory default for a new badge or after resetting MIDI
settings. A firmware upgrade preserves any valid preset the musician already
saved.
Review `midi map` after changing presets.

### Carrier Instrument

`carrier` is isolated from the five established presets. It preserves the
current channel, pitch map, scale, root, octave, span, tuning profile, and
MIDI-local thresholds, then interprets one hand gesture in three phases:

1. **Strike:** approach speed sets true Note On velocity while the deepest
   point in the short attack window selects the quantized note.
2. **Sustain:** pitch locks; proximity sends CC74, movement sends CC1, relative
   shadow sends CC11, and hold depth/time sends Channel Pressure.
3. **Release:** withdrawal speed sends CC91 before Note Off. A quick withdrawal
   produces a tighter tail and a slow withdrawal produces a longer tail.

Carrier uses ordinary MIDI 1.0 messages. The receiving instrument determines
how audible each CC or Channel Pressure lane is; patches that ignore a
controller will still receive notes normally. `midi panic`, disconnect, mode
exit, or selecting another preset cleans up Carrier-owned notes and controls.

### Pitch Organization

- Modes: `scale`, `fixed`
- Scales: `major`, `minor`, `pent`, `blues`, `chromatic`
- Root: 0-11 or note name (`C`, `C#`, `Db`, and so on)
- Octave: 0-8
- Scale span: 1-32 degrees
- Fixed note: MIDI note 0-127

`midi note <0-127>` selects fixed-note mode. Scale/root/octave commands return
to scale mode.

### Timing And Articulation

- Articulation: `swipe`, `pluck`
- Gate: `free`, `1/16`, `1/8`, `1/4`, `1/2`, `1bar`
- Retrigger grid: `instant`, `1/16`, `1/8`, `1/4`
- Dwell: 0-500 ms

Clock-relative gates and repeat/quantize behavior are most deterministic while
a valid MIDI Clock is present. Without clock, the firmware uses local timing
fallbacks where implemented.

### Velocity

- `fixed`: every attack uses the configured velocity.
- `prox`: closer attacks move upward through the configured velocity range.
- `inverse`: closer attacks move downward through the configured range.

Velocity values are standard MIDI 0-127. A Note On with velocity zero may be
interpreted as Note Off by MIDI receivers, so use zero deliberately.

### Expression

Destinations:

- `off`
- `mod` (CC1)
- `expression` (CC11)
- `filter` (CC74)
- `reverb` (CC91)
- `cc` (user-selected Control Change number)
- `pitchbend` (14-bit channel Pitch Bend)
- `pressure` (Channel Pressure)

Sources are `prox`, `ambient`, and `white`. On CodeCell, `white` intentionally
uses ambient light as a hardware fallback. Expression can be inverted and
smoothed at `off`, `light`, `medium`, or `strong` levels. Expression depth is a
MIDI value range from 0 to 127.

### Performance Modifiers

Ten modifiers can be controlled independently at `off`, `subtle`, `medium`,
`high`, or `extreme`:

`expression`, `gate`, `repeat`, `range`, `chord`, `motion`, `velocity`,
`quantize`, `glide`, and `phrase`.

Fixed combinations are:

- `clear-channel`
- `numbers-station`
- `tower-sweep`
- `repeater-storm`
- `long-lines`

Five user slots save modifier combinations only. Four scene slots save the full
MIDI performance state.

## 10. Instrument Tuning

Tuning affects MIDI Controller only. It does not change the shared main-menu
sensor, DeFUNKd gestures, DEFUNKT562 calibration, or Setup gestures.

Enter MIDI Controller before running tuning mutations.

### Quick Far/Close Tuning

1. Put your hand at the farthest playable position.
2. Send `midi tune far`.
3. Put your hand at the closest comfortable position.
4. Send `midi tune close`.
5. Send `midi tune apply`.
6. Play-test the result.
7. Send `midi settings save` only when satisfied.

The first point must be above the active note-on threshold. If the badge returns
`tune_far_below_gate`, move closer and try again.

### Guided Three-Point Tuning

1. Send `midi tune start`.
2. Place your hand at the displayed FAR target and send `midi tune next`.
3. Move to the displayed MID target and send `midi tune next`.
4. Move to the displayed CLOSE target and send `midi tune next`.
5. Send `midi tune save` to apply the three-point curve.
6. Send `midi settings save` to make it the startup default.

With factory C-minor settings, the target notes are C3, F3, and C4. Each point
must be closer than the previous point. The OLED shows the step, target note,
live proximity, and result.

`midi tune cancel` abandons the active capture session. `midi tune reset`
restores the target-specific production note/expression ranges and MIDI-local
thresholds. Reset changes runtime settings and marks them dirty; save afterward
only if you want the reset to persist.

### Manual Thresholds

`midi threshold <enter> <exit>` changes the MIDI attack/release gate only.
`exit` must be lower than `enter`; both must be 0-4095. Use this only when the
note range feels good but attack/release sensitivity does not.

`midi threshold reset` restores the target default.

## 11. Persistence, Scenes, And Reset Scope

Most MIDI configuration commands change the active runtime and set `dirty` to
1. They do not automatically overwrite the startup configuration.

- `midi settings save`: save the current complete MIDI state as the startup
  default.
- `midi scene save 1` through `4`: save the current complete MIDI state in a
  scene slot.
- `midi scene load 1` through `4`: load a scene into the active runtime.
- `perf user save 1` through `5`: save only the ten modifier levels.
- `perf user load 1` through `5`: load only those modifier levels.

Reset commands have different scopes:

| Command/action | Scope | Reboots? |
| --- | --- | --- |
| `midi tune reset` | MIDI note/expression sensor ranges, tuning curve, and MIDI thresholds | No |
| `perf reset` | Ten active performance modifiers | No |
| Setup `RESTORE DEFAULTS` | LED brightness and normal face LED styles | No |
| `midi reset-current confirm` | Active MIDI settings only; saved startup state and slots remain | No |
| `midi settings reset confirm` | Entire MIDI namespace, including startup settings, scenes, and user modifier slots | No |
| Setup `BURN HANDLE` or `factory-reset confirm` | Setup, MIDI, and Signal Clash namespaces, including career, player keypair, team, and ROOT certificate | Yes |

Burn Handle preserves the hardware-derived stable badge ID because it comes
from the physical ESP32. It also preserves the read-only CTF SPIFFS archive.
The next Signal Clash initialization creates a new player epoch, keypair,
automatic handle, team, and PROSPECT career.

## 12. Setup Menu

### Enter

1. Start from normal Station 562 or Control Room operation.
2. Hold for at least twelve seconds.
3. Release on the Service Channel request.
4. Double swipe within six seconds.

### Navigate

- Short swipe: next item or next option.
- Hold two seconds: select, save, or return.
- Fifteen seconds without interaction: discard unsaved preview changes and
  return to normal Station 562.

Menu order:

1. LED BRIGHTNESS
2. STATION 562 LED
3. CONTROL ROOM LED
4. SIGNAL CLASH TEAM
5. REQUEST INDUCTION, only when the career is ROOT-eligible
6. ROOT INDUCTION, only when the badge can sponsor or witness
7. RESTORE DEFAULTS
8. REBOOT BADGE
9. BURN HANDLE
10. RETURN TO STATION

Brightness choices are OFF, LOW, MEDIUM, and HIGH. The selected brightness also
applies to party visual LED output.

The Station 562 and Control Room animation choices are:

- STATION DEFAULT
- CONTROL ROOM
- NEON ROGUE
- MICROWAVE SWEEP
- PACKET RAIN
- FIREWALL JAMMER
- SATELLITE RELAY

Signal Clash team choices are AUTO, RED, and BLUE.

Burn Handle requires a double swipe and then a final one-second hold during the
six-second **ARE YOU SURE?** window. Releasing before the final hold completes
cancels it.

## 13. Software Sleep And Battery Reality

From normal Station 562 operation, perform five short swipes within nine
seconds. The same gesture wakes the badge.

In Sleep:

- OLED is off,
- BLE advertising/scanning is stopped,
- normal LED animation is off,
- one faint red heartbeat appears for about 40 ms every ten seconds,
- the proximity sensor and CPU path remain active enough to detect wake.

This is software standby. It is not ESP deep sleep and cannot disconnect the
battery. The firmware makes no battery-runtime or true power-off claim.

Sleep entry is blocked while Signal Clash, DeFUNKd, DEFUNKT562, Setup, or MIDI
Controller owns the interaction path.

## 14. DEFUNKT562 Tamper-Evident Mode

DEFUNKT562 is not a normal display mode. It is a deliberate tamper/blackout
state.

### Enter

1. Hold until the ten-second DEFUNKT562 loading step completes.
2. Release before the twelve-second Setup step.
3. Double swipe within five seconds.
4. A 30-second acquisition/placement window begins.
5. Only the final ten seconds are averaged for the sensor baseline.
6. The badge then enters armed blackout.

Normal puzzle BLE stops during calibration and armed blackout. A qualifying
tamper event changes BLE behavior to the `562_ALERT!` identity.

Do not enter DEFUNKT562 casually. Its exit is intentionally hidden and provides
LED cues rather than OLED instructions.

## 15. BLE Identity And Services

### Advertised Names

| State | BLE name/behavior |
| --- | --- |
| Normal puzzle | `STATION_562`, rotating manufacturer data |
| DeFUNKd | `DEFUNKD_562`, DeFUNKd advertisement plus scan |
| MIDI Controller | `S562_MIDI`, connectable BLE MIDI and config GATT |
| Signal Clash | `SIGNAL_CLASH`, connectable game identity/config GATT plus game service data |
| ROOT induction | `S562 INDUCTION`, temporary ceremony-local peer GATT |
| DEFUNKT562 calibration/armed | BLE silent |
| DEFUNKT562 alert | `562_ALERT!` |
| Software Sleep | BLE off |

### Standard BLE MIDI

- Service: `03B80E5A-EDE8-4B33-A751-6CE34EC4C700`
- Characteristic: `7772E5DB-3868-4112-A1A9-F2669D106BF3`

### Station 562 Config/Identity GATT

- Service: `9C5E5620-4F52-4249-5441-4C4445430001`
- Identity read: `9C5E5621-4F52-4249-5441-4C4445430001`
- Capabilities read: `9C5E5622-4F52-4249-5441-4C4445430001`
- Snapshot read: `9C5E5623-4F52-4249-5441-4C4445430001`
- Command write: `9C5E5624-4F52-4249-5441-4C4445430001`
- Result read/notify: `9C5E5625-4F52-4249-5441-4C4445430001`
- Signal Clash transaction write: `9C5E5626-4F52-4249-5441-4C4445430001`
- Signal Clash transaction result: `9C5E5627-4F52-4249-5441-4C4445430001`

ROOT ceremony temporarily uses a separate service:

- Ceremony service: `9C5E5630-4F52-4249-5441-4C4445430001`
- Ceremony transaction: `9C5E5631-4F52-4249-5441-4C4445430001`
- Ceremony result: `9C5E5632-4F52-4249-5441-4C4445430001`

The config service is discoverable after connecting in MIDI Controller or
Signal Clash. It is not a general BLE terminal and is not advertised as an
independent owner mode.

Apps write one compact UTF-8 JSON command envelope at a time:

```json
{"schema":"station562.badge.config.command.v1","seq":1,"command":"midi channel 4"}
```

The command string is limited to 127 characters. Results use:

```json
{"schema":"station562.badge.config.result.v1","seq":1,"ok":true,"code":"channel_set","dirty":1}
```

#### Config Access Tiers

The config service uses application-level physical authorization; it does not
turn BLE MIDI into an OS-bonded or passkey-paired device.

In MIDI Controller, every new BLE connection begins with this public surface:

- standard BLE MIDI reads/writes/notifications,
- read-only identity, capabilities, snapshot, and result characteristics,
- exact commands `signal hacked` and `signal restored`,
- the bounded `signal game` referee control surface.

The two signal commands require a valid, running clock. They emit bounded
Station 562 events and do not expose the serial parser or arbitrary commands.
The referee surface is experimental and intended for controlled operator use.

Every accepted `midi ...` or `perf ...` configuration mutation is privileged.
The first privileged write returns `physical_confirmation_required` and opens
an **ACCESS REQUEST** screen for 20 seconds. Two deliberate swipes authorize
only the requesting BLE connection. The app then retries the original command
with a new sequence number. Authorization remains valid for that connection,
so later configuration commands do not ask again.

Authorization is revoked by disconnect, MIDI Controller exit, reboot, or BLE
stack reset. Another connection cannot inherit it. A new prompt is rate-limited
for 25 seconds after a request, and the badge refuses to begin authorization
while MIDI Clock, a note performance, or MIDI audition is active. Whole-badge
`factory-reset confirm` always returns `command_not_allowed` over BLE, even on
an authorized connection.

In Signal Clash, public GATT is limited to game intents and read-only identity
or career information:

- `status`, `stats`, `act`, `exit`, and `input`;
- `choose`;
- `whoami`, `wg handle get`, and `wg identity status`.

Changing or randomizing the handle is elevated. The first request opens a
two-second physical hold approval and authorization belongs only to that
connection. Signal Clash GATT never exposes arbitrary USB commands, Burn
Handle, or factory reset.

Important access result codes include:

| Code | Meaning |
| --- | --- |
| `physical_confirmation_required` | The badge opened the physical approval screen |
| `authorized` | Double swipe approved the requesting connection |
| `authorization_pending` | That connection already has a request in progress |
| `authorization_busy` | Another connection owns the pending request |
| `authorization_rate_limited` | Wait for the prompt cooldown before retrying |
| `authorization_timeout` | The physical approval window expired |
| `performance_active` | Approval cannot interrupt active performance/clock |
| `command_not_public` | Command is outside both accepted public and privileged surfaces |
| `command_not_allowed` | Command is deliberately forbidden over BLE |

## 16. USB Serial Terminal

### Connect

The production terminal runs at 115200 baud. A USB data cable is required.

Using Arduino CLI on macOS or Linux:

```sh
arduino-cli board list
arduino-cli monitor -p /dev/cu.usbmodemXXXX --config baudrate=115200,dtr=off,rts=off
```

Linux ports commonly look like `/dev/ttyACM0`; Windows ports look like `COM4`.
Replace the example with the port reported by `arduino-cli board list`.

Press `Ctrl-C` to close the monitor. Close every serial monitor before flashing
or before another program opens the same USB port. Keep DTR and RTS off for
read-only checks; enabling them can reset some ESP32 USB configurations.

Type:

```text
help
```

and press Enter. Commands are lowercase and exact. Unknown top-level commands
return `[CMD] error=unknown; send help`. Verify every mutation by reading status
or checking its `ok=`/`error=` response.

### Read-Only Status Commands

| Command | Output |
| --- | --- |
| `help` | Production command list |
| `version` | Firmware, hardware target, stable badge ID, and per-binary build ID |
| `midi status` | Compact config snapshot JSON |
| `midi clock` | BLE MIDI clock, transport, BPM, counters, and sync-advertisement status |
| `midi auth` | Authorized/pending connection, approval swipes, and retry cooldown |
| `midi map` | Effective preset, modifiers, sensor ranges, and proximity-to-note map |
| `midi tune status` | Live proximity, ranges, thresholds, and current tuning session |
| `midi settings status` | Dirty state, full map, scenes, and performance summary |
| `midi scene status` | Four scene slots |
| `perf status` | Modifier levels, fixed presets, and five user slots |
| `perf user status` | Alias for the performance/user-slot status |
| `sleep status` | Sleep state, blockers, swipe timing, and heartbeat settings |
| `signal status` | Clock, prompt, Party, invitation, and restoration diagnostics |
| `signal animation-info status` | Whether the party debug overlay is visible |
| `wargames status` | Signal Clash mode, input, peer, event, and visual diagnostics |
| `wargames stats` | Complete persistent career and current match counters |
| `wargames peers` | Currently visible Signal Clash peers and radio evidence |
| `wg whoami` | Handle, badge ID, rank, certificate, and key fingerprint |
| `wg disciplines` | Discipline powers and selection rule |

Recognized read-only aliases are `status midi`, `clock midi`, `midi tune`,
`status sleep`, and `status signal`. Use the primary forms above in scripts and
support instructions so logs remain consistent.

Before flashing a batch, run `version` on each connected badge. Compare the
`firmware` field to the intended release and the `build_id` field to a known
badge from the same compiled artifact. Matching version strings alone do not
prove that two badges contain the same local build.

### Immediate MIDI Operations

| Command | Effect |
| --- | --- |
| `midi audition` | Send an eight-note test phrase; requires a BLE MIDI host |
| `midi audition stop` | Stop and clean up the test phrase |
| `midi panic` | Stop active performance and send MIDI panic cleanup |
| `midi expression send <0-127>` | Send one value through the selected expression destination |
| `midi enter` | Enter MIDI Controller from USB only |
| `midi exit` | Exit MIDI Controller cleanly |

Always run `midi audition stop` or `midi panic` if a test is interrupted and a
host appears to retain a note.

### Basic MIDI Configuration

| Command | Accepted values |
| --- | --- |
| `midi preset <name>` | `lead`, `pluck`, `pad`, `run`, `hybrid`, `carrier` |
| `midi channel <n>` | 1-16 |
| `midi mode <mode>` | `scale`, `fixed` |
| `midi scale <name>` | `major`, `minor`, `pent`, `blues`, `chromatic` |
| `midi root <root>` | 0-11 or note name such as `C`, `F#`, `Bb` |
| `midi octave <n>` | 0-8 |
| `midi start <note>` | Start the playable range on `root`, a scale note such as `C4`, or MIDI note 0-127 |
| `midi span <n>` | 1-32 |
| `midi note <n>` | 0-127; also selects fixed mode |
| `midi articulation <name>` | `swipe`, `pluck` |
| `midi gate <length>` | `free`, `1/16`, `1/8`, `1/4`, `1/2`, `1bar` |
| `midi retrigger <grid>` | `instant`, `1/16`, `1/8`, `1/4` |
| `midi dwell <ms>` | 0-500 |

`midi start` does not transpose the key. It rotates the playable range to a
later degree of the configured scale. For example, after `midi root A`,
`midi octave 3`, and `midi scale minor`, the commands `midi start A3`,
`midi start C4`, and `midi start E4` all remain in A minor. A note outside the
configured scale is rejected. Run `midi settings save` to preserve the start
note across reboot.

### Velocity And Expression

| Command | Effect |
| --- | --- |
| `midi velocity <0-127>` | Set fixed velocity and select fixed velocity mode |
| `midi velocity-mode <mode>` | `fixed`, `prox`, `inverse` |
| `midi velocity-range <min> <max>` | Set proximity velocity output range, 0-127 |
| `midi expression <dest>` | `off`, `mod`, `expression`, `filter`, `reverb`, `cc`, `pitchbend`, `pressure` |
| `midi expression-source <source>` | `prox`, `ambient`, `white` |
| `midi expression invert <on|off>` | Reverse expression direction |
| `midi expression smooth <level>` | `off`, `light`, `medium`, `strong` |
| `midi expression-depth <min> <max>` | Set expression output depth, 0-127 |
| `midi cc <0-127>` | Select a custom CC and select custom-CC expression mode |
| `midi cc-range <min> <max>` | Set expression sensor input range |
| `midi expression-range <min> <max>` | Alias for `midi cc-range` |

### Sensor Mapping And Tuning

| Command | Effect |
| --- | --- |
| `midi note-range <far> <close>` | Replace note sensor range and clear any three-point tuning curve |
| `midi threshold <enter> <exit>` | Set MIDI-local attack/release thresholds |
| `midi threshold reset` | Restore target thresholds |
| `midi tune far` | Capture quick far point; requires MIDI Mode |
| `midi tune close` | Capture quick close point; requires MIDI Mode |
| `midi tune apply` | Apply captured quick range; requires MIDI Mode |
| `midi tune start` | Begin guided three-point capture; requires scale mode and MIDI Mode |
| `midi tune next` | Capture the displayed guided point; requires MIDI Mode |
| `midi tune save` | Apply the completed three-point curve; requires MIDI Mode |
| `midi tune cancel` | Cancel the current capture session |
| `midi tune reset` | Restore target tuning defaults; requires MIDI Mode |

Range pairs accept spaces, commas, slashes, or a hyphen as the separator. Use
spaces for readability.

### Performance Modifiers

```text
perf <setting> <off|subtle|medium|high|extreme>
```

Settings are:

```text
expression gate repeat range chord motion velocity quantize glide phrase
```

Other commands:

| Command | Effect |
| --- | --- |
| `perf reset` | Set all ten modifiers off |
| `perf preset clear-channel` | Load the neutral modifier combination |
| `perf preset numbers-station` | Load the Numbers Station combination |
| `perf preset tower-sweep` | Load the Tower Sweep combination |
| `perf preset repeater-storm` | Load the Repeater Storm combination |
| `perf preset long-lines` | Load the Long Lines combination |
| `perf user save <1-5>` | Save current modifier levels |
| `perf user load <1-5>` | Load a saved modifier combination |
| `perf user clear <1-5>` | Clear a user modifier slot |

### Scenes And Persistence

| Command | Effect |
| --- | --- |
| `midi scene save <1-4>` | Save the full active MIDI configuration to a scene |
| `midi scene load <1-4>` | Load a scene into the active runtime |
| `midi scene clear <1-4>` | Erase one scene |
| `midi settings save` | Save the complete active MIDI configuration as startup default |
| `midi settings reset confirm` | Clear the entire MIDI namespace, scenes, and user modifier slots |

### Sleep And SIGNAL Control/Diagnostics

| Command | Effect |
| --- | --- |
| `sleep enter` | Enter software sleep if the current mode permits it |
| `sleep exit` | Wake from software sleep |
| `signal hacked` | From a clocked MIDI conductor, emit the five-second invitation event |
| `signal restored` | From the same clocked conductor, emit the five-second restoration event |
| `signal prompt` | Diagnostic: force the prompt; requires DeFUNKd |
| `signal enter` | Diagnostic: force active party visuals; requires DeFUNKd |
| `signal exit` | Exit the overlay/party visual path |
| `signal animation-info on` | Show party animation debug text |
| `signal animation-info off` | Hide party animation debug text; production default |

`signal hacked` and `signal restored` use the production over-air event path;
the same exact command strings are the only public DeFUNKd Signal Party
commands exposed through Config GATT.
`signal prompt`, `signal enter`, and `signal exit` bypass portions of that path
and are USB-only troubleshooting hooks. Normal Party entry still requires a
real invitation event followed by the follower's physical double swipe.

Conductor result codes are:

| Command | Successful codes | Guardrail codes |
| --- | --- | --- |
| `signal hacked` | `invitation_started`, `invitation_active` | `clock_required`, `invitation_rate_limited` |
| `signal restored` | `restoration_started`, `restoration_active` | `clock_required`, `restoration_rate_limited` |

#### Triggering SIGNAL HACKED And SIGNAL RESTORED

USB/operator procedure:

1. Put the conductor badge in MIDI Controller Mode.
2. Connect `S562_MIDI` to a MIDI host and enable Clock Out.
3. Start transport and run `midi clock` on the conductor. Continue only when
   `Active` and `Running` are both yes and BPM is nonzero.
4. Put one or more follower badges in DeFUNKd. Followers may remain in any
   eligible state from SOLO through DANCE FLOOR.
5. Send `signal hacked` on the conductor's USB terminal.
6. Confirm `[SIGNAL] ok=invitation_started`. Each eligible follower should show
   the alternating SIGNAL HACKED/CURIOUS prompt.
7. Double swipe each follower that should join. Ignored followers remain in
   normal DeFUNKd.
8. Keep host transport running. Send `signal restored` to the same conductor
   badge.
9. Confirm `[SIGNAL] ok=restoration_started`. Followers that accepted that
   conductor return to SOLO; ordinary clock-synchronized DeFUNKd timing remains
   available.

Config GATT uses the same conductor and behavior. nRF Connect does not generate
MIDI Clock, so complete steps 1-4 above before opening nRF Connect.

1. Connect nRF Connect to the conductor named `S562_MIDI`.
2. Expand Station 562 config service `5620`.
3. Enable notifications on result characteristic `5625`.
4. Choose **Write** on command characteristic `5624` and select UTF-8/text.
5. Send:

```json
{"schema":"station562.badge.config.command.v1","seq":1,"command":"signal hacked"}
```

6. Match the `5625` result to `seq:1` and confirm `invitation_started` or
   `invitation_active`.
7. To restore while clock continues, send a fresh sequence number:

```json
{"schema":"station562.badge.config.command.v1","seq":2,"command":"signal restored"}
```

8. Match the result to `seq:2` and confirm `restoration_started` or
   `restoration_active`.

These two exact commands are public and do not open the configuration
**ACCESS REQUEST** prompt. They expose no general terminal command. Standard
protected MIDI configuration still requires the physical per-session
authorization described above. A `clock_required` result means Clock Out or
host transport is not currently running.

Operational guardrails:

- Clock Out alone never triggers SIGNAL HACKED.
- Both commands require active/running clock.
- AFTER PARTY and COOLDOWN do not show the invitation.
- Restoration ownership is the physical conductor badge/source, not merely the
  phone or app connection.
- `invitation_active`/`restoration_active` means that event is already in its
  five-second burst and is not an error.
- A same-event retry during cooldown returns `*_rate_limited`.
- Stopping clock remains the fallback Party exit but takes the existing loss
  grace; `signal restored` is the deliberate immediate exit.

### Signal Clash USB Commands

The terminal retains `wargames` and `wg` names for protocol compatibility even
though the screen says Signal Clash.

| Command | Effect |
| --- | --- |
| `wargames enter` or `wg enter` | Enter Signal Clash from USB |
| `wargames exit` or `wg exit` | Exit Signal Clash |
| `wargames status` or `wg status` | Detailed runtime diagnostics |
| `wargames stats` or `wg stats` | Complete career and match counters |
| `wargames peers` | Visible peer table |
| `wargames attack` or `wg act` | Trigger the terminal combat intent when terminal input is enabled |
| `wargames join` | Accept a staged referee invitation |
| `wargames team <auto|red|blue>` | Set team preference |
| `wg input <sensor|terminal|auto>` | Select the Signal Clash input source |
| `wg whoami` | Print identity and certificate summary |
| `wg handle get` or `wg identity status` | Read handle or identity state |
| `wg choose <breaker|ghost|cipher|handler>` | Select an unlocked discipline |
| `wg handle set NAME` | Set the handle through the elevated path |
| `wg handle randomize` | Generate another automatic handle through the elevated path |
| `wg ceremony status` | Current ROOT ceremony state |
| `wg ceremony log` | Ceremony diagnostics |
| `wg ceremony abort` | Abort the local ceremony role |

`wg input terminal` and forced visual/ceremony commands are developer
diagnostics. Restore `wg input sensor` or `wg input auto` before normal play.
The complete production command catalog and Config GATT forms are in
[Terminal And BLE Command Reference](STATION562_TERMINAL_AND_BLE_REFERENCE.md).

### Signal Clash Career And Disciplines

Signal Clash celebrates automatic rank promotion, five and ten unique captured
badges, ROOT induction eligibility, successful ROOT induction, and referee match
victory. Career celebrations last about 2.5-4 seconds and use the current team
color. Combat, defense, exit, and authorization prompts always interrupt them.
If one capture unlocks several milestones, only the highest-value result is
shown: ROOT inducted, ROOT eligible, rank up, ten unique, then five unique.

Discipline selection unlocks at SPECIALIST. The choice is permanent for that
persona; changing it requires **BURN HANDLE / FACTORY RESET**.

| Discipline | Power |
| --- | --- |
| BREAKER | Adds 6 percentage points to compromise probability |
| GHOST | Has approximately 6% automatic evade protection; Heat cools every 9 seconds instead of 15 |
| CIPHER | Regenerates one roaming PATCH after 90 seconds without one; receives one temporary PATCH at the start of each referee round |
| HANDLER | Nearby teammates gain a 6-point attack bonus; a confirmed supported capture earns the Handler one assist and 4 REP |

The CIPHER referee PATCH exists only in RAM for that round. It is consumed by
one otherwise successful attack, disappears at round end, and never changes the
badge's persistent PATCH inventory.

USB reference commands:

| Command | Effect |
| --- | --- |
| `wg disciplines` | Print all four discipline powers and the selection rule |
| `wg stats` | Print career, discipline, payload, match, and identity counters |
| `wg choose <breaker\|ghost\|cipher\|handler>` | Select while the SPECIALIST discipline-choice window is active |

### Whole-Badge Factory Reset

```text
factory-reset confirm
```

This is the USB equivalent of Setup **BURN HANDLE**. It clears Setup, MIDI, and
Signal Clash NVS, including the handle, career, team, player keypair, and ROOT
certificate, then schedules a reboot. It preserves the immutable hardware badge
ID and CTF SPIFFS archive. It is immediate once the exact command is accepted;
there is no second terminal prompt and it is never allowed over BLE.

## 17. Reading The MIDI Snapshot

`midi status` prints the current compact GATT snapshot JSON. V6.3.0 fields
include:

- `stable_id`: permanent hardware-derived badge ID.
- `firmware`: should match the release intended for that badge.
- `runtime_active`: 1 only while MIDI Controller Mode is active.
- `connected` / `ble_connected`: 1 when a BLE client is attached.
- `midi`: channel, last note, velocity, and expression controller.
- `scale_state`: root, octave, span, and fixed note.
- `range` / `thr`: MIDI-local proximity range and gate thresholds.
- `clock`: active, running, BPM x100, beat, phase, Clock/Start/Continue/Stop
  counters, inferred starts, explicit-stop latch, and sync-payload status.
- `invite`: active flag, current event token, and event age in milliseconds.
- `restore`: active flag, current event token, and event age in milliseconds.
- `preset`: active MIDI preset name.
- `tune`: active flag, step, point count, far captured, and close captured.
- `war`: referee state, token, roster, team assignment, and score summary.
- `event`: current bounded operator event type and remaining state.
- `audition`: 1 while the built-in phrase is active.
- `dirty`: 1 means active MIDI configuration has unsaved changes.

The snapshot's `mode` string names the MIDI configuration domain; when read over
USB outside MIDI Controller, use the actual OLED/mode flags rather than treating
that string as proof that MIDI Mode is active.

## 18. Troubleshooting

### Connected, But No Sound

1. Confirm the badge OLED says connected.
2. Confirm the app selected `S562_MIDI` as a MIDI input.
3. Arm or select an audible synth track.
4. Run `midi audition`.
5. If the app receives notes but remains silent, the issue is in app routing or
   audio, not the badge sensor.
6. Run `midi audition stop` after the test.

### Badge Is Not Discoverable

- Confirm it is in MIDI Controller if you are searching for `S562_MIDI`.
- Confirm it is in normal Station mode if you are searching for `STATION_562`.
- Exit software Sleep.
- DEFUNKT562 calibration/armed mode is intentionally BLE silent.
- Close another app that may already hold the BLE connection.
- Reboot the badge from Setup if the correct mode remains undiscoverable.

### Clock Does Not Start

- Confirm the host is actually sending MIDI Clock, not only tempo metadata.
- Run `midi clock` and inspect RX/clock counters.
- Stop and restart host transport after connecting.
- At 120 BPM, a healthy MIDI Clock sends 48 pulses per second (24 PPQN).

### Notes Feel Too Close Or Too Far

1. Run `midi map` and `midi tune status`.
2. Confirm the target's expected factory range.
3. Use quick far/close tuning for the simplest adjustment.
4. Use guided three-point tuning only when the middle of the range needs shaping.
5. If tuning becomes worse, run `midi tune reset`.
6. Save only after playing the result.

### A Setting Reverted After Reboot

Check `dirty` in `midi status`. Runtime edits persist only after `midi settings
save`, a scene save, or a user modifier save at the appropriate scope.

### Terminal Command Has No Response

- Confirm 115200 baud.
- Press Enter after the command.
- Use lowercase exact spelling.
- Unknown top-level commands return `[CMD] error=unknown; send help`.
- Run `help` and use a listed command.
- Run a matching status command to confirm whether a mutation occurred.

### SIGNAL HACKED Does Not Appear

- Confirm the conductor reports active/running clock with `midi clock`.
- Ordinary Clock Out is intentionally silent; send exact `signal hacked`.
- The prompt is suppressed in AFTER PARTY and COOLDOWN.
- A recently ignored invitation may still be in its 2-minute, 5-minute, or
  1-hour backoff.
- Use `signal status` on the follower to inspect clock validity, invitation
  token, source, state eligibility, and backoff.

### SIGNAL RESTORED Does Not Exit Party

- Confirm the restoration was sent by the same conductor that owns Party.
- Confirm the conductor clock is still active/running; otherwise the command
  returns `clock_required`.
- Repeated same-event requests can return `restoration_active` or
  `restoration_rate_limited`.
- Use `signal status` on the follower and inspect `Restoration token/applied`.
- Clock loss remains the fallback and returns Party to SOLO after its grace
  period even when no restoration event arrives.

### Signal Clash Has No Target

- Confirm both badges are in Signal Clash, not DeFUNKd or Station 562.
- Confirm the teams are opposing. Use `wg stats` or the rotating team page.
- Allow several seconds for BLE observations to stabilize.
- Move the badges closer or change their orientation.
- Use `wargames peers` to inspect the radio evidence.
- A target can remain locked through short packet gaps by design.

### Signal Clash REP Did Not Increase

- Repeat captures against the same badge are limited by a ten-minute
  per-opponent REP window.
- Lifetime hack counters can increase while repeat REP is suppressed.
- The attacker scores a capture only after receiving the target's
  acknowledgment.
- `wg stats` shows REP, unique captures, lifetime hacks, defenses, evasions,
  assists, and rank gates.

### ROOT Ceremony Does Not Start

- The candidate must have at least 250 REP and ten unique captures.
- The sponsor and witness must both be ROOT and must be different badges.
- The sponsor needs an unused sponsorship slot; the witness does not.
- Put all three badges into their Setup roles before waiting for discovery.
- Keep them close and powered for the full signed exchange.
- Teams do not need to match.
- Use `wg ceremony status` and `wg ceremony log` over USB if support is needed.

## 19. Optional Hardware CTF

V6.3.0 contains a six-stage, read-only hardware-hacking challenge. Its stage
order, evidence types, hidden commands, and validation path are intentionally
not summarized in this owner manual.

The CTF is designed so:

- one owner can complete it with one badge;
- Python, standard ESP32 tools, and a generic BLE utility are sufficient;
- no macOS-only tool is required;
- every custom validator is recovered during legitimate play;
- AI assistance is allowed, but physical sensor and BLE presence remain
  necessary;
- no stage requires writing or erasing badge flash.

Do not guess destructive `esptool` commands. Begin with the
[Hardware CTF Player Guide](../ctf/STATION562_HARDWARE_CTF_PLAYER_GUIDE.md).
The guide provides prerequisites and safety rules without publishing flags.

Burn Handle does not erase the CTF archive. A full-chip erase does.

## 20. Known V6.3.0 Limits

- Software Sleep is not true power-off or deep sleep.
- No USB MIDI on the current CodeCell C3 or XIAO C6 hardware path.
- MIDI 1.0 only; no MIDI 2.0/UMP or full MPE.
- No onboard audio.
- Standard BLE MIDI remains connectable without OS bonding/passkey pairing.
  Config mutations are instead protected by per-connection physical approval;
  this does not prevent an untrusted central from attempting ordinary MIDI.
- Companion-app tuning UI is future work; terminal/config GATT is the current
  tuning surface.
- USB and Config GATT command text is limited to 127 characters; use the
  documented compact forms.
- Referee best-of-three Operations remain experimental/operator-only; roaming
  Signal Clash is the supported game.
- RSSI-based target qualification is affected by bodies, cases, walls,
  orientation, and crowded-room radio traffic.
- Large-room DeFUNKd and Signal Clash convergence is best-effort rather than an
  authoritative shared global view.
- Sleep current and battery runtime have not been characterized as a release
  claim.
- The shared firmware does not report battery percentage, voltage, or estimated
  time remaining on the OLED or terminal.

## 21. Owner/Operator Recovery Appendix

### DEFUNKT562 Service Exit

This sequence is intentionally absent from the OLED. Use it only when the owner
must recover a badge from DEFUNKT562 calibration, blackout, or alert.

1. Cover the sensor continuously for 20 seconds.
2. Wait for the triple red release cue.
3. Release within five seconds.
4. Perform two deliberate cover-and-release swipes within eight seconds.
5. Wait for the confirmation cues.
6. Begin a final hold within eight seconds and keep holding for four seconds.
7. The badge returns to normal Station 562 operation.

A failed or timed-out attempt does not exit the mode. Start again from the
20-second hold.

### Hidden Puzzle/Easter-Egg Content

V6.3.0 contains hidden puzzle/easter-egg content. Its exact unlock sequence is
intentionally omitted so the discovery experience is not spoiled. Maintainers
can use separately controlled internal validation material when recovery or
event support requires it.

## 22. Firmware And Support References

- Current firmware: `V6.3.0`
- Quick start: `docs/user/STATION562_QUICK_START.md`
- Terminal and BLE reference:
  `docs/user/STATION562_TERMINAL_AND_BLE_REFERENCE.md`
- Self-flash guide: `docs/SELF_FLASH_GUIDE.md`
- Hardware CTF player guide:
  `docs/ctf/STATION562_HARDWARE_CTF_PLAYER_GUIDE.md`

Production badges are delivered flashed and functional. Owners can reinstall
the official binary bundle with the public updater; source compilation remains
a maintainer operation.
