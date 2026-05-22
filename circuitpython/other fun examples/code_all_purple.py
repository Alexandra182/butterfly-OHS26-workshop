"""All purple.

Lights every LED on both wings a steady purple. The simplest possible
program — set the color once and leave it on.
"""
import board
import neopixel

NUM_PIXELS = 26

pixels = neopixel.NeoPixel(board.GP2, NUM_PIXELS, brightness=0.3, auto_write=False)

PURPLE = (160, 0, 200)

pixels.fill(PURPLE)
pixels.show()

print("All LEDs purple")
