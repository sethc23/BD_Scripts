# Handle Results f(x)s
from rd_lib import pd,time
np=pd.np
from data_prep import set_mock_pts,order_q_re_order_deliv_num


alert_bell=False

def pull_from_order(order_q_i,errorCheck=True):
    """ Get data from Order[i] and copy to DG Queue"""
    dg_ID = order_q_i.dg_id.astype(np.int64).values[0]
    order_q_i = order_q_i.sort_index(by=['start_time','end_time'], ascending=[True,True]).reset_index(drop=True)

    df = pd.DataFrame(order_q_i.ix[:,['start_time','start_node','deliv_id']].astype(np.int64).as_matrix(),columns=['time','pt','deliv_id'])
    df = df.append(pd.DataFrame(order_q_i.ix[:,['end_time','end_node','deliv_id']].astype(np.int64).as_matrix(),columns=['time','pt','deliv_id']),ignore_index=True)
    if order_q_i.ix[0,'dg_node'].astype(np.int64) != order_q_i.ix[0,'start_node'].astype(np.int64):
        df = pd.DataFrame([order_q_i.ix[0,['order_time','dg_node','deliv_id']].astype(np.int64).tolist()],columns=['time','pt','deliv_id']).append(df)

    df = df.sort_index(by='time', ascending=True).reset_index(drop=True)
    df_ind = df.index.tolist()
    pta_ind,ptb_ind = df_ind[:-1],df_ind[1:]
    # pta deliv_id is dropped because deliv_id and mock_pt based on destination pt
    pta,ptb = df.ix[pta_ind,:].drop(['deliv_id'],axis=1).reset_index(drop=True),df.ix[ptb_ind,:].reset_index(drop=True)
    new_dg_q = pd.DataFrame(pta.as_matrix(),columns=['pta-t','pta'])
    new_dg_q['ptb-t'] = ptb['time'].values
    new_dg_q['ptb'] = ptb['pt'].values
    new_dg_q['deliv_id'] = ptb['deliv_id'].values
    new_dg_q['dg_id'] = dg_ID
    new_dg_q = new_dg_q[['dg_id','pta','ptb','pta-t','ptb-t','deliv_id']]
    new_dg_q = new_dg_q.sort_index(by=['dg_id','pta-t','ptb-t','deliv_id'], ascending=[True,True,True,True]).reset_index(drop=True)

    # rearrange inconsistent route due to multi-purpose point
    ordered_dg_q = rearrange_dupe_locs_dg_q(new_dg_q)

    # fill in mock points
    final_dg_q = set_mock_pts(ordered_dg_q)

    if errorCheck==True: error_check(order_q_i=None,dg_q_i=final_dg_q)
    return final_dg_q

def updateOrderResults(order_q_i,new,order_results,errorCheck=True):
    now = new['order_time']
    # First, format order_results with proper columns and fill static data
    # Second, reverse adjustments made for partial, non-completed trip analysis
    # Third, add-in any staticOrders (which should fit perfectly in place)
    # Fourth, re-adjust delivery numbers (resulting from partial trip analysis) and error check

    # First:
    results_with_dg_format = pd.merge(order_q_i,order_results,how='right')
    fillColumns =['id','dg_X','dg_Y','ave_X','ave_Y','status']
    results_with_dg_format[fillColumns] = order_q_i.reset_index(drop=True).ix[0,fillColumns[:-1]].tolist() + ['on deck']
    f_ord_res = results_with_dg_format.reset_index(drop=True)

    # Second:
    partial_check_orders = order_q_i[(order_q_i.start_time<=now) & (order_q_i.end_time>now)].sort_index(by='deliv_id',ascending=True).reset_index(drop=True)
    if len(partial_check_orders.index)!=0:
        partial_ids = partial_check_orders.deliv_id.tolist()
        res_needing_edit = f_ord_res[f_ord_res.deliv_id.isin(partial_ids)==True].sort_index(by='deliv_id',ascending=True).reset_index(drop=True)
        replCols = ['travel_time_to_loc','order_time','start_X','start_Y','start_time']
        res_needing_edit.ix[:,replCols] = partial_check_orders.ix[:,replCols].values
        a = pd.merge(res_needing_edit,f_ord_res[f_ord_res.deliv_id.isin(partial_ids)==False],how='outer').sort_index(by='start_time')
        clean_ord_results = a.reset_index(drop=True)
    else: clean_ord_results = f_ord_res

    # Third:
    clean_ord_res_ids = clean_ord_results.deliv_id.tolist()
    orders_to_add = partial_check_orders[partial_check_orders.deliv_id.isin(clean_ord_res_ids)==False]
    if len(orders_to_add.index) != 0:
        full_order_q_i = pd.merge(orders_to_add,clean_ord_results,how='outer')
        print '\ndid it\n'
    else: full_order_q_i = clean_ord_results

    #c_check2(order_q_i,order_results,new,full_order_q_i)

    # Fourth:
    new_order_q_i = order_q_re_order_deliv_num(full_order_q_i)
    check_order_q_i = new_order_q_i.append(order_q_i[order_q_i.end_time<=now]).sort_index(by='start_time',ascending=True).reset_index(drop=True)
    if errorCheck == True: error_check(order_q_i=check_order_q_i,dg_q_i=None,arg3='sim_data')

    check_dg_q_i = pull_from_order(check_order_q_i,errorCheck=False) # false here because it would duplicate part of the above check
    new_dg_q_i = check_dg_q_i[check_dg_q_i['ptb-t']>now]

    return new_order_q_i,new_dg_q_i

def compare_orders(orderA,orderB,order_q_i=''):
    orderA = orderA.sort_index(by='deliv_id',ascending=True)
    orderB = orderB.sort_index(by='deliv_id',ascending=True)
    a = True if orderA.deliv_id.astype(np.int64).tolist()      == orderB.deliv_id.astype(np.int64).tolist() else False
    b = True if orderA.id.astype(np.int64).tolist()              == orderB.id.astype(np.int64).tolist() else False
    c = True if orderA.order_time.astype(np.int64).tolist()       == orderB.order_time.astype(np.int64).tolist() else False
    d = True if orderA.start_X.astype(np.int64).tolist()         == orderB.start_X.astype(np.int64).tolist() else False
    e = True if orderA.start_Y.astype(np.int64).tolist()         == orderB.start_Y.astype(np.int64).tolist() else False
    f = True if orderA.start_time.astype(np.int64).tolist()       == orderB.start_time.astype(np.int64).tolist() else False
    g = True if orderA.end_time.astype(np.int64).tolist()         == orderB.end_time.astype(np.int64).tolist() else False
    h = True if orderA.end_X.astype(np.int64).tolist()           == orderB.end_X.astype(np.int64).tolist() else False
    i = True if orderA.end_Y.astype(np.int64).tolist()           == orderB.end_Y.astype(np.int64).tolist() else False
    if [a,b,c,d,e,f,g,h,i].count(False)!=0:
        print 'c_trouble with update orders'
        print [a,b,c,d,e,f,g,h,i]
        if order_q_i != '': print '\nNon-cython results\n',orderA,'\nCython results\n',orderB,'\norder_q_i\n',order_q_i
        else: print '\nNon-cython results\n',orderA,'\nCython results\n',orderB
        systemError()
    return

def fix_dg_q_delID_dupes(static_dg_q,new_dg_q,arg_dg_group_i):
    # there should be only two of each deliv_id, otherwise it needs to be fixed...
    del_ids = new_dg_q.deliv_id.astype(pd.np.int64).tolist()
    unique_ids = dict(zip(del_ids,range(0,len(new_dg_q.index)))).keys()
    idCount = map(lambda s: del_ids.count(s),unique_ids)
    if len(unique_ids)-idCount.count(2)!=0:
        # in some cases, new_dg_q will have three rows with a given deliv_id for a reason different than realPoints adjustment
        # Instance #1:
        #   two orders have same pick-up location, and bestCombo begins by picking up second order.
        #   in such case, new_dg_q would have deliv_id of first order instead of correctly having deliv_id of second order
        rowInd = static_dg_q[static_dg_q.deliv_id == unique_ids[idCount.index(3)]].index.values[0]
        staticRow = static_dg_q.ix[rowInd,:] # because rowInd is type=int, then Series is result
        rowInd = new_dg_q[new_dg_q.ptax==staticRow['ptax']].index.values[0]
        row = new_dg_q.ix[rowInd,:]
        row['deliv_id']  = unique_ids[idCount.index(1)]
        static_dg_q.ix[rowInd,:] = row

        new_dg_q = pd.merge(static_dg_q,new_dg_q,how='outer')
        new_dg_q.dg_id = arg_dg_group_i.id[0]
        if idCount.count(3)>1 or idCount.count(1)>1:
            print 'check update_dg_q_Results -- unknown condition re: delivery ids'
            systemError()

    return new_dg_q.reset_index(drop=True)

def rearrange_dupe_locs_dg_q(dg_q_i):
    a=dg_q_i.copy()
    if a.pta.tolist()[1:]!=a.ptb.tolist()[:-1]:
        b = a.groupby('ptb-t')
        end_times_all = a['ptb-t'].astype(pd.np.int64).tolist()
        end_times_uniq = b.groups.keys()
        end_time_cnt = [end_times_all.count(x) for x in end_times_uniq]
        if end_time_cnt.count(3)==0:
            print 'unknown inconsistency with route'
            print '\nall:\n',end_times_all,'\nuniq:\n',end_times_uniq,'\ncount:\n',end_time_cnt
            print a
            systemError()
        else:
            timePt = end_times_uniq[end_time_cnt.index(3)]
            # stPt = end_times_all.index(timePt)
            end_times_all.reverse()
            for it in end_times_all:
                if it==timePt:
                    endPt = len(end_times_all) - end_times_all.index(it)
                    break
            a = a.ix[:endPt-3,:].append(a.ix[endPt-1:endPt-1,:]).append(a.ix[endPt-2:endPt-2,:]).reset_index(drop=True)
    return a

def error_check(order_q_i=None,dg_q_i=None,arg3=None):

    def check_dg_q_positions_times(A): # should include "now" b/c avoiding unimportant errors is easier than troubleshooting
        if (A.ptax.tolist()[1:]!=A.ptbx.tolist()[:-1] or A.ptay.tolist()[1:]!=A.ptby.tolist()[:-1]):
            B = rearrange_dupe_locs_dg_q(A)
            if (B.ptax.tolist()[1:]!=B.ptbx.tolist()[:-1] or B.ptay.tolist()[1:]!=B.ptby.tolist()[:-1]):
                print 'why positions not aligned?'
                print B
                systemError()
        if A['pta-t'].tolist()[1:]!=A['ptb-t'].tolist()[:-1]:
            print 'why are times not aligned'
            print A
            systemError()

        # TODO: tighten up use of dg_X/Y re: updating.  see notes below.
        # for checking times in simulation analysis, first point based on dg_X/Y and should not be considered reliable.
        #   this is because all orders carry DG's current location until the orders are removed from queue.
        #   one fix would be to only update DG location for dynamic orders.
        #       - once traveling to a pickup location is final, dg_X/Y becomes final.
        #       - this fix would include adjusting the changes made to the initial order_results
        #       - this fix would also include changing how order_q_i is updated (if dg_pool is not already responsible)
        #       - dg_pool would have to be reviewed to ensure that locations were taken from proper orders.
        # Second, room should be allowed for breaks.  TODO: How to distinguish b/t breaks and errors?
        #   for now, extra time to arrive at a location is no longer an error

        # A['travel_time'] = A[['ptax','ptay','ptbx','ptby']].apply(lambda s: pd_get_travel_time(*s),axis=1)
        # A['expectedArrival'] = A['pta-t'] + A['travel_time']
        # A['passtimecheck'] = False
        # goodInd = A[(A['ptb-t'] == A['expectedArrival']) | ((A['expectedArrival'] - A['ptb-t'])>=0)].index
        # A.ix[goodInd,'passtimecheck'] = True
        # A.ix[A.index - goodInd,'passtimecheck'] = A.travel_time.map(lambda s: True if s )
        # # if len(A[A.passcheck==False])!=0:
        # if A.passtimecheck.tolist()[1:].count(False)!=0:
        #     print 'why do the times not match up?'
        #     print A
        #     systemError()
        return
    def check_order_q_positions(order_q_i):
        order_q_i = order_q_i.sort_index(by='deliv_id',ascending=True).reset_index(drop=True)
        order_del_ids = order_q_i.deliv_id.unique().astype(np.int64).tolist()
        sorted_sim_del_ids = sorted(sim_data[sim_data.index.isin(order_del_ids)==True].index.astype(np.int64).tolist())
        sim_orders = sim_data.ix[sorted_sim_del_ids,:].reset_index(drop=True)
        sim_orders['deliv_id'] = sorted_sim_del_ids
        a = True if order_q_i.start_X.astype(np.int64).tolist() == sim_orders.start_X.astype(np.int64).tolist() else False
        b = True if order_q_i.start_Y.astype(np.int64).tolist() == sim_orders.start_Y.astype(np.int64).tolist() else False
        c = True if order_q_i.end_X.astype(np.int64).tolist() == sim_orders.end_X.astype(np.int64).tolist() else False
        d = True if order_q_i.end_Y.astype(np.int64).tolist() == sim_orders.end_Y.astype(np.int64).tolist() else False
        e = True if order_q_i.order_time.astype(np.int64).tolist() == sim_orders.order_time.astype(np.int64).tolist() else False
        if [a,b,c,d,e].count(False)!=0:
            print '\nwhy is order completed different from source?'
            print '\n[ start_X,start_Y,end_X,end_Y,order_time ]\n',[a,b,c,d,e]
            print '\norder_q_i\n',order_q_i
            print '\nsim_orders\n',sim_orders
            systemError()

    def order_q_test_battery(order_q_i):
        pull_from_order(order_q_i,errorCheck=True)
        if order_q_i.dg_id.unique().shape[0]>1:
            print '\nwhy more than one update?'
            print order_q_i
            systemError()
        if (order_q_i.end_time.values - order_q_i.start_time.values).min()<0:
            print '\nwhy end_time before start_time?'
            print order_q_i
            systemError()
        if (order_q_i.end_time.values - order_q_i.order_time.values).max()>max_delivery_time:
            print '\nwhy late delivery?'
            print order_q_i
            systemError()
        deliv_nums = sorted(order_q_i.deliv_num.unique().tolist())
        if deliv_nums[0]==0: deliv_nums = deliv_nums[1:]
        if len(deliv_nums)!=max(deliv_nums):
            print '\nwhy misnumbered delivery numbers?'
            print order_q_i
            systemError()

    def dg_q_test_battery(dg_q_i):
        check_dg_q_positions_times(dg_q_i)
        del_ids = dg_q_i.deliv_id
        del_ids,del_uniq = del_ids.tolist(),del_ids.unique()
        del_uniq_id_count = [del_ids.count(it) for it in del_uniq]
        if del_uniq_id_count.count(3)!=0:
            print 'why dupe deliv_id?'
            print dg_q_i
            systemError()
        if len(dg_q_i.mock_pt.tolist()) != dg_q_i.mock_pt.unique().shape[0]:
            print 'why dupe mock_pt?'
            print dg_q_i
            systemError()

    if arg3=='sim_data':
        check_order_q_positions(order_q_i)
        return
    if type(order_q_i) != NoneType: order_q_test_battery(order_q_i)
    if type(dg_q_i) != NoneType: dg_q_test_battery(dg_q_i)

    return

def systemError():
    if alert_bell == True:
        cmd='say -v Bells "dong"'
        # system(cmd)

    print time(),'systemError()'
    raise SystemError
