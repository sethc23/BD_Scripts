# Normal Delivery Simulation
def NormalDelivery(vendors):
    print '\nstarting Normal Delivery Sim.\n'
    def deliver_all_orders(d_orders,d_time,results):
        a = d_orders.sort('start_time').reset_index(drop=True)
        # create back_log data
        try: current_location = a.ix[0,['vend_X','vend_Y']].astype(pd.np.int64).tolist()
        except: systemError()
        delivery_locations = a[['end_X','end_Y']].astype(pd.np.int64).as_matrix().tolist()
        order_times = a.order_time.astype(pd.np.int64).tolist()

        # GET BEST DELIVERY ROUTE -- ( starting location is inserted at beginning of "shortest_combo"
        shortest_combo,shortest_time = bestDeliveryRoute(current_location,d_time,delivery_locations,order_times)

        start_pt,home_pt = current_location,current_location
        time_pt = d_time # which is when DG is planning on leaving
        start,end=False,False
        for i in range(len(shortest_combo)):
            b = a.ix[i,:]
            b['start_time'] = time_pt
            b[['start_X','start_Y']] = start_pt
            b['travel_time'] = get_travel_time(start_pt,b[['end_X','end_Y']].astype(pd.np.int64).tolist())
            time_pt += b['travel_time']
            b['end_time'] = time_pt
            b['total_order_time'] = b['end_time'] - b['order_time']
            if i==0: b['tripStart']=True
            if i+1==len(shortest_combo): b['tripEnd']=True
            results = results.append(b)
            start_pt = b[['end_X','end_Y']].astype(pd.np.int64).tolist()
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

        order_times = V.order_time.astype(pd.np.int64).tolist()
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
            #     time = V[V.index==len(vend_results)-1+1].order_time.astype(pd.np.int64).values[0]        # time = next order.order_time


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
                    time = V[V.index==len(vend_results)-1+1].order_time.astype(pd.np.int64).values[0]        # time = next order.order_time
                except:
                    systemError()

            # while loop safety
            if pt > len(V):
                print 'why not exit?'
                systemError()
            else: pt+=1

            # print '\nvend_results:\n',vend_results
            # a=0
            del_ids = vend_results.deliv_id.astype(pd.np.int64).tolist()
            uniq_del_ids = dict(zip(del_ids,range(len(del_ids)))).keys()
            for it in uniq_del_ids:
                if del_ids.count(it)>1:
                    print vend_results
                    print it
                    systemError()

        if len(vend_results)!=len(V):
            print vend_results
            print len(vend_results),len(V)
            del_ids = vend_results.deliv_id.astype(pd.np.int64).tolist()
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
