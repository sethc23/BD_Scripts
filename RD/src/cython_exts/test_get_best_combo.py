
def test_get_best_combo(start_X, start_Y, mockCombo,
                                    realCombo,
                                    orderSK,
                                    pointSK,
                                    orderTimes,
                                    deliveryIDs,
                                    d,
                                    tripStart, sp,
                                    maxOrderTime,
                                    maxTravelTime,
                                    tT,                 # c_travelTimes
                                    sT,                 # c_startTimes
                                    eT,                 # c_endTimes
                                    odt,                # c_odtTimes
                                    oMax,                # c_max_order-to-deliveryTime
                                    tMax,                # c_MaxTravelToLocTime
                                    tdd,                # c_tddTimes
                                    ctm,                  # c_ctMarker
                                    return_orders):     # c_returnVars

    r = mockCombo.shape[0]                                    # number of rows
    pts = mockCombo.shape[1]                                  # number of pts
    BI = r+1                                                  # time in between each pt, best index.
    minT = 8*maxOrderTime                                     # minimum total route time (assuming 8 routes is max route #)

    for j in range(pts):
        for i in range(r):
            if j == 0:
                xptb=realCombo[i][j][0]
                yptb=realCombo[i][j][1]
                x=abs(start_X-xptb)
                y=abs(start_Y-yptb)
                t=sp*(x+y)
                ctm[i] = tripStart+t
                tT[i][j] = tripStart+t
                oMax[i] = 0
                tMax[i] = tripStart+t
            else:
                xpta=realCombo[i][j-1][0]
                ypta=realCombo[i][j-1][1]
                xptb=realCombo[i][j][0]
                yptb=realCombo[i][j][1]
                x=abs(xpta-xptb)
                y=abs(ypta-yptb)
                t=sp*(x+y)
                ctm[i] += t
                tT[i][j] = t
                if t > tMax[i]:
                    tMax[i] = t

            mc_pt=mockCombo[i][j]
            if mc_pt<100: sT[i][mc_pt]=ctm[i]
            else: eT[i][mc_pt-100]=ctm[i]

            if j == pts-1:                          # this is the last part of the 2D iteration
                for k in range(d):
                    orderSK_pt=orderSK[i][k]
                    eT_pt=eT[i][k]
                    tdd[i][k]=eT_pt-sT[i][k]
                    odt_pt=eT_pt-orderTimes[orderSK_pt]
                    odt[i][k]=odt_pt
                    if odt_pt>oMax[i]:
                        oMax[i]=odt_pt              # update max order-to-delivery time [ per row ] -- keeping biggest value

                if oMax[i]<=maxOrderTime:           # if order-to-delivery max is acceptable &
                    if tMax[i] <= maxTravelTime:    # max travelToLoc time is acceptable -->  save row as Best Index
                        if ctm[i]<minT:             # for all acceptable rows, keep one with lowest cumul. time.
                            minT=ctm[i]
                            BI=i

    if minT==8*maxOrderTime:
        return_orders[0][13]=0                      # interpretted on return as an error
        return_orders[1][13]=BI
        return return_orders
    elif BI == r+1:
        return_orders[0][13]=0                      # interpretted on return as an error
        return_orders[1][13]=505                    # interpretted on return as "error setting best index"
        return return_orders
    else:
        for e in range(d):
            orderSK_pt=orderSK[BI][e]
            return_orders[e][0] = start_X                # dg_X
            return_orders[e][1] = start_Y                # dg_Y
            return_orders[e][2] = orderSK_pt+1             # deliveryNum (starts at zero)
            return_orders[e][3] = deliveryIDs[orderSK_pt]          # deliveryID (already sorted by key)
            return_orders[e][4] = orderTimes[orderSK_pt]           # orderTime
            mc_pt=pointSK[BI][e*2]
            return_orders[e][5] = tT[BI][mc_pt]        # travelTimeToLoc
            return_orders[e][6] = realCombo[BI][mc_pt][0]     # startX // see below for explanation
            return_orders[e][7] = realCombo[BI][mc_pt][1]     # startY
            return_orders[e][8] = sT[BI][e]            # startTime
            return_orders[e][9] = tdd[BI][e]           # travelTime
            return_orders[e][10]= eT[BI][e]            # endTime
            mc_pt=pointSK[BI][e*2+1]
            return_orders[e][11]= realCombo[BI][mc_pt][0]     # endX
            return_orders[e][12]= realCombo[BI][mc_pt][1]     # endY
            return_orders[e][13]= odt[BI][e]           # totalOrderTime
            return_orders[e][14]= BI
        return return_orders

    ## Assume [1,0] = orderSK, a.k.a. Order Sort Key.
    ##  the '1' being first means the second order, i.e., order B, is picked up first.
    ##  thus, orderSK[0] = 1.
    ##
    ## Assume [1,3,0,2] = pointSK, a.k.a. Point Sort Key, which corresponds to points [A1,A2,B1,B2].
    ##  the '1' at the beginning means the pickup of the first order, i.e., A1, occurs at index 1 in the route.
    ##  the '0' in the third position means that pickup of B1 occurs at index 0 in the route.
    ##
    ## In order to identify the X-axis location of a point on a particular order,
    ##  Start with the order key, which shows that the second order pickup precedes the first order pickup.
    ##      deliveryNum = 1 and the second order is the subject of the first iteration of return_orders.
    ##  Now, orderSK[e]=1 can be used as an index in pointSK to identify the index of B1 in the permutated array of locations.
    ##      (The '*2' keeps the index consistent with an order pickup being every other point in [A1,A2,B1,B2,...n1,n2].)
