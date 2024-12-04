#! /usr/bin/env python

import serial
import json
import time
import socket

hostname = socket.gethostname()

# Open a serial connection on the Pi's UART port
ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)

state = False

if hostname == 'light-server':
  numLEDs = 300
else:
  numLEDs = 35

ledSeq3 = { 'type': 'steady-repeat-colors',
            'interval': 1.0,
            'colors': [ { 'h': 0, 's': 1.0, 'v': 0.15 },
                        { 'h': 126, 's': 1.0, 'v': 0.15 } ]}

cnt = 0
# Prepare JSON data to send
data_to_send = { 'state': False, 'num-leds': numLEDs}
cnt = (cnt + 1) % 3
json_data = json.dumps(data_to_send)
print("cnt:", cnt)

# Send JSON data over serial
ser.write(json_data.encode() + b'\n')

# Read response from the other device
response = ser.readline().decode().strip()
if response:
    try:
        response_data = json.loads(response)
        if response_data['rtn'] != 'ACK':
            print("ERROR: no ack", response_data)
    except json.JSONDecodeError:
        print("Received invalid JSON data |" + response + '|')
