import numpy as np
import warnings
import sys
warnings.filterwarnings('ignore')

#! /usr/bin/env python3
#recommended usage:
#python -u ./PrintRSSI.py | ./DataGather.py

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
angles1 = np.linspace(1,360,360)

print("Data Set:")
print(strengths1)
print("Max RSSI:")
print(max(strengths1))
print("Min RSSI:")
print(min(strengths1))
