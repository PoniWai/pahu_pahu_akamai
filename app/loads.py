from machine import Pin


def anal_ps(mode):
    if mode is 'on':
        anal_pwr.off()  # feedback pulled low = start
    elif mode is 'off':
        anal_pwr.on()  # feedback pulled high = stop
    else:
        pass


v0 = Pin(13, Pin.OUT)
v1 = Pin(27, Pin.OUT)
v2 = Pin(12, Pin.OUT)  # boot fail if pulled high
# board_cooler = v0
# black_space = v1 (most powerful)
# white_space = v0 & v1 (least powerful)
# red_valve = v2
# green_valve = v0 & v2
# black_valve = v1 & v2
# white_valve = v0 & v1 & v2


f0 = Pin(2, Pin.OUT)
f1 = Pin(4, Pin.OUT)
f2 = Pin(16, Pin.OUT)
# green_space = f0 (mid powerful)
# cool_crc = f1
# cool_crc2 =f0 & f1
# cool_crc3 = f2
# cool_top = f0 & f2
# humidifier = f1 & f2


# charge anal
anal_pwr = Pin(18, Pin.OUT)  # 1 = off, 0 = on
anal_pwr.on()  # feedback pulled high

charge_relay = Pin(19, Pin.OUT)
charge_relay.off()

# food for plants
main_light = Pin(17, Pin.OUT)
blue_light = Pin(26, Pin.OUT)
black_light = Pin(25, Pin.OUT)

pump = Pin(32, Pin.OUT)

high_voltage = Pin(33, Pin.OUT)

# reserved
rez = Pin(5, Pin.OUT)
rez2 = Pin(15, Pin.OUT)  # pwm at boot
