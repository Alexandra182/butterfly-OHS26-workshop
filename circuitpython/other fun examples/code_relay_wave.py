"""Relay rainbow animation via IR.

A butterfly occasionally ignites a rainbow that rotates around its 26
NeoPixels, then re-broadcasts the wave over IR. Each neighbor that
hears it plays the same animation, decrements the time-to-live, and
passes it on — so the rainbow ripples through the swarm until TTL=0.
A short list of recent wave IDs suppresses echoes so the same pulse
doesn't bounce around forever. The wave's "hue offset" byte rotates
the rainbow's starting color so different waves are visually distinct.
"""
import board
import neopixel
import pulseio
import adafruit_irremote
import time
import random

NUM_PIXELS = 26

# --- NeoPixel setup ---
pixels = neopixel.NeoPixel(board.GP2, NUM_PIXELS, brightness=0.3, auto_write=False)

# --- IR (Qwiic): receiver on GP0, transmitter on GP1 ---
pulsein = pulseio.PulseIn(board.GP0, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()
pulseout = pulseio.PulseOut(board.GP1, frequency=38000, duty_cycle=2**15)
encoder = adafruit_irremote.GenericTransmit(
    header=[9000, 4500], one=[560, 1690], zero=[560, 560], trail=0
)

# Tag byte (+ inverse) identifies a wave message vs. other IR traffic
WAVE_TAG = 0xA5

# Tunables
INITIAL_TTL = 6              # hops before the wave dies out
SPONTANEOUS_CHANCE = 0.002   # per ~20ms tick — ~1 ignition every 10s per butterfly
RAINBOW_ROTATIONS = 2        # full rotations of the rainbow per ignition
RAINBOW_STEP = 0.04          # seconds between rotation frames
RECENT_WAVES_MAX = 8         # how many past wave IDs to remember
IDLE_COLOR = (4, 2, 8)       # faint resting glow

# Rolling list of wave IDs we've already played, to suppress echoes
recent_waves = []


def wheel(pos):
    """Map 0..255 to a saturated RGB triple along the color wheel."""
    pos &= 255
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)


def remember(wave_id):
    recent_waves.append(wave_id)
    if len(recent_waves) > RECENT_WAVES_MAX:
        recent_waves.pop(0)


def broadcast(wave_id, ttl, hue_offset):
    encoder.transmit(
        pulseout,
        [WAVE_TAG, ~WAVE_TAG & 0xFF, wave_id, ttl, hue_offset],
    )
    # Drop the echo of our own transmission so we don't trigger ourselves
    pulsein.clear()


def play_rainbow(hue_offset):
    """Rotate a full rainbow around the ring for RAINBOW_ROTATIONS turns."""
    total_steps = NUM_PIXELS * RAINBOW_ROTATIONS
    for step in range(total_steps):
        for i in range(NUM_PIXELS):
            pos = (i + step) * 256 // NUM_PIXELS + hue_offset
            pixels[i] = wheel(pos)
        pixels.show()
        time.sleep(RAINBOW_STEP)
    pixels.fill(IDLE_COLOR)
    pixels.show()


def ignite(wave_id, ttl, hue_offset):
    """Pass the wave on (if it still has hops) then play it locally."""
    remember(wave_id)
    # Re-broadcast first so neighbors start their animation roughly in parallel
    if ttl > 0:
        broadcast(wave_id, ttl - 1, hue_offset)
    play_rainbow(hue_offset)


pixels.fill(IDLE_COLOR)
pixels.show()
print(f"Relay rainbow — TTL={INITIAL_TTL}, ignition chance={SPONTANEOUS_CHANCE}/tick")

while True:
    pulses = decoder.read_pulses(pulsein, max_pulse=10000, blocking=False)
    if pulses:
        try:
            code = decoder.decode_bits(pulses)
            if (
                len(code) == 5
                and code[0] == WAVE_TAG
                and code[1] == (~WAVE_TAG & 0xFF)
            ):
                wave_id, ttl, hue_offset = code[2], code[3], code[4]
                if wave_id not in recent_waves:
                    print(f"Wave 0x{wave_id:02X} received (ttl={ttl}, offset={hue_offset})")
                    ignite(wave_id, ttl, hue_offset)
        except adafruit_irremote.IRNECRepeatException:
            pass
        except adafruit_irremote.IRDecodeException:
            pass

    if random.random() < SPONTANEOUS_CHANCE:
        wave_id = random.randint(1, 255)
        hue_offset = random.randint(0, 255)
        print(f"Igniting wave 0x{wave_id:02X} (offset={hue_offset})")
        ignite(wave_id, INITIAL_TTL, hue_offset)

    time.sleep(0.02)
