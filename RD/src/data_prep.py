from rd_lib import pd,np,MODEL_dg_pool,NoneType
import assumptions as A
from pg_fxs import pg_get_travel_dist
from utility_and_permutation_fxs import get_all_node_combo_dist_miles

def get_node_combos_and_times(new,order_q_grp,dg_grp,dg_grp_ids):
    new_nodes   = new[['start_node','end_node']].astype(int).tolist()
    order_nodes = order_q_grp.ix[:,['start_node','end_node']].astype(int).as_matrix().flatten().tolist()
    all_nodes   = new_nodes + order_nodes
    uniq_nodes  = np.unique(all_nodes).tolist()
    z           = get_all_node_combo_dist_miles(uniq_nodes,clean=True)
    zx          = ''
    for it in dg_grp_ids:
        dg_nodes        = np.unique(new_nodes + order_q_grp[order_q_grp.dg_id==it].ix[:,['start_node','end_node']].astype(int).as_matrix().flatten().tolist()).tolist()
        z_tmp           = z[(z.A.isin(dg_nodes)==True)&(z.B.isin(dg_nodes))]
        z_tmp['dg_id']  = it
        if type(zx) == str:     zx = z_tmp.copy()
        else:                   zx = zx.append(z_tmp,ignore_index=True)
    p1_arr,p2_arr,dist,minutes,these_dg_ids = list(zip(*zx.as_matrix()))
    p1_arr = np.ascontiguousarray(map(lambda s: int(s),p1_arr),dtype=np.intc)
    p2_arr = np.ascontiguousarray(map(lambda s: int(s),p2_arr),dtype=np.intc)
    these_dg_ids = np.ascontiguousarray(map(lambda s: int(s),these_dg_ids),dtype=np.intc)
    minutes = np.ascontiguousarray(list(minutes),dtype=np.float)
    return p1_arr,p2_arr,minutes,these_dg_ids
def set_mock_pts(new_dg_q):
    # create dictionary associating deliv_ids with mock_pts (based on pickup locations)
    #   then, iterate through rows of new_dg_q and update dict with new mock_pts for each new deliv_id
    all_del_ids = new_dg_q.deliv_id.astype(np.int64).tolist()
    unique_del_ids = new_dg_q.deliv_id.astype(np.int64).unique().tolist()
    id_mock_pt_dict = dict(zip(unique_del_ids,range(0,len(unique_del_ids))))
    counter_list = [all_del_ids[:i].count(all_del_ids[i]) for i in range(0,len(all_del_ids))]
    new_mock_pts = [100+id_mock_pt_dict[all_del_ids[i]] if (counter_list[i]==1 or all_del_ids.count(all_del_ids[i])==1) else id_mock_pt_dict[all_del_ids[i]] for i in range(0,len(all_del_ids))]
    new_dg_q['mock_pt'] = new_mock_pts
    return new_dg_q
def order_q_re_order_deliv_num(order_q_i):
    pta = order_q_i[order_q_i.status=='on route']
    pta.deliv_num = 0
    ptb = order_q_i[order_q_i.status!='on route'].sort_index(by='start_time', ascending=True).reset_index(drop=True)
    ptb.deliv_num = range(1,len(ptb.index)+1)
    order_q_i = pd.merge(pta,ptb,how='outer').sort_index(by='deliv_num', ascending=True).reset_index(drop=True)
    return order_q_i
def getComboStartInfo(new,order_q_i):
    """
    Defining:
        x == new['order_time'] == now
        start,end == start_time,end_time

    Then:
        If x>start & x>end: ignore (which should have been cleared from queue and are not considered here)
        If x>start & x=end: ignore (which should have been cleared from queue and are not considered here)
        If x>start & x<end: use end points only
        If x=start & x<end: use end points only
        If x<start & x<end: use both points

    DG's potential new trip will start at the next location DG arrives (at least t=t+1)
    tripStartPts and tripStartTime are the points at the next location and the arrival time
    """

    start_loc=new['start_node']
    end_loc=new['end_node']

    if len(order_q_i[order_q_i.end_time>new['order_time']].index)==0:
        tripStartTime,tripStartPt = new['order_time'],start_loc
        bestComboVars = 1,tripStartTime,tripStartPt,None,None
        return bestComboVars

    partial_check_orders = order_q_i[(order_q_i['start_time']<=new['order_time']) & (new['order_time']<order_q_i['end_time'])].reset_index(drop=True)
    full_check_orders = order_q_i[(new['order_time']<order_q_i['start_time']) & (new['order_time']<order_q_i['end_time'])].reset_index(drop=True)
    # partial_check_orders = order_q_i[(order_q_i['start_time']<=new['order_time']) & (new['order_time']<order_q_i['end_time'])].sort_index(by='end_time',ascending=True).reset_index(drop=True)
    # full_check_orders = order_q_i[(new['order_time']<order_q_i['start_time']) & (new['order_time']<order_q_i['end_time'])].sort_index(by='start_time',ascending=True).reset_index(drop=True)

    # get trip start time and start point
    sTimes = order_q_i.start_time.astype(np.int64).tolist()
    eTimes = order_q_i.end_time.astype(np.int64).tolist()
    aTimes = np.array(sorted(sTimes+eTimes))
    tripStartTime = aTimes[np.where(aTimes>new['order_time'])[0][0]]
    if sTimes.count(tripStartTime)!=0: tripStartPt = order_q_i.ix[sTimes.index(tripStartTime),'start_node'].astype(np.int64).tolist()
    else: tripStartPt = order_q_i.ix[eTimes.index(tripStartTime),'end_node'].astype(np.int64).tolist()

    # get trip points from partial orders (as well as delivery IDs and order times)
    # a = partial_check_orders.ix[:,['end_X','end_Y']].astype(np.int64).values
    # b = np.array([[a.T[0],a.T[1]],[a.T[0],a.T[1]]]).T
    # c = []
    # for it in b: c.extend(it.T.tolist())
    tripPoints = partial_check_orders.ix[:,'end_node'].astype(np.int64).tolist()
    tripDeliveryIDs = partial_check_orders.deliv_id.astype(np.int64).tolist()
    tripOrderTimes = partial_check_orders.order_time.astype(np.int64).tolist()

    # add trip points from full orders
    a = full_check_orders.ix[:,['start_node','end_node']].astype(np.int64).values.tolist()
    # b = np.array([[a.T[0],a.T[1]],[a.T[2],a.T[3]]]).T
    # c = []
    # for it in b: c.extend(it.T.tolist())
    tripPoints.extend(a)
    tripDeliveryIDs.extend(full_check_orders.deliv_id.astype(np.int64).tolist())
    tripOrderTimes.extend(full_check_orders.order_time.astype(np.int64).tolist())

    # append new order info
    tripPoints.extend([start_loc,end_loc])
    tripPoints = np.ascontiguousarray(np.array(tripPoints,dtype=np.intc),dtype=np.intc)
    tripDeliveryIDs.append(new['deliv_id'])
    tripOrderTimes.append(new['order_time'])

    bestComboVars = tripPoints,tripStartTime,tripStartPt,tripDeliveryIDs,tripOrderTimes
    return bestComboVars
def format_new_to_order(new,order_q):
    A = order_q.ix[:-1,:]
    cols = ['deliv_id','order_time','start_X','start_Y','end_X','end_Y']
    B = A.append(pd.Series({'deliv_id':new[4],
                                'order_time':new[5],
                                'start_X':new[6],
                                'start_Y':new[7],
                                'end_X':new[8],
                                'end_Y':new[9]},
                               index=cols),ignore_index=True).fillna(0)
    return B
def set_dg_pool_order(globalVars,new):
    """ the DG_Pool order is important to quickly finding best DG.
        DG not fitting criteria are excluded from analysis.
        the remaining DG are grouped"""
    order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

    # 1) ineligible per conditions
    # 2) each DG that has not started making deliveries yet or has finished with deliveries --> sorted by total_delivered
    # 3) each DG already making deliveries
    maxed_out_dg = dg_pool[(dg_pool.current_deliveries>=A.max_delivery_per_dg)]
    potentialDG = dg_pool.ix[dg_pool.index - maxed_out_dg.index,:]
    dg_node_list = potentialDG.dg_node.astype(np.int).tolist()
    trav_dist_list = pg_get_travel_dist(int(new['start_node']),dg_node_list)
    trav_dist_dict = dict(zip(dg_node_list,trav_dist_list))
    # TODO rework sql to produce dictionary instead of bare list
    potentialDG['travel_dist_to_loc'] = potentialDG.dg_node.map(trav_dist_dict)
    potentialDG['travel_time_to_loc'] = potentialDG.travel_dist_to_loc.map(lambda s: round((s * (60.0/A.MPH)),0) )
    singleTripTime = round(pg_get_travel_dist(int(new['start_node']),int(new['end_node'])) * (60.0/A.MPH),1)
    potentialDG['travel_time'] = potentialDG.dg_node.map(lambda s: singleTripTime)
    potentialDG['total_travel_time'] = potentialDG.travel_dist_to_loc.map(lambda s: round( (s * (60.0/A.MPH)) + singleTripTime,1) )
    potentialDG['dest_node'] = new['end_node']

    potentialDG = potentialDG[ potentialDG.total_travel_time <= A.max_delivery_time ].drop(['travel_dist_to_loc'],axis=1)

    startingDG = potentialDG[(potentialDG.current_deliveries==0)]
    working_DG =  potentialDG.ix[potentialDG.index - maxed_out_dg.index - startingDG.index,:]

    # unusedDG = dg_pool.ix[dg_pool.index - maxed_out_dg.index - startingDG.index - working_DG.index,:]
    # if len(unusedDG.index)!=0:
    #     print '\nUn-Used DG in DG Pool\n',unusedDG
    #     systemError()


    # 2) each DG that has not started making deliveries yet or has finished with deliveries --> sorted by total_delivered
    if len(startingDG.index)!=0:
        startingDG['closeby'] = startingDG.total_travel_time.map(lambda s: True if s<=A.max_travelToLocTime else False) # i.e., within proximity condition
        dropCols = ['closeby']
        avail_startingDG = startingDG[(startingDG.closeby==True)].drop(dropCols,axis=1)
        avail_startingDG = avail_startingDG.sort_index(by=['total_travel_time'], ascending=[True]).reset_index(drop=True)
    else: avail_startingDG = MODEL_dg_pool.copy()

    # 3) each DG already making deliveries
    if len(working_DG.index)!=0:
        working_DG['closeby'] = working_DG.travel_time.map(lambda s: True if s<=A.max_travelToLocTime else False) # i.e., within proximity condition
        dropCols = ['closeby']
        avail_working_DG = working_DG[(working_DG.closeby==True)].drop(dropCols,axis=1)
        avail_working_DG = avail_working_DG.sort_index(by=['total_delivered','current_deliveries','travel_time'], ascending=[False,False,True]).reset_index(drop=True)
    else: avail_working_DG = MODEL_dg_pool.copy()


    if len(avail_working_DG.index)+len(avail_startingDG.index)==0:
        import embed_ipython as I; I.embed()
        return [],None,'re-pool'
    elif len(avail_working_DG.index)==0:
        return [],avail_startingDG.ix[:0,:],'OK'
    else:
        dg_groups = []
        if len(avail_working_DG.index) < A.DG_pool_grp_part_size:
            dg_groups.append(avail_working_DG.append(avail_startingDG.ix[:0,:],ignore_index=True))
            free_dg = avail_startingDG.ix[1:1,:]
            return dg_groups,free_dg,'OK'
        else:
            dg_pool_parts = int(round(len(avail_working_DG.index)/float(A.DG_pool_grp_part_size)))
            for i in range(0,dg_pool_parts):
                if i==(dg_pool_parts-1):
                    dg_groups.append(avail_working_DG.ix[i*A.DG_pool_grp_part_size:,:].reset_index(drop=True))
                else:
                    dg_groups.append(avail_working_DG.ix[i*A.DG_pool_grp_part_size:((i+1)*A.DG_pool_grp_part_size)-1,:].reset_index(drop=True))
            free_dg = avail_startingDG.ix[:0,:]
            return dg_groups,free_dg,'OK'

        # avail_grps = avail_working_DG.groupby(by='current_deliveries')
        # grp_list = avail_grps.groups.keys()
        # tmp_dg_groups = [avail_grps.get_group(it).sort_index(by=['total_delivered','travel_time'], ascending=[False,True]).reset_index(drop=True) for it in grp_list]
        # dg_groups = []
        # for it in tmp_dg_groups:
        #     dg_pool_parts = int(round(len(it.index)/float(A.DG_pool_grp_part_size)))
        #     if dg_pool_parts==0: dg_groups.append(it)
        #     else:
        #         for i in range(0,dg_pool_parts):
        #             if i==(dg_pool_parts-1): dg_groups.append(it.ix[i*A.DG_pool_grp_part_size:,:].reset_index(drop=True))
        #             else: dg_groups.append(it.ix[i*A.DG_pool_grp_part_size:((i+1)*A.DG_pool_grp_part_size)-1,:].reset_index(drop=True))
        # dg_groups.append(avail_startingDG.ix[:0,:])

    return dg_groups,free_dg,'OK'
# def set_dg_pool_grp_order(globalVars,newOrders):
#     order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
#     model_dg_pool_grp = pd.DataFrame(columns=['id', 'dg_X', 'dg_Y', 'total_delivered', 'current_deliveries','travel_time','total_travel_time'])
#     dg_pool = dg_pool.sort_index(by='id',ascending=True)
#
#     dgp_grp_indicies = []
#     for i in range(0,len(newOrders)):
#         new = newOrders.ix[i,:]
#         # constant variables:
#         singleTripTime = pd_get_travel_time(new['start_X'],new['start_Y'],new['end_X'],new['end_Y'])
#         # 1) ineligible per conditions
#         # 2) each DG that has not started making deliveries yet or has finished with deliveries --> sorted by total_delivered
#         # 3) each DG already making deliveries
#         maxed_out_dg = dg_pool[(dg_pool.current_deliveries>=A.max_delivery_per_dg)]
#         startingDG = dg_pool[(dg_pool.current_deliveries==0)]
#         working_DG =  dg_pool.ix[dg_pool.index - maxed_out_dg.index - startingDG.index,:]
#
#         # 2) each DG that has not started making deliveries yet or has finished with deliveries --> sorted by total_delivered
#         if len(startingDG.index)!=0:
#             startingDG['travel_time']=startingDG[['dg_X','dg_Y']].apply(lambda s: pd_get_travel_time(new['start_X'],new['start_Y'],*s),axis=1)
#             startingDG['total_travel_time'] = startingDG['travel_time'] + singleTripTime
#             startingDG['closeby'] = startingDG.travel_time.map(lambda s: True if s<=A.max_travelToLocTime else False) # i.e., within proximity condition
#             startingDG['timely'] = startingDG.total_travel_time.map(lambda s: True if s<=A.max_delivery_time else False) # i.e., within delivery time condition
#             dropCols = ['closeby','timely']
#             avail_startingDG = startingDG[(startingDG.timely==True) & (startingDG.closeby==True)].drop(dropCols,axis=1)
#             avail_startingDG = avail_startingDG.sort_index(by=['total_delivered','travel_time'], ascending=[False,True])
#         else: avail_startingDG = model_dg_pool_grp.ix[:-1,:]
#
#         # 3) each DG already making deliveries
#         if len(working_DG.index)!=0:
#             working_DG['travel_time']=working_DG[['dg_X','dg_Y']].apply(lambda s: pd_get_travel_time(new['start_X'],new['start_Y'],*s),axis=1)
#             working_DG['total_travel_time'] = working_DG['travel_time'] + singleTripTime
#             working_DG['closeby'] = working_DG.travel_time.map(lambda s: True if s<=A.max_travelToLocTime else False) # i.e., within proximity condition
#             working_DG['timely'] = working_DG.total_travel_time.map(lambda s: True if s<=A.max_delivery_time else False) # i.e., within delivery time condition
#             dropCols = ['closeby','timely']
#             avail_working_DG = working_DG[(working_DG.timely==True) & (working_DG.closeby==True)].drop(dropCols,axis=1)
#             avail_working_DG = avail_working_DG.sort_index(by=['total_delivered','current_deliveries','travel_time'], ascending=[False,False,True])
#         else: avail_working_DG = model_dg_pool_grp.ix[:-1,:]
#
#         dgp_grp,dgp_cnt = [],[]
#
#         if len(avail_working_DG.index)+len(avail_startingDG.index)==0:
#
#             globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
#             # set re-pool size here, use newSubVar as variable for number of new DG
#             globalVars = update_global_vars(globalVars,'re-pool',newAddVar=False,newSubVar=False,replaceVar={})
#             dg_pool = globalVars[4]
#
#             startingDG = dg_pool[(dg_pool.current_deliveries==0)]
#             startingDG['travel_time']=startingDG[['dg_X','dg_Y']].apply(lambda s: pd_get_travel_time(new['start_X'],new['start_Y'],*s),axis=1)
#             startingDG['total_travel_time'] = startingDG['travel_time'] + singleTripTime
#             startingDG['closeby'] = startingDG.travel_time.map(lambda s: True if s<=A.max_travelToLocTime else False) # i.e., within proximity condition
#             startingDG['timely'] = startingDG.total_travel_time.map(lambda s: True if s<=A.max_delivery_time else False) # i.e., within delivery time condition
#             dropCols = ['closeby','timely']
#             avail_startingDG = startingDG[(startingDG.timely==True) & (startingDG.closeby==True)].drop(dropCols,axis=1)
#             avail_startingDG = avail_startingDG.sort_index(by=['total_delivered','travel_time'], ascending=[False,True])
#
#             dgp_cnt.append( avail_startingDG.index[0] )
#
#         elif len(avail_working_DG.index)==0:
#
#             dgp_cnt.append( avail_startingDG.index[0] )
#
#         else:
#
#             dgp_cnt.append( avail_startingDG.index[0] )
#
#             dg_pool_parts = int(round(len(avail_working_DG.index)/float(A.DG_pool_grp_part_size)))
#             if dg_pool_parts==0:
#                 single_grp = avail_working_DG.index
#                 dgp_cnt.append(len(single_grp))
#                 dgp_grp.append( single_grp )
#
#             else:
#                 for i in range(0,dg_pool_parts):
#
#                     if i==(dg_pool_parts-1):
#                         grp = avail_working_DG.ix[i*A.DG_pool_grp_part_size:,:].index
#                         dgp_cnt.append(len(grp))
#                         dgp_grp.append( grp )
#
#                     else:
#                         grp = avail_working_DG.ix[i*A.DG_pool_grp_part_size:((i+1)*A.DG_pool_grp_part_size)-1,:].index
#                         dgp_cnt.append(len(grp))
#                         dgp_grp.append( grp )
#
#         dgp_grp_indicies.append([dgp_cnt,dgp_grp])
#
#             # avail_grps = avail_working_DG.groupby(by='current_deliveries')
#             # grp_list = avail_grps.groups.keys()
#             # tmp_dg_groups = [avail_grps.get_group(it).sort_index(by=['total_delivered','travel_time'], ascending=[False,True]).reset_index(drop=True) for it in grp_list]
#             # dg_groups = []
#             # for it in tmp_dg_groups:
#             #     dg_pool_parts = int(round(len(it.index)/float(A.DG_pool_grp_part_size)))
#             #     if dg_pool_parts==0: dg_groups.append(it)
#             #     else:
#             #         for i in range(0,dg_pool_parts):
#             #             if i==(dg_pool_parts-1): dg_groups.append(it.ix[i*A.DG_pool_grp_part_size:,:].reset_index(drop=True))
#             #             else: dg_groups.append(it.ix[i*A.DG_pool_grp_part_size:((i+1)*A.DG_pool_grp_part_size)-1,:].reset_index(drop=True))
#             # dg_groups.append(avail_startingDG.ix[:0,:])
#
#     # this function returns a 3D list.
#     # for each order,
#     #   the first list starts with the index of the free DG and then
#     #       provides the count for each of the subsequent groups
#     #   the second list is the index of the first group
#     #   the third list is the index for the second group
#     #   etc...
#
#     globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
#     return globalVars, dgp_grp_indicies
