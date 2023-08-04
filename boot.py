import webrepl

webrepl.start()
print('Preewa')


def connectToWifiAndUpdate():
    import time
    import machine
    import network
    import gc
    import wififuncs
    from ota_updater import OTAUpdater
    time.sleep(1)
    print('Memory free:', gc.mem_free())

    wlan = wififuncs.get_connection()
    if wlan is not None:
        network_config = wlan.ifconfig()
        print(f'\nIP: {network_config[0]} \
            Subnet: {network_config[1]} \
            Gateway: {network_config[2]} \
            DNS: {network_config[3]}')
        otaUpdater = OTAUpdater('https://github.com/PoniWai/pahu_pahu_akamai',
                                main_dir='app',
                                secrets_file=None)
        hasUpdated = otaUpdater.install_update_if_available()
        if hasUpdated:
            machine.reset()
        else:
            del (otaUpdater)
            gc.collect()


connectToWifiAndUpdate()
