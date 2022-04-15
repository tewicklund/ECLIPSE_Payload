#! /usr/bin/env python3

#recommended usage:
#python -u ./PrintRSSI.py | ./arrayTest.py

import numpy as np
import sys

print("hello!")
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
arr = arr[0:359]
print("Data Set:")
print(arr)
print("Max RSSI:")
print(max(arr))
print("Min RSSI:")
print(min(arr))
