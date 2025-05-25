import chess
import chess.engine
import os
import time
from manage_move import manage_move
from read_board import read_board

# Pfad zur Stockfish-Engine ggf. anpassen
ENGINE_PATH = "/usr/games/stockfish"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)

    print("Spiel gestartet. Du spielst Weiß")
    print("\nAktuelles Brett:")
    print(board)
    while not board.is_game_over():

        # Spielerzug
        while True:
            start, target = read_board()
            try:
                move = chess.Move(start, target)
                if move in board.legal_moves:
                    board.push(move)
                    clear_screen()
                    print("----")
                    print(f"Mensch spielt: {move}")
                    print("\nAktuelles Brett:")
                    print(board)
                    break
                else:
                    clear_screen()
                    print("----")
                    print("Ungültiger Zug. Versuch es nochmal.")
                    print("\nAktuelles Brett:")
                    print(board)
                    print("Mensch ist am Zug!")

            except:
                print("Ungültige Eingabe. Beispiel: e2e4")

        if board.is_game_over():
            break

        # Engine-Zug
        result = engine.play(board, chess.engine.Limit(time=0.5))
        captured_piece = board.piece_at(result.move.to_square)
        board.push(result.move)
        clear_screen()
        print("----")
        print(f"Roboter spielt: {result.move}")
        print("\nAktuelles Brett:")
        print(board)

        input("Robotermove bestätigen")
        manage_move(result.move, captured_piece)
        # !! An dieser Stelle eine Funktion aufrufen um den Roboter 
        # den Move "result.move" (String) machen zu lassen. Funktion wird verlassen, 
        # wenn der Roboter fertig ist.

        print("Mensch ist am Zug!")


    print("\nSpiel beendet:", board.result())
    print(board)
    engine.quit()

if __name__ == "__main__":
    main()
