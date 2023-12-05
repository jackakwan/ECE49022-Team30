import machine
import time
import utime
import os
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep, ticks_ms
from network import WLAN, STA_IF
from ir_program import *
cols = [machine.Pin(19), machine.Pin(18), machine.Pin(17), machine.Pin(16)]
rows = [machine.Pin(4), machine.Pin(5), machine.Pin(2), machine.Pin(15)]
keymap = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['*', '0', '#', 'D']]

latchPin = machine.Pin(12, machine.Pin.OUT)
clockPin = machine.Pin(14, machine.Pin.OUT)
dataPin = machine.Pin(23, machine.Pin.IN)

def readBoard():
    press = False
    while not press:
        switchVar = 0
        latchPin.off()
        clockPin.off()

        dataIn = 0
        latchPin.off()
        clockPin.off()
        clockPin.on()
        latchPin.on()
        
    
        for j in range(16):
            value = dataPin.value()

            if value:
                a = 1 << j
                dataIn = dataIn | a

            clockPin.off()
            clockPin.on()
        j = 0
        
        if switchVar != dataIn:
            switchVar = dataIn
            if dataIn != 65535:
                i = 0
                while i < 16:
                    temp = dataIn
                    temp &= (1 << i)
                    if not temp:
                        string = "Button " + str(16 - i) + " pressed!"
                        print(string)
                        buttonNum = 16-i
                        press = True
                        return buttonNum
                    i += 1

        for row in rows:
            row.init(mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)

        for col in cols:
            col.init(mode=machine.Pin.OUT)

        for col in cols:
            col.value(0)
            for i, row in enumerate(rows):
                if row.value() == 0:
                    col.value(1)
                    key = keymap[i][cols.index(col)]
                    if key == 'D':
                        return 0
                    print("Key", key, "pressed!")
                    press = True
                    if type(key) == str:
                        return key
                    return 100 + int(key)
            col.value(1)

        utime.sleep_ms(100)  # Adjust the delay if needed

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
    printToDisplay("Select the WiFi network you wish to connect to")
    time.sleep(3)
    printToDisplay("1 to confirm, 2 to continue")
    wlan = WLAN(STA_IF)
    wlan.disconnect()
    wlan.active(True)
    networks = wlan.scan()
    for network in networks:
        printToDisplay(network)
        choiceA = readBoard()
        while(choiceA != 1 or choiceA != 2):
            printToDisplay("Invalid input, try again")
            choiceA = readBoard()
        if(choiceA == 1):
            printToDisplay("Enter your password:")
            password = readBoard()
            WIFI_TIMEOUT = 60
            printToDisplay('Connecting...')
            wlan.connect(network, password)
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
        elif(choiceA == 2):
            continue    

def create_profile_directory():
    #This function will create a text file containing all profiles being used as well as the current profile selected
    allFiles = os.listdir("/")
    if "profile_list.txt" in allFiles:
        print("directory exists, exiting")
        return
    print("creating dir")
    with open("profile_list.txt", 'w') as file:
       file.write("Profile Directory\n")
       file.write("cur: None\n")
    file.close()

def edit_profile_directory(profile_to_add):
    numProfiles = 0
    try:
        with open("profile_list.txt", "r") as file_read:
            lines = file_read.readlines()
        file_read.close()
        with open("profile_list.txt", "w+") as file_write:
            for line in lines:
                if "cur" not in line:
                    numProfiles = numProfiles + 1
                    file_write.write(line)
                if(numProfiles > 8):
                    print("Maximum number of profiles reached, cannot add another until an existing profile is deleted")
                    return 1
                if "cur" in line:
                    temp = line
            file_write.write(f"{numProfiles}: {profile_to_add}\n")
            file_write.write(f"{temp}\n")
        file_write.close()
    except:
        print("Error opening the profile directory") 
    

def set_current_profile(profile):
    update = False
    with open("profile_list.txt", 'r') as file_read:
        lines = file_read.readlines()
    file_read.close()
    with open("profile_list.txt", 'w+') as file_write:
        for line in lines:
            if "cur" not in line and profile in line:
                update = True
                file_write.write(line)
            elif("cur" not in line):
                file_write.write(line)
            elif "cur" in line:
                temp = line
        if(update):
            file_write.write(f"cur: {profile}\n")
        else:
            print(f"Profile: {profile} not found in directory, exiting")
            #Rewrite the previous current profile
            for line in lines:
                if "cur" in line:
                    file_write.write(temp)
            file_write.close()
            return 
    file_write.close()

def delete_profile(profile):
    allFiles = os.listdir("/")
    for file in allFiles:
        if profile in file:
            os.remove(file)
    with open("profile_list.txt", 'r') as file_read:
        lines = file_read.readlines()
    file_read.close()
    with open("profile_list.txt", "w+") as file_write:
        for line in lines:
            if profile not in line:
                file_write.write(line)
            if f"cur: {profile}" in line:
                file_write.write("cur: None")
    print("deleted")
    file_write.close()

def delete_all_profiles():
    print("deleting all")
    allFiles = os.listdir("/")
    for file in allFiles:
        if file.endswith(".txt"):
            os.remove(file)

def list_all_profiles():
    with open("profile_list.txt", 'r') as file_read:
        lines = file_read.readlines()
    file_read.close()
    
    allProfiles = []
    for line in lines:
        profiles = line.split(":")
        allProfiles.append(profiles[1].rsplit("\n").split())
    for profile in allProfiles:
        printToDisplay(profile)
        time.sleep(1)

def pair():
    numTV = 1
    numSpeakers = 1
    numProjectors = 1
    numProfiles = 0
    printToDisplay("1 - IR 2 - WiFi")
    choiceA = readBoard()
    while(choiceA != '1' and choiceA != '2'):
        printToDisplay("Invalid input, try again")
        choiceA = readBoard()
    if(choiceA == '1'):
        printToDisplay("1: Add, 2:Update 3:Set, 4:Del")
        choiceB = readBoard()
        while(choiceB != '1' and choiceB != '2' and choiceB != '3' and choiceB != '4'):
            printToDisplay("Invalid Input, please try again")
            time.sleep(3)
            printToDisplay("1: Add, 2:Update 3:Set, 4:Del")
            choiceB = readBoard()
        if(choiceB == '1'):
            printToDisplay("Select type of  device")
            time.sleep(3)
            printToDisplay("1: TV 2: Speaker 3: Projector")
            choiceC = readBoard()
            while(choiceC != '1' and choiceC != '2' and choiceC != '3'):
                printToDisplay("Invalid Input, please try again")
                choiceC = readBoard()
            with open("profile_list.txt", 'r') as file_read:
                lines = file_read.readlines()
                for line in lines:
                    if "cur" not in line:
                        if "TV" in line:
                            numTV = numTV + 1
                        elif "Speaker" in line:
                            numSpeakers = numSpeakers + 1
                        elif "Projector" in line:
                            numProjectors = numProjectors + 1
            file_read.close()
            if(choiceC == '1'):
                device = "TV"
                count = numTV
            elif(choiceC == '2'):
                device = "Speakers"
                count = numSpeakers
            elif(choiceC == '3'):
                device = "Projector"
                count = numProjectors
            profileName = f"{device}{count}"
            profilePath = f'{profileName}.txt'
            edit_profile_directory(profileName)
            with open(profilePath, "w") as file_create:
                printToDisplay("Profile Creation Complete")
            file_create.close()
            time.sleep(3)
            printToDisplay("Add signal?     1: Y 2: N")
            choiceD = readBoard()
            while(choiceD != '1' and choiceD != '2'):
                printToDisplay("Invalid Input, try again")
                choiceD = readBoard()
            if(choiceD == '1'):
                set_current_profile(profileName)
                ir_clone_signal()
            elif(choiceD == '2'):
                return 1
        elif(choiceB == '2'):
            count = 0
            with open("profile_list.txt", 'r') as file_read:
                lines = file_read.readlines()
                for line in lines:
                    if "Profile Directory" in line or "cur" in line:
                        continue
                    else:
                        count = count + 1
                if(count == 0):
                    printToDisplay("No profiles,    exiting")
                    file_read.close()
                    return
            printToDisplay("Select profile  to update")
            time.sleep(3)
            printToDisplay("1: Y 2: N")
            time.sleep(3)
            with open("profile_list.txt", 'r') as file_read:
                lines = file_read.readlines()
                for line in lines:
                    if ':' in line:
                        printToDisplay(line)
                        choiceE = readBoard()
                        while(choiceE != '1' and choiceE != '2'):
                            printToDisplay("Invalid input, try again")
                            time.sleep(3)
                            printToDisplay(line)
                            choiceE = readBoard()
                        if(choiceE == '1'):
                            profileLine = line.split(":")
                            profile = profileLine[1].rsplit("\n")
                            number = profileLine[0].strip()
                            if "cur" in number:
                                continue
                            name = profile[0].strip()
                            set_current_profile(name)
                            ir_clone_signal()
                            file_write.close()
                        else:
                            continue
                printToDisplay("No profile selected")
                time.sleep(3)
                printToDisplay("Exiting")
            file_read.close()
            return
        elif(choiceB == '3'):
            printToDisplay("Select profile  to set")
            time.sleep(3)
            printToDisplay("1: Y 2: N")
            time.sleep(3)
            with open("profile_list.txt", 'r') as file_read:
                lines = file_read.readlines()
                for line in lines:
                    if ':' in line:
                        printToDisplay(line)
                        choiceE = readBoard()
                        while(choiceE != '1' and choiceE != '2'):
                            printToDisplay("Invalid input, try again")
                            time.sleep(3)
                            printToDisplay(line)
                            choiceE = readBoard()
                        if(choiceE == '1'):
                            profileLine = line.split(":")
                            profile = profileLine[1].rsplit("\n")
                            number = profileLine[0].strip()
                            name = profile[0].strip()
                            set_current_profile(name)
                            printToDisplay("Success, exiting")
                            return
                        else:
                            continue
                    else:
                        continue
            file_read.close()
            return
        elif(choiceB == '4'):
            printToDisplay("Select profile  to delete")
            time.sleep(3)
            printToDisplay("1: Y 2: N")
            time.sleep(3)
            with open("profile_list.txt", 'r') as file_read:
                lines = file_read.readlines()
                for line in lines:
                    print(line)
                    if "cur" not in line and ':' in line:
                        printToDisplay(line)
                        choiceF = readBoard()
                        while(choiceF != '1' and choiceF != '2'):
                            printToDisplay("Invalid input, try again")
                            time.sleep(3)
                            printToDisplay(line)
                            choiceF = readBoard()
                        if(choiceF == '1'):
                            profileLine = line.split(":")
                            profile = profileLine[1].rsplit("\n")
                            name = profile[0].strip()
                            delete_profile(name)
                            return
                        else:
                            continue
                    else:
                        continue
    elif(choiceA == '2'):
        wifi_connect()
#delete_all_profiles()
create_profile_directory()
ir = NEC_16(Pin(33, Pin.IN), callback)
pair()
