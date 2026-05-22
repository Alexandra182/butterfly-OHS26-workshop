"""Wing flap with body-to-tip color gradient.

Same flap motion as code_wing_flap.py, but each LED's color is fixed
by its distance from the body: light lavender near the body, fading
to deep purple at the wingtip. The bright band still sweeps outward
and back, revealing the gradient as it moves.
"""
import board
import neopixel
import time

NUM_PIXELS = 26
WING_SIZE = 13
TIP_DISTANCE = WING_SIZE // 2  # 6 LEDs from body to wingtip

pixels = neopixel.NeoPixel(board.GP2, NUM_PIXELS, brightness=0.15, auto_write=False)

# Tunables
INNER_COLOR = (140, 60, 220)    # soft purple near the body
OUTER_COLOR = (25, 0, 50)       # deep purple at the wingtip
BAND = 1.8                      # half-width of the bright band, in LED units
STEP = 0.05                     # seconds per frame
FRAMES_PER_HALF = 14            # frames to travel body -> tip (or tip -> body)


def wing_distance(i):
    j = i if i < WING_SIZE else i - WING_SIZE
    return min(j, WING_SIZE - 1 - j)


def color_for(distance):
    """Linear blend from INNER_COLOR (dist 0) to OUTER_COLOR (TIP_DISTANCE)."""
    t = distance / TIP_DISTANCE
    return (
        int(INNER_COLOR[0] * (1 - t) + OUTER_COLOR[0] * t),
        int(INNER_COLOR[1] * (1 - t) + OUTER_COLOR[1] * t),
        int(INNER_COLOR[2] * (1 - t) + OUTER_COLOR[2] * t),
    )


def render(front):
    for i in range(NUM_PIXELS):
        d_body = wing_distance(i)
        d_front = abs(d_body - front)
        level = max(0.0, 1.0 - d_front / BAND)
        r, g, b = color_for(d_body)
        pixels[i] = (int(r * level), int(g * level), int(b * level))
    pixels.show()


print("Wing flap (gradient) — light at body, deep purple at wingtip")
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
