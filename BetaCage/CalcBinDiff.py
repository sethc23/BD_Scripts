import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
from pylab import *
from numpy import *
from scipy import *
import matplotlib.mlab as mlab


openfiles = ["MIN_Sim_000_0000.txt", "MIN_Sim_000_0001.txt",
             "MIN_Sim_000_0002.txt", "MIN_Sim_000_0003.txt",
             "MIN_Sim_000_0004.txt"]
numfile = len(openfiles)
Depth = []
Energy = []
for k in range(0, numfile):
    fin = open(openfiles[k], 'r')
    data = fin.readlines()
    end = len(data)
    for i in range(0, end):
        row = data[i]
        allcolumns = row.split()
        E = float(allcolumns[0])
        Energy.append(E)
        D = float(5000 - eval(allcolumns[1]))
        Depth.append(D)
    fin.close()

a = array([Depth])
b = array([Energy])
Sample = array([Depth, Energy])
TotalEnergy = sum(Energy)
print TotalEnergy

arg = argsort(Sample[0][:])
SampleDSort = take(Sample, arg, 1)
# #
samplesize = len(SampleDSort[0])

minD = min(Depth)
maxD = max(Depth)
plotX = []
plotY = []

point = 0
for t in range(1, 6):
    histX = []
    histY = []
    nbins = 10 * t
    xW = (maxD - minD) / (nbins)
    
    startPt = 0
    endPt = 0
    for s in range(1, nbins + 1):
        rightB = s * xW
        leftB = (s - 1) * xW
        enddone = 0
        for u in range(startPt, samplesize):
            if (SampleDSort[0][u] > rightB) and (enddone == 0) :
                endPt = u - 1
                enddone = 1
            if endPt == -1 and (enddone == 0):
                endPt = 1
            if s == nbins - 1:
                endPt = samplesize

        SumEnergy = take(SampleDSort[1], range(startPt, endPt))
        startPt = endPt
        # BinEnergy=sum(SumEnergy)
        BinEnergyL = len(SumEnergy)
        BinEnergyS = sum(SumEnergy)
        BinEnergy = BinEnergyS / BinEnergyL
        if BinEnergyL == 0 or BinEnergyS == 0:
            BinEnergy = 0
          
        
        histY.append(BinEnergy)
        histX.append(nbins)

    MaxEnergy = max(histY)
    topY = .80 * MaxEnergy
    botY = .20 * MaxEnergy
    
    print "Total Energy from data = ", TotalEnergy
    SumEnergyHist = sum(histY)
    print "histogram energy = ", SumEnergyHist
    
    bins = len(histY)
    startbin = histY.index(MaxEnergy)
    endbin = 0
    for w in range(startbin, bins):
        if (topY >= histY[w] >= botY):
            endbin = w
            
    bindiff = endbin - startbin
    if endbin == 0:
        bindiff = 0
    plotX.append(nbins)
    plotY.append(bindiff)

binmax = max(plotY)
# print binmax
binmaxindex = plotY.index(binmax)
binNumber = plotX[binmaxindex]
# print binNumber

minX = min(plotX)
maxX = max(plotX)
minY = min(plotY)
maxY = max(plotY)
plt.plot(plotX, plotY)
plt.xlabel('Number of Total Bins')
plt.ylabel('Bins between 80-20%')
plt.title('Bin Difference b/t 80-20% vs. Total Bins Used in Distr.')
plt.axis([minX, maxX, minY, maxY])
plt.grid(True)
plt.show()
