# def Assumption(get_var='',assumptions=None):

global work_area,deliv_radius_per_vendor_in_miles,vend_num
global vend_hours_delivering,deliveries_per_vend,DG_num
global max_travelToLocTime,DG_start_location_in_work_area
global travel_speed,MPH,wait_at_vendor,max_delivery_time



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
#   on bike -- 10 mph on average??

# if assumptions==None:
assumptions = { 'work_area'                         : ['14 st','10 ave','59 st','1 ave'],
                'deliv_radius_per_vendor_in_miles'  : 1.0, # waist of MN is about 2 miles
                'deliv_radius_per_vendor_in_km'     : 1.0 * 1.60934,
                'vend_num'                          : 5,
                'vend_hours_delivering'             : 1,
                'deliveries_per_vend'               : [3,8], # range of deliveries
                'DG_num'                            : 10,
                'max_travelToStartLocTime'          : 10,
                'DG_start_location_in_work_area'    : True,
                'travel_speed'                      : 1.0, # time to walk one street block
                'MPH'                               : 12.5,
                'wait_at_vendor'                    : 5,
                'max_delivery_time'                 : 40
                }

for k,v in assumptions.iteritems():
    globals()[k] = v

global DG_start_location_grid,DG_pool_grp_part_size,max_delivery_per_dg
global max_travelToLocTime,totalTime,reuse_dg_pool,avenue_labels

# vend_location_grid=avenues_of_vendors,streets_of_vendors
# vend_deliver_avenues,vend_deliver_streets=6,15 # distance per vendor
# vend_deliver_radius = vend_deliver_streets/2.0
# vend_delivery_grid = vend_deliver_avenues,vend_deliver_streets

rd_conditions = {   'DG_start_location_grid'    : work_area,
                    'DG_pool_grp_part_size'     : 5,
                    'max_delivery_per_dg'       : 4,
                    'max_travelToLocTime'       : 15,
                    'totalTime'                 : vend_hours_delivering*60,
                    'reuse_dg_pool'             : True,
                    'avenue_labels'             : ['11th','10th','9th','8th','7th','6th','5th','Madison',
                                                   'Park','Lexington','3rd','2nd','1st',
                                                   'Ave. A','Ave. B','Ave. C','Ave. D']}

for k,v in rd_conditions.iteritems():
    globals()[k] = v

#all=dict(assumptions.items() + rd_conditions.items() + { '\n':'\n'}.items())
#if get_var=='all': return all

# OTHER ASSUMPTIONS APPLIED IN MODELING --
# (1) vendors will make optimum delivery route based on overall shortest time
#       (regardless if first order included in route is delivered last)
#     In other words, vendor will maximize (end_time-start_time),
#        as opposed to maximizing (end_time-order_time).

#if all.keys().count(get_var)!=0:
#    return all[get_var]