def sortListArray(listArray, columnIndex):
    for i in range(0, len(listArray)):
        if i == len(listArray) - 1:
            break
        if len(listArray[i]) != len(listArray[i + 1]):
            print 'error - must array must have lists of same length'
            print asda
            
    a = listArray[columnIndex]
    b = range(0, len(a))
    c = zip(a, b)
    c.sort()
    d = [x[1] for x in c]
    f = range(0, len(d))
    c = zip(d, f)
    c.sort()
    key = [x[1] for x in c]
    newListArray = []
    for col in listArray:
        c = zip(key, col)
        c.sort()
        newListArray.append([x[1] for x in c])
    return newListArray

def test2():
    a = ['q', 'w', 'e', 't']
    b = [6, 8, 4, 3]
    c = ['a', 's', 'd', 'f']
    d = [a, b, c, c]
    print 'original= ', d
    test = sortListArray(d, 0)
    print 'sorted by 0=   ', test
    print ''
    print 'original= ', d
    test = sortListArray(d, 1)
    print 'sorted by 1=   ', test
    print ''
    g = [a, b, c, d]
    print 'original= ', test
    test = sortListArray(test, 2)
    print 'sorted by 2=   ', test
    print ''


def test1():
    a = ['q', 'w', 'e', 't']
    b = [6, 8, 4, 3]
    d = [b, a, a]
    print 'original=            ', d
    test = sortListArray(d, 0)
    print 'sorted by index 0=   ', test
    print ''
    d = [b, a, a]
    print 'original=            ', d
    test = sortListArray(d, 1)
    print 'sorted by index 1=   ', test
    print ''

# #print "in this case, sorting lists of letters by numeric order"
# #print ''
# #test1()
# #test2()
