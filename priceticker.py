#!/usr/bin/env python

# simple binary clock
# bcd for hours, minutes and seconds
# chart for time past the hour (one light per whole ten minutes)
# show weather every hour

import sys
import time
import urllib
import urllib.parse
import urllib.request
import json
import scrollphat
import secret
import requests

weatherurl = "http://api.openweathermap.org/data/2.5/weather?"
steemurl = "https://api.coinmarketcap.com/v1/ticker/steem/"
sbdurl = "https://api.coinmarketcap.com/v1/ticker/steem-dollars/"

def scroll():
    time.sleep(0.5)
    for i in range(scrollphat.buffer_len()*2-11):
        try:
            scrollphat.scroll()
            time.sleep(0.2)
        except KeyboardInterrupt:
            scrollphat.clear()
            sys.exit(-1)


def getweather():
    #print('Get weather')
    url = weatherurl + urllib.parse.urlencode({'q':secret.location,'APPID':secret.appid,'units':'metric'})
    uh = urllib.request.urlopen(url)
    data = uh.read().decode('utf-8')
    js = json.loads(data)
    conditions = js['weather'][0]['main']
    temperature = js['main']['temp']
    weatherstr = conditions + " " + str(round(temperature, 1)) + "C     "
    return weatherstr


def getprices():
    #print('Get prices')
    resp = requests.get(steemurl)
    steemprice = resp.json()[0]['price_usd']
    resp = requests.get(sbdurl)
    sbdprice = resp.json()[0]['price_usd']
    pricestr = "Stm $" + str(round(float(steemprice), 2)) + "   SBD $" + str(round(float(sbdprice), 2)) + "     "
    return pricestr


def showstr(s):
    scrollphat.write_string(s)
    scroll()
    scrollphat.clear()


scrollphat.set_brightness(15)
wlasttime = 0
plasttime = 0
while True:
    try:
        #current = time.strftime('%H0%M0%S')
        nowtime = time.time()
        if nowtime - wlasttime > 600:
            weatherstr = getweather()
            wlasttime = nowtime
        if nowtime - plasttime > 120:
            pricestr = getprices()
            plasttime = nowtime
        showstr(weatherstr)
        time.sleep(2.5)
        showstr(pricestr)
        time.sleep(2.5)
    except KeyboardInterrupt:
        scrollphat.clear()
        sys.exit(-1)
