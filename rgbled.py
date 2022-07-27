# importing device modules
from machine import Pin, PWM
import time
import dht11
import myrequests as requests
import wifi
import ujson

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

# ngrok url
ngrok = "1529-2a00-23c6-1a96-301-cccb-13fc-81bf-9893.eu.ngrok.io"

# functions to turn RGB LED specific colors
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

# functions to flash RGB LED to certain colors
def redButtonClick():
    for i in range(3):
        setRed()
        time.sleep(0.5)
        setOff()
        time.sleep(0.5)

def yellowButtonClick():
    for i in range(3):
        setYellow()
        time.sleep(0.5)
        setOff()
        time.sleep(0.5)
        
def greenButtonClick():
    for i in range(3):
        setGreen()
        time.sleep(0.5)
        setOff()
        time.sleep(0.5)

# function to read from sensors and return the readings
def sensorRead():
    # temp and humidity sensor - DHT11 sensor
    if dht.measure() == 0:
        print("DHT data error")
        return
    temperature = dht.temperature()
    humidity = dht.humidity()
    print("temperature: %0.2fC  humidity: %0.2f"%(temperature, humidity) + "%")
    return temperature, humidity

# function to send a POST request to the snowplow collector
def event(satisfaction, temperature, humidity):
    post_data = ujson.dumps({"satisfaction_rating":satisfaction, "temperature":temperature, "humidity":humidity})
    request_url = "http://"+ngrok+"/com.snowplowanalytics.iglu/v1?schema=iglu%3Acom.myvendor%2Fsatisfaction%2Fjsonschema%2F1-0-0&aid=satisfaction-meter&p=iot"
    res = requests.post(request_url, headers = {'content-type': 'application/json'}, data = post_data)
    print(res.status_code)
    
# event loop which checks if buttons have been pressed
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
        