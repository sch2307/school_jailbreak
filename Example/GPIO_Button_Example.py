# coding=utf-8
import RPi.GPIO as GPIO
import time

# Raspberry Pi 3번 핀을 버튼 입력으로 사용합니다.
button_pin = 3

# Raspberry Pi 보드의 핀 순서를 사용합니다.
GPIO.setmode(GPIO.BOARD)

# button_pin을 GPIO 입력으로 설정합니다.
GPIO.setup(button_pin, GPIO.IN)

try:
    '''
    계속 반복해서 button_pin의 상태를 읽어 
    buttonInput 변수에 저장합니다.
    '''
    while True:
        """
        button_pin 값을 읽어 buttonInput 에 저장합니다.
        """
        buttonInput = GPIO.input(button_pin)
        print(buttonInput)

except KeyboardInterrupt:
    GPIO.cleanup()

"""
KeyboardInterrupt가 발생하면 핀 설정 상태를 초기화 합니다.
"""
