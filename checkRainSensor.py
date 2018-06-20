#!/usr/local/python/bin/python
"""
Plot the current status from the RPi rain sensors
"""
from collections import defaultdict
from datetime import datetime
import pymysql
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl
import numpy as np

# pylint: disable = invalid-name
# pylint: disable = redefined-outer-name

DB_HOST = '10.2.5.32'
DB_DATABASE = 'ngts_ops'
DB_USER = 'ops'

colours = [(206/250., 200/250., 170/250.),
           (203/250., 81/250., 205/250.),
           (213/250., 89/250., 52/250.),
           (135/250., 215/250., 83/250.),
           (210/250., 76/250., 121/250.)]

def getLastXhrs(tlim):
    """
    Grab the last X hours of rain sensor data
    """
    rs = defaultdict(list)
    times = []
    qry = """
        SELECT (bucket-UNIX_TIMESTAMP())/3600.0 AS trel,
        rs01, rs02, rs03, rs04, rs05
        FROM rpi_rg11_rain_sensors
        HAVING trel>%s
        """
    qry_args = (float(tlim)*-1, )
    with pymysql.connect(host=DB_HOST, db=DB_DATABASE, user=DB_USER) as cur:
        cur.execute(qry, qry_args)
        results = cur.fetchall()
    for row in results:
        times.append(float(row[0]))
        rs[1].append(int(row[1]))
        rs[2].append(int(row[2]))
        rs[3].append(int(row[3]))
        rs[4].append(int(row[4]))
        rs[5].append(int(row[5]))
    return times, rs

def plotRainSensor(outdir, tlim):
    """
    Make a plot of the 16 rain sensors
    """
    times, rs = getLastXhrs(tlim)
    pl.figure(1, figsize=(5, 5))
    ax = pl.subplot2grid((5, 4), (0, 0), colspan=5, rowspan=4)
    ax.set_color_cycle(colours)
    ax.set_xlim(-24, 5.2)
    ax.set_ylim(0, 1.1)
    for i in rs:
        ax.plot(times, np.abs((np.array(rs[i])-1)+(i*0.003)), '-')
    ax.set_xlabel('Hours since {}'.format(datetime.utcnow().replace(microsecond=0)))
    ax.set_ylabel('Rain (0=DRY, 1=WET)')
    pl.rc('legend', **{'fontsize':9})
    pl.legend(("01", "02", "03", "04", "05"),
              loc='upper right', numpoints=1)
    pl.savefig('{}/rpi_rain_sensor.png'.format(outdir),
               bbox_inches='tight')
)
if __name__ == "__main__":
    outdir = "/srv/www/ngts/monitor/flask-monitor/monitor/static"
    plotRainSensor(outdir, 24)
