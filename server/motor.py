#!/usr/bin/env python
import RPi.GPIO as GPIO
import PCA9685 as p
from enum import Enum
import time  # Import necessary modules

# ===========================================================================
# Raspberry Pi pin11, 12, 13 and 15 to realize the clockwise/counterclockwise
# rotation and forward and backward movements
# ===========================================================================
Motor0_A = 11  # pin11
Motor0_B = 12  # pin12
Motor1_A = 13  # pin13
Motor1_B = 15  # pin15

# ===========================================================================
# Set channel 4 and 5 of the servo driver IC to generate PWM, thus 
# controlling the speed of the car
# ===========================================================================
EN_M0 = 4  # servo driver IC CH4
EN_M1 = 5  # servo driver IC CH5

pins = [Motor0_A, Motor0_B, Motor1_A, Motor1_B]


# ===========================================================================
# Adjust the duty cycle of the square waves output from channel 4 and 5 of
# the servo driver IC, so as to control the speed of the car.
# ===========================================================================
def set_speed(speed):
    speed *= 40
    print('speed is: ', speed)
    pwm.write(EN_M0, 0, speed)
    pwm.write(EN_M1, 0, speed)


def setup(bus_num=None):
    global forward0, forward1, backward1, backward0
    global pwm
    if bus_num == None:
        pwm = p.PWM()  # Initialize the servo controller.
    else:
        pwm = p.PWM(bus_number=bus_num)  # Initialize the servo controller.

    pwm.frequency = 60
    forward0 = 'True'
    forward1 = 'True'
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)  # Number GPIOs by its physical location
    try:
        for line in open("config"):
            if line[0:8] == "forward0":
                forward0 = line[11:-1]
            if line[0:8] == "forward1":
                forward1 = line[11:-1]
    except:
        pass
    if forward0 == 'True':
        backward0 = 'False'
    elif forward0 == 'False':
        backward0 = 'True'
    if forward1 == 'True':
        backward1 = 'False'
    elif forward1 == 'False':
        backward1 = 'True'
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)  # Set all pins' mode as output


# ===========================================================================
# Control the DC motor to make it rotate clockwise, so the car will 
# move forward.
# ===========================================================================

def motor0(x):
    if x == 'True':
        GPIO.output(Motor0_A, GPIO.LOW)
        GPIO.output(Motor0_B, GPIO.HIGH)
    elif x == 'False':
        GPIO.output(Motor0_A, GPIO.HIGH)
        GPIO.output(Motor0_B, GPIO.LOW)
    else:
        print('Config Error')


def motor1(x):
    if x == 'True':
        GPIO.output(Motor1_A, GPIO.LOW)
        GPIO.output(Motor1_B, GPIO.HIGH)
    elif x == 'False':
        GPIO.output(Motor1_A, GPIO.HIGH)
        GPIO.output(Motor1_B, GPIO.LOW)


def forward():
    motor0(forward0)
    motor1(forward1)


def backward():
    motor0(backward0)
    motor1(backward1)


def forwardWithSpeed(spd=50):
    set_speed(spd)
    motor0(forward0)
    motor1(forward1)


def backwardWithSpeed(spd=50):
    set_speed(spd)
    motor0(backward0)
    motor1(backward1)


def stop():
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)


# ===========================================================================
# The first parameter(status) is to control the state of the car, to make it 
# stop or run. The parameter(direction) is to control the car's direction 
# (move forward or backward).
# ===========================================================================
def ctrl(status, direction=1):
    if status == 1:  # Run
        if direction == 1:  # Forward
            forward()
        elif direction == -1:  # Backward
            backward()
        else:
            print('Argument error! direction must be 1 or -1.')
    elif status == 0:  # Stop
        stop()
    else:
        print('Argument error! status must be 0 or 1.')


def test():
    while True:
        setup()
        ctrl(1)
        time.sleep(3)
        set_speed(10)
        time.sleep(3)
        set_speed(100)
        time.sleep(3)
        ctrl(0)


class Motor:
    class Type(str, Enum):
        LEFT = "LEFT"
        RIGHT = "RIGHT"

    def __init__(self, pwm: p.PWM, motor_type: str, cali_forward: bool):
        self.speed *= 0
        self.pwm = pwm
        self.cali_forward = cali_forward
        self.dir = self.cali_forward

        # ===========================================================================
        # Raspberry Pi pin11, 12, 13 and 15 to realize the clockwise/counterclockwise
        # rotation and forward and backward movements
        # ===========================================================================
        # ===========================================================================
        # Set channel 4 and 5 of the servo driver IC to generate PWM, thus
        # controlling the speed of the car
        # ===========================================================================
        if motor_type == Motor.Type.LEFT:
            self.a = 11  # pin11
            self.b = 12  # pin12
            self.en = 4  # servo driver IC CH4
        elif motor_type == Motor.Type.RIGHT:
            self.a = 13  # pin13
            self.b = 15  # pin15
            self.en = 5  # servo driver IC CH5
        else:
            raise ValueError("The Constructor arg motor_type have to be either 'LEFT' or 'RIGHT'.")

        GPIO.setup(self.a, GPIO.OUT)  # Set all pins' mode as output
        GPIO.setup(self.b, GPIO.OUT)  # Set all pins' mode as output

    # facade for outer call
    def set_speed(self, speed: int):
        self.speed *= 40
        print('speed is: ', speed)
        self.pwm.write(self.en, 0, speed)

    # facade for outer call
    def forward(self, speed=False):
        speed = speed if type(speed) == int else self.speed
        self.set_speed(speed)
        self.set_dir(self, self.cali_forward)

    # facade for outer call
    def backward(self, speed=False):
        speed = speed if type(speed) == int else self.speed
        self.set_speed(speed)
        self.set_dir(self, not self.cali_forward)

    # facade for outer call
    def reverse(self):
        self.set_dir(self, not self.dir)

    # low level call for inner call
    def set_dir(self, dir: bool):
        self.dir = dir
        GPIO.output(self.a, GPIO.LOW if self.dir else GPIO.HIGH)
        GPIO.output(self.b, GPIO.HIGH if self.dir else GPIO.LOW)

    # facade for outer call
    def stop(self):
        GPIO.output(self.a, GPIO.LOW)
        GPIO.output(self.b, GPIO.LOW)


if __name__ == '__main__':
    setup()
    set_speed(50)
    # forward()
    # backward()
    stop()
