# Build Your Own Butterfly-Shaped Wearable

A hands-on workshop at the **Open Hardware Summit 2026** where you build and personalize your own butterfly-shaped wearable device.

**Date:** Sunday, May 24, 2026, 2:00 PM – 4:00 PM CEST
**Location:** TU Berlin, Room 2, Berlin, Germany
**Register:** [Eventbrite](https://www.eventbrite.com/e/build-your-own-butterfly-shaped-wearable-at-the-open-hardware-summit-2026-tickets-1983821948852)

This repo contains firmware and code examples for two beginner-friendly programming environments: **CircuitPython** and **MicroBlocks**.

The badge is built around an **RP2040** microcontroller and features **26 NeoPixel LEDs** arranged in a butterfly shape, plus a **Qwiic connector** for attaching modules such as an IR transceiver for badge-to-badge communication.

---

## What You'll Do

- Program the butterfly wearable using CircuitPython
- Learn embedded systems fundamentals with the RP2040
- Integrate NeoPixel LEDs and an IR transceiver
- Code a swarm effect where butterflies communicate and glow in sync
- Leave with a functional, open-source wearable

---

## What's Provided

- Custom butterfly-shaped PCB
- IR transceiver module
- USB-C to USB-A cable

Bring a laptop with a USB port. LiPo batteries are not included; the badge runs on USB power during the workshop.

---

## Hardware

| Component | Details |
|---|---|
| Microcontroller | RP2040 |
| LEDs | 26 × NeoPixel (WS2812B), wired to **GP2** |
| Qwiic connector | GND, 3V3, **GP1** (pin 2), **GP0** (pin 3) |

---

## Getting Started

The board supports two programming environments: **CircuitPython** and **MicroBlocks**. Each has its own bootloader in its respective folder.

### Entering bootloader mode

1. Press and hold the pushbutton on the board while powering it on (plugging in the USB).
2. A new drive will appear on your computer.
3. Drag the bootloader `.uf2` file onto that drive. The board will reboot automatically.

### Option A - CircuitPython

1. **Flash the bootloader** - drag `circuitpython/bootloader/adafruit-circuitpython-raspberry_pi_pico-en_GB-9.2.9.uf2` onto the drive. The board reboots as a `CIRCUITPY` drive.

2. **Copy the libraries** - copy the contents of `circuitpython/libraries/` into the `lib/` folder on the `CIRCUITPY` drive.

3. **Copy a code example** - copy one of the `.py` files from `circuitpython/workshop_exercises/` (or `circuitpython/other fun examples/`) onto the `CIRCUITPY` drive and rename it `code.py`. The board runs `code.py` automatically on boot.

4. **Serial console (optional)** - connect with any serial terminal (115200 baud) or use the [Mu editor](https://codewith.mu/) to see `print()` output.

### Option B - MicroBlocks

1. **Flash the bootloader** - drag `microblocks/bootloader/vm_pico_w.uf2` onto the drive.

2. **Open MicroBlocks** - download the [MicroBlocks IDE](https://microblocks.fun) or use the browser-based version, then connect to the board over USB and start building block programs.

---

## Workshop Exercises

The workshop is built around five bite-sized exercises in `circuitpython/workshop_exercises/`. Each one is self-contained, prints to the serial console, and ends with challenges for fast finishers. Work through them in order - they build skill by skill.

| File | Skill |
|---|---|
| `01_addressing_leds.py` | Address the 26 NeoPixels one at a time |
| `02_loops_and_brightness.py` | Animate color and brightness over time with loops |
| `03_wing_flap.py` | Map code to the physical wing shape (distance from the body) |
| `04_first_ir_message.py` | Send and receive a message between two boards over IR |
| `05_color_stack.py` | Capstone: catch neighbors' colors over IR; each catch shifts them out along your wings |

After the exercises, flash one of the swarm examples below for the group finale.

## Other Fun Examples

Ready-to-run demos in `circuitpython/other fun examples/`. All use 26 NeoPixels on **GP2** at up to 30% brightness.

| File | Description |
|---|---|
| `code-single-neopixel.py` | Turns all 26 LEDs solid purple - good first test |
| `code_fade_inout.py` | Pulses all LEDs purple, fading smoothly between 1% and 30% brightness |
| `code_rainbow.py` | Cycles a full rainbow across all LEDs |
| `code_rainbow_cycling.py` | Rotates a rainbow pattern around the LEDs |
| `code_rainbow_fade.py` | Rotating rainbow with a sine-wave brightness pulse |
| `code_wing_flap.py` | Sweeps light from the body out to the wingtips and back |
| `code_wing_flap_gradient.py` | Wing flap colored by distance from the body |
| `code_ir_send.py` | Displays a rainbow and broadcasts the pattern via IR every 3 seconds |
| `code_ir_receive.py` | Listens for an IR pattern signal and plays a rainbow animation when received |
| `code_ir_transceiver.py` | Low-level IR send/receive demo (receives any NEC signal, transmits every 5 s) |
| `code_firefly_sync.py` | Mirollo-Strogatz firefly sync - butterflies flash periodically and converge to blink in unison via IR |
| `code_color_trade.py` | Each butterfly starts with a random vibrant color and blends toward the colors of nearby butterflies via IR |
| `code_relay_wave.py` | A rotating rainbow that ripples butterfly-to-butterfly via IR, dying out after a fixed number of hops |

### Trying an example

```
# Copy to CIRCUITPY drive and rename:
cp circuitpython/workshop_exercises/01_addressing_leds.py /media/$USER/CIRCUITPY/code.py
```

---

## IR Transceiver

### Wiring

Connect the IR transceiver module to the Qwiic connector on the butterfly board using the following pinout:

| RP2040 | IR module |
|---|---|
| 3V3 | VIN |
| GND | GND |
| GP0 | IRin |
| GP1 | IRout |

### Usage

An IR transceiver module can be connected via the Qwiic connector (GP0 / GP1). `code_ir_transceiver.py` demonstrates badge-to-badge communication:

- **Receives** IR signals and prints the decoded bytes.
- **Transmits** a configurable NEC command every 5 seconds.

To change what is sent, edit these two lines at the top of the file:

```python
SEND_ADDRESS = 0x00
SEND_COMMAND = 0x16
```

Requires the `adafruit_irremote` and `pulseio` libraries installed on the `CIRCUITPY` drive.

---

## Repository Layout

```
butterfly-OHS26-workshop/
├── circuitpython/
│   ├── bootloader/             # CircuitPython 9.2.9 UF2 for Pico W
│   ├── libraries/              # Drop required .mpy libraries here
│   ├── workshop_exercises/     # The five guided workshop exercises (start here)
│   └── other fun examples/     # Ready-to-run demos and swarm firmware
└── microblocks/
    └── bootloader/             # MicroBlocks VM UF2 for Pico W
```

---

## License

See [LICENSE](LICENSE) for details.
