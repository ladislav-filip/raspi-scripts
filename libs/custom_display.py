import tm1637

class CustomDisplay:
    """
    Třída CustomDisplay poskytuje metody pro práci s 7-segmentovým displejem TM1637.
    Metody:
        __init__():
            Inicializuje displej se specifikovanými piny CLK a DIO a nastaví jas.
        show(text):
            Zobrazí zadaný text na displeji.
            Argumenty:
                text (str): Text k zobrazení na displeji.
        showError():
            Zobrazí chybovou zprávu ("ERR") na displeji.
        format_number_for_display(number):
            Formátuje číslo s plovoucí desetinnou čárkou pro zobrazení rozdělením na celé a desetinné části,
            a následným spojením do řetězce bez desetinné čárky.
            Argumenty:
                number (float): Číslo k formátování.
            Návratová hodnota:
                str: Formátované číslo jako řetězec, s celou částí následovanou dvoucifernou desetinnou částí.
        format_number_with_degree(number):
            Formátuje dané číslo na řetězec se symbolem stupně.
            Funkce zaokrouhlí dané číslo na nejbližší celé číslo, zkontroluje, zda je v rozmezí -50 až 80,
            a formátuje ho na řetězec o šířce 3 znaků s mezerami zleva a symbolem stupně.
            Argumenty:
                number (float): Číslo k formátování.
            Návratová hodnota:
                str: Formátovaný řetězec se symbolem stupně.
            Vyvolá:
                ValueError: Pokud je číslo mimo rozmezí -50 až 80.
    """

    def __init__(self):
        # Nastavení pinů, které jste použili pro připojení DIO a CLK
        CLK = 18
        DIO = 17

        # Inicializace displeje
        self._display = tm1637.TM1637(clk=CLK, dio=DIO)

        # Nastavení jasu (volitelně, rozsah 0-7)
        self._display.brightness(1)

    def show(self, text):
        """
        Zobrazí zadaný text na displeji.
        Argumenty:
            text (str): Text k zobrazení na displeji.
        """
        self._display.show(text)

    def show_error(self):
        """
        Zobrazí chybovou zprávu na displeji.
        """
        self._display.show("ERR")

    @staticmethod
    def format_number_for_display(number):
        """
        Formátuje číslo s plovoucí desetinnou čárkou pro zobrazení rozdělením na celé a desetinné části,
        a následným spojením do řetězce bez desetinné čárky.
        Argumenty:
            number (float): Číslo k formátování.
        Návratová hodnota:
            str: Formátované číslo jako řetězec, s celou částí následovanou dvoucifernou desetinnou částí.
        """
        # Rozdělení čísla na celé a desetinné části
        integer_part = int(number)
        decimal_part = int((number - integer_part) * 100)
        
        # Zformátování čísla na text pro zobrazení na displeji
        formatted_number = f"{integer_part}{decimal_part:02d}"
        return formatted_number

    @staticmethod
    def format_number_with_degree(number):
        """
        Formátuje dané číslo na řetězec se symbolem stupně.
        Funkce zaokrouhlí dané číslo na nejbližší celé číslo, zkontroluje, zda je v rozmezí -50 až 80,
        a formátuje ho na řetězec o šířce 3 znaků s mezerami zleva a symbolem stupně.
        Argumenty:
            number (float): Číslo k formátování.
        Návratová hodnota:
            str: Formátovaný řetězec se symbolem stupně.
        Vyvolá:
            ValueError: Pokud je číslo mimo rozmezí -50 až 80.
        """
        # Získání celého čísla
        integer_part = int(round(number))
        
        # Kontrola rozsahu a formátování na řetězec o délce 4 znaků
        if -50 <= integer_part <= 80:
            formatted_number = f"{integer_part: >3}*"  # Formátování na tříznakové číslo s mezerami zleva a přidání '*'
        else:
            raise ValueError("Number out of range -50 to 80")
        
        return formatted_number