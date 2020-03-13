# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 16:42:49 2020
Data2Graph v2
@author: Jake Ford
"""

import numpy as np
import matplotlib.pyplot as plt
import csv


def script():
    capvals = [10,22]
    files = ["10ncap.txt", "22ncap.txt"]
    for x in range(0,1):
        cap_TvsP(files[x],capvals[x])
    res_TvsP("100res.txt")
    plt.close('all')


def fixdata(input):
    rawdata = np.loadtxt(fname = input,delimiter=",")   # Store data in Numpy Array
    data = rawdata.T                                    # Transpose array to seperate data sets
    dims = data.shape									# Get length of data and therefore time taken
    time = dims[1]
    timeary = np.linspace(1, time, time) 				# Ensure time data is continuous
    data[0] = timeary
    return(data)
    

def cap_TvsP(input,capval):
    plt.close('all')
    data = fixdata(input)
    data[5] = data[5]*0.000000001*capval # calculate charge Q(c) by multiplying (cap) voltage drop by cap value (convert to F from nF)
    starttime = 0
    endtime = 0
    timedif = 0
    time = 0
    twicecount = 0
    prevsign = data[1,0] / abs(data[1,0]) # gives if first cycle value is pos or neg
    timelst = []
    for val in data[1, 0:100000]:
        sign = val / abs(val)
        if (sign != prevsign):
            twicecount = twicecount + 1
            if (twicecount == 1):
                midtime = int(data[0, time]) # Mid point of cycle (when crosses through 0V)
            if (twicecount == 2):
                endtime = int(data[0, time])   # End point of cycle (second time passing through 0V)
                timedif = endtime - starttime   # Length of cycle
                timelst.append([starttime, midtime, endtime, timedif])  # append data to list
                starttime = endtime     # Start of next cycle = End of next
                twicecount = 0        
        prevsign = sign
        time = time + 1 # used to determine current time
    powers = []
    timelst = [ x for x in timelst if 330 <= x[3] <= 335]
    for cycle in timelst:
        area = abs(np.trapz(data[5, cycle[0]:cycle[2]], data[1, cycle[0]:cycle[2]])) # calculate area within lissajous curve (Q(c) vs V) for each cycle
        powers.append([area/(cycle[3]*0.000001), cycle[3]]) # power = area / cycle time in seconds, second half lists cycle time
    timename = str(capval)+"nFcycles.csv"
    with open(timename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(timelst)
    powername = str(capval)+"nFpower.csv"
    with open(powername, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(powers)
        
    powers = np.fliplr(powers)
    
    plt.scatter(*zip(*powers), s = 5) # turn powers[[power1,time1],[power2,time2]] into powers[[power1,power2],[time1,time2]]
    plt.xlabel("Cycle time (in "+r'$\mu$'+"s)")
    plt.ylabel("Power Consumption (in W)")
    plt.title("Cycle length vs Power Consumption, "+str(capval)+"nF (First 100000 microseconds)")
    
    plt.show
    plt.savefig(str(capval)+"nF cycle_times vs power")
    
    
def res_TvsP(input):
    plt.close('all')
    rawdata = np.loadtxt(fname = input,delimiter=",")   # Store data in Numpy Array
    data = rawdata.T                                    # Transpose array to seperate data sets
    dims = data.shape									# Get length of data and therefore time taken
    time = dims[1]
    timeary = np.linspace(1, time, time) 				# Ensure time data is continuous    
    data[0] = timeary
    data[2] = data[2]*0.001 # convert current to A instead of mA
    combineddata = data[5]*data[2]
    starttime = 0
    endtime = 0
    timedif = 0
    time = 0
    twicecount = 0
    prevsign = data[1,0] / abs(data[1,0])
    timelst = [] # start time, mid time, end time
    for val in data[1]:
        sign = val / abs(val)
        if (sign != prevsign):
            twicecount = twicecount + 1
            if (twicecount == 1):
                midtime = int(data[0, time])
            if (twicecount == 2):
                endtime = int(data[0, time])
                timedif = endtime - starttime
                timelst.append([starttime, midtime, endtime, timedif])
                starttime = endtime
                twicecount = 0        
        prevsign = sign
        time = time + 1
    powers = []
    timelst = [x for x in timelst if 330 <= x[3] <= 335]
    popcount = 0
    for time in timelst: # Removing cycles that are too small
        if time[3] < 5:
            timelst.pop(popcount)
            popcount = popcount - 1 # as list gets smaller
        popcount = popcount + 1
        
    for cycle in timelst: # calculating power comp
        power = np.trapz(combineddata[cycle[0]:cycle[2]], data[0, cycle[0]:cycle[2]])
        powers.append([power, cycle[3]])
    
    timename = "100ohmcycles.csv"    
    with open(timename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(timelst)
    powername = "100ohmpower.csv"
    with open(powername, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(powers)
        
    powers = np.fliplr(powers)
    
    plt.scatter(*zip(*powers), s = 5)
    plt.xlabel("Cycle time (in "+r'$\mu$'+"s)")
    plt.ylabel("Power Consumption (in W)")
    plt.title("Cycle length vs Power Consumption, 100ohms")
    
    plt.show
    plt.savefig("100ohm cycle_times vs power")
    

def barcomparison():
    plt.close('all')
    tenpower = []
    tentime = []
    twtwopower = []
    twtwotime = []
    onehunpower = []
    onehuntime = []
    with open('10nFpower.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            power = float(row[0])
            time = float(row[1])
            tenpower.append(power)
            tentime.append(time)
    tenavg = sum(tenpower)/len(tenpower)
    
    with open('22nFpower.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            power = float(row[0])
            time = float(row[1])
            twtwopower.append(power)
            twtwotime.append(time)
    twtwoavg = sum(twtwopower)/len(twtwopower)
    
    with open('100ohmpower.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            power = float(row[0])
            time = float(row[1])
            onehunpower.append(power)
            onehuntime.append(time)
    onehunavg = sum(onehunpower)/len(onehunpower)

    avgs = [tenavg, twtwoavg, onehunavg]
    maxdata = [max(tenpower), max(twtwopower), max(onehunpower)]
    mindata = [min(tenpower), min(twtwopower), min(onehunpower)]
    x = np.arange(3)
    stds = [np.std(tenpower), np.std(twtwopower), np.std(onehunpower)]
    plt.xticks(x, ('10nF Capacitor','22nF Capacitor','100'+r'$\Omega$' + ' Resistor'))
    plt.ylabel('Power Consumption (in W)')
    plt.xlabel('Component Used')
    plt.title('Power Measurement Comparison with Standard Deviation Error Bars')
    means = plt.bar(x, avgs, yerr=stds, capsize=10, zorder=0)
    mins = plt.scatter(x, mindata, color='red', zorder=5)
    maxs = plt.scatter(x, maxdata, color='green', zorder=10)

    plt.legend([means, maxs, mins],['Mean Value','Maximum Value','Minimum Value'])
    plt.show
    plt.savefig('method comparison bar chart')
    #error bars based on minima maxima
    #avg out power comp (per time?)


def histcomparison():
    plt.close('all')
    tenpower = []
    tentime = []
    twtwopower = []
    twtwotime = []
    onehunpower = []
    onehuntime = []
    with open('10nFpower.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            power = float(row[0])
            time = float(row[1])
            tenpower.append(power)
            tentime.append(time)

    with open('22nFpower.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            power = float(row[0])
            time = float(row[1])
            twtwopower.append(power)
            twtwotime.append(time)
  
    with open('100ohmpower.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            power = float(row[0])
            time = float(row[1])
            onehunpower.append(power)
            onehuntime.append(time)

    fig, axs = plt.subplots(3, 1, sharex=True)
    axs[0].hist(tenpower, bins=15)
    axs[0].set_ylabel('Frequency \n (10nF Capacitor)')
    axs[1].hist(twtwopower, bins=10)
    axs[1].set_ylabel('Frequency \n (22nF Capacitor)')
    axs[2].hist(onehunpower, bins=20)
    axs[2].set_ylabel('Frequency \n (100'+r'$\Omega$' + ' Resistor)')
    axs[2].set_xlabel('Power Consumption per Cycle (in Watts)')
    plt.savefig('method comparison histogram')


def timeprog():
    plt.close('all')
    tenpower = []
    tentime = []
    twtwopower = []
    twtwotime = []
    onehunpower = []
    onehuntime = []
    with open('10nFpower.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            power = float(row[0])
            time = float(row[1])
            tenpower.append(power)
            tentime.append(time)
    with open('22nFpower.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            power = float(row[0])
            time = float(row[1])
            twtwopower.append(power)
            twtwotime.append(time)  
    with open('100ohmpower.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            power = float(row[0])
            time = float(row[1])
            onehunpower.append(power)
            onehuntime.append(time)            
    x1 = np.arange(len(tenpower))
    x2 = np.arange(len(twtwopower))
    x3 = np.arange(len(onehunpower))
    fig, axs = plt.subplots(3, 1, sharex=True)
    axs[0].scatter(x1, tenpower, marker='.')
    axs[0].set_ylabel('Power Consumption \n (10nF Capacitor)')
    axs[1].scatter(x2, twtwopower, marker='.')
    axs[1].set_ylabel('Power Consumption \n (22nF Capacitor)')
    axs[2].scatter(x3, onehunpower, marker='.')
    axs[2].set_ylabel('Power Consumption \n (100'+r'$\Omega$' + ' Resistor)')
    axs[2].set_xlabel('Cycle Number')
    plt.savefig('Cycle Power Progression')
    
    
def ivgraph(input):
    plt.close('all')
    rawdata = np.loadtxt(fname = input,delimiter=",")   # Store data in Numpy Array
    data = rawdata.T                                    # Transpose array to seperate data sets
    dims = data.shape									# Get length of data and therefore time taken
    time = dims[1]
    timeary = np.linspace(1, time, time) 				# Ensure time data is continuous    
    data[0] = timeary
    data[2] = data[2]*0.001 # convert current to A instead of mA
 #   plt.plot(data[0],data[2])
    plt.plot(data[0],data[2],c='r')
    plt.xlabel('Time (in '+r'$\mu$'+'s)')
    plt.ylabel('Voltage')
    plt.title('100 ohm resistor I-t')
    
    
def anomtest():
    plt.close('all')
    data = fixdata('100res.txt')
    onehunpower = []
    onehuntime = []
    with open('100ohmpower.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            power = float(row[0])
            time = float(row[1])
            onehunpower.append(power)
            onehuntime.append(time)
#    plt.plot(data[0],data[2])
#    plt.plot(data[0],data[5],c='g')
    combineddata = data[5]*data[2]
    plt.plot(data[0],combineddata,c='b')
    count = 0
    for t,p in zip(onehuntime, onehunpower):
        count = count + t
        color = 'k'
        if p > 0.14:
            color = 'r'
        plt.axvline(count, -15, 15, c=color,linewidth=1)
    plt.xlabel('Instantaneous Power')
    plt.ylabel('Time (in '+r'$\mu$'+'s)')
    
    