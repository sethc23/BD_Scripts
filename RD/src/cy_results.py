# Cython Result f(x)s
def receive_c_order_by_min(ret_order_q,showVar=True):
    a = np.asarray(ret_order_q)
    if showVar==True: print a,'\n'
    # print a.shape

    sim_cols=['vendorID','vend_X','vend_Y','order_num','deliv_id','order_time','start_X','start_Y','end_X','end_Y']
    oq_cols=['id','dg_X','dg_Y','deliv_num','travel_time_to_loc','deliv_id','order_time','start_X','start_Y','start_time','end_time','end_X','end_Y','total_order_time','travel_time']
    o_res_cols = ['dg_X','dg_Y','deliv_num','deliv_id','order_time','travel_time_to_loc',
                     'start_X','start_Y','start_time','travel_time','end_time','end_X','end_Y',
                     'total_order_time','id']
    ret_cols = o_res_cols if a.shape[1]==14 else oq_cols
    order_q_ret = pd.DataFrame(a,columns=ret_cols)
    if showVar==True: print order_q_ret

    remaining_deliv_ids = order_q_ret[order_q_ret.deliv_num==950].deliv_id.astype(pd.np.int64).tolist()
    order_q_ret = order_q_ret[(order_q_ret.deliv_num!=0) & (order_q_ret.deliv_id.isin(remaining_deliv_ids)==False)]
    b = order_q_ret.astype(pd.np.int64).as_matrix()
    order_q_ret['ave_X'] = np.nan
    order_q_ret['ave_Y'] = order_q_ret.ave_X.map(lambda s: s)
    order_q_ret['status'] = order_q_ret.ave_X.map(lambda s: 'on deck')
    c = ['id','dg_X','dg_Y','ave_X','ave_Y','status','deliv_num','travel_time_to_loc','deliv_id','order_time',
           'start_X','start_Y','start_time','end_time','end_X','end_Y','total_order_time','travel_time']
    order_q_ret = order_q_ret.ix[:,c]

    return order_q_ret,b,remaining_deliv_ids
