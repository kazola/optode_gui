import os
import time
import serial
from serial import SerialException
import platform


if platform.system() == 'Windows':
    SERIAL_PORT_ARDUINO_4808_0 = 'COM3'
    SERIAL_PORT_ARDUINO_4808_1 = 'COM4'
else:
    SERIAL_PORT_ARDUINO_4808_0 = '/dev/ttyUSB0'
    SERIAL_PORT_ARDUINO_4808_1 = '/dev/ttyUSB1'
SERIAL_PORT = SERIAL_PORT_ARDUINO_4808_1
if not os.path.exists(SERIAL_PORT_ARDUINO_4808_1):
    SERIAL_PORT = SERIAL_PORT_ARDUINO_4808_0


# global serial port object
SERIAL_BYTE_TIMEOUT = .25
g_sp = serial.Serial()
g_sp.baudrate = 9600
g_sp.port = SERIAL_PORT
g_sp.timeout = SERIAL_BYTE_TIMEOUT


def get_answer_from_optode(ser, timeout_secs=1):
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
