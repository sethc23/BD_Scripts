
resume = False
save = False

from math import fabs as c_abs
# from libc.math cimport abs as c_abs
# cimport cython
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
import pandas,numpy

def systemError():
    print 'systemError()'
    raise SystemError

def oq_to_order_q(ret_order_q,showVar=True):
    a = numpy.asarray(ret_order_q)
    if showVar==True: print a,'\n'
    # print a.shape

    oq_cols=['id','dg_X','dg_Y','deliveryNum','travelTimeToLoc','deliveryID','orderTime','start_X','start_Y','startTime','endTime','end_X','end_Y','totalOrderTime','travelTime']
    o_res_cols = ['dg_X','dg_Y','deliveryNum','deliveryID','orderTime','travelTimeToLoc',
                     'start_X','start_Y','startTime','travelTime','endTime','end_X','end_Y',
                     'totalOrderTime','id']
    ret_cols = o_res_cols if a.shape[1]==14 else oq_cols
    order_q_ret = pandas.DataFrame(a,columns=ret_cols)

    return order_q_ret

def c2_order_by_min(oq,                 # order queue
                    oq_b,
                    reorder_q,
                    dgp,              # pool of DG
                    dgp_b,              # dg_pool (Secondary)
                    dg_seg_size,
                    newOrders,          # new orders
                    deliveryIDs,          # delivery IDs
                    orderTimes,           # order times
                    sp,                        # speed
                    md,                        # max delivery time
                    mdpp,                      # max delivery per person
                    mttlt,                     # max time to delivery locations
                    c_tripPoints,       # empty trip points array
                    orderSet2,          # permutation data for 2 orders
                    orderSet3,          # permutation data for 3 orders
                    orderSet4,          # permutation data for 4 orders
                    orderSet5,          # permutation data for 5 orders
                    orderSetInd,        # columns for [pt0, pt[i], i0, i[i], a1, [i]]
                    realCombos,       # blank real points, which will be arranged in same orders as mock combos
                    tT,                 # c_travelTimes
                    sT,                 # c_startTimes      #   NOTE: the left list with the "c_"
                    eT,                 # c_endTimes        #   are indicies for keeping track of
                    odt,                # c_odtTimes        #   certain things in getBestCombo.
                    oMax,                 # c_MaxOrderToDeliveryTimes
                    tMax,                 # c_MaxTravelToLocTimes
                    tdd,                # c_tddTimes
                    ctm,                  # c_ctm (cumulative time marker)
                    rv_comboStartInfo,  # return for combo start info (cols = 14)
                    rv_bestCombo,       # return for eval single order of best combo (cols = 15)
                                                    # returns "o_res" format
                    rv_updatedBestCombo,        # return for individual order results (cols = 15)
                    rv_bestDG):            # return for group results (cols = 15)

    # /////
    delivery_scheduled = False
    f = '/Users/admin/SERVER2/BD_Scripts/RD/'
    if resume == True:
        order_q = pandas.read_csv(f+'order_q.txt', sep='\t')
        dg_pool = pandas.read_csv(f+'dg_pool.txt', sep='\t')
        oq = order_q.as_matrix()
        dgp = dg_pool.as_matrix()

        remaining_delivery_ids = order_q[order_q.deliveryNum==950].deliveryID.astype(int).tolist()
        all_orders = newOrders.T[4].astype(int).tolist()
        oq_orders = order_q.deliveryID.astype(int).tolist()

        for it in all_orders:
            if oq_orders.count(it) != 0:
                last_order_pt = all_orders.index(it)
                break

        newOrders = newOrders[last_order_pt:]

    # \\\\\

    ord_num = newOrders.shape[0]
    dgp_num = dgp.shape[0]
    dgp_cols = dgp.shape[1]
    oq_num = oq.shape[0]
    oq_cols = oq.shape[1]
    reorder_pt = 0

    # TODO: bestDG should not be limited to 5 orders ... if DG with max deliveries is being considered,
    # only the last four deliveries with the new delivery should be considered.

    if oq[0,3] == 0:
        next_oq_pt = 0
    else:
        next_oq_pt = oq_num - ord_num + 1

    for g in range(dgp_num):
        if dgp[g,3] == 0 and dgp[g,4] == 0:
            next_dgp_pt = g
            break

    for ord_i in range(ord_num):

        if ord_i != 0:
            next_oq_pt += 1

        deliveryID = newOrders[ord_i,4]
        now = newOrders[ord_i,5]

        x1 = newOrders[ord_i,6]
        y1 = newOrders[ord_i,7]
        x2 = newOrders[ord_i,8]
        y2 = newOrders[ord_i,9]
        x = c_abs(x2-x1)
        y = c_abs(y2-y1)
        toDel = sp*(x+y)

        dg_end = 0
        dg_grp_pt = 0
        # TODO: take dg_seg_size from function arguments
        while dg_end == 0:  # process groups of DG from the pool.  take the best of the first group with a best.

            dg_grp_s = dg_grp_pt * dg_seg_size
            dg_grp_e = (dg_grp_pt * dg_seg_size) + dg_seg_size
            dg_grp_pt += 1

            if dg_grp_e >= dgp_num:
                dg_grp_e = dgp_num-1
                dg_end = 1

            # for dgp_i in range(dg_grp_s,dg_grp_e):
            # ...
            # 1. how to handle when only single DG's left? --> breaks out of while loop and checks for best grp_i
            # 2.
            # if result, go with it, else next dgp_grp

            bestDG_var = 0
            rv_bestDG[0,3] = 0               # setup to ensure no result returns error for no result
            bestGrpDG_i = -1
            bestSoloDG_dgp_i = -1

            minTimeIncrease = 1600
            bestGrpDG_i_totalOrders = md
            bestGrpDG_i_currentDelivs = 0
            bestGrpDG_i_totalDelivs = 0
            bestDG_var = 0
            bestSoloDG_time = 0

            # -->> GET BEST DG IN GRP

            for dgp_i in range(dg_grp_s,dg_grp_e):
                complete = 0                # 0,2 --> no result;  # 1 --> process result

                dg_ID = dgp[dgp_i,0]
                dg_X = dgp[dgp_i,1]
                dg_Y = dgp[dgp_i,2]
                totalDelivs = dgp[dgp_i,3]

                st_oq_ind = -1
                started = 0
                g=-1
                currentDelivs = 0
                for oq_i in range(oq_num):
                    deliveryNum = oq[oq_i,3]
                    thisID = oq[oq_i,0]
                    if deliveryNum!=0 and thisID == dg_ID:
                        if started==0:
                            started = 1
                            st_oq_ind = oq_i
                        end_oq_ind = oq_i + 1       # keep index of last run
                        currentDelivs +=1
                        oq[oq_i,1] = dg_X                # update current location
                        oq[oq_i,2] = dg_Y
                        g = end_oq_ind - st_oq_ind
                    if started == 1 and g == dgp[dgp_i,4]: # g = currentDelivs
                        break

                dgp[dgp_i,4] = currentDelivs
                totalDG_orders = currentDelivs + totalDelivs
                if totalDG_orders==0:    # new DG
                    dg_end = 1
                    break

                deliveryCount = currentDelivs + 1
                r_o = 0

                # TODO: Need to bump this up to full md. But, first need to group DG evals.
                if currentDelivs+1 >= mdpp:         # if equal or more than allowed deliveries
                    complete = 2                    # signal for "Stop Eval This DG"

                else:                               # ... currentDelivs > 0

                    # get best combo from DG, if any, and keep if best
                    o = oq[st_oq_ind:end_oq_ind]
                    r_o = o.shape[0]

                    #----------------------------------------------------
                    #rv_comboStartInfo = get_combo_start_info(new,o,returnVar)

                    h=0     # h == index pt for order_q rows
                    k=0     # k == index pt for order_q cols
                    n=0
                    tripStartTime = 1000
                    for j in range(r_o):    # GOAL: identify where/when new trip will begin (in light of current trip)
                        s = o[j,9]       # prior order start time
                        e = o[j,10]      # prior order end time
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

                    if n==0:
                        rv_comboStartInfo[0,0] = now
                        rv_comboStartInfo[0,1] = newOrders[ord_i,6]    # tripPtX = start_X
                        rv_comboStartInfo[0,2] = newOrders[ord_i,7]    # tripPtY = start_Y
                        rv_comboStartInfo[0,5] = -1        # this signals an error -- rv_comboStartInfo[0,0] == -1
                        complete = 2

                    else:

                        rv_comboStartInfo[0,0] = tripStartTime
                        n = 7+k
                        s = o[h,n]
                        rv_comboStartInfo[0,1] = s         # tripPtX = start_X | end_X
                        n += 1
                        s = o[h,n]
                        rv_comboStartInfo[0,2] = s         # tripPtY = start_Y | end_Y

                        h = 0
                        for j in range(r_o):  # TODO: need to re-write so easier to understand and resolves arrangement issue

                            s = o[j,9]
                            e = o[j,10]
                            g = 1

                            # Note (1): When endTime==now, that point is not included in tripPoints.
                            #   BUT, that point is the basis for tripStartTime and tripStartPt.

                            # START LOCATION
                            if now < s and now < e:      # IF not start yet, use start point as start location

                                x1 = o[j,7]
                                y1 = o[j,8]
                                x2 = o[j,11]
                                y2 = o[j,12]

                            elif s <= now and now < e:   # ELIF, (already started | starting) & (ending now | ending later),
                                                                    #   use the end point as start location
                                x1 = o[j,11]
                                y1 = o[j,12]
                                x2 = o[j,11]
                                y2 = o[j,12]

                            else:

                                g = 0

                            if g == 1:

                                rv_comboStartInfo[h,3] = x1
                                rv_comboStartInfo[h,4] = y1
                                rv_comboStartInfo[h,5] = x2
                                rv_comboStartInfo[h,6] = y2

                                rv_comboStartInfo[h,7] = o[j,5]   # deliveryID
                                rv_comboStartInfo[h,8] = o[j,6]   # orderTime

                                h += 1

                        rv_comboStartInfo[h,3] = newOrders[ord_i,6]
                        rv_comboStartInfo[h,4] = newOrders[ord_i,7]
                        rv_comboStartInfo[h,5] = newOrders[ord_i,8]
                        rv_comboStartInfo[h,6] = newOrders[ord_i,9]

                        rv_comboStartInfo[h,7] = newOrders[ord_i,4]
                        rv_comboStartInfo[h,8] = newOrders[ord_i,5]

                    # rv_comboStartInfo = get_combo_start_info(new,o,returnVar)
                    #----------------------------------------------------

                    tripStartTime = rv_comboStartInfo[0,0]
                    tripStartPtX = rv_comboStartInfo[0,1]
                    tripStartPtY = rv_comboStartInfo[0,2]

                    # else --no error--
                    if rv_comboStartInfo[0,5] == -1:     # if error, then try single order eval

                        #----------------------------------------------------
                        # rv_updatedBestCombo = eval_single_order(new,o,tripStartPtX,tripStartPtY,tripStartTime,sp,md,returnVar)

                        x1 = tripStartPtX
                        y1 = tripStartPtY
                        x2 = newOrders[ord_i,6]
                        y2 = newOrders[ord_i,7]
                        x = c_abs(x2-x1)
                        y = c_abs(y2-y1)
                        toLoc = sp*(x+y)

                        if tripStartTime + toLoc + toDel <= md:

                            rv_updatedBestCombo[0,0] = dg_ID
                            rv_updatedBestCombo[0,1] = dg_X
                            rv_updatedBestCombo[0,2] = dg_Y
                            rv_updatedBestCombo[0,3] = 1           # deliveryNum
                            rv_updatedBestCombo[0,4] = toLoc
                            rv_updatedBestCombo[0,5] = newOrders[ord_i,4]      # deliveryID
                            t = newOrders[ord_i,5]
                            rv_updatedBestCombo[0,6] = t           # orderTime
                            rv_updatedBestCombo[0,7] = newOrders[ord_i,6]      # start_X
                            rv_updatedBestCombo[0,8] = newOrders[ord_i,7]      # start_Y
                            s = tripStartTime + toLoc
                            rv_updatedBestCombo[0,9] = s           # startTime
                            e = tripStartTime + toLoc + toDel
                            rv_updatedBestCombo[0,10] = e          # endTime
                            rv_updatedBestCombo[0,11] = newOrders[ord_i,8]     # end_X
                            rv_updatedBestCombo[0,12] = newOrders[ord_i,9]     # end_Y
                            rv_updatedBestCombo[0,13] = s - t      # totalOrderTime
                            rv_updatedBestCombo[0,14] = e - s      # travelTime

                        else:
                            rv_updatedBestCombo[0,13] = 0     # signals "No Result"

                        # rv_updatedBestCombo = eval_single_order(new,o,tripStartPtX,tripStartPtY,tripStartTime,sp,md,returnVar)
                        #----------------------------------------------------

                        n = rv_updatedBestCombo.shape[0]
                        if rv_updatedBestCombo[0,13] == 0:    # signal for "No Result"
                            complete = 2                # signal for "Stop Eval This DG"
                        else:
                            complete = 1                # signal for "Order Evaluated"

                    # elif no error, then complete remains 0

                if complete == 0:

                    k=0
                    for j in range(deliveryCount):
                        deliveryIDs[j] = rv_comboStartInfo[j,7]
                        orderTimes[j] = rv_comboStartInfo[j,8]
                        c_tripPoints[k,0] = rv_comboStartInfo[j,3]
                        c_tripPoints[k,1] = rv_comboStartInfo[j,4]
                        k += 1
                        c_tripPoints[k,0] = rv_comboStartInfo[j,5]
                        c_tripPoints[k,1] = rv_comboStartInfo[j,6]
                        k += 1

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
                        oq[0,0] = 450
                        oq[0,3] = 450
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

                    ptx0 =  tripPoints[0,0]
                    pty0 =  tripPoints[0,1]
                    ptx100 =  tripPoints[1,0]
                    pty100 =  tripPoints[1,1]

                    ptx1 =  tripPoints[2,0]
                    pty1 =  tripPoints[2,1]
                    ptx101 =  tripPoints[3,0]
                    pty101 =  tripPoints[3,1]

                    if deliveryCount >= 3:
                        ptx2 =  tripPoints[4,0]
                        pty2 =  tripPoints[4,1]
                        ptx102 =  tripPoints[5,0]
                        pty102 =  tripPoints[5,1]
                    if deliveryCount >= 4:
                        ptx3 =  tripPoints[6,0]
                        pty3 =  tripPoints[6,1]
                        ptx103 =  tripPoints[7,0]
                        pty103 =  tripPoints[7,1]
                    if deliveryCount >= 5:
                        ptx4 =  tripPoints[8,0]
                        pty4 =  tripPoints[8,1]
                        ptx104 =  tripPoints[9,0]
                        pty104 =  tripPoints[9,1]
                    if deliveryCount >= 6:
                        ptx5 =  tripPoints[10,0]
                        pty5 =  tripPoints[10,1]
                        ptx105 =  tripPoints[11,0]
                        pty105 =  tripPoints[11,1]
                    if deliveryCount >= 7:
                        ptx6 =  tripPoints[12,0]
                        pty6 =  tripPoints[12,1]
                        ptx106 =  tripPoints[13,0]
                        pty106 =  tripPoints[13,1]
                    if deliveryCount >= 8:
                        ptx7 =  tripPoints[14,0]
                        pty7 =  tripPoints[14,1]
                        ptx107 =  tripPoints[15,0]
                        pty107 =  tripPoints[15,1]

                    for j in range(pts):
                        for k in range(r_mc):
                            mpt = mockCombos[k,j]
                            if mpt == 0:
                                tmp_realCombos[k,j,0] = ptx0
                                tmp_realCombos[k,j,1] = pty0
                            elif mpt == 100:
                                tmp_realCombos[k,j,0] = ptx100
                                tmp_realCombos[k,j,1] = pty100
                            elif mpt == 1:
                                tmp_realCombos[k,j,0] = ptx1
                                tmp_realCombos[k,j,1] = pty1
                            elif mpt == 101:
                                tmp_realCombos[k,j,0] = ptx101
                                tmp_realCombos[k,j,1] = pty101
                            elif mpt == 2:
                                tmp_realCombos[k,j,0] = ptx2
                                tmp_realCombos[k,j,1] = pty2
                            elif mpt == 102:
                                tmp_realCombos[k,j,0] = ptx102
                                tmp_realCombos[k,j,1] = pty102
                            elif mpt == 3:
                                tmp_realCombos[k,j,0] = ptx3
                                tmp_realCombos[k,j,1] = pty3
                            elif mpt == 103:
                                tmp_realCombos[k,j,0] = ptx103
                                tmp_realCombos[k,j,1] = pty103
                            elif mpt == 4:
                                tmp_realCombos[k,j,0] = ptx4
                                tmp_realCombos[k,j,1] = pty4
                            elif mpt == 104:
                                tmp_realCombos[k,j,0] = ptx104
                                tmp_realCombos[k,j,1] = pty104
                            elif mpt == 5:
                                tmp_realCombos[k,j,0] = ptx5
                                tmp_realCombos[k,j,1] = pty5
                            elif mpt == 105:
                                tmp_realCombos[k,j,0] = ptx105
                                tmp_realCombos[k,j,1] = pty105
                            elif mpt == 6:
                                tmp_realCombos[k,j,0] = ptx6
                                tmp_realCombos[k,j,1] = pty6
                            elif mpt == 106:
                                tmp_realCombos[k,j,0] = ptx106
                                tmp_realCombos[k,j,1] = pty106
                            elif mpt == 7:
                                tmp_realCombos[k,j,0] = ptx7
                                tmp_realCombos[k,j,1] = pty7
                            elif mpt == 107:
                                tmp_realCombos[k,j,0] = ptx107
                                tmp_realCombos[k,j,1] = pty107

                    # realCombos = c_mapper(tripPoints, mockCombos,tmp_realCombos)
                    #----------------------------------------------------

                    #----------------------------------------------------
                    # rv_bestCombo = get_best_combo(tripStartPtX,  # returns "o_res" format
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
                            if j == 0:
                                xptb = tmp_realCombos[k,j,0]
                                yptb = tmp_realCombos[k,j,1]
                                x = c_abs( tripStartPtX - xptb )
                                y = c_abs( tripStartPtY - yptb )
                                t = sp * ( x + y )
                                ctm[k] = t
                                tT[k,j] = t
                                tMax[k] = t
                            else:
                                xpta = tmp_realCombos[k,j-1,0]
                                ypta = tmp_realCombos[k,j-1,1]
                                xptb = tmp_realCombos[k,j,0]
                                yptb = tmp_realCombos[k,j,1]
                                x = c_abs( xpta - xptb )
                                y = c_abs( ypta - yptb )
                                t = sp * ( x + y )
                                ctm[k] += t
                                tT[k,j] = t
                                if t > tMax[k]:
                                    tMax[k] = t

                            mc_pt = mockCombos[k,j]
                            if mc_pt < 100: sT[k,mc_pt] = ctm[k] + tripStartTime
                            else: eT[k,mc_pt-100] = ctm[k] + tripStartTime

                            if j == pts-1 and tMax[k] <= mttlt: # this is the last part of the 2D iteration
                                                                        # if max travelToLoc time is acceptable --> find Best Index
                                oMax[k] = 0
                                for n in range(deliveryCount):
                                    orderSK_pt = orderSK[k,n]
                                    eT_pt = eT[k,orderSK_pt]
                                    tdd[k,orderSK_pt] = eT_pt - sT[k,orderSK_pt]
                                    odt_pt = eT_pt - orderTimes[orderSK_pt]
                                    odt[k,orderSK_pt] = odt_pt
                                    if odt_pt > oMax[k]:
                                        oMax[k] = odt_pt              # update max order-to-delivery time [ per row ] -- keeping biggest value

                                if oMax[k] != 0 and oMax[k] <= md: # if order-to-delivery max is valid and acceptable
                                    if ctm[k] < minT:                 # for all acceptable rows, keep one with lowest cumul. time.
                                        minT = ctm[k]
                                        BI = k                        # setting Best Index

                    if minT == 8 * md:
                        rv_bestCombo[0,13] = 0                      # interpretted on return as an error
                        rv_bestCombo[1,13] = BI
                    elif BI == r_mc + 1:
                        rv_bestCombo[0,13] = 0                      # interpretted on return as an error
                        rv_bestCombo[1,13] = 505                    # interpretted on return as "error setting best index"
                    else:
                        for g in range(deliveryCount):                              # DEFINITION:
                            orderSK_pt=orderSK[BI,g]
                            rv_bestCombo[g,0] = tripStartPtX                      # dg_X
                            rv_bestCombo[g,1] = tripStartPtY                      # dg_Y
                            rv_bestCombo[g,2] = orderSK_pt + 1                    # deliveryNum (starts at zero)
                            rv_bestCombo[g,3] = deliveryIDs[orderSK_pt]           # deliveryID (already sorted by key)
                            rv_bestCombo[g,4] = orderTimes[orderSK_pt]            # orderTime
                            mc_pt = pointSK[BI,orderSK_pt*2]
                            rv_bestCombo[g,5] = tT[BI,mc_pt]                      # travelTimeToLoc
                            rv_bestCombo[g,6] = tmp_realCombos[BI,mc_pt,0]        # startX // see below for explanation
                            rv_bestCombo[g,7] = tmp_realCombos[BI,mc_pt,1]        # startY
                            rv_bestCombo[g,8] = sT[BI,orderSK_pt]                 # startTime
                            rv_bestCombo[g,9] = tdd[BI,orderSK_pt]                # travelTime
                            rv_bestCombo[g,10]= eT[BI,orderSK_pt]                 # endTime
                            mc_pt=pointSK[BI,(orderSK_pt*2)+1]
                            rv_bestCombo[g,11]= tmp_realCombos[BI,mc_pt,0]        # endX
                            rv_bestCombo[g,12]= tmp_realCombos[BI,mc_pt,1]        # endY
                            rv_bestCombo[g,13]= odt[BI,orderSK_pt]                # totalOrderTime
                            rv_bestCombo[g,14]= BI

                    # rv_bestCombo = get_best_combo(tripStartPtX,...  # returns "o_res" format
                    #----------------------------------------------------

                    if rv_bestCombo[0,13] != 0:                 # (general error | error setting best index)

                        # TODO: NEED TO ALSO CHANGE FORMAT
                        #
                        # SHOULD PASTE ALL VALUES IN BEST DG HERE IF THAT IS THE CASE
                        #
                        #----------------------------------------------------
                        # rv_bestCombo = update_order_results(o,rv_bestCombo,now) # expects "o_res" input // returns "o_res" format

                        r_res = rv_bestCombo.shape[0]
                        # iterate through o_res to replace info with static order info
                        for j in range(r_o):
                            if o[j,9] <= now and o[j,10] > now:  # if then they are static orders...
                                # use deliveryID to temp. use deliveryNum column in "o_res" as an index to "o"
                                d = o[j,5]               # order deliveryID
                                for k in range(r_res):
                                    c = rv_bestCombo[k,3]           # order result deliveryID
                                    if c == d:          # if order deliveryID matches order results deliveryID ...
                                        rv_bestCombo[k,5] = o[j,4]   # travelTimeToLoc
                                        rv_bestCombo[k,4] = o[j,6]   # orderTime
                                        rv_bestCombo[k,6] = o[j,7]   # start_X
                                        rv_bestCombo[k,7] = o[j,8]   # start_Y
                                        rv_bestCombo[k,8] = o[j,9]   # startTime
                                        if rv_bestCombo[k,11] == tripStartPtX and rv_bestCombo[k,12] == tripStartPtY:
                                            rv_bestCombo[k,10] = o[j,10]   # endTime IF used as starting point.
                                        break                 # only one point can be a starting point

                        # rv_bestCombo = update_order_results(o,rv_bestCombo,now) # expects "o_res" input // returns "o_res" format
                        #----------------------------------------------------

                        # update result with additional vars and different format
                        # rv_updatedBestCombo in "oq"/"o" format
                        # rv_bestCombo in "o_res" format

                        for g in range(deliveryCount):
                            rv_updatedBestCombo[g,0] = dg_ID
                            rv_updatedBestCombo[g,1] = dg_X
                            rv_updatedBestCombo[g,2] = dg_Y
                            rv_updatedBestCombo[g,3] = rv_bestCombo[g,2]             # deliveryNum
                            rv_updatedBestCombo[g,4] = rv_bestCombo[g,5]             # travelTimeToLocation
                            rv_updatedBestCombo[g,5] = rv_bestCombo[g,3]             # deliveryID
                            rv_updatedBestCombo[g,6] = rv_bestCombo[g,4]             # orderTime
                            rv_updatedBestCombo[g,7] = rv_bestCombo[g,6]             # start_X
                            rv_updatedBestCombo[g,8] = rv_bestCombo[g,7]             # start_Y
                            rv_updatedBestCombo[g,9] = rv_bestCombo[g,8]             # startTime
                            rv_updatedBestCombo[g,10] = rv_bestCombo[g,10]           # endTime
                            rv_updatedBestCombo[g,11] = rv_bestCombo[g,11]           # end_X
                            rv_updatedBestCombo[g,12] = rv_bestCombo[g,12]           # end_Y
                            rv_updatedBestCombo[g,13] = rv_bestCombo[g,13]           # totalOrderTime
                            rv_updatedBestCombo[g,14] = rv_bestCombo[g,9]            # travelTime
                        complete = 1

                if complete == 1:
                    # checkVar = (order_result.endTime.max() - order_result.startTime.min()) - (order_q_i.endTime.max() - order_q_i.startTime.min())
                    # TODO: how can this be setup to account for travelTimeToLoc for fresh DGs??
                    # checkVar = ( e2 - s2 ) - ( e1 - s1 )

                    # assuming there DG is already scheduled for an order ...
                    # need to find the max/min for this result and compare with previous result
                    # current result
                    e2 = rv_updatedBestCombo[0,10]
                    s2 = rv_updatedBestCombo[0,9]

                    # older result
                    e1 = o[0,10]
                    s1 = o[0,9]
                    for j in range(1,deliveryCount):
                        s = rv_updatedBestCombo[j,9]
                        e = rv_updatedBestCombo[j,10]
                        if e > e2:
                            e2 = e      # min of current result
                        if s < s2:
                            s2 = s

                        ## ------------- //
                        if j != deliveryCount-1:
                            s = o[j,9]
                            e = o[j,10]
                            if e > e1:
                                e1 = e  # min of older result
                            if s < s1:
                                s1 = s
                        ## // -------------

                    timeDiff = (e2-s2) - (e1-s1)
                    if timeDiff <= minTimeIncrease:

                        if totalDG_orders < bestGrpDG_i_totalOrders:

                            minTimeIncrease = timeDiff
                            bestGrpDG_i_totalOrders = totalDG_orders
                            bestGrpDG_i = dgp_i

                            rv_bestDG[:deliveryCount] = rv_updatedBestCombo[:deliveryCount]
                            rv_bestDG[deliveryCount:] = 0

            if bestGrpDG_i != -1 or dg_end == 1:
                dg_end = 1
                break

        if bestGrpDG_i == -1:

            for new_dg_i in range(next_dgp_pt,dgp_num):
                x1 = dgp[new_dg_i,1]
                y1 = dgp[new_dg_i,2]
                x2 = newOrders[ord_i,6]
                y2 = newOrders[ord_i,7]
                x = c_abs(x2-x1)
                y = c_abs(y2-y1)
                toLoc = sp*(x+y)        # dg_pool loc to vendor
                totalTravTime = toLoc + toDel
                if toLoc <= mttlt and totalTravTime <= md:
                    # check to see if best solo, and save if so
                    if bestSoloDG_time == 0 or totalTravTime < bestSoloDG_time:
                        bestSoloDG_time = totalTravTime
                        bestSoloDG_dgp_i = new_dg_i


        #
        # --------------
        # --------------
        #

        # rv_bestDG is the best DG from DG Queue
        # bestSoloDG_dgp_i points to best DG from DG Pool
        # 950 means re-pool necessary

        if bestGrpDG_i == -1 and bestSoloDG_dgp_i == -1:            # A:    need to re-pool ...

            reorder_q[reorder_pt] = newOrders[ord_i,4]              # deliveryID
            reorder_pt += 1
            next_oq_pt -= 1     # this offsets the expected addition
            # print 'updated reorder pt'

        elif bestGrpDG_i == -1 and bestSoloDG_dgp_i != -1:          # B:    use new dg

            # in both cases, setup update for dg_pool
            dgp_i = bestSoloDG_dgp_i
            dg_ID = dgp[dgp_i,0]
            dgp[dgp_i,4] = 1
            deliveryCount = 1
            next_dgp_pt += 1

            oq_s_pt = oq_num
            for oq_i in range(oq_num):
                if oq[oq_i,3] == 0:
                    if next_oq_pt == 0:
                        oq_s_pt = 0
                    break
                thisID = oq[oq_i,0]
                if thisID < dg_ID:
                    oq_s_pt = oq_i+1        # the row before DG's orders (in the queue)
                else:
                    break

            if oq[0,3] == 0 or dg_ID <= oq[0,0]:            # is newOrder at TOP ?
                g = 0
                oq_b[1:next_oq_pt+1] = oq[0:next_oq_pt]
            else:
                oq_b[0:oq_s_pt] = oq[0:oq_s_pt]
                g = oq_s_pt
                oq_b[oq_s_pt+1:next_oq_pt] = oq[oq_s_pt:next_oq_pt-1]

            oq_b[g,0] = dg_ID                       # id
            oq_b[g,1] = dgp[dgp_i,1]                # dg_X
            oq_b[g,2] = dgp[dgp_i,2]                # dg_Y
            oq_b[g,3] = 1                           # deliveryNum
            oq_b[g,4] = bestSoloDG_time - toDel     # travel time to location
            oq_b[g,5] = newOrders[ord_i,4]          # deliveryID
            oq_b[g,6] = newOrders[ord_i,5]          # orderTime
            oq_b[g,7] = newOrders[ord_i,1]          # start X
            oq_b[g,8] = newOrders[ord_i,2]          # start Y
            oq_b[g,9] = oq_b[g,6] + oq_b[g,4]       # startTime
            oq_b[g,10] = oq_b[g,9] + toDel          # endTime
            oq_b[g,11] = newOrders[ord_i,8]         # end X
            oq_b[g,12] = newOrders[ord_i,9]         # end Y
            oq_b[g,13] = bestSoloDG_time            # total order time
            oq_b[g,14] = toDel                      # travel time

        elif bestGrpDG_i != -1:                                         # C:    use bestDG from previous calculations

            # as before, setup update for dg_pool
            dgp_i = bestGrpDG_i
            dg_ID = dgp[dgp_i,0]
            deliveryCount = dgp[dgp_i,4] + 1
            dgp[dgp_i,4] = deliveryCount

            oq_s_pt = oq_num
            for oq_i in range(oq_num):
                if oq[oq_i,3] == 0:
                    break
                thisID = oq[oq_i,0]
                if thisID < dg_ID:
                    oq_s_pt = oq_i+1        # the row before DG's orders (in the queue)
                else:
                    break

            if dg_ID <= oq[0,0]:                                    # is newOrder at TOP ?
                oq_b[0:deliveryCount] = rv_bestDG[0:deliveryCount]
                oq_b[deliveryCount:next_oq_pt+1] = oq[deliveryCount-1:next_oq_pt]
            elif oq[0,0] < dg_ID < oq[next_oq_pt-1,0]:              # is newOrder in MIDDLE ?
                oq_b[0:oq_s_pt] = oq[0:oq_s_pt]                                                     # top
                oq_b[oq_s_pt:oq_s_pt+deliveryCount] = rv_bestDG[0:deliveryCount]                    # middle
                oq_b[oq_s_pt+deliveryCount:next_oq_pt-1] = oq[oq_s_pt+deliveryCount+1:next_oq_pt]   # bottom
            elif dg_ID >= oq[next_oq_pt-1,0]:                       # is newOrder at BOTTOM ?
                oq_b[0:oq_s_pt] = oq[0:oq_s_pt]                                                     # top
                oq_b[oq_s_pt:oq_s_pt+deliveryCount] = rv_bestDG[0:deliveryCount]                    # middle
                oq_b[oq_s_pt+deliveryCount:next_oq_pt] = oq[oq_s_pt+deliveryCount-1:next_oq_pt-1]


            if dgp[dgp_i,0]==45:
                print oq_b
                systemError()

        if next_oq_pt+1 > oq_num:
            last_order_pt = next_oq_pt
        else:
            last_order_pt = next_oq_pt + 1
        for oq_i in range(last_order_pt):
            oq[oq_i] = oq_b[oq_i]
        if deliveryID == 8006:
            return oq
        # SECOND --> UPDATE DG POOL ORDER (needs to go last because updating effect dgp_i)
        total = dgp[dgp_i,4] + dgp[dgp_i,3]
        for i in range(dgp_num):
            thisID = dgp[i,0]
            if thisID != dg_ID:
                thisCurrentDeliv = dgp[i,4]
                thisTotalDelivs = dgp[i,3]
                thisTotal = thisCurrentDeliv + thisTotalDelivs
                if thisTotal > total or thisTotal == 0:
                    g = i
                    break

        # if g == dgp_i: pass
        if g==0:
            dgp_b[0:1] = dgp[dgp_i:dgp_i+1]
            dgp_b[1:dgp_i+1] = dgp[0:dgp_i]
            dgp_b[dgp_i+1:] = dgp[dgp_i+1:]
        elif g < dgp_i:             # if insert is above changed DG, e.g., DG moves from zero to 1 currentDeliv
            n = dgp_i - g
            dgp_b[dgp_i+1:] = dgp[dgp_i+1:]
            dgp_b[g+1:g+1+n] = dgp[g:g+n]
            dgp_b[g:g+1] = dgp[dgp_i:dgp_i+1]
            dgp_b[0:g] = dgp[0:g]
        elif dgp_i < g:             # if insert is below changed DG, e.g., DG moves from 1 to 2 currentDeliv
            n = g - dgp_i
            dgp_b[0:dgp_i] = dgp[0:dgp_i]
            dgp_b[dgp_i:dgp_i+n-1] = dgp[dgp_i+1:dgp_i+n]
            dgp_b[dgp_i+n-1:dgp_i+n] = dgp[dgp_i:dgp_i+1]
            dgp_b[dgp_i+n:] = dgp[dgp_i+n:]

        for i in range(dgp_num):
            dgp[i:i+1] = dgp_b[i:i+1]

        # /////

        # if ord_i != 0 and save==True and ord_i<10:
        #     order_q = oq_to_order_q(oq,showVar=False)
        #     order_q.to_csv(f+'order_q.txt', index=False, header=True, sep='\t')
        #     dgp_cols = ['id', 'dg_X', 'dg_Y', 'totalDelivered', 'currentDeliveries']
        #     dg_pool = pandas.DataFrame(dgp,columns=dgp_cols)
        #     dg_pool.to_csv(f+'dg_pool.txt', index=False, header=True, sep='\t')

        # \\\\\

        # for oq_i in range(oq_num):
        #     if oq[oq_i,0]==0:
        #         if oq_i != next_oq_pt:
        #             print 'issue with oq point'
        #             systemError()
        #         break
        deliv_ids = oq[:next_oq_pt].T[5].astype(int).tolist()
        deliv_id_dict = dict(zip(deliv_ids,range(0,len(deliv_ids))))
        if len(deliv_ids) != len(deliv_id_dict.keys()):
            print '\nerror with deliv IDs\n\n'
            print oq
            print dgp
            systemError()
        if deliveryID==8134:
            delivery_scheduled=True
    #
    #
    #
    # if reorder_pt != 0:
    #     for oq_i in range(reorder_pt):
    #         oq[next_oq_pt,3] = 950
    #         oq[next_oq_pt,5] = reorder_q[oq_i]
    #         next_oq_pt += 1
    #     order_q = oq_to_order_q(oq,showVar=False)
    #     order_q.to_csv(f+'order_q.txt', index=False, header=True, sep='\t')
    #     dgp_cols = ['id', 'dg_X', 'dg_Y', 'totalDelivered', 'currentDeliveries']
    #     dg_pool = pandas.DataFrame(dgp,columns=dgp_cols)
    #     dg_pool.to_csv(f+'dg_pool.txt', index=False, header=True, sep='\t')
    #     print 'saved to:',f+'order_q.txt'

    return oq