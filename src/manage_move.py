import chess
import socket

pos_captured_pieces = 64

def manage_move(move, captured_piece):

    # Vier Sonderfälle | Rochaden
    if move.uci() == "e1g1":  # Weiß kurze Rochade
        move_piece(chess.E1, chess.G1)  # König e1 → g1
        move_piece(chess.H1, chess.F1)  # Turm h1 → f1

    elif move.uci() == "e1c1":  # Weiß lange Rochade
        move_piece(chess.E1, chess.C1)  # König e1 → c1
        move_piece(chess.A1, chess.D1)  # Turm a1 → d1

    elif move.uci() == "e8g8":  # Schwarz kurze Rochade
        move_piece(chess.E8, chess.G8)  # König e8 → g8
        move_piece(chess.H8, chess.F8)  # Turm h8 → f8

    elif move.uci() == "e8c8":  # Schwarz lange Rochade
        move_piece(chess.E8, chess.C8)  # König e8 → c8
        move_piece(chess.A8, chess.D8)  # Turm a8 → d8
    
    # Wenn eine Figur abgeworfen wird, muss diese erst weggestellt werden
    elif captured_piece:
        move_piece(move.to_square, pos_captured_pieces)
        pos_captured_pieces += 1    # Auf nächste freie Stelle stellen
        move_piece(move.from_square, move.to_square)
        return
    else:
        move_piece(move.from_square, move.to_square)


def move_piece(start, target):
    start_x = start // 8
    start_y = start % 8
    target_x = target // 8
    target_y = target % 8

    HOST = "192.168.131.39"
    PORT = 30000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server läuft auf {HOST}:{PORT}, wartet auf Verbindung...")

    client_socket, client_address = server_socket.accept()
    print(f"Verbindung von {client_address} angenommen.")

    data = client_socket.recv(1024).decode().strip()
    print(f"Empfangen: {data}")

    if data == "send":
        msg = f'({start_x},{start_y},{target_x},{target_y})\n'
        client_socket.sendall(msg.encode())
        print(f"Gesendet: {msg.strip()}")

        # Auf "done" vom Client warten
        while True:
            done_msg = client_socket.recv(1024).decode().strip()
            print(f"Antwort vom Client: {done_msg}")
            if done_msg.lower() == "done":
                print("Roboter hat den Zug abgeschlossen.")
                break

    client_socket.close()
    server_socket.close()
