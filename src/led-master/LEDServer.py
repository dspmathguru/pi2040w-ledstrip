#! /usr/bin/env python

import serial
import json
import time

# Open a serial connection on the Pi's UART port
ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)

state = False

ledSeq1 = { 'type': 'shift-colors',
           'interval': 1.0,
           'colors': [ { 'h': 0, 's': 1.0, 'v': 0.35 },
                       { 'h': 20, 's': 1.0, 'v': 0.35 },
                       { 'h': 40, 's': 1.0, 'v': 0.35 },
                       { 'h': 60, 's': 1.0, 'v': 0.35 },
                       { 'h': 80, 's': 1.0, 'v': 0.35 },
                       { 'h': 126, 's': 1.0, 'v': 0.5 },
                       { 'h': 126, 's': 1.0, 'v': 0.5 },
                       { 'h': 126, 's': 1.0, 'v': 0.5 },
                       { 'h': 126, 's': 1.0, 'v': 0.5 } ]}

ledSeq2 = { 'type': 'steady-repeat-colors',
           'interval': 1.0,
           'colors': [ { 'h': 0, 's': 1.0, 'v': 0.35 },
                       { 'h': 126, 's': 1.0, 'v': 0.35 } ]}

cnt = 0
while True:
  # Prepare JSON data to send
  if cnt % 3 == 0:
    data_to_send = { 'state': True, 'sequence': ledSeq1 }
  elif cnt % 3 == 1:
    data_to_send = { 'state': True, 'sequence': ledSeq2 }
  else:
    data_to_send = { 'state': False }
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
