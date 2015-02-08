from numpy import *
from arrayFout import *
from arrayFin import *
from listFout import *
from listFin import *

a = [0.5, 0.5, 0.5, 0.5, 0.5]
# b = [0.6,0.7,0.8,0.9,0.10]
# d = [0.6,0.7,0.8,0.9,0.10]

# c = array([a,b,d])
# d = array([c,c])
# e = array([d,d])
# #c = array([a,b,b,a]);
# #c = array([a,b,c,b,a])
# print "input data set:"
# print c
# print 'c shape = ',shape(c)
# print 'c len = ',len(shape(c))
# #print 'd = ',len(shape(d))
# #print 'd[0] = ',len(shape(d[0]))
# #print 'e = ',len(shape(e))
# #print 'e[0] = ',len(shape(e[0]))
# arrayFout(c,'testArray.txt')
print a
listFout(a, 'testArray.txt')
test = listFin('testArray.txt')
print test

