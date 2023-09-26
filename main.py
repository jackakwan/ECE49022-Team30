import machine
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
from functions import *

inputStr = readKeypad()
printToDisplay(inputStr)

