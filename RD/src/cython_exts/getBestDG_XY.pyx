
cimport cython
# from get_best_combo import c_get_best_combo as get_best_combo

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long[:,::1] c_getBestDG(long[::1] new,
                            long[:,::1] o_grp,              # group of order_q_i
                            long[::1] dg_grp_ids,           # unique IDs for groups
                            long[:,::1] dg_grp,
                            long[::1] deliveryIDs,          # delivery IDs
                            long[::1] orderTimes,           # order times
                            double precision MPH,           # speed
                            long md,                        # max delivery time
                            long mdpp,                      # max delivery per person
                            long mttlt,                     # max time to delivery locations
                            long[:,::1] c_tripPoints,       # empty trip points array
                            long[:,::1] orderSet2,          # permutation data for 2 orders
                            long[:,::1] orderSet3,          # permutation data for 2 orders
                            long[:,::1] orderSet4,          # permutation data for 2 orders
                            long[:,::1] orderSet5,          # permutation data for 2 orders
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
                            long[:,::1] returnVar1,         # return for combo start info (cols = 14)
                            long[:,::1] returnVar2,         # return for eval single order of best combo (cols = 15)
                            long[:,::1] returnVar_i,        # return for individual order results (cols = 15)
                            long[:,::1] returnVars):        # return for group results (cols = 15)
    """

    new_ord_cols= ['order_time','deliv_id','start_node','end_node']

    ord_grp_cols= ['order_time','deliv_id','dg_id','dg_node','travel_time_to_loc',
                    'start_node','start_time','travel_time','end_time','end_node','total_order_time']

    dg_grp_cols = ['dg_id','dg_node','current_deliveries','total_delivered','total_travel_time']


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
    # 	        s_d	oq	dgP	o	IR	new	o_res	geQ	gNew gIR
    # id (dg)	    --	0	0	--	0	--	--	2	--  --
    # id (vendor)	0	--	--	--	--	--	--	--	--	--
    # vend_X	    1	--	--	--	--	1	--	--	--	--
    # vend_Y	    2	--	--	--	--	2	--	--	--	--
    # orderNum	    3	--	--	--	--	3	--	--	--	--
    # dg_X/node     --	1	1	1	--	--	0	3	--	--
    # dg_Y          --	2	2	2	--	--	1	--	--	--
    # deliveryNum  	--	3	--	3	--	--	2	--	--	--
    # travTimeToLoc	--	4	--	4	--	--	5	4	--	--
    #	--
    # deliveryID  	4	5	--	5	7	4	3	1	0	4
    # orderTime  	5	6	--	6	8	5	4	0	1	5
    #
    # start_X/node  6	7	--	7	--	6	6	5	2	--
    # start_Y  	    7	8	--	8	--	7	7	--	--	--
    #
    # startTime  	--	9	--	9	--	--	8	6	--	--
    # endTime  	    --	10	--	10	--	--	9	8	--	--
    #
    # end_X/node    8	11	--	11	--	8	10	9	3	--
    # end_Y  	    9	12	--	12	--	9	11	--	--	--
    #
    # totOrdTime 	--	13	--	13	--	--	12	10	--	--
    # travelTime	--	14	--	14	--	--	13	7	--	--
    # totalDeliv	--	--	3	--	--	--	--	--	--	--
    # currDelivs	--	--	4	--	--	--	--	--	--	--
    # bestIndex	    --	--	--	--	--	--	14	--	--	--
    # tripStTime	--	--	--	--	0	--	--	--	--	0
    # tripStX/node  --	--	--	--	1	--	--	--	--	1
    # tripStY	-	--	--	--	2	--	--	--	--	--
    # tripPt_node1	--	--	--	--	3	--	--	--	--	2
    # tripPt_Y_1st	--	--	--	--	4	--	--	--	--	--
    # tripPt_node2	--	--	--	--	5	--	--	--	--	3
    # tripPt_Y_2nd	--	--	--	--	6	--	--	--	--	--

    """

    # cdefs
    cdef long[:,::1] c_get_combo_start_info
    cdef int groupNum = dg_grp_ids.shape[0]
    cdef int groupRows = o_grp.shape[0]
    cdef int grp_s_pt = 0
    cdef int grp_e_pt = 0
    cdef int complete,i,j,k,h,n,g,r_o,c_o,r_res,mpt,pts,r_mc
    cdef long s,e,x,y,t,dg_X,dg_Y,ID
    cdef long x1,y1,x2,y2,toLoc,toDel
    cdef long orderCount,currentID,currentX,currentY,deliveryCount
    cdef long[::1] ai
    cdef long[::1] grp_row
    cdef long[::1] aj
    cdef long[::1] ak
    cdef long[::1] ah
    cdef long[:,::1] o
    cdef long NOW = new[0]
    cdef long[:,::1] aii
    cdef long[:,::1] comboStartInfoReturn
    cdef long travel_time
    cdef long tripStartTime
    cdef long tripStartPtX
    cdef long tripStartPtY
    cdef long[:,::1] tripPoints
    cdef long[:,::1] rv_i                   # individual return value
    cdef long ro,
    cdef long[::1] bi
    cdef long[:,::1] testSet
    cdef long[:,::1] bii
    cdef long[:,::1] cii
    cdef long[:,::1] mockCombos
    cdef long[:,:] orderSK
    cdef long[:,:] pointSK
    cdef long[:,:,::1] tmp_realCombos
    cdef int BI
    cdef long minT                           # time in between each pt, best index.
    cdef long mc_pt,orderSK_pt,odt_pt,ttl_pt,sT_pt,eT_pt,xpta,ypta,xptb,yptb
    cdef long[:,::1] akk
    cdef long[:,::1] ajj
    cdef long[:,::1] bestComboReturn
    cdef long[:,::1] updateResReturn
    cdef long c,d
    cdef long s1,e1,s2,e2,checkVar
    cdef long[::1] bj
    cdef long minVar = md
    cdef int ept = returnVars.shape[0]

    returnVars[0][11] = 0           # default is error in case returned

    for i in range(groupNum):
        complete     = 0            # 0,2 --> no result, 1 --> process result
        orderCount   = 0
        currentID    = dg_grp_ids[i]
        ai           = dg_grp[i]
        current_node = ai[0]

        for j in range(grp_s_pt,groupRows):
            grp_row = o_grp[j]
            if grp_row[0] != currentID:
                break
            else:
                grp_e_pt = j+1
                if grp_row[10] > NOW:   # grp_row[10] = endTime
                    orderCount += 1
                grp_row[1] = current_node

        o   = o_grp[grp_s_pt:grp_e_pt]
        r_o = o.shape[0]
        c_o = o.shape[1]
        grp_s_pt = grp_e_pt
        deliveryCount = orderCount+1
        aii = returnVar1[:deliveryCount]

        #----------------------------------------------------
        #comboStartInfoReturn = get_combo_start_info(new,o,aii)
        h=0
        k=0
        n=0
        tripStartTime = 1000
        for j in range(r_o):
            aj = o[j]               # "o" is working part of o_grp / ord_grp
            s  = aj[2]              # start time
            e  = aj[4]              # end time
            if e>NOW:               # is there at least one order with an endTime less than now? if not, then return for single order.
                n=1
            if s-NOW < tripStartTime-NOW and s-NOW>0:
                tripStartTime = s
                h=j                 # h == index pt for order_q rows
                k=3                 # k == index pt for whether last point is/was ( startPt | endPt )
            # if t==endTime, it is too late to change DG's next destination
            if e-NOW < tripStartTime-NOW and e-NOW > 0:
                tripStartTime = e
                h=j
                k=5

        aj = aii[0]
        if n==0:
            aj[0]   = NOW
            aj[1]   = new[2]        # tripStartPt
            aj[2]   = -1            # this signals an error
        else:
            ah      = o[h]
            aj[0]   = tripStartTime
            s       = ah[k]
            aj[1]   = s             # tripPtA = (start_A | end_A)

            n = 0
            h = 0
            k = 0
            for j in range(r_o):
                aj  = o[j]
                s   = aj[6]         # start time
                e   = aj[8]         # end time
                g   = 1

                # if i==0:
                #     p1 = aj[5]
                #     p2 = aj[5]
                if (NOW < s and NOW < e):      # IF not start yet, use start point as start location
                    p1 = aj[5]
                    p2 = aj[9]
                elif (s <= NOW and NOW < e):   # ELIF, (already started | starting) & (ending now | ending later),
                    p1 = aj[9]
                    p2 = aj[9]
                else:
                    g  = 0

                if g == 1:
                    ah    = aii[h]
                    ah[4] = aj[1]       # deliveryID
                    ah[5] = aj[0]       # orderTime
                    h    += 1

                    ak    = aii[k]
                    k    += 1
                    t     = n+2
                    ak[t] = p1
                    if k == deliveryCount:
                        k = 0
                        n = 2

                    ak = aii[k]
                    k += 1
                    t = n+2
                    ak[t] = p2
                    if k == deliveryCount:
                        k = 0
                        n = 2

            ah      = aii[h]
            ah[4]   = new[1]            # deliv_id
            ah[5]   = new[0]            # orderTime
            k       = deliveryCount-1
            ak      = aii[k]
            ak[2]   = new[2]
            ak[3]   = new[3]

        comboStartInfoReturn = aii

        # if i == 1:
        #     return comboStartInfoReturn
        # comboStartInfoReturn = get_combo_start_info(new,o,aii)
        #----------------------------------------------------

        ai              = aii[0]
        tripStartTime   = ai[0]
        tripStartPt     = ai[1]

        if ai[2] == -1:

            #----------------------------------------------------
            # rv_i = eval_single_order(new,o,tripStartPt,tripStartTime,sp,md,aii)

            pt1         = tripStartPt
            pt2         = new[2]
            pt3         = new[3]

            # totalTime   =


            if tripStartTime + toLoc + toDel <= md:
                for j in range(r_o):
                    ai  = o[j]      # ord_que item
                    bi  = aii[j]    # combo_start_info_results ("gIR")
                    for j in range(c_o):
                        bi[j] = ai[j]
                    if j==r_o-1:
                        ID = ai[0]
                        dg_X = ai[1]
                        dg_Y = ai[2]
                j = r_o+1
                bi = aii[j]
                bi[0] = ID
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
            else:
                aii[0][13] = 0    # signals no result
                rv_i = aii[0:0]

            # rv_i = eval_single_order(new,o,tripStartPtX,tripStartPtY,tripStartTime,sp,md,aii)
            #----------------------------------------------------

            if rv_i[0][13] == 0:
                complete = 2
            else:
                complete = 1
            # no result == (rv_i[0][13] == 0) & ( len(returnVar)==1 [ instead of expected 2 ] )

        ## ////////////////////////////////
        ## --------------------------------
        # if i == 1:
        #     returnVars[0][0] = 505
        #     returnVars[1][0] = 505
        #     returnVars[0][1] = deliveryCount
        #     returnVars[1][1] = complete
        #     returnVars[0][2] = tripStartPtX
        #     returnVars[1][2] = tripStartPtY
        #     return returnVars
        ## --------------------------------
        ## \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

        if complete == 0:

            for j in range(deliveryCount):
                ai              = comboStartInfoReturn[j]
                deliveryIDs[j]  = ai[7]
                orderTimes[j]   = ai[8]
                bi              = c_tripPoints[j]
                bi[0]           = ai[3]
                bi[1]           = ai[4]
                k               = j + deliveryCount
                bi              = c_tripPoints[k]
                bi[0]           = ai[5]
                bi[1]           = ai[6]

            tripPoints = c_tripPoints[:deliveryCount*2]

            ## ////////////////////////////////
            ## --------------------------------
            #
            # if i == 1:
            #     return c_tripPoints

            ## --------------------------------
            ## \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

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

            pts = mockCombos.shape[1]
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

            ## ////////////////////////////////
            ## --------------------------------

            # if i == 1:
            #     return mockCombos
                # return realCombos[0]

            ## --------------------------------
            ## \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

            # realCombos = c_mapper(tripPoints, mockCombos,tmp_realCombos)
            #----------------------------------------------------

            #----------------------------------------------------
            # bestComboReturn = get_best_combo(tripStartPtX,  # returns "o_res" format
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
            #                        returnVar2[:deliveryCount])
            BI = r_mc + 1
            minT =  (8 * md)     # minimum total route time (assuming 8 routes is max route #)
            bestComboReturn = returnVar2[:deliveryCount]
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
            # if i == 1:
            #     bestComboReturn[0][0] = 99
            #     bestComboReturn[1][0] = 99
            #
            #     BI = 3
            #     bestComboReturn[0][1] = oMax[0]
            #     bestComboReturn[0][2] = oMax[1]
            #     bestComboReturn[0][3] = oMax[2]
            #     bestComboReturn[0][4] = oMax[3]
            #     bestComboReturn[0][5] = oMax[4]
            #     bestComboReturn[0][6] = oMax[5]
            #     bestComboReturn[0][7] = oMax[6]
            #
            #     # bestComboReturn[0][1] = tMax[0]
            #     # bestComboReturn[0][2] = tMax[1]
            #     # bestComboReturn[0][3] = tMax[2]
            #     # bestComboReturn[0][4] = tMax[3]
            #     # bestComboReturn[0][5] = tMax[4]
            #     # bestComboReturn[0][6] = tMax[5]
            #     # bestComboReturn[0][7] = tMax[6]
            #
            #     bestComboReturn[1][1] = ctm[0]
            #     bestComboReturn[1][2] = ctm[1]
            #     bestComboReturn[1][3] = ctm[2]
            #     bestComboReturn[1][4] = ctm[3]
            #     bestComboReturn[1][5] = ctm[4]
            #     bestComboReturn[1][6] = ctm[5]
            #     bestComboReturn[1][7] = ctm[6]
            #
            #     bestComboReturn[0][8] = minT
            #     bestComboReturn[1][8] = 505
            #
            #     bestComboReturn[0][9] = tripStartPtX
            #     bestComboReturn[1][9] = tripStartPtY
            #
            #     return bestComboReturn
                # return realCombos[BI]


            if minT == 8 * md:
                bestComboReturn[0][11] = 0                      # interpretted on return as an error
                bestComboReturn[1][11] = BI
            elif BI == r_mc + 1:
                bestComboReturn[0][11] = 0                      # interpretted on return as an error
                bestComboReturn[1][11] = 505                    # interpretted on return as "error setting best index"
            else:
                #aii = realCombos[BI]
                for e in range(deliv_cnt):
                    orderSK_pt  = orderSK[BI][e]
                    ak          = bestComboReturn[e]
                    ak[e][0]    = tripStartPt                   # dg_node
                    ak[e][1]    = orderSK_pt+1                  # deliveryNum (starts at zero)
                    ak[e][2]    = deliveryIDs[orderSK_pt]       # deliveryID (already sorted by key)
                    ak[e][3]    = orderTimes[orderSK_pt]        # order_time
                    mc_pt       = pointSK[BI][orderSK_pt*2]
                    ak[e][4]    = tT[BI][mc_pt]                 # travelTimeToLoc
                    ak[e][5]    = realCombos[BI][mc_pt]         # start_node
                    ak[e][6]    = sT[BI][orderSK_pt]            # startTime
                    ak[e][7]    = tdd[BI][orderSK_pt]           # travelTime
                    ak[e][8]    = eT[BI][orderSK_pt]            # endTime
                    mc_pt       = pointSK[BI][(orderSK_pt*2)+1]
                    ak[e][9]    = realCombos[BI][mc_pt]         # end_node
                    ak[e][10]   = odt[BI][orderSK_pt]           # totalOrderTime
                    ak[e][11]   = BI



            ## ////////////////////////////////
            ## --------------------------------

            # if i == 2:
            #     return bestComboReturn
                # return realCombos[0]

            ## --------------------------------
            ## \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

            # bestComboReturn = get_best_combo(tripStartPtX,...  # returns "o_res" format
            #----------------------------------------------------

            if bestComboReturn[0][11] != 0:                 # (general error | error setting best index)

                #----------------------------------------------------
                # updateResReturn = update_order_results(o,bestComboReturn,now) # expects "o_res" input // returns "o_res" format

                aii = bestComboReturn
                r_res = aii.shape[0]
                # iterate through o_res to replace info for static orders
                for j in range(r_o):
                    aj = o[j]
                    if aj[9] <= NOW and aj[10] > NOW:  # if then they are static orders...
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
                                break
                updateResReturn = aii

                # updateResReturn = update_order_results(o,bestComboReturn,now) # expects "o_res" input // returns "o_res" format
                #----------------------------------------------------
                import pdb; pdb.set_trace();
                rv_i = returnVar_i[:deliveryCount]
                aii = rv_i.T
                k = deliveryCount-1
                bi = rv_i[k]
                bii = updateResReturn.T
                cii = o.T
                aii[0][:r_o] = cii[0]       # id
                bi[0] = cii[0][0]
                aii[1][:r_o] = cii[1]       # dg_X
                bi[1] = cii[1][0]
                aii[2][:r_o] = cii[2]       # dg_y
                bi[2] = cii[2][0]
                aii[3] = bii[2]             # deliveryNum
                aii[4] = bii[5]             # travelTimeToLocation
                aii[5] = bii[3]             # deliveryID
                aii[6] = bii[4]             # orderTime
                aii[7] = bii[6]            # start_X
                aii[8] = bii[7]            # start_Y
                aii[9] = bii[8]            # startTime
                aii[10] = bii[10]          # endTime
                aii[11] = bii[11]          # end_X
                complete = 1

        if complete == 1:
            # checkVar = (order_result.endTime.max() - order_result.startTime.min()) - (order_q_i.endTime.max() - order_q_i.startTime.min())
            # checkVar = ( e2 - s2 ) - ( e1 - s1 )
            aj = rv_i[0]
            e2 = aj[10]
            s2 = aj[9]
            bj = o[0]
            e1 = bj[10]
            s1 = bj[9]
            for j in range(1,deliveryCount):
                aj = rv_i[j]
                s = aj[9]
                e = aj[10]
                if e > e2:
                    e2 = e
                if s < s2:
                    s2 = s
                ## -------------
                if j != deliveryCount-1:
                    bj = o[j]
                    s = bj[9]
                    e = bj[10]
                    if e > e1:
                        e1 = e
                    if s < s1:
                        s1 = s
                ## -------------
            checkVar = (e2-s2) - (e1-s1)
            # if i == 0:
            #     returnVars[0][0] = rv_i[0][9]
            #     returnVars[0][1] = rv_i[1][9]
            #     returnVars[0][2] = rv_i[0][10]
            #     returnVars[0][3] = rv_i[1][10]
            #     returnVars[1][0] = o[0][9]
            #     returnVars[1][1] = o[1][9]
            #     returnVars[1][2] = o[0][10]
            #     returnVars[1][3] = o[1][10]
            #     return returnVars
            if checkVar < minVar:
                minVar = checkVar
                returnVars[:deliveryCount] = returnVar_i[:deliveryCount]
                returnVars[deliveryCount:] = 0
                ept = deliveryCount
    aii = returnVars[:ept]
    return aii