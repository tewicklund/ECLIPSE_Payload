#This code tries to calculate the distance from the rocket to the payload using the RSSI of the recieved packets


#import any packages we might need:
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

#test connection to the Radio:
try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    print('RFM9x: Detected')
except RuntimeError as error:
    # Thrown on version mismatch
    print('RFM9x Error: ', error)
    
#print RSSI of packets labelled "RDE"
while True:
    packet=None
    packet=rfm9x.receive()
    if packet is None:
        print("waiting for packet")
    else:
        last10values=[0,0,0,0,0,0,0,0,0,0]
        for x in last10values:
            prev_packet=packet
            packet_text=str(prev_packet, "utf-8")
            if (packet_text=="RDE"):
                rssi=rfm9x.last_rssi
                last10values(x)=rssi
                rssiString=str(rssi)
                #print("Signal Strength:" + rssiString + " dBm")
                #distance=rssi*???
            time.sleep(0.1)
        AverageRSSI=sum(last10values)/10
        print(AverageRSSI)
        
        
