#!/bin/bash

# Aktivace virtuálního prostředí
source /home/pilif/display/bin/activate

# python3 /home/pilif/scripts/read-env.py

# Spuštění Python skriptu
python3 /home/pilif/scripts/read-temp.py

# Deaktivace virtuálního prostředí (volitelně)
deactivate

