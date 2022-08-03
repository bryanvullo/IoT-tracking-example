from machine import Pin, PWM
import time

redpin = PWM(Pin(13))
greenpin = PWM(Pin(12))
bluepin = PWM(Pin(11))

freq_num = 10000
redpin.freq(freq_num)
greenpin.freq(freq_num)
bluepin.freq(freq_num)

redbutton = Pin(7, Pin.IN, Pin.PULL_UP)
yellowbutton = Pin(8, Pin.IN, Pin.PULL_UP)
greenbutton = Pin(9, Pin.IN, Pin.PULL_UP)

def setRed():
    redpin.duty_u16(0)
    greenpin.duty_u16(65535)
    bluepin.duty_u16(65535)

def setGreen():
    redpin.duty_u16(65535)
    greenpin.duty_u16(0)
    bluepin.duty_u16(65535)
    
def setYellow():
    redpin.duty_u16(0)
    greenpin.duty_u16(0)
    bluepin.duty_u16(65535)
    
def setOff():
    redpin.duty_u16(65535)
    greenpin.duty_u16(65535)
    bluepin.duty_u16(65535)

while True:
    if not redbutton.value():
        setRed()
        time.sleep(0.5)
        setOff()
        time.sleep(0.5)
        setRed()
        time.sleep(0.5)
        setOff()
        time.sleep(0.5)
        setRed()
        time.sleep(0.5)
        setOff()
        time.sleep(0.5)
        
    if not yellowbutton.value():
        setYellow()
        time.sleep(0.5)
        setOff()
        time.sleep(0.5)
        setYellow()
        time.sleep(0.5)
        setOff()
        time.sleep(0.5)
        setYellow()
        time.sleep(0.5)
        setOff()
        time.sleep(0.5)
        
    if not greenbutton.value():
        setGreen()
        time.sleep(0.5)
        setOff()
        time.sleep(0.5)
        setGreen()
        time.sleep(0.5)
        setOff()
        time.sleep(0.5)
        setGreen()
        time.sleep(0.5)
        setOff()
        time.sleep(0.5)
        