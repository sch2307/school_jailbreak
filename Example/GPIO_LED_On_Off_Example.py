# coding=utf-8
"""
LED를 제어하기 위해 RPi.GPIO 모듈을 GPIO로 import 합니다.
sleep 함수를 사용하기 위해서 time 모듈을 import 합니다.
"""
import time

import RPi.GPIO as GPIO

# Raspberry Pi 핀 번호를 의미합니다.
led_pinG = 37
led_pinR = 35
led_pinB = 33

# Raspberry Pi GPIO 핀 번호를 사용하도록 설정합니다.
GPIO.setmode(GPIO.BOARD)

"""
led_pin을 GPIO 출력으로 설정합니다. 이를 통해 led_pin으로
True 혹은 False를 쓸 수 있게 됩니다.
"""
GPIO.setup(led_pinG, GPIO.OUT)
GPIO.setup(led_pinR, GPIO.OUT)
GPIO.setup(led_pinB, GPIO.OUT)

#  1s = 1000ms
try:
    while True:
        # led_pin 에 연결된 LED 가 켜집니다.
        GPIO.output(led_pinB, True)
        time.sleep(0.5)  # 5ms
        # led_pin 에 연결된 LED 가 꺼집니다.
        GPIO.output(led_pinB, False)
        time.sleep(0.5)  # 5ms

except KeyboardInterrupt:
    GPIO.cleanup()

"""
control + c 키를 눌러서 KeyboardInterrupt를 발생시키면
GPIO.cleanup()을 호출하여 GPIO를 초기 상태로 돌려놓습니다.
"""
