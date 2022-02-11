def test_serial_arduino(ser) -> tuple:
    ser.write('1'.encode())
    a = ser.readall()
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


def test_gpio_out_arduino(ser) -> tuple:
    ser.write('4'.encode())
    a = ser.readall()
    if a == b'0':
        return 0, ''
    return 1, ''


def test_btn_display_1_out(ser) -> tuple:
    ser.write('5'.encode())
    a = bytes()
    n = int(5 / .25)
    for i in range(n):
        # n times * timeout = .25
        a += ser.read()

    if a == b'0':
        return 0, ''
    return 1, ''


def test_display_1_in(ser) -> tuple:
    ser.write('6'.encode())
    a = ser.readall()
    if not a:
        # no answer
        return 1, ''

    # a: b'768'
    if int(a.decode()) < 100:
        return 0, 'display off'
    return 0, 'display on'


def test_led_strip_arduino(ser) -> tuple:
    ser.write('7'.encode())
    a = ser.readall()
    print(a)
    if a == b'leds':
        return 0, ''
    return 1, ''


def test_wifi_1(ser) -> tuple:
    ser.write('8'.encode())
    a = ser.readall()
    if not a:
        return 1, ''

    # a: b'768'
    print(a)
    if int(a.decode()) < 100:
        return 0, 'wifi_1 off'
    return 0, 'wifi_1 on'


def test_motor(ser) -> tuple:
    ser.write('9'.encode())
    a = bytes()
    n = int(12 / .25)
    for i in range(n):
        # n times * timeout = .25
        a += ser.read()

    if a == b'0':
        return 0, ''
    return 1, ''
