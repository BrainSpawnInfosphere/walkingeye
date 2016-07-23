#!/usr/bin/env python

import Module as mod
import forecastio  # change to yahoo??
import time
import os


class Plugin(mod.Module):
	def __init__(self, API_KEY=None, geo=None):
		mod.Module.__init__(self, 'weather')
		if API_KEY is None: API_KEY = os.getenv('FORECAST_IO')
		api_key = API_KEY  # self.info['FORECAST_API_KEY']

		if geo is None:
			geo = {}
			geo['latitude'] = os.getenv('FORECAST_LATITUDE')
			geo['longitude'] = os.getenv('FORECAST_LONGITUDE')

		# if api_key is None:
		# 	self.logger.error('Need Forecast.io token, exiting now ...')
		# 	exit()

		# Latitude, Longitude for location
		# lat = self.info['Geolocation']['LATITUDE']
		# long = self.info['Geolocation']['LONGITUDE']

		self.forecast = forecastio.load_forecast(api_key, geo['latitude'], geo['longitude'])
		self.weather_time = time.localtime()

		# self.intent = 'weather'

	def grabWeatherDay(self, day):
		"""
		Grab a forcast
		in: day of week (0-6) to grab weather forecast and json info
		out: forecast txt
		"""
		j = self.forecast.json

		high = int(round(j['daily']['data'][day]['apparentTemperatureMax'],0))
		low = int(round(j['daily']['data'][day]['apparentTemperatureMin'],0))
		clouds = int(round(j['daily']['data'][day]['cloudCover']*100.0,0))
		sum = j['daily']['summary']
		wind = int(round(j['daily']['data'][day]['windSpeed'],0))

		days = ['today','tomorrow', 'there']

		if day > 2:
			day = 2

		resp = '{0!s} will be a high of {1:d} and low of {2:d} with {3:d} percent clouds and {4:d} mile per hour winds'.format(days[day], high, low, clouds, wind)

		return resp


	def process(self, entity):
		"""
		Handles the weather request. If the last one isn't too old, it just uses that one.
		in: entity {"datetime": [{
				"grain": "day",
				"type": "value",
				"value": "2015-03-04T00:00:00.000-08:00"
			}]}
		out: txt response
		"""

		resp = ''

		# last time forecast.io was called
		now = time.localtime()
		diff = (time.mktime(now) - time.mktime(self.weather_time)) / 60
		# print 'diff', diff

		# grab the json info
		j = self.forecast.json

		# update if it has been too long ... 5 mins
		if diff > 5:
			self.forecast.update()
			j = self.forecast.json
			self.weather_time = now
			print 'update'

		# get weather asked for: today, tomorrow, monday, sunday, etc
		if 'datetime' in entity:
			t = entity['datetime'][0]['value']
			asked = time.strptime(t.split('.')[0],'%Y-%m-%dT%H:%M:%S')

			# get how many days in future
			w_time = asked.tm_mday - now.tm_mday
			if w_time >= 0 or w_time < 7: resp = self.grabWeatherDay( int( w_time ) )

		else:
			temp = j['currently']['apparentTemperature']
			rain = j['currently']['precipProbability']*100.0
			resp = 'The weather is currently {0:d} degrees with {1:d} percent chance of rain'.format(temp, rain)

		return resp


if __name__ == '__main__':
	geo = {
		'latitude': 38.8,
		'longitude': -104.8
	}
	token = os.getenv('FORECAST_IO')
	w = Plugin(token, geo)
	print w.process({})
