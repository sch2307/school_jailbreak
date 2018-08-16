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


class Car(object):

    def __init__(self):
        self.moduleInitialize()

        # Variable Setup
        self.forward_speed = 35
        self.backward_speed = 32

    def drive_parking(self):
        self.front_steering.turn_straight()
        self.rear_wheels_drive.stop()

    def first_main(self):
        # front_wheels center allignment
        self.front_steering.turn_straight()

        # forward-assignment
        self.rear_wheels_drive.forward_with_speed(30)
        time.sleep(2) #30-2s
        self.rear_wheels_drive.forward_with_speed(60)
        time.sleep(2) #60-2s
        self.rear_wheels_drive.forward_with_speed(90)
        time.sleep(2) #90-2s

        # backward-assignment
        self.rear_wheels_drive.backward_with_speed(30)
        time.sleep(2) #30-2s
        self.rear_wheels_drive.backward_with_speed(60)
        time.sleep(2) #60-2s
        self.rear_wheels_drive.backward_with_speed(90)
        time.sleep(2) #90-2s

        # stop
        self.rear_wheels_drive.stop()

    def lineFollower_main(self):
        # lineFollower Setup
        turning_angle = 35
        delay = 0.0005

        a_step = 5
        b_step = 10
        c_step = 30
        d_step = 45

        self.rear_wheels_drive.forward_with_speed(self.forward_speed)

        while True:
            lt_status_now = self.line_detector.read_digital()

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
                self.front_steering.turn(90)
            # turn right
            elif sum(lt_status_now[:3]) > sum(lt_status_now[2:]):
                turning_angle = int(90 - step)
            # turn left
            elif sum(lt_status_now[:3]) < sum(lt_status_now[2:]):
                turning_angle = int(90 + step)
            elif lt_status_now == [0, 0, 0, 0, 0]:
                # rgb sensor check
                self.rear_wheels_drive.forward_with_speed(self.forward_speed)
                time.sleep(0.1)
                self.rear_wheels_drive.stop()
                if self.line_detector.read_digital() == [0, 0, 0, 0, 0]:
                    time.sleep(0.05)
                    self.rear_wheels_drive.stop()
                    store_angle = turning_angle
                    turning_angle = 120 if turning_angle < 90 else 60
                    self.front_steering.turn(turning_angle)
                    time.sleep(0.1)
                    while sum(self.line_detector.read_digital()) <= 1:
                        self.rear_wheels_drive.backward_with_speed(self.backward_speed)
                        time.sleep(0.1)
                    self.rear_wheels_drive.stop()
                    turning_angle = store_angle
                    self.front_steering.turn(turning_angle)
                    time.sleep(0.1)
                    self.rear_wheels_drive.forward_with_speed(self.forward_speed)
                    time.sleep(0.4)
                else:
                    self.rear_wheels_drive.forward_with_speed(self.forward_speed)
                    print("COLOR DETECT")

            self.front_steering.turn(turning_angle)
            time.sleep(delay)

    def moduleInitialize(self):
        try:
            # ================================================================
            # ULTRASONIC MODULE DRIVER INITIALIZE
            # ================================================================
            self.distance_detector = Ultrasonic_Sensor.Ultrasonic_Avoidance(35)

            # ================================================================
            # TRACKING MODULE DRIVER INITIALIZE
            # ================================================================
            self.line_detector = Tracking_Sensor.SEN040134_Tracking([16, 18, 22, 40, 32])

            # ================================================================
            # RGB MODULE DRIVER INITIALIZE
            # ================================================================
            self.color_getter = RGB_Sensor.TCS34725()

            # ================================================================
            # FRONT WHEEL DRIVER SETUP
            # ================================================================
            self.front_steering = front_wheels.Front_Wheels(db='config')
            self.front_steering.ready()

            # ================================================================
            # REAR WHEEL DRIVER SETUP
            # ================================================================
            self.rear_wheels_drive = rear_wheels.Rear_Wheels(db='config')
            self.rear_wheels_drive.ready()

            # ================================================================
            # SET LIMIT OF TURNING DEGREE
            # ===============================================================
            self.front_steering.turning_max = 35

            # ================================================================
            # SET FRONT WHEEL CENTOR ALLIGNMENT
            # ================================================================
            self.front_steering.turn_straight()

            # ================================================================
            # DISABLE RGB MODULE INTERRUPTION
            # ================================================================
            self.color_getter.set_interrupt(False)

        except:
            print("MODULE INITIALIZE ERROR")
            print("CONTACT TO Kookmin Univ. Teaching Assistant")


if __name__ == "__main__":
    try:
        car = Car()
        car.first_main() #1st_assignment
        car.lineFollower_main() #2nd-3rd assignment

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        car.drive_parking()
