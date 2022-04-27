import configparser
import requests
from gpiozero import Buzzer
from time import sleep
import RPi.GPIO as GPIO
import sys,os

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
check_interval = str(config['APP_CONF']['CHECK_INTERVAL'])
mode = str(config['APP_CONF']['MODE'])

# Set the 1st oldvalue to the value of the crypto now for determined the 1st variation 
oldvalue = requests.get(api_link + crypto_conversion).json()['result']['X' + crypto + 'Z' + end_currency]['a'][0]


def blink(pin):
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)

def turnoff(pin):
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)

def gain():
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
    turnoff(green)
    blink(red)
    if(buzz_active):
        buzzer.on()
        sleep(buzz_duration*2)
        buzzer.off()

while 1 :
    print("###############")
    resp = requests.get(api_link + crypto_conversion)
    newvalue = resp.json()['result']['X' + crypto + 'Z' + end_currency]['a'][0]
    variation += float(newvalue)-float(oldvalue)
    match mode :
        case "all" :
            if (variation > 0) :
                gain()
                variation = 0
            if (variation < 0) :
                perdition()
                variation = 0
            break
    print(crypto + " Value : " + newvalue + '\n' + "Variation : \n" + str(variation))
    oldvalue = newvalue
    sleep(check_interval)

