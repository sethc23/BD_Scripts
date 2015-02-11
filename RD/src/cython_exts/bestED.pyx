
cimport cython
from os import getcwd
from sys import path as py_path
py_path.append(getcwd()+'/cython_exts')
from get_combo_start_info cimport c_get_combo_start_info as get_combo_start_info
from eval_single_order cimport c_eval_single_order as eval_single_order
from map_points_to_combos cimport c_mapper2,c_mapper3,c_mapper4,c_mapper5,c_mapper6,c_mapper7
from get_best_combo cimport c_get_best_combo as get_best_combo
from update_order_results cimport c_update_order_results as update_order_results



@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long[:,::1] c_bestED(long[::1] new,                   # new order
                            long[:,::1] o,                  # order_q_i
                            long deliveryCount,             # delivery count
                            long[::1] deliveryIDs,          # delivery IDs
                            long[::1] orderTimes,           # order times
                            long sp,                        # speed
                            long md,                        # max delivery time
                            long mttlt,                     # max time to delivery locations
                            long[:,::1] tripPoints,         # empty trip points array
                            long[:,::1] mockCombos,         # mock combos
                            long[:,:,::1] realCombos,       # real points arranged in same orders as mock combos
                            long[:,::1] orderSK,            # sort index for orders
                            long[:,::1] pointSK,            # sort index for route locations
                            long[:,::1] tT,                 # c_travelTimes     # the below list with the "c_"
                            long[:,::1] sT,                 # c_startTimes      #   are indicies for keeping
                            long[:,::1] eT,                 # c_endTimes        #   track of certain things.
                            long[:,::1] odt,                # c_odtTimes
                            long[::1] oMax,                 # c_MaxOrderToDeliveryTimes
                            long[::1] tMax,                 # c_MaxTravelToLocTimes
                            long[:,::1] tdd,                # c_tddTimes
                            long[::1] ctm,                  # cumulative time marker
                            long[:,::1] o_res,
                            long[:,::1] returnVar):
    """
    # IMPORTANT INDICIES:
    # -------------------------------------------
    #   Global:
    #       s_d   == sim_data
    #       oq    == order_q
    #       dgp   == dg_pool
    #       o     == order_q_i
    #   Results:
    #       IR == results from getStartInfo function
    #       (results from eval_single_order have 'oq' format)
    #       new == new
    #       o_res == order results
    # -------------------------------------------
    # --	        s_d	oq	dgP	o	IR	new	o_res
    # id (dg)	    --	0	0	--	--	--  --
    # id (vendor)	0	--	--	--	--	--	--
    # vend_X	    1	--	--	--	--	1	--
    # vend_Y	    2	--	--	--	--	2	--
    # orderNum	    3	--	--	--	--	3	--
    # dg_X  	    --	1	1	1	--	--	0
    # dg_Y  	    --	2	2	2	--	--	1
    # deliveryNum  	--	3	--	3	--	--	2
    # travTimeToLoc	--	4	--	4	--	--	5
    #	--
    # deliveryID  	4	5	--	5	7	4	3
    # orderTime  	5	6	--	6	8	5	4
    #
    # start_X  	    6	7	--	7	--	6	6
    # start_Y  	    7	8	--	8	--	7	7
    #
    # startTime  	--	9	--	9	--	--	8
    # endTime  	    --	10	--	10	--	--	9
    #
    # end_X  	    8	11	--	11	--	8	10
    # end_Y  	    9	12	--	12	--	9	11
    #
    # totOrdTime 	--	13	--	13	--	--	12
    # travelTime	--	14	--	14	--	--	13
    # totalDeliv	--	--	3	--	--	--	--
    # currDelivs	--	--	4	--	--	--	--
    # bestIndex	    --	--	--	--	--	--	14
    # tripStTime	--	--	--	--	0	--	--
    # tripStX	    --	--	--	--	1	--	--
    # tripStY	    --	--	--	--	2	--	--
    # tripPt_X_1st	--	--	--	--	3	--	--
    # tripPt_Y_1st	--	--	--	--	4	--	--
    # tripPt_X_2nd	--	--	--	--	5	--	--
    # tripPt_Y_2nd	--	--	--	--	6	--	--
    """
    # cdefs
    cdef int r = o.shape[0]
    cdef int c = o.shape[1]
    cdef long now = new[5]
    cdef long s,e,t
    cdef int i,j,k,n
    cdef long x1,y1,x2,y2,x,y,toLoc,toDel
    cdef long tripStartTime
    cdef long tripStartPtX
    cdef long tripStartPtY
    cdef long[::1] ai
    cdef long[::1] bi

    returnVar = get_combo_start_info(new,o,returnVar)
    ai = returnVar[0]
    tripStartTime = ai[0]
    tripStartPtX = ai[1]
    tripStartPtY = ai[2]

    if ai[5] == -1:
        returnVar = eval_single_order(new,o,tripStartPtX,tripStartPtY,tripStartTime,sp,md,returnVar)
        return returnVar

    n = deliveryCount
    for i in range(n):
        ai = returnVar[i]
        deliveryIDs[i] = ai[7]
        orderTimes[i] = ai[8]
        bi = tripPoints[i]
        bi[0] = ai[3]
        bi[1] = ai[4]
        k=i+n
        bi = tripPoints[k]
        bi[0] = ai[5]
        bi[1] = ai[6]

    if deliveryCount == 2:
        realCombos = c_mapper2(tripPoints, mockCombos,realCombos)
    if deliveryCount == 3:
        realCombos = c_mapper3(tripPoints, mockCombos,realCombos)
    if deliveryCount == 4:
        realCombos = c_mapper4(tripPoints, mockCombos,realCombos)
    if deliveryCount == 5:
        realCombos = c_mapper5(tripPoints, mockCombos,realCombos)
    if deliveryCount == 6:
        realCombos = c_mapper6(tripPoints, mockCombos,realCombos)
    if deliveryCount == 7:
        realCombos = c_mapper7(tripPoints, mockCombos,realCombos)

    o_res = get_best_combo(tripStartPtX,
                           tripStartPtY,
                           mockCombos,
                           realCombos,
                           orderSK,
                           pointSK,
                           orderTimes,
                           deliveryIDs,
                           deliveryCount,
                           tripStartTime,
                           sp,
                           md,
                           mttlt,
                           tT,
                           sT,
                           eT,
                           odt,
                           oMax,
                           tMax,
                           tdd,
                           ctm,
                           o_res)

    if o_res[0][13] != 0:   # (general error | error setting best index)
        o_res = update_order_results(o,o_res[:n],now)

    return o_res



