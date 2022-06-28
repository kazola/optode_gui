from optode_gui.commands import *
import pathlib
import time
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget
from optode_gui.settings import ctx
from PyQt5.QtCore import pyqtSignal, QRect
from PyQt5.QtCore import QObject


class GUISignalsOptode(QObject):
    p_bar = pyqtSignal(int)


def gui_create_signals(self):
    gs = GUISignalsOptode()
    return gs


def gui_trace_clear(gui):
    gui.lst_trace.clear()


def gui_trace(gui, s):
    if not s:
        return
    gui.lst_trace.addItem(s)
    print(s)
    time.sleep(.1)
    gui.lst_trace.scrollToBottom()


def gui_trace_rv(gui, rv, name):
    # rv: (code, msg)
    v, msg = rv
    if v:
        gui_trace(gui, '\t[ ER ] {}'.format(name))
    else:
        # this pollutes a bit the output but, meh
        gui_trace(gui, '\t[ OK ] {}'.format(name))
    if msg:
        gui_trace(gui, '\t{}'.format(msg))


# shorter code and global variables
g_gui_busy = False
gt = gui_trace
gt_rv = gui_trace_rv
g_g = None
g_ser = None


def gui_busy_get(gui):
    global g_gui_busy
    if g_gui_busy:
        gui_trace(gui, '..... wait, I am busy')
        return True
    g_gui_busy = True
    return False


def gui_busy_free():
    global g_gui_busy
    g_gui_busy = False


def gui_setup_view(my_win):
    w = my_win
    w.setupUi(w)
    v = '1.0.00'
    s = ' GUI for optode v{}'.format(v)
    w.setWindowTitle(s)
    path = str(pathlib.Path(ctx.dir_res / 'icon_eye.ico'))
    w.setWindowIcon(QIcon(path))
    return w


def gui_setup_window_center(my_win):
    # get window + screen shape, match both, adjust upper left corner
    r = my_win.frameGeometry()
    c = QDesktopWidget().availableGeometry().center()
    r.moveCenter(c)
    my_win.move(r.topLeft())
    pass


def gui_setup_buttons(my_win):
    w = my_win
    w.btn_serial.clicked.connect(w.click_btn_serial)
    w.btn_clr_log.clicked.connect(w.click_btn_clr_log)

    w.btn_test_display_1.clicked.connect(w.click_btn_test_display_1)
    w.btn_test_wifi_1.clicked.connect(w.click_btn_test_wifi_1)
    w.btn_test_display_2.clicked.connect(w.click_btn_test_display_2)
    w.btn_test_wifi_2.clicked.connect(w.click_btn_test_wifi_2)

    w.btn_test_led_strip_on.clicked.connect(w.click_btn_test_led_strip_on)
    w.btn_test_led_strip_off.clicked.connect(w.click_btn_test_led_strip_off)
    w.btn_test_motor_move_left.clicked.connect(w.click_btn_test_motor_move_left)
    w.btn_test_motor_move_right.clicked.connect(w.click_btn_test_motor_move_right)
    w.btn_test_motor_limit_left.clicked.connect(w.click_btn_test_motor_limit_left)
    w.btn_test_motor_limit_right.clicked.connect(w.click_btn_test_motor_limit_right)


def _gui_decorator_serial(func):
    def _pre():
        if gui_busy_get(g_g):
            return 1
        if not g_ser:
            gt(g_g, 'no serial port set-up')
            return 1
        if not g_ser.is_open:
            gt(g_g, 'serial port NOT open')
            return 1

    def _post():
        gui_busy_free()

    def wrapper(args=''):
        if _pre():
            return 1
        func(args)
        _post()
    return wrapper


def gui_setup_decorator_serial(g, ser):
    global g_g
    global g_ser
    g_g = g
    g_ser = ser


@_gui_decorator_serial
def gui_btn_test_serial(args=None):
    gt(g_g, 'testing serial port')
    time.sleep(.1)
    rv = cmd_test_serial(g_ser)
    gt_rv(g_g, rv, 'test_serial')


@_gui_decorator_serial
def gui_btn_test_display(i: int):
    assert i in (1, 2)
    gt(g_g, 'look at iris #{} display'.format(i))
    rv = cmd_test_btn_display_out(i, g_ser)
    gt_rv(g_g, rv, 'test_btn_display_out_{}'.format(i))
    rv = cmd_test_adc_display_in(i, g_ser)
    gt_rv(g_g, rv, 'test_adc_display_{}'.format(i))


@_gui_decorator_serial
def gui_btn_test_scan(i: int):
    assert i in (1, 2)
    rv = cmd_test_adc_display_in(i, g_ser)
    gt_rv(g_g, rv, 'test_adc_display_{}'.format(i))
    if rv[1].endswith('OFF'):
        gt(g_g, 'display OFF, not testing scan')
        gui_busy_free()
        return

    gt(g_g, 'toggling scan {}'.format(i))
    rv = cmd_test_btn_scan_out(i, g_ser)
    gt_rv(g_g, rv, 'test_btn_scan_{}_out'.format(i))


@_gui_decorator_serial
def gui_btn_test_wifi(i: int):
    assert i in (1, 2)
    rv = cmd_test_adc_display_in(i, g_ser)
    gt_rv(g_g, rv, 'test_adc_display_{}'.format(i))
    if rv[1].endswith('OFF'):
        gt(g_g, 'display OFF, not testing wi-fi')
        gui_busy_free()
        return

    gt(g_g, 'toggling wi-fi {}'.format(i))
    rv = cmd_test_btn_wifi_out(i, g_ser)
    gt_rv(g_g, rv, 'test_btn_wifi_{}_out'.format(i))

    rv = cmd_test_adc_wifi(i, g_ser)
    gt_rv(g_g, rv, 'test_adc_wifi_{}'.format(i))


@_gui_decorator_serial
def gui_btn_test_led_strip_on(args=None):
    gt(g_g, 'testing led strip_on')
    rv = cmd_test_led_strip_on(g_ser)
    gt_rv(g_g, rv, 'test_led_strip_on')


@_gui_decorator_serial
def gui_btn_test_led_strip_off(args=None):
    gt(g_g, 'testing led strip_off')
    rv = cmd_test_led_strip_off(g_ser)
    gt_rv(g_g, rv, 'test_led_strip_off')


@_gui_decorator_serial
def gui_btn_test_motor_move_left(args=None):
    gt(g_g, 'motor should spin left')
    time.sleep(.1)
    rv = cmd_test_motor_move_left(g_ser)
    gt_rv(g_g, rv, 'test_motor_move_left')


@_gui_decorator_serial
def gui_btn_test_motor_move_right(args=None):
    gt(g_g, 'motor should spin right')
    time.sleep(.1)
    rv = cmd_test_motor_move_right(g_ser)
    gt_rv(g_g, rv, 'test_motor_move_right')


@_gui_decorator_serial
def gui_btn_test_motor_limit_left(args=None):
    gt(g_g, 'press motor limit left')
    time.sleep(.1)
    rv = cmd_test_motor_limit_left(g_ser)
    gt_rv(g_g, rv, 'test_motor_limit_left')


@_gui_decorator_serial
def gui_btn_test_motor_limit_right(args=None):
    gt(g_g, 'press motor limit right')
    time.sleep(.1)
    rv = cmd_test_motor_limit_right(g_ser)
    gt_rv(g_g, rv, 'test_motor_limit_right')


@_gui_decorator_serial
def gui_btn_test_motor_adc(args=None):
    rv = cmd_test_motor_adc(g_ser)
    gt_rv(g_g, rv, 'test_adc_motor')


@_gui_decorator_serial
def gui_btn_test_motor_switch_left(args=None):
    rv = cmd_test_motor_limit_left(g_ser)
    gt_rv(g_g, rv, 'test_motor_switch_left')
    gt(g_g, '\n')


@_gui_decorator_serial
def gui_btn_test_motor_switch_right(args=None):
    rv = cmd_test_motor_limit_right(g_ser)
    gt_rv(g_g, rv, 'test_motor_switch_right')
    gt(g_g, '\n')


@_gui_decorator_serial
def gui_btn_test_battery_adc(args=None):
    rv = cmd_test_power_adc_12v(g_ser)
    gt_rv(g_g, rv, 'test_adc_battery')
