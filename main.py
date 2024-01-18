import machine
import time
import functions
from micropyserver import MicroPyServer
import network
import json

SSID = "SYNERGY-MGM-01"
PASSWORD = "Synergy_2024@MGM-01"

CLOSED_SERVO_ANGLE = 15
OPEN_SERVO_ANGLE = 90

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

lid_timer = machine.Timer()
lid_timer_enabled = False

def close_lid(_):
    global operation_status
    global lid_timer_enabled
    operation_status["is_lid_open"] = False
    lid_servo.move(CLOSED_SERVO_ANGLE)
    lid_timer_enabled = False
    print("lid closed")

def operate_lid(_):
    global operation_status
    global lid_timer
    global lid_timer_enabled
    if operation_status["override_sensor"] == True:
        return
    dist = ultrasen_1.get_reading()
    if dist <= THRESHOLD_DISTANCE:
        lid_servo.move(OPEN_SERVO_ANGLE)
        operation_status["is_lid_open"] = True
        operation_status["last_opened_time"] = time.time()
        lid_timer.deinit()
        lid_timer_enabled = False
        print("lid opened")
    elif dist > THRESHOLD_DISTANCE:
        if operation_status["is_lid_open"] == True:
            if lid_timer_enabled == False:
                lid_timer = machine.Timer(mode=0, period=5000, callback=close_lid)
                lid_timer_enabled = True

def query_status(request):
    reading = ultrasen_2.get_reading()
    status = {"is_lid_open": operation_status["is_lid_open"], "last_opened_time": operation_status["last_opened_time"], "level_reading": reading}
    server.send("HTTP/1.0 200 OK\r\n\r\n")
    server.send(json.dumps(status))

close_lid(None)
operation_timer = machine.Timer()
operation_timer.init(mode=1, period=100, callback=operate_lid)
server = MicroPyServer()
server.add_route("/query_status", query_status, method="PUT")
server.start()