import os
from wireless import Wireless

def check_ping():
    hostname = "google.com"
    response = os.system("ping -c 1 " + hostname + " > /dev/null")
    # and then check the response...
    pingstatus_connected = (response == 0)

    return pingstatus_connected


def get_current_access_point():
    w = Wireless()
    return w.current()

if __name__ == "__main__":
    print( get_current_access_point() )
    x = check_ping()
    print(x)
    print(type(x))
