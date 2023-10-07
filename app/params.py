import time

import ds18x20
import onewire
import dht
from machine import Pin, ADC

from app.loads import anal_ps
from sets import Settings
        

class Params:
    #ds18b20
    solution_temp = -666
    air_temp = -666
    space_temp = -666
    #dht11
    brd_temp = -666
    brd_hmd = -666
    #dht22
    air_temp = -666
    air_hmd = -666
    
    pH = -666
    ec_upper = -666
    ec_lower = -666
    v_bat = -666
    v_ps = -666
    i_bat = -666

    # def __init__(self,
    #              solution_temp,
    #              air_temp,
    #              space_temp,
    #              brd_dht_temp,
    #              humidity,
    #              brd_bmp_temp,
    #              pressure,
    #              ):
    #     self.solution_temp = solution_temp
    #     self.air_temp = air_temp
    #     self.space_temp = space_temp
    #     self.brd_dht_temp = brd_dht_temp
    #     self.humidity = humidity
    #     self.brd_bmp_temp = brd_bmp_temp
    #     self.pressure = pressure

    def onw_read():
        roms = ds18b20.scan()
        ds18b20.convert_temp()
        time.sleep(0.75)
        temps = {}
        for rom in roms:
            temps[''.join('%02X' % i for i in iter(rom))] = ds18b20.read_temp(rom)
        return temps

    @staticmethod
    def digi_sensors():
        try:
            # DS18B20 Temperatures
            onewire_dict = Settings.load_settings().onewire_dict
            temps = Params.onw_read()
            if onewire_dict['miska'] is not None:
                Params.solution_temp = temps[onewire_dict['miska']]
            if onewire_dict['air'] is not None:
                Params.air_temp = temps[onewire_dict['air']]
            if onewire_dict['space'] is not None:
                Params.space_temp = temps[onewire_dict['space']]
            channel_sw.off()
            # DHT11 sensor
            dht11.measure()
            Params.brd_dht_temp = dht11.temperature()
            Params.humidity = dht11.humidity()
            # DHT22 sensor
            dht22.measure()
            Params.brd_bmp_temp = bmp085.temperature
            Params.pressure = bmp085.pressure
        except OSError as e:
            print(e)

    @staticmethod
    def anal_sensors(heat=False):
        try:
            anal_ps('on')
            channel_sw.on()
            time.sleep(1)
            if heat:
                co2_htr.on()
            Params.v_ps = voltage.read()
            Params.ec_lower = ec.read()
            channel_sw.off()
            time.sleep(1)
            Params.v_bat = voltage.read()
            Params.ec_upper = ec.read()
            Params.pH = pH.read()
            if heat:
                time.sleep(20)
                Params.co2 = co2.read()
            co2_htr.off()
            anal_ps('off')
        except OSError as e:
            print(e)


# anal pins

current = ADC(Pin(34))
current.atten(ADC.ATTN_11DB)  # Full range: 3.3v

voltage = ADC(Pin(35))
voltage.atten(ADC.ATTN_11DB)  # Full range: 3.3v

ec = ADC(Pin(39))
ec.atten(ADC.ATTN_11DB)  # Full range: 3.3v

pH = ADC(Pin(36))
pH.atten(ADC.ATTN_11DB)  # Full range: 3.3v

channel_sw = Pin(14, Pin.OUT)  # pwm at boot

# digi sensors
ds18b20 = ds18x20.DS18X20(onewire.OneWire(Pin(23)))  # pwm at boot, boot pin
dht11 = dht.DHT11(Pin(21))
dht22 = dht.DHT22(Pin(22))
