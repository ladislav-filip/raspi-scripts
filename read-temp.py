#!/usr/bin/env python
import requests

from decimal import Decimal
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from libs import custom_display, helper, logger
from libs.env_load import database_name, ha_password, ha_username, influxdb_url

customDisplay = custom_display.CustomDisplay()

def is_data_older_than_15_minutes(json_data, timezone_str="UTC"):
    """
    Kontroluje, zda jsou data v poskytnutém JSON starší než 15 minut.

    Argumenty:
        json_data (dict): JSON data obsahující časové informace.
        timezone_str (str, volitelný): Řetězec časového pásma, který má být použit 
        pro porovnání času. Výchozí hodnota je "UTC".

    Návratová hodnota:
        bool: True, pokud jsou data starší než 15 minut, jinak False.
        None: Pokud JSON neobsahuje očekávaná data nebo dojde k chybě při zpracování.

    Výjimky:
        Žádné: Tato funkce zpracovává výjimky interně a místo vyvolání je zaznamenává chyby.
    """
    try:
        # Kontrola, zda existují očekávané klíče
        results = json_data.get("results", [])
        if not results or "series" not in results[0]:
            logger.log_error("JSON neobsahuje data.")
            return None

        # Získání času z JSON
        time_str = results[0]["series"][0]["values"][0][0]  # Předpoklad: čas na indexu [0][0]
        return helper.is_data_older_than_minutes(time_str, 15, timezone_str)
    except (KeyError, IndexError, ValueError) as e:
        logger.log_error(f"Chyba při zpracování JSON: {e}")
        return None

def get_degree_value_from_response(response):
    result = response.json()
    # Extract the last value from the response
    if "series" in result["results"][0]:
        last_value = result["results"][0]["series"][0]["values"][0][1]
        logger.log_info(f"Poslední hodnota z měření 'teplota': {last_value}")
        formatted_number = custom_display.CustomDisplay.format_number_with_degree(last_value)

        if is_data_older_than_15_minutes(result):
            customDisplay.show("OLD")
            logger.log_info("Data je starší než 15 minut.")
        else:
            return formatted_number

    return None    

def get_last_value_from_influxdb(sensor):    
    # Query to get the last value from "teplota" measurement
    query = f"SELECT value FROM teplota WHERE sensor = '{sensor}' ORDER BY time DESC LIMIT 1"
    logger.log_info(f"Získávání poslední hodnoty z měření 'teplota' pro senzor '{sensor}'.")

    # Send GET request to InfluxDB API
    try:
        response = requests.get(
            f"{influxdb_url}/query",
            params={
                "db": database_name,
                "q": query
            },
            auth=(ha_username, ha_password),
            timeout=10  # Add a timeout of 10 seconds
        )

        return response
    except Exception as e:
        logger.log_error(f"Chyba při získávání dat z InfluxDB: {e}")

    return None

def main():
    response = get_last_value_from_influxdb("msr-mosnov")
    # log write response
    logger.log_info(f"Response: {response.text.encode('utf8')}")
    if response:
        value = get_degree_value_from_response(response)
        if value:
            customDisplay.show(value)
        else:
            customDisplay.show_error()
    else:
        customDisplay.show_error()

if __name__ == "__main__":
    main()