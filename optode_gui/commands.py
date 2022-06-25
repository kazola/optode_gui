from optode_gui.utils_serial import get_answer_from_optode as _gao


def cmd_test_serial(ser) -> tuple:
    ser.write('1'.encode())
    a = _gao(ser, 2)
    if a == b'hello':
        return 0, ''
    return 1, ''


def cmd_test_power_adc_12v(ser) -> tuple:
    # --------------------------------
    # needs voltage-divider at board
    # --------------------------------
    ser.write('2'.encode())
    a = _gao(ser, 1)
    if not a:
        return 1, ''

    # a: b'768'
    s = 'battery ADC value = {}'.format(a)
    if int(a.decode()) > 900:
        return 0, s
    return 1, s


def cmd_test_led_strip(ser) -> tuple:
    ser.write('3'.encode())
    a = _gao(ser, 4)
    if a == b'leds':
        return 0, ''
    return 1, ''


def cmd_test_btn_display_out(i, ser) -> tuple:
    assert i in (1, 2)
    _m = {1: '4', 2: '8'}
    ser.write(_m[i].encode())
    a = _gao(ser, 4)
    if a == b'0':
        return 0, ''
    return 1, ''


def cmd_test_adc_display_in(i, ser) -> tuple:
    assert i in (1, 2)
    _m = {1: '5', 2: '9'}
    ser.write(_m[i].encode())
    a = _gao(ser, 1)
    if not a:
        return 1, ''

    # a: b'768'
    print('\tdisplay #{} ADC value ='.format(i), a)
    if int(a.decode()) < 100:
        return 0, 'display #{} is OFF'.format(i)
    return 0, 'display #{} is ON'.format(i)


def cmd_test_btn_wifi_out(i, ser) -> tuple:
    assert i in (1, 2)
    _m = {1: '6', 2: 'a'}
    ser.write(_m[i].encode())
    a = _gao(ser, 2)
    if a == b'0':
        return 0, ''
    return 1, ''


def cmd_test_adc_wifi(i, ser) -> tuple:
    assert i in (1, 2)
    _m = {1: '7', 2: 'b'}
    ser.write(_m[i].encode())
    a = _gao(ser, 3)
    print('\twi-fi #{} ADC value ='.format(i), a)
    if not a:
        return 1, ''

    if int(a.decode()) < 100:
        return 0, 'wi-fi #{} is OFF'.format(i)
    return 0, 'wi-fi #{} is ON'.format(i)


def cmd_test_motor_adc(ser) -> tuple:
    # --------------------------------
    # needs voltage-divider at board
    # --------------------------------
    ser.write('c'.encode())
    a = _gao(ser, 1)
    if not a:
        return 1, ''

    # a: b'768'
    s = 'motor ADC value = {}'.format(a)
    if int(a.decode()) > 900:
        return 0, s
    return 1, s


def cmd_test_motor_move_left(ser) -> tuple:
    ser.write('d'.encode())
    # look at seconds set in firmware test
    a = _gao(ser, 3)
    print(a)
    if a == b'motor_left_done':
        return 0, ''
    return 1, ''


def cmd_test_motor_move_right(ser) -> tuple:
    ser.write('e'.encode())
    # look at seconds set in firmware test
    a = _gao(ser, 3)
    print(a)
    if a == b'motor_right_done':
        return 0, ''
    return 1, ''


def cmd_test_motor_limit_left(ser) -> tuple:
    ser.write('f'.encode())
    a = _gao(ser, 1)
    if not a:
        return 1, ''
    return 0, a.decode()


def cmd_test_motor_limit_right(ser) -> tuple:
    ser.write('g'.encode())
    a = _gao(ser, 1)
    if not a:
        return 1, ''
    return 0, a.decode()
