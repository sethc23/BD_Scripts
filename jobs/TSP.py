'''
Created on Dec 5, 2013

@author: sethchase
'''


def pd_combine_to_tuples(*items):
    return str([items[0],items[1]])

      
def Assumption(get_var):
    avenues_of_vendors,streets_of_vendors=4,20
    vend_location_grid=avenues_of_vendors*5,streets_of_vendors
    vend_num = 500
    vend_deliveries = 30
    vend_hours_delivering = 6
    vend_deliver_avenues,vend_deliver_streets=3,15
    vend_deliver_radius = vend_deliver_streets/2.0
    vend_delivery_grid = vend_deliver_avenues*5,vend_deliver_streets
    time_to_first_pickup = 10
    DG_start_location_grid=vend_location_grid
    DG_start_num = vend_num
    travel_speed = 1.0 # time to walk one street
    wait_at_vendor=5
    max_delivery_time=40
    max_delivery_per_person=4
    
    # OTHER ASSUMPTIONS APPLIED IN MODELING -- 
    # (1) vendors will make optimum delivery route based on overall shortest time
    #       (regardless if first order included in route is delivered last)
    #     In other words, vendor will maximize (endTime-startTime),
    #        as opposed to maximizing (endTime-orderTime).
    
    if get_var == 'vend_location_grid': return vend_location_grid
    if get_var == 'vend_num': return vend_num
    if get_var == 'vend_deliveries': return vend_deliveries
    if get_var == 'vend_hours_delivering': return vend_hours_delivering
    if get_var == 'vend_deliver_radius': return vend_deliver_radius
    if get_var == 'vend_delivery_grid': return vend_delivery_grid
    if get_var == 'DG_start_num': return DG_start_num
    if get_var == 'DG_start_location_grid': return DG_start_location_grid
    if get_var == 'time_to_first_pickup': return time_to_first_pickup
    if get_var == 'travel_speed': return travel_speed
    if get_var == 'wait_at_vendor': return wait_at_vendor
    if get_var == 'max_delivery_time': return max_delivery_time
    if get_var == 'max_delivery_per_person': return max_delivery_per_person

def pd_get_travel_time(p1a,p1b,p2a,p2b):
    travel_speed=Assumption('travel_speed')
    x=abs(p1a-p2a)
    y=abs(p1b-p2b)
    return int(round(travel_speed*(x+y),0))

def pd_combine(*items):#p1a,p1b,p2a,p2b):
    return str([x for x in items])

def pd_split_tuple(item):
    return item[0],item[1]

def pd_get_combo_index(it,combo):
    c=str(combo).replace('1','')
    c=c.replace('2','')
    c=eval(c)
    i1=c.index(it)
    i2=c.index(it,i1+1)
    return "["+str(i1)+':'+str(i2)+']'

def pd_get_trip_times(item):
    tripTimes,tripIndex = item
    return sum(eval(tripTimes+tripIndex))

def pd_get_trip_times2(item):
    tripTimes,tripIndex = item
    tripStartIndex=eval(tripIndex.replace(':',','))[0]
    tripEndIndex=eval(tripIndex.replace(':',','))[1]
    return sum(eval(tripTimes+'[:'+str(tripStartIndex)+']')),sum(eval(tripTimes+'[:'+str(tripEndIndex)+']'))

def pd_get_max_end_times(*items):
    return max(eval(items))

def pd_get_diff_StEn(item):
    start,end = item
    return end-start

# def pd_get_trip_end(*items):
#     a=[x for x in items]
#     return np.mean(a)

# def pd_get_trip_info2(*items):
#     a=[x for x in items]
#     print a
#     print type(np.mean(a))
#     print type(np.std(a))
#     return np.mean(a),np.std(a)

def pd_get_start_times(item):
    tripTimes,tripIndex = item
    tripStartIndex=eval(tripIndex.replace(':',','))[0]
    return sum(eval(tripTimes+'[:'+str(tripStartIndex)+']'))

def pd_get_end_times(item):
    tripTimes,tripIndex = item
    tripEndIndex=eval(tripIndex.replace(':',','))[1]
    return sum(eval(tripTimes+'[:'+str(tripEndIndex)+']'))



def bestExpeditedDeliveryRoute():
    a=[]
    from sys import path
    path.append('/Users/admin/SERVER2/BD_Scripts/utility')
    from permutations import genperm, genOrderedPairPerm,genAllPairPerm_NoRep
    import pandas as pd
    import numpy as np
    from time import time
    
    DictPair4=genAllPairPerm_NoRep(4,2)
    OrderPair4=genOrderedPairPerm(4)
     
    openPath='/Users/admin/Desktop/seamless/test_locations.txt'
    df=pd.read_csv(openPath, sep='\t', header=0)
    
    DG_contracts = df.groupby(by='id')
    groupList=[key for key,value in DG_contracts.groups.iteritems()] # this is the list of DG_IDs
    for j in range(0,len(DG_contracts.size().tolist())): # this weird thing is the number of DG groups
        t1=time()
        dg_group_i=DG_contracts.get_group(groupList[j])
        dg_group_i=dg_group_i.reset_index(drop=True)
        
    #     DG_working=DG_working.sort_index(by=['id','deliveryNum'], ascending=[True,True])
    #     df['start']=zip(df.sx,df.sy)#'sy']].apply(lambda s: tuple(s),axis=1)#lambda s: pd_combine_to_tuples(*s), axis=1)
    #     df['end']=zip(df.ex,df.ey)
    #     #df['from']=df[['sx','sy']].apply(lambda s: pd_combine_to_tuples(*s), axis=1)
    #     #df['to']=df[['ex','ey']].apply(lambda s: pd_combine_to_tuples(*s), axis=1)
    #     df['combined']=zip(df.start,df.end)
    #     #df['combined']=df[['from','to']].apply(lambda s: pd_combine_to_tuples(*s), axis=1)
    #      
    #     print df.head()
        
    
    
        start_loc=(20,-4)
        delivery_count=4
        location_count=(delivery_count*2)+1
        ABC='ABCDEFGHIJKLMNOPQRUSTUVXYZ'
        delivery_cols=list(''.join(ABC[:delivery_count]).upper())
        
        # ------------------
        # mock_pairs provides every combination between two locations (e.g., A1-B1, A1-C1, etc...)
        #     the point is to calculate the distances between every two points, and then add them up for each permutation (i.e., mock_travel_combo).
        #     This saves a lot of redundant processing.
        # mock_pairs_loc actually holds the coordinates
        # ------------------
    
        #mock_pairs=genAllPairPerm_NoRep(delivery_count,2)
        mock_pairs = eval('DictPair'+str(delivery_count))
        # need to incorporate starting position in mock_pairs dictionary
        a=[it for it in mock_pairs if it[0]=='A1']
        a=eval(str(a).replace('A1','A0'))
        a.insert(0,['A0','A1'])
        a.extend(mock_pairs)
        mock_pairs=a
        
        # ------------------
        #
        # Because combinations can cover several files, entire process will iterate between files of 100000 combinations
        # when necessary.  Whether there is one file (i.e., one iteration) or several, all files will be treated as the same.
        #
        # ------------------
        
        #combo_generator=genOrderedPairPerm(delivery_count,generator=True,printThis=False)
    
        mock_pairs_locs=str(mock_pairs)
        # convert all combos having placeholder variables to real locations
        # first, adjustment to convert A0 to the starting point
        x1,y1=start_loc[0],start_loc[1]
        new_var=str(x1)+', '+str(y1)
        mock_pairs_locs=mock_pairs_locs.replace("'A0'",new_var)
             
        mock_travel_combos = eval('OrderPair'+str(delivery_count))
        mock_travel_combos = str(mock_travel_combos)
        # need to incorporate starting position in mock_travel_combos    
        t=mock_travel_combos[1:]
        mock_travel_combos='['+t.replace('[',"['A0', ")
        mock_travel_combos_locs=str(mock_travel_combos)
        # as seen above with mock_pairs_loc
        mock_travel_combos_locs=mock_travel_combos_locs.replace("'A0'",new_var)
        pt=0
        for i in range(0,delivery_count):
            ind=ABC[pt]
            pt+=1
            x1,y1=dg_group_i.ix[i,'start_X'],dg_group_i.ix[i,'start_Y']
            x2,y2=dg_group_i.ix[i,'end_X'],dg_group_i.ix[i,'end_Y']
    
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
        pairs['travelTime']=pairs.apply(lambda s: pd_get_travel_time(*s),axis=1)
    
        pairs['combined']=pairs[column_names].apply(lambda s: pd_combine(*s),axis=1)
        printString+='pairs - shape'+str(pairs.shape)+'\n\r'
        printString+=str(pairs.head())+'\n\r'
        mapper=dict(zip(pairs.combined,pairs.travelTime))
        
        combos=pd.DataFrame(mock_travel_combos_locs,dtype = 'int32')
        combos['Mock Combos']=pd.DataFrame(mock_travel_combos).apply(lambda s: pd_combine(*s),axis=1)
        combos['travelTime']=np.zeros((len(combos.index),))
        
        trip_names=list(ABC[:location_count-1].lower())    
        for i in range(0,location_count-1): 
            testCols=combos[combos.columns[i*2:i*2+4]]
            testCols['combined']=testCols.apply(lambda s: pd_combine(*s),axis=1)
            testCols['travelTimes']= [ mapper[x] for x in testCols['combined'] ]
            combos['travelTime']+=testCols['travelTimes']
            combos[trip_names[i]]=testCols['travelTimes']
    
        combos['combined']=combos[trip_names].apply(lambda s: pd_combine(*s),axis=1)        
        delivery_cols=list(''.join(ABC[:delivery_count]).upper())
        for it in delivery_cols:
            combos['i-'+it]=combos['Mock Combos'].apply(lambda s: pd_get_combo_index(it,s))
            combos[it+'-St'],combos[it+'-En']=zip(*combos[['combined','i-'+it]].apply(pd_get_trip_times2,axis=1).map(pd_split_tuple))
            combos[it+'-T'] = combos[[it+'-St',it+'-En']].apply(pd_get_diff_StEn,axis=1)
        
        TravelTimesCols=[it+'-T' for it in delivery_cols]
        combos['travelTimes'] = combos[TravelTimesCols].apply(lambda s: pd_combine(*s),axis=1)
        combos['maxTime']=combos['travelTimes'].apply(lambda s: max(eval(s))) 
        max_delivery_time=40
        combos=combos[ combos['maxTime'] < max_delivery_time]
        combos=combos.sort_index(by=['travelTime'], ascending=[True])
        combos=combos.reset_index(drop=True)
        t2=time()
        print t2-t1,combos.ix[0,'Mock Combos'],combos.ix[0,'travelTime'],
#         print combos.iloc[:,:10].head()
#         print combos.iloc[:,10:20].head()
#         print combos.iloc[:,20:30].head()
#         print combos.iloc[:,30:].head()
#         print sdfds
        a.append(t2-t1)
    return a


def networkx():
    a=[]
    import pandas as pd
    from time import time
    
    from sys import path
    path.append('/Users/admin/SERVER2/BD_Scripts/utility')
    from permutations import genAllPairPerm_NoRep
    
    import networkx as nx
    
    openPath='/Users/admin/Desktop/seamless/test_locations.txt'
    df=pd.read_csv(openPath, sep='\t', header=0)
     
    DictPair4=genAllPairPerm_NoRep(4,2)
     
    DG_contracts = df.groupby(by='id')
    groupList=[key for key,value in DG_contracts.groups.iteritems()] # this is the list of DG_IDs
    a=[]
    for j in range(0,len(DG_contracts.size().tolist())): # this weird thing is the number of DG groups
        t1=time()
        G=nx.Graph()
        
        dg_group_i=DG_contracts.get_group(groupList[j])
        dg_group_i=dg_group_i.reset_index(drop=True)
      
        start_loc=(20,-4)
        delivery_count=4
        location_count=(delivery_count*2)+1
        ABC='ABCDEFGHIJKLMNOPQRUSTUVXYZ'
        delivery_cols=list(''.join(ABC[:delivery_count]).upper())
      
       
        mock_pairs=genAllPairPerm_NoRep(delivery_count,2)
        mock_pairs = eval('DictPair'+str(delivery_count))
      
        a=[it for it in mock_pairs if it[0]=='A1']
        a=eval(str(a).replace('A1','A0'))
        a.insert(0,['A0','A1'])
        a.extend(mock_pairs)
        mock_pairs=a
       
        mock_pairs_locs=str(mock_pairs)
      
        x1,y1=start_loc[0],start_loc[1]
        new_var=str(x1)+', '+str(y1)
        mock_pairs_locs=mock_pairs_locs.replace("'A0'",new_var)
        
    
        pos={}
        pos['A0']=(11,4)
        pt=0
        for i in range(0,delivery_count):
            ind=ABC[pt]
            pt+=1
            x1,y1=dg_group_i.ix[i,'start_X'],dg_group_i.ix[i,'start_Y']
            pos[ind+'1']=(x1,y1)
            x2,y2=dg_group_i.ix[i,'end_X'],dg_group_i.ix[i,'end_Y']
            pos[ind+'2']=(x2,y2)
            new_var=str(x1)+', '+str(y1)
            mock_pairs_locs=mock_pairs_locs.replace("'"+ind+"1'",new_var)
            new_var=str(x2)+', '+str(y2)
            mock_pairs_locs=mock_pairs_locs.replace("'"+ind+"2'",new_var)
       
        mock_pairs_locs=eval(mock_pairs_locs)       
        column_names=['p1x','p1y','p2x','p2y']
        pairs=pd.DataFrame(mock_pairs_locs,columns=column_names,dtype = 'int32')
        pairs['travelTime']=pairs.apply(lambda s: pd_get_travel_time(*s),axis=1)
        t_times=pairs['travelTime'].tolist()
        
        for i in range(0,len(mock_pairs)):
            G.add_edge(mock_pairs[i][0],mock_pairs[i][1])
            G[mock_pairs[i][0]][mock_pairs[i][1]]['weight']=t_times[i]
        
    #     z=zip([it[0] for it in mock_pairs],[it[1] for it in mock_pairs],t_times)
    #     print z
        
        #f=open('/Users/admin/Desktop/seamless/edgeList.txt','w')
        #for i in range(0,len(t_times)):
        #    f.writelines(str(mock_pairs[i][0])+' '+str(mock_pairs[i][1])+" {'weight': "+str(t_times[i])+'}'+'\n')
            #print str(mock_pairs[i][0])+' '+str(mock_pairs[i][1])+" {'weight': "+str(t_times[i])+'}'+'\n'
        #f.close()
    #     G=nx.read_edgelist('/Users/admin/Desktop/seamless/edgeList.txt')
        
    
        
    #     pos={}
    #     
    #     pos['A1']=(20,0)
    #     G.add_edge('A1','A2')
      
    #     pos['A2']=(17,-6)
        nx.draw_networkx(G,pos,node_size=200,node_color='blue')
    
        import matplotlib.pyplot as plt
        #nx.draw(G)
        plt.show()
        
    #     path=nx.single_source_dijkstra_path(G, 'A0')
    #     print path,'\r\n'
    #     path=nx.all_pairs_dijkstra_path(G)#.single_source_dijkstra_path(G, 'A0')
    #     print path,'\r\n'
        path=nx.shortest_path(G, 'A0')
        print path,'\r\n'    
        path=nx.single_source_dijkstra(G, 'A0','B2')#et, cutoff, weight).floyd_warshall(G)
        print path,'\r\n'  
         
    
        
        raise SystemExit
 
def length(p1,p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    try:
        return sqrt((p1[0]-p2[0])^2 + (p1[1]-p2[1])^2)
    except:
        return sqrt((eval(p1[0])-eval(p2[0]))^2 + (eval(p1[1])-eval(p2[1]))^2)

def check(checkList,setOne,setTwo):
    print checkList
    a=''
    for it in setTwo:
        if str(checkList).find(str(it)) != -1:
            try:
                if (checkList.count(it) != checkList.count(setOne[setTwo.index(it)]) and 
                    checkList.count(it) != 0):
                    return False
            except:
                pass
            try:
                if checkList.index(setOne[setTwo.index(it)]) > checkList.index(it):
                    return False
            except:
                pass
    return True
    
def solve_tsp_dynamic(points,labels): # assuming A0 is first, A1 is second, A2 is third, etc...
    from itertools import combinations
    # calc all lengths
    all_distances = [[length(x,y) for y in points] for x in points]
    setOne,setTwo=[2*n+1 for n in range(0,len(points)/2)],[2*(n+1) for n in range(0,len(points)/2)]
    # initial value - just distance from 0 to every other point + keep the track of edges
    A = {(frozenset([0, idx+1]), idx+1): (dist, [0,idx+1]) for idx,dist in enumerate(all_distances[0][1:])}
    E = A
    cnt = len(points)
    for m in range(2, cnt):
        print 'm',m
        B = {}
        D = {}
        for S in [ frozenset(C) | {0}  for C in combinations(range(1, cnt), m)]:
            print 'S',S
            for j in S - {0}:
                print 'j',j
                b_sets=[]
                #B[(S, j)] = min([(A[(S-{j},k)][0] + all_distances[k][j], A[(S-{j},k)][1] + [j]) for k in S if k != 0 and k!=j])
                for k in S: 
                    print 'k',k
                    if k != 0 and k!=j:
                        try:
                            b_sets.append((A[(S-{j},k)][0] + all_distances[k][j], A[(S-{j},k)][1] + [j]))# for k in S if k != 0 and k!=j and check(A[(S-{j},k)][1] + [j],setOne,setTwo)==True] )  #this will use 0th index of tuple for ordering, the same as if key=itemgetter(0) used
                        except:
                            print 'wait'
                        try:
                            if check(A[(S-{j},k)][1] + [j],setOne,setTwo)==True and j!=0:
                                D[(S, j)] = (E[(S-{j},k)][0] + all_distances[k][j], E[(S-{j},k)][1] + [j])
                                print 'new set',A[(S-{j},k)][1] + [j]
                            else:
                                print 'avoided',A[(S-{j},k)][1] + [j]
                        except:
                            pass
                B[(S, j)] = min(b_sets)
        A = B
        E = D
    res = min([(A[d][0] + all_distances[0][d[1]], A[d][1]) for d in iter(A)])
    return res[1]

def pd_point_in_area(T,start_pt,items):
    S_x,S_y = start_pt
    To_x,To_y = items
    return (To_x - S_x)**2 + (To_y - S_y)**2 <= (40-T)**2
  
def checkGroup(T0,pt1,pt2,all,pairs):
    #at T, is "to" location within radii for all remaining stops?
    T=T0-get_travel_time(all[all.mock_name == pt1].reset_index().ix[0,'loc'],all[all.mock_name == pt2].reset_index().ix[0,'loc'])
    start_pt=all[all.mock_name == 'A0'].reset_index().ix[0,'loc']
    all['in_area']=all['loc'].apply(lambda s: pd_point_in_area(T,start_pt,s))
    #pairs['remaining_pts']=
    if len( all[ all.in_area == True ].index ) != 0: return True
    else: return False

def get_travel_time(p1,p2):
    travel_speed=Assumption('travel_speed')
    try:
        if type(p1)!= list and type(p1)!= tuple: p1=eval(p1)
        if type(p2)!= list and type(p2)!= tuple: p2=eval(p2)
    except:
        pass
    x=abs(p1[0]-p2[0])
    y=abs(p1[1]-p2[1])
    return int(round(travel_speed*(x+y),0))    
        
def Assumption(get_var):
    avenues_of_vendors,streets_of_vendors=4,20
    vend_location_grid=avenues_of_vendors*5,streets_of_vendors
    vend_num = 60
    vend_deliveries = 30
    vend_hours_delivering = 6
    vend_deliver_avenues,vend_deliver_streets=3,15
    vend_deliver_radius = vend_deliver_streets/2.0
    vend_delivery_grid = vend_deliver_avenues*5,vend_deliver_streets
    time_to_first_pickup = 10
    DG_start_location_grid=vend_location_grid
    DG_start_num = vend_num
    travel_speed = 1.0 # time to walk one street
    wait_at_vendor=5
    max_delivery_time=40
    max_delivery_per_person=4
    
    # OTHER ASSUMPTIONS APPLIED IN MODELING -- 
    # (1) vendors will make optimum delivery route based on overall shortest time
    #       (regardless if first order included in route is delivered last)
    #     In other words, vendor will maximize (endTime-startTime),
    #        as opposed to maximizing (endTime-orderTime).
    
    if get_var == 'vend_location_grid': return vend_location_grid
    if get_var == 'vend_num': return vend_num
    if get_var == 'vend_deliveries': return vend_deliveries
    if get_var == 'vend_hours_delivering': return vend_hours_delivering
    if get_var == 'vend_deliver_radius': return vend_deliver_radius
    if get_var == 'vend_delivery_grid': return vend_delivery_grid
    if get_var == 'DG_start_num': return DG_start_num
    if get_var == 'DG_start_location_grid': return DG_start_location_grid
    if get_var == 'time_to_first_pickup': return time_to_first_pickup
    if get_var == 'travel_speed': return travel_speed
    if get_var == 'wait_at_vendor': return wait_at_vendor
    if get_var == 'max_delivery_time': return max_delivery_time
    if get_var == 'max_delivery_per_person': return max_delivery_per_person

def TSP_by_area(t0,all,pairs):
    start_pts = {val: i for i,val in enumerate([ it for it in all_locs['mock_name'] if it.find('1')!=-1 ])}.keys()
    end_pts = {val: i for i,val in enumerate([ it for it in all_locs['mock_name'] if it.find('2')!=-1 ])}.keys()
    A0=all[all.mock_name == 'A0'].ix[0,'loc']
    S0=A0
    T=40-t0
    B=[S0]
    pt1='A0'
    b=['A0']
    remaining_pts = [ it for it in all['mock_name'] if b.count(it)==0 ]   
    avail_pts =  [ it for it in remaining_pts if (start_pts.count(it)!=0 or (end_pts.count(it)!=0 and b.count(it[0]+'1')!=0)) ]
    start,end=True,False
    while end==False:
        if start==True:
            start=False
            a = [ ( pi*get_travel_time(S0,all[all.mock_name == it].reset_index().ix[0,'loc'])**2 )  
                 for it in avail_pts if checkGroup(T,pt1,it,all,pairs) == True ]
            if len(a) == 0: 
                return None
            else: 
                B.append(all[all.mock_name == avail_pts[a.index(min(a))]].reset_index().ix[0,'loc'])
                b.append(avail_pts[a.index(min(a))])
        else:
            # S0 equals location used to determine min(a)
            S0= all[all.mock_name == b[len(b)-1]].reset_index().ix[0,'loc']
            T = T - get_travel_time(all[all.mock_name == pt1].reset_index().ix[0,'loc'],S0)
            pt1=b[len(b)-1]
            avail_pts =  [ it for it in all['mock_name'] if (b.count(it)==0 and (start_pts.count(it)!=0 or (end_pts.count(it)!=0 and b.count(it[0]+'1')!=0))) ]
            C = all[ all.mock_name == b[len(b)-1] ]
            a = [ ( pi*get_travel_time(S0,all[all.mock_name == it].reset_index().ix[0,'loc'])**2 )
                 for it in avail_pts if checkGroup(T,pt1,it,all,pairs) == True ]
            if len(a) == 0: 
                return None
            else: 
                B.append(all[all.mock_name == avail_pts[a.index(min(a))]].reset_index().ix[0,'loc'])
                b.append(avail_pts[a.index(min(a))])
            if len(B) == location_count: 
                return B,b

def graph_trip(trip,trip_loc,p_title):
    G=nx.Graph()
    pos={}
    pos[trip[0]]=(trip_loc[0][0],trip_loc[0][1])
    for i in range(1,len(trip)):
        G.add_edge(trip[i-1],trip[i])
        pos[trip[i]]=(trip_loc[i][0],trip_loc[i][1])
    nx.draw_networkx(G,pos,node_size=500,node_color='blue')
    import matplotlib.pyplot as plt
    plt.title(p_title)
    plt.grid(True)
    plt.show()


def compare_trips(trip1,trip_loc1,trip2,trip_loc2,p1_title,p2_title,show=False,save=True,baseDir='/Users/admin/Desktop/seamless/graphs/'):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(14, 8))
    
    plt.subplot(1, 2, 1)
    G=nx.Graph()
    pos1={}
    pos1[trip1[0]]=(trip_loc1[0][0],trip_loc1[0][1])
    for i in range(1,len(trip1)):
        G.add_edge(trip1[i-1],trip1[i])
        pos1[trip1[i]]=(trip_loc1[i][0],trip_loc1[i][1])
    nx.draw_networkx(G,pos1,node_size=500,node_color='blue')
    plt.title(p1_title)
    plt.grid(True)

    plt.subplot(1, 2, 2)
    F=nx.Graph()
    pos2={}
    pos2[trip2[0]]=(trip_loc2[0][0],trip_loc2[0][1])
    for i in range(1,len(trip2)):
        F.add_edge(trip2[i-1],trip2[i])
        pos2[trip2[i]]=(trip_loc2[i][0],trip_loc2[i][1])
    nx.draw_networkx(F,pos2,node_size=500,node_color='blue')
    plt.title(p2_title)
    plt.grid(True)
    if show == True: plt.show()
    if save == True: plt.savefig(baseDir+p1_title[:p1_title.find('\t')]+'.png')
    
   

test=True
#testTime=bestExpeditedDeliveryRoute()
#testTime=networkx()


a=[]
import pandas as pd
from time import time
from math import sqrt
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/utility')
from permutations import genAllPairPerm_NoRep
from math import pi
import networkx as nx

openPath='/Users/admin/Desktop/seamless/test_locations.txt'
df=pd.read_csv(openPath, sep='\t', header=0)
 
DictPair4=genAllPairPerm_NoRep(4,2)
 
DG_contracts = df.groupby(by='id')
groupList=[key for key,value in DG_contracts.groups.iteritems()] # this is the list of DG_IDs
a=[]
cmp_trips = [['A0', 'C1', 'A1', 'C2', 'A2', 'B1', 'D1', 'D2', 'B2'],
             ['A0', 'A1', 'A2', 'C1', 'D1', 'C2', 'B1', 'D2', 'B2'],
             ['A0', 'C1', 'A1', 'B1', 'D1', 'D2', 'C2', 'B2', 'A2'],
             ['A0', 'C1', 'B1', 'D1', 'B2', 'A1', 'D2', 'C2', 'A2'],
             ['A0', 'B1', 'A1', 'C1', 'D1', 'C2', 'B2', 'A2', 'D2'],
             ['A0', 'A1', 'B1', 'A2', 'B2', 'C1', 'D1', 'C2', 'D2'],
             ['A0', 'A1', 'A2', 'B1', 'B2', 'D1', 'C1', 'C2', 'D2'],
             ['A0', 'B1', 'C1', 'C2', 'B2', 'A1', 'D1', 'A2', 'D2'],
             ['A0', 'C1', 'C2', 'B1', 'B2', 'A1', 'D1', 'A2', 'D2']]
cmp_times = [57,47,49,65,46,78,68,75,94]

for j in range(0,len(DG_contracts.size().tolist())): # this weird thing is the number of DG groups
    

    
    dg_group_i=DG_contracts.get_group(groupList[j])
    dg_group_i=dg_group_i.reset_index(drop=True)
  
    start_loc=(20,-4)
    delivery_count=4
    location_count=(delivery_count*2)+1
    ABC='ABCDEFGHIJKLMNOPQRUSTUVXYZ'
    delivery_cols=list(''.join(ABC[:delivery_count]).upper())
  
   
    mock_pairs=genAllPairPerm_NoRep(delivery_count,2)
    mock_pairs = eval('DictPair'+str(delivery_count))
  
    a=[it for it in mock_pairs if it[0]=='A1']
    a=eval(str(a).replace('A1','A0'))
    a.insert(0,['A0','A1'])
    a.extend(mock_pairs)
    mock_pairs=a
   
    mock_pairs_locs=str(mock_pairs)
  
    x1,y1=start_loc[0],start_loc[1]
    new_var=str(x1)+', '+str(y1)
    mock_pairs_locs=mock_pairs_locs.replace("'A0'",new_var)

    a,b=[],[]
    a.append([11,4])
    b.append('A0')
    pt=0
    for i in range(0,delivery_count):
        ind=ABC[pt]
        pt+=1
        x1,y1=dg_group_i.ix[i,'start_X'],dg_group_i.ix[i,'start_Y']
        a.append([x1,y1])#pos[ind+'1']=(x1,y1)
        b.append(ind+'1')
        x2,y2=dg_group_i.ix[i,'end_X'],dg_group_i.ix[i,'end_Y']
        a.append([x2,y2])#pos[ind+'2']=(x2,y2)
        b.append(ind+'2')
        new_var=str(x1)+', '+str(y1)
        mock_pairs_locs=mock_pairs_locs.replace("'"+ind+"1'",new_var)
        new_var=str(x2)+', '+str(y2)
        mock_pairs_locs=mock_pairs_locs.replace("'"+ind+"2'",new_var)
   
    mock_pairs_locs=eval(mock_pairs_locs)       
    column_names=['p1x','p1y','p2x','p2y']
    pairs=pd.DataFrame(mock_pairs_locs,columns=column_names,dtype = 'int32')
    pairs['orderTimes']=pairs.apply(lambda s: 0,axis=1)
    pairs['travelTimes']=pairs[['p1x','p1y','p2x','p2y']].apply(lambda s: pd_get_travel_time(*s),axis=1)
    pairs['S']=pd.Series([it[0] for it in mock_pairs])
    pairs['E']=pd.Series([it[1] for it in mock_pairs])
    
    pairs[(pairs.S == 'A0') & (pairs.E.apply(lambda s: s.find('2') != -1))]
    all_locs = pd.DataFrame({'mock_name': b,'loc': a})                             
    
    
    t0=0
    t1=time()
    trip_loc1,trip1 = TSP_by_area(t0,all_locs,pairs)
    t2=time()
    #get_trip_time(trip,pairs)
    tripTime=[]
    for i in range(1,len(trip1)):
        tripTime.append(pairs[(pairs.S == trip1[i-1]) & (pairs.E == trip1[i])].reset_index().ix[0,'travelTimes'])
    print j,t2-t1,trip1,sum(tripTime)
    p1_title = 'plot '+str(j)+'\t'+': Time = '+str(sum(tripTime))+'\n'+str(trip1)
    trip2=cmp_trips[j]
    trip_loc2=[all_locs[all_locs.mock_name == it].reset_index().ix[0,'loc'] for it in trip2]
    p2_title = 'plot '+str(j)+'\t'+': Time = '+str(cmp_times[j])+'\n'+str(trip2)
    compare_trips(trip1,trip_loc1,trip2,trip_loc2,p1_title,p2_title,show=False,save=True)
    q=0
    #raise SystemExit


         
#         print t2-t1
#         for i in range(0,len(mock_pairs)):
#             G.add_edge(mock_pairs[i][0],mock_pairs[i][1])
#             G[mock_pairs[i][0]][mock_pairs[i][1]]['weight']=t_times[i]
#             
#     t1=time()
#     z=solve_tsp_dynamic(a,b)
#     t2=time()
#     print z
    
  

  
  
# df = [ID             timeLeft               S              E              P1x         P1y         P2x         P2y         travTime]
 
 

    
#     z=zip([it[0] for it in mock_pairs],[it[1] for it in mock_pairs],t_times)
#     print z
    
    #f=open('/Users/admin/Desktop/seamless/edgeList.txt','w')
    #for i in range(0,len(t_times)):
    #    f.writelines(str(mock_pairs[i][0])+' '+str(mock_pairs[i][1])+" {'weight': "+str(t_times[i])+'}'+'\n')
        #print str(mock_pairs[i][0])+' '+str(mock_pairs[i][1])+" {'weight': "+str(t_times[i])+'}'+'\n'
    #f.close()
#     G=nx.read_edgelist('/Users/admin/Desktop/seamless/edgeList.txt')
    


     
#     path=nx.single_source_dijkstra_path(G, 'A0')
#     print path,'\r\n'
#     path=nx.all_pairs_dijkstra_path(G)#.single_source_dijkstra_path(G, 'A0')
#     print path,'\r\n'
#     path=nx.shortest_path(G, 'A0')
#     print path,'\r\n'    
#     path=nx.floyd_warshall(G)#, weight).single_source_dijkstra(G, 'A0','B2')#et, cutoff, weight).floyd_warshall(G)
#     print path,'\r\n'  
     

    
    #















    