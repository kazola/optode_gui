from optode_gui.commands import *
import pathlib
import time
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget
from optode_gui.settings import ctx
from PyQt5.QtCore import pyqtSignal, QRect
from PyQt5.QtCore import QObject

from optode_gui.utils_serial import g_sp


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
    w.btn_test_display_2.clicked.connect(w.click_btn_test_display_2)
    w.btn_test_scan_1.clicked.connect(w.click_btn_test_scan_1)
    w.btn_test_scan_2.clicked.connect(w.click_btn_test_scan_2)
    w.btn_test_wifi_1.clicked.connect(w.click_btn_test_wifi_1)
    w.btn_test_wifi_2.clicked.connect(w.click_btn_test_wifi_2)

    w.btn_test_led_strip_on.clicked.connect(w.click_btn_test_led_strip_on)
    w.btn_test_led_strip_off.clicked.connect(w.click_btn_test_led_strip_off)
    w.btn_test_motor_move_left.clicked.connect(w.click_btn_test_motor_move_left)
    w.btn_test_motor_move_right.clicked.connect(w.click_btn_test_motor_move_right)
    w.btn_test_motor_limit_left.clicked.connect(w.click_btn_test_motor_limit_left)
    w.btn_test_motor_limit_right.clicked.connect(w.click_btn_test_motor_limit_right)
    w.btn_test_motor_speed.clicked.connect(w.click_btn_test_motor_speed)

    w.btn_loop.clicked.connect(w.click_btn_test_loop)


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


# allows cleaner code
def gui_setup_decorator_serial(g, ser):
    global g_g
    global g_ser
    g_g = g
    g_ser = ser


def gui_btn_test_serial(args=None):
    p = g_g.combo_ports.currentText()
    if not p:
        gt(g_g, 'no serial port to try')
        return

    # remove spaces put there for aesthetics
    p = p.replace(' ', '')
    g_sp.port = p
    g_sp.open()
    gt(g_g, 'testing serial port {}'.format(p))
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


@_gui_decorator_serial
def gui_btn_test_motor_speed(args=None):
    gt(g_g, 'press motor speed')
    time.sleep(.1)
    rv = cmd_test_motor_speed(g_ser)
    print(rv)
    gt_rv(g_g, rv, 'test_motor_speed')


def _lt(s):
    g_g.lst_trace.addItem('    - {}'.format(s))


def _loop():
    def _post():
        time.sleep(1)
        _lt('switch display #1 OFF')
        cmd_test_btn_display_out(1, g_ser)
        rv = cmd_test_adc_display_in(1, g_ser)
        if rv[1].endswith('ON'):
            return 'error btn_display_1_off'

        time.sleep(1)
        _lt('switch display #2 OFF')
        cmd_test_btn_display_out(2, g_ser)
        rv = cmd_test_adc_display_in(2, g_ser)
        if rv[1].endswith('ON'):
            return 'error btn_display_2_off'

        g_g.lst_trace.addItem('\nend of loop')

    def _pre():
        s = '\n\n\nstart of loop with {} runs'.format(reps)
        g_g.lst_trace.addItem(s)
        g_g.lst_trace.addItem('-' * (len(s) + 7))

        time.sleep(1)
        _lt('motor towards start')
        rv = cmd_test_motor_move_left(g_ser)
        if rv[0]:
            return 'pre: error motor_move_left'

        time.sleep(1)
        _lt('switch display #1 ON')
        cmd_test_btn_display_out(1, g_ser)
        rv = cmd_test_adc_display_in(1, g_ser)
        if rv[1].endswith('OFF'):
            return 'pre: error btn_display_1_on'

        time.sleep(1)
        _lt('switch display #2 ON')
        cmd_test_btn_display_out(2, g_ser)
        rv = cmd_test_adc_display_in(2, g_ser)
        if rv[1].endswith('OFF'):
            return 'pre: error btn_display_2_on'

    def _do():
        s = '\nrun {} of {} starts'.format(i + 1, reps)
        g_g.lst_trace.addItem(s)

        time.sleep(1)
        _lt('switch SCAN #1 ON')
        cmd_test_btn_scan_out(1, g_ser)

        time.sleep(1)
        _lt('switch SCAN #2 ON')
        cmd_test_btn_scan_out(2, g_ser)

        time.sleep(1)
        _lt('switch LED ON')
        cmd_test_led_strip_on(g_ser)

        time.sleep(1)
        _lt('motor towards right')
        rv = cmd_test_motor_move_right(g_ser)
        if rv[0]:
            return 'do: error motor_move_right'

        time.sleep(1)
        _lt('switch LED OFF')
        cmd_test_led_strip_off(g_ser)

        time.sleep(1)
        _lt('switch SCAN #1 OFF')
        cmd_test_btn_scan_out(1, g_ser)

        time.sleep(1)
        _lt('switch SCAN #2 OFF')
        cmd_test_btn_scan_out(2, g_ser)

        time.sleep(1)
        _lt('switch WIFI #1 ON')
        cmd_test_btn_wifi_out(1, g_ser)
        rv = cmd_test_adc_wifi(1, g_ser)
        if rv[1].endswith('OFF'):
            return 'do: error btn_wifi_1_on'

        time.sleep(1)
        _lt('switch WIFI #2 ON')
        cmd_test_btn_wifi_out(2, g_ser)
        rv = cmd_test_adc_wifi(2, g_ser)
        if rv[1].endswith('OFF'):
            return 'do: error btn_wifi_2_on'

        _delay_bw_runs = 10
        _adjusted_delay_wifi = delay_wifi - _delay_bw_runs
        _lt('wait: {} secs for download'.format(_adjusted_delay_wifi))
        time.sleep(_adjusted_delay_wifi)

        time.sleep(1)
        _lt('switch WIFI #1 OFF')
        cmd_test_btn_wifi_out(1, g_ser)
        rv = cmd_test_adc_wifi(1, g_ser)
        if rv[1].endswith('ON'):
            return 'do: error btn_wifi_1_off'

        time.sleep(1)
        _lt('switch WIFI #2 OFF')
        cmd_test_btn_wifi_out(2, g_ser)
        rv = cmd_test_adc_wifi(2, g_ser)
        if rv[1].endswith('ON'):
            return 'do: error btn_wifi_2_off'

        s = 'run {} of {} ended OK'.format(i + 1, reps)
        g_g.lst_trace.addItem(s)

        _ = 10
        _lt('wait: {} secs bw runs'.format(_))
        time.sleep(_)

    # ------------
    # loop core
    # ------------
    reps = g_g.spin_loop_reps.value()
    delay_wifi = g_g.spin_loop_delay_time.value()

    _ = _pre()
    if _:
        g_g.lst_trace.addItem(_)
        return

    _ = 0
    for i in range(reps):
        _ = _do()
        if _:
            g_g.lst_trace.addItem(_)
            break

    _post()


@_gui_decorator_serial
def gui_btn_test_loop(args=None):
    _loop()

