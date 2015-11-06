# saved as greeting-server.py
import Pyro4
from collections import defaultdict
import RPi.GPIO as g

class GreetingMaker(object):
    def get_fortune(self, name):
		rs=defaultdict(list)
		g.setmode(g.BCM)
		gpio_nums=[2,3,4,17,27,22,10,9,11,5,6,13,19,26,20,21]
		for i in gpio_nums:
			g.setup(i,g.IN)
		for i in range(0,len(gpio_nums)):
			rs[(i+1)]=g.input(gpio_nums[i])
		return rs

daemon = Pyro4.Daemon("10.2.5.107")                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(GreetingMaker)   # register the greeting maker as a Pyro object
ns.register("example.greeting", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls