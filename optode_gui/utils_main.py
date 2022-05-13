import time
from optode_gui.gui.utils_gui import gui_busy_get, gui_trace, gui_trace_rv, \
    gui_busy_free
from optode_gui.gui.tests.tests_optode import test_serial, test_power_adc_12v, \
    test_btn_display_1_out, \
    test_adc_display_1_in, test_led_strip, test_adc_wifi_1, test_motor_adc, \
    test_btn_wifi_1_out, test_motor_move_left, test_motor_move_right, test_motor_switch_left, test_motor_switch_right

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
    def wrapper():
        if _pre():
            return 1
        func()
        _post()
    return wrapper


def decorator_setup(g, ser):
    global g_g
    global g_ser
    g_g = g
    g_ser = ser


@decorator_serial
def btn_test_serial():
    gt(g_g, 'testing serial port')
    time.sleep(.1)
    rv = test_serial(g_ser)
    gt_rv(g_g, rv, 'test_serial')


@decorator_serial
def btn_test_display_1():
    gt(g_g, 'look at iris #1 display')
    rv = test_btn_display_1_out(g_ser)
    gt_rv(g_g, rv, 'test_btn_display_out_1')
    rv = test_adc_display_1_in(g_ser)
    gt_rv(g_g, rv, 'test_adc_display_1')


@decorator_serial
def btn_test_wifi_1():
    rv = test_adc_display_1_in(g_ser)
    gt_rv(g_g, rv, 'test_adc_display_1')
    if rv[1].endswith('OFF'):
        gt(g_g, 'display OFF, not testing wi-fi')
        gui_busy_free()
        return

    gt(g_g, 'toggling wi-fi')
    rv = test_btn_wifi_1_out(g_ser)
    gt_rv(g_g, rv, 'test_btn_wifi_1_out')
    rv = test_adc_wifi_1(g_ser)
    gt_rv(g_g, rv, 'test_adc_wifi_1')


@decorator_serial
def btn_test_led_strip():
    gt(g_g, 'testing led strip')
    rv = test_led_strip(g_ser)
    gt_rv(g_g, rv, 'test_led_strip')


@decorator_serial
def btn_test_motor_move_left():
    gt(g_g, 'motor should spin left')
    time.sleep(.1)
    rv = test_motor_move_left(g_ser)
    gt_rv(g_g, rv, 'test_motor_move_left')


@decorator_serial
def btn_test_motor_move_right():
    gt(g_g, 'motor should spin right')
    time.sleep(.1)
    rv = test_motor_move_right(g_ser)
    gt_rv(g_g, rv, 'test_motor_move_right')


@decorator_serial
def btn_test_motor_adc():
    rv = test_motor_adc(g_ser)
    gt_rv(g_g, rv, 'test_adc_motor')


@decorator_serial
def btn_test_motor_switch_left():
    rv = test_motor_switch_left(g_ser)
    gt_rv(g_g, rv, 'test_motor_switch_left')
    gt(g_g, '\n')


@decorator_serial
def btn_test_motor_switch_right():
    rv = test_motor_switch_right(g_ser)
    gt_rv(g_g, rv, 'test_motor_switch_right')
    gt(g_g, '\n')


@decorator_serial
def btn_test_battery_adc():
    rv = test_power_adc_12v(g_ser)
    gt_rv(g_g, rv, 'test_adc_battery')
