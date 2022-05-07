#This code sends a start pulse and then waits for result

#General setup:

import numpy as np
import warnings
import sys
import time
from datetime import datetime
import RPi.GPIO as GPIO
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_rfm9x
warnings.filterwarnings('ignore')


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
    g = 0
    while g == 0:
        message=bytes("START","utf-8")
        rfm9x.send(message)
        packet=rfm9x.receive()
        if packet is None:
            print("waiting for packet")
        else:
            print("Recieved Start Confirmation")
            g=1
            break
        time.sleep(0.01)

start()
time.sleep(20)

k=0

timest = str(datetime.now().time())

packet_text = 'Started'
while True:
    packet=rfm9x.receive()
    if packet is None:
        print("Last Location")
        print(packet_text)
    else:
        try:
            print("Recieved Location")
            prev_packet=packet
            packet_text=str(prev_packet, "utf-8")
            print(packet_text)
            k=k+1
            lines = ["Flight: ", str(k)]
            lines1 = ["Coordinates: ", packet_text]
            with open('Payload_Landing_Result_{}.txt'.format(timest), 'a') as f:
                f.writelines(lines)
                f.write("\n")
                f.writelines(lines1)
                f.write("\n")
                f.write("\n")
        except:
            print("Last Location")
            print(packet_text)
    time.sleep(0.01)
