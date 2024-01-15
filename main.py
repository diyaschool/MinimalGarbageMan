import machine
import time
import functions
from micropyserver import MicroPyServer
import network
import json

#wlan = network.WLAN(network.STA_IF)
#wlan.active(True)
#print("Connecting to Wifi...")
#wlan.connect("Network_24", "Internet@localhost")
#while True:
#    if wlan.status() == 3:
#        break
#    elif wlan.status() < 0:
#        raise OSError("Unable to connect to wifi!")
#    time.sleep(0.5)
#print("Connected!")

SSID = "SYNERGY-MGM-01"
PASSWORD = "Synergy_2024@MGM-01"

wlan = network.WLAN(network.AP_IF)
wlan.config(essid=SSID, password=PASSWORD)
wlan.active(True)

while wlan.active() == False:
    pass

print(wlan.ifconfig())

THRESHOLD_DISTANCE = 10

lid_servo = functions.Servo(22)
ultrasen_1 = functions.UltrasonicSensor(trig_pin=3, echo_pin=2)
ultrasen_2 = functions.UltrasonicSensor(trig_pin=7, echo_pin=6)

operation_status = {"is_lid_open": False, "last_opened_time": 0, "override_sensor": False}
op_timer2 = machine.Timer()

def close_lid(_):
    global operation_status
    operation_status["is_lid_open"] = False
    servo.move(0)

def operate_lid(_):
    global operation_status
    if operation_status["override_sensor"] == True:
        return
    dist = ultrasen_1.get_reading()
    if operation_status["is_lid_open"] == False:
        if dist <= THRESHOLD_DISTANCE:
            servo.move(90)
            operation_status["is_lid_open"] = True
            operation_status["last_opened_time"] = time.time()
    if operation_status["is_lid_open"] == True:
        if dist > THRESHOLD_DISTANCE:
            timer = machine.Timer(mode=0, period=5000, callback=close_lid)

def query_status(request):
    reading = ultrasen_2.get_reading()
    status = {"is_lid_open": operation_status["is_lid_open"], "last_opened_time": operation_status["last_opened_time"], "level_reading": reading}
    server.send("HTTP/1.0 200 OK\r\n\r\n")
    server.send(json.dumps(status))

operation_timer = machine.Timer()
operation_timer.init(mode=1, period=100, callback=operate_lid)
server = MicroPyServer()
server.add_route("/query_status", query_status, method="PUT")
server.start()