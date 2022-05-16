import time
from optode_gui.gui.utils_gui import gui_busy_get, gui_trace, gui_trace_rv, \
    gui_busy_free
from optode_gui.tests_optode import test_serial, test_power_adc_12v, \
    test_led_strip, test_motor_adc, \
    test_motor_move_left, test_motor_move_right, test_motor_switch_left, test_motor_switch_right, \
    test_btn_display_out, test_adc_display_in, test_btn_wifi_out, test_adc_wifi


# shorter code
gt = gui_trace
gt_rv = gui_trace_rv


# global variables
g_g = None
g_ser = None


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


def decorator_serial(func):
    def wrapper(args=''):
        if _pre():
            return 1
        func(args)
        _post()
    return wrapper


def decorator_setup(g, ser):
    global g_g
    global g_ser
    g_g = g
    g_ser = ser


@decorator_serial
def btn_test_serial(args=None):
    gt(g_g, 'testing serial port')
    time.sleep(.1)
    rv = test_serial(g_ser)
    gt_rv(g_g, rv, 'test_serial')


@decorator_serial
def btn_test_display(i: int):
    assert i in (1, 2)
    gt(g_g, 'look at iris #{} display'.format(i))
    rv = test_btn_display_out(i, g_ser)
    gt_rv(g_g, rv, 'test_btn_display_out_{}'.format(i))
    rv = test_adc_display_in(i, g_ser)
    gt_rv(g_g, rv, 'test_adc_display_{}'.format(i))


@decorator_serial
def btn_test_wifi(i: int):
    assert i in (1, 2)
    rv = test_adc_display_in(i, g_ser)
    gt_rv(g_g, rv, 'test_adc_display_{}'.format(i))
    if rv[1].endswith('OFF'):
        gt(g_g, 'display OFF, not testing wi-fi')
        gui_busy_free()
        return

    gt(g_g, 'toggling wi-fi {}'.format(i))
    rv = test_btn_wifi_out(i, g_ser)
    gt_rv(g_g, rv, 'test_btn_wifi_{}_out'.format(i))

    rv = test_adc_wifi(i, g_ser)
    gt_rv(g_g, rv, 'test_adc_wifi_{}'.format(i))


@decorator_serial
def btn_test_led_strip(args=None):
    gt(g_g, 'testing led strip')
    rv = test_led_strip(g_ser)
    gt_rv(g_g, rv, 'test_led_strip')


@decorator_serial
def btn_test_motor_move_left(args=None):
    gt(g_g, 'motor should spin left')
    time.sleep(.1)
    rv = test_motor_move_left(g_ser)
    gt_rv(g_g, rv, 'test_motor_move_left')


@decorator_serial
def btn_test_motor_move_right(args=None):
    gt(g_g, 'motor should spin right')
    time.sleep(.1)
    rv = test_motor_move_right(g_ser)
    gt_rv(g_g, rv, 'test_motor_move_right')


@decorator_serial
def btn_test_motor_adc(args=None):
    rv = test_motor_adc(g_ser)
    gt_rv(g_g, rv, 'test_adc_motor')


@decorator_serial
def btn_test_motor_switch_left(args=None):
    rv = test_motor_switch_left(g_ser)
    gt_rv(g_g, rv, 'test_motor_switch_left')
    gt(g_g, '\n')


@decorator_serial
def btn_test_motor_switch_right(args=None):
    rv = test_motor_switch_right(g_ser)
    gt_rv(g_g, rv, 'test_motor_switch_right')
    gt(g_g, '\n')


@decorator_serial
def btn_test_battery_adc(args=None):
    rv = test_power_adc_12v(g_ser)
    gt_rv(g_g, rv, 'test_adc_battery')
