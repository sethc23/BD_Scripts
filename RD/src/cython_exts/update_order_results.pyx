
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long[:,::1] c_update_order_results(long[:, ::1] o_u, long[:, ::1] o_res_u, long now_u):
    cdef long p = o_u.shape[0]
    cdef long p_res = o_res_u.shape[0]
    cdef long C,D
    cdef int i,j
    cdef long[::1] ai
    cdef long[::1] aj

    # iterate through o_res to replace info for static orders
    for i in range(p):
        ai = o_u[i]
        if ai[9] <= now_u and ai[10] > now_u:  # if then they are static orders...

            # use deliveryID to temp. use deliveryNum column in "o_res" as an index to "o"
            D = ai[5]               # order deliveryID
            for j in range(p_res):
                aj = o_res_u[j]
                C = aj[3]           # order result deliveryID
                if C == D:          # if order deliveryID matches order results deliveryID ...

                    aj[5] = ai[4]   # travelTimeToLoc
                    aj[4] = ai[6]   # orderTime
                    aj[6] = ai[7]   # start_X
                    aj[7] = ai[8]   # start_Y
                    aj[8] = ai[9]   # startTime

                    break

    return o_res_u

    # important indicies:
    #
    #      order_q_i [o] / [new] / order_result [o_res]
    # id  		        0	0	--
    # vend_X	 	    --	1	--
    # vend_Y	 	    --	2	--
    # orderNum	        --	3	--
    # dg_X  		    1	--	0
    # dg_Y  		    2	--	1
    # deliveryNum  	    3	--	2
    # travelTimeToLoc   4	--	5
    # deliveryID  	    5	4	3
    # orderTime  	    6	5	4
    # start_X  	        7	6	6
    # start_Y  	        8	7	7
    # startTime  	    9	8	8
    # endTime  	        10	9	10
    # end_X  		    11	10	11
    # end_Y  		    12	11	12
    # totalOrderTime 	13	12	13
    # travelTime	    14	13	9
    # bestIndex	        --	--	--