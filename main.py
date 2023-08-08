import machine
import network
import gc
import _thread
import time
import app.webfuncs as webfuncs
from ota_updater import OTAUpdater
from app.sets import Settings
# from params import Params


wlan = None
wlan_ap = None
wlan_sta = None


def get_connection():
    """
    Return a working WLAN instance or None
    """
    global wlan_ap
    del (wlan_ap)
    global wlan_sta
    wlan_sta = network.WLAN(network.STA_IF)
    # First check if there already any connection
    if wlan_sta.isconnected():
        return wlan_sta
    sets = Settings.load_settings()

    # Try to connect as station
    try:
        wlan_sta.active(True)
        if wlan_sta.isconnected():
            return wlan_sta
        print('\nTrying to connect to ' + sets.wifi_dict['sta_ssid'] +
              ' with password: ' + sets.wifi_dict['sta_password'])
        wlan_sta.connect(sets.wifi_dict['sta_ssid'],
                         sets.wifi_dict['sta_password'])
        for retry in range(80):
            if wlan_sta.isconnected():
                return wlan_sta
            time.sleep(0.15)
            print('.', end='')
        print('\nNot connected to: ' + sets.wifi_dict['sta_ssid'])
    except OSError as exc:
        print(exc)
    return None


def set_connection():
    """
    Start access point
    """
    global wlan_sta
    del (wlan_sta)
    global wlan_ap
    wlan_ap = network.WLAN(network.AP_IF)
    wlan_ap.active(True)
    sets = Settings.load_settings()
    wlan_ap.config(essid=sets.wifi_dict['ap_ssid'],
                   password=sets.wifi_dict['ap_password'],
                   authmode=3,  # WPA2
                   channel=int(sets.wifi_dict['ap_channel']),
                   )
    print('\nConnect to WiFi ' + sets.wifi_dict['ap_ssid'] +
          ' with password: ' + sets.wifi_dict['ap_password'])


def connectToWifiAndUpdate():
    time.sleep(1)
    print('Memory free', gc.mem_free())

    global wlan
    wlan = get_connection()
    if wlan is not None:
        network_config = wlan.ifconfig()
        print(
            f'\nIP: {network_config[0]} Subnet: {network_config[1]}\nGateway: {network_config[2]}DNS: {network_config[3]}')

    otaUpdater = OTAUpdater('https://github.com/PoniWai/pahu_pahu_akamai',
                            main_dir='app',
                            secrets_file=None)
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del (otaUpdater)
        gc.collect()


try:
    connectToWifiAndUpdate()
except OSError as exc:
    print('Update error:', exc)


def web_thread():
    while True:
        if wlan is None:
            set_connection()
            webfuncs.start_web('192.168.4.1')
        else:
            webfuncs.start_web(wlan.ifconfig()[0])


_thread.start_new_thread(web_thread, ())
