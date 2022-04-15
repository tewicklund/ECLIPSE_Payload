import numpy as np
import warnings
import sys
import time
import RPi.GPIO as GPIO
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_rfm9x
warnings.filterwarnings('ignore')

#This code sends a start pulse and then waits for result

# Configure RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

#Configure the GPIO:
GPIO.setmode(GPIO.BCM)

#Check connection to Radio:
try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 910.0)
    print('RFM9x: Detected')
    #set transmission power to max (5 to 23)
    rfm9x.tx_power=23
    
except RuntimeError as error:
    # Thrown on version mismatch
    print('RFM9x Error: ', error)
 
#Rapidly send the string "RDE"
print("Sending Start Pulses...")
def start():
    while True:
        message=bytes("START","utf-8")
        rfm9x.send(message)
        packet=rfm9x.receive()
        if packet is None:
            print("waiting for packet")
        else:
            print("Recieved Start Confirmation")
            sys.exit()
        time.sleep(0.01)

start()

packet_text = 'Started'
while True:
    packet=rfm9x.receive()
    if packet is None:
        print("Last Location")
        print(packet_text)
    else:
        print("Recieved Location")
        prev_packet=packet
        packet_text=str(prev_packet, "utf-8")
        print(packet_text)
    time.sleep(0.01)
