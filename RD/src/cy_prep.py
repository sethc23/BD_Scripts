from rd_lib import pd,np,NoneType
import var_global as G
from handle_results import pull_from_order,compare_orders
from assumptions import max_delivery_per_dg
from assumptions import max_travelToStartLocTime as mttlt
from data_prep import get_node_combos_and_times
from cy_scratch import N_getBestDG
# from cy_lib import c_getBestDG


# Cython Prep f(x)s
def c_check5(globalVars,dg_grp,new,checkOrder='',errorCheck=True):
    # order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
    order_q = globalVars[0]
    D       = globalVars[1]                         # orders delivered

    # TODO account for case where additional order for same vendor occurs prior to first pickup

    order_q_grp = order_q.ix[:-1,:]
    dg_grp_ids = dg_grp.dg_id.unique().tolist()     # the order of IDs is paramount
    for it in dg_grp_ids:
        order_q_grp = order_q_grp.append(order_q[(order_q.dg_id==it)].sort_index(by='start_time',ascending=True))

    # print '\nGroup:\n',grp
    # print '\nDeliveryID =',new['deliv_id'],'- Group IDs =',grp_ids
    # print '\norders being considered\n',order_q_grp.append(format_new_to_order(new,order_q))

    new_ord_cols= ['order_time','deliv_id','start_node','end_node']

    ord_grp_cols= ['order_time','deliv_id','dg_id','dg_node','travel_time_to_loc',
                   'start_node','start_time','travel_time','end_time','end_node','total_order_time']

    dg_grp_cols = ['dg_id','dg_node','current_deliveries','travel_time_to_loc','travel_time','total_travel_time']

    c_new       = np.ascontiguousarray(new[new_ord_cols].astype(np.float_),dtype=np.float_)
    c_ord_grp   = np.ascontiguousarray(order_q_grp.ix[:,ord_grp_cols].astype(np.float_).as_matrix(),dtype=np.float_)
    c_dg_grp_ids= np.ascontiguousarray(dg_grp_ids,dtype=np.intc)
    c_dg_grp    = np.ascontiguousarray(dg_grp.ix[:,dg_grp_cols].astype(np.float_).as_matrix(),dtype=np.float_)

    p1_arr,p2_arr,minutes,dg_id_arr = get_node_combos_and_times(new,order_q_grp,dg_grp,dg_grp_ids)
    minutes     = np.ascontiguousarray(minutes,dtype=np.float_)

    # if c_dg_grp_ids.shape[0]==3:
    #     print '\n\n',new[new_ord_cols]
    #     print '\n\n',order_q_grp.ix[:,ord_grp_cols]
    #     print '\n\n',dg_grp.ix[:,dg_grp_cols],'\n'
    #     import embed_ipython as I; I.embed()

    # import embed_ipython as I; I.embed()
    #c_vars = c_getBestDG( c_new,
    c_vars = N_getBestDG( c_new,
                          c_ord_grp,
                          c_dg_grp_ids,
                          c_dg_grp,
                          p1_arr,
                          p2_arr,
                          dg_id_arr,
                          minutes,
                          G.c_deliv_ids,
                          G.c_order_times,
                          G.c_max_delivery_time, # a.k.a., "md"
                          G.c_mttlt,
                          G.c_tripPoints,
                          G.c_ptPairSet,
                          G.c_tmp_minutes,
                          G.c_orderSet2,
                          G.c_orderSet3,
                          G.c_orderSet4,
                          G.c_orderSet5,
                          G.c_orderSetInd,
                          G.c_realCombos,
                          G.c_travel_times,
                          G.c_start_times,
                          G.c_end_times,
                          G.c_odtTimes,
                          G.c_oMaxTimes,
                          G.c_tMaxTimes,
                          G.c_tddTimes,
                          G.c_ctMarker,
                          G.c_rv_comboStartInfo,
                          G.c_rv_bestCombo,
                          G.c_returnVars)

    c_rows = c_vars.shape[0]
    if c_vars[c_rows-1][11] != 0:
        order_q_i = pd.DataFrame(np.asarray(c_vars),columns=[   'order_time', 'deliv_id', 'dg_id', 'dg_node', \
                                                                'travel_time_to_loc', 'start_node', 'start_time', \
                                                                'travel_time', 'end_time', 'end_node', \
                                                                'total_order_time', 'status'])

        order_q_i['status']  = order_q_i.status.map(lambda s: 'on deck')
        if type(checkOrder) != str and type(checkOrder) != NoneType:    compare_orders(checkOrder,order_q_i)
        DG_ID           = order_q_i.dg_id.tolist()[0]
        earliestStart   = order_q_grp.start_time.astype(np.int_).min()
        check_order_q_i = order_q_i.append(D[(D.dg_id==DG_ID) & (D.end_time>earliestStart)])
        dg_q_i          = pull_from_order(check_order_q_i,errorCheck=errorCheck)
        updated         = True
        return updated,order_q_i,dg_q_i
    else:
        updated         = False
        return updated,None,None
def c_check4(new,order_q_i,check_order_result=''):

    # from cython_exts.get_combo_start_info import c_get_combo_start_info

    take_cols = ['deliv_id','order_time','start_node','end_node']
    c_new = np.ascontiguousarray(new[take_cols].astype(np.intc).tolist(),dtype=np.intc)

    take_cols = ['deliv_id','order_time','start_time','start_node','end_time','end_node']
    c_order_q_i = np.ascontiguousarray(order_q_i.ix[:,take_cols].astype(np.intc).as_matrix(),dtype=np.intc)
    r = len(order_q_i[new['order_time']<order_q_i.end_time])
    c_returnVar = np.ascontiguousarray(np.empty((r+1,6), dtype=np.intc,order='C'))

    c_new = np.ascontiguousarray(new.astype(np.intc).tolist(),dtype=np.intc)
    c_order_q_i = np.ascontiguousarray(order_q_i.drop(['status','ave_X','ave_Y'],axis=1).astype(np.intc).as_matrix(),dtype=np.intc)
    d = len(order_q_i[order_q_i.end_time>new['order_time']])+1
    int_vars = np.asarray([d,travel_speed,max_delivery_time,max_travelToLocTime],dtype=np.intc)
    c_delivery_count,c_speed,c_max_delivery_time,c_mttlt = int_vars[0],int_vars[1],int_vars[2],int_vars[3]

    c_tripPoints = np.ascontiguousarray(np.empty((d*2,2), dtype=np.intc,order='C'), dtype=np.intc)
    c_deliv_ids = np.ascontiguousarray(np.empty((d,), dtype=np.intc,order='C'), dtype=np.intc)
    c_order_times = np.ascontiguousarray(np.empty((d,), dtype=np.intc,order='C'), dtype=np.intc)
    c_returnVar = np.ascontiguousarray(np.empty((d,14), dtype=np.intc,order='C'), dtype=np.intc)

    if d < max_delivery_per_dg: testSet = orderSet[orderSet['mc'+str(d)]==True].reset_index(drop=True)
    else: testSet = orderSet

    c_orderSortKey = np.ascontiguousarray(testSet.ix[:,'i0':'i'+str(d-1)].astype(np.intc).as_matrix(),dtype=np.intc)
    c_ptsSortKey = np.ascontiguousarray(testSet.ix[:,'a1':ABC[d-1].lower()+'2'].astype(np.intc).as_matrix(),dtype=np.intc)
    points = testSet.ix[:,'pt0':'pt'+str(d*2-1)]
    c_mockCombos = np.ascontiguousarray(points.astype(np.intc).as_matrix(),dtype=np.intc)
    r,c = c_mockCombos.shape
    c_realCombos = np.empty((r,c,2),dtype=np.intc,order='C')

    test_pt = len(testSet.index)
    c_global_vars = (c_travel_times[:test_pt],c_start_times[:test_pt],c_end_times[:test_pt],c_odtTimes[:test_pt],
                     c_oMaxTimes[:test_pt],c_tMaxTimes[:test_pt],c_tddTimes[:test_pt],c_ctMarker[:test_pt],c_returnVars[:r])

    c_travel_times_r,c_start_times_r,c_end_times_r,c_odtTimes_r,c_oMaxTimes_r,c_tMaxTimes_r,c_tddTimes_r,c_ctMarker_r,c_returnVars_r = c_global_vars

    c_vars = c_bestED(c_new,
                      c_order_q_i,
                      c_delivery_count,
                      c_deliv_ids,
                      c_order_times,
                      c_speed,
                      c_max_delivery_time,
                      c_mttlt,
                      c_tripPoints,
                      c_mockCombos,
                      c_realCombos,
                      c_orderSortKey,
                      c_ptsSortKey,
                      c_travel_times_r,
                      c_start_times_r,
                      c_end_times_r,
                      c_odtTimes_r,
                      c_oMaxTimes_r,
                      c_tMaxTimes_r,
                      c_tddTimes_r,
                      c_ctMarker_r,
                      c_returnVars_r,
                      c_returnVar)

    if c_vars[0][13] != 0:   # (general error | error setting best index)
        c_order_q_i = pd.DataFrame([[col for col in row] for row in c_vars],columns=['dg_X','dg_Y','deliv_num','deliv_id','order_time','travel_time_to_loc','start_X','start_Y','start_time','travel_time','end_time','end_X','end_Y','total_order_time','bestIndex'])
        c_order_q_i = c_order_q_i.drop('bestIndex',axis=1).reset_index(drop=True)

        # add in extra info and organize columns
        results_with_dg_format = pd.merge(order_q_i,c_order_q_i,how='right')
        fillColumns =['id','dg_X','dg_Y','ave_X','ave_Y','status']
        results_with_dg_format[fillColumns] = order_q_i.reset_index(drop=True).ix[0,fillColumns[:-1]].tolist() + ['on deck']
        c_order_q_results = results_with_dg_format.reset_index(drop=True)
        c_order_q_results.columns = order_q_i.columns

        # re-adjust delivery numbers (resulting from partial trip analysis) and error check
        new_order_q_i = order_q_re_order_deliv_num(c_order_q_results)
        now = new['order_time']
        check_order_q_i = new_order_q_i.append(order_q_i[order_q_i.end_time<=now]).sort_index(by='start_time',ascending=True).reset_index(drop=True)
        if errorCheck == True: error_check(order_q_i=check_order_q_i,dg_q_i=None,arg3='sim_data')

        check_dg_q_i = pull_from_order(check_order_q_i,errorCheck=False) # false here because it would duplicate part of the above check
        new_dg_q_i = check_dg_q_i[check_dg_q_i['ptb-t']>now]

    else:
        if c_vars[1][13] == 505:
            print 'c_check4 -- error with data:  trouble setting best index'
            systemError()
        else: new_order_q_i,new_dg_q_i = None,None



    if str(check_order_result) == '': return new_order_q_i,new_dg_q_i
    else:
        if type(check_order_result) == type(new_order_q_i) and type(new_order_q_i) == NoneType: return
        else: return compare_orders(check_order_result,new_order_q_i,order_q_i)
def c_check3(new,order_q_i,tripStartPt,tripStartTime,check_order_results=''):

    # import embed_ipython as I; I.embed();

    c_new = np.ascontiguousarray(new.astype(np.intc).tolist(),dtype=np.intc)
    c_order_q_i = np.ascontiguousarray(order_q_i.drop(['status','ave_X','ave_Y'],axis=1).astype(np.intc).as_matrix(),dtype=np.intc)
    c_tripStartPtX = long(tripStartPtX)
    c_tripStartPtY = long(tripStartPtY)
    c_tripStartTime = long(tripStartTime)
    c_speed = long(travel_speed)
    c_max_delivery_time = long(max_delivery_time)
    r = len(order_q_i[order_q_i.end_time>new['order_time']])+1 # how is this being set?
    print 'check c_check3'
    systemError()
    c_returnVar = np.ascontiguousarray(np.empty((r,14), dtype=np.intc,order='C'), dtype=np.intc)

    c_order_result = c_eval_single_order(c_new,c_order_q_i,c_tripStartPtX,c_tripStartPtY,
                                   c_tripStartTime,c_speed,c_max_delivery_time,c_returnVar)
    new_order_result = pd.DataFrame(np.asarray(c_order_result).T,columns=order_q_i.columns)
    if str(check_order_result) == '': return new_order_result
    else: return compare_orders(check_order_results,new_order_result,order_q_i)
def c_check2(order_q_i,order_results,new,check_order_results=''):
    now = new['order_time']
    c_order_q_i = np.ascontiguousarray(order_q_i.drop(['status','ave_X','ave_Y'],axis=1).astype(np.intc).as_matrix(),dtype=np.intc)
    c_order_results = np.ascontiguousarray(order_results.astype(np.intc).as_matrix(),dtype=np.intc)
    c_now = long(now)
    c_order_results = c_update_order_results(c_order_q_i,c_order_results,c_now)
    new_order_results = pd.DataFrame(np.asarray(c_order_results),columns=order_results.columns)
    if str(check_order_results) == '': return new_order_results
    else: return compare_orders(check_order_results,new_order_results,order_q_i)
def c_check1(new,order_q_i,bestComboVars=''):
    from cython_exts.get_combo_start_info import c_get_combo_start_info

    take_cols = ['deliv_id','order_time','start_node','end_node']
    c_new = np.ascontiguousarray(new[take_cols].astype(np.intc).tolist(),dtype=np.intc)
    take_cols = ['deliv_id','order_time','start_time','start_node','end_time','end_node']
    c_order_q_i = np.ascontiguousarray(order_q_i.ix[:,take_cols].astype(np.intc).as_matrix(),dtype=np.intc)
    r = len(order_q_i[new['order_time']<order_q_i.end_time])
    c_returnVar = np.ascontiguousarray(np.empty((r+1,6), dtype=np.intc,order='C'))

    #import embed_ipython as I; I.embed()

    c_returnVar = c_get_combo_start_info(c_new,c_order_q_i,c_returnVar)

    if c_returnVar[0][5] == -1:
        print '\nonly single order'
        tripStartTime,tripStartPt = new['order_time'],new['start_node']
        bestComboVars = 1,tripStartTime,tripStartPt,None,None
        return bestComboVars
    C = np.asarray(c_returnVar)
    c_tripStartTime = C[0][0]
    c_tripStartPt = C[0][1].astype(np.int64)

    a = C.T[2].astype(np.int64).tolist()#+C.T[5].astype(np.int64).tolist()
    b = C.T[3].astype(np.int64).tolist()#+C.T[6].astype(np.int64).tolist()

    c_tripPoints = np.ascontiguousarray(np.array(map(list,zip(a,b))).flatten())
    c_tripDeliveryIDs = C.T[4].astype(np.int64).tolist()
    c_tripOrderTimes = C.T[5].astype(np.int64).tolist()

    c_bestComboVars = c_tripPoints,c_tripStartTime,c_tripStartPt,c_tripDeliveryIDs,c_tripOrderTimes
    return c_bestComboVars

    # if bestComboVars == '': return c_bestComboVars
    # tripPoints,tripStartTime,tripStartPt,tripDeliveryIDs,tripOrderTimes = bestComboVars

    # print '\n'
    # print tripPoints.astype(np.int64).tolist()
    # print c_tripPoints.astype(np.int64).tolist()
    # c_check4(new,order_q_i,check_order_result='')

    a = True if str(tripPoints.astype(np.int64).tolist())    ==str(c_tripPoints.astype(np.int64).tolist()) else False
    b = True if str(tripStartTime)                      ==str(c_tripStartTime) else False
    c = True if str(tripStartPt)                        ==str(c_tripStartPt) else False
    d = True if str(tripDeliveryIDs)                    ==str(tripDeliveryIDs) else False
    e = True if str(tripOrderTimes)                     ==str(c_tripOrderTimes) else False
    if [a,b,c,d,e].count(False)!=0:
        print '\nc_check1: trouble with c_getStartInfo'
        print [a,b,c,d,e]
        print tripPoints.astype(np.int64).tolist()
        print c_tripPoints.astype(np.int64).tolist()
        print tripOrderTimes
        print c_tripOrderTimes
        print order_q_i
        print new
        systemError()
