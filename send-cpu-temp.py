#!/usr/bin/env python

import os
import requests

# InfluxDB connection details
influxdb_url = os.getenv("INFLUX_URL")
database_name = os.getenv("INFLUX_DB")	
username = os.getenv("INFLUX_USER_W")	
password = os.getenv("INFLUX_PWD_W")

def get_cpu_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return temp.replace("temp=", "").replace("'C\n", "")

url = f"{influxdb_url}/write?u={username}&p={password}&db={database_name}"
print(url)

temp_c = get_cpu_temp()

payload = "teplota,sensor=raspi4 value=" + str(temp_c)
headers = {
  'Content-Type': 'text/plain'
}
response = requests.request("POST", url, headers=headers, data = payload)
print(response.text.encode('utf8'))
