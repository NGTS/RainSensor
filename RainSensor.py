# script to poll the RPi rain sensor

import RPi.GPIO as g
import time

g.setmode(g.BCM)
g.setup(2,g.IN) # RS01
g.setup(3,g.IN) # RS02
g.setup(4,g.IN) # RS03
g.setup(17,g.IN) # RS04

g.setup(27,g.IN) # RS05
g.setup(22,g.IN) # RS06
g.setup(10,g.IN) # RS07
g.setup(9,g.IN) # RS08

g.setup(11,g.IN) # RS09
g.setup(5,g.IN) # RS10
g.setup(6,g.IN) # RS11
g.setup(13,g.IN) # RS12

g.setup(19,g.IN) # RS13
g.setup(26,g.IN) # RS14
g.setup(20,g.IN) # RS15
g.setup(21,g.IN) # RS16

rs={}
gpio_nums=[2,3,4,17,27,22,10,9,11,5,6,13,19,26,20,21]

while(1):
	sensor_alert=""
	for i in range(0,len(gpio_nums)):
		r=g.input(gpio_nums[i])
		if r != 0:
			sensor_alert="%s," % (gpio_nums[i])
	if len(sensor_alert) == 0:
		print "DRY"
	else:
		print sensor_alert[:-1]
	time.sleep(2)