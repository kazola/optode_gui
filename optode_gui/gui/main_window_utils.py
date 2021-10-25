import pathlib
import time

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDesktopWidget
from optode_gui.gui.tests.tests_optode import test_serial, test_battery, test_vcc5v, test_gpio_out, test_btn_scan_1, \
    test_vcc3v_display, test_led_strip, test_vcc_wifi_1
from optode_gui.settings import ctx


g_gui_busy = False


def gui_progress_bar_visible(gui, v):
    gui.p_bar.setVisible(v)


def gui_trace(gui, s):
    if not s:
        return
    gui.lst_trace.addItem(s)
    print(s)
    time.sleep(.01)
    gui.lst_trace.scrollToBottom()


def _gui_rv(gui, rv, name):
    # rv: (code, msg)
    v, msg = rv
    if v == 0:
        s = '[ OK ] {}'.format(name)
    else:
        s = '[ ER ] {}'.format(name)
    gui_trace(gui, s)
    if msg:
        s = '\t{}'.format(msg)
        gui_trace(gui, s)


def gui_trace_clear(gui):
    gui.lst_trace.clear()


def gui_busy_get(gui):
    global g_gui_busy
    if g_gui_busy:
        gui_trace(gui, 'wait, I am busy')
        return True
    g_gui_busy = True
    return False


def gui_busy_free():
    global g_gui_busy
    g_gui_busy = False


def gui_setup_view(my_win):
    # qt designer stuff
    w = my_win
    w.setupUi(w)

    # version on window title bar
    v = '1.0.00'
    s = ' GUI for optode v{}'.format(v)
    w.setWindowTitle(s)
    path = str(pathlib.Path(ctx.dir_res / 'icon_eye.ico'))
    w.setWindowIcon(QIcon(path))

    return w


def gui_setup_buttons(my_win):
    w = my_win
    w.btn_tests.clicked.connect(w.click_btn_tests)
    w.btn_clr_log.clicked.connect(w.click_btn_clr_log)


def gui_setup_window_center(my_win):
    # get window + screen shape, match both, adjust upper left corner
    r = my_win.frameGeometry()
    c = QDesktopWidget().availableGeometry().center()
    r.moveCenter(c)
    my_win.move(r.topLeft())


def _sleep_with_timeout_n_message(gui, s, i):
    gui_trace(gui, s)
    for i in range(i):
        gui_trace(gui, '.')
        time.sleep(1)


def btn_tests(gui, ser):
    if gui_busy_get(gui):
        return
    if not ser.is_open:
        print('cannot open serial port')
        return

    gui_trace_clear(gui)
    gui_trace(gui, '-------- start of tests --------')

    rv = test_serial(ser)
    _gui_rv(gui, rv, 'test_serial')

    rv = test_battery(ser)
    _gui_rv(gui, rv, 'test_battery')

    rv = test_vcc5v(ser)
    _gui_rv(gui, rv, 'test_vcc5v')

    rv = test_gpio_out(ser)
    _gui_rv(gui, rv, 'test_gpio_out_13')

    rv_scan_1 = rv = test_btn_scan_1(ser)
    _gui_rv(gui, rv, 'test_btn_scan_1')

    rv_vcc_3v_1 =rv = test_vcc3v_display(ser)
    _gui_rv(gui, rv, 'test_vcc3v_display')

    rv = test_led_strip(ser)
    _gui_rv(gui, rv, 'test_led_strip')

    if rv_vcc_3v_1 != b'0':
        s = 'wait 10 seconds before checking wi-fi'
        _sleep_with_timeout_n_message(gui, s, 10)
        rv = test_vcc_wifi_1(ser)
        _gui_rv(gui, rv, 'test_vcc_wifi_1')

    gui_trace(gui, '-------- end of tests --------')
    gui_busy_free()
