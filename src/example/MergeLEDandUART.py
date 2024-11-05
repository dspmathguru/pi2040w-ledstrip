#
import plasma
from plasma import plasma2040
import time
import os
import machine

uart = machine.UART(0, 115200)
print(uart)

b = None
msg = ""

NUM_LEDS = 35
HUE_1 = 10
HUE_2 = 283.7
BRIGHTNESS = 0.5
SPEED = 0.5

SATURATION = 1.0
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma2040.DAT)

# Start updating the LED strip
led_strip.start()

while True:
    for i in range(NUM_LEDS):
        # the if statements below use a modulo operation to identify the even and odd numbered LEDs
        if (i % 2) == 0:
            led_strip.set_hsv(i, HUE_1 / 360, SATURATION, BRIGHTNESS)
        else:
            led_strip.set_hsv(i, HUE_2 / 360, SATURATION, BRIGHTNESS)
    time.sleep(SPEED)

    for i in range(NUM_LEDS):
        if (i % 2) == 0:
            led_strip.set_hsv(i, HUE_2 / 360, SATURATION, BRIGHTNESS)
        else:
            led_strip.set_hsv(i, HUE_1 / 360, SATURATION, BRIGHTNESS)
    time.sleep(SPEED)
    if uart.any():
      b = uart.readline()
      print(type(b))
      print(b)
      try:
        msg = b.decode('utf-8')
        print(type(msg))
        print(">> " + msg)
      except:
        pass

    
