
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long[:,:,::1] c_mapper2(long[:,::1] realPoints, long[:,:] mockCombos,long[:,:,::1] realCombos):
    # realCombos = c_map_combos(realPoints, mockCombos)
    # realCombos[0] = [ [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..], etc... ] --> realCombos = [:,:,::1]
    # realPoints[0] = [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..] --> realPoints = [:,::1]
    # mockCombos[0] = [ [ 0, 100, 1, 101, etc..], etc..] --> mockCombos = [:,::1]
    cdef long r = mockCombos.shape[0]                                           # number of rows
    cdef long pts = mockCombos.shape[1]                                         # number of pts
    cdef long i,j,mpt
    cdef long pointNumber = realPoints.shape[0]

    cdef long ptx0 =  realPoints[0][0]
    cdef long pty0 =  realPoints[0][1]
    cdef long ptx100 =  realPoints[1][0]
    cdef long pty100 =  realPoints[1][1]
    cdef long ptx1 =  realPoints[2][0]
    cdef long pty1 =  realPoints[2][1]
    cdef long ptx101 =  realPoints[3][0]
    cdef long pty101 =  realPoints[3][1]

    for j in range(pts):
        for i in range(r):
            mpt = mockCombos[i][j]
            if mpt == 0:
                realCombos[i][j][0] = ptx0
                realCombos[i][j][1] = pty0
            if mpt == 100:
                realCombos[i][j][0] = ptx100
                realCombos[i][j][1] = pty100
            if mpt == 1:
                realCombos[i][j][0] = ptx1
                realCombos[i][j][1] = pty1
            if mpt == 101:
                realCombos[i][j][0] = ptx101
                realCombos[i][j][1] = pty101
    return realCombos

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long[:,:,::1] c_mapper3(long[:,::1] realPoints, long[:,:] mockCombos,long[:,:,::1] realCombos):
    # realCombos = c_map_combos(realPoints, mockCombos)
    # realCombos[0] = [ [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..], etc... ] --> realCombos = [:,:,::1]
    # realPoints[0] = [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..] --> realPoints = [:,::1]
    # mockCombos[0] = [ [ 0, 100, 1, 101, etc..], etc..] --> mockCombos = [:,::1]
    cdef long r = mockCombos.shape[0]                                           # number of rows
    cdef long pts = mockCombos.shape[1]                                         # number of pts
    cdef long i,j,mpt
    cdef long pointNumber = realPoints.shape[0]

    cdef long ptx0 =  realPoints[0][0]
    cdef long pty0 =  realPoints[0][1]
    cdef long ptx100 =  realPoints[1][0]
    cdef long pty100 =  realPoints[1][1]
    cdef long ptx1 =  realPoints[2][0]
    cdef long pty1 =  realPoints[2][1]
    cdef long ptx101 =  realPoints[3][0]
    cdef long pty101 =  realPoints[3][1]
    cdef long ptx2 =  realPoints[4][0]
    cdef long pty2 =  realPoints[4][1]
    cdef long ptx102 =  realPoints[5][0]
    cdef long pty102 =  realPoints[5][1]

    for j in range(pts):
        for i in range(r):
            mpt = mockCombos[i][j]
            if mpt == 0:
                realCombos[i][j][0] = ptx0
                realCombos[i][j][1] = pty0
            if mpt == 100:
                realCombos[i][j][0] = ptx100
                realCombos[i][j][1] = pty100
            if mpt == 1:
                realCombos[i][j][0] = ptx1
                realCombos[i][j][1] = pty1
            if mpt == 101:
                realCombos[i][j][0] = ptx101
                realCombos[i][j][1] = pty101
            if mpt == 2:
                realCombos[i][j][0] = ptx2
                realCombos[i][j][1] = pty2
            if mpt == 102:
                realCombos[i][j][0] = ptx102
                realCombos[i][j][1] = pty102
    return realCombos

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long [:,:,::1] c_mapper4(long[:,::1] realPoints, long[:,:] mockCombos,long[:,:,::1] realCombos):
    # realCombos = c_map_combos(realPoints, mockCombos)
    # realCombos[0] = [ [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..], etc... ] --> realCombos = [:,:,::1]
    # realPoints[0] = [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..] --> realPoints = [:,::1]
    # mockCombos[0] = [ [ 0, 100, 1, 101, etc..], etc..] --> mockCombos = [:,::1]
    cdef long r = mockCombos.shape[0]                                           # number of rows
    cdef long pts = mockCombos.shape[1]                                         # number of pts
    cdef long i,j,mpt

    cdef long ptx0 =  realPoints[0][0]
    cdef long pty0 =  realPoints[0][1]
    cdef long ptx100 =  realPoints[1][0]
    cdef long pty100 =  realPoints[1][1]
    cdef long ptx1 =  realPoints[2][0]
    cdef long pty1 =  realPoints[2][1]
    cdef long ptx101 =  realPoints[3][0]
    cdef long pty101 =  realPoints[3][1]
    cdef long ptx2 =  realPoints[4][0]
    cdef long pty2 =  realPoints[4][1]
    cdef long ptx102 =  realPoints[5][0]
    cdef long pty102 =  realPoints[5][1]
    cdef long ptx3 =  realPoints[6][0]
    cdef long pty3 =  realPoints[6][1]
    cdef long ptx103 =  realPoints[7][0]
    cdef long pty103 =  realPoints[7][1]

    for j in range(pts):
        for i in range(r):
            mpt = mockCombos[i][j]
            if mpt == 0:
                realCombos[i][j][0] = ptx0
                realCombos[i][j][1] = pty0
            if mpt == 100:
                realCombos[i][j][0] = ptx100
                realCombos[i][j][1] = pty100
            if mpt == 1:
                realCombos[i][j][0] = ptx1
                realCombos[i][j][1] = pty1
            if mpt == 101:
                realCombos[i][j][0] = ptx101
                realCombos[i][j][1] = pty101
            if mpt == 2:
                realCombos[i][j][0] = ptx2
                realCombos[i][j][1] = pty2
            if mpt == 102:
                realCombos[i][j][0] = ptx102
                realCombos[i][j][1] = pty102
            if mpt == 3:
                realCombos[i][j][0] = ptx3
                realCombos[i][j][1] = pty3
            if mpt == 103:
                realCombos[i][j][0] = ptx103
                realCombos[i][j][1] = pty103
    return realCombos

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long [:,:,::1] c_mapper5(long[:,::1] realPoints, long[:,:] mockCombos,long[:,:,::1] realCombos):
    # realCombos = c_map_combos(realPoints, mockCombos)
    # realCombos[0] = [ [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..], etc... ] --> realCombos = [:,:,::1]
    # realPoints[0] = [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..] --> realPoints = [:,::1]
    # mockCombos[0] = [ [ 0, 100, 1, 101, etc..], etc..] --> mockCombos = [:,::1]
    cdef long r = mockCombos.shape[0]                                           # number of rows
    cdef long pts = mockCombos.shape[1]                                         # number of pts
    cdef long i,j,mpt

    cdef long ptx0 =  realPoints[0][0]
    cdef long pty0 =  realPoints[0][1]
    cdef long ptx100 =  realPoints[1][0]
    cdef long pty100 =  realPoints[1][1]
    cdef long ptx1 =  realPoints[2][0]
    cdef long pty1 =  realPoints[2][1]
    cdef long ptx101 =  realPoints[3][0]
    cdef long pty101 =  realPoints[3][1]
    cdef long ptx2 =  realPoints[4][0]
    cdef long pty2 =  realPoints[4][1]
    cdef long ptx102 =  realPoints[5][0]
    cdef long pty102 =  realPoints[5][1]
    cdef long ptx3 =  realPoints[6][0]
    cdef long pty3 =  realPoints[6][1]
    cdef long ptx103 =  realPoints[7][0]
    cdef long pty103 =  realPoints[7][1]
    cdef long ptx4 =  realPoints[8][0]
    cdef long pty4 =  realPoints[8][1]
    cdef long ptx104 =  realPoints[9][0]
    cdef long pty104 =  realPoints[9][1]

    for j in range(pts):
        for i in range(r):
            mpt = mockCombos[i][j]
            if mpt == 0:
                realCombos[i][j][0] = ptx0
                realCombos[i][j][1] = pty0
            if mpt == 100:
                realCombos[i][j][0] = ptx100
                realCombos[i][j][1] = pty100
            if mpt == 1:
                realCombos[i][j][0] = ptx1
                realCombos[i][j][1] = pty1
            if mpt == 101:
                realCombos[i][j][0] = ptx101
                realCombos[i][j][1] = pty101
            if mpt == 2:
                realCombos[i][j][0] = ptx2
                realCombos[i][j][1] = pty2
            if mpt == 102:
                realCombos[i][j][0] = ptx102
                realCombos[i][j][1] = pty102
            if mpt == 3:
                realCombos[i][j][0] = ptx3
                realCombos[i][j][1] = pty3
            if mpt == 103:
                realCombos[i][j][0] = ptx103
                realCombos[i][j][1] = pty103
            if mpt == 4:
                realCombos[i][j][0] = ptx4
                realCombos[i][j][1] = pty4
            if mpt == 104:
                realCombos[i][j][0] = ptx104
                realCombos[i][j][1] = pty104
    return realCombos

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long [:,:,::1] c_mapper6(long[:,::1] realPoints, long[:,:] mockCombos,long[:,:,::1] realCombos):
    # realCombos = c_map_combos(realPoints, mockCombos)
    # realCombos[0] = [ [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..], etc... ] --> realCombos = [:,:,::1]
    # realPoints[0] = [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..] --> realPoints = [:,::1]
    # mockCombos[0] = [ [ 0, 100, 1, 101, etc..], etc..] --> mockCombos = [:,::1]
    cdef long r = mockCombos.shape[0]                                           # number of rows
    cdef long pts = mockCombos.shape[1]                                         # number of pts
    cdef long i,j,mpt

    cdef long ptx0 =  realPoints[0][0]
    cdef long pty0 =  realPoints[0][1]
    cdef long ptx100 =  realPoints[1][0]
    cdef long pty100 =  realPoints[1][1]
    cdef long ptx1 =  realPoints[2][0]
    cdef long pty1 =  realPoints[2][1]
    cdef long ptx101 =  realPoints[3][0]
    cdef long pty101 =  realPoints[3][1]
    cdef long ptx2 =  realPoints[4][0]
    cdef long pty2 =  realPoints[4][1]
    cdef long ptx102 =  realPoints[5][0]
    cdef long pty102 =  realPoints[5][1]
    cdef long ptx3 =  realPoints[6][0]
    cdef long pty3 =  realPoints[6][1]
    cdef long ptx103 =  realPoints[7][0]
    cdef long pty103 =  realPoints[7][1]
    cdef long ptx4 =  realPoints[8][0]
    cdef long pty4 =  realPoints[8][1]
    cdef long ptx104 =  realPoints[9][0]
    cdef long pty104 =  realPoints[9][1]
    cdef long ptx5 =  realPoints[10][0]
    cdef long pty5 =  realPoints[10][1]
    cdef long ptx105 =  realPoints[11][0]
    cdef long pty105 =  realPoints[11][1]

    for j in range(pts):
        for i in range(r):
            mpt = mockCombos[i][j]
            if mpt == 0:
                realCombos[i][j][0] = ptx0
                realCombos[i][j][1] = pty0
            if mpt == 100:
                realCombos[i][j][0] = ptx100
                realCombos[i][j][1] = pty100
            if mpt == 1:
                realCombos[i][j][0] = ptx1
                realCombos[i][j][1] = pty1
            if mpt == 101:
                realCombos[i][j][0] = ptx101
                realCombos[i][j][1] = pty101
            if mpt == 2:
                realCombos[i][j][0] = ptx2
                realCombos[i][j][1] = pty2
            if mpt == 102:
                realCombos[i][j][0] = ptx102
                realCombos[i][j][1] = pty102
            if mpt == 3:
                realCombos[i][j][0] = ptx3
                realCombos[i][j][1] = pty3
            if mpt == 103:
                realCombos[i][j][0] = ptx103
                realCombos[i][j][1] = pty103
            if mpt == 4:
                realCombos[i][j][0] = ptx4
                realCombos[i][j][1] = pty4
            if mpt == 104:
                realCombos[i][j][0] = ptx104
                realCombos[i][j][1] = pty104
            if mpt == 5:
                realCombos[i][j][0] = ptx5
                realCombos[i][j][1] = pty5
            if mpt == 105:
                realCombos[i][j][0] = ptx105
                realCombos[i][j][1] = pty105
    return realCombos

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long [:,:,::1] c_mapper7(long[:,::1] realPoints, long[:,:] mockCombos,long[:,:,::1] realCombos):
    # realCombos = c_map_combos(realPoints, mockCombos)
    # realCombos[0] = [ [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..], etc... ] --> realCombos = [:,:,::1]
    # realPoints[0] = [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..] --> realPoints = [:,::1]
    # mockCombos[0] = [ [ 0, 100, 1, 101, etc..], etc..] --> mockCombos = [:,::1]
    cdef long r = mockCombos.shape[0]                                           # number of rows
    cdef long pts = mockCombos.shape[1]                                         # number of pts
    cdef long i,j,mpt

    cdef long ptx0 =  realPoints[0][0]
    cdef long pty0 =  realPoints[0][1]
    cdef long ptx100 =  realPoints[1][0]
    cdef long pty100 =  realPoints[1][1]
    cdef long ptx1 =  realPoints[2][0]
    cdef long pty1 =  realPoints[2][1]
    cdef long ptx101 =  realPoints[3][0]
    cdef long pty101 =  realPoints[3][1]
    cdef long ptx2 =  realPoints[4][0]
    cdef long pty2 =  realPoints[4][1]
    cdef long ptx102 =  realPoints[5][0]
    cdef long pty102 =  realPoints[5][1]
    cdef long ptx3 =  realPoints[6][0]
    cdef long pty3 =  realPoints[6][1]
    cdef long ptx103 =  realPoints[7][0]
    cdef long pty103 =  realPoints[7][1]
    cdef long ptx4 =  realPoints[8][0]
    cdef long pty4 =  realPoints[8][1]
    cdef long ptx104 =  realPoints[9][0]
    cdef long pty104 =  realPoints[9][1]
    cdef long ptx5 =  realPoints[10][0]
    cdef long pty5 =  realPoints[10][1]
    cdef long ptx105 =  realPoints[11][0]
    cdef long pty105 =  realPoints[11][1]
    cdef long ptx6 =  realPoints[12][0]
    cdef long pty6 =  realPoints[12][1]
    cdef long ptx106 =  realPoints[13][0]
    cdef long pty106 =  realPoints[13][1]

    for j in range(pts):
        for i in range(r):
            mpt = mockCombos[i][j]
            if mpt == 0:
                realCombos[i][j][0] = ptx0
                realCombos[i][j][1] = pty0
            if mpt == 100:
                realCombos[i][j][0] = ptx100
                realCombos[i][j][1] = pty100
            if mpt == 1:
                realCombos[i][j][0] = ptx1
                realCombos[i][j][1] = pty1
            if mpt == 101:
                realCombos[i][j][0] = ptx101
                realCombos[i][j][1] = pty101
            if mpt == 2:
                realCombos[i][j][0] = ptx2
                realCombos[i][j][1] = pty2
            if mpt == 102:
                realCombos[i][j][0] = ptx102
                realCombos[i][j][1] = pty102
            if mpt == 3:
                realCombos[i][j][0] = ptx3
                realCombos[i][j][1] = pty3
            if mpt == 103:
                realCombos[i][j][0] = ptx103
                realCombos[i][j][1] = pty103
            if mpt == 4:
                realCombos[i][j][0] = ptx4
                realCombos[i][j][1] = pty4
            if mpt == 104:
                realCombos[i][j][0] = ptx104
                realCombos[i][j][1] = pty104
            if mpt == 5:
                realCombos[i][j][0] = ptx5
                realCombos[i][j][1] = pty5
            if mpt == 105:
                realCombos[i][j][0] = ptx105
                realCombos[i][j][1] = pty105
            if mpt == 6:
                realCombos[i][j][0] = ptx6
                realCombos[i][j][1] = pty6
            if mpt == 106:
                realCombos[i][j][0] = ptx106
                realCombos[i][j][1] = pty106
    return realCombos

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long [:,:,::1] c_mapper8(long[:,::1] realPoints, long[:,:] mockCombos,long[:,:,::1] realCombos):
    # realCombos = c_map_combos(realPoints, mockCombos)
    # realCombos[0] = [ [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..], etc... ] --> realCombos = [:,:,::1]
    # realPoints[0] = [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], etc..] --> realPoints = [:,::1]
    # mockCombos[0] = [ [ 0, 100, 1, 101, etc..], etc..] --> mockCombos = [:,::1]
    cdef long r = mockCombos.shape[0]                                           # number of rows
    cdef long pts = mockCombos.shape[1]                                         # number of pts
    cdef long i,j,mpt

    cdef long ptx0 =  realPoints[0][0]
    cdef long pty0 =  realPoints[0][1]
    cdef long ptx100 =  realPoints[1][0]
    cdef long pty100 =  realPoints[1][1]
    cdef long ptx1 =  realPoints[2][0]
    cdef long pty1 =  realPoints[2][1]
    cdef long ptx101 =  realPoints[3][0]
    cdef long pty101 =  realPoints[3][1]
    cdef long ptx2 =  realPoints[4][0]
    cdef long pty2 =  realPoints[4][1]
    cdef long ptx102 =  realPoints[5][0]
    cdef long pty102 =  realPoints[5][1]
    cdef long ptx3 =  realPoints[6][0]
    cdef long pty3 =  realPoints[6][1]
    cdef long ptx103 =  realPoints[7][0]
    cdef long pty103 =  realPoints[7][1]
    cdef long ptx4 =  realPoints[8][0]
    cdef long pty4 =  realPoints[8][1]
    cdef long ptx104 =  realPoints[9][0]
    cdef long pty104 =  realPoints[9][1]
    cdef long ptx5 =  realPoints[10][0]
    cdef long pty5 =  realPoints[10][1]
    cdef long ptx105 =  realPoints[11][0]
    cdef long pty105 =  realPoints[11][1]
    cdef long ptx6 =  realPoints[12][0]
    cdef long pty6 =  realPoints[12][1]
    cdef long ptx106 =  realPoints[13][0]
    cdef long pty106 =  realPoints[13][1]
    cdef long ptx7 =  realPoints[14][0]
    cdef long pty7 =  realPoints[14][1]
    cdef long ptx107 =  realPoints[15][0]
    cdef long pty107 =  realPoints[15][1]

    for j in range(pts):
        for i in range(r):
            mpt = mockCombos[i][j]
            if mpt == 0:
                realCombos[i][j][0] = ptx0
                realCombos[i][j][1] = pty0
            if mpt == 100:
                realCombos[i][j][0] = ptx100
                realCombos[i][j][1] = pty100
            if mpt == 1:
                realCombos[i][j][0] = ptx1
                realCombos[i][j][1] = pty1
            if mpt == 101:
                realCombos[i][j][0] = ptx101
                realCombos[i][j][1] = pty101
            if mpt == 2:
                realCombos[i][j][0] = ptx2
                realCombos[i][j][1] = pty2
            if mpt == 102:
                realCombos[i][j][0] = ptx102
                realCombos[i][j][1] = pty102
            if mpt == 3:
                realCombos[i][j][0] = ptx3
                realCombos[i][j][1] = pty3
            if mpt == 103:
                realCombos[i][j][0] = ptx103
                realCombos[i][j][1] = pty103
            if mpt == 4:
                realCombos[i][j][0] = ptx4
                realCombos[i][j][1] = pty4
            if mpt == 104:
                realCombos[i][j][0] = ptx104
                realCombos[i][j][1] = pty104
            if mpt == 5:
                realCombos[i][j][0] = ptx5
                realCombos[i][j][1] = pty5
            if mpt == 105:
                realCombos[i][j][0] = ptx105
                realCombos[i][j][1] = pty105
            if mpt == 6:
                realCombos[i][j][0] = ptx6
                realCombos[i][j][1] = pty6
            if mpt == 106:
                realCombos[i][j][0] = ptx106
                realCombos[i][j][1] = pty106
            if mpt == 7:
                realCombos[i][j][0] = ptx7
                realCombos[i][j][1] = pty7
            if mpt == 107:
                realCombos[i][j][0] = ptx107
                realCombos[i][j][1] = pty107
    return realCombos
