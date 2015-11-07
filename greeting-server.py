# saved as greeting-server.py
import Pyro4
from collections import defaultdict
import RPi.GPIO as g

class RainSensor(object):
    def get_rain(self, name):
		rs=defaultdict(list)
		g.setmode(g.BCM)
		gpio_nums=[18,23,4,17,27,22,10,9,11,5,6,13,19,26,20,21]
		for i in gpio_nums:
			g.setup(i,g.IN)
		for i in range(0,len(gpio_nums)):
			rs[(i+1)]=g.input(gpio_nums[i])
		return rs

daemon = Pyro4.Daemon("10.2.5.107")                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(RainSensor)   # register the greeting maker as a Pyro object
ns.register("example.sensor", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls

# start name server with
# python -m Pyro4.naming -n 10.2.5.107