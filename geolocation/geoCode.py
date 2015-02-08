
from time import sleep
import pandas as pd
# generally             --
# java version          -- https://developers.google.com/maps/documentation/javascript/geocoding
# java limits           -- https://developers.google.com/maps/documentation/geocoding/#Limits
# also, consider geopy  -- https://pypi.python.org/pypi/geopy


def getGPScoord(all_addr,printGPS=True,savePath='tmp_results.txt'):
    from pygeocoder import Geocoder # sudo port select python python26

    if type(all_addr) is list:
        z=all_addr
    else:
        f=open(R,'r')
        x=f.read()
        f.close()
        z=x.split('\r')

    d = pd.DataFrame({'addr':z})
    _iter = pd.Series(d.addr.unique().tolist()).iterkv()

    y=[]
    pt,s=0,'Address\tZip\tLat.\tLong.\r'
    #    print '\n"--" means only one result found.\nOtherwise, numbered results will be shown.'
    print s
    for k,it in _iter:
        results = Geocoder.geocode(it)
        if results.count > 1:
            for i in range(0,results.count):

                res=results[i]
                r_data = res.data[0]
                t = {'res_i'            : i,
                     'orig_addr'        : it.rstrip(),
                     'addr_valid'       : res.valid_address,
                     'partial_match'    : r_data['partial_match'] if res.valid_address != True else False,
                     'form_addr'        : res.formatted_address,
                     'geometry'         : r_data['geometry'],
                     'res_data'         : str(r_data),
                     }

                y.append(t)
                a=str(i)+'\t'+str(it.rstrip())+'\t'+str(res.postal_code)+'\t'+str(res.coordinates[0])+'\t'+str(res.coordinates[1])
                s+=a+'\r'
                if printGPS==True: print a

        else:
    #
            res=results
            r_data = res.data[0]
            partial_option = True if r_data.keys().count('partial_match') != 0 else False
            t = {'res_i'            : -1,
                 'orig_addr'        : it.rstrip(),
                 'addr_valid'       : res.valid_address,
                 'partial_match'    : r_data['partial_match'] if partial_option else False,
                 'form_addr'        : res.formatted_address,
                 'geometry'         : r_data['geometry'],
                 'res_data'             : str(r_data),
                 }

            y.append(t)
            a='--'+'\t'+str(it.rstrip())+'\t'+str(results.postal_code)+'\t'+str(results.coordinates[0])+'\t'+str(results.coordinates[1])
            s+=a+'\r'
            if printGPS==True: print a

        pt+=1
        if pt==5:
            sleep(2.6)
            pt=0

    d = pd.DataFrame(y)
    d['lat'],d['lon'] = zip(*d.geometry.map(lambda s: (s['location']['lat'],s['location']['lng'])))
    if savePath!='': d.to_csv(savePath)
    return d

def get_reverse_geo(fileWithCoords):
    from pygeocoder import Geocoder # sudo port select python python26
    #fileWithAddresses='/Users/admin/Desktop/work_locations.txt'
    f=open(fileWithCoords,'r')
    x=f.read()
    f.close()
    z=x.split('\r')
    pt=0
    for i in range(0,len(z)):
        a=z[i].split('\t')
        print Geocoder.reverse_geocode(eval(a[0]),eval(a[1]))
        pt+=1
        if pt==10:
            sleep(10)
            pt=0

def getArcLenBtCoords(lat1, long1, lat2, long2):
    import math
    #print lat1
    #print long1
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    try:
        phi1 = (90.0 - eval(str(lat1)))*degrees_to_radians
        phi2 = (90.0 - eval(str(lat2)))*degrees_to_radians
    except:
        print lat1
        print lat2
        raise SystemExit
                
    # theta = longitude
    try:
        theta1 = eval(str(long1))*degrees_to_radians
        theta2 = eval(str(long2))*degrees_to_radians
    except:
        print long1
        print long2
        raise SystemExit
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    # radius of earth = 3,959 mi
    return arc*3959

def getTriCoorLocations():
    f=open('/Users/admin/desktop/test_locations.txt','r')
    x=f.read()
    f.close()
    x=x.split('\r')
    print len(x)
    test_locations,test_lat,test_long=[],[],[]
    for it in x:
        #try:
#             a,b=it.split('\t')[0],it.split('\t')[1]
#             test_locations.append(a)
#             it=b
#             test_lat.append(eval(it)[0]) # in format: (latitude, longitude)
#             test_long.append(eval(it)[1])
        #except:
        #print type(it),len(it),it
        #print len(x[0].split('\t')),x[0].split('\t')[0],x[0].split('\t')[2]#,x[0].split('\t')[0]
        a=it.split('\t')[0],it.split('\t')[1],it.split('\t')[2]
        test_locations.append(a[0])
        test_lat.append(eval(a[1])) # in format: \t latitude \t longitude
        test_long.append(eval(a[2]))           
    print len(test_locations),len(test_lat),len(test_long)


    f=open('/Users/admin/desktop/work_locations.txt','r')
    y=f.read()
    f.close()
    y=y.split('\r')
    print len(y)
    work_locations,work_lat,work_long=[],[],[]
    for it in y:
#         try:
#             a,b=it.split('\t')[0],it.split('\t')[1]
#             work_locations.append(a)
#             it=b
#             work_lat.append(eval(it)[0]) # in format: (latitude, longitude)
#             test_long.append(eval(it)[1])
#         except:
        a=it.split('\t')[0],it.split('\t')[1],it.split('\t')[2]
        work_locations.append(a[0])
        work_lat.append(eval(a[1])) # in format: \t latitude \t longitude
        work_long.append(eval(a[2])) 
    print len(work_locations),len(work_lat),len(work_long)

    v='Work Location\tWork Coord\tNW T-Location\tNW Coord\tNE T-Location\tNE Coord\tSW T-Location\tSW Coord\tSE T-Location\tSE Coord\t'
    results=[v]
    
    for i in range(0,len(work_locations)):
        w_lat,w_long=work_lat[i],work_long[i]
        tL,tR,bL,bR=20,20,20,20
        top_left,top_right,bot_left,bot_right=["","",""],["","",""],["","",""],["","",""]
        for j in range(0,len(test_locations)):
            t_lat,t_long=test_lat[j],test_long[j]
            dist=getArcLenBtCoords(w_lat, w_long, t_lat, t_long)
            if t_lat-w_lat>0: # testing for west of work location
                if t_long-w_long>0: # testing for north of work location, else it is south..
                    if tL>dist:
                        tL=dist
                        top_left=[dist,test_locations[j],[t_lat,t_long]]
                else:
                    if bL>dist:
                        bL=dist
                        bot_left=[dist,test_locations[j],[t_lat,t_long]]
            else:
                if t_long-w_long>0: # testing for north of work location, else it is south..
                    if tR>dist:
                        tR=dist
                        top_right=[dist,test_locations[j],[t_lat,t_long]]
                else:
                    if bR>dist:
                        bR=dist
                        bot_right=[dist,test_locations[j],[t_lat,t_long]]
                        
        locations=[work_locations[i],[work_lat[i],work_long[i]]],top_left,top_right,bot_left,bot_right
        results.append(locations)

#         results.append(work_locations[i]+'\t'+str(work_lat[i],work_long[i])+'\t'+
#                        top_left[0]+'\t'+str(test_lat[top_left[1]])+','+str(test_long[top_left[1]])+'\t'+
#                        bot_left[0]+'\t'+str(test_lat[bot_left[1]])+','+str(test_long[bot_left[1]])+'\t'+
#                        top_right[0]+'\t'+str(test_lat[top_right[1]])+','+str(test_long[top_right[1]])+'\t'+
#                        bot_right[0]+'\t'+str(test_lat[bot_right[1]])+','+str(test_long[bot_right[1]]))
    for it in results: print it
    
if __name__ == '__main__':
    fileWithAddresses = '/Users/admin/Desktop/work_locations.txt'
    getGPScoord(fileWithAddresses,printGPS=True,save=False,reverse=False)
    #get_reverse_geo(fileWithAddresses)
    #
    
	
    
	#getTriCoorLocations()
    #p1 = ["40.522064", "-74.198690799999994"]
    #p2 = ["40.6175608", "-73.941171400000002"]
#    dist=getArcLenBtCoords(p1[0], p1[1], p2[0], p2[1])
#    print dist
    #print dist
#    from geopy import geocoders  
#        from geopy.point import Point
#    from geopy import distance  
#_, ne = g.geocode('Newport, RI')  
#_, cl = g.geocode('Cleveland, OH')  
#    distance.distance(p1, p2).miles 

#