# encoding: utf-8
# filename: math_functions.pyx
cdef int x1,y1,x2,y2,x3,y3

cpdef float minimum_relative_distance(int x3, int y3, int x1, int y1, int x2, int y2):
    cdef int px,py
    cdef float lengthSq,u,x,y,dx,dy,dist
    px = x2-x1
    py = y2-y1
    lengthSq = px*px + py*py
    u = ((x3-x1) * px + (y3-y1) * py) / lengthSq
    if u > 1: u=1
    elif u < 0: u=0
    x = x1 + u * px
    y = y1 + u * py
    dx = x - x3
    dy = y - y3
    dist = dx*dx + dy*dy
    # actual distance is sqrt(dist)
    return dist
