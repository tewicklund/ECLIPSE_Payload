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
warnings.filterwarnings('ignore')

#! /usr/bin/env python3
#recommended usage:
#python -u ./PrintRSSI.py | ./arrayTest.py

print("hello!")

CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

starttime = str(datetime.now().time())

#Look For Start Signal
try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 910.0)
    print('RFM9x: Detected')
    #set transmission power to max (5 to 23)
    rfm9x.tx_power=23

except RuntimeError as error:
    # Thrown on version mismatch
    print('RFM9x Error: ', error)
packet_text = 'Started'

def findstart():
    g = 0
    while g == 0:
        packet=rfm9x.receive()
        if packet is None:
            print("Looking For Start Signal")
        else:
            print("Found Start Signal")
            message=bytes("START","utf-8")
            for i in range(30):
                for i in range(100):
                    rfm9x.send(message)
                    time.sleep(0.01)
                print("Sending Confirmation")
                g=1
                break
        time.sleep(0.01)

findstart()
print("Found Start Signal")

#check that the radio works:
try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    print('RFM9x: Detected')
except RuntimeError as error:
    # Thrown on version mismatch

    print('RFM9x Error: ', error)

def coord(X, Y):
    if X >= 0 and X <= 250:
        X = "K"
    elif X>250 and X <=500:
        X = "L"
    elif X>500 and X <=750:
        X = "M"
    elif X>750 and X <=1000:
        X = "N"
    elif X>1000 and X <=1250:
        X = "O"
    elif X>1250 and X <=1500:
        X = "P"
    elif X>1500 and X <=1750:
        X = "Q"
    elif X>1750 and X <=2000:
        X = "R"
    elif X>2000 and X <=2250:
        X = "S"
    elif X>2250 and X <=2500:
        X = "T"
    elif X<0 and X >= -250:
        X = "J"
    elif X<-250 and X >=-500:
        X = "I"
    elif X<-500 and X >=-750:
        X = "H"
    elif X<-750 and X >=-1000:
        X = "G"
    elif X<-1000 and X >=-1250:
        X = "F"
    elif X<-1250 and X >=-1500:
        X = "E"
    elif X<-1500 and X >=-1750:
        X = "D"
    elif X<-1750 and X >=-2000:
        X = "C"
    elif X<-2000 and X >=-2250:
        X = "B"
    elif X<-2250 and X >=-2500:
        X = "A"
    else:
        print("out of range")
        X = "Z"
    
    if Y >= 0 and Y <= 250:
         Y = "10"
    elif Y>250 and Y <=500:
        Y = "9"
    elif Y>500 and Y <=750:
        Y = "8"
    elif Y>750 and Y <=1000:
        Y = "7"
    elif Y>1000 and Y <=1250:
        Y = "6"
    elif Y>1250 and Y <=1500:
        Y = "5"
    elif Y>1500 and Y <=1750:
        Y = "4"
    elif Y>1750 and Y <=2000:
        Y = "3"
    elif Y>2000 and Y <=2250:
        Y = "2"
    elif Y>2250 and Y <=2500:
        Y = "1"
    elif Y<0 and Y >= -250:
        Y = "11"
    elif Y<-250 and Y >=-500:
        Y = "12"
    elif Y<-500 and Y >=-750:
        Y = "13"
    elif Y<-750 and Y >=-1000:
        Y = "14"
    elif Y<-1000 and Y >=-1250:
        Y = "15"
    elif Y<-1250 and Y >=-1500:
        Y = "16"
    elif Y<-1500 and Y >=-1750:
        Y = "17"
    elif Y<-1750 and Y >=-2000:
        Y = "18"
    elif Y<-2000 and Y >=-2250:
        Y = "19"
    elif Y<-2250 and Y >=-2500:
        Y = "20"
    else:
        print("out of range")
        Y = "99"

    return(X,Y)

def RDE(RSSI):
    distance = 36.7*np.exp(0.0236*RSSI)
    return distance

def returnRSSI():
    try:
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
    except:
        return("waiting for packet")

def takerange(x,y):
    sampleCount=740
    arr=np.full(sampleCount, np.NaN)
    for i in range(sampleCount):
        data=returnRSSI()
        if(data.replace(" ","").isdigit()): #remove spaces to check if only numbers recieved
            print("Number Detected: ", y, x)
            a, b = map(int, data.split())
            print("got data "+str(b)+" at coord "+str(a))
		    ####TODO: change index from i to instead be calculated by angle from message
            arr[int(a)]=float(b)
        else:
            print("warning, number not found, got "+data)
    return(arr)


def takedataset(y):
    data1 = takerange(1,y)
    print(data1)
    data2 = takerange(2,y)
    print(data2)
    data3 = takerange(3,y)
    print(data3)
    data = np.nanmean([data1,data2, data3], axis = 0)
    data = data[0:320]
    print(data)
    return(data)

strengths1 = takedataset(1)
strengths1 = -strengths1
RSS1 = -min(strengths1)
distance12 = RDE(RSS1)
angles1 = np.linspace(1,360,360)
angles2 = np.linspace(1,360,360)

#Blindspot 1
bottom = strengths1[0:4]
bottom = np.nanmean(bottom)
top = strengths1[315:320]
top = np.nanmean(top)
add = np.linspace(top,bottom,40)
strengths1 = np.concatenate((strengths1, add))
mean = np.nanmean(strengths1, axis=0)-20
strengths1 = np.nan_to_num(strengths1,nan=mean)

runtime = 200

for i in range(runtime):
    k = 1

    strengths2 = takedataset(2)
    strengths2 = -strengths2
    RSS2 = -min(strengths2)
    distance23 = RDE(RSS2)

    #Blindspot 2
    bottom = strengths2[0:4]
    bottom = np.nanmean(bottom)
    top = strengths2[315:320]
    top = np.nanmean(top)
    add = np.linspace(top,bottom,40)
    strengths2 = np.concatenate((strengths2, add))
    mean = np.nanmean(strengths2, axis=0)-20
    strengths2 = np.nan_to_num(strengths2,nan=mean)

    #Circular Means
    angles1 = np.deg2rad(angles1)
    angles2 = np.deg2rad(angles2)
    strengths1 = ((min(strengths1))/strengths1)
    strengths2 = ((min(strengths1))/strengths2)
    strengths1 = (strengths1/(np.nansum(strengths1)))
    sins = np.nanmean(np.sin(angles1)*strengths1)
    coss = np.nanmean(np.cos(angles1)*strengths1)
    AverageAngle1 = abs(np.rad2deg(np.arctan2(sins,coss)))
    strengths2 = (strengths2/(np.nansum(strengths2)))
    sins = np.nanmean(np.sin(angles1)*strengths2)
    coss = np.nanmean(np.cos(angles1)*strengths2)
    AverageAngle2 = abs(np.rad2deg(np.arctan2(sins,coss)))

    #Average Angle
    print("Average Angle 1:")
    print(AverageAngle1)
    print("Average Angle 2:")
    print(AverageAngle2)

    #Distance Calculation
    Angle1 = np.deg2rad(AverageAngle1)
    Angle2 = np.deg2rad(AverageAngle2)

    groundx = -distance12*np.cos(Angle1)
    groundy = -distance12*np.sin(Angle1)

    finalx = groundx + distance23*np.cos(Angle2)
    finaly = groundy + distance23*np.sin(Angle2)

    print("Final X Coordinate:")
    print(finalx)
    print("Final Y Coordinate:")
    print(finaly)

    X1,Y1 = coord(finalx, finaly)
    print(["Coordinates: ", X1," ",Y1])
    
    result = X1+Y1

    try:
        rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 910.0)
        print('RFM9x: Detected')
        #set transmission power to max (5 to 23)
        rfm9x.tx_power=23
    
    except RuntimeError as error:
        # Thrown on version mismatch
        print('RFM9x Error: ', error)
    
    #Send Result
    print("Sending Result Pulses...")

    def start():
        i = 0
        while i < 100:
            message=bytes(result,"utf-8")
            rfm9x.send(message)
            time.sleep(0.01)
            i = i + 1
    start()

    lines = ["Flight: ", str(k)]
    lines1 = ["Coordinates: ", X1," ",Y1]
    lines2 = ["Coordinates (X,Y): ", str(finalx)," ",str(finaly)]
    lines3 = ["Angles (1,2): ", str(np.rad2deg(Angle1))," ",str(np.rad2deg(Angle2))]
    with open('PayloadCoord_{}.txt'.format(starttime), 'a') as f:
        f.writelines(lines)
        f.write("\n")
        f.writelines(lines1)
        f.write("\n")
        f.writelines(lines2)
        f.write("\n")
        f.writelines(lines3)
        f.write("\n")
        f.write("\n")

    try:
        rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
        print('RFM9x: Detected')
    except RuntimeError as error:
        # Thrown on version mismatch
        print('RFM9x Error: ', error)
    k = k+1
