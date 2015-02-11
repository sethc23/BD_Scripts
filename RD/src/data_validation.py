# Data Validation f(x)s
from rd_lib import pd,np
import assumptions as A
from sim_data_gen import init_dg_pool
from handle_results import pull_from_order,systemError

def set_col_types(globalVars):
    from rd_lib import ord_q_cols_types,dg_q_cols_types,dg_pool_cols_types
    order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

    for k,v in ord_q_cols_types.iteritems():
        order_q[k]=order_q[k].astype(v)
        order_delivered[k]=order_delivered[k].astype(v)

    for k,v in dg_q_cols_types.iteritems():
        dg_q[k] = dg_q[k].astype(v)
        dg_delivered[k] = dg_delivered[k].astype(v)

    for k,v in dg_pool_cols_types.iteritems():
        dg_pool[k] = dg_pool[k].astype(v)

    globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
    return globalVars

# @profile
def order_by_min(globalVars,ordersNow,errorCheck=True):

    def getDG_q_i_from_oq_ret(ordersNow,order_q_ret,added_orders,order_delivered,dg_q):
        now = ordersNow.order_time.astype(np.int64).values[0]
        d = order_delivered
        changedDG_ids = added_orders.id.unique().tolist()
        for it in changedDG_ids:
            # append nothing if all prior orders completed else append all
            startMin = order_q_ret[order_q_ret.id==it].order_time.values.min()
            # f = d.ix[:-1,:] if len(d[(d.id==it) & ((d.end_time>now) | (d.end_time>startMin))])==0 else d[d.id==it]
            f = d[(d.id==it) & ((d.end_time>now) | (d.end_time>startMin))]
            check_order_q_i = order_q_ret[order_q_ret.id==it].append(f)
            check_dg_q_i = pull_from_order(check_order_q_i,errorCheck=False)
            # TODO: need to re-activate errorCheck for this
            new_dg_q_i = check_dg_q_i[check_dg_q_i['ptb-t']>now]
            dg_q = dg_q[dg_q.dg_id!=it].append(new_dg_q_i)
        return dg_q

    stop,loop_i=False,0
    last_loop_i,last_remaining_orders_cnt = -2,-2
    while stop==False:
        loop_i += 1
        # print 'Number of Orders =',len(ordersNow)
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
        order_q = order_q.sort('vend_id')
        # print len(dg_pool[(dg_pool.total_delivered==0) & (dg_pool.current_deliveries==0)]),' unused DG'
        # print dg_pool[dg_pool['current_deliveries']!=0]

        ## FIND
        # TODO: use
        vend_dims = sim_data.vend_X.min(),sim_data.vend_X.max(),sim_data.vend_Y.min(),sim_data.vend_Y.max()
        # for i in np.arange(vend_dims[0],vend_dims[1],max_travelToLocTime)

        ncols = round((vend_dims[1] - vend_dims[0])/max_travelToLocTime)+1
        x_spread = round((vend_dims[1] - vend_dims[0])/ncols)
        x_units = np.arange(vend_dims[0],vend_dims[1]+1,x_spread)

        nrows = round((vend_dims[3] - vend_dims[2])/max_travelToLocTime)+1
        y_spread = round((vend_dims[3] - vend_dims[2])/nrows)
        y_units = np.arange(vend_dims[2],vend_dims[3]+1,y_spread)


        dgp_geo_units = np.empty((x_units.shape[0],y_units.shape[0], 2))
        dgpNew = dg_pool[(dg_pool.current_deliveries==0)&(dg_pool.total_delivered>0)]
        pt=0
        for i in range(1,x_units.shape[0]):
            mid_x = round(x_units[i]-x_units[i-1]/2.0)

            for j in range(1,y_units.shape[0]):
                mid_y = round(y_units[j]-y_units[j-1]/2.0)

                dgp_geo_units[i-1,j-1,1] = mid_x
                dgp_geo_units[i-1,j-1,0] = mid_y

                dgpNew[str(pt)] = dgpNew.ix[:,['dg_X','dg_Y']].apply(lambda s: pd_get_travel_time(mid_x,mid_y,*s),axis=1)
                pt += 1

        # dgpNew.ix[:,[str(i) for i in range(pt)]].apply(lambda s: pd_min_of_list(*s),axis=1)

        dgpNew['shortestDist'] = dgpNew.ix[:,[str(i) for i in range(pt)]].apply(lambda s: pd_min_of_list(*s),axis=1)

        dgpNew['closestCtr'] = 0
        for i in range(1,pt):
            # dgpNew.ix[:,['shortestDist',str(i)]].apply
            # D.head().ix[:,['closestCtrPt','shortestDist',str(i)]].apply(lambda it: pd_index_of_list(*it),axis=1)
            # dgpNew['check'] = i if dgpNew.ix[:,str(i)]==dgpNew.ix[:,'shortestCtr'] else False
            # dgpNew['closestCtr'] = dgpNew.closestCtr
            # dgpNew['closestCtr'] = dgpNew.ix[:,[str(i) for i in range(pt)]].apply(lambda s: pd_min_of_list(*s),axis=1)
            dgpNew['closestCtr'] = dgpNew.ix[:,[str(i),'shortestDist','closestCtr']].apply(lambda s: i if s[0]==s[1] else s[2],axis=1)
        print dgpNew


        ctr_pts = [ dgpNew.closestCtr.astype(np.int64).tolist().count(i) for i in range(pt) ]
        ctr_pt_dict = dict(zip(range(pt),ctr_pts))
        ctr_pts_sorted = sorted(ctr_pts)
        ctr_pt_sorted_dict = dict(zip(range(pt),ctr_pts_sorted))
        l=zip(ctr_pts,range(pt))
        ctr_pt_inds = [it[1] for it in sorted(l)]

        pt2=0
        for i in range(dgp_geo_units.shape[0]-1):
            # mid_x = round(x_units[i]-x_units[i-1]/2.0)


            for j in range(dgp_geo_units.shape[1]-1):
                # mid_y = round(y_units[j]-y_units[j-1]/2.0)
                mid_x = dgp_geo_units[i,j,0]
                mid_y = dgp_geo_units[i,j,1]# = mid_y

                it = ctr_pt_inds[pt2]

                dg_grp_num = sum(ctr_pts)/len(ctr_pts) - ctr_pts[it]
                pt2 += 1

                chg_dg_grp = dgpNew.sort_index(by=str(it),ascending=[True]).reset_index(drop=True).ix[:dg_grp_num,:]
                a=0

                # chg_dg_grp.ix[:,['dg_X','dg_Y','']

                # def getInfo(*items):


        for it in ctr_pt_inds:
            dg_grp_num = sum(ctr_pts)/len(ctr_pts) - ctr_pts[it]
            chg_dg_grp = dgpNew.sort_index(by=str(it),ascending=[True]).reset_index(drop=True).ix[:dg_grp_num,:]
            # what is the next position for each DG as moving toward
            # dgp_geo_units[]
        n=0
        ct_pts[3]
        for i in range(len(ctr_pts_sorted)):
            dg_grp_num = sum(ctr_pts)/len(ctr_pts) - ctr_pts[it]
            if dg_grp_num > len(remaining_dg): dg_grp_num = remaining_dg









        dg_total = dg_pool.current_deliveries.values + dg_pool.total_delivered.values
        if dg_total.sum() != len(order_q) + len(order_delivered):
            print 'dg_total.sum() != len(order_q)'
            systemError()
        elif dg_pool.current_deliveries.max()>5:
            max_val = dg_pool.current_deliveries.max()
            print dg_pool[dg_pool.current_deliveries==max_val]
            print 'too many deliveries'
            systemError()

        newOrderIDs = ordersNow.deliv_id.astype(np.int64).tolist()
        c_newOrders = np.ascontiguousarray(ordersNow.astype(np.intc).as_matrix(),dtype=np.intc)
        clean_order_q = order_q.drop(['status','ave_X','ave_Y'],axis=1).sort_index(by=['id','start_time'],ascending=[True,True]).reset_index(drop=True).astype(np.intc).as_matrix()
        d = len(ordersNow)
        z = np.zeros((d,clean_order_q.shape[1]), dtype=np.intc,order='C')
        c_order_q_a = np.ascontiguousarray(clean_order_q.tolist() + z.tolist(),dtype=np.intc)
        c_order_q_b = np.ascontiguousarray(np.zeros(c_order_q_a.shape, dtype=np.intc,order='C'))
        c_reorder_q = np.ascontiguousarray(np.zeros((c_order_q_a.shape[0],), dtype=np.intc,order='C'))
        # c_dg_seg_size = np.intc(len(c_order_q_a)/float(A.DG_pool_grp_part_size))
        c_dg_seg_size = np.intc(A.DG_pool_grp_part_size)
        # print order_q
        # print dg_pool
        c_dgp_a = np.ascontiguousarray(dg_pool.astype(np.intc).as_matrix(),dtype=np.intc)
        c_dgp_b = np.ascontiguousarray(np.zeros(c_dgp_a.shape, dtype=np.intc,order='C'))

        ret_order_q = c_order_by_min(c_order_q_a,
                                c_order_q_b,
                                c_reorder_q,
                                c_dgp_a,
                                c_dgp_b,
                                c_dg_seg_size,
                                c_newOrders,
                                c_deliv_ids,
                                c_order_times,
                                c_speed,
                                c_max_delivery_time,
                                c_max_delivery_per_dg,
                                c_mttlt,
                                c_tripPoints,
                                G.c_orderSet2,
                                G.c_orderSet3,
                                G.c_orderSet4,
                                G.c_orderSet5,
                                G.c_orderSetInd,
                                c_realCombos,
                                c_travel_times,
                                c_start_times,
                                c_end_times,
                                c_odtTimes,
                                c_oMaxTimes,
                                c_tMaxTimes,
                                c_tddTimes,
                                c_ctMarker,
                                c_rv_comboStartInfo,
                                c_rv_bestCombo,
                                c_rv_updatedBestCombo,
                                c_bestDG)

        # import pstats, cProfile
        #
        # cProfile.runctx('c_order_by_min(c_order_q_a,'+
        #                         'c_order_q_b,'+
        #                         'c_reorder_q,'+
        #                         'c_dgp_a,'+
        #                         'c_dgp_b,'+
        #                         'c_dg_seg_size,'+
        #                         'c_newOrders,'+
        #                         'c_deliv_ids,'+
        #                         'c_order_times,'+
        #                         'c_speed,'+
        #                         'c_max_delivery_time,'+
        #                         'c_max_delivery_per_dg,'+
        #                         'c_mttlt,'+
        #                         'c_tripPoints,'+
        #                         'c_orderSet2,'+
        #                         'c_orderSet3,'+
        #                         'c_orderSet4,'+
        #                         'c_orderSet5,'+
        #                         'c_orderSetInd,'+
        #                         'c_realCombos,'+
        #                         'c_travel_times,'+
        #                         'c_start_times,'+
        #                         'c_end_times,'+
        #                         'c_odtTimes,'+
        #                         'c_oMaxTimes,'+
        #                         'c_tMaxTimes,'+
        #                         'c_tddTimes,'+
        #                         'c_ctMarker,'+
        #                         'c_rv_comboStartInfo,'+
        #                         'c_rv_bestCombo,'+
        #                         'c_rv_updatedBestCombo,'+
        #                         'c_bestDG)')#, globals(), locals(), "seamless.py.prof")

        # cProfile.runctx("calc_pi.approx_pi()", globals(), locals(), "Profile.prof")

        # s = pstats.Stats("Profile.prof")
        # s.strip_dirs().sort_stats("time").print_stats()
        #
        # print '\n\n'
        # print s
        # TODO: need to fix distribution of vendors/deliveries
        # print np.asarray(ret_order_q)
        # systemError()
        order_q_ret,a,remaining_order_ids = receive_c_order_by_min(ret_order_q,showVar=False)
        order_q_ind = order_q_ret.index.tolist()
        # systemError()
        # if order_q_ret.deliv_id.tolist().count(4037) != 0:
        #     print 'found order'
        #     systemError()
        endPt = len(order_q_ind) - 1
        if len(remaining_order_ids) != 0:   # a[endPt][0]==950 and a[endPt][3]==950:
            re_pool = True
            order_q_ret = order_q_ret.ix[order_q_ind[:-1],:]  # remove last row...
            # systemError()
        elif a[endPt][0]==450 and a[endPt][3]==450:
            print 'need to account for deliveryCount == 1 (which is not ever expected)'
            systemError()
        elif a[endPt][0]==555 and a[endPt][3]==555:
            print order_q_ret#[(order_q_ret.id==139) | (order_q_ret.id==555)]
            # from cython_scratch import test
            # x=test(c_orderSet4,c_orderSetInd,c_tripPoints[:8],c_realCombos)
            # print x
            a=0
            systemError()
        else: re_pool = False

        added_orders = order_q_ret[order_q_ret.deliv_id.isin(newOrderIDs)==True]
        added_deliv_ids = added_orders.deliv_id.astype(np.int64).tolist()
        completed_orders = ordersNow[(ordersNow.deliv_id.isin(added_deliv_ids)==True)]
        remaining_orders = ordersNow.ix[ordersNow.index - completed_orders.index,:]

        if len(remaining_orders)==0: re_pool = False
        else:
            re_pool = True
            ordersNow = remaining_orders

        order_q = order_q.append(added_orders).sort_index(by='id').reset_index(drop=True)
        # TODO: move down back into re-pool option only b/c this is repetitive of "update per min"
        # update location for DG without orders
        # vend_dims = sim_data.vend_X.min(),sim_data.vend_X.max(),sim_data.vend_Y.min(),sim_data.vend_Y.max()
        # # for i in np.arange(vend_dims[0],vend_dims[1],max_travelToLocTime)
        # x_units = np.arange(A[0],A[1]+max_travelToLocTime,max_travelToLocTime)
        # y_units = np.arange(A[2],A[3]+max_travelToLocTime,max_travelToLocTime)
        # dgp_geo_units = np.empty(((x.shape[0]-1), (y.shape[0]-1)))
        # pt=0
        # for i in range(1,x_units.shape[0]):
        #     mid_x = round(x_units[i]-x_units[i-1]/2.0)
        #
        #     for j in range(1,y_units.shape[0]):
        #         mid_y = round(y_units[j]-y_units[j-1]/2.0)
        #
        #         dg_pool[str(pt)] = dg_pool.ix[:,['dg_X','dg_Y']].apply(lambda s: pd_get_travel_time(mid_x,mid_y,*s),axis=0).apply(lambda s: pd_combine(*s),axis=0)


        width = vend_dims[1]-vend_dims[0]
        height = vend_dims[3]-vend_dims[2]
        x_units,y_units = round(max_travelToLocTime/float(width)),round(max_travelToLocTime/float(height))
        dx = round(width/x_units)
        dy = round(height/y_units)
        a = np.empty(np.array((x_units,y_units)))
        for i in range(x_units):
            for j in range(y_units):
                a[i,j] = [( dx*(i+1) - dx*i ),( dy*(j+1) - dy*j )]

        # update dg_pool (if there was a specific order, it will be maintained)
        updatedDG_ids = added_orders.id.astype(np.int64).unique().tolist()
        updatedDG = dg_pool[dg_pool.dg_id.isin(updatedDG_ids)==True]
        updatedDG.current_deliveries = updatedDG.current_deliveries.values + 1
        globalVars = update_global_vars(globalVars,'update dg_pool',newAddVar=updatedDG,newSubVar=False,replaceVar={'id':updatedDG_ids})
        dg_pool = globalVars[4]
        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
        globalVars = update_global_vars(globalVars,'organize dg_pool',newAddVar=False,newSubVar=False,replaceVar={})
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars


        # print '\n1. total dg_pool - used dg - order_q - order_q (old) - ordersNow(old) - ordersDone - ordersRemaining'
        print len(dg_pool),len(dg_pool[(dg_pool.current_deliveries!=0) | (dg_pool.total_delivered!=0)]),len(order_q),len(globalVars[0]),c_newOrders.shape[0],len(completed_orders),len(remaining_orders)

        # error check included in next function
        dg_q = getDG_q_i_from_oq_ret(ordersNow,order_q_ret,added_orders,order_delivered,dg_q)

        if re_pool == False:
            break       # dg_pool order will be set on the "per order" basis
        else:
            # re-pool
            globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
            repool_size = len(remaining_order_ids)*3
            # set re-pool size here, use newSubVar as variable for number of new DG
            globalVars = update_global_vars(globalVars,'re-pool',newAddVar=False,newSubVar=repool_size,replaceVar={})
            globalVars = update_global_vars(globalVars,'organize dg_pool',newAddVar=False,newSubVar=False,replaceVar={})
            order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
            a=0
            # print '\n2. dg_pool - order_q - ordersNow - ordersDone - ordersRemaining\n',len(dg_pool),len(globalVars[0]),len(ordersNow),len(completed_orders),len(remaining_orders)

        if last_loop_i+1==loop_i and last_remaining_orders_cnt==len(remaining_orders):
            print 'order_by_min caught in loop'
            print remaining_orders
            print dg_pool
            systemError()
        else:
            last_loop_i = loop_i
            last_remaining_orders_cnt = len(remaining_orders)


    # # compare with results from previous method
    # for j in range(0,4):#len(ordersNow)):
    #     thisOrder=ordersNow.iloc[j,:].copy()
    #     thisOrder['deliv_id'] = ordersNow.index[j]
    #     globalVars = getBestDG(globalVars,thisOrder,errorCheck=errorCheck)
    # order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
    # print '\n'
    # print order_q
    # orderDG_a = sorted(order_q.id.astype(np.int64).unique().tolist())
    # orderDG_b = sorted(order_q_ret.id.astype(np.int64).unique().tolist())
    # if orderDG_a != orderDG_b:
    #     print 'different DGs for orders'
    #     systemError()
    # else:
    #     for it in orderDG_a:
    #         orderA = order_q[order_q.id==it]
    #         orderB = order_q_ret[order_q_ret.id==it]
            # compare_orders(orderA,orderB)
    order_q = order_q.reset_index(drop=True)
    globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
    return globalVars

def updateCurrentLocation(globalVars,now,changedDG=[]):
    order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
    travel_speed=A.travel_speed

    # if just finishing delivery, and currentDeliv will be 0, update location from order_q endPoint ...
    if len(changedDG) != 0:
        oq = order_q
        last_orders = oq[(oq.deliv_id.isin(changedDG)==True) & (oq.end_time==now)]
        if len(last_orders)!=0:
            last_order_ids = last_orders.deliv_id.astype(np.int64).tolist()
            last_order_id_ind_dict = dict(zip(last_orders.deliv_id.astype(np.int64).tolist(),last_orders.index))

            dyn_dg_pool = dg_pool[dg_pool.dg_id.isin(last_order_ids)==True]
            dyn_dg_pool_ids = dyn_dg_pool.dg_id.astype(np.int64).tolist()

            take_index = map(lambda s: last_order_id_ind_dict[s],dyn_dg_pool_ids)

            stat_dg_pool = dg_pool.ix[dg_pool.index - dyn_dg_pool.index]

            dyn_dg_pool[['dg_X','dg_Y']] = last_orders.ix[dyn_dg_pool_ids,['end_X','end_Y']].values
            dg_pool = pd.merge(stat_dg_pool,dyn_dg_pool,how='outer')

    static_dg_pool = dg_pool[(dg_pool.current_deliveries==0)]
    dyn_dg_pool = dg_pool.ix[dg_pool.index - static_dg_pool.index,:]
    if len(dyn_dg_pool.index)==0: return globalVars
    dyn_dg_pool_ids = dyn_dg_pool.dg_id.astype(np.int64).values.tolist()
    dg_q_i = dg_q[(dg_q.dg_id.isin(dyn_dg_pool_ids)==True) & (dg_q['pta-t'] <= now) & (now <=dg_q['ptb-t'])]

    # update DG pool position based on contents of DG Queue...(replace soon)
    dg_q_start = dg_q_i[dg_q_i['pta-t']==now].reset_index(drop=True)
    if len(dg_q_start.index)!=0:
        dg_q_start_ids = dg_q_start.dg_id.unique().astype(np.int64).tolist()
        new_dg_pool = dg_pool[dg_pool.dg_id.isin(dg_q_start_ids)].reset_index(drop=True)
        new_dg_pool['map'] = new_dg_pool.dg_id.map(lambda s: dg_q_start_ids.index(int(s)))
        new_dg_pool.ix[:,'dg_node'] = dg_q_start.ix[new_dg_pool.map.astype(np.int64).tolist(),'pta'].values

        globalVars = update_global_vars(globalVars,'update dg_pool',newAddVar=new_dg_pool.drop(['map'],axis=1).reset_index(drop=True),newSubVar=False,replaceVar={'dg_id':dg_q_start_ids})
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
    dg_q_end = dg_q_i[dg_q_i['ptb-t']==now].reset_index(drop=True)
    if len(dg_q_end.index)!=0:
        dg_q_end_ids = dg_q_end.dg_id.unique().astype(np.int64).tolist()
        new_dg_pool = dg_pool[dg_pool.dg_id.isin(dg_q_end_ids)].reset_index(drop=True)
        new_dg_pool['map'] = new_dg_pool.dg_id.map(lambda s: dg_q_end_ids.index(int(s)))
        new_dg_pool.ix[:,'dg_node'] = dg_q_end.ix[new_dg_pool.map.astype(np.int64).tolist(),'ptb'].values

        globalVars = update_global_vars(globalVars,'update dg_pool',newAddVar=new_dg_pool.drop(['map'],axis=1).reset_index(drop=True),newSubVar=False,replaceVar={'dg_id':dg_q_end_ids})
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt

    # find DG position if mid-route
    # df = dg_q_i[(dg_q_i['pta-t']>now) & (now<dg_q_i['ptb-t'])] # do not reset index as it is used later
    # if len(df.index)!=0:
    #     df['L'] = (now - df['pta-t'])*travel_speed
    #     df['dx'] = df['ptbx']-df['ptax']
    #     df['posx'] =  df.dx.map(lambda s: True if s>0 else False)
    #     df['dy'] = df['ptby']-df['ptay']
    #     df['posy'] =  df.dy.map(lambda s: True if s>0 else False)
    #     df['abs_dx'] = df.dx.map(lambda s: s if s>0 else -1*s)
    #     df['xonly'] =  df.abs_dx - df.L
    #     df['xonly'] = df.xonly.map(lambda s: True if s>=0 else False)
    #     df_xonly = df[df.xonly==True].reset_index(drop=True)
    #     if len(df_xonly.index)!=0:
    #
    #         df_xonly['dg_X'],df_xonly['dg_Y'] = np.empty((len(df_xonly.index),), dtype=np.intc),df_xonly['ptay'].values
    #         df_xonly_posInd = df_xonly[df_xonly.posx==True].index
    #         df_xonly_negInd = df_xonly.index - df_xonly_posInd
    #
    #         df_xonly.ix[df_xonly_posInd,'dg_X'] = df_xonly.ix[df_xonly_posInd,'ptax'] + df_xonly.ix[df_xonly_posInd,'L']
    #         df_xonly.ix[df_xonly_negInd,'dg_X'] = df_xonly.ix[df_xonly_negInd,'ptax'] - df_xonly.ix[df_xonly_negInd,'L']
    #
    #         df_xonly_ids = df_xonly.dg_id.astype(np.int64).values.tolist()
    #         new_dg_pool = dg_pool[dg_pool.dg_id.isin(df_xonly_ids)].reset_index(drop=True)
    #         new_dg_pool['map'] = new_dg_pool.dg_id.map(lambda s: df_xonly_ids.index(int(s)))
    #         new_dg_pool.ix[:,['dg_X','dg_Y']] = df_xonly.ix[new_dg_pool.map.astype(np.int64).tolist(),['ptax','ptay']].values
    #         globalVars = update_global_vars(globalVars,'update dg_pool',newAddVar=new_dg_pool.drop(['map'],axis=1).reset_index(drop=True),newSubVar=False,replaceVar={'id':df_xonly_ids})
    #         order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
    #         globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
    #
    #         df_xonly['zero'] = df_xonly.dx.map(lambda s: True if s==0 else False)
    #         if len(df_xonly[df_xonly.zero==True].index)>0:
    #             print 'check this in update location'
    #             systemError()
    #
    #     df_xy = df.ix[df.index - df_xonly.index,:]
    #     if len(df_xy.index)!=0:
    #         df_xy['dg_X'],df_xy['dg_Y'] = df_xy['ptbx'].values,np.empty((len(df_xy.index),), dtype=np.intc)
    #         # change L based on X-axis changes
    #         df_xy_posInd = df_xy[df_xy.posx==True].index
    #         df_xy_negInd = df_xy.index - df_xy_posInd
    #         df_xy.ix[df_xy_posInd,'L'] = df_xy.ix[df_xy_posInd,'L'] - df_xy.ix[df_xy_posInd,'dx']
    #         df_xy.ix[df_xy_negInd,'L'] = df_xy.ix[df_xy_negInd,'L'] + df_xy.ix[df_xy_negInd,'dx']
    #         # Determine Y-axis values
    #         df_xy_posInd = df_xy[df_xy.posy==True].index
    #         df_xy_negInd = df_xy.index - df_xy_posInd
    #         df_xy.ix[df_xy_posInd,'dg_Y'] = df_xy.ix[df_xy_posInd,'ptay'] + df_xy.ix[df_xy_posInd,'L']
    #         df_xy.ix[df_xy_negInd,'dg_Y'] = df_xy.ix[df_xy_negInd,'ptay'] - df_xy.ix[df_xy_negInd,'L']
    #         # Update dg_pool
    #         df_xy_ids = df_xy.dg_id.astype(np.int64).values.tolist()
    #         new_dg_pool = dg_pool[dg_pool.dg_id.isin(df_xy_ids)].reset_index(drop=True)
    #         new_dg_pool['map'] = new_dg_pool.dg_id.map(lambda s: df_xy_ids.index(int(s)))
    #         new_dg_pool.ix[:,['dg_X','dg_Y']] = df_xy.ix[new_dg_pool.map.astype(np.int64).tolist(),['ptax','ptay']].values
    #         globalVars = update_global_vars(globalVars,'update dg_pool',newAddVar=new_dg_pool.drop(['map'],axis=1).reset_index(drop=True),newSubVar=False,replaceVar={'id':df_xy_ids})
    #         order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
    #         globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt

    return globalVars

def update_global_vars(globalVars,varName,newAddVar=False,newSubVar=False,replaceVar={},errorCheck=False): # replaceVar={'id':10}
    order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

    def updatePerOrder(globalVars,newAddVar,newSubVar,replaceVar): # single dg_id
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
        order_addition,dg_q_addition = newAddVar,newSubVar
        dg_ID = replaceVar.values()[0]
        # replace order_q_i
        order_q = pd.merge(order_q[order_q['dg_id']!=dg_ID],order_addition,how='outer')
        order_q = order_q.reset_index(drop=True)
        # replace dg_q_i
        dg_q = pd.merge(dg_q[dg_q['dg_id']!=dg_ID],dg_q_addition,how='outer')
        dg_q = dg_q.reset_index(drop=True)
        # update dg_pool
        static_dg_pool = dg_pool[dg_pool['dg_id']!=dg_ID]
        dynamic_dg_pool = dg_pool[dg_pool['dg_id']==dg_ID].copy()

        order_id_group = order_addition.groupby(by='dg_id')
        dynamic_dg_pool['current_deliveries'] = dynamic_dg_pool.dg_id.map(lambda s: len(order_id_group.get_group(s)))
        dg_pool = pd.merge(static_dg_pool,dynamic_dg_pool,how='outer').astype(np.int64).reset_index(drop=True)
        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
        return globalVars
    def update_dg_pool(globalVars):
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

        order_grouped = order_q.groupby(by='dg_id')
        groupList = order_grouped.groups.keys()

        # update dg_pool.current_deliveries (if in order_q, updating currentDeliv)
        stat_dg_pool = dg_pool[dg_pool.dg_id.isin(groupList)==False]
        dyn_dg_pool = dg_pool.ix[dg_pool.index - stat_dg_pool.index]
        dyn_dg_pool.current_deliveries = dyn_dg_pool.dg_id.map(lambda s: len(order_grouped.get_group(s))).values
        dg_pool = pd.merge(stat_dg_pool,dyn_dg_pool,how='outer')

        # update dg_pool.current_deliveries (not in order_q, setting currentDeliv = 0)
        dyn_dg_pool = dg_pool[(dg_pool.dg_id.isin(groupList)==False) & (dg_pool.current_deliveries != 0)].copy()
        if len(dyn_dg_pool) != 0:
            stat_dg_pool = dg_pool.ix[dg_pool.index - dyn_dg_pool.index,:].copy()
            dyn_dg_pool['current_deliveries'] = 0
            dg_pool = pd.merge(stat_dg_pool,dyn_dg_pool,how='outer')

        # update dg_pool.total_delivered
        delivered_grouped = order_delivered.groupby(by='dg_id')
        groupList = delivered_grouped.groups.keys()
        stat_dg_pool = dg_pool[dg_pool.dg_id.isin(groupList)==False]
        dyn_dg_pool = dg_pool.ix[dg_pool.index - stat_dg_pool.index,:]
        dyn_dg_pool.total_delivered = dyn_dg_pool.dg_id.map(lambda s: len(delivered_grouped.get_group(s)))
        dg_pool = pd.merge(stat_dg_pool,dyn_dg_pool,how='outer')

        # DG Sort Order:
        # 1. all DG with totalDelivs != 0 (grouped least to most currentDelivs+total_delivered)
        # 2. remaining DG with zero totalDelivs

        dg_pool['total'] = dg_pool['current_deliveries'] + dg_pool['total_delivered']
        dg_pool = dg_pool[dg_pool.total!=0].sort_index(by=['total','total_delivered'],ascending=[True,True]).append(dg_pool[dg_pool.total==0].sort_index(by='total',ascending=True)).drop(['total'],axis=1).reset_index(drop=True)

        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
        return globalVars
    def updatePerMinute(globalVars,now):
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

        # check for orders completed at t=now, if any
        full_completedOrders=order_q[order_q.end_time <= now]
        clean_completedOrders=full_completedOrders[full_completedOrders.status!='on route']
        orders_dg_ids = clean_completedOrders.deliv_id.unique().tolist()
        # orders_del_ids = clean_completedOrders.deliv_id.unique().tolist()
        # df = pd.DataFrame({'orders':orders_del_ids})
        # df['ids'] = df.orders.map(lambda s: clean_completedOrders[clean_completedOrders.deliv_id==s].id.astype(np.int64).tolist()[0])
        # order_del_dg_dict = dict(zip(df.orders.astype(np.int64).values,df.ids.astype(np.int64).values))

        # update location for all DG
        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
        globalVars = updateCurrentLocation(globalVars,now,orders_dg_ids)
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

        # update --> dg_pool (current_deliveries, total_delivered)
        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
        globalVars = update_dg_pool(globalVars)
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

        # nothing (else) to update
        if len(clean_completedOrders.index) == 0: return globalVars

        # check for errors
        # check_orders = clean_completedOrders
        if errorCheck == True: error_check(order_q_i=clean_completedOrders,dg_q_i=None,arg3='sim_data')

        # update --> order delivered and order_q
        order_delivered = pd.merge(order_delivered,full_completedOrders,how='outer').sort_index(by=['deliv_id','start_time'], ascending=[True,True]).reset_index(drop=True)
        order_q = order_q.ix[order_q.index - full_completedOrders.index,:].sort_index(by=['deliv_id','start_time'], ascending=[True,True]).reset_index(drop=True)

        # update --> dg_q delivered
        deliveries_completed = dg_q[dg_q['ptb-t']<=now]
        dg_delivered = pd.merge(dg_delivered,deliveries_completed,how='outer').reset_index(drop=True)

        # update --> dg_q
        dg_q = dg_q[dg_q['ptb-t']>now]

        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
        return globalVars

    if varName == 'update per order':
        globalVars = updatePerOrder(globalVars,newAddVar,newSubVar,replaceVar)
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

    elif varName == 'update per minute':
        globalVars = updatePerMinute(globalVars,newAddVar)
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

    elif varName == 're-pool':
        dg_pool_pt+=1
        if type(newSubVar)!=False: repool_size = newSubVar
        else: repool_size = A.DG_pool_grp_size
        dg_pool = init_dg_pool(pt=dg_pool_pt,dg_grp_size=repool_size,old_dg_pool=dg_pool,load=A.reuse_dg_pool,save=False,filePath='')
        print 'new dg_pool = ',dg_pool_pt

    elif varName == 'update dg_pool':
        VarKey,oldVarValue = replaceVar.keys()[0],replaceVar.values()[0]
        if type(oldVarValue) == list:  dg_pool = pd.merge(dg_pool[(dg_pool[VarKey].isin(oldVarValue)==False)],newAddVar,how='outer')
        else:  dg_pool = pd.merge(dg_pool[dg_pool[VarKey]!=oldVarValue],newAddVar,how='outer')
        dg_pool = dg_pool.reset_index(drop=True)

    elif varName == 'organize dg_pool':
        globalVars = update_dg_pool(globalVars)
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

    else:
        print 'why not accounted for in updating?'
        systemError()

    if dg_pool.dg_node.fillna(99).tolist().count(99)!=0:
        print 'hold up - check your global vars'
        systemError()

    globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
    return globalVars
