# importing device modules
from machine import Pin, PWM
import time
import ujson
# importing my own modules
import dht11
import myrequests as requests
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

# collector url
collector = "bryan-pipeline-rds-20220727213438582900000002.cbpnfeamlxtg.eu-west-1.rds.amazonaws.com"

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
    measurement = dht.measure()
    while measurement == 0:
        print("DHT data error")
        time.sleep(1)
        measurement = dht.measure()
        
    temperature = dht.temperature()
    humidity = dht.humidity()
    print("temperature: %0.2fC  humidity: %0.2f"%(temperature, humidity) + "%")
    return temperature, humidity

# gets the epoch time difference as pico clock resets at boot
def getTimeDifference():
    res = requests.get("http://worldtimeapi.org/api/timezone/Europe/London")
    t_proper = res.json()["unixtime"]
    t_machine = time.time()
    difference = t_proper - t_machine
    return difference

# returns epoch time in ms
def getTime():
    t_machine = time.time() # machine time in s
    t_s = t_machine + time_difference
    t_ms = t_s * 1000
    return t_ms

# gets the location using an API and returns the city
def getLocation():
    API_KEY = ""
    baseURL = "http://api.ipstack.com/check?access_key="
    url = baseURL + API_KEY
    res = requests.get(url).json()
    return res["city"]# gets the location using an API and returns the city

# gets weather from API and returns data
def getWeather(city):
    baseURL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = ""
    
    url = baseURL + "appid=" + API_KEY + "&q=" + city
    res = requests.get(url).json()
    
    city = res["name"]
    temperature = float( res["main"]["temp"] ) - 273.15
    windspeed = float( res["wind"]["speed"] )
    humidity = int( res["main"]["humidity"] )
    pressure = int( res["main"]["pressure"] )
    conditions = res["weather"][0]["description"]
    print(city, temperature, windspeed, humidity, pressure, conditions)
    
    return [city, temperature, windspeed, humidity, pressure, conditions]

# function to send a POST request to the snowplow collector    
def event(satisfaction, temperature, humidity, time, weather):
    post_data = ujson.dumps({
      "schema": "iglu:com.snowplowanalytics.snowplow/payload_data/jsonschema/1-0-4",
      "data": [
        {
          "e": "ue", 
          "tna": "snplow5", 
          "tv": "upython-0.0.1",
          "aid": "satisfaction-meter", 
          "p": "iot", 
          "dtm": str(time), 
          "stm": str(time), 
          "ue_pr": ujson.dumps({
            "schema": "iglu:com.snowplowanalytics.snowplow/unstruct_event/jsonschema/1-0-0", 
            "data": {
              "schema": "iglu:com.myvendor/satisfaction/jsonschema/1-0-2", 
              "data": {
                "satisfaction_rating": satisfaction 
              }
            }
          }),
          "co": ujson.dumps({
              "schema": "iglu:com.snowplowanalytics.snowplow/contexts/jsonschema/1-0-0",
              "data": [
                {
                    "schema": "iglu:com.myvendor/weather/jsonschema/1-0-1",
                    "data": { 
                    "city": weather[0],
                    "temperature_celsius": weather[1],
                    "windspeed": weather[2],
                    "humidity": weather[3],
                    "pressure": weather[4],
                    "conditions": weather[5]
                      }
                  },
                {
                    "schema": "iglu:com.myvendor/sensors/jsonschema/2-0-0", 
                    "data": { 
                    "temperature": temperature,
                    "humidity": humidity
                      }
                  }
              ]
            })
        }
      ]
    })
    request_url = "http://"+collector+"/com.snowplowanalytics.snowplow/tp2"
    res = requests.post(request_url, headers = {'content-type': 'application/json'}, data = post_data)
    print(res.status_code)

# runs once
setOff()
time_difference = getTimeDifference()
    
# event loop which checks if buttons have been pressed
while True:
    
    if not redbutton.value():
        redButtonClick()
        # sensor and API data collection
        temperature, humidity = sensorRead()
        time = getTime() 
        city = getLocation()
        weather = getWeather(city)
        # send event
        event('bad', temperature, humidity, time, weather)
        
    elif not yellowbutton.value():
        yellowButtonClick()
        temperature, humidity = sensorRead()
        time = getTime() 
        city = getLocation()
        weather = getWeather(city)
        event('average', temperature, humidity, time, weather)
        
    elif not greenbutton.value():
        greenButtonClick()
        temperature, humidity = sensorRead()
        time = getTime() 
        city = getLocation()
        weather = getWeather(city)
        event('good', temperature, humidity, time, weather)
        