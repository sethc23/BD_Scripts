
from libc.math cimport abs as c_abs
cimport cython
# from get_best_combo import c_get_best_combo as get_best_combo


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
# --	        s_d	oq	dgP	o	IR	new	o_res
# id (dg)	    --	0	0	0   --	0	--
# id (vendor)	0	--	--	--	--	--	--
# vend_X	    1	--	--	--	--	1	--
# vend_Y	    2	--	--	--	--	2	--
# orderNum	    3	--	--	--	--	3	--
# dg_X  	    --	1	1	1	--	--	0
# dg_Y  	    --	2	2	2	--	--	1
# deliveryNum  	--	3	--	3	--	--	2
# travTimeToLoc	--	4	--	4	--	--	5
#
# deliveryID  	4	5	--	5	7	4	3
# orderTime  	5	6	--	6	8	5	4
#
# start_X  	    6	7	--	7	--	6	6
# start_Y  	    7	8	--	8	--	7	7
#
# startTime  	--	9	--	9	--	--	8
# endTime  	    --	10	--	10	--	--	10
#
# end_X  	    8	11	--	11	--	8	11
# end_Y  	    9	12	--	12	--	9	12
#
# totOrdTime 	--	13	--	13	--	--	13
# travelTime	--	14	--	14	--	--	9
# totalDelivs	--	--	3	--	--	--	--
# currDelivs	--	--	4	--	--	--	--
# bestIndex	    --	--	--	--	--	--	--
# tripStTime	--	--	--	--	0	--	--
# tripStX	    --	--	--	--	1	--	--
# tripStY	    --	--	--	--	2	--	--
# tripPt-a_X	--	--	--	--	3	--	--
# tripPt-a_Y	--	--	--	--	4	--	--
# tripPt-b_X	--	--	--	--	5	--	--
# tripPt-b_Y	--	--	--	--	6	--	--

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long[:,::1] c_order_by_min(   long[:,::1] oq,                 # order queue
                                    # long[:,::1] oq_sorting,         # order queue dupe for sorting
                                    long[:,::1] dgp,                # pool of DG
                                    long[:,::1] newOrders,          # new orders
                                    long[::1] deliveryIDs,          # delivery IDs
                                    long[::1] orderTimes,           # order times
                                    long sp,                        # speed
                                    long md,                        # max delivery time
                                    long mdpp,                      # max delivery per person
                                    long mttlt,                     # max time to delivery locations
                                    long[:,::1] c_tripPoints,       # empty trip points array
                                    long[:,::1] orderSet2,          # permutation data for 2 orders
                                    long[:,::1] orderSet3,          # permutation data for 3 orders
                                    long[:,::1] orderSet4,          # permutation data for 4 orders
                                    long[:,::1] orderSet5,          # permutation data for 5 orders
                                    long[:,::1] orderSetInd,        # columns for [pt0, pt[i], i0, i[i], a1, [i]]
                                    long[:,:,::1] realCombos,       # blank real points, which will be arranged in same orders as mock combos
                                    long[:,::1] tT,                 # c_travelTimes
                                    long[:,::1] sT,                 # c_startTimes      #   NOTE: the left list with the "c_"
                                    long[:,::1] eT,                 # c_endTimes        #   are indicies for keeping track of
                                    long[:,::1] odt,                # c_odtTimes        #   certain things in getBestCombo.
                                    long[::1] oMax,                 # c_MaxOrderToDeliveryTimes
                                    long[::1] tMax,                 # c_MaxTravelToLocTimes
                                    long[:,::1] tdd,                # c_tddTimes
                                    long[::1] ctm,                  # c_ctm (cumulative time marker)
                                    long[:,::1] rv_comboStartInfo,  # return for combo start info (cols = 14)
                                    long[:,::1] rv_bestCombo,       # return for eval single order of best combo (cols = 15)
                                                                    # returns "o_res" format
                                    long[:,::1] rv_updatedBestCombo,        # return for individual order results (cols = 15)
                                    long[:,::1] rv_bestDG):            # return for group results (cols = 15)
    # cdefs
    cdef int ord_num = newOrders.shape[0]
    cdef int dgp_num = dgp.shape[0]
    cdef int oq_num = oq.shape[0]
    cdef int ord_i,ord
    cdef int dgp_i
    cdef int oq_i,oq_pt,next_oq_pt,zero_i,test_pt
    cdef int o_res_i,o_res_cnt
    cdef int o_res_rows = rv_bestDG.shape[0]
    cdef long totalDelivs, currentDelivs, totalTravTime, deliveryID, deliveryNum, bestDG_var
    cdef int started,st_oq_ind,end_oq_ind
    cdef long startTime,endTime
    cdef long bestSoloDG_time
    cdef int bestSoloDG_dgp_i,bestGrpDG_i
    cdef long[:,::1] c_get_combo_start_info
    cdef long[:,::1] o_grp
    cdef int groupRows
    cdef int grp_s_pt = 0
    cdef int grp_e_pt = 0
    cdef int complete,i,j,k,h,n,g,r_o,c_o,r_res,mpt,pts,r_mc
    cdef long s,e,x,y,t,dg_X,dg_Y,ID
    cdef long x1,y1,x2,y2,toLoc,toDel
    cdef long orderCount,currentX,currentY,deliveryCount,thisID
    cdef long[::1] ai
    cdef long[::1] grp_row
    cdef long[::1] aj
    cdef long[::1] ak
    cdef long[::1] ah
    cdef long[:,::1] o
    cdef long[::1] new
    cdef long now
    cdef long dg_ID
    cdef long[:,::1] aii
    cdef long tripStartTime
    cdef long tripStartPtX
    cdef long tripStartPtY
    cdef long[:,::1] tripPoints
    cdef long[:,::1] rv_comboStartInfo_i
    cdef long[:,::1] rv_i                   # individual return value
                                            # rv_i has {"oq","o"} format
    cdef long ro
    cdef long[::1] bi
    cdef long[:,::1] testSet
    cdef long[:,::1] bii
    cdef long[:,::1] cii
    cdef long[::1] ci
    cdef long[:,::1] dii
    cdef long[::1] di
    cdef long ptx0,pty0,ptx100,pty100
    cdef long ptx1,pty1,ptx101,pty101
    cdef long ptx2,pty2,ptx102,pty102
    cdef long ptx3,pty3,ptx103,pty103
    cdef long ptx4,pty4,ptx104,pty104
    cdef long ptx5,pty5,ptx105,pty105
    cdef long ptx6,pty6,ptx106,pty106
    cdef long ptx7,pty7,ptx107,pty107
    cdef long[:,::1] mockCombos
    cdef long[:,:] orderSK
    cdef long[:,:] pointSK
    cdef long[:,:,::1] tmp_realCombos
    cdef int BI
    cdef long minT                           # time in between each pt, best index.
    cdef long mc_pt,orderSK_pt,odt_pt,ttl_pt,sT_pt,eT_pt,xpta,ypta,xptb,yptb
    cdef long[:,::1] akk
    cdef long[:,::1] ajj
    cdef long[:,::1] rv_bestCombo_i
    cdef long[:,::1] rv_updatedBestCombo_i
    cdef long c,d
    cdef long s1,e1,s2,e2
    cdef long[::1] bj
    cdef long timeDiff
    cdef long minTimeIncrease,bestGrpDG_i_currentDelivs,bestGrpDG_i_totalDelivs

    # General Idea:
        # for each order:
            # get bestDG,
            # add to order_per_min return, and
            # update dgp.
        # return order queue

    # TODO: bestDG should not be limited to 5 orders ... if DG with max deliveries is being considered,
    # only the last four deliveries with the new delivery should be considered.

    if oq[0][3] == 0:                       # if deliveryNum is zero, than nothing in queue ...
        next_oq_pt = 0
    else:
        for oq_i in range(oq_num):
            test_pt = (oq_num-1)-oq_i       # working backwards ...
            if oq[test_pt][3] != 0:         # the moment deliveryNum does not equal 0 ...
                next_oq_pt = test_pt + 1
                break

    for ord_i in range(ord_num):
        new = newOrders[ord_i]
        deliveryID = new[4]
        now = new[5]

        bestDG_var = 0

        x1 = new[6]
        y1 = new[7]
        x2 = new[8]
        y2 = new[9]
        x = c_abs(x2-x1)
        y = c_abs(y2-y1)
        toDel = sp*(x+y)

        rv_bestDG[0][3] = 0               # setup to ensure no result returns error for no result
        bestSoloDG_dgp_i = -1
        bestSoloDG_time = 0
        bestGrpDG_i = -1

        minTimeIncrease = 1600
        bestGrpDG_i_currentDelivs = 0
        bestGrpDG_i_totalDelivs = 0
        bestDG_var = 0

        # [ 1 ] -->> GET BEST DG
        for dgp_i in range(dgp_num):
            complete = 0                # 0,2 --> no result;  # 1 --> process result

            ai = dgp[dgp_i]
            dg_ID = ai[0]
            currentX = ai[1]
            currentY = ai[2]
            totalDelivs = ai[3]

            currentDelivs = 0
            for oq_i in range(oq_num):
                bi = oq[oq_i]
                if bi[0] == dg_ID:
                    currentDelivs +=1
                    bi[1] = currentX
                    bi[2] = currentY
            ai[4] = currentDelivs
            deliveryCount = currentDelivs + 1
            r_o = 0
            c_o = 0

            if currentDelivs==0:
                x1 = ai[1]
                y1 = ai[2]
                x2 = new[6]
                y2 = new[7]
                x = c_abs(x2-x1)
                y = c_abs(y2-y1)
                toLoc = sp*(x+y)        # dg_pool loc to vendor
                totalTravTime = toLoc + toDel
                if toLoc <= mttlt and totalTravTime <= md:
                    # check to see if best solo, and save if so
                    if bestSoloDG_time == 0 or totalTravTime < bestSoloDG_time:
                        bestSoloDG_time = totalTravTime
                        bestSoloDG_dgp_i = dgp_i

                if bestDG_var==0 or toLoc<bestDG_var:
                    bestDG_var = toLoc

            else:
                st_oq_ind = -1
                started = 0
                for oq_i in range(oq_num):
                    bi = oq[oq_i]
                    deliveryNum = bi[3]
                    thisID = bi[0]
                    if deliveryNum!=0 and thisID == dg_ID:
                        if st_oq_ind==-1:
                            started = 1
                            st_oq_ind = oq_i
                        end_oq_ind = oq_i + 1       # keep index,startTime,endTime of last run
                        startTime = bi[9]
                        endTime = bi[10]
                        bi[1] = currentX            # update current location
                        bi[2] = currentY
                    if started == 1 and (thisID != dg_ID or deliveryNum == 0):
                        break

                # TODO: Need to bump this up to full md. But, first need to group DG evals.
                if currentDelivs+1 >= mdpp:         # if equal or more than allowed deliveries
                    complete = 2                    # signal for "Stop Eval This DG"

                else:                               # ... currentDelivs > 0

                    # get best combo from DG, if any, and keep if best
                    o = oq[st_oq_ind:end_oq_ind]
                    groupRows = end_oq_ind - st_oq_ind
                    r_o = o.shape[0]
                    c_o = o.shape[1]

                    rv_comboStartInfo_i = rv_comboStartInfo[:deliveryCount]
                    #----------------------------------------------------
                    #rv_comboStartInfo = get_combo_start_info(new,o,aii)

                    aii = rv_comboStartInfo_i
                    h=0     # h == index pt for order_q rows
                    k=0     # k == index pt for order_q cols
                    n=0
                    tripStartTime = 1000
                    for j in range(r_o):    # GOAL: identify where/when new trip will begin (in light of current trip)
                        aj = o[j]
                        s = aj[9]       # prior order start time
                        e = aj[10]      # prior order end time
                        if e>now:       # is there at least one order with an endTime less than now? if not, then return for single order.
                            n=1
                        if s-now < tripStartTime-now and s-now > 0:       # if trip hasn't started, and
                            tripStartTime = s                           # there is more time before this part of trip begins
                            h=j
                            k=0
                        if e-now < tripStartTime-now and e-now > 0:     # if t==endTime, it is too late to change DG's next destination
                            tripStartTime = e
                            h=j
                            k=4

                    aj = aii[0]
                    if n==0:
                        aj[0] = now
                        aj[1] = new[6]    # tripPtX = start_X
                        aj[2] = new[7]    # tripPtY = start_Y
                        aj[5] = -1        # this signals an error -- rv_comboStartInfo[0][0] == -1
                        complete = 2

                    else:
                        ah = o[h]

                        aj[0] = tripStartTime
                        n = 7+k
                        s = ah[n]
                        aj[1] = s         # tripPtX = start_X | end_X
                        n += 1
                        s = ah[n]
                        aj[2] = s         # tripPtY = start_Y | end_Y

                        h = 0
                        for j in range(r_o):  # TODO: need to re-write so easier to understand and resolves arrangement issue

                            aj = o[j]
                            s = aj[9]
                            e = aj[10]
                            g = 1

                            # Note (1): When endTime==now, that point is not included in tripPoints.
                            #   BUT, that point is the basis for tripStartTime and tripStartPt.

                            # START LOCATION
                            if (now < s and now < e):      # IF not start yet, use start point as start location

                                x1 = aj[7]
                                y1 = aj[8]
                                x2 = aj[11]
                                y2 = aj[12]

                            elif (s <= now and now < e):   # ELIF, (already started | starting) & (ending now | ending later),
                                                                    #   use the end point as start location
                                x1 = aj[11]
                                y1 = aj[12]
                                x2 = aj[11]
                                y2 = aj[12]

                            else:

                                g = 0

                            if g == 1:

                                ah = aii[h]

                                ah[3] = x1
                                ah[4] = y1
                                ah[5] = x2
                                ah[6] = y2

                                ah[7] = aj[5]   # deliveryID
                                ah[8] = aj[6]   # orderTime

                                h += 1

                        ah = aii[h]

                        ah[3] = new[6]
                        ah[4] = new[7]
                        ah[5] = new[8]
                        ah[6] = new[9]

                        ah[7] = new[4]
                        ah[8] = new[5]

                    rv_comboStartInfo_i = aii
                    # rv_comboStartInfo = get_combo_start_info(new,o,aii)
                    #----------------------------------------------------

                    aii = rv_comboStartInfo_i
                    ai = aii[0]
                    tripStartTime = ai[0]
                    tripStartPtX = ai[1]
                    tripStartPtY = ai[2]

                    # else --no error--
                    if ai[5] == -1:     # if error, then try single order eval

                        rv_updatedBestCombo_i = rv_updatedBestCombo[:1]
                        #----------------------------------------------------
                        # rv_i = eval_single_order(new,o,tripStartPtX,tripStartPtY,tripStartTime,sp,md,aii)

                        aii = rv_updatedBestCombo_i
                        x1 = tripStartPtX
                        y1 = tripStartPtY
                        x2 = new[6]
                        y2 = new[7]
                        x = c_abs(x2-x1)
                        y = c_abs(y2-y1)
                        toLoc = sp*(x+y)

                        if tripStartTime + toLoc + toDel <= md:

                            for j in range(r_o): # for each row
                                ai = o[j]
                                bi = aii[j]
                                for j in range(c_o): # and for each columns
                                    bi[j] = ai[j]       # copy to rv_
                                if j==r_o-1:
                                    # ID = ai[0]
                                    dg_X = ai[1]
                                    dg_Y = ai[2]
                            j = r_o+1 # why this
                            bi = aii[j]
                            bi[0] = dg_ID
                            bi[1] = dg_X
                            bi[2] = dg_Y
                            bi[3] = j           # deliveryNum
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
                            rv_i = aii[0:2]

                            # update dg_pool.currentDeliveries
                            bi = dgp[bestSoloDG_dgp_i]
                            bi[4] = 1
                        else:
                            aii[0][13] = 0    # signals "No Result"
                            rv_i = aii[0:0]

                        # rv_i = eval_single_order(new,o,tripStartPtX,tripStartPtY,tripStartTime,sp,md,aii)
                        #----------------------------------------------------

                        n = rv_i.shape[0]
                        if rv_i[0][13] == 0 or n==1:    # signal for "No Result"
                            complete = 2                # signal for "Stop Eval This DG"
                        else:
                            complete = 1                # signal for "Order Evaluated" , result = rv_i

                    # elif no error, then complete remains 0

                if complete == 0:

                    aii = rv_comboStartInfo_i
                    k=0
                    for j in range(deliveryCount):
                        ai = aii[j]
                        deliveryIDs[j] = ai[7]
                        orderTimes[j] = ai[8]
                        bi = c_tripPoints[k]
                        k += 1
                        bi[0] = ai[3]
                        bi[1] = ai[4]
                        bi = c_tripPoints[k]
                        k += 1
                        bi[0] = ai[5]
                        bi[1] = ai[6]

                    tripPoints = c_tripPoints[:deliveryCount*2]
                    if deliveryCount==2:
                        testSet=orderSet2
                        ai = orderSetInd[0]
                    elif deliveryCount==3:
                        testSet=orderSet3
                        ai = orderSetInd[1]
                    elif deliveryCount==4:
                        testSet=orderSet4
                        ai = orderSetInd[2]
                    elif deliveryCount==5:
                        testSet=orderSet5
                        ai = orderSetInd[3]
                    else:
                        oq[0][0] = 450
                        oq[0][3] = 450
                        return oq

                    # breaking up testSet info
                    bii=testSet.T
                    cii=bii[ai[0]:ai[1]]
                    mockCombos = cii.T
                    r_mc = mockCombos.shape[0]
                    bii=testSet.T
                    cii=bii[ai[2]:ai[3]]
                    orderSK = cii.T
                    bii=testSet.T
                    cii=bii[ai[4]:ai[5]]
                    pointSK = cii.T

                    tmp_realCombos = realCombos[:r_mc]




                    #----------------------------------------------------
                    # realCombos = c_mapper(tripPoints, mockCombos,tmp_realCombos)

                    pts = mockCombos.shape[1]   # columns
                    ajj = tripPoints.T
                    bi = ajj[0]
                    ci = ajj[1]

                    ptx0 =  bi[0:1][0]
                    pty0 =  ci[0:1][0]
                    ptx100 =  bi[1:2][0]
                    pty100 =  ci[1:2][0]
                    # if deliveryCount == 2:
                    ptx1 =  bi[2:3][0]
                    pty1 =  ci[2:3][0]
                    ptx101 =  bi[3:4][0]
                    pty101 =  ci[3:4][0]

                    if deliveryCount >= 3:
                        ptx2 =  bi[4:5][0]
                        pty2 =  ci[4:5][0]
                        ptx102 =  bi[5:6][0]
                        pty102 =  ci[5:6][0]
                    if deliveryCount >= 4:
                        ptx3 =  bi[6:7][0]
                        pty3 =  ci[6:7][0]
                        ptx103 =  bi[7:8][0]
                        pty103 =  ci[7:8][0]
                    if deliveryCount >= 5:
                        ptx4 =  bi[8:9][0]
                        pty4 =  ci[8:9][0]
                        ptx104 =  bi[9:10][0]
                        pty104 =  ci[9:10][0]
                    if deliveryCount >= 6:
                        ptx5 =  bi[10:11][0]
                        pty5 =  ci[10:11][0]
                        ptx105 =  bi[11:12][0]
                        pty105 =  ci[11:12][0]
                    if deliveryCount >= 7:
                        ptx6 =  bi[12:13][0]
                        pty6 =  ci[12:13][0]
                        ptx106 =  bi[13:14][0]
                        pty106 =  ci[13:14][0]
                    if deliveryCount >= 8:
                        ptx7 =  bi[14:15][0]
                        pty7 =  ci[14:15][0]
                        ptx107 =  bi[15:16][0]
                        pty107 =  ci[15:16][0]

                    for j in range(pts):
                        for k in range(r_mc):
                            mpt = mockCombos[k][j]
                            akk = tmp_realCombos[k]
                            aj = akk[j]
                            if mpt == 0:
                                aj[0] = ptx0
                                aj[1] = pty0
                            elif mpt == 100:
                                aj[0] = ptx100
                                aj[1] = pty100
                            elif mpt == 1:
                                aj[0] = ptx1
                                aj[1] = pty1
                            elif mpt == 101:
                                aj[0] = ptx101
                                aj[1] = pty101
                            elif mpt == 2:
                                aj[0] = ptx2
                                aj[1] = pty2
                            elif mpt == 102:
                                aj[0] = ptx102
                                aj[1] = pty102
                            elif mpt == 3:
                                aj[0] = ptx3
                                aj[1] = pty3
                            elif mpt == 103:
                                aj[0] = ptx103
                                aj[1] = pty103
                            elif mpt == 4:
                                aj[0] = ptx4
                                aj[1] = pty4
                            elif mpt == 104:
                                aj[0] = ptx104
                                aj[1] = pty104
                            elif mpt == 5:
                                aj[0] = ptx5
                                aj[1] = pty5
                            elif mpt == 105:
                                aj[0] = ptx105
                                aj[1] = pty105
                            elif mpt == 6:
                                aj[0] = ptx6
                                aj[1] = pty6
                            elif mpt == 106:
                                aj[0] = ptx106
                                aj[1] = pty106
                            elif mpt == 7:
                                aj[0] = ptx7
                                aj[1] = pty7
                            elif mpt == 107:
                                aj[0] = ptx107
                                aj[1] = pty107

                    realCombos = tmp_realCombos

                    # realCombos = c_mapper(tripPoints, mockCombos,tmp_realCombos)
                    #----------------------------------------------------

                    rv_bestCombo_i = rv_bestCombo[:deliveryCount]
                    #----------------------------------------------------
                    # rv_bestCombo_i = get_best_combo(tripStartPtX,  # returns "o_res" format
                    #                        tripStartPtY,
                    #                        mockCombos,
                    #                        realCombos,
                    #                        orderSK,
                    #                        pointSK,
                    #                        orderTimes,
                    #                        deliveryIDs,
                    #                        deliveryCount,
                    #                        tripStartTime,
                    #                        sp,
                    #                        md,
                    #                        mttlt,
                    #                        tT,
                    #                        sT,
                    #                        eT,
                    #                        odt,
                    #                        oMax,
                    #                        tMax,
                    #                        tdd,
                    #                        ctm,
                    #                        rv_bestCombo[:deliveryCount])
                    BI = r_mc + 1
                    minT =  (8 * md)     # minimum total route time (assuming 8 routes is max route #)
                    for j in range(pts):
                        for k in range(r_mc):
                            akk = realCombos[k]
                            if j == 0:
                                aj = akk[j]
                                xptb = aj[0]
                                yptb = aj[1]
                                x = c_abs( tripStartPtX - xptb )
                                y = c_abs( tripStartPtY - yptb )
                                t = sp * ( x + y )
                                ctm[k] = t
                                tT[k][j] = t
                                tMax[k] = t
                            else:
                                aj = akk[j-1]
                                xpta = aj[0]
                                ypta = aj[1]
                                aj = akk[j]
                                xptb = aj[0]
                                yptb = aj[1]
                                x = c_abs( xpta - xptb )
                                y = c_abs( ypta - yptb )
                                t = sp * ( x + y )
                                ctm[k] += t
                                tT[k][j] = t
                                if t > tMax[k]:
                                    tMax[k] = t

                            mc_pt = mockCombos[k][j]
                            if mc_pt < 100: sT[k][mc_pt] = ctm[k] + tripStartTime
                            else: eT[k][mc_pt-100] = ctm[k] + tripStartTime

                            if j == pts-1 and tMax[k] <= mttlt: # this is the last part of the 2D iteration
                                                                        # if max travelToLoc time is acceptable --> find Best Index
                                oMax[k] = 0
                                for n in range(deliveryCount):
                                    orderSK_pt = orderSK[k][n]
                                    eT_pt = eT[k][orderSK_pt]
                                    tdd[k][orderSK_pt] = eT_pt - sT[k][orderSK_pt]
                                    odt_pt = eT_pt - orderTimes[orderSK_pt]
                                    odt[k][orderSK_pt] = odt_pt
                                    if odt_pt > oMax[k]:
                                        oMax[k] = odt_pt              # update max order-to-delivery time [ per row ] -- keeping biggest value

                                if oMax[k] != 0 and oMax[k] <= md: # if order-to-delivery max is valid and acceptable
                                    if ctm[k] < minT:                 # for all acceptable rows, keep one with lowest cumul. time.
                                        minT = ctm[k]
                                        BI = k                        # setting Best Index

                    if minT == 8 * md:
                        rv_bestCombo_i[0][13] = 0                      # interpretted on return as an error
                        rv_bestCombo_i[1][13] = BI
                    elif BI == r_mc + 1:
                        rv_bestCombo_i[0][13] = 0                      # interpretted on return as an error
                        rv_bestCombo_i[1][13] = 505                    # interpretted on return as "error setting best index"
                    else:
                        aii = realCombos[BI]
                        for g in range(deliveryCount):
                            orderSK_pt=orderSK[BI][g]
                            ak = rv_bestCombo_i[g]                  # DEFINITION:
                            ak[0] = tripStartPtX                    # dg_X
                            ak[1] = tripStartPtY                    # dg_Y
                            ak[2] = orderSK_pt + 1                  # deliveryNum (starts at zero)
                            ak[3] = deliveryIDs[orderSK_pt]         # deliveryID (already sorted by key)
                            ak[4] = orderTimes[orderSK_pt]          # orderTime
                            mc_pt = pointSK[BI][orderSK_pt*2]
                            ak[5] = tT[BI][mc_pt]                   # travelTimeToLoc
                            aj = aii[mc_pt]
                            ak[6] = aj[0]   # startX // see below for explanation
                            ak[7] = aj[1]   # startY
                            ak[8] = sT[BI][orderSK_pt]              # startTime
                            ak[9] = tdd[BI][orderSK_pt]             # travelTime
                            ak[10]= eT[BI][orderSK_pt]              # endTime
                            mc_pt=pointSK[BI][(orderSK_pt*2)+1]
                            aj = aii[mc_pt]
                            ak[11]= aj[0]                           # endX
                            ak[12]= aj[1]                           # endY
                            ak[13]= odt[BI][orderSK_pt]             # totalOrderTime
                            ak[14]= BI

                    # rv_bestCombo_i = get_best_combo(tripStartPtX,...  # returns "o_res" format
                    #----------------------------------------------------

                    if rv_bestCombo_i[0][13] != 0:                 # (general error | error setting best index)

                        # TODO: NEED TO ALSO CHANGE FORMAT
                        #
                        # SHOULD PASTE ALL VALUES IN BEST DG HERE IF THAT IS THE CASE
                        #
                        #----------------------------------------------------
                        # rv_bestCombo_i = update_order_results(o,rv_bestCombo_i,now) # expects "o_res" input // returns "o_res" format

                        aii = rv_bestCombo_i
                        r_res = aii.shape[0]
                        # iterate through o_res to replace info with static order info
                        for j in range(r_o):
                            aj = o[j]
                            if aj[9] <= now and aj[10] > now:  # if then they are static orders...
                                # use deliveryID to temp. use deliveryNum column in "o_res" as an index to "o"
                                d = aj[5]               # order deliveryID
                                for k in range(r_res):
                                    ak = aii[k]
                                    c = ak[3]           # order result deliveryID
                                    if c == d:          # if order deliveryID matches order results deliveryID ...
                                        ak[5] = aj[4]   # travelTimeToLoc
                                        ak[4] = aj[6]   # orderTime
                                        ak[6] = aj[7]   # start_X
                                        ak[7] = aj[8]   # start_Y
                                        ak[8] = aj[9]   # startTime
                                        if ak[11] == tripStartPtX and ak[12] == tripStartPtY:
                                            ak[10] = aj[10]   # endTime IF used as starting point.
                                        break                 # only one point can be a starting point

                        rv_bestCombo_i = aii
                        # rv_bestCombo_i = update_order_results(o,rv_bestCombo_i,now) # expects "o_res" input // returns "o_res" format
                        #----------------------------------------------------

                        # RESET DELIVERY COUNT HERE

                        # rv_i is var to fill (using rv_updatedBestCombo, which is same as above when defining rv_i)
                        rv_i = rv_updatedBestCombo[:deliveryCount]
                        aii = rv_i.T
                        # ai = rv_i[deliveryCount-1] # the last row
                        bii = rv_bestCombo_i.T  # var with updated order info (in "o_res" format)
                        cii = o.T   # var with original order info (and less one order) (in "o" format)
                        ci = o[0]   # first original order
                        # dii = rv_i[:deliveryCount-1]  # all rows but the last row

                        # take from old orders (e.g., id,dg_X,dg_Y)
                        # (applied to new orders var EXCEPT for last row)
                        r_o = o.shape[0]
                        for g in range(deliveryCount):
                            ai = rv_i[g]
                            ai[0] = dg_ID       # id
                            ai[1] = ci[0]       # dg_X
                            ai[2] = ci[1]       # dg_y

                        # take from new orders
                        aii[3] = bii[2]             # deliveryNum
                        aii[4] = bii[5]             # travelTimeToLocation
                        aii[5] = bii[3]             # deliveryID
                        aii[6] = bii[4]             # orderTime
                        aii[7] = bii[6]             # start_X
                        aii[8] = bii[7]             # start_Y
                        aii[9] = bii[8]             # startTime
                        aii[10] = bii[10]           # endTime
                        aii[11] = bii[11]           # end_X
                        aii[12] = bii[12]           # end_Y
                        aii[13] = bii[13]           # totalOrderTime
                        aii[14] = bii[9]            # travelTime
                        complete = 1

                if complete == 1:
                    # checkVar = (order_result.endTime.max() - order_result.startTime.min()) - (order_q_i.endTime.max() - order_q_i.startTime.min())
                    # TODO: how can this be setup to account for travelTimeToLoc for fresh DGs??
                    # checkVar = ( e2 - s2 ) - ( e1 - s1 )

                    # assuming there DG is already scheduled for an order ...
                    # need to find the max/min for this result and compare with previous result
                    aj = rv_i[0]        # current result
                    e2 = aj[10]
                    s2 = aj[9]

                    bj = o[0]           # older result
                    e1 = bj[10]
                    s1 = bj[9]
                    for j in range(1,deliveryCount):
                        aj = rv_i[j]
                        s = aj[9]
                        e = aj[10]
                        if e > e2:
                            e2 = e      # min of current result
                        if s < s2:
                            s2 = s

                        ## ------------- //
                        if j != deliveryCount-1:
                            bj = o[j]
                            s = bj[9]
                            e = bj[10]
                            if e > e1:
                                e1 = e  # min of older result
                            if s < s1:
                                s1 = s
                        ## // -------------

                    timeDiff = (e2-s2) - (e1-s1)
                    if timeDiff <= minTimeIncrease:

                        if (deliveryCount > bestGrpDG_i_currentDelivs) or (totalDelivs > bestGrpDG_i_totalDelivs):

                            if deliveryCount > bestGrpDG_i_currentDelivs:
                                bestGrpDG_i_currentDelivs = currentDelivs
                            if totalDelivs > bestGrpDG_i_totalDelivs:
                                bestGrpDG_i_totalDelivs = totalDelivs

                            minTimeIncrease = timeDiff
                            bestGrpDG_i = dgp_i

                            rv_bestDG[:deliveryCount] = rv_i
                            rv_bestDG[deliveryCount:] = 0
                            bestDG_var = deliveryCount
        #
        #                     if dg_ID == 139:
        #                         oq[next_oq_pt][0] = 555
        #                         oq[next_oq_pt][3] = 555
        #                         oq[next_oq_pt][4] = rv_bestDG.shape[0]
        #                         oq[next_oq_pt][5] = deliveryID
        #                         oq[next_oq_pt][6] = tripStartTime
        #                         oq[next_oq_pt][7] = tripStartPtX
        #                         oq[next_oq_pt][8] = tripStartPtY
        #                         oq[next_oq_pt][9] = rv_comboStartInfo_i.shape[0]
        #                         oq[next_oq_pt][10] = rv_comboStartInfo_i[0][0]
        #                         oq[next_oq_pt][11] = rv_comboStartInfo_i[0][1]
        #                         oq[next_oq_pt][12] = rv_comboStartInfo_i[0][2]
        #                         oq[next_oq_pt][13] = rv_comboStartInfo_i[1][1]
        #                         oq[next_oq_pt][14] = rv_comboStartInfo_i[1][2]
        #
        #                         oq[next_oq_pt-12] = rv_bestDG[0]
        #                         oq[next_oq_pt-11] = rv_bestDG[1]
        #                         oq[next_oq_pt-10] = rv_bestDG[2]
        #                         oq[next_oq_pt-9] = rv_bestDG[3]
        #
        #                         oq[next_oq_pt-8][3] = 1
        #                         oq[next_oq_pt-8][4] = realCombos[0][0][0]
        #                         oq[next_oq_pt-8][5] = realCombos[0][0][1]
        #                         oq[next_oq_pt-8][0] = 170
        #                         oq[next_oq_pt-7][3] = o[0][5]
        #                         oq[next_oq_pt-7][4] = realCombos[0][1][0]
        #                         oq[next_oq_pt-7][5] = realCombos[0][1][1]
        #                         oq[next_oq_pt-7][10] = rv_comboStartInfo_i[0][3]
        #                         oq[next_oq_pt-7][11] = rv_comboStartInfo_i[0][4]
        #                         oq[next_oq_pt-7][12] = rv_comboStartInfo_i[0][5]
        #                         oq[next_oq_pt-7][13] = rv_comboStartInfo_i[0][6]
        #                         oq[next_oq_pt-7][0] = 170
        #                         oq[next_oq_pt-6][3] = 2
        #                         oq[next_oq_pt-6][4] = realCombos[0][2][0]
        #                         oq[next_oq_pt-6][5] = realCombos[0][2][1]
        #                         oq[next_oq_pt-6][0] = 170
        #                         oq[next_oq_pt-5][3] = o[1][5]
        #                         oq[next_oq_pt-5][4] = realCombos[0][3][0]
        #                         oq[next_oq_pt-5][5] = realCombos[0][3][1]
        #                         oq[next_oq_pt-5][10] = rv_comboStartInfo_i[1][3]
        #                         oq[next_oq_pt-5][11] = rv_comboStartInfo_i[1][4]
        #                         oq[next_oq_pt-5][12] = rv_comboStartInfo_i[1][5]
        #                         oq[next_oq_pt-5][13] = rv_comboStartInfo_i[1][6]
        #                         oq[next_oq_pt-5][0] = 170
        #                         oq[next_oq_pt-4][3] = 3
        #                         oq[next_oq_pt-4][4] = realCombos[0][4][0]
        #                         oq[next_oq_pt-4][5] = realCombos[0][4][1]
        #                         oq[next_oq_pt-4][0] = 170
        #                         oq[next_oq_pt-3][3] = o[2][5]
        #                         oq[next_oq_pt-3][4] = realCombos[0][5][0]
        #                         oq[next_oq_pt-3][5] = realCombos[0][5][1]
        #                         oq[next_oq_pt-3][10] = rv_comboStartInfo_i[2][3]
        #                         oq[next_oq_pt-3][11] = rv_comboStartInfo_i[2][4]
        #                         oq[next_oq_pt-3][12] = rv_comboStartInfo_i[2][5]
        #                         oq[next_oq_pt-3][13] = rv_comboStartInfo_i[2][6]
        #                         oq[next_oq_pt-3][0] = 170
        #
        #                         oq[next_oq_pt-2][3] = 4
        #                         oq[next_oq_pt-2][4] = realCombos[0][6][0]
        #                         oq[next_oq_pt-2][5] = realCombos[0][6][1]
        #                         oq[next_oq_pt-2][0] = 170
        #
        #                         oq[next_oq_pt-1][3] = deliveryID
        #                         oq[next_oq_pt-1][4] = realCombos[0][7][0]
        #                         oq[next_oq_pt-1][5] = realCombos[0][7][1]
        #                         oq[next_oq_pt-1][10] = rv_comboStartInfo_i[3][3]
        #                         oq[next_oq_pt-1][11] = rv_comboStartInfo_i[3][4]
        #                         oq[next_oq_pt-1][12] = rv_comboStartInfo_i[3][5]
        #                         oq[next_oq_pt-1][13] = rv_comboStartInfo_i[3][6]
        #                         oq[next_oq_pt-1][0] = 170
        #
        #                         # oq[next_oq_pt-4] = rv_bestCombo_i[1]
        #                         # oq[next_oq_pt-4][0] = 170
        #                         # oq[next_oq_pt-5] = rv_bestCombo_i[0]
        #                         # oq[next_oq_pt-5][0] = 170
        #                         return oq
        # #
        # --------------
        # --------------
        #

        # rv_bestDG is the best DG from DG Queue
        # bestSoloDG_dgp_i points to best DG from DG Pool
        # 950 means re-pool necessary

        if bestGrpDG_i == -1 and bestSoloDG_dgp_i == -1:            # A:    need to re-pool ...

            oq[next_oq_pt][0] = 950
            oq[next_oq_pt][1] = ord_i
            oq[next_oq_pt][2] = dgp_i
            oq[next_oq_pt][3] = newOrders[ord_i][4]
            oq[next_oq_pt][3] = 950
            return oq

        elif bestGrpDG_i == -1 and bestSoloDG_dgp_i != -1:          # B:    use new dg

            ai = oq[next_oq_pt]
            next_oq_pt = next_oq_pt + 1
            bi = dgp[bestSoloDG_dgp_i]

            bi[4] = 1 # UPDATE DG POOL

            ai[0] = bi[0]                       # id
            ai[1] = bi[1]                       # dg_X
            ai[2] = bi[2]                       # dg_Y

            ai[3] = 1                           # deliveryNum

            ai[4] = bestSoloDG_time - toDel     # travel time to location
            ai[5] = new[4]                      # deliveryID

            ai[6] = new[5]                      # orderTime

            ai[7] = new[1]                      # start X
            ai[8] = new[2]                      # start Y

            ai[9] = ai[6] + ai[4]               # startTime
            ai[10] = ai[9] + toDel              # endTime

            ai[11] = new[8]                     # end X
            ai[12] = new[9]                     # end Y
            ai[13] = bestSoloDG_time            # total order time
            ai[14] = toDel                      # travel time


        else:                                                       # C:    use bestDG from previous calculations

            # FIRST, update dgp with dgp_i


            # SECOND, create groups of currentDelivs
            #   will wait to see results before adding feature
            # TODO: compare results for more structured DG evaluations

            # THIRD, for every entry in oq with different dg_ID, re-copy back to oq
            dg_ID = rv_bestDG[0][0]
            next_oq_pt = 0
            currentDelivs = 0
            for oq_i in range(oq_num):
                bi = oq[oq_i]
                if bi[3] != 0 and bi[0] != dg_ID:
                    oq[next_oq_pt] = bi                     # oq is updated in-place with only non-CurrentID info
                    next_oq_pt += 1
                elif bi[3] != 0 and bi[0] == dg_ID:
                    currentDelivs +=1
            deliveryCount = currentDelivs + 1

            # FOURTH, copy rv_bestDG info to array ( and update DG Pool )
            # o_res_rows = bestGrpDG_i_currentDelivs + 1
            ai = dgp[bestGrpDG_i]
            ai[4] = deliveryCount

            for o_res_i in range(deliveryCount):
                bi = rv_bestDG[o_res_i]
                if bi[3] != 0:                              # if deliveryNum != 0
                    oq[next_oq_pt] = bi
                    next_oq_pt += 1
                else:
                    break

            # FIFTH, zero out remaining part of array
            for zero_i in range(next_oq_pt,oq_num):
                # TODO: cut this when debug is complete
                ai = oq[zero_i]
                if ai[3] != 0:
                    g=zero_i+1
                    oq[g][0] = 555
                    oq[g][1] = 998
                    oq[g][2] = 998
                    oq[g][3] = 555
                    oq[g][4] = zero_i
                    oq[g][5] = next_oq_pt
                    oq[g][6] = oq_num

                    return oq
                oq[zero_i] = 0





    return oq