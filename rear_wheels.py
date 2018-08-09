#!/usr/bin/env python
import RPi.GPIO as GPIO
from PCA9685 import PCA9685 as p

# ===========================================================================
# Raspberry Pi pin11, 12, 13 and 15 to realize the clockwise/counterclockwise
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
def setSpeed(speed):
    speed *= 40
    print('speed is: ', speed)
    pwm.write(EN_M0, 0, speed)
    pwm.write(EN_M1, 0, speed)


def setup(busnum=None):
    global forward0, forward1, backward0, backward1, pwm

    if busnum == None:
        pwm = p.PWM()  # Initialize the servo controller.
    else:
        pwm = p.PWM(bus_number=busnum)  # Initialize the servo controller.

    pwm.frequency = 60
    forward0 = True
    forward1 = False
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)  # Number GPIOs by its physical location
    try:
        for line in open("config"):
            if line[0:8] == "forward0":
                leftMotorDirection = True if line[11:-1] == "True" else False
            if line[0:8] == "forward1":
                rightMotorDirection = True if line[11:-1] == "True" else False
                forward0 = line[11:-1]
            if line[0:8] == "forward1":
                forward1 = line[11:-1]
    except:
        pass
    if forward0:
        backward0 = False
    else:
        backward0 = True
    if forward1:
        backward1 = False
    else:
        backward1 = True
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)  # Set all pins' mode as output


# ===========================================================================
# Control the DC motor to make it rotate clockwise, so the car will 
# move forward.
# ===========================================================================

def left_motor(x):
    if x:
        GPIO.output(Motor0_A, GPIO.HIGH)
        GPIO.output(Motor0_B, GPIO.LOW)
    elif not x:
        GPIO.output(Motor0_A, GPIO.LOW)
        GPIO.output(Motor0_B, GPIO.HIGH)
    else:
        print('Config Error')


def right_motor(x):
    if x:
        GPIO.output(Motor1_A, GPIO.LOW)
        GPIO.output(Motor1_B, GPIO.HIGH)
    elif not x:
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


def forwardWithSpeed(spd=50):
    setSpeed(spd)
    left_motor(forward0)
    right_motor(forward1)


def backwardWithSpeed(spd=50):
    setSpeed(spd)
    left_motor(backward0)
    right_motor(backward1)


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
