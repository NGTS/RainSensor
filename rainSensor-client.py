#!/usr/local/python/bin/python
from datetime import datetime 
import Pyro4, sys, time, pymysql, logging, getpass
import argparse as ap

def argParse():
	parser=ap.ArgumentParser()
	parser.add_argument('--v',help='increase verbosity',action='store_true')
	parser.add_argument('--debug',help='run in debugging mode',action='store_true')
	return parser.parse_args()

# parse arguments
args=argParse()

# whoami?
me=getpass.getuser()

# initial setup
if me == "James":
	if not args.debug:
		db=pymysql.connect(host='localhost',db='ngts_prep')
		cur=conn.cursor()
	logfile="/Users/James/Desktop/www_cron/getRainSensors.log"
elif me=="ops":
	if not args.debug:
		conn=pymysql.connect(host='ds',db='ngts_ops')
		cur=conn.cursor()
	logfile="/usr/local/cron/logs/getRainSensors.log"
else:
	print "WHOAMI!?"
	sys.exit(1)

# connect to RPi via Pyro	
# use name server object lookup uri shortcut
getRain = Pyro4.Proxy("PYRONAME:example.sensor")  

# loop 'forever'
while(1):
	rs=getRain.get_rain('test')
	if args.v:
		print rs

	# generate time stamps
	bucket=(int(time.time())/60)*60
	tsample=datetime.utcnow().isoformat().replace('T',' ')[:-7] # remove microseconds

	# update the database
	qry="REPLACE INTO rpi_rain_sensor (tsample,bucket,rs01,rs02,rs03,rs04,rs05,rs06,rs07,rs08,rs09,rs10,rs11,rs12,rs13,rs14,rs15,rs16) VALUES ('%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)" % (tsample,bucket,rs[1],rs[2],rs[3],rs[4],rs[5],rs[6],rs[7],rs[8],rs[9],rs[10],rs[11],rs[12],rs[13],rs[14],rs[15],rs[16])
	if args.v:
		print qry

	if not args.debug:
		cur.execute(qry)
		conn.commit()

	#  wait for a few sec
	time.sleep(5)

