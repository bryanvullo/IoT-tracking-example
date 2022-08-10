# Snowplow IoT Project
## Intro
My name is Bryan and I'm a 18 year old Pre-Graduate Student 
This project is about showing how you can track data from an IoT device.
I will be using sensors and APIs to collect data. Then Snowplow will validate and send my events to my data warehouse. 

## Snowplow
Snowplow Analytics holds the throne when it comes to tracking behavioral data; IoT devices can be a gold mine. This is because IoT devices have the capability to send lots of small events as they get interacted with, these events can then be highly enriched by sensor data, APIs and Snowplow's automatic enrichment process.
What makes Snowplow the best in terms of tracking is their unique and flexible schema architecture. Where engineers can define the data structure that they want to track, assign the type of data they expect, minimum and maximum values, etc. Once these are made and events are sent through these schemas, Snowplow validates each event to these rules. This gives you the flexibility and control of your data!

## My Device
I will be using a Raspberry Pi Pico W as my Microcontroller which will connect wirelessly and send off events to my data warehouse. For more information on this project's code or build check out my full blog post here.

## Code
```rgb.py``` is my main file which I execute on my Raspberry Pi.
The other files: ```myrequest.py```, ```wifi.py```, ```dht11.py``` are used within ```rgb.py``` and need to also be stored on the Raspberry Pi.