
#@profile
def N_getBestDG(    new,
                    o_grp,              # group of order_q_i
                    dg_grp_ids,         # unique IDs for groups
                    dg_grp,             # DGs to analyze. (last DG is 'free DG')
                    p1_arr,             # p1_arr and p2 are pairs for all route point pairs
                    p2_arr,
                    dg_id_arr,          # p1/p2 are separated by DG
                    minutes,            # time between p1 and p2
                    deliveryIDs,        # delivery IDs
                    orderTimes,         # order times
                    md,                 # max delivery time
                    mttlt,              # max time to delivery locations
                    c_tripPoints,       # empty trip points array
                    ptPairSet,
                    tmp_minutes,        # temporary minutes array to match with ptPairSet
                    orderSet2,          # permutation data for 2 orders
                    orderSet3,          # permutation data for 2 orders
                    orderSet4,          # permutation data for 2 orders
                    orderSet5,          # permutation data for 2 orders
                    orderSetInd,        # columns for [pt0, pt[i], i0, i[i], a1, [i]]
                    realCombos,         # blank real points, which will be arranged in same orders as mock combos
                    tT,                 # c_travelTimes
                    sT,                 # c_startTimes      #   NOTE: the left list with the "c_"
                    eT,                 # c_endTimes        #   are indicies for keeping track of
                    odt,                # c_odtTimes        #   certain things in getBestCombo.
                    oMax,               # c_MaxOrderToDeliveryTimes
                    tMax,               # c_MaxTravelToLocTimes
                    tdd,                # c_tddTimes
                    ctm,                # c_ctm (cumulative time marker)
                    returnVar1,         # temporary returnVar (used for combo_start_info)
                    returnVar_i,        # another temp. returnVar (used as placeholder for potential bestDG
                    returnVar):         # primary returnVar, which may or may not be used

    o_grp_num       = dg_grp_ids.shape[0]
    o_grp_rows      = o_grp.shape[0]
    o_grp_s_pt      = 0
    o_grp_e_pt      = 0
    t_grp_rows      = dg_id_arr.shape[0]
    t_grp_s_pt      = 0
    t_grp_e_pt      = 0
    NOW             = new[0]
    new_DG          = 0
    added_cost      = md*2
    found_a_dg      = 0
    returnVar[0][0] = -1           # default is error in case returned

    # iterate through each DG (w/ DG's current orders)
    for i in range(o_grp_num):
        complete    = 0            # 0,2 --> no result, 1 --> process result
        orderCount  = 0
        currentID   = dg_grp_ids[i]
        currentDG   = dg_grp[i]

        o_grp_s_pt = o_grp_e_pt
        if o_grp_s_pt == o_grp_rows:
            new_DG = 1
        else:
            # get current group of orders (for currentDG)
            for j in range(o_grp_s_pt,o_grp_rows):
                grp_row         = o_grp[j]
                orderCount     += 1
                o_grp_e_pt      = j
                if grp_row[2] != currentID:
                    break
                elif dg_id_arr[j] == currentID and j==o_grp_rows-1:
                    break

            # get current group of travel times b/t nodes
            t_grp_s_pt = t_grp_e_pt
            for j in range(t_grp_s_pt,t_grp_rows):
                if dg_id_arr[j] != currentID:
                    t_grp_e_pt  = j
                    break
                elif dg_id_arr[j] == currentID and j==t_grp_rows-1:
                    t_grp_e_pt  = j+1
                    break

        o   = o_grp[o_grp_s_pt:o_grp_e_pt]
        r_o = o.shape[0]
        r_t = t_grp_e_pt - t_grp_s_pt
        deliveryCount = orderCount+1
        aii = returnVar1[:deliveryCount]

        #----------------------------------------------------
        #comboStartInfoReturn = get_combo_start_info(new,o,aii)

        #import pdb; pdb.set_trace()

        h=0
        k=0
        n=0
        tripStartTime = 1000
        for j in range(r_o):
            dj = o[j]
            s  = dj[6]                  # start time
            e  = dj[8]                  # end time
            if e > NOW:                 # Is there at least one order with an endTime less than now?
                n=1                     #       If not, then return for single order
            if 0 < s-NOW < tripStartTime-NOW:    # changed to ">=" due to case where two orders
                tripStartTime = s
                h=j                 # h == index pt for order_q rows
                k=5                 # k == index pt for whether last point is/was ( startPt | endPt )
            # if t==endTime, it is too late to change DG's next destination
            if 0 < e-NOW < tripStartTime-NOW:
                tripStartTime = e
                h=j
                k=9

        dj = aii[0]
        if n==0:
            dj[0]       = NOW
            dj[1]       = new[2]        # tripStartPt
            dj[2]       = -1            # this signals an error
            new_DG   = 1
        else:
            dh      = o[h]
            dj[0]   = tripStartTime
            st_pt   = dh[k]
            dj[1]   = st_pt         # tripPtA = (start_A | end_A)

            n = 0
            h = 0
            k = 0
            for j in range(r_o):
                dj  = o[j]
                s   = dj[6]         # start time
                e   = dj[8]         # end time
                g   = 1

                if NOW < s and NOW < e:      # IF not start yet, use start point as start location
                    p1 = dj[5]
                    p2 = dj[9]
                elif s <= NOW and NOW < e:   # ELIF, (already started | starting) & (ending now | ending later),
                    p1 = dj[9]
                    p2 = dj[9]
                else:
                    g  = 0

                if g == 1:
                    dh    = aii[h]      # combo_start_info_return_var
                    dh[4] = dj[1]       # deliveryID from o[j]
                    dh[5] = dj[0]       # orderTime from o[j]
                    h    += 1

                    dk    = aii[k]
                    k    += 1
                    v     = n+2
                    dk[v] = p1
                    v    += 1
                    dk[v] = p2
                    if k == deliveryCount:
                        k = 0
                        n = 2

            dh      = aii[h]            # Note: ak[0] (tripStartTime) / ak[1] (tripStartPt): only provided in first row
            dh[2]   = new[2]            # start_node
            dh[3]   = new[3]            # end_node
            dh[4]   = new[1]            # deliv_id
            dh[5]   = new[0]            # orderTime

        comboStartInfoReturn = aii      # [0]   tripStartTime
                                        # [1]   tripStartPt
                                        # [2]   tripPtA
                                        # [3]   tripPtB
                                        # [4]   deliveryID
                                        # [5]   orderTime

        # comboStartInfoReturn = get_combo_start_info(new,o,aii)
        #----------------------------------------------------

        dj              = comboStartInfoReturn[0]
        tripStartTime   = dj[0]
        tripStartPt     = dj[1]

        #import pdb; pdb.set_trace()

        if new_DG == 1:

            #----------------------------------------------------
            # rv_i = eval_single_order(new,o,tripStartPt,tripStartTime,sp,md,aii)

            # bi      = returnVar[current_res_row]
            dbi      = returnVar[0]

            dbi[0]   = dj[0]                 # order_time
            dbi[1]   = new[1]                # deliv_id
            dbi[2]   = currentDG[0]          # dg_id
            dbi[3]   = currentDG[1]          # dg_node
            dbi[4]   = currentDG[3]          # travel_to_loc_time
            dbi[5]   = new[2]                # start_node
            dbi[6]   = dbi[0] + currentDG[3]  # order_time + travel_to_loc_time = start_time
            dbi[7]   = currentDG[4]          # travel_time
            dbi[8]   = dbi[0] + currentDG[5]  # order_time + total_travel_time = end_time
            dbi[9]   = new[3]                # end_node
            dbi[10]  = 0.0                     # total_order_time
            dbi[11]  = 99.0                    # best_index

            return returnVar[:1]    #current_res_row+1]

            # rv_i = eval_single_order(new,o,tripStartPtX,tripStartPtY,tripStartTime,sp,md,aii)
            #----------------------------------------------------

        current_cost = o[orderCount-1][8] - tripStartTime
        if complete == 0:

            k=-1
            for j in range(deliveryCount):
                di              = comboStartInfoReturn[j]
                deliveryIDs[j]  = di[4]
                orderTimes[j]   = di[5]
                if j>k: k=j
                c_tripPoints[k] = di[2]             # tripPtA
                k+=1
                c_tripPoints[k] = di[3]             # tripPtB
                k+=1

            tripPoints  = c_tripPoints[:deliveryCount*2]

            if deliveryCount==2:
                testSet=orderSet2
                ai = orderSetInd[0]
            if deliveryCount==3:
                testSet=orderSet3
                ai = orderSetInd[1]
            if deliveryCount==4:
                testSet=orderSet4
                ai = orderSetInd[2]
            if deliveryCount==5:
                testSet=orderSet5
                ai = orderSetInd[3]

            bii         = testSet.T             # real ugly these few line.
            cii         = bii[ai[0]:ai[1]]      # orderSK and pointSK are key.
            mockCombos  = cii.T                 # they provide means to circle back to best DG upon calc. conclusion.
            r_mc        = mockCombos.shape[0]   # this mess extracts index keys.
            cii         = bii[ai[2]:ai[3]]
            orderSK     = cii.T                 # Order Sort Key: provides sort-order of delivery-order in permutation
            cii         = bii[ai[4]:ai[5]]
            pointSK     = cii.T                 # Point Sort Key: provides index for [A1,A2,B1,B2...etc] in permutation

            cii         = bii[ai[6]:ai[7]]      # Point Pair Sort Key: provides index (to ptPairSet) for each segment
            ptPairSK    = cii.T                 #                       [A1-A2,A2-B1,etc..]
            ptPairSetCnt= ai[9]
                                                # PtPair Set SK:
            ptPairSetSK = ptPairSet[:ptPairSetCnt]
            ptMinutes   = tmp_minutes[:ptPairSetCnt]

            #----------------------------------------------------
            # map minutes to applicable ptPairSet
            for j in range(ptPairSetCnt):
                # try:
                ptA,ptB             = tripPoints[ptPairSetSK[j]]
                # except:
                #     print 'line 257'
                #     import embed_ipython as I; I.embed()
                if ptA==ptB:
                    ptMinutes[j]    = 0
                else:
                    for k in range(r_t):
                        _ptA        = p1_arr[k]
                        _ptB        = p2_arr[k]
                        if (ptA==_ptA and ptB==_ptB) or (ptA==_ptB and ptB==_ptA):
                            ptMinutes[j] = minutes[k]
                            break
            # RESULT:  sum( ptMinutes[ptPairSK[0]] ) = travel time for route[0]
            #----------------------------------------------------


            #----------------------------------------------------
            # realCombos = c_mapper(tripPoints, mockCombos,tmp_realCombos)

            tmp_realCombos  = realCombos[:r_mc]
            dj              = tripPoints
            pt0             = dj[0]
            pt100           = dj[1]
            pt1             = dj[2]
            pt101           = dj[3]
            if deliveryCount >= 3:
                pt2         = dj[4]
                pt102       = dj[5]
            if deliveryCount >= 4:
                pt3         = dj[6]
                pt103       = dj[7]
            if deliveryCount >= 5:
                pt4         = dj[8]
                pt104       = dj[9]
            if deliveryCount >= 6:
                pt5         = dj[10]
                pt105       = dj[11]
            if deliveryCount >= 7:
                pt6         = dj[12]
                pt106       = dj[13]
            if deliveryCount >= 8:
                pt7         = dj[14]
                pt107       = dj[15]

            # realCombos = c_mapper(tripPoints, mockCombos,tmp_realCombos)
            #----------------------------------------------------

            #----------------------------------------------------
            # bestComboReturn

            BI              = r_mc + 1
            minT            = (8 * md)      # minimum total route time (assuming 8 routes is max route #)
            tmp_returnVar   = returnVar[:deliveryCount]

            #import pdb; pdb.set_trace()
            #import embed_ipython as I; I.i_trace()
            #import embed_ipython as I; I.embed()

            ajj                     = ptPairSK.T
            pts                     = mockCombos.shape[1]
            for j in range(pts):                # columns

                if j!=0:
                    tj              = ajj[j-1]
                    tk              = ptMinutes[tj]

                for k in range(r_mc):           # rows

                    #----------------------------------------------------
                    # map realCombos from mockCombos
                    mpt = mockCombos[k][j]
                    dk = tmp_realCombos[k]
                    if mpt == 0:
                        dk[j] = pt0
                    elif mpt == 100:
                        dk[j] = pt100
                    elif mpt == 1:
                        dk[j] = pt1
                    elif mpt == 101:
                        dk[j] = pt101
                    elif mpt == 2:
                        dk[j] = pt2
                    elif mpt == 102:
                        dk[j] = pt102
                    elif mpt == 3:
                        dk[j] = pt3
                    elif mpt == 103:
                        dk[j] = pt103
                    elif mpt == 4:
                        dk[j] = pt4
                    elif mpt == 104:
                        dk[j] = pt104
                    elif mpt == 5:
                        dk[j] = pt5
                    elif mpt == 105:
                        dk[j] = pt105
                    elif mpt == 6:
                        dk[j] = pt6
                    elif mpt == 106:
                        dk[j] = pt106
                    elif mpt == 7:
                        dk[j] = pt7
                    elif mpt == 107:
                        dk[j] = pt107
                    #----------------------------------------------------

                    if j == 0:
                        ctm[k]      = tripStartTime
                    else:
                        t           = tk[k]
                        ctm[k]     += t
                        tT[k][j]    = t
                        if t > tMax[k]:
                            tMax[k] = t

                    mc_pt = mockCombos[k][j]
                    if mc_pt < 100:
                        sT[k][mc_pt]    = ctm[k]
                    else:
                        eT[k][mc_pt-100]= ctm[k]
                    if j == pts-1 and tMax[k] <= mttlt:         # this is the last part of the 2D iteration
                                                                # if max travelToLoc time is acceptable --> find Best Index
                        oMax[k] = 0
                        for n in range(deliveryCount):
                            orderSK_pt          = orderSK[k][n]
                            eT_pt               = eT[k][orderSK_pt]
                            tdd[k][orderSK_pt]  = eT_pt - sT[k][orderSK_pt]
                            odt_pt              = eT_pt - orderTimes[orderSK_pt]
                            odt[k][orderSK_pt]  = odt_pt
                            if odt_pt > oMax[k]:
                                oMax[k] = odt_pt                # update max order-to-delivery time [ per row ] -- keeping biggest value
                        if oMax[k] != 0 and oMax[k] <= md:      # if order-to-delivery max is valid and acceptable
                            if ctm[k] < minT:                   # for all acceptable rows, keep one with lowest cumul. time.
                                minT    = ctm[k]
                                BI      = k                     # setting Best Index

            if minT == 8 * md or BI == r_mc+1:
                pass
            else:
                new_cost = ctm[BI] - current_cost
                if new_cost < added_cost:
                    added_cost      = new_cost
                    found_a_dg      = 1
                    tmp_returnVar   = returnVar_i[:deliveryCount]
                    di              = tmp_realCombos[BI]

                    #import embed_ipython as I; I.i_trace()

                    for j in range(deliveryCount):
                        orderSK_pt      = orderSK[BI][j]
                        dk              = tmp_returnVar[j]
                        if j==0:
                            first_row   = o[0]
                            if tripStartPt==first_row[5]:               # i.e., tripStartPt==start_node
                                dk[:7]  = first_row[:7]
                            else:
                                dk[:11] = first_row
                        else:
                            dk[0]       = orderTimes[orderSK_pt]            # orderTime
                            dk[1]       = deliveryIDs[orderSK_pt]           # deliveryID (already sorted by key)
                            dk[2]       = currentID                         # dg_id
                            dk[3]       = currentDG[1]                      # dg_node
                            mc_pt       = pointSK[BI][orderSK_pt*2]
                            dk[4]       = tT[BI][mc_pt]                     # travelTimeToLoc
                            dk[5]       = di[mc_pt]                         # start_node
                            dk[6]       = sT[BI][orderSK_pt]                # startTime
                        dk[7]       = tdd[BI][orderSK_pt]                   # travelTime
                        dk[8]       = eT[BI][orderSK_pt]                    # endTime
                        mc_pt       = pointSK[BI][(orderSK_pt*2)+1]
                        dk[9]       = di[mc_pt]                             # end_node
                        dk[10]      = odt[BI][orderSK_pt]                   # totalOrderTime
                        dk[11]      = BI                                    # best index

            # bestComboReturn
            #----------------------------------------------------

        # else:  # no results for a particular DG
        if i==o_grp_num-2 and found_a_dg==1:
            return tmp_returnVar
    # aii = returnVar[:ept]
    # print 'cy_scratch finis'
    # import embed_ipython as I; I.embed();
    # return aii

"""
import pandas as pd
pd.DataFrame(c_vars,columns=[ 'order_time', 'deliv_id', 'dg_id', 'dg_node',
                            'travel_time_to_loc', 'start_node', 'start_time',
                            'travel_time', 'end_time', 'end_node',
                            'total_order_time', 'status'])
"""


# ---------------------------------------------
# ---------------------------------------------
