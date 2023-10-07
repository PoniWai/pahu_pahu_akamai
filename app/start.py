import time
import _thread
import lib.wifi as wifi
import app.webfuncs as webfuncs
import machine
import esp32


def web_thread():
    while True:
        wlan = wifi.get_connection()
        if wlan is None:
            wifi.set_connection()
            webfuncs.start_web('192.168.4.1')
        else:
            webfuncs.start_web(wlan.ifconfig()[0])


def sensors_thread():
    while True:
        print("Hall Sensor Value:", esp32.hall_sensor())
        print("Temperature:", (esp32.raw_temperature() - 32) / 1.8, "°C")
        time.sleep(10)


_thread.start_new_thread(web_thread, ())
_thread.start_new_thread(sensors_thread, ())
