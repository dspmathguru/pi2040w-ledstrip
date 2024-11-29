import plasma
from plasma import plasma2040
import time

class LedStrip:

  def __init__(self, nL = 35, h1 = 0, h2 = 127, b=0.5, s = 1):
    # Set how many LEDs you have
    self.NUM_LEDS = nL

    self.HUE_1 = h1
    self.HUE_2 = h2

    # Set up brightness (between 0 and 1)
    self.BRIGHTNESS = b

    # Set up speed (wait time between colour changes, in seconds)
    self.SPEED = s

    # Pick *one* LED type by uncommenting the relevant line below:

    # APA102 / DotStar™ LEDs
    # led_strip = plasma.APA102(NUM_LEDS, 0, 0, plasma2040.DAT, plasma2040.CLK)
    # WS2812 / NeoPixel™ LEDs
    self.led_strip = plasma.WS2812(self.NUM_LEDS, 0, 0, plasma2040.DAT)

    # Start updating the LED strip
    self.led_strip.start()

  def doBlink(self):
    while True:
      for i in range(self.NUM_LEDS):
        if (i % 2) == 0:
          self.led_strip.set_hsv(i, self.HUE_1 / 360, 1.0, self.BRIGHTNESS)
        else:
          self.led_strip.set_hsv(i, self.HUE_2 / 360, 1.0, self.BRIGHTNESS)
      time.sleep(self.SPEED)

      for i in range(self.NUM_LEDS):
        if (i % 2) == 0:
          self.led_strip.set_hsv(i, self.HUE_2 / 360, 1.0, self.BRIGHTNESS)
        else:
          self.led_strip.set_hsv(i, self.HUE_1 / 360, 1.0, self.BRIGHTNESS)
      time.sleep(self.SPEED)


def main():
  ls = LedStrip()
  ls.doBlink()

if __name__ == "__main__":
    main()
