## Raspberry Pi Rain Sensor

```rainsensor.py``` runs on the Raspberry Pi, it reads the sensors and logs the information in the database. It also checks in with centralHub.

```checkRainSensor.py``` runs on cron on the webserver and plots the rain values. 0=Dry and 1=Wet
