import pathlib
import time
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDesktopWidget
from optode_gui.settings import ctx


g_gui_busy = False


def gui_trace_clear(gui):
    gui.lst_trace.clear()


def gui_progress_bar_visible(gui, v):
    gui.p_bar.setVisible(v)


def gui_trace(gui, s):
    if not s:
        return
    gui.lst_trace.addItem(s)
    print(s)
    time.sleep(.01)
    gui.lst_trace.scrollToBottom()


def gui_trace_rv(gui, rv, name):
    # rv: (code, msg)
    v, msg = rv
    if v == 0:
        s = '[ OK ] {}'.format(name)
    else:
        s = '[ ER ] {}'.format(name)
    gui_trace(gui, s)
    if msg:
        gui_trace(gui, '\t{}'.format(msg))


# needed, GUI button presses are threaded
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
    w.progressBar.setValue(0)


def gui_setup_window_center(my_win):
    # get window + screen shape, match both, adjust upper left corner
    r = my_win.frameGeometry()
    c = QDesktopWidget().availableGeometry().center()
    r.moveCenter(c)
    my_win.move(r.topLeft())
