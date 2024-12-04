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

RED = { 'h': 0, 's': 1.0, 'v': 0.5 }
GREEN = { 'h': 145, 's': 1.0, 'v': 0.5}
BLUE =  { 'h': 126, 's': 1.0, 'v': 0.5 }


ledSeq1 = { 'type': 'shift-colors',
            'interval': 1.0,
            'colors': [ RED, RED,
                        GREEN, GREEN, 
                        GREEN, GREEN, 
                        GREEN, GREEN ]}

ledSeq2 = { 'type': 'shift-colors',
            'interval': 1.0,
            'colors': [ RED, RED, RED,
                        RED, RED, RED,
                        RED,
                        GREEN ]}

ledSeq3 = { 'type': 'steady-repeat-colors',
            'interval': 1.0,
            'colors': [ RED, GREEN ]}

cnt = 0
while True:
  # Prepare JSON data to send
  if cnt % 3 == 0:
    data_to_send = { 'state': True,
                     'num-leds': numLEDs,
                     'sequence': ledSeq1 }
  elif cnt % 3 == 1:
    data_to_send = { 'state': True,
                     'num-leds': numLEDs,
                     'sequence': ledSeq2 }
  else:
    data_to_send = { 'state': True,
                     'num-leds': numLEDs,
                     'sequence': ledSeq3 }
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

  time.sleep(5)
