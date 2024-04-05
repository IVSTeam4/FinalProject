import RPi.GPIO as GPIO
import time

from time import sleep, perf_counter
from threading import Thread

Tr = 11
Ec = 8

def init () :
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Tr, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(Ec, GPIO.IN)
    
    
def checkdist () :
    GPIO.output(Tr, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(Tr, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(Tr, GPIO.LOW)
    
    while not GPIO.input(Ec) :
        pass    
    t1 = time.time()  
    while GPIO.input(Ec) :
        pass
    t2 = time.time()
    
    dist = ((t2 - t1) * 340) / 2
    
    return dist


def cleanup () :
    GPIO.cleanup()