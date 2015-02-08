import numpy as np
import scipy as scipy
from time import strftime
from pylab import *
from numpy import *
from scipy import *
import matplotlib.mlab as mlab
from arrayFout import *
from listFout import *
from listFin import *

print "started calc at - "
print strftime("%a, %d %b %Y %H:%M:%S")

openfiles = ["MIN_Sim_000_0000.txt", "MIN_Sim_000_0001.txt",
             "MIN_Sim_000_0002.txt", "MIN_Sim_000_0003.txt",
             "MIN_Sim_000_0004.txt"]

numfile = len(openfiles)
PartNum = []
Energy = []
Deposition = []
Depth = []
for k in range(0, numfile):
    fin = open(openfiles[k], 'r')
    data = fin.readlines()
    end = len(data)
    for i in range(0, end):
        row = data[i]
        allcolumns = row.split()
        Electron = float(allcolumns[0])
        PartNum.append(Electron)
        E = float(allcolumns[1])
        Energy.append(E)
        Dep = float(allcolumns[2])
        Deposition.append(Dep)
        D = float(5000 - eval(allcolumns[3]))
        Depth.append(D)
    fin.close()



Sample = array([Deposition, Depth])
SampleL = len(Depth)
print 'sample size = ', SampleL
TotalEnergy = sum(Deposition)
print 'total energy = ', TotalEnergy
# arg = argsort(Sample[0][:])
# SamplePSort = take(Sample, arg,1)
# arg = argsort(Sample[1][:])
# SampleESort = take(Sample, arg,1)
arg = argsort(Sample[1][:])
SampleDSort = take(Sample, arg, 1)


for i in range(0, SampleL):
    if SampleDSort[1][i] > 0.004:
        mm4 = i - 1
        break

EnergySum4mm = sum(SampleDSort[0][0:mm4])
print EnergySum4mm

                   
