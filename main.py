import pathlib
import sys
from PyQt5.QtWidgets import QApplication
from optode_gui.gui.main_window import MainWindowOptodeGUI
from optode_gui.utils_serial import basic_uart_test
from optode_gui.settings import ctx


TEST_BASIC_UART_COMM = False


if __name__ == "__main__":

    assert sys.version_info >= (3, 8, 0)
    r = pathlib.Path.cwd() / 'optode_gui'
    ctx.dir_res = r / 'gui/res'

    # ----------------------
    # serial terminal app
    # ----------------------
    if TEST_BASIC_UART_COMM:
        basic_uart_test()

    # ------------------------
    # Graphical Interface app
    # ------------------------
    else:
        app = QApplication(sys.argv)
        mw = MainWindowOptodeGUI()
        mw.show()
        sys.exit(app.exec_())



