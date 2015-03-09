import                                  datetime            as dt
import                                  codecs
from time                           import sleep
from urllib                         import quote_plus,unquote
from re                             import findall          as re_findall
from re                             import sub              as re_sub           # re_sub('patt','repl','str','cnt')
from re                             import search           as re_search        # re_search('patt','str')
from subprocess                     import Popen            as sub_popen
from subprocess                     import PIPE             as sub_PIPE
from traceback                      import format_exc       as tb_format_exc
from sys                            import exc_info         as sys_exc_info
from types                          import NoneType
from time                           import sleep            as delay
from os                             import environ          as os_environ
from uuid                           import uuid4            as get_guid
from os                             import path             as os_path
from sys                            import path             as py_path
py_path.append(                             os_path.join(os_environ['HOME'],'.scripts'))
from system_settings                import *
# from System_Control               import System_Reporter
# SYS_r                               =   System_Reporter()
import                                      pandas          as pd
# from pandas.io.sql                import execute              as sql_cmd
pd.set_option(                              'expand_frame_repr', False)
pd.set_option(                              'display.max_columns', None)
pd.set_option(                              'display.max_rows', 1000)
pd.set_option(                              'display.width', 180)
np = pd.np
np.set_printoptions(                        linewidth=200,threshold=np.nan)
import                                      geopandas       as gd
from sqlalchemy                     import create_engine
from logging                        import getLogger
from logging                        import INFO             as logging_info

getLogger(                                  'sqlalchemy.dialects.postgresql').setLevel(logging_info)
routing_eng                             =   create_engine(r'postgresql://postgres:postgres@%s:%s/%s'
                                                  %(DB_HOST,DB_PORT,'routing'),
                                                  encoding='utf-8',
                                                  echo=False)
from psycopg2                       import connect          as pg_connect
conn                                    =   pg_connect("dbname='routing' "+
                                                     "user='postgres' "+
                                                     "host='%s' password='' port=8800" % DB_HOST);
cur                                     =   conn.cursor()

INSTANCE_GUID                           =   'tmp_'+str(get_guid().hex)[:7]

# py_path.append(                         os_path.join(os_environ['BD'],'geolocation'))
# from f_postgres import geoparse#,ST_PREFIX_DICT,ST_SUFFIX_DICT

#### from f_vendor_postgre import get_bldg_street_idx
#### from f_vendor_postgre import get_addr_body,match_simple_regex
#### from f_vendor_postgre import match_simple,match_simple_regex,match_levenshtein_series
# from f_postgres import make_index,geom_inside_street_box,make_column_primary_serial_key

# from ipdb import set_trace as i_trace; i_trace()



def get_tables_headers(filePath=''):
    df_t = pd.read_sql_query("select * from information_schema.tables",engine)
    all_t = df_t[(df_t.table_schema=='public') & (df_t.table_catalog=='routing')].table_name.tolist()
    w,max_l = {},0
    print("All Routing Tables")
    for i in range(0,len(all_t)):
        t=all_t[i]
        print(str(i)+'\t\t'+t+'\n')
        df = pd.read_sql_query("SELECT * FROM "+t+" LIMIT 1", engine)
        x = df.columns
        w.update({t : x.values.tolist()})
        if len(x)>max_l: max_l=len(x)
        for it in x: print(it)
        print('\n\n')
        print('\n',df.head())
        print('\n\n')
    j=pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in w.iteritems() ]))
    j.to_csv(filePath)
    return j
def copy_select_to_hd5(table):
    t=table
    if t=='lion_ways':
        save_cols = [   'LBoro',
                        'NodeIDFrom',
                        'NodeIDTo',
                        'RBoro',
                        'SegCount',
                        'SegmentID',
                        'SeqNum',
                        'Street',
                        'StreetCode'
                    ]
        s = str(['x.'+it for it in save_cols]).strip("[]").replace("'",'')
        w = ' WHERE x.LBoro=1 OR x.RBoro=1'
        df = pd.read_sql_query("SELECT "+s+" FROM "+t+" x"+w,engine)
        df.to_hdf(BASE_SAVE_PATH+t+'_select.h5','table')
        return
    # elif t=='lion_nodes':

    elif t=='pluto':
        save_cols = [   'Address',
                        'BldgClass',
                        'BldgDepth',
                        'BldgFront',
                        'Block',
                        'Borough',
                        'Lot',
                        'LotFront',
                        'LotType',
                        'NumBldgs',
                        'NumFloors',
                        'ResArea',
                        'UnitsRes',
                        'UnitsTotal',
                        'ZipCode'       ]
        s = str(['x.'+it for it in save_cols]).strip("[]").replace("'",'')
        w = ' WHERE x.LBoro=1 OR x.RBoro=1'
        df = pd.read_sql_query("SELECT "+s+" FROM "+t+" x"+w,engine)
        df.to_hdf(BASE_SAVE_PATH+t+'_select.h5','table')
        return

def clean_street_names(df,from_label,to_label):
    def remove_non_ascii(text):
        return re_sub(r'[^\x00-\x7F]+',' ', text)

    df_ignore = df[df[from_label].map(lambda s: type(s))==NoneType]
    df_ignore_idx = df_ignore.index.tolist()
    if len(df_ignore_idx)>0:
        df = df.ix[df[df.index.isin(df_ignore_idx)==False].index,:]

    df[to_label]=df[from_label].map(lambda s: s.lower().strip())
    df[to_label]=df[to_label].map(remove_non_ascii)

    # st_strip_before
    for k,v in ST_STRIP_BEFORE_DICT.iteritems():
        df[to_label]=df[to_label].map(lambda s: re_sub(k,v,s))

    # st_prefix
    for k,v in ST_PREFIX_DICT.iteritems():
        df[to_label]=df[to_label].map(lambda s: re_sub(r'^('+k+r')\s',v+r' ',s)
                                        if ST_SUFFIX_DICT.values().count(
                                        re_sub(r'^('+k+r')\s',v+r' ',s)
                                        ) == 0 else s)

    # st_suffix
    for k,v in ST_SUFFIX_DICT.iteritems():
        df[to_label]=df[to_label].map(lambda s: re_sub(r'\s('+k+r')$'   ,r' '+v,s))

    # st_body
    for k,v in ST_BODY_DICT.iteritems():
        df[to_label]=df[to_label].map(lambda s: re_sub(k,v,s))

    # st_strip_after
    for k,v in ST_STRIP_AFTER_DICT.iteritems():
        df[to_label]=df[to_label].map(lambda s: re_sub(k,v,s))

    return df.append(df_ignore)

def update_remaining_lots():
    import fiona
    from shapely.geometry import mapping
    
    def save_polygon_shape(fPath,poly_set):
        schema = {
            'geometry': 'Polygon',
            'properties': {'id': 'int'},
        }

        cnt = len(poly_set)
        with fiona.open(fPath, 'w', 'ESRI Shapefile', schema) as c:
            for i in range(0,cnt):
                c.write({
                    'geometry': mapping(poly_set[i]),
                    'properties': {'id': i+1},
                })

    cmd = "select bbl from lot_pts where geom is null and ignore is false and place is false"
    l = pd.read_sql_query(cmd,engine)
    cmd = "select geom from pluto where bbl = any(array"+str(l.bbl.tolist()).replace("'",'')+")"
    p = gd.read_postgis(cmd,conn)
    poly_set=p.geom
    fPath = '/Users/admin/Projects/GIS/map_data/remaining_lots.shp'
    save_polygon_shape(fPath,poly_set)

def add_points_to_remaining_lots(show_some_detail=True,show_steps=False):
    ### add_points_to_remaining_lots
#    show_some_detail=False
#    show_steps=False

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
    for block in chain(uniq_blocks):
        if show_some_detail==True: print 'block\t',block

        lot_pts,A,skip = [],[],False
        plt.clf()

        uniq_street = all_pts[all_pts.block==block].bldg_street.unique().tolist()
        if uniq_street.count('')!=0:    dev = uniq_street.pop(uniq_street.index(''))
        if uniq_street.count(None)!=0:  dev = uniq_street.pop(uniq_street.index(None))

        for street_name in chain(uniq_street):
            if show_some_detail==True: print 'street_name\t',street_name

            ### Get All Lots on Block and On This Street
            pts = all_pts[(all_pts.block==block)&(all_pts.bldg_street==street_name)].sort('bldg_num').reset_index(drop=True)
            cmd=""" SELECT _bbl bbl,geom
                    FROM pluto p,unnest(array%s) _bbl
                    WHERE p.bbl = _bbl"""%str(pts.bbl.astype(int).tolist()).replace("'",'')
            lots = gd.read_postgis(cmd,engine)
            #if show_steps==True: A.extend(lots.geom)

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

        if me=='y' and lot_pts!=[]:
            c = gd.GeoDataFrame(lot_pts)
            d = engine.execute("""
                        UPDATE lot_pts
                        SET geom = the_geom
                        FROM
                            (SELECT these_bbl the_bbl
                                FROM unnest(array%(these_bbl)s) these_bbl) as t1,
                            (SELECT st_geomfromtext(these_geoms,4326) the_geom
                                FROM unnest(array%(these_geoms)s) these_geoms) as t2
                        WHERE bbl = the_bbl
                    """.replace('\n','')%{'these_bbl'  : str(c.bbl.tolist()),
                                          'these_geoms' : str([it.to_wkt() for it in c.geom])
                                          }
                           ,engine)
        else:
            if me!='y': break
    print 'DONE!'

def convert_street_names_in_lot_pts():
    cmd = "select bbl,bldg_street from lot_pts where geom is not null and ignore is false and bldg_street is not null"
    l = lots = pd.read_sql_query(cmd,engine)

    l = geoparse(l,'bldg_street','bldg_street')

    engine.execute('drop table if exists temp')
    l.to_sql('temp',engine,if_exists='append',index=False)
    # engine.execute('update lot_pts l set bldg_num_start = t.bldg_num_start from temp t where t.bbl = l.bbl')
    engine.execute('update lot_pts l set bldg_street = t.bldg_street from temp t where t.bbl = l.bbl')
    engine.execute('drop table if exists temp')

    ## Update lot_pts with lot_idx = {bldg_street.bldg_num}

    cmd = """
        SELECT bbl, a.bbl %(3)s
        FROM lot_pts a
        INNER JOIN unnest(array[%(1)s]) %(2)s
        ON a.start_idx <= %(2)s and %(2)s <= a.end_idx
        """.replace('\n',' ') % T
    res = pd.read_sql_query(cmd,engine)

def make_index(describe=True,commit=False):
    # from sys import path as sys_path
    # sys_path.append('/Users/admin/SERVER2/BD_Scripts/geolocation')
    # from f_postgres import geoparse,ST_PREFIX_DICT,ST_SUFFIX_DICT

    from re import search as re_search # re_search('pattern','string')
    from re import sub as re_sub  # re_sub('pattern','repl','string','count')

    cmd = "select bbl,bldg_num,bldg_street from lot_pts where geom is not null and ignore is false and bldg_street is not null"
    l = lots = pd.read_sql_query(cmd,engine)

    ## geoparse everything
    l = geoparse(l,'bldg_street','clean_addr')
    ## reduce to unique way (street,road,avenue,lane, etc...)
    addr_bbl_dict = dict(zip(l.clean_addr.tolist(),l.bbl.tolist()))
    ul = pd.DataFrame({'addr':addr_bbl_dict.keys(),'bbl':addr_bbl_dict.values()})

    # ul['has_number_in_name'] = ul.addr.map(lambda s: bool(re_search(r'[0-9]',s)))
    #
    # nn = non_numbered_streets = ul[ul.has_number_in_name==False].sort('addr')
    # n  = numbered_street      = ul.ix[ul.index-nn.index,:]
    #
    #n = a[a[street_column].str.contains('^(w)\s[0-9]+')==True]
    #from f_nyc_data import create_numbered_streets
    #n  = create_numbered_streets(n.copy(),street_column='addr')
    #print len(n.index),'length of generated number streets'
    #
    # ul_num_street_idx = nn.index.copy()
    # ul.drop(['has_number_in_name','bbl'],axis=1,inplace=True)
    # nn.drop(['has_number_in_name','bbl'],axis=1,inplace=True)
    # nn = nn.reset_index(drop=True)
    #
    # a = n.append(nn,ignore_index=True)
    # a = pd.DataFrame({'addr':dict(zip(a.addr.tolist(),range(0,len(a.index)))).keys()})

    a = ul.copy()
    a['nid'] = a.index
    a['bldg_street_idx'] = a.nid.map(lambda s: str('%05d' % s))
    a['addr'] = a.addr.map(lambda s: s.lower().strip())

    # add entries with or without different combinations of info (e.g., e/w, st/ave, etc...)
    a_idx = a.bldg_street_idx.tolist()

    # pre_re_s = re_search_string = r'^('+"|".join(ST_PREFIX_DICT.values())+r')\s'
    # alp  = a_less_prefix = pd.DataFrame({'addr':a.addr.map(lambda s: re_sub(pre_re_s,r'',s).strip()
    #                                        if ST_SUFFIX_DICT.values().count(  # this extra is to prevent a "st" result
    #                                         re_sub(pre_re_s,r'',s).strip()
    #                                         ) == 0 else ''),
    #                                      'bldg_street_idx': a_idx})

    suf_re_s = re_search_string = r'\s('+r'|'.join(ST_SUFFIX_DICT.values())+r')$'
    als  = a_less_suffix = pd.DataFrame({'addr':a.addr.map(lambda s: re_sub(suf_re_s,r'',s).strip()
                                           if ST_SUFFIX_DICT.values().count(  # this extra is to prevent a "w" result
                                            re_sub(suf_re_s,r'',s).strip()
                                            ) == 0 else s),
                                         'bldg_street_idx':a_idx})

    nw = num_ways = als[als.addr.str.contains('\d+')]
    nw['below13'] = nw.addr.map(lambda s: True if eval(re_search('\d+',s).group().strip())<=12 else False)
    nw['one_word'] = nw.addr.map(lambda s: True if len(s.split(' '))==1 else False)
    als = als[als.index.isin(nw[(nw.below13==True)&(nw.one_word==True)].index.tolist())==False]

    # alps = a_less_prefix_less_suffix = pd.DataFrame({'addr':alp.addr.map(lambda s: re_sub(suf_re_s,'',s).strip()),
    #                                      'bldg_street_idx':a_idx})

    alr = avenues_lettered_reversed = a[a.addr.map(lambda s: (s.find('avenue')==0)&(len(s.split(' '))==2))].copy()
    alr['addr'] = alr.addr.map(lambda s: s.split(' ')[1]+' ave')

    sns = street_not_st = a[a.addr.map(lambda s: bool(re_search('(st)$',s)))].copy()
    sns['addr'] = sns.addr.map(lambda s: re_sub(r'(st)$',r'street',s).strip())

    ana = avenue_not_ave = a[a.addr.map(lambda s: bool(re_search('(ave)$',s)))].copy()
    ana['addr'] = ana.addr.map(lambda s: re_sub(r'(ave)$',r'avenue',s).strip())

    if describe==True:
        print '\n',len(ana),'ana',ana.head()
        print '\n',len(sns),'sns',sns.head()
        print '\n',len(alr),'alr',alr.head()
        # print '\n',len(alp),'alp',alp.head()
        print '\n',len(als),'als',als.head()
        # print '\n',len(alps),'alps',alps.head()

    # combine all frames
    all_f = ana.append(sns,ignore_index=True)\
                .append(alr,ignore_index=True)\
                .append(als,ignore_index=True)\
                .reset_index(drop=True)



    # reduce to unique items in frames
    all_f_list = all_f.addr.tolist()
    all_f['cnt'] = all_f.addr.map(lambda s: all_f_list.count(s))
    all_f = all_f[all_f.cnt==1]

    # remove combine original street names with street name permutations
    uniq_orig_addr = a.addr.unique().tolist()
    all_f = all_f[all_f.addr.isin(uniq_orig_addr)==False].reset_index(drop=True)

    # add index 'nid' to new addr.s
    st_pt=int(a.nid.max())+1
    end_pt=st_pt+len(all_f)
    all_f['nid'] = range(st_pt,end_pt)

    A = a.append(all_f,ignore_index=True)
    A = A[A.addr!=''].reset_index(drop=True)
    # A.head()
    J = A.addr.tolist()
    all_unique_addr_list = dict(zip(J,range(0,len(J)))).keys()

    if describe==True:
        print '\n',all_unique_addr_list.count('s'),'"s" count'
        print all_unique_addr_list.count('w'),'"w" count\n'

    bldg_idx_addr_map = dict(zip(A.bldg_street_idx.tolist(),A.addr.tolist()))
    addr_bldg_idx_map = dict(zip(A.addr.tolist(),A.bldg_street_idx.tolist()))
    B = pd.DataFrame({'addr':all_unique_addr_list})
    B['bldg_street_idx'] = B.addr.map(addr_bldg_idx_map)
    st_pt=int(a.nid.max())+1
    end_pt=st_pt+len(B.index)
    B['nid'] = range(st_pt,end_pt)
    B['one_word'] = B.addr.map(lambda s: True if len(s.split(' '))==1 else False)

    if describe==True: print '\n',len(B.index),'total row count in address_idx'

    if commit==False: return B
    engine.execute('drop table if exists address_idx')
    B.to_sql('address_idx',engine,if_exists='append',index=False)
    engine.execute('ALTER TABLE address_idx ADD PRIMARY KEY (nid)')
    return B
def create_lot_idx_start_pts():
    cmd = """
    update lot_pts
    set lot_idx_start = to_number(
        concat(
            a.bldg_street_idx,
            '.',
            to_char(bldg_num,'00000')
        )
    ,'00000D00000')
    from address_idx a
    where a.addr = bldg_street
    """.replace('\n',' ')
    engine.execute(cmd)
def create_lot_idx_end_pts():
    cmd = """
    update lot_pts
    set lot_idx_end = to_number(
        concat(
            a.bldg_street_idx,
            '.',
            to_char(bldg_num_end,'00000')
        )
    ,'00000D00000')
    from address_idx a
    where a.addr = bldg_street
    """.replace('\n',' ')
    engine.execute(cmd)
def convert_zip_street_num_to_street_num():
    cmd="""
    update lot_pts l
    set lot_idx_end = to_number(
        concat(
            substring(to_char(end_idx,'999999999999999') from 7 for 5),
            '.',
            substring(to_char(end_idx,'999999999999999') from 12 for 5)
        )
    ,'99999D99999')
    where end_idx is not null
    """.replace('\n',' ')
    engine.execute(cmd)
def add_bldg_range_pts():
    ###Add "bldg_num_end" values

    cmd = "select bbl,bldg_num,bldg_street from lot_pts where geom is not null and ignore is false and bldg_street is not null"
    l = pd.read_sql_query(cmd,engine)
    uniq_streets = l.bldg_street.unique().tolist()

    i=0
    for u_st in uniq_streets:
        #print i,u_st
        i+=1
        d = l[(l.bldg_street==u_st)&(l.bldg_num!=0)].sort('bldg_num').reset_index(drop=True)
        d_len = len(d.index)
        if d_len > 0:
            d['d_idx'] = range(0,d_len)

            d['bldg_num_next'] = d.ix[:,['d_idx','bldg_num']
                                      ].apply(lambda s: s[1] if s[0]==d_len-1
                                              else (d.ix[s[0]+1,'bldg_num']-s[1])-1,axis=1)

            # d['bldg_num_start'] = d.ix[:,['d_idx','bldg_num'
            #                             ,'bldg_num_next']
            #                          ].apply(lambda s: s[1] if s[0]>0 else 0,axis=1)

            d['bldg_num_end'] = d.ix[:,['d_idx','bldg_num'
                                        ,'bldg_num_next']
                                     ].apply(lambda s: s[1] if s[0]==d_len-1
                                             else s[1]+s[2],axis=1)

            d=d.drop(['bldg_num_next','bldg_num','bldg_street','d_idx'],axis=1)

        #     if d.ix[0,'bldg_num_end']==-1:
        #         n = d[d.bldg_num_end>-1]
        #         n_idx = n.index[0]
        #         first_real = d.ix[n_idx,'bldg_num_end']
        #         d.ix[0,'bldg_num_end'] = first_real

            engine.execute('drop table if exists temp')
            d.to_sql('temp',engine,if_exists='append',index=False)
            # engine.execute('update lot_pts l set bldg_num_start = t.bldg_num_start from temp t where t.bbl = l.bbl')
            engine.execute('update lot_pts l set bldg_num_end = t.bldg_num_end from temp t where t.bbl = l.bbl')
            engine.execute('drop table if exists temp')

    #print pd.read_sql_query('select count(*) cnt from lot_pts',engine).cnt[0],'\tTOTAL LOTS'
    #print pd.read_sql_query('select count(*) cnt from lot_pts where bldg_num_end is null',engine).cnt[0],'\tremaining lots without bldg_num_end'
def add_geoms_to_index():

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

    lion_ways = gd.read_postgis("select lw.gid,lw.clean_street,lw.streetcode,lw.geom from address_idx a "+
                                "inner join lion_ways lw on lw.clean_street = a.street",engine)
    print len(lion_ways),'total lion ways'
    uniq_streets = lion_ways.clean_street.unique().tolist()
    print len(uniq_streets),'uniq streets'
    uniq_streetcodes = lion_ways.streetcode.unique().tolist()
    print len(uniq_streetcodes),'uniq streetcodes'
    g = lion_ways.groupby('clean_street')
    t = []
    for name,grp in g:
        a=geom_txts_to_collection(grp.geom)
        T = { '1':a}
        cmd = """
        select st_astext(st_linefrommultipoint(st_boundary(st_unaryunion(
        %(1)s
        )))) this_line""".replace('\n',' ') % T
        this_line = pd.read_sql_query(cmd,engine).ix[0,'this_line']
        this_nid = pd.read_sql_query("select nid from address_idx where street = '%s' order by nid"%name,engine).ix[0,'nid']
        t.append({'street':name,
                  'nid':this_nid,
                  'geom':this_line})
    d = pd.DataFrame(t)
    engine.execute('drop table if exists temp')
    d.to_sql('temp',engine,if_exists='append',index=False)
    engine.execute('update address_idx a set geom = ST_GeomFromText(t.geom,4326) from temp t where t.nid = a.nid and t.street = a.street')
    engine.execute('drop table if exists temp')


def save_point_shape(fPath,x,y):

    schema = {
        'geometry': 'Point',
        'properties': {'id': 'int'},
    }

    pt_len = len(x)
    with fiona.open(fPath, 'w', 'ESRI Shapefile', schema) as c:
        for i in range(1,pt_len+1):
            c.write({
                'geometry': mapping(Point(x[i-1],y[i-1])),
                'properties': {'id': i},
            })
def save_polygon_shapefile():
    from osgeo import ogr

    # Here's an example Shapely geometry
    # poly = Polygon(zip(x_outer,y_outer))
    poly = poly_all.convex_hull

    # Now convert it to a shapefile with OGR
    driver = ogr.GetDriverByName('Esri Shapefile')
    ds = driver.CreateDataSource('/Users/admin/Projects/GIS/outer_MN.shp')
    layer = ds.CreateLayer('', None, ogr.wkbPolygon)
    # Add one attribute
    layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
    defn = layer.GetLayerDefn()

    ## If there are multiple geometries, put the "for" loop here

    # Create a new feature (attribute and geometry)
    feat = ogr.Feature(defn)
    feat.SetField('id', 123)

    # Make a geometry, from Shapely object
    geom = ogr.CreateGeometryFromWkb(poly.wkb)
    feat.SetGeometry(geom)

    layer.CreateFeature(feat)
    feat = geom = None  # destroy these

    # Save and close everything
    ds = layer = feat = geom = None
def polygon_from_points():
    #Create polygon from lists of points
    from_nodes = pd.read_sql_query("SELECT lat,lon FROM lion_nodes",engine)
    x = from_nodes.lon.tolist()
    y = from_nodes.lat.tolist()
    poly_all = Polygon(zip(x,y))

    # Extract the point values that define the perimeter of the polygon
    # x_outer,y_outer = poly_all.exterior.coords.xy
def plot_pluto_block(block):
    # 121 madison is on block 860
    m = gd.read_postgis("SELECT * FROM pluto where block = "+block+'"',conn)
    m.plot()
def geoms_to_text(geoms):
    if type(geoms) != list: geoms=[geoms]
    s=''
    for it in geoms:
        try:
            s+="ST_GeomFromText('"+it.to_wkt()+"',4326),"
        except:
            s+="ST_GeomFromText('"+it+"',4326),"
    return s.rstrip(',')
def geoms_as_text(geoms):
    if type(geoms) != list: geoms=[geoms]
    s=''
    for it in geoms:
        s+="ST_AsText("+it+"),"
    return s.rstrip(',')
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
    return cmd

def lion_node_changes1():
    t = 'lion_nodes'
    ####Get all unique lion_node ids with a Manhattan boolean attribute
    # select_lion = pd.read_hdf(BASE_SAVE_PATH+t+'_select.h5', 'table')
    # uniq_nodes = np.unique(np.array(select_lion.nodeidfrom.unique().tolist()+
    #                                 select_lion.nodeidto.unique().tolist())).tolist()
    ####Add Manhattan Column/Attribute to lion_nodes
    # ADD COLUMN
    cmd = "ALTER TABLE "+t+" ADD COLUMN manhattan boolean"
    # sql_cmd(cmd,engine)

    # ADD ATTRIBUTE
    cmd = ("UPDATE "+t+" SET manhattan = True "+
           "WHERE "+t+".nodeid IN "+
           str(uniq_nodes).replace("[u'","('").replace("u'","'").replace(']',')'))
    # sql_cmd(cmd,engine)
    ####Reduce Nodes in lion_nodes
    cmd="select gid,nodeid,geom from lion_nodes where lion_nodes.manhattan is true"
    with_MN=pd.read_sql_query(cmd,engine)
    print 'with_MN',len(with_MN.index)

    cmd="select gid,nodeid,geom from lion_nodes where lion_nodes.manhattan is not true"
    without_MN=pd.read_sql_query(cmd,engine)
    print 'without_MN',len(without_MN.index)

    cmd="select count(*) from lion_nodes"
    lion_cnt = pd.read_sql_query(cmd,engine)
    print 'lion_cnt',lion_cnt.ix[0,0]

    if lion_cnt.ix[0,0] - (len(with_MN.index) + len(without_MN.index)) == 0:
        print "with_MN + without_MN = lion_cnt"

        # drop column vintersect
        cmd="ALTER TABLE lion_nodes DROP COLUMN vintersect"
        # sql_cmd(cmd,engine)

        # delete without_MN
        cmd="DELETE FROM lion_nodes WHERE lion_nodes.manhattan is not true"
        # sql_cmd(cmd,engine)


    #     Keep only lion_ways
    #     where either lion_ways.nodeIDFrom or lion_ways.nodeIDTo
    #     are in ARRAY(lion_nodes.nodeid),
    #     i.e., lion_nodes.manhattan is True

    #     Note the format for "lion_nodes.nodeid" was numeric(10),
    #     whereas the format for "lion_ways.nodeidfrom" was char(254)

    ### NOTE:

    # Another way to do this:
    #
    # 1. load layer in QGIS,
    # 2. Click Database --> DB Manager,
    # 3. run sql "select gid,nodeid,vintersect,geom from lion_nodes where lion_nodes.manhattan is true", and
    # 4. create new layer and re-import.
def lion_nodes_changes2():
    ####Remove Nodes from "lion_nodes" based on changed "lion_ways"
    nodes_from_lion_nodes = pd.read_sql_query("SELECT nodeid FROM lion_nodes",engine)
    nodes_from_lion_ways = pd.read_sql_query("SELECT nodeidfrom,nodeidto FROM lion_ways",engine)

    check_nodes = nodes_from_lion_nodes.nodeid.map(int)
    good_nodes = nodes_from_lion_ways.nodeidfrom.map(int).append(nodes_from_lion_ways.nodeidto.map(int))

    check_nodes = pd.Series(check_nodes.unique())
    good_nodes = good_nodes.unique().tolist()

    bool_check = check_nodes.isin(good_nodes)
    df = pd.DataFrame({'nodes':check_nodes,'good':bool_check})
    nodes_to_remove = df[(df.good==False)].nodes.tolist()
    print len(nodes_from_lion_nodes.nodeid),'\t','total nodes'
    print len(nodes_to_remove),'\t','nodes to remove'

    # ## Finally, did a quick in QGIS, the marked nodes were ripe for removal, and the DB was updated via pgAdmin3 query:
    #
    #     DELETE FROM lion_nodes WHERE lion_nodes.remove IS True;
    #
    # ## Also, added coordinates (lat,long) to "lion_nodes"
    #
    #     ALTER TABLE lion_nodes ADD COLUMN lat float
    #     ALTER TABLE lion_nodes ADD COLUMN lon float
    #
    #     UPDATE lion_nodes SET lat = ST_Y(geom)
    #     UPDATE lion_nodes SET lon = ST_X(geom)
def pluto_changes():
    ##Pluto -- Alter Table and Add Columns

    # Create Index on pluto.address:
    #
    #     CREATE INDEX pluto_addr_idx ON pluto("address");
    #
    # Add Columns for building number and street:
    #
    #     ALTER TABLE pluto ADD COLUMN "bldg_num" integer;
    #     ALTER TABLE pluto ADD COLUMN "bldg_street" character varying (28);

    df = pd.read_sql_query("select gid,address,bldg_num,bldg_street from pluto;",conn)
    print '\n'
    print len(df.index),'\t','Total Addresses (slash geometries?)'
    df['isdigit']=df.bldg_num.map(lambda s: str(s).isdigit())
    a = df[(df.isdigit==True)&(df.bldg_num!=0)]
    print len(a.index),'\t','Buildings with Street Numbers'
    print len(df.index)-len(a.index),'\t','Difference'

    a['num'] = a.bldg_num.map(int)
    a.drop(['bldg_num','isdigit'],axis=1,inplace=True)
    a = a.rename(columns={'num':'bldg_num'})

    a['street'] = a.address.map(lambda s: s[s.find(' ')+1:].lower())
    a.drop(['bldg_street'],axis=1,inplace=True)
    a = a.rename(columns={'street':'bldg_street'})

    output = a
    print '\n',output.head()
    output.dtypes
    output.to_sql('pluto_info',engine,if_exists='append',index=False,index_label='gid')
def lion_ways_changes1():
    t='lion_ways'
    ####Remove All Non-Manhattan Entries:
    all_ways = sql_cmd("select count(*) from "+t,engine).fetchall()[0][0]
    mn_ways = sql_cmd("select count(*) from lion_ways where left( lion_ways.streetcode, 1 )  = '1'",engine).fetchall()[0][0]
    non_mn_ways = sql_cmd("select count(*) from lion_ways where left( lion_ways.streetcode, 1 )  != '1'",engine).fetchall()[0][0]
    print 'Total "'+t+'" \t=',all_ways
    print '\t'+'in Manhattan \t=',mn_ways
    print '\t'+'non-Manhattan \t=',non_mn_ways
    print '\t'+'TOTAL in & non \t=',mn_ways + non_mn_ways

    if mn_ways + non_mn_ways == all_ways:
        cmd = ("DELETE FROM "+t+" WHERE LEFT( lion_ways.streetcode, 1 )  != '1';")
    #     sql_cmd(cmd,engine)
        print '\n'+'DATA REMOVED from "'+t+'"'
        new_all_ways = sql_cmd("select count(*) from "+t,engine).fetchall()[0][0]
        print '\n'+'Total "'+t+'" \t=',new_all_ways

    all_ways = sql_cmd("select count(*) from "+t,engine).fetchall()[0][0]
    marked_ways = sql_cmd("select count(*) from lion_ways WHERE lion_ways.featuretyp IN ('1','2','3','7')",engine).fetchall()[0][0]
    remaining_ways = sql_cmd("select count(*) from lion_ways WHERE lion_ways.featuretyp NOT IN ('1','2','3','7')",engine).fetchall()[0][0]
    print 'Total "'+t+'" \t=',all_ways
    print '\t'+'marked \t\t=',marked_ways
    print '\t'+'remaining \t=',remaining_ways
    print '\t'+'SUM TOTAL \t=',marked_ways + remaining_ways

    if marked_ways + remaining_ways == all_ways:
        cmd = ("DELETE FROM "+t+" WHERE lion_ways.featuretyp IN ('1','2','3','7')")
    #     sql_cmd(cmd,engine)
        print '\n'+'DATA REMOVED from "'+t+'"'
        new_all_ways = sql_cmd("select count(*) from "+t,engine).fetchall()[0][0]
        print '\n'+'Total "'+t+'" \t=',new_all_ways
def add_clean_street_to_lion_ways():
    lw = pd.read_sql_query("select lw.gid,lw.street from lion_ways lw",engine)
    lw = geoparse(lw,'street','clean_street')
    engine.execute('drop table if exists temp')
    lw.to_sql('temp',engine,if_exists='append',index=False)
    engine.execute('update lion_ways lw set clean_street = t.clean_street from temp t where t.gid = lw.gid')
    engine.execute('drop table if exists temp')
def reduce_ways():
    ##Reduce Ways_vertices_pgr

    # Here, trying to reduce OSM data by using convex hull of pluto to find points outside of the hull and set remove to true.

    pts = gd.read_postgis("SELECT id gid,the_geom geom FROM ways_vertices_pgr",conn)
    f = '/Users/admin/Projects/GIS/map_data/MN_pluto_lines_hull.shp'
    hull = gd.GeoDataFrame.from_file(f)

    #####Executed these SQL queries in QGIS:

        # ALTER TABLE ways_vertices_pgr ADD COLUMN "remove" boolean;
        # UPDATE ways_vertices_pgr SET remove = False;

def postgres_plotting():
    ##Plotting

    # from pylab import *
    import matplotlib.pyplot as plt
    from matplotlib.collections import PatchCollection
    from mpl_toolkits.basemap import Basemap
    from shapely.geometry import Point, MultiPoint, MultiPolygon
    from descartes import PolygonPatch
    b = hull.bounds.ix[0,:]
    ####Make subplot for hull
    minx, maxx, miny, maxy = b['minx'], b['maxx'], b['miny'], b['maxy']
    w, h = maxx - minx, maxy - miny
    fig = plt.figure(figsize=(w*1.2,h*1.2))
    ax = fig.add_axes([minx - 0.2, miny - 0.1, w, h])
    patches = [PolygonPatch(hull.geometry[0],fc='#cc00cc', ec='#555555', alpha=0.5, zorder=4)]
    ax.add_collection(PatchCollection(patches, match_original=True));
    ####Make subplot for way_vertices
    x,y = zip(*pts.geom.map(lambda s: s.coords[0]))
    T = pd.DataFrame({'lon': x ,'lat' : y })
    slim_T = T[(minx<=T.lon)&(T.lon<=maxx)&(miny<=T.lat)&(T.lat<=maxy)]
    a=len(T.index)
    b=len(slim_T.index)
    print 'Total Way Vertices','\t',a
    print 'Way Vertices in hull','\t',b

    ax2 = fig.add_subplot(222)
    ax2.plot(slim_T.lon, slim_T.lat, 'r')

    # main figure
    ax2.set_xlabel('long.')
    ax2.set_ylabel('lat.')
    ax2.set_title('OSM Pts in Pluto')
    plt.show();
def enable_pg_routing_with_nyc_data():
    ### Enable pgRouting for NYC Data

    ## create new table for routing:
    cmd1 = "CREATE SEQUENCE mn_ways_gid_seq START 1;"
    cmd2 = """create table mn_ways (
                gid integer NOT NULL DEFAULT nextval('mn_ways_gid_seq'::regclass),
                length double precision,
                name text,
                x1 double precision,
                y1 double precision,
                x2 double precision,
                y2 double precision,
                reverse_cost double precision,
                rule text,
                to_cost double precision,
                maxspeed_forward integer,
                maxspeed_backward integer,
                osm_id bigint,
                priority double precision DEFAULT 1,
                the_geom geometry(LineString,4326),
                source integer,
                target integer,
                CONSTRAINT pk_mn_ways PRIMARY KEY (gid)
            );""".replace('\n','')
    # engine.execute(cmd1)
    # engine.execute(cmd2)

    ## add simplified geom data from lion_ways

    # uniq_streets = pd.read_sql_query("select street streets from lion_ways",engine).streets.unique().tolist()
    # print len(uniq_streets)
    # i=1
    # for u_st in uniq_streets[1:]:
    #     print i,u_st
    #     cmd = ("insert into mn_ways (the_geom) "+
    #            "select (st_dump( st_unaryunion( st_collect(l.geom) ) ) ).geom "+
    #            "from lion_ways l where l.street = '"+u_st+"'")
    #     engine.execute(cmd)
    #     i+=1

    ## add length  ( in meters...)  (divide by 0.3048)
    # engine.execute("UPDATE mn_ways SET length = "+
    #                "ST_Length_Spheroid(the_geom,'SPHEROID["+
    #                '"'+"WGS 84"+'"'+",6378137,298.257223563]')::DOUBLE PRECISION;")


    ## create table for nodes (b/c nodes will be generated)
    # used createtopo but wanted to use nodenetwork
    # engine.execute("SELECT pgr_nodenetwork         ('mn_ways', 0.00001,'the_geom','gid');") # need to fix

    # also, see
        # pgr_nodenetwork(text, double precision, text, text, text)
        # pgr_createverticestable(edge_table, the_geom, source, target, row_where)

    ## create topology
    # engine.execute("SELECT pgr_createTopology('mn_ways', 0.00001, 'the_geom', 'gid');")

    ## add indicies
    # engine.execute('CREATE INDEX mn_source_idx ON mn_ways("source");')
    # engine.execute('CREATE INDEX mn_target_idx ON mn_ways("target");')

    ## add cost column
    # engine.execute('UPDATE mn_ways SET reverse_cost = length;')
def use_USPS_street_abbr_as_nyc_street_names():
    ###Use USPS Street Abbr. as map for NYC Street Names (unsuccessful)

    from regex import sub as re_sub
    from regex import escape as re_escape

    def multisub(subs, subject):
        "Simultaneously perform all substitutions on the subject string."
        pattern = '|'.join('(%s)' % p for p, s in subs)
    #     print pattern
        substs = [s for p, s in subs]
    #     print substs
        replace = lambda m: ' '+substs[m.lastindex - 1]+' '
        return re_sub('\s?'+pattern+'\s?', replace, subject)

        # multisub([('hi', 'bye'), ('bye', 'hi')], 'hi and bye')
        # returns 'bye and hi'
    # multisub(X,'1 AVENUE LOWER NB ROADBED'.lower())

    # fpath_abbr = SND_NON_S_PATH.replace('snd14Bcow_non_s_recs','usps_street_abbr')
    # u = pd.read_csv(fpath_abbr,index_col=0)
    # fpath_abbr_regex = fpath_abbr.replace('.csv','_regex.csv')
    # df = pd.read_csv(fpath_abbr_regex,index_col=0)
    # print len(u),len(df)

    # g = u.groupby('prim_suff')
    # df = pd.DataFrame({'prim_suff':g.groups.keys()}).sort('prim_suff').reset_index(drop=True)

    # suff_abbr_map = dict(zip(u.prim_suff.tolist(),u.usps_abbr.tolist()))
    # df['usps_abbr'] = df.prim_suff.map(suff_abbr_map)

    # f = lambda s: str(g.get_group(s).common_use.map(lambda s: s.lower()).tolist()).strip(' ').replace(', ',' | ').replace("'",'').strip('[]')
    # df['pattern'] = df.prim_suff.map(f)
    # df['combined'] = df.ix[:,['pattern','usps_abbr']].apply(lambda s: (s[0],s[1].lower()),axis=1)
    # usps_repl_list = df.combined.tolist()


    # regex_repl_path = '/Users/admin/Projects/GIS/table_data/usps_street_abbr_regex.txt'
    # f = open(regex_repl_path,'r')
    # usps_repl_list = f.read().split('\n')
    # f.close()

    tmp = d.ix[:50,:]
    tmp['clean2'] = tmp.full_stname.map(lambda s: multisub(usps_repl_list,s.lower()))
    tmp.ix[:,['full_stname','clean_name','clean2']]

def combine_east_west():
    ### Combine East/West Streets
    a = gd.read_postgis("select street,geom from address_idx where geom is not null",engine)

    ns = num_streets = a[a.street.str.contains('(^e\s[0-9])|(^w\s[0-9])')==True]
    ns['num'] = ns.street.map(lambda s: eval(re_search(r'([0-9]+)',s).groups()[0]))
    ns['below60'] = ns.num.map(lambda d: True if d<60 else False)
    ns.head()
    east_streets = ns[(ns.street.str.contains('^e\s[0-9]')==True)&(ns.below60==True)].sort('num').reset_index(drop=True)
    west_streets = ns[(ns.street.str.contains('^w\s[0-9]')==True)&(ns.below60==True)].sort('num').reset_index(drop=True)
    east_num_geom_map = dict(zip(east_streets.num.tolist(),east_streets.geom.tolist()))
    west_num_geom_map = dict(zip(west_streets.num.tolist(),west_streets.geom.tolist()))
    east_keys,west_keys = east_num_geom_map.keys(),west_num_geom_map.keys()
    save_for_later = []
    for it in east_keys:
        if west_keys.count(it)==0:
            save_for_later.append({'street_names':str(it)+' st',
                                   'geom':east_num_geom_map.pop(it)})

    for it in west_keys:
        if east_keys.count(it)==0:
            save_for_later.append({'street_names':str(it)+' st',
                                   'geom':east_num_geom_map.pop(it)})
    east_keys,west_keys = east_num_geom_map.keys(),west_num_geom_map.keys()
    east_streets = east_streets[east_streets.num.isin(east_keys)].sort('num').reset_index(drop=True)
    west_streets = west_streets[west_streets.num.isin(west_keys)].sort('num').reset_index(drop=True)
    print len(east_streets),len(west_streets)
    print east_streets.head()
    print west_streets.head()

    cs = combined_streets = pd.DataFrame({'street':east_streets.street.map(lambda s: s.replace('e ','')).tolist(),
                                          'east':east_streets.geom.tolist(),
                                          'west':west_streets.geom.tolist()})
    cs = cs.ix[:,['street','west','east']]
    cs['west'] = cs.west.map(str)
    cs['east'] = cs.east.map(str)

    g = cs.ix[:,['west','east']].as_matrix()
    T = { '1':'street',
          'street_names':str(east_streets.street.map(lambda s: s.replace('e ','')).tolist()).replace("u'","'").strip('[]'),
          '2':'streets',
          'streets':str(g).replace(")'\n  '",")<.>").replace("']\n [ '","', '").strip('[]')}
    cmd =   """
            SELECT
                %(1)s[i],
                st_makeline(
                    st_geomfromtext((string_to_array(%(2)s[i],'<.>'))[1]),
                    st_geomfromtext((string_to_array(%(2)s[i],'<.>'))[2])
                ) geom
            FROM (
                SELECT generate_series(1, array_upper(%(2)s, 1)) AS i, %(2)s, %(1)s
                FROM
                    (SELECT array[%(street_names)s] %(1)s) as %(1)s,
                    (SELECT array[%(streets)s] %(2)s) as %(2)s
                ) t
            """.replace('\n',' ') % T

    g = gd.read_postgis(cmd,engine)

    nid_start = 1+pd.read_sql_query("select nid from address_idx order by nid desc limit 1",engine).nid.tolist()[0]
    g['nid'] = range(nid_start,nid_start+len(g))
    g['geom'] = g.geom.map(str)

    engine.execute('drop table if exists temp')
    g.to_sql('temp',engine,if_exists='append',index=False)
    engine.execute('INSERT INTO address_idx (street, nid, geom) select street, nid, st_geomfromtext(geom,4326) from temp')
    engine.execute('drop table if exists temp')

def compare_lion_ways_content():
    ### Read Lion Ways from DB/File
    current_db,new_db = 'lion_ways','lion_ways2'
    conditions = [" where specaddr is null",
                  ' and (lboro = 1 or rboro=1) ',
                  " and segmenttyp != 'R' "]

    # cols = ['gid','street','safstreetn','featuretyp','segmenttyp','rb_layer',
    #    'specaddr','facecode','seqnum','streetcode','safstreetc','geom']

    cmd = "select %(1)s from %(3)s %(2)s" % \
            { '1' : '*',#','.join(cols),
              '2' : ''.join(conditions),
              '3' : current_db}
    a1 = gd.read_postgis(cmd,engine)

    cmd2 = "select %(1)s from %(3)s %(2)s" % \
            { '1' : '*',#','.join(cols),
              '2' : ''.join(conditions),
              '3' : new_db}
    a2 = gd.read_postgis(cmd,engine)
    ### Comparing Overlapping Streets
    uniq_geoms = a2.geom.map(lambda s: str(s)).unique().tolist()
    all_str_geoms = a2.geom.map(lambda s: str(s)).tolist()
    print '\nUnique Geoms, All Geoms, (difference)'
    print len(uniq_geoms),len(all_str_geoms),len(all_str_geoms)-len(uniq_geoms),'\n'
    a2['cnt'] = a2.geom.map(lambda s: all_str_geoms.count(str(s)))
    a2['str_geom'] = a2.geom.map(lambda s: str(s))
    A=a2[a2.cnt>1].sort(['str_geom','gid'],ascending=[True,True])
    G = A.groupby('str_geom')
    K = G.groups.keys()
    print len(K),'groups of matching geoms being checked...\n'
    rem_cols = ['gid','llo_hyphen','lhi_hyphen','rlo_hyphen','rhi_hyphen','fromleft','toleft','fromright','toright']
    skip_these_gid = []#[99689,104049,
    #                   99686,104048,]
    skip_these_streets = ['BIKE PATH']
    end_msg,t=True,[]
    for grp in K:
        r = G.get_group(grp).reset_index(drop=True)
        R1 = r.drop(rem_cols,axis=1).ix[0,:].to_dict()
        R2 = r.drop(rem_cols,axis=1).ix[1,:].to_dict()
        if R1!=R2:
            if (len(r[r.gid.isin(skip_these_gid)==False])>0 &
                len(r[r.street.isin(skip_these_streets)==False])>1):
                j=R1.keys()
                for it in j:
                    if str(R1[it])!=str(R2[it]):
                        print K.index(grp)
                        print it
                        print R1[it]
                        print R2[it]
                        end_msg=False
                        break
        t.append(r.ix[1,'gid'])

    l=pd.DataFrame({'gid':t,'geom':None})
    engine.execute('drop table if exists temp')
    l.to_sql('temp',engine,if_exists='append',index=False)
    engine.execute("update lion_ways l set geom = t.geom from temp t where t.gid = l.gid")
    engine.execute('drop table if exists temp')
    end_msg=True
    if end_msg==True:
        print 'Between',current_db,'and',new_db,'with the conditions:\n'
        for it in conditions:
            print '-',it
        print '\nThe only differences between rows were in columns:\n'
        for it in rem_cols:
            print '-',it
        print '\n',len(t),'rows had geoms stripped\n'





class ST_Parts:

    def __init__(self):


        ST_STRIP_BEFORE_DICT    =   {
                                    r'(,|"|'+r"')"                  :r'',
                                    r'(\s){2,}'                     :r' ',
                                    r'(?P<num>[0-9])(\s)(th)'       :r'\g<num>th',
                                    }

        ST_PREFIX_DICT = {  r'east'         :r'e',
                            r'north'        :r'n',
                            r'south'        :r's',
                            r'west'         :r'w',
                            }

        ST_SUFFIX_DICT = {  'alley'         :r'aly',
                            'avenue'        :r'ave',
                            'boulevard'     :r'blvd',
                            'circle'        :r'cir',
                            'court'         :r'ct',
                            'drive'         :r'dr',
                            'east'          :r'e',
                            'highway'       :r'hwy',
                            'island'        :r'isle',
                            'lane'          :r'ln',
                            'market'        :r'mkt',
                            'north'         :r'n',
                            'parkway'       :r'pkwy',
                            'place'         :r'pl',
                            'plaza'         :r'plz',
                            'road'          :r'rd',
                            'south'         :r's',
                            'square'        :r'sq',
                            'street'        :r'st',
                            'terrace'       :r'ter',
                            'west'          :r'w',
                            }

        ST_BODY_DICT = {    r'\s(north)\s'          :r' n ',
                            r'\s(south)\s'          :r' s ',
                            r'\s(west)\s'           :r' w ',
                            r'\s(east)\s'           :r' e ',
                            r'\s(avenue)\s'         :r' ave ',
                            r'\s(place)\s'          :r' pl ',
                            r'\s(square)\s'         :r' sq ',
                            r'\s(terrace)\s'        :r' ter ',

                            r'(1st|first)'          :r'1',
                            r'(2nd|second)'         :r'2',
                            r'(3rd|third)'          :r'3',
                            r'(4th|fourth)'         :r'4',
                            r'(5th|fifth)'          :r'5',
                            r'(6th|sixth)'          :r'6',
                            r'(7th|seventh)'        :r'7',
                            r'(8th|eigth)'          :r'8',
                            r'(9th|nineth|ninth)'   :r'9',
                            r'(0th)'                :r'0',
                            r'(1th)'                :r'1',
                            r'(2th)'                :r'2',
                            r'(3th)'                :r'3',

                            r'(tenth)'              :r'10',
                            r'(eleventh)'           :r'11',
                            r'(twelth|twelfth)'     :r'12',

                            r'(ave[nues]*)\s(of)(\s(the))?\s(amer[icas]*)$'       :r'6 ave',

                            r'^(st.|st)\s'           :r'saint ',
                            r'^fort\s'               :r'ft ',
                            r'^f\sd\sr\s'            :r'fdr ',

                            }

        ST_STRIP_AFTER_DICT =   {
                                r'(\.|,|\-)'         :r'',
                                }
        self.ST_STRIP_BEFORE_DICT       =   ST_STRIP_BEFORE_DICT
        self.ST_PREFIX_DICT             =   ST_PREFIX_DICT
        self.ST_SUFFIX_DICT             =   ST_SUFFIX_DICT
        self.ST_BODY_DICT               =   ST_BODY_DICT
        self.ST_STRIP_AFTER_DICT        =   ST_STRIP_AFTER_DICT





class pgSQL_Functions:
    """

    NOTE: USE plpythonu and plluau for WRITE ACESS

    """


    def __init__(self):
        self.Make                       =   self.Make()
        self.Run                        =   self.Run()

    class Run:

        def __init__(self):
            self.Run                    =   self

        def make_column_primary_serial_key(self,table_name,uid_col,is_new_col=True):
            """
            Usage: make_column_primary_serial_key('table_name','uid_col',is_new_col=True)
            """
            T                           =   {'tbl'                  :   table_name,
                                             'uid_col'              :   uid_col,
                                             'is_new_col'           :   is_new_col}
            cmd                         =   """select z_make_column_primary_serial_key( '%(tbl)s',
                                                                                        '%(uid_col)s',
                                                                                         %(is_new_col)s );
                                            """ % T
            conn.set_isolation_level(       0)
            cur.execute(                    cmd)

    class Make:

        def __init__(self):
            pass


        def z_make_column_primary_serial_key(self):
            """

            Usage:

                select z_make_column_primary_serial_key({table_name}::text,
                                                        {col_name}::text,
                                                        {BOOL_is_new_col}::boolean)


            """
            T = {'tbl'      :   '%(tbl)s',
                 'uid_col'  :   '%(uid_col)s',
                 'T'        :   '% T'}
            cmd=""" CREATE OR REPLACE FUNCTION public.z_make_column_primary_serial_key(
                        table_name text,
                        col_name text,
                        new_col boolean)
                    RETURNS text AS
                    $BODY$

                        T = {'tbl':table_name,'uid_col':col_name}
                        if new_col:
                            p0 = "ALTER TABLE %(tbl)s ADD COLUMN %(uid_col)s SERIAL;" %(T)s
                            e = plpy.execute(p0)


                        p1 = "UPDATE %(tbl)s SET %(uid_col)s = nextval(pg_get_serial_sequence('%(tbl)s','%(uid_col)s'))" %(T)s
                        e = plpy.execute(p1)

                        p2 = "ALTER TABLE %(tbl)s ADD PRIMARY KEY (%(uid_col)s)" %(T)s
                        e = plpy.execute(p2)

                        return 'ok'

                    $BODY$
                    LANGUAGE plpythonu
                """ % T
            conn.set_isolation_level(       0)
            cur.execute(                    cmd)
        def z_get_way_between_ways(self):
            cmd="""CREATE OR REPLACE FUNCTION
                    z_get_way_between_ways( IN get_way text, in ways1 text,
                                            IN ways2 text, out geom_res geometry(LineString,4326))
                     AS $$
                    begin
                        select st_line_substring(line1,arr[1],arr[2]) into geom_res
                        from (
                            select line1, array_sort(array[pt1, pt2]) arr
                            from (
                                select
                                    line1,
                                    st_line_locate_point(line1,z_intersection_point_bin(get_way,ways1)) pt1,
                                    st_line_locate_point(line1,z_intersection_point_bin(get_way,ways2)) pt2
                                from
                                    (select geom line1 from address_idx where street = get_way limit 1) as l1
                            ) as t
                        ) as t;
                    end;
                    $$ language plpgsql;
                """.replace('\n','')
            engine.execute(cmd)
        def z_intersection_point(self):
            cmd="""
                DROP FUNCTION z_intersection_point(text,text);
                CREATE OR REPLACE FUNCTION z_intersection_point(IN way1 text, IN way2 text)
                  RETURNS text AS $$
                declare
                    _geom geometry; geom_type text;
                begin
                    select st_intersection(line1,line2) into _geom
                    from
                        (select geom line1 from address_idx where street = way1 limit 1) as _line1,
                        (select geom line2 from address_idx where street = way2 limit 1) as _line2;
                    select geometrytype(_geom) into geom_type;
                    if geom_type = 'LINESTRING' then
                        return st_astext(st_line_interpolate_point(_geom,0.5));
                    elsif geom_type = 'POINT' then
                        return st_astext(_geom);
                    end if;
                end;
                $$ language plpgsql;
                """.replace('\n','')
            engine.execute(cmd)
        def z_get_way_box(self):
            cmd="""
                CREATE OR REPLACE FUNCTION
                z_get_way_box( IN way1 text, in way2 text, in way3 text, in way4 text, out geom_res geometry(Polygon,4326))
                AS $$
                begin

                    select st_makepolygon(st_linemerge(st_collect(array[
                    z_get_way_between_ways(way1,way2,way4),
                    z_get_way_between_ways(way2,way1,way3),
                    z_get_way_between_ways(way3,way2,way4),
                    z_get_way_between_ways(way4,way1,way3)
                    ]))) into geom_res;

                end;
                $$ language plpgsql;
                """.replace('\n','')
            conn.set_isolation_level(       0)
            cur.execute(                    cmd)
        def z_parse_NY_addrs(self):
            T = {'fct_name'                 :   'z_parse_NY_addrs',
                 'fct_args_types'           :   [ ['','query_str','text'],],
                 'fct_return'               :   'SETOF parsed_addr',
                 'fct_lang'                 :   'plpythonu',
                 'cmt'                      :   """ Example:  ''select
                                                                    orig_addr,num,predir,name,suftype,
                                                                    city,state,zip
                                                                from z_parse_NY_addrs(''pluto'',''address'',''zipcode'',100);'' """}
            T.update( {'fct_args'           :   ', '.join([' '.join(j) for j in T['fct_args_types']]),
                       'fct_types'          :   ', '.join([j[2] for j in T['fct_args_types'] if j[0].upper()!='OUT']),
                       })

            for it in T['fct_args'].split(','):
                arg=it.strip().split(' ')[0]
                T.update({arg:arg})

            a="""

                DROP TYPE IF EXISTS parsed_addr CASCADE;
                DROP FUNCTION IF EXISTS %(fct_name)s( %(fct_types)s );

                CREATE TYPE parsed_addr AS (
                    src_gid integer,
                    orig_addr character varying,
                    bldg text,
                    num text,
                    pretype text,
                    predir text,
                    name text,
                    suftype text,
                    sufdir text,
                    city text,
                    state text,
                    zip text
                );


                CREATE OR REPLACE FUNCTION public.%(fct_name)s( %(fct_args)s )
                RETURNS %(fct_return)s
                AS $$

                    query_dict = {   '_QUERY_STR'        :   query_str.replace('####','##'), }
                    q=\"\"\"
                        select  src_gid,
                                orig_addr,
                                (_parsed).building bldg,
                                (_parsed).house_num num,
                                (_parsed).pretype,
                                (_parsed).predir,
                                regexp_replace( (_parsed).name,'(.*)(QQQQ)(.*)','\\1 \\3','g') as name,
                                (_parsed).suftype,
                                (_parsed).sufdir,
                                (_parsed).city,
                                (_parsed).state,
                                (_parsed).postcode zip
                        from
                            (
                            select  standardize_address('tiger.pagc_lex','tiger.pagc_gaz', 'tiger.pagc_rules',
                                        concat(f2.address,', New York, NY, ',f2.zipcode) ) _parsed,
                                    f2.orig_addr orig_addr,
                                    f2.src_gid src_gid

                                from
                                    (
                                    select
                                        z_custom_addr_pre_filter( f1.address ) address,
                                        f1.zipcode zipcode,
                                        f1.address orig_addr,
                                        f1.gid src_gid
                                    from
                                        (
                                        ##(_QUERY_STR)s
                                        ) as f1
                                    group by f1.address,f1.zipcode,f1.gid
                                    ) as f2
                            ) as f3;
                    \"\"\" ## query_dict

                    return plpy.execute(q)

                $$ LANGUAGE %(fct_lang)s;

            COMMENT ON FUNCTION public.%(fct_name)s(%(fct_types)s) IS '%(cmt)s';
            """ % T
            cmd                         =   a.replace('##','%')
            conn.set_isolation_level(       0)
            self.z_custom_addr_pre_filter()
            cur.execute(                    cmd)
        def z_custom_addr_pre_filter(self):
            """

            Most of these should really be systematically created from the NYC Street Name Dictionary (SND)

            See here: http://www.nyc.gov/html/dcp/html/bytes/applbyte.shtml#geocoding_application

            """
            cmd="""
                CREATE OR REPLACE FUNCTION public.z_custom_addr_pre_filter(addr text)
                RETURNS text AS $$

                    if addr==nil then
                        return
                    else
                        addr = addr:upper()
                    end

                    local cnt = addr:find( "^([0-9]*)([%-]*)([a-zA-Z0-9]*)%s([a-zA-Z0-9]*)(.*)" )
                    local no_num_cnt = addr:find("^([0-9]+)(.*)")
                    -- when first character not digit, EAST 76 STREET --> num=E 76,NAME=NEW YORK
                    -- when first character not digit, MARGINAL STREET --> NAME=ST NEW YORK
                    --


                    if ( cnt == 0 or cnt == nil or no_num_cnt == nil ) then
                        addr = "0|"..addr
                    else
                        addr = addr:gsub("^([0-9]*)([%-]*)([a-zA-Z0-9]*)%s([a-zA-Z0-9]*)(.*)","%1%2%3|%4 %5")
                    end

                    local cmd = [[select repl_from,repl_to
                            from regex_repl
                            where tag = 'custom_addr_pre_filter'
                            and is_active is true
                            order by run_order ASC]]

                    for row in server.rows(cmd) do
                        addr = string.gsub(addr,row.repl_from,row.repl_to)
                    end
                    return addr
                $$ LANGUAGE plluau;
            """
            conn.set_isolation_level(       0)
            cur.execute(                    cmd)

class pgSQL_Triggers:

    def __init__(self):
        self.Create                     =   self.Create()
        self.Destroy                    =   self.Destroy()

    class Create:
        def __init__(self):
            self.Create                 =   self
        def z_auto_add_primary_key(self):
            c                           =   """
                DROP FUNCTION if exists z_auto_add_primary_key();

                CREATE OR REPLACE FUNCTION z_auto_add_primary_key()
                  RETURNS event_trigger AS
                $BODY$
                DECLARE
                    has_index boolean;
                    tbl text;
                    _seq text;
                BEGIN
                    has_index = (select relhasindex from pg_class
                            where relnamespace=2200
                            and relkind='r'
                            order by oid desc limit 1);

                    IF (
                        pg_trigger_depth()=0
                        and has_index=False )
                    THEN
                        tbl = (select relname t from pg_class
                            where relnamespace=2200
                            and relkind='r'
                            order by oid desc limit 1);
                        _seq = format('%I_uid_seq',tbl);
                        execute format('alter table %I add column uid serial primary key',tbl);
                        execute format('alter table %I alter column uid set default z_next_free(
                                    ''%I'',
                                    ''uid'',
                                    ''%I'')',tbl,tbl,_seq);
                    end if;
                END;
                $BODY$
                  LANGUAGE plpgsql;


                DROP EVENT TRIGGER if exists missing_primary_key_trigger;

                CREATE EVENT TRIGGER missing_primary_key_trigger
                ON ddl command end
                WHEN TAG IN ('CREATE TABLE')
                EXECUTE PROCEDURE z_auto_add_primary_key();

                                                """
            conn.set_isolation_level(           0)
            cur.execute(                        c)
        def z_auto_add_last_updated_field(self):
            c                           =   """
                DROP FUNCTION if exists z_auto_add_last_updated_field() cascade;

                CREATE OR REPLACE FUNCTION z_auto_add_last_updated_field()
                  RETURNS event_trigger AS
                $BODY$
                DECLARE
                    last_table text;
                    has_last_updated boolean;


                BEGIN
                    last_table := (select relname from pg_class
                                 where relnamespace=2200
                                 and relkind='r'
                                 order by oid desc limit 1);

                    SELECT count(*)>0 INTO has_last_updated FROM information_schema.columns
                        where table_name='||quote_ident(last_table)||'
                        and column_name='last_updated';

                    IF (
                        pg_trigger_depth()=0
                        and has_last_updated=False )
                    THEN
                        execute format('alter table %I add column last_updated timestamp with time zone',last_table);
                    end if;

                END;
                $BODY$
                  LANGUAGE plpgsql;

                DROP EVENT TRIGGER if exists missing_last_updated_field;

                CREATE EVENT TRIGGER missing_last_updated_field
                ON ddl_command_end
                WHEN TAG IN ('CREATE TABLE')
                EXECUTE PROCEDURE z_auto_add_last_updated_field();
                                            """
            conn.set_isolation_level(0)
            cur.execute(c)

    class Destroy:
        def __init__(self):
            self.Destroy                =   self
        def z_auto_add_primary_key(self):
            c                           =   """
            DROP FUNCTION if exists
                z_auto_add_primary_key() cascade;

            DROP EVENT TRIGGER if exists missing_primary_key_trigger;
                                            """
            conn.set_isolation_level(0)
            cur.execute(c)
        def z_auto_add_last_updated_field(self):
            c                           =   """
            DROP FUNCTION if exists
                z_auto_add_last_updated_field() cascade;

            DROP EVENT TRIGGER if exists missing_last_updated_field;
                                            """
            conn.set_isolation_level(0)
            cur.execute(c)


class Tables:
    """

    Pluto:

        update pluto set address = regexp_replace(address,'F\sD\sR','FDR','g') where address ilike '%f d r%';


    """

    def __init__(self):
        self.Make                       =   self.Make()

    class Make:

        def __init__(self):
            pass


        def scrape_lattice(self,pt_buff_in_miles,lattice_table_name):
            meters_in_one_mile              =   1609.34

            z                               =   pd.read_sql("select min(lat) a,max(lat) b,min(lon) c,max(lon) d from lws_vertices_pgr",routing_eng)
            lat_min,lat_max,lon_min,lon_max =   z.a[0],z.b[0],z.c[0],z.d[0]
            lat_mid,lon_mid                 =   lat_min+((lat_max-lat_min)/float(2)),lon_min+((lon_max-lon_min)/float(2))
            lat_cmd                         =   """
                                                SELECT ST_Distance_Sphere(ptA,ptB) lat_dist
                                                from (SELECT ST_GeomFromText('POINT(%s %s)',4326) as ptA,
                                                             ST_GeomFromText('POINT(%s %s)',4326) as ptB) as foo;
                                                """%(str(lon_mid),str(lat_max),str(lon_mid),str(lat_min))
            lon_cmd                         =   """
                                                SELECT ST_Distance_Sphere(ptA,ptB) lon_dist
                                                from (SELECT ST_GeomFromText('POINT(%s %s)',4326) as ptA,
                                                             ST_GeomFromText('POINT(%s %s)',4326) as ptB) as foo;
                                                """%(str(lon_max),str(lat_mid),str(lon_min),str(lat_mid))
            lat_range                       =   pd.read_sql(lat_cmd,routing_eng).lat_dist[0] + (pt_buff_in_miles * meters_in_one_mile)
            lon_range                       =   pd.read_sql(lon_cmd,routing_eng).lon_dist[0] + (pt_buff_in_miles * meters_in_one_mile)
            lat_segs                        =   int(round(lat_range/float(pt_buff_in_miles * meters_in_one_mile),))
            lon_segs                        =   int(round(lon_range/float(pt_buff_in_miles * meters_in_one_mile),))

            lat_mid_distances               =   np.arange(0,lat_range,
                                                        pt_buff_in_miles * meters_in_one_mile)+((pt_buff_in_miles * meters_in_one_mile)/2)
            lon_mid_distances               =   np.arange(0,lon_range,
                                                        pt_buff_in_miles * meters_in_one_mile)+((pt_buff_in_miles * meters_in_one_mile)/2)

            # set starting point
            lat_d                           =   lat_mid_distances[0]
            lon_d                           =   lon_mid_distances[0]
            T                               =   {   'latt_tbl'          :   lattice_table_name,
                                                    'X'                 :   str(lon_min),
                                                    'Y'                 :   str(lat_min),
                                                    'sw_dist'           :   str(np.sqrt(lat_d**2 + lon_d**2)),
                                                    'sw_rad'            :   str(225)   }
            cmd                             =   """
                                                    select
                                                        st_x(sw_geom::geometry(Point,4326))  min_x,
                                                        st_y(sw_geom::geometry(Point,4326))  min_y
                                                    FROM
                                                        (select
                                                            ST_Project( st_geomfromtext('Point(%(X)s %(Y)s)',4326),
                                                                        %(sw_dist)s,
                                                                        radians(%(sw_rad)s)) sw_geom) as foo;

                                                """ % T
            min_x,min_y                     =   pd.read_sql(cmd,routing_eng).ix[0,['min_x','min_y']]

            # create lattice table
            conn.set_isolation_level(           0)
            cur.execute(                        """
                                                    DROP TABLE IF EXISTS %(latt_tbl)s;

                                                    CREATE TABLE %(latt_tbl)s (
                                                        gid             serial primary key,
                                                        x               double precision,
                                                        y               double precision,
                                                        bbl             numeric,
                                                        address         text,
                                                        zipcode         integer,
                                                        yelp_cnt        integer DEFAULT 0,
                                                        yelp_updated    timestamp with time zone,
                                                        sl_open_cnt     integer DEFAULT 0,
                                                        sl_closed_cnt   integer DEFAULT 0,
                                                        sl_updated      timestamp with time zone,
                                                        geom            geometry(Point,4326));

                                                    UPDATE %(latt_tbl)s
                                                    SET gid = nextval(pg_get_serial_sequence('%(latt_tbl)s','gid'));

                                                """ % T )



            # create and push X/Y points to pgsql -- set geom at end
            pt                              =   0
            for i in range(0,lat_segs):
                lat_d                       =   lat_mid_distances[i]
                for j in range(0,lon_segs):
                    lon_d                   =   lon_mid_distances[j]
                    T                       =   {   'table_name'        :lattice_table_name,
                                                    'X'                 :str(min_x),
                                                    'Y'                 :str(min_y),
                                                    'n_dist'            :str(lat_d),
                                                    'ne_dist'           :str(np.sqrt(lat_d**2 + lon_d**2)),
                                                    'e_dist'            :str(lon_d),
                                                    'n_rad'             :str(0),
                                                    'ne_rad'            :str(45),
                                                    'e_rad'             :str(90)   }
                    # (lat_min,lon_min) is southwest most point
                    # lattice created by moving northeast

                    ## North     azimuth 0       (0)
                    ## East      azimuth 90      (pi/2)
                    ## South     azimuth 180     (pi)
                    ## West      azimuth 270     (pi*1.5)
                    cmd                     =   """
                                                INSERT INTO %(table_name)s(x,y)
                                                    select
                                                        st_x(e_geom::geometry(Point,4326))  e_geom_x,
                                                        st_y(n_geom::geometry(Point,4326))  n_geom_y
                                                    FROM
                                                        (select
                                                            ST_Project( st_geomfromtext('Point(%(X)s %(Y)s)',4326),
                                                                        %(n_dist)s,
                                                                        radians(%(n_rad)s)) n_geom) as foo1,
                                                        (select
                                                            ST_Project( st_geomfromtext('Point(%(X)s %(Y)s)',4326),
                                                                        %(e_dist)s,
                                                                        radians(%(e_rad)s)) e_geom) as foo2;

                                                """.replace('\n','')%T
                    conn.set_isolation_level(   0)
                    cur.execute(                cmd)

            T                               =   {  'latt_tbl'           :   lattice_table_name,
                                                   'tmp_tbl'            :   'tmp_'+INSTANCE_GUID,
                                                   'tmp_tbl_2'          :   'tmp_'+INSTANCE_GUID+'_2',
                                                   'tmp_tbl_3'          :   'tmp_'+INSTANCE_GUID+'_3',
                                                   'buf_rad'            :   str(int((pt_buff_in_miles *
                                                                              meters_in_one_mile)/2.0))}

            conn.set_isolation_level(           0)
            cur.execute(                        """
                                                UPDATE %(latt_tbl)s SET geom = ST_SetSRID(ST_MakePoint(x,y), 4326);

                                                -- 1. Remove points outside geographic land boundary of manhattan

                                                DROP TABLE IF EXISTS %(tmp_tbl)s;

                                                CREATE TABLE %(tmp_tbl)s as
                                                select st_buffer(st_concavehull(all_pts,50)::geography,%(buf_rad)s)::geometry geom
                                                    from
                                                    (SELECT ST_Collect(f.the_geom) as all_pts
                                                        FROM (
                                                        SELECT (ST_Dump(geom)).geom as the_geom
                                                        FROM pluto_centroids)
                                                        as f)
                                                    as f1;

                                                delete from %(latt_tbl)s l
                                                using %(tmp_tbl)s t
                                                where not st_within(l.geom,t.geom);

                                                drop table %(tmp_tbl)s;


                                                -- 2. match lattice points with closest tax lots and collect addresses
                                                DROP TABLE IF EXISTS %(tmp_tbl_2)s;
                                                CREATE TABLE %(tmp_tbl_2)s as
                                                        SELECT st_collect(pc.geom) all_pts
                                                        FROM pluto_centroids pc
                                                        INNER JOIN pluto p on p.gid=pc.p_gid
                                                        WHERE NOT p.zipcode=0
                                                        AND p.real_address is true;


                                                DROP TABLE IF EXISTS %(tmp_tbl_3)s;
                                                CREATE TABLE %(tmp_tbl_3)s as
                                                WITH res AS (
                                                    SELECT
                                                        l.gid l_gid,
                                                        st_closestpoint(t.all_pts,l.geom) t_geom,
                                                        ROW_NUMBER() OVER(PARTITION BY l.geom
                                                                          ORDER BY st_closestpoint(t.all_pts,l.geom) DESC) AS rk
                                                    FROM %(latt_tbl)s l,%(tmp_tbl_2)s t
                                                    )
                                                SELECT s.l_gid l_gid,p.gid p_gid
                                                    FROM res s
                                                    INNER JOIN pluto_centroids pc on pc.geom=s.t_geom
                                                    INNER JOIN pluto p on p.gid=pc.p_gid
                                                    WHERE s.rk = 1;


                                                update %(latt_tbl)s l
                                                set
                                                    address = p.address,
                                                    bbl = p.bbl,
                                                    zipcode = p.zipcode
                                                from %(tmp_tbl_3)s t
                                                INNER JOIN pluto p on p.gid=t.p_gid
                                                WHERE t.l_gid = l.gid;

                                                drop table %(tmp_tbl_3)s;
                                                drop table %(tmp_tbl_2)s;


                                                -- 3. remove lattice points furthest from tax lot having duplicate BBL values
                                                DROP TABLE IF EXISTS %(tmp_tbl_2)s;
                                                CREATE TABLE %(tmp_tbl_2)s as
                                                    WITH res AS (
                                                        SELECT
                                                            l.gid l_gid,
                                                            ROW_NUMBER() OVER(PARTITION BY l.bbl
                                                                              ORDER BY st_distance(pc.geom,l.geom) ASC) AS rk

                                                        FROM %(latt_tbl)s l
                                                        INNER JOIN pluto p on p.bbl=l.bbl
                                                        INNER JOIN pluto_centroids pc on pc.p_gid = p.gid
                                                        )
                                                    SELECT s.l_gid l_gid
                                                        FROM res s
                                                        WHERE s.rk = 1;

                                                DROP TABLE IF EXISTS %(tmp_tbl_3)s;
                                                CREATE TABLE %(tmp_tbl_3)s as
                                                    select *
                                                    from %(latt_tbl)s l
                                                    WHERE EXISTS (select 1 from %(tmp_tbl_2)s t where t.l_gid=l.gid);
                                                drop table %(latt_tbl)s;
                                                ALTER TABLE %(tmp_tbl_3)s rename to %(latt_tbl)s;

                                                DROP TABLE IF EXISTS %(tmp_tbl_2)s;
                                                DROP TABLE IF EXISTS %(tmp_tbl_3)s;



                                                """ % T )


            T.update(                           { 'latt_tbl'            :   lattice_table_name,})

            # PROVE THAT ALL ADDRESSES ARE UNIQUE ( assuming no two addresses have the same BBL )
            assert True                    ==   pd.read_sql(""" select all_bbl=uniq_bbl _bool
                                                                from
                                                                    (select count(distinct y1.bbl) uniq_bbl
                                                                        from %(latt_tbl)s y1) as f1,
                                                                    (select count(y2.bbl) all_bbl
                                                                        from %(latt_tbl)s y2) as f2
                                                            """ % T,routing_eng)._bool[0]

        def usps_table(self):
            py_path.append(                         os_path.join(os_environ['BD'],'geolocation/USPS'))
            from USPS_syntax_pdf_scrape         import load_from_file
            py_path.append(                         os_path.join(os_environ['BD'],'html'))
            from scrape_vendors                 import Scrape_Vendors
            SV = Scrape_Vendors()

            # Files
            dir_path = os_path.join(os_environ['BD'],'geolocation/USPS')
            fpath_pdf                               =   dir_path + '/usps_business_abbr.pdf'
            fpath_xml                               =   dir_path + '/usps_business_abbr.xml'

            street_abbr_csv                         =   dir_path + '/usps_street_abbr.csv'
            biz_abbr_csv                            =   dir_path + '/usps_business_abbr.csv'
            regex_biz_abbr_csv                      =   dir_path + '/usps_business_abbr_regex.csv'
            regex_street_abbr_csv                   =   dir_path + '/usps_street_abbr_regex.csv'
            # t                                       =   extract_pdf_contents_from_stdout(fpath_pdf)

            A = load_from_file(street_abbr_csv).ix[:,['common_use','usps_abbr']]
            B = load_from_file(biz_abbr_csv).ix[:,['common_use','usps_abbr']]

            # Asserts Based on Previous Run
            assert len(A)==482
            assert len(B)==5969
            assert len(A)+len(B)==6451

            B.to_sql('usps',eng,index=False)
            A.to_sql('tmp_usps',eng,index=False)

            SV.SF.PGFS.Run.make_column_primary_serial_key('usps','gid',True)
            SV.SF.PGFS.Run.make_column_primary_serial_key('tmp_usps','gid',True)

            conn.set_isolation_level(0)
            cur.execute("""

            alter table usps add column abbr_type text;
            update usps set abbr_type='business';

            alter table tmp_usps add column abbr_type text;
            update tmp set abbr_type='street';

            insert into usps (common_use,usps_abbr,abbr_type)
            select t.common_use,t.usps_abbr,t.abbr_type
            from tmp_usps t;

            drop table tmp_usps;
            """)

        def mn_zipcodes(self):
            """
            incomplete and untested
            """
            src = 'http://www.unitedstateszipcodes.org/zip_code_database.csv'
            z = pd.read_csv(src)
            x = z[(z.state=='NY')&(z.county=='New York County')&(z.type!='PO BOX')].sort('zip')

            # print len(x)
            # print x.type.unique().tolist()
            # print str(x.zip.tolist())
            #
            # # result
            # mn_zipcodes = [10001, 10002, 10003, 10004, 10005, 10006,
            #                10007, 10009, 10010, 10011, 10012, 10013,
            #                10014, 10015, 10016, 10017, 10018, 10019,
            #                10020, 10021, 10022, 10023, 10024, 10025,
            #                10026, 10027, 10028, 10029, 10030, 10031,
            #                10032, 10033, 10034, 10035, 10036, 10037,
            #                10038, 10039, 10040, 10041, 10043, 10044,
            #                10045, 10046, 10047, 10048, 10055, 10060,
            #                10065, 10069, 10072, 10075, 10079, 10080,
            #                10081, 10082, 10087, 10090, 10094, 10095,
            #                10096, 10098, 10099, 10102, 10103, 10104,
            #                10105, 10106, 10107, 10109, 10110, 10111,
            #                10112, 10114, 10115, 10117, 10118, 10119,
            #                10120, 10121, 10122, 10123, 10124, 10125,
            #                10126, 10128, 10130, 10131, 10132, 10133,
            #                10138, 10149, 10151, 10152, 10153, 10154,
            #                10155, 10157, 10158, 10160, 10161, 10162,
            #                10164, 10165, 10166, 10167, 10168, 10169,
            #                10170, 10171, 10172, 10173, 10174, 10175,
            #                10176, 10177, 10178, 10179, 10184, 10196,
            #                10197, 10199, 10203, 10211, 10212, 10213,
            #                10256, 10257, 10258, 10259, 10260, 10261,
            #                10265, 10269, 10270, 10271, 10273, 10275,
            #                10277, 10278, 10279, 10280, 10281, 10282,
            #                10285, 10286, 10292]

        def nyc_snd(self):
            from f_nyc_data import load_parsed_snd_datafile_into_db
            load_parsed_snd_datafile_into_db(table_name='nyc_snd',drop_prev=True)

        def regex_repl(self):
            """

            From lua-users.org:

            Limitations of Lua patterns

            Especially if you're used to other languages with regular expressions,
            you might expect to be able to do stuff like this:

                '(foo)+' -- match the string "foo" repeated one or more times
                '(foo|bar)' -- match either the string "foo" or the string "bar"

            Unfortunately Lua patterns do not support this, only single characters
            can be repeated or chosen between, not sub-patterns or strings. The
            solution is to either use multiple patterns and write some custom logic,
            use a regular expression library like lrexlib or Lua PCRE, or use LPeg.
            LPeg is a powerful text parsing library for Lua based on
            Parsing Expression Grammar. It offers functions to create and combine
            patterns in Lua code, and also a language somewhat like Lua patterns or
            regular expressions to conveniently create small parsers.


            """
            a="""

                drop table if exists regex_repl;

                create table regex_repl (
                    tag text,
                    repl_from text,
                    repl_to text,
                    repl_flag text,
                    run_order integer,
                    comment text,
                    is_active boolean default true
                );

                insert into regex_repl (tag,
                                        repl_from,
                                        repl_to,
                                        repl_flag,
                                        run_order)
                values

                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(AVENUE)([%s]+)([A-F])([%s]*)(.*)','%1|%4 %2 %3 %5','','0'),

                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(AVE[NUE]*[%s]*[OF]*[%s]*[THE]*[%s]*[AME]*[R]?[ICA]*[S]?[%s]*)(.*)','%1|6 AVENUE %3','','0'),

                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(AVENUE)[%s]?([a-zA-Z]*)$','0|%1 %2 %3','','0'),
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(AVE)[%s]?([a-zA-Z]*)$','0|%1 %2 %3','','0'),
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(AV)[%s]?([a-zA-Z]*)$','0|%1 %2 %3','','0'),


                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(WEST)%s(END)%s(AVE)[%s]?([a-zA-Z]*)$',
                        '%1|%2QQQQ%3 %4 %5','','1'),
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(WEST)%s(END)%s(AVENUE)[%s]?([a-zA-Z]*)$',
                        '%1|%2QQQQ%3 %4 %5','','1'),
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(WEST)%s(END)%s(AV)[%s]?([a-zA-Z]*)$',
                        '%1|%2QQQQ%3 %4 %5','','1'),

                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(EAST)%s(RIVER)%s(DRIVE)[%s]?([a-zA-Z]*)$',
                        '%1|%2QQQQ%3 %4 %5','','1'),
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(EAST)%s(RIVER)%s(DR)[%s]?([a-zA-Z]*)$',
                        '%1|%2QQQQ%3 %4 %5','','1'),
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(EAST)%s(RIVER)%s(DRV)[%s]?([a-zA-Z]*)$',
                        '%1|%2QQQQ%3 %4 %5','','1'),

                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(PI)(KE)([%s]+)(SLIP)(.*)$',
                        '%1|%2QQQQ%3 %5','','1'),

                    ('custom_addr_pre_filter',
                        '([^|]*)|(.*)(%s)(TERRACE)([%s]*)([a-zA-Z]*)$','%1|%2 TERR %5','','2'),
                    ('custom_addr_pre_filter',
                        '(.*)%|(LA)(%s)(.*)?','%1|%2QQQQ%4 ','','3'),
                    ('custom_addr_pre_filter',
                        '([0-9]+)[%-]([a-zA-Z0-9]+)%|(.*)','%1|%3, Bldg. %2','','4'),
                    ('custom_addr_pre_filter',
                        '([0-9]+)([a-zA-Z]+)%|(.*)','%1|%3, Bldg. %2','','5'),
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(.*)(,%s)(Bldg%.)%s([a-zA-Z0-9]+)$','Bldg. %5, %1|%2','g','6'),
                    ('custom_addr_pre_filter',
                        '([^%|]*)%|(.*)','%1 %2','g','7')


                ;
            """
            conn.set_isolation_level(               0)
            cur.execute(                            a)
