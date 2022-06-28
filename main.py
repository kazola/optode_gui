import pathlib
import sys
from PyQt5.QtWidgets import QApplication
from optode_gui.gui.main_window import MainWindowOptodeGUI
from optode_gui.settings import ctx


if __name__ == "__main__":

    assert sys.version_info >= (3, 8, 0)
    r = pathlib.Path.cwd() / 'optode_gui'
    ctx.dir_res = r / 'gui/res'

    app = QApplication(sys.argv)
    mw = MainWindowOptodeGUI()
    mw.show()
    sys.exit(app.exec_())



