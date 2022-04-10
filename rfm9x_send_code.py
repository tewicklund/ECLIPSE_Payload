#https://learn.adafruit.com/lora-and-lorawan-radio-for-raspberry-pi/raspberry-pi-wiring
#sudo pip3 install adafruit-circuitpython-rfm9x

#This code simply sends packets constantly, the LEDs do nothing.

import time
import RPi.GPIO as GPIO
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_rfm9x

# Configure RFM9x LoRa Radio

CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

GPIO.setmode(GPIO.BCM)

rled=19
bled=26
GPIO.setup(rled, GPIO.OUT);
GPIO.setup(bled, GPIO.OUT);

try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    print('RFM9x: Detected')
    #set transmission power to max (5 to 23)
    rfm9x.tx_power=23
except RuntimeError as error:
    # Thrown on version mismatch

    print('RFM9x Error: ', error)
while True:

    message=bytes("Hey","utf-8")
    rfm9x.send(message)
    time.sleep(0.01)
