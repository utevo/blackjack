# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSizePolicy, QLayout, QMainWindow
from PySide2.QtGui import QImage, QIcon, QPixmap, QFont
from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader

from model import Model


class Card(QWidget):
    def __init__(self, rank, suit,):
        super().__init__()

        font = QFont()
        font.setPixelSize(20)

        layout = QVBoxLayout(self)
        rank_label = QLabel(self)
        rank_label.setText(rank)
        rank_label.setFont(font)
        rank_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(rank_label)

        suit_pixmap = QPixmap(f'./images/{suit}.svg')
        suit_label = QLabel()
        suit_label.setPixmap(suit_pixmap)
        h = suit_label.height()

        suit_label.setPixmap(suit_pixmap.scaled(h*1.5, h / 5, Qt.KeepAspectRatio))
        suit_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(suit_label)



class CardDeckManager:
    def __init__(self, layout: QLayout, read_cards, notify):
        self.layout = layout
        self.read_cards = read_cards
        self.card_changed_notify = notify
        self.load_cards()
        notify.connect(lambda: self.handle_change())

    def handle_change(self):
        self.delete_cards()
        self.load_cards()

    def delete_cards(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

    def load_cards(self):
        cards = self.read_cards()
        for card_data in cards:
            self.layout.addWidget(Card(card_data[0], card_data[1]))

class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.load_ui()
        self.setMinimumSize(800, 420)

        self.model = Model()
        self.ui.hitButton.clicked.connect(self.model.hit)
        self.ui.standButton.clicked.connect(self.model.stand)

        self.model.player_points_changed.connect(self.ui.playerPoints.setNum)
        self.model.casino_points_changed.connect(self.ui.casinoPoints.setNum)

        self.model.player_values_changed.connect(self.ui.playerValues.setText)
        self.model.casino_values_changed.connect(self.ui.casinoValues.setText)



        CardDeckManager(layout=self.ui.playerCardsLayout,
                                       read_cards=self.model.read_player_cards, notify=self.model.player_cards_changed)
        CardDeckManager(layout=self.ui.casinoCardsLayout,
                                       read_cards=self.model.read_casino_cards, notify=self.model.casino_cards_changed)

        self.model.start()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()


if __name__ == "__main__":
    app = QApplication([])
    widget = Window()
    widget.show()
    sys.exit(app.exec_())
