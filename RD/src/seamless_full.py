'''
Created on Nov 2, 2013

GENERAL MODELING STRATEGY/OUTLINE

    for each order,
        l=travel_time
        can any DG arrive by (40-l):
            if none available,
                add new DG to order_q
                send out on delivery
            for all DG who can arrive:
                pick best DG by ...
                    shortest order_time
                    **most even DG distribution
                    *most deliveries per person (= chaos method)
                    DG ranking

*   used in FIRST IMPLEMENTATION
**  used in SECOND IMPLEMENTATION

(based on company history, may be best to consider potential for new orders during travel to vendor.
 -- this can be based on probability of (order per minute) * (minutes to vendor)
    -->>--  the longer it takes to get to a location, the more likely there will be another order,
            and the more important it is to send DG with more available time)

(OR, rely on chaos theory and make decisions based on what information is available, not what is
predicted! --> in which case, pack as many deliveries per DG as possible) --> FIRST IMPLEMENTATION.


In the FIRST IMPLEMENTATION, orders were distributed in round robin fashion to DG capable of satisfying
condition and making delivery (provided it was determinable within the combination of 5 pickups/deliveries.
Simple robin distribution is inadequate as the distribution is made blindly without any considerations of whether
 another DG is better positioned to take order.

 - numerous ways could be used to make the first implemention better, but a second branch was started to
 explore a SECOND IMPLEMENTATION based on practical business reasons.

 - one such way to improve FIRST IMPLEMENTATION:
    -identify most inconvenient deliveries (and best combo without it, which can be calculated concurrently
    with c_best_combo method. a subprocess could re-distribute orders based on the outlier delivery center point
     and inlier center points of each DG route. this method could the "Bohr approach" after Neils Bohr

 - other strategies include:
    - least number of orders
    - weighted least number of orders
    - weighted round robin
    - most amount of time
    - centered around a (static or dynamic) point
    - work-stealing approach
    - ant colony optimization
    - swarm intelligence
    - clustering, generalized assignment problem
        make clusters limited by number of nodes


The SECOND IMPLEMENTATION attempts to prove/disprove a hypothesis.

PURPOSE:  In the most practical sense, this business will begin best if delivery guys
continue to work with restaurants with whom they have experience.  This means the delivery system
should start out with maximizing deliveries in particular areas, where a delivery guy covers a single
area and continues to serve the same restaurant.  Although the system may metamorphose into one based
on a level of chaos if more efficient, for now, the system should mirror practical business concerns.
In doing so, it is necessary to predict the minimum coverage required to satisfy delivery conditions
with a certain margin of safety.  Once a formula is identified for predicting the necessary coverage,
a two week period of monitoring a restaurant is assumed to be enough time to calibrate the initial
system.  Adding new restaurants to an active system will be based on the same premise (though the
transition time will likely be shorter).  Therefore, this calibration system should scale well with
the business.

HYPOTHESIS: Assuming a lattice of circles bound by the delivery radii of all restaurants, where the
circles' center points are:

X             Y
0              0,2,4,...2n
1              1,3,5,...2n+1
2              0,2,4,...2n
.
.
n


and where the areas of the circles are pi*((40-r)**2)*C*D
---> C will be a constant approximately proportional to the number of deliveries per hour.
---> D will be a constant approximately proportional to the density of restaurants.

OBJECTIVES:
- determine the maximum radii (95% confidence) for randomized pickup/drop-off locations
    and constant # of deliveries per hour for a constant density of restaurants where all
    deliveries satisfy all conditions.
- determine C by applying the above process to a range of deliveries per hour.
- determine D by applying the two above processes to a range of restaurant densities.

VERIFICATION:
- use density variable to predict deliveries per hour.
- use deliveries per hour to predict restaurant density.
- randomize deliveries per hour and restaurant densities, predict results, and verify accuracy of constants.

METHOD:
    1. Identify [x,y] ranges for vendors and expand based on delivery radii --> Xmax,Ymax,Xmin,Ymin
    2. Use monte carlo method to determine radii (as later identified)
      -starting points: max radii == pi*(40**2), min radii == 0
    3. (number of circles) n == (along X) : (Xmax-Xmin)/r,  (along Y) : (Ymax-Ymin)/r
    4. (center points) C == (along X) : 2*n,  (along Y) : 2*(n+1)
    5. All DG[i] start at C[i] and move back to C[i] during downtime.
    6. Start simulation. When an order comes in, check if primary DG for that area can deliver order.
      -this check includes taking last 5 pts of [current route + new delivery] and checking for availability.
      -(the above and other small steps could have significant impacts)
    7. If primary DG unavailable, apply same process for secondary DG, and the tertiary DGs.
    8. If still not available, save as undelivered and move on.
    9. If count of undelivered exceeds 7% of total deliveries -- end simulation.
    10. If end process, redefine radius as midway length between failed and successful radii
    ----
    Use above process to:
        a. find max radii within undeliverable limit
        b. find max radii with 0 undeliverables
        c. randomize vendor and delivery locations & run again until 95% confidence level

Possible Business Names:
-orcabee

@author: sethchase
'''


cython=True
# cython=False
# resume=True
resume=False
# save=True
save=False

makeData=False
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

# load=True
load=False
errorCheck=False
global_op_vars=False

way_t,vert_t,vert_g = 'lion_ways_slim','lion_ways_slim_vertices_pgr','the_geom'

""" UPDATES + NOTES
Done -- 1. problem with picking right del_ID.  it should be based on first occurences in dynamic_dg_q.deliv_id

Done -- 2. figure out to fully reverse effect of checking combos for partial trips

Done -- 3.  Why is id==32 starting at 11 with order_time=4 at T=5 ?
    Why does dg_q_group not have destination for 1351 ?

Done -- 4. add option to verify clean_order_results

5. re-work dg_pool to:
    -only have purposeful information in rows
    -keep totalDeliveries column
    -to be updated on each access point (newDG,re-pool,new order assignment)
    -use sorted dg_pool to provide order for bestCombo
    -should be up-to-date with all location information(or at least be accessible)

Done -- 6. change graph 3 to combine plots with mean of Orders aligned and scaled right

Done -- isolate/consolidate changes to global data vars to single function (for simplicity and debugging)

Done -- 7. re-do delivery count on remove order

Done -- 8. change function that creates dg_q data from order_q data to start at certain point in time.
            -This seemed required when presented with the case of a second order completing before a first order,
                which left a gap of time in the order_q_i and thus the pulled dg_q.

9. QUERY: Should pull dg_q order function always include row from dg_X/Y to first point?
    - this is posed in light of dg_X/Y always being up-to-date.

10. re-implement dictionary for time-to-position for each DG in dg_pool.

Done -- 11. changed getComboInfo to uniformly select static orders and dg_q

Done -- 12. checked all index sorting to confirm that ascending=True was intended to mean [0,4,4]

Done -- 13. created function to re-order dg_q points based on mock_pt so points are always paired, A1,A2,B1,B2, etc..

company name -- BC, BC Delivery, BCD,

why is there a marked feature that the number of active DG first begins to closely follow number of Active Deliveries
    at t=40?  40 is of course the number that also corresponds with the maximum delivery time.

but why is the mean number of orders per DG continuous decline at t<20 maybe t<10?

----

    driver of this system is the orders.
    ??  the total travel time/dist for all DG  x  speed == the number of used DG  x  total number of minutes

    if each DG is working for total_time, and DG travels at 1 point per minute, then each DG will travel total_time points.
    if all DG are working for total_time, then (number of DG * total_time) should equal total dist traveled by DG.
    --at the very least, the numbers should be the same for all results.

    re-pool should start small and build out as necessary in increments (e.g., 20). the increment size could be based on times of the day.

    group selection for checking availability should be based segmentations of most deliveries, i.e., five equal segments based on count of
    totalDG_pool but ordered most-to-least deliveries.


        (timing could also be changed to be at the moment DG needs to make the decision)

    group selection could be secondarily re-analyzed at decision times.

    i can say at any given point in time, an attractive force in one direction and magnitude is acting on an object.
    what is that direction and magnitude at time Z ?

        that direction will unlikely be a straight line.


    total_time * No. of DG

    1 pt per minute


    dg_pool needs to be the source of available DG
    (as opposed to those DG on the order_q being selected,
    which works early on but not later when smaller pool)

        -

"""
if cython==False: from order_by_min2 import c2_order_by_min as c_order_by_min
from time import time
# print time()
import pandas as pd
np = pd.np
from numpy.lib.scimath import sqrt
import pyximport,pp
import geopandas as gd
np.set_printoptions(linewidth=200,threshold=np.nan)
# pd.set_option('expand_frame_repr',False)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width',180)
pyximport.install(build_in_temp=False,inplace=True)
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True
from os import path,listdir,system,getcwd
from sys import path as py_path
this_cwd = getcwd()+'/'
# py_path.append(this_cwd+'/cython_exts')
if cython==True: from cython_exts.order_by_min import c_order_by_min
# from get_combo_start_info import c_get_combo_start_info
# from update_order_results import c_update_order_results
# from eval_single_order import c_eval_single_order
# from bestED import c_bestED
# from getBestDG import c_getBestDG
py_path.append(this_cwd+'../../geolocation')
from f_postgres import geom_inside_street_box,make_column_primary_serial_key
from sqlalchemy import create_engine
engine = create_engine(r'postgresql://postgres:postgres@192.168.2.50:8800/routing',
                       encoding='utf-8',
                       echo=False)

# engine = create_engine(r'postgresql://postgres:postgres@localhost/routing',
#                        encoding='utf-8',
#                        echo=False)

print '\nStart Time:\n',time()
def test_get_best_combo(start_X,
                        start_Y,
                        mockCombo,
                        realCombo,
                        orderSK,
                        pointSK,
                        order_times,
                        deliv_ids,
                        d,
                        tripStart, sp,
                        maxOrderTime,
                        maxTravelTime,
                        tT,                 # c_travel_times
                        sT,                 # c_start_times
                        eT,                 # c_end_times
                        odt,                # c_odtTimes
                        oMax,               # c_max_order-to-deliveryTime
                        tMax,               # c_MaxTravelToLocTime
                        tdd,                # c_tddTimes
                        ctm,                # c_ctMarker
                        return_orders):     # c_returnVars
    r = mockCombo.shape[0]                                    # number of rows
    pts = mockCombo.shape[1]                                  # number of pts
    BI = r+1                                                  # time in between each pt, best index.
    minT = 8*maxOrderTime                                     # minimum total route time (assuming 8 routes is max route #)

    for j in range(pts):
        for i in range(r):
            if j == 0:
                xptb=realCombo[i][j][0]
                yptb=realCombo[i][j][1]
                x=abs(start_X-xptb)
                y=abs(start_Y-yptb)
                t=sp*(x+y)
                ctm[i] = tripStart+t
                tT[i][j] = tripStart+t
                oMax[i] = 0
                tMax[i] = tripStart+t
            else:
                xpta=realCombo[i][j-1][0]
                ypta=realCombo[i][j-1][1]
                xptb=realCombo[i][j][0]
                yptb=realCombo[i][j][1]
                x=abs(xpta-xptb)
                y=abs(ypta-yptb)
                t=sp*(x+y)
                ctm[i] += t
                tT[i][j] = t
                if t > tMax[i]:
                    tMax[i] = t

            mc_pt=mockCombo[i][j]
            if mc_pt<100: sT[i][mc_pt]=ctm[i]
            else: eT[i][mc_pt-100]=ctm[i]

            if j == pts-1:                          # this is the last part of the 2D iteration
                for k in range(d):
                    orderSK_pt=orderSK[i][k]
                    eT_pt=eT[i][k]
                    tdd[i][k]=eT_pt-sT[i][k]
                    odt_pt=eT_pt-order_times[orderSK_pt]
                    odt[i][k]=odt_pt
                    if odt_pt>oMax[i]:
                        oMax[i]=odt_pt              # update max order-to-delivery time [ per row ] -- keeping biggest value

                if oMax[i]<=maxOrderTime:           # if order-to-delivery max is acceptable &
                    if tMax[i] <= maxTravelTime:    # max travelToLoc time is acceptable -->  save row as Best Index
                        if ctm[i]<minT:             # for all acceptable rows, keep one with lowest cumul. time.
                            minT=ctm[i]
                            BI=i

    if minT==8*maxOrderTime:
        return_orders[0][13]=0                      # interpretted on return as an error
        return_orders[1][13]=BI
        return return_orders
    elif BI == r+1:
        return_orders[0][13]=0                      # interpretted on return as an error
        return_orders[1][13]=505                    # interpretted on return as "error setting best index"
        return return_orders
    else:
        for e in range(d):
            orderSK_pt=orderSK[BI][e]
            return_orders[e][0] = start_X                # dg_X
            return_orders[e][1] = start_Y                # dg_Y
            return_orders[e][2] = orderSK_pt+1             # deliv_num (starts at zero)
            return_orders[e][3] = deliv_ids[orderSK_pt]          # deliv_id (already sorted by key)
            return_orders[e][4] = order_times[orderSK_pt]           # order_time
            mc_pt=pointSK[BI][e*2]
            return_orders[e][5] = tT[BI][mc_pt]        # travel_time_to_loc
            return_orders[e][6] = realCombo[BI][mc_pt][0]     # startX // see below for explanation
            return_orders[e][7] = realCombo[BI][mc_pt][1]     # startY
            return_orders[e][8] = sT[BI][e]            # start_time
            return_orders[e][9] = tdd[BI][e]           # travel_time
            return_orders[e][10]= eT[BI][e]            # end_time
            mc_pt=pointSK[BI][e*2+1]
            return_orders[e][11]= realCombo[BI][mc_pt][0]     # endX
            return_orders[e][12]= realCombo[BI][mc_pt][1]     # endY
            return_orders[e][13]= odt[BI][e]           # total_order_time
            return_orders[e][14]= BI
        return return_orders

    ## Assume [1,0] = orderSK, a.k.a. Order Sort Key.
    ##  the '1' being first means the second order, i.e., order B, is picked up first.
    ##  thus, orderSK[0] = 1.
    ##
    ## Assume [1,3,0,2] = pointSK, a.k.a. Point Sort Key, which corresponds to points [A1,A2,B1,B2].
    ##  the '1' at the beginning means the pickup of the first order, i.e., A1, occurs at index 1 in the route.
    ##  the '0' in the third position means that pickup of B1 occurs at index 0 in the route.
    ##
    ## In order to identify the X-axis location of a point on a particular order,
    ##  Start with the order key, which shows that the second order pickup precedes the first order pickup.
    ##      deliv_num = 1 and the second order is the subject of the first iteration of return_orders.
    ##  Now, orderSK[e]=1 can be used as an index in pointSK to identify the index of B1 in the permutated array of locations.
    ##      (The '*2' keeps the index consistent with an order pickup being every other point in [A1,A2,B1,B2,...n1,n2].)

from types import NoneType
import sys
reload(sys)
sys.setdefaultencoding('UTF8')

def listFin(F_in,delimiter=''):
    L_out = []
    if delimiter=='':
        fin = open(F_in, 'r')
        data = fin.readlines()
        fin.close()
        for row in data:
        #    #L_out.append(float(data[i]))
            try:
                L_out.append(eval(row))
            except:
                L_out.append(row)
        return L_out
    else:
        fin = open(F_in, 'r')
        data = fin.read()
        fin.close()
        data=data.split('\r')
        for row in data:
            nrow=row.split(delimiter)
            row_vars=[]
            for it in nrow:
                try:
                    row_vars.append(eval(it))
                except:
                    row_vars.append(it)
            L_out.append(row_vars)
        return L_out
def listFout(L_in, F_out):
    row = len(L_in)
    fileArray = []
    for line in range(0, row):
        fileArray.append(L_in[line])
    fmin = open(F_out, "w")
    for i in range(0, row):
        line = str(fileArray[i])
        fmin.writelines(line)
        fmin.writelines('\n')
    fmin.close()
def systemError():
    if alert_bell == True:
        cmd='say -v Bells "dong"'
        # system(cmd)

    print time(),'systemError()'
    raise SystemError
def genSeg(segSize,generator):
    num = 0
    while num < segSize:
        yield generator.next()
        num += 1
def genAllPairPerm_NoRep(pairCount,choose,generator=False,printThis=False):
    basePath='/Users/admin/Desktop/seamless/perm_data/AllPairPerm_NoRep-'
    filePath=basePath+str(pairCount)+'.txt'
    if path.isfile(filePath):
        return listFin(filePath)
    else:
        # formula = n! / (n-r)!
        if pairCount > 26:
            print "too many pairs"
            systemError()
        return gen_good_combos(pairCount,choose)
def getFilesFolders(workDir, full=False):
    x = listdir(workDir)
    try: a = x.pop(x.index('.DS_Store'))
    except: pass
    popList, y = [], []
    for i in range(0, len(x)):
        if path.isdir(x[i]):
            popList.append(i)
        else: y.append(workDir.rstrip('/')+'/'+x[i])
    popList.reverse()
    for it in popList: x.pop(it)
    if full == False: return x
    else:
        return y
def genOrderedPairPerm(pairCount,generator=False,printThis=False):
    basePath='/Users/admin/Desktop/seamless/perm_data/'
    filePath=basePath+'OrderedPairPerm-'+str(pairCount)+'-0.txt'
    if path.isfile(filePath):
        z=getFilesFolders(basePath)
        p=len(str(z).split('OrderedPairPerm-'+str(pairCount)))-1
        z=[]
        for i in range(0,p):
            filePath=basePath+'OrderedPairPerm-'+str(pairCount)+'-'+str(i)+'.txt'
            if generator == False:
                a=listFin(filePath)
                z.extend(a)
            else:
                z.append(filePath)
        if generator == False: return z
        if generator == True: return fileDataGenerator(z)
    else:
        if pairCount > 26:
            print "too many pairs"
            systemError()
        return gen_good_perms(pairCount,pairCount+1)
def fileDataGenerator(fileList):
    for i in range(0,len(fileList)):
        f=open(fileList[i],'r')
        x=f.read()
        f.close()
        yield eval('['+x.replace('\n',',')+']')
def all_perms(elements):
    if len(elements) <=1:
        yield elements
    else:
        for perm in all_perms(elements[1:]):
            for i in range(len(elements)):
                yield perm[:i] + elements[0:1] + perm[i:]
def all_pair_perms(elements,choose):
    from itertools import permutations
    return permutations(list(elements),2)
def good_perms(elements):
    z=[]
    for it in elements:
        z.append(it+'1')
        z.append(it+'2')
    for perm in all_perms(z):
        add=True
        for it in elements:
            q=''.join(perm).replace(it+'1','3').replace(it+'2','4').replace('1','').replace('2','')
            if [int(s) for s in list(q) if s.isdigit()] != sorted([int(s) for s in list(q) if s.isdigit()]):
                add=False
                break
        if add==True: yield perm
def good_combos(elements,choose):
    z=[]
    for it in elements:
        z.append(it+'1')
        z.append(it+'2')
    for perm in all_pair_perms(z,choose):
        add=True
        for it in elements:
            q=''.join(perm).replace(it+'1','3').replace(it+'2','4').replace('1','').replace('2','')
            if [int(s) for s in list(q) if s.isdigit()] != sorted([int(s) for s in list(q) if s.isdigit()]):
                add=False
                break
        if add==True: yield eval(str(perm).replace('(','[').replace(')',']'))
def gen_good_perms(L1,L2):
    t1= time()
    ABC='ABCDEFGHIJKLMNOPQRUSTUVXYZ'
    seg=10000
    for i in range(L1,L2):
        t1=time()
        b=list(ABC[:i])
        q=good_perms(b)
        b=genSeg(seg,q)
        p=list(b)
        pt=0
        basePath='/Users/admin/Desktop/seamless/perm_data/OrderedPairPerm-'+str(i)+'-'+str(pt)+'.txt'
        listFout(p,basePath)
        pt+=1
        while len(p) == seg:
            b=genSeg(seg,q)
            p=list(b)
            basePath='/Users/admin/Desktop/seamless/perm_data/OrderedPairPerm-'+str(i)+'-'+str(pt)+'.txt'
            listFout(p,basePath)
            pt+=1
        t2= time()
        print i,t2-t1
    return p
def gen_good_combos(pairCount,choose):
    ABC='ABCDEFGHIJKLMNOPQRUSTUVXYZ'
    b=list(ABC[:pairCount])
    q=good_combos(b,choose)
    g=list(q)
    basePath='/Users/admin/Desktop/seamless/perm_data/AllPairPerm_NoRep-'
    filePath=basePath+str(pairCount)+'.txt'
    listFout(g,filePath)
    return g
from random import randint,random
def randomNum(start_num,end_num,float_num=False):

    if float_num == False:
        if type(start_num) == float:
            a=str(start_num)
            c=len(a)-1
            start_num=int(start_num*c*10)
            end_num=int(end_num*c*10)
            x=randint(start_num,end_num)
            x=x/(c*10.0)
            return x
        else: return randint(start_num,end_num)
    else: return random()
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
def bestDeliveryRoute(current_location, start_time, delivery_locations, order_times):
    from math import factorial
    def genperm(iter_count):
        from itertools import permutations
        return permutations(iter_count)

    if len(delivery_locations)>5:
        print '\ntoo many delivery locations == too many permutations\n'
        print delivery_locations
        print '\n'
        systemError()

    x=genperm(delivery_locations)
    travel_combo=map(list,x.next())
    travel_combo.insert(0,current_location)
    travel_combo.insert(len(travel_combo),current_location)
    # best delivery irregardless of meeting delivery conditions
    shortest_time=get_multi_travel_times(travel_combo)
    shortest_combo=travel_combo[1:-1]
    # best delivery & delivery cond. good
    trav_str,total_order_time,cumul_time_pt = [],[],start_time
    for i in range(1,len(travel_combo[:-1])):
        it = travel_combo[i]
        trav_str.append(str(it))
        total_order_time_pt = order_times[i-1]
        time_to_next_loc = get_travel_time(travel_combo[i-1],it)
        cumul_time = cumul_time_pt + time_to_next_loc
        cumul_time_pt = cumul_time
        total_order_time.append(cumul_time - total_order_time_pt)
    if max(total_order_time)<=max_delivery_time:
        shortest_time_Conditions=get_multi_travel_times(travel_combo)
        shortest_combo_Conditions=travel_combo[1:-1]
    else:
        shortest_time_Conditions = max_delivery_time * 2
    loc_ot_dict = dict(zip(trav_str,order_times))


    for i in range(1,factorial(len(delivery_locations))):
        try:
            travel_combo=map(list,x.next())
        except:
            print 'error'
            travel_combo=map(list,x.next())
        # best delivery irregardless of meeting delivery conditions
        travel_combo.insert(0,current_location)
        travel_combo.insert(len(travel_combo),current_location)
        travel_combo_time=get_multi_travel_times(travel_combo)
        if travel_combo_time<shortest_time:
            shortest_time=travel_combo_time
            shortest_combo=travel_combo[1:-1]

        # best combo satisfying conditions
        re_sorted_order_times = 'e'
        trav_str,total_order_time,cumul_time_pt = [],[],start_time
        for i in range(1,len(travel_combo[:-1])):
            it = travel_combo[i]
            trav_str.append(str(it))
            total_order_time_pt = loc_ot_dict[str(it)]
            time_to_next_loc = get_travel_time(travel_combo[i-1],it)
            cumul_time = cumul_time_pt + time_to_next_loc
            cumul_time_pt = cumul_time
            total_order_time.append(cumul_time - total_order_time_pt)
        if max(total_order_time)<shortest_time_Conditions:
            shortest_time_Conditions=get_multi_travel_times(travel_combo)
            shortest_combo_Conditions=travel_combo[1:-1]

    if shortest_time_Conditions != max_delivery_time * 2:
        bestCombo = shortest_combo_Conditions
        bestTime = shortest_time_Conditions
    else:
        bestCombo = shortest_combo
        bestTime = shortest_time

    return bestCombo,bestTime

def pg_get_random_pt_in_circle_around_node(node,cir_rad):

    ## North     azimuth 0       (0)
    ## East      azimuth 90      (pi/2)
    ## South     azimuth 180     (pi)
    ## West      azimuth 270     (pi*1.5)

    T = {'1':str(node),
         '2':str(random()*cir_rad),
         '3':str(randomNum(0,360)),
         'vert_t':vert_t,
         'vert_g':vert_g}
    cmd =   """
            select ST_Project(%(vert_g)s, %(2)s, radians(%(3)s)) geom
            from %(vert_t)s where id = %(1)s
            """%T
    return gd.read_postgis(cmd,engine).geom[0].to_wkt()

def pg_get_random_node_in_box(box_area):
    cmd =   """
            select z_get_nodes_in_geom('%(vert_t)s',
                           '%(vert_g)s',
                           z_get_way_box(%(1)s))
            """%{'1':box_area,'vert_t':vert_t,'vert_g':vert_g}

def pg_get_nodes_in_geom(in_geom=''):
    if in_geom!='':
        T = {   'node_table':vert_t,
                'node_col':vert_g,
                'in_geom':in_geom}
    else:
        T = {   'node_table':vert_t,
                'node_col':vert_g,
                'in_geom':"z_get_way_box(%s)"%str(work_area).strip('[]')}

    cmd = """select z_get_nodes_in_geom(
                        '%(node_table)s',
                        '%(node_col)s',
                        %(in_geom)s ) res"""%T
    d = pd.DataFrame(eval(pd.read_sql(cmd,engine).res[0]))
    return d

def pg_update_table_with_random_pt_in_circle_around_node(table,col,gid,node,cir_rad):

    ## North     azimuth 0       (0)
    ## East      azimuth 90      (pi/2)
    ## South     azimuth 180     (pi)
    ## West      azimuth 270     (pi*1.5)

    T = {'1':str(node),
         '2':str(random()*cir_rad),
         '3':str(randomNum(0,360))}
    cmd =   """
                select ST_Project(st_geomfromtext('%(1)s',4326), %(2)s, radians(%(3)s)) geom
            """%T
    return str(gd.read_postgis(""%T,engine).geom[0])

def pg_get_cir_ctr_and_rad_bounding_way_box(way_box):
    T = {'1':str(way_box).strip('[]')}
    cir_ctr = gd.read_postgis("select st_centroid(ST_MinimumBoundingCircle(z_get_way_box(%(1)s))) geom"%T,engine).geom[0]
    cir_rad = pd.read_sql_query("""
                        select st_maxdistance(outer_ring,ctr_pt) res
                        from
                            (select st_centroid(ST_MinimumBoundingCircle(z_get_way_box(%(1)s))) ctr_pt) as t1,
                            (select ST_ExteriorRing(ST_MinimumBoundingCircle(z_get_way_box(%(1)s))) outer_ring) as t2
                        """.replace('\n',' ')%T,engine).res[0]
    return cir_ctr,cir_rad

def pg_get_travel_time(start_node,end_node):
    return MPH * pd.read_sql("select z_get_miles_between_nodes('%s',%s,%s) dist"%(way_t,start_node,end_node),engine).dist[0]

def make_simulation_data_from_real_data(savePath=''):
    from classes import Vendor,Delivery,DG
    from random import randrange

    if savePath == '': savePath=this_cwd+'/sim_data/vendor_sim_data.txt'
    a = Vendor()
    col_names = a.toDict().keys()
    df = pd.DataFrame(columns=col_names)

    cmd=geom_inside_street_box(work_area,geom_table='vendors',geom_label='geom',
                               table_cols=['seam_id','node'],conditions=None)
    vdf=gd.read_postgis(cmd,engine)
    if len(vdf)>vend_num: vdf=vdf.ix[:vend_num,:]

    vendors = []
    for i in range(0,vend_num):
        it = vdf.ix[i,:]
        v = Vendor()
        v.vend_id = i
        vend_node = it.node
        deliv_per_vend = randomNum(*deliveries_per_vend)
        for j in range(0,deliv_per_vend):
            v.order_num = j
            stop = False
            v.delivery.start_node = vend_node
            v.delivery.order_time = randomNum(0,vend_hours_delivering*60)
            v.delivery.end_point = pg_get_random_pt_in_circle_around_node(vend_node,cir_rad=deliv_radius_per_vendor_in_km)
            v.delivery.end_node = pd.read_sql("select z_get_closest_node_to_point_text('%s','%s','%s') pt"%(vert_t,vert_g,v.delivery.end_point),engine).pt[0]
            vendors.append(v.toDict())

    df = pd.DataFrame(vendors)
    df = df.ix[:,[   'vend_id',
                     'order_num',
                     'order_time',
                     'start_point',
                     'start_node',
                     'start_time',
                     'travel_time',
                     'end_time',
                     'end_point',
                     'end_node',
                     'total_order_time',
                     'deliv_id'  ]]
    engine.execute('drop table if exists sim_data')
    df.drop(['deliv_id'],axis=1).to_sql('sim_data',engine,if_exists='append',index=False)
    make_column_primary_serial_key(table='sim_data',p_key='deliv_id',new_col=True)

    # df = df.drop(['start_time','end_time','total_order_time','travel_time'],axis=1)
    # df = pd.DataFrame(df.astype(long).as_matrix(),columns=df.columns)
    df['deliv_id'] = df.index
    df.to_hdf(savePath.rstrip('.txt')+'.h5','table')
    return df

def make_simulation_data(savePath=''):
    from random import randrange

    if savePath == '': savePath=this_cwd+'/sim_data/vendor_sim_data.txt'

    a = Vendor()
    a = a.printHeader(printer=False,fullHeading=True)
    z = a.split('\t')

    col_names = a.to
    df = pd.DataFrame(columns=col_names)

    vend,vendors = a+'\r',[]
    for i in range(0,vend_num):
        v = Vendor()
        v.id = i
        x = 3*randrange(0,vend_loc_x_max) #note: the "3*" is based on 1 avenue = 3 streets
        y = randrange(0,vend_loc_y_max)
        v.vend_X = x
        v.vend_Y = y
        for j in range(0,deliveries_per_vend):
            v.order_num = j
            stop = False
            # while stop == False:
            x_min,x_max = v.vend_X-(int(round((vend_del_x_range/2.0)))*3),v.vend_X+(int(round((vend_del_x_range/2.0)))*3)
            y_min,y_max = v.vend_Y-int(round((vend_del_y_range/2.0))),v.vend_Y+int(round((vend_del_y_range/2.0)))
            x = 3*int(round(randomNum((x_min/3.0),(x_max/3.0)),0))
            y = int(round(randomNum(y_min,y_max),0))
            # if sqrt((x-vend_loc_x_max)**2 + (y-vend_loc_y_max)**2) < vend_deliver_radius:
            v.delivery.start_X = v.vend_X
            v.delivery.start_Y = v.vend_Y
            v.delivery.order_time = randomNum(0,vend_hours_delivering*60)
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
    df = pd.DataFrame(df.astype(long).as_matrix(),columns=df.columns)
    df.to_hdf(savePath.rstrip('.txt')+'.h5','table')
    return df
def open_pd_sim_data(openPath=''):
    if openPath == '': openPath=this_cwd+'/sim_data/pd_vendor_sim_data.txt'
    DTYPES={'id':np.long,
           'vend_X':np.long,
           'vend_Y':np.long,
           'order_num':np.dtype(long),
           #'deliv_id':np.dtype(long),
           'order_time':np.dtype(long),
           #'start_time':np.dtype(long),
           'start_X':np.dtype(long),
           'start_Y':np.dtype(long),
           #'end_time':np.dtype(long),
           'end_X':np.dtype(long),
           'end_Y':np.dtype(long),
           #'total_order_time':np.dtype(long),
           #'travel_time':np.dtype(long)
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

def NormalDelivery(vendors):
    print '\nstarting Normal Delivery Sim.\n'
    def deliver_all_orders(d_orders,d_time,results):
        a = d_orders.sort('start_time').reset_index(drop=True)
        # create back_log data
        try: current_location = a.ix[0,['vend_X','vend_Y']].astype(np.int64).tolist()
        except: systemError()
        delivery_locations = a[['end_X','end_Y']].astype(np.int64).as_matrix().tolist()
        order_times = a.order_time.astype(np.int64).tolist()

        # GET BEST DELIVERY ROUTE -- ( starting location is inserted at beginning of "shortest_combo"
        shortest_combo,shortest_time = bestDeliveryRoute(current_location,d_time,delivery_locations,order_times)

        start_pt,home_pt = current_location,current_location
        time_pt = d_time # which is when DG is planning on leaving
        start,end=False,False
        for i in range(len(shortest_combo)):
            b = a.ix[i,:]
            b['start_time'] = time_pt
            b[['start_X','start_Y']] = start_pt
            b['travel_time'] = get_travel_time(start_pt,b[['end_X','end_Y']].astype(np.int64).tolist())
            time_pt += b['travel_time']
            b['end_time'] = time_pt
            b['total_order_time'] = b['end_time'] - b['order_time']
            if i==0: b['tripStart']=True
            if i+1==len(shortest_combo): b['tripEnd']=True
            results = results.append(b)
            start_pt = b[['end_X','end_Y']].astype(np.int64).tolist()
        return_time = get_travel_time(start_pt,home_pt)
        time = time_pt + return_time
        return results,time

    wait_at_vendor=Assumption('wait_at_vendor')

    vend_cols = eval(str(vendors.columns.tolist()).replace('id','v_id'))
    vendors.columns = vend_cols
    vendors['dg_id'] = 0
    vendors = vendors.ix[:,['dg_id']+vend_cols]
    vendors['start_time'] = 0
    vendors['end_time'] = 0
    vendors['total_order_time'] = 0
    vendors['travel_time'] = 0
    vendors['tripStart'] = False
    vendors['tripEnd'] = False

    vendor_grp = vendors.groupby('v_id')
    groupList = vendor_grp.groups.keys()

    all_results = vendors.reset_index(drop=True).ix[:-1,:]
    for j in range(len(groupList)):

        V = vendor_grp.get_group(groupList[j]).sort_index(by='order_time',ascending=True).reset_index(drop=True)

        # Time starts on first delivery order.
        # DG does delivery for all undelivered orders up to (time + wait time)
        #   time = DG return time
        # DG returns.
        # DG does delivery for all undelivered orders up to (time + wait time)
        #   time = DG return time
        # DG returns.
        # etc...
        # each time there are more than 5 orders:
        #   an additional DG is used to deliver first five orders
        #
        #   then orders are delivered in groups of 5 (no wait time in between)


        # Time starts on first delivery order.
        # DG does delivery for all undelivered orders up to (time + wait time)
        #   time = DG return time
        # DG returns.

        # if any total_order_time>md upon DG doing delivery for all undelivered orders up to (time + wait time):
        #   go back to time of first undelivered order.
        #       build new grp undelivered orders provided total_order_time<=md

        # DG does delivery for all undelivered orders up to (time + wait time)
        #   time = DG return time
        # DG returns.
        # etc...
        # each time there are more than 5 orders:
        #   an additional DG is used to deliver first five orders
        #
        #   then orders are delivered in groups of 5 (no wait time in between)
        #

        order_times = V.order_time.astype(np.int64).tolist()
        vend_results = V.ix[:-1,:]

        currentDG = 0
        time=order_times[0]
        pt=0
        while len(V) != len(vend_results) and len(V)>len(vend_results):

            d_time = time + wait_at_vendor
            # print 'd_time =',d_time
            # print 'time',time

            # if time>120:
            #     print orders_for_delivery
            #     print deliver_all_orders(orders_for_delivery,d_time,vend_results)[0]
            #     systemError()

            # orders_for_delivery = V[(V.index>len(vend_results)-1) & (V.order_time<=d_time)]
            # print orders_for_delivery
            # if len(orders_for_delivery)>=2:
            #
            #     print time
            #     a = orders_for_delivery.reset_index(drop=True)
            #     complete = False
            #     dg_ID = 0
            #     s,e = 0,1
            #     n_time = d_time
            #     while complete==False:
            #         if len(a) < e:
            #             complete=True
            #             systemError()
            #             break
            #         first_check_orders = a.ix[s:e,:]
            #         first_vend_results,first_time = deliver_all_orders(first_check_orders,n_time,vend_results)
            #         e += 1
            #         second_check_orders = a.ix[s:e,:]
            #         second_vend_results,first_time = deliver_all_orders(second_check_orders,n_time,vend_results)
            #         if second_vend_results.total_order_time.max()>max_delivery_time or e>len(a):
            #             e -= 1
            #             check_orders = a.ix[s:e,:]
            #             check_orders.dg_id = dg_ID
            #             dg_ID += 1
            #             print vend_results
            #             vend_results,time = deliver_all_orders(check_orders,n_time,vend_results)
            #             print vend_results,'\n\n'
            #             s = e
            #             e += 1
            #         else:
            #             e += 1
            #     orders_for_delivery.dg_id = 1
            #     vend_results,time = deliver_all_orders(orders_for_delivery,d_time,vend_results)
            #     print vend_results
            #     print time
            #     systemError()
                # a = orders_for_delivery.reset_index(drop=True)
                # b = int(len(a)/5.0)
                # for k in range(1,b):
                #     check_orders = a.ix[(k-1)*5:k*5,:]
                #     vend_results,d_time = deliver_all_orders(check_orders,d_time,vend_results)
                # if len(a) > 5*b:
                #     last_check = a.ix[b*5:,:]
                #     vend_results,d_time = deliver_all_orders(last_check,d_time,vend_results)
                # time = d_time
                #
                # one method -- take most amount of orders where delivery<md
                #
            # if len(orders_for_delivery) != 0:
            #     vend_results,time = deliver_all_orders(orders_for_delivery,d_time,vend_results)
            # elif len(orders_for_delivery) == 0:
            #     time = V[V.index==len(vend_results)-1+1].order_time.astype(np.int64).values[0]        # time = next order.order_time


            # if DG cannot timely deliver orders occurring between d_time (time DG leaves for delivery) and time (time dg returns)
            #   send out as many DG as necessary to ensure total_order_time.max()<=md
            # print 'time =',time

            # check_orders = V[(V.order_time>d_time) & (V.order_time<=time)]
            orders_for_delivery = V[(V.index>len(vend_results)-1) & (V.order_time<=d_time)]
            # print 'orders_for_delivery\n',orders_for_delivery
            if len(orders_for_delivery)!=0:

                # if time>150:
                #     print deliver_all_orders(orders_for_delivery,time,vend_results)[0]

                if len(orders_for_delivery)<=5 and deliver_all_orders(orders_for_delivery,d_time,vend_results)[0].total_order_time.max()<=max_delivery_time:
                    vend_results,time = deliver_all_orders(orders_for_delivery,d_time,vend_results)

                elif len(orders_for_delivery)<=5 and deliver_all_orders(orders_for_delivery,time,vend_results)[0].total_order_time.max()<=max_delivery_time:
                    vend_results,time = deliver_all_orders(orders_for_delivery,time,vend_results) # note "time" not "d_time"

                else:  # See #1 below

                    # FIRST -- work backward and figure out if DG can deliver any undelivered orders.
                    #   if so, do not use in multi-DG
                    a = orders_for_delivery.sort_index(by='order_time',ascending=False).reset_index(drop=True)
                    complete = False
                    s,e = 0,0
                    while complete==False:
                        if len(a) == e:     # here, because of #1, DG cannot deliver all orders. so if all orders is next iteration, e -= 1
                            complete=True
                            e -= 1
                            break
                        save_orders = a.ix[s:e,:]

                        if len(save_orders)<=5 and deliver_all_orders(save_orders,time,vend_results)[0].total_order_time.max()<=max_delivery_time:
                            e += 1
                        else:
                            complete = True
                            if e!=0:
                                vend_results,time = deliver_all_orders(a.ix[s:e-1,:],time,vend_results)
                                # e -= 1
                            break


                    # SECOND -- work forward from earliest undelivered and maintain delivery condition using multi-DG
                    b = a.ix[e:,:].sort_index(by='order_time',ascending=True).reset_index(drop=True)
                    complete = False
                    dg_ID = 1
                    s,e = 0,0

                    while complete==False:
                        if len(b) <= e:
                            complete=True
                            break
                        # print '2',e-s
                        first_orders_for_delivery = b.ix[s:e,:]
                        first_orders_for_delivery.dg_id = dg_ID
                        n_time = first_orders_for_delivery.order_time.max()
                        first_vend_results,first_time = deliver_all_orders(first_orders_for_delivery,n_time,vend_results)
                        e += 1
                        # print '3',e-s,time,d_time
                        second_orders_for_delivery = b.ix[s:e,:]
                        if len(first_orders_for_delivery) == len(second_orders_for_delivery):
                            vend_results = first_vend_results
                            complete=True
                            break
                        second_orders_for_delivery.dg_id = dg_ID
                        n_time = second_orders_for_delivery.order_time.max()
                        second_vend_results,first_time = deliver_all_orders(second_orders_for_delivery,n_time,vend_results)

                        if second_vend_results.total_order_time.max()>max_delivery_time or e>len(b):
                            vend_results = first_vend_results
                            dg_ID += 1
                            s = e
                        elif second_vend_results.total_order_time.max()<=max_delivery_time and len(second_orders_for_delivery)==5:
                            vend_results = second_vend_results
                            dg_ID += 1
                            e += 1
                            s = e
                    # TODO: small issue: when additional DG are used in normal delivery, additional DG start_time==latest(add. DG orders.order_time)
                    #   add. DG start_time could also equal latest possible time to leave and satisfy delivery conditions.
                    #   -- Result? lowers total_order_time values?


            elif len(orders_for_delivery) == 0:
                try:
                    time = V[V.index==len(vend_results)-1+1].order_time.astype(np.int64).values[0]        # time = next order.order_time
                except:
                    systemError()

            # while loop safety
            if pt > len(V):
                print 'why not exit?'
                systemError()
            else: pt+=1

            # print '\nvend_results:\n',vend_results
            # a=0
            del_ids = vend_results.deliv_id.astype(np.int64).tolist()
            uniq_del_ids = dict(zip(del_ids,range(len(del_ids)))).keys()
            for it in uniq_del_ids:
                if del_ids.count(it)>1:
                    print vend_results
                    print it
                    systemError()

        if len(vend_results)!=len(V):
            print vend_results
            print len(vend_results),len(V)
            del_ids = vend_results.deliv_id.astype(np.int64).tolist()
            uniq_del_ids = dict(zip(del_ids,range(len(del_ids)))).keys()
            for it in uniq_del_ids:
                if del_ids.count(it)>1:
                    print it
            systemError()


        # print vend_results
        # systemError()
        all_results = pd.merge(all_results,vend_results,how='outer')
        print j+1,'of',len(groupList)

    savePath = this_cwd+'/sim_data/ND_results.txt'
    all_results.to_csv(savePath, index=False, header=True, sep='\t')
    print '\nNormal Delivery Simulation Completed\n'
    return

def init_dg_pool(pt,dg_grp_size=None,old_dg_pool=None,load=False,save=False,filePath=''):
    from random import randrange

    if filePath == '': filePath=this_cwd+'/sim_data/pd_dg_pool.txt'
    if load == True:
        new_dg_pool = gd.read_postgis("select dg_id,total_delivered,current_deliveries,st_geomfromtext(dg_node) geom from dg_pool",engine)
    
    elif load==False:
        DG_start_location_grid = Assumption('DG_start_location_grid')
        new_dg_pool = pd.DataFrame({'dg_id':range(pt*DG_num,(DG_num*pt)+DG_num)})
        ## get info for circle that bounds way box
        cir_ctr,cir_rad = pg_get_cir_ctr_and_rad_bounding_way_box(work_area)
        ## get random points within circle
        node_ids = pg_get_nodes_in_geom()
        node_cnt = len(node_ids)
        new_dg_pool['dg_node'] = new_dg_pool.dg_id.map(lambda s: node_ids.ix[randrange(0,node_cnt),'id'])
        new_dg_pool['coords'] = new_dg_pool.index*0
        new_dg_pool['total_delivered'] = new_dg_pool.index*0
        new_dg_pool['current_deliveries'] = new_dg_pool.index*0

        if save == True:
            if old_dg_pool==None:  engine.execute('drop table if exists dg_pool')
            new_dg_pool.drop(['dg_id'],axis=1).to_sql('dg_pool',engine,if_exists='append',index=False)
            if old_dg_pool==None:  make_column_primary_serial_key(table='dg_pool',p_key='dg_id',new_col=True)
            print 'made primary key'

    if old_dg_pool!=None:
        maxID = old_dg_pool.dg_id.values.max()
        new_dg_pool.dg_id = new_dg_pool.dg_id.values + (maxID+1)
        new_dg_pool = pd.merge(old_dg_pool,new_dg_pool,how='outer').sort('dg_id').reset_index(drop=True)

    return new_dg_pool

from pg_fxs import pg_get_travel_dist

def new_dg_to_order_q(new,order_q_i,errorCheck=True):
    row = order_q_i.reset_index(drop=True).ix[0,:].copy()
    row['status'] = 'on deck'
    row['deliv_num'] = 1

    node_array = [order_q_i['dg_node'][0],new['end_node']]
    cost_tbl = pg_get_travel_dist(new['start_node'],node_array)

    row['travel_time_to_loc'] = cost_tbl.cost[0] * MPH
    row['deliv_id'] = new['deliv_id']
    row['order_time'] = new['order_time']
    row['start_point'] = new['start_point']
    row['start_node'] = new['start_node']
    row['start_time'] = new['order_time'] + row['travel_time_to_loc']

    row['travel_time']=cost_tbl.cost[1] * MPH
    row['end_time'] = row['start_time'] + row['travel_time']
    row['end_point'] = new['end_point']
    row['end_node'] = new['end_node']
    row['total_order_time']= row['end_time'] - row['order_time']

    updated_order_q_i = order_q_i.ix[:-1,:].append(row)
    updated_dg_q_i = pull_from_order(updated_order_q_i,errorCheck=errorCheck)
    if errorCheck==True: error_check(order_q_i=updated_order_q_i,dg_q_i=None)
    return updated_order_q_i,updated_dg_q_i
def updateCurrentLocation(globalVars,now,changedDG=[]):
    order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
    travel_speed=Assumption('travel_speed')

    # if just finishing delivery, and currentDeliv will be 0, update location from order_q endPoint ...
    if len(changedDG) != 0:
        oq = order_q
        last_orders = oq[(oq.id.isin(changedDG)==True) & (oq.end_time==now)]
        if len(last_orders)!=0:
            last_order_ids = last_orders.id.astype(np.int64).tolist()
            last_order_id_ind_dict = dict(zip(last_orders.id.astype(np.int64).tolist(),last_orders.index))

            dyn_dg_pool = dg_pool[dg_pool.dg_id.isin(last_order_ids)==True]
            dyn_dg_pool_ids = dyn_dg_pool.dg_id.astype(np.int64).tolist()

            take_index = map(lambda s: last_order_id_ind_dict[s],dyn_dg_pool_ids)

            stat_dg_pool = dg_pool.ix[dg_pool.index - dyn_dg_pool.index]

            dyn_dg_pool[['dg_X','dg_Y']] = last_orders.ix[dyn_dg_pool_ids,['end_X','end_Y']].values
            dg_pool = pd.merge(stat_dg_pool,dyn_dg_pool,how='outer')

    static_dg_pool = dg_pool[(dg_pool.current_deliveries==0)]
    dyn_dg_pool = dg_pool.ix[dg_pool.index - static_dg_pool.index,:]
    if len(dyn_dg_pool.index)==0: return globalVars
    dyn_dg_pool_ids = dyn_dg_pool.dg_id.astype(np.int64).values.tolist()
    dg_q_i = dg_q[(dg_q.dg_id.isin(dyn_dg_pool_ids)==True) & (dg_q['pta-t'] <= now) & (now <=dg_q['ptb-t'])]

    dg_q_start = dg_q_i[dg_q_i['pta-t']==now].reset_index(drop=True)
    if len(dg_q_start.index)!=0:
        dg_q_start_ids = dg_q_start.dg_id.astype(np.int64).values.tolist()
        new_dg_pool = dg_pool[dg_pool.dg_id.isin(dg_q_start_ids)].reset_index(drop=True)
        new_dg_pool['map'] = new_dg_pool.dg_id.map(lambda s: dg_q_start_ids.index(int(s)))
        new_dg_pool.ix[:,['dg_X','dg_Y']] = dg_q_start.ix[new_dg_pool.map.astype(np.int64).tolist(),['ptax','ptay']].values

        globalVars = update_global_vars(globalVars,'update dg_pool',newAddVar=new_dg_pool.drop(['map'],axis=1).reset_index(drop=True),newSubVar=False,replaceVar={'id':dg_q_start_ids})
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt

    dg_q_end = dg_q_i[dg_q_i['ptb-t']==now].reset_index(drop=True)
    if len(dg_q_end.index)!=0:
        dg_q_end_ids = dg_q_end.dg_id.astype(np.int64).values.tolist()
        new_dg_pool = dg_pool[dg_pool.dg_id.isin(dg_q_end_ids)].reset_index(drop=True)
        new_dg_pool['map'] = new_dg_pool.dg_id.map(lambda s: dg_q_end_ids.index(int(s)))
        new_dg_pool.ix[:,['dg_X','dg_Y']] = dg_q_end.ix[new_dg_pool.map.astype(np.int64).tolist(),['ptax','ptay']].values

        globalVars = update_global_vars(globalVars,'update dg_pool',newAddVar=new_dg_pool.drop(['map'],axis=1).reset_index(drop=True),newSubVar=False,replaceVar={'id':dg_q_end_ids})
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt

    df = dg_q_i[(dg_q_i['pta-t']>now) & (now<dg_q_i['ptb-t'])] # do not reset index as it is used later
    if len(df.index)!=0:
        df['L'] = (now - df['pta-t'])*travel_speed
        df['dx'] = df['ptbx']-df['ptax']
        df['posx'] =  df.dx.map(lambda s: True if s>0 else False)
        df['dy'] = df['ptby']-df['ptay']
        df['posy'] =  df.dy.map(lambda s: True if s>0 else False)
        df['abs_dx'] = df.dx.map(lambda s: s if s>0 else -1*s)
        df['xonly'] =  df.abs_dx - df.L
        df['xonly'] = df.xonly.map(lambda s: True if s>=0 else False)
        df_xonly = df[df.xonly==True].reset_index(drop=True)
        if len(df_xonly.index)!=0:

            df_xonly['dg_X'],df_xonly['dg_Y'] = np.empty((len(df_xonly.index),), dtype=np.long),df_xonly['ptay'].values
            df_xonly_posInd = df_xonly[df_xonly.posx==True].index
            df_xonly_negInd = df_xonly.index - df_xonly_posInd

            df_xonly.ix[df_xonly_posInd,'dg_X'] = df_xonly.ix[df_xonly_posInd,'ptax'] + df_xonly.ix[df_xonly_posInd,'L']
            df_xonly.ix[df_xonly_negInd,'dg_X'] = df_xonly.ix[df_xonly_negInd,'ptax'] - df_xonly.ix[df_xonly_negInd,'L']

            df_xonly_ids = df_xonly.dg_id.astype(np.int64).values.tolist()
            new_dg_pool = dg_pool[dg_pool.dg_id.isin(df_xonly_ids)].reset_index(drop=True)
            new_dg_pool['map'] = new_dg_pool.dg_id.map(lambda s: df_xonly_ids.index(int(s)))
            new_dg_pool.ix[:,['dg_X','dg_Y']] = df_xonly.ix[new_dg_pool.map.astype(np.int64).tolist(),['ptax','ptay']].values
            globalVars = update_global_vars(globalVars,'update dg_pool',newAddVar=new_dg_pool.drop(['map'],axis=1).reset_index(drop=True),newSubVar=False,replaceVar={'id':df_xonly_ids})
            order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
            globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt

            df_xonly['zero'] = df_xonly.dx.map(lambda s: True if s==0 else False)
            if len(df_xonly[df_xonly.zero==True].index)>0:
                print 'check this in update location'
                systemError()

        df_xy = df.ix[df.index - df_xonly.index,:]
        if len(df_xy.index)!=0:
            df_xy['dg_X'],df_xy['dg_Y'] = df_xy['ptbx'].values,np.empty((len(df_xy.index),), dtype=np.long)
            # change L based on X-axis changes
            df_xy_posInd = df_xy[df_xy.posx==True].index
            df_xy_negInd = df_xy.index - df_xy_posInd
            df_xy.ix[df_xy_posInd,'L'] = df_xy.ix[df_xy_posInd,'L'] - df_xy.ix[df_xy_posInd,'dx']
            df_xy.ix[df_xy_negInd,'L'] = df_xy.ix[df_xy_negInd,'L'] + df_xy.ix[df_xy_negInd,'dx']
            # Determine Y-axis values
            df_xy_posInd = df_xy[df_xy.posy==True].index
            df_xy_negInd = df_xy.index - df_xy_posInd
            df_xy.ix[df_xy_posInd,'dg_Y'] = df_xy.ix[df_xy_posInd,'ptay'] + df_xy.ix[df_xy_posInd,'L']
            df_xy.ix[df_xy_negInd,'dg_Y'] = df_xy.ix[df_xy_negInd,'ptay'] - df_xy.ix[df_xy_negInd,'L']
            # Update dg_pool
            df_xy_ids = df_xy.dg_id.astype(np.int64).values.tolist()
            new_dg_pool = dg_pool[dg_pool.dg_id.isin(df_xy_ids)].reset_index(drop=True)
            new_dg_pool['map'] = new_dg_pool.dg_id.map(lambda s: df_xy_ids.index(int(s)))
            new_dg_pool.ix[:,['dg_X','dg_Y']] = df_xy.ix[new_dg_pool.map.astype(np.int64).tolist(),['ptax','ptay']].values
            globalVars = update_global_vars(globalVars,'update dg_pool',newAddVar=new_dg_pool.drop(['map'],axis=1).reset_index(drop=True),newSubVar=False,replaceVar={'id':df_xy_ids})
            order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
            globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt

    return globalVars
def eval_combos(var_group,saveOutput=False):
    delivery_count,dg_group_i,new,deliv_id,start_loc,end_loc=var_group
    location_count=(delivery_count*2)+1
    row=dg_group_i.iloc[0,:]

    #
    # mock_pairs = pairSet[pairSet['mc'+str(delivery_count)]==True][['a','b']]
    # mock_pairs.a = mock_pairs.a.map(num_to_mock_dict)
    # mock_pairs.b = mock_pairs.b.map(num_to_mock_dict)
    #
    # mock_travel_combos = orderSet[orderSet['mc'+str(delivery_count)]==True].ix[:,'pt0':'pt7']
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
    max_delivery_time = Assumption('max_delivery_time')
    #combos=combos[(combos.maxOrderTime <= max_delivery_time)]
    saveOutput=True
    if saveOutput==True:
        pd_Combos_path=this_cwd+'/sim_data/EDA_combos_data.txt'
        combos.to_csv(pd_Combos_path, index=False, header=True, sep='\t')
    return combos

def get_best_combo(testSet,get_combo_vars,c_global_vars,test=False,parallel=False):
    # if parallel == True:
    from get_best_combo import c_get_best_combo
    from map_points_to_combos import c_mapper2,c_mapper3,c_mapper4,c_mapper5,c_mapper6,c_mapper7
    stPtx,stPty,c_tripStartTime,order_times,c_travel_speed,c_max_delivery_time,c_max_travelToLocTime,c_delivery_count,deliv_ids,realPoints = get_combo_vars
    c_travel_times_r,c_start_times_r,c_end_times_r,c_odtTimes_r,c_oMaxTimes_r,c_tMaxTimes_r,c_tddTimes_r,c_ctMarker_r,c_returnVars_r = c_global_vars

    points=testSet.ix[:,'pt0':'pt'+str(c_delivery_count*2-1)]
    orderSortKey=np.ascontiguousarray(testSet.ix[:,'i0':'i'+str(c_delivery_count-1)].as_matrix(),dtype=np.long)
    ptsSortKey=np.ascontiguousarray(testSet.ix[:,'a1':ABC[c_delivery_count-1].lower()+'2'].as_matrix(),dtype=np.long)
    mockCombos=np.ascontiguousarray(points.as_matrix(),dtype=np.long)
    r,c = mockCombos.shape
    realCombos = np.empty((r,c,2),dtype=np.long,order='C')
    if c_delivery_count == 2:  realCombos = c_mapper2(realPoints, mockCombos, realCombos)
    if c_delivery_count == 3:  realCombos = c_mapper3(realPoints, mockCombos, realCombos)
    if c_delivery_count == 4:  realCombos = c_mapper4(realPoints, mockCombos, realCombos)
    if c_delivery_count == 5:  realCombos = c_mapper5(realPoints, mockCombos, realCombos)
    if c_delivery_count == 6:  realCombos = c_mapper6(realPoints, mockCombos, realCombos)
    if c_delivery_count == 7:  realCombos = c_mapper7(realPoints, mockCombos, realCombos)

    if test==True:
        c_vars = test_get_best_combo(stPtx, stPty, mockCombos, realCombos,
                                  orderSortKey, ptsSortKey, order_times,
                                  deliv_ids, c_delivery_count, c_tripStartTime, c_travel_speed, c_max_delivery_time,
                                  c_max_travelToLocTime, c_travel_times_r, c_start_times_r, c_end_times_r,
                                  c_odtTimes_r, c_oMaxTimes_r, c_tMaxTimes_r, c_tddTimes_r,
                                  c_ctMarker_r, c_returnVars_r)
    else:
        c_vars = c_get_best_combo(stPtx, stPty, mockCombos, realCombos,
                                  orderSortKey, ptsSortKey, order_times,
                                  deliv_ids, c_delivery_count, c_tripStartTime, c_travel_speed, c_max_delivery_time,
                                  c_max_travelToLocTime, c_travel_times_r, c_start_times_r, c_end_times_r,
                                  c_odtTimes_r, c_oMaxTimes_r, c_tMaxTimes_r, c_tddTimes_r,
                                  c_ctMarker_r, c_returnVars_r)

    if c_vars[0][13] != 0:
        order_q_results = pd.DataFrame([[col for col in row] for row in c_vars],columns=['dg_X','dg_Y','deliv_num','deliv_id','order_time','travel_time_to_loc','start_X','start_Y','start_time','travel_time','end_time','end_X','end_Y','total_order_time','bestIndex'])
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
def eval_additional_order(tripStartPt,tripStartTime,var_group,errorCheck=True):
    order_q_i,new,start_loc,end_loc = var_group
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
def run_parallel(testSet,get_delivery_combo,get_combo_vars):
    ppservers=()
    #ppservers = ("192.168.5.2",)
    num_processes=2
    job_server = pp.Server(ppservers=ppservers)
    #print job_server.get_ncpus()
    jobs=[]
    for i in range(0,num_processes):
        runSet=testSet.iloc[(len(testSet.index)*i)/num_processes:(len(testSet.index)*(i+1))/num_processes,:].reset_index(drop=True)
        jobs.append(job_server.submit(get_delivery_combo,(runSet,get_combo_vars,True), (Assumption,), ('pd','np','get_delivery_combo',)))
    #print job_server.print_stats()
    results,travel_times,start,pt=[],[],False,0
    for job in jobs:
        res = job()
        #print res
        if type(res) != NoneType:
            results.append(res)
            travel_times.append(sum(res.travel_time.tolist()))
    if len(travel_times)!=0:
        print 'why return:\n'
        print results[travel_times.index(min(travel_times))]
        systemError()
    return results[travel_times.index(min(travel_times))]
def fix_dg_q_delID_dupes(static_dg_q,new_dg_q,arg_dg_group_i):
    # there should be only two of each deliv_id, otherwise it needs to be fixed...
    del_ids = new_dg_q.deliv_id.astype(np.int64).tolist()
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
        end_times_all = a['ptb-t'].astype(np.int64).tolist()
        end_times_uniq = b.groups.keys()
        end_time_cnt = [end_times_all.count(x) for x in end_times_uniq]
        if end_time_cnt.count(3)==0:
            print 'unknown inconsistency with route'
            print '\nall:\n',end_times_all,'\nuniq:\n',end_times_uniq,'\ncount:\n',end_time_cnt
            print a
            # systemError()
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
def set_mock_pts(new_dg_q):
    # create dictionary associating deliv_ids with mock_pts (based on pickup locations)
    #   then, iterate through rows of new_dg_q and update dict with new mock_pts for each new deliv_id
    all_del_ids = new_dg_q.deliv_id.astype(np.int64).tolist()
    unique_del_ids = new_dg_q.deliv_id.astype(np.int64).unique().tolist()
    id_mock_pt_dict = dict(zip(unique_del_ids,range(0,len(unique_del_ids))))
    counter_list = [all_del_ids[:i].count(all_del_ids[i]) for i in range(0,len(all_del_ids))]
    new_mock_pts = [100+id_mock_pt_dict[all_del_ids[i]] if (counter_list[i]==1 or all_del_ids.count(all_del_ids[i])==1) else id_mock_pt_dict[all_del_ids[i]] for i in range(0,len(all_del_ids))]
    new_dg_q['mock_pt'] = new_mock_pts
    return new_dg_q
def order_q_re_order_deliv_num(order_q_i):
    pta = order_q_i[order_q_i.status=='on route']
    pta.deliv_num = 0
    ptb = order_q_i[order_q_i.status!='on route'].sort_index(by='start_time', ascending=True).reset_index(drop=True)
    ptb.deliv_num = range(1,len(ptb.index)+1)
    order_q_i = pd.merge(pta,ptb,how='outer').sort_index(by='deliv_num', ascending=True).reset_index(drop=True)
    return order_q_i
def getComboStartInfo(new,order_q_i):
    start_loc=[new['start_X'],new['start_Y']]
    end_loc=[new['end_X'],new['end_Y']]
    # assuming x == new['order_time'] == now, and assuming start,end=start_time,end_time
    #   if start<x & end<x: ignore (which should have been cleared from queue and are not considered here)
    #   if start<x & end=x: ignore (which should have been cleared from queue and are not considered here)
    #   if start<x & x<end: use end points only
    #   if start=x & x<end: use end points only
    #   if x<start & x<end: use both points
    # DG potential new trip will start at the next location DG arrives (at least t=t+1)
    # tripStartPts and tripStartTime are the points at the next location and the arrival time

    if len(order_q_i[order_q_i.end_time>new['order_time']].index)==0:
        tripStartTime,tripStartPt = new['order_time'],start_loc
        bestComboVars = 1,tripStartTime,tripStartPt,None,None
        return bestComboVars

    partial_check_orders = order_q_i[   (order_q_i['start_time'] <= new['order_time']) & 
                                        (new['order_time'] < order_q_i['end_time'])  ].reset_index(drop=True)
    full_check_orders = order_q_i[(new['order_time'] < order_q_i['start_time'])].reset_index(drop=True) #  & (new['order_time'] < order_q_i['end_time'])  ??
    # partial_check_orders = order_q_i[(order_q_i['start_time']<=new['order_time']) & (new['order_time']<order_q_i['end_time'])].sort_index(by='end_time',ascending=True).reset_index(drop=True)
    # full_check_orders = order_q_i[(new['order_time']<order_q_i['start_time']) & (new['order_time']<order_q_i['end_time'])].sort_index(by='start_time',ascending=True).reset_index(drop=True)

    # get trip start time and start point
    sTimes = order_q_i.start_time.astype(np.int64).tolist()
    eTimes = order_q_i.end_time.astype(np.int64).tolist()
    aTimes = np.array(sorted(sTimes+eTimes))
    tripStartTime = aTimes[np.where(aTimes>new['order_time'])[0][0]]
    if sTimes.count(tripStartTime)!=0: tripStartPt = order_q_i.ix[sTimes.index(tripStartTime),['start_X','start_Y']].astype(np.int64).tolist()
    else: tripStartPt = order_q_i.ix[eTimes.index(tripStartTime),['end_X','end_Y']].astype(np.int64).tolist()

    # get trip points from partial orders (as well as delivery IDs and order times)
    a = partial_check_orders.ix[:,['end_X','end_Y']].astype(np.int64).values
    b = np.array([[a.T[0],a.T[1]],[a.T[0],a.T[1]]]).T
    c = []
    for it in b: c.extend(it.T.tolist())
    tripPoints = c[:]
    tripDeliveryIDs = partial_check_orders.deliv_id.astype(np.int64).tolist()
    tripOrderTimes = partial_check_orders.order_time.astype(np.int64).tolist()

    # add trip points from full orders
    a = full_check_orders.ix[:,['start_X','start_Y','end_X','end_Y']].astype(np.int64).values
    b = np.array([[a.T[0],a.T[1]],[a.T[2],a.T[3]]]).T
    c = []
    for it in b: c.extend(it.T.tolist())
    tripPoints.extend(c[:])
    tripDeliveryIDs.extend(full_check_orders.deliv_id.astype(np.int64).tolist())
    tripOrderTimes.extend(full_check_orders.order_time.astype(np.int64).tolist())

    # append new order info
    tripPoints.extend([start_loc,end_loc])
    tripPoints = np.ascontiguousarray(np.array(tripPoints,dtype=np.long),dtype=np.long)
    tripDeliveryIDs.append(new['deliv_id'])
    tripOrderTimes.append(new['order_time'])

    bestComboVars = tripPoints,tripStartTime,tripStartPt,tripDeliveryIDs,tripOrderTimes
    return bestComboVars
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

    c_check2(order_q_i,order_results,new,full_order_q_i)

    # Fourth:
    new_order_q_i = order_q_re_order_deliv_num(full_order_q_i)
    check_order_q_i = new_order_q_i.append(order_q_i[order_q_i.end_time<=now]).sort_index(by='start_time',ascending=True).reset_index(drop=True)
    if errorCheck == True: error_check(order_q_i=check_order_q_i,dg_q_i=None,arg3='sim_data')

    check_dg_q_i = pull_from_order(check_order_q_i,errorCheck=False) # false here because it would duplicate part of the above check
    new_dg_q_i = check_dg_q_i[check_dg_q_i['ptb-t']>now]

    return new_order_q_i,new_dg_q_i

def format_new_to_order(new,order_q):
    A = order_q.ix[:-1,:]
    cols = ['deliv_id','order_time','start_X','start_Y','end_X','end_Y']
    B = A.append(pd.Series({'deliv_id':new[4],
                                'order_time':new[5],
                                'start_X':new[6],
                                'start_Y':new[7],
                                'end_X':new[8],
                                'end_Y':new[9]},
                               index=cols),ignore_index=True).fillna(0)
    return B

def c_check4(new,order_q_i,check_order_result=''):

    c_new = np.ascontiguousarray(new.astype(long).tolist(),dtype=np.long)
    c_order_q_i = np.ascontiguousarray(order_q_i.drop(['status','ave_X','ave_Y'],axis=1).astype(long).as_matrix(),dtype=np.long)
    d = len(order_q_i[order_q_i.end_time>new['order_time']])+1
    int_vars = np.asarray([d,travel_speed,max_delivery_time,max_travelToLocTime],dtype=np.long)
    c_delivery_count,c_speed,c_max_delivery_time,c_mttlt = int_vars[0],int_vars[1],int_vars[2],int_vars[3]

    c_tripPoints = np.ascontiguousarray(np.empty((d*2,2), dtype=np.long,order='C'), dtype=np.long)
    c_deliv_ids = np.ascontiguousarray(np.empty((d,), dtype=np.long,order='C'), dtype=np.long)
    c_order_times = np.ascontiguousarray(np.empty((d,), dtype=np.long,order='C'), dtype=np.long)
    c_returnVar = np.ascontiguousarray(np.empty((d,14), dtype=np.long,order='C'), dtype=np.long)

    if d < max_delivery_per_dg: testSet = orderSet[orderSet['mc'+str(d)]==True].reset_index(drop=True)
    else: testSet = orderSet

    c_orderSortKey = np.ascontiguousarray(testSet.ix[:,'i0':'i'+str(d-1)].astype(long).as_matrix(),dtype=np.long)
    c_ptsSortKey = np.ascontiguousarray(testSet.ix[:,'a1':ABC[d-1].lower()+'2'].astype(long).as_matrix(),dtype=np.long)
    points = testSet.ix[:,'pt0':'pt'+str(d*2-1)]
    c_mockCombos = np.ascontiguousarray(points.astype(long).as_matrix(),dtype=np.long)
    r,c = c_mockCombos.shape
    c_realCombos = np.empty((r,c,2),dtype=np.long,order='C')

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
def c_check3(new,order_q_i,tripStartPtX,tripStartPtY,tripStartTime,check_order_results=''):
    c_new = np.ascontiguousarray(new.astype(long).tolist(),dtype=np.long)
    c_order_q_i = np.ascontiguousarray(order_q_i.drop(['status','ave_X','ave_Y'],axis=1).astype(long).as_matrix(),dtype=np.long)
    c_tripStartPtX = long(tripStartPtX)
    c_tripStartPtY = long(tripStartPtY)
    c_tripStartTime = long(tripStartTime)
    c_speed = long(travel_speed)
    c_max_delivery_time = long(max_delivery_time)
    r = len(order_q_i[order_q_i.end_time>new['order_time']])+1 # how is this being set?
    print 'check c_check3'
    systemError()
    c_returnVar = np.ascontiguousarray(np.empty((r,14), dtype=np.long,order='C'), dtype=np.long)

    c_order_result = c_eval_single_order(c_new,c_order_q_i,c_tripStartPtX,c_tripStartPtY,
                                   c_tripStartTime,c_speed,c_max_delivery_time,c_returnVar)
    new_order_result = pd.DataFrame(np.asarray(c_order_result).T,columns=order_q_i.columns)
    if str(check_order_result) == '': return new_order_result
    else: return compare_orders(check_order_results,new_order_result,order_q_i)
def c_check2(order_q_i,order_results,new,check_order_results=''):
    now = new['order_time']
    c_order_q_i = np.ascontiguousarray(order_q_i.drop(['status','ave_X','ave_Y'],axis=1).astype(long).as_matrix(),dtype=np.long)
    c_order_results = np.ascontiguousarray(order_results.astype(long).as_matrix(),dtype=np.long)
    c_now = long(now)
    c_order_results = c_update_order_results(c_order_q_i,c_order_results,c_now)
    new_order_results = pd.DataFrame(np.asarray(c_order_results),columns=order_results.columns)
    if str(check_order_results) == '': return new_order_results
    else: return compare_orders(check_order_results,new_order_results,order_q_i)
def c_check1(new,order_q_i,bestComboVars=''):
    #from get_combo_start_info import c_get_combo_start_info

    c_new = np.ascontiguousarray(new.astype(long).tolist(),dtype=np.long)
    c_order_q_i = np.ascontiguousarray(order_q_i.drop(['status','ave_X','ave_Y'],axis=1).astype(long).as_matrix(),dtype=np.long)
    r = len(order_q_i[new['order_time']<order_q_i.end_time])
    c_returnVar = np.ascontiguousarray(np.empty((r+1,9), dtype=np.long,order='C'), dtype=np.long)

    c_returnVar = c_get_combo_start_info(c_new,c_order_q_i,c_returnVar)

    if c_returnVar[0][5] == -1:
        print '\nonly single order'
        tripStartTime,tripStartPt = new['order_time'],[new['start_X'],new['start_Y']]
        bestComboVars = 1,tripStartTime,tripStartPt,None,None
        return bestComboVars
    C = np.asarray(c_returnVar)
    c_tripStartTime = C[0][0]
    c_tripStartPt = C[0][1:3].astype(np.int64).tolist()
    a = C.T[3].astype(np.int64).tolist()+C.T[5].astype(np.int64).tolist()
    b = C.T[4].astype(np.int64).tolist()+C.T[6].astype(np.int64).tolist()
    c_tripPoints = np.ascontiguousarray(map(list,zip(a,b)),dtype=np.long)
    c_tripDeliveryIDs = C.T[7].astype(np.int64).tolist()
    c_tripOrderTimes = C.T[8].astype(np.int64).tolist()
    c_bestComboVars = c_tripPoints,c_tripStartTime,c_tripStartPt,c_tripDeliveryIDs,c_tripOrderTimes
    if bestComboVars == '': return c_bestComboVars
    tripPoints,tripStartTime,tripStartPt,tripDeliveryIDs,tripOrderTimes = bestComboVars

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

def bestExpeditedDeliveryRoute(order_q_i,new,errorCheck=True):
    # pull information from data for computation
    bestComboVars = getComboStartInfo(new,order_q_i)
    c_check1(new,order_q_i,bestComboVars)
    tripPoints,tripStartTime,tripStartPt,tripDeliveryIDs,tripOrderTimes = bestComboVars
    if str(tripPoints) == '1':
        print 'single order mated\n'
        var_group = order_q_i,new,[new['start_X'],new['start_Y']],[new['end_X'],new['end_Y']]
        order_results,dg_q_results = eval_additional_order(tripStartPt,tripStartTime,var_group,errorCheck=errorCheck)
        c_check3(new,order_q_i,tripStartPt[0],tripStartPt[1],tripStartTime,order_results)
        return order_results,dg_q_results # returns None,None if that is the case

    # prepare variables for using c++, i.e., contiguous memory for using memoryviews & type == long (a.k.a., int64)
    order_times = np.ascontiguousarray(tripOrderTimes,dtype=np.long)
    deliv_ids = np.ascontiguousarray(tripDeliveryIDs,dtype=np.long)
    int_vars = np.asarray([tripPoints.shape[0]*.5,tripStartTime,travel_speed,max_delivery_time,max_travelToLocTime],dtype=np.long)
    c_delivery_count,c_tripStartTime,c_travel_speed,c_max_delivery_time,c_max_travelToLocTime = int_vars[0],int_vars[1],int_vars[2],int_vars[3],int_vars[4]
    get_combo_vars = long(tripStartPt[0]),long(tripStartPt[1]),c_tripStartTime,order_times,c_travel_speed,c_max_delivery_time,c_max_travelToLocTime,c_delivery_count,deliv_ids,tripPoints

    if c_delivery_count < max_delivery_per_dg: testSet=orderSet[orderSet['mc'+str(c_delivery_count)]==True].reset_index(drop=True)
    else: testSet=orderSet

    # split processes here for parallel processing
    test,parallel=False,False
    if c_delivery_count<4 or parallel==False:
        test_pt=len(testSet.index)
        c_global_vars_reduced = (c_travel_times[:test_pt],c_start_times[:test_pt],c_end_times[:test_pt],c_odtTimes[:test_pt],
                                 c_oMaxTimes[:test_pt],c_tMaxTimes[:test_pt],c_tddTimes[:test_pt],c_ctMarker[:test_pt],
                                 c_returnVars[:c_delivery_count])
        # if order_q_i.dg_id.astype(np.int64).values[0]==6 and new['deliv_id']==1772: test=True
        order_results = get_best_combo(testSet,get_combo_vars,c_global_vars_reduced,test,parallel)
    # TODO: may need another level of parallel processing for evaluating orders (as opposed to combos here)
    else: order_results = run_parallel()

    if type(order_results) == NoneType: return None,None
    else:
        final_order_q_i,final_dg_q_i = updateOrderResults(order_q_i,new,order_results,errorCheck)
        return final_order_q_i,final_dg_q_i
def set_dg_pool_order(globalVars,new):
    order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
    model_dg_pool_grp = pd.DataFrame(columns=['id', 'dg_node', 'total_delivered', 'current_deliveries','travel_time','totalTime'])

    # constant variables:

    singleTripTime = pg_get_travel_time(new['start_node'],new['end_node'])
    # 1) ineligible per conditions
    # 2) each DG that has not started making deliveries yet or has finished with deliveries --> sorted by total_delivered
    # 3) each DG already making deliveries
    maxed_out_dg = dg_pool[(dg_pool.current_deliveries>=max_delivery_per_dg)]
    potentialDG = dg_pool.ix[dg_pool.index - maxed_out_dg.index,:]

    cost_tbl = pg_get_travel_dist(new['start_node'],potentialDG.dg_node.tolist())

    target_cost_dict = dict(zip(cost_tbl.target.tolist(),cost_tbl.cost.tolist()))
    potentialDG['travel_dist'] = potentialDG.dg_node.map(target_cost_dict)
    potentialDG['travel_time'] = potentialDG.travel_dist * MPH

    startingDG = potentialDG[(potentialDG.current_deliveries==0)]
    working_DG =  potentialDG.ix[potentialDG.index - maxed_out_dg.index - startingDG.index,:]

    # unusedDG = dg_pool.ix[dg_pool.index - maxed_out_dg.index - startingDG.index - working_DG.index,:]
    # if len(unusedDG.index)!=0:
    #     print '\nUn-Used DG in DG Pool\n',unusedDG
    #     systemError()


    # 2) each DG that has not started making deliveries yet or has finished with deliveries --> sorted by total_delivered
    if len(startingDG.index)!=0:
        startingDG['totalTime'] = startingDG['travel_time'] + singleTripTime
        startingDG['closeby'] = startingDG.travel_time.map(lambda s: True if s<=max_travelToLocTime else False) # i.e., within proximity condition
        startingDG['timely'] = startingDG.totalTime.map(lambda s: True if s<=max_delivery_time else False) # i.e., within delivery time condition
        dropCols = ['closeby','timely','travel_dist']
        avail_startingDG = startingDG[(startingDG.timely==True) & (startingDG.closeby==True)].drop(dropCols,axis=1)
        avail_startingDG = avail_startingDG.sort_index(by=['total_delivered','travel_time'], ascending=[False,True]).reset_index(drop=True)
    else: avail_startingDG = model_dg_pool_grp.ix[:-1,:]

    # 3) each DG already making deliveries
    if len(working_DG.index)!=0:
        working_DG['totalTime'] = working_DG['travel_time'] + singleTripTime
        working_DG['closeby'] = working_DG.travel_time.map(lambda s: True if s<=max_travelToLocTime else False) # i.e., within proximity condition
        working_DG['timely'] = working_DG.totalTime.map(lambda s: True if s<=max_delivery_time else False) # i.e., within delivery time condition
        dropCols = ['closeby','timely','travel_dist']
        avail_working_DG = working_DG[(working_DG.timely==True) & (working_DG.closeby==True)].drop(dropCols,axis=1)
        avail_working_DG = avail_working_DG.sort_index(by=['total_delivered','current_deliveries','travel_time'], ascending=[False,False,True]).reset_index(drop=True)
    else: avail_working_DG = model_dg_pool_grp.ix[:-1,:]


    if len(avail_working_DG.index)+len(avail_startingDG.index)==0: return [],None,'re-pool'
    elif len(avail_working_DG.index)==0: return [],avail_startingDG.ix[:0,:],'OK'
    else:  # note:  DG_pool_grp_part_size taken from global defined in Assumptions
        dg_groups = []
        dg_pool_parts = int(round(len(avail_working_DG.index)/float(DG_pool_grp_part_size)))
        if dg_pool_parts==0: dg_groups.append(avail_working_DG)
        else:
            for i in range(0,dg_pool_parts):
                if i==(dg_pool_parts-1): dg_groups.append(avail_working_DG.ix[i*DG_pool_grp_part_size:,:].reset_index(drop=True))
                else: dg_groups.append(avail_working_DG.ix[i*DG_pool_grp_part_size:((i+1)*DG_pool_grp_part_size)-1,:].reset_index(drop=True))
        free_dg = avail_startingDG.ix[:0,:]
        # avail_grps = avail_working_DG.groupby(by='current_deliveries')
        # grp_list = avail_grps.groups.keys()
        # tmp_dg_groups = [avail_grps.get_group(it).sort_index(by=['total_delivered','travel_time'], ascending=[False,True]).reset_index(drop=True) for it in grp_list]
        # dg_groups = []
        # for it in tmp_dg_groups:
        #     dg_pool_parts = int(round(len(it.index)/float(DG_pool_grp_part_size)))
        #     if dg_pool_parts==0: dg_groups.append(it)
        #     else:
        #         for i in range(0,dg_pool_parts):
        #             if i==(dg_pool_parts-1): dg_groups.append(it.ix[i*DG_pool_grp_part_size:,:].reset_index(drop=True))
        #             else: dg_groups.append(it.ix[i*DG_pool_grp_part_size:((i+1)*DG_pool_grp_part_size)-1,:].reset_index(drop=True))
        # dg_groups.append(avail_startingDG.ix[:0,:])

    return dg_groups,free_dg,'OK'
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
def set_dg_pool_grp_order(globalVars,newOrders):
    order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
    model_dg_pool_grp = pd.DataFrame(columns=['id', 'dg_X', 'dg_Y', 'total_delivered', 'current_deliveries','travel_time','totalTime'])
    dg_pool = dg_pool.sort_index(by='id',ascending=True)

    dgp_grp_indicies = []
    for i in range(0,len(newOrders)):
        new = newOrders.ix[i,:]
        # constant variables:
        singleTripTime = pd_get_travel_time(new['start_X'],new['start_Y'],new['end_X'],new['end_Y'])
        # 1) ineligible per conditions
        # 2) each DG that has not started making deliveries yet or has finished with deliveries --> sorted by total_delivered
        # 3) each DG already making deliveries
        maxed_out_dg = dg_pool[(dg_pool.current_deliveries>=max_delivery_per_dg)]
        startingDG = dg_pool[(dg_pool.current_deliveries==0)]
        working_DG =  dg_pool.ix[dg_pool.index - maxed_out_dg.index - startingDG.index,:]

        # 2) each DG that has not started making deliveries yet or has finished with deliveries --> sorted by total_delivered
        if len(startingDG.index)!=0:
            startingDG['travel_time']=startingDG[['dg_X','dg_Y']].apply(lambda s: pd_get_travel_time(new['start_X'],new['start_Y'],*s),axis=1)
            startingDG['totalTime'] = startingDG['travel_time'] + singleTripTime
            startingDG['closeby'] = startingDG.travel_time.map(lambda s: True if s<=max_travelToLocTime else False) # i.e., within proximity condition
            startingDG['timely'] = startingDG.totalTime.map(lambda s: True if s<=max_delivery_time else False) # i.e., within delivery time condition
            dropCols = ['closeby','timely']
            avail_startingDG = startingDG[(startingDG.timely==True) & (startingDG.closeby==True)].drop(dropCols,axis=1)
            avail_startingDG = avail_startingDG.sort_index(by=['total_delivered','travel_time'], ascending=[False,True])
        else: avail_startingDG = model_dg_pool_grp.ix[:-1,:]

        # 3) each DG already making deliveries
        if len(working_DG.index)!=0:
            working_DG['travel_time']=working_DG[['dg_X','dg_Y']].apply(lambda s: pd_get_travel_time(new['start_X'],new['start_Y'],*s),axis=1)
            working_DG['totalTime'] = working_DG['travel_time'] + singleTripTime
            working_DG['closeby'] = working_DG.travel_time.map(lambda s: True if s<=max_travelToLocTime else False) # i.e., within proximity condition
            working_DG['timely'] = working_DG.totalTime.map(lambda s: True if s<=max_delivery_time else False) # i.e., within delivery time condition
            dropCols = ['closeby','timely']
            avail_working_DG = working_DG[(working_DG.timely==True) & (working_DG.closeby==True)].drop(dropCols,axis=1)
            avail_working_DG = avail_working_DG.sort_index(by=['total_delivered','current_deliveries','travel_time'], ascending=[False,False,True])
        else: avail_working_DG = model_dg_pool_grp.ix[:-1,:]

        dgp_grp,dgp_cnt = [],[]

        if len(avail_working_DG.index)+len(avail_startingDG.index)==0:

            globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
            # set re-pool size here, use newSubVar as variable for number of new DG
            globalVars = update_global_vars(globalVars,'re-pool',newAddVar=False,newSubVar=False,replaceVar={})
            dg_pool = globalVars[4]

            startingDG = dg_pool[(dg_pool.current_deliveries==0)]
            startingDG['travel_time']=startingDG[['dg_X','dg_Y']].apply(lambda s: pd_get_travel_time(new['start_X'],new['start_Y'],*s),axis=1)
            startingDG['totalTime'] = startingDG['travel_time'] + singleTripTime
            startingDG['closeby'] = startingDG.travel_time.map(lambda s: True if s<=max_travelToLocTime else False) # i.e., within proximity condition
            startingDG['timely'] = startingDG.totalTime.map(lambda s: True if s<=max_delivery_time else False) # i.e., within delivery time condition
            dropCols = ['closeby','timely']
            avail_startingDG = startingDG[(startingDG.timely==True) & (startingDG.closeby==True)].drop(dropCols,axis=1)
            avail_startingDG = avail_startingDG.sort_index(by=['total_delivered','travel_time'], ascending=[False,True])

            dgp_cnt.append( avail_startingDG.index[0] )

        elif len(avail_working_DG.index)==0:

            dgp_cnt.append( avail_startingDG.index[0] )

        else:  # note:  DG_pool_grp_part_size taken from global defined in Assumptions

            dgp_cnt.append( avail_startingDG.index[0] )

            dg_pool_parts = int(round(len(avail_working_DG.index)/float(DG_pool_grp_part_size)))
            if dg_pool_parts==0:
                single_grp = avail_working_DG.index
                dgp_cnt.append(len(single_grp))
                dgp_grp.append( single_grp )

            else:
                for i in range(0,dg_pool_parts):

                    if i==(dg_pool_parts-1):
                        grp = avail_working_DG.ix[i*DG_pool_grp_part_size:,:].index
                        dgp_cnt.append(len(grp))
                        dgp_grp.append( grp )

                    else:
                        grp = avail_working_DG.ix[i*DG_pool_grp_part_size:((i+1)*DG_pool_grp_part_size)-1,:].index
                        dgp_cnt.append(len(grp))
                        dgp_grp.append( grp )

        dgp_grp_indicies.append([dgp_cnt,dgp_grp])
            # avail_grps = avail_working_DG.groupby(by='current_deliveries')
            # grp_list = avail_grps.groups.keys()
            # tmp_dg_groups = [avail_grps.get_group(it).sort_index(by=['total_delivered','travel_time'], ascending=[False,True]).reset_index(drop=True) for it in grp_list]
            # dg_groups = []
            # for it in tmp_dg_groups:
            #     dg_pool_parts = int(round(len(it.index)/float(DG_pool_grp_part_size)))
            #     if dg_pool_parts==0: dg_groups.append(it)
            #     else:
            #         for i in range(0,dg_pool_parts):
            #             if i==(dg_pool_parts-1): dg_groups.append(it.ix[i*DG_pool_grp_part_size:,:].reset_index(drop=True))
            #             else: dg_groups.append(it.ix[i*DG_pool_grp_part_size:((i+1)*DG_pool_grp_part_size)-1,:].reset_index(drop=True))
            # dg_groups.append(avail_startingDG.ix[:0,:])

    # this function returns a 3D list.
    # for each order,
    #   the first list starts with the index of the free DG and then
    #       provides the count for each of the subsequent groups
    #   the second list is the index of the first group
    #   the third list is the index for the second group
    #   etc...

    globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
    return globalVars, dgp_grp_indicies

def getBestDG_grp_old(globalVars,grp,new):
    order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
    D = order_delivered
    updated = False
    best_order_results,best_dg_q_results,bestDG = None,None,None
    now = new['order_time']
    for i in range(0,len(grp.index)):
        dg_from_pool = grp.ix[i:i,:]
        dg_ID = dg_from_pool['id'].astype(np.int64).values[0]
        order_q_i = order_q[order_q.id==dg_ID]
        earliestStart = order_q_i.start_time.astype(np.int64).min()
        order_q_i = order_q_i.append(D[(D.id==dg_ID) & (D.end_time>earliestStart)]).sort_index(by='start_time',ascending=True).reset_index(drop=True)

        if len(order_q_i.index)==0:
            # if a viable result is not already found, pick best from pool (easy, no real calc.)
            # if already found a viable result, then go with the viable result
            # if updated==False:
            #     new_dg_id = dg_ID
            #     order_q_i = pd.merge(dg_from_pool.drop(['total_delivered','current_deliveries','travel_time','totalTime'],axis=1),order_q.ix[:-1,:],how='left')
            #     # TODO: review whether dg_pool calc.s make it to new_dg_to_order_q
            #     new_order_result,new_dg_result = new_dg_to_order_q(new,order_q_i,errorCheck=errorCheck)
            # else: new_order_result,new_dg_result,new_dg_id = best_order_results,best_dg_q_results,bestDG
            # globalVars = update_global_vars(globalVars,'update per order',new_order_result,new_dg_result,replaceVar={'id':new_dg_id})
            # return globalVars
            print 'check getBestDG_grp_old'
            systemError()

        else:

            order_q_i.ix[:,['dg_X','dg_Y']] = dg_from_pool[['dg_X','dg_Y']].values
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

def c_check5(globalVars,grp,new,checkOrder='',errorCheck=True):
    order_q = globalVars[0]
    D = globalVars[1]
    dg_pool = globalVars[4]

    grp_ids = grp.dg_id.unique().tolist()  # the order of IDs is important

    order_q_grp = order_q.ix[:-1,:]
    dg_pool_grp = dg_pool.ix[:-1,:]
    for it in grp_ids:
        order_q_grp = order_q_grp.append(order_q[(order_q.deliv_id==it)].sort_index(by='start_time',ascending=True))
        dg_pool_grp = dg_pool_grp.append(dg_pool[(dg_pool.dg_id==it)])
    # order_q_grp.dg_X = order_q_grp.id.map(lambda s: dg_pool[dg_pool.dg_id==s].ix[:,'dg_X'].values[0])
    # order_q_grp.dg_Y = order_q_grp.id.map(lambda s: dg_pool[dg_pool.dg_id==s].ix[:,'dg_Y'].values[0])
    # order_q_grp = order_q_grp.reset_index(drop=True)

    # print '\nGroup:\n',grp
    # print '\nDeliveryID =',new['deliv_id'],'- Group IDs =',grp_ids
    # print '\norders being considered\n',order_q_grp.append(format_new_to_order(new,order_q))

    # new[['deliv_id','order_time','start_time','start_node','travel_time','end_node','end_time','total_order_time']].astype(np.long)
    # c_new = np.ascontiguousarray(new.astype(np.long).tolist(),dtype=np.long)
    c_new = np.ascontiguousarray(new[['deliv_id','order_time','start_node','end_node']].astype(np.long))
    c_grp = np.ascontiguousarray(order_q_grp.drop(['status'],axis=1).reset_index(drop=True).astype(np.long).as_matrix(),dtype=np.long)
    c_grp_ids = np.ascontiguousarray(grp_ids,dtype=np.long)
    c_dgp = np.ascontiguousarray(dg_pool_grp.astype(np.long).as_matrix(),dtype=np.long)
    # dg_pool_grp = dg_pool[(dg_pool.dg_id.isin(grp_ids)==True)]
    max_return_rows = dg_pool_grp.current_deliveries.max() + 1
    c_returnVars = np.ascontiguousarray(np.empty((max_return_rows,15), dtype=np.long,order='C'))

    c_vars = c_getBestDG( c_new,
                          c_grp,
                          c_grp_ids,
                          c_dgp,
                          c_deliv_ids,
                          c_order_times,
                          c_speed,
                          c_max_delivery_time,
                          c_max_delivery_per_dg,
                          c_mttlt,
                          c_tripPoints,
                          c_orderSet2,
                          c_orderSet3,
                          c_orderSet4,
                          c_orderSet5,
                          c_orderSetInd,
                          c_realCombos,
                          c_travel_times,
                          c_start_times,
                          c_end_times,
                          c_odtTimes,
                          c_oMaxTimes,
                          c_tMaxTimes,
                          c_tddTimes,
                          c_ctMarker,
                          c_rv_comboStartInfo,
                          c_rv_bestCombo,
                          c_rv_updatedBestCombo,
                          c_returnVars)

    #----------------------------------------------------------------------------
    #----------------------------------------------------------------------------

    # a = np.asarray(c_vars)
    # print a,'\n'
    # for i in range(0,a.shape[0]):
    #     b=a[i].astype(np.int64).tolist()
    #     print b[9],b
    # if a.shape[1]==15:
    #     # "oq" format
    #     c = pd.DataFrame(a,columns=['id','dg_X','dg_Y','deliv_num','travel_time_to_loc','deliv_id','order_time',
    #                                     'start_X','start_Y','start_time','end_time','end_X','end_Y','total_order_time',
    #                                     'travel_time'])
    #     # "o_res" format
    #     # c = pd.DataFrame(a,columns=['dg_X','dg_Y','deliv_num','deliv_id','order_time','travel_time_to_loc','start_X',
    #     #                                 'start_Y','start_time','travel_time','end_time','end_X','end_Y','total_order_time',
    #     #                                 'bestIndex'])
    #     # c.columns = ['dg_X','dg_Y','deliv_num','travel_time_to_loc','deliv_id','order_time',
    #     #              'start_X','start_Y','start_time','end_time','end_X','end_Y','total_order_time',
    #     #              'travel_time','bestIndex']
    #     print c
    #     if type(checkOrder) != str:
    #         compare_orders(checkOrder,c)
    #         print '\nCompare Orders -- PASSED\n'
    # raise SystemError()

    #----------------------------------------------------------------------------
    #----------------------------------------------------------------------------

    if c_vars[0][13] != 0:
        order_q_i = pd.DataFrame(np.asarray(c_vars),columns=['id','dg_X','dg_Y','deliv_num','travel_time_to_loc',
                                                                    'deliv_id','order_time','start_X','start_Y',
                                                                    'start_time','end_time','end_X','end_Y',
                                                                    'total_order_time','travel_time'])
        order_q_i['ave_X'] = np.nan
        order_q_i['ave_Y'] = order_q_i.ave_X.map(lambda s: s)
        order_q_i['status'] = order_q_i.ave_X.map(lambda s: 'on deck')
        c=['id','dg_X','dg_Y','ave_X','ave_Y','status','deliv_num','travel_time_to_loc','deliv_id','order_time',
           'start_X','start_Y','start_time','end_time','end_X','end_Y','total_order_time','travel_time']
        order_q_i = order_q_i.ix[:,c]
        if type(checkOrder) != str and type(checkOrder) != NoneType:
            compare_orders(checkOrder,order_q_i)
        DG_ID = order_q_i.dg_id.tolist()[0]
        earliestStart = order_q_grp.start_time.astype(np.int64).min()
        check_order_q_i = order_q_i.append(D[(D.id==DG_ID) & (D.end_time>earliestStart)])
        dg_q_i = pull_from_order(check_order_q_i,errorCheck=errorCheck)
        updated = True
        return updated,order_q_i,dg_q_i
    else:
        updated = False
        return updated,None,None


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

    remaining_deliv_ids = order_q_ret[order_q_ret.deliv_num==950].deliv_id.astype(np.int64).tolist()
    order_q_ret = order_q_ret[(order_q_ret.deliv_num!=0) & (order_q_ret.deliv_id.isin(remaining_deliv_ids)==False)]
    b = order_q_ret.astype(np.int64).as_matrix()
    order_q_ret['ave_X'] = np.nan
    order_q_ret['ave_Y'] = order_q_ret.ave_X.map(lambda s: s)
    order_q_ret['status'] = order_q_ret.ave_X.map(lambda s: 'on deck')
    c = ['id','dg_X','dg_Y','ave_X','ave_Y','status','deliv_num','travel_time_to_loc','deliv_id','order_time',
           'start_X','start_Y','start_time','end_time','end_X','end_Y','total_order_time','travel_time']
    order_q_ret = order_q_ret.ix[:,c]

    return order_q_ret,b,remaining_deliv_ids

# @profile
def order_by_min(globalVars,ordersNow,errorCheck=True):

    def getDG_q_i_from_oq_ret(ordersNow,order_q_ret,added_orders,order_delivered,dg_q):
        now = ordersNow.order_time.astype(np.int64).values[0]
        d = order_delivered
        changedDG_ids = added_orders.id.unique().tolist()
        for it in changedDG_ids:
            # append nothing if all prior orders completed else append all
            startMin = order_q_ret[order_q_ret.id==it].order_time.values.min()
            # f = d.ix[:-1,:] if len(d[(d.id==it) & ((d.end_time>now) | (d.end_time>startMin))])==0 else d[d.id==it]
            f = d[(d.id==it) & ((d.end_time>now) | (d.end_time>startMin))]
            check_order_q_i = order_q_ret[order_q_ret.id==it].append(f)
            check_dg_q_i = pull_from_order(check_order_q_i,errorCheck=False)
            # TODO: need to re-activate errorCheck for this
            new_dg_q_i = check_dg_q_i[check_dg_q_i['ptb-t']>now]
            dg_q = dg_q[dg_q.dg_id!=it].append(new_dg_q_i)
        return dg_q

    stop,loop_i=False,0
    last_loop_i,last_remaining_orders_cnt = -2,-2
    while stop==False:
        loop_i += 1
        # print 'Number of Orders =',len(ordersNow)
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
        order_q = order_q.sort('vend_id')
        # print len(dg_pool[(dg_pool.total_delivered==0) & (dg_pool.current_deliveries==0)]),' unused DG'
        # print dg_pool[dg_pool['current_deliveries']!=0]

        ## FIND
        # TODO: use
        vend_dims = sim_data.vend_X.min(),sim_data.vend_X.max(),sim_data.vend_Y.min(),sim_data.vend_Y.max()
        # for i in np.arange(vend_dims[0],vend_dims[1],max_travelToLocTime)

        ncols = round((vend_dims[1] - vend_dims[0])/max_travelToLocTime)+1
        x_spread = round((vend_dims[1] - vend_dims[0])/ncols)
        x_units = np.arange(vend_dims[0],vend_dims[1]+1,x_spread)

        nrows = round((vend_dims[3] - vend_dims[2])/max_travelToLocTime)+1
        y_spread = round((vend_dims[3] - vend_dims[2])/nrows)
        y_units = np.arange(vend_dims[2],vend_dims[3]+1,y_spread)


        dgp_geo_units = np.empty((x_units.shape[0],y_units.shape[0], 2))
        dgpNew = dg_pool[(dg_pool.current_deliveries==0)&(dg_pool.total_delivered>0)]
        pt=0
        for i in range(1,x_units.shape[0]):
            mid_x = round(x_units[i]-x_units[i-1]/2.0)

            for j in range(1,y_units.shape[0]):
                mid_y = round(y_units[j]-y_units[j-1]/2.0)

                dgp_geo_units[i-1,j-1,1] = mid_x
                dgp_geo_units[i-1,j-1,0] = mid_y

                dgpNew[str(pt)] = dgpNew.ix[:,['dg_X','dg_Y']].apply(lambda s: pd_get_travel_time(mid_x,mid_y,*s),axis=1)
                pt += 1

        # dgpNew.ix[:,[str(i) for i in range(pt)]].apply(lambda s: pd_min_of_list(*s),axis=1)

        dgpNew['shortestDist'] = dgpNew.ix[:,[str(i) for i in range(pt)]].apply(lambda s: pd_min_of_list(*s),axis=1)

        dgpNew['closestCtr'] = 0
        for i in range(1,pt):
            # dgpNew.ix[:,['shortestDist',str(i)]].apply
            # D.head().ix[:,['closestCtrPt','shortestDist',str(i)]].apply(lambda it: pd_index_of_list(*it),axis=1)
            # dgpNew['check'] = i if dgpNew.ix[:,str(i)]==dgpNew.ix[:,'shortestCtr'] else False
            # dgpNew['closestCtr'] = dgpNew.closestCtr
            # dgpNew['closestCtr'] = dgpNew.ix[:,[str(i) for i in range(pt)]].apply(lambda s: pd_min_of_list(*s),axis=1)
            dgpNew['closestCtr'] = dgpNew.ix[:,[str(i),'shortestDist','closestCtr']].apply(lambda s: i if s[0]==s[1] else s[2],axis=1)
        print dgpNew


        ctr_pts = [ dgpNew.closestCtr.astype(np.int64).tolist().count(i) for i in range(pt) ]
        ctr_pt_dict = dict(zip(range(pt),ctr_pts))
        ctr_pts_sorted = sorted(ctr_pts)
        ctr_pt_sorted_dict = dict(zip(range(pt),ctr_pts_sorted))
        l=zip(ctr_pts,range(pt))
        ctr_pt_inds = [it[1] for it in sorted(l)]

        pt2=0
        for i in range(dgp_geo_units.shape[0]-1):
            # mid_x = round(x_units[i]-x_units[i-1]/2.0)


            for j in range(dgp_geo_units.shape[1]-1):
                # mid_y = round(y_units[j]-y_units[j-1]/2.0)
                mid_x = dgp_geo_units[i,j,0]
                mid_y = dgp_geo_units[i,j,1]# = mid_y

                it = ctr_pt_inds[pt2]

                dg_grp_num = sum(ctr_pts)/len(ctr_pts) - ctr_pts[it]
                pt2 += 1

                chg_dg_grp = dgpNew.sort_index(by=str(it),ascending=[True]).reset_index(drop=True).ix[:dg_grp_num,:]
                a=0

                # chg_dg_grp.ix[:,['dg_X','dg_Y','']

                # def getInfo(*items):


        for it in ctr_pt_inds:
            dg_grp_num = sum(ctr_pts)/len(ctr_pts) - ctr_pts[it]
            chg_dg_grp = dgpNew.sort_index(by=str(it),ascending=[True]).reset_index(drop=True).ix[:dg_grp_num,:]
            # what is the next position for each DG as moving toward
            # dgp_geo_units[]
        n=0
        ct_pts[3]
        for i in range(len(ctr_pts_sorted)):
            dg_grp_num = sum(ctr_pts)/len(ctr_pts) - ctr_pts[it]
            if dg_grp_num > len(remaining_dg): dg_grp_num = remaining_dg









        dg_total = dg_pool.current_deliveries.values + dg_pool.total_delivered.values
        if dg_total.sum() != len(order_q) + len(order_delivered):
            print 'dg_total.sum() != len(order_q)'
            systemError()
        elif dg_pool.current_deliveries.max()>5:
            max_val = dg_pool.current_deliveries.max()
            print dg_pool[dg_pool.current_deliveries==max_val]
            print 'too many deliveries'
            systemError()

        newOrderIDs = ordersNow.deliv_id.astype(np.int64).tolist()
        c_newOrders = np.ascontiguousarray(ordersNow.astype(np.long).as_matrix(),dtype=np.long)
        clean_order_q = order_q.drop(['status','ave_X','ave_Y'],axis=1).sort_index(by=['id','start_time'],ascending=[True,True]).reset_index(drop=True).astype(np.long).as_matrix()
        d = len(ordersNow)
        z = np.zeros((d,clean_order_q.shape[1]), dtype=np.long,order='C')
        c_order_q_a = np.ascontiguousarray(clean_order_q.tolist() + z.tolist(),dtype=np.long)
        c_order_q_b = np.ascontiguousarray(np.zeros(c_order_q_a.shape, dtype=np.long,order='C'))
        c_reorder_q = np.ascontiguousarray(np.zeros((c_order_q_a.shape[0],), dtype=np.long,order='C'))
        # c_dg_seg_size = np.long(len(c_order_q_a)/float(Assumption('DG_pool_grp_part_size')))
        c_dg_seg_size = np.long(Assumption('DG_pool_grp_part_size'))
        # print order_q
        # print dg_pool
        c_dgp_a = np.ascontiguousarray(dg_pool.astype(np.long).as_matrix(),dtype=np.long)
        c_dgp_b = np.ascontiguousarray(np.zeros(c_dgp_a.shape, dtype=np.long,order='C'))

        ret_order_q = c_order_by_min(c_order_q_a,
                                c_order_q_b,
                                c_reorder_q,
                                c_dgp_a,
                                c_dgp_b,
                                c_dg_seg_size,
                                c_newOrders,
                                c_deliv_ids,
                                c_order_times,
                                c_speed,
                                c_max_delivery_time,
                                c_max_delivery_per_dg,
                                c_mttlt,
                                c_tripPoints,
                                c_orderSet2,
                                c_orderSet3,
                                c_orderSet4,
                                c_orderSet5,
                                c_orderSetInd,
                                c_realCombos,
                                c_travel_times,
                                c_start_times,
                                c_end_times,
                                c_odtTimes,
                                c_oMaxTimes,
                                c_tMaxTimes,
                                c_tddTimes,
                                c_ctMarker,
                                c_rv_comboStartInfo,
                                c_rv_bestCombo,
                                c_rv_updatedBestCombo,
                                c_bestDG)

        # import pstats, cProfile
        #
        # cProfile.runctx('c_order_by_min(c_order_q_a,'+
        #                         'c_order_q_b,'+
        #                         'c_reorder_q,'+
        #                         'c_dgp_a,'+
        #                         'c_dgp_b,'+
        #                         'c_dg_seg_size,'+
        #                         'c_newOrders,'+
        #                         'c_deliv_ids,'+
        #                         'c_order_times,'+
        #                         'c_speed,'+
        #                         'c_max_delivery_time,'+
        #                         'c_max_delivery_per_dg,'+
        #                         'c_mttlt,'+
        #                         'c_tripPoints,'+
        #                         'c_orderSet2,'+
        #                         'c_orderSet3,'+
        #                         'c_orderSet4,'+
        #                         'c_orderSet5,'+
        #                         'c_orderSetInd,'+
        #                         'c_realCombos,'+
        #                         'c_travel_times,'+
        #                         'c_start_times,'+
        #                         'c_end_times,'+
        #                         'c_odtTimes,'+
        #                         'c_oMaxTimes,'+
        #                         'c_tMaxTimes,'+
        #                         'c_tddTimes,'+
        #                         'c_ctMarker,'+
        #                         'c_rv_comboStartInfo,'+
        #                         'c_rv_bestCombo,'+
        #                         'c_rv_updatedBestCombo,'+
        #                         'c_bestDG)')#, globals(), locals(), "seamless.py.prof")

        # cProfile.runctx("calc_pi.approx_pi()", globals(), locals(), "Profile.prof")

        # s = pstats.Stats("Profile.prof")
        # s.strip_dirs().sort_stats("time").print_stats()
        #
        # print '\n\n'
        # print s
        # TODO: need to fix distribution of vendors/deliveries
        # print np.asarray(ret_order_q)
        # systemError()
        order_q_ret,a,remaining_order_ids = receive_c_order_by_min(ret_order_q,showVar=False)
        order_q_ind = order_q_ret.index.tolist()
        # systemError()
        # if order_q_ret.deliv_id.tolist().count(4037) != 0:
        #     print 'found order'
        #     systemError()
        endPt = len(order_q_ind) - 1
        if len(remaining_order_ids) != 0:   # a[endPt][0]==950 and a[endPt][3]==950:
            re_pool = True
            order_q_ret = order_q_ret.ix[order_q_ind[:-1],:]  # remove last row...
            # systemError()
        elif a[endPt][0]==450 and a[endPt][3]==450:
            print 'need to account for deliveryCount == 1 (which is not ever expected)'
            systemError()
        elif a[endPt][0]==555 and a[endPt][3]==555:
            print order_q_ret#[(order_q_ret.id==139) | (order_q_ret.id==555)]
            # from cython_scratch import test
            # x=test(c_orderSet4,c_orderSetInd,c_tripPoints[:8],c_realCombos)
            # print x
            a=0
            systemError()
        else: re_pool = False

        added_orders = order_q_ret[order_q_ret.deliv_id.isin(newOrderIDs)==True]
        added_deliv_ids = added_orders.deliv_id.astype(np.int64).tolist()
        completed_orders = ordersNow[(ordersNow.deliv_id.isin(added_deliv_ids)==True)]
        remaining_orders = ordersNow.ix[ordersNow.index - completed_orders.index,:]

        if len(remaining_orders)==0: re_pool = False
        else:
            re_pool = True
            ordersNow = remaining_orders

        order_q = order_q.append(added_orders).sort_index(by='id').reset_index(drop=True)
        # TODO: move down back into re-pool option only b/c this is repetitive of "update per min"
        # update location for DG without orders
        # vend_dims = sim_data.vend_X.min(),sim_data.vend_X.max(),sim_data.vend_Y.min(),sim_data.vend_Y.max()
        # # for i in np.arange(vend_dims[0],vend_dims[1],max_travelToLocTime)
        # x_units = np.arange(A[0],A[1]+max_travelToLocTime,max_travelToLocTime)
        # y_units = np.arange(A[2],A[3]+max_travelToLocTime,max_travelToLocTime)
        # dgp_geo_units = np.empty(((x.shape[0]-1), (y.shape[0]-1)))
        # pt=0
        # for i in range(1,x_units.shape[0]):
        #     mid_x = round(x_units[i]-x_units[i-1]/2.0)
        #
        #     for j in range(1,y_units.shape[0]):
        #         mid_y = round(y_units[j]-y_units[j-1]/2.0)
        #
        #         dg_pool[str(pt)] = dg_pool.ix[:,['dg_X','dg_Y']].apply(lambda s: pd_get_travel_time(mid_x,mid_y,*s),axis=0).apply(lambda s: pd_combine(*s),axis=0)


        width = vend_dims[1]-vend_dims[0]
        height = vend_dims[3]-vend_dims[2]
        x_units,y_units = round(max_travelToLocTime/float(width)),round(max_travelToLocTime/float(height))
        dx = round(width/x_units)
        dy = round(height/y_units)
        a = np.empty(np.array((x_units,y_units)))
        for i in range(x_units):
            for j in range(y_units):
                a[i,j] = [( dx*(i+1) - dx*i ),( dy*(j+1) - dy*j )]

        # update dg_pool (if there was a specific order, it will be maintained)
        updatedDG_ids = added_orders.id.astype(np.int64).unique().tolist()
        updatedDG = dg_pool[dg_pool.dg_id.isin(updatedDG_ids)==True]
        updatedDG.current_deliveries = updatedDG.current_deliveries.values + 1
        globalVars = update_global_vars(globalVars,'update dg_pool',newAddVar=updatedDG,newSubVar=False,replaceVar={'id':updatedDG_ids})
        dg_pool = globalVars[4]
        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
        globalVars = update_global_vars(globalVars,'organize dg_pool',newAddVar=False,newSubVar=False,replaceVar={})
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars


        # print '\n1. total dg_pool - used dg - order_q - order_q (old) - ordersNow(old) - ordersDone - ordersRemaining'
        print len(dg_pool),len(dg_pool[(dg_pool.current_deliveries!=0) | (dg_pool.total_delivered!=0)]),len(order_q),len(globalVars[0]),c_newOrders.shape[0],len(completed_orders),len(remaining_orders)

        # error check included in next function
        dg_q = getDG_q_i_from_oq_ret(ordersNow,order_q_ret,added_orders,order_delivered,dg_q)

        if re_pool == False:
            break       # dg_pool order will be set on the "per order" basis
        else:
            # re-pool
            globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
            repool_size = len(remaining_order_ids)*3
            # set re-pool size here, use newSubVar as variable for number of new DG
            globalVars = update_global_vars(globalVars,'re-pool',newAddVar=False,newSubVar=repool_size,replaceVar={})
            globalVars = update_global_vars(globalVars,'organize dg_pool',newAddVar=False,newSubVar=False,replaceVar={})
            order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
            a=0
            # print '\n2. dg_pool - order_q - ordersNow - ordersDone - ordersRemaining\n',len(dg_pool),len(globalVars[0]),len(ordersNow),len(completed_orders),len(remaining_orders)

        if last_loop_i+1==loop_i and last_remaining_orders_cnt==len(remaining_orders):
            print 'order_by_min caught in loop'
            print remaining_orders
            print dg_pool
            systemError()
        else:
            last_loop_i = loop_i
            last_remaining_orders_cnt = len(remaining_orders)


    # # compare with results from previous method
    # for j in range(0,4):#len(ordersNow)):
    #     thisOrder=ordersNow.iloc[j,:].copy()
    #     thisOrder['deliv_id'] = ordersNow.index[j]
    #     globalVars = getBestDG(globalVars,thisOrder,errorCheck=errorCheck)
    # order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
    # print '\n'
    # print order_q
    # orderDG_a = sorted(order_q.id.astype(np.int64).unique().tolist())
    # orderDG_b = sorted(order_q_ret.id.astype(np.int64).unique().tolist())
    # if orderDG_a != orderDG_b:
    #     print 'different DGs for orders'
    #     systemError()
    # else:
    #     for it in orderDG_a:
    #         orderA = order_q[order_q.id==it]
    #         orderB = order_q_ret[order_q_ret.id==it]
            # compare_orders(orderA,orderB)
    order_q = order_q.reset_index(drop=True)
    globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
    return globalVars

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
            set_dg_groups,status = set_dg_pool_order(globalVars,new)

        # print '---',new['deliv_id'],'---'
        pt=-1
        for grp in set_dg_groups:
            pt+=1
            # print 'set #',pt,'\n'
            # print new['deliv_id']
            # print grp
            # updated,best_order_results,best_dg_q_results = getBestDG_grp_old(globalVars,grp,new)
            # c_updated,c_best_order_results,c_best_dg_q_results = c_check5(globalVars,grp,new,checkOrder=best_order_results)

            updated,best_order_results,best_dg_q_results = c_check5(globalVars,grp,new,errorCheck=errorCheck)

            # if updated != c_updated:
            #     print pt,new['deliv_id']
            #     systemError()


            if updated == True:
                bestDG = best_order_results.id.astype(np.int64).tolist()[0]
                globalVars = update_global_vars(globalVars,'update per order',best_order_results,best_dg_q_results,replaceVar={'id':bestDG})
                return globalVars

        if updated == False:
            if len(free_dg) != 0:
                dg_ID = free_dg['dg_id'].astype(np.int64).values[0]
                new_dg_id = dg_ID
                order_q_i = pd.merge(free_dg.drop(['total_delivered','current_deliveries','travel_time','totalTime'],axis=1),order_q.ix[:-1,:],how='left')
                # TODO: review whether dg_pool calc.s make it to new_dg_to_order_q
                new_order_result,new_dg_result = new_dg_to_order_q(new,order_q_i,errorCheck=errorCheck)
                globalVars = update_global_vars(globalVars,'update per order',new_order_result,new_dg_result,replaceVar={'id':new_dg_id})
                return globalVars
            else:
                order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
                globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
                # set re-pool size here, use newSubVar as variable for number of new DG
                globalVars = update_global_vars(globalVars,'re-pool',newAddVar=False,newSubVar=False,replaceVar={})
                order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

            # TODO: add feature to watch for excessively un-used portions of dg_pool

        # end of while loop

def update_global_vars(globalVars,varName,newAddVar=False,newSubVar=False,replaceVar={}): # replaceVar={'id':10}
    order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

    def updatePerOrder(globalVars,newAddVar,newSubVar,replaceVar): # single dg_id
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars
        order_addition,dg_q_addition = newAddVar,newSubVar
        dg_ID = replaceVar.values()[0]
        # replace order_q_i
        order_q = pd.merge(order_q[order_q['dg_id']!=dg_ID],order_addition,how='outer')
        order_q = order_q.reset_index(drop=True)
        # replace dg_q_i
        dg_q = pd.merge(dg_q[dg_q['dg_id']!=dg_ID],dg_q_addition,how='outer')
        dg_q = dg_q.reset_index(drop=True)
        # update dg_pool
        static_dg_pool = dg_pool[dg_pool['dg_id']!=dg_ID]
        dynamic_dg_pool = dg_pool[dg_pool['dg_id']==dg_ID]

        order_id_group = order_addition.groupby(by='dg_id')

        dynamic_dg_pool['current_deliveries'] = dynamic_dg_pool.dg_id.map(lambda s: order_id_group.get_group(s).deliv_num.max())
        dg_pool = pd.merge(static_dg_pool,dynamic_dg_pool,how='outer').astype(np.int64).reset_index(drop=True)
        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
        return globalVars
    def update_dg_pool(globalVars):
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

        order_grouped = order_q.groupby(by='dg_id')
        groupList = order_grouped.groups.keys()

        # update dg_pool.current_deliveries (if in order_q, updating currentDeliv)
        stat_dg_pool = dg_pool[dg_pool.dg_id.isin(groupList)==False]
        dyn_dg_pool = dg_pool.ix[dg_pool.index - stat_dg_pool.index]
        dyn_dg_pool.current_deliveries = dyn_dg_pool.dg_id.map(lambda s: len(order_grouped.get_group(s))).values
        dg_pool = pd.merge(stat_dg_pool,dyn_dg_pool,how='outer')

        # update dg_pool.current_deliveries (not in order_q, setting currentDeliv = 0)
        dyn_dg_pool = dg_pool[(dg_pool.dg_id.isin(groupList)==False) & (dg_pool.current_deliveries != 0)]
        if len(dyn_dg_pool) != 0:
            stat_dg_pool = dg_pool.ix[dg_pool.index.tolist() - dyn_dg_pool.index.tolist(),:]
            dyn_dg_pool.current_deliveries = 0
            dg_pool = pd.merge(stat_dg_pool,dyn_dg_pool,how='outer')

        # update dg_pool.total_delivered
        delivered_grouped = order_delivered.groupby(by='dg_id')
        groupList = delivered_grouped.groups.keys()
        stat_dg_pool = dg_pool[dg_pool.dg_id.isin(groupList)==False]
        dyn_dg_pool = dg_pool.ix[dg_pool.index - stat_dg_pool.index]
        dyn_dg_pool.total_delivered = dyn_dg_pool.dg_id.map(lambda s: len(delivered_grouped.get_group(s)))
        dg_pool = pd.merge(stat_dg_pool,dyn_dg_pool,how='outer')

        # DG Sort Order:
        # 1. all DG with totalDelivs != 0 (grouped least to most currentDelivs+total_delivered)
        # 2. remaining DG with zero totalDelivs

        dg_pool['total'] = dg_pool['current_deliveries'] + dg_pool['total_delivered']
        dg_pool = dg_pool[dg_pool.total!=0].sort_index(by=['total','total_delivered'],ascending=[True,True]).append(dg_pool[dg_pool.total==0].sort_index(by='total',ascending=True)).drop(['total'],axis=1).reset_index(drop=True)

        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
        return globalVars
    def updatePerMinute(globalVars,now):
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

        # check for orders completed at t=now, if any
        full_completedOrders=order_q[order_q.end_time <= now]
        clean_completedOrders=full_completedOrders[full_completedOrders.status!='on route']
        orders_dg_ids = clean_completedOrders.deliv_id.unique().tolist()
        # orders_del_ids = clean_completedOrders.deliv_id.unique().tolist()
        # df = pd.DataFrame({'orders':orders_del_ids})
        # df['ids'] = df.orders.map(lambda s: clean_completedOrders[clean_completedOrders.deliv_id==s].id.astype(np.int64).tolist()[0])
        # order_del_dg_dict = dict(zip(df.orders.astype(np.int64).values,df.ids.astype(np.int64).values))

        # update location for all DG
        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
        globalVars = updateCurrentLocation(globalVars,now,orders_dg_ids)
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

        # update --> dg_pool (current_deliveries, total_delivered)
        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
        globalVars = update_dg_pool(globalVars)
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

        # nothing (else) to update
        if len(clean_completedOrders.index) == 0: return globalVars

        # check for errors
        # check_orders = clean_completedOrders
        if errorCheck == True: error_check(order_q_i=clean_completedOrders,dg_q_i=None,arg3='sim_data')

        # update --> order delivered and order_q
        order_delivered = pd.merge(order_delivered,full_completedOrders,how='outer').sort_index(by=['id','start_time'], ascending=[True,True]).reset_index(drop=True)
        order_q = order_q.ix[order_q.index - full_completedOrders.index,:].sort_index(by=['id','start_time'], ascending=[True,True]).reset_index(drop=True)

        # update --> dg_q delivered
        deliveries_completed = dg_q[dg_q['ptb-t']<=now]
        dg_delivered = pd.merge(dg_delivered,deliveries_completed,how='outer').reset_index(drop=True)

        # update --> dg_q
        dg_q = dg_q[dg_q['ptb-t']>now]

        globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
        return globalVars

    if varName == 'update per order':
        globalVars = updatePerOrder(globalVars,newAddVar,newSubVar,replaceVar)
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

    elif varName == 'update per minute':
        globalVars = updatePerMinute(globalVars,newAddVar)
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

    elif varName == 're-pool':
        dg_pool_pt+=1
        if type(newSubVar)!=False: repool_size = newSubVar
        else: repool_size = Assumption('DG_pool_grp_size')
        dg_pool = init_dg_pool(pt=dg_pool_pt,dg_grp_size=repool_size,old_dg_pool=dg_pool,load=reuse_dg_pool,save=False,filePath='')
        print 'new dg_pool = ',dg_pool_pt

    elif varName == 'update dg_pool':
        VarKey,oldVarValue = replaceVar.keys()[0],replaceVar.values()[0]
        if type(oldVarValue) == list:  dg_pool = pd.merge(dg_pool[(dg_pool[VarKey].isin(oldVarValue)==False)],newAddVar,how='outer')
        else:  dg_pool = pd.merge(dg_pool[dg_pool[VarKey]!=oldVarValue],newAddVar,how='outer')
        dg_pool = dg_pool.reset_index(drop=True)

    elif varName == 'organize dg_pool':
        globalVars = update_dg_pool(globalVars)
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

    else:
        print 'why not accounted for in updating?'
        systemError()

    if dg_pool.dg_node.fillna(99).tolist().count(99)!=0:
        print 'hold up - check your global vars'
        systemError()

    globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt
    return globalVars
def global_simulation_vars(assumptions=None):
    # getGlobalAssumptions = Assumption('')
    global ABC,mock_to_num_dict,num_to_mock_dict,ind_to_mock_dict,mock_to_ind_dict,num_to_ind_dict,ind_to_num_dict
    ABC='ABCDEFGHIJKLMNOPQRUSTUVXYZ'
    max_delivery_per_dg = Assumption('max_delivery_per_dg')
    ## create dict for total number of possible mock points, e.g., A1:A2,B1:B2,etc...
    mock_to_num_dict=dict(zip([it+'1' for it in ABC[:max_delivery_per_dg]],np.arange(0,(len(ABC)+1),1).astype(np.long)))
    mock_to_num_dict.update(dict(zip([it+'2' for it in ABC[:max_delivery_per_dg]],np.arange(100,100*(len(ABC)+1),1).astype(np.long))))
    num_to_mock_dict = {v:k for k,v in mock_to_num_dict.iteritems()}
    a=[]
    w=[a.extend([it+'1',it+'2']) for it in ABC[:max_delivery_per_dg]]
    ## create maps to quickly interchange between attributes
    ind_to_mock_dict = dict(zip(range(0,len(a)),a))
    mock_to_ind_dict = {v:k for k,v in ind_to_mock_dict.iteritems()}
    w=[mock_to_num_dict[it] for it in a]
    ind_to_num_dict = dict(zip(range(0,max_delivery_per_dg*2),w))
    num_to_ind_dict = {v:k for k,v in ind_to_num_dict.iteritems()}

    # MAKE AND GET COMBINATION DATA # TODO: global_simulation_vars: check perms
    # gen_good_perms(5,6)
    # make_pairSet_store()
    # make_orderSet_store()
    global orderSet,pairSet

    orderSet=pd.read_hdf(this_cwd+'perm_data/store_orderSet.h5', 'table')
    pairSet=pd.read_hdf(this_cwd+'perm_data/store_pairSet.h5', 'table')
    # print orderSet.ix[:10,'i0':]
    # systemError()

    # MAKE AND GET TRANSACTIONAL ARRAYS
    global c_orderSet,c_realCombos
    r = len(orderSet.index)
    pts = max_delivery_per_dg*2
    d = max_delivery_per_dg
    c_realCombos = np.empty((r,pts,2),dtype=np.long,order='C')
    ordSortCols = ['mc2','mc3','mc4','mc5']
    orderSet = orderSet.sort_index(by=ordSortCols,ascending=[True,True,True,True])
    c_orderSet = np.ascontiguousarray(orderSet.astype(long).as_matrix(),dtype=np.long)

    global c_mc_ranges,c_orderSK_range,c_pointSK_range,c_points_range
    global c_orderSet2,c_orderSet3,c_orderSet4,c_orderSet5,c_orderSetInd
    ordCols = orderSet.columns.tolist()
    orderSetInd = []
    mc_ranges,orderSK_range,pointSK_range,points_range = [],[],[],[]
    for i in range(2,6):
        rowPts = []
        # rowPts.append(ordCols.index('mc'+str(i)))
        rowPts.append(ordCols.index('pt0'))
        rowPts.append(ordCols.index('pt0')+(2*i))
        rowPts.append(ordCols.index('i0'))
        rowPts.append(ordCols.index('i'+str(i-1))+1)
        rowPts.append(ordCols.index('a1'))
        rowPts.append(ordCols.index('a1')+(2*i))
        orderSetInd.append(rowPts)
        indList = np.array(orderSet[orderSet['mc'+str(i)]==True].index.astype(long),dtype=np.long)
        # indList = orderSet[orderSet['mc'+str(i)]==True].index.astype(long).tolist()
        mc_ranges.append(indList)
        # if i <= max_delivery_per_dg: orderSK_range.append(np.array(range(ordCols.index('i0'),ordCols.index('i'+str(i-1))),dtype=np.long))
        # pointSK_range.append(np.array(range(ordCols.index('a1'),ordCols.index('a1')+(2*i)-1),dtype=np.long))
        # points_range.append(np.array(range(ordCols.index('pt0'),ordCols.index('pt0')+(2*i)-1),dtype=np.long))
    # c_mc_ranges = mc_ranges
    # c_mc_ranges = np.ascontiguousarray(mc_ranges)#,dtype=np.long)
    # c_mc_range2 = np.ascontiguousarray(mc_ranges[0],dtype=np.long)
    # c_mc_range3 = np.ascontiguousarray(mc_ranges[1],dtype=np.long)
    # c_mc_range4 = np.ascontiguousarray(mc_ranges[2],dtype=np.long)
    # c_mc_range5 = np.ascontiguousarray(mc_ranges[3],dtype=np.long)
    c_orderSet2 = np.ascontiguousarray(orderSet.ix[mc_ranges[0],:].astype(long).as_matrix(),dtype=np.long)
    c_orderSet3 = np.ascontiguousarray(orderSet.ix[mc_ranges[1],:].astype(long).as_matrix(),dtype=np.long)
    c_orderSet4 = np.ascontiguousarray(orderSet.ix[mc_ranges[2],:].astype(long).as_matrix(),dtype=np.long)
    c_orderSet5 = np.ascontiguousarray(orderSet.ix[mc_ranges[3],:].astype(long).as_matrix(),dtype=np.long)
    c_orderSetInd = np.ascontiguousarray(orderSetInd,dtype=np.long)
    # c_orderSK_range = np.ascontiguousarray(orderSK_range,dtype=np.long)
    # c_pointSK_range = np.ascontiguousarray(pointSK_range,dtype=np.long)
    # c_points_range = np.ascontiguousarray(points_range,dtype=np.long)

    global c_speed,c_max_delivery_time,c_mttlt,c_max_delivery_per_dg
    int_vars = np.asarray([travel_speed,max_delivery_time,max_travelToLocTime,max_delivery_per_dg],dtype=np.long)
    c_speed,c_max_delivery_time,c_mttlt,c_max_delivery_per_dg = int_vars[0],int_vars[1],int_vars[2],int_vars[3]

    global c_tripPoints,c_deliv_ids,c_order_times,c_rv_comboStartInfo,c_rv_bestCombo,c_bestDG
    c_tripPoints = np.ascontiguousarray(np.empty((pts,2), dtype=np.long,order='C'), dtype=np.long)
    c_deliv_ids = np.ascontiguousarray(np.empty((d,), dtype=np.long,order='C'), dtype=np.long)
    c_order_times = np.ascontiguousarray(np.empty((d,), dtype=np.long,order='C'), dtype=np.long)
    c_rv_comboStartInfo = np.ascontiguousarray(np.zeros((d,14), dtype=np.long,order='C'), dtype=np.long)
    c_rv_bestCombo = np.ascontiguousarray(np.zeros((d,15), dtype=np.long,order='C'), dtype=np.long)
    c_bestDG = np.ascontiguousarray(np.empty((d,15), dtype=np.long, order='C'), dtype=np.long)

    global c_travel_times,c_start_times,c_end_times,c_odtTimes,c_oMaxTimes,c_tMaxTimes,c_tddTimes,c_ctMarker,c_rv_updatedBestCombo,c_returnVars
    c_travel_times = np.ascontiguousarray(np.empty((r,pts), dtype=np.long,order='C'))
    c_start_times = np.ascontiguousarray(np.empty((r,d), dtype=np.long,order='C'))
    c_end_times = np.ascontiguousarray(np.empty((r,d), dtype=np.long,order='C'))
    c_odtTimes = np.ascontiguousarray(np.empty((r,d), dtype=np.long,order='C'))
    c_tddTimes = np.ascontiguousarray(np.empty((r,d), dtype=np.long,order='C'))
    c_oMaxTimes = np.ascontiguousarray(np.zeros(r, dtype=np.long,order='C'))
    c_tMaxTimes = np.ascontiguousarray(np.zeros(r, dtype=np.long,order='C'))
    c_ctMarker = np.ascontiguousarray(np.zeros(r, dtype=np.long,order='C'))
    c_rv_updatedBestCombo = np.ascontiguousarray(np.empty((d,15), dtype=np.long,order='C'))
    c_returnVars = np.ascontiguousarray(np.empty((d,15), dtype=np.long,order='C'))

def make_orderSet_store():
    # TODO: before adding all ordered pairs, need to verify accuracy/completeness (especially first set of data)
    dropCols=[]
    ptCols=['pt'+str(it) for it in range(0,max_delivery_per_dg*2)]
    pts=pd.DataFrame(genOrderedPairPerm(max_delivery_per_dg),columns=ptCols)
    for it in ptCols: pts[it] = pts[it].map(mock_to_num_dict)
    pts['mc'+str(max_delivery_per_dg)]=pts.apply(lambda x: True, axis=1)
    pts['mockComboMax']=pts[ptCols].apply(lambda x: [pd_combine(*x)], axis=1).ix[:,0]
    pts['mockComboMax']=pts['mockComboMax'].map(lambda s: eval(s))

    for i in np.arange(max_delivery_per_dg-1,1,-1):
        ptsCols=['pt'+str(it) for it in range(0,i*2)]
        ptsTemp=pd.DataFrame(np.array(genOrderedPairPerm(i)),columns=ptsCols)
        for it in ptsCols:
            ptsTemp[it] = ptsTemp[it].map(mock_to_num_dict)
        ptsTemp['mc']= ptsTemp.apply(lambda x: str(pd_combine(*x)), axis=1)
        pts['temp']= pts[ptsCols].apply(lambda x: str(pd_combine(*x)), axis=1)
        pts['isdupe']= pts.duplicated(['temp'])
        pts['mc'+str(i)]=pts.temp.where(pts.temp.isin(ptsTemp.mc)).where(pts.isdupe == False).apply(lambda s: True if type(s)==str else False)

    dropCols.extend(['temp','isdupe'])
    for it in ABC[:max_delivery_per_dg]:
        pts[it.lower()+'1']=pts['mockComboMax'].apply(lambda x: x.index(mock_to_num_dict[it+'1']))
        pts[it.lower()+'2']=pts['mockComboMax'].apply(lambda x: x.index(mock_to_num_dict[it+'2']))
    dropCols.extend(['mockComboMax'])
    cols=[]
    x=[cols.extend([ABC[n].lower()+'1']) for n in range(0,max_delivery_per_dg)]
    pts['sortKey']=pts[cols].apply(lambda s: [pd_combine(*s)],axis=1).ix[:,0]
    pts['sortKey']=pts['sortKey'].map(lambda s: eval(s)).map(pd_create_sortKey)
    for i in range(0,max_delivery_per_dg):
        pts['i'+str(i)]=pts['sortKey'].map(lambda s: s[i])
    dropCols.append('sortKey')
    pts=pts.drop(dropCols,axis=1)
    pts.to_hdf(this_cwd+'/perm_data/store_orderSet.h5','table')#,append=True)
def make_pairSet_store():
    max_delivery_per_dg = Assumption('max_delivery_per_dg')
    dictPairs=pd.DataFrame(genAllPairPerm_NoRep(max_delivery_per_dg,2),columns=['a','b'])
    for it in ['a','b']:
        dictPairs[it] = dictPairs[it].map(mock_to_num_dict)
    dictPairs['mc'+str(max_delivery_per_dg)]=dictPairs.a.map(lambda s: True)

    for i in np.arange(max_delivery_per_dg-1,1,-1):
        pairsTemp=pd.DataFrame(np.array(genAllPairPerm_NoRep(i,2)),columns=['a','b'])
        for it in ['a','b']:
            pairsTemp[it] = pairsTemp[it].map(mock_to_num_dict)
        pairsTemp['mc']=pairsTemp.apply(lambda x: str(pd_combine(*x)), axis=1)
        dictPairs['temp']=dictPairs[['a','b']].apply(lambda x: str(pd_combine(*x)), axis=1)
        dictPairs['mc'+str(i)]=dictPairs.temp.where(dictPairs.temp.isin(pairsTemp.mc)).map(lambda s: True if type(s) == str else False)
        # a=dictPairs.where(dictPairs.temp.isin(pairsTemp.mc)).apply(lambda s: [pd_combine(*x)] if type(s) == list else False)
        # dictPairs['mc'+str(i)]=dictPairs['mc'+str(i)].map(lambda s: True if s == True else False)

    dictPairs=dictPairs.drop('temp',axis=1)
    dictPairs.to_hdf(this_cwd+'/perm_data/store_pairSet.h5','table',append=False)

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
        x_tick_num = np.arange(odf.xloc.astype(np.int64).min(),odf.xloc.astype(np.int64).max()+1,3)
        y_tick_num = np.arange(odf.yloc.astype(np.int64).min(),odf.yloc.astype(np.int64).max()+1,1)
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
        x_max,y_max = odf.xloc.astype(np.int64).max(),odf.yloc.astype(np.int64).max()
        x_min,y_min = odf.xloc.astype(np.int64).min(),odf.yloc.astype(np.int64).min()
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
    x=np.array(graphData.x.values,dtype=np.float)
    y=np.array(graphData.y.values,dtype=np.float)
    # x=np.array(realdata.long.values,dtype=np.float)
    # y=np.array(realdata.lat.values,dtype=np.float)
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
        x_tick_num = np.arange(odf.xloc.astype(np.int64).min(),odf.xloc.astype(np.int64).max()+1,3)
        y_tick_num = np.arange(odf.yloc.astype(np.int64).min(),odf.yloc.astype(np.int64).max()+1,1)
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
        x_max,y_max = odf.xloc.astype(np.int64).max(),odf.yloc.astype(np.int64).max()
        x_min,y_min = odf.xloc.astype(np.int64).min(),odf.yloc.astype(np.int64).min()
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
    total_max_dg_used = df.max_dg_used.astype(np.int64).max()
    df['total_hours'] = 0
    for it in range(total_max_dg_used):
        df['total_hours'] += df.vendors.map(lambda s: vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it].end_time.max() - vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it].start_time.min()).fillna(0).values
        df['total_hours'] += df.vendors.map(lambda s: vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it].sort('start_time').return_travel_time.astype(np.int64).values[-1] if len(vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it])!=0 else 0).fillna(0).values


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
    total_dg_used_normal = ndf.max_dg_used.astype(np.int64).sum()
    total_max_dg_used = ndf.max_dg_used.astype(np.int64).max()
    ndf['total_hours'] = 0
    for it in range(total_max_dg_used):
        ndf['total_hours'] += ndf.vendors.map(lambda s: vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it].end_time.max() - vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it].start_time.min()).fillna(0).values
        ndf['total_hours'] += ndf.vendors.map(lambda s: vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it].sort('start_time').return_travel_time.astype(np.int64).values[-1] if len(vend_grps.get_group(s)[vend_grps.get_group(s).dg_id==it])!=0 else 0).fillna(0).values
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

    deliveryCounts = df['DeliveryCount'].astype(np.int64).values.tolist()
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
    odf['allDeliveryLocs'] = odf.del_id.map(lambda s: OD[OD.deliv_id==s].reset_index(drop=True).ix[0,['end_X','end_Y']].astype(np.int64).tolist())
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
    # ldf = pd.DataFrame({'locations': np.unique(OD[['start_X','start_Y']].astype(np.int64).as_matrix())})
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

def RUN_NORMAL_DELIVERY_SIMULATION(makeData=False,showSimData=False):
    sim_data_Path=this_cwd+'/sim_data/vendor_sim_data.txt'
    if makeData==True: sim_data = make_simulation_data(savePath=sim_data_Path)
    else: sim_data = pd.read_hdf(sim_data_Path.rstrip('.txt')+'.h5', 'table')
    sim_data = sim_data.sort_index(by=['order_time','vend_Y','vend_X'], ascending=[True,True,True])
    if showSimData==True: DISPLAY_SIMULATION_DATA()
    getGlobalAssumptions = Assumption('')
    NormalDelivery(sim_data)

def init_global_vars(load,save,resume):
    from classes import Vendor,Delivery,DG

    if resume==False:
        dg_head = DG().toDict().keys()
        order_q = pd.DataFrame(columns=dg_head)
        order_delivered = pd.DataFrame(columns=dg_head)
        dg_pool_pt = 0
        dg_pool = init_dg_pool(pt=dg_pool_pt,old_dg_pool=None,load=load,save=save,filePath='')
        dg_q = pd.DataFrame(columns=['dg_id','pta','ptb','pta-t','ptb-t','deliv_id','mock_pt'])
        dg_delivered = pd.DataFrame(columns=dg_q.columns)
        program_stats = pd.DataFrame(columns=['order_minute','order_count','average_time_per_order','running_epoch'])
        stpt=0

    else:
        globalVars_plus = get_saved_global_vars()
        order_q,order_delivered,dg_q,dg_delivered,dg_pool,program_stats = globalVars_plus
        try:
            if int(order_delivered.order_time.max())+1 == Assumption('vend_hours_delivering')*60:
                print '\nSimulation is completed.\n',Assumption('vend_hours_delivering')*60,'minutes simulated.\n'
                return None
            else: stpt = int(order_q.order_time.max().astype(np.int64)+1)
        except:
            # stpt = int(order_q.order_time.max().astype(np.int64)+1)
            stpt = 0

        dg_pool_pt = int((len(dg_pool.index)/Assumption('DG_pool_grp_size'))-1)

    globalVars_plus = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt,program_stats,stpt
    return globalVars_plus
def export_all_data(globalVars,program_stats=False):
    order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

    pd_EDA_order_q_Path=this_cwd+'/sim_data/EDA_order_q_data.txt'
    order_q=order_q.sort_index(by=['id','order_time','deliv_num'], ascending=[True,True,True])
    order_q.to_csv(pd_EDA_order_q_Path, index=False, header=True, sep='\t')

    pd_EDA_dg_q_Path=this_cwd+'/sim_data/EDA_dg_q_data.txt'
    dg_q=dg_q.sort_index(by='dg_id', ascending=True)
    dg_q.to_csv(pd_EDA_dg_q_Path, index=False, header=True, sep='\t')

    pd_EDA_data_Path=this_cwd+'/sim_data/EDA_dg_pool.txt'
    dg_pool=dg_pool.sort_index(by=['id'], ascending=[True])
    dg_pool.to_csv(pd_EDA_data_Path, index=False, header=True, sep='\t')

    pd_EDA_data_Path=this_cwd+'/sim_data/EDA_order_delivered.txt'
    order_delivered=order_delivered.sort_index(by=['id','order_time','deliv_num'], ascending=[True,True,True])
    order_delivered.to_csv(pd_EDA_data_Path, index=False, header=True, sep='\t')

    pd_EDA_data_Path=this_cwd+'/sim_data/EDA_dg_delivered.txt'
    dg_delivered=dg_delivered.sort_index(by=['dg_id'], ascending=[True])
    dg_delivered.to_csv(pd_EDA_data_Path, index=False, header=True, sep='\t')

    if type(program_stats) != bool:
        program_stats.to_csv(this_cwd+'/sim_data/program_stats.txt', index=False, header=True, sep='\t')
    print 'data exported'
    return True
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
    program_stats.running_epoch = (time() - program_stats.running_epoch.max()) + program_stats.running_epoch
    globalVars_plus = order_q,order_delivered,dg_q,dg_delivered,dg_pool,program_stats
    return globalVars_plus


def Assumption(get_var='',assumptions=None):
    # global work_area,deliv_radius_per_vendor_in_miles,vend_num
    # global vend_hours_delivering,deliveries_per_vend, max_travelToLocTime
    # global DG_num,DG_start_location_in_work_area
    # global travel_speed, wait_at_vendor, max_delivery_time
    # global DG_pool_grp_part_size,max_delivery_per_dg,max_travelToLocTime
    # global totalTime,reuse_dg_pool,avenue_labels

    # avenues_of_vendors,streets_of_vendors=4,10
    # John Tauranac, in the "Manhattan Block by Block" street atlas, gives the average distance between avenues as 750 feet, or about seven avenues to a mile
    # 254 group:
    #   Varick to Ave. C on Houston --> 1.3 mi
    #   44th to Houston on 7th Ave. --> 2.3 mi
    #   1.3 mi. * 7 ave./mi. == avenues_of_vendors
    #   2.3 mi. * 20 st./mi. == streets_of_vendors
    #
    # 17-20 blocks per mile --> 18.5 blocks per mile
    #   1 mile per 18.5 blocks @ 1 block per min --> 1 mile per 18.5 min
    #       60/18.5 = 3.25

    if assumptions==None:
        assumptions = { 'work_area'                         : ['14 st','10 ave','59 st','1 ave'],
                        'deliv_radius_per_vendor_in_miles'  : 2.0, # waist of MN is about 2 miles
                        'deliv_radius_per_vendor_in_km'     : 2.0 * 1.60934,
                        'vend_num'                          : 5,
                        'vend_hours_delivering'             : 1,
                        'deliveries_per_vend'               : [3,8], # range of deliveries
                        'DG_num'                            : 10,
                        'max_travelToStartLocTime'          : 10,
                        'DG_start_location_in_work_area'    : True,
                        'travel_speed'                      : 1.0, # time to walk one street block
                        'MPH'                               : 3.25,
                        'wait_at_vendor'                    : 5,
                        'max_delivery_time'                 : 40
                        }

    for k,v in assumptions.iteritems():
        globals()[k] = v

    # vend_location_grid=avenues_of_vendors,streets_of_vendors
    # vend_deliver_avenues,vend_deliver_streets=6,15 # distance per vendor
    # vend_deliver_radius = vend_deliver_streets/2.0
    # vend_delivery_grid = vend_deliver_avenues,vend_deliver_streets

    rd_conditions = {   'DG_start_location_grid'    : work_area,
                        'DG_pool_grp_part_size'     : 5,
                        'max_delivery_per_dg'       : 5,
                        'max_travelToLocTime'       : 15,
                        'totalTime'                 : vend_hours_delivering*60,
                        'reuse_dg_pool'             : True,
                        'avenue_labels'             : ['11th','10th','9th','8th','7th','6th','5th','Madison',
                                                       'Park','Lexington','3rd','2nd','1st',
                                                       'Ave. A','Ave. B','Ave. C','Ave. D']}

    for k,v in rd_conditions.iteritems():
        globals()[k] = v

    all=dict(assumptions.items() + rd_conditions.items() + { '\n':'\n'}.items())
    if get_var=='all': return all

    # OTHER ASSUMPTIONS APPLIED IN MODELING --
    # (1) vendors will make optimum delivery route based on overall shortest time
    #       (regardless if first order included in route is delivered last)
    #     In other words, vendor will maximize (end_time-start_time),
    #        as opposed to maximizing (end_time-order_time).

    if all.keys().count(get_var)!=0:
        return all[get_var]


def RUN_CHAOS_SIMULATION(assumptions=None,makeData=False,showSimData=False,runNormalDel=False,load=False,save=False,
                         resume=False,errorCheck=False,global_op_vars=False):

    #pass
    # global c_get_best_combo
    # global c_mapper2,c_mapper3,c_mapper4,c_mapper5,c_mapper6,c_mapper7
    # global minimum_relative_distance
    # from get_best_combo import c_get_best_combo
    # from get_combo_start_info import c_get_combo_start_info
    # from map_points_to_combos import c_mapper2,c_mapper3,c_mapper4,c_mapper5,c_mapper6,c_mapper7
    # from math_functions import minimum_relative_distance

    t1A=time()
    print t1A
    if global_op_vars == True:
        global sim_data,order_q,order_delivered,dg_pool,dg_pool_pt,dg_q,dg_delivered
    else: global sim_data
    global_simulation_vars(assumptions)

    sim_data_Path=this_cwd+'/sim_data/vendor_sim_data.txt'
    if makeData==True: sim_data = make_simulation_data_from_real_data(savePath=sim_data_Path)
    else:
        sim_data = pd.read_hdf(sim_data_Path.rstrip('.txt')+'.h5', 'table')
        # sim_data = pd.read_sql_table('sim_data',engine,index_col='deliv_id')
    sim_data = sim_data.sort_index(by=['order_time','vend_id'], ascending=[True,True])

    if showSimData==True: DISPLAY_SIMULATION_DATA()
    if runNormalDel==True: RUN_NORMAL_DELIVERY_SIMULATION(makeData=False,showSimData=False)

    globalVars_plus = init_global_vars(load,save,resume)
    if globalVars_plus==None: return

    order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt,program_stats,stpt = globalVars_plus
    globalVars = order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt

    stpt = 0
    print 'starting at',stpt
    pt=0
    for i in range(stpt,totalTime+1):
        now=i

        # maintain lists of data
        globalVars = update_global_vars(globalVars,'update per minute',now)

        # UPDATE to/from PGSQL HERE

        # export data on a regular basis
        # if pt==1:
        #     pt = 0
        #     if save == True: x = export_all_data(globalVars,program_stats)
        # pt+=1

        # process all current orders
        ordersNow=sim_data[(sim_data.order_time == now)]
        t1=time()

        # globalVars = order_by_min(globalVars,ordersNow,errorCheck=errorCheck)
        # print 'finished'
        # systemError()

        for j in range(0,len(ordersNow.index)):
            thisOrder = ordersNow.iloc[j,:].copy()
            globalVars = getBestDG(globalVars,thisOrder,errorCheck=errorCheck)
        # raise SystemError

        if len(ordersNow.index) != 0:
            program_stats = program_stats.append(pd.Series([i,len(ordersNow.index),round((time()-t1)/len(ordersNow.index),2),round(time())],index=program_stats.columns),ignore_index=True)
            print 'minute'+'\t'+str(i)+'\t'+'orders='+'\t'+str(len(ordersNow.index))+'\t'+str((time()-t1)/len(ordersNow.index))+'\t'+str(time())


    # move remaining orders at close to 'delivered'
    if now == totalTime: globalVars = update_global_vars(globalVars,'update per minute',globalVars[0].end_time.max())
    if save == True: export_all_data(globalVars,program_stats)
    print 'done'
    print time()-t1A
    return

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

"""METHOD:

    1. Identify [x,y] ranges for vendors and expand based on delivery radii --> Xmax,Ymax,Xmin,Ymin
    2. Use monte carlo method to determine radii (as later identified)
      -starting points: max radii == pi*(40**2), min radii == 0
    3. (number of circles) n == (along X) : (Xmax-Xmin)/r,  (along Y) : (Ymax-Ymin)/r
    4. (center points) C == (along X) : 2*n,  (along Y) : 2*(n+1)
    5. All DG[i] start at C[i] and move back to C[i] during downtime.
    6. Start simulation. When an order comes in, check if primary DG for that area can deliver order.
      -this check includes taking last 5 pts of [current route + new delivery] and checking for availability.
      -(the above and other small steps could have significant impacts)
    7. If primary DG unavailable, apply same process for secondary DG, and the tertiary DGs.
    8. If still not available, save as undelivered and move on.
    9. If count of undelivered exceeds 7% of total deliveries -- end simulation.
    10. If end process, redefine radius as midway length between failed and successful radii
    ----
    Use above process to:
        a. find max radii within undeliverable limit
        b. find max radii with 0 undeliverables
        c. randomize vendor and delivery locations & run again until 95% confidence level
"""

""" MODIFICATION TO FIRST IMPLEMENTATION:

    1. save best combo for one less delivery and all other returnVars
    2. save average X/Y for reduced best combo and for outer_delivery
    3. after each distribution, re-distribute and look move orders to DG with better positioning
    4. do step 3 in one iteration, starting with most inconvenient order
"""

if __name__ == '__main__':
    if normal_sim == True: RUN_NORMAL_DELIVERY_SIMULATION()
    if chaos_sim == True: RUN_CHAOS_SIMULATION(assumptions=None,
                                               makeData=makeData,
                                               showSimData=showSimData,
                                               runNormalDel=runNormalDel,
                                               load=load,
                                               save=save,
                                               resume=resume,
                                               errorCheck=errorCheck,
                                               global_op_vars=global_op_vars)
    if show_data_results == True:
        # if normal_sim == True: DISPLAY_NORMAL_DELIVERY_DATA()
        # if chaos_sim == True: DISPLAY_EDA_DATA()
        DISPLAY_EDA_DATA()
        # DISPLAY_NORMAL_DELIVERY_DATA()
        # DISPLAY_SIMULATION_DATA()

    if showRealData==True: DISPLAY_REAL_DATA()

    if show_normal_results==True: DISPLAY_NORMAL_DELIVERY_DATA()

    if lattice_sim == True: RUN_LATTICE_SIMULATION()
