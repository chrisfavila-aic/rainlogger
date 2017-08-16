source /home/pi/rainlogger.conf

if [ "$(hostname -I | grep 172)" ]; then
    if [ "$(iwlist wlan0 scan | grep $SSID_SITE)" ] || [ "$(iwlist wlan0 scan | grep $SSID_MOBILE)" ]; then
        ifdown wlan0
        ifup wlan0;
    fi;
fi
