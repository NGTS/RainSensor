#!/usr/local/python/bin/python
import pymysql
from collections import defaultdict
from astropy.time import Time
import matplotlib.pyplot as pl
import argparse as ap
import numpy as np

colours=[(206/250.,200/250.,170/250.),
		(203/250.,81/250.,205/250.),
		(213/250.,89/250.,52/250.),
		(135/250.,215/250.,83/250.),
		(210/250.,76/250.,121/250.),
		(208/250.,180/250.,70/250.),
		(99/250.,140/250.,75/250.),
		(128/250.,121/250.,213/250.),
		(120/250.,153/250.,179/250.),
		(167/250.,118/250.,92/250.),
		(120/250.,214/250.,181/250.),
		(193/250.,128/250.,174/250.)]

def argParse():
	description='''Script to check the rain sensor calibration and plot the sensor values'''
	parser=ap.ArgumentParser(description=description)
	parser.add_argument('--check',type=int,help="check the sensors for last X hours")
	parser.add_argument('--plot',type=int,help="plot sensor values for last X hours")
	return parser.parse_args()

def getLastXhrs(tlim):
	conn=pymysql.connect(host='ds',db='ngts_ops')
	cur=conn.cursor()
	rs=defaultdict(list)
	times=[]
	qry="SELECT (bucket-UNIX_TIMESTAMP())/3600.0 AS trel,rs01,rs02,rs03,rs04,rs05,rs06,rs07,rs08,rs09,rs10,rs11,rs12,rs13,rs14,rs15,rs16 FROM rpi_rain_sensor HAVING trel>-%d" % (tlim)
	cur.execute(qry)
	for row in cur:
		times.append(row[0])
		rs[1].append(row[1])
		rs[2].append(row[2])
		rs[3].append(row[3])
		rs[4].append(row[4])
		rs[5].append(row[5])
		rs[6].append(row[6])
		rs[7].append(row[7])
		rs[8].append(row[8])
		rs[9].append(row[9])
		rs[10].append(row[10])
		rs[11].append(row[11])
		rs[12].append(row[12])
		rs[13].append(row[13])
		rs[14].append(row[14])
		rs[15].append(row[15])
		rs[16].append(row[16])
	return times,rs

def checkRainSensor(tlim):
	times,rs=getLastXhrs(tlim)
	for i in rs:
		if 0 in rs[i]:
			print "Faulty Sensor: %d" % (i)

def plotRainSensor(tlim):
	times,rs=getLastXhrs(tlim)
	fig=pl.figure(1,figsize=(5,5))
	ax=pl.subplot2grid((5,4),(0,0),colspan=5,rowspan=4)
	ax.set_color_cycle(colours)
	ax.set_xlim(-24,5)
	ax.set_ylim(0,1.1)
	for i in rs:
		ax.plot(times,np.abs((np.array(rs[i])-1)+(i*0.003)),'-')
	ax.set_xlabel('Hours ago')
	ax.set_ylabel('Rain (0=DRY, 1=WET)')
	pl.rc('legend',**{'fontsize':9})
	pl.legend(("01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16"),loc='upper right',numpoints=1)
	pl.savefig('/home/ops/ngts/prism/monitor/img/rpi_rain_sensor.png',bbox_inches='tight')


if __name__=="__main__":
	args=argParse()
	if args.check: 
		checkRainSensor(args.check)
	if args.plot:
		plotRainSensor(args.plot)


