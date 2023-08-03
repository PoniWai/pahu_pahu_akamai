import wififuncs
import _thread
import time
import app.webfuncs as webfuncs
# from params import Params


def sensors_thread():
    """sensors htread
    """
    i = 3000
    while True:
        i -= 1
        Params.digi_sensors()
        time.sleep(1)
        if i is 0:
            Params.anal_sensors(True)
            i = 3000
        else:
            Params.anal_sensors()
        print(i)


def web_thread():
    while True:
        wlan = wififuncs.get_connection()
        if wlan is None:
            wififuncs.set_connection()
            webfuncs.start_web('192.168.4.1')
        else:
            network_config = wlan.ifconfig()
            print(f'\nIP: {network_config[0]} \
                Subnet: {network_config[1]} \
                Gateway: {network_config[2]} \
                DNS: {network_config[3]}')
            webfuncs.start_web(network_config[0])


# _thread.start_new_thread(sensors_thread, ())
_thread.start_new_thread(web_thread, ())
