from classes import Vendor,Delivery,DG
from pg_fxs import pg_get_random_pt_in_circle_around_node
from pg_fxs import pg_get_cir_ctr_and_rad_bounding_way_box,pg_get_nodes_in_geom
from rd_lib import engine,time,this_cwd,pd,np,gd,way_t,vert_t,vert_g
import assumptions as A
from pg_fxs import geom_inside_street_box,make_column_primary_serial_key
from random import randrange


def make_simulation_data_from_real_data(savePath=''):

    if savePath == '': savePath=this_cwd+'/sim_data/vendor_sim_data.txt'
    a = Vendor()
    col_names = a.toDict().keys()
    df = pd.DataFrame(columns=col_names)

    vdf=geom_inside_street_box(A.work_area,geom_table='vendors',geom_label='geom',
                               table_cols=['seam_id','node'],conditions=None)

    if len(vdf)>A.vend_num: vdf=vdf.ix[:A.vend_num,:]

    vendors = []
    for i in range(0,A.vend_num):
        it = vdf.ix[i,:]
        v = Vendor()
        v.vend_id = i
        vend_node = it.node
        v.delivery.start_node = vend_node
        deliv_per_vend = randrange(*A.deliveries_per_vend)
        for j in range(0,deliv_per_vend):
            v.delivery.order_time = randrange(0,A.vend_hours_delivering*60)
            status,rand_pt_in_cir,rand_node = pg_get_random_pt_in_circle_around_node(vend_node,cir_radius=A.deliv_radius_per_vendor_in_km)
            if status!='ok':
                raise SystemError
            # v.delivery.end_point = rand_pt_in_cir
            v.delivery.end_node = rand_node
            vendors.append(v.toDict())

    df = pd.DataFrame(vendors)
    df['deliv_id'] = df.index
    df = df.ix[:,   ['vend_id',
                     'order_time',
                     'deliv_id',
                     'start_node',
                     'end_node'
                    ]]
    df['order_time'] = df.order_time.astype(float)
    df[['vend_id','deliv_id','start_node','end_node']] = df[['vend_id','deliv_id',
                                                             'start_node','end_node']].astype(int)
    df.to_hdf(savePath.rstrip('.txt')+'.h5','table')
    engine.execute('drop table if exists sim_data')
    df.to_sql('sim_data',engine,index=False)
    make_column_primary_serial_key(table='sim_data',p_key='gid',new_col=True)
    return df
def make_simulation_data(savePath=''):
    if savePath == '': savePath=this_cwd+'/sim_data/vendor_sim_data.txt'

    a = Vendor()
    a = a.printHeader(printer=False,fullHeading=True)
    z = a.split('\t')

    col_names = a.to
    df = pd.DataFrame(columns=col_names)

    vend,vendors = a+'\r',[]
    for i in range(0,A.vend_num):
        v = Vendor()
        v.id = i
        x = 3*randrange(0,A.vend_loc_x_max) #note: the "3*" is based on 1 avenue = 3 streets
        y = randrange(0,A.vend_loc_y_max)
        v.vend_X = x
        v.vend_Y = y
        for j in range(0,A.deliveries_per_vend):
            v.order_num = j
            stop = False
            # while stop == False:
            x_min,x_max = v.vend_X-(int(round((A.vend_del_x_range/2.0)))*3),v.vend_X+(int(round((A.vend_del_x_range/2.0)))*3)
            y_min,y_max = v.vend_Y-int(round((A.vend_del_y_range/2.0))),v.vend_Y+int(round((A.vend_del_y_range/2.0)))
            x = 3*int(round(randrange((x_min/3.0),(x_max/3.0)),0))
            y = int(round(randrange(y_min,y_max),0))
            # if sqrt((x-vend_loc_x_max)**2 + (y-vend_loc_y_max)**2) < vend_deliver_radius:
            v.delivery.start_X = v.vend_X
            v.delivery.start_Y = v.vend_Y
            v.delivery.order_time = randrange(0,A.vend_hours_delivering*60)
            v.delivery.end_X = x
            v.delivery.end_Y = y
            # stop = True
            vend += v.toString()+'\r'
            vendors.append(v)
            df = df.append(dict(zip(col_names,v.toList())),ignore_index=True)

    f = open(savePath,'w')
    f.write(vend)
    f.close()
    df.deliv_id = df.index
    df = df.drop(['start_time','end_time','total_order_time','travel_time'],axis=1)
    df = pd.DataFrame(df.astype(np.intc).as_matrix(),columns=df.columns)
    df.to_hdf(savePath.rstrip('.txt')+'.h5','table')
    return df
def open_pd_sim_data(openPath=''):
    if openPath == '': openPath=this_cwd+'/sim_data/pd_vendor_sim_data.txt'
    DTYPES={'id':np.long,
           'vend_X':np.long,
           'vend_Y':np.long,
           'order_num':np.dtype(np.intc),
           #'deliv_id':np.dtype(np.intc),
           'order_time':np.dtype(np.intc),
           #'start_time':np.dtype(np.intc),
           'start_X':np.dtype(np.intc),
           'start_Y':np.dtype(np.intc),
           #'end_time':np.dtype(np.intc),
           'end_X':np.dtype(np.intc),
           'end_Y':np.dtype(np.intc),
           #'total_order_time':np.dtype(np.intc),
           #'travel_time':np.dtype(np.intc)
           }
    df=pd.read_csv(openPath,sep='\t', header=0)
    df2=pd.read_csv(openPath,converters=DTYPES,sep='\t', header=0)
    try:
        df['vend_X']=df['vend_X'].map(lambda x: eval(x))
        df['vend_Y']=df['vend_Y'].map(lambda x: eval(x))
        df['start_X']=df['start_X'].map(lambda x: eval(x))
        df['start_Y']=df['start_Y'].map(lambda x: eval(x))
        df['end_X']=df['end_X'].map(lambda x: eval(x))
        df['end_Y']=df['end_Y'].map(lambda x: eval(x))
    except:
        pass
    return df
def open_simulation_data(openPath=''):
    if openPath == '': openPath=this_cwd+'/sim_data/vendor_sim_data.txt'
    f=open(openPath,'r')
    output=f.read()
    f.close()
    output=output[:-1].split('\r')
    vendorsB=[]
    for it in output:
        v=Vendor()
        v.fromString(it)
        vendorsB.append(v)
    return vendorsB
def init_dg_pool(pt,dg_grp_size=None,old_dg_pool=False,load=False,save=False,filePath=''):

    # if filePath == '': filePath=this_cwd+'/sim_data/pd_dg_pool.txt'
    if load == True:
        # new_dg_pool = gd.read_postgis("select dg_id,total_delivered,current_deliveries,st_geomfromtext(dg_node) geom from dg_pool",engine)
        new_dg_pool = pd.read_sql("select * from dg_pool",engine)

    elif load==False and type(old_dg_pool)==bool:
        from rd_lib import dg_pool_cols_types
        # DG_start_location_grid = A.DG_start_location_grid
        new_dg_pool = pd.DataFrame({'dg_id':range(pt*A.DG_num,(A.DG_num*pt)+A.DG_num)})
        ## get info for circle that bounds way box
        # cir_ctr,cir_rad = pg_get_cir_ctr_and_rad_bounding_way_box(A.work_area)
        ## get random points within circle
        node_ids = pg_get_nodes_in_geom()
        node_cnt = len(node_ids)
        new_dg_pool['dg_node'] = new_dg_pool.dg_id.map(lambda s: node_ids.ix[randrange(0,node_cnt),'id'])
        new_dg_pool['dest_node'] = new_dg_pool.index*0
        new_dg_pool['total_delivered'] = new_dg_pool.index*0
        new_dg_pool['current_deliveries'] = new_dg_pool.index*0
        for k,v in dg_pool_cols_types.iteritems():
            new_dg_pool[k]=new_dg_pool[k].astype(v)
        new_dg_pool = new_dg_pool.ix[:,dg_pool_cols_types.keys()]

        if save == True:
            if old_dg_pool==None:  engine.execute('drop table if exists dg_pool')
            new_dg_pool.drop(['dg_id'],axis=1).to_sql('dg_pool',engine,if_exists='append',index=False)
            if old_dg_pool==None:  make_column_primary_serial_key(table='dg_pool',p_key='dg_id',new_col=True)

    if type(old_dg_pool)!=bool:
        maxID = old_dg_pool.dg_id.values.max()
        new_dg_pool.dg_id = new_dg_pool.dg_id.values + (maxID+1)
        new_dg_pool = pd.merge(old_dg_pool,new_dg_pool,how='outer').sort('dg_id').reset_index(drop=True)

    return new_dg_pool

def init_global_vars(load,save,resume):
    # from classes import Vendor,Delivery,DG
    from rd_lib import MODEL_order_q,MODEL_dg_q
    if resume==False:
        order_q         = MODEL_order_q.copy()
        order_delivered = order_q.copy()
        dg_pool_pt      = 0
        dg_pool         = init_dg_pool(pt=dg_pool_pt,old_dg_pool=False,load=load,save=save,filePath='')
        dg_q            = MODEL_dg_q.copy()
        dg_delivered    = dg_q.copy()
        program_stats   = pd.DataFrame(columns=['order_minute','order_count',
                                                'average_time_per_order','running_epoch'])
        stpt=0

    else:
        globalVars_plus = get_saved_global_vars()
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,program_stats = globalVars_plus
        try:
            if int(order_delivered.order_time.max())+1 == A.vend_hours_delivering*60:
                print '\nSimulation is completed.\n',A.vend_hours_delivering*60,'minutes simulated.\n'
                return None
            else: stpt = int(order_q.order_time.max().astype(pd.np.int64)+1)
        except:
            stpt = int(order_q.order_time.max().astype(pd.np.int64)+1)

        dg_pool_pt = int((len(dg_pool.index)/A.DG_pool_grp_part_size)-1)

    globalVars_plus = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt,program_stats,stpt
    return globalVars_plus
def get_saved_global_vars():
    order_q_Path=this_cwd+'/sim_data/EDA_order_q_data.txt'
    dg_q_Path=this_cwd+'/sim_data/EDA_dg_q_data.txt'
    dg_pool_Path=this_cwd+'/sim_data/EDA_dg_pool.txt'
    order_delivered_Path=this_cwd+'/sim_data/EDA_order_delivered.txt'
    dg_delivered_Path=this_cwd+'/sim_data/EDA_dg_delivered.txt'
    program_stats_Path = this_cwd+'/sim_data/program_stats.txt'
    order_q = pd.read_csv(order_q_Path, na_values=[' '], sep='\t')
    dg_q = pd.read_csv(dg_q_Path, na_values=[' '],  sep='\t')
    dg_pool = pd.read_csv(dg_pool_Path, na_values=[' '],  sep='\t')
    order_delivered = pd.read_csv(order_delivered_Path, na_values=[' '],  sep='\t')
    dg_delivered = pd.read_csv(dg_delivered_Path, na_values=[' '], sep='\t')
    program_stats = pd.read_csv(program_stats_Path, na_values=[' '], sep='\t')
    # program_stats.running_epoch = (time() - program_stats.running_epoch.max()) + program_stats.running_epoch
    globalVars_plus = order_q,order_delivered,dg_q,dg_delivered,dg_pool,program_stats
    return globalVars_plus
