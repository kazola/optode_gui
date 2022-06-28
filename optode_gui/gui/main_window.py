import os
import threading as th
from serial import SerialException
import optode_gui.gui.designer_main as _dm
from PyQt5.QtWidgets import (QMainWindow)
from optode_gui.gui.utils_main_window import *
from optode_gui.utils_serial import g_sp


class MainWindowOptodeGUI(QMainWindow, _dm.Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindowOptodeGUI, self).__init__(*args, **kwargs)
        gui_setup_view(self)
        gui_setup_window_center(self)
        gui_setup_buttons(self)
        self.gui_sig = gui_create_signals(self)
        self._gui_serial_open()

        # allows cleaner code
        gui_setup_decorator_serial(self, g_sp)

    @staticmethod
    def _ts(): gui_btn_test_serial()
    def click_btn_serial(self): self._th(self._ts)

    @staticmethod
    def _td1(): gui_btn_test_display(1)
    def click_btn_test_display_1(self): self._th(self._td1)

    @staticmethod
    def _td2(): gui_btn_test_display(2)
    def click_btn_test_display_2(self): self._th(self._td2)

    @staticmethod
    def _ts1(): gui_btn_test_scan(1)
    def click_btn_test_scan_1(self): self._th(self._ts1)

    @staticmethod
    def _ts2(): gui_btn_test_scan(2)
    def click_btn_test_scan_2(self): self._th(self._ts2)

    @staticmethod
    def _tw1(): gui_btn_test_wifi(1)
    def click_btn_test_wifi_1(self): self._th(self._tw1)

    @staticmethod
    def _tw2(): gui_btn_test_wifi(2)
    def click_btn_test_wifi_2(self): self._th(self._tw2)

    @staticmethod
    def _test_led_strip_on(): gui_btn_test_led_strip_on()
    def click_btn_test_led_strip_on(self): self._th(self._test_led_strip_on())

    @staticmethod
    def _test_led_strip_off(): gui_btn_test_led_strip_off()
    def click_btn_test_led_strip_off(self): self._th(self._test_led_strip_off())

    @staticmethod
    def _tml(): gui_btn_test_motor_move_left()
    def click_btn_test_motor_move_left(self): self._th(self._tml)

    @staticmethod
    def _tmr(): gui_btn_test_motor_move_right()
    def click_btn_test_motor_move_right(self): self._th(self._tmr)

    @staticmethod
    def _tll(): gui_btn_test_motor_limit_left()
    def click_btn_test_motor_limit_left(self): self._th(self._tll)

    @staticmethod
    def _tlr(): gui_btn_test_motor_limit_right()
    def click_btn_test_motor_limit_right(self): self._th(self._tlr)

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

    def _gui_serial_open(self):
        try:
            g_sp.open()
            self.lst_trace.addItem("using port {}".format(g_sp.port))
        except SerialException:
            print('error: GUI cannot open serial {}'.format(g_sp.port))
            os._exit(1)
