import urllib2
import xml.etree.ElementTree as ET
import time
from neopixel import *
import sys
import os


# LED strip configuration:
LED_COUNT      = 57     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 70      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_RGB   # Strip type and colour ordering
		



strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

# retrieve airports from file "airports"
with open("airports") as f:
    airports = f.readlines()
airports = [x.strip() for x in airports]
# print airport # (remove # to output airport list)


lcount = 0 # Counter for number of refreshes on data
looop = 1
while looop == 1: # Starts endless loop of data refreshes
        try:
                lcount = lcount + 1
                mydict = {
                "":""
                }
                url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=1.5&stationString="
                for airportcode in airports:
                        if airportcode == "NULL":
                                continue
                        # print airportcode
                        url = url + airportcode + ","

                # print url # (remove # to show wx request)
                content = urllib2.urlopen(url).read()
                # print content # (remove # to show wx response)


                root = ET.fromstring(content)


                for metar in root.iter('METAR'):
                        if airportcode == "NULL":
                                continue
                        
                        stationId = metar.find('station_id').text
                        # print stationId
                        
                        if metar.find('flight_category') is None:
                                # print "Skipping"
                                continue

                        flightCateory = metar.find('flight_category').text
                        # print flightCateory
                        if stationId in mydict:
                                continue
                        
                        mydict[stationId] = flightCateory
                        
                        

                #print mydict # (remove # to show stations w/WX cat)

                i = 0
                for airportcode in airports:
                        if airportcode == "NULL":
                                i = i +1
                                continue
                        # print 
                        color = Color(0,0,0)

                        flightCateory = mydict.get(airportcode,"No")
                        

                        if  flightCateory != "No":
                                # print airportcode + " " + flightCateory
                                if flightCateory == "VFR":
                                        # print "VFR"
                                        color = Color(75,0,0)
                                elif flightCateory == "MVFR":
                                        color = Color(0,0,255)
                                        # print "MVFR"
                                elif flightCateory == "IFR":
                                        color = Color(0,100,0)
                                        # print "IFR"
                                elif flightCateory == "LIFR":
                                        color = Color(0,100,100)
                                        # print "LIFR"
                        else:
                                color = Color(0,0,0)
                                # print "N/A"

                        print "Setting light " + str(i) + " for " + airportcode + " " + flightCateory + " " + str(color)
                        strip.setPixelColor(i, color)
                        strip.show()
                        time.sleep(1)
                        i = i+1
                # print lcount (remove # to show number of wx updates)
                time.sleep (600) # 10 minutes till next check
                
        except urllib2.URLError:
                print "Connection Reset!"
                time.sleep (180) # pause for 3 minutes on URL err then retry

print "fin"











