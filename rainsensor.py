#!/usr/bin/python
"""
Raspberry Pi rain sensors

start name server with:
python -m Pyro4.naming -n 10.2.5.107
"""
import time
import datetime
import argparse
import logging
from collections import defaultdict
import Pyro4
import RPi.GPIO as g
import pymysql

# pylint: disable = invalid-name

SLEEP_TIME = 5

logging.basicConfig(
    level='INFO', format='%(asctime)s : %(message)s')
logger = logging.getLogger(__name__)

class RainSensor(object):
    """
    Rain sensor class
    """
    def __init__(self):
        """Sets up the output dict and GPIO pin mode"""
        self._running = True
        self.rs = defaultdict(list)
        g.setmode(g.BCM)
        self.gpio_nums = [2, 3, 4, 5, 6]
        for i in self.gpio_nums:
            if i == 2 or i == 3:
                g.setup(i, g.IN)
            else:
                g.setup(i, g.IN, pull_up_down=g.PUD_UP)

    def running(self):
        """Returns false if the daemon should be terminated"""
        return self._running

    def get_rain(self):
        """Returns the rain sensor values in a dict"""
        for i in range(0, len(self.gpio_nums)):
            self.rs[(i+1)] = g.input(self.gpio_nums[i])
        print(self.rs)
        return self.rs

def update_rain_info(sensor, time_value):
    """
    Log the rain sensor information
    """
    host = '10.2.5.32'
    db = 'ngts_ops'
    user = 'ops'
    logger.debug('Fetching rain sensor measurements')
    rs = sensor.get_rain()
    bucket = (int(time_value)/60)*60
    tsample = datetime.datetime.utcnow().isoformat().replace('T', ' ')[:-7] # remove microseconds

    qry = """
         REPLACE INTO rpi_rg11_rain_sensors
         (tsample, bucket, rs01, rs02, rs03, rs04, rs05)
         VALUES
         (%s, %s, %s, %s, %s, %s, %s)
         """
    # forcing final three sensors to be 0 for now
    params = (tsample, bucket, rs[1], rs[2], rs[3], rs[4], rs[5])
    with pymysql.connect(host=host, db=db, user=user) as cursor:
        logger.debug('Updating database: %s : %s', qry, params)
        cursor.execute(qry, params)

def rain_sensor_watcher(sensor):
    """
    Set up the rain sensor watcher
    """
    # Connect to central hub
    logger.debug('Connecting to central hub')
    hub = Pyro4.Proxy('PYRONAME:central.hub')
    logger.debug('Entering main loop')
    while True:
        # Inform the central hub that it's working
        hub.report_in('rain_sensor')
        # Upload rain info to the database
        update_rain_info(sensor, time.time())
        logger.debug('Sleeping for %s seconds', SLEEP_TIME)
        time.sleep(SLEEP_TIME)

def argParse():
    """
    Parse the command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    args = argParse()
    if args.verbose:
        logger.setLevel('DEBUG')
    sensor = RainSensor()
    rain_sensor_watcher(sensor)
