#!/usr/bin/env python

import os
import json
import requests
import tm1637
from decimal import Decimal
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo 

# Nastavení pinů, které jste použili pro připojení DIO a CLK
CLK = 18
DIO = 17

# Inicializace displeje
display = tm1637.TM1637(clk=CLK, dio=DIO)

# Nastavení jasu (volitelně, rozsah 0-7)
display.brightness(1)


def format_number_for_display(number):
    # Rozdělení čísla na celé a desetinné části
    integer_part = int(number)
    decimal_part = int((number - integer_part) * 100)
    
    # Zformátování čísla na text pro zobrazení na displeji
    formatted_number = f"{integer_part}{decimal_part:02d}"
    return formatted_number

def format_number_with_degree(number):
    # Získání celého čísla
    integer_part = int(round(number))
    
    # Kontrola rozsahu a formátování na řetězec o délce 4 znaků
    if -50 <= integer_part <= 80:
        formatted_number = f"{integer_part: >3}*"  # Formátování na tříznakové číslo s mezerami zleva a přidání '*'
    else:
        raise ValueError("Number out of range -30 to 40")
    
    return formatted_number    


def is_data_older_than_15_minutes(json_data, timezone_str="UTC"):
    """
    Ověří, zda čas v JSON odpovědi je starší než 5 minut, s podporou časových zón.
    
    :param json_data: JSON odpověď jako Python slovník
    :param timezone_str: Řetězec definující časovou zónu (např. "Europe/Prague")
    :return: True, pokud je čas starší než 5 minut, False pokud není, None pokud je JSON nevalidní.
    """
    try:
        # Nastavení časové zóny
        tz = ZoneInfo(timezone_str)

        # Kontrola, zda existují očekávané klíče
        results = json_data.get("results", [])
        if not results or "series" not in results[0]:
            print("JSON neobsahuje data.")
            return None

        # Získání času z JSON
        time_str = results[0]["series"][0]["values"][0][0]  # Předpoklad: čas na indexu [0][0]
        time_str = time_str.split(".")[0]  # Odstranění desetinných míst
        print(f"Čas z JSON: {time_str}")

        # Převod času na datetime objekt
        measurement_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
        # Nastavení časové zóny na UTC (čas v JSON je obvykle v UTC)
        measurement_time = measurement_time.replace(tzinfo=ZoneInfo("UTC"))

        # Aktuální čas v dané časové zóně
        current_time = datetime.now(tz)
        print(f"Aktuální čas: {current_time}")

        # Výpočet rozdílu
        time_difference = current_time - measurement_time
        return time_difference > timedelta(minutes=15)

    except (KeyError, IndexError, ValueError) as e:
        print(f"Chyba při zpracování JSON: {e}")
        return None


# InfluxDB connection details
influxdb_url = os.getenv("INFLUX_URL")
database_name = os.getenv("INFLUX_DB")	
username = os.getenv("HA_USER")	
password = os.getenv("HA_PASSWORD")

# Query to get the last value from "teplota" measurement
query = "SELECT value FROM teplota WHERE sensor = 'garden' ORDER BY time DESC LIMIT 1"

# Send GET request to InfluxDB API
response = requests.get(
    f"{influxdb_url}/query",
    params={
        "db": database_name,
        "q": query
    },
    auth=(username, password)
)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    result = response.json()

    # Vypsání formátovaného JSON
    #print("Formátovaný JSON odpovědi:")
    #print(json.dumps(result, indent=4, ensure_ascii=False))

    # Extract the last value from the response
    if "series" in result["results"][0]:
        last_value = result["results"][0]["series"][0]["values"][0][1]
        print(f"Last value from 'teplota' measurement: {last_value}")
        formatted_number = format_number_with_degree(last_value)
        # Zobrazení symbolu stupně (např. tečka) na poslední pozici
        display.show(formatted_number)    

        # Kontrola stáří dat
        if is_data_older_than_5_minutes(result):
            display.show("OLD")
            print("Data is older than 5 minutes.")

    else:
        display.show("NaN")
        print("No data found in 'teplota' measurement.")
else:
   display.show('ERR')
