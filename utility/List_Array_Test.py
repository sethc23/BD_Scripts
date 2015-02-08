from listFin import *
from listFout import *
from arrayFin import *
from arrayFout import *
from numpy import *

a = range(1, 11)
print 'start list = ', a
listFout(a, 'testList.txt')
TestList = listFin('testList.txt')
print 'return list = ', TestList

b = range(11, 21)
c = array([a, b, b, a])
print 'start shape = ', shape(c)
print 'start array = '
print c
arrayFout(c, 'testArray.txt')
TestArray = arrayFin('testArray.txt')
print 'return array = '
print TestArray
print 'return shape = ', shape(TestArray)
