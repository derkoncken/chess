import serial
import time

# Pfad und Baudrate an dein Brett anpassen
PORT = '/dev/ttyACM0'
BAUDRATE = 19200
POLL_COMMAND = bytes([0x42])  # DGT_SEND_BRD

def poll_dgt_board():
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
            ser.write(POLL_COMMAND)
            time.sleep(0.1)  # kurze Pause, damit Brett antworten kann
            data = ser.read(100)  # Lese Antwort
            if data and data[0] == 0x86 and len(data) >= 67:
                piece_data = data[3:67]  # Bytes 3–66 = Brettfelder
                print("Brett erfolgreich gepollt.")
                return piece_data  # Liste von 64 Figurencodes
            else:
                print("Ungültige oder keine Antwort vom DGT-Brett.")
                return None
    except serial.SerialException as e:
        print("Fehler beim Zugriff auf das DGT-Board:", e)
        return None

def correct_dgt_output(array):
    array.reverse()
    result = []
    for i in range(0, 64, 8):
        row = array[i:i+8]
        result.extend(row[::-1])  # Zeile umdrehen und anhängen
    return result

def detect_move(bytes1, bytes2):
    bytes1 = list(bytes1)
    bytes2 = list(bytes2)
    bytes1 = correct_dgt_output(bytes1)
    bytes2 = correct_dgt_output(bytes2)
    """Vergleicht zwei Bytestrings und gibt die Indizes mit Unterschieden zurück."""
    laenge = min(len(bytes1), len(bytes2))
    unterschiede = []

    for i in range(laenge):
        if bytes1[i] != bytes2[i]:
            #unterschiede.append((i, bytes1[i], bytes2[i]))
            unterschiede.append(i)
    
    if unterschiede == [0, 2, 3, 4]:
        return [4,2]
    if unterschiede == [4, 5, 6, 7]:
        return [4,6]
    if unterschiede == [56, 58, 59, 60]:
        return [60,58]
    if unterschiede == [60, 61, 62, 63]:
        return [60,62]

    if len(unterschiede) == 2:
        start, target = unterschiede
        if bytes1[start] == 0:
            start, target = target, start
        return start, target

    # Hinweis, wenn die Längen unterschiedlich sind
    if len(bytes1) != len(bytes2):
        print(f"Achtung: Unterschiedliche Länge ({len(bytes1)} vs {len(bytes2)})")

    print(unterschiede)
    return unterschiede[0], unterschiede[1]


def read_board():

    pattern_before = poll_dgt_board()
    input("Drücke Enter um Zug zu bestätigen ... ")
    pattern_after = poll_dgt_board()

    start, target = detect_move(pattern_before, pattern_after)

    return start, target
