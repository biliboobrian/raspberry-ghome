from yeelight import Bulb

def turn_on_screen_light():
    bulb = Bulb("192.168.1.80")
    bulb.turn_on()

def turn_off_screen_light():
    bulb = Bulb("192.168.1.80")
    bulb.turn_off()

def turn_on_salon_light():
    bulb = Bulb("192.168.1.81")
    bulb.turn_on()
    bulb = Bulb("192.168.1.82")
    bulb.turn_on()

def turn_off_salon_light():
    bulb = Bulb("192.168.1.81")
    bulb.turn_off()
    bulb = Bulb("192.168.1.82")
    bulb.turn_off()

def turn_on_cuisine_light():
    bulb = Bulb("192.168.1.83")
    bulb.turn_on()
    bulb = Bulb("192.168.1.84")
    bulb.turn_on()

def turn_off_cuisine_light():
    bulb = Bulb("192.168.1.83")
    bulb.turn_off()
    bulb = Bulb("192.168.1.84")
    bulb.turn_off()