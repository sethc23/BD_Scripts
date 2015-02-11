# Execution f(x)s

# RUN_CHAOS_SIMULATION() in iPython

def RUN_NORMAL_DELIVERY_SIMULATION(makeData=False,showSimData=False):
    sim_data_Path=this_cwd+'/sim_data/vendor_sim_data.txt'
    if makeData==True: sim_data = make_simulation_data(savePath=sim_data_Path)
    else: sim_data = pd.read_hdf(sim_data_Path.rstrip('.txt')+'.h5', 'table')
    sim_data = sim_data.sort_index(by=['order_time','vend_Y','vend_X'], ascending=[True,True,True])
    if showSimData==True: DISPLAY_SIMULATION_DATA()
    NormalDelivery(sim_data)

def RUN_LATTICE_SIMULATION():

    global_simulation_vars()
    makeData=False
    load=True
    t1A=time()

    sim_data_Path=this_cwd+'/sim_data/vendor_sim_data.txt'
    if makeData==True:
        df = make_simulation_data(savePath=sim_data_Path)
    else:
        df = pd.read_hdf(sim_data_Path.rstrip('.txt')+'.h5', 'table')
    df = df.sort_index(by=['order_time','vend_Y','vend_X'], ascending=[True,True,True])

    # vendor min/max X/Y determined here
    Xset,Yset=np.array(df.vend_X.astype(np.int64)),np.array(df.vend_Y.astype(np.int64))
    Xmin,Xmax=Xset.min(),Xset.max()
    Ymin,Ymax=Yset.min(),Yset.max()


    global order_q,dg_q,dg_pool,delivered
    dg_head = DG().printHeader(printer=False,fullHeading=True).split('\t')
    dg_pool = init_dg_pool(pt=0,old_dg_pool=False,load=load,save=True,filePath='')
    order_q = pd.DataFrame(columns=dg_head)
    delivered=pd.DataFrame(columns=dg_head)
    dg_pool = pd.merge(dg_pool,delivered,how='left')


    """
    trav_cols = [ABC[i].lower() for i in range(0,max_delivery_per_dg*2)]
    desc_cols = ['-i','-ID','-OT','-St','-En']
    dg_queue_cols = range(0,1+(max_delivery_per_dg*2))+['mockCombo','travel_time']+trav_cols+['combined']
    dg_queue_cols += [ ABC[pt]+label for pt in range(0,max_delivery_per_dg) for label in desc_cols ]
    dg_queue_cols += ['deliv_ids','travel_times','del_times','maxDel_time','ave_X','ave_Y','tripMean','tripStd']
    dg_q = pd.DataFrame(columns=dg_queue_cols)

    total_time=Assumption('vend_hours_delivering')*60
    for i in range(0,total_time):
        now=i
        # remove completed orders on this minute, if any
        completedOrders=order_q[(order_q.end_time <= now)]
        delivered=pd.concat([delivered,completedOrders]) # includes completed trips to vendor
        order_q=order_q[order_q.end_time > now].reset_index(drop=True)
        # identify and re-pool DG that have completed orders
        delivered['ready']=delivered['id'].apply(lambda s: (order_q.id.tolist().count(s) == 0 and dg_pool.dg_id.tolist().count(s) == 0))
        if len(delivered[delivered.ready == True].index) != 0:
            re_pool = delivered[delivered.ready == True]
            re_pool.status = 'ready'
            re_pool['dg_X'],re_pool['dg_Y'] = re_pool['end_X'],re_pool['end_Y']
            re_pool = re_pool.drop('ready',axis=1).reset_index(drop=True)
            dg_pool = pd.concat([re_pool,dg_pool]).reset_index(drop=True).groupby('id').first().reset_index()
        delivered = delivered.drop('ready',axis=1).reset_index(drop=True)
        # process all current orders
        ordersNow=df[(df.order_time == now)]
        t1=time()
        for j in range(0,len(ordersNow.index)):
            thisOrder=ordersNow.iloc[j,:]#.copy()
            order_q,dg_q,dg_pool = getBestDG(order_q,dg_q,dg_pool,thisOrder,ordersNow.index[j],showVars=False,saveOutput=False)
        if len(ordersNow.index) != 0: print 'minute'+'\t'+str(i)+'\t'+'orders='+'\t'+str(len(ordersNow.index))+'\t'+str((time()-t1)/len(ordersNow.index))+'\t'+str(time())

    # move remaining orders at close to 'delivered'
    completedOrders=order_q[(order_q.end_time >= now)]
    pieces = [delivered,completedOrders]
    delivered=pd.concat(pieces)

    print 'done'
    print time()-t1A
    # cmd='say -v Bells "dong"'
    # system(cmd)
    """

# if __name__ == '__main__':
#     if normal_sim == True: RUN_NORMAL_DELIVERY_SIMULATION()
#     if chaos_sim == True: RUN_CHAOS_SIMULATION(assumptions=None,
#                                                makeData=makeData,
#                                                showSimData=showSimData,
#                                                runNormalDel=runNormalDel,
#                                                load=load,
#                                                save=save,
#                                                resume=resume,
#                                                errorCheck=errorCheck,
#                                                global_op_vars=global_op_vars)
#     if show_data_results == True:
#         # if normal_sim == True: DISPLAY_NORMAL_DELIVERY_DATA()
#         # if chaos_sim == True: DISPLAY_EDA_DATA()
#         DISPLAY_EDA_DATA()
#         # DISPLAY_NORMAL_DELIVERY_DATA()
#         # DISPLAY_SIMULATION_DATA()

#     if showRealData==True: DISPLAY_REAL_DATA()

#     if show_normal_results==True: DISPLAY_NORMAL_DELIVERY_DATA()

#     if lattice_sim == True: RUN_LATTICE_SIMULATION()
