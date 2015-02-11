# Data Analysis f(x)s

from rd_lib import this_cwd,pd,np,gd,way_t,vert_t,vert_g,NoneType
import assumptions as A
import var_global as G
from pg_fxs import pg_get_travel_dist
from fxs_for_fxs import pd_get_travel_time,pd_combine,pd_list_to_combo_index
from fxs_for_fxs import pd_get_combo_index,pd_get_trip_times,pd_get_diff_StEn
from data_prep import set_dg_pool_order,getComboStartInfo
from cy_prep import c_check1,c_check3,c_check4,c_check5     #c_check2
from data_validation import update_global_vars,updateCurrentLocation
from utility_and_permutation_fxs import genAllPairPerm_NoRep,genAllStructPerm,get_all_node_combo_dist_miles
from handle_results import pull_from_order,updateOrderResults,systemError,error_check


def new_dg_to_order_q(new,order_q_i,errorCheck=True):
    row = pd.Series(index=order_q_i.columns)
    row['order_time']   = new['order_time']
    row['deliv_id']     = new['deliv_id']
    row['dg_id']        = order_q_i.dg_id[0]
    row['dg_node']      = order_q_i.dg_node[0]
    row['dest_node']    = new['start_node']
    node_array          = [order_q_i['dg_node'][0].astype(np.int),int(new['end_node'])]
    cost_list           = pg_get_travel_dist(int(new['start_node']),node_array)
    row['travel_time_to_loc'] = round(cost_list[0] * (60.0/A.MPH),1)
    row['start_node']   = new['start_node']
    row['start_time']   = new['order_time'] + row['travel_time_to_loc']
    row['travel_time']  = round(cost_list[1] * (60.0/A.MPH),1)
    row['end_time']     = row['start_time'] + row['travel_time']
    row['end_node']     = new['end_node']
    row['total_order_time'] = row['end_time'] - row['order_time']
    row['status']       = 'on deck'
    updated_order_q_i   = order_q_i.ix[:-1,:].append(row,ignore_index=True)
    updated_dg_q_i      = pull_from_order(updated_order_q_i,errorCheck=errorCheck)
    if errorCheck==True: error_check(order_q_i=updated_order_q_i,dg_q_i=None)
    return updated_order_q_i,updated_dg_q_i
def eval_combos(var_group,saveOutput=False):
    delivery_count,dg_group_i,new,deliv_id,start_loc,end_loc=var_group
    location_count=(delivery_count*2)+1
    row=dg_group_i.iloc[0,:]

    #
    # mock_pairs = pairSet[pairSet['mc'+str(delivery_count)]==True][['a','b']]
    # mock_pairs.a = mock_pairs.a.map(num_to_mock_dict)
    # mock_pairs.b = mock_pairs.b.map(num_to_mock_dict)
    #
    # mock_travel_combos = G.orderSet[G.orderSet['mc'+str(delivery_count)]==True].ix[:,'pt0':'pt7']
    # for i in range(0,len(mock_travel_combos.columns)):
    #     mock_travel_combos[mock_travel_combos.columns.tolist()[i]]=mock_travel_combos.iloc[:,i].map(num_to_mock_dict)
    # mock_travel_combos = mock_travel_combos.apply(lambda s: [pd_combine(*s)],axis=1).head()
    # mock_travel_combos = mock_travel_combos.map(lambda s: s[0]).tolist()
    #


    mock_pairs=genAllPairPerm_NoRep(delivery_count,2)

    ABC='ABCDEFGHIJKLMNOPQRUSTUVXYZ'
    mock_pairs_locs=str(mock_pairs)
    # convert all combos having placeholder variables to real locations
    # first, adjustment to convert A0 to the starting point
    x1,y1=row['dg_X'],row['dg_Y']
    # new_var=str(x1)+', '+str(y1)
    # mock_pairs_locs=mock_pairs_locs.replace("'A0'",new_var)

    mock_travel_combos = genOrderedPairPerm(delivery_count)
    mock_travel_combos = str(mock_travel_combos)
    # need to incorporate starting position in mock_travel_combos
    # t=mock_travel_combos[1:]
    # mock_travel_combos='['+t.replace('[',"['A0', ")
    mock_travel_combos_locs=str(mock_travel_combos)
    # # as seen above with mock_pairs_loc
    # mock_travel_combos_locs=mock_travel_combos_locs.replace("'A0'",new_var)

    pt=0
    deliv_ids=[]
    for i in range(0,delivery_count):
        ind=ABC[pt]
        pt+=1
        if i < len(dg_group_i.index):
            deliv_ids.append(dg_group_i.ix[i,'deliv_id'])  # delivery IDs #1 will now correspond with A1-A2, etc..
            x1,y1=dg_group_i.ix[i,'start_X'],dg_group_i.ix[i,'start_Y']
            x2,y2=dg_group_i.ix[i,'end_X'],dg_group_i.ix[i,'end_Y']
        else:                   # accounts for adding new delivery
            deliv_ids.append(deliv_id)
            x1,y1=start_loc
            x2,y2=end_loc

        new_var=str(x1)+', '+str(y1)
        mock_pairs_locs=mock_pairs_locs.replace("'"+ind+"1'",new_var)
        mock_travel_combos_locs=mock_travel_combos_locs.replace("'"+ind+"1'",new_var)

        new_var=str(x2)+', '+str(y2)
        mock_pairs_locs=mock_pairs_locs.replace("'"+ind+"2'",new_var)
        mock_travel_combos_locs=mock_travel_combos_locs.replace("'"+ind+"2'",new_var)

    mock_pairs_locs=eval(mock_pairs_locs)
    mock_travel_combos=eval(mock_travel_combos)
    mock_travel_combos_locs=eval(mock_travel_combos_locs)
    printString='\r\nMock Pair Locs\r\n'+str(mock_pairs_locs[0])+'\n\r'

    column_names=['p1x','p1y','p2x','p2y']
    pairs=pd.DataFrame(mock_pairs_locs,columns=column_names,dtype = 'int32')
    pairs['travel_time']=pairs.apply(lambda s: pd_get_travel_time(*s),axis=1)

    pairs['combined']=pairs[column_names].apply(lambda s: pd_combine(*s),axis=1)
    printString+='pairs - shape'+str(pairs.shape)+'\n\r'
    printString+=str(pairs.head())+'\n\r'
    mapper=dict(zip(pairs.combined,pairs.travel_time))

    combos=pd.DataFrame(mock_travel_combos_locs,dtype = 'int32')
    combos['Mock Combos']=pd.DataFrame(mock_travel_combos).apply(lambda s: pd_combine(*s),axis=1)
    combos['travel_time']=np.zeros((len(combos.index),))

    printString+='\r\nMock Travel Combos \r\n'+str(combos.head())+'\n\r'

    trip_names=list(ABC[:location_count-2].lower())
    for i in range(0,location_count-2):
        testCols=combos[combos.columns[i*2:i*2+4]]
        testCols['combined']=testCols.apply(lambda s: pd_combine(*s),axis=1)
        testCols['travel_times']= [ mapper[x] for x in testCols['combined'] ]
        combos['travel_time']+=testCols['travel_times']
        combos[trip_names[i]]=testCols['travel_times']

    combos['combined']=combos[trip_names].apply(lambda s: pd_combine(*s),axis=1)
    delivery_cols=list(''.join(ABC[:delivery_count]).upper())
    order_times=dg_group_i.ix[:,'order_time'].tolist()
    order_times.append(new['order_time'])
    for it in delivery_cols:
        combos['i-'+it]=combos['Mock Combos'].apply(lambda s: pd_get_combo_index(it,s))
        combos[it+'-St'],combos[it+'-En']=zip(*combos[['combined','i-'+it]].apply(pd_get_trip_times,axis=1).map(pd_split_tuple))
        combos[it+'-T'] = combos[[it+'-St',it+'-En']].apply(pd_get_diff_StEn,axis=1)
        combos[it+'-OT']=combos[it+'-En'].apply(lambda x: x-order_times[delivery_cols.index(it)])

    indCols = ['i-'+it for it in delivery_cols]
    combos['deliv_ids'] = combos[indCols].apply(lambda s: pd_combine(*s),axis=1).apply(lambda s: pd_list_to_combo_index(s, deliv_ids))
    TravelTimesCols = [it+'-T' for it in delivery_cols]
    combos['travel_times'] = combos[TravelTimesCols].apply(lambda s: pd_combine(*s),axis=1)
    OrderTimesCols = [it+'-OT' for it in delivery_cols]
    combos['orderLen'] = combos[OrderTimesCols].apply(lambda s: pd_combine(*s),axis=1)
    combos['maxOrderTime'] = combos['orderLen'].apply(lambda s: max(eval(s)))
    X_cols = [2*n for n in range(0,location_count)]
    Y_cols = [2*n+1 for n in range(0,location_count)]
#     combos['ave_X'] = combos[X_cols].apply(lambda s: pd_combine(*s),axis=1).apply(lambda s: np.mean(eval(s)))
#     combos['ave_Y'] = combos[Y_cols].apply(lambda s: pd_combine(*s),axis=1).apply(lambda s: np.mean(eval(s)))
    combos['tripMean'] = combos['travel_times'].apply(lambda s: np.mean(eval(s)))
    combos['tripStd'] = combos['travel_times'].apply(lambda s: np.std(eval(s)))
    max_delivery_time = A.max_delivery_time
    #combos=combos[(combos.maxOrderTime <= max_delivery_time)]
    saveOutput=True
    if saveOutput==True:
        pd_Combos_path=this_cwd+'/sim_data/EDA_combos_data.txt'
        combos.to_csv(pd_Combos_path, index=False, header=True, sep='\t')
    return combos
def get_best_combo(testSet,get_combo_vars,c_global_vars,test=False,parallel=False):
    # if parallel == True:
    from cython_exts.get_best_combo import c_get_best_combo
    from cython_exts.map_points_to_combos import c_mapper2,c_mapper3,c_mapper4,c_mapper5#,c_mapper6,c_mapper7

    tripStartPt,c_tripStartTime,order_times,c_travel_speed,c_max_delivery_time,c_max_travelToLocTime,c_delivery_count,deliv_ids,realPoints = get_combo_vars
    c_travel_times_r,c_start_times_r,c_end_times_r,c_odtTimes_r,c_oMaxTimes_r,c_tMaxTimes_r,c_tddTimes_r,c_ctMarker_r,c_returnVars_r = c_global_vars

    points=testSet.ix[:,'pt0':'pt'+str(c_delivery_count*2-1)]
    orderSortKey=np.ascontiguousarray(testSet.ix[:,'i0':'i'+str(c_delivery_count-1)].as_matrix(),dtype=np.intc)
    ptsSortKey=np.ascontiguousarray(testSet.ix[:,'a1':G.ABC[c_delivery_count-1].lower()+'2'].as_matrix(),dtype=np.intc)
    mockCombos=np.ascontiguousarray(points.as_matrix(),dtype=np.intc)
    r,c = mockCombos.shape
    realCombos = np.empty((r,c),dtype=np.intc,order='C')
    if c_delivery_count == 2:  realCombos = c_mapper2(realPoints, mockCombos, realCombos)
    if c_delivery_count == 3:  realCombos = c_mapper3(realPoints, mockCombos, realCombos)
    if c_delivery_count == 4:  realCombos = c_mapper4(realPoints, mockCombos, realCombos)
    if c_delivery_count == 5:  realCombos = c_mapper5(realPoints, mockCombos, realCombos)
    #if c_delivery_count == 6:  realCombos = c_mapper6(realPoints, mockCombos, realCombos)
    #if c_delivery_count == 7:  realCombos = c_mapper7(realPoints, mockCombos, realCombos)


    z = get_all_node_combo_dist_miles(realPoints)
    p1 = np.ascontiguousarray(z.A.tolist(),dtype=np.intc)
    p2 = np.ascontiguousarray(z.B.tolist(),dtype=np.intc)
    minutes = np.ascontiguousarray(z.minutes.tolist(),dtype=np.intc)
    total_time = np.empty((len(minutes),),dtype=np.intc,order='C')


    if test==True:
        c_vars = test_get_best_combo(tripStartPt, mockCombos, realCombos,
                                  orderSortKey, ptsSortKey, order_times,
                                  deliv_ids, c_delivery_count, c_tripStartTime, c_travel_speed, c_max_delivery_time,
                                  c_max_travelToLocTime, c_travel_times_r, c_start_times_r, c_end_times_r,
                                  c_odtTimes_r, c_oMaxTimes_r, c_tMaxTimes_r, c_tddTimes_r,
                                  c_ctMarker_r, c_returnVars_r)
    else:
        c_vars = c_get_best_combo(p1,p2,minutes,total_time,A.MPH,tripStartPt, mockCombos, realCombos,
                                  orderSortKey, ptsSortKey, order_times,
                                  deliv_ids, c_delivery_count, c_tripStartTime, c_travel_speed, c_max_delivery_time,
                                  c_max_travelToLocTime, c_travel_times_r, c_start_times_r, c_end_times_r,
                                  c_odtTimes_r, c_oMaxTimes_r, c_tMaxTimes_r, c_tddTimes_r,
                                  c_ctMarker_r, c_returnVars_r)

    if c_vars[0][13] != 0:
        print np.array(c_vars)
        order_q_results = pd.DataFrame([[col for col in row] for row in c_vars],columns=['dg_node','deliv_num','deliv_id','order_time','travel_time_to_loc','start_node','start_time','travel_time','end_time','end_node','total_order_time','bestIndex'])
        order_q_results = order_q_results.drop('bestIndex',axis=1)
        # print 'best index = ',c_vars[0][14]
        return order_q_results
    else:
        if c_vars[1][13] == 505: print "\nget_best_combo --> Best Index Not Set\n"
        return None

    # TODO: add column and other pertinent info for one less delivery (for later improving overall times)
    # TODO: add trip_positions to eval_combo? -- 3D Interpolation

def getSortedPoints(new_dg_q_group):
    A=new_dg_q_group.mock_pt.astype(np.int64).tolist()
    B=sorted(A)
    B=B[:B.index(100)]
    B=[x for x in A if B.count(x)!=0]
    C=[]
    w=[C.extend([x,x+100]) for x in B]
    D=dict(zip(A,range(0,len(A))))
    sortOrder=map(lambda s: D[s],C)
    return new_dg_q_group.ix[sortOrder,:]
def adjustTripPoints(dg_q_group):
    dg_q_group = dg_q_group.reset_index(drop=True)
    mock_pts = dg_q_group.mock_pt.astype(np.int64).values.tolist()
    del_ids = dg_q_group.deliv_id.astype(np.int64).values.tolist()
    locs,mocks,ids=[],[],[]
    for mpt in mock_pts:
        i = mock_pts.index(mpt)
        if ids.count(del_ids[i])==0: ids.append(del_ids[i])
        pair_here = True if del_ids.count(del_ids[i])>1 else False
        if pair_here == True:
            locs.append(dg_q_group.ix[i,['ptbx','ptby']].astype(np.int64).values.tolist())
            mocks.append(mpt)
        else:
            if mpt>=100:
                if i==0: locs.extend([dg_q_group.ix[i,['ptax','ptay']].astype(np.int64).tolist(),dg_q_group.ix[i,['ptbx','ptby']].astype(np.int64).tolist()])
                else: locs.extend([dg_q_group.ix[i,['ptbx','ptby']].astype(np.int64).tolist(),dg_q_group.ix[i,['ptbx','ptby']].astype(np.int64).tolist()])
                mocks.extend([mpt-100,mpt])
            else:
                print 'unknown option in adjustRealPoints'
                print dg_q_group
                systemError()
    return locs,mocks,ids
def un_adjustTripPoints(order_q,static_dg_q,dynamic_dg_q,order_result):
    dg_ID = dynamic_dg_q.dg_id.values[0]

    static_dg_q = static_dg_q.reset_index(drop=True)
    stat_del_ids = static_dg_q.deliv_id.astype(np.int64).values.tolist()
    dynamic_dg_q = dynamic_dg_q.reset_index(drop=True)
    dyn_mock_pts = dynamic_dg_q.mock_pt.astype(np.int64).values.tolist()
    dyn_del_ids = dynamic_dg_q.deliv_id.astype(np.int64).values.tolist()
    order_result_ids = order_result.deliv_id.astype(np.int64).values.tolist()
    order_q_group = order_q[(order_q.id==dg_ID) & (order_q.status!='on route')].reset_index(drop=True)
    ord_q_del_ids = order_q_group.deliv_id.tolist()

    for mpt in dyn_mock_pts:
        i = dyn_mock_pts.index(mpt)
        pair_here = True if dyn_del_ids.count(dyn_del_ids[i])>1 else False
        if pair_here == True: pass
        else:
            if mpt>=100:
                ord_row_ind = order_result_ids.index(dyn_del_ids[i])
                ord_row = order_result.ix[ord_row_ind,:]

                A = order_q_group.ix[ord_q_del_ids.index(dyn_del_ids[i]),:]
                ord_row[['start_X','start_Y']] = A[['start_X','start_Y']].values
                ord_row['start_time'] = A['start_time']
                ord_row['travel_time_to_loc'] = A['travel_time_to_loc']
                order_result.ix[ord_row_ind,:] = ord_row
            else:
                print 'unknown option in un-adjustRealPoints'
                systemError()
    return order_result
def eval_additional_order(var_group,errorCheck=True):
    order_q_i,new,tripStartPt,tripStartTime = var_group

    # order_q_i,new,start_loc,end_loc = var_group
    pta,ptb,ptc = tripStartPt,list(start_loc),list(end_loc)
    toLoc = pd_get_travel_time(*pta+ptb)
    toDel = pd_get_travel_time(*ptb+ptc)
    if tripStartTime + toLoc + toDel <= max_delivery_time:
        row=order_q_i.ix[0,:].copy()
        row['deliv_num']=2
        row['travel_time_to_loc']=toLoc
        row['deliv_id']=new['deliv_id']
        row['order_time']=new['order_time']
        row['start_X'],row['start_Y']=new['start_X'],new['start_Y']
        row['start_time']=tripStartTime+toLoc
        row['end_time']=row['start_time']+toDel
        row['end_X'],row['end_Y']=end_loc
        row['total_order_time']=row['end_time']-row['order_time']
        row['travel_time']=row['end_time']-row['start_time']
        order_results = order_q_i.append(row,ignore_index=True).reset_index(drop=True)
        dg_q_results = pull_from_order(order_results,errorCheck=errorCheck)
        return order_results,dg_q_results
    else:
        return None,None

def getPtsFrom_dg_q(x):
    ptxs = [x.ptax.astype(np.int64).values[0]]+x.ptbx.astype(np.int64).values.tolist()
    ptys = [x.ptay.astype(np.int64).values[0]]+x.ptby.astype(np.int64).values.tolist()
    return np.array([ptxs,ptys],dtype=int).T.tolist()
def dg_q_reorganize_mock_pts(dg_result):
    # reorganize mock_pts for consistency and b/c values are reduced later upon completed delivery
    A=dg_result.mock_pt.astype(np.int64).tolist()
    B=sorted(A)
    if str(len(B)/2.0)[str(len(B)/2.0).find('.'):str(len(B)/2.0).find('.')+2] != '.0':
        print 'why odd number of mock_pts to organize?'
        systemError()
    sorted_pickup_pts=B[:len(B)/2]
    unsorted_pickup_pts=[x for x in A if sorted_pickup_pts.count(x)!=0]
    E=dict(zip(unsorted_pickup_pts,sorted_pickup_pts))
    for i,j in E.items(): E.update({i+100:j+100})
    dg_result.mock_pt = map(lambda s: E[s],A)
    return dg_result
def dg_q_reorganize_BY_mock_pts(dg_q_i,reset=False):
    if len(dg_q_i.index)==1: return dg_q_i
    A = dg_q_i.mock_pt.astype(np.int64).tolist()
    B = [it for it in A if it<100]
    C = []
    for it in A:
        if B.count(it)!=0:
            C.extend([it,it+100])               # if startPt, add start and end pts (assuming there is an endPt in list)
        elif B.count(it-100)==0: C.append(it)   # if 'it' is an endPt without a startPt, then add 'it'
        else: pass                              # else, it is an endPt that is already accounted for with its startPt
    new_dg_q_i = dg_q_i
    if A != C:
        D = dict(zip([A.index(it) for it in C],range(0,len(A))))
        new_sort = [D[it] for it in sorted(D.keys())]
        if len(new_sort)!=len(new_dg_q_i.index):
            print 'why diff len?'
            systemError()
        new_dg_q_i['sortOrder']=new_sort
        new_dg_q_i = new_dg_q_i.sort_index(by='sortOrder',ascending=True).drop(['sortOrder'],axis=1)
    if reset==True: new_dg_q_i = new_dg_q_i.reset_index(drop=True)
    return new_dg_q_i
def getBestDG(globalVars,new,errorCheck=True):
    order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

    # globalVars, dgp_grp_indicies = set_dg_pool_grp_order(globalVars,ordersNow)
    # order_q = c_order_by_min(..)
    # update dg_pool - - < <

    updated=False
    while updated == False:

        set_dg_groups,free_dg, status = set_dg_pool_order(globalVars,new)
        if status == 're-pool':
            globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
            # set re-pool size here, use newSubVar as variable for number of new DG
            globalVars = update_global_vars(globalVars,'re-pool',newAddVar=False,newSubVar=False,replaceVar={})
            order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
            set_dg_groups,free_dg,status = set_dg_pool_order(globalVars,new)

        # print '---',new['deliv_id'],'---'
        pt=-1
        for dg_grp in set_dg_groups:
            pt+=1
            # print 'set #',pt,'\n'
            # print new['deliv_id']
            # print grp

            # updated,best_order_results,best_dg_q_results = getBestDG_grp_old(globalVars,grp,new,errorCheck=errorCheck)
            # c_updated,c_best_order_results,c_best_dg_q_results = c_check5(globalVars,grp,new,checkOrder=best_order_results)
            updated,best_order_results,best_dg_q_results = c_check5(globalVars,dg_grp,new,errorCheck=errorCheck)


            # if updated != c_updated:
            #     print pt,new['deliv_id']
            #     systemError()


            if updated == True:
                bestDG = best_order_results.dg_id.astype(np.int64).tolist()[0]
                globalVars = update_global_vars(globalVars,'update per order',best_order_results,best_dg_q_results,replaceVar={'dg_id':bestDG})
                return globalVars

        if updated == False:
            if len(free_dg) != 0:
                dg_ID = free_dg['dg_id'].astype(np.int64).values[0]
                new_dg_id = dg_ID
                order_q_i = pd.merge(free_dg.drop(['total_delivered','current_deliveries','total_travel_time'],axis=1),order_q.ix[:-1,:],how='left')
                # TODO: review whether dg_pool calc.s make it to new_dg_to_order_q
                new_order_result,new_dg_result = new_dg_to_order_q(new,order_q_i,errorCheck=errorCheck)
                globalVars = update_global_vars(globalVars,'update per order',new_order_result,new_dg_result,replaceVar={'dg_id':new_dg_id})
                return globalVars
            else:
                order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
                globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
                # set re-pool size here, use newSubVar as variable for number of new DG
                globalVars = update_global_vars(globalVars,'re-pool',newAddVar=False,newSubVar=False,replaceVar={})
                order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

            # TODO: add feature to watch for excessively un-used portions of dg_pool

        # end of while loop
def bestExpeditedDeliveryRoute(order_q_i,new,errorCheck=True):
    # pull information from data for computation

    bestComboVars = getComboStartInfo(new,order_q_i)

    bestComboVars = c_check1(new,order_q_i,bestComboVars)
    tripPoints,tripStartTime,tripStartPt,tripDeliveryIDs,tripOrderTimes = bestComboVars
    # if new['deliv_id']==29 and order_q_i.dg_id.tolist().count(2.0) != 0:
    #     print tripPoints
    if str(tripPoints) == '1':
        print 'single order mated\n'
        var_group = order_q_i,new,tripStartPt,tripStartTime
        order_results,dg_q_results = eval_additional_order(var_group,errorCheck=errorCheck)
        c_check3(new,order_q_i,tripStartPt,tripStartTime,order_results)
        return order_results,dg_q_results # returns None,None if that is the case

    # prepare variables for using c++, i.e., contiguous memory for using memoryviews & type == long (a.k.a., int64)
    order_times = np.ascontiguousarray(tripOrderTimes,dtype=np.intc)
    deliv_ids = np.ascontiguousarray(tripDeliveryIDs,dtype=np.intc)
    int_vars = np.asarray([tripPoints.shape[0]*.5,tripStartTime,A.travel_speed,A.max_delivery_time,A.max_travelToLocTime],dtype=np.intc)
    c_delivery_count,c_tripStartTime,c_travel_speed,c_max_delivery_time,c_max_travelToLocTime = int_vars[0],int_vars[1],int_vars[2],int_vars[3],int_vars[4]
    get_combo_vars = long(tripStartPt),c_tripStartTime,order_times,c_travel_speed,c_max_delivery_time,c_max_travelToLocTime,c_delivery_count,deliv_ids,tripPoints

    #
    #

    if c_delivery_count < A.max_delivery_per_dg: testSet=G.orderSet[G.orderSet['mc'+str(c_delivery_count)]==True].reset_index(drop=True)
    else: testSet=G.orderSet

    # split processes here for parallel processing
    test,parallel=False,False
    if c_delivery_count<4 or parallel==False:
        test_pt=len(testSet.index)
        c_global_vars_reduced = (G.c_travel_times[:test_pt],G.c_start_times[:test_pt],G.c_end_times[:test_pt],G.c_odtTimes[:test_pt],
                                 G.c_oMaxTimes[:test_pt],G.c_tMaxTimes[:test_pt],G.c_tddTimes[:test_pt],G.c_ctMarker[:test_pt],
                                 G.c_returnVars[:c_delivery_count])
        # if order_q_i.dg_id.astype(np.int64).values[0]==6 and new['deliv_id']==1772: test=True
        order_results = get_best_combo(testSet,get_combo_vars,c_global_vars_reduced,test,parallel)
    # TODO: may need another level of parallel processing for evaluating orders (as opposed to combos here)
    # else: order_results = run_parallel()

    if type(order_results) == NoneType: return None,None
    else:
        final_order_q_i,final_dg_q_i = updateOrderResults(order_q_i,new,order_results,errorCheck)
        return final_order_q_i,final_dg_q_i
def getBestDG_grp_old(globalVars,grp,new,errorCheck):
    order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
    D = order_delivered
    updated = False
    best_order_results,best_dg_q_results,bestDG = None,None,None
    now = new['order_time']
    for i in range(0,len(grp.index)):
        dg_from_pool = grp.ix[i:i,:]
        dg_ID = dg_from_pool['dg_id'].astype(np.int64).values[0]

        order_q_i = order_q[order_q.dg_id==dg_ID]
        earliestStart = order_q_i.start_time.astype(np.int64).min()
        order_q_i = order_q_i.append(D[(D.dg_id==dg_ID) & (D.end_time>earliestStart)]).sort_index(by='start_time',ascending=True).reset_index(drop=True)

        if len(order_q_i.index)==0:
            # if a viable result is not already found, pick best from pool (easy, no real calc.)
            # if already found a viable result, then go with the viable result
            # if updated==False:
            #     new_dg_id = dg_ID
            #     order_q_i = pd.merge(dg_from_pool.drop(['total_delivered','current_deliveries','travel_dist','total_travel_time'],axis=1),order_q.ix[:-1,:],how='left')
            #     # TODO: review whether dg_pool calc.s make it to new_dg_to_order_q
            #     new_order_result,new_dg_result = new_dg_to_order_q(new,order_q_i,errorCheck=errorCheck)
            # else: new_order_result,new_dg_result,new_dg_id = best_order_results,best_dg_q_results,bestDG
            # globalVars = update_global_vars(globalVars,'update per order',new_order_result,new_dg_result,replaceVar={'id':new_dg_id})
            # return globalVars
            print 'check getBestDG_grp_old'
            systemError()

        else:
            order_q_i.ix[:,'dg_node'] = dg_from_pool.dg_node
            # TODO when more than one DG, check why above line is needed
            order_result,dg_result = bestExpeditedDeliveryRoute(order_q_i,new,errorCheck=errorCheck)
            # print 'grp item #',i
            # print order_q_i.ix[:0,:]
            # print order_result
            # print '\n'


            c_check4(new,order_q_i,check_order_result=order_result)

            if type(order_result) == NoneType: pass
            else:

                # print 'old EDA result:\n',order_result # TODO: delete

                # additional time
                clean_order_q_i = order_q_i[order_q_i.end_time>now]
                checkVar = (order_result.end_time.max() - order_result.start_time.min()) - (clean_order_q_i.end_time.max() - clean_order_q_i.start_time.min())
                # shortest time to pick up location
                # checkVar = order_result[order_result.deliv_id == new['deliv_id']].travel_time_to_loc.values[0]
                if updated==False: updated,add_to_results=True,True
                elif checkVar < minVar:
                    add_to_results=True
                if add_to_results==True:
                    add_to_results,minVar = False,checkVar
                    best_order_results,best_dg_q_results,bestDG = order_result,dg_result,dg_ID

    return updated,best_order_results,best_dg_q_results
