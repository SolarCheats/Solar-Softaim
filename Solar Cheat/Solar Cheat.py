import json
import os
import sys
import threading

from pynput import keyboard
from termcolor import colored


def on_release(key):
    try:
        if key == keyboard.Key.f1:
            Aimbot.update_status_aimbot()
        if key == keyboard.Key.f2:
            Aimbot.clean_up()
    except NameError:
        pass

def main():
    global solar
    solar = Aimbot(collect_data = "collect_data" in sys.argv)
    solar.start()

def setup():
    path = "lib/config"
    if not os.path.exists(path):
        os.makedirs(path)

    print("[INFO] In-game X and Y axis sensitivity should be the same")
    def prompt(str):
        valid_input = False
        while not valid_input:
            try:
                number = float(input(str))
                valid_input = True
            except ValueError:
                print("[!] Invalid Input. Make sure to enter only the number (e.g. 6.9)")
        return number

    xy_sens = prompt("X-Axis and Y-Axis Sensitivity (from in-game settings): ")
    targeting_sens = prompt("Targeting Sensitivity (from in-game settings): ")

    print("[INFO] Your in-game targeting sensitivity must be the same as your scoping sensitivity")
    sensitivity_settings = {"xy_sens": xy_sens, "targeting_sens": targeting_sens, "xy_scale": 10/xy_sens, "targeting_scale": 1000/(targeting_sens * xy_sens)}

    with open('lib/config/config.json', 'w') as outfile:
        json.dump(sensitivity_settings, outfile)
    print("[INFO] Sensitivity configuration complete")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

    print(colored('''
    .d8888b.   .d88888b.  888             d8888 8888888b.  
d88P  Y88b d88P" "Y88b 888            d88888 888   Y88b 
Y88b.      888     888 888           d88P888 888    888 
 "Y888b.   888     888 888          d88P 888 888   d88P 
    "Y88b. 888     888 888         d88P  888 8888888P"  
      "888 888     888 888        d88P   888 888 T88b   
Y88b  d88P Y88b. .d88P 888       d8888888888 888  T88b  
 "Y8888P"   "Y88888P"  88888888 d88P     888 888   T88b
By-Numb
    (Neural Network Aimbot)''', "blue"))

    path_exists = os.path.exists("lib/config/config.json")
    if not path_exists or ("setup" in sys.argv):
        if not path_exists:
            print("[!] Sensitivity configuration is not set")
        setup()
    path_exists = os.path.exists("lib/data")
    if "collect_data" in sys.argv and not path_exists:
        os.makedirs("lib/data")
    from lib.aimbot import Aimbot
    listener = keyboard.Listener(on_release=on_release)
    listener.start()
    main()
