# coding=utf-8
"""
LED를 제어하기 위해 RPi.GPIO 모듈을 GPIO로 import 합니다.
sleep 함수를 사용하기 위해서 time 모듈을 import 합니다.
"""

import time

import RPi.GPIO as GPIO


# 18은 broadcom 사의 GPIO핀 번호를 의미합니다.
led_pinG = 37
led_pinR = 35
led_pinB = 33

# BCM GPIO 핀 번호를 사용하도록 설정합니다.
GPIO.setmode(GPIO.BOARD)

"""
led_pin을 GPIO 출력으로 설정합니다. 이를 통해 led_pin으로
True 혹은 False를 쓸 수 있게 됩니다.
"""
GPIO.setup(led_pinR, GPIO.OUT)
GPIO.setup(led_pinG, GPIO.OUT)
GPIO.setup(led_pinB, GPIO.OUT)

# 1s = 1000ms
try:
    while True:
        time.sleep(0.01)
        for sec in range(0, 101, 1):
            """
            for 문을 통해 증가하는 초를 밀리초 단위로
            변환하여 지연시간을 준다.
            """
            milisec = sec * 0.0001

            """
            100Hz의 주파수로 점멸하는 LED의 밝기를 
            조절하기위해 상하비를 조절한다.
            """
            GPIO.output(led_pinG, True)
            time.sleep(milisec)
            GPIO.output(led_pinG, False)
            time.sleep(0.01 - milisec)

        for sec in range(100, -1, -1):
            milisec = sec * 0.0001

            GPIO.output(led_pinG, True)
            time.sleep(milisec)
            GPIO.output(led_pinG, False)
            time.sleep(0.01 - milisec)


except KeyboardInterrupt:
    GPIO.cleanup()

"""
control + c 키를 눌러서 KeyboardInterrupt를 발생시키면
GPIO.cleanup()을 호출하여 GPIO를 초기 상태로 돌려놓습니다.
"""
