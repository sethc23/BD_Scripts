
import pandas,numpy,pyximport
pyximport.install(build_in_temp=False,inplace=True)
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True
from os import path,listdir,system,getcwd
from sys import path as py_path
py_path.append(getcwd()+'/cython_exts')
from getBestDG import c_getBestDG


def compare_orders(orderA,orderB,order_q_i=''):
    orderA = orderA.sort_index(by='deliveryID',ascending=True)
    orderB = orderB.sort_index(by='deliveryID',ascending=True)
    a = True if orderA.deliveryID.astype(int).tolist()      == orderB.deliveryID.astype(int).tolist() else False
    b = True if orderA.travelTimeToLoc.astype(int).tolist() == orderB.travelTimeToLoc.astype(int).tolist() else False
    c = True if orderA.orderTime.astype(int).tolist()       == orderB.orderTime.astype(int).tolist() else False
    d = True if orderA.start_X.astype(int).tolist()         == orderB.start_X.astype(int).tolist() else False
    e = True if orderA.start_Y.astype(int).tolist()         == orderB.start_Y.astype(int).tolist() else False
    f = True if orderA.startTime.astype(int).tolist()       == orderB.startTime.astype(int).tolist() else False
    g = True if orderA.endTime.astype(int).tolist()         == orderB.endTime.astype(int).tolist() else False
    h = True if orderA.end_X.astype(int).tolist()           == orderB.end_X.astype(int).tolist() else False
    i = True if orderA.end_Y.astype(int).tolist()           == orderB.end_Y.astype(int).tolist() else False
    if [a,b,c,d,e,f,g,h,i].count(False)!=0:
        print 'c_trouble with update orders'
        print [a,b,c,d,e,f,g,h,i]
        if order_q_i != '': print '\nNon-cython results\n',orderA,'\nCython results\n',orderB,'\norder_q_i\n',order_q_i
        else: print '\nNon-cython results\n',orderA,'\nCython results\n',orderB
        raise SystemError
    return
def format_new_to_order(new,order_q):
    A = order_q.ix[:-1,:]
    cols = ['deliveryID','orderTime','start_X','start_Y','end_X','end_Y']
    B = A.append(pandas.Series({'deliveryID':new[4],
                                'orderTime':new[5],
                                'start_X':new[6],
                                'start_Y':new[7],
                                'end_X':new[8],
                                'end_Y':new[9]},
                               index=cols),ignore_index=True).fillna(0)
    return B

def c_check5(globalSimVars,globalVars,grp,new,checkOrder=''):
    order_q = globalVars[0]
    D = globalVars[1]
    dg_pool = globalVars[4]

    (c_deliveryIDs,
      c_orderTimes,
      c_speed,
      c_max_delivery_time,
      c_mttlt,
      c_tripPoints,
      c_orderSet2,
      c_orderSet3,
      c_orderSet4,
      c_orderSet5,
      c_orderSetInd,
      c_realCombos,
      c_travelTimes,
      c_startTimes,
      c_endTimes,
      c_odtTimes,
      c_oMaxTimes,
      c_tMaxTimes,
      c_tddTimes,
      c_ctMarker,
      c_returnVar1,
      c_returnVar2,
      c_returnVars_i) = globalSimVars

    grp_ids = grp.id.unique().tolist()  # the order of IDs is important
    # grp_ids = [8.0, 0.0, 7.0]
    grp_ids = [0.0, 7.0]
    order_q_grp = order_q.ix[:-1,:]
    for it in grp_ids: order_q_grp = order_q_grp.append(order_q[(order_q.id==it)])
    order_q_grp.dg_X = order_q_grp.id.map(lambda s: dg_pool[dg_pool.id==s].ix[:,'dg_X'].values[0])
    order_q_grp.dg_Y = order_q_grp.id.map(lambda s: dg_pool[dg_pool.id==s].ix[:,'dg_Y'].values[0])

    print '\nGroup:\n',grp
    print '\nDeliveryID =',new['deliveryID'],'- Group IDs =',grp_ids
    print '\norders being considered\n',order_q_grp.append(format_new_to_order(new,order_q))

    c_new = numpy.ascontiguousarray(new.astype(numpy.long).tolist(),dtype=numpy.long)
    c_grp = numpy.ascontiguousarray(order_q_grp.drop(['status','ave_X','ave_Y'],axis=1).reset_index(drop=True).astype(numpy.long).as_matrix(),dtype=numpy.long)
    c_grp_ids = numpy.ascontiguousarray(grp_ids,dtype=numpy.long)
    dg_pool_grp = dg_pool[(dg_pool.id.isin(grp_ids)==True)]
    max_return_rows = dg_pool_grp.currentDeliveries.max() + 1
    c_returnVars = numpy.ascontiguousarray(numpy.empty((max_return_rows,15), dtype=numpy.long,order='C'))

    c_vars = c_getBestDG( c_new,
                          c_grp,
                          c_grp_ids,
                          c_deliveryIDs,
                          c_orderTimes,
                          c_speed,
                          c_max_delivery_time,
                          c_mttlt,
                          c_tripPoints,
                          c_orderSet2,
                          c_orderSet3,
                          c_orderSet4,
                          c_orderSet5,
                          c_orderSetInd,
                          c_realCombos,
                          c_travelTimes,
                          c_startTimes,
                          c_endTimes,
                          c_odtTimes,
                          c_oMaxTimes,
                          c_tMaxTimes,
                          c_tddTimes,
                          c_ctMarker,
                          c_returnVar1,
                          c_returnVar2,
                          c_returnVars_i,
                          c_returnVars)

    #----------------------------------------------------------------------------
    #----------------------------------------------------------------------------

    a = numpy.asarray(c_vars)
    print a,'\n'
    for i in range(0,a.shape[0]):
        b=a[i].astype(int).tolist()
        print b[9],b
    if a.shape[1]==15:
        # "oq" format
        # c = pandas.DataFrame(a,columns=['id','dg_X','dg_Y','deliveryNum','travelTimeToLoc','deliveryID','orderTime',
        #                                 'start_X','start_Y','startTime','endTime','end_X','end_Y','totalOrderTime',
        #                                 'travelTime'])
        # "o_res" format
        c = pandas.DataFrame(a,columns=['dg_X','dg_Y','deliveryNum','deliveryID','orderTime','travelTimeToLoc','start_X',
                                        'start_Y','startTime','travelTime','endTime','end_X','end_Y','totalOrderTime',
                                        'bestIndex'])
        # c.columns = ['dg_X','dg_Y','deliveryNum','travelTimeToLoc','deliveryID','orderTime',
        #              'start_X','start_Y','startTime','endTime','end_X','end_Y','totalOrderTime',
        #              'travelTime','bestIndex']
        print c
        if type(checkOrder) != str:
            compare_orders(checkOrder,c)
            print '\nCompare Orders -- PASSED\n'
    raise SystemError()

    #----------------------------------------------------------------------------
    #----------------------------------------------------------------------------

    if c_vars[0][13] != 0:
        order_q_i = pandas.DataFrame(numpy.asarray(c_vars),columns=['id','dg_X','dg_Y','deliveryNum','travelTimeToLoc',
                                                                    'deliveryID','orderTime','start_X','start_Y',
                                                                    'startTime','endTime','end_X','end_Y',
                                                                    'totalOrderTime','travelTime'])
        order_q_i['ave_X'] = numpy.nan
        order_q_i['ave_Y'] = order_q_i.ave_X.map(lambda s: s)
        order_q_i['status'] = order_q_i.ave_X.map(lambda s: 'on deck')
        DG_ID = order_q_i.id.tolist()[0]
        earliestStart = order_q_grp.startTime.astype(int).min()
        check_order_q_i = order_q_i.append(D[(D.id==DG_ID) & (D.endTime>earliestStart)])
        dg_q_i = pull_from_order(check_order_q_i,errorCheck=True)
        updated = True
        return updated,order_q_i,dg_q_i
    else:
        updated = False
        return updated,None,None