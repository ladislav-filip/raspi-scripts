from datetime import datetime
import tm1637
import time

# Nastavení pinů, které jste použili pro připojení DIO a CLK
CLK = 22
DIO = 23

# Inicializace displeje
display = tm1637.TM1637(clk=CLK, dio=DIO)

# Nastavení jasu (volitelně, rozsah 0-7)
display.brightness(6)

# Zobrazení číslic (např. 12:34)
display.numbers(99, 99)

while True:
    # Získání aktuálního času
    now = datetime.now()
    hour = now.hour
    minute = now.minute

    # Zobrazení aktuálního času (formát HH:MM)
    display.numbers(hour, minute)

    # Počkejte jednu minutu před dalším aktualizováním
    time.sleep(60)