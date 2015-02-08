from bisect_left import *
from numpy import *
from arrayFout import *


a = range(0, 100)
end = len(a)
b = []

for i in range(0, end):
    # print i
    leftvalue = i
    leftindex = bisect_left(a, leftvalue)
    
    b.append(leftindex)
    print leftindex
    print 'end = ', i
# test = array([a,b])
# arrayFout(test,'testbisectRange.txt')
