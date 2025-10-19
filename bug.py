import time
import RPi.GPIO as GPIO
import random
from shifter import Shifter
import threading

class Bug:
    def __init__(self, timestep = 0.1, x = 3, isWrapOn = False):
        self.timestep = timestep
        self.x = x
        self.isWrapOn = isWrapOn
        self.__shifter = Shifter(serialPin = 21, latchPin = 20, clockPin = 16)
        self.__thread = None
        self.__running = False

    def __run(self):
        while self.__running:
            pattern = 1 << self.x
            self.__shifter.shiftByte(pattern)
            step = random.choice([-1, 1])
            self.x = self.x + step
            if self.isWrapOn:
                if self.x < 0:
                    self.x = 7
                elif self.x > 7:
                    self.x = 0
            else:
                if self.x < 0:
                  self.x = 0
                elif self.x > 7: 
                  self.x = 7
            time.sleep(self.timestep)
        self.__shifter.shiftByte(0)
    
    def start(self):
        if not self.__running:
            self.__running = True
            self.__thread = threading.Thread(target = self.__run)
            self.__thread.start()
            
    def stop(self):
        if self.__running:
            self.__running = False
            self.__thread.join()
