from machine import Pin


def anal_ps(mode):
    if mode is 'on':
        anal_pwr.off()  # feedback pulled low = start
    elif mode is 'off':
        anal_pwr.on()  # feedback pulled high = stop
    else:
        pass


# valves 1-7
v0 = Pin(13, Pin.OUT)
v1 = Pin(27, Pin.OUT)
v2 = Pin(12, Pin.OUT)  # boot fail if pulled high

# fans 1-5, humidifier 6
f0 = Pin(2, Pin.OUT)
f1 = Pin(4, Pin.OUT)
f2 = Pin(16, Pin.OUT)

# charge anal
anal_pwr = Pin(18, Pin.OUT)  # 1 = off, 0 = on
anal_pwr.on()  # feedback pulled high

charge_relay = Pin(19, Pin.OUT)
charge_relay.off()

# energy for plants
main_light = Pin(17, Pin.OUT)
morn_light = Pin(25, Pin.OUT)
even_light = Pin(26, Pin.OUT)
uv_light = Pin(32, Pin.OUT)

high_voltage = Pin(33, Pin.OUT)

# reserved
rez = Pin(5, Pin.OUT)
