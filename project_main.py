######################################################################
### Date: 2018/07/12
### file name: project_main.py
### Purpose: this code has been generated for the 4WD moving
###         object to perform the project with ultra sensor
### this code is used for the student only
######################################################################

# =======================================================================
# import GPIO library and time module 
# =======================================================================
import RPi.GPIO as GPIO
import time

# =======================================================================
#  set GPIO warnings as false 
# =======================================================================
GPIO.setwarnings(False)

# =======================================================================
# import getDistance() method in the ultraModule 
# =======================================================================
from SR02 import SR02_Ultrasonic

# =======================================================================
# import ALL method in the rear/front Motor Module 
# =======================================================================
import rear_wheels
import front_wheels

# =======================================================================    
# setup and initilaize the left motor and right motor
# =======================================================================
forward_speed = 80
backward_speed = 70
turning_angle = 40

calibrate = False
max_off_track_count = 40

delay = 0.0005

def straight_run():
    while True:
        rear_wheels.forwardWithSpeed(70)
        FR.turn_straight()

def setup():
    if calibrate:
        cali()

def lineFollwer_main():
    global turning_angle
    off_track_count = 0

    a_step = 3
    b_step = 10
    c_step = 30
    d_step = 45

    rear_wheels.forwardWithSpeed(forward_speed)

    while True:
        lt_status_now = []
        # Angle calculate
        if lt_status_now == [0, 0, 1, 0, 0]:
            step = 0
        elif lt_status_now == [0, 1, 1, 0, 0] or lt_status_now == [0, 0, 1, 1, 0]:
            step = a_step
        elif lt_status_now == [0, 1, 0, 0, 0] or lt_status_now == [0, 0, 0, 1, 0]:
            step = b_step
        elif lt_status_now == [1, 1, 0, 0, 0] or lt_status_now == [0, 0, 0, 1, 1]:
            step = c_step
        elif lt_status_now == [1, 0, 0, 0, 0] or lt_status_now == [0, 0, 0, 0, 1]:
            step = d_step

        # Direction calculate
        if lt_status_now == [0, 0, 1, 0, 0]:
            off_track_count = 0
            FR.turn(90)
        # turn right
        elif lt_status_now in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
            off_track_count = 0
            turning_angle = int(90 - step)
        # turn left
        elif lt_status_now in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
            off_track_count = 0
            turning_angle = int(90 + step)
        elif lt_status_now == [0, 0, 0, 0, 0]:
            off_track_count += 1
            if off_track_count > max_off_track_count:
                #tmp_angle = -(turning_angle - 90) + 90
                tmp_angle = (turning_angle - 90) / abs(90 - turning_angle)
                tmp_angle *= FR.turning_max
                rear_wheels.backwardWithSpeed(backward_speed)
                FR.turn(tmp_angle)

                #lf.wait_tile_center()
                rear_wheels.stop()

                FR.turn(turning_angle)
                time.sleep(0.2)
                rear_wheels.forwardWithSpeed(forward_speed)
                time.sleep(0.2)

        else:
            off_track_count = 0

        FR.turn(turning_angle)
        time.sleep(delay)

def cali():
    mount = 100
    FR.turn(70)
    print("\n cali white")
    time.sleep(4)
    FR.turn(90)
    # white_references = lf.get_avearge(mount)
    FR.turn(95)
    time.sleep(0.5)
    FR.turn(85)
    time.sleep(0.5)
    FR.turn(90)
    time.slee(1)

    FR.turn(110)
    print("\n cali black")
    time.sleep(4)
    FR.turn(90)
    # black_references = lf.get_average(mount)
    FR.turn(95)
    time.sleep(0.5)
    FR.turn(85)
    time.sleep(0.5)
    FR.turn(90)
    time.sleep(1)

    # for i in range(0, 5):
    # references[i] = (white_references[i] + black_references[i]) / 2
    # lf.references = references
    # print("Middle references =", references)
    # time.sleep(1)

def destroy():
    rear_wheels.pwm_low()
    FR.turn(90)

if __name__ == "__main__":
    try:
        while True:
            # =======================================================================    
            # setup and initilaize the left motor and right motor
            # =======================================================================

            # ULTRASONIC MODULE ACTIVE
            UA = SR02_Ultrasonic.Ultrasonic_Avoidance(35);

            # FRONT WHEEL SETUP
            FR = front_wheels.Front_Wheels(db='config')
            FR.ready()

            # REAR WHEEL SETUP
            rear_wheels.setup()

            # IS LINE FOLLOWER FR VAR SETUP
            FR.turning_max = 45
            
    except KeyboardInterrupt:
            # when the Ctrl+C key has been pressed,
            # the moving object will be stopped
        rear_wheels.pwm_low()
