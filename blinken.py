import RPi.GPIO as GPIO
import time
from random import random


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

l1_4 = 2
l2_4 = 3
l3_4 = 4
l4_4 = 14

l1_5 = 17
l2_5 = 27
l3_5 = 22
l4_5 = 23
l5_5 = 24

l1_6 = 13
l2_6 = 19
l3_6 = 26
l4_6 = 16
l5_6 = 20
l6_6 = 21

gpioToBoard = [0,0,3,5,7,29,31,26,24,21,
19,23,32,33,8,10,36,11,12,35,
38,40,15,23,18,22,37,13]

all_leds = [2,3,4,14,17,27,22,23,24,13,19,26,16,20,21]
all_leds = [gpioToBoard[i] for i in all_leds]

button = gpioToBoard[12]

btn_down = False
lights_on = False

#GPIO.setmode(GPIO.BCM)  

for led in all_leds:
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, GPIO.LOW)


GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
    if not GPIO.input(button): #button pressed --> GPIO.input() == False
        if not btn_down:
            btn_down = True
            if not lights_on:
                    for led in all_leds:
                        if random() > 0.5:
                            GPIO.output(led, GPIO.HIGH)
                        else:
                            GPIO.output(led, GPIO.LOW)
                    lights_on = True
            else:
                for led in all_leds:
                    GPIO.output(led, GPIO.LOW)
                lights_on = False
    else:
        btn_down = False
    
    time.sleep(.2)
