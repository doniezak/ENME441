import RPi.GPIO as GPIO
import time

class Shifter:
   
    def__init__(self, serialPin, latchPin, clockPin):
        self.serialPin = serialPin
        self.latchPin = latchPin
        self.clockPin = clockPin
        GPIO.setmode(GPIO.BCM)        
        GPIO.setup(serialPin, GPIO.OUT)
        GPIO.setup(latchPin, GPIO.OUT, initial=0)  # start latch & clock low
        GPIO.setup(clockPin, GPIO.OUT, initial=0)
    
    def __ping(self, p):  # ping the clock or latch pin
        GPIO.output(p, 1)
        time.sleep(0)
        GPIO.output(p, 0)
    
    def shiftByte(self, b):  # send a byte of data to the output
        for i in range(8):
            GPIO.output(self.serialPin, b & (1 << i))
            self.__ping(self.clockPin)  # add bit to register
        self.__ping(self.latchPin)  # send register to output
