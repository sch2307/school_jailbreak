######################################################################
### Date: 2017/10/5
### file name: project3_student.py
### Purpose: this code has been generated for the three-wheeled moving
###         object to perform the project3 with ultra sensor
###         swing turn, and point turn
### this code is used for the student only
######################################################################

# =======================================================================
# import GPIO library and time module 
# =======================================================================
import RPi.GPIO as GPIO
from time import sleep

# =======================================================================
#  set GPIO warnings as false 
# =======================================================================
GPIO.setwarnings(False)

# =======================================================================
# import getDistance() method in the ultraModule 
# =======================================================================
#from Ultrasonic_Avoidance import *

# =======================================================================
# import ALL method in the rear/front Motor Module 
# =======================================================================
import rear_wheel
import front_wheel

# =======================================================================
# import ALL method in the steering_libs
# =======================================================================
import steering_libs

# =======================================================================    
# setup and initilaize the left motor and right motor
# =======================================================================

if __name__ == "__main__":
    print("START SETUP")
    steering_libs.pwm_setup()
    rear_wheel.setup()
    front_wheel.setup()
    print("SETUP COMPLETE")
    try:
        while True:
            # =======================================================================    
            # setup and initilaize the left motor and right motor
            # =======================================================================
            
            #TEST MODULE
            print('start moving')
            # rear_wheel.forwardWithSpeed()
            # front_wheel.turn(50)
            # rear_wheel.forward()
            front_wheel.home()
            
    except KeyboardInterrupt:
            # when the Ctrl+C key has been pressed,
            # the moving object will be stopped
        steering_libs.pwm_low()    
