import numpy as np
from ROOT import *
import time
import datetime
import matplotlib.pyplot as plt
import sys
csv = 'pump.csv'
transducer = [] #Set up all the empty arrays we'll fill with delicious data
currentLoop = []
countDeriv = []
sotera = []
calculated = []
cf = open(csv) #open our csv file
cf.readline() #skip first line
for line in cf:
	a = line.split(',')
	run = a[0]
	f = TFile.Open('out'+run+'.root','read')
	start = a[1]+' '+a[2]
	timestamp = time.mktime(datetime.datetime.strptime(start, '%m/%d/%Y %H:%M:%S').timetuple())
	#timestamp += int(sys.argv[1]) #temporary to test time offset
	dt  = float(a[6])
	m = float(a[5])
	calculated.append(m/dt*60)
	#datarray = [event.channels for event in f.tree if event.time > timestamp and event.time < timestamp + dt]
	datarray = []
	for event in f.tree:
		if event.time > timestamp and event.time < timestamp + dt:
			print(str(event.time)+'\t'+str(event.channels[3])+'\t'+str(dt))
			datarray.append(event.channels)	
	transducer.append(sum([x[5] for x in datarray])/len(datarray))
	currentLoop.append(sum([x[1] for x in datarray])/len(datarray))	
	countDeriv.append(sum([x[3] for x in datarray])/len(datarray))
	sotera.append(float(a[4]))
	f.Close()
#m = [np.polyfit(x,calculated,1) for x in [transducer,currentLoop,countDeriv,sotera]]
#print('Linear Fits for measurements:')
#print('Measurement\t| m\t| b')
#names=['Transducer','Current Loop','Counter','Sotera']
#for cn,n in enumerate(names): print(n+'\t| '+str(m[cn][0]) +'\t| '+ str(m[cn,1]))
plt.figure(1)
plt.subplot(221)
plt.plot(transducer,calculated,'.')
plt.subplot(222)
plt.plot(currentLoop,calculated,'.')
plt.subplot(223)
plt.plot(countDeriv,calculated,'.')
plt.subplot(224)
plt.plot(sotera,calculated,'.')
plt.show()
