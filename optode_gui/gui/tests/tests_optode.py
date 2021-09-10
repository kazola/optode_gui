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
