"""Exercise 05 - Catch your neighbors' colors (the capstone)

This exercise puts exercises 03 and 04 together:
  - From ex. 03: arrange colors by DISTANCE from the body (body_distance).
  - From ex. 04: SEND and RECEIVE messages over IR between boards.

Every butterfly has an ID (1-10), and each ID owns a fixed color. A butterfly
broadcasts its ID over IR. When another butterfly hears it, it "catches" that
color and shows it on its wings.

Every catch SHIFTS the wing: the newest color enters right above the body
and pushes every older color one ring out toward the wingtip. Your own color
stays pinned at the body. Six caught colors fit per wing; catch another and
the oldest slides off the tip. The same color can be caught over and over, so
a chatty neighbor will fill your wing with its color.

Same code on every board — just give each one a different MY_ID.
Plug the IR transceiver into the Qwiic connector with the Qwiic cable first.

Run it as-is first, then try the CHALLENGES at the bottom.
"""
import board
import neopixel
import pulseio
import adafruit_irremote
import time

# --- NeoPixel setup ---
pixels = neopixel.NeoPixel(board.GP2, 26, brightness=0.3, auto_write=False)
OFF = (0, 0, 0)

# --- IR setup (Qwiic): receiver on GP0, transmitter on GP1 ---
pulsein = pulseio.PulseIn(board.GP0, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()
pulseout = pulseio.PulseOut(board.GP1, frequency=38000, duty_cycle=2**15)
encoder = adafruit_irremote.GenericTransmit(
    header=[9000, 4500], one=[560, 1690], zero=[560, 560], trail=0
)

# Each ID owns one color. Give every board a different MY_ID from this set.
ID_COLORS = {
    1: (255, 0, 0),      # red
    2: (255, 110, 0),    # orange
    3: (230, 230, 0),    # yellow
    4: (0, 255, 0),      # green
    5: (0, 200, 255),    # cyan
    6: (40, 0, 255),     # blue
    7: (180, 0, 255),    # purple
    8: (255, 0, 140),    # pink
    9: (0, 255, 150),    # teal
    10: (255, 255, 255), # white
}

MY_ID = 8                # <-- change this on each board!
MY_COLOR = ID_COLORS[MY_ID]

SEND_EVERY = 1.5         # seconds between broadcasts of our own ID
MAX_CAUGHT = 6           # caught colors visible per wing (rings 1..6 above body)

# Caught colors, newest first. A new catch goes in at the front (ring 1, next
# to the body) and pushes the rest out toward the tip. Our own color is the
# pinned base and is not stored here.
stack = []


def body_distance(i):
    """How far pixel i is from the body, 0 (at body) to 6 (wingtip). From ex. 03."""
    j = i if i < 13 else i - 13
    return min(j, 12 - j)


def id_of(color):
    """Which ID owns this color (just for readable serial output)."""
    for cid, c in ID_COLORS.items():
        if c == color:
            return cid
    return "?"


def render():
    """Body ring = MY_COLOR; each ring outward shows the next caught color."""
    pixels.fill(OFF)
    for i in range(26):
        d = body_distance(i)
        if d == 0:
            pixels[i] = MY_COLOR          # base of the stack = our own identity
        elif d - 1 < len(stack):
            pixels[i] = stack[d - 1]      # ring 1 -> stack[0], ring 2 -> stack[1] ...
    pixels.show()


def catch(sender_id):
    """Insert a neighbor's color at the body; everything shifts out toward the tip."""
    stack.insert(0, ID_COLORS[sender_id])  # newest enters next to the body (ring 1)
    if len(stack) > MAX_CAUGHT:
        stack.pop()                        # oldest slides off the wingtip
    print(f"Caught #{sender_id}. Stack now: {[id_of(c) for c in stack]}")


print(f"Butterfly #{MY_ID} ({MY_COLOR}) ready. Broadcasting and catching colors.")
render()
last_send = time.monotonic()

while True:
    now = time.monotonic()

    # --- Broadcast our own ID (like ex. 04) ---
    if now - last_send >= SEND_EVERY:
        encoder.transmit(pulseout, [MY_ID, ~MY_ID & 0xFF, MY_ID, ~MY_ID & 0xFF])
        last_send = now
        pulsein.clear()                   # ignore the echo of our own transmission

    # --- Listen for neighbors (like ex. 04) ---
    pulses = decoder.read_pulses(pulsein, max_pulse=10000, blocking=False)
    if pulses:
        try:
            code = decoder.decode_bits(pulses)
            sender = code[0]
            if len(code) == 4 and sender in ID_COLORS and sender != MY_ID:
                catch(sender)
                render()
        except adafruit_irremote.IRNECRepeatException:
            pass
        except adafruit_irremote.IRDecodeException:
            pass

# ---------------------------------------------------------------------------
# CHALLENGES — edit the code above and re-save to try these:
#
# 1. Give your board a different MY_ID and a partner a different one too.
#    Watch each other's color climb your wings.
#
# 2. Reverse the flow: make new colors enter at the WINGTIP and slide back
#    toward the body instead of outward. (Append instead of insert(0), and
#    pop(0) instead of pop().)
#
# 3. Flash the whole butterfly briefly in the caught color before adding it
#    to the stack, so a catch is easy to spot. (Reuse the green-flash idea
#    from ex. 04.)
#
# 4. Forget over time: if no new color is caught for 10 seconds, pop one
#    color off the stack so old encounters slowly fade away.
# ---------------------------------------------------------------------------
