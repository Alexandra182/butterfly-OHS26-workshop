import board
import neopixel
import pulseio
import adafruit_irremote
import time

# --- NeoPixel setup ---
pixels = neopixel.NeoPixel(board.GP2, 26, brightness=0.3, auto_write=False)

# --- IR receiver on GP0 (Qwiic connector) ---
pulsein = pulseio.PulseIn(board.GP0, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

# Must match the sender
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

def show_rainbow():
    """Play a short rainbow animation."""
    for step in range(80):
        for i in range(26):
            pixels[i] = wheel((i * 256 // 26 + step * 4) & 255)
        pixels.show()
        time.sleep(0.05)
    pixels.fill((0, 0, 0))
    pixels.show()

# Start with LEDs off
pixels.fill((0, 0, 0))
pixels.show()

print("Listening for IR pattern signal...")

while True:
    pulses = decoder.read_pulses(pulsein, max_pulse=10000, blocking=False)
    if pulses:
        try:
            code = decoder.decode_bits(pulses)
            print(f"Received {len(code)} bytes: {[hex(b) for b in code]}")
            if len(code) == 4 and code[0] == ADDRESS and code[2] == COMMAND:
                print("Pattern matched — lighting up!")
                show_rainbow()
            else:
                print(f"No match (expected address=0x{ADDRESS:02X} command=0x{COMMAND:02X})")
        except adafruit_irremote.IRNECRepeatException:
            print("Repeat signal received")
        except adafruit_irremote.IRDecodeException as e:
            print(f"Decode error: {e}")
