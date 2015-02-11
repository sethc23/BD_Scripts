# Data Visualization
def DISPLAY_REAL_DATA():
    import matplotlib.pyplot as plt
    from matplotlib.colors import colorConverter

    def pythag(x1,y1,x2,y2):
        # x1,y1,x2,y2 = [x for x in s]
        a,b=(x2-x1)**2,(y2-y1)**2
        return sqrt(a+b)
    def fig2():
        # create plot
        fig, ax1 = plt.subplots(figsize=(10,10))
        fig.canvas.set_window_title('A Visualization of Simulation Data')
        ax1.set_title('Distribution of NYC Vendors, Delivery Locations, and Delivery Coverage Areas')
        ax1.set_xlabel('Avenues')
        ax1.set_ylabel('Streets')
        # add values
        colorBox = {'vendLoc':'firebrick',
                    'vendLocEdge':'black',
                    'vendRadius':'royalblue',
                    'delivHeat':'#00FF00',
                    'delivEdge':'black',
                    'delivPoint':'black',
                    'legendText':'black',
                    'fig_bg':fig.get_facecolor()}

        markerBox = {'vendPt':'o',
                     'delivPt':'x'}

        for i in range(1,vLocCountMax):
            plotPts = vudf[vudf.locCount==i].ix[:,['x','y']].as_matrix().tolist()
            plt.plot(*zip(*plotPts), marker=markerBox['vendPt'],markersize=2+(3*i), color=colorBox['vendLoc'], ls='')
        A=vdf[['xloc','yloc','maxDist']].as_matrix().tolist()
        for x,y,r in A:
            ax1.add_artist(plt.Circle(xy=(x, y), radius=r, transform=ax1.transData._b, color=colorBox['vendRadius'], alpha=0.05))
        B=odf[['xloc','yloc','percentage']].as_matrix().tolist()
        for x,y,p in B:
            ax1.add_artist(plt.Rectangle(xy=(x-1.5, y-.5), height=1,width=3,transform=ax1.transData._b, edgecolor=colorBox['delivEdge'],
                                         facecolor=colorConverter.to_rgba(colorBox['delivHeat'], alpha=p)))

        # plt.plot(*zip(*uniqDeliveryLocs), marker=markerBox['delivPt'],markersize=5, color=colorBox['delivPoint], ls='')
        # add plot ticks and labels
        x_tick_num = np.arange(odf.xloc.astype(pd.np.int64).min(),odf.xloc.astype(pd.np.int64).max()+1,3)
        y_tick_num = np.arange(odf.yloc.astype(pd.np.int64).min(),odf.yloc.astype(pd.np.int64).max()+1,1)
        plt.xticks(x_tick_num)
        plt.yticks(y_tick_num)
        x_tick_label = Assumption('avenues')[-1*len(x_tick_num):]
        y_tick_label = (23+y_tick_num.min())+y_tick_num
        xtickNames = plt.setp(ax1, xticklabels=x_tick_label)
        plt.setp(xtickNames, rotation=45, fontsize=10)
        ytickNames = plt.setp(ax1, yticklabels=y_tick_label)
        plt.setp(xtickNames, fontsize=8)
        ax1.grid(which='both',axis='both')
        plt.setp(ax1.get_xticklabels(minor=True), visible=True)
        # fix plot axes
        x1,x2,y1,y2=ax1.axis()
        x_max,y_max = odf.xloc.astype(pd.np.int64).max(),odf.yloc.astype(pd.np.int64).max()
        x_min,y_min = odf.xloc.astype(pd.np.int64).min(),odf.yloc.astype(pd.np.int64).min()
        x_buff=6
        y_buff=3
        plt.axis([x_min-x_buff,x_max+x_buff,y_min-y_buff,y_max+y_buff])
        # add legend
        plt.figtext(0.79, 0.1,  str(len(vend_ids)) + ' Vendors (size=count)',verticalalignment='center',
                    bbox=dict(facecolor=colorBox['vendLoc'],edgecolor=colorBox['legendText']),
                    color=colorBox['legendText'],weight='heavy',fontsize=10,zorder=0)

        plt.figtext(0.79, 0.075, 'Vendor Delivery Radius',verticalalignment='center',
                    bbox=dict(facecolor=colorBox['vendRadius'],edgecolor=colorBox['legendText'], alpha=0.80),
                    color=colorBox['legendText'], weight='roman', fontsize=10,zorder=10)

        plt.figtext(0.79, 0.05, 'Delivery Locations (color=count)',verticalalignment='center',
                    bbox=dict(facecolor=colorBox['delivHeat'],edgecolor=colorBox['legendText']),
                    color='black', weight='heavy',fontsize=10,zorder=10)

        # adjust spacing and show plot
        plt.subplots_adjust(hspace=0.5)
        plt.show()


    real_gps_Path=this_cwd+'/vendor_data/vendor_gps.txt'
    realdata = pd.read_csv(real_gps_Path, sep='\t')


    import np as np
    import np.random
    import matplotlib.pyplot as plt

    from matplotlib import cm as CM


    realdata = pd.read_csv(real_gps_Path, sep='\t')
    realdata['x'] = realdata['Long.']
    realdata['y'] = realdata['Lat.']


    x_min,x_max = -73.9910,-73.9812
    y_min,y_max = 40.7150,40.7330
    # boxPts=[ [-73.9910,40.7150],        # a,b,c,d == W,N,E,S
    #          [-73.9910,40.7330],
    #          [-73.9812,40.7330],
    #          [-73.9812,40.7150] ]
    # a,b,c,d = boxPts
    # AB = (b[1]-a[1])/(b[0]-a[0])
    # b1 = (a[1]-(AB*a[0]))
    #
    # AD = (d[1]-a[1])/(d[0]-a[0])
    # b2 = (a[1]-(AD*a[0]))
    #
    # BC = (c[1]-b[1])/(c[0]-b[0])
    # b3 = (c[1]-(BC*c[0]))
    #
    # DC = (c[1]-d[1])/(c[0]-d[0])
    # b4 = (c[1]-(DC*c[0]))


    realdata['inBox'] = realdata.ix[:,['x','y']].apply(lambda s: True if (x_min<=s[0]<=x_max and y_min<=s[1]<=y_max) else False,axis=1)
    graphData = realdata[realdata.inBox==True]
    x=np.array(graphData.x.values,dtype=np.float_)
    y=np.array(graphData.y.values,dtype=np.float_)
    # x=np.array(realdata.long.values,dtype=np.float_)
    # y=np.array(realdata.lat.values,dtype=np.float_)
    plt.subplot(111)

    plt.hexbin(x, y, gridsize=30, cmap=CM.jet, bins=None)
    plt.axis([x_min,x_max,y_min,y_max])
    # plt.axis([min(x.tolist()), max(x.tolist()),
    #           min(y.tolist()), max(y.tolist())])

    cb = plt.colorbar()
    cb.set_label('mean value')
    plt.show()

    # heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
    # extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # plt.clf()
    # plt.imshow(heatmap, extent=extent)
    # plt.show()


    return
def DISPLAY_SIMULATION_DATA():
    import matplotlib.pyplot as plt
    from matplotlib.colors import colorConverter

    def pythag(x1,y1,x2,y2):
        # x1,y1,x2,y2 = [x for x in s]
        a,b=(x2-x1)**2,(y2-y1)**2
        return sqrt(a+b)
    def fig2():
        # create plot
        fig, ax1 = plt.subplots(figsize=(10,10))
        fig.canvas.set_window_title('A Visualization of Simulation Data')
        ax1.set_title('Distribution of NYC Vendors, Delivery Locations, and Delivery Coverage Areas')
        ax1.set_xlabel('Avenues')
        ax1.set_ylabel('Streets')
        # add values
        colorBox = {'vendLoc':'firebrick',
                    'vendLocEdge':'black',
                    'vendRadius':'royalblue',
                    'delivHeat':'#00FF00',
                    'delivEdge':'black',
                    'delivPoint':'black',
                    'legendText':'black',
                    'fig_bg':fig.get_facecolor()}

        markerBox = {'vendPt':'o',
                     'delivPt':'x'}

        for i in range(1,vLocCountMax):
            plotPts = vudf[vudf.locCount==i].ix[:,['x','y']].as_matrix().tolist()
            plt.plot(*zip(*plotPts), marker=markerBox['vendPt'],markersize=2+(3*i), color=colorBox['vendLoc'], ls='')
        A=vdf[['xloc','yloc','maxDist']].as_matrix().tolist()
        for x,y,r in A:
            ax1.add_artist(plt.Circle(xy=(x, y), radius=r, transform=ax1.transData._b, color=colorBox['vendRadius'], alpha=0.05))
        B=odf[['xloc','yloc','percentage']].as_matrix().tolist()
        for x,y,p in B:
            ax1.add_artist(plt.Rectangle(xy=(x-1.5, y-.5), height=1,width=3,transform=ax1.transData._b, edgecolor=colorBox['delivEdge'],
                                         facecolor=colorConverter.to_rgba(colorBox['delivHeat'], alpha=p)))

        # plt.plot(*zip(*uniqDeliveryLocs), marker=markerBox['delivPt'],markersize=5, color=colorBox['delivPoint], ls='')
        # add plot ticks and labels
        x_tick_num = np.arange(odf.xloc.astype(pd.np.int64).min(),odf.xloc.astype(pd.np.int64).max()+1,3)
        y_tick_num = np.arange(odf.yloc.astype(pd.np.int64).min(),odf.yloc.astype(pd.np.int64).max()+1,1)
        plt.xticks(x_tick_num)
        plt.yticks(y_tick_num)
        x_tick_label = Assumption('avenues')[-1*len(x_tick_num):]
        y_tick_label = (9+y_tick_num.min())+y_tick_num
        xtickNames = plt.setp(ax1, xticklabels=x_tick_label)
        plt.setp(xtickNames, rotation=45, fontsize=10)
        ytickNames = plt.setp(ax1, yticklabels=y_tick_label)
        plt.setp(xtickNames, fontsize=8)
        ax1.grid(which='both',axis='both')
        plt.setp(ax1.get_xticklabels(minor=True), visible=True)
        # fix plot axes
        x1,x2,y1,y2=ax1.axis()
        x_max,y_max = odf.xloc.astype(pd.np.int64).max(),odf.yloc.astype(pd.np.int64).max()
        x_min,y_min = odf.xloc.astype(pd.np.int64).min(),odf.yloc.astype(pd.np.int64).min()
        x_buff=6
        y_buff=3
        plt.axis([x_min-x_buff,x_max+x_buff,y_min-y_buff,y_max+y_buff])
        # add legend
        plt.figtext(0.79, 0.1,  str(len(vend_ids)) + ' Vendors (size=count)',verticalalignment='center',
                    bbox=dict(facecolor=colorBox['vendLoc'],edgecolor=colorBox['legendText']),
                    color=colorBox['legendText'],weight='heavy',fontsize=10,zorder=0)

        plt.figtext(0.79, 0.075, 'Vendor Delivery Radius',verticalalignment='center',
                    bbox=dict(facecolor=colorBox['vendRadius'],edgecolor=colorBox['legendText'], alpha=0.80),
                    color=colorBox['legendText'], weight='roman', fontsize=10,zorder=10)

        plt.figtext(0.79, 0.05, 'Delivery Locations (color=count)',verticalalignment='center',
                    bbox=dict(facecolor=colorBox['delivHeat'],edgecolor=colorBox['legendText']),
                    color='black', weight='heavy',fontsize=10,zorder=10)

        # adjust spacing and show plot
        plt.subplots_adjust(hspace=0.5)
        plt.show()

    sim_data_Path=this_cwd+'/sim_data/vendor_sim_data.txt'
    sim_data = pd.read_hdf(sim_data_Path.rstrip('.txt')+'.h5', 'table')
    sim_data = sim_data.sort_index(by=['order_time','vend_Y','vend_X'], ascending=[True,True,True])

    # sim data --> vendors
    vend_ids = sim_data.id.unique()
    vend_id_grp = sim_data.groupby(by='id')
    vdf = pd.DataFrame({'id':vend_ids})
    vdf['locations'] = vdf.id.map(lambda s: vend_id_grp.get_group(s).reset_index(drop=True).ix[0,['vend_X','vend_Y']].tolist())
    vend_loc_list = vdf.locations.map(lambda s: str(s)).tolist()
    vend_loc_list_uniq = dict(zip(vend_loc_list,range(len(vend_loc_list)))).keys()

    vudf = pd.DataFrame({'uniqVends':dict(zip(vend_loc_list_uniq,range(len(vend_loc_list)))).keys()})
    vudf['locCount'] = vudf.uniqVends.map(lambda s: vend_loc_list.count(str(s)))
    vLocCountMax = vudf.locCount.max()
    vudf['x'] = vudf.uniqVends.map(lambda s: eval(s)[0])
    vudf['y'] = vudf.uniqVends.map(lambda s: eval(s)[1])
    vudf['locPercentage'] = vudf.locCount.map(lambda s: s/float(vLocCountMax))

    vdf['xloc'] = vdf.locations.map(lambda s: int(s[0]))
    vdf['yloc'] = vdf.locations.map(lambda s: int(s[1]))
    vdf['minx'] = vdf.id.map(lambda s: int(vend_id_grp.get_group(s).end_X.min()))
    vdf['maxx'] = vdf.id.map(lambda s: int(vend_id_grp.get_group(s).end_X.max()))
    vdf['miny'] = vdf.id.map(lambda s: int(vend_id_grp.get_group(s).end_Y.min()))
    vdf['maxy'] = vdf.id.map(lambda s: int(vend_id_grp.get_group(s).end_Y.max()))
    vdf['topleft'] = vdf[['xloc','yloc','minx','maxy']].apply(lambda s: pythag(*s),axis=1)
    vdf['topright'] = vdf[['xloc','yloc','maxx','maxy']].apply(lambda s: pythag(*s),axis=1)
    vdf['botright'] = vdf[['xloc','yloc','maxx','miny']].apply(lambda s: pythag(*s),axis=1)
    vdf['botleft'] = vdf[['xloc','yloc','minx','miny']].apply(lambda s: pythag(*s),axis=1)
    vdf['maxDist'] = vdf[['topleft','topright','botright','botleft']].apply(lambda s: max(*s),axis=1)
    # sim data --> orders/deliveries
    allDeliveryLocs = sim_data.ix[:,['end_X','end_Y']].as_matrix().tolist()
    deliv_dict = dict(zip([str(it) for it in allDeliveryLocs],range(0,len(allDeliveryLocs)))).keys()
    uniqDeliveryLocs = [eval(it) for it in deliv_dict]
    odf = pd.DataFrame({'deliveryLocs':uniqDeliveryLocs})
    odf['xloc'] = odf.deliveryLocs.map(lambda s: s[0])
    odf['yloc'] = odf.deliveryLocs.map(lambda s: s[1])
    odf['orderCount'] = odf.deliveryLocs.map(lambda s: allDeliveryLocs.count(s))
    oCountMax = odf.orderCount.max()
    odf['percentage'] = odf.orderCount.map(lambda s: s/float(oCountMax))
    # odf2 = pd.DataFrame({'deliveryLocs':allDeliveryLocs})
    # odf2['xloc'] = odf2.deliveryLocs.map(lambda s: s[0])
    # odf2['yloc'] = odf2.deliveryLocs.map(lambda s: s[1])


    fig2()
    plt.show()
    return
def DISPLAY_NORMAL_DELIVERY_DATA():
    normal_del_Path=this_cwd+'/sim_data/ND_results.txt'
    norm_del_res = pd.read_csv(normal_del_Path, sep='\t')
    norm_del_res['return_travel_time'] = norm_del_res.ix[:,['tripEnd','vend_X','vend_Y','end_X','end_Y']].apply(lambda s: pd_get_travel_time(*s[1:]) if s[0]==True else 0,axis=1)

    vend_grps = norm_del_res.groupby('v_id')
    df = pd.DataFrame({'vendors':vend_grps.groups.keys()})
    df['max_dg_used'] = df.vendors.map(lambda s: vend_grps.get_group(s).dg_id.max())
    total_max_dg_used = df.max_dg_used.astype(pd.np.int64).max()
    df['total_hours'] = 0
    for it in range(total_max_dg_used):
        df['total_hours'] += df.vendors.map(lambda s: vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it].end_time.max() - vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it].start_time.min()).fillna(0).values
        df['total_hours'] += df.vendors.map(lambda s: vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it].sort('start_time').return_travel_time.astype(pd.np.int64).values[-1] if len(vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it])!=0 else 0).fillna(0).values


    chart=pd.DataFrame({'deliveryTimes':norm_del_res['end_time']-norm_del_res['order_time']})

    import matplotlib.pyplot as plt
    fig, ax1 = plt.subplots(figsize=(10,10))
    chart.deliveryTimes.hist(ax=ax1,bins=50)
    ax1.set_title('Distribution of Delivery Times')
    ax1.set_ylabel('No. of Deliveries')
    ax1.set_xlabel('Minutes per Delivery')
    plt.show()
def DISPLAY_EDA_DATA():
    import matplotlib.pyplot as plt
    from matplotlib.colors import colorConverter
    from datetime import datetime
    # from matplotlib import patches
    # import matplotlib.gridspec as gridspec

    sim_data_Path=this_cwd+'/sim_data/vendor_sim_data.txt'
    order_q_Path=this_cwd+'/sim_data/EDA_order_q_data.txt'
    dg_q_Path=this_cwd+'/sim_data/EDA_dg_q_data.txt'
    order_delivered_Path=this_cwd+'/sim_data/EDA_order_delivered.txt'
    dg_delivered_Path=this_cwd+'/sim_data/EDA_dg_delivered.txt'
    dg_pool_Path=this_cwd+'/sim_data/EDA_dg_pool.txt'
    prog_stats_path = this_cwd+'/sim_data/program_stats.txt'

    sim_data = pd.read_hdf(sim_data_Path.rstrip('.txt')+'.h5', 'table')
    sim_data = sim_data.sort_index(by=['order_time','vend_Y','vend_X'], ascending=[True,True,True])

    normal_del_Path=this_cwd+'/sim_data/ND_results.txt'
    norm_del_res = pd.read_csv(normal_del_Path, sep='\t')

    order_q = pd.read_csv(order_q_Path,sep='\t')
    order_delivered = pd.read_csv(order_delivered_Path,sep='\t')
    dg_q = pd.read_csv(dg_q_Path,sep='\t')
    dg_delivered = pd.read_csv(dg_delivered_Path,sep='\t')
    OD = pd.merge(order_delivered[order_delivered.status!='on route'],order_q[order_q.status!='on route'],how='outer')
    DG = pd.merge(dg_delivered,dg_q,how='outer')
    dg_pool = pd.read_csv(dg_pool_Path,sep='\t')
    program_stats = pd.read_csv(prog_stats_path,sep='\t')

    modelVars = Assumption(get_var='all')

    # program_stats data
    timeSimulated_program = int(program_stats.order_minute.max()-program_stats.order_minute.min())+1
    simulatedDuration = int((program_stats.running_epoch.max()-program_stats.running_epoch.min())/60)
    avg_sim_time_per_order,std_sim_time_per_order = round(program_stats.average_time_per_order.mean(),2),round(program_stats.average_time_per_order.std(),2)

    # normal delivery
    maxNormalEndtime = norm_del_res.end_time.max()
    if maxNormalEndtime < modelVars['totalTime']:
        adj_norm_del_res = norm_del_res[norm_del_res.start_time<=timeSimulated_program]
    else:
        adj_norm_del_res = norm_del_res

    adj_norm_del_res['return_travel_time'] = adj_norm_del_res.ix[:,['tripEnd','vend_X','vend_Y','end_X','end_Y']].apply(lambda s: pd_get_travel_time(*s[1:]) if s[0]==True else 0,axis=1)
    vend_grps = adj_norm_del_res.groupby('v_id')
    ndf = pd.DataFrame({'vendors':vend_grps.groups.keys()})
    # calc. for total hours, Base: vendors
    ndf['max_dg_used'] = ndf.vendors.map(lambda s: vend_grps.get_group(s).dg_id.max())
    total_dg_used_normal = ndf.max_dg_used.astype(pd.np.int64).sum()
    total_max_dg_used = ndf.max_dg_used.astype(pd.np.int64).max()
    ndf['total_hours'] = 0
    for it in range(total_max_dg_used):
        ndf['total_hours'] += ndf.vendors.map(lambda s: vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it].end_time.max() - vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it].start_time.min()).fillna(0).values
        ndf['total_hours'] += ndf.vendors.map(lambda s: vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it].sort('start_time').return_travel_time.astype(pd.np.int64).values[-1] if len(vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it])!=0 else 0).fillna(0).values
    norm_del_total_dg_time_min = ndf.total_hours.sum()
    norm_del_total_dg_time_hours = round(norm_del_total_dg_time_min/60.0,2)
    # calc. for delivery time, Base: orders
    norm_orders = pd.DataFrame({'deliveryTimes':adj_norm_del_res['end_time']-adj_norm_del_res['order_time']})

    # order data --> by DG
    dg_ids = OD.id.unique()
    dg_id_grp = OD.groupby(by='id')
    df = pd.DataFrame({'id':dg_ids})
    df['DeliveryCount'] = df.id.map(lambda s: len(dg_id_grp.get_group(s).index))
    ave_orders_per_dg,std_orders_per_dg = round(df.DeliveryCount.mean(),2),round(df.DeliveryCount.std(),2)
    df['total_contig_dg_time'] = df.id.map(lambda s: dg_id_grp.get_group(s).end_time.max() - dg_id_grp.get_group(s).start_time.min())

    change={}
    for ID in dg_ids:
        b=OD[OD.id==ID]
        a=pull_from_order(b,errorCheck=False)
        a['travel_time'] = a[['ptax','ptay','ptbx','ptby']].apply(lambda s: pd_get_travel_time(*s),axis=1)
        a['expectedArrival'] = a['pta-t'] + a['travel_time']
        a['passtimecheck'] = False
        goodInd = a[a['ptb-t'] == a['expectedArrival']].index
        a.ix[goodInd,'passtimecheck'] = True
        c = a[a.passtimecheck==False]
        c['restTime'] = c['ptb-t'] - c['expectedArrival']
        c['restTime'] = c.restTime.map(lambda s: s if s>0 else 0)
        change.update({ID:c.restTime.sum()})

    df['restTime'] = df.id.map(lambda s: change[s])
    df['actual_total_dg_time'] = df['total_contig_dg_time'] - df['restTime']

    total_contig_dg_time_min = df.total_contig_dg_time.sum()
    total_contig_dg_time_hours = round(total_contig_dg_time_min/60.0,2)
    time_efficiency_increase = round( (norm_del_total_dg_time_hours-total_contig_dg_time_hours)/float(norm_del_total_dg_time_hours)*100,2 )
    ave_total_contig_dg_hours,std_total_contig_dg_hours = round(df.total_contig_dg_time.mean()/60.0,2),round(df.total_contig_dg_time.std(),2)

    actual_total_dg_time_min = df.actual_total_dg_time.sum()
    actual_total_dg_time_hours = round(actual_total_dg_time_min/60.0,2)
    actual_timeEfficiencyIncrease = round( (norm_del_total_dg_time_hours-actual_total_dg_time_hours)/float(norm_del_total_dg_time_hours)*100,2 )
    ave_actual_total_dg_hours,std_actual_total_dg_hours = round(df.actual_total_dg_time.mean()/60.0,2),round(df.actual_total_dg_time.std(),2)

    deliveryCounts = df['DeliveryCount'].astype(pd.np.int64).values.tolist()
    deliv_num = df[df.DeliveryCount>0].DeliveryCount.unique()

    ##### CHART 1
    chart1 = pd.DataFrame({'DeliveryCountNums':deliv_num.tolist()})
    chart1['DelivCountFreq'] = chart1.DeliveryCountNums.map(lambda s: deliveryCounts.count(s))
    chart1 = chart1.sort_index(by='DeliveryCountNums',ascending=True)
    # plot1() # Frequency of Delivery Count

    # order data --> by deliveries
    timeSimulated_orders = OD.order_time.max()
    minTotalDGTime = round(df.actual_total_dg_time.min()/60.0,1)
    maxTotalDGTime = round(df.actual_total_dg_time.max()/60.0,1)
    dg_startHour = eval(str(minTotalDGTime)[:str(minTotalDGTime).find('.')])
    dg_endHour = eval(str(maxTotalDGTime)[:str(maxTotalDGTime).find('.')])
    if eval(str(minTotalDGTime)[-1])<=5: pass
    else: dg_startHour += .5

    if eval(str(maxTotalDGTime)[-1])<=5: dg_endHour += .5
    else: dg_endHour += 1

    ##### CHART 2
    chart2 = pd.DataFrame({'hours':np.arange(dg_startHour,dg_endHour+.25,.25)})
    chart2['dg_count'] = chart2.hours.map(lambda s: len(df[(df.actual_total_dg_time>=(s*60)) & (df.actual_total_dg_time<((s+.25)*60))].index))


    odf = pd.DataFrame({'del_id':OD.deliv_id})
    odf['allDeliveryLocs'] = odf.del_id.map(lambda s: OD[OD.deliv_id==s].reset_index(drop=True).ix[0,['end_X','end_Y']].astype(pd.np.int64).tolist())
    odf['deliveryTimes'] = OD['end_time'] - OD['order_time']
    maxTime = modelVars['max_delivery_time']
    odf['lateDelivery'] = odf.deliveryTimes.map(lambda s: True if s>maxTime else False)
    time_grouped = odf.groupby(by='deliveryTimes')
    time_unique = odf.groupby(by='deliveryTimes').groups.keys()
    # chart2 = pd.DataFrame({'TotalTimeNums':time_unique})
    # chart2['TotalTimeFreq'] = chart2.TotalTimeNums.map(lambda s: len(time_grouped.get_group(s).index))
    # plot2() # Distribution of Total Distance Traveled

    # order data -- locations
    # TODO: finish this part of the data for figure 2 (which should rely on orders delivered and not sim_data)
    # ldf = pd.DataFrame({'locations': np.unique(OD[['start_X','start_Y']].astype(pd.np.int64).as_matrix())})
    # uniq_pickup_locs = dict(zip(map(lambda s: str(s),ldf.locations),range(0,len(map(lambda s: str(s),ldf.locations)))))
    # ldf['xloc'] = ldf.locations.map(lambda s: int(s[0]))
    # ldf['yloc'] = ldf.locations.map(lambda s: int(s[1]))
    #
    # ldf['minx'] = ldf.id.map(lambda s: int(vend_id_grp.get_group(s).end_X.min()))
    # ldf['maxx'] = ldf.id.map(lambda s: int(vend_id_grp.get_group(s).end_X.max()))
    # ldf['miny'] = ldf.id.map(lambda s: int(vend_id_grp.get_group(s).end_Y.min()))
    # ldf['maxy'] = ldf.id.map(lambda s: int(vend_id_grp.get_group(s).end_Y.max()))
    #
    # ldf['topleft'] = ldf[['xloc','yloc','minx','maxy']].apply(lambda s: pythag(*s),axis=1)
    # ldf['topright'] = ldf[['xloc','yloc','maxx','maxy']].apply(lambda s: pythag(*s),axis=1)
    # ldf['botright'] = ldf[['xloc','yloc','maxx','miny']].apply(lambda s: pythag(*s),axis=1)
    # ldf['botleft'] = ldf[['xloc','yloc','minx','miny']].apply(lambda s: pythag(*s),axis=1)
    # ldf['maxDist'] = ldf[['topleft','topright','botright','botleft']].apply(lambda s: max(*s),axis=1)

    # chart3=pd.DataFrame({'deliveryTimes':sorted(OD['total_order_time'])})
    chart3=pd.DataFrame({'deliveryTimes':OD['end_time']-OD['order_time']})
    # plot3() # Distribution of Delivery Times

    # dg_q data
    DG['distance'] = DG['ptb-t']-DG['pta-t']
    DG_id_grp = DG.groupby(by='dg_id')
    dg_q = pd.DataFrame({'dg_id':DG_id_grp.groups.keys()})
    dg_q_id_cnt = len(dg_q.dg_id)
    dg_q['totalDistance']=dg_q.dg_id.map(lambda s: DG_id_grp.get_group(s).distance.sum())
    # plot2()

    # all data - By Time
    maxTime = OD.end_time.max()
    cf = pd.DataFrame({'Time':range(0,int(maxTime)+1)})
    cf['OrdersThisMinute']=cf.Time.map(lambda s: len(OD[OD.order_time==s]))
    cf['ActiveDeliveries']=cf.Time.map(lambda s: len(OD[(OD.end_time>=s) & (s>=OD.order_time)].index))
    cf['ActiveDG']=cf.Time.map(lambda s: len(OD[(OD.end_time>=s) & (s>=OD.order_time)].groupby(by='id').size().index))
    ave_activeDG_per_minute,std_activeDG_per_minute = round(cf[cf.Time<=timeSimulated_program-1].ActiveDG.mean(),2),round(cf[cf.Time<=timeSimulated_program-1].ActiveDG.std(),2)
    cf['ActiveDG_order_mean']=cf.Time.map(lambda s: OD[(OD.end_time>=s) & (s>=OD.order_time)].groupby(by='id').size().mean())
    ave_mean_of_orders_per_DG_per_min = round(cf[cf.Time<=timeSimulated_program-1].ActiveDG_order_mean.mean(),2)
    # plot5() # Number of Active Orders/DG

    fig = plt.figure(1,figsize=(18,12))


    def get_assumptions(text=True,get_txt_vars='',all=''):
        s=''
        return [s.join(str(k)+' = '+str(v)+'\n') for k,v in all if get_txt_vars.count(k)>0]

    def plot1():
        # subplot 1 / Left - deliveriesPerDG
        ax1_1 = plt.subplot2grid((4,3),(0,0), colspan=1)
        chart1.plot(x='DeliveryCountNums', y='DelivCountFreq', ax=ax1_1, kind='bar')
        #chart1.DelivCountFreq.hist(ax=ax1_1,bins=len(chart1.index))
        ax1_1.set_title('Distribution of Orders per DG')
        ax1_1.set_xlabel('Orders per DG')
        ax1_1.set_ylabel('No. of DG')
        # Total DG num, Orders per Vendor, Total Orders
        # Total distance traveled, total distance ordered
    def plot2():
        # subplot 1 / Middle
        ax1_2 = plt.subplot2grid((4,3),(0,1), colspan=1)
        # chart2.minutes.hist(ax=ax1_2,bins=chart2_binNum)#
        chart2. plot(x='hours', y='dg_count', ax=ax1_2, kind='bar')
        ax1_2.set_title('Distribution of Hours per DG')
        ax1_2.set_xlabel('Hours per DG')
        ax1_2.set_ylabel('No. of DG')
        # chart2.TotalTimeFreq.plot(ax=ax1_2,kind='bar')
        # chart2.TotalTimeFreq.hist(ax=ax1_2)#,bins=50)
        # ax1_2.set_title('Distribution of Total Distance Traveled')
        # ax1_2.set_xlabel('Blocks/Minutes per DG')
        # ax1_2.set_ylabel('No. of DG')
    def plot3():
        # subplot 1 / Right
        # fig = plt.figure(1,figsize=(18,10))
        ax1_3 = plt.subplot2grid((4,3),(0,2), colspan=1)
        colorBox = {'normalDeliv':'red',
                'edges':'black',
                'algoDeliv':'blue',
                'legendText':'black',
                'fig_bg':fig.get_facecolor()}
        norm_orders.deliveryTimes.hist(ax=ax1_3,bins=50,color=colorBox['normalDeliv'])
        chart3.deliveryTimes.hist(ax=ax1_3,bins=50,color=colorBox['algoDeliv'],alpha=0.8)
        ax1_3.set_title('Distribution of Delivery Times')
        ax1_3.set_ylabel('No. of Deliveries')
        ax1_3.set_xlabel('Minutes per Delivery')

        patches, labels = ax1_3.get_legend_handles_labels()
        upperLabels = ['Normal Delivery','Algo Delivery']
        from matplotlib.font_manager import FontProperties
        fontP = FontProperties()
        fontP.set_size('x-small')

        ax1_3.legend(patches,upperLabels,loc='upper left', #bbox_to_anchor=(1, -0.12),
                  prop=fontP,fancybox=True, shadow=True, ncol=1)

        # A=np.array(ax1_3.get_position()._points).flatten()
        # x1 = A[2]
        # y1 = A[2]-ax1_3.get_position()._get_height()-(.2*ax1_3.get_position()._get_height())
        # plt.figtext(x1, y1,  'Normal Delivery',verticalalignment='center',
        #             horizontalalignment='right',
        #             bbox=dict(facecolor=colorBox['normalDeliv'],edgecolor=colorBox['legendText']),
        #             color=colorBox['legendText'],weight='heavy',fontsize=10,zorder=0)
        # y2 = A[2]-ax1_3.get_position()._get_height()-(.32*ax1_3.get_position()._get_height())
        # plt.figtext(x1, y2,  'Algo Delivery',verticalalignment='center',
        #             horizontalalignment='right',
        #             bbox=dict(facecolor=colorBox['algoDeliv'],edgecolor=colorBox['legendText']),
        #             color=colorBox['legendText'],weight='heavy',fontsize=10)

    def plot4():
        #----- ROW 2
        # create subplot
        ax3 = plt.subplot2grid((4,3),(1,0), colspan=3)
        cf.plot(x='Time',y='ActiveDeliveries',ax=ax3)#,color='r')
        cf.plot(x='Time',y='ActiveDG',ax=ax3)#,color='g')

        ax3.minorticks_on()
        ax3.yaxis.tick_left()
        ax3.set_title('Number of Active Deliveries and DG (left)  /  Mean of Orders per DG (right)')
        ax3.set_ylabel('No. of Active')
        # overlay second plot of mean orders
        ax4 = ax3._make_twin_axes(sharex=ax3, frameon=False)
        # cf.plot(x='Time',y='OrdersThisMinute',ax=ax4,color='red')
        ln3 = cf.plot(x='Time',y='ActiveDG_order_mean',ax=ax4,color='#9900FF')
        ax4.yaxis.tick_right()
        ax4.set_ylabel('Mean of Orders per DG')
        ax4.yaxis.set_label_position('right')
        ax4.yaxis.set_offset_position('right')
        ax4.xaxis.set_visible(False)
        ax4.set_xlabel('Time (min)')
        # Shink current axis by 20% (in prep for putting legend on right
        box = ax3.get_position()
        # ax3.set_position([box.x0, box.y0 + box.height * 0.1,
        #                  box.width, box.height * 0.9])
        # ax4.set_position([box.x0, box.y0 + box.height * 0.1,
        #                  box.width, box.height * 0.9])

        # Put a legend below current axis
        patches, labels = ax3.get_legend_handles_labels()
        patches2, labels2 = ax4.get_legend_handles_labels()
        upperLabels = ['Active Deliveries','Active DG','New Orders Each Minute','Mean Order per DG']
        from matplotlib.font_manager import FontProperties
        fontP = FontProperties()
        fontP.set_size('x-small')

        ax3.legend(patches+patches2,upperLabels,loc='center', #bbox_to_anchor=(1, -0.12),
                  prop=fontP,fancybox=True, shadow=True, ncol=2)

        # ax3.set_position([box.x0, box.y0, box.width * 0.7, box.height])
        # ax4.set_position([box.x0, box.y0, box.width * 0.7, box.height])
        # add marker for end of simulated time
        ax3.axvline(x=timeSimulated_program,linewidth=2,color='black')
        x0,x1,y0,y1 = ax3.axis()
        ax3.annotate('End of Simulated Time', xy=(timeSimulated_program, int(round(y1/2.0))),
                     xytext=(timeSimulated_program-int(round(x1/8.0)), int(round(y1/2.0))+int(round(y1/7.0))),
                     color='grey',fontsize=10,
                     arrowprops=dict(headwidth=int(round(y1/20.0))*.8,width=int(round(y1/15.0))*.2,facecolor='grey', shrink=0.1)) #width='',frac=

        ax3.set_zorder(1) # make it on top
        ax3.set_frame_on(False) # make it transparent
        ax4.set_frame_on(True) # make sure there is any background
    def plot5():
        ax4 = plt.subplot2grid((4,3),(2,0), colspan=3, rowspan=2)
        ax4.set_title('\n')
        # ax.set_xlabel('xlabel')
        # ax.set_ylabel('ylabel')

        vendor_vars =[['Number of Vendors',modelVars['vend_num']],
                    ['Area of Vendor Population [Ave./St.]',[modelVars['avenues_of_vendors'],modelVars['streets_of_vendors']]],
                    ['Area of Delivery Coverage per Vendor [Ave./St.]',[modelVars['vend_deliver_avenues'],modelVars['vend_deliver_streets']]],
                    # ['Delivery Radius per Vendor [St.]',modelVars['vend_deliver_radius']],
                    ['Deliveries per Vendor',modelVars['deliveries_per_vend']],
                    ['Total Vendor Hours',modelVars['vend_hours_delivering']] ]


        dg_vars = [['Total Time [min]',60*modelVars['vend_hours_delivering']],
                   ['Max Delivery Time per Order',modelVars['max_delivery_time']],
                    ['Max DG Wait Time at Vendor',modelVars['wait_at_vendor']],
                    ['Max Travel Time to Next Loc',modelVars['max_travelToLocTime']],
                    ['Max Travel Time to Start Loc',modelVars['max_travelToStartLocTime']],
                    ['Max Delivery Per Person per 40 min.',modelVars['max_delivery_per_dg']],
                    ['Travel Speed per DG [min/St.]',modelVars['travel_speed']],
                    ['Area of Start Position for DG [Ave./St.]',list(modelVars['DG_start_location_grid [x,y]'])],
                    ['Static DG Start Positions?',modelVars['reuse_dg_pool']]]

        all_conds = vendor_vars + ['\n'] + dg_vars
        height = len(all_conds)+2
        width = 21
        buff=1.0
        x1,x2=buff+.2,buff+.3
        ax4.text(x2, height-1, 'Vendor Conditions', style='normal',fontsize=14,horizontalalignment='left')
        for i in range(0,len(all_conds)):
            it=all_conds[i]
            y=len(all_conds)-i
            if it == '\n': ax4.text(x2, y, 'DG Conditions', style='normal',fontsize=14,horizontalalignment='left')
            else:
                ax4.text(x1, y, str(all_conds[i][1]), style='normal',color='grey',fontsize=11.5,horizontalalignment='right')
                ax4.text(x2, y, ' =  '+str(all_conds[i][0]), style='normal',color='grey',fontsize=11.5,horizontalalignment='left')

        startMinute = int(OD.order_time.min())
        endMinute = int(OD.order_time.max())
        deliv_ids = OD.deliv_id
        deliv_ids_all = deliv_ids.tolist()
        deliv_ids_uniq = deliv_ids.unique().tolist()
        combined_dgIDs = OD.id.unique().tolist() + order_q.id.unique().tolist()
        # dgIDs_uniq = OD.id.unique().tolist()
        dgIDs_uniq = dict(zip(combined_dgIDs,range(0,len(combined_dgIDs)))).keys()

        sim_results =[
                    ['Total Orders Delivered',len(deliv_ids_all)],
                    ['Total DG for Normal Delivery',total_dg_used_normal],
                    ['Total DG for Algo Delivery',len(dgIDs_uniq)],
                    ['Ave. Number of Orders per DG',ave_orders_per_dg],
                    ['Ave. Number of Contig. Hours per DG',ave_total_contig_dg_hours],
                    ['Ave. Mean of Orders per DG per Minute',ave_mean_of_orders_per_DG_per_min],
                    ['Ave. Number of Active DG per Minute (A)',ave_activeDG_per_minute],
                    ['Actual DG Hour Total for Algo-Based Delivery',actual_total_dg_time_hours],
                    ['Contig. DG Hour Total for Algo-Based Delivery',total_contig_dg_time_hours],
                    ['Contig. DG Hour Total for Normal Delivery',norm_del_total_dg_time_hours],
                    ['Eff. Increase in Contig. Labor Time [%]',time_efficiency_increase],
                    ['Eff. Increase in Actual Labor Time [%]',actual_timeEfficiencyIncrease],
                    ['Eff. Increase in DG Count ( A / vendor count ) [%]',round( 100*( (float(modelVars['vend_num']) - ave_activeDG_per_minute) / float(modelVars['vend_num']) ),2)]
                    ]

        # sim_stats = [
        #             # ['[Ave. & Std.] of Active DG per Minute',[ave_activeDG_per_minute,std_activeDG_per_minute]],
        #             # ['Ave. Mean of Orders per DG per Minute',ave_mean_of_orders_per_DG_per_min],
        #             # ['[Ave. & Std.] of Total DG Hours (Max. - Min.)',[ave_total_dg_hours,std_total_dg_hours]],
        #             # ['[Ave. & Std.] of Total DG Orders',[ave_orders_per_dg,std_orders_per_dg]]
        #             ]

        sim_results_data = [['Total Minutes Simulated',timeSimulated_program],
                            ['Simulation Duration [min]',simulatedDuration],
                            ['[Avg. & Std.] of Simulation Time [sec] per Order',[avg_sim_time_per_order,std_sim_time_per_order]]
                            ]

        sim_vars = sim_results + ['3'] +  sim_results_data
        x1,x2=x1+(width/3),x2+(width/3)
        ax4.text(x2, height-1, 'Results', style='normal',fontsize=14,horizontalalignment='left')
        for i in range(0,len(sim_vars)):
            it = sim_vars[i]
            y=len(all_conds)-i
            if it == '2': ax4.text(x2, y, 'Result Stats.', style='normal',fontsize=14,horizontalalignment='left')
            elif it == '3': ax4.text(x2, y, 'Simulation Info.', style='normal',fontsize=14,horizontalalignment='left')
            else:
                ax4.text(x1, y, str(it[1]), style='normal',color='blue',fontsize=11.5,horizontalalignment='right')
                ax4.text(x2, y, ' =  '+str(it[0]), style='normal',color='blue',fontsize=11.5,horizontalalignment='left')

        # Quality Check 1
        onlyUniqueDeliveryIDs_A = len(deliv_ids_all)
        onlyUniqueDeliveryIDs_B = len(deliv_ids_uniq)
        if onlyUniqueDeliveryIDs_A == onlyUniqueDeliveryIDs_B: onlyUniqueDeliveryIDs = True
        else: onlyUniqueDeliveryIDs = False
        # Quality Check 2
        lateDeliveries = odf[odf['lateDelivery']==True].deliveryTimes
        allTimelyDelivered_A = lateDeliveries.shape[0]
        allTimelyDelivered_B = 0
        if allTimelyDelivered_A == allTimelyDelivered_B: allTimelyDelivered=True
        else: allTimelyDelivered=False
        # Quality Check 3
        totalOrderMatch_A = len(sim_data.index)
        totalOrderMatch_B = modelVars['vend_num']*modelVars['deliveries_per_vend']
        if totalOrderMatch_A == totalOrderMatch_B: totalOrderMatch=True
        else: totalOrderMatch=False
        # Quality Check 4
        OD_sim_order_cnt_A = len(deliv_ids_all)+len(order_q[order_q.order_time<=timeSimulated_program-1])
        OD_sim_order_cnt_B = totalOrderMatch_A
        if OD_sim_order_cnt_A == OD_sim_order_cnt_B: OD_sim_order_cnt=True
        else: OD_sim_order_cnt=False
        # Quality Check 5
        OD_DG_pool_order_cnt_A = OD_sim_order_cnt_A # order queue
        OD_DG_pool_order_cnt_B = dg_pool.total_delivered.sum()
        if OD_DG_pool_order_cnt_A == OD_DG_pool_order_cnt_B: OD_DG_pool_order_cnt=True
        else: OD_DG_pool_order_cnt=False
        # Quality Check 6
        OD_dg_pool_id_cnt_A = len(dgIDs_uniq)
        OD_dg_pool_id_cnt_B = len(dg_pool[(dg_pool.current_deliveries!=0) | (dg_pool.total_delivered!=0)].id.tolist())
        if OD_dg_pool_id_cnt_A == OD_dg_pool_id_cnt_B: OD_dg_pool_id_cnt = True
        else: OD_dg_pool_id_cnt = False
        # Quality Check 7
        OD_dg_id_cnt_A = len(dgIDs_uniq)
        OD_dg_id_cnt_B = dg_q_id_cnt
        if OD_dg_id_cnt_A == OD_dg_id_cnt_B: OD_dg_id_cnt = True
        else: OD_dg_id_cnt = False


        check_vars =    [
                        ['Only Unique DeliveryIDs in Order Queue?','onlyUniqueDeliveryIDs'],        # QC 1
                        ['All Orders Delivered within '+str(modelVars['max_delivery_time'])+
                         ' minutes?','allTimelyDelivered'],                                         # QC 2
                        ['Count of Orders:  Sim. data == Assumptions?','totalOrderMatch'],          # QC 3
                        ['Count of Orders:  Order Queue == Sim. data?','OD_sim_order_cnt'],         # QC 4
                        ['Count of Orders:  Order Queue == DG Pool?','OD_DG_pool_order_cnt'],       # QC 5
                        ['Count of IDs:  Order Queue == DG Pool?','OD_dg_pool_id_cnt'],             # QC 6
                        ['Count of IDs:  Order Queue == DG Queue?','OD_dg_id_cnt']                  # QC 7
                        ]

        x1,x2,x3=width-(width/3.0),width-buff-.3,width-(width/3.0)+((width/3.0)/8.0)
        #x1,x2=x1+(width/3),x2+(width/3)
        ax4.text(x1, height-1, 'Quality Checks', style='normal',fontsize=14,horizontalalignment='left')
        extra_lines=0
        for i in range(0,len(check_vars)):
            y=len(all_conds)-i-extra_lines
            if eval(check_vars[i][1])==True: textColor = 'green'
            else: textColor='red'

            ax4.text(x1, y, str(check_vars[i][0]), style='normal',color=textColor,fontsize=11.5,horizontalalignment='left')
            ax4.text(x2, y, ' = ', style='normal',color=textColor,fontsize=11.5,horizontalalignment='right')
            ax4.text(x2, y, eval(check_vars[i][1]), style='normal',color=textColor,fontsize=11.5,horizontalalignment='left')
            if eval(check_vars[i][1])==False:
                extra_lines+=1
                y=len(all_conds)-i-extra_lines
                showText = str(eval(check_vars[i][1]+'_A')) + '  does not equal  ' + str(eval(check_vars[i][1]+'_B'))
                ax4.text(x3, y, showText, style='italic',color='grey',fontsize=10,horizontalalignment='left')

        ax4.text(x2, 1, 'Plotted '+datetime.now().strftime('%m/%d/%Y  %H:%M:%S'), style='normal',color='black',fontsize=10,horizontalalignment='right')
        # # TODO: add display option to see total demand of travel distance vs. total planned distance

        ax4.plot()#[2], [1], 'o')
        ax4.axis([0, width, 0, height])
        ax4.xaxis.set_visible(False)
        ax4.yaxis.set_visible(False)

    plot1()
    plot2()
    plot3()
    plot4()
    plot5()
    plt.subplots_adjust(hspace=0.1)
    plt.tight_layout()

    plt.show()

    # DISPLAY_SIMULATION_DATA()
