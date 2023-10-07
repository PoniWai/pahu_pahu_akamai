import network
import socket
import ure
import time
from app.sets import Settings


wlan_ap = None
wlan_sta = None

server_socket = None


def do_connect(ssid, password):
    # Try to connect as station
    try:
        wlan_sta.active(True)
        connected = wlan_sta.isconnected()
        if connected:
            return None
        print(f'\nTrying to connect to {ssid} with password:{password}')
        wlan_sta.connect(ssid, password)
        for retry in range(100):
            if connected:
                break
            time.sleep(0.15)
            print('.', end='')
    except OSError as exc:
        print('Connection error:', exc)

    if connected:
        print('\nConnected. Network config: ', wlan_sta.ifconfig())
    else:
        print('\nFailed. Not Connected to: ' + ssid)
    return connected


def set_connection():
    """
    Start access point
    """
    global wlan_sta
    wlan_sta = None
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


def get_connection():
    """return a working WLAN(STA_IF) instance or None"""
    global wlan_ap
    wlan_ap = None
    global wlan_sta
    wlan_sta = network.WLAN(network.STA_IF)

    sets = Settings.load_settings()

    # First check if there already is any connection:
    if wlan_sta.isconnected():
        return wlan_sta
    connected = False

    try:
        # ESP connecting to WiFi takes time, wait a bit and try again:
        time.sleep(3)
        if wlan_sta.isconnected():
            return wlan_sta

        # Read known network profiles from file
        profiles = sets.wifi_dict['sta_dict']

        # Search WiFis in range
        wlan_sta.active(True)
        networks = wlan_sta.scan()

        AUTHMODE = {0: "open", 1: "WEP", 2: "WPA-PSK",
                    3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}
        for ssid, bssid, channel, rssi, authmode, hidden in sorted(networks, key=lambda x: x[3], reverse=True):
            ssid = ssid.decode('utf-8')
            encrypted = authmode > 0
            print("ssid: %s chan: %d rssi: %d authmode: %s" %
                  (ssid, channel, rssi, AUTHMODE.get(authmode, '?')))
            if encrypted:
                if ssid in profiles:
                    password = profiles[ssid]
                    connected = do_connect(ssid, password)
                else:
                    print("skipping unknown encrypted network")
            else:  # open
                connected = do_connect(ssid, None)
            if connected:
                break
    except OSError as e:
        print(f"Exception: {e}")

    return wlan_sta if connected else None
