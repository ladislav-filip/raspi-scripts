import tm1637
import time

# Nastavení pinů, které jste použili pro připojení DIO a CLK
CLK = 22
DIO = 23

# Inicializace displeje
display = tm1637.TM1637(clk=CLK, dio=DIO)

# Nastavení jasu (volitelně, rozsah 0-7)
display.brightness(1)

# Zobrazení číslic (např. 12:34)
display.numbers(12, 34)

# Nebo můžete zobrazit libovolný text
# Příklad: posouvání textu "HELLO"
text = 'HELLO'
while True:
    for i in range(len(text)):
        display.show(text[i:i+4])
        time.sleep(0.3)

