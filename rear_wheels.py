import RPi.GPIO as GPIO
from PCA9685 import PCA9685 as p

# ===========================================================================
# Raspberry Pi pin 11, 12, 13 and 15 to realize the clockwise/counterclockwise
# rotation and forward and backward movements
# ===========================================================================
Motor0_A = 11  # GPIO 17
Motor0_B = 12  # GPIO 18
Motor1_A = 13  # GPIO 27
Motor1_B = 15  # GPIO 22

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
    print('speed is: ', (speed / 40))
    pwm.write(EN_M0, 0, speed)
    pwm.write(EN_M1, 0, speed)


def setup(busnum):
    global forward0, forward1, backward0, backward1, pwm

    if busnum is None:
        pwm = p.PWM()  # Initialize the servo controller.
    else:
        pwm = p.PWM(bus_number=busnum)  # Initialize the servo controller.

    pwm.frequency = 60
    forward0 = True
    forward1 = True

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)  # Number GPIOs by its physical location

    try:

        for line in open("config"):
            if line[0:8] == 'forward0':
                forward0 = True if line[11:-1] == 'True' else False
            if line[0:8] == 'forward1':
                forward1 = True if line[11:-1] == 'True' else False

    except IOError as e:
        print(e)

    backward0 = not forward0
    backward1 = not forward1

    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)  # Set all pins' mode as output


# ===========================================================================
# Control the DC motor to make it rotate clockwise, so the car will
# move forward.
# ===========================================================================


def left_motor(set_direction):
    if set_direction:
        GPIO.output(Motor0_A, GPIO.HIGH)
        GPIO.output(Motor0_B, GPIO.LOW)
    elif not set_direction:
        GPIO.output(Motor0_A, GPIO.LOW)
        GPIO.output(Motor0_B, GPIO.HIGH)
    else:
        print('Config Error')


def right_motor(set_direction):
    if set_direction:
        GPIO.output(Motor1_A, GPIO.LOW)
        GPIO.output(Motor1_B, GPIO.HIGH)
    elif not set_direction:
        GPIO.output(Motor1_A, GPIO.HIGH)
        GPIO.output(Motor1_B, GPIO.LOW)
    else:
        print('Config Error')


def forward():
    left_motor(forward0)
    right_motor(forward1)


def backward():
    left_motor(backward0)
    right_motor(backward1)


def forward_with_speed(speed):
    set_speed(speed)
    left_motor(forward0)
    right_motor(forward1)


def backward_with_speed(speed):
    set_speed(speed)
    left_motor(backward0)
    right_motor(backward1)


def stop():
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)
