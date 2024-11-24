#!/usr/bin/env python

"""
Měření teploty CPU Raspberry Pi a odesílání dat do InfluxDB.

Tento skript čte teplotu CPU z Raspberry Pi pomocí příkazu vcgencmd
a odesílá naměřené hodnoty do instance InfluxDB pro další zpracování.
"""

import os
import requests
from libs import logger
from libs.env_load import influxdb_url, database_name, username, password

# check if all environment variable exists
if influxdb_url is None or database_name is None or username is None or password is None:
    logger.log_error("Some of the environment variables are not set.")
    exit(1)

def get_cpu_temp():
    """
    Získá aktuální teplotu CPU Raspberry Pi.

    Tato funkce spustí příkaz `vcgencmd measure_temp` pro získání teploty CPU,
    přečte výstup a zpracuje jej, aby vrátila teplotu jako řetězec.

    Návratová hodnota:
      str: Aktuální teplota CPU v Celsiích.
    """
    temp = os.popen("vcgencmd measure_temp").readline()
    return temp.replace("temp=", "").replace("'C\n", "")

def send_data(data_payload, headers):
    """
    Odesílá data do instance InfluxDB.

    Tato funkce sestaví URL pomocí poskytnutých přihlašovacích údajů InfluxDB a názvu databáze,
    poté odešle POST požadavek s daným payloadem na endpoint pro zápis do InfluxDB. Zaloguje
    URL (s maskovaným heslem) a odpověď ze serveru.

    Argumenty:
      data_payload (str): Data, která mají být odeslána do instance InfluxDB.

    Návratová hodnota:
      bool: True, pokud byla data úspěšně odeslána, False v opačném případě.

    Výjimky:
      requests.exceptions.ConnectionError: Pokud dojde k chybě připojení při odesílání požadavku.
      Exception: Pro jakékoli jiné výjimky, které nastanou během požadavku.
    """
    url = f"{influxdb_url}/write?u={username}&p={password}&db={database_name}"
    url_for_log = f"{influxdb_url}/write?u={username}&p=******&db={database_name}"
    logger.log_info(f"URL: {url_for_log}")
    try:
        response = requests.request("POST", url, headers=headers, data = data_payload)
        logger.log_info(f"Response: {response.text.encode('utf8')}")
        return True
    except requests.exceptions.ConnectionError as e:
        logger.log_error(f"Connection error: {e}")
    except Exception as e:
        logger.log_error(f"Unknown error: {e}")
    return False

def main():
    """
    Hlavní funkce pro získání teploty CPU a odeslání jako payload.

    Tato funkce získá teplotu CPU, naformátuje ji do řetězce payloadu
    a odešle data pomocí funkce send_data.

    Návratová hodnota:
      None
    """
    temp_c = get_cpu_temp()

    payload = "teplota,sensor=raspi4 value=" + str(temp_c)
    headers = {
      'Content-Type': 'text/plain'
    }

    send_data(payload, headers)

if __name__ == "__main__":
    main()
