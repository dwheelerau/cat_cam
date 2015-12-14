#!/usr/bin/env python

import Adafruit_BBIO.GPIO as GPIO
import time
from time import gmtime,strftime #for formated time

ALARM_LEVEL = 5 #set to 5 as only that many lights

def init_gpio():
    #init GPIOs
    GPIO.setup("P8_10", GPIO.OUT)
    GPIO.setup("P8_12", GPIO.OUT)
    GPIO.setup("P8_14", GPIO.OUT)
    GPIO.setup("P8_16", GPIO.OUT)
    #GPIO.setup("P8_18", GPIO.OUT) #maybe change to 26
    GPIO.setup("P8_26", GPIO.OUT) #alarm ping

#alert function for led control

def indicate_alert(alarm_level):
    if alarm_level == 0:
        GPIO.output("P8_10", GPIO.LOW)
        GPIO.output("P8_12", GPIO.LOW)
        GPIO.output("P8_14", GPIO.LOW)
        GPIO.output("P8_16", GPIO.LOW)
        #GPIO.output("P8_18", GPIO.LOW)
        GPIO.output("P8_26", GPIO.LOW)

    if  alarm_level >= 1:
        GPIO.output("P8_10", GPIO.HIGH)
    if  alarm_level >= 2:
        GPIO.output("P8_12", GPIO.HIGH)
    if  alarm_level >= 3:
        GPIO.output("P8_14", GPIO.HIGH)
    if  alarm_level >= 4:
        GPIO.output("P8_16", GPIO.HIGH)
    #note I have not shown the P_18 string here
    if  alarm_level >= 5:
        GPIO.output("P8_26", GPIO.HIGH)

#main function to start monitoring
def start_monitoring():

    alarm_buffer = 0
    init_gpio()

    while True:
        new_state = GPIO.input("P8_8")
        if new_state == 0:
            alarm_buffer += 1

            indicate_alert(alarm_buffer)

            if alarm_buffer > ALARM_TRIGGER:
                alarm_buffer = 0

                alarm_status = "@%s ALARM" % time.strftime(
                "%y-%m-%d %H:%M:%S")
                print alarm_status

                #trigger alarm with 5 flashes (this could be camera)

                for i in range(0,5): #flash last led
                    GPIO.output("P8_26", GPIO.HIGH)
                    time.sleep(0.3)
                    GPIO.output("P8_26", GPIO.LOW)
                    time.sleep(0.3)

        else:#no alarm info comming through reset
            alarm_buffer = 0
            indicate_alert(alarm_buffer)
        time.sleep(0.1)

