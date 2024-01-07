from machine import Pin


anal_pwr = Pin(18, Pin.OUT)  # 1 = off, 0 = on
anal_pwr.on()  # feedback pulled high

charge_relay = Pin(19, Pin.OUT)
charge_relay.off()
