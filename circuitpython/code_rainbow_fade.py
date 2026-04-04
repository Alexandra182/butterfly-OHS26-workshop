import board
import neopixel
import time
import math

# Set up the NeoPixel strip
# Using GPIO2 for NeoPixel control
pixel_pin = board.GP2
num_pixels = 26

# Create NeoPixel object with variable brightness
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, auto_write=False)

print("Starting rainbow rotation with fading animation...")

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

# Rainbow rotation with fading animation
rotation_step = 0
fade_step = 0
max_brightness = 0.3  # 30% maximum brightness
min_brightness = 0.05  # 5% minimum brightness

while True:
    # Calculate current brightness using sine wave for smooth fading
    brightness_range = max_brightness - min_brightness
    current_brightness = min_brightness + (brightness_range * (math.sin(fade_step * 0.1) + 1) / 2)
    
    for i in range(num_pixels):
        # Calculate rainbow color for each LED with rotation
        color_position = ((i + rotation_step) * 256 // num_pixels) & 255
        base_color = wheel(color_position)
        
        # Apply fading by scaling the color values
        faded_color = (
            int(base_color[0] * current_brightness),
            int(base_color[1] * current_brightness),
            int(base_color[2] * current_brightness)
        )
        pixels[i] = faded_color
    
    pixels.show()
    time.sleep(0.05)  # Control animation speed
    
    # Update animation counters
    rotation_step = (rotation_step + 1) % num_pixels
    fade_step += 1
