######################################################################
# Date: 2018/08/09
# file name: 2nd_assignment_main.py
# Purpose: this code has been generated for the 4WD moving
#         object to perform the project with ultra sensor
# this code is used for the student only
######################################################################


# =======================================================================
# import GPIO library and time module
# =======================================================================
import RPi.GPIO as GPIO
import time

# =======================================================================
# import ALL method in the SEN040134 Tracking Module
# =======================================================================
from SEN040134 import SEN040134_Tracking as Tracking_Sensor

# =======================================================================
# import ALL method in the TCS34725 RGB Module
# =======================================================================
from TCS34725 import TCS34725_RGB as RGB_Sensor

# =======================================================================
# import ALL method in the SR02 Ultrasonic Module
# =======================================================================
from SR02 import SR02_Ultrasonic as Ultrasonic_Sensor

# =======================================================================
# import ALL method in the rear/front Motor Module
# =======================================================================
import rear_wheels
import front_wheels

# =======================================================================
#  set GPIO warnings as false
# =======================================================================
GPIO.setwarnings(False)


# =======================================================================
# 2ND_ASSIGNMENT_CODE
# Complete the code to perform Second Assignment
# =======================================================================
def lineFollower_main():
    # implement the assignment code here
    pass


def moduleInitialize():
    try:
        # ================================================================
        # ULTRASONIC MODULE DRIVER INITIALIZE
        # ================================================================
        global distance_detector
        distance_detector = Ultrasonic_Sensor.Ultrasonic_Avoidance(35)

        # ================================================================
        # TRACKING MODULE DRIVER INITIALIZE
        # ================================================================
        global line_detector
        line_detector = Tracking_Sensor.SEN040134_Tracking([16, 18, 22, 40, 32])

        # ================================================================
        # RGB MODULE DRIVER INITIALIZE
        # ================================================================
        global color_getter
        color_getter = RGB_Sensor.TCS34725()

        # ================================================================
        # FRONT WHEEL DRIVER SETUP
        # ================================================================
        global front_steering
        front_steering = front_wheels.Front_Wheels(db='config')
        front_steering.ready()

        # ================================================================
        # REAR WHEEL DRIVER SETUP
        # ================================================================
        global rear_wheels_drive
        rear_wheels_drive = rear_wheels.Rear_Wheels(db='config')
        rear_wheels_drive.ready()

        # ================================================================
        # SET LIMIT OF TURNING DEGREE
        # ================================================================
        front_steering.turning_max = 35

        # ================================================================
        # SET FRONT WHEEL CENTOR ALLIGNMENT
        # ================================================================
        front_steering.turn_straight()

        # ================================================================
        # DISABLE RGB MODULE INTERRUPTION
        # ================================================================
        color_getter.set_interrupt(False)

    except:
        print("MODULE INITIALIZE ERROR")
        print("CONTACT TO Kookmin Univ. Teaching Assistant")


if __name__ == "__main__":
    try:
        moduleInitialize()
        lineFollwer_main()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        rear_wheels_drive.stop()
        front_steering.turn_straight()
