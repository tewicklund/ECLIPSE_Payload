#https://learn.adafruit.com/lora-and-lorawan-radio-for-raspberry-pi/raspberry-pi-wiring
#sudo pip3 install adafruit-circuitpython-rfm9x

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


try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    rfm9x.tx_power=23
    print('RFM9x: Detected')
except RuntimeError as error:
    # Thrown on version mismatch

    print('RFM9x Error: ', error)
while True:

    message=bytes("Hey","utf-8")
    rfm9x.send(message)
    time.sleep(0.01)
