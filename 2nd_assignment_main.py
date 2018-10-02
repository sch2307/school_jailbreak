#########################################################################
# Date: 2018/10/02
# file name: 2nd_assignment_main.py
# Purpose: this code has been generated for the 4 wheel drive body
# moving object to perform the project with line detector
# this code is used for the student only
#########################################################################

from myCar import MyCar
import time


class AssignmentMain(object):

    def __init__(self):
        self.myCar = MyCar()

    def drive_parking(self):
        self.myCar.drive_parking()

    # =======================================================================
    # 2ND_ASSIGNMENT_CODE
    # Complete the code to perform Second Assignment
    # =======================================================================
    def assignment_main(self):
        # implement the assignment code here
        pass


if __name__ == "__main__":
    try:
        Assignment_main = AssignmentMain()
        Assignment_main.assignment_main()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        Assignment_main.drive_parking()