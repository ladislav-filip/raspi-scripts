from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import libs.logger as logger

def is_data_older_than_minutes(time_str, than_minutes=15, timezone_str="UTC"):
    try:
        # Nastavení časové zóny
        tz = ZoneInfo(timezone_str)

        time_str = time_str.split(".")[0]  # Odstranění desetinných míst
        logger.log_info(f"Čas z JSON: {time_str}")

        # Převod času na datetime objekt
        measurement_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
        # Nastavení časové zóny na UTC (čas v JSON je obvykle v UTC)
        measurement_time = measurement_time.replace(tzinfo=ZoneInfo("UTC"))

        # Aktuální čas v dané časové zóně
        current_time = datetime.now(tz)
        logger.log_info(f"Aktuální čas: {current_time}")

        # Výpočet rozdílu
        time_difference = current_time - measurement_time
        return time_difference > timedelta(minutes=than_minutes)

    except (KeyError, IndexError, ValueError) as e:
        logger.log_error(f"Chyba při zpracování JSON: {e}")
        return None
