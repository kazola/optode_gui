import time

from optode_gui.gui.main_window_utils import gui_busy_get, gui_trace_clear, gui_trace, gui_trace_rv, \
    gui_busy_free
from optode_gui.gui.tests.tests_optode import test_serial_arduino, test_12v_arduino, test_5v_arduino, test_gpio_out_arduino, test_btn_display_1_out, \
    test_display_1_in, test_led_strip_arduino, test_wifi_1


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
    gui_trace(gui, '\n')

    rv = test_serial_arduino(ser)
    gui_trace_rv(gui, rv, 'test_serial')
    gui_trace(gui, '\n')

    rv = test_12v_arduino(ser)
    gui_trace_rv(gui, rv, 'test_battery')
    gui_trace(gui, '\n')

    # rv = test_led_strip_arduino(ser)
    # gui_trace_rv(gui, rv, 'test_led_strip')
    # gui_trace(gui, '\n')


    # rv = test_5v_arduino(ser)
    # gui_trace_rv(gui, rv, 'test_vcc5v')
    # gui_trace(gui, '\n')

    # rv = test_gpio_out_arduino(ser)
    # gui_trace_rv(gui, rv, 'test_gpio_out_13')
    # gui_trace(gui, '\n')

    rv = test_btn_display_1_out(ser)
    gui_trace_rv(gui, rv, 'test_btn_display_out_1')
    gui_trace(gui, '\n')

    rv_vcc_3v_1 = rv = test_display_1_in(ser)
    gui_trace_rv(gui, rv, 'test_vcc3v_display')
    gui_trace(gui, '\n')



    #if rv_vcc_3v_1 != b'0':
    #    s = 'checking wi-fi in 10 seconds...'
    #    _sleep_with_timeout_n_message(gui, s, 10)
    #    rv = test_wifi_1(ser)
    #    gui_trace_rv(gui, rv, 'test_vcc_wifi_1')
    #    gui_trace(gui, '\n')

    gui_trace(gui, '-------- end of tests --------')
    gui_busy_free()
