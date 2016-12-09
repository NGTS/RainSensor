## Raspberry Pi Rain Sensor

* checkRainSensor   - script to calibrate and poll the rain sensors
* rainsensor.py - script for running the rain sensor.

## Usage

Command line options for `rainsensor.py`:

* `-v/--verbose`: verbose mode
* `--nohub`: do not connect to Pyro monitor server

Commands line aoptions for `checkRainSensor.py`

* `--check X`: check the rain sensor calibration for the past X hours
* `--plot X`: plot the rain sensor data for the past X hours
