#This code turns on the blue LED if the ground station is receiving packets, red if it isn't.

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
    #Configure blue and red LEDs
    blueLED=26
    redLED=19

    GPIO.setup(blueLED, GPIO.OUT)    #blue LED
    GPIO.setup(redLED, GPIO.OUT)    #red LED
    while True:
    packet=None
    packet=rfm9x.receive()
    if packet is None:
        print("waiting for packet")
        GPIO.output(redLED, GPIO.HIGH)
        GPIO.output(blueLED, GPIO.LOW)
    else:
        prev_packet=packet
        GPIO.output(redLED, GPIO.LOW)
        GPIO.output(blueLED, GPIO.HIGH)
        
        
    time.sleep(0.1)
except RuntimeError as error:
    # Thrown on version mismatch

    print('RFM9x Error: ', error)
    


#GPIO.output(blueLED, GPIO.HIGH)
#GPIO.output(redLED, GPIO.HIGH)


