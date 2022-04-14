import numpy as np
import warnings
import pandas as pd
import sys
warnings.filterwarnings('ignore')

#! /usr/bin/env python3
#recommended usage:
#python -u ./PrintRSSI.py | ./arrayTest.py

print("hello!")

#Creating Data Set For Testing 1
angles1 = np.linspace(1,360,360)
strengths1 = np.linspace(-60,-60,45)
strengths = np.linspace(-30,-30,180)
strengths2 = np.linspace(-60,-60,135)
strengths1 = np.concatenate((strengths1, strengths, strengths2))
strengths1 = strengths1[0:320]

#Creating Data Set For Testing 2
angles2 = np.linspace(1,360,360)
twostrengths1 = np.linspace(-60,-60,45)
twostrengths = np.linspace(-30,-30,180)
twostrengths2 = np.linspace(-60,-60,135)
strengths2 = np.concatenate((twostrengths1, twostrengths, twostrengths2))
strengths2 = strengths2[0:320]

def RDE(RSSI):
    distance = RSSI
    return distance

def takerange():
    sampleCount=711
    arr=np.full(sampleCount, np.NaN)
    for i in range(sampleCount):
        data=input()
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
    data3 = takerange()
    data4 = takerange()
    data = np.mean([data1,data2,data3,data4], axis = 0)
    return(data)

strengths1 = takedataset()
RSS1 = max(strengths1)
distance12 = RDE(RSS1)
angles1 = np.linspace(1,360,360)
angles2 = np.linspace(1,360,360)

#strength = np.zeros(360)
#Angles = int((a-620)*(180/1000))
#strength[Angles] = RecievedStrength

runtime = 1
for i in range(runtime):

    strengths1 = takedataset()
    RSS1 = max(strengths1)
    distance23 = RDE(RSS1)

    #Blindspot 1
    bottom = strengths2[0:4]
    bottom = np.nanmean(bottom)
    top = strengths1[315:319]
    top = np.nanmean(top)
    add = np.linspace(top,bottom,40)
    strengths1 = np.concatenate((strengths1, add))
    col_mean = np.nanmean(strengths1, axis=0)
    inds = np.where(np.isnan(strengths1))
    strengths1[inds] = np.take(col_mean, inds[1])

    #Blindspot 2
    bottom = strengths2[0:4]
    bottom = np.nanmean(bottom)
    top = strengths2[315:319]
    top = np.nanmean(top)
    add = np.linspace(top,bottom,40)
    strengths2 = np.concatenate((strengths2, add))
    angles1[strengths1 != np.NaN]
    col_mean = np.nanmean(strengths1, axis=0)
    inds = np.where(np.isnan(strengths1))
    strengths1[inds] = np.take(col_mean, inds[1])

    #Circular Means
    angles1 = np.deg2rad(angles1)
    angles2 = np.deg2rad(angles2)
    strengths1 = ((min(strengths1))/strengths1)
    strengths2 = ((min(strengths1))/strengths2)
    strengths1 = (strengths1/(sum(strengths1)))
    sins = np.mean(np.sin(angles1)*strengths1)
    coss = np.mean(np.cos(angles1)*strengths1)
    AverageAngle1 = abs(np.rad2deg(np.arctan2(sins,coss)))
    strengths2 = (strengths2/(sum(strengths2)))
    sins = np.mean(np.sin(angles1)*strengths2)
    coss = np.mean(np.cos(angles1)*strengths2)
    AverageAngle2 = abs(np.rad2deg(np.arctan2(sins,coss)))

    #Average Angle
    print("Average Angle 1:")
    print(AverageAngle1)
    print("Average Angle 2:")
    print(AverageAngle2)

    #Distance Calculation
    Angle1 = np.deg2rad(AverageAngle1)
    Angle2 = np.deg2rad(AverageAngle2)

    groundx = distance12*np.cos(Angle1)
    groundy = distance12*np.sin(Angle1)

    finalx = groundx + distance23*np.cos(Angle2)
    finaly = groundy + distance23*np.sin(Angle2)

    X = finalx
    Y = finaly

    print("Final X Coordinate:")
    print(finalx)
    print("Final Y Coordinate:")
    print(finaly)
