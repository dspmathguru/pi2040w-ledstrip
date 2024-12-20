#! /usr/bin/env python

import serial
import json
import time
import socket


import datetime as dt  
def isNowInTimePeriod(startTime, endTime, nowTime): 
    if startTime < endTime: 
        return nowTime >= startTime and nowTime <= endTime 
    else: 
        #Over midnight: 
        return nowTime >= startTime or nowTime <= endTime 

#normal example: 
isNowInTimePeriod(dt.time(13,45), dt.time(21,30), dt.datetime.now().time())

#over midnight example: 
isNowInTimePeriod(dt.time(20,30), dt.time(1,30), dt.datetime.now().time())


hostname = socket.gethostname()

startTime = dt.time(16,45)
endTime = dt.time(22,00)


# Open a serial connection on the Pi's UART port
ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)

state = False

if hostname == 'light-server':
  numLEDs = 300
  RED = { 'h': 360 - 0, 's': 1.0, 'v': .8 }
  GREEN = { 'h': 360 - 145, 's': 1.0, 'v': 1.0}
  BLUE =  { 'h': 360 - 126, 's': 1.0, 'v': 1.0 }
else:
  numLEDs = 35
  RED = { 'h': 0, 's': 1.0, 'v': 1.0 }
  GREEN = { 'h': 145, 's': 0.5, 'v': 1.0}
  BLUE =  { 'h': 126, 's': 1.0, 'v': 1.0 }

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
                        GREEN,
                        GREEN ]}

ledSeq3 = { 'type': 'steady-repeat-colors',
            'interval': 1.0,
            'colors': [ RED, GREEN ]}

cnt = 0
while True:
  if isNowInTimePeriod(startTime, endTime, dt.datetime.now().time()):
    # Prepare JSON data to send
    if cnt % 3 == 0:
      data_to_send = { 'state': True,
                       'num-leds': numLEDs,
                       'sequence': ledSeq1 }
    elif cnt % 3 == 1:
      data_to_send = { 'state': True,
                       'num-leds': numLEDs,
                       'sequence': ledSeq2 }
    elif cnt % 3 == 2:
      data_to_send = { 'state': True,
                       'num-leds': numLEDs,
                       'sequence': ledSeq3 }
    else:
      data_to_send = { 'state': False,
                       'num-leds': numLEDs }

    cnt = (cnt + 1) % 3
    print("cnt:", cnt)

  else:
    print(dt.datetime.now().time())
    data_to_send = { 'state': False,
                     'num-leds': numLEDs }

  json_data = json.dumps(data_to_send)

  # Send JSON data over serial
  ser.write(json_data.encode() + b'\n')

  NACK = True
  while NACK:
    # Read response from the other device
    response = ser.readline().decode().strip()
    if response:
      try:
        response_data = json.loads(response)
        if response_data['rtn'] != 'ACK':
          NACK = True
          print("ERROR: no ack, will resend", response_data)
        else:
          NACK = False
      except json.JSONDecodeError:
        print("Received invalid JSON data |" + response + '|')
        
    
  time.sleep(5)
