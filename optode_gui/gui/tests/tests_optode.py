import time
from serial import SerialException


def _read_serial(ser, timeout_secs=1):
    a = bytes()
    t = time.perf_counter() + timeout_secs
    while 1:
        if time.perf_counter() > t:
            break
        try:
            a += ser.read()
        except SerialException:
            pass
    return a


def test_serial(ser) -> tuple:
    ser.write('1'.encode())
    a = _read_serial(ser, 2)
    if a == b'hello':
        return 0, ''
    return 1, ''


def test_power_adc_12v(ser) -> tuple:
    # --------------------------------
    # needs voltage-divider at board
    # --------------------------------
    ser.write('2'.encode())
    a = _read_serial(ser, 1)
    if not a:
        return 1, ''

    # a: b'768'
    s = 'battery ADC value = {}'.format(a)
    if int(a.decode()) > 900:
        return 0, s
    return 1, s


# -------------
# LED section
# -------------

def test_led_strip(ser) -> tuple:
    ser.write('3'.encode())
    a = _read_serial(ser, 4)
    if a == b'leds':
        return 0, ''
    return 1, ''


# ----------------
# display section
# ----------------

def test_btn_display_1_out(ser) -> tuple:
    ser.write('4'.encode())
    a = _read_serial(ser, 4)
    if a == b'0':
        return 0, ''
    return 1, ''


def test_adc_display_1_in(ser) -> tuple:
    ser.write('5'.encode())
    a = _read_serial(ser, 1)
    if not a:
        return 1, ''

    # a: b'768'
    print('display #1 ADC value =', a)
    if int(a.decode()) < 100:
        return 0, 'display #1 is OFF'
    return 0, 'display #1 is ON'


# ----------------
# wi-fi section
# ----------------

def test_btn_wifi_1_out(ser) -> tuple:
    ser.write('6'.encode())
    a = _read_serial(ser, 3)
    if a == b'0':
        return 0, ''
    return 1, ''


def test_adc_wifi_1(ser) -> tuple:
    ser.write('7'.encode())
    a = _read_serial(ser, 1)
    if not a:
        return 1, ''

    # a: b'768'
    print('wi-fi #1 ADC value =', a)
    if int(a.decode()) < 100:
        return 0, 'wi-fi #1 is OFF'
    return 0, 'wi-fi #1 is ON'


# ----------------
# motor section
# ----------------

def test_motor_adc(ser) -> tuple:
    # --------------------------------
    # needs voltage-divider at board
    # --------------------------------
    ser.write('8'.encode())
    a = _read_serial(ser, 1)
    if not a:
        return 1, ''

    # a: b'768'
    s = 'motor ADC value = {}'.format(a)
    if int(a.decode()) > 900:
        return 0, s
    return 1, s


def test_motor_move_left(ser) -> tuple:
    ser.write('9'.encode())
    # look at seconds set in firmware test
    a = _read_serial(ser, 3)
    print(a)
    if a == b'motor_left_done':
        return 0, ''
    return 1, ''


def test_motor_move_right(ser) -> tuple:
    ser.write('a'.encode())
    # look at seconds set in firmware test
    a = _read_serial(ser, 3)
    print(a)
    if a == b'motor_right_done':
        return 0, ''
    return 1, ''


def test_motor_switch_left(ser) -> tuple:
    ser.write('b'.encode())
    a = _read_serial(ser, 1)
    if not a:
        return 1, ''
    return 0, a.decode()


def test_motor_switch_right(ser) -> tuple:
    ser.write('c'.encode())
    a = _read_serial(ser, 1)
    if not a:
        return 1, ''
    return 0, a.decode()
