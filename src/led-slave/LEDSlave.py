import ujson
import utime
from machine import UART
import gc
import sys
import micropython

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
        utime.sleep_ms(sleepTime)
        send_json_packet({ 'rtn': 'ACK' })
        rtn = ujson.loads(line)
        return rtn
      except ValueError:
        send_json_packet({ 'rtn': "ERR: Error parsing JSON\n" })
  return None

def parseJSON(packet, ls):
  if 'state' in packet:
    ls.setState(packet)
  if 'sequence' in packet:
    ls.setSeq(packet['sequence'])

def main():
  global on
  last_task = utime.ticks_ms()

  ls = LEDStrip()
  utime.sleep_ms(sleepTime)
  ls.turnOff()

  while True:
    # Check for incoming JSON data
    packet = read_json_packet()
    if packet:
      parseJSON(packet, ls)
            
    # Execute tasks periodically
    ls.doSeq()
        
    # Add a small delay to reduce CPU load, adjust as necessary

    utime.sleep_ms(sleepTime)

if __name__ == "__main__":
  main()

    
