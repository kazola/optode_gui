from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject


class SignalsGUI(QObject):
    p_bar = pyqtSignal(int)


def create_gui_signals(self):
    gs = SignalsGUI()
    return gs
