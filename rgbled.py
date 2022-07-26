# importing device modules
from machine import Pin, PWM
import time
import dht11
import urequests as requests
import wifi

    # device initialisation
# RGB LED 
redpin = PWM(Pin(13))
greenpin = PWM(Pin(12))
bluepin = PWM(Pin(11))

freq_num = 10000
redpin.freq(freq_num)
greenpin.freq(freq_num)
bluepin.freq(freq_num)

# temp and humidity sensor
temperature = 0
humidity = 0
dht = dht11.DHT11(15)
time.sleep(1)

# buttons
redbutton = Pin(7, Pin.IN, Pin.PULL_UP)
yellowbutton = Pin(8, Pin.IN, Pin.PULL_UP)
greenbutton = Pin(9, Pin.IN, Pin.PULL_UP)

    # collecter information
# ngrok url
ngrok = "0e9f-2a00-23c6-1a96-301-cccb-13fc-81bf-9893.eu.ngrok.io"

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

def sensorRead():
    # temp and humidity sensor - DHT11 sensor
    if dht.measure() == 0:
        print("DHT data error")
        return
    temperature = dht.temperature()
    humidity = dht.humidity()
    print("temperature: %0.2fC  humidity: %0.2f"%(temperature, humidity) + "%")
    return temperature, humidity
    
def event(satisfaction, temperature, humidity):
    requests.get(url="http://"+ngrok+"/com.snowplowanalytics.iglu/v1?schema=iglu%3Acom.myvendor%2Fsatisfaction%2Fjsonschema%2F1-0-0&satisfaction="+satisfaction+"&temperature="+str(temperature)+"&humidity="+str(humidity))
    
    # http://e4de-2a00-23c6-1a96-301-cccb-13fc-81bf-9893.eu.ngrok.io/com.snowplowanalytics.iglu/v1?
    # schema=iglu%3Acom.myvendor%2Fsatisfaction%2Fjsonschema%2F1-0-0
    # &satisfaction=satifaction
    # &temperature=temperature
    # &humidity=humidity
    

while True:
    setOff()
    
    if not redbutton.value():
        temperature, humidity = sensorRead()
        redButtonClick()
        event('bad', temperature, humidity)
        
    elif not yellowbutton.value():
        temperature, humidity = sensorRead()
        yellowButtonClick()
        event('average', temperature, humidity)
        
    elif not greenbutton.value():
        temperature, humidity = sensorRead()
        greenButtonClick()
        event('good', temperature, humidity)
        