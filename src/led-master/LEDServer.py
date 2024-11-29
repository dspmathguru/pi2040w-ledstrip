#! /usr/bin/env python

import serial
import json
import time

# Open a serial connection on the Pi's UART port
ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)

state = True

while True:
  # Prepare JSON data to send
  data_to_send = {
    "state": state
  }
  state = not state
  json_data = json.dumps(data_to_send)

  # Send JSON data over serial
  ser.write(json_data.encode() + b'\n')
  print(f"Sent: {json_data}")

  # Read response from the other device
  response = ser.readline().decode().strip()
  if response:
    try:
      response_data = json.loads(response)
      print(f"Received: {response_data}")
    except json.JSONDecodeError:
      print("Received invalid JSON data")

  time.sleep(5)  # Wait for 2 seconds before next transmission
