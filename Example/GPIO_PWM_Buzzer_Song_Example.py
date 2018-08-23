# coding=utf-8
"""
Buzzer 를 제어하기 위해 RPi.GPIO 모듈을 GPIO로 import 합니다.
sleep 함수를 사용하기 위해서 time 모듈을 import 합니다.
"""
import time

import RPi.GPIO as GPIO

# 18은 broadcom 사의 GPIO핀 번호를 의미합니다.
buzzer_pin = 8

# BCM GPIO 핀 번호를 사용하도록 설정합니다.
GPIO.setmode(GPIO.BOARD)

"""
음계별 표준 주파수
[ 도, 레, 미, 파, 솔, 라 시, 도]
"""
scale = [261.6, 293.6, 329.6, 349.2, 391.9, 440.0, 493.8, 523.2]

"""
buzzer_pin 을 GPIO 출력으로 설정합니다. 이를 통해 led_pin으로
True 혹은 False를 쓸 수 있게 됩니다.
"""
GPIO.setup(buzzer_pin, GPIO.OUT)

# Song Array
list = [4, 4, 5, 5, 4, 4, 2, 4, 4, 2, 2, 1, 4, 4, 5, 5, 4, 4, 2, 4, 2, 1, 2, 0]

try:
    p = GPIO.PWM(buzzer_pin, 100)
    p.start(5)     # start the PWM on 100% duty cycle
    # p.ChangeDutyCycle(5)  # change the duty cycle to 90%

    for i in range(len(list)):
        print (i + 1)
        p.ChangeFrequency(scale[list[i]]*2)
        time.sleep(0.25)

    p.stop()  # stop the PWM output

finally:
    GPIO.cleanup()
