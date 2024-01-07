import time
import _thread
import lib.wifi as wifi
import app.loads as loads
import app.webfuncs as webfuncs
from app.params import Params
import app.battery


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
    loads.on_light()
      
    while True:
        loads.cool_out.on()
    
        # Read sensors
        Params.digi_sensors()
        Params.anal_sensors()
        # Check parameters and run coolers if needed
        loads.check_top_tmp()
        loads.check_brd()
        print('\n\n\n')
        print('----==Soil Moisture==-----\n')
        print(f'upper: {round(Params.ec_upper/40.96, 1)} | \
            lower: {round(Params.ec_lower/40.96, 1)}\n')
        print('----==Air==----\n')
        print(f'Temperatures: ds {round(Params.air_ds_tmp, 1)} | \
            dht {Params.air_tmp}\n')
        print(f'Humidity: {Params.air_hmd}\n')
        print('----==Space==----\n')
        print(f'Temperature: {round(Params.space_ds_tmp, 1)}\n')
        print('----==Board==----\n')
        print(f'Temperature: {Params.brd_tmp} | \
            Humidity: {Params.brd_hmd}\n')
        print('----==Power==----\n')
        print('----==Power==----\n')
        print(f'Chip temperature: {round(Params.chip_tmp, 1)} | \
            +12V: {round(Params.v_ps*0.0123, 1)}\n')
        print('\n\n\n')
        time.sleep(15)
    

_thread.start_new_thread(web_thread, ())
# _thread.start_new_thread(sensors_thread, ())
