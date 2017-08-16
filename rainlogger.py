#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import urllib2

#dictionary to hold parameters from rainlogger.conf
conf_params={}

#store parameters to a dictionary
with open('/home/pi/rainlogger.conf') as f:
  for line in f:
    (key, val) = line.split('=')
    conf_params[key] = val

#GPIO pin to monitor
PIN = 17

#setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#variable to monitor
tip_state = False

#callback
def cb(channel):
    global tip_state
    tip_state = True

#register the callback to pin interrupt
GPIO.add_event_detect(PIN, GPIO.FALLING, callback=cb, bouncetime=1000)

#loop
try:
    while True:
        if tip_state == True:
           if GPIO.input(PIN) == True:
               with open(conf_params['DATA_FOLDER'] + "/false_positives.csv", "a") as file:
                   file.write(time.strftime("%y/%m/%d %H:%M:%S") + "\n")
               tip_state = False
               print "false positive"
           
        if tip_state == True:
           timestamp = time.strftime("%y/%m/%d %H:%M:%S")
           date = time.strftime("%y%m%d")
           filename = conf_params['DATA_FOLDER'] + "/" + date + ".csv"
           with open(filename, 'a') as file:
               file.write(timestamp + '\n')
           try:
               urllib2.urlopen("https://api.thingspeak.com/update?api_key=" + conf_params['THINGSPEAK_KEY'] + "&field1=" + timestamp)
           except:
               print "can't upload" 
           tip_state = False
           print "tip detected!"
        
        
except:
    print "error occured"

finally:
    GPIO.cleanup()
