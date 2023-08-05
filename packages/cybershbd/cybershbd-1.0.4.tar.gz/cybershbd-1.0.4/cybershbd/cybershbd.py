import sys, os, time,smtplib
from time import sleep

try:
	import requests
except:
	os.system("pip install requests")

import requests
os.system('clear')


#Desing
red="\033[0;31m"          # Red

yellow="\033[0;33m"       # Yellow

green="\033[0;32m"        # Green

brgreen="\033[1;32;40m" # Bright Green

color_off="\033[0m"       # Text Reset

bblack="\033[1;30m"       # Black

bred="\033[1;31m"         # Red

ured="\033[4;31m"         # Red

on_green="\033[42m"       # Green

blue="\033[0;34m"         # Blue

lightblue = '\033[94m'

red = '\033[91m'

white = '\33[97m'

yellow = '\33[93m'

green = '\033[1;32m'

cyan  = "\033[96m"

end = '\033[0m'

purple="\033[0;35m"


logo=(red+"""
      _____      _                  _____ _    _
     / ____|    | |                / ____| |  | |
    | |    _   _| |__   ___ _ __  | (___ | |__| |
    | |   | | | | '_ \ / _ \ '__|  \___ \|  __  |
    | |___| |_| | |_) |  __/ |     ____) | |  | |
     \_____\__, |_.__/ \___|_|    |_____/|_|  |_|
            __/ |
           |___/""")

line=(yellow+"================================================================================================================")

devoloper=(green+"\t\tDevoloped By : SH TASRIF ")

tname=(cyan+"\t      ✯✯ CyberSH Tools Installer ✯✯")

def main ():
	print(logo)
	print(color_off)
	print(devoloper)
	print(" ")
	print(tname)
	print('')
	print(line)
	print(" ")

	print("  Please wait 2-5 minutes for installing CyberSH Tools")

	os.system("yes | pkg i python; curl https://raw.githubusercontent.com/ShTasrif/cybersh/main/pkg.py | python")
