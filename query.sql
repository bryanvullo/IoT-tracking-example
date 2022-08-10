SELECT app_id, events.collector_tstamp, sat.satisfaction_rating, sensors.temperature, sensors.humidity, 
weather.temperature_celsius, weather.windspeed, weather.humidity, weather.pressure, weather.conditions
	FROM atomic.events
	LEFT JOIN atomic.com_myvendor_satisfaction_1 AS sat ON events.event_id = sat.root_id 
	LEFT JOIN atomic.com_myvendor_sensors_2 AS sensors ON events.event_id = sensors.root_id
	LEFT JOIN atomic.com_myvendor_weather_1 AS weather ON events.event_id = weather.root_id
	WHERE events.collector_tstamp >= '2022-08-02T00:00:00Z' 
	ORDER BY events.collector_tstamp DESC