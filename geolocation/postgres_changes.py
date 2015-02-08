
###Using PostgresSQL Server [ db1.public.routing ]:

from sys import path as sys_path
sys_path.append('/Users/admin/SERVER2/BD_Scripts/geolocation')
# from f_postgres import geoparse#,ST_PREFIX_DICT,ST_SUFFIX_DICT

# from f_vendor_postgre import get_addr_body,match_simple_regex
# from f_vendor_postgre import match_simple,match_simple_regex,match_levenshtein_series
from f_postgres import make_index,geom_inside_street_box
from re import search as re_search # re_search('pattern','string')
from re import sub as re_sub  # re_sub('pattern','repl','string','count')

import pandas as pd
import geopandas as gd
import numpy as np
from types import NoneType
from sqlalchemy import create_engine

engine = create_engine(r'postgresql://postgres:postgres@localhost/routing',
                       encoding='utf-8',
                       echo=False)
%load_ext sql
%sql postgresql://postgres:postgres@localhost/routing

BASE_SAVE_PATH = '/Users/admin/Projects/GIS/table_data/'


### add_points_to_remaining_lots
show_some_detail=False
show_steps=False
from IPython.display import FileLink, FileLinks
save_fig_path = '/Users/admin/Projects/GIS/matplotlib_data/nyc_block_and_lot.png'
matplot_files = FileLinks("/Users/admin/Projects/GIS/matplotlib_data/")
# display(matplot_files)
from math import degrees as rad_to_deg
from math import radians as deg_to_rad
from itertools import chain
from matplotlib import pyplot as plt

def geoms_to_collection(geoms):
    s='GEOMETRYCOLLECTION('
    for it in geoms:
        s+=it.to_wkt()+','
    return s.rstrip(',')+')'
def geoms_to_text(geoms):
    if type(geoms_to_text) != list: geoms=list(geoms)
    s=''
    for it in geoms:
        try:
            s+="ST_GeomFromText('"+it.to_wkt()+"'),"
        except:
            s+="ST_GeomFromText('"+it+"'),"
    return s.rstrip(',')
def geom_txts_to_collection(geom_txts):
    return "ST_Collect(ARRAY["+geoms_to_text(geom_txts)+'])'

all_pts = pd.read_sql_query("select * from lot_pts where geom is null and ignore is false and place is false",engine)
all_pts['block'] = all_pts.bbl.map(lambda s: str(s)[1:6])
uniq_blocks = all_pts.block.unique().tolist()
if show_some_detail==True: print len(uniq_blocks),'unique blocks'
if show_some_detail==True: print 'pluto has 1961 unique blocks'
# a=pd.read_sql_query("select distinct block from pluto",engine).block.tolist()
# for it in a:
#     if uniq_blocks.count(str('%05d'%it))==0:
#         print it
if show_some_detail==True: print 'lot 656 is a pier and was removed from lot_pts'

#
### iter block for add_points_to_remaining_lots
engine.execute('drop table if exists temp;')
for block in chain(uniq_blocks[:5]):
    print 'block\t',block
    
    lot_pts,A,skip = [],[],False
    if show_some_detail==True: print 'block\t',block

    uniq_street = all_pts[all_pts.block==block].bldg_street.unique().tolist()
    if uniq_street.count('')!=0:    dev = uniq_street.pop(uniq_street.index(''))
    if uniq_street.count(None)!=0:  dev = uniq_street.pop(uniq_street.index(None))

    for street_name in chain(uniq_street):
        if show_some_detail==True: print 'street_name\t',street_name

        ### Get All Lots on Block and On This Street
#         pts = all_pts[(all_pts.block==block)&(all_pts.bldg_street==street_name)].sort('bldg_num').reset_index(drop=True)
#         cmd=""" SELECT _bbl bbl,geom
#                 FROM pluto p,unnest(array%s) _bbl
#                 WHERE p.bbl = _bbl"""%str(pts.bbl.astype(int).tolist()).replace("'",'')
        lots = gd.read_postgis("""
                select * from pluto 
                where substring(to_char(bbl,'9999999999') from 3 for 5) = '%s'
                """%block,engine)

#         lots = gd.read_postgis(cmd,engine)
        #if show_steps==True: A.extend(lots.geom)
        print '\t\t',len(lots),'lots'

        ### Create Buffer Around Lots
        s = str([it.to_wkt() for it in lots.geom])
        T = {'buffer': '0.0005',
             'geoms' : s}
        cmd =   """ SELECT ST_Buffer(ST_ConvexHull((ST_Collect(the_geom))), %(buffer)s) as geom
                    FROM ( SELECT (ST_Dump( unnest(array[%(geoms)s]) )).geom the_geom) as t""".replace('\n','')%T
        block_buffer = gd.read_postgis(cmd,engine)
        #if show_steps==True: A.extend(block_buffer.geom)

        ### Get street as Line from lion_ways
        cmd =   """ SELECT st_makeline(_geom) geom
                    FROM
                        st_geomfromtext(
                        ' %(block_buffer)s '
                        , 4326) block_buffer,
                        (select ( st_dump( geom )).geom _geom
                            FROM lion_ways l
                            WHERE l.clean_street = '%(1)s'
                            AND l.geom is not null  ) as t2
                    WHERE st_intersects(_geom,block_buffer) is True
                """.replace('\n','')%{'1':str(street_name),
                                      'block_buffer':str(block_buffer.geom[0].to_wkt())}
        try:
            line_geom = gd.read_postgis(cmd,engine)
            skip_street=False
        except AttributeError:
            print 'skipping street:',street_name
            skip_street=True

        if skip_street==False:

            # A.extend(line_geom.geom)
            LINE = line_geom.geom[0].to_wkt()

            ### Keep only part of line intersecting with buffer
            s1 = str([it.to_wkt() for it in block_buffer.geom][0])
            s2 = str([it.to_wkt() for it in line_geom.geom][0])
            T = {'block_buffer': s1,
                 'street_line' : s2}
            cmd =   """ SELECT res_geom geom
                        FROM
                            st_geomfromtext('%(block_buffer)s') s1,
                            st_geomfromtext('%(street_line)s') s2,
                            st_intersection(s1,s2) res_geom
                    """.replace('\n','')%T
            tmp_part_line=gd.read_postgis(cmd,engine)
    #
            if show_steps==True:  A.extend(tmp_part_line.geom)

            for i in range(0,len(lots.geom)):
                bbl,lot = lots.ix[i,['bbl','geom']].values

                cmd =   """ SELECT ( st_dump( _geom )).geom,ST_NPoints((( st_dump( _geom )).geom))
                        FROM (
                            SELECT ( st_dump( st_geomfromtext('%(1)s') )).geom _geom
                            ) as t
                    """.replace('\n','')%{'1':str(lot.to_wkt())}

                ### Get Single Lot Polygon
                lot=gd.read_postgis(cmd,engine)
                if show_some_detail==True: A.append(lot.geom[0])

                ### Get Line From Lot Polygon
                perim_line = lot.boundary[0].to_wkt()
                # if show_steps==True: A.append(lot.boundary[0])

                ### Get Points of Segment of Lot Polygon Closest to Street
                cmd =   """ SELECT ( st_dumppoints( st_geomfromtext('%(1)s') )).geom""".replace('\n','')%{'1':str(perim_line)}
                points = gd.read_postgis(cmd,engine).geom
                t1,t2={},{}
                for j in range(1,len(points)):
                    poly_seg_pts=points[j-1],points[j]
                    dist_from_street = pd.read_sql("""  select
                                                        st_distance(
                                                           st_geomfromtext(' %(start_pt)s '),
                                                           st_geomfromtext(' %(street)s '))
                                                           +
                                                        st_distance(
                                                           st_geomfromtext(' %(end_pt)s '),
                                                           st_geomfromtext(' %(street)s '))
                                                        dist
                                                    """.replace('\n','')%{'start_pt':str(poly_seg_pts[0]),
                                                                          'end_pt' : str(poly_seg_pts[1]),
                                                                          'street' : LINE},engine)
                    t1.update({j:dist_from_street.dist[0]})
                    t2.update({j:poly_seg_pts})
                closest_seg_pts = t2[t1.values().index(min(t1.values()))+1]

                ### Lot Segment MidPoint
                lot_seg_mid_pt = gd.read_postgis("""   SELECT ST_Line_Interpolate_Point(st_makeline(ptA,ptB),0.5) geom
                                                        FROM
                                                            st_geomfromtext(' %(start_pt)s ') ptA,
                                                            st_geomfromtext(' %(end_pt)s ') ptB
                                                """.replace('\n','')%{'start_pt': str(closest_seg_pts[0]),
                                                                      'end_pt'  : str(closest_seg_pts[1]),
                                                                      'street'  : LINE},engine)

                if show_steps==True: A.append(lot_seg_mid_pt.geom[0])

                ### Closest Point in Street
                street_seg_mid_pt = gd.read_postgis("""
                    SELECT ST_ClosestPoint(
                        st_geomfromtext(' %(street)s '),
                        st_geomfromtext(' %(mid_pt)s ')) geom
                    """.replace('\n','')%{'mid_pt'  : str(lot_seg_mid_pt.geom[0].to_wkt()),
                                          'street'  : LINE},engine)
                #A.append(street_seg_mid_pt.geom[0])

                ### Absolute Angle of Segment (12=0 deg.,6=180 deg.)
                seg_angle = pd.read_sql("""     SELECT ST_Azimuth(ptA,ptB) ang
                                                FROM
                                                            st_geomfromtext(' %(start_pt)s ') ptA,
                                                            st_geomfromtext(' %(end_pt)s ') ptB
                                                """.replace('\n','')%{'start_pt': str(closest_seg_pts[0]),
                                                                      'end_pt'  : str(closest_seg_pts[1])},engine).ang[0]

                ### Point on Street that Intersects with perp. line extending from Poly Segment Midpoint
                this_lot_pt = gd.read_postgis("""
                    SELECT ( st_dumppoints( st_intersection( street, st_makeline(
                        st_makeline(mid_pt::geometry(Point,4326),ptA::geometry(Point,4326)),
                        st_makeline(mid_pt::geometry(Point,4326),ptB::geometry(Point,4326))))  )).geom
                    FROM
                        st_geomfromtext(' %(mid_pt)s ', 4326) mid_pt,
                        st_geomfromtext(' %(street)s ', 4326) street,
                        st_geomfromtext(' %(line_seg_pt)s ', 4326) line_seg_pt,
                        ST_Distance_Spheroid(mid_pt,line_seg_pt,
                            'SPHEROID["WGS 84",6378137,298.257223563]') dist,
                        ST_Project(mid_pt,dist+(dist*1.1),%(ang1)s) ptA,
                        ST_Project(mid_pt,dist+(dist*1.1),%(ang2)s) ptB
                                                """.replace('\n','')%{'mid_pt' : str(lot_seg_mid_pt.geom[0].to_wkt()),
                                                                      'line_seg_pt' : str(street_seg_mid_pt.geom[0].to_wkt()),
                                                                      'street'  : LINE,
                                                                      'ang1' : str(deg_to_rad(90-(360-rad_to_deg(seg_angle)))),
                                                                      'ang2' : str(deg_to_rad(270-(360-rad_to_deg(seg_angle))))},
                                              engine).geom
            #
                if len(this_lot_pt)==0 or len(lot.geom)>1:
                    print 'skipping lot:',lots.bbl.tolist()[i]
                    if len(lot.geom)>1:
                        print '\t\tabove too much for single lot'
                else:

                    if show_some_detail==True: A.append(this_lot_pt[0]) # taking first value...
                    lot_pts.append({'bbl':bbl,
                                    'geom':this_lot_pt[0]})

                    ### Line Connecting Lot to Street
                    line_lot_to_street = gd.read_postgis("""
                        SELECT ST_ShortestLine(lot_pt,mid_pt) geom
                        FROM
                            st_geomfromtext(' %(lot_pt)s ',4326) lot_pt,
                            st_geomfromtext(' %(mid_pt)s ',4326) mid_pt
                        """.replace('\n','')%{'mid_pt'  : str(lot_seg_mid_pt.geom[0].to_wkt()),
                                              'lot_pt'  : this_lot_pt[0]},engine)
            #
                    if len(line_lot_to_street.geom)>1:
                        gd.GeoSeries(line_lot_to_street.geom).plot()
                        print 'too much for Line Connecting Lot to Street'
                        raise SystemError
                    if show_some_detail==True: A.append(line_lot_to_street.geom[0])


            if show_some_detail==True:
                d=gd.GeoSeries(A).plot(fig_size=(26,22),
                                       save_fig_path=save_fig_path,
                                       save_and_show=False)

            if show_some_detail==True: me = raw_input('y?')
            else: me='y'

            if (me=='y' or me=='yq') and lot_pts!=[]:
                c = gd.GeoDataFrame(lot_pts)
                d=[]
                dev=[d.extend(zip(*it.coords.xy)) for it in c.geom]
                D = pd.DataFrame({'bbl':c.bbl.tolist(),'xy':d})
                D['x'],D['y'] = zip(*D.xy)
                D.to_sql('temp',engine,if_exists='append')

                print 'added street_name\t',street_name,'with',len(lot_pts),'lots'
                if me=='yq': raise SystemError
                else:
                    lot_pts,A,skip = [],[],False
                    plt.clf()
            else:
                if me!='y': raise SystemExit


engine.execute("""
UPDATE lot_pts l
SET geom = st_setsrid(st_makepoint(t.x,t.y),4326) 
FROM temp t 
WHERE l.bbl = t.bbl
""")
print 'DONE!'