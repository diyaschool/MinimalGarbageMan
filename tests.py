import machine
import time
import functions

def main():
    servo = functions.Servo(22)
    while True:
        servo.move(90)
        time.sleep(5)
        servo.move(0)
        time.sleep(5)

def main2():
    ultrasen_1 = functions.UltrasonicSensor(trig_pin=3, echo_pin=2)
    while True:
        dist = ultrasen_1.get_reading()
        print(dist)
        utime.sleep(0.25)

def main3():
    ultrasen_1 = functions.UltrasonicSensor(trig_pin=3, echo_pin=2)
    while True:
        dist = ultrasen_1.get_reading()
        if dist <= THRESHOLD_DISTANCE:
            print("detected!")
        utime.sleep(0.1)

def main4():
    ultrasen_1 = functions.UltrasonicSensor(trig_pin=3, echo_pin=2)
    servo = functions.Servo(22)
    servo.move(0)
    while True:
        dist = ultrasen_1.get_reading()
        if dist <= THRESHOLD_DISTANCE:
            servo.move(90)
            time.sleep(5)
        if dist > THRESHOLD_DISTANCE:
            servo.move(0)
        utime.sleep(0.05)
