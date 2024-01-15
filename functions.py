import machine
import time

class Servo:
    __servo_pwm_freq = 50
    __min_u16_duty = 1640 - 500 # offset for correction
    __max_u16_duty = 7864 - 0  # offset for correction
    min_angle = 0
    max_angle = 180
    current_angle = 0.001

    def __init__(self, pin):
        self.current_angle = -0.001
        self.__angle_conversion_factor = (self.__max_u16_duty - self.__min_u16_duty) / (self.max_angle - self.min_angle)
        self.__motor = machine.PWM(machine.Pin(pin))
        self.__motor.freq(self.__servo_pwm_freq)
    def _angle_to_u16_duty(self, angle):
        return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u16_duty
    def move(self, angle):
        # round to 2 decimal places, so we have a chance of reducing unwanted servo adjustments
        angle = round(angle, 2)
        # do we need to move?
        if angle == self.current_angle:
            return
        self.current_angle = angle
        # calculate the new duty cycle and move the motor
        duty_u16 = self._angle_to_u16_duty(angle)
        self.__motor.duty_u16(duty_u16)

class UltrasonicSensor:
    def __init__(self, trig_pin=3, echo_pin=2):
        self.trigger = machine.Pin(trig_pin, machine.Pin.OUT)
        self.echo = machine.Pin(echo_pin, machine.Pin.IN)
    def get_reading(self):
        self.trigger.low()
        time.sleep_us(2)
        self.trigger.high()
        time.sleep_us(5)
        self.trigger.low()
        while self.echo.value() == 0:
            signaloff = time.ticks_us()
        while self.echo.value() == 1:
            signalon = time.ticks_us()
        timepassed = signalon - signaloff
        distance = (timepassed * 0.0343) / 2
        return distance
