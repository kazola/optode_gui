import serial


SERIAL_PORT_ARDUINO_MEGA = '/dev/ttyACM0'
SERIAL_PORT_ARDUINO_4808 = '/dev/ttyUSB1'
SERIAL_PORT = SERIAL_PORT_ARDUINO_4808


# global serial port object
SERIAL_BYTE_TIMEOUT = .25
g_sp = serial.Serial()
g_sp.baudrate = 9600
g_sp.port = SERIAL_PORT
g_sp.timeout = SERIAL_BYTE_TIMEOUT


def basic_uart_test():
    g_sp.open()
    if g_sp.is_open:
        print('ok')
        while 1:
            rv = g_sp.readall()
            print(rv)
    g_sp.close()
