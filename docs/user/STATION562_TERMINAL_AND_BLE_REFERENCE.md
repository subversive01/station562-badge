# Station 562 V6.3.0 Terminal And BLE Command Reference

This is the production command reference for badge owners, musicians, and event
operators. Puzzle and CTF discovery commands are intentionally left to the
badge's own `help` output and recovered instructions.

Public display language says **Signal Clash**. USB commands retain `wargames`
and `wg` for compatibility.

DeFUNKd means the autonomous nearby-badge social/dance mode. DEFUNKT562 is the
separate tamper-evident blackout mode. They are not two names for the same
feature.

## Safety First

- Use a USB data cable, not a charge-only cable.
- The terminal baud rate is always **115200** on both XIAO and CodeCell.
- Close serial monitors before flashing or opening the same port elsewhere.
- Read output before repeating a command.
- `factory-reset confirm` is destructive to owner settings and Signal Clash
  identity.
- `midi settings reset confirm` erases all saved MIDI data.
- Hardware exploration must remain read-only. Never improvise erase or write
  commands on a player badge.

## Find The USB Port

With Arduino CLI:

```sh
arduino-cli board list
```

Common port names:

- macOS: `/dev/cu.usbmodem1301`
- Linux: `/dev/ttyACM0`
- Windows: `COM4`

Reconnect the badge and run the command again if it is not listed.

## Open The Terminal

Recommended Arduino CLI command:

```sh
arduino-cli monitor \
  -p /dev/cu.usbmodem1301 \
  --config baudrate=115200,dtr=off,rts=off
```

Replace the example port with the detected port. Press `Ctrl-C` to exit.

Windows owners may use Arduino IDE Serial Monitor, PuTTY, or Tera Term at
115200 baud. Select a line ending that sends Enter/newline.

### `screen` On macOS Or Linux

Open:

```sh
screen /dev/cu.usbmodem1301 115200
```

Useful controls:

| Action | Keys or command |
| --- | --- |
| Detach without closing | `Ctrl-A`, then `D` |
| List sessions | `screen -ls` |
| Reattach | `screen -r SESSION_ID` |
| Close from inside | `Ctrl-A`, then `\`, then confirm |
| Close a stale named session | `screen -S SESSION_ID -X quit` |

`Sorry, could not find a PTY` usually means the device disconnected, the port
name changed, or another process owns it. Close the stale session, reconnect the
badge, list ports again, and reopen.

### Capture A Terminal Log

Arduino CLI can be copied from the terminal window. With `screen`, enable its
local log:

1. press `Ctrl-A`, then `H`;
2. reproduce the output;
3. press `Ctrl-A`, then `H` again to stop;
4. find `screenlog.0` in the directory where `screen` was started.

For any sensor diagnostic, preserve the complete BEGIN-to-END output block.

## Command Rules

Type:

```text
help
```

Commands are lowercase and exact. The line limit is 127 characters. Unknown
commands return:

```text
[CMD] error=unknown; send help
```

Mutating commands normally print `[MIDI] ok=...`, `[PERF] ok=...`,
`[WARGAMES] ok=...`, or a matching `error=...`. Run the related status command
afterward when the change matters.

## Core Commands

| Command | Purpose |
| --- | --- |
| `help` | Print the production command catalog |
| `version` | Print firmware, target, hardware, stable ID, and build ID |
| `sleep status` | Show software-standby state and gesture counters |
| `sleep enter` | Enter software standby when no mode blocks it |
| `sleep exit` | Wake from software standby |
| `factory-reset confirm` | Burn Handle, clear Setup/MIDI/Signal Clash NVS, and reboot |

`version` is the fastest way to verify a flashed badge. The expected release
field is `V6.3.0`.

## MIDI Status And Immediate Actions

| Command | Purpose |
| --- | --- |
| `midi status` | Compact JSON snapshot used by apps |
| `midi clock` | Clock, transport, BPM, counters, and beat-broadcast state |
| `midi auth` | Config-GATT authorization and cooldown state |
| `midi map` | Effective pitch, sensor, preset, and modifier map |
| `midi audition` | Play the built-in eight-note test through a connected host |
| `midi audition stop` | Stop the audition and clean up its notes |
| `midi panic` | Stop performance and send note/control cleanup |
| `midi expression send <0-127>` | Send one value to the active expression destination |
| `midi enter` | Enter MIDI Controller; USB only |
| `midi exit` | Exit MIDI Controller cleanly |

The badge makes no sound by itself. `midi audition` requires a connected host
with `S562_MIDI` routed to an audible instrument.

## MIDI Pitch And Playing Behavior

| Command | Accepted values |
| --- | --- |
| `midi preset <name>` | `lead`, `pluck`, `pad`, `run`, `hybrid`, `carrier` |
| `midi channel <n>` | 1-16 |
| `midi mode <mode>` | `scale`, `fixed` |
| `midi scale <name>` | `major`, `minor`, `pent`, `blues`, `chromatic` |
| `midi root <root>` | 0-11 or note name such as `C`, `F#`, `Bb` |
| `midi octave <n>` | 0-8 |
| `midi start <value>` | `root`, a scale note with octave, or MIDI note 0-127 |
| `midi span <n>` | 1-32 scale degrees |
| `midi note <n>` | MIDI note 0-127 and select fixed mode |
| `midi articulation <name>` | `swipe`, `pluck` |
| `midi gate <length>` | `free`, `1/16`, `1/8`, `1/4`, `1/2`, `1bar` |
| `midi retrigger <grid>` | `instant`, `1/16`, `1/8`, `1/4` |
| `midi dwell <ms>` | 0-500 |

Example: A minor beginning on C4, then save it:

```text
midi mode scale
midi root A
midi octave 3
midi scale minor
midi start C4
midi settings save
```

Example: C4 as the scale root and first note:

```text
midi mode scale
midi root C
midi octave 4
midi start root
midi settings save
```

`midi start` rotates the playable scale but does not change its key.

## MIDI Velocity And Expression

| Command | Purpose |
| --- | --- |
| `midi velocity <0-127>` | Set fixed velocity and select fixed mode |
| `midi velocity-mode <fixed|prox|inverse>` | Choose velocity model |
| `midi velocity-range <min> <max>` | Set proximity velocity output range |
| `midi expression <destination>` | `off`, `mod`, `expression`, `filter`, `reverb`, `cc`, `pitchbend`, `pressure` |
| `midi expression-source <source>` | `prox`, `ambient`, `white` |
| `midi expression invert <on|off>` | Reverse expression direction |
| `midi expression smooth <level>` | `off`, `light`, `medium`, `strong` |
| `midi expression-depth <min> <max>` | Set output depth, 0-127 |
| `midi cc <0-127>` | Select a custom CC destination |
| `midi cc-range <min> <max>` | Set expression sensor input range |
| `midi expression-range <min> <max>` | Alias for `midi cc-range` |

Carrier overrides several performance semantics while active: strike speed
drives Note On velocity, strike depth selects pitch, sustain drives CC74, CC1,
CC11, and Channel Pressure, and withdrawal speed sends CC91.

## MIDI Sensor Range And Tuning

| Command | Purpose |
| --- | --- |
| `midi note-range <far> <close>` | Replace the note range and clear a three-point curve |
| `midi threshold <enter> <exit>` | Set MIDI-only attack/release thresholds |
| `midi threshold reset` | Restore target thresholds |
| `midi tune status` | Live value, active range, curve, and capture state |
| `midi tune far` | Capture quick far point in MIDI Mode |
| `midi tune close` | Capture quick close point in MIDI Mode |
| `midi tune apply` | Apply quick far/close range |
| `midi tune start` | Start guided three-point tuning |
| `midi tune next` | Capture the displayed FAR, MID, or CLOSE point |
| `midi tune save` | Apply the completed three-point curve |
| `midi tune cancel` | Cancel guided capture |
| `midi tune reset` | Restore target tuning defaults |

Factory target defaults:

| Target | Note range | Expression range | Gate enter/exit |
| --- | ---: | ---: | ---: |
| XIAO ESP32-C6 | 30-550 | 30-410 | 50/24 |
| CodeCell ESP32-C3 | 30-410 | 0-420 | 100/80 |

Tuning changes only MIDI-local behavior. It does not alter the main menu,
Signal Clash, DeFUNKd, Setup, or DEFUNKT562 sensor logic.

## MIDI Persistence

| Command | Purpose |
| --- | --- |
| `midi scene status` | List four full-scene slots |
| `midi scene save <1-4>` | Save the complete active MIDI state |
| `midi scene load <1-4>` | Load a full scene into runtime |
| `midi scene clear <1-4>` | Clear a scene |
| `midi settings status` | Full active and saved MIDI summary |
| `midi settings save` | Save active state as startup default |
| `midi reset-current confirm` | Reset active MIDI state only |
| `midi settings reset confirm` | Erase all MIDI data, scenes, and user modifier slots |

Runtime edits set `dirty=1`. Use `midi settings save` only after testing the
new behavior.

## Performance Modifiers

General form:

```text
perf <setting> <off|subtle|medium|high|extreme>
```

Settings:

```text
expression gate repeat range chord motion velocity quantize glide phrase
```

| Command | Purpose |
| --- | --- |
| `perf status` | Print all modifier levels and user slots |
| `perf reset` | Turn all ten modifiers off |
| `perf preset clear-channel` | Neutral modifier combination |
| `perf preset numbers-station` | Numbers Station combination |
| `perf preset tower-sweep` | Tower Sweep combination |
| `perf preset repeater-storm` | Repeater Storm combination |
| `perf preset long-lines` | Long Lines combination |
| `perf user status` | List five modifier-only user slots |
| `perf user save <1-5>` | Save current modifier levels |
| `perf user load <1-5>` | Load one modifier combination |
| `perf user clear <1-5>` | Clear one modifier slot |

## Signal Clash Owner Commands

`wargames` and `wg` refer to Signal Clash.

| Command | Purpose |
| --- | --- |
| `wargames enter` / `wg enter` | Enter Signal Clash |
| `wargames exit` / `wg exit` | Exit Signal Clash |
| `wargames status` / `wg status` | Full runtime diagnostics |
| `wargames stats` / `wg stats` | Full career and game counters |
| `wargames peers` | Current peer/radio table |
| `wargames attack` | Send an attack intent when terminal input is enabled |
| `wargames join` | Accept a staged referee invitation |
| `wargames team <auto|red|blue>` | Change team preference |
| `wg act` | Context action: attack, defend, join, fork, or choose |
| `wg input <sensor|terminal|auto>` | Select game input ownership |
| `wg team <auto|red|blue>` | Team preference alias |
| `wg whoami` | Identity, certificate, and key fingerprint |
| `wg handle get` / `wargames handle get` | Read the current handle |
| `wg identity status` / `wargames identity status` | Read identity state |
| `wg disciplines` | Print discipline powers |
| `wg choose <breaker|ghost|cipher|handler>` | Choose an unlocked discipline |
| `wg handle set NAME` | Set a handle through the elevated path |
| `wg handle randomize` | Generate a handle through the elevated path |

`wg handle` by itself is incomplete and returns the unknown-command error.
Handle changes require `wg handle set NAME` or `wg handle randomize`.

Handles contain 3-12 visible characters. Lowercase letters are normalized to
uppercase. Valid characters are `A-Z`, `0-9`, `-`, `_`, and `+`; spaces and
reserved system, team, rank, and protocol names are rejected.

### ROOT Ceremony Commands

Normal ceremonies should be entered physically from Setup. USB diagnostics:

| Command | Purpose |
| --- | --- |
| `wg ceremony status` | Current ceremony role and radio state |
| `wg ceremony log` | Bounded ceremony trace |
| `wg ceremony abort` | Abort the local role |
| `wg ceremony enter <candidate|sponsor|witness>` | Developer diagnostic role entry |

The `enter` form bypasses physical menu navigation and should not be used to
claim a user-validated ceremony.

### Signal Clash Sensor Capture

These read-only diagnostics capture and summarize VCNL4040 behavior:

| Command | Purpose |
| --- | --- |
| `wargames sensor status` | Current capture state |
| `wargames sensor capture` | Start the default capture |
| `wargames sensor capture <2000-8000>` | Capture for an explicit duration in ms |
| `wargames sensor summary` | Human-readable metrics from the last capture |
| `wargames sensor dump` | Complete CSV evidence from the last capture |
| `wargames sensor cancel` | Cancel capture |

## Developer/Operator Signal Clash Diagnostics

These commands are compiled into production for event support but are not
ordinary player actions:

| Command | Purpose |
| --- | --- |
| `wg crypto benchmark` | USB cryptography timing diagnostic |
| `wg venue status` | Venue-object state |
| `wg venue dedicated <dead-drop|control-node [red|blue|none]|clear>` | Configure a dedicated object identity |
| `wg venue virtual add <slot> <dead-drop|control-node> [red|blue|none]` | Add a volatile referee-hosted object |
| `wg venue virtual clear` | Clear volatile objects |
| `wg visual <list|target|incoming|firewall|evade|attack success|attack failed|defense success|defense failed|clear>` | Preview visual states |

Developer builds may expose additional `wg fork` commands that are intentionally
omitted from `help`. Do not use hidden diagnostics as player mechanics.

## DeFUNKd Autonomous-Mode Signal Party Commands

| Command | Purpose |
| --- | --- |
| `signal hacked` | Start the clock-bound invitation burst |
| `signal restored` | Start the matching restoration burst |
| `signal status` | Print clock, prompt, token, Party, and restoration state |
| `signal prompt` | USB diagnostic: force the DeFUNKd prompt |
| `signal enter` | USB diagnostic: force Party visuals |
| `signal exit` | USB diagnostic: leave the visual overlay |
| `signal animation-info on` | Show animation diagnostic text |
| `signal animation-info off` | Hide diagnostic text |
| `signal animation-info status` | Read diagnostic-overlay state |

`signal hacked` and `signal restored` require active, running MIDI Clock on the
MIDI conductor. Clock alone never triggers the prompt. Restoration must come
from the same conductor token accepted by the follower.

## Experimental Referee Commands

These commands operate the archived/deferred best-of-three engine. They are
available for controlled development but are not a V6.3.0 event promise.

| Command | Purpose |
| --- | --- |
| `signal game arm` | Arm referee staging |
| `signal game disarm` | Stop referee staging/match |
| `signal game status` | Referee state |
| `signal game stats` | Referee and career counters |
| `signal game team <auto|red|blue>` | Referee/team preference |
| `signal game event zero-day-leak` | Bounded network event |
| `signal game event fbi-sweep` | Bounded network event |
| `signal game event lockdown <5-120|stop>` | Timed event |
| `signal game event blackout <5-120|stop>` | Timed event |

Do not confuse `signal game` with DeFUNKd `signal hacked`. They are different
protocol paths.

## Config GATT

### Services And Characteristics

Standard BLE MIDI:

- Service: `03B80E5A-EDE8-4B33-A751-6CE34EC4C700`
- Characteristic: `7772E5DB-3868-4112-A1A9-F2669D106BF3`

Station 562 config:

| Short label | Full UUID | Properties |
| --- | --- | --- |
| 5620 | `9C5E5620-4F52-4249-5441-4C4445430001` | Service |
| 5621 | `9C5E5621-4F52-4249-5441-4C4445430001` | Identity read |
| 5622 | `9C5E5622-4F52-4249-5441-4C4445430001` | Capabilities read |
| 5623 | `9C5E5623-4F52-4249-5441-4C4445430001` | Snapshot read |
| 5624 | `9C5E5624-4F52-4249-5441-4C4445430001` | Command write |
| 5625 | `9C5E5625-4F52-4249-5441-4C4445430001` | Result read/notify |
| 5626 | `9C5E5626-4F52-4249-5441-4C4445430001` | Signal Clash transaction |
| 5627 | `9C5E5627-4F52-4249-5441-4C4445430001` | Signal Clash result |

ROOT ceremony:

| Short label | Full UUID |
| --- | --- |
| 5630 | `9C5E5630-4F52-4249-5441-4C4445430001` |
| 5631 | `9C5E5631-4F52-4249-5441-4C4445430001` |
| 5632 | `9C5E5632-4F52-4249-5441-4C4445430001` |

### Command Envelope

Write UTF-8 JSON to 5624:

```json
{"schema":"station562.badge.config.command.v1","seq":100,"command":"midi status"}
```

Use a fresh sequence number for each write and retry. Command text is limited
to 127 characters; the complete payload is limited to 255 bytes.

Subscribe to 5625 notifications before writing. A result resembles:

```json
{"schema":"station562.badge.config.result.v1","seq":100,"ok":true,"code":"ok","dirty":0}
```

Match both `seq` and `code`. GATT reads can replay the current characteristic
value; do not treat an old sequence as the new result.

### nRF Connect Workflow

1. Put the badge in the mode that owns the requested command:
   - MIDI and DeFUNKd Signal Party commands use MIDI Controller and
     `S562_MIDI`.
   - Signal Clash commands use Signal Clash and `SIGNAL_CLASH`.
2. Connect to that advertised name in nRF Connect.
3. Expand the Station 562 config service whose UUID ends in `5620`.
4. Find result characteristic `5625` and enable notifications.
5. Find command characteristic `5624`, choose **Write**, and select
   UTF-8/text rather than hexadecimal input.
6. Paste one compact JSON object. Use straight ASCII quotes and a sequence
   number not already used on this connection.
7. Send the write and wait for a `5625` notification with the same `seq`.
8. Judge the request by both `ok` and `code`; an old characteristic value may
   be a replay of the previous result.

For Signal Clash transaction-level tests, use 5626/5627 according to the
transaction schema advertised in capabilities. Ordinary textual owner commands
use 5624/5625.

### SIGNAL HACKED

With the badge in MIDI Controller, a BLE MIDI host connected, Clock Out enabled,
and transport running, write this as UTF-8 text to `5624`:

```json
{"schema":"station562.badge.config.command.v1","seq":1,"command":"signal hacked"}
```

The matching `5625` notification must use `seq:1`. Expected successful codes
include `invitation_started` or `invitation_active`.

### SIGNAL RESTORED

Keep the same conductor and clock running, then use a fresh sequence:

```json
{"schema":"station562.badge.config.command.v1","seq":2,"command":"signal restored"}
```

The matching notification must use `seq:2`. Expected successful codes include
`restoration_started` or `restoration_active`.

These two exact commands are public and do not open ACCESS REQUEST.
nRF Connect only writes the event request; it does not generate MIDI Clock. If
the conductor does not already report active/running clock and nonzero BPM,
either command returns `clock_required`.

### Referee Arm And Disarm

The experimental referee surface is also available over GATT:

```json
{"schema":"station562.badge.config.command.v1","seq":210,"command":"signal game arm"}
```

```json
{"schema":"station562.badge.config.command.v1","seq":211,"command":"signal game disarm"}
```

Event injection commands are elevated and require authorization. Do not use the
referee engine for ordinary roaming Signal Clash.

## BLE Physical Authorization

### MIDI Configuration

The first protected `midi ...` or `perf ...` command on a connection returns:

```text
physical_confirmation_required
```

The badge opens **ACCESS REQUEST** for 20 seconds.

1. Verify that you initiated the request.
2. Double swipe the badge.
3. Wait for the same sequence to return `authorized`.
4. Retry the original command with a new sequence number.
5. The retry should return its normal success result.

Authorization lasts only for that BLE connection. Disconnect, MIDI exit, reboot,
or BLE reset revokes it. New prompts have a 25-second cooldown. Active clock,
note performance, or audition can temporarily return `performance_active`.

`factory-reset confirm` always returns `command_not_allowed` over BLE.

### Signal Clash Handle Changes

While physically in Signal Clash, status, stats, actions, input selection,
discipline choice, and identity reads are public game intents. Handle mutation
is elevated:

1. send `wg handle set NAME` or `wg handle randomize`;
2. hold the badge sensor for two seconds when asked;
3. retry with a new sequence if the result contract requests it.

No other USB terminal surface is exposed over BLE.

## Common Result Codes

| Code | Meaning |
| --- | --- |
| `ok` | Request completed |
| `physical_confirmation_required` | Physical approval opened |
| `authorized` | Connection approved |
| `authorization_pending` | This connection already owns a request |
| `authorization_busy` | Another connection owns the request |
| `authorization_rate_limited` | Wait for the prompt cooldown |
| `authorization_timeout` | Approval window expired |
| `performance_active` | Protected prompt cannot interrupt performance |
| `command_not_public` | Outside the accepted BLE surface |
| `command_not_allowed` | Deliberately forbidden over BLE |
| `clock_required` | Start MIDI Clock and transport first |
| `mode_inactive` | Enter the required physical mode |
| `control_busy` | Another input/connection owns the action lease |

## Recommended Verification Recipes

### Verify A Flash

```text
version
```

Confirm:

- firmware `V6.3.0`;
- correct XIAO or CodeCell target;
- expected stable hardware ID.

### Verify MIDI Without Playing

```text
midi enter
midi status
midi map
midi audition
midi audition stop
midi panic
midi exit
```

### Inspect A Signal Clash Career

```text
wargames enter
wg whoami
wg stats
wargames peers
wargames exit
```

### Restore Normal Sensor Control After Diagnostics

```text
wg input sensor
```

or:

```text
wg input auto
```

Do this before handing the badge back to a player.
