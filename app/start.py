import time
import _thread
import lib.wifi as wifi
import app.loads as loads
import app.webfuncs as webfuncs
from app.params import Params


def web_thread():
    while True:
        wlan = wifi.get_connection()
        if wlan is None:
            wifi.set_connection()
            # TODO: restart if not connected in 1 min
            webfuncs.start_web('192.168.4.1')
        else:
            webfuncs.start_web(wlan.ifconfig()[0])


def sensors_thread():
    while True:
        Params.digi_sensors()        
        Params.anal_sensors()
        
        loads.on_light()
        time.sleep(2)
        
        loads.cool_out.on()
        time.sleep(2)
        
        loads.on_cool_top()
        time.sleep(2)
        
        loads.on_cool_brd()
        time.sleep(2)


        loads.off_light()
        loads.on_cool_brd()
        time.sleep(2)
        
        loads.cool_out.off()
        time.sleep(2)
        
        loads.off_cool_top()
        time.sleep(2)
        
        loads.off_cool_brd()
        time.sleep(2)


_thread.start_new_thread(web_thread, ())
_thread.start_new_thread(sensors_thread, ())
