import board
import neopixel
import time
import math

# Set up the NeoPixel strip
# Using GPIO2 for NeoPixel control
pixel_pin = board.GP2
num_pixels = 26

# Create NeoPixel object with initial brightness
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.01, auto_write=False)

# Define purple color (Red, Green, Blue values)
purple = (128, 0, 128)  # Purple color

# Set all pixels to purple color
for i in range(num_pixels):
    pixels[i] = purple

print("Starting fade animation between 1% and 30% brightness...")

# Fade animation loop
while True:
    # Fade in from 1% to 30%
    for brightness in range(1, 31):
        pixels.brightness = brightness / 100.0  # Convert to decimal
        pixels.show()
        time.sleep(0.05)  # Small delay for smooth animation
    
    # Fade out from 30% to 1%
    for brightness in range(30, 0, -1):
        pixels.brightness = brightness / 100.0  # Convert to decimal
        pixels.show()
        time.sleep(0.05)  # Small delay for smooth animation
