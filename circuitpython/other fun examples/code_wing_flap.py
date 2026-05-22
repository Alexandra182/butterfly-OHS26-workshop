"""Wing flap animation.

Each wing is a loop around the wing edge. For wing 1 (LEDs 1-13),
LEDs 1 and 13 sit closest to the body and LED 7 is the wingtip; wing 2
(LEDs 14-26) mirrors this — LEDs 14 and 26 at the body, LED 20 at the
tip. A soft band of light sweeps from the body outward to the wingtip
and back on both wings in unison.
"""
import board
import neopixel
import time

NUM_PIXELS = 26
WING_SIZE = 13
TIP_DISTANCE = WING_SIZE // 2  # 6 LEDs from body to wingtip

pixels = neopixel.NeoPixel(board.GP2, NUM_PIXELS, brightness=0.3, auto_write=False)

# Tunables
COLOR = (180, 60, 200)     # wing color
BAND = 1.8                 # half-width of the bright band, in LED units
STEP = 0.05                # seconds per frame
FRAMES_PER_HALF = 14       # frames to travel body -> tip (or tip -> body)


def wing_distance(i):
    """Distance (in LEDs) from the body for pixel index i."""
    j = i if i < WING_SIZE else i - WING_SIZE
    return min(j, WING_SIZE - 1 - j)


def render(front):
    """Light each LED based on how close it is to the wavefront `front`."""
    for i in range(NUM_PIXELS):
        d = abs(wing_distance(i) - front)
        level = max(0.0, 1.0 - d / BAND)
        pixels[i] = (
            int(COLOR[0] * level),
            int(COLOR[1] * level),
            int(COLOR[2] * level),
        )
    pixels.show()


print("Wing flap — body to wingtip and back")
while True:
    # Open: body -> wingtip
    for frame in range(FRAMES_PER_HALF):
        front = frame * TIP_DISTANCE / (FRAMES_PER_HALF - 1)
        render(front)
        time.sleep(STEP)
    # Close: wingtip -> body
    for frame in range(FRAMES_PER_HALF):
        front = TIP_DISTANCE - frame * TIP_DISTANCE / (FRAMES_PER_HALF - 1)
        render(front)
        time.sleep(STEP)
