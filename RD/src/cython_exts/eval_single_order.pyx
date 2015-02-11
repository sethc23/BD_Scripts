
from libc.math cimport abs as c_abs
cimport cython

# IMPORTANT INDICIES:
# -------------------------------------------
#   Global:
#       oq == order_q
#       dgp == dg_pool
#       o == order_q_i
#   Results:
#       IR == results from getStartInfo function
#       (results from eval_single_order have 'oq' format)
#       new == new
#       o_res == order results
# -------------------------------------------
# --	        oq	dgP	o	IR	new	o_res
# id  	        0	0	0	--	0	--
# vend_X	    --	--	--	--	1	--
# vend_Y	    --	--	--	--	2	--
# orderNum	    --	--	--	--	3	--
# dg_X  	    1	1	1	--	--	0
# dg_Y  	    2	2	2	--	--	1
# deliveryNum  	3	--	3	--	--	2
# travTimeToLoc	4	--	4	--	--	5
#
# deliveryID  	5	--	5	7	4	3
# orderTime  	6	--	6	8	5	4
#
# start_X  	    7	--	7	--	6	6
# start_Y  	    8	--	8	--	7	7
#
# startTime  	9	--	9	--	--	8
# endTime  	    10	--	10	--	--	9
#
# end_X  	    11	--	11	--	8	10
# end_Y  	    12	--	12	--	9	11
#
# totOrdTime 	13	--	13	--	--	12
# travelTime	14	--	14	--	--	13
# totalDeliv	--	3	--	--	--	--
# currDelivs	--	4	--	--	--	--
# bestIndex	    --	--	--	--	--	14
# tripStTime	--	--	--	0	--	--
# tripStX	    --	--	--	1	--	--
# tripStY	    --	--	--	2	--	--
# tripPt_X_1st	--	--	--	3	--	--
# tripPt_Y_1st	--	--	--	4	--	--
# tripPt_X_2nd	--	--	--	5	--	--
# tripPt_Y_2nd	--	--	--	6	--	--


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long[:,::1] c_eval_single_order(long[::1] new,
                                      long[:, ::1] o,
                                      long tripStartPtX,
                                      long tripStartPtY,
                                      long tripStartTime,
                                      long sp,long md,
                                      long[:, ::1] returnVar):
    # new,order_q_i,tripStartPtX,tripStartPtY,tripStartTime,speed,max_delivery_time,returnVar
    cdef int r = o.shape[0]                            # number of rows
    cdef int c = o.shape[1]
    cdef long s,e,t,dg_X,dg_Y,ID
    cdef int i,j
    cdef long x1,y1,x2,y2,x,y,toLoc,toDel
    cdef long[::1] ai
    cdef long[::1] bi

    x1 = tripStartPtX
    y1 = tripStartPtY
    x2 = new[6]
    y2 = new[7]
    x = c_abs(x2-x1)
    y = c_abs(y2-y1)
    toLoc = sp*(x+y)

    # x2 = new[6]
    # y2 = new[7]
    x1 = new[8]
    y1 = new[9]
    x = c_abs(x1-x2)
    y = c_abs(y1-y2)
    toDel = sp*(x+y)

    if tripStartTime + toLoc + toDel <= md:
        for i in range(r):
            ai = o[i]
            bi = returnVar[i]
            for j in range(c):
                bi[j] = ai[j]
            if i==r-1:
                ID = ai[0]
                dg_X = ai[1]
                dg_Y = ai[2]
        i = r+1
        bi = returnVar[i]
        bi[0] = ID
        bi[1] = dg_X
        bi[2] = dg_Y
        bi[3] = i           # deliveryNum
        bi[4] = toLoc
        bi[5] = new[4]      # deliveryID
        t = new[5]
        bi[6] = t           # orderTime
        bi[7] = new[6]      # start_X
        bi[8] = new[7]      # start_Y
        s = tripStartTime + toLoc
        bi[9] = s           # startTime
        e = tripStartTime + toLoc + toDel
        bi[10] = e          # endTime
        bi[11] = new[8]     # end_X
        bi[12] = new[9]     # end_Y
        bi[13] = s - t      # totalOrderTime
        bi[14] = e - s      # travelTime
        return returnVar[0:2]
    else:
        returnVar[0][13] = 0    # signals no result
        return returnVar[0:0]