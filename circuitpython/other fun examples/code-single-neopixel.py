import board
import neopixel

# Set up the NeoPixel strip
# Using GPIO2 for NeoPixel control
pixel_pin = board.GP2
num_pixels = 26

# Create NeoPixel object
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

# Define purple color (Red, Green, Blue values)
purple = (128, 0, 128)  # Purple color

# Turn on all 26 pixels with purple color
for i in range(num_pixels):
    pixels[i] = purple

# Update the pixels to show the changes
pixels.show()

print("All 26 NeoPixels are now purple at 30% brightness!")