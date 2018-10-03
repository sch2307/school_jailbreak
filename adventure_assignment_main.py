#########################################################################
# Date: 2018/10/02
# file name: adventure_assignment_main.py
# Purpose: this code has been generated for the 4 wheel drive body
# moving object to perform the project with extension module
# this code is used for the student only
#########################################################################

from car import Car
import time


class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)

    def drive_parking(self):
        self.car.drive_parking()

    # =======================================================================
    # ADVENTURE_ASSIGNMENT_CODE
    # Complete the code to perform Adventure Assignment
    # =======================================================================
    def car_startup(self):
        # Implement the assignment code here.
        pass


if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()