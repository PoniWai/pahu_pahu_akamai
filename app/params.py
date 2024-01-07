import time

import esp32

import ds18x20
import onewire
import dht
from machine import Pin, ADC

from app.sets import Settings


class Params:

    # chip
    chip_tmp = -666

    # ds18b20
    air_ds_tmp = -666
    space_ds_tmp = -666

    # dht11
    brd_tmp = -666
    brd_hmd = -666

    # dht22
    air_tmp = -666
    air_hmd = -666

    # soil
    ec_upper = -666
    ec_lower = -666

    # power
    i_bat = -666
    v_bat = -666
    v_ps = -666

    def __init__(self,
                 chip_tmp,
                 air_ds_tmp,
                 space_ds_tmp,
                 brd_tmp,
                 brd_hmd,
                 air_tmp,
                 air_hmd,
                 ec_upper,
                 ec_lower,
                 i_bat,
                 v_bat,
                 v_ps,
                 ):
        self.chip_tmp = chip_tmp
        self.air_ds_tmp = air_ds_tmp
        self.space_ds_tmp = space_ds_tmp
        self.brd_tmp = brd_tmp
        self.brd_hmd = brd_hmd
        self.air_tmp = air_tmp
        self.air_hmd = air_hmd
        self.ec_upper = ec_upper
        self.ec_lower = ec_lower
        self.i_bat = i_bat
        self.v_bat = v_bat
        self.v_ps = v_ps

    def onw_read():
        roms = ds18b20.scan()
        ds18b20.convert_temp()
        time.sleep(0.75)
        temps = {}
        for rom in roms:
            temps[''.join('%02X' % i for i in iter(rom))
                  ] = ds18b20.read_temp(rom)
        return temps

    @staticmethod
    def digi_sensors():
        try:
            # chip Temperature
            Params.chip_tmp = (esp32.raw_temperature()-32)/1.8

            # DS18B20 Temperatures
            onewire_dict = Settings.load_settings().onewire_dict
            temps = Params.onw_read()

            if onewire_dict['air'] is not None:
                Params.air_ds_tmp = temps[onewire_dict['air']]
            if onewire_dict['space'] is not None:
                Params.space_ds_tmp = temps[onewire_dict['space']]

            # DHT11 sensor
            dht11.measure()
            Params.brd_tmp = dht11.temperature()
            Params.brd_hmd = dht11.humidity()

            # DHT22 sensor
            dht22.measure()
            Params.air_tmp = dht22.temperature()
            Params.air_hmd = dht22.humidity()
        except OSError as exc:
            print(exc)

    @ staticmethod
    def anal_sensors():
        try:
            channel_sw.on()
            time.sleep(1)
            Params.v_ps = voltage.read()
            Params.ec_lower = ec.read()
            channel_sw.off()
            time.sleep(1)
            Params.v_bat = voltage.read()
            Params.i_bat = current.read()
            Params.ec_upper = ec.read()
        except OSError as exc:
            print(exc)


# anal pins

current = ADC(Pin(34))
current.atten(ADC.ATTN_11DB)  # Full range: 3.3v

voltage = ADC(Pin(35))
voltage.atten(ADC.ATTN_11DB)  # Full range: 3.3v

ec = ADC(Pin(39))
ec.atten(ADC.ATTN_11DB)  # Full range: 3.3v

# digi sensors
ds18b20 = ds18x20.DS18X20(onewire.OneWire(Pin(23)))
dht11 = dht.DHT11(Pin(21))
dht22 = dht.DHT22(Pin(22))

channel_sw = Pin(14, Pin.OUT)  # pwm at boot
