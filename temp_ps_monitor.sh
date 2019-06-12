#!/bin/bash

status=`ps -efww | grep -w "temperature_logger.py" | grep -v grep | grep -v $$ | grep -w "root" | awk '{ print $2 }'`
if [ ! -z "$status" ]; then
    echo "[`date`] : Temperature monitor process already running...Exiting..."
            exit 1;
    else
            screen -dmS temperature /usr/bin/python /root/temperature_logger.py
                echo "[`date`] : No temperature monitor process found. Starting..."
        fi