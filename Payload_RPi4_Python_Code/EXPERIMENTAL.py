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

# Configure RFM9x LoRa Radio

CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

#! /usr/bin/env python3
#recommended usage:
#python -u ./PrintRSSI.py | ./DataGather.py


#check that the radio works:
try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    print('RFM9x: Detected')
except RuntimeError as error:
    # Thrown on version mismatch

    print('RFM9x Error: ', error)

def returnRSSI():
    packet=None
    packet=rfm9x.receive()
    if packet is None:
        return("waiting for packet")
        pass
    else:
        prev_packet=packet
        packet_text=str(prev_packet, "utf-8")
        packet_int=int(packet_text[0:-1])
        packet_int=int((packet_int-620)*.18)
        return("{:.0f} {:.0f}".format(packet_int, rfm9x.last_rssi*-1))




def takerange():
    sampleCount=711
    arr=np.full(sampleCount, np.NaN)
    for i in range(sampleCount):
        data=returnRSSI()
        if(data.replace(" ","").isdigit()): #remove spaces to check if only numbers recieved
            print("number detected")
            a, b = map(int, data.split())
            print("got data "+str(b)+" at coord "+str(a))
		    ####TODO: change index from i to instead be calculated by angle from message
            arr[int(a)]=b
        else:
            print("warning, number not found, got "+data)
    return(arr)

def takedataset():
    data1 = takerange()
    data2 = takerange()
    #data3 = takerange()
    #data4 = takerange()
    data = np.mean([data1,data2], axis = 0)
    data = data[0:359]
    return(data)

strengths1 = takedataset()
angles1 = np.linspace(1,360,360)

print("Data Set:")
print(strengths1)
print("Max RSSI:")
print(max(strengths1))
print("Min RSSI:")
print(min(strengths1))
