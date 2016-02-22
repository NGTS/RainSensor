#!/usr/bin/python
# start name server with
# python -m Pyro4.naming -n 10.2.5.107

import Pyro4
from collections import defaultdict
import RPi.GPIO as g
import time
import datetime
import pymysql

SLEEP_TIME = 5

class RainSensor(object):
    
	def __init__(self):
		"""Sets up the output dict and GPIO pin mode"""
		self._running = True
		self.rs=defaultdict(list)
		g.setmode(g.BCM)

	def running(self):
		"""Returns false if the daemon should be terminated"""
		return self._running

	def get_rain(self, name):
		"""Returns the rain sensor values in a dict"""
		gpio_nums=[18,23,4,17,27,22,10,9,11,5,6,13,19,26,20,21]
		for i in gpio_nums:
			g.setup(i,g.IN)
		for i in range(0,len(gpio_nums)):
			self.rs[(i+1)]=g.input(gpio_nums[i])
		return self.rs

def update_rain_info(sensor, time_value):
	host = 'ds'
	db = 'ngts_ops'
	user = 'ops'

	rs = sensor.get_rain('test')
	bucket=(int(time_value)/60)*60
	tsample=datetime.datetime.utcnow().isoformat().replace('T',' ')[:-7] # remove microseconds

	qry= "REPLACE INTO rpi_rain_sensor (tsample,bucket,rs01,rs02,rs03,rs04,rs05,rs06,rs07,rs08,rs09,rs10,rs11,rs12,rs13,rs14,rs15,rs16) VALUES ('%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)"
	params = (tsample,bucket,rs[1],rs[2],rs[3],rs[4],rs[5],rs[6],rs[7],rs[8],rs[9],rs[10],rs[11],rs[12],rs[13],rs[14],rs[15],rs[16])

	with pymysql.connect(host=host, db=db, user=user) as cursor:
		cursor.execute(qry, params)

def rain_sensor_watcher(sensor):
	# Connect to central hub
	hub = Pyro4.Proxy('PYRONAME:central.hub')
	try:
		hub.startThread('Rain Sensors')
	except Exception as err:
		print('Cannot connect to central hub')
		raise

	while True:
		# Store this time value for updating
		time_value = time.time()

		# Inform the central hub that it's working
		hub.update_rain(time_value)

		# Upload rain info to the database
		update_rain_info(sensor, time_value)

		time.sleep(SLEEP_TIME)



if __name__ == '__main__':
	sensor = RainSensor()
	rain_sensor_watcher(sensor)

# vim: set noexpandtab ts=4:
