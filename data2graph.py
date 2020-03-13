# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 12:48:01 2020

@author: Jake Ford
"""
import numpy as np
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileMerger
import csv


def fixdata(input):
    rawdata = np.loadtxt(fname = input,delimiter=",")   # Store data in Numpy Array
    data = rawdata.T                                    # Transpose array to seperate data sets
    dims = data.shape									# Get length of data and therefore time taken
    time = dims[1]
    timeary = np.linspace(1, time, time) 				# Ensure time data is continuous
    data[0] = timeary
    return(data)


def cyclecalc(input):
    data = fixdata(input)
    prevsign = data[5,0] / abs(data[5,0]) # Returns -1 or 1
    count = 0
    timelst = []
    for t in data[5]:
        sign = t / abs(t)
        if (sign != prevsign):
            x = data[0,count]
            timelst.append(x)
        prevsign = sign
        count = count + 1
    timedif = []
    for x, t in enumerate(timelst):
        if x+1 < len(timelst):
            timedif.append(timelst[(x+1)] - timelst[(x)])
    crctd = [i for i in timedif if i > 5]
    return sum(crctd)/len(crctd)

def capsinglecycle(input,capval):
    data = fixdata(input)
    data[5] = data[5]*0.000000001*capval
    # Split data into "cycle" groups - around inversion points. if sign change 2x cut section ignore double changes?
#    'cycles = np.array  # begin empty? np array of split sections listed, plus length of cycle
    starttime = 0
    endtime = 0
    timedif = 0
    count = 0
    twicecount = 0
    prevsign = data[5,0] / abs(data[5,0])
    timelst = []
    for val in data[5, 0:100000]:
        sign = val / abs(val)
        if (sign != prevsign):
            twicecount = twicecount + 1
            if (twicecount == 1):
                midtime = int(data[0, count])
            if (twicecount == 2):
                endtime = int(data[0, count])
                timedif = endtime - starttime
                timelst.append([starttime, midtime, endtime, timedif])
                starttime = endtime
                twicecount = 0        
        prevsign = sign
        count = count + 1
    areas = []
    for cycle in timelst:
        area = np.trapz(data[5, cycle[0]:cycle[2]], data[1, cycle[0]:cycle[2]])
        areas.append([area/(cycle[3]*0.000001), cycle[3]])
    name = str(capval)+"nFcycletimes.csv"
    with open(name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(timelst)
    plt.scatter(*zip(*areas), s = 5)
    plt.ylabel("Cycle time in microseconds")
    plt.xlabel("Power Consumption")
    plt.title("Cycle length vs Power Consumption, "+str(capval)+"nF (First 100000 microseconds)")
    plt.show
#        'cycles = np.arrayfromifloop        
#    'cycleareas = np.array # begin empty? np array of areas of sections, plus length of cycle
#    for cyclevals in cycles:
#        area = np.trapz[data[5, 'cycles(startval:endval)], data[1, 'cycles(startval:endval)]) /'time]
#        cycleareas.append(area, 'cycles(time))
#    return cycleareas

def capgraph(input,capval,limit):
    data = fixdata(input)
    data[5] = (data[5]*0.000000001*capval) # turns V into V*C = Q
    plt.plot(data[1, 0:limit],data[5, 0:limit],linewidth=0.5)
    plt.title("Lissajous Curve, "+str(capval)+"nF, "+str(limit)+" Samples")
    area = np.trapz(data[5, 0:limit], data[1, 0:limit]) / ( limit / cyclecalc(input) ) # NEEDED?
    powercom = area / ( cyclecalc(input) * 0.000001 )   # Divide by cycle time (calculated in microseconds)
    plt.figtext(0.5, 0,"Power Consumption: "+str(powercom), wrap=True, horizontalalignment='center', fontsize=8)
    plt.xlabel("Voltage (in V)")
    plt.ylabel("Charge (in C)")
    plt.show()
    plt.savefig(str(capval)+"nF "+str(limit)+" Samples.pdf")


def ressinglecycle(input):
    rawdata = np.loadtxt(fname = input,delimiter=",")   # Store data in Numpy Array
    data = rawdata.T                                    # Transpose array to seperate data sets
    dims = data.shape									# Get length of data and therefore time taken
    time = dims[1]
    timeary = np.linspace(1, time, time) 				# Ensure time data is continuous    
    data[0] = timeary
    data[2] = data[2]*0.001
    combineddata = data[1]*data[2]
    starttime = 0
    endtime = 0
    timedif = 0
    count = 0
    twicecount = 0
    prevsign = combineddata[0] / abs(combineddata[0])
    timelst = [] # start time, mid time, end time
    for val in combineddata:
        sign = val / abs(val)
        if (sign != prevsign):
            twicecount = twicecount + 1
            if (twicecount == 1):
                midtime = int(data[0, count])
            if (twicecount == 2):
                endtime = int(data[0, count])
                timedif = endtime - starttime
                timelst.append([starttime, midtime, endtime, timedif])
                starttime = endtime
                twicecount = 0        
        prevsign = sign
        count = count + 1
    powers = []
    for cycle in timelst:
        powerin = np.trapz(data[0, cycle[0]:cycle[1]], combineddata[cycle[0]:cycle[1]])
        powerout = np.trapz(data[0, cycle[1]:cycle[2]], combineddata[cycle[1]:cycle[2]])
        power = powerin - powerout
        powers.append([power/(cycle[3]*0.000001), cycle[3]])
    plt.scatter(*zip(*powers), s = 5)
    plt.ylabel("Cycle time in microseconds")
    plt.xlabel("Power Consumption")
    plt.title("Cycle length vs Power Consumption, 100ohms")
    plt.show

def resgraph(input, limit):
    rawdata = np.loadtxt(fname = input,delimiter=",")   # Store data in Numpy Array
    data = rawdata.T                                    # Transpose array to seperate data sets
    dims = data.shape									# Get length of data and therefore time taken
    time = dims[1]
    timeary = np.linspace(1, time, time) 				# Ensure time data is continuous
    data[0] = timeary
    data[2] = data[2]*0.001
    combineddata = data[1, 0:limit]*data[2, 0:limit]
    plt.plot(data[0, 0:limit], combineddata[0:limit], linewidth=0.5)
    timedata = data[0]*0.001    # convert ms to s for integration
    area = np.trapz(combineddata[0:limit], timedata[0:limit]) / (limit/cyclecalc(input))
    powercom = area / ( cyclecalc(input) * 0.000001 )   # Divide by cycle time (calculated in microseconds)
    plt.figtext(0.5, 0,"Power Consumption: "+str(powercom), wrap=True, horizontalalignment='center', fontsize=8)
    plt.xlabel("Time (in mS)")
    plt.ylabel("Power (in W)")
    plt.show()
    plt.savefig("100ohm "+str(limit)+" Samples.pdf")

    
def script():
    twtwcap = [1000, 10000, 100000, 150000, 178760]
    tencap = [1000, 10000, 100000, 150000, 171000]
    res = [1000,10000,96876]
    for x in twtwcap:
        capgraph("22ncap.txt", 22, x)
        plt.close('all')
    for x in tencap:
        capgraph("10ncap.txt", 10, x)
        plt.close('all')
    for x in res:
        resgraph("100res.txt", x)
        plt.close('all')
    twtwpdfs = ["22nF 1000 Samples.pdf", "22nF 10000 Samples.pdf", "22nF 100000 Samples.pdf", "22nF 150000 Samples.pdf", "22nF 178760 Samples.pdf"]
    tenpdfs = ["10nF 1000 Samples.pdf", "10nF 10000 Samples.pdf", "10nF 100000 Samples.pdf", "10nF 150000 Samples.pdf", "10nF 171000 Samples.pdf"]
    respdfs = ["100ohm 1000 Samples.pdf", "100ohm 10000 Samples.pdf", "100ohm 96876 Samples.pdf"]
    merger = PdfFileMerger()
    for pdf in twtwpdfs:
        merger.append(pdf)
    merger.write("22nF Capacitor Results.pdf")
    merger.close()
    merger = PdfFileMerger()
    for pdf in tenpdfs:
        merger.append(pdf)
    merger.write("10nF Capacitor Results.pdf")
    merger.close()
    merger = PdfFileMerger()
    for pdf in respdfs:
        merger.append(pdf)
    merger.write("100ohm Resistor Results.pdf")
    merger.close()