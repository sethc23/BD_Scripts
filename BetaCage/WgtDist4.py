import numpy as np
import scipy as scipy
from time import strftime
from pylab import *
from numpy import *
from scipy import *
import matplotlib.mlab as mlab
from listFout import *
from listFin import *
from arrayFin import *

EntrDose = arrayFin('EntrDose.txt')
MaxDose = arrayFin('MaxDose.txt')
histX = listFin('histX.txt')



# #histY_EntrDose = arrayFin('EntrDose.txt')
# #histY_EntrDose2 = arrayFin('EntrDose2.txt')
# histY_MaxDose = array([MaxDi2,Depth])



# print "Total Energy from data = ",TotalEnergy
# MaxEnergy = max(histY)
# topY=.80*MaxEnergy
# botY=.20*MaxEnergy

# #hist = array([histX,histY_MaxDose])
# #bins=len(hist[0])
# #SumEnergyHist = sum(hist[1])
# #print "histogram energy = ",SumEnergyHist

# SumPercentage = sum(SamplePts)
# print "histogram percentage sum = ",SumPercentage

# #a = array(SamplePts)
# #b = array(0.01)
# #b.repeat(len(SamplePts)-1,0)
# #height = max(histY)
# #c = array(height)
# #c.repeat(len(SamplePts)-1,0)
# #FractPercentY = array(a*b*c)
# #d = array(histX)
# #FractPercentX = array(d+(xW/4))

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
        
# bindiff = endbin-startbin
# print "bin diff = ",bindiff

# print "plotX = ",plotX
# print "plotY = ",plotY

# #poly4f = np.polyfit(plotX,plotY,4)
# #poly4v = np.polyval(poly4f,plotX)
# #poly3d = np.polyder(poly4f)
# #poly3v = np.polyval(poly3d,plotX)
# #poly2d = np.polyder(poly3d)
# #poly2v = np.polyval(poly2d,plotX)



# #
# #fig1 = plt.figure()
# #ax = fig1.add_subplot(111)
# ##title(['Sum of Bins = ',SumEnergyHist])
# #
# #xW = (max(histX)-min(histX))/len(histX)
# #
# #p1 = ax.bar(hist[0],hist[1],xW,color='b')
# ##p2 = ax.bar(FractPercentX,FractPercentY,xW/2,color='r')
# #
# #value = str(SumEnergyHist)
# #ax.set_xlabel('Depth(mm)')
# #ax.set_ylabel('Max Dose (MeV)')
# #ax.set_title('100 bins - 100,000 electrons of 5keV Energy \n Sum of Bins = '+value)
# #              
# ##ax.legend( (p1[0], p2[0]), ('Energy', 'Percent of Samples times Max Height') )
# #axis1 = ([min(hist[0]),max(hist[0]),min(hist[1]),max(hist[1])])
# #plt.axis(axis1)
# #ax.grid(True)
# #
# #
# #fig2 = plt.figure()
# #bx = fig2.add_subplot(111)





# #p3 = bx.plot(plotX,plotY,'k-')
# #p3a = bx.plot(plotX,plotY,'ko')
# #p4 = bx.plot(plotX,poly4v,'b-')
# #p5 = bx.plot(plotX,poly3v,'g-')
# #p6 = bx.plot(plotX,poly2v,'c-')

# #bx.set_xlabel('Depth(mm)')
# #bx.set_ylabel('Energy(keV)')
# #bx.set_title('Histogram of 5kev')
# #bx.legend( (p3[0], p4[0], p5[0], p6[0]),
# #           ('Plot of bins between 80-20%','4th-Polyfit to Plot',
# #            '1st Derivative of 4th-Polyfit','2nd Derivative of 4th-Polyfit') )
# #axis2 = ([min(plotX),max(plotX),min(plotY),max(plotY)])
# #plt.axis(axis2)
# #bx.grid(True)

# #plt.show()
