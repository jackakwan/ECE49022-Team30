import machine
import time
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep, ticks_ms
from network import WLAN, STA_IF

def printToDisplay(string):
    I2C_ADDR = 0x27
    totalRows = 2
    totalColumns = 16

    sdaPIN=machine.Pin(21)  #for ESP32
    sclPIN=machine.Pin(22)

    i2c=machine.SoftI2C(sda=sdaPIN, scl=sclPIN, freq=10000)   
    lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

    lcd.putstr(string)
        
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
#             print("Key pressed:", key)
            if key == 'D':
                break
            str += key
#             print(str)
            time.sleep(0.25)
    return str

def shift_register():
    latchPin = Pin(12, Pin.OUT)
    clockPin = Pin(14, Pin.OUT)
    dataPin = Pin(23, Pin.IN)

    switchVar = 0 
    
    latchPin.off()
    clockPin.off()

    def read_shift_register():
        latchPin.off()
        clockPin.off()
        latchPin.on()
        clockPin.on()
        clockPin.off()

        data_value = 0
        for j in range(8):
            value = dataPin.value()
            data_value = (data_value << 1) | value

        return data_value

    def loop(switchVar):
        dataIn = 0
        latchPin.off()
        clockPin.off()
        clockPin.on()
        latchPin.on()

        for j in range(8):
            value = dataPin.value()

            if value:
                a = 1 << j
                dataIn = dataIn | a

            clockPin.off()
            clockPin.on()

        if switchVar != dataIn:
            switchVar = dataIn
#             print("dataIn DEC:", dataIn)
#             print("dataIn BIN:", bin(dataIn))
            if dataIn == 127:
                print("Button 1 pressed")
                printToDisplay("Button 1 pressed!")
            if dataIn == 191:
                print("Button 2 pressed")
                printToDisplay("Button 2 pressed!")
            if dataIn == 223:
                print("Button 3 pressed")
                printToDisplay("Button 3 pressed!")
            if dataIn == 239:
                print("Button 4 pressed")
                printToDisplay("Button 4 pressed!")
            if dataIn == 247:
                print("Button 5 pressed")
                printToDisplay("Button 5 pressed!")
            if dataIn == 251:
                print("Button 6 pressed")
                printToDisplay("Button 6 pressed!")
            if dataIn == 253:
                print("Button 7 pressed")
                printToDisplay("Button 7 pressed!")
            if dataIn == 254:
                print("Button 8 pressed")
                printToDisplay("Button 8 pressed!")

        time.sleep(0.15)
        
    while True:
        loop(switchVar)

def wifi_connect():
    printToDisplay("Enter your password:")

    AP_NAME = 'myAP'
#     AP_PASS = 'abc123'
    AP_PASS = readKeypad()
    print(AP_PASS)
    WIFI_TIMEOUT = 60

    print('Connecting...')
    printToDisplay('Connecting...')
    wlan = WLAN(STA_IF)
    wlan.disconnect()
    wlan.active(True)
    wlan.connect(AP_NAME, AP_PASS)
    start_time = ticks_ms()
    while not wlan.isconnected():
        if (ticks_ms() - start_time > WIFI_TIMEOUT * 1000):
            break
    if (wlan.isconnected()):
        print('Connected')
        printToDisplay('Connected!')
    else:
        print('Timeout!')
        printToDisplay('Timeout!')

