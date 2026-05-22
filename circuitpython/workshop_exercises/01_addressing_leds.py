"""Exercise 01 - Addressing LEDs individually

Our board has 26 NeoPixels that can be addressed individually.
Each pixel is set with pixels[index] = (red, green, blue), where each
value is 0-255. 
Nothing actually changes on the board until you call
pixels.show().

Run it as-is first, then try the CHALLENGES at the bottom.
"""
import board
import neopixel
import time

# 26 NeoPixels on GP2. auto_write=False means changes are buffered until
# we explicitly call pixels.show() — faster, and lets us set many at once.
pixels = neopixel.NeoPixel(board.GP2, 26, brightness=0.3, auto_write=False)

# A few colors to play with (Red, Green, Blue), each 0-255
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
OFF = (0, 0, 0)

# Start with every pixel off.
pixels.fill(OFF)
pixels.show()

# Light a SINGLE pixel. Indices go from 0 to 25 (not 1 to 26!).
pixels[0] = RED      # the very first LED
pixels.show()
time.sleep(1)

# Light a few specific pixels in different colors.
pixels[6] = GREEN    # index 6 = wingtip of wing 1
pixels[19] = BLUE    # index 19 = wingtip of wing 2
pixels.show()
time.sleep(1)

# Walk one lit pixel along the whole strip, one at a time.
for i in range(26):
    pixels.fill(OFF)     # clear the previous pixel
    pixels[i] = RED      # light only the current one
    pixels.show()
    print(f"Lit pixel {i}")
    time.sleep(0.1)

pixels.fill(OFF)
pixels.show()

# ---------------------------------------------------------------------------
# CHALLENGES — edit the code above and re-save to try these:
#
# 1. Change the (R, G, B) numbers to mix your own favourite color .
#
# 2. Make the walking pixel leave a trail: don't clear with fill(OFF),
#    instead let each pixel stay lit so the strip fills up.
#
# 3. Light only the two pixels closest to the body on each wing
#    (indices 0, 12, 13, 25) in your favorite color.
# ---------------------------------------------------------------------------
