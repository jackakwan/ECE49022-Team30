
# ECE49022-Team30
Software Development for a Universal Remote Control

Contents:

 - main.py: Main file where all other functions are called
 - functions.py: Helper file with the code for all functions. Current capabilties include: 
	 - Driving an LCD display through an I2C interface
	 - Debouncing a 4x4 keypad
	 - Connecting to a Wi-Fi network
	 - Reading 8 different button presses from Parallel In Serial Out Shift Register
 - i2c_lcd.py/lcd_api.py: Additional code for driving LCD displays
 - ESP32_GENERIC: Firmware to be flashed onto ESP32 during first time of usage.
 - ir_rx.py: IR receiver library
 - ir_tx.py: IR transmitter library
 - ir_program.py: File containing all necessary functions to send, receive, pair, and disconnect from profiles using IR signals.
   	- Pair/Disconnect functionality is done by creating/deleting text files containing the IR key for each device in the form of [Signal Name]: [Data], [Address]
   	- Profile selection simply changes what text file is being read from at a given moment. 
   

   
