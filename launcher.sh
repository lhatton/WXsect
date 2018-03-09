#!/bin/sh
# launcher.sh
# navigate to home, then WXsect, then execute metar script, then back home

# sleep 300
cd /
cd home/pi/WXsect
# sudo python test.py
sudo python metar.py
cd /

