#!/usr/bin/python
# start name server with
# python -m Pyro4.naming -n 10.2.5.107

import Pyro4
from collections import defaultdict
import RPi.GPIO as g

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

if __name__ == '__main__':
	# make a Pyro daemon
	daemon = Pyro4.Daemon("10.2.5.32")                
	rain_sensor=RainSensor()
	# find the name server
	ns = Pyro4.locateNS()      
	# register the greeting maker as a Pyro object            
	uri = daemon.register(RainSensor)   
	# register the object with a name in the name server
	ns.register("example.sensor", uri)   
	
	print("Ready.")
	# start the event loop of the server to wait for calls
	daemon.requestLoop(loopCondition=rain_sensor.running)
