'''
File: ir_program.py
Author: Jack Kwan
Last modified: 10/19/2023

File Description: This file contains necessary functions to send, receive, pair, and delete IR signals. 

Function: ir_clone_signal()
Parameters: None

This function updates the global variable 'signalToClone' which stores the name of the button the user is attempting to pair

Function: ir_send_signal(signalToSend)
Parameters:
    1. signalToSend - The name of the signal intending on being sent

This function takes the name of the signal that the user wants to send, searches for the current profile, searches that profile's IR key for the signal, and, if found, sends the signal.
Otherwise, this function prints an error to the terminal. 

Function: callback(data, addr, ctrl)
Parameters:
    1. data		#The code for the instruction
    2. addr		#The address for the instruction
    3. ctrl		#ext
This function does two things:
    1. If the user is attempting to pair, this function will take the data and address of the signal it just received and store it in the associated signal table
    2. If not, the user will take the data and address of the signal and print to the terminal for testing purposes (will be removed in future iterations)

Callback is run every time the IR receiver detects a signal using the enabled protocol (in our case, NEC)
        
Function: ir_delete_profile(profile)
Parameters:
    1. profile  #The profile to be deleted
This function deletes a given profile (by delete, we mean to delete the text file containing the IR key for the associated device and as a result, any attempt to send a signal will produce an error)
'''

import machine
import time
import os
from ir_rx import NEC_16
from ir_tx import NEC
from functions import printToDisplay, readKeypad

signalToClone = ''

def ir_clone_signal():
    #This function is called when the user is trying to program the remote, and simply sets the global variable signalToClone to what button the user intends to set
    pairProcess = True
    printToDisplay('Please press the button on the universal remote you wish to program')   #Tell user to press a button
    signalToClone = readKeypad()    #Read button press
    time.sleep(5)
    if(signalToClone == ''):
        printToDisplay('No button pressed, exiting pairing process')
        pairProcess = False #Update boolean
        return -1
    else:
        return signalToClone

def ir_send_signal(signalToSend):
    #This function takes a signal name as a string, finds the associated signal for the current profile, and sends it using the IR transmitter
    signalCode = []    
    with open("profile_list.txt", 'r') as file_read:
            lines = file_read.readlines()
            for line in lines:
                if ("cur" in line):
                    profileLine = line.split(":")
                    profile = profileLine[1].rsplit("\n").strip()
    path = f"{profile}.txt"
    allFiles = os.listdir("/")
    if path in allFiles:
        with open(path, 'r') as file:
            ir_key = file.readlines()
            for key in ir_key:
                if(signalToSend in key):
                    signal = key.split(":")
                    signal[1].rstrip("\n").strip()
                    code = list(signal[1].split(","))
                    for ind in code:
                        signalCode.append("".join(ind.split()))
                if(signalCode == []):
                    print("Signal not found, please clone the signal to the remote")
        if(signalCode != []):
            nec.transmit(signalCode[1], signalCode[0])
        else:
            print("There was an error finding the signal data")
    else:
        print("Error: Profile not found.")

    
    

def callback(data, addr, ctrl):
    if data >= 0:  # NEC protocol sends repeat codes.
    #print('Data {:02x} Addr {:04x}'.format(data, addr))
        if pairProcess:
            #Set the data and address of the instruction received 
            newData = f"0x{data:02x}"
            newAddr = f"0x{addr:04x}"
            with open(path, 'r') as file_read:
                    #ir_key[signalToClone] = data
                    lines = file_read.readlines()
                    for line in lines:
                        if ("cur" in line):
                            profileLine = line.split(":")
                            profile = profileLine[1].rsplit("\n").strip()
            path = f"{profile}.txt"	#Some path to the file containing the IR key for the current profile
            allFiles = os.listdir("/")
            #print(allFiles)
            if path in allFiles:
                with open(path, 'r') as file_read:
                    #ir_key[signalToClone] = data
                    lines = file_read.readlines()
                    with open(path, 'w+') as file_write:
                        for line in lines:
                            if(signalToClone not in line):
                                file_write.write(f"{line}")
                        if not (data == 'f0' and addr == '0381'):
                            file_write.write(f"{signalToClone}: {newData}, {newAddr}\n")
                            file_write.close()
                file_read.close()
            elif path not in allFiles:
                with open(path, 'w') as file:
                    #ir_key[signalToClone] = data
                    if not (data == 'f0' and addr == '0381'):
                        file.write(f"{signalToClone}: {newData}, {newAddr}\n")
                        file.close()
            else:
                print("surely we don't enter this loop")
            #print('Data {:02x} Addr {:04x}'.format(data, addr))   Test print
       #return (ir_key)
       
        else:
        #Not a pairing process, print the signal that is detected. This functionality will be removed in the future
            print('Data {:02x} Addr {:04x}'.format(data, addr))

def ir_delete_profile(profile):
    try:
        path = f"{profile}.txt" #Path containing the profile
        os.remove(path)
    except:
        print("The profile you're trying to delete does not exist.")


          
#Some main calling
#Code to send a signal

if __name__ == "__MAIN__":
    #Test parameters

    pairProcess = True
    signalToSend = "POWER"
    #Enable IR transmit and receive pins
    ir = NEC_16(Pin(32, Pin.IN), callback)
    nec = NEC(Pin(26, Pin.OUT, value = 0))
    ir_send_signal(signalToSend)
