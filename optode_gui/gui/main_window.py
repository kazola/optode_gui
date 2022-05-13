import os
import threading as th
import optode_gui.gui.designer_main as _dm
from PyQt5.QtWidgets import (QMainWindow)
from optode_gui.gui.sig import create_gui_signals
from optode_gui.gui.utils_gui import (
    gui_setup_view,
    gui_setup_window_center,
    gui_setup_buttons
)
from optode_gui.utils_main import btn_test_wifi_1, btn_test_display_1, btn_test_led_strip, \
    btn_test_motor_move_left, btn_test_motor_move_right, decorator_setup, btn_test_serial
from optode_gui.utils_serial import g_sp


class MainWindowOptodeGUI(QMainWindow, _dm.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindowOptodeGUI, self).__init__(*args, **kwargs)
        gui_setup_view(self)
        gui_setup_window_center(self)
        gui_setup_buttons(self)
        self.gui_sig = create_gui_signals(self)
        g_sp.open()

        # allows cleaner code
        decorator_setup(self, g_sp)

    @staticmethod
    def _test_serial(): btn_test_serial()
    def click_btn_serial(self): self._th(self._test_serial)

    @staticmethod
    def _test_wifi_1(): btn_test_wifi_1()
    def click_btn_test_wifi_1(self): self._th(self._test_wifi_1)

    @staticmethod
    def _test_display_1(): btn_test_display_1()
    def click_btn_test_display_1(self): self._th(self._test_display_1)

    @staticmethod
    def _test_led_strip(): btn_test_led_strip()
    def click_btn_test_led_strip(self): self._th(self._test_led_strip)

    @staticmethod
    def _test_motor_move_left(): btn_test_motor_move_left()
    def click_btn_test_motor_move_left(self): self._th(self._test_motor_move_left)

    @staticmethod
    def _test_motor_move_right(): btn_test_motor_move_right()
    def click_btn_test_motor_move_right(self): self._th(self._test_motor_move_right)

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



