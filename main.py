import machine
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
from functions import *
from ir_program import *

def main():
    with open("profile_list.txt", 'w') as file:
        file.write("Profile Directory")
    while(True):
        buttonPress = readBoard()
        if(buttonPress == 1):
            ir_clone_signal()
        