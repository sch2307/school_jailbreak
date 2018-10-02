######################################################################
# Date: 2018/10/02
# file name: professor_assignment_main.py
# Purpose: this code has been generated for the 4WD moving
#         object to perform the project with ultra sensor
# this code is used for the student only
######################################################################

from myCar import MyCar
import time


class AssignmentMain(object):

    def __init__(self, car_name):
        self.myCar = MyCar(car_name)

        # Variable Setup
        self.forward_speed = 35
        self.backward_speed = 32

    def drive_parking(self):
        self.myCar.drive_parking()

    def first_main(self):
        # front_wheels center alignment
        self.myCar.steering.turn_straight()

        # forward-assignment
        self.myCar.accelerator.go_forward(30)
        for i in range(15): # 30-2s
            if self.myCar.distance_detector.get_distance() < 20:
                print("1st Avoidance Step")
                self.myCar.accelerator.go_forward(5)
                time.sleep(0.1)
                self.myCar.accelerator.stop()
                time.sleep(0.1)
                break
            time.sleep(0.1)
        self.myCar.accelerator.go_forward(60)
        for i in range(15):
            if self.myCar.distance_detector.get_distance() < 30:
                print("2nd Avoidance Step")
                self.myCar.accelerator.go_forward(5)
                time.sleep(0.1)
                self.myCar.accelerator.stop()
                time.sleep(0.1)
                break
            time.sleep(0.1)

        self.myCar.accelerator.go_forward(90)
        for i in range(15):
            if self.myCar.distance_detector.get_distance() < 40:
                print("3rd Avoidance Step")
                self.myCar.accelerator.go_forward(5)
                time.sleep(0.1)
                self.myCar.accelerator.stop()
                time.sleep(1)
                break
            time.sleep(0.1)

        # backward-assignment
        """ 30 speed - 2 sec """
        self.myCar.accelerator.go_backward(30)
        time.sleep(2)
        """ 60 speed - 2 sec """
        self.myCar.accelerator.go_backward(60)
        time.sleep(2)
        """ 90 speed - 2 sec """
        self.myCar.accelerator.go_backward(90)
        time.sleep(2)

        # stop
        self.myCar.accelerator.stop()

    def lineFollower_main(self):
        # lineFollower Setup
        turning_angle = 35
        delay = 0.0005

        a_step = 5
        b_step = 10
        c_step = 30
        d_step = 45

        self.myCar.accelerator.go_forward(self.forward_speed)

        while True:
            lt_status_now = self.myCar.line_detector.read_digital()

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
                self.myCar.steering.turn(90)
            # turn right
            elif sum(lt_status_now[:3]) > sum(lt_status_now[2:]):
                turning_angle = int(90 - step)
            # turn left
            elif sum(lt_status_now[:3]) < sum(lt_status_now[2:]):
                turning_angle = int(90 + step)
            elif lt_status_now == [0, 0, 0, 0, 0]:
                # rgb sensor check
                self.myCar.accelerator.go_forward(self.forward_speed)
                time.sleep(0.1)
                self.myCar.accelerator.stop()
                if self.myCar.line_detector.read_digital() == [0, 0, 0, 0, 0]:
                    time.sleep(0.05)
                    self.myCar.accelerator.stop()
                    store_angle = turning_angle
                    turning_angle = 120 if turning_angle < 90 else 60
                    self.myCar.steering.turn(turning_angle)
                    time.sleep(0.1)
                    while sum(self.myCar.line_detector.read_digital()) <= 1:
                        self.myCar.accelerator.go_backward(self.backward_speed)
                        time.sleep(0.1)
                    self.myCar.accelerator.stop()
                    turning_angle = store_angle
                    self.myCar.steering.turn(turning_angle)
                    time.sleep(0.1)
                    self.myCar.accelerator.go_forward(self.forward_speed)
                    time.sleep(0.4)
                else:
                    self.myCar.accelerator.go_forward(self.forward_speed)
                    print("COLOR DETECT")

            self.myCar.steering.turn(turning_angle)
            time.sleep(delay)


if __name__ == "__main__":
    try:
        Assignment_main = AssignmentMain("CarName")
        '''1st assignment'''
        # Assignment_main.first_main()
        '''2nd-3rd assignment'''
        Assignment_main.lineFollower_main()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        Assignment_main.drive_parking()
