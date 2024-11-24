import os

# InfluxDB connection details
influxdb_url = os.getenv("INFLUX_URL")
database_name = os.getenv("INFLUX_DB")	
username = os.getenv("INFLUX_USER_W")	
password = os.getenv("INFLUX_PWD_W")