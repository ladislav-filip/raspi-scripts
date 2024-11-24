#!/usr/bin/env python
#
# Načtení teploty z CPU a odeslání do InfluxDB
#
#
#

import os
import requests
from libs import logger
from libs.env_load import influxdb_url, database_name, username, password

# check if all environment variable exists
if influxdb_url is None or database_name is None or username is None or password is None:
    logger.log_error("Some of the environment variables are not set.")
    exit(1)

# get CPU temperature
def get_cpu_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return temp.replace("temp=", "").replace("'C\n", "")

# send data to InfluxDB
def send_data(payload):
    url = f"{influxdb_url}/write?u={username}&p={password}&db={database_name}"
    url_for_log = f"{influxdb_url}/write?u={username}&p=******&db={database_name}"
    logger.log_info(f"URL: {url_for_log}")
    try:
      response = requests.request("POST", url, headers=headers, data = payload)
      logger.log_info(f"Response: {response.text.encode('utf8')}")
      return True
    except requests.exceptions.ConnectionError as e:
      logger.log_error(f"Connection error: {e}")
    except Exception as e:
      logger.log_error(f"Unknown error: {e}")
    return False

temp_c = get_cpu_temp()

payload = "teplota,sensor=raspi4 value=" + str(temp_c)
headers = {
  'Content-Type': 'text/plain'
}

send_data(payload)
