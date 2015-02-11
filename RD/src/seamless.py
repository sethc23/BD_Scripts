# Simulation Vars
use_cython=True
# cython=False
# resume=True
resume=False
# load=True
load=False
save=True
# save=False

# makeData=False
makeData=True
runNormalDel=False
alert_bell=False

showRealData=False
showSimData=False
# normal_sim = True
normal_sim = False
show_normal_results = False
chaos_sim = True
# chaos_sim = False
# show_data_results = True
show_data_results = False
lattice_sim = False


errorCheck=False
global_op_vars=False

from rd_lib             import pd,time,this_cwd,engine
from sim_data_gen       import init_global_vars
from data_validation    import update_global_vars,set_col_types
from data_analysis      import getBestDG
from data_recordation   import export_all_data
from assumptions        import totalTime

# Execution f(x)s
def RUN_CHAOS_SIMULATION(makeData=False,showSimData=False,runNormalDel=False,load=False,save=False,
                         resume=False,errorCheck=False,global_op_vars=False):

    t1A=time()
    print t1A
    if global_op_vars == True:
        global sim_data,order_q,order_delivered,dg_pool,dg_pool_pt,dg_q,dg_delivered
    else: global sim_data

    sim_data_Path=this_cwd+'/sim_data/vendor_sim_data.txt'
    if makeData==True:
        from sim_data_gen import make_simulation_data_from_real_data
        sim_data = make_simulation_data_from_real_data(savePath=sim_data_Path)
    else:
        # sim_data = pd.read_hdf(sim_data_Path.rstrip('.txt')+'.h5', 'table')
        sim_data = pd.read_sql_table('sim_data',engine,index_col='gid')

    sim_data = sim_data.sort_index(by=['order_time','vend_id'], ascending=[True,True])
    if showSimData==True:
        from data_visual import DISPLAY_SIMULATION_DATA
        DISPLAY_SIMULATION_DATA()
    if runNormalDel==True:
        RUN_NORMAL_DELIVERY_SIMULATION(makeData=False,showSimData=False)

    globalVars_plus = init_global_vars(load,save,resume)
    if globalVars_plus==None: return

    order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt,program_stats,stpt = globalVars_plus
    globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
    globalVars = set_col_types(globalVars)

    print 'starting at',stpt
    pt=0
    for i in range(stpt,totalTime+1):
        now=i

        # maintain lists of data
        globalVars = update_global_vars(globalVars,'update per minute',now)

        # UPDATE to/from PGSQL HERE

        # export data on a regular basis
        if pt==1:
            pt = 0
            if save == True: x = export_all_data(globalVars,program_stats)
        pt+=1

        # process all current orders
        ordersNow=sim_data[(sim_data.order_time == now)]
        t1=time()

        for j in range(0,len(ordersNow.index)):
            thisOrder = ordersNow.iloc[j,:].copy()
            globalVars = getBestDG(globalVars,thisOrder,errorCheck=errorCheck)
        # raise SystemError

        # if i==2:
        #     break

        if len(ordersNow.index) != 0:
            program_stats = program_stats.append(pd.Series([i,len(ordersNow.index),round((time()-t1)/len(ordersNow.index),2),round(time())],index=program_stats.columns),ignore_index=True)
            print 'minute'+'\t'+str(i)+'\t'+'orders='+'\t'+str(len(ordersNow.index))+'\t'+str((time()-t1)/len(ordersNow.index))+'\t'+str(time())


    # move remaining orders at close to 'delivered'
    if now == totalTime: globalVars = update_global_vars(globalVars,'update per minute',globalVars[0].end_time.max())
    if save == True: export_all_data(globalVars,program_stats)
    print 'done'
    print time()-t1A
    return


RUN_CHAOS_SIMULATION(makeData,showSimData,runNormalDel,load,save,resume,errorCheck,global_op_vars)
