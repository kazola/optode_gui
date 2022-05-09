import os
import threading as th
from PyQt5.QtCore import pyqtSlot
import optode_gui.gui.designer_main as _dm
from PyQt5.QtWidgets import (QMainWindow)
from optode_gui.gui.sig import create_gui_signals
from optode_gui.gui.gui_utils import (
    gui_setup_view,
    gui_setup_window_center,
    gui_setup_buttons
)
from optode_gui.main_utils import btn_tests, btn_test_wifi, btn_test_display
from optode_gui.serial_utils import g_sp


class MainWindowOptodeGUI(QMainWindow, _dm.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindowOptodeGUI, self).__init__(*args, **kwargs)
        gui_setup_view(self)
        gui_setup_window_center(self)
        gui_setup_buttons(self)
        self.gui_sig = create_gui_signals(self)
        g_sp.open()

    @pyqtSlot(int, name='slot_progress_bar')
    def slot_progress_bar(self, v):
        self.p_bar.setValue(v)

    def _tests(self): btn_tests(self, g_sp)
    def click_btn_tests(self): self._th(self._tests)
    def _test_wifi(self): btn_test_wifi(self, g_sp)
    def click_btn_test_wifi(self): self._th(self._test_wifi)
    def _test_display(self): btn_test_display(self, g_sp)
    def click_btn_test_display(self): self._th(self._test_display)

    @staticmethod
    def _th(cb):
        # trick for responsive GUI
        th.Thread(target=cb).start()

    def closeEvent(self, _):
        _.accept()
        if g_sp.is_open:
            g_sp.close()
        os._exit(0)

    def click_btn_clr_log(self):
        self.lst_trace.clear()



