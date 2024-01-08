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
        time_tpl = time.localtime(time.time())
        print('\n\n\n')
        print(f'Y-{time_tpl[0]-1970} M-{time_tpl[1]} D-{time_tpl[2]} | {time_tpl[3]}:{time_tpl[4]}:{time_tpl[5]}')
        print('Soil Moisture==-----', end = ' ')
        print(f'upper: {round(Params.ec_upper/40.96, 1)} | \
lower: {round(Params.ec_lower/40.96, 1)}\n')
        print('Air==----', end = ' ')
        print(f'ds {round(Params.air_ds_tmp, 1)} | \
dht T: {Params.air_tmp} RH: {Params.air_hmd}\n')
        print(f'Space Temperature==---- {round(Params.space_ds_tmp, 1)}\n')
        print('Board==----', end = ' ')
        print(f'Temperature: {Params.brd_tmp} | \
Humidity: {Params.brd_hmd}\n')
        print('Power==----', end = ' ')
        print(f'Chip temperature: {round(Params.chip_tmp, 1)} | \
+12V: {round(Params.v_ps*0.004984, 1)}')
        time.sleep(15)
    

# _thread.start_new_thread(web_thread, ())
_thread.start_new_thread(sensors_thread, ())
