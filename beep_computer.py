import configparser
import requests
from time import sleep
import logging
import sys,os
import winsound
import ctypes  # An included library with Python install.   




logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)  

# Get the .ini
config = configparser.ConfigParser()
config.read('./param.ini')


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
    print('blink_fonct')


def turnoff(pin):
    print('turnoff_fonct')


def gain():
    print('gain_fonct')
    frequency = 200  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)
    
def perdition():
    print('perdition_fonct')
    frequency = 1000  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

    


def time(variation):
    print("time mode")
    if (variation > 0) :
        gain()
    elif (variation < 0) :
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

