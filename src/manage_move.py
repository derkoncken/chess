import chess
import socket

# Globale Variable für die Position der gefangenen Figuren
global pos_captured_pieces
pos_captured_pieces = 64

def manage_move(move, captured_piece, pos_captured_pieces):
    """
    Verarbeitet einen Schachzug, einschließlich Rochaden und Schlagen von Figuren.
    Ruft move_piece auf, um die Bewegung an den Roboter zu senden.
    """
    # Vier Sonderfälle | Rochaden
    if move.uci() == "e1g1":  # Weiß kurze Rochade
        move_piece(chess.E1, chess.G1,0)  # König e1 → g1
        move_piece(chess.H1, chess.F1,1)  # Turm h1 → f1

    elif move.uci() == "e1c1":  # Weiß lange Rochade
        move_piece(chess.E1, chess.C1,0)  # König e1 → c1
        move_piece(chess.A1, chess.D1,1)  # Turm a1 → d1

    elif move.uci() == "e8g8":  # Schwarz kurze Rochade
        move_piece(chess.E8, chess.G8,0)  # König e8 → g8
        move_piece(chess.H8, chess.F8,1)  # Turm h8 → f8

    elif move.uci() == "e8c8":  # Schwarz lange Rochade
        move_piece(chess.E8, chess.C8,0)  # König e8 → c8
        move_piece(chess.A8, chess.D8,1)  # Turm a8 → d8
    
    # Wenn eine Figur abgeworfen wird, muss diese erst weggestellt werden
    elif captured_piece:
        move_piece(move.to_square, pos_captured_pieces,0)  # Geschlagene Figur entfernen
        pos_captured_pieces += 1    # Auf nächste freie Stelle stellen
        move_piece(move.from_square, move.to_square,1)     # Ziehende Figur bewegen
        return pos_captured_pieces
    else:
        move_piece(move.from_square, move.to_square,1)     # Normale Bewegung
    return pos_captured_pieces

def move_piece(start, target, home):
    """
    Sendet einen Bewegungsbefehl an den Roboter über eine TCP-Verbindung.
    start: Startfeld (0-63)
    target: Zielfeld (0-63 oder Position für geschlagene Figuren)
    home: 0 = Figur wird entfernt, 1 = Figur wird bewegt
    """
    print(start, target)
    # Umrechnung von Feldnummer in x/y-Koordinaten
    start_y = start // 8
    start_x = start % 8
    target_y = target // 8
    target_x = target % 8

    HOST = "192.168.131.39"
    PORT = 30000

    # Server-Socket einrichten
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server läuft auf {HOST}:{PORT}, wartet auf Verbindung...")

    # Auf Verbindung vom Client (Roboter) warten
    client_socket, client_address = server_socket.accept()
    print(f"Verbindung von {client_address} angenommen.")

    # Auf "send" vom Client warten
    data = client_socket.recv(1024).decode().strip()
    print(f"Empfangen: {data}")

    if data == "send":
        # Bewegungsdaten an den Client senden
        msg = f'({start_x},{start_y},{target_x},{target_y},{home})\n'
        client_socket.sendall(msg.encode())
        print(f"Gesendet: {msg.strip()}")

        # Auf "done" vom Client warten
        while True:
            done_msg = client_socket.recv(1024).decode().strip()
            print(f"Antwort vom Client: {done_msg}")
            if done_msg.lower() == "done":
                print("Roboter hat den Zug abgeschlossen.")
                break

    # Verbindung schließen
    client_socket.close()
    server_socket.close()
