import os

# InfluxDB connection details
influxdb_url = os.getenv("INFLUX_URL")
database_name = os.getenv("INFLUX_DB")
username = os.getenv("INFLUX_USER_W")
password = os.getenv("INFLUX_PWD_W")
ha_username = os.getenv("HA_USER")
ha_password = os.getenv("HA_PASSWORD")
