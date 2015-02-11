# f(x)s for f(x)s
def get_travel_time(p1,p2):
    travel_speed=Assumption('travel_speed')
    if type(p1)!= list and type(p1)!= tuple:
        try:
            p1=eval(p1)
        except:
            print type(p1)
            p1=eval(p1)
    if type(p2)!= list and type(p2)!= tuple: p2=eval(p2)
    x=abs(p1[0]-p2[0])
    y=abs(p1[1]-p2[1])
    return int(round(travel_speed*(x+y),0))

def pd_get_travel_time(*items):
    p1a,p1b,p2a,p2b = items
    travel_speed=Assumption('travel_speed')
    x=abs(p1a-p2a)
    y=abs(p1b-p2b)
    return int(round(travel_speed*(x+y),0))
def pd_combine(*items):
    return str([x for x in items])
def pd_min_of_list(*items):
    return min([x for x in items])
def pd_index_of_list(ind,*it):
    return [ind if it[1]==it[2] else it[0] for x in it]

def pd_index_in_list(it,*items):
    return str([x for x in items].index(it))
def pd_append_list(items):
    p=eval(str(items))[0]
    for it in eval(str(items))[1:]:
        if (type(p)==list or type(p)==tuple):
            p.append(it)
        else: p+=it
    return p
def pd_list_to_combo_index(colInds,compList):
    return str(dict(zip([it[0] for it in colInds],compList)).values())
def pd_set_to_orderedSet_index(keys,vals,compList):
    d=dict(zip(keys,vals))
    return [d[it] for it in compList]
    #return str(dict(zip([it[0] for it in colInds],compList)).values())

def create_combo_sortKey(startPos):
    c = zip(startPos, range(0, len(startPos)))
    c.sort()
    d = [x[1] for x in c]
    f = range(0, len(d))
    c = zip(d, f)
    c.sort()
    return [x[1] for x in c]
def pd_create_sortKey(combo): # [1,0,2,4,6] to [1,0,2,3,4]
    d2=dict(zip([i for i in range(0,len(combo))],combo))
    d3={v:k for k,v in d2.iteritems()}
    x=sorted(d2.values())
    return [d3[it] for it in x]

def apply_sortKey(sortKey,compList):
    return [x[1] for x in sorted(zip(sortKey, compList))]
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
    tripStartIndex=tripIndex[0]
    tripEndIndex=tripIndex[1]
    #tripEndIndex=eval(tripIndex.replace(':',','))[1]
    return sum(eval(tripTimes+'[:'+str(tripStartIndex)+']')),sum(eval(tripTimes+'[:'+str(tripEndIndex)+']'))
def pd_get_diff_StEn(item):
    start,end = item
    return end-start
def pd_proximity(newLoc,s):
    ave_X,ave_Y = s
    n_x,n_y = newLoc
    return sqrt((ave_X-n_x)**2+(ave_Y-n_y)**2)
def pd_mock_to_num_dict(fromDict,listVar): return fromDict[listVar]

def get_multi_travel_times(itinerary):
    travel_speed=Assumption('travel_speed')
    t=0
    for i in range(1,len(itinerary)): t+=get_travel_time(itinerary[i-1],itinerary[i])
    return t