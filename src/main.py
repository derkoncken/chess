import chess
import chess.engine
import os
import sys
import time
from manage_move import manage_move
from read_board import poll_dgt_board, detect_move
from update_chess_board import update_piece_labels
from gui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from qt_material import apply_stylesheet

# Pfad zur Engine
ENGINE_PATH = "/usr/games/stockfish"

# Globale Variablen
pos_captured_pieces = 64
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)

# GUI Setup
app = QtWidgets.QApplication(sys.argv)
apply_stylesheet(app, theme='light_red.xml')  # andere Themes möglich
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

#test pattern_before = poll_dgt_board()


# ✅ QThread-Klasse für manage_move
class MoveThread(QtCore.QThread):
    finished = QtCore.pyqtSignal(int)

    def __init__(self, move, captured_piece, pos_captured_pieces):
        super().__init__()
        self.move = move
        self.captured_piece = captured_piece
        self.pos_captured_pieces = pos_captured_pieces

    def run(self):
        updated_pos = manage_move(self.move, self.captured_piece, self.pos_captured_pieces)
        self.finished.emit(updated_pos)

def plot_png_on_label(label, png_path):
    pixmap = QPixmap(png_path)  # Pfad zum Bild
    label.setPixmap(pixmap)
    label.setScaledContents(True)  # optional: skaliert das Bild auf Label-Größe

def button_triggered():
    global state, pattern_before, pos_captured_pieces

    """
    try:
        #test pattern_after = poll_dgt_board()
        start, target = 8, 16#detect_move(pattern_before, pattern_after)
        move = chess.Move(start, target)
    except Exception as e:
        ui.label.setText(f"Zugerkennung fehlgeschlagen: {e}")
        return

    if move in board.legal_moves:
        board.push(move)
        ui.label.setText(f"Du spielst: {move}")
        update_piece_labels(board, ui)
    else:
        ui.label.setText("Falscher Zug!")
        return

    if board.is_game_over():
        ui.label.setText("Du hast gewonnen!")
        return
    """
    result = engine.play(board, chess.engine.Limit(time=1))
    captured_piece = board.piece_at(result.move.to_square)
    board.push(result.move)
    ui.label.setText(f"Roboter spielt: {result.move}")
    update_piece_labels(board, ui)
    return
    # ✅ Thread starten
    move_thread = MoveThread(result.move, captured_piece, pos_captured_pieces)
    move_thread.finished.connect(on_move_done)
    move_thread.start()

    # Wichtig: Thread referenzieren, damit er nicht sofort gelöscht wird
    ui._move_thread = move_thread


def on_move_done(new_pos):
    global pos_captured_pieces, pattern_before, state
    pos_captured_pieces = new_pos

    if board.is_game_over():
        ui.label.setText("Roboter hat gewonnen!")
        return
    else:
        ui.label.setText("Bitte ziehen und bestätigen")

    try:
        pattern_before = poll_dgt_board()
    except Exception as e:
        ui.label.setText(f"Zugerkennung fehlgeschlagen: {e}")


def poll_board_before_triggered():
    global pattern_before
    pattern_before = poll_dgt_board()


ui.button.clicked.connect(button_triggered)
ui.poll_board_before.clicked.connect(poll_board_before_triggered)
plot_png_on_label(ui.chess_board, "src/chessboard.png")
plot_png_on_label(ui.logo, "src/logo.png")
update_piece_labels(board, ui)

plot_png_on_label(ui.chess_board, "src/chessboard.png")

# App starten
sys.exit(app.exec_())







"""


# Pfad zur Stockfish-Engine ggf. anpassen
ENGINE_PATH = "/usr/games/stockfish"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    pos_captured_pieces = 64
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)

    print("Spiel gestartet. Du spielst Weiß")
    print("\nAktuelles Brett:")
    print(board)
    while not board.is_game_over():
        # 1. ermittel zug
        # 2. mach zug
        # 1. ermittel zug (bot)
        # 2. mach zug (bot)
    
        # current player
        #while True
        # 1. ermittel zug
        # 2. mach zug
        # 3. isGameOver?
        # 4. switch currenet player

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
        pos_captured_pieces = manage_move(result.move, captured_piece, pos_captured_pieces)
        # !! An dieser Stelle eine Funktion aufrufen um den Roboter 
        # den Move "result.move" (String) machen zu lassen. Funktion wird verlassen, 
        # wenn der Roboter fertig ist.

        print("Mensch ist am Zug!")


    print("\nSpiel beendet:", board.result())
    print(board)
    engine.quit()

if __name__ == "__main__":
    main()

"""
