import machine
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import time
from time import sleep

def printToDisplay(string):
    I2C_ADDR = 0x27
    totalRows = 2
    totalColumns = 16

    sdaPIN=machine.Pin(21)  #for ESP32
    sclPIN=machine.Pin(22)

    i2c=machine.SoftI2C(sda=sdaPIN, scl=sclPIN, freq=10000)   

    # i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)     #initializing the I2C method for ESP32

    lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

    while True:
        lcd.putstr("I2C LCD")
        sleep(2)
        lcd.clear()
        lcd.putstr(string)
        sleep(2)
        lcd.clear()
        
def readKeypad():
    cols = [machine.Pin(19), machine.Pin(18), machine.Pin(17), machine.Pin(16)]
    rows = [machine.Pin(4), machine.Pin(5), machine.Pin(2), machine.Pin(15)]

    keymap = [
        ['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']
    ]

    for row in rows:
        row.init(mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)

    for col in cols:
        col.init(mode=machine.Pin.OUT)

    def read_keypad():
        for col in cols:
            col.value(0)
            for i, row in enumerate(rows):
                if row.value() == 0:
                    col.value(1)
#                     print(row,col)
                    return keymap[i][cols.index(col)]
            col.value(1)
        return None

    str = ''
    while True:
        key = read_keypad()
        if key:
            print("Key pressed:", key)
            if key == 'D':
                break
            str += key
            print(str)
            time.sleep(0.5)
    return str
    

