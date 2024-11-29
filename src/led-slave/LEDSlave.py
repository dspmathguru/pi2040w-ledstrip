import ujson
import utime
from machine import UART

from LEDStrip import LEDStrip

# Serial setup for communication
uart = UART(0, 115200)

i = 1 # 1 second
mS = 1000
interval = int(i * mS)
on = False
sleepTime = 10 # mS

# Buffer for incoming data
received_data = ""

def send_json_packet(data):
  json_data = ujson.dumps(data)
  uart.write(json_data + "\n")  # Adding newline for easier parsing

def read_json_packet():
  global received_data
  if uart.any():
    received_data += uart.read().decode()
    if "\n" in received_data:
      line, received_data = received_data.split("\n", 1)
      try:
        send_json_packet({ 'rtn': 'ACK' })
        return ujson.loads(line)
      except ValueError:
        send_json_packet({ 'rtn': "ERR: Error parsing JSON: |" + str(line) + "|\n" })
  return None

def doLED(ls):
  global on
  if on:
    ls.doBlink()
  else:
    ls.doOff()

def parseJSON(packet):
  global on
  if 'state' in packet:
    on = packet['state']

def main():
  global on
  last_task = utime.ticks_ms()

  ls = LEDStrip()
    
  while True:
    # Check for incoming JSON data
    packet = read_json_packet()
    if packet:
      parseJSON(packet)
            
    # Execute tasks periodically
    current_time = utime.ticks_ms()
    tick_time = utime.ticks_diff(current_time, last_task)
    if tick_time > interval:
      doLED(ls)
      last_task = current_time
        
    # Add a small delay to reduce CPU load, adjust as necessary
    utime.sleep_ms(sleepTime)

if __name__ == "__main__":
  main()

    
