import board
import neopixel
import time
import math

# Set up the NeoPixel strip
# Using GPIO2 for NeoPixel control
pixel_pin = board.GP2
num_pixels = 26

# Create NeoPixel object at 30% brightness
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

print("Starting rainbow cycling animation at 30% intensity...")

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

# Rainbow cycling animation
rainbow_offset = 0
while True:
    for i in range(num_pixels):
        # Calculate rainbow color for each LED
        color_position = (i * 256 // num_pixels + rainbow_offset) & 255
        pixels[i] = wheel(color_position)
    
    pixels.show()
    time.sleep(0.05)  # Control cycling speed
    
    # Move the rainbow pattern
    rainbow_offset = (rainbow_offset + 1) % 256
