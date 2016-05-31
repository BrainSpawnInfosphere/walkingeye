#!/usr/bin/env python

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import plugins.DatePlugin as dt
import plugins.RandomPlugin as ran
import plugins.WeatherPlugin as weather
import plugins.TimePlugin as Time
import plugins.ExitPlugin as bye


def check(a, b):
	assert a == b


def test_random():
	p = ran.Plugin()
	for topic in ['greeting', 'feelings', 'error', 'joke', 'mean']:
		yield check, p.handleIntent(topic), isinstance(p.process(0), basestring)
		# assert typeplg.


def test_exit():
	b = bye.Plugin()
	ans = b.process(0)
	assert ans is 'exit_loop' and b.handleIntent('safe_word')


def test_time():
	t = Time.Plugin()
	ans = t.process(0)
	assert isinstance(ans, basestring) and t.handleIntent('time')


def test_date():
	d = dt.Plugin()
	ans = d.process(0)
	assert isinstance(ans, basestring) and d.handleIntent('date')


def test_weather():
	geo = {
		'latitude': 38.8,
		'longitude': -104.8
	}
	token = os.getenv('FORECAST_IO')
	w = weather.Plugin(token, geo)
	ans = w.process({})
	assert isinstance(ans, basestring) and w.handleIntent('weather')
