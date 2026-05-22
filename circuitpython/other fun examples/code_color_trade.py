"""Color trading via IR.

Each butterfly starts with a random vibrant color (its "personality").
Every BROADCAST_INTERVAL it broadcasts its current RGB over IR.
On receiving another butterfly's color, it blends its own toward that
color by BLEND_RATE. Over time the room drifts toward a shared tint.
A brief brightness boost marks each successful trade.
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

# Tag byte (+ inverse) identifies a color-trade message vs. other IR noise
TRADE_TAG = 0xC0

# Tunables
BROADCAST_INTERVAL = 2.0   # seconds between sending our color
BLEND_RATE = 0.30          # how far to move toward a received color (0..1)
FLASH_BOOST = 1.7          # brightness multiplier during a trade flash
FLASH_DURATION = 0.35      # seconds the trade flash lasts


def random_vibrant():
    """Pick a saturated random color so nobody starts muddy."""
    pos = random.randint(0, 255)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)


def blend(c1, c2, rate):
    return (
        int(c1[0] * (1 - rate) + c2[0] * rate),
        int(c1[1] * (1 - rate) + c2[1] * rate),
        int(c1[2] * (1 - rate) + c2[2] * rate),
    )


def render(color, boost=1.0):
    r = min(255, int(color[0] * boost))
    g = min(255, int(color[1] * boost))
    b = min(255, int(color[2] * boost))
    pixels.fill((r, g, b))
    pixels.show()


def broadcast(color):
    encoder.transmit(
        pulseout,
        [TRADE_TAG, ~TRADE_TAG & 0xFF, color[0], color[1], color[2]],
    )
    # Drop the echo of our own transmission so we don't trade with ourselves
    pulsein.clear()


my_color = random_vibrant()
# Stagger the first broadcast so the room doesn't sync-pulse
last_send = time.monotonic() - random.random() * BROADCAST_INTERVAL
flash_until = 0.0

print(f"Color trading — starting color: {my_color}")

while True:
    now = time.monotonic()

    if now - last_send >= BROADCAST_INTERVAL:
        broadcast(my_color)
        last_send = now

    pulses = decoder.read_pulses(pulsein, max_pulse=10000, blocking=False)
    if pulses:
        try:
            code = decoder.decode_bits(pulses)
            if (
                len(code) == 5
                and code[0] == TRADE_TAG
                and code[1] == (~TRADE_TAG & 0xFF)
            ):
                other = (code[2], code[3], code[4])
                my_color = blend(my_color, other, BLEND_RATE)
                flash_until = now + FLASH_DURATION
                print(f"Trade: {other} -> me {my_color}")
        except adafruit_irremote.IRNECRepeatException:
            pass
        except adafruit_irremote.IRDecodeException:
            pass

    boost = FLASH_BOOST if now < flash_until else 1.0
    render(my_color, boost)
    time.sleep(0.02)
