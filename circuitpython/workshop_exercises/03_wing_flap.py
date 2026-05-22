"""Exercise 03 - Wing flap (mapping code to physical shape)

So far we've treated the 26 pixels as a straight line. But on the board
they aren't! Each wing is a LOOP: both ends of its range sit next to the
body, and the middle pixel is the wingtip.

  Wing 1: pixels 0..12   -> 0 and 12 are at the body, 6 is the tip
  Wing 2: pixels 13..25  -> 13 and 25 are at the body, 19 is the tip

So if we just lit pixels 0, 1, 2, 3... in order, the light would NOT
travel in a straight line out the wing. To make a real "flap" that sweeps
from the body to the tip, we light pixels by their DISTANCE from the body.

Run it as-is first, then try the CHALLENGES at the bottom.
"""
import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.GP2, 26, brightness=0.3, auto_write=False)

ORANGE = (255, 90, 0)
PURPLE = (255,0, 255)
OFF = (0, 0, 0)

def scaled(color, level):
      r, g, b = color
      return (int(r * level), int(g * level), int(b * level))

def body_distance(i):
    """How far pixel i is from the body, 0 (at body) to 6 (wingtip)."""
    j = i if i < 13 else i - 13   # position within its own wing (0..12)
    return min(j, 12 - j)          # both ends of the loop are near the body


# Print the mapping once at startup so you can SEE that index order is not
# the same as physical position. Open the serial console (Mu, 115200 baud).
print("pixel index -> distance from body:")
for i in range(26):
    wing = 1 if i < 13 else 2
    print(f"  pixel {i:2d}  (wing {wing})  distance {body_distance(i)}")
print()


def light_ring(d):
    """Light every pixel that sits teps from the body, and report it."""
    # level = d / 6                       # 0.0 at body, 1.0 at the tips
    # a = scaled(ORANGE, 1 - level)
    # b = scaled(PURPLE, level)
    # color = (a[0] + b[0], a[1] + b[1], a[2] + b[2])
    
    pixels.fill(OFF)
    lit = []
    for i in range(26):
        if body_distance(i) == d:
            pixels[i] = ORANGE # color
            lit.append(i)
    pixels.show()
    print(f"distance {d}: lit pixels {lit}")


# --- Flap: sweep light out from the body to the tips, then back ---------------
while True:
    # pixels.fill(OFF)
    print("--- flapping out ---")
    for d in range(7):           # outward: body (0) to tips (6)
        light_ring(d)
        time.sleep(0.06)

    print("--- flapping in ---")
    for d in range(5, -1, -1):   # inward: tips back to body
        light_ring(d)
        time.sleep(0.06)

# ---------------------------------------------------------------------------
# CHALLENGES — edit the code above and re-save to try these:
#
# 1. Leave a trail: remove the pixels.fill(OFF) so the wing fills up from
#    the body outward instead of showing one ring at a time.
#
# 2. Color by distance: instead of always ORANGE, make the body end one
#    color and the tips another. Use the scaled() blend trick from ex. 02
#    with level = d / 6
#
# 3. Flap only ONE wing. Hint: in body_distance, the test `i < 13` tells
#    you which wing pixel i belongs to.
#
# 4. Speed up the flap as it goes, make time.sleep() shorter for higher d.
# ---------------------------------------------------------------------------
