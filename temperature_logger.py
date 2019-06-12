#! /usr/bin/env python

"""Reads temperature from DS18B20 and sends to influxDB"""

import os
import time
from influxdb import InfluxDBClient

## BEGIN CONFIGURATION
INFLUX_HOST = '1.1.1.1'
HOST = 'PI_HOSTNAME'
PORT = 8086
DBNAME = 'temperature'
USER = 'pi'
PASSWORD = 'SOMEPASSWORD'
TEMP_SENSOR = '/sys/bus/w1/devices/SOME_NUMBER/w1_slave'
READ_SLEEP = 1
## END CONFIGURATION

def main():
    """Create DB connection, read temperature and write to DB"""
    client = InfluxDBClient(INFLUX_HOST, PORT, USER, PASSWORD, DBNAME)
    client.create_database(DBNAME)

    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    while True:
        json_body = get_data_points()
        client.write_points(json_body)
        _ok(json_body)
        time.sleep(READ_SLEEP)

def temp_raw():
    """Read temperature from sensor"""
    read_file = open(TEMP_SENSOR, 'r')
    lines = read_file.readlines()
    read_file.close()
    return lines

def read_temp_celcius():
    """Cleanup raw temperature reading"""
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_float = float(temp_string) / 1000.0
        final_temp_c = round(temp_float, 2)
        return final_temp_c

def convert_temp_farhenheit(temperature_c):
    """Convert Celsius to Farhenheit"""
    temp_f = 9.0/5.0 * temperature_c + 32
    converted_temp = float(round(temp_f, 2))
    return converted_temp

def get_data_points():
    """Construct JSON to send to DB"""
    temperature_c = read_temp_celcius()
    temperature_f = convert_temp_farhenheit(temperature_c)
    #iso = time.ctime()
    # Use UTC for db entry
    iso = time.asctime(time.gmtime())
    json_body = [{
        "measurement": "temperature",
        "tags": {"host": HOST},
        "time": iso,
        "fields": {
            "temp_c": temperature_c,
            "temp_f": temperature_f,
        }
    }]
    return json_body

# Formatters
def _info(msg):
    print '* %s' % msg

def _ok(msg):
    green = '\033[1;32m{0}\033[00m'
    print green.format('+ %s' % msg)

def _warn(msg):
    yellow = '\033[01;33m{0}\033[00m'
    print yellow.format('- %s' % msg)

def _error(msg):
    red = '\033[01;31m{0}\033[00m'
    print red.format('- %s' % msg)

if __name__ == '__main__':
    main()
