#!/usr/bin/python
# start name server with
# python -m Pyro4.naming -n 10.2.5.107

import Pyro4
from collections import defaultdict
import RPi.GPIO as g
import time
import datetime
import pymysql
import argparse
import logging

SLEEP_TIME = 5

logging.basicConfig(
    level='INFO', format='%(asctime)s : %(message)s')
logger = logging.getLogger(__name__)

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

	logger.debug('Fetching rain sensor measurements')
	rs = sensor.get_rain('test')
	bucket=(int(time_value)/60)*60
	tsample=datetime.datetime.utcnow().isoformat().replace('T',' ')[:-7] # remove microseconds

	qry= "REPLACE INTO rpi_rain_sensor (tsample,bucket,rs01,rs02,rs03,rs04,rs05,rs06,rs07,rs08,rs09,rs10,rs11,rs12,rs13,rs14,rs15,rs16) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	params = (tsample,bucket,rs[1],rs[2],rs[3],rs[4],rs[5],rs[6],rs[7],rs[8],rs[9],rs[10],rs[11],rs[12],rs[13],rs[14],rs[15],rs[16])

	with pymysql.connect(host=host, db=db, user=user) as cursor:
		logger.debug('Updating database: %s : %s', qry, params)
		cursor.execute(qry, params)
		# implicit commit

class NullHub(object):
	'''
	Null object to wrap the lack of a central hub
	'''
	def startThread(self, name): pass
	def update_rain(self, time_value): pass

def rain_sensor_watcher(sensor, communicate_with_hub):
	# Connect to central hub
	if communicate_with_hub:
		logger.debug('Connecting to central hub')
		hub = Pyro4.Proxy('PYRONAME:central.hub')
	else:
		logger.debug('Not communicating with central hub')
		hub = NullHub()

	try:
		hub.startThread('Rain Sensors')
	except Exception as err:
		logger.exception('Cannot connect to central hub')
		raise

	while True:
		# Store this time value for updating
		time_value = time.time()

		# Inform the central hub that it's working
		hub.update_rain(time_value)

		# Upload rain info to the database
		update_rain_info(sensor, time_value)

		logger.debug('Sleeping for %s seconds', SLEEP_TIME)
		time.sleep(SLEEP_TIME)


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verbose', action='store_true')
	parser.add_argument('--nohub', action='store_true', help='Do not communicate with central hub server')
	return parser.parse_args()

if __name__ == '__main__':
	args = get_args()
	if args.verbose:
		logger.setLevel('DEBUG')
	sensor = RainSensor()
	rain_sensor_watcher(sensor, communicate_with_hub=not args.nohub)

# vim: set noexpandtab ts=4 sw=4:
