import socket
import os


# folder paths
dir_data = None
dir_res = None


def get_lock(name):
    # hold a ref or garbage collector makes all this not work
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    try:
        # '\0' so the lock does not take a filesystem entry
        get_lock._lock_socket.bind('\0' + name)
    except socket.error:
        s = '{} already running so NOT executing this one'
        print(s.format(name))
        os._exit(1)

