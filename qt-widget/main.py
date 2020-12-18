# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

from model import Model

class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()
        self.load_ui()

        self.model = Model()
        self.ui.hitButton.clicked.connect(self.model.hit)
        self.ui.standButton.clicked.connect(self.model.stand)

        # import ipdb; ipdb.set_trace()
        self.model.player_points_changed.connect(self.ui.playerPoints.setNum)
        self.model.casino_points_changed.connect(self.ui.casinoPoints.setNum)

        self.model.player_values_changed.connect(self.ui.playerValues.setText)
        self.model.casino_values_changed.connect(self.ui.casinoValues.setText)


        import ipdb; ipdb.set_trace()

        self.model.start()

        # player_cards_changed = Signal(list)
        # casino_cards_changed = Signal(list)


        # message_changed = Signal(str)



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
