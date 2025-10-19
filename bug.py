import time
import RPi.GPIO as GPIO
import random
from shifter import Shifter

serialPin = 21
latchPin = 20
clockPin = 16

shifter = Shifter(serialPin, latchPin, clockPin)

position = 0

try:
    while 1:
        pattern = 1 << position
        shifter.shiftByte(pattern)
        step = random.choice([-1, 1])
        position = position + step
        if position < 0:
          position = 0
        if position > 7: 
          position = 7
        time.sleep(0.05)
except:
    GPIO.cleanup()
