######################################################################
# Date: 2018/07/12
# file name: project_main.py
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
#  set GPIO warnings as false 
# =======================================================================
GPIO.setwarnings(False)


# =======================================================================
# import ALL method in the SEN040134 Tracking Module
# =======================================================================
from SEN040134 import SEN040134_Tracking


# =======================================================================
# import ALL method in the TCS34725 RGB Module
# =======================================================================
from TCS34725 import TCS34725_RGB


# =======================================================================
# import ALL method in the SR02 Ultrasonic Module
# =======================================================================
from SR02 import SR02_Ultrasonic


# =======================================================================
# import ALL method in the rear/front Motor Module 
# =======================================================================
import rear_wheels
import front_wheels


# =======================================================================    
# setup and initialize the left motor and right motor
# =======================================================================
forward_speed = 34
backward_speed = 34
turning_angle = 35

# calibrate = True
max_off_track_count = 40

delay = 0.0005


# def straight_run():
#     while True:
#         rear_wheels.forwardWithSpeed(70)
#         FR.turn_straight()


def setup():
    # if calibrate:
    cali()


def lineFollwer_main():
    global turning_angle
    # off_track_count = 0

    a_step = 5
    b_step = 10
    c_step = 30
    d_step = 45
    
    rear_wheels.forwardWithSpeed(forward_speed)

    while True:
        # SR02-Ultrasonic avoidance
        uDistance = UA.get_distance()
        if 0 <= uDistance <= 2:
            print("DISTANCE", uDistance)
            rear_wheels.stop()
            break

        # TCS34725-RGB Module
        cr, cg, cb, clr = RM.get_raw_data()
        lux = TCS34725_RGB.calculate_lux(cr, cg, cb)
        print(" RED : ", cr, " GREEN : ", cg, " BLUE : ", cb, " LUX : ", lux)
        lt_status_now = LF.read_digital()
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
            # off_track_count = 0
            FR.turn(90)
        # turn right
        # elif lt_status_now in ([0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 0, 0, 0, 0]):
        elif sum(lt_status_now[:3]) > sum(lt_status_now[2:]):
            # off_track_count = 0
            turning_angle = int(90 - step)
        # turn left
        # elif lt_status_now in ([0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]):
        elif sum(lt_status_now[:3]) < sum(lt_status_now[2:]):
            # off_track_count = 0
            turning_angle = int(90 + step)
        elif lt_status_now == [0, 0, 0, 0, 0]:
            # rgb sensor check
            rear_wheels.forwardWithSpeed(forward_speed)
            time.sleep(0.1)
            rear_wheels.stop()
            if LF.read_digital() == [0, 0, 0, 0, 0]:
                # off_track_count += 1
                # if off_track_count > max_off_track_count:
                    # #tmp_angle = -(turning_angle - 90) + 90
                #    tmp_angle = (turning_angle - 90) / abs(90 - turning_angle)
                #    tmp_angle *= FR.turning_max
                #    rear_wheels.backwardWithSpeed(backward_speed)
                #    FR.turn(tmp_angle)

                #    LF.wait_tile_center()
                #    rear_wheels.stop()
            
                #    FR.turn(turning_angle)
                #    time.sleep(0.2)
                #    rear_wheels.forwardWithSpeed(forward_speed)
                #    time.sleep(0.2)
                time.sleep(0.05)
                rear_wheels.stop()
                store_angle = turning_angle
                turning_angle = 120 if turning_angle < 90 else 60
                FR.turn(turning_angle)
                time.sleep(0.1)
                while sum(LF.read_digital()) <= 1:
                    rear_wheels.backwardWithSpeed(backward_speed)
                    time.sleep(0.1)
                rear_wheels.stop()
                turning_angle = store_angle
                FR.turn(turning_angle)
                time.sleep(0.1)
                rear_wheels.forwardWithSpeed(forward_speed)
                time.sleep(0.4)
            else:
                rear_wheels.forwardWithSpeed(forward_speed)
                print("color")
        else:
            pass
            # off_track_count = 0

        FR.turn(turning_angle)
        
        time.sleep(delay)


def cali():
    # mount = 100
    FR.turn(70)
    print("front Wheel cali")
    time.sleep(4)
    FR.turn(90)
    FR.turn(95)
    time.sleep(0.5)
    FR.turn(85)
    time.sleep(0.5)
    FR.turn(90)
    time.sleep(1)

    FR.turn(110)
    time.sleep(4)
    FR.turn(90)
    FR.turn(95)
    time.sleep(0.5)
    FR.turn(85)
    time.sleep(0.5)
    FR.turn(90)
    time.sleep(1)


def destroy():
    rear_wheels.pwm_low()
    FR.turn(90)


if __name__ == "__main__":
    try:
        # =======================================================================    
        # setup and initialize the left motor and right motor
        # =======================================================================

        # ULTRASONIC MODULE DRIVER INITIALIZE
        UA = SR02_Ultrasonic.Ultrasonic_Avoidance(35)

        # TRACKING MODULE DRIVER INITIALIZE
        LF = SEN040134_Tracking.SEN040134_Tracking([16, 18, 22, 40, 32])

        # RGB MODULE DRIVER INITIALIZE
        RM = TCS34725_RGB.TCS34725()

        # FRONT WHEEL DRIVER SETUP
        FR = front_wheels.Front_Wheels(db='config')
        FR.ready()

        # REAR WHEEL DRIVER SETUP
        rear_wheels.setup(1)

        # IS LINE FOLLOWER FR VAR SETUP
        FR.turning_max = 35
        
        # Front wheel Calibration
        setup()
        
        # RGB Module interrupt SETUP
        RM.set_interrupt(False)
        
        # start
        lineFollwer_main()
        
    except KeyboardInterrupt:
            # when the Ctrl+C key has been pressed,
            # the moving object will be stopped
        rear_wheels.stop()
