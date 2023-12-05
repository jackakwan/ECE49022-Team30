from machine import Pin
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
from testpair import *
from ir_program import *

def main():
    buttonMapping = {1: "Power", 2: "Menu", 3: "Volume Up", 4: "Channel Up",
                     5: "Volume Down", 6: "Channel Down", 7: "Mute", 8: "Last",
                     9: "Pair", 10: "Source", 11: "Delete", 12: "Settings",
                     13: "Up", 14: "Left", 15: "Right", 16: "Down", 17:"Enter"}
    delete_all_profiles()
    create_profile_directory()
    ir = NEC_16(Pin(33, Pin.IN), callback)
    nec = NEC(Pin(26, Pin.OUT, value = 0))
    while(1):
        with open("profile_list.txt", 'r') as file_read:
            lines = file_read.readlines()
        file_read.close()
        for line in lines:
            if "cur" in line:
                current = line.split(":")
                nameRaw = current[1].rstrip("\n")

                #printToDisplay(name)
                break
            else:
                continue
        printToDisplay("TV1")
        uInput = readBoard()
        instruction = buttonMapping[uInput]
        if(instruction == "Pair"):
            pair()
        else:
            ir_send_signal(instruction, nec)
        
main()
#     
#    for i in range(0,5):
#         nec.transmit(0x0004, 0x08)
#         time.sleep(3)
#         nec.transmit(0x0004, 0x09)
#         time.sleep(1)
#         nec.transmit(0x0004, 0x02)
#         time.sleep(1)
#         nec.transmit(0x0004, 0x02)
#         time.sleep(1)
#         nec.transmit(0x0004, 0x03)
#         time.sleep(1)
#         nec.transmit(0x0004, 0x03)
#         time.sleep(3)
#         nec.transmit(0x0004, 0x08)
           
        

