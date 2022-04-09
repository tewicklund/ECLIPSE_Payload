#This code constantly sends a pluse that says "RDE"
#This comment was added as a test

#General setup:
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

#Configure the GPIO:
GPIO.setmode(GPIO.BCM)

#Check connection to Radio:
try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    print('RFM9x: Detected')
    #set transmission power to max (5 to 23)
    rfm9x.tx_power=23
    
except RuntimeError as error:
    # Thrown on version mismatch
    print('RFM9x Error: ', error)
 
#Rapidly send the string "RDE"
print("Sending Pulses...")
while True:
    message=bytes("RDE","utf-8")
    rfm9x.send(message)
    time.sleep(0.01)
