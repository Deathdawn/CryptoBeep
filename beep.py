import configparser
import requests
from gpiozero import Buzzer
from time import sleep
import logging
import RPi.GPIO as GPIO
import sys,os


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Get the .ini
config = configparser.ConfigParser()
config.read('param.ini')


# Set the port numbers
red = int(config['PIN_CONF']['RED'])
green = int(config['PIN_CONF']['GREEN'])
buzzer = Buzzer(int(config['PIN_CONF']['BUZZER']))

# Set the app configuration
buzz_active = int(config['BUZZ_CONF']['BUZZ_ACTIVE'])
buzz_duration = float(config['BUZZ_CONF']['BUZZ_DURATION'])
buzz_gain_interval = float(config['BUZZ_CONF']['BUZZ_GAIN_INTERVAL'])

# Set app configuration
api_link = str(config['APP_CONF']['API_LINK'])
crypto = str(config['APP_CONF']['CRYPTO'])
end_currency = str(config['APP_CONF']['END_CURRENCY'])
crypto_conversion = str(crypto + end_currency )
check_interval = int(config['APP_CONF']['CHECK_INTERVAL'])
mode = str(config['APP_CONF']['MODE'])
variation_scale = float(config['APP_CONF']['VARIATION'])

# Set the 1st old_value to the value of the crypto now for determined the 1st variation 
old_value = float(requests.get(api_link + crypto_conversion).json()['result']['X' + crypto + 'Z' + end_currency]['a'][0]) #requests.get(api_link + crypto_conversion).json()['result']['X' + crypto + 'Z' + end_currency]['a'][0]


def blink(pin):
    logging.debug('blink_fonct')
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)

def turnoff(pin):
    logging.debug('turnoff_fonct')
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)

def gain():
    logging.debug('gain_fonct')
    blink(green)
    turnoff(red)
    if(buzz_active):
        buzzer.on()
        sleep(buzz_duration)
        buzzer.off()
        sleep(buzz_gain_interval)
        buzzer.on()
        sleep(buzz_duration)
        buzzer.off()
    

    
def perdition():
    logging.debug('perdition_fonct')
    turnoff(green)
    blink(red)
    if(buzz_active):
        buzzer.on()
        sleep(buzz_duration*2)
        buzzer.off()
    


def time(variation):
    print("time mode")
    if (variation > 0) :
        gain()
    elif (-variation < 0) :
        perdition()
    print(crypto + " Value : " + str(new_value) + '\n' + "Variation : \n" + str(variation))
    return float(new_value)

def variation(variation):
    print("variation mode")
    if (variation > variation_scale) :
        gain()
        print(crypto + " Value : " + str(new_value) + " OldValue : " + str(old_value) + '\n' + "Variation : \n" + str(variation))
        return float(new_value)
    elif (variation < -variation_scale) :
        perdition()
        print(crypto + " Value : " + str(new_value) + " OldValue : " + str(old_value) + '\n' + "Variation : \n" + str(variation))
        return float(new_value)
    print(crypto + " Value : " + str(new_value) + " OldValue : " + str(old_value) + '\n' + "Variation : \n" + str(variation))
    return float(old_value)

chose_mode = {"TIME" : time , "VARIATION" : variation}

while 1 :
    
    print("###############")
    new_value = float(requests.get(api_link + crypto_conversion).json()['result']['X' + crypto + 'Z' + end_currency]['a'][0])
    variation = (float(new_value) - float(old_value))/float(new_value) * 100  
    old_value = chose_mode.get(mode)(variation)
    sleep(check_interval)

