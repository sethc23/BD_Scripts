
# from ipdb import set_trace as i_trace; i_trace()


def get_tables_headers(filePath=''):
    df_t = self.T.pd.read_sql_query("select * from information_schema.tables",engine)
    all_t = df_t[(df_t.table_schema=='public') & (df_t.table_catalog=='routing')].table_name.tolist()
    w,max_l = {},0
    print("All Routing Tables")
    for i in range(0,len(all_t)):
        t=all_t[i]
        print(str(i)+'\t\t'+t+'\n')
        df = self.T.pd.read_sql_query("SELECT * FROM "+t+" LIMIT 1", engine)
        x = df.columns
        w.update({t : x.values.tolist()})
        if len(x)>max_l: max_l=len(x)
        for it in x: print(it)
        print('\n\n')
        print('\n',df.head())
        print('\n\n')
    j=self.T.pd.DataFrame(dict([ (k,self.T.pd.Series(v)) for k,v in w.iteritems() ]))
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
        df = self.T.pd.read_sql_query("SELECT "+s+" FROM "+t+" x"+w,engine)
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
        df = self.T.pd.read_sql_query("SELECT "+s+" FROM "+t+" x"+w,engine)
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
    l = self.T.pd.read_sql_query(cmd,engine)
    cmd = "select geom from pluto where bbl = any(array"+str(l.bbl.tolist()).replace("'",'')+")"
    p = self.T.gd.read_postgis(cmd,conn)
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

    all_pts = self.T.pd.read_sql_query("select * from lot_pts where geom is null and ignore is false and place is false",engine)
    all_pts['block'] = all_pts.bbl.map(lambda s: str(s)[1:6])
    uniq_blocks = all_pts.block.unique().tolist()
    if show_some_detail==True: print len(uniq_blocks),'unique blocks'
    if show_some_detail==True: print 'pluto has 1961 unique blocks'
    # a=self.T.pd.read_sql_query("select distinct block from pluto",engine).block.tolist()
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
            lots = self.T.gd.read_postgis(cmd,engine)
            #if show_steps==True: A.extend(lots.geom)

            ### Create Buffer Around Lots
            s = str([it.to_wkt() for it in lots.geom])
            T = {'buffer': '0.0005',
                 'geoms' : s}
            cmd =   """ SELECT ST_Buffer(ST_ConvexHull((ST_Collect(the_geom))), %(buffer)s) as geom
                        FROM ( SELECT (ST_Dump( unnest(array[%(geoms)s]) )).geom the_geom) as t""".replace('\n','')%T
            block_buffer = self.T.gd.read_postgis(cmd,engine)
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
                line_geom = self.T.gd.read_postgis(cmd,engine)
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
                tmp_part_line=self.T.gd.read_postgis(cmd,engine)
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
                    lot=self.T.gd.read_postgis(cmd,engine)
                    if show_some_detail==True: A.append(lot.geom[0])

                    ### Get Line From Lot Polygon
                    perim_line = lot.boundary[0].to_wkt()
                    # if show_steps==True: A.append(lot.boundary[0])

                    ### Get Points of Segment of Lot Polygon Closest to Street
                    cmd =   """ SELECT ( st_dumppoints( st_geomfromtext('%(1)s') )).geom""".replace('\n','')%{'1':str(perim_line)}
                    points = self.T.gd.read_postgis(cmd,engine).geom
                    t1,t2={},{}
                    for j in range(1,len(points)):
                        poly_seg_pts=points[j-1],points[j]
                        dist_from_street = self.T.pd.read_sql("""  select
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
                    lot_seg_mid_pt = self.T.gd.read_postgis("""   SELECT ST_Line_Interpolate_Point(st_makeline(ptA,ptB),0.5) geom
                                                            FROM
                                                                st_geomfromtext(' %(start_pt)s ') ptA,
                                                                st_geomfromtext(' %(end_pt)s ') ptB
                                                    """.replace('\n','')%{'start_pt': str(closest_seg_pts[0]),
                                                                          'end_pt'  : str(closest_seg_pts[1]),
                                                                          'street'  : LINE},engine)

                    if show_steps==True: A.append(lot_seg_mid_pt.geom[0])

                    ### Closest Point in Street
                    street_seg_mid_pt = self.T.gd.read_postgis("""
                        SELECT ST_ClosestPoint(
                            st_geomfromtext(' %(street)s '),
                            st_geomfromtext(' %(mid_pt)s ')) geom
                        """.replace('\n','')%{'mid_pt'  : str(lot_seg_mid_pt.geom[0].to_wkt()),
                                              'street'  : LINE},engine)
                    #A.append(street_seg_mid_pt.geom[0])

                    ### Absolute Angle of Segment (12=0 deg.,6=180 deg.)
                    seg_angle = self.T.pd.read_sql("""     SELECT ST_Azimuth(ptA,ptB) ang
                                                    FROM
                                                                st_geomfromtext(' %(start_pt)s ') ptA,
                                                                st_geomfromtext(' %(end_pt)s ') ptB
                                                    """.replace('\n','')%{'start_pt': str(closest_seg_pts[0]),
                                                                          'end_pt'  : str(closest_seg_pts[1])},engine).ang[0]

                    ### Point on Street that Intersects with perp. line extending from Poly Segment Midpoint
                    this_lot_pt = self.T.gd.read_postgis("""
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
                        line_lot_to_street = self.T.gd.read_postgis("""
                            SELECT ST_ShortestLine(lot_pt,mid_pt) geom
                            FROM
                                st_geomfromtext(' %(lot_pt)s ',4326) lot_pt,
                                st_geomfromtext(' %(mid_pt)s ',4326) mid_pt
                            """.replace('\n','')%{'mid_pt'  : str(lot_seg_mid_pt.geom[0].to_wkt()),
                                                  'lot_pt'  : this_lot_pt[0]},engine)
            #
                        if len(line_lot_to_street.geom)>1:
                            self.T.gd.GeoSeries(line_lot_to_street.geom).plot()
                            print 'too much for Line Connecting Lot to Street'
                            raise SystemError
                        if show_some_detail==True: A.append(line_lot_to_street.geom[0])


        if show_some_detail==True:
            d=self.T.gd.GeoSeries(A).plot(fig_size=(26,22),
                                   save_fig_path=save_fig_path,
                                   save_and_show=False)

        if show_some_detail==True: me = raw_input('y?')
        else: me='y'

        if me=='y' and lot_pts!=[]:
            c = self.T.gd.GeoDataFrame(lot_pts)
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
    l = lots = self.T.pd.read_sql_query(cmd,engine)

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
    res = self.T.pd.read_sql_query(cmd,engine)

def make_index(describe=True,commit=False):
    # from sys import path as sys_path
    # sys_path.append('/Users/admin/SERVER2/BD_Scripts/geolocation')
    # from f_postgres import geoparse,ST_PREFIX_DICT,ST_SUFFIX_DICT

    from re import search as re_search # re_search('pattern','string')
    from re import sub as re_sub  # re_sub('pattern','repl','string','count')

    cmd = "select bbl,bldg_num,bldg_street from lot_pts where geom is not null and ignore is false and bldg_street is not null"
    l = lots = self.T.pd.read_sql_query(cmd,engine)

    ## geoparse everything
    l = geoparse(l,'bldg_street','clean_addr')
    ## reduce to unique way (street,road,avenue,lane, etc...)
    addr_bbl_dict = dict(zip(l.clean_addr.tolist(),l.bbl.tolist()))
    ul = self.T.pd.DataFrame({'addr':addr_bbl_dict.keys(),'bbl':addr_bbl_dict.values()})

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
    # a = self.T.pd.DataFrame({'addr':dict(zip(a.addr.tolist(),range(0,len(a.index)))).keys()})

    a = ul.copy()
    a['nid'] = a.index
    a['bldg_street_idx'] = a.nid.map(lambda s: str('%05d' % s))
    a['addr'] = a.addr.map(lambda s: s.lower().strip())

    # add entries with or without different combinations of info (e.g., e/w, st/ave, etc...)
    a_idx = a.bldg_street_idx.tolist()

    # pre_re_s = re_search_string = r'^('+"|".join(ST_PREFIX_DICT.values())+r')\s'
    # alp  = a_less_prefix = self.T.pd.DataFrame({'addr':a.addr.map(lambda s: re_sub(pre_re_s,r'',s).strip()
    #                                        if ST_SUFFIX_DICT.values().count(  # this extra is to prevent a "st" result
    #                                         re_sub(pre_re_s,r'',s).strip()
    #                                         ) == 0 else ''),
    #                                      'bldg_street_idx': a_idx})

    suf_re_s = re_search_string = r'\s('+r'|'.join(ST_SUFFIX_DICT.values())+r')$'
    als  = a_less_suffix = self.T.pd.DataFrame({'addr':a.addr.map(lambda s: re_sub(suf_re_s,r'',s).strip()
                                           if ST_SUFFIX_DICT.values().count(  # this extra is to prevent a "w" result
                                            re_sub(suf_re_s,r'',s).strip()
                                            ) == 0 else s),
                                         'bldg_street_idx':a_idx})

    nw = num_ways = als[als.addr.str.contains('\d+')]
    nw['below13'] = nw.addr.map(lambda s: True if eval(re_search('\d+',s).group().strip())<=12 else False)
    nw['one_word'] = nw.addr.map(lambda s: True if len(s.split(' '))==1 else False)
    als = als[als.index.isin(nw[(nw.below13==True)&(nw.one_word==True)].index.tolist())==False]

    # alps = a_less_prefix_less_suffix = self.T.pd.DataFrame({'addr':alp.addr.map(lambda s: re_sub(suf_re_s,'',s).strip()),
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
    B = self.T.pd.DataFrame({'addr':all_unique_addr_list})
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
    l = self.T.pd.read_sql_query(cmd,engine)
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

    #print self.T.pd.read_sql_query('select count(*) cnt from lot_pts',engine).cnt[0],'\tTOTAL LOTS'
    #print self.T.pd.read_sql_query('select count(*) cnt from lot_pts where bldg_num_end is null',engine).cnt[0],'\tremaining lots without bldg_num_end'
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

    lion_ways = self.T.gd.read_postgis("select lw.gid,lw.clean_street,lw.streetcode,lw.geom from address_idx a "+
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
        this_line = self.T.pd.read_sql_query(cmd,engine).ix[0,'this_line']
        this_nid = self.T.pd.read_sql_query("select nid from address_idx where street = '%s' order by nid"%name,engine).ix[0,'nid']
        t.append({'street':name,
                  'nid':this_nid,
                  'geom':this_line})
    d = self.T.pd.DataFrame(t)
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
    from_nodes = self.T.pd.read_sql_query("SELECT lat,lon FROM lion_nodes",engine)
    x = from_nodes.lon.tolist()
    y = from_nodes.lat.tolist()
    poly_all = Polygon(zip(x,y))

    # Extract the point values that define the perimeter of the polygon
    # x_outer,y_outer = poly_all.exterior.coords.xy
def plot_pluto_block(block):
    # 121 madison is on block 860
    m = self.T.gd.read_postgis("SELECT * FROM pluto where block = "+block+'"',conn)
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
    # select_lion = self.T.pd.read_hdf(BASE_SAVE_PATH+t+'_select.h5', 'table')
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
    with_MN=self.T.pd.read_sql_query(cmd,engine)
    print 'with_MN',len(with_MN.index)

    cmd="select gid,nodeid,geom from lion_nodes where lion_nodes.manhattan is not true"
    without_MN=self.T.pd.read_sql_query(cmd,engine)
    print 'without_MN',len(without_MN.index)

    cmd="select count(*) from lion_nodes"
    lion_cnt = self.T.pd.read_sql_query(cmd,engine)
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
    nodes_from_lion_nodes = self.T.pd.read_sql_query("SELECT nodeid FROM lion_nodes",engine)
    nodes_from_lion_ways = self.T.pd.read_sql_query("SELECT nodeidfrom,nodeidto FROM lion_ways",engine)

    check_nodes = nodes_from_lion_nodes.nodeid.map(int)
    good_nodes = nodes_from_lion_ways.nodeidfrom.map(int).append(nodes_from_lion_ways.nodeidto.map(int))

    check_nodes = self.T.pd.Series(check_nodes.unique())
    good_nodes = good_nodes.unique().tolist()

    bool_check = check_nodes.isin(good_nodes)
    df = self.T.pd.DataFrame({'nodes':check_nodes,'good':bool_check})
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

    df = self.T.pd.read_sql_query("select gid,address,bldg_num,bldg_street from pluto;",conn)
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
    lw = self.T.pd.read_sql_query("select lw.gid,lw.street from lion_ways lw",engine)
    lw = geoparse(lw,'street','clean_street')
    engine.execute('drop table if exists temp')
    lw.to_sql('temp',engine,if_exists='append',index=False)
    engine.execute('update lion_ways lw set clean_street = t.clean_street from temp t where t.gid = lw.gid')
    engine.execute('drop table if exists temp')
def reduce_ways():
    ##Reduce Ways_vertices_pgr

    # Here, trying to reduce OSM data by using convex hull of pluto to find points outside of the hull and set remove to true.

    pts = self.T.gd.read_postgis("SELECT id gid,the_geom geom FROM ways_vertices_pgr",conn)
    f = '/Users/admin/Projects/GIS/map_data/MN_pluto_lines_hull.shp'
    hull = self.T.gd.GeoDataFrame.from_file(f)

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
    T = self.T.pd.DataFrame({'lon': x ,'lat' : y })
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

    # uniq_streets = self.T.pd.read_sql_query("select street streets from lion_ways",engine).streets.unique().tolist()
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
    # u = self.T.pd.read_csv(fpath_abbr,index_col=0)
    # fpath_abbr_regex = fpath_abbr.replace('.csv','_regex.csv')
    # df = self.T.pd.read_csv(fpath_abbr_regex,index_col=0)
    # print len(u),len(df)

    # g = u.groupby('prim_suff')
    # df = self.T.pd.DataFrame({'prim_suff':g.groups.keys()}).sort('prim_suff').reset_index(drop=True)

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
    a = self.T.gd.read_postgis("select street,geom from address_idx where geom is not null",engine)

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

    cs = combined_streets = self.T.pd.DataFrame({'street':east_streets.street.map(lambda s: s.replace('e ','')).tolist(),
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

    g = self.T.gd.read_postgis(cmd,engine)

    nid_start = 1+self.T.pd.read_sql_query("select nid from address_idx order by nid desc limit 1",engine).nid.tolist()[0]
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
    a1 = self.T.gd.read_postgis(cmd,engine)

    cmd2 = "select %(1)s from %(3)s %(2)s" % \
            { '1' : '*',#','.join(cols),
              '2' : ''.join(conditions),
              '3' : new_db}
    a2 = self.T.gd.read_postgis(cmd,engine)
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

    l=self.T.pd.DataFrame({'gid':t,'geom':None})
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


class pgSQL_Functions:
    """

    NOTE: USE plpythonu and plluau for WRITE ACESS

    """


    def __init__(self,_parent):
        self.T                              =   _parent.T
        self.Make                           =   self.Make(self)
        self.Run                            =   self.Run(self)

    class Run:

        def __init__(self,_parent):
            self.T                          =   _parent.T
            self.Run                        =   self

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
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    cmd)

    class Make:

        def __init__(self,_parent):
            self.T                          =   _parent.T
            self.Make                       =   self

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
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    cmd)
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
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    cmd)
        def z_parse_NY_addrs(self):
            T = {'fct_name'                 :   'z_parse_NY_addrs',
                 'fct_args_types'           :   [ ['IN','query_str','text'],],
                 'fct_return'               :   'SETOF parsed_addr',
                 'fct_lang'                 :   'plpythonu',
                 'cmt'                      :   '\n'.join([ "Example:",
                                                            "select * from z_parse_NY_addrs(",
                                                            "    ''select gid,address,zipcode",
                                                            "     from pluto",
                                                            "     where address is not null order by gid''",
                                                            ");"])}
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
                    src_gid bigint,
                    orig_addr text,
                    bldg text,
                    box text,
                    unit text,
                    num text,
                    pretype text,
                    qual text,
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

                    #plpy.log('starting parser')

                    query_str = args[0]
                    qs,res = query_str.lower().split(' '),[]
                    drop_items = []

                    if qs.count('offset')>0:
                        q_offset = int(qs[qs.index('offset')+1])
                        drop_items.extend(['offset',str(q_offset)])
                    else:
                        q_offset = 0

                    if qs.count('limit')>0:
                        q_max = int(qs[qs.index('limit')+1])
                        drop_items.extend(['limit',str(q_max)])
                    else:
                        q_max = -1

                    if 0<q_max<=100:
                        q_lim = q_max
                    else:
                        q_lim = 100

                    drop_idx = sorted([qs.index(it) for it in drop_items])
                    drop_idx.reverse()
                    for it in drop_idx:
                        z=qs.pop(it)



                    query_str = ' '.join(qs)
                    stop=False

                    pt=0
                    #plpy.log("START")
                    while stop==False:
                        pt+=1

                        if q_max>0:
                            if q_offset + q_lim > q_max:
                                q_lim = q_max - q_offset

                        q_range = 'OFFSET ##s LIMIT ##s' ## (q_offset,q_lim)

                        query_dict = {   '_QUERY_STR'        :   ' '.join([query_str.replace('####','##'),
                                                                           q_range]), }


                        #plpy.log(str(pt)+' '+query_dict['_QUERY_STR'])

                        q=\"\"\"
                            select (res).*
                            from
                                (
                                select  z_custom_addr_post_filter(

                                            standardize_address('tiger.pagc_lex','tiger.pagc_gaz',
                                                                    'tiger.pagc_rules',f2.addr_zip),
                                            f2.orig_addr,
                                            f2.src_gid
                                            ) res
                                from
                                    (
                                    select
                                        z_custom_addr_pre_filter( f1.address,f1.zipcode ) addr_zip,
                                        f1.address orig_addr,
                                        f1.gid src_gid
                                    from
                                        (
                                        ##(_QUERY_STR)s
                                        ) as f1
                                    ) as f2
                                ) as f3
                        \"\"\" ## query_dict

                        q_res = plpy.execute(q)
                        #plpy.log(q)

                        res.extend(q_res)

                        if len(q_res)<q_lim or len(res)==q_max:
                            #plpy.log('exit 1623')
                            stop=True
                            break
                        else:
                            q_offset = q_offset + q_lim


                    return res


                $$ LANGUAGE %(fct_lang)s;

            COMMENT ON FUNCTION public.%(fct_name)s(%(fct_types)s) IS '%(cmt)s';
            """ % T
            cmd                         =   a.replace('##','%')
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    cmd)
        def z_custom_addr_post_filter(self):
            cmd="""

                DROP FUNCTION IF EXISTS z_custom_addr_post_filter(stdaddr,text,integer);
                DROP FUNCTION IF EXISTS z_custom_addr_post_filter(stdaddr[],text[],integer[]);
                CREATE OR REPLACE FUNCTION z_custom_addr_post_filter(   res stdaddr,
                                                                        orig_addr text,
                                                                        src_gid bigint)
                RETURNS parsed_addr AS $$
                    --log("start")
                    local some_src_cols = {"building","house_num","predir","qual","pretype","name","suftype","sufdir",
                                            "city","state","postcode","box","unit",}

                    local some_dest_cols = {"bldg","num","predir","qual","pretype","name","suftype","sufdir",
                                            "city","state","zip","box","unit"}
                    tmp_pt = {}
                    local tmp = res
                    local tmp_col = ""
                    --log(1521)
                    for k,v in pairs(some_dest_cols) do
                        tmp_col = some_src_cols[k]
                        tmp_pt[v] = tmp[tmp_col]
                    end
                    tmp_pt["src_gid"] = src_gid
                    tmp_pt["orig_addr"] = orig_addr
                    tmp_pt["zip"] = tmp.postcode
                    --log(1529)
                    -- CLEAN UP TEMP SUBSTITUTION {Qx5 = no space, Qx4 = space} < -- OUTPUT
                    if tmp_pt["name"] then
                        if tmp_pt["name"]:find("QQQQQ") then
                            tmp_pt["name"] = tmp_pt["name"]:gsub("(QQQQQ)","")
                        end
                        if tmp_pt["name"]:find("QQQQ") then
                            tmp_pt["name"] = tmp_pt["name"]:gsub("(QQQQ)"," ")
                        end
                        if tmp_pt["name"]:find("AVENUE OF THE") then
                            tmp_pt["suftype"] = "AVE"
                        end
                    end
                    --log(1542)

                    local t = ""
                    local s1,e1,s2,e2 = 0,0,0,0

                    -- DISCARD PRETYPES, MOVE THEM BACK TO 'NAME', UPDATE SUFTYPE
                    if tmp_pt["pretype"] then
                        --log("1549")
                        if tmp_pt["num"]==0 then
                            s1,e1=0,0
                        else
                            s1,e1 = orig_addr:find(tmp_pt["num"])
                        end
                        if e1==nil then
                            log("1555")
                            log(tmp_pt["num"])
                            log(tmp_pt["name"])
                            log(orig_addr)
                            log(tmp_pt["pretype"])
                            log(src_gid)
                            if true then return end
                        end
                        if not orig_addr then
                            log("1566")
                            log(tmp_pt["num"])
                            log(tmp_pt["name"])
                            log(orig_addr)
                            log(tmp_pt["pretype"])
                            log(src_gid)
                            if true then return end
                        end

                        s2,e2 = orig_addr:find(tmp_pt["name"])

                        if s2==nil then
                            log("1578")
                            log(tmp_pt["num"])
                            log(tmp_pt["name"])
                            log(orig_addr)
                            log(tmp_pt["pretype"])
                            log(tostring(src_gid))
                            if true then return end
                        end
                        --log("1575")
                        t = orig_addr:sub(e1+2,s2-2)

                        -- if this string has a space, meaning at least two words, take only last word
                        if t:find("[%s]")==nil then
                            tmp_pt["name"] = t.." "..tmp_pt["name"]
                        else
                            t = t:gsub("(.*)%s([a-zA-Z0-9]+)$","%2")
                            tmp_pt["name"] = t.." "..tmp_pt["name"]
                        end
                        tmp_pt["pretype"] = nil
                        --log("1586")
                        t = orig_addr:sub(e2+2)

                        cmd = string.format([[  select usps_abbr abbr
                                                from usps where common_use ilike '%s']],t)

                        for row in server.rows(cmd) do
                            t = row.abbr
                            break
                        end
                        --log("1596")
                        tmp_pt["suftype"] = t:upper()

                    end
                    --log("1600")
                    -- FOR ANY PREDIR NOT 'E' OR 'W', MOVE BACK TO 'NAME'
                    if tmp_pt["predir"] and (tmp_pt["predir"]~="E" and tmp_pt["predir"]~="W") then
                        --log("1742")
                        if tmp_pt["predir"]=='N' then t = "NORTH" end
                        if tmp_pt["predir"]=='S' then t = "SOUTH" end

                        tmp_pt["predir"] = nil
                        tmp_pt["name"] = t.." "..tmp_pt["name"]
                    end
                    --log("1610")
                    -- WHEN UNIT CONTAINS 'PIER', e.g., 'PIER-15 SOUTH STREET' (filtered as '0 PIER-15 SOUTH STREET')
                    if tmp_pt["unit"] then
                        if tmp_pt["unit"]:find('# 0 PIER') and tmp_pt["bldg"]==nil then
                            tmp_pt["bldg"] = "PIER "..tmp_pt["num"]
                            tmp_pt["num"] = 0
                            tmp_pt["unit"] = nil
                        end
                    end

                    -- IF num,predir, and name==number but no suftype, add it.
                    if not tmp_pt["suftype"] then
                        if type(tmp_pt["name"])==type(11) then
                            if ( tmp_pt["predir"]=='E' or tmp_pt["predir"]=='W' ) then
                                tmp_pt["suftype"] = "ST"
                                -- NOT DOING AVENUES BECAUSE SO FEW AND HIGHER ODDS OF THIS BEING A MISTAKE
                            end
                        end
                    end

                    return tmp_pt

                $$ LANGUAGE plluau;
            """
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    cmd)
        def z_custom_addr_post_filter_with_iter(self):
            cmd="""

                DROP FUNCTION IF EXISTS z_custom_addr_post_filter_with_iter(stdaddr[],text[],integer[]);
                CREATE OR REPLACE FUNCTION z_custom_addr_post_filter_with_iter(   res stdaddr[],
                                                                        orig_addr text[],
                                                                        src_gid integer[])
                RETURNS SETOF parsed_addr AS $$
                    return _U(res,orig_addr,src_gid)
                end
                do
                    _U = function(res,orig_addr,src_gid)

                    local some_src_cols = {"building","house_num","predir","qual","pretype","name","suftype","sufdir",
                                            "city","state","postcode","box","unit",}

                    local some_dest_cols = {"bldg","num","predir","qual","pretype","name","suftype","sufdir",
                                            "city","state","zip","box","unit"}


                    for i=1, #res do

                        local tmp = res[i]
                        local tmp_pt = {}
                        local tmp_col = ""

                        for k,v in pairs(some_dest_cols) do
                            tmp_col = some_src_cols[k]
                            tmp_pt[v]=tmp[tmp_col]
                        end
                        tmp_pt["src_gid"] = src_gid[i]
                        tmp_pt["orig_addr"] = orig_addr[i]
                        tmp_pt["zip"]=tmp.postcode

                        -- CLEAN UP TEMP SUBSTITUTION {Qx5 = no space, Qx4 = space} < -- OUTPUT
                        if tmp_pt["name"] then
                            if tmp_pt["name"]:find("QQQQQ") then
                                tmp_pt["name"] = tmp_pt["name"]:gsub("(QQQQQ)","")
                            end
                            if tmp_pt["name"]:find("QQQQ") then
                                tmp_pt["name"] = tmp_pt["name"]:gsub("(QQQQ)"," ")
                            end
                            if tmp_pt["name"]:find("AVENUE OF THE") then
                                tmp_pt["suftype"] = "AVE"
                            end
                        end

                        local t = ""
                        local s1,e1,s2,e2 = 0,0,0,0

                        -- DISCARD PRETYPES, MOVE THEM BACK TO 'NAME', UPDATE SUFTYPE
                        if tmp_pt["pretype"] then
                            --log("1702")
                            if tmp_pt["num"]==0 then
                                s1,e1=0,0
                            else
                                s1,e1 = orig_addr[i]:find(tmp_pt["num"])
                            end

                            if e1==nil then
                                log(tmp_pt["num"])
                                log(tmp_pt["name"])
                                log(orig_addr[i])
                                log(tmp_pt["pretype"])
                                log(src_gid[i])
                                if true then return end
                            end

                            s2,e2 = orig_addr[i]:find(tmp_pt["name"])

                            if s2==nil then
                                log(tmp_pt["num"])
                                log(tmp_pt["name"])
                                log(orig_addr[i])
                                log(tmp_pt["pretype"])
                                log(src_gid[i])
                                if true then return end
                            end

                            t = orig_addr[i]:sub(e1+2,s2-2)

                            -- if this string has a space, meaning at least two words, take only last word
                            if t:find("[%s]")==nil then
                                tmp_pt["name"] = t.." "..tmp_pt["name"]
                            else
                                t = t:gsub("(.*)%s([a-zA-Z0-9]+)$","%2")
                                tmp_pt["name"] = t.." "..tmp_pt["name"]
                            end
                            tmp_pt["pretype"] = nil

                            t = orig_addr[i]:sub(e2+2)

                            cmd = string.format([[  select usps_abbr abbr
                                                    from usps where common_use ilike '%s']],t)

                            for row in server.rows(cmd) do
                                t = row.abbr
                                break
                            end

                            tmp_pt["suftype"] = t:upper()

                        end

                        -- FOR ANY PREDIR NOT 'E' OR 'W', MOVE BACK TO 'NAME'
                        if tmp_pt["predir"] and (tmp_pt["predir"]~="E" and tmp_pt["predir"]~="W") then
                            --log("1742")
                            if tmp_pt["predir"]=='N' then t = "NORTH" end
                            if tmp_pt["predir"]=='S' then t = "SOUTH" end

                            tmp_pt["predir"] = nil
                            tmp_pt["name"] = t.." "..tmp_pt["name"]
                        end

                        -- WHEN UNIT CONTAINS 'PIER', e.g., 'PIER-15 SOUTH STREET' (filtered as '0 PIER-15 SOUTH STREET')
                        if tmp_pt["unit"] then
                            if tmp_pt["unit"]:find('# 0 PIER') and tmp_pt["bldg"]==nil then
                                tmp_pt["bldg"] = "PIER "..tmp_pt["num"]
                                tmp_pt["num"] = 0
                                tmp_pt["unit"] = nil
                            end
                        end
                        coroutine.yield(tmp_pt)
                    end

                end

                $$ LANGUAGE plluau;
            """
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    cmd)
        def z_custom_addr_pre_filter(self):
            """

            Most of these should really be systematically created from the NYC Street Name Dictionary (SND)

            See here: http://www.nyc.gov/html/dcp/html/bytes/applbyte.shtml#geocoding_application

            """
            cmd="""
                drop function if exists z_custom_addr_pre_filter(text);
                CREATE OR REPLACE FUNCTION z_custom_addr_pre_filter(addr text, zipcode bigint)
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
                        addr = addr:gsub("^([0-9]*)([%-]*)([a-zA-Z0-9]*)[%s]*([a-zA-Z0-9]*)[%s]*(.*)",
                                         "%1%2%3|%4 %5")
                    end

                    local cmd = [[select repl_from,repl_to
                            from regex_repl
                            where tag = 'custom_addr_pre_filter'
                            and is_active is true
                            order by run_order ASC]]

                    for row in server.rows(cmd) do
                        addr = string.gsub(addr,row.repl_from,row.repl_to)
                    end

                    if zipcode==nil or zipcode==0 then
                        zipcode=11111
                    end

                    return addr..", New York, NY, "..tostring(zipcode)
                $$ LANGUAGE plluau;
            """
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    cmd)


class pgSQL_Triggers:

    def __init__(self,_parent):
        self.T                              =   _parent.T
        self.Create                         =   self.Create(self)
        self.Destroy                        =   self.Destroy(self)

    class Create:
        def __init__(self,_parent):
            self.T                          =   _parent.T
            self.Create                     =   self
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
            self.T.conn.set_isolation_level(           0)
            self.T.cur.execute(                        c)
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
            self.T.conn.set_isolation_level(0)
            self.T.cur.execute(c)

    class Destroy:
        def __init__(self,_parent):
            self.T                          =   _parent.T
            self.Destroy                    =   self
        def z_auto_add_primary_key(self):
            c                           =   """
            DROP FUNCTION if exists
                z_auto_add_primary_key() cascade;

            DROP EVENT TRIGGER if exists missing_primary_key_trigger;
                                            """
            self.T.conn.set_isolation_level(0)
            self.T.cur.execute(c)
        def z_auto_add_last_updated_field(self):
            c                               =   """
            DROP FUNCTION if exists
                z_auto_add_last_updated_field() cascade;

            DROP EVENT TRIGGER if exists missing_last_updated_field;
                                            """
            self.T.conn.set_isolation_level(0)
            self.T.cur.execute(c)

class pgSQL_Tables:
    """

    Pluto:

        update pluto set address = regexp_replace(address,'F\sD\sR','FDR','g') where address ilike '%f d r%';


    """

    def __init__(self,_parent):
        self.T                              =   _parent.T
        self.Make                           =   self.Make(self)
        self.Update                         =   self.Update(self)

    class Update:
        def __init__(self,_parent):
            self.T                          =   _parent.T

        def prep_vendor_data_for_adding_geom(self,data_type,data_set,purpose,args=None):
            """
            This is a custom function for preparing data in a particular way.

            Uses:

                df = prep_data(data_type='db',data_set='seamless',purpose='get_bldg_street_idx')

                df = prep_data(data_type='db',data_set='mnv',purpose='get_bldg_street_idx')

                df = prep_data(data_type='db',data_set='yelp',purpose='google_geocode')


            """
            self.T.py_path.append(              self.T.os_environ['BD'] + '/geolocation')
            from f_geolocation                  import Addr_Parsing
            self.Parsing                    =   Addr_Parsing()

            # from pygeocoder                   import Geocoder
            # from time                         import sleep            as delay

            def format_db(db,purpose,args):

                # ------------------
                # ------------------
                if   (db=='seamless' or db=='seamless_geom_error'):
                    T                       =   {'db_tbl'           :   db,
                                                 'id_col'           :   'vend_id',
                                                 'vend_name'        :   'vend_name',
                                                 'address_col'      :   'address',
                                                 'zip_col'          :   'zipcode',
                                                }
                elif (db=='yelp' or db=='yelp_geom_error'):
                    T                       =   {'db_tbl'           :   db,
                                                 'id_col'           :   'gid',
                                                 'vend_name'        :   'vend_name',
                                                 'address_col'      :   'address',
                                                 'zip_col'          :   'postal_code',
                                                    }
                elif db=='mnv':
                    T                       =   {'db_tbl'           :   db,
                                                 'id_col'           :   'id',
                                                 'vend_name'        :   'vend_name',
                                                 'address_col'      :   'address',
                                                 'zip_col'          :   'zipcode',
                                                    }
                # ------------------
                # ------------------

                if purpose=='google_geocode':
                    cmd                     =   """
                                                    select %(id_col)s id,%(vend_name)s vend_name,
                                                        %(address_col)s address,%(zip_col)s zipcode
                                                    from %(db_tbl)s
                                                    where address is not null
                                                    and (char_length(bbl::text)!=10 or bbl is null)
                                                """%T
                    df                      =   self.T.pd.read_sql(cmd,self.T.eng)
                    return df,T

                if purpose=='get_bldg_street_idx':
                    cmd                     =   """
                                                    select %(id_col)s id,%(address_col)s address,%(zip_col)s zipcode
                                                    from %(db_tbl)s
                                                    where address is not null and geom is null
                                                    and (bbl::text='NaN' or bbl is null or char_length(bbl::text)<10)
                                                """%T
                    df                      =   self.T.pd.read_sql(cmd,self.T.eng)
                    df                      =   self.Parsing.clean_street_names(df,'address','address')
                    df['address']           =   df.address.map(lambda s: s.decode('ascii','ignore').encode('utf-8','ignore'))
                    df['bldg_num']          =   df.address.map(lambda s: s.split(' ')[0])
                    df['clean_bldg_num']    =   df.bldg_num.map(lambda s: None if ''==''.join([it for it in str(s)
                                                                                               if str(s).isdigit()])
                                                          else int(''.join([it for it in str(s) if str(s).isdigit()])))
                    df                      =   df[df.clean_bldg_num.map(lambda s: True if str(s)[0].isdigit()
                                                                                    else False)].reset_index(drop=True)
                    df['bldg_street']       =   df.address.map(lambda s: ' '.join(s.split(' ')[1:]))
                    df['clean_bldg_num']    =   df.clean_bldg_num.map(int)
                    df['zipcode']           =   df.zipcode.map(int)
                    df['addr_set']          =   map(lambda s: ' '.join(map(str,s.tolist())),
                                                            df.ix[:,['clean_bldg_num','bldg_street']].as_matrix())
                    df.rename(                  columns={'clean_bldg_num':'addr_num','bldg_street':'addr_street'},
                                                inplace=True)
                    return df,T

            if data_type=='db':
                return format_db(               data_set,purpose,args)
        def add_geom_using_address(self,working_table):
            """

            Usages:

                working_table = 'seamless' | 'yelp' | 'seamless_geom_error' | 'mnv'

            """
            # 1. load NYC TABLE -- Libraries & F(x)s
            # 2. format data for and run 'get_bldg_street_idx' function
            df,T = self.prep_vendor_data_for_adding_geom(data_type      =   'db',
                                                         data_set       =   working_table,
                                                         purpose        =   'get_bldg_street_idx')
            addr_tot                        =   len(df)
            addr_uniq                       =   len(df.addr_set.unique().tolist())
            self.T.__init__(                    T)
            recognized,not_recog,TCL        =   self.Parsing.get_bldg_street_idx(   df,
                                                         addr_set_col   =   'addr_set',
                                                         addr_num_col   =   'addr_num',
                                                         addr_street_col=   'addr_street',
                                                         zipcode_col    =   'zipcode',
                                                         show_info      =   False  )

            to_check_later                  =   TCL
            addr_recog                      =   len(recognized)
            addr_unrecog                    =   len(not_recog)
            addr_TCL                        =   len(to_check_later)

            # 3. push data to table 'tmp'
            z                               =   self.T.pd.merge(df,recognized.ix[:, ['addr_set','bldg_street_idx']], on='addr_set',how='outer')
            z                               =   z.drop(['addr_set'],axis=1)
            self.T.conn.set_isolation_level(    0)
            self.T.cur.execute(                 'drop table if exists %(tmp_tbl)s' % self.T)
            z.to_sql(                           self.T.tmp_tbl,self.T.eng,index=False)
            tmp_rows                        =   len(z)

            # 4. add necessary columns if not exist to $working_table
            cmd                             =   """   select column_name cols, data_type
                                                from INFORMATION_SCHEMA.COLUMNS
                                                where table_name = '%(tmp_tbl)s'""" % self.T
            tbl_info                        =   self.T.pd.read_sql(cmd,self.T.eng)
            tbl_cols                        =   map(str,tbl_info.cols.tolist())
            cols_needed                     =   { 'camis'           :   'integer',
                                                   'bbl'            :   'integer',
                                                   'lot_cnt'        :   'integer DEFAULT 1',
                                                   'geom'           :   'geometry(Point,4326)'}
            for k,v in cols_needed.iteritems():
                if tbl_cols.count(k)==0:
                    self.T.conn.set_isolation_level(0)
                    self.T.cur.execute('alter table %(tbl)s add column %(k)s %(v)s'%{'tbl':self.T.tmp_tbl,'k':k,'v':v})

            # from ipdb import set_trace as i_trace; i_trace()

            if not len(recognized):
                self.T.conn.set_isolation_level(0)
                self.T.cur.execute(             "DROP TABLE IF EXISTS %(tmp_tbl)s;" % self.T)
                print '\tTABLE:',working_table
                print addr_tot,'\t\ttotal addresses without geom [%s]'%working_table
                print addr_uniq,'\t\t# of unique addresses [%s]'%working_table
                print addr_recog,'\t\t\trecognized'
                print addr_unrecog,'\t\t\tnot_recog'
                print addr_TCL,'\t\t\tto_check_later'
                # print tmp_rows,'\t\trows in %(tmp_tbl)s' % self.T
                return

            # 5. update table $working_table and delete table 'tmp'
            self.T.conn.set_isolation_level(0)
            self.T.cur.execute("""

                -- COPY BBL VALUE WHERE A MATCH EXISTS AND VALUE OF ADDRESS NUMBER EQUAL/BETWEEN EXISTING DB PTS
                update %(tmp_tbl)s s set bbl = l.bbl
                    from lot_pts l
                    where
                        char_length(l.bbl::text)        >=  10
                        and s.bldg_street_idx::text     !=  'NaN'
                        and s.addr_num::text            !=  'NaN'
                        --and s.id                      =   s.%(id_col)s
                        and (
                            to_number(concat(s.bldg_street_idx,'.',to_char(s.addr_num,'00000')),'00000.00000')
                            between l.lot_idx_start and l.lot_idx_end
                            );


                -- COPY BBL VALUE WHERE A MATCH EXISTS BUT THE NEW ADDRESS HAS STREET NUMBER EXCEEDING THE DB IDX
                with upd as (   select *
                                from
                                    (
                                    select
                                        id,bldg_street_idx,l.bbl,l.lot_idx_end,
                                        max(l.lot_idx_end) over (partition by bldg_street_idx) as max_thing
                                    from lot_pts l,%(tmp_tbl)s t
                                    where t.bldg_street_idx is not null
                                        and regexp_replace(lot_idx_end::text,'^([0-9]{1,5})\.([0-9]{1,5})$',
                                                    '\\1','g')::integer
                                                    = t.bldg_street_idx::integer
                                     ) f1
                                where lot_idx_end = max_thing       )
                update %(tmp_tbl)s t set bbl = d.bbl from upd d where t.id = d.id;


                -- COPY OVER LOT COUNTS
                update %(tmp_tbl)s s set lot_cnt = (select count(l.bbl) from %(db_tbl)s l
                                                     where s.bbl is not null
                                                     and l.bbl is not null
                                                     and l.bbl=s.bbl);


                -- COPY OVER GEOM FOR MATCHING BBL
                update %(tmp_tbl)s s set geom = pc.geom
                    from pluto_centroids pc
                    where   pc.bbl = s.bbl
                            and pc.bbl is not null;


                -- COPY ALL NEW DATA BACK TO WORKING TABLE (i.e., seamless, yelp)
                update %(db_tbl)s l set geom = t.geom
                    from %(tmp_tbl)s t
                    where t.geom is not null and t.id = l.%(id_col)s;


                -- DROP TMP TABLE
                DROP TABLE IF EXISTS %(tmp_tbl)s;

            """ % self.T)

            # no_geoms = self.T.pd.read_sql('select count(*) c from %(tmp_tbl)s where geom is null'%self.T,self.T.eng).c[0]

            # 6. provide result info
            print '\tTABLE:',working_table
            print addr_tot,'\t\ttotal addresses without geom [%s]'%working_table
            print addr_uniq,'\t\t# of unique addresses [%s]'%working_table
            print addr_recog,'\t\t\trecognized'
            print addr_unrecog,'\t\t\tnot_recog'
            print addr_TCL,'\t\t\tto_check_later'
            # print tmp_rows,'\t\trows in %(tmp_tbl)s' % self.T
            # print no_geoms,'\t\trows without geoms'

        def add_geom_using_external(self,working_tbl,print_gps=True):
            """

            Usages:

                 add_geom_using_geocoding(self,working_tbl=('seamless' | 'yelp' | 'mnv'))

            """


            tbl                         =   working_tbl
            print_gps                   =   False


            df,T = self.prep_vendor_data_for_adding_geom(data_type='db',
                                                         data_set=tbl,
                                                         purpose='google_geocode')
            addr_start_cnt = len(df)
            df['zipcode'] = df.zipcode.map(lambda s: '' if str(s).lower()=='nan' else str(int(s)))
            df['chk_addr'] = df.ix[:,['address','zipcode']].apply(lambda s: str(s[0]+', New York, NY, '+str(s[1])).strip(),axis=1)
            uniq_addr_start_cnt = len(df.chk_addr.unique().tolist())

            # get google geocode results
            all_chk_addr = df.chk_addr.tolist()
            uniq_addr = self.T.pd.DataFrame({'addr':all_chk_addr}).addr.unique().tolist()
            uniq_addr_dict = dict(zip(uniq_addr,range(len(uniq_addr))))
            _iter = self.T.pd.Series(uniq_addr).iterkv()

            # if two vendors have same address: only one id will be associated with address

            y,z=[],[]
            pt,s=0,'Address\tZip\tLat.\tLong.\r'
            #    print '\n"--" means only one result found.\nOtherwise, numbered results will be shown.'
            if print_gps==True: print s
            for k,it in _iter:
                try:
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
                            z.append(k)
                            a=str(i)+'\t'+str(it.rstrip())+'\t'+str(res.postal_code)+'\t'+str(res.coordinates[0])+'\t'+str(res.coordinates[1])
                            s+=a+'\r'
                            if print_gps==True: print a

                    else:

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
                        z.append(k)
                        a='--'+'\t'+str(it.rstrip())+'\t'+str(results.postal_code)+'\t'+str(results.coordinates[0])+'\t'+str(results.coordinates[1])
                        s+=a+'\r'
                        if print_gps==True: print a

                except:
                    pass

                pt+=1
                if pt==5:
                    delay(2.6)
                    pt=0

            d = self.T.pd.DataFrame(y)
            d['iter_keys'] = z
            d['lat'],d['lon'] = zip(*d.geometry.map(lambda s: (s['location']['lat'],s['location']['lng'])))
            tbl_dict = dict(zip(df.chk_addr.tolist(),df.id.tolist()))
            d['%s_id'%tbl] = d.orig_addr.map(tbl_dict)

            # push orig_df to pgSQL
            d['geometry'] = d.geometry.map(str)
            d['res_data'] = d.res_data.map(str)
            self.T.conn.set_isolation_level(0)
            self.T.cur.execute( """drop table if exists tmp;""")
            d.to_sql('tmp',self.T.eng)
            self.T.conn.set_isolation_level(0)
            self.T.cur.execute("""
                alter table tmp add column gid serial primary key;
                update tmp set gid = nextval(pg_get_serial_sequence('tmp','gid'));
            """)
            # update 'geocoded' and $tbl
            cmd="""
            with upd as (
                        update geocoded g
                        set
                            addr_valid = t.addr_valid,
                            form_addr = t.form_addr,
                            geometry = t.geometry,
                            orig_addr = t.orig_addr,
                            partial_match = t.partial_match,
                            res_data = t.res_data,
                            res_i = t.res_i,
                            lat = t.lat,
                            lon = t.lon,
                            %(db_tbl)s_id = t.%(db_tbl)s_id
                        from tmp t
                        where g.orig_addr = t.orig_addr
                        returning t.orig_addr orig_addr
                    )
            insert into geocoded (
                                    addr_valid,
                                    form_addr,
                                    geometry,
                                    orig_addr,
                                    partial_match,
                                    res_data,
                                    res_i,
                                    lat,
                                    lon,
                                    %(db_tbl)s_id
                                )
            select
                    t.addr_valid,
                    t.form_addr,
                    t.geometry,
                    t.orig_addr,
                    t.partial_match,
                    t.res_data,
                    t.res_i,
                    t.lat,
                    t.lon,
                    t.%(db_tbl)s_id
            from
                tmp t,
                (select array_agg(f.orig_addr) upd_addrs from upd f) as f1
                where (not upd_addrs && array[t.orig_addr]
                        or upd_addrs is null);

            UPDATE %(db_tbl)s t set geom = st_setsrid(st_makepoint(g.lon,g.lat),4326)
                FROM geocoded g
                WHERE g.addr_valid is true
                and g.%(db_tbl)s_id = t.%(id_col)s
                and t.geom is null;

            """%T
            self.T.conn.set_isolation_level(0)
            self.T.cur.execute(cmd)

            # provide result info
            uniq_search_queries = len(d['%s_id'%tbl].unique().tolist())
            search_query_res_cnt = len(d)
            single_res_cnt = len(d[d.res_i==-1])
            remaining_no_addr = self.T.pd.read_sql('select count(*) c from %s where geom is null'%tbl,self.T.eng).c[0]

            print '\tTABLE:',tbl
            print addr_start_cnt,'\t total addresses in %s'%tbl
            print uniq_addr_start_cnt,'\t unique addresses in %s'%tbl
            print uniq_search_queries,'\t # of unique Search Queries'
            print search_query_res_cnt,'\t # of Search Query Results'
            print single_res_cnt,'\t # of Query Results with a Single Result'
            print remaining_no_addr,'\t # of Vendors in %s still without geom'%tbl
        def update_lot_pt_idx(self):
            a="""
            update lot_pts set lot_idx_start =
                (to_char(regexp_replace(lot_idx_start::text,
                                        '^([0-9]{1,5})\.([0-9]{1,5})$',
                                        '\\1','g')::integer,'00000')
                    ||'.'|| trim(leading ' ' from to_char(bldg_num_start,'00000')))::numeric(10,5)
            where regexp_replace(lot_idx_start::text,'^([0-9]{1,5})\.([0-9]{1,5})$','\\2','g')::integer
                != bldg_num_start::integer
            """
            return

    class Make:

        def __init__(self,_parent):
            self.T                          =   _parent.T

        def scrape_lattice(self,pt_buff_in_miles,lattice_table_name):
            meters_in_one_mile              =   1609.34

            z                               =   self.T.pd.read_sql("select min(lat) a,max(lat) b,min(lon) c,max(lon) d from lws_vertices_pgr",self.eng)
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
            lat_range                       =   self.T.pd.read_sql(lat_cmd,self.T.eng).lat_dist[0] + (pt_buff_in_miles * meters_in_one_mile)
            lon_range                       =   self.T.pd.read_sql(lon_cmd,self.T.eng).lon_dist[0] + (pt_buff_in_miles * meters_in_one_mile)
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
            min_x,min_y                     =   self.T.pd.read_sql(cmd,self.T.eng).ix[0,['min_x','min_y']]

            # create lattice table
            self.T.conn.set_isolation_level(           0)
            self.T.cur.execute(                        """
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
                    self.T.conn.set_isolation_level(   0)
                    self.T.cur.execute(                cmd)

            T                               =   {  'latt_tbl'           :   lattice_table_name,
                                                   'tmp_tbl'            :   'tmp_'+INSTANCE_GUID,
                                                   'tmp_tbl_2'          :   'tmp_'+INSTANCE_GUID+'_2',
                                                   'tmp_tbl_3'          :   'tmp_'+INSTANCE_GUID+'_3',
                                                   'buf_rad'            :   str(int((pt_buff_in_miles *
                                                                              meters_in_one_mile)/2.0))}

            self.T.conn.set_isolation_level(           0)
            self.T.cur.execute(                        """
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
            assert True                    ==   self.T.pd.read_sql(""" select all_bbl=uniq_bbl _bool
                                                                from
                                                                    (select count(distinct y1.bbl) uniq_bbl
                                                                        from %(latt_tbl)s y1) as f1,
                                                                    (select count(y2.bbl) all_bbl
                                                                        from %(latt_tbl)s y2) as f2
                                                            """ % T,self.T.eng)._bool[0]

        def usps_table(self):
            self.T.py_path.append(                        self.T.os_environ['BD'] + '/geolocation/USPS')
            from USPS_syntax_pdf_scrape         import load_from_file
            self.T.py_path.append(                        self.T.os_environ['BD'] + '/html')
            from scrape_vendors                 import Scrape_Vendors
            SV = Scrape_Vendors()

            # Files
            dir_path                                =   self.T.os_environ['BD'] + '/geolocation/USPS'
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

            self.T.conn.set_isolation_level(0)
            self.T.cur.execute("""

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
            z = self.T.pd.read_csv(src)
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

        def nyc_snd(self,table_name='snd',drop_prev=True):
            from f_nyc_data import load_parsed_snd_datafile_into_db
            load_parsed_snd_datafile_into_db(table_name,drop_prev)

        def regex_repl(self):
            """

            NOTE:
                Because this table is used within a lua function (z_custom_addr_pre_filter),
                some syntax differences exist between regex_replace in pgSQL and the below regex expressions.

                SO, USE LUA CONSOLE TO TEST!

                    addr = "5|LITTLE WEST 12 STREET"
                    p = "([0-9]+)%|(LITTLE W[\.]?[E]?[S]?[T]?[%s]12)[T]?[H]?[%s]?(.*)$"
                    r = "%1|LITTLEQQQQWESTQQQQ12 %3"
                    print(addr:gsub(p,r))

                Some of the differences:

                    1. escape character is percentage symbol '%' instead of backslash '\'
                    2. no numerical quantifiers, i.e., {3} or {3,} or {3,7}
                    3. no alternate patterns, i.e., (one|two)

            ALSO NOTE:

                Below expressions cannot reference replacements for captures above 9.

                For example, the attempted replacement of `capture #37` would result in `capture #3` + `7`

                Lua does not yet provide mechanism to name captures. From lua-users.org:

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

                    -- AVENUE B --> B AVENUE
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(AVENUE)([%s]+)([A-F])([%s]*)(.*)',
                        '%1|%4 %2 %3 %5','','0'),

                    -- AVENUE OF THE AMERICAS
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(AVE?N?U?E?[%s]+O?F?)[%s]+[THE]*[%s]*(AMERI?C?A?S?[%s]*)(.*)',
                        '%1|6 AVENUE %4','','0'),


                    -- AVENUE OF THE FINEST
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(AVE[NUE]*[%s]+OF[%s]+)[THE]*[%s]*(FINEST?)[%s]*(.*)',
                        '%1|AVENUEQQQQOFQQQQTHEQQQQFINEST %4','','0'),


                    -- 3 AVENUE --> 0 3 AVENUE  (b/c street num required for parsing)
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(AVENUE)[%s]?([a-zA-Z]*)$',
                        '0|%1 %2 %3','','0'),
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(AVE)[%s]?([a-zA-Z]*)$',
                        '0|%1 %2 %3','','0'),
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(AV)[%s]?([a-zA-Z]*)$',
                        '0|%1 %2 %3','','0'),


                    -- special streets where 'EAST' and 'WEST' don't refer to an end of a street
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(WEST)%s(END)%s(AV)(.*)$',
                        '%1|%2QQQQ%3 %4%5','','1'),
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(EAST)%s(RIVER)%s(DR)(.*)$',
                        '%1|%2QQQQ%3 %4%5','','1'),


                    -- b/c PIKE in 'PIKE SLIP' does not refer to a highway
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(PI)(KE)[%s]+(SLIP)(.*)$',
                        '%1|%2QQQQ%3 %4%5','','1'),

                    -- b/c WALL in 'WALL STREET' no longer refers to a wall
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(WALL)[%s]+(STR?E?E?T?)[%s]?(.*)$',
                        '%1|WAQQQQQLL %3 %4','','1'),


                    -- b/c WEST in 'LITTLE WEST 12 STREET' does not refer to the west end of Little West 12th Street
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(LITTLE W[.]?[E]?[S]?[T]?[%s]12)[T]?[H]?[%s]?(.*)$',
                        '%1|LITTLEQQQQWESTQQQQ12 %3','','1'),


                    -- STREETS WITH STREET NUMBERS HAVING '1/2'
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(1)%s(/2)[%s]+(.*)',
                        '%1 %2%3|%4','','1'),

                    -- PARSER HANDLED STREETS WITH TERRACE SHORTENED BETTER
                    ('custom_addr_pre_filter',
                        '([^|]*)|(.*)(%s)(TERRACE)([%s]*)([a-zA-Z]*)$',
                        '%1|%2 TERR %5','','2'),

                    -- STREETS WITH SPANISH 'LA' EXCEPT IT DOESN'T STAND FOR 'LANE'
                    ('custom_addr_pre_filter',
                        '([^|]*)|(LA)[%s]+(.*)',
                        '%1|%2QQQQ%3','','3'),

                    -- STREETS WITH MISSING/MISPELLED TAIL LETTERS, e.g., 'STREE', 'AV', 'P'
                    ('custom_addr_pre_filter',
                        '([^|]*)|(.*)[%s]+(STR?E?E?T?)$',
                        '%1|%2 STREET','','3'),
                    ('custom_addr_pre_filter',
                        '([^|]*)|(.*)[%s]+(AVE?N?U?E?)$',
                        '%1|%2 AVENUE','','3'),
                    ('custom_addr_pre_filter',
                        '([^|]*)|(.*)[%s]+(PL?A?C?E?)$',
                        '%1|%2 PLACE','','3'),


                    ('custom_addr_pre_filter',
                        '([0-9]+)[%-]([a-zA-Z0-9]+)%|(.*)',
                        '%1|%3, Bldg. %2','','4'),
                    ('custom_addr_pre_filter',
                        '([0-9]+)([a-zA-Z]+)%|(.*)',
                        '%1|%3, Bldg. %2','','5'),
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(.*)(,%s)(Bldg%.)%s([a-zA-Z0-9]+)$',
                        'Bldg. %5, %1|%2','g','6'),
                    ('custom_addr_pre_filter',
                        '([^%|]*)%|[%s]*(.*)[%s]*',
                        '%1 %2','g','7')

                ;
            """
            self.T.conn.set_isolation_level(               0)
            self.T.cur.execute(                            a)

        def tmp_addr_idx_pluto(self):
            cmd                         =   """
                drop table if exists tmp_addr_idx_pluto;
                create table tmp_addr_idx_pluto as
                    select * from z_parse_NY_addrs(
                        'select gid,address,zipcode from pluto
                        where address is not null order by gid');

                select z_make_column_primary_serial_key( 'tmp_addr_idx_pluto', 'gid', true);
                                            """
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    cmd)
            tmp_tbl_matches_pluto       =   """
                select pluto_cnt=tmp_cnt is_true from
                    (select count(distinct src_gid) tmp_cnt
                        from tmp_addr_idx_pluto) as f1,
                    (select count(distinct gid) pluto_cnt
                        from pluto where address is not null) as f2;
                                            """
            assert self.T.pd.read_sql(tmp_tbl_matches_pluto,self.T.eng).is_true[0]==True
            tmp_tbl_appears_valid       =   """
                select count(*)=0 is_true from tmp_addr_idx_pluto where
                    box is not null
                    or unit is not null
                    or pretype is not null
                    or qual is not null
                    or (sufdir is not null and sufdir != 'N'
                         and sufdir != 'E' and sufdir != 'W' and sufdir != 'S' )
                    or name is null
                    or city is null
                    or state is null
                    or zip is null or zip = '0'
                    or num is null
                                            """
            assert self.T.pd.read_sql(tmp_tbl_appears_valid,self.T.eng).is_true[0]==True

        def tmp_addr_idx_snd(self):
            # TMP_SND
            a="""
            drop table if exists tmp_snd;

            create table tmp_snd as
            select distinct on (primary_name) concat('0 ',primary_name) address,'11111'::integer zipcode
            from snd;

            select z_make_column_primary_serial_key( 'tmp_snd', 'gid', true);

            """
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    a)
            # Remove from TMP_SND
            full_entries_with_words = [' APPR','APPROACH',' EXIT','ENTRANCE','PEDESTRIAN',
                                       'DRIVE NB','DRIVE SB','NORTHBOUND','SOUTHBOUND',' HOUSES',
                                       'FERRY ROUTE','TERMINAL','RAMP',' HOSPITAL',' UNDERPASS',
                                       ' PATH',' PK-NEAR',' HSPTL',' EXPWY','COMPLEX',
                                       ' PLAYGROUND',' STATION',' WALK',' FIELDS','(SITE 7 )',' GREENWAY','PS ',
                                       'CMPX',' YARD',' MEMORIAL',
                                       ' COLLEGE',' TUNNEL',' TOWERS',' NB',' SB',' ET '
                                      ' SLIP ',' INSTITUTE ',' PROMENADE',' BUILDING','CITY LIMIT',' EXPRESSWAY',
                                       ' CITY',' HOUSE',' EN','IND-A','(GROUP 5 )','METRO NORTH','MEDICAL CENTER',
                                       'TAFT REHABS','THE MALL','UNNAMED STREET','AUX PO',
                                      'GR HILL','CHELSEA PIERS','UNIVERSITY','HIGH LINE','MANHATTAN MARINA',
                                       'WASHINGTON HTS','SOUTH ST VIADUCT','SOUTH STREET SEAPORT',
                                       'RANDALLS ISLAND','MANHATTANVILLES']
            for it in full_entries_with_words:
                a = "delete from tmp_snd where address ilike '%s'" % ('%%'+it+'%%')
                self.T.conn.set_isolation_level(       0)
                self.T.cur.execute(                    a)
            # CLEAN ADDRESS IN TMP_SND
            remove_suffix = [' LOOP',' TRANSVERSE',' CROSSING', 'EXTENSION',' REHAB']
            for it in remove_suffix:
                a = "update tmp_snd set address = regexp_replace(address,'%s','')" % it
                self.T.conn.set_isolation_level(       0)
                self.T.cur.execute(                    a)
            fix_extra_end_spaces = "update tmp_snd set address = regexp_replace(address,'[\s]+$','')"
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    fix_extra_end_spaces)
            # de-dupe
            T = {'tbl':'tmp_snd',
                 'uid_col':'gid',
                 'partition_col':'address',
                 'sort_col':'gid'}
            a="""
                drop table if exists tmp1;
                create table tmp1 as
                    WITH res AS (
                        SELECT
                            t.%(uid_col)s t_%(uid_col)s,
                            ROW_NUMBER() OVER(PARTITION BY t.%(partition_col)s
                                              ORDER BY %(sort_col)s ASC) AS rk
                        FROM %(tbl)s t
                        )
                    SELECT s.t_%(uid_col)s t_%(uid_col)s
                        FROM res s
                        WHERE s.rk = 1;

                drop table if exists tmp2;

                create table tmp2 as
                    select *
                    from %(tbl)s t1
                    WHERE EXISTS (select 1 from tmp1 t2 where t2.t_%(uid_col)s = t1.%(uid_col)s);
                drop table %(tbl)s;

                create table %(tbl)s as select * from tmp2;
                alter table %(tbl)s add primary key (%(uid_col)s);

                drop table if exists tmp1;
                drop table if exists tmp2;
                """%T
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    a)
            fix_wall_streets = """
            update tmp_snd set address = regexp_replace(address,'WALL STREET','WALLQQQQSTREET')
            where address ilike '%wall street %'
            """
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    fix_wall_streets)

            # Reload tmp_addr_idx_snd
            cmd                         =   """
                drop table if exists tmp_addr_idx_snd;
                create table tmp_addr_idx_snd as
                    select * from z_parse_NY_addrs(
                        'select gid,address,zipcode from tmp_snd order by gid');

                select z_make_column_primary_serial_key( 'tmp_addr_idx_snd', 'gid', true);


            delete from tmp_addr_idx_snd where bldg is not null or unit is not null or city is null;
            alter table tmp_addr_idx_snd
                drop column bldg, drop column box,drop column unit,
                drop column pretype,drop column qual,drop column predir
                drop column num,drop column qual,drop column predir,
                drop column zip,drop column city,drop column state;

            delete from tmp_addr_idx_snd s
            using (
                select array_agg(concat(t.predir,' ',t.name,' ',t.suftype,' ',t.sufdir)) all_idx
                from tmp_addr_idx_pluto t) as f1
            where concat(s.predir,' ',s.name,' ',s.suftype,' ',s.sufdir) = any (all_idx);

                                            """
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    cmd)
            return

        def addr_idx(self):
            self.T.tmp_addr_idx_pluto()
            self.T.tmp_addr_idx_snd()

            # Take all uniq from tmp_addr_idx pluto & snd
            T = {'new_tbl':'tmp_addr_idx',
                 'old_tbl':'tmp_addr_idx_pluto',
                 'uid_col':'gid',
                 'partition_col':'name',
                 'sort_col':'num',
                 'sort_method_1':'ASC',
                 'sort_method_2':'DESC',
                 'wc':'%'}
            a="""

            alter table %(old_tbl)s add column num_fl double precision,add column zip_int integer;
            update %(old_tbl)s set num = regexp_replace(num,' 1/2','.5')
            where num ilike '%(wc)s1/2%(wc)s';
            update %(old_tbl)s set num_fl = num::double precision,zip_int = zip::integer;
            alter table %(old_tbl)s drop column num,drop column zip,drop column num_int;
            alter table %(old_tbl)s rename column num_fl to num;
            alter table %(old_tbl)s rename column zip_int to zip;
            alter table %(old_tbl)s drop column if exists num_fl,drop column if exists zip_int;

            drop table if exists %(new_tbl)s;
            create table %(new_tbl)s as
                WITH res AS (
                    SELECT
                        t.%(uid_col)s t_%(uid_col)s,
                        ROW_NUMBER() OVER(PARTITION BY concat(t.predir,' ',t.name,' ',t.suftype,' ',t.sufdir)
                                          ORDER BY %(sort_col)s %(sort_method_1)s) AS rk
                    FROM %(old_tbl)s t
                    )
                SELECT t.*
                FROM
                    res s,
                    %(old_tbl)s t
                WHERE s.rk = 1
                and t.%(uid_col)s = s.t_%(uid_col)s;

            alter table %(new_tbl)s add column num_max double precision,add column num_min double precision;
            update %(new_tbl)s set num_min = num;

            WITH res AS (
                SELECT
                    t.%(uid_col)s t_%(uid_col)s,
                    ROW_NUMBER() OVER(PARTITION BY concat(t.predir,' ',t.name,' ',t.suftype,' ',t.sufdir)
                                      ORDER BY %(sort_col)s %(sort_method_2)s) AS rk
                FROM %(old_tbl)s t
                )
            UPDATE %(new_tbl)s t1
            SET num_max = t2.num
            FROM
                res s,
                %(old_tbl)s t2
            WHERE s.rk = 1
            and t2.%(uid_col)s = s.t_%(uid_col)s
            and concat(t1.predir,' ',t1.name,' ',t1.suftype,' ',t1.sufdir) =
            concat(t2.predir,' ',t2.name,' ',t2.suftype,' ',t2.sufdir);

            alter table tmp_addr_idx
                drop column orig_addr,drop column box,drop column unit,
                drop column pretype,drop column qual,drop column num;

            """ % T
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    a)
            return

        def pluto_changes(self):
            """
                CHANGES MADE INITIALLY AND RECORDED HERE BUT THIS FUNCTION IS NOT YET TESTED
            """
            a                       =   """
                update pluto set gid = regexp_replace(gid,'([0-9]+)([O])(.*)','\\10\\2','g')
                    where gid = 20453
                        or gid = 15296
                        or gid = 40214
                        or gid = 31800
                        or gid = 30225
                        or gid = 26608
                        or gid = 36230;
            """



class To_Class:
    def __init__(self, init=None):
        if init is not None:
            self.__dict__.update(init)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

class pgSQL:

    def __init__(self):
        import                                  datetime            as dt
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
        from sys                            import path             as py_path
        py_path                             =   py_path
        py_path.append(                         os_environ['HOME'] + '/.scripts')
        from system_settings                import DB_HOST,DB_PORT
        # from System_Control               import System_Reporter
        # SYS_r                               =   System_Reporter()
        import                                  pandas          as pd
        # from pandas.io.sql                import execute              as sql_cmd
        pd.set_option(                         'expand_frame_repr', False)
        pd.set_option(                              'display.max_columns', None)
        pd.set_option(                              'display.max_rows', 1000)
        pd.set_option(                              'display.width', 180)
        np                                  =   pd.np
        np.set_printoptions(                    linewidth=200,threshold=np.nan)
        import                                  geopandas       as gd
        from sqlalchemy                         import create_engine
        from logging                            import getLogger
        from logging                            import INFO             as logging_info
        getLogger(                                  'sqlalchemy.dialects.postgresql').setLevel(logging_info)
        eng                                 =   create_engine(r'postgresql://postgres:postgres@%s:%s/%s'
                                                          %(DB_HOST,DB_PORT,'routing'),
                                                          encoding='utf-8',
                                                          echo=False)
        from psycopg2                           import connect          as pg_connect
        pd                                  =   pd
        gd                                  =   gd
        conn                                =   pg_connect("dbname='routing' "+
                                                             "user='postgres' "+
                                                             "host='%s' password='' port=8800" % DB_HOST);
        cur                                 =   conn.cursor()

        D                                   =   {'pd'           :   pd,
                                                 'np'           :   np,
                                                 'gd'           :   gd,
                                                 'conn'         :   conn,
                                                 'cur'          :   cur,
                                                 'eng'          :   eng,
                                                 'os_environ'   :   os_environ,
                                                 'py_path'      :   py_path,
                                                 'guid'         :   str(get_guid().hex)[:7]}
        D.update(                               {'tmp_tbl'      :   'tmp_'+D['guid']})
        self.T                              =   To_Class(D)
        # py_path.append(                         os_path.join(os_environ['BD'],'geolocation'))
        #### from f_vendor_postgre import get_bldg_street_idx
        #### from f_vendor_postgre import get_addr_body,match_simple_regex
        #### from f_vendor_postgre import match_simple,match_simple_regex,match_levenshtein_series
        # from f_postgres import make_index,geom_inside_street_box,make_column_primary_serial_key

        # from ipdb import set_trace as i_trace; i_trace()

        self.Functions                      =   pgSQL_Functions(self)
        self.Triggers                       =   pgSQL_Triggers(self)
        self.Tables                         =   pgSQL_Tables(self)
        # self.ST_Parts                       =   ST_Parts(self)

