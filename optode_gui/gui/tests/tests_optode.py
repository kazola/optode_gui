import time


def test_serial(ser) -> tuple:
    ser.write('1'.encode())
    a = ser.readall()
    if a == b'hello':
        return 0, ''
    return 1, ''


def test_battery(ser) -> tuple:
    ser.write('2'.encode())
    a = ser.readall()
    if not a:
        return 1, ''

    # a: b'768'
    s = 'battery ADC value: {}'.format(a.decode())
    if int(a.decode()) > 512:
        return 0, s
    return 1, s


def test_vcc5v(ser) -> tuple:
    ser.write('3'.encode())
    a = ser.readall()
    if not a:
        return 1, ''

    # a: b'768'
    s = '5V ADC value: {}'.format(a.decode())
    if int(a.decode()) > 1000:
        return 0, s
    return 1, s


def test_gpio_out(ser) -> tuple:
    ser.write('4'.encode())
    a = ser.readall()
    if a == b'0':
        return 0, ''
    return 1, ''


def test_btn_scan_1(ser) -> tuple:

    ser.write('5'.encode())
    a = bytes()
    n = int(5 / .25)
    for i in range(n):
        # n times * timeout = .25
        a += ser.read()

    if a == b'0':
        return 0, ''
    return 1, ''


def test_vcc3v_display(ser) -> tuple:
    ser.write('6'.encode())
    a = ser.readall()
    if not a:
        return 1, ''

    # a: b'768'
    print(a)
    if int(a.decode()) < 100:
        return 0, 'display off'
    return 0, 'display on'
