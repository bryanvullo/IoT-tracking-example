# importing snowplow
import snowplow_tracker
from snowplow_tracker import Tracker, Emitter
from snowplow_tracker import SelfDescribingJson

# importing device modules
from machine import Pin, PWM
import time

# snowplow initialisation
e = Emitter('localhost:9090') #some endpoint
t = Tracker( e,
            app_id="Bryan's App")

# device initialisation
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

def track_satisfaction(rating):
    t.track_self_describing_event(
        # event
        SelfDescribingJson("iglu:com.myvendor/satisfaction/jsonschema/1-0-0",
        {
            "satisfaction_rating": rating
        }
    ))

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

def redButtonClick():
    track_satisfaction("Bad")
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

def yellowButtonClick():
    track_satisfaction("Average")
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

def greenButtonClick():
    track_satisfaction("Good")
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


while True:
    setOff()
    
    if not redbutton.value():
        redButtonClick()
        
    elif not yellowbutton.value():
        yellowButtonClick()
        
    elif not greenbutton.value():
        greenButtonClick()
        