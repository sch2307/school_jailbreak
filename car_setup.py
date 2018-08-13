import sys
from PyQt5.QtWidgets import *
import front_wheels
import rear_wheels


class Setup(QWidget):
    def __init__(self):
        super().__init__()
        self.is_run = False
        self.db_data = {}
        self.init_database()
        self.init_modules()
        self.init_ui()
        self.show_database()

    def init_ui(self):
        # Servo motor control button
        servo_left = QPushButton("<<")
        servo_right = QPushButton(">>")
        control_message = QLabel("Servo motor Control Menu")

        # Servo motor accurate control button
        servo_left_fine = QPushButton(" < ")
        servo_right_fine = QPushButton(" > ")
        control_message_fine = QLabel("Servo motor Accurate Control Menu")

        # Set servo motor control button layout
        servo_button_box = QHBoxLayout()
        servo_button_box.addStretch(1)
        servo_button_box.addWidget(servo_left)
        servo_button_box.addStretch(1)
        servo_button_box.addWidget(servo_right)
        servo_button_box.addStretch(1)

        message_box = QHBoxLayout()
        message_box.addStretch(1)
        message_box.addWidget(control_message)
        message_box.addStretch(1)

        servo_control_box = QVBoxLayout()
        servo_control_box.addLayout(message_box)
        servo_control_box.addLayout(servo_button_box)

        # Set servo motor accurate control button layout
        fine_message_box = QHBoxLayout()
        fine_message_box.addStretch(1)
        fine_message_box.addWidget(control_message_fine)
        fine_message_box.addStretch(1)

        servo_button_box_fine = QHBoxLayout()
        servo_button_box_fine.addStretch(1)
        servo_button_box_fine.addWidget(servo_left_fine)
        servo_button_box_fine.addStretch(1)
        servo_button_box_fine.addWidget(servo_right_fine)
        servo_button_box_fine.addStretch(1)

        servo_fine_control_box = QVBoxLayout()
        servo_fine_control_box.addLayout(fine_message_box)
        servo_fine_control_box.addLayout(servo_button_box_fine)

        # Set servo motor control layout
        servo_box = QVBoxLayout()
        servo_box.addLayout(servo_control_box)
        servo_box.addLayout(servo_fine_control_box)

        # Set text print box layout
        self.config_text = QTextEdit()
        self.config_text.setReadOnly(True)
        config_box = QHBoxLayout()
        config_box.addWidget(self.config_text)

        # motor control button
        motor_message = QLabel("Rear Motor Control Menu")
        left_message = QLabel("Left")
        right_message = QLabel("Right")
        drive_message = QLabel("Drive")
        left_reverse = QPushButton("Reverse")
        right_reverse = QPushButton("Reverse")
        run_button = QPushButton("Run")
        stop_button = QPushButton("Stop")

        # Set motor contorl layout
        motor_line_one = QHBoxLayout()
        motor_line_two = QHBoxLayout()
        motor_line_three = QHBoxLayout()
        motor_line_one.addStretch(1)
        motor_line_one.addWidget(motor_message)
        motor_line_one.addStretch(1)
        motor_line_two.addStretch(1)
        motor_line_two.addWidget(left_message)
        motor_line_two.addStretch(3)
        motor_line_two.addWidget(drive_message)
        motor_line_two.addStretch(3)
        motor_line_two.addWidget(right_message)
        motor_line_two.addStretch(1)
        motor_line_three.addWidget(left_reverse)
        motor_line_three.addWidget(run_button)
        motor_line_three.addWidget(stop_button)
        motor_line_three.addWidget(right_reverse)
        motor_control = QVBoxLayout()
        motor_control.addLayout(motor_line_one)
        motor_control.addLayout(motor_line_two)
        motor_control.addLayout(motor_line_three)

        # Save button
        save_button = QPushButton("Save")
        save_box = QHBoxLayout()
        save_box.addStretch(1)
        save_box.addWidget(save_button)

        # Set car_setup application layout
        total_control_box = QHBoxLayout()
        total_control_box.addLayout(servo_box)
        total_control_box.addLayout(motor_control)
        main_box = QVBoxLayout()
        main_box.addLayout(total_control_box)
        main_box.addLayout(config_box)
        main_box.addLayout(save_box)

        # link run button in run_button_clicked function
        run_button.clicked.connect(lambda: self.run_button_clicked())
        
        # link save button in save_button_clicked function 
        save_button.clicked.connect(lambda: self.save_button_clicked())
        
        # link stop button in stop_button_clicked function
        stop_button.clicked.connect(lambda: self.stop_button_clicked())
        
        # link reverse button in left/right_reverse_clicked function
        left_reverse.clicked.connect(lambda: self.left_reverse_clicked())
        right_reverse.clicked.connect(lambda: self.right_reverse_clicked())
        
        # link servo_left/right button in left/right_servo_clicked function 
        servo_left.clicked.connect(lambda: self.left_servo_clicked())
        servo_right.clicked.connect(lambda: self.right_servo_clicked())

        # link servo_left/right_fine in left/right_accurate_servo_clicked function
        servo_left_fine.clicked.connect(lambda: self.left_accurate_servo_clicked())
        servo_right_fine.clicked.connect(lambda: self.right_accurate_servo_clicked())

        # Set window
        self.setLayout(main_box)
        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle("Car Setup")
        self.show()

    def init_modules(self):
        # front_wheels PWM Driver Initialize
        global fr_wheels
        fr_wheels = front_wheels.Front_Wheels(db='config')
        fr_wheels.ready()
        fr_wheels.calibration()

        # rear_wheels PWM Driver Initialize
        global rear_wheels
        rear_wheels.setup(1)

    def init_database(self):
        self.db_data["turning_offset"] = -22
        self.db_data["forward0"] = True
        self.db_data["forward1"] = False
        f = open("./config", 'w')
        f.write("# File based database.\n")
        f.write("\n")
        f.write("turning_offset = -22\n")
        f.write("forward0 = True\n")
        f.write("forward1 = False\n")
        f.close()

    def show_database(self):
        f = open("./config", 'r')
        print_text = ""
        for line in f:
            print_text += line
            # print_text += "\n"
        f.close()
        self.config_text.setText(print_text)

    def save_button_clicked(self):
        f = open("./config", 'w')
        f.write("# File based database.\n")
        f.write("\n")
        temp = "turning_offset = " + str(self.db_data["turning_offset"]) + "\n"
        f.write(temp)
        temp = "forward0 = "
        if self.db_data["forward0"] is True:
            temp += "True\n"
        else:
            temp += "False\n"
        f.write(temp)
        temp = "forward1 = "
        if self.db_data["forward1"] is True:
            temp += "True\n"
        else:
            temp += "False\n"
        f.write(temp)
        f.close()

    def left_reverse_clicked(self):
        self.db_data["forward0"] = not self.db_data["forward0"]
        self.save_button_clicked()
        self.show_database()
        if self.is_run:
            self.run_button_clicked()

    def right_reverse_clicked(self):
        self.db_data["forward1"] = not self.db_data["forward1"]
        self.save_button_clicked()
        self.show_database()
        if self.is_run:
            self.run_button_clicked()

    def run_button_clicked(self):
        self.is_run = True
        self.init_modules()
        rear_wheels.forward_with_speed(40)

    def stop_button_clicked(self):
        self.is_run = False
        rear_wheels.stop()

    def left_servo_clicked(self):
        fr_wheels.cali_left()
        self.db_data["turning_offset"] = fr_wheels.return_cali_offset()
        self.save_button_clicked()
        self.show_database()

    def right_servo_clicked(self):
        fr_wheels.cali_right()
        self.db_data["turning_offset"] = fr_wheels.return_cali_offset()
        self.save_button_clicked()
        self.show_database()

    def left_accurate_servo_clicked(self):
        fr_wheels.cali_accurate_left()
        self.db_data["turning_offset"] = fr_wheels.return_cali_offset()
        self.save_button_clicked()
        self.show_database()

    def right_accurate_servo_clicked(self):
        fr_wheels.cali_accurate_right()
        self.db_data["turning_offset"] = fr_wheels.return_cali_offset()
        self.save_button_clicked()
        self.show_database()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    setup = Setup()
    sys.exit(app.exec_())
