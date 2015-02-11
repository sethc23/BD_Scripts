# PG f(x)s

from random import random,randrange
from rd_lib import pd,np,gd,engine,this_cwd
from rd_lib import way_t,vert_t,vert_g
import assumptions as A

def pg_get_random_pt_in_circle_around_node(node,cir_radius,vert_t=vert_t,vert_g=vert_g):

    ## North     azimuth 0       (0)
    ## East      azimuth 90      (pi/2)
    ## South     azimuth 180     (pi)
    ## West      azimuth 270     (pi*1.5)

    T = {'1':str(node),
         '2':str( round(randrange(100,int(cir_radius*1000)),1) ),
         '3':str(randrange(0,360)),
         'vert_t':vert_t,
         'vert_g':vert_g}
    cmd =   """
            select ST_Project(%(vert_g)s, %(2)s, radians(%(3)s)) geom
            from %(vert_t)s where id = %(1)s
            """%T
    cnt=10
    while cnt>0:
        rand_pt_in_cir = gd.read_postgis(cmd,engine).geom[0].to_wkt()
        rand_node = pd.read_sql("select z_get_closest_node_to_point_text('%s','%s','%s') pt"%(vert_t,vert_g,rand_pt_in_cir),engine).pt[0]
        if rand_node!=node:
            break
        else:
            cnt-=1
            if cnt<0:
                break

    if cnt<0: return 'fail',rand_pt_in_cir,rand_node
    else: return 'ok',rand_pt_in_cir,rand_node

def pg_get_random_node_in_box(box_area,vert_t=vert_t,vert_g=vert_g):
    cmd =   """
            select z_get_nodes_in_geom('%(vert_t)s',
                           '%(vert_g)s',
                           z_get_way_box(%(1)s))
            """%{'1':box_area,'vert_t':vert_t,'vert_g':vert_g}
def pg_get_nodes_in_geom(in_geom='',vert_t=vert_t,vert_g=vert_g):
    if in_geom!='':
        T = {   'node_table':vert_t,
                'node_col':vert_g,
                'in_geom':in_geom}
    else:
        T = {   'node_table':vert_t,
                'node_col':vert_g,
                'in_geom':"z_get_way_box(%s)"%str(A.work_area).strip('[]')}

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
         '3':str(randrange(0,360))}
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

def pg_get_travel_dist(node_array1,node_array2,way_t=way_t):
    """
    USAGE:

        pg_get_travel_dist( 2646,                           2.8277209975200002
                            1836)

        pg_get_travel_dist( 2646,                           [   1.86996766966,
                            [1836, 1788, 1534])                 1.97567025639,
                                                                2.11327815249   ]

        pg_get_travel_dist( [1836, 1788],                    [   1.86599323835,
                            [2646, 1727])                        1.82317672544   ]


    """
    if type(node_array1)!=list:
        if type(node_array2)!=list:
            return pd.read_sql("""
                        select z_get_miles_between_nodes('%s',
                        %s,
                        %s) arr"""%(way_t,str(node_array1).strip('[]'),str(node_array2).strip('[]')),engine).arr[0]
        else:
            return pd.read_sql("""
                        select z_get_miles_between_nodes('%s',
                        %s,
                        array[%s]) arr"""%(way_t,str(node_array1).strip('[]'),str(node_array2).strip('[]')),engine).arr[0]
    else:
        return pd.read_sql("""
                    select z_get_miles_between_nodes('%s',
                    array[%s],
                    array[%s]) arr"""%(way_t,str(node_array1).strip('[]'),str(node_array2).strip('[]')),engine).arr[0]

def geom_inside_street_box(ways,geom_table,geom_label,table_cols=None,conditions=None):
    T = {'1':str(ways).strip('[]'),
         '2':geom_table,
         '3':geom_label}
    if table_cols!=None:
        T.update({'4':', %s'%str(table_cols).strip('[]').replace("'",'')})
    else:
        T.update({'4':''})
    cmd =   """
        select res_geom geom %(4)s
        from
            %(2)s t,
            (select z_get_way_box(%(1)s) box_geom) as d,
            st_intersection(t.%(3)s,box_geom) res_geom
        where t.%(3)s is not null
        and st_astext(res_geom) != 'GEOMETRYCOLLECTION EMPTY'
        """.replace('\n',' ') % T
    return gd.read_postgis(cmd,engine)
def make_column_primary_serial_key(table='',p_key='id',new_col=False):
    T = {'1':table,
         '2':p_key}
    if new_col==True:
        cmd = """
        ALTER TABLE %(1)s ADD COLUMN %(2)s SERIAL;
        """.replace('\n',' ') % T
        engine.execute(cmd)
    cmd = """
    UPDATE %(1)s SET %(2)s = nextval(pg_get_serial_sequence('%(1)s','%(2)s'));
    ALTER TABLE %(1)s ADD PRIMARY KEY (%(2)s);
    """.replace('\n',' ') % T
    engine.execute(cmd)

def pg_get_scrape_addresses():
    """
    Restaurants are located and identified by their proximity to geographic coordinates.

    WORKFLOW:
    1. A template of lattice points separated bilaterally by a 'pt_buffer' and covering MN is first generated.
    2. Lots are located nearest to the lattice points.
    3. Addresses starting with numbers are selected from the identified lots.
    4. Addresses returned.
    """
    pass

def make_lattice(pt_buff_in_miles=False):
    # import embed_ipython as I; I.embed()
    from os.path import abspath
    from sys import path as py_path
    py_path.append(abspath(this_cwd+'/web_scraping/geolocation'))
    from web_scraping.geolocation import geoCode
    from geoCode import getArcLenBtCoords
    # 1/3 km between 5th and 6th ave. on W. 12th
    # 1 miles = 1609.34 meters
    miles_to_meters = 1609.34
    if type(pt_buff_in_miles)==bool:
        pt_buff_in_miles = 0.75 # 0.3
    lattice_table_name = 'scrape_lattice'

    z = pd.read_sql("select min(lat) a,max(lat) b,min(lon) c,max(lon) d from lws_vertices_pgr",engine)
    lat_min,lat_max,lon_min,lon_max = z.a[0],z.b[0],z.c[0],z.d[0]
    lat_mid,lon_mid = lat_min+((lat_max-lat_min)/float(2)),lon_min+((lon_max-lon_min)/float(2))
    lat_cmd =   """
                SELECT ST_Distance_Sphere(ptA,ptB) lat_dist
                from (SELECT ST_GeomFromText('POINT(%s %s)',4326) as ptA,
                             ST_GeomFromText('POINT(%s %s)',4326) as ptB) as foo;
                """%(str(lon_mid),str(lat_max),str(lon_mid),str(lat_min))
    lon_cmd =   """
                SELECT ST_Distance_Sphere(ptA,ptB) lon_dist
                from (SELECT ST_GeomFromText('POINT(%s %s)',4326) as ptA,
                             ST_GeomFromText('POINT(%s %s)',4326) as ptB) as foo;
                """%(str(lon_max),str(lat_mid),str(lon_min),str(lat_mid))
    lat_range = pd.read_sql(lat_cmd,engine).lat_dist[0]
    lon_range = pd.read_sql(lon_cmd,engine).lon_dist[0]
    lat_segs = int(round(lat_range/float(pt_buff_in_miles * miles_to_meters),))
    lon_segs = int(round(lon_range/float(pt_buff_in_miles * miles_to_meters),))

    lat_seg_len = lat_range/lat_segs
    lon_seg_len = lon_range/lon_segs

    # lat_mid_distances = (np.arange(0,lat_segs) * (lat_range/lat_segs)) - (lat_range/lat_segs)/2
    # lon_mid_distances = (np.arange(0,lon_segs) * (lon_range/lon_segs)) - (lon_range/lon_segs)/2
    # lat_mid_distances[0],lon_mid_distances[0] = 0,0

    # create lattice table
    engine.execute('drop table if exists %s'%(lattice_table_name))
    engine.execute("""
                        CREATE TABLE %(table_name)s (
                            gid		serial primary key,
                            x		double precision,
                            y 		double precision,
                            geom	geometry(Point,4326));

                  """%{'table_name':lattice_table_name})
    engine.execute("""
                        UPDATE %(table_name)s SET gid = nextval(pg_get_serial_sequence('%(table_name)s','gid'));
                    """%{'table_name':lattice_table_name})
    # ALTER TABLE %(table_name)s ADD PRIMARY KEY (gid);
    for i in range(0,lat_segs):
        lat_d = lat_seg_len * i
        T = {   'table_name':lattice_table_name,
                    'X':str(lon_min),
                    'Y':str(lat_min),
                    'n_dist':str(lat_d),
                    'n_rad':str(0)  }
        cmd =   """
                SELECT
                        st_x(n_geom::geometry(Point,4326))  new_x,
                        st_y(n_geom::geometry(Point,4326))  new_y
                FROM
                    (SELECT
                        ST_Project( st_geomfromtext('Point(%(X)s %(Y)s)',4326),
                                    %(n_dist)s,
                                    radians(%(n_rad)s)) n_geom)
                    AS foo;
                """.replace('\n','')%T
        X = pd.read_sql(cmd,engine).new_x[0]
        Y = pd.read_sql(cmd,engine).new_y[0]

        lon_d = 0
        for j in range(0,lon_segs+1):
            lon_d += lon_seg_len
            T = {   'table_name':lattice_table_name,
                    'X':str(X),
                    'Y':str(Y),
                    'e_dist':str(lon_d),
                    'e_rad':str(90)   }
            engine.execute("""
                    INSERT INTO %(table_name)s(x,y)
                    SELECT
                        st_x(n_geom::geometry(Point,4326))  new_x,
                        st_y(n_geom::geometry(Point,4326))  new_y
                    FROM
                        (SELECT
                            ST_Project( st_geomfromtext('Point(%(X)s %(Y)s)',4326),
                                        %(e_dist)s,
                                        radians(%(e_rad)s)) n_geom)
                        AS foo;
                      """.replace('\n','')%T)
            cmd =   """
                SELECT
                        st_x(n_geom::geometry(Point,4326))  new_x,
                        st_y(n_geom::geometry(Point,4326))  new_y
                FROM
                    (SELECT
                        ST_Project( st_geomfromtext('Point(%(X)s %(Y)s)',4326),
                                    %(e_dist)s,
                                    radians(%(e_rad)s)) n_geom)
                    AS foo;
                """.replace('\n','')%T
            X = pd.read_sql(cmd,engine).new_x[0]
            Y = pd.read_sql(cmd,engine).new_y[0]
            import embed_ipython as I; I.embed()
                    #
                    #     INSERT INTO %(table_name)s(x,y)
                    # select
                    #     st_x(e_geom::geometry(Point,4326))  e_geom_x,
                    #     st_y(e_geom::geometry(Point,4326))  e_geom_y
                    # FROM
                    #     (select
                    #         ST_Project( st_geomfromtext('Point(%(X)s %(Y)s)',4326),
                    #                     %(e_dist)s,
                    #                     radians(%(e_rad)s)) e_geom)
                    #     as foo;
                    #
                    # .replace('\n','')%T

    #         z = gd.read_postgis(cmd,engine)
    #         z = pd.read_sql(cmd,engine)
            # import pdb; pdb.set_trace();
            #import embed_ipython as I; I.embed()
            # import embed_ipython as I; I.i_trace()
    #     print cmd
        engine.execute(cmd)
    engine.execute('UPDATE %s SET geom = ST_SetSRID(ST_MakePoint(x,y), 4326);'%(lattice_table_name))
    # print A

if __name__ == '__main__':
    from sys import argv
    try:
        cmd = []
        for i in range(0, len(argv)): cmd.append(argv[i])
            # cmd[0] == current working directory
            # cmd[1] == function to apply
            # cmd[2] == variable for the function
        stop = False
    except:
        cmd = []
        stop = True
    # print
    if stop == False:
        if cmd[1]   == 'make_lattice':          make_lattice()

