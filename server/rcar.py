import motor
import model
import RPi.GPIO as GPIO
import PCA9685 as p
import time


class RCar:
    def __init__(self):
        self.config = model.Configurer()

        if self.config.bus_num == None:
            pwm = p.PWM()  # Initialize the servo controller.
        else:
            pwm = p.PWM(bus_number=self.config.bus_num)  # Initialize the servo controller.

        # pwm.frequency = 60
        # pwm.frequency(60)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)  # Number GPIOs by its physical location

        self.left_motor = motor.Motor(pwm, motor.Motor.Type.LEFT, self.config.forward_0)
        self.right_motor = motor.Motor(pwm, motor.Motor.Type.RIGHT, self.config.forward_1)

    def forward(self, speed: int):
        self.left_motor.forward(speed)
        self.right_motor.forward(speed)

    def backward(self, speed: int):
        self.left_motor.backward(speed)
        self.right_motor.backward(speed)

    # low level : needs left motor speed and right motor's speed to turn
    # stops after turning
    def turn(self, angle: int, **speeds):
        left_speed = speeds["left"]
        right_speed = speeds["right"]

        if left_speed > 0:
            self.left_motor.forward(left_speed)
        else:
            self.left_motor.backward(abs(left_speed))

        if right_speed > 0:
            self.left_motor.forward(right_speed)
        else:
            self.left_motor.backward(abs(right_speed))

        def calc_trn_dur(angle, relative_wheel_speed):
            k = 0.01
            c = 0.1
            turning_duration = k * angle / (c * relative_wheel_speed)
            return turning_duration

        time.sleep(calc_trn_dur(angle, abs(left_speed - right_speed)))
        self.stop()

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()
