# Station 562 V6.3.0 Hardware Pinout

This is the production firmware pin assignment for the two supported Station
562 targets. GPIO numbers are ESP32 GPIO numbers, not physical connector-pin
numbers.

This reference is included so owners can write their own independent firmware
and use the badge hardware for other projects. The official Station 562 source
is not required to address the OLED, sensor, or LEDs described here.

Custom firmware is outside the supported production release. A sketch with a
different partition layout, whole-chip erase, factory reset, or NVS writes can
remove the Station 562 handle, career, keypair, ROOT certificate, settings, or
CTF. The public updater can reinstall the official firmware/CTF bundle, but it
cannot reconstruct owner data that was erased.

## CodeCell ESP32-C3

| Function | Connection | Notes |
| --- | --- | --- |
| I2C SDA | GPIO8 | Shared by OLED and VCNL4040 |
| I2C SCL | GPIO9 | Shared by OLED and VCNL4040 |
| OLED | I2C address `0x3C` | 128x64 SSD1306; no dedicated reset pin |
| Proximity/light sensor | I2C address `0x60` | Onboard VCNL4040, accessed through the CodeCell library |
| External LED chain | GPIO5 | 16 SK6812-EC20 addressable RGB LEDs, GRB, 800 kHz |

The CodeCell sensor initializes the shared I2C bus at 400 kHz. GPIO6 is not
used by the Station 562 LED subsystem. The separate onboard CodeCell status LED
is forced off by production firmware and is not part of the 16-pixel animation
chain.

## Seeed Studio XIAO ESP32-C6

### Shared I2C Bus

| Function | XIAO label | ESP32-C6 GPIO | Notes |
| --- | --- | --- | --- |
| I2C SDA | D4 | GPIO22 | OLED and VCNL4040 data |
| I2C SCL | D5 | GPIO23 | OLED and VCNL4040 clock |
| Sensor interrupt | D3 | GPIO21 | Wired/configured, but V6.3.0 polls the sensor with interrupts disabled |

The OLED and sensor intentionally use the same SDA/SCL wires. I2C allows this
because each peripheral has a different address:

| Peripheral | I2C address |
| --- | --- |
| SSD1306 OLED | `0x3C` |
| VCNL4040 proximity/ambient/white-light sensor | `0x60` |

The XIAO production bus runs at 100 kHz. The OLED has no dedicated reset pin.

### Five PWM LEDs

The XIAO badge has five discrete red/white LED channels rather than a serial
RGB pixel chain.

| Channel | XIAO label | ESP32-C6 GPIO | Physical color |
| --- | --- | --- | --- |
| 0 | D6 | GPIO16 | White |
| 1 | D7 | GPIO17 | Red |
| 2 | D8 | GPIO19 | Red |
| 3 | D9 | GPIO20 | White |
| 4 | D10 | GPIO18 | Red |

Firmware drives these channels with 5 kHz, 8-bit PWM. Existing animations use
a 16-position logical layout that is compressed onto the five physical
channels:

| Logical LED positions | Physical channel |
| --- | --- |
| 0-2 | 0 / GPIO16 |
| 3-5 | 1 / GPIO17 |
| 6-8 | 2 / GPIO19 |
| 9-11 | 3 / GPIO20 |
| 12-15 | 4 / GPIO18 |

The XIAO onboard status LED is GPIO15, active-low. Production firmware keeps it
off; it is not part of badge animations.

## Electrical Notes

- Use 3.3 V logic and a common ground.
- Do not apply 5 V logic directly to ESP32 GPIO pins.
- Sharing SDA/SCL is correct; do not add another device at `0x3C` or `0x60`
  without changing its address or isolating the bus.
- These assignments describe the frozen V6.3.0 badge wiring. They are not a
  generic ESP32-C3 or ESP32-C6 development-board pinout.
