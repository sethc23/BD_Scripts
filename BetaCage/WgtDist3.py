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



Sample = array([PartNum, Energy, Deposition, Depth])
SampleL = len(Depth)
TotalEnergy = sum(Energy)
arg = argsort(Sample[0][:])
SamplePSort = take(Sample, arg, 1)
# arg = argsort(Sample[1][:])
# SampleESort = take(Sample, arg,1)
arg = argsort(Sample[3][:])
SampleDSort = take(Sample, arg, 1)



TotalElectrons = int(max(PartNum))
PartNumRev = array(PartNum)
PartNumRev = PartNumRev.tolist()
PartNumRev.sort(reverse=True)
num = 1
EntrDose = array([])
EntrDose.resize([3, TotalElectrons])
MaxDose = array([])
MaxDose.resize([2, TotalElectrons])
print "Time@/100 electrons processed: "

for v in range(1, 1000):
    if v == 100 * num:
        num = num + 1
        print strftime("%H:%M:%S")
    startPart = PartNum.index(v)
    endPart = abs(SampleL - PartNumRev.index(v))
    cut = range(startPart, endPart)
    cutSample = take(SamplePSort, cut, 1)

    EntrD = cutSample[2][0]
    EntrDi2 = EntrD * 0.5
    MaxDose_P = max(cutSample[2][:])
    MaxDi2 = MaxDose_P * 0.5
    cutSample_L = cutSample[2][:]
    cutSample_L = cutSample_L.tolist()
    MaxDose_I = cutSample_L.index(MaxDose_P)

    EntrDose[0][v] = EntrD
    EntrDose[1][v] = EntrDi2
    EntrDose[2][v] = cutSample[3][0]

    MaxDose[0][v] = MaxDi2
    MaxDose[1][v] = cutSample[3][MaxDose_I]

arrayFout(EntrDose, 'EntrDose.txt')
arrayFout(MaxDose, 'MaxDose.txt')
    
# #arg = argsort(EntrDose[2][:])
# #EntrDSort = take(EntrDose, arg,1)
# #arg = argsort(MaxDose[1][:])
# #MaxDSort = take(MaxDose, arg,1)
# #
# #
# #
# #maxD = max(Depth)
# #minD = min(Depth)
# #histX = []
# #histY_MaxDose = []
# #histY_EntrDose = []
# #histY_EntrDose2 = []
# #nbins = 100
# #xW = (maxD-minD)/(nbins*maxD)
# #
# #startPt1 = 0
# #endPt1 = 0
# #startPt2 = 0
# #endPt2 = 0
# #for s in range(1,nbins+1):
# #    rightB = s*xW
# #    leftB = (s-1)*xW
# #    middlePt = (rightB-leftB)/(2)
# #    
# #    enddone2 = 0
# #    for w in range(startPt2,TotalElectrons):
# #        if (MaxDSort[1][w]>rightB) and (enddone2 == 0) :
# #            endPt2 = w-1
# #            enddone2 = 1
# #        if endPt2 == -1 and (enddone2 == 0):
# #            endPt2 = 1
# #        if s == nbins-1:
# #            endPt2 = TotalElectrons       
# #    #MaxPercentPts = (float(endPt2-startPt2)/float(TotalElectrons))*100.0
# #    SumMaxDose=take(MaxDSort[0],range(startPt2,endPt2))
# #    startPt2=endPt2
# #    BinMaxDoseL = len(SumMaxDose)
# #    BinMaxDoseS = sum(SumMaxDose)
# #    if BinMaxDoseL <=5:
# #        BinMaxDoseL=0
# #    if BinMaxDoseL == 0 or BinMaxDoseS == 0:
# #        BinMaxDose=0
# #    elif BinMaxDoseL != 0 and BinMaxDoseS != 0:
# #        BinMaxDose = float(BinMaxDoseS)/float(BinMaxDoseL)
# #    histY_MaxDose.append(BinMaxDose)
# #    
# #    enddone1 = 0
# #    for u in range(startPt1,TotalElectrons):
# #        if (EntrDSort[2][u]>rightB) and (enddone1 == 0) :
# #            endPt1 = u-1
# #            enddone1 = 1
# #        if endPt1 == -1 and (enddone1 == 0):
# #            endPt1 = 1
# #        if s == nbins-1:
# #            endPt1 = TotalElectrons     
# #    #EntrPercentPts = (float(endPt1-startPt1)/float(TotalElectrons))*100.0
# #    SumEntrDose=take(EntrDSort[0],range(startPt1,endPt1))
# #    SumEntrDose2=take(EntrDSort[1],range(startPt1,endPt1))
# #    startPt1=endPt1
# #    BinEntrDoseL = len(SumEntrDose)
# #    BinEntrDoseS = sum(SumEntrDose)
# #    BinEntrDoseL2 = len(SumEntrDose2)
# #    BinEntrDoseS2 = sum(SumEntrDose2)
# #    if BinEntrDoseL <=5:
# #        BinEntrDoseL=0
# #    if BinEntrDoseL == 0 or BinEntrDoseS == 0:
# #        BinEntrDose=0
# #    elif BinEntrDoseL != 0 and BinEntrDoseS != 0:
# #        BinEntrDose = float(BinEntrDoseS)/float(BinEntrDoseL)
# #    if BinEntrDoseL2 <=5:
# #        BinEntrDoseL2=0
# #    if BinEntrDoseL2 == 0 or BinEntrDoseS2 == 0:
# #        BinEntrDose2=0
# #    elif BinEntrDoseL2 != 0 and BinEntrDoseS2 != 0:
# #        BinEntrDose2 = float(BinEntrDoseS2)/float(BinEntrDoseL2)
# #
# #    histY_EntrDose.append(BinEntrDose)
# #    histY_EntrDose2.append(BinEntrDose2)
# #    histX.append(leftB)
# #
# #
# ##EntranceDose = [Entr, EntrDi2, Depth]
# ##MaxDose = [MaxDi2, Depth]
# ##a = array([histY_EntrDose])
# ##b = array([histY_MaxDose])
# ##d = array([histX])
# #
####print 'List or array',shape(EntrDose)
####print 'new array',shape(EntrDose)
# #
# #
# ##listFout(d,'histX.txt')

