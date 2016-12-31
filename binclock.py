#!/usr/bin/env python

# simple binary clock
# bcd for hours, minutes and seconds
# chart for time past the hour (one light per whole ten minutes)
# please see disclaimer at bottom of file

import sys
import time
import urllib
import urllib.parse
import urllib.request
import json
import scrollphat
import secret

weatherurl = "http://api.openweathermap.org/data/2.5/weather?"
location = "Arlesey"

def string_to_bcd(digit):

    bcd_digit = bin(int(digit))[2:]
    return ('00000' + bcd_digit)[-5:]


def plot_digit(digit, position):

    bcd_digit = string_to_bcd(digit)
    for y in range(0, 5, 1):
        scrollphat.set_pixel(position, y, int(bcd_digit[y]) == 1)


def weather():
    url = weatherurl + urllib.parse.urlencode({'q':location,'APPID':secret.appid,'units':'metric'})
    uh = urllib.request.urlopen(url)
    data = uh.read().decode('utf-8')
    js = json.loads(data)
    conditions = js['weather'][0]['main']
    temperature = js['main']['temp']
    scrollphat.write_string(conditions + " " + str(temperature) + "C   ")
    for i in range(scrollphat.buffer_len()*2):
        try:
            scrollphat.scroll()
            time.sleep(0.1)
        except KeyboardInterrupt:
            scrollphat.clear()
            sys.exit(-1)
    scrollphat.clear()


scrollphat.set_brightness(25)
while True:
    try:
        current = time.strftime('%H0%M0%S')
        for x in range(0, 8):
            plot_digit(current[x], x)
        for i in range(0, 5):
            scrollphat.set_pixel(10, i, (5 - i) <= ((int(current[3:5])) / 10))
        scrollphat.update()
        if current[-2:] == "00":
            weather()
        time.sleep(0.5)
    except KeyboardInterrupt:
        scrollphat.clear()
        sys.exit(-1)
