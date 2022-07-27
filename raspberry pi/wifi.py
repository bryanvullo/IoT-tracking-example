import network
import time
from machine import Pin

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid = "BTHub6-KSKG"
pw = "AbDNRFD3TiHM"

wlan.connect(ssid, pw)

def light_onboard_led():
    led = Pin('LED', Pin.OUT)
    led.value(1)
    
timeout = 10
while timeout > 0:
    if wlan.status() >= 3:
        print('Connected')
        light_onboard_led()
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)
   
wlan_status = wlan.status()