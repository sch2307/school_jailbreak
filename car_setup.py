import sys
from PyQt5.QtWidgets import *


class Setup(QWidget):
    def __init__(self):
        super().__init__()
        self.config_file = open("./config", 'w')
        self.config_data = dict()
        self.config_data["turning_offset"] = 0
        self.config_data["forward0"] = "True"
        self.config_data["forward1"] = "False"
        self.init_ui()

    def init_ui(self):
        # 서보모터 컨트롤 버튼
        servo_left = QPushButton("<<")
        servo_right = QPushButton(">>")
        control_message = QLabel("서보 컨트롤")

        # 서보모터 미세 컨트롤 버튼
        servo_left_fine = QPushButton(" < ")
        servo_right_fine = QPushButton(" > ")
        control_message_fine = QLabel("미세한 서보 컨트롤")

        # 서보모터 컨트롤 레이아웃 구성
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

        # 서보모터 미세 컨트롤 레이아웃 구성
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

        # 서보모터 컨트롤 전체 레이아웃 구성
        servo_box = QVBoxLayout()
        servo_box.addLayout(servo_control_box)
        servo_box.addLayout(servo_fine_control_box)

        # 텍스트 출력 레이아웃 구성
        config_text = QTextEdit()
        config_text.setReadOnly(True)
        config_box = QHBoxLayout()
        # config_box.addStretch(1)
        config_box.addWidget(config_text)
        # config_box.addStretch(1)

        # 모터 컨트롤 버튼
        motor_message = QLabel("모터 컨트롤")
        left_message = QLabel("Left")
        right_message = QLabel("Right")
        drive_message = QLabel("Drive")
        left_reverse = QPushButton("Reverse")
        right_reverse = QPushButton("Reverse")
        run_button = QPushButton("Run")
        stop_button = QPushButton("Stop")

        # 모터 컨트롤 레이아웃
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

        # Save 버튼
        save_button = QPushButton("Save")
        save_box = QHBoxLayout()
        save_box.addStretch(1)
        save_box.addWidget(save_button)

        # 프로그램 전체 레이아웃 구성
        total_control_box = QHBoxLayout()
        total_control_box.addLayout(servo_box)
        total_control_box.addLayout(motor_control)
        main_box = QVBoxLayout()
        main_box.addLayout(total_control_box)
        main_box.addLayout(config_box)
        main_box.addLayout(save_box)

        self.setLayout(main_box)
        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle("Car Setup")
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    setup = Setup()
    sys.exit(app.exec_())
