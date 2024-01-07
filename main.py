import machine
import gc
from lib.ota_updater import OTAUpdater
import lib.wifi as wifi


def connect_and_update():
    try:
        print('Memory free', gc.mem_free())
        wlan = wifi.get_connection()
        if wlan is not None:
            net_conf = wlan.ifconfig()
            print(
                f'\nIP: {net_conf[0]} Subnet: {net_conf[1]}\nGateway: {net_conf[2]} DNS: {net_conf[3]}')
            otaUpdater = OTAUpdater(
                'https://github.com/PoniWai/pahu_pahu_akamai')
            hasUpdated = otaUpdater.install_update_if_available()
            if hasUpdated:
                machine.reset()
            else:
                del (otaUpdater)
                gc.collect()
    except OSError as exc:
        print('Update error:', exc)


connect_and_update()




import app.start
