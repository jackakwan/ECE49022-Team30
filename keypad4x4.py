# Write your code here :-)
import machine
import time

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
                print(row,col)
                return keymap[i][cols.index(col)]
        col.value(1)
    return None


while True:
    key = read_keypad()
    if key:
        print("Key pressed:", key)
    time.sleep(0.1)

