import network
import machine
import utime

network.country("IN")
network.hostname("sgb-01")

led = machine.Pin("LED", machine.Pin.OUT)
led.toggle()
utime.sleep(0.5)
led.toggle()