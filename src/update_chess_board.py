from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QPoint
import chess
import os

def update_piece_labels(board, ui):
    """
    Zeigt Figuren auf dem Brett basierend auf einem chess.Board().
    Nutzt 32 QLabel-Objekte: label_piece_0 bis label_piece_31
    Mit Logging für Debugzwecke.
    """

    square_size = 85
    offset_x = 20
    offset_y = 20

    print("▶️ Starte Figuren-Update")
    print(f"Figuren auf dem Brett: {len(board.piece_map())}")

    # Blende alle Figuren-Labels aus
    for i in range(32):
        label = getattr(ui, f"label_piece_{i}", None)
        if label:
            label.hide()
        else:
            print(f"⚠️ Label label_piece_{i} nicht gefunden")

    # Zeige alle aktuellen Figuren
    piece_index = 0
    for square, piece in board.piece_map().items():
        if piece_index >= 32:
            print("⚠️ Mehr als 32 Figuren – zu viele für Labels")
            break

        file = chess.square_file(square)
        rank = chess.square_rank(square)

        x = offset_x + file * square_size
        y = offset_y + (7 - rank) * square_size

        color = 'w' if piece.color == chess.WHITE else 'b'
        symbol = piece.symbol().lower()
        image_path = f"src/icons/{color}{symbol}.png"

        if not os.path.exists(image_path):
            print(f"❌ Bild nicht gefunden: {image_path}")
            continue

        label_name = f"label_piece_{piece_index}"
        label = getattr(ui, label_name, None)

        if label:
            pixmap = QPixmap(image_path)
            label.setPixmap(pixmap)
            label.move(QPoint(x, y))
            label.setVisible(True)
            print(f"✅ {label_name}: {color}{symbol} auf {chess.square_name(square)} → ({x},{y})")
        else:
            print(f"❌ QLabel {label_name} nicht gefunden")

        piece_index += 1

    print("✅ Figurenaktualisierung abgeschlossen.\n")
