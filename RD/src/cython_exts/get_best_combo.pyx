cimport cython
@cython.nonecheck(False)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef long[:,::1] c_get_best_combo( long[::1] p1,                   # p1/p2 are pairs for all unique node combos
                                    long[::1] p2,   #long[:,::1] node_list,          # matrix of nodes for all realCombos
                                    long[::1] minutes,               # the calculated distance in miles for each pair
                                    long[::1] total_time,         # an empty array for inserting total distance
                                    double MPH,                     # speed to use in finding time from distance
                                    long tripStartPt,
                                    long[:, :] mockCombos,
                                    long[:, ::1] realCombos,
                                    long[:, :] orderSK,
                                    long[:, :] pointSK,
                                    long[::1] orderTimes,
                                    long[::1] deliveryIDs,
                                    long deliv_cnt,
                                    long tripStartTime,
                                    long sp,
                                    long maxOrderTime,
                                    long maxTravelTime,
                                    long[:,::1] tT,                 # c_travelTimes
                                    long[:,::1] sT,                 # c_startTimes
                                    long[:,::1] eT,                 # c_endTimes
                                    long[:,::1] odt,                # c_odtTimes
                                    long[::1] oMax,                 # c_MaxOrderToDeliveryTimes
                                    long[::1] tMax,                 # c_MaxTravelToLocTimes
                                    long[:,::1] tdd,                # c_tddTimes
                                    long[::1] ctm,                  # c_ctMarker
                                    long[:,::1] return_orders):     # c_returnVars


    """
    
    Assume [1,0] = orderSK, a.k.a. Order Sort Key.
     the '1' being first means the second order, i.e., order B, is picked up first.
     thus, orderSK[0] = 1.

    Assume [1,3,0,2] = pointSK, a.k.a. Point Sort Key, which corresponds to points [A1,A2,B1,B2].
     the '1' at the beginning means the pickup of the first order, i.e., A1, occurs at index 1 in the route.
     the '0' in the third position means that pickup of B1 occurs at index 0 in the route.

    In order to identify the X-axis location of a point on a particular order,
     Start with the order key, which shows that the second order pickup precedes the first order pickup.
         deliveryNum = 1 and the second order is the subject of the first iteration of return_orders.
     Now, orderSK[e]=1 can be used as an index in pointSK to identify the index of B1 in the permutated array of locations.
         (The '*2' keeps the index consistent with an order pickup being every other point in [A1,A2,B1,B2,...n1,n2].)
    
    # RETURNS

            ['dg_node','deliv_num','deliv_id','order_time',
             'travel_time_to_loc','start_node','start_time',
             'travel_time','end_time','end_node','total_order_time','bestIndex']
             
             
    """

    cdef long r = mockCombos.shape[0]                # number of rows
    cdef long pts = mockCombos.shape[1]              # number of pts
    cdef long BI = r+1                              # time in between each pt, best index.
    cdef long minT = (8*maxOrderTime)               # minimum total route time (assuming 8 routes is max route #)
    cdef long i,j,e,t
    cdef long mc_pt,orderSK_pt,odt_pt,ttl_pt,x,y,sT_pt,eT_pt,xpta,ypta,xptb,yptb

    cdef int m_len = minutes.shape[0]
    cdef long _min
    cdef long[:] row
    cdef long ptA
    cdef long ptB
    cdef long p1_p
    cdef long p2_p
    cdef int p

    for j in range(pts):

        for i in range(r):

            if j == 0:
                ctm[i] = tripStartTime
                tT[i][j] = tripStartTime
                tMax[i] = tripStartTime
                pass
            else:
                ptA=realCombos[i][j-1]
                ptB=realCombos[i][j]
                for p in range(m_len):
                    p1_p = p1[p]
                    p2_p = p2[p]
                    if ( (ptA==p1_p and ptB==p2_p) or
                         (ptA==p2_p and ptB==p1_p) ):
                            t = minutes[p]
                            ctm[i] += t
                            tT[i][j] = t
                            if t > tMax[i]:
                                tMax[i] = t
                            break

            mc_pt = mockCombos[i][j]
            if mc_pt < 100:         sT[i][mc_pt] = ctm[i]+tripStartTime
            else:                   eT[i][mc_pt-100] = ctm[i]+tripStartTime

            if j == pts-1 and tMax[i] <= maxTravelTime: # this is the last part of the 2D iteration
                                                        # if max travelToLoc time is acceptable --> find Best Index
                oMax[i] = 0
                for k in range(deliv_cnt):
                    orderSK_pt          = orderSK[i][k]
                    eT_pt               = eT[i][orderSK_pt]
                    tdd[i][orderSK_pt]  = eT_pt-sT[i][orderSK_pt]
                    odt_pt              = eT_pt-orderTimes[orderSK_pt]
                    odt[i][orderSK_pt]  = odt_pt
                    if odt_pt > oMax[i]:
                        oMax[i] = odt_pt            # update max order-to-delivery time [ per row ] -- keeping biggest value

                if oMax[i]!=0 and oMax[i]<=maxOrderTime: # if order-to-delivery max is valid and acceptable
                    if ctm[i]<minT:                 # for all acceptable rows, keep one with lowest cumul. time.
                        minT=ctm[i]
                        BI=i                        # setting Best Index

    if minT==8*maxOrderTime or BI == r+1:
        return_orders[0][13]=0                              # interpretted on return as "no valid index available"
        return_orders[1][13]=505
        return_orders[2][13]=505
        return return_orders
    else:
        for e in range(deliv_cnt):
            orderSK_pt=orderSK[BI][e]
            return_orders[e][0] = tripStartPt               # dg_X
            return_orders[e][1] = orderSK_pt+1              # deliveryNum (starts at zero)
            return_orders[e][2] = deliveryIDs[orderSK_pt]   # deliveryID (already sorted by key)
            return_orders[e][3] = orderTimes[orderSK_pt]    # orderTime
            mc_pt   =   pointSK[BI][orderSK_pt*2]
            return_orders[e][4] = tT[BI][mc_pt]             # travelTimeToLoc
            return_orders[e][5] = realCombos[BI][mc_pt]     # startX // see below for explanation
            return_orders[e][6] = sT[BI][orderSK_pt]        # startTime
            return_orders[e][7] = tdd[BI][orderSK_pt]       # travelTime
            return_orders[e][8] = eT[BI][orderSK_pt]         # endTime
            mc_pt   =   pointSK[BI][(orderSK_pt*2)+1]
            return_orders[e][9] = realCombos[BI][mc_pt]      # endX
            return_orders[e][10]= odt[BI][orderSK_pt]       # totalOrderTime
            return_orders[e][11]= BI
        return return_orders