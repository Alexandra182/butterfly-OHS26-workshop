"""Exercise 02 - Loops and brightness

The goal of this exercise is to use loops to gradually change a color over time, 
not just set it once.
A NeoPixel's brightness comes from how big its (R, G, B) numbers are:
(255, 0, 0) is bright red, (20, 0, 0) is dim red, (0, 0, 0) is off.
By looping a number up and down and multiplying the color by it, we
get a smooth fade, the building block of every animation.

Run it as-is first, then try the CHALLENGES at the bottom.
"""
import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.GP2, 26, brightness=0.3, auto_write=False)

PURPLE = (160, 0, 255)
CYAN = (0, 200, 255)  

def scaled(color, level):
    """Return color dimmed to `level`, a fraction from 0.0 (off) to 1.0 (full)."""
    r, g, b = color
    return (int(r * level), int(g * level), int(b * level))


# --- Part 1: fade ALL pixels up, then down, forever ---------------------------
# range(0, 101, 5) counts 0, 5, 10 ... 100. Dividing by 100 gives 0.0 .. 1.0.
while True:
    # Fade up
    for step in range(0, 101, 5):
        level = step / 100
        pixels.fill(scaled(PURPLE, level))
        pixels.show()
        time.sleep(0.02)

    # Fade down
    for step in range(100, -1, -5):
        level = step / 100
        pixels.fill(scaled(PURPLE, level))
        pixels.show()
        time.sleep(0.02)

# ---------------------------------------------------------------------------
# CHALLENGES — edit the code above and re-save to try these:
#
# 1. Change the speed of the fade. Which line controls it? (Two ways: the
#    sleep time, and the step size in range.)
#
# 2. Fade a SINGLE pixel instead of all of them. Replace pixels.fill(...)
#    with pixels.fill(OFF) then pixels[6] = scaled(PURPLE, level).
#
# 3. Fade between TWO colors instead of fading to black. Blend like:
#    a = scaled(PURPLE, 1 - level)
#    b = scaled(CYAN, level)
#    pixels.fill((a[0] + b[0], a[1] + b[1], a[2] + b[2]))
# ---------------------------------------------------------------------------
