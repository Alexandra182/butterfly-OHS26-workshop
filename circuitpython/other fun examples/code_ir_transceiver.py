import board
import pulseio
import adafruit_irremote
import time

# IR receiver on GP0, transmitter on GP1 (Qwiic connector)
receiver_pin = board.GP0
transmitter_pin = board.GP1

# --- Receiver setup ---
pulsein = pulseio.PulseIn(receiver_pin, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

# --- Transmitter setup ---
pulseout = pulseio.PulseOut(transmitter_pin, frequency=38000, duty_cycle=2**15)
encoder = adafruit_irremote.GenericTransmit(header=[9000, 4500], one=[560, 1690], zero=[560, 560], trail=0)

# Example NEC command to send: address 0x00, command 0x16 (play/pause on many devices)
SEND_ADDRESS = 0x00
SEND_COMMAND = 0x16

print("IR transceiver ready. Listening for signals...")
print(f"Will also send address=0x{SEND_ADDRESS:02X} command=0x{SEND_COMMAND:02X} every 5 seconds.")

last_send = time.monotonic()

while True:
    # --- Receive ---
    pulses = decoder.read_pulses(pulsein, max_pulse=10000, blocking=False)
    if pulses:
        try:
            code = decoder.decode_bits(pulses)
            print(f"Received {len(code)} bytes: {[hex(b) for b in code]}")
        except adafruit_irremote.IRNECRepeatException:
            print("NEC repeat signal")
        except adafruit_irremote.IRDecodeException as e:
            print(f"Decode error: {e}")

    # --- Transmit every 5 seconds ---
    now = time.monotonic()
    if now - last_send >= 5.0:
        print(f"Sending: address=0x{SEND_ADDRESS:02X} command=0x{SEND_COMMAND:02X}")
        encoder.transmit(pulseout, [SEND_ADDRESS, ~SEND_ADDRESS & 0xFF, SEND_COMMAND, ~SEND_COMMAND & 0xFF])
        last_send = now
