import pymysql
from collections import defaultdict

def checkRainSensor():
	conn=pymysql.connect(host='ds',db='ngts_ops')
	cur=conn.cursor()
	rs=defaultdict(list)
	qry="SELECT * FROM rpi_rain_sensor"
	cur.execut(qry)
	for row in cur:
		rs[1].append(row[2])
		rs[2].append(row[3])
		rs[3].append(row[4])
		rs[4].append(row[5])
		rs[5].append(row[6])
		rs[6].append(row[7])
		rs[7].append(row[8])
		rs[8].append(row[9])
		rs[9].append(row[10])
		rs[10].append(row[11])
		rs[11].append(row[12])
		rs[12].append(row[13])
		rs[13].append(row[14])
		rs[14].append(row[15])
		rs[15].append(row[16])
		rs[16].append(row[17])
	for i in rs:
		if 0 in rs[i]:
			print "Faulty Sensor: %d" % (i)

if __name__=="__main__":
	checkRainSensor()