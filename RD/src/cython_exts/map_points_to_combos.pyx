
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long[:,::1] c_mapper2(long[::1] realPoints, long[:,:] mockCombos,long[:,::1] realCombos):
    # realCombos = c_map_combos(realPoints, mockCombos)
    # realCombos = [ [ p1, p2, p3, p4, etc..], etc... ]  --> realCombos = [:,::1]
    # realPoints = [ p1, p2, p3, p4, etc.. ]             --> realPoints = [::1]
    # mockCombos = [ [ 0, 100, 1, 101, etc..], etc..]    --> mockCombos = [:,::1]
    cdef long r = mockCombos.shape[0]
    cdef long pts = mockCombos.shape[1]
    cdef long i,j,mpt
    cdef long pointNumber = realPoints.shape[0]

    cdef long pt0
    cdef long pt100 = realPoints[1]
    cdef long pt1 = realPoints[2]
    cdef long pt101 = realPoints[3]

    pt0 = realPoints[0]
    for j in range(pts):
        for i in range(r):
            mpt = mockCombos[i][j]
            if mpt == 0:
                realCombos[i][j] = pt0
            if mpt == 100:
                realCombos[i][j] = pt100
            if mpt == 1:
                realCombos[i][j] = pt1
            if mpt == 101:
                realCombos[i][j] = pt101
    return realCombos

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long[:,::1] c_mapper3(long[::1] realPoints, long[:,:] mockCombos,long[:,::1] realCombos):
    # realCombos = c_map_combos(realPoints, mockCombos)
    # realCombos[0] = [ [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..], etc... ] --> realCombos = [:,:,::1]
    # realPoints[0] = [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..] --> realPoints = [:,::1]
    # mockCombos[0] = [ [ 0, 100, 1, 101, etc..], etc..] --> mockCombos = [:,::1]
    cdef long r = mockCombos.shape[0]                                           # number of rows
    cdef long pts = mockCombos.shape[1]                                         # number of pts
    cdef long i,j,mpt
    # cdef long pointNumber = realPoints.shape[0]

    cdef long pt0 =  realPoints[0]
    cdef long pt100 =  realPoints[1]
    cdef long pt1 =  realPoints[2]
    cdef long pt101 =  realPoints[3]
    cdef long pt2 =  realPoints[4]
    cdef long pt102 =  realPoints[5]

    for j in range(pts):
        for i in range(r):
            mpt = mockCombos[i][j]
            if mpt == 0: realCombos[i][j] = pt0
            if mpt == 100: realCombos[i][j] = pt100
            if mpt == 1: realCombos[i][j] = pt1
            if mpt == 101: realCombos[i][j] = pt101
            if mpt == 2: realCombos[i][j] = pt2
            if mpt == 102: realCombos[i][j] = pt102
    return realCombos

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long [:,::1] c_mapper4(long[::1] realPoints, long[:,:] mockCombos,long[:,::1] realCombos):
    # realCombos = c_map_combos(realPoints, mockCombos)
    # realCombos[0] = [ [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..], etc... ] --> realCombos = [:,:,::1]
    # realPoints[0] = [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..] --> realPoints = [:,::1]
    # mockCombos[0] = [ [ 0, 100, 1, 101, etc..], etc..] --> mockCombos = [:,::1]
    cdef long r = mockCombos.shape[0]                                           # number of rows
    cdef long pts = mockCombos.shape[1]                                         # number of pts
    cdef long i,j,mpt

    cdef long pt0 =  realPoints[0]
    cdef long pt100 =  realPoints[1]
    cdef long pt1 =  realPoints[2]
    cdef long pt101 =  realPoints[3]
    cdef long pt2 =  realPoints[4]
    cdef long pt102 =  realPoints[5]
    cdef long pt3 =  realPoints[6]
    cdef long pt103 =  realPoints[7]

    for j in range(pts):
        for i in range(r):
            mpt = mockCombos[i][j]
            if mpt == 0: realCombos[i][j] = pt0
            if mpt == 100: realCombos[i][j] = pt100
            if mpt == 1: realCombos[i][j] = pt1
            if mpt == 101: realCombos[i][j] = pt101
            if mpt == 2: realCombos[i][j] = pt2
            if mpt == 102: realCombos[i][j] = pt102
            if mpt == 3: realCombos[i][j] = pt3
            if mpt == 103: realCombos[i][j] = pt103
    return realCombos

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long [:,::1] c_mapper5(long[::1] realPoints, long[:,:] mockCombos,long[:,::1] realCombos):
    # realCombos = c_map_combos(realPoints, mockCombos)
    # realCombos[0] = [ [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..], etc... ] --> realCombos = [:,:,::1]
    # realPoints[0] = [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..] --> realPoints = [:,::1]
    # mockCombos[0] = [ [ 0, 100, 1, 101, etc..], etc..] --> mockCombos = [:,::1]
    cdef long r = mockCombos.shape[0]                                           # number of rows
    cdef long pts = mockCombos.shape[1]                                         # number of pts
    cdef long i,j,mpt

    cdef long pt0 =  realPoints[0]
    cdef long pt100 =  realPoints[1]
    cdef long pt1 =  realPoints[2]
    cdef long pt101 =  realPoints[3]
    cdef long pt2 =  realPoints[4]
    cdef long pt102 =  realPoints[5]
    cdef long pt3 =  realPoints[6]
    cdef long pt103 =  realPoints[7]
    cdef long pt4 =  realPoints[8]
    cdef long pt104 =  realPoints[9]
    for j in range(pts):
        for i in range(r):
            mpt = mockCombos[i][j]
            if mpt == 0: realCombos[i][j] = pt0
            if mpt == 100: realCombos[i][j] = pt100
            if mpt == 1: realCombos[i][j] = pt1
            if mpt == 101: realCombos[i][j] = pt101
            if mpt == 2: realCombos[i][j] = pt2
            if mpt == 102: realCombos[i][j] = pt102
            if mpt == 3: realCombos[i][j] = pt3
            if mpt == 103: realCombos[i][j] = pt103
            if mpt == 4: realCombos[i][j] = pt4
            if mpt == 104: realCombos[i][j] = pt104
    return realCombos

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long [:,::1] c_mapper6(long[::1] realPoints, long[:,:] mockCombos,long[:,::1] realCombos):
    # realCombos = c_map_combos(realPoints, mockCombos)
    # realCombos[0] = [ [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..], etc... ] --> realCombos = [:,:,::1]
    # realPoints[0] = [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..] --> realPoints = [:,::1]
    # mockCombos[0] = [ [ 0, 100, 1, 101, etc..], etc..] --> mockCombos = [:,::1]
    cdef long r = mockCombos.shape[0]                                           # number of rows
    cdef long pts = mockCombos.shape[1]                                         # number of pts
    cdef long i,j,mpt

    cdef long pt0 =  realPoints[0]
    cdef long pt100 =  realPoints[1]
    cdef long pt1 =  realPoints[2]
    cdef long pt101 =  realPoints[3]
    cdef long pt2 =  realPoints[4]
    cdef long pt102 =  realPoints[5]
    cdef long pt3 =  realPoints[6]
    cdef long pt103 =  realPoints[7]
    cdef long pt4 =  realPoints[8]
    cdef long pt104 =  realPoints[9]
    cdef long pt5 =  realPoints[10]
    cdef long pt105 =  realPoints[11]

    for j in range(pts):
        for i in range(r):
            mpt = mockCombos[i][j]
            if mpt == 0: realCombos[i][j] = pt0
            if mpt == 100: realCombos[i][j] = pt100
            if mpt == 1: realCombos[i][j] = pt1
            if mpt == 101: realCombos[i][j] = pt101
            if mpt == 2: realCombos[i][j] = pt2
            if mpt == 102: realCombos[i][j] = pt102
            if mpt == 3: realCombos[i][j] = pt3
            if mpt == 103: realCombos[i][j] = pt103
            if mpt == 4: realCombos[i][j] = pt4
            if mpt == 104: realCombos[i][j] = pt104
            if mpt == 5: realCombos[i][j] = pt5
            if mpt == 105: realCombos[i][j] = pt105
    return realCombos

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long [:,::1] c_mapper7(long[::1] realPoints, long[:,:] mockCombos,long[:,::1] realCombos):
    # realCombos = c_map_combos(realPoints, mockCombos)
    # realCombos[0] = [ [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..], etc... ] --> realCombos = [:,:,::1]
    # realPoints[0] = [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..] --> realPoints = [:,::1]
    # mockCombos[0] = [ [ 0, 100, 1, 101, etc..], etc..] --> mockCombos = [:,::1]
    cdef long r = mockCombos.shape[0]                                           # number of rows
    cdef long pts = mockCombos.shape[1]                                         # number of pts
    cdef long i,j,mpt

    cdef long pt0 =  realPoints[0]
    cdef long pt100 =  realPoints[1]
    cdef long pt1 =  realPoints[2]
    cdef long pt101 =  realPoints[3]
    cdef long pt2 =  realPoints[4]
    cdef long pt102 =  realPoints[5]
    cdef long pt3 =  realPoints[6]
    cdef long pt103 =  realPoints[7]
    cdef long pt4 =  realPoints[8]
    cdef long pt104 =  realPoints[9]
    cdef long pt5 =  realPoints[10]
    cdef long pt105 =  realPoints[11]
    cdef long pt6 =  realPoints[12]
    cdef long pt106 =  realPoints[13]
    for j in range(pts):
        for i in range(r):
            mpt = mockCombos[i][j]
            if mpt == 0: realCombos[i][j] = pt0
            if mpt == 100: realCombos[i][j] = pt100
            if mpt == 1: realCombos[i][j] = pt1
            if mpt == 101: realCombos[i][j] = pt101
            if mpt == 2: realCombos[i][j] = pt2
            if mpt == 102: realCombos[i][j] = pt102
            if mpt == 3: realCombos[i][j] = pt3
            if mpt == 103: realCombos[i][j] = pt103
            if mpt == 4: realCombos[i][j] = pt4
            if mpt == 104: realCombos[i][j] = pt104
            if mpt == 5: realCombos[i][j] = pt5
            if mpt == 105: realCombos[i][j] = pt105
            if mpt == 6: realCombos[i][j] = pt6
            if mpt == 106: realCombos[i][j] = pt106
    return realCombos

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long [:,::1] c_mapper8(long[::1] realPoints, long[:,:] mockCombos,long[:,::1] realCombos):
    # realCombos = c_map_combos(realPoints, mockCombos)
    # realCombos[0] = [ [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..], etc... ] --> realCombos = [:,:,::1]
    # realPoints[0] = [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..] --> realPoints = [:,::1]
    # mockCombos[0] = [ [ 0, 100, 1, 101, etc..], etc..] --> mockCombos = [:,::1]
    cdef long r = mockCombos.shape[0]                                           # number of rows
    cdef long pts = mockCombos.shape[1]                                         # number of pts
    cdef long i,j,mpt

    cdef long pt0 =  realPoints[0]
    cdef long pt100 =  realPoints[1]
    cdef long pt1 =  realPoints[2]
    cdef long pt101 =  realPoints[3]
    cdef long pt2 =  realPoints[4]
    cdef long pt102 =  realPoints[5]
    cdef long pt3 =  realPoints[6]
    cdef long pt103 =  realPoints[7]
    cdef long pt4 =  realPoints[8]
    cdef long pt104 =  realPoints[9]
    cdef long pt5 =  realPoints[10]
    cdef long pt105 =  realPoints[11]
    cdef long pt6 =  realPoints[12]
    cdef long pt106 =  realPoints[13]
    cdef long pt7 =  realPoints[14]
    cdef long pt107 =  realPoints[15]
    for j in range(pts):
        for i in range(r):
            mpt = mockCombos[i][j]
            if mpt == 0: realCombos[i][j] = pt0
            if mpt == 100: realCombos[i][j] = pt100
            if mpt == 1: realCombos[i][j] = pt1
            if mpt == 101: realCombos[i][j] = pt101
            if mpt == 2: realCombos[i][j] = pt2
            if mpt == 102: realCombos[i][j] = pt102
            if mpt == 3: realCombos[i][j] = pt3
            if mpt == 103: realCombos[i][j] = pt103
            if mpt == 4: realCombos[i][j] = pt4
            if mpt == 104: realCombos[i][j] = pt104
            if mpt == 5: realCombos[i][j] = pt5
            if mpt == 105: realCombos[i][j] = pt105
            if mpt == 6: realCombos[i][j] = pt6
            if mpt == 106: realCombos[i][j] = pt106
            if mpt == 7: realCombos[i][j] = pt7
            if mpt == 107: realCombos[i][j] = pt107
    return realCombos
