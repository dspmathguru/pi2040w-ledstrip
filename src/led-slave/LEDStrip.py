import plasma
from plasma import plasma2040
import time
import utime
import gc

class LEDStrip:
  isEven = True
  mS = 1000

  def __init__(self, nL = 35):
    # Set how many LEDs you have
    self.NUM_LEDS = nL
    self.on = False
    self.led_strip = plasma.WS2812(self.NUM_LEDS, 0, 0, plasma2040.DAT)
    self.seq = None

    # Start updating the LED strip
    self.led_strip.start()
    current_time = utime.ticks_ms()
    self.last_time = current_time

  def setState(self, packet):
    if 'state' in packet:
      self.on = packet['state']
    
  def setSeq(self, seq):
    self.seq = seq
    self.cnt = 0
    self.Ncolors = len(seq['colors'])

  def setHSV(self, i, hsv):
    self.led_strip.set_hsv(i, hsv['h'] / 360., hsv['s'], hsv['v'])

  # shouldn't be called outside, this is private
  def _doSeq(self):
    if self.seq['type'] == 'shift-colors':
      print('type:', self.seq['type'])
      for i in range(self.NUM_LEDS):
        self.setHSV(i, self.seq['colors'][(i + self.cnt) % self.Ncolors])
      self.cnt = (self.cnt + 1) % self.Ncolors
    if self.seq['type'] == 'steady-repeat-colors':
      if self.cnt == 0:
        print('type:', self.seq['type'])
        for i in range(self.NUM_LEDS):
          self.setHSV(i, self.seq['colors'][i % self.Ncolors])
        self.cnt = 1

  def setNumLEDs(self, nL):
    self.NUM_LEDS = nL
    self.led_strip.stop()
    self.led_strip = plasma.WS2812(self.NUM_LEDS, 0, 0, plasma2040.DAT)
    self.led_strip.start()

  def turnOff(self):
    print('off')
    self.on = False
    for i in range(self.NUM_LEDS):
      self.setHSV(i, { 'h': 0, 's': 0, 'v': 0 } )
    self.seq = None

  def doSeq(self):
    current_time = utime.ticks_ms()
    tick_time = utime.ticks_diff(current_time, self.last_time)
    if self.seq and (tick_time > self.seq['interval'] * self.mS):
      if self.on:
        self._doSeq()
      else:
        self.turnOff()
      self.last_time = current_time

def main():
  ls = LEDStrip()
  ledSeq = { 'type': 'swap-colors',
               'interval': 1.0,
               'colors': [ { 'h': 0, 's': 1.0, 'v': 0.35 },
                           { 'h': 0, 's': 1.0, 'v': 0.35 },
                           { 'h': 0, 's': 1.0, 'v': 0.35 },
                           { 'h': 0, 's': 1.0, 'v': 0.35 },
                           { 'h': 0, 's': 1.0, 'v': 0.35 },
                           { 'h': 126, 's': 1.0, 'v': 0.5 } ]}

  ls.setSeq(ledSeq)

  while true:
    ls.doSeq()
    utime.sleep_ms(30)

if __name__ == "__main__":
    main()

