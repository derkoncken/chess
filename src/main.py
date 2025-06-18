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
pos_captured_pieces = 72
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
    show_gui(True)
    
    try:
        pattern_after = poll_dgt_board()
        start, target = detect_move(pattern_before, pattern_after)
        print("Start: " + str(start) + " ,Ziel: " + str(target))
        move = chess.Move(start, target)
    except Exception as e:
        ui.label.setText(f"Zugerkennung fehlgeschlagen: {e}")
        show_gui(True)
        return

    if move in board.legal_moves:
        board.push(move)
        ui.label.setText(f"Du spielst: {move}")
        update_piece_labels(board, ui)
    else:
        ui.label.setText("Falscher Zug!")
        show_gui(True)
        return

    if board.is_game_over():
        ui.label.setText("Du hast gewonnen!")
        return
    
    result = engine.play(board, chess.engine.Limit(depth=ui.difficulty.value()))
    captured_piece = board.piece_at(result.move.to_square)
    board.push(result.move)
    ui.label.setText(f"Roboter spielt: {result.move}")
    update_piece_labels(board, ui)
    show_gui(True) #Test
    
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
        show_gui(True)
    except Exception as e:
        ui.label.setText(f"Zugerkennung fehlgeschlagen: {e}")


def poll_board_before_triggered():
    global pattern_before
    pattern_before = poll_dgt_board()

def reset_board():
    global board, engine
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)
    update_piece_labels(board, ui)
    show_gui(True)
    pos_captured_pieces = 72

def show_gui(state):
    ui.button.setEnabled(state)
    ui.poll_board_before.setEnabled(state)
    ui.reset_board.setEnabled(state)
    ui.difficulty.setEnabled(state)

def adjust_difficulty():
    diff = ui.difficulty.value()
    ui.difficulty_value.setText(str(diff))
    if diff < 6:
        ui.comparision.setText("Einfach, 800–1200 Elo")
    elif diff < 11:
        ui.comparision.setText("Mittel, 1300–1800 Elo")
    elif diff < 26:
        ui.comparision.setText("Schwer, 1900–2400 Elo")
    else:
        ui.comparision.setText("Magnus Carlson")



ui.button.clicked.connect(button_triggered)
ui.poll_board_before.clicked.connect(poll_board_before_triggered)
ui.reset_board.clicked.connect(reset_board)
ui.difficulty.valueChanged.connect(adjust_difficulty)

adjust_difficulty()
pattern_before = poll_dgt_board()
plot_png_on_label(ui.chess_board, "src/chessboard.png")
plot_png_on_label(ui.logo, "src/logo.png")
update_piece_labels(board, ui)

plot_png_on_label(ui.chess_board, "src/chessboard.png")

# App starten
sys.exit(app.exec_())



