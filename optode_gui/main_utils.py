import time
from optode_gui.gui.gui_utils import gui_busy_get, gui_trace_clear, gui_trace, gui_trace_rv, \
    gui_busy_free
from optode_gui.gui.tests.tests_optode import test_serial_arduino, test_12v_arduino, test_5v_arduino, \
     test_btn_display_1_out, \
    test_display_1_in, test_led_strip_arduino, test_wifi_1, test_motor_adc, test_motor_movement, test_motor_switches


def btn_tests(g, ser):
    """
    sends test commands to Arduino via serial port
    """

    if gui_busy_get(g):
        return

    if not ser.is_open:
        print('cannot open serial port')
        return

    gt = gui_trace
    gt_rv = gui_trace_rv

    gui_trace_clear(g)
    gt(g, '-------- start of tests --------')
    gt(g, '\n')

    rv = test_serial_arduino(ser)
    gt_rv(g, rv, 'test_serial')
    gt(g, '\n')

    # rv = test_12v_arduino(ser)
    # gt_rv(g, rv, 'test_battery')
    # gt(g, '\n')

    # rv = test_5v_arduino(ser)
    # gt_rv(g, rv, 'test_vcc5v')
    # gt(g, '\n')

    # rv = test_led_strip_arduino(ser)
    # gt_rv(g, rv, 'test_led_strip')
    # gt(g, '\n')

    # rv = test_btn_display_1_out(ser)
    # gt_rv(g, rv, 'test_btn_display_out_1')
    # gt(g, '\n')
    #
    # rv_dis = rv = test_display_1_in(ser)
    # gt_rv(g, rv, 'test_vcc3v_display')
    # gt(g, '\n')

    # if rv_dis[1] == 'display on':
    #     for i in range(10):
    #         gt(g, 'will check wi-fi in {}'.format(10 - i))
    #         time.sleep(1)
    #     rv = test_wifi_1(ser)
    #     gt_rv(g, rv, 'test_vcc_wifi_1')
    #     gt(g, '\n')

    #rv_adc_mot = rv = test_motor_adc(ser)
    #gt_rv(g, rv, 'test_motor_adc')
    #gt(g, '\n')

    gt(g, '[ .... ] look / hear motor moving')
    time.sleep(.1)
    rv = test_motor_movement(ser)
    gt_rv(g, rv, 'motor_test_run')
    gt(g, '\n')

    # rv = test_motor_switches(ser)
    # gt_rv(g, rv, 'test_motor_switches')
    # gt(g, '\n')

    gt(g, '-------- end of tests --------')
    gui_busy_free()
