from app.sets import Settings

import time
import network

wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)


def get_connection():
    """
    Return a working WLAN instance or None
    """

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
    wlan_ap.active(True)
    sets = Settings.load_settings()
    wlan_ap.config(essid=sets.wifi_dict['ap_ssid'],
                   password=sets.wifi_dict['ap_password'],
                   authmode=3,  # WPA2
                   channel=int(sets.wifi_dict['ap_channel']),
                   )
    print('\nConnect to WiFi ' + sets.wifi_dict['ap_ssid'] +
          ' with password: ' + sets.wifi_dict['ap_password'])
