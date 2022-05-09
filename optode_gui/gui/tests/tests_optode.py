import time

from optode_gui.serial_utils import SERIAL_BYTE_TIMEOUT


def test_serial_arduino(ser) -> tuple:
    ser.write('1'.encode())
    a = ser.readall()
    print(a)
    if a == b'hello':
        return 0, ''
    return 1, ''


def test_12v_arduino(ser) -> tuple:
    ser.write('2'.encode())
    a = ser.readall()
    if not a:
        return 1, ''

    # a: b'768'
    s = 'battery ADC value: {}'.format(a.decode())
    if int(a.decode()) > 512:
        return 0, s
    return 1, s


def test_5v_arduino(ser) -> tuple:
    ser.write('3'.encode())
    a = ser.readall()
    if not a:
        return 1, ''

    # a: b'768'
    s = '5V ADC value: {}'.format(a.decode())
    if int(a.decode()) > 1000:
        return 0, s
    return 1, s


def test_btn_display_1_out(ser) -> tuple:
    ser.write('5'.encode())
    a = bytes()
    seconds = 4
    n = int(seconds / SERIAL_BYTE_TIMEOUT)
    for i in range(n):
        a += ser.read()
    if a == b'0':
        return 0, ''
    return 1, ''


def test_adc_display_1_in(ser) -> tuple:
    ser.write('6'.encode())
    a = ser.readall()
    if not a:
        # no answer
        return 1, ''

    # a: b'768'
    print('adc display #1 value =', a)
    if int(a.decode()) < 100:
        return 0, 'display #1 is OFF'
    return 0, 'display #1 is ON'


def test_led_strip_arduino(ser) -> tuple:
    ser.write('4'.encode())
    a = ser.readall()
    print(a)
    if a == b'leds':
        return 0, ''
    return 1, ''


def test_btn_wifi_1_out(ser) -> tuple:
    ser.write('7'.encode())
    a = bytes()
    n = int(4 / SERIAL_BYTE_TIMEOUT)
    for i in range(n):
        a += ser.read()

    if a == b'0':
        return 0, ''
    return 1, ''


def test_adc_wifi_1(ser) -> tuple:
    ser.write('8'.encode())
    a = ser.readall()
    if not a:
        return 1, ''

    # a: b'768'
    print('adc wifi #1 value =', a)
    if int(a.decode()) < 400:
        return 0, 'wifi #1 is OFF'
    return 0, 'wifi #1 is ON'


def test_motor_adc(ser) -> tuple:
    ser.write('9'.encode())
    a = ser.readall()
    if not a:
        print('k')
        return 1, ''

    # a: b'768'
    s = 'motor ADC value: {}'.format(a.decode())
    if int(a.decode()) > 900:
        return 0, s
    return 1, s


def test_motor_movement(ser) -> tuple:
    ser.write('a'.encode())
    a = bytes()

    # calculate waiting time w/ firmware code
    delay_ms, steps_ms, slack_ms = 2 * 500, 2 * 300, 1000
    wait_ms = delay_ms + steps_ms + slack_ms
    till = time.perf_counter() + (wait_ms / 1000)
    while time.perf_counter() < till:
        a += ser.read()

    if a == b'motor_test_run':
        return 0, ''
    return 1, ''


def test_motor_switches(ser) -> tuple:
    time.sleep(2)
    ser.write('b'.encode())
    a = ser.readall()
    if not a:
        return 1, ''
    return 0, a.decode()
