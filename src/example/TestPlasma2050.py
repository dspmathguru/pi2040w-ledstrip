# Code from https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/examples/plasma2040/alternating-blinkies.py
# Assumes use of https://shop.pimoroni.com/products/10m-addressable-rgb-led-star-wire

# This super simple example sets up two alternating colours, great for festive lights!

import plasma
from plasma import plasma2040
import time

# Set how many LEDs you have
NUM_LEDS = 35

# Pick two hues from the colour wheel (from 0-360°, try https://www.cssscript.com/demo/hsv-hsl-color-wheel-picker-reinvented/ )
HUE_1 = 10
HUE_2 = 283.7

# Set up brightness (between 0 and 1)
BRIGHTNESS = 0.5

# Set up speed (wait time between colour changes, in seconds)
SPEED = 1

SATURATION = 1.0

# Pick *one* LED type by uncommenting the relevant line below:

# APA102 / DotStar™ LEDs
# led_strip = plasma.APA102(NUM_LEDS, 0, 0, plasma2040.DAT, plasma2040.CLK)

# WS2812 / NeoPixel™ LEDs
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
