# Station 562 V6.3.0 Troubleshooting FAQ

Start with the least disruptive action. Do not use factory reset, Burn Handle,
whole-chip erase, eFuse commands, or raw NVS writes as troubleshooting steps.

## The OLED Is Off

The badge may be in software standby rather than powered off.

1. Remove your hand and leave the sensor completely clear.
2. Look for one faint red heartbeat about every ten seconds.
3. Perform five deliberate short swipes within nine seconds to wake it.
4. If USB terminal access is available, run `sleep status`, followed by
   `sleep exit` if needed.

Software standby turns off the OLED and BLE, but it is not deep sleep and still
uses battery.

## The Badge Appears Frozen

Perform a complete power cycle:

1. Disconnect USB.
2. Unplug the battery connector without pulling on its wires.
3. Wait ten seconds.
4. Connect USB only and check whether the badge starts.
5. Reconnect the battery after normal operation returns.

Removing USB alone is not a complete reset while the battery remains connected.

## A Swipe Does Not Register

The sensor will not recognize every hand movement.

- Swipe over the sensor at the top of the badge.
- Begin with your hand clearly away from the sensor.
- Move close, then pull completely away.
- Pause briefly with the sensor clear before the next swipe.
- Use two separate movements for a double swipe.
- Avoid extremely fast passes.
- Retry the gesture if the badge does not acknowledge it.

For a hold, move close and remain steady. Do not repeatedly move in and out of
range unless the screen specifically asks for swipes.

## A Confirmation Window Disappeared

Move your hand away and repeat the mode-entry hold. Release only after the
desired loading step completes, then perform two distinct swipes. If one swipe
is missed, try the complete entry sequence again.

## The Wrong Mode Opens

The main hold ladder continues advancing while the sensor remains covered:

| Approximate hold | Selection |
| ---: | --- |
| 2 seconds | Station 562 / Control Room face |
| 4 seconds | Signal Clash |
| 6 seconds | DeFUNKd |
| 8 seconds | MIDI Controller |
| 10 seconds | DEFUNKT562 |
| 12 seconds | Setup / Service Channel |

Release when the intended loading step completes. Signal Clash, MIDI,
DEFUNKT562, and Setup then require double-swipe confirmation.

## Signal Clash Will Not Exit

1. Hold very close for five seconds.
2. Keep holding when the full-screen **KEEP HOLD** progress appears after about
   three seconds.
3. Release when asked.
4. Double swipe within four seconds.

If the final swipes are missed, return to the normal roaming screen and repeat
the complete exit sequence. USB owners may also use `wargames exit`.

## DeFUNKd Will Not Exit

Hold the sensor continuously for about three seconds. Keep your hand steady
until the exit feedback completes. If nothing happens, clear the sensor and
repeat the hold.

## MIDI Controller Will Not Exit

A phone, tablet, computer, or music app may still hold the BLE connection.

1. Disconnect `S562_MIDI` from the host's Bluetooth MIDI panel.
2. Close any app that automatically reconnects. Turn off Bluetooth temporarily
   if the connection immediately returns.
3. After disconnect, the badge allows about 45 seconds for reconnection and
   then shows an exit prompt.
4. Double swipe within four seconds to exit.

USB terminal access provides an immediate fallback:

```text
midi exit
```

With no host and no activity, MIDI Controller exits automatically after about
two minutes.

## DEFUNKT562 Will Not Exit

DEFUNKT562 is intentionally harder to leave than the everyday modes. Follow the
complete **DEFUNKT562 Service Exit** procedure in the
[Advanced Owner Guide](STATION562_ADVANCED_OWNER_GUIDE.md#defunkt562-service-exit).

## Setup Feels Unresponsive

- Use one short, deliberate swipe to move between items or choices.
- Fully uncover the sensor after each swipe.
- Hold steadily for about two seconds to select or save.
- Use **RETURN TO STATION** to exit normally.

Do not select **BURN HANDLE** as a way to leave Setup. Burn Handle erases the
player identity, career, team, keypair, ROOT certificate, and saved settings.

## The Expected BLE Name Is Missing

BLE identity changes with mode:

| Mode | Name or behavior |
| --- | --- |
| Station 562 puzzle | `STATION_562` |
| Signal Clash | `SIGNAL_CLASH` |
| DeFUNKd | `DEFUNKD_562` |
| MIDI Controller | `S562_MIDI` |
| DEFUNKT562 armed | BLE silent |
| DEFUNKT562 alert | `562_ALERT!` |
| Software standby | BLE off |

Confirm the OLED mode, stop and restart scanning, and allow several seconds for
the new advertisement. A badge already connected to another phone or app may
not accept a second connection; disconnect or disable Bluetooth on the previous
host.

## MIDI Connects But Produces No Sound

The badge is a MIDI controller and has no sound engine.

1. Connect to `S562_MIDI` from the app's Bluetooth MIDI panel.
2. Select it as a MIDI input.
3. Arm or select an audible software instrument.
4. Run `midi audition` from USB to test the route.
5. Run `midi audition stop` afterward.

If the app receives MIDI but remains silent, check the app's instrument and
audio routing.

## MIDI Clock Or SIGNAL HACKED Does Not Work

- Connect the conductor as `S562_MIDI`.
- Enable MIDI Clock Out in the host.
- Start host transport after connecting.
- Run `midi clock` and confirm active clock, running transport, nonzero BPM.
- Put follower badges in DeFUNKd.

nRF Connect can send `signal hacked` and `signal restored`, but it cannot
generate MIDI Clock. A `clock_required` result means the host clock or transport
is not active.

## Signal Clash Shows No Target

- Both badges must be in Signal Clash.
- They must currently be on opposing teams.
- Bring the badges closer and allow several seconds for radio observations to
  stabilize.
- Keep bodies, bags, and large objects from blocking the badges while checking.
- Run `wargames peers` over USB to view the current peer table.

Team preference can be changed from Setup under **SIGNAL CLASH TEAM**.

## DeFUNKd Does Not See Other Badges

Confirm every participating badge displays DeFUNKd rather than Signal Clash,
MIDI Controller, or the normal Station 562 face. Keep the badges near one
another and allow several seconds for the social state to stabilize. If one
badge remains absent, perform a complete power cycle on that badge.

## Battery Drains While Stored

Software standby is not power-off. For storage, disconnect the battery. The
firmware does not report battery percentage, voltage, or remaining runtime.

## The Computer Shows No Serial Port

- Confirm the USB cable carries data.
- Close programs that may already own the port.
- Avoid an unpowered hub.
- Try another cable or USB port.
- Disconnect and reconnect the badge.
- Run `python tools/flash_station562.py --list` again.

For ROM bootloader entry, follow the XIAO or CodeCell instructions in
[Platform Recovery](../SELF_FLASH_GUIDE.md#platform-recovery).

## An Update Was Interrupted

Reconnect the badge and rerun the same updater command. The updater verifies the
target and release bundle before writing. If normal detection fails, use the
hardware-specific [Platform Recovery](../SELF_FLASH_GUIDE.md#platform-recovery)
procedure.

If the ESP32 ROM loader still does not appear, the public updater cannot recover
the badge.

## The Handle, Career, Or ROOT Status Is Missing

Do not run another reset. A normal V6.3.0 update preserves owner NVS. Check:

```text
version
wg whoami
wg stats
```

Burn Handle, `factory-reset confirm`, whole-chip erase, or manual NVS writes can
remove owner data. Reflashing cannot reconstruct data that was erased.
