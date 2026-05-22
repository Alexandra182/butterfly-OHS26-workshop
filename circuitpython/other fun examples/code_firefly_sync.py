"""Firefly synchronization via IR (Mirollo-Strogatz coupled oscillators).

Each butterfly ramps brightness over a fixed PERIOD, flashes when its
phase hits 1, broadcasts an IR pulse, and resets. Neighbors that hear
the pulse nudge their own phase forward by COUPLING. Start the room
desynchronized; within ~30s the whole swarm converges to flash in unison.
"""
import board
import neopixel
import pulseio
import adafruit_irremote
import time
import random

# --- NeoPixel setup ---
pixels = neopixel.NeoPixel(board.GP2, 26, brightness=0.3, auto_write=False)

# --- IR (Qwiic): receiver on GP0, transmitter on GP1 ---
pulsein = pulseio.PulseIn(board.GP0, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()
pulseout = pulseio.PulseOut(board.GP1, frequency=38000, duty_cycle=2**15)
encoder = adafruit_irremote.GenericTransmit(
    header=[9000, 4500], one=[560, 1690], zero=[560, 560], trail=0
)

# All butterflies in the swarm share this NEC address/command
SYNC_ADDRESS = 0xF1
SYNC_COMMAND = 0x55

# Tunables — the workshop crowd can play with these
PERIOD = 2.0          # seconds per blink cycle
COUPLING = 0.12       # phase kick on hearing a neighbor's pulse (0..1)
REFRACTORY = 0.3      # ignore IR for this long after firing (anti-echo)
FLASH_COLOR = (220, 180, 60)  # warm firefly yellow

# Random start phase so the room is initially desynchronized
phase = random.random()
last_tick = time.monotonic()
last_fire = -10.0


def render(p):
    # phase**8 keeps most of the cycle dark with a sharp peak near p=1
    scale = p ** 8
    r, g, b = FLASH_COLOR
    pixels.fill((int(r * scale), int(g * scale), int(b * scale)))
    pixels.show()


def fire():
    pixels.fill(FLASH_COLOR)
    pixels.show()
    encoder.transmit(
        pulseout,
        [SYNC_ADDRESS, ~SYNC_ADDRESS & 0xFF, SYNC_COMMAND, ~SYNC_COMMAND & 0xFF],
    )
    # Drop the buffered echo of our own transmission so we don't kick ourselves
    pulsein.clear()


print(f"Firefly sync — period={PERIOD}s, coupling={COUPLING}")
print(f"Sync code: 0x{SYNC_ADDRESS:02X}/0x{SYNC_COMMAND:02X}")

while True:
    now = time.monotonic()
    dt = now - last_tick
    last_tick = now

    phase += dt / PERIOD

    if phase >= 1.0:
        phase = 0.0
        last_fire = now
        fire()

    # Listen for neighbors (skip during refractory window after firing)
    if now - last_fire > REFRACTORY:
        pulses = decoder.read_pulses(pulsein, max_pulse=10000, blocking=False)
        if pulses:
            try:
                code = decoder.decode_bits(pulses)
                if (
                    len(code) == 4
                    and code[0] == SYNC_ADDRESS
                    and code[2] == SYNC_COMMAND
                ):
                    phase = min(1.0, phase + COUPLING)
            except adafruit_irremote.IRNECRepeatException:
                pass
            except adafruit_irremote.IRDecodeException:
                pass

    render(phase)
    time.sleep(0.01)
