
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long[:,::1] c_get_combo_start_info(long[::1] new, long[:, ::1] o, long[:, ::1] returnVar):
    """
    # INPUTS:
    c_new = np.ascontiguousarray(pd.DataFrame([[    13,     11,
                                                    430,    2581    ]],
                                          columns=['deliv_id'   ,'order_time',
                                                   'start_node' ,'end_node']
                                          ).iloc[0].astype(long).tolist(),dtype=np.long)
    cols = ['deliv_id'  ,'order_time',
            'start_time','start_node',
            'end_time'  ,'end_node']
    vals = np.array([[ 16.  ,  8.  ,
                       10.1 , 893. ,
                       13.4 , 4417. ]])
    c_order_q_i = np.ascontiguousarray(pd.DataFrame(vals,columns=cols).astype(long).as_matrix(),dtype=np.long)
    r=1
    c_returnVar = np.ascontiguousarray(np.empty((r+1,6), dtype=np.long,order='C'))

    # RETURNS:
     [0]   tripStartTime
     [1]   tripStartPt
     [2]   tripPtA
     [3]   tripPtB
     [4]   deliveryID
     [5]   orderTime
    """
    cdef long r = o.shape[0]
    cdef long z = returnVar.shape[0]
    cdef long s,e,x,y
    cdef long p1,p2
    cdef int i,j,k,n,t,g
    cdef long now = new[1]
    cdef long tripStartTime = 1000          # arbitrarily set high initially, but replaced early in iteration
    cdef long[::1] ai
    cdef long[::1] aj
    cdef long[::1] ak

    n=0
    k=0
    j=0

    for i in range(r):
        ai = o[i]
        s  = ai[2]       # start time
        e  = ai[4]       # end time

        if e>now:       # is there at least one order with an endTime less than now? if not, then return for single order.
            n=1

        # if t==endTime, it is too late to change DG's next destination
        # these two below conditions find the first tripPt that can be changed, i.e., tripPt that DG is not on route to
        if s-now < tripStartTime-now and s-now>0:
            tripStartTime = s
            j=i                                         # j == row index pt
            k=3                                         # k == index pt for whether last point is ( startPt | endPt )
        if e-now < tripStartTime-now and e-now>0:
            tripStartTime = e
            j=i
            k=5

    ai = returnVar[0]
    if n==0:
        ai[0] = now
        ai[1] = new[2]      # tripPtA = start_node
        ai[5] = -1          # this signals an error
        return returnVar
    else:
        aj      = o[j]
        ai[0]   = tripStartTime
        s       = aj[k]
        ai[1]   = s                 # tripPtA = (start_A | end_A)

    n = 0
    j = 0
    k = 0
    for i in range(r):
        ai = o[i]
        s  = ai[2]
        e  = ai[4]
        g  = 1

        # if i==0:
        #     p1 = ai[5]
        #     p2 = ai[5]
        if (now < s and now < e):      # IF not start yet, use start point as start location
            p1 = ai[3]
            p2 = ai[5]
        elif (s <= now and now < e):   # ELIF, (already started | starting) & (ending now | ending later),
            p1 = ai[5]
            p2 = ai[5]
        else:
            g = 0

        if g == 1:
            aj = returnVar[j]
            aj[4] = ai[0]       # deliveryID
            aj[5] = ai[1]       # orderTime
            j += 1

            ak = returnVar[k]
            k += 1

            t = n+2
            ak[t] = p1
            t += 1
            ak[t] = p2
            if k == z:
                k = 0
                n = 2

            ak = returnVar[k]
            k += 1

            t = n+2
            ak[t] = p1
            t += 1
            ak[t] = p2
            if k == z:
                k = 0
                n = 2

    aj = returnVar[j]  # sets deliv_id and orderTime for last row
    aj[4] = new[0]
    aj[5] = new[1]
    # k = z-2
    # ak = returnVar[k]
    # ak[3] = new[2]
    # k += 1
    k = z-1
    ak = returnVar[k]
    ak[2] = new[2]
    ak[3] = new[3]

    return returnVar

# RETURNS:
# [0]   tripStartTime
# [1]   tripStartPt
# [2]   tripPtA
# [3]   tripPtB
# [4]   deliveryID
# [5]   orderTime