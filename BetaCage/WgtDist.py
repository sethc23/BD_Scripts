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

EntrDose = array([])
EntrDose.resize([3, TotalElectrons])
MaxDose = array([])
MaxDose.resize([2, TotalElectrons])
for v in range(1, TotalElectrons):
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
    
    


# #    if (SamplePSort[2][v] == startPart):
# #        lowD = SamplePSort[2]
# #        if (lowD<lowD_I):
# #            
# #            lowD_I = lowD
# #        if (maxD>maxD_1):
# #            
# #            
# #            
# #        endPt = u-1
# #        enddone = 1
# #    if endPt == -1 and (enddone == 0):
# #        endPart = 1
# #    if s == nbins-1:
# #        endPart = samplesize
# #
# #
# #EntranceDose = 
# #
# #MaxDi2
# #
# #EntrDi2



# #maxD = max(Depth)
# #minD = min(Depth)
# #samplesize=len(SampleDSort[0])
# #print "samplesize = ",samplesize
# #histX = []
# #histY = []
# #SamplePts = []
# #nbins = 100
# #xW = (maxD-minD)/(nbins*maxD)
# ##print "final depth = ",(xW*(nbins+1))
# #startPt = 0
# #endPt = 0
# #for s in range(1,nbins+1):
# #    rightB = s*xW
# #    leftB = (s-1)*xW
# #    middlePt = (rightB-leftB)/(2)
# #    enddone = 0
# #    for u in range(startPt,samplesize):
# #        if (SampleDSort[0][u]>rightB) and (enddone == 0) :
# #            endPt = u-1
# #            enddone = 1
# #        if endPt == -1 and (enddone == 0):
# #            endPt = 1
# #        if s == nbins-1:
# #            endPt = samplesize
# #            
# #    PercentPts = (float(endPt-startPt)/float(samplesize))*100.0
# #    SumEnergy=take(SampleDSort[1],range(startPt,endPt))
# #    startPt=endPt
# #    #BinEnergy=sum(SumEnergy)
# #    BinEnergyL = len(SumEnergy)
# #    BinEnergyS=sum(SumEnergy)
# #
# #    if BinEnergyL <=5:
# #        BinEnergy=0
# #        BinEnergyL=0
# #    if BinEnergyL == 0 or BinEnergyS == 0:
# #        BinEnergy=0
# #    elif BinEnergyL != 0 and BinEnergyS != 0:
# #        BinEnergy = float(BinEnergyS)/float(BinEnergyL)
# #    
# #    BinEnergyX = BinEnergy*(1/middlePt)
# #    #NormX = leftB/maxD
# #    SamplePts.append(PercentPts)
# #    #histY.append(BinEnergy)
# #    histY.append(BinEnergyX)
# #    histX.append(leftB)
# #
# #
# #
# #
# #print "Total Energy from data = ",TotalEnergy
# #MaxEnergy = max(histY)
# #topY=.80*MaxEnergy
# #botY=.20*MaxEnergy
# #hist = array([histX,histY])
# #bins=len(histY)
# #SumEnergyHist = sum(hist[1])
# #print "histogram energy = ",SumEnergyHist
# #SumPercentage = sum(SamplePts)
# #print "histogram percentage sum = ",SumPercentage
# #
# #a = array(SamplePts)
# #b = array(0.01)
# #b.repeat(len(SamplePts)-1,0)
# #height = max(histY)
# #c = array(height)
# #c.repeat(len(SamplePts)-1,0)
# #FractPercentY = array(a*b*c)
# #d = array(histX)
# #FractPercentX = array(d+(xW/4))
# #
# #plotX = []
# #plotY = []
# #startbin = histY.index(MaxEnergy)
# #endbin=0
# #for w in range(28,bins):
# #    #if (topY>=histY[w]>=botY):
# #    xval = histX[w]+(.5*xW)
# #    plotX.append(xval)
# #    yval = histY[w]
# #    plotY.append(yval)
# #    endbin = w
# #        
# #bindiff = endbin-startbin
# #print "bin diff = ",bindiff
# #
# ##print "plotX = ",plotX
# ##print "plotY = ",plotY
# #
# #poly4f = np.polyfit(plotX,plotY,4)
# #poly4v = np.polyval(poly4f,plotX)
# #poly3d = np.polyder(poly4f)
# #poly3v = np.polyval(poly3d,plotX)
# #poly2d = np.polyder(poly3d)
# #poly2v = np.polyval(poly2d,plotX)
# #
# #
# #fig1 = plt.figure()
# #ax = fig1.add_subplot(111)
# #title(['SampleSize = ',samplesize])
# #
# #p1 = ax.bar(histX,histY,xW,color='b')
# #p2 = ax.bar(FractPercentX,FractPercentY,xW/2,color='r')
# #
# #ax.set_xlabel('Depth(mm)')
# #ax.set_ylabel('Energy(keV)')
# #ax.set_title('Histogram of 5kev')
# #ax.legend( (p1[0], p2[0]), ('Energy', 'Percent of Samples times Max Height') )
# #axis1 = ([min(histX),max(histX),min(histY),max(histY)])
# #plt.axis(axis1)
# #ax.grid(True)
# #
# #
# #fig2 = plt.figure()
# #bx = fig2.add_subplot(111)
# #
# #p3 = bx.plot(plotX,plotY,'k-')
# #p3a = bx.plot(plotX,plotY,'ko')
# #p4 = bx.plot(plotX,poly4v,'b-')
# #p5 = bx.plot(plotX,poly3v,'g-')
# #p6 = bx.plot(plotX,poly2v,'c-')
# #
# #bx.set_xlabel('Depth(mm)')
# #bx.set_ylabel('Energy(keV)')
# #bx.set_title('Histogram of 5kev')
# #bx.legend( (p3[0], p4[0], p5[0], p6[0]),
# #           ('Plot of bins between 80-20%','4th-Polyfit to Plot',
# #            '1st Derivative of 4th-Polyfit','2nd Derivative of 4th-Polyfit') )
# #axis2 = ([min(plotX),max(plotX),min(plotY),max(plotY)])
# #plt.axis(axis2)
# #ax.grid(True)
# #
# #plt.show()
