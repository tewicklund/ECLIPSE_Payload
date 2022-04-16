#! /usr/bin/env python3
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
    print('RFM9x: Detected')
except RuntimeError as error:
    # Thrown on version mismatch

    print('RFM9x Error: ', error)
while True:
    packet=None
    packet=rfm9x.receive()
    if packet is None:
        print("waiting for packet")
        pass
    else:
        prev_packet=packet
        packet_text=str(prev_packet, "utf-8")
        print(packet_text)
        packet_int=int(packet_text[0:-1])
        packet_int=int((packet_int-620)*.18)
        print("{:.0f} {:.0f}".format(packet_int, rfm9x.last_rssi*-1))
        #print(str)
    time.sleep(0.1)
