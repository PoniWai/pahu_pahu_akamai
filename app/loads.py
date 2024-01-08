from machine import Pin
from app.params import Params


def on_cool_brd():
    v1.off()
    v2.off()
    v0.on()


def off_cool_brd():
    v0.off()
    v1.off()
    v2.off()


def on_cool_top():
    f1.off()
    f0.on()
    f2.on()


def off_cool_top():
    f0.off()
    f1.off()
    f2.off()


def on_light():
    v2.off()
    v0.on()
    v1.on()
    main_light.on()
    central_light.on()


def off_light():
    v0.off()
    v1.off()
    v2.off()
    central_light.off()
    main_light.off()


def check_top_tmp():

    if Params.space_ds_tmp > 40:
        on_cool_top()
    elif Params.space_ds_tmp < 35:
        off_cool_top()


def check_brd():
    if Params.brd_tmp > 40 or Params.brd_hmd > 70 or Params.chip_tmp > 60:
        on_cool_brd()
    elif Params.brd_tmp < 35 and Params.brd_hmd < 50 and Params.chip_tmp < 55:
        off_cool_brd()
        on_light()


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


# food for plants
main_light = Pin(17, Pin.OUT)
central_light = Pin(33, Pin.OUT)
# blue_light = Pin(26, Pin.OUT)
# black_light = Pin(25, Pin.OUT)

# pump = Pin(32, Pin.OUT)

cool_out = Pin(26, Pin.OUT)

# reserved
# rez = Pin(5, Pin.OUT)

rez2 = Pin(15, Pin.OUT)  # pwm at boot
rez2.off()  # turn off current source
