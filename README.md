# pi-temperature-logger

pi-temperature-logger is designed to run on a raspberry pi with a DS18B20 temperature sensor. It will read the current temperature in celcius format, convert it to farenheit, and send both values to an influxDB instance.

### Download & Setup

* git clone https://github.com/kdim953/pi-temperature-logger.git

* pip install -r requirements.txt

### Configuration

##### Edit temperature-logger.py
* INFLUX_HOST: IP/Hostname of InfluxDB instance
* HOST: Local hostname of reader reported to InfluxDB
* PORT: InfluxDB port
* DBNAME: Name of database
* USER: InfluxDB username
* PASSWORD: InfluxDB password
* TEMP_SENSOR: Location of temp sensor raw file
* READ_SLEEP: Time in between each temperature reading in seconds

### Running
* ```screen -dmS temperature python temperature_logger.py```
OR
* Use the included bash script to monitor the process:
  * ```crontab -e root```
  * ```*/1 * * * * /PATH_TO_REPO/temp_ps_monitor.sh >/dev/null 2>&1```