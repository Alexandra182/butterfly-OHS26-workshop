"""Exercise 04 - Talk to your neighbor (first IR message)

Until now each butterfly worked alone. Now we add the IR transceiver
(plugged into the Qwiic connector) so two boards can talk.

How IR works here, in plain terms:
  - To SEND, we blink an infrared LED in a precise pattern (a few bytes).
  - To RECEIVE, an IR sensor watches for that pattern and decodes it back
    into the same bytes.
Infrared is invisible to your eyes but a phone camera can often see the
transmit LED flash - try it!

This SAME code goes on BOTH boards. Each butterfly shouts its own ID every
couple of seconds, and flashes green whenever it HEARS another butterfly.
Point two boards at each other and watch them both blink.

Plug the IR transceiver module into the Qwiic connector with the Qwiic
cable before running. No wiring needed - it only fits one way.
"""
import board
import neopixel
import pulseio
import adafruit_irremote
import time

# --- NeoPixel setup ---
pixels = neopixel.NeoPixel(board.GP2, 26, brightness=0.3, auto_write=False)
GREEN = (0, 255, 0)
OFF = (0, 0, 0)

# --- IR setup (Qwiic): receiver on GP0, transmitter on GP1 ---
pulsein = pulseio.PulseIn(board.GP0, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()
# frequency=38000: flicker the IR LED at 38 kHz - the "carrier" the receiver
#   is tuned to, so it ignores sunlight and room lighting.
# duty_cycle=2**15: how much of each flicker the LED is on. It's a 16-bit
#   number where 0 = always off and 65535 = always on, so 2**15 (=32768) is
#   the halfway point = 50% on. 50% is the standard square-wave drive for IR.
pulseout = pulseio.PulseOut(board.GP1, frequency=38000, duty_cycle=2**15)
encoder = adafruit_irremote.GenericTransmit(
    header=[9000, 4500], one=[560, 1690], zero=[560, 560], trail=0
)

# Give your butterfly a number. The code works the same whatever you pick -
# it just helps you tell who's talking in the serial console.
MY_ID = 1

SEND_EVERY = 2.0   # seconds between shouts

pixels.fill(OFF)
pixels.show()
print(f"Butterfly #{MY_ID} ready. Shouting every {SEND_EVERY}s, listening always.")

last_send = time.monotonic()

while True:
    now = time.monotonic()

    # --- SEND: shout our ID every SEND_EVERY seconds ---
    # NEC format wants 4 bytes: [value, ~value, value2, ~value2]. The ~ copies
    # are an error check. We send MY_ID twice with its inverses.
    if now - last_send >= SEND_EVERY:
        encoder.transmit(pulseout, [MY_ID, ~MY_ID & 0xFF, MY_ID, ~MY_ID & 0xFF])
        print(f"Sent: I am #{MY_ID}")
        last_send = now
        pulsein.clear()   # ignore the echo of our own transmission

    # --- RECEIVE: did we hear anyone? ---
    pulses = decoder.read_pulses(pulsein, max_pulse=10000, blocking=False)
    if pulses:
        try:
            code = decoder.decode_bits(pulses)
            sender = code[0]
            print(f"Heard butterfly #{sender}!")
            # Flash green to show we got a message
            pixels.fill(GREEN)
            pixels.show()
            time.sleep(0.15)
            pixels.fill(OFF)
            pixels.show()
        except adafruit_irremote.IRNECRepeatException:
            pass
        except adafruit_irremote.IRDecodeException:
            print("Heard something, but couldn't decode it")

# ---------------------------------------------------------------------------
# CHALLENGES — edit the code above and re-save to try these:
#
# 1. Give each board a different MY_ID, then print only when you hear a
#    SPECIFIC neighbor (e.g. `if sender == 2:`).
#
# 2. Change the flash color depending on WHO you heard. Make a dict like
#    COLORS = {1: RED, 2: GREEN, 3: BLUE} and use COLORS[sender].
#
# 3. Use a wing-flap (exercise 03) as the "message received" animation
#    instead of a plain green flash.
#
# 4. Point a phone camera at the IR transmitter LED while it sends. Can you
#    see it flash? (Many phone front cameras can see infrared.)
# ---------------------------------------------------------------------------
