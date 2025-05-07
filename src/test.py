import serial
import time

PORT = '/dev/ttyACM0'
BAUDRATE = 9600  # Wird laut DGT-Doku verwendet
POLL_COMMAND = bytes([0x42])  # DGT_SEND_BRD

with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
    print(f"Verbunden mit {PORT}")
    ser.write(POLL_COMMAND)
    time.sleep(0.2)  # Warten auf Antwort
    data = ser.read(100)
    if data:
        print("Antwort (Hex):", data.hex())
    else:
        print("Keine Antwort erhalten.")
