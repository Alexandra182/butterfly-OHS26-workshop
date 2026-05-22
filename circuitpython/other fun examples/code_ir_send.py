import board
import neopixel
import pulseio
import adafruit_irremote
import time

# --- NeoPixel setup ---
pixels = neopixel.NeoPixel(board.GP2, 26, brightness=0.3, auto_write=False)

# --- IR transmitter on GP1 (Qwiic connector) ---
pulseout = pulseio.PulseOut(board.GP1, frequency=38000, duty_cycle=2**15)
encoder = adafruit_irremote.GenericTransmit(
    header=[9000, 4500], one=[560, 1690], zero=[560, 560], trail=0
)

# Identifier for this butterfly's pattern broadcast
ADDRESS = 0xAB
COMMAND = 0x01  # 0x01 = rainbow pattern

def wheel(pos):
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

print("Broadcasting rainbow pattern via IR every 3 seconds...")

offset = 0
last_send = time.monotonic()

while True:
    # Show rainbow on own LEDs
    for i in range(26):
        pixels[i] = wheel((i * 256 // 26 + offset) & 255)
    pixels.show()
    offset = (offset + 1) % 256

    # Broadcast IR pattern every 3 seconds
    if time.monotonic() - last_send >= 3.0:
        encoder.transmit(pulseout, [ADDRESS, ~ADDRESS & 0xFF, COMMAND, ~COMMAND & 0xFF])
        print("Sent rainbow pattern signal")
        last_send = time.monotonic()

    time.sleep(0.05)
