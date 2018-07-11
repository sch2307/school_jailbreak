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
import rear_wheels
import front_wheels

# =======================================================================    
# setup and initilaize the left motor and right motor
# =======================================================================

def lineVar_Initialize():
    

if __name__ == "__main__":
    
    global isLineFollower
    
    # FRONT WHEEL SETUP
    FR = front_wheels.Front_Wheels(db='config')
    FR.ready()
    
    # REAR WHEEL SETUP
    rear_wheels.setup()
    
    try:
        while True:
            # =======================================================================    
            # setup and initilaize the left motor and right motor
            # =======================================================================
            FR.turn(70)
            
    except KeyboardInterrupt:
            # when the Ctrl+C key has been pressed,
            # the moving object will be stopped
        steering_libs.pwm_low()    
