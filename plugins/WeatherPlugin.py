#!/usr/bin/env python

from Module import *
import forecastio
import time



####################################################################
# 
# 
####################################################################
class Plugin(Module):
	def __init__(self):
		Module.__init__(self,'weather')
		api_key = self.info['FORECAST_API_KEY']
	
		if api_key is None:
			self.logger.error('Need Forecast.io token, exiting now ...')
			exit()

		# Latitude, Longitude for location
		lat = self.info['Geolocation']['LATITUDE']
		long = self.info['Geolocation']['LONGITUDE']  
	
		self.forecast = forecastio.load_forecast(api_key, lat, long)
		self.weather_time = time.gmtime()
		
		#self.intent = 'weather'
	
	"""
	Grab a forcast
	in: day of week (0-6) to grab weather forecast and json info
	out: forecast txt
	"""
	def grabWeatherDay(self,day):
		j = self.forecast.json
		
		high = int(round(j['daily']['data'][day]['apparentTemperatureMax'],0))
		low = int(round(j['daily']['data'][day]['apparentTemperatureMin'],0))
		clouds = int(round(j['daily']['data'][day]['cloudCover']*100.0,0))
		sum = j['daily']['summary']
		wind = int(round(j['daily']['data'][day]['windSpeed'],0))
	
		days = ['today','tomorrow', 'there']
	
		if day > 2:
			day = 2
	
		resp = '%s will be a high of %d and low of %d with %d percent clouds and %d mile per hour winds'%(days[day],high,low,clouds,wind)
	
		return resp

	"""
	Handles the weather request. If the last one isn't too old, it just uses that one.
	in: what day (now, tomorrow, today, etc)
	out: txt response
	todo: 
	"""
	def process(self, entity):	
		resp = ''
		w_time = 'today'
		
		if 'datetime' in entity: 
			w_time = entity['datetime']['body']
	
		# convert time to seconds from epoch and div by 60 for minutes
		now = time.localtime()
		diff = (time.mktime(self.weather_time) - time.mktime(now))/60
		
		j = self.forecast.json
		
		# update if it has been too long
		if diff > 5:
			self.forecast.update()
			j = self.forecast.json
			self.weather_time = now
	
		if w_time == 'tomorrow':
			resp = self.grabWeatherDay(1)
		
		elif w_time == 'today':
			resp = self.grabWeatherDay(0)
		
		elif w_time == 'this week':
			resp =  j['daily']['summary']
		
		else:
			temp = j['currently']['apparentTemperature']
			rain = j['currently']['precipProbability']*100.0	
			resp = 'The weather is currently %d degrees with %d percent chance of rain'%(temp,rain)
		
		return resp


if __name__ == '__main__':
	w = Plugin()
	print w.process({})