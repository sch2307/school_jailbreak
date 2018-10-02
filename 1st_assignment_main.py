#########################################################################
# Date: 2018/10/02
# file name: 1st_assignment_main.py
# Purpose: this code has been generated for the 4 wheels drive body
# moving object to perform the project with ultra sensor
# this code is used for the student only
#########################################################################

from myCar import MyCar
import time


class AssignmentMain(object):

    def __init__(self, car_name):
        self.myCar = MyCar(car_name)

    def drive_parking(self):
        self.myCar.drive_parking()

    # =======================================================================
    # 1ST_ASSIGNMENT_CODE
    # Complete the code to perform First Assignment
    # =======================================================================
    def assignment_main(self):
        # Implement the assignment code here.
        pass


if __name__ == "__main__":
    try:
        Assignment_main = AssignmentMain()
        Assignment_main.assignment_main()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        Assignment_main.drive_parking()