######################################################################
# Date: 2018/08/09
# file name: professor_assignment_main.py
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

forward_speed = 35
backward_speed = 32
turning_angle = 35

delay = 0.0005

def first_main():
    # front_wheels center allignment
    front_steering.turn_straight()

    # forward-assignment
    rear_wheels_drive.forward_with_speed(30)
    time.sleep(2) #30-2s
    rear_wheels_drive.forward_with_speed(60)
    time.sleep(2) #60-2s
    rear_wheels_drive.forward_with_speed(90)
    time.sleep(2) #90-2s

    # backward-assignment
    rear_wheels_drive.backward_with_speed(30)
    time.sleep(2) #30-2s
    rear_wheels_drive.backward_with_speed(60)
    time.sleep(2) #60-2s
    rear_wheels_drive.backward_with_speed(90)
    time.sleep(2) #90-2s

    # stop
    rear_wheels_drive.stop()

def lineFollower_main():
    global turning_angle

    a_step = 5
    b_step = 10
    c_step = 30
    d_step = 45

    rear_wheels_drive.forward_with_speed(forward_speed)

    while True:
        lt_status_now = line_detector.read_digital()

        # Angle calculate
        if lt_status_now == [0, 0, 1, 0, 0] or lt_status_now == [0, 1, 1, 1, 0]:
            step = 0
        elif lt_status_now == [0, 1, 1, 0, 0] or lt_status_now == [0, 0, 1, 1, 0]:
            step = a_step
        elif lt_status_now == [0, 1, 0, 0, 0] or lt_status_now == [0, 0, 0, 1, 0]:
            step = b_step
        elif lt_status_now == [1, 1, 0, 0, 0] or lt_status_now == [0, 0, 0, 1, 1]:
            step = c_step
        elif lt_status_now == [1, 0, 0, 0, 0] or lt_status_now == [0, 0, 0, 0, 1]:
            step = d_step
        else:
            step = 0

        # Direction calculate
        if lt_status_now == [0, 0, 1, 0, 0]:
            front_steering.turn(90)
        # turn right
        elif sum(lt_status_now[:3]) > sum(lt_status_now[2:]):
            turning_angle = int(90 - step)
        # turn left
        elif sum(lt_status_now[:3]) < sum(lt_status_now[2:]):
            turning_angle = int(90 + step)
        elif lt_status_now == [0, 0, 0, 0, 0]:
            # rgb sensor check
            rear_wheels_drive.forward_with_speed(forward_speed)
            time.sleep(0.1)
            rear_wheels_drive.stop()
            if line_detector.read_digital() == [0, 0, 0, 0, 0]:
                time.sleep(0.05)
                rear_wheels_drive.stop()
                store_angle = turning_angle
                turning_angle = 120 if turning_angle < 90 else 60
                front_steering.turn(turning_angle)
                time.sleep(0.1)
                while sum(line_detector.read_digital()) <= 1:
                    rear_wheels_drive.backward_with_speed(backward_speed)
                    time.sleep(0.1)
                rear_wheels_drive.stop()
                turning_angle = store_angle
                front_steering.turn(turning_angle)
                time.sleep(0.1)
                rear_wheels_drive.forward_with_speed(forward_speed)
                time.sleep(0.4)
            else:
                rear_wheels_drive.forward_with_speed(forward_speed)
                print("COLOR DETECT")

        front_steering.turn(turning_angle)
        time.sleep(delay)

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
        # ===============================================================
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
        #first_main()
        lineFollower_main()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        rear_wheels_drive.stop()
        front_steering.turn_straight()
