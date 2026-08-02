# Signal Clash Player Guide

Signal Clash is the persistent RED-versus-BLUE game built into every Station
562 badge. Players roam with their badges, find nearby opponents over BLE,
attack and defend with the proximity sensor, convert captured badges, earn REP,
and build a career.

No phone, app, referee, internet connection, or MIDI Clock is required. Signal
Clash starts at **PROSPECT** and the highest earned identity is **ROOT**.

Protocol and terminal text may still say `WARGAMES` or `wg` for compatibility.
Those names refer to Signal Clash.

## Getting Started

### 1. Enter Signal Clash

Start on the normal Station 562 or Control Room face.

1. Cover and hold the sensor.
2. Watch the mode loading screens.
3. Release when the four-second **SIGNAL CLASH** step completes.
4. Double swipe when the confirmation screen appears.
5. Move your hand away and keep the sensor clear while entry finishes.

The badge ignores attacks for 2.5 seconds and ignores the exit gesture for ten
seconds after entry. This prevents the entry swipes or a lingering hand from
becoming an accidental game action.

### 2. Read The Roaming Screens

The normal display rotates through three pages:

1. `[HANDLE]` and rank;
2. REP, unique captures, discipline, and Heat;
3. team and rank.

After one minute without activity, the badge settles on a low-power identity
page. Two faint team-color LED pulses appear every five seconds. The radio and
sensor remain active, and gameplay wakes the normal display. XIAO hardware uses
white LEDs to represent the logical BLUE team.

### 3. Exit Signal Clash

The exit path remains available during ordinary roaming and standby:

1. Hold very close for five continuous seconds.
2. At three seconds, the full-screen **KEEP HOLD** progress appears.
3. Release when asked.
4. Double swipe within four seconds.

The badge returns to normal Station 562 operation. Active combat or
authorization prompts finish their own short interaction window first.

### 4. Choose A Team

The first game initialization chooses RED or BLUE automatically from the
badge's hardware identity. AUTO is deterministic, but it does not guarantee
that every nearby group will begin with equal teams.

To choose a team before playing:

1. Return to a normal Station 562 face.
2. Hold through the mode ladder and release at the twelve-second **SERVICE
   CHANNEL** step.
3. Double swipe to enter Setup.
4. Short swipe to **SIGNAL CLASH TEAM**.
5. Hold for two seconds to select it.
6. Choose AUTO, RED, or BLUE, then hold for two seconds to save.

Changing teams does not erase the handle, rank, REP, or career. It can also be
done over USB with `wargames team <auto|red|blue>`.

### 5. Set A Handle

The badge creates an automatic hacker handle on first entry. To personalize it,
connect to the USB serial terminal and run:

```text
wg handle get
wg handle set YOUR_NAME
```

Use `wg handle randomize` to generate another automatic handle. Handles are
3-12 characters, lowercase becomes uppercase, and the allowed characters are
`A-Z`, `0-9`, `-`, `_`, and `+`. Spaces and reserved system names are rejected.

A handle can also be changed through the restricted Signal Clash GATT surface
while the badge is physically in the game. BLE handle changes require the
two-second sensor hold shown on the OLED. Signal Clash does not expose a general
BLE terminal.

### 6. Find And Attack An Opponent

Both badges must be in Signal Clash and on opposing teams. The badge
automatically chooses the strongest qualified opposing signal; no target ID is
entered.

For a basic **PORT SCAN**:

1. Wait for the OLED to show a target.
2. Begin with your hand clear.
3. Move your hand from far to close over the sensor.
4. Pull your hand completely away.
5. Read the large attack result.

A successful capture changes the target to your team. Three acknowledged Port
Scan attacks charge **0.DAY**, a stronger depth-and-hold attack. Performing the
same Port Scan gesture against an extremely close, stable target automatically
qualifies as **COVERT INTRUSION** and can earn bonus REP.

### 7. Defend Your Badge

An incoming attack opens a full-screen defense choice.

**FIREWALL**

Move close, hold steady, and use the shrinking ring guide to match the target
depth. A strong defense can block the attack; a good defense reduces its chance
of success.

**EVADE**

1. Swipe once to choose Evade and start the moving marker.
2. Swipe once more to commit the marker's current position.

Evade accepts one committed timing attempt. Clear success and failure screens
show the outcome. A stored **PATCH** automatically blocks one otherwise
successful attack.

### 8. Choose A Class

Signal Clash calls classes **disciplines**. Discipline selection unlocks at
SPECIALIST, after 100 REP and three unique captures. It is not available to a
new PROSPECT.

When the choice unlocks, follow the OLED selection screen. The complete powers
are available from the USB terminal:

```text
wg disciplines
```

The owner command below can make the selection while the discipline-choice
window is active:

```text
wg choose breaker
wg choose ghost
wg choose cipher
wg choose handler
```

Choose carefully. A discipline is permanent for that player identity. Changing
it requires **BURN HANDLE / FACTORY RESET**, which erases the entire career.

### 9. Understand Network Fork

If every locally visible badge belongs to one team, combat pauses and the OLED
shows **NETWORK OWNED**. After five continuous minutes without an opposing
signal, each badge receives a 60-second **NETWORK FORK** offer.

- Double swipe **BREAK CONSENSUS** to defect to the opposing team.
- Do nothing to remain on the winning team.

Each badge chooses independently. A defector receives 15 seconds of capture
protection and a temporary Fork Advantage. If nobody defects, another offer
appears after the next domination interval.

### 10. The Basic Objective

The everyday loop is simple:

1. find opposing badges;
2. attack, defend, and capture;
3. earn REP and unique-capture credit;
4. unlock a discipline;
5. advance from PROSPECT toward ROOT.

Same-team badges are allies, not valid attack targets. Signal Clash is intended
for casual all-day roaming, so no external match controller is needed.

## Extended Guide

### Identity And Persistence

On first Signal Clash initialization, the badge:

- reads its immutable hardware-derived badge ID;
- creates a random identity epoch;
- generates a per-player P-256 keypair;
- creates an automatic themed handle;
- starts at PROSPECT;
- stores the career in redundant NVS records.

The private player key remains on the badge. Reboots and normal V6.3.0 updates
preserve the identity, team preference, counters, rank, discipline, payloads,
and ROOT certificate.

### Radio Targeting

Signal Clash scans and advertises concurrently while active. It chooses the
strongest qualified opposing peer and gives a locked target a grace period for
ordinary packet loss.

The regular attack threshold is approximately `-70 dBm`. Covert Intrusion
requires a stable peer around `-52 dBm` plus several confirming observations.
RSSI is not a precise distance measurement. Bodies, cases, walls, antenna
orientation, and radio congestion all affect it.

### Port Scan Details

The accepted far-close-far cover is deliberately broad, roughly 40-1000 ms in
the gesture model. Motion is classified STANDARD, CLEAN, or PRECISE.

| Result quality | Compromise effect |
| --- | ---: |
| Base Port Scan | 45% |
| CLEAN | +8 percentage points |
| PRECISE | +15 percentage points |

The final probability is clamped to 25-90% after active modifiers.

### 0.DAY Details

Three acknowledged Port Scan attacks charge 0.DAY. When it is ready:

1. use the circular guide to move into the target depth band;
2. hold steadily for about 0.9-3.5 seconds;
3. release.

0.DAY begins with a 70% compromise chance before quality, discipline, Heat,
ally, payload, and target modifiers. A stored offensive 0.DAY payload can add
20 percentage points where the combat path permits it.

### Covert Intrusion Details

Covert Intrusion is an automatic close-range form of Port Scan. It uses the
same far-close-far gesture and requires no separate menu. A credited Covert
Intrusion capture awards five bonus REP.

### Attack Modifiers

| Modifier | Effect |
| --- | ---: |
| BREAKER discipline | +6 percentage points |
| Nearby HANDLER ally | +6 percentage points |
| Fork Advantage | +8 percentage points |
| Exposed H3 target | +8 percentage points |
| Offensive 0.DAY payload | +20 percentage points |
| TRACE after a failed attack | +10 per stack, maximum two |

TRACE lasts about 18 seconds. A captured badge changes team before it
acknowledges the result, and the attacker receives capture credit only after
that acknowledgment. The captured badge then receives about 3.5 seconds of
protection.

### Defense Details

The defense window is designed to allow normal human reaction time. No input
keeps the bounded window open, while a decisive successful gesture resolves
immediately.

For Firewall, about one second establishes the hold and roughly two more
seconds judge stability. PRECISE blocks the attack; CLEAN reduces compromise
chance by 20 percentage points.

For Evade, PRECISE blocks the attack and CLEAN reduces compromise chance by 15
percentage points. GHOST may also receive an automatic 6% evade.

A defensive PATCH blocks one otherwise successful attack and is consumed.
CIPHER regenerates a missing roaming PATCH after 90 seconds.

### Heat And Exposure

Aggressive activity raises Heat from H0 through H3. Heat cools every 15 seconds
during normal roaming. GHOST cools every nine seconds. At H3, the badge is
exposed and a successful opposing hack can award bonus REP.

### REP And Career Progression

| Rank | Automatic requirement |
| --- | --- |
| PROSPECT | Starting rank |
| OPERATOR | 50 REP and 1 unique captured badge |
| SPECIALIST | 100 REP and 3 unique captured badges |
| MADE | 150 REP and 5 unique captured badges |
| CELL_LEADER | 250 REP, 10 unique captures, and 3 combined successful defenses, evasions, or assists |
| ROOT eligible | 250 REP and 10 unique captures |
| ROOT | Successful three-badge physical induction |

ROOT eligibility depends only on REP and unique captures, regardless of the
automatic rank. Statistics alone never grant ROOT.

| Event | REP |
| --- | ---: |
| Confirmed capture | 10 |
| Covert Intrusion bonus | 5 |
| Successful Firewall or Evade | 4 |
| HANDLER assist | 4 |
| Successful hack of an exposed H3 target | 5 |

Capture and defense REP has a ten-minute per-opponent anti-farm window.
Lifetime counters still update when repeat REP is suppressed. Each hardware
badge ID grants unique-capture credit once.

Rank promotion, five and ten unique captures, ROOT eligibility, and ROOT
induction trigger interruptible OLED and LED celebrations. If one result earns
several milestones, the badge shows only the highest-value event:

```text
ROOT INDUCTED > ROOT ELIGIBLE > RANK UP > 10 UNIQUE > 5 UNIQUE
```

### Discipline Powers

| Discipline | Power |
| --- | --- |
| BREAKER | Adds 6 percentage points to compromise probability |
| GHOST | Approximately 6% automatic evade and Heat cools every 9 seconds |
| CIPHER | Regenerates one missing PATCH after 90 seconds |
| HANDLER | Nearby teammates gain +6 attack chance; a confirmed teammate-assisted capture awards the Handler an assist and 4 REP |

### Payloads

Reaching OPERATOR grants an offensive 0.DAY payload and a defensive PATCH when
the matching slot is empty. Every five unique opponents may refill one missing
payload, alternating the preferred slot. Payloads persist with the career.

### ROOT Induction Ceremony

An eligible candidate needs three physical badges:

1. the eligible candidate;
2. a ROOT sponsor;
3. a different ROOT witness.

The ceremony does not require matching teams, a computer, a phone, or an
offline signing key.

1. On the candidate, enter Setup and select **REQUEST INDUCTION**.
2. On each ROOT badge, enter Setup and select **ROOT INDUCTION**.
3. Assign one ROOT as SPONSOR and the other as WITNESS.
4. Follow the hold confirmation shown on each OLED.
5. Keep the three badges powered and nearby until all show the final result.

The badges temporarily use `S562 INDUCTION` BLE discovery and a dedicated GATT
exchange. Sponsoring consumes one of the ROOT badge's two lifetime sponsorship
slots. Witnessing consumes no slot.

### ROOT Combat

ROOT cannot be captured by one ordinary non-ROOT attack.

- Non-ROOT attacks against ROOT become raid hits.
- Five unique non-ROOT attackers must land accepted hits within 90 seconds.
- A non-ROOT 0.DAY does not bypass the ROOT guard.
- ROOT-versus-ROOT 0.DAY uses the normal strong-attack path.

### Terminal Game Commands

Connect to the USB serial terminal at 115200 baud. The complete connection and
session instructions are in the
[Terminal and BLE Reference](STATION562_TERMINAL_AND_BLE_REFERENCE.md).

| Command | Purpose |
| --- | --- |
| `wargames enter` / `wg enter` | Enter Signal Clash |
| `wargames exit` / `wg exit` | Exit Signal Clash |
| `wargames status` / `wg status` | Show game, sensor, peer, and radio state |
| `wargames stats` / `wg stats` | Show complete career and game counters |
| `wargames peers` | Show currently visible peers |
| `wargames team <auto\|red\|blue>` | Set team preference |
| `wg act` | Perform the current context action |
| `wg input <sensor\|auto>` | Restore physical or automatic game input |
| `wg whoami` | Show identity, certificate, and key fingerprint |
| `wg handle get` | Show the current handle |
| `wg identity status` | Show player identity state |
| `wg disciplines` | List discipline powers and selection rules |
| `wg choose <breaker\|ghost\|cipher\|handler>` | Select an unlocked discipline |
| `wg handle set NAME` | Set the player handle |
| `wg handle randomize` | Generate a new automatic handle |
| `wg ceremony status` | Show current ceremony role and radio state |
| `wg ceremony log` | Show the bounded ceremony trace |
| `wg ceremony abort` | Abort this badge's ceremony role |

`wg handle` by itself is incomplete. Use `wg handle get`, `wg handle set NAME`,
or `wg handle randomize`.

### BLE Game Access

While physically in Signal Clash, its restricted GATT surface accepts game
status, stats, actions, input selection, discipline choice, and read-only
identity requests. Handle mutation requires the two-second physical hold and a
retry if requested by the result transaction.

This surface never exposes arbitrary USB terminal commands, Burn Handle, or
factory reset. The exact UUIDs, JSON envelope, result codes, and nRF Connect
workflow are in the
[Terminal and BLE Reference](STATION562_TERMINAL_AND_BLE_REFERENCE.md).

### Burn Handle / Factory Reset

Setup **BURN HANDLE** and USB `factory-reset confirm` are the same destructive
player reset. They erase Setup and MIDI preferences plus the Signal Clash
handle, career, identity epoch, player keypair, team, discipline, counters,
payloads, and ROOT certificate, then reboot.

They do not change the immutable hardware badge ID or remove the hardware CTF.
The next Signal Clash initialization creates a new PROSPECT identity.

Do not use Burn Handle to leave the game, change teams, or recover from a
missed gesture.

### Troubleshooting

For missing targets, unreliable swipes, entry or exit trouble, BLE discovery,
and power questions, use the
[Troubleshooting FAQ](STATION562_TROUBLESHOOTING.md).
