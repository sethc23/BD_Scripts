
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

    if describe==True: print '\n',len(B.index),'total row count in addr_idx'

    if commit==False: return B
    engine.execute('drop table if exists addr_idx')
    B.to_sql('addr_idx',engine,if_exists='append',index=False)
    engine.execute('ALTER TABLE addr_idx ADD PRIMARY KEY (nid)')
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
    from addr_idx a
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
    from addr_idx a
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

    lion_ways = self.T.gd.read_postgis("select lw.gid,lw.clean_street,lw.streetcode,lw.geom from addr_idx a "+
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
        this_nid = self.T.pd.read_sql_query("select nid from addr_idx where street = '%s' order by nid"%name,engine).ix[0,'nid']
        t.append({'street':name,
                  'nid':this_nid,
                  'geom':this_line})
    d = self.T.pd.DataFrame(t)
    engine.execute('drop table if exists temp')
    d.to_sql('temp',engine,if_exists='append',index=False)
    engine.execute('update addr_idx a set geom = ST_GeomFromText(t.geom,4326) from temp t where t.nid = a.nid and t.street = a.street')
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
    a = self.T.gd.read_postgis("select street,geom from addr_idx where geom is not null",engine)

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

    nid_start = 1+self.T.pd.read_sql_query("select nid from addr_idx order by nid desc limit 1",engine).nid.tolist()[0]
    g['nid'] = range(nid_start,nid_start+len(g))
    g['geom'] = g.geom.map(str)

    engine.execute('drop table if exists temp')
    g.to_sql('temp',engine,if_exists='append',index=False)
    engine.execute('INSERT INTO addr_idx (street, nid, geom) select street, nid, st_geomfromtext(geom,4326) from temp')
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

        def get_geocode_info(self,addr_queries):
            print 'NEED TO FIX'
            # T                           =   {'req'                  :   addr_queries}
            # cmd                         =   """select z_get_geocode_info( '%(req)s' );
            #                                 """ % T
            # self.T.conn.set_isolation_level(       0)
            # self.T.cur.execute(                    cmd)

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
            cmd=""" CREATE OR REPLACE FUNCTION z_make_column_primary_serial_key(
                        table_name text,
                        col_name text,
                        new_col boolean)
                    RETURNS text AS
                    $$

                        T = {'tbl':table_name,'uid_col':col_name}
                        if new_col:
                            p0 = "ALTER TABLE %(tbl)s ADD COLUMN %(uid_col)s SERIAL;" % T
                            e = plpy.execute(p0)

                        p2 = \"\"\"

                                ALTER TABLE %(tbl)s ADD PRIMARY KEY (%(uid_col)s);


                            \"\"\" % T
                        e = plpy.execute(p2)

                        from time import sleep
                        sleep(2)

                        p2 = \"\"\"



                                UPDATE %(tbl)s SET %(uid_col)s =
                                    nextval(pg_get_serial_sequence('%(tbl)s','%(uid_col)s'));

                            \"\"\" % T

                        plpy.log(p2)
                        e = plpy.execute(p2)

                        return 'ok'

                    $$
                    LANGUAGE plpythonu
                """
            cmd="""
                    DROP FUNCTION IF EXISTS z_make_column_primary_serial_key(text,text,boolean);

                    CREATE OR REPLACE FUNCTION z_make_column_primary_serial_key(
                        IN tbl text,
                        IN uid_col text,
                        IN new_col boolean)
                    RETURNS VOID AS
                    $$
                    DECLARE
                        _seq text;
                    BEGIN

                        IF (new_col=True)
                        THEN execute format('alter table %I add column %s serial primary key;',tbl,uid_col);
                        END IF;

                                --UPDATE %(tbl)s SET %(uid_col)s =
                                --    nextval(pg_get_serial_sequence('%(tbl)s','%(uid_col)s'));


                        execute format('alter table %I add primary key (%s);',tbl,uid_col);
                        _seq = format('%I_%s',tbl,uid_col);
                        execute format('alter table %I alter column %s set default z_next_free(''%s'',''%s'',''%s'')',
                                                   tbl,            uid_col,                    tbl,uid_col,_seq);
                        --execute format('alter table %I alter column %s set default
                        --                    nextval(pg_get_serial_sequence(''%I'',''%s''));',
                        --                ,tbl,uid_col,tbl,uid_col);

                    END;
                    $$
                    LANGUAGE plpgsql
                """
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    cmd)
        def z_next_free(self):
            cmd="""
                --DROP FUNCTION z_next_free(text, text, text);

                CREATE OR REPLACE FUNCTION z_next_free( table_name text,
                                                        uid_col text,
                                                        _seq text)
                RETURNS integer AS
                $BODY$
                stop=False
                T = {'tbl':table_name,'uid_col':uid_col,'_seq':_seq}
                p = \"\"\"

                            select count(column_name) c
                            from INFORMATION_SCHEMA.COLUMNS
                            where table_name = '%(tbl)s'
                            and column_name = '%(uid_col)s';

                    \"\"\" % T
                cnt = plpy.execute(p)[0]['c']

                if cnt==0:
                    p = "create sequence %(tbl)s_%(uid_col)s_seq start with 1;"%T
                    t = plpy.execute(p)
                    p = "alter table %(tbl)s alter column %(uid_col)s set DEFAULT z_next_free('%(tbl)s'::text, 'uid'::text, '%(tbl)s_uid_seq'::text);"%T
                    t = plpy.execute(p)
                stop=False
                while stop==False:
                    p = "SELECT nextval('%(tbl)s_%(uid_col)s_seq') next_val"%T
                    try:
                        t = plpy.execute(p)[0]['next_val']
                    except plpy.spiexceptions.UndefinedTable:
                        p = "select max(%(uid_col)s) from %(tbl)s;" % T
                        max_num = plpy.execute(p)[0]['max']
                        T.update({'max_num':str(max_num)})
                        p = "create sequence %(tbl)s_%(uid_col)s_seq start with %(max_num)s;" % T
                        t = plpy.execute(p)
                        p = "SELECT nextval('%(tbl)s_%(uid_col)s_seq') next_val"%T
                        t = plpy.execute(p)[0]['next_val']
                    T.update({'next_val':t})
                    p = "SELECT count(%(uid_col)s) cnt from %(tbl)s where %(uid_col)s=%(next_val)s"%T
                    chk = plpy.execute(p)[0]['cnt']
                    if chk==0:
                        stop=True
                        break
                return T['next_val']

                $BODY$
                LANGUAGE plpythonu
            """
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
                                    (select geom line1 from addr_idx where street = get_way limit 1) as l1
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
                        (select geom line1 from addr_idx where street = way1 limit 1) as _line1,
                        (select geom line2 from addr_idx where street = way2 limit 1) as _line2;
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

        def z_attempt_to_add_range_from_addr(self):
            """

            USAGE:

                select z_attempt_to_add_range_from_addr(num,predir,street_name,suftype,sufdir)
                from yelp where uid = 18486;
            """
            cmd="""

                drop function if exists z_attempt_to_add_range_from_addr(text,text,text,text,text) cascade;

                CREATE OR REPLACE FUNCTION z_attempt_to_add_range_from_addr(    IN new_street_num text,
                                                                                IN predir text,
                                                                                IN street_name text,
                                                                                IN suftype text,
                                                                                IN sufdir text)
                RETURNS text AS $$

                    if int(new_street_num) ## 2==0:
                        parity = '2'
                    else:
                        parity = '1'

                    T = {   'num'           :   new_street_num,
                            'parity'        :   parity,
                            'predir'        :   predir,
                            'name'          :   street_name,
                            'suftype'       :   suftype,
                            'sufdir'        :   sufdir}

                    p1 =    \"\"\"
                                select uid,max_num,min_num
                                from
                                    (select f1.uid,f1.max_num
                                        from
                                        (
                                        select
                                            uid,max_num,
                                            max(max_num) over (partition by block) as max_thing
                                        from pad_adr p
                                        where street_name = '##(name)s'
                                        and   predir = '##(predir)s'
                                        and   parity = '##(parity)s'
                                        and   min_num < ##(num)s
                                        order by min_num
                                        ) f1
                                    where f1.max_num=f1.max_thing) f2,
                                    (select min_num
                                    from
                                        (
                                        select block,billbbl,min_num,min(min_num) over (partition by block) as min_thing
                                        from pad_adr
                                        where street_name = '##(name)s'
                                        and   predir = '##(predir)s'
                                        and   parity = '##(parity)s'
                                        and   min_num > ##(num)s
                                        order by min_num
                                        ) f3
                                    where f3.min_num=f3.min_thing
                                    limit 1) f4
                            \"\"\" ## T

                    e1                      =   plpy.execute(p1)[0]
                    start_num               =   int(e1['max_num'])
                    end_num                 =   int(e1['min_num'])
                    for j in range(start_num+1,end_num+1):
                        if ((j ## 2==0) == (start_num ## 2==0)):
                            low_num         =   j
                            break
                    high_num = [it for it in range(low_num,end_num) if ((it ## 2==0) == (start_num ## 2==0))][-1:][0]

                    T.update(  {'uid'       :   e1['uid'],
                                'min_num'   :   low_num,
                                'max_num'   :   high_num    } )

                    p2 =    \"\"\"
                                insert into pad_adr
                                    (
                                    block,lot,bin,
                                    lhns,lcontpar,lsos,
                                    hhns,hcontpar,hsos,
                                    scboro,sc5,sclgc,stname,addrtype,realb7sc,validlgcs,parity,b10sc,segid,
                                    zipcode,bbl,stnum_w_letter,predir,street_name,suftype,sufdir,
                                    min_num,max_num,
                                    billbbl,tmp
                                    )
                                select
                                    block,lot,bin,
                                    lhns,lcontpar,lsos,
                                    hhns,hcontpar,hsos,
                                    scboro,sc5,sclgc,stname,addrtype,realb7sc,validlgcs,parity,b10sc,segid,
                                    zipcode,bbl,stnum_w_letter,predir,street_name,suftype,sufdir,
                                    ##(min_num)s,##(max_num)s,
                                    billbbl,tmp
                                from ( select * from pad_adr where uid = ##(uid)s ) f
                            \"\"\" ## T

                    plpy.execute(               p2)
                    return 'ok'

                $$ LANGUAGE plpythonu;
            """.replace('##','%')
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return

        def z_run_string_functions(self):
            a="""

                -- USE USPS ABBREVIATION GUIDE
                UPDATE  yelp y SET street_name = f2.repl
                from    (
                        select  distinct on (f1.street_name) f1.uid,
                                regexp_replace(upper(f1.street_name),upper(u.usps_abbr),upper(u.pattern)) repl
                        from
                            usps u,
                            (select uid,street_name from yelp where geom is null and street_name is not null) f1
                        where u.usps_abbr ilike f1.street_name
                        and u.pattern is not null
                        ) f2
                WHERE f2.uid = y.uid


                -- USE STRING DISTANCE
                UPDATE yelp y SET street_name = f2.jaro_b
                FROM    (
                        select (z).* from
                            (
                            select z_update_by_string_dist(array_agg(y.uid),array_agg(y.street_name),'pad_adr','street_name') z
                            from yelp y where geom is null and street_name is not null
                            ) f1
                        ) f2
                WHERE   f2.jaro > 0.8 and f2.jaro != 1.0
                        and f2.idx = y.uid

                -- CROSS WITH SND
                select z_attempt_to_add_range_from_addr(num,predir,street_name,suftype,sufdir)
                from yelp where uid = 18486



            """
        def z_update_by_crossing_with_usps(self):
            cmd="""

                DROP FUNCTION IF EXISTS z_update_by_crossing_with_usps(integer,text,text);
                CREATE OR REPLACE FUNCTION z_update_by_crossing_with_usps(  _idx            integer,
                                                                            tbl             text,
                                                                            gid_col         text)
                RETURNS text AS $$

                from traceback                      import format_exc       as tb_format_exc
                from sys                            import exc_info         as sys_exc_info

                # <<  WITH BLDG. NUMBER  >>  #

                try:

                    T = {   'tbl'       :   tbl,
                            'gid_col'   :   gid_col,
                            'idx'       :   str(_idx)     }

                    p = \"\"\"  WITH upd AS (
                                    SELECT  distinct on (s.uid)
                                            f.uid::bigint src_gid,
                                            s.to_num,s.to_predir,s.to_street_name,s.to_suftype,s.to_sufdir
                                    FROM    snd s,
                                            (   select ##(gid_col)s uid,concat_ws(' ',num,predir,street_name,suftype,sufdir ) concat_addr
                                                from ##(tbl)s where ##(gid_col)s = ##(idx)s   ) f
                                    WHERE   concat_ws(' ',s.from_num,s.from_predir,s.from_street_name,s.from_suftype,s.from_sufdir ) = f.concat_addr
                                    )
                                UPDATE ##(tbl)s t set
                                        num         =   u.to_num,
                                        predir      =   u.to_predir,
                                        street_name =   u.to_street_name,
                                        suftype     =   u.to_suftype,
                                        sufdir      =   u.to_sufdir
                                FROM    upd u
                                WHERE   u.src_gid   =   t.##(gid_col)s::bigint
                                RETURNING t.##(gid_col)s
                        \"\"\" ## T


                    plpy.log(p)
                    res                         =   plpy.execute(p)
                    if len(res)==1:
                        return "OK"
                    else:
                        return 'nothing updated'


                except:
                    plpy.log(                       "f(x) z_update_by_crossing_with_usps FAILED")
                    plpy.log(                       tb_format_exc() )
                    plpy.log(                       sys_exc_info()[0] )
                    return "error"

                $$ LANGUAGE plpythonu;



                DROP FUNCTION IF EXISTS z_update_by_crossing_with_usps(integer[],text,text);
                CREATE OR REPLACE FUNCTION z_update_by_crossing_with_usps(  _idx            integer[],
                                                                            tbl             text,
                                                                            gid_col         text)
                RETURNS text AS $$

                from traceback                      import format_exc       as tb_format_exc
                from sys                            import exc_info         as sys_exc_info

                # <<  WITH BLDG. NUMBER  >>  #

                try:

                    T = {   'tbl'       :   tbl,
                            'gid_col'   :   gid_col,
                            'idx_arr'   :   str(_idx).replace("u'","'").replace("'",'').strip('[]')     }

                    p = \"\"\"  WITH upd AS (
                                    SELECT  distinct on (s.uid)
                                            f.uid::bigint src_gid,
                                            s.to_num,s.to_predir,s.to_street_name,s.to_suftype,s.to_sufdir
                                    FROM    snd s,
                                            (   select ##(gid_col)s uid,concat_ws(' ',num,predir,street_name,suftype,sufdir ) concat_addr
                                                from ##(tbl)s where array[##(gid_col)s] && array[##(idx_arr)s]   ) f
                                    WHERE   concat_ws(' ',s.from_num,s.from_predir,s.from_street_name,s.from_suftype,s.from_sufdir ) = f.concat_addr
                                    )
                                UPDATE ##(tbl)s t set
                                        num         =   u.to_num,
                                        predir      =   u.to_predir,
                                        street_name =   u.to_street_name,
                                        suftype     =   u.to_suftype,
                                        sufdir      =   u.to_sufdir
                                FROM    upd u
                                WHERE   u.src_gid   =   t.##(gid_col)s::bigint
                                RETURNING t.##(gid_col)s
                        \"\"\" ## T


                    res                         =   plpy.execute(p)

                    plpy.log(res)

                    if len(res)>0:
                        res                     =   map(lambda s: s['##(gid_col)s' ## T],res)
                        idx                     =   [ it for it in idx if res.count(it)==0 ]

                except:
                    plpy.log(                       "f(x) z_update_with_parsed_info FAILED")
                    plpy.log(                       tb_format_exc() )
                    plpy.log(                       sys_exc_info()[0] )
                    return "error"


                $$ LANGUAGE plpythonu;

            """.replace('##','%')
            # print cmd
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return
        def z_update_by_crossing_with_snd(self):
            cmd="""

                DROP FUNCTION IF EXISTS z_update_by_crossing_with_snd(integer[],text,text);

                CREATE OR REPLACE FUNCTION z_update_by_crossing_with_snd(   _idx             integer[],
                                                                            tbl             text,
                                                                            gid_col         text)
                RETURNS text AS $$

                from traceback                      import format_exc       as tb_format_exc
                from sys                            import exc_info         as sys_exc_info

                # <<  WITH BLDG. NUMBER  >>  #

                try:

                    T = {   'tbl'       :   tbl,
                            'gid_col'   :   gid_col,
                            'idx_arr'   :   str(_idx).replace("u'","'").replace("'",'').strip('[]')     }

                    p = \"\"\"  WITH upd AS (
                                    SELECT  distinct on (s.uid)
                                            f.uid::bigint src_gid,
                                            s.to_num,s.to_predir,s.to_street_name,s.to_suftype,s.to_sufdir
                                    FROM    snd s,
                                            (   select ##(gid_col)s uid,concat_ws(' ',num,predir,street_name,suftype,sufdir ) concat_addr
                                                from ##(tbl)s where ##(gid_col)s = any ( array[##(idx_arr)s] )   ) f
                                    WHERE   concat_ws(' ',s.from_num,s.from_predir,s.from_street_name,s.from_suftype,s.from_sufdir ) = f.concat_addr
                                    )
                                UPDATE ##(tbl)s t set
                                        num         =   u.to_num,
                                        predir      =   u.to_predir,
                                        street_name =   u.to_street_name,
                                        suftype     =   u.to_suftype,
                                        sufdir      =   u.to_sufdir
                                FROM    upd u
                                WHERE   u.src_gid   =   t.##(gid_col)s::bigint
                                RETURNING t.##(gid_col)s
                        \"\"\" ## T


                    res                         =   plpy.execute(p)

                    plpy.log(res)

                    if len(res)>0:
                        res                     =   map(lambda s: s['##(gid_col)s' ## T],res)
                        idx                     =   [ it for it in idx if res.count(it)==0 ]

                except:
                    plpy.log(                       "f(x) z_update_with_parsed_info FAILED")
                    plpy.log(                       tb_format_exc() )
                    plpy.log(                       sys_exc_info()[0] )
                    return "error"



                #  <<  WITHOUT BLDG. NUMBER  >>  #
                try:

                    T.update(  {   'idx_arr'   :   str(_idx).replace("u'","'").replace("'",'').strip('[]'),     } )

                    p = \"\"\"  WITH upd AS (
                                    SELECT  distinct on (s.uid)
                                            f.uid::bigint src_gid,
                                            s.to_predir,s.to_street_name,s.to_suftype,s.to_sufdir
                                    FROM    snd s,
                                            (   select ##(gid_col)s uid,concat_ws(' ',predir,street_name,suftype,sufdir ) concat_addr
                                                from ##(tbl)s where ##(gid_col)s = any ( array[##(idx_arr)s] )   ) f
                                    WHERE   concat_ws(' ',s.from_predir,s.from_street_name,s.from_suftype,s.from_sufdir ) = f.concat_addr
                                    )
                                UPDATE ##(tbl)s t set
                                        predir      =   u.to_predir,
                                        street_name =   u.to_street_name,
                                        suftype     =   u.to_suftype,
                                        sufdir      =   u.to_sufdir
                                FROM    upd u
                                WHERE   u.src_gid   =   t.##(gid_col)s::bigint
                                RETURNING t.##(gid_col)s
                        \"\"\" ## T

                    res = plpy.execute(p)
                    plpy.log(res)
                    plpy.log(p)
                except:
                    plpy.log("f(x) z_update_with_parsed_info FAILED")
                    plpy.log(                       tb_format_exc())
                    plpy.log(                       sys_exc_info()[0])
                    return "error"

                return 'ok'


                $$ LANGUAGE plpythonu;

            """.replace('##','%')
            # print cmd
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return
        def z_update_addr_with_string_dist_on_usps(self):
            cmd="""

                DROP FUNCTION IF EXISTS z_update_addr_with_string_dist_on_usps(integer,text,text,text,text[],text,text[]);
                CREATE OR REPLACE FUNCTION z_update_addr_with_string_dist_on_usps(       idx                integer,
                                                                                         tbl                text,
                                                                                         uid_col            text,
                                                                                         addr_col           text,
                                                                                         zip_col            text,
                                                                                         compare_from_cols  text[],
                                                                                         compare_to_tbl     text,
                                                                                         compare_to_cols    text[])
                RETURNS text AS $$

                from traceback                      import format_exc       as tb_format_exc
                from sys                            import exc_info         as sys_exc_info

                T       =   {   'idx'           :   str(idx),
                                'tbl'           :   tbl,
                                'uid_col'       :   uid_col,
                                'addr_col'      :   addr_col,
                                'zip_col'       :   zip_col,
                                'comp_from_cols':   ','.join(compare_from_cols),
                                'comp_to_tbl'   :   compare_to_tbl,
                                'comp_to_cols'  :   ','.join(["'"+it+"'" for it in compare_to_cols]),   }

                #plpy.log(T)
                try:

                    p   =   \"\"\"

                            WITH upd AS (

                                SELECT f2.*
                                FROM
                                        (
                                        select (z).* from
                                            (
                                            select z_get_string_dist(       array_agg(f.uid),
                                                                            array_agg(f.comp_element),
                                                                            '##(comp_to_tbl)s'::text,
                                                                            array[ ##(comp_to_cols)s ]) z
                                            from
                                                (
                                                -- SELECT LAST ELEMENT FROM VALUE WHEN SPLIT BY ' '
                                                select
                                                    uid,
                                                    split_part(f_str, ' ', array_upper(regex_split,1)) comp_element
                                                from
                                                    (
                                                    select
                                                        uid,
                                                        regexp_split_to_array(comp_cols, ' ') regex_split,
                                                        comp_cols f_str
                                                    from
                                                        (
                                                        select
                                                            src_gid::integer uid,
                                                            ##(comp_from_cols)s comp_cols
                                                        from
                                                            (
                                                            select (z).*
                                                            from
                                                                (
                                                                    select z_parse_NY_addrs('
                                                                    select
                                                                        ##(uid_col)s::bigint gid,
                                                                        ##(addr_col)s::text address,
                                                                        ##(zip_col)s::bigint zipcode
                                                                    FROM ##(tbl)s
                                                                    WHERE ##(uid_col)s = ##(idx)s
                                                                        ') z
                                                                ) fe4
                                                            ) fe3
                                                        ) fe2
                                                    ) fe1
                                                ) f
                                            ) f1
                                        ) f2
                                WHERE   f2.jaro > 0.8 and f2.jaro != 1.0
                                ORDER BY f2.jaro DESC
                                LIMIT 1
                                )
                            UPDATE ##(tbl)s t SET
                                ##(addr_col)s = regexp_replace(upper(t.address),u.orig_str,u.jaro_b,'g')
                            FROM upd u
                            WHERE u.idx = t.##(uid_col)s
                            RETURNING t.##(uid_col)s uid

                            \"\"\" ## T

                    plpy.log(p)
                    res = plpy.execute(p)
                    plpy.log(res)
                    if len(res)==1:
                        return "OK"
                    else:
                        return 'nothing updated'

                except Exception as e:
                    plpy.log(                       tb_format_exc())
                    plpy.log(                       sys_exc_info()[0])
                    plpy.log(                       e)
                    return "ERROR"

                $$ LANGUAGE plpythonu;
            """.replace('##','%')
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return
        def z_update_addr_with_string_dist_on_snd(self):
            cmd="""

                DROP FUNCTION IF EXISTS z_update_addr_with_string_dist_on_snd(  integer,text,text,text,
                                                                                text,text[]);
                CREATE OR REPLACE FUNCTION z_update_addr_with_string_dist_on_snd(       idx                 integer,
                                                                                        tbl                 text,
                                                                                        uid_col             text,
                                                                                        addr_col            text,

                                                                                        zip_col             text,
                                                                                        compare_from_cols   text[])
                RETURNS text AS $$

                from traceback                      import format_exc       as tb_format_exc
                from sys                            import exc_info         as sys_exc_info

                T       =   {   'idx'           :   str(idx),
                                'tbl'           :   tbl,
                                'uid_col'       :   uid_col,
                                'addr_col'      :   addr_col,
                                'zip_col'       :   zip_col,
                                'comp_from_cols':   ','.join(compare_from_cols),

                                'comp_to_tbl'   :   'snd',
                                'comp_to_cols_1':   'primary_name',
                                'comp_to_cols_2':   'variation',}

                #plpy.log(T)
                try:

                    p   =   \"\"\"

                            WITH upd_1 AS (

                                SELECT f2.*
                                FROM
                                        (
                                        select (z).* from
                                            (
                                            select z_get_string_dist(       array_agg(f.uid),
                                                                            array_agg(f.comp_element),
                                                                            '##(comp_to_tbl)s'::text,
                                                                            array[ '##(comp_to_cols_1)s' ]) z
                                            from
                                                (
                                                select
                                                    src_gid::integer uid,
                                                    concat_ws(' ',##(comp_from_cols)s) comp_element
                                                from
                                                    (
                                                    select (z).*
                                                    from
                                                        (
                                                            select z_parse_NY_addrs('
                                                            select
                                                                ##(uid_col)s::bigint gid,
                                                                ##(addr_col)s::text address,
                                                                ##(zip_col)s::bigint zipcode
                                                            FROM ##(tbl)s
                                                            WHERE ##(uid_col)s = ##(idx)s
                                                            ') z
                                                        ) fe1
                                                    ) fe
                                                ) f
                                            ) f1
                                        ) f2

                                WHERE   f2.jaro > 0.8 and f2.jaro != 1.0
                                ORDER BY f2.jaro DESC
                                LIMIT 1
                            ),
                            upd_2 AS (

                                SELECT f2.*
                                FROM
                                        (
                                        select (z).* from
                                            (
                                            select z_get_string_dist(       array_agg(f.uid),
                                                                            array_agg(f.comp_element),
                                                                            '##(comp_to_tbl)s'::text,
                                                                            array[ '##(comp_to_cols_2)s' ]) z
                                            from
                                                (
                                                select
                                                    src_gid::integer uid,
                                                    concat_ws(' ',##(comp_from_cols)s) comp_element
                                                from
                                                    (
                                                    select (z).*
                                                    from
                                                        (
                                                            select z_parse_NY_addrs('
                                                            select
                                                                ##(uid_col)s::bigint gid,
                                                                ##(addr_col)s::text address,
                                                                ##(zip_col)s::bigint zipcode
                                                            FROM ##(tbl)s
                                                            WHERE ##(uid_col)s = ##(idx)s
                                                            ') z
                                                        ) fe1
                                                    ) fe
                                                ) f
                                            ) f1
                                        ) f2

                                WHERE   f2.jaro > 0.8 and f2.jaro != 1.0
                                ORDER BY f2.jaro DESC
                                LIMIT 1
                                )

                            UPDATE ##(tbl)s t SET
                                address = regexp_replace(upper(t.address),repl_array[1],repl_array[2],'g')
                            FROM
                                (
                                SELECT
                                    idx,
                                    ARRAY[a,b] repl_array
                                FROM
                                    (
                                    select
                                        idx,
                                        regexp_split_to_table(repl_from,' ') a,
                                        regexp_split_to_table(repl_to,' ') b
                                    from
                                        (
                                        SELECT
                                            (select * from string_to_array(arr,','))[1] idx,
                                            (select * from string_to_array(arr,','))[2] repl_from,
                                            (select * from string_to_array(arr,','))[3] repl_to
                                        FROM
                                            (
                                            select CASE WHEN f1.jaro>f2.jaro THEN f1.arr ELSE f2.arr END
                                            from
                                                (select concat_ws(',',idx,orig_str,jaro_b) arr,jaro from upd_1) f1,
                                                (select concat_ws(',',idx,orig_str,jaro_b) arr,jaro from upd_2) f2
                                            ) f3
                                        ) f4
                                    ) f5
                                WHERE a!=b
                                ) f
                            WHERE f.idx::integer = t.##(uid_col)s::integer
                            RETURNING t.##(uid_col)s

                            \"\"\" ## T

                    #plpy.log(p)
                    res = plpy.execute(p)
                    #plpy.log(res)
                    if len(res)==1:
                        return "OK"
                    else:
                        return 'nothing updated'

                except Exception as e:
                    plpy.log(                       tb_format_exc())
                    plpy.log(                       sys_exc_info()[0])
                    plpy.log(                       e)
                    return "ERROR"

                $$ LANGUAGE plpythonu;
            """.replace('##','%')
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return
        def z_update_addr_with_string_dist_on_pad_adr(self):
            cmd="""

                DROP FUNCTION IF EXISTS z_update_addr_with_string_dist_on_pad_adr(integer,text,text,text,text,text[]);
                CREATE OR REPLACE FUNCTION z_update_addr_with_string_dist_on_pad_adr(      idx             integer,
                                                                                tbl             text,
                                                                                uid_col         text,
                                                                                addr_col        text,
                                                                                zip_col         text,
                                                                                compare_cols    text[])
                RETURNS text AS $$

                from traceback                      import format_exc       as tb_format_exc
                from sys                            import exc_info         as sys_exc_info

                T       =   {   'idx'           :   str(idx),
                                'tbl'           :   tbl,
                                'uid_col'       :   uid_col,
                                'addr_col'      :   addr_col,
                                'zip_col'       :   zip_col,
                                'comp_cols'     :   ','.join(["'"+it+"'" for it in compare_cols]),  }

                #plpy.log(T)
                try:

                    p   =   \"\"\"

                            WITH upd AS (

                                SELECT f2.*
                                FROM
                                        (
                                        select (z).* from
                                            (
                                            select z_get_string_dist(       array_agg(f.uid),
                                                                            array_agg(f.concat_addr),
                                                                            'pad_adr'::text,
                                                                            array[ ##(comp_cols)s ]) z
                                            from
                                                (

                                                select src_gid::integer uid,concat_ws(  ' ',predir,name,
                                                                                        suftype,sufdir) concat_addr
                                                from
                                                    (
                                                    select (z).*
                                                    from
                                                        (
                                                            select z_parse_NY_addrs('
                                                            select
                                                                ##(uid_col)s::bigint gid,
                                                                ##(addr_col)s::text address,
                                                                ##(zip_col)s::bigint zipcode
                                                            FROM ##(tbl)s
                                                            WHERE ##(uid_col)s = ##(idx)s
                                                            ') z
                                                        ) fe1
                                                    ) fe
                                                ) f
                                            ) f1
                                        ) f2
                                WHERE   f2.jaro > 0.8 and f2.jaro != 1.0
                                ORDER BY f2.jaro DESC
                                LIMIT 1
                                )
                            UPDATE ##(tbl)s t SET
                                ##(addr_col)s = regexp_replace(upper(t.address),u.orig_str,u.jaro_b,'g')
                            FROM upd u
                            WHERE u.idx = t.##(uid_col)s
                            RETURNING t.##(uid_col)s uid

                            \"\"\" ## T

                    plpy.log(p)
                    res = plpy.execute(p)
                    plpy.log(res)
                    if len(res)==1:
                        return "OK"
                    else:
                        return 'nothing updated'

                except Exception as e:
                    plpy.log(                       tb_format_exc())
                    plpy.log(                       sys_exc_info()[0])
                    plpy.log(                       e)
                    return "ERROR"

                $$ LANGUAGE plpythonu;
            """.replace('##','%')
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return
        def z_get_string_dist(self):
            cmd="""

                DROP TYPE IF EXISTS string_dist_results cascade;
                CREATE TYPE string_dist_results as (
                    idx integer,
                    orig_str text,
                    jaro double precision,
                    jaro_b text,
                    leven integer,
                    leven_b text,
                    nysiis text,
                    rating_codex text
                );

                DROP FUNCTION IF EXISTS z_get_string_dist(integer[],text,text,text[],
                                                                boolean,boolean,boolean,boolean,boolean);

                CREATE OR REPLACE FUNCTION z_get_string_dist(       idx             integer[],
                                                                    string_set      text[],
                                                                    compare_tbl     text,
                                                                    compare_col     text[],
                                                                    jaro            boolean default true,
                                                                    leven           boolean default true,
                                                                    nysiis          boolean default true,
                                                                    rating_codex    boolean default true,
                                                                    usps_repl_first boolean default true)
                RETURNS SETOF string_dist_results AS $$

                    from jellyfish                      import cjellyfish as J
                    from traceback                      import format_exc       as tb_format_exc
                    from sys                            import exc_info         as sys_exc_info

                    class string_dist_results:

                        def __init__(self,upd=None):
                            if upd:
                                self.__dict__.update(       upd)


                    important_cols = ['street_name','variation','primary_name','common_use','usps_abbr','pattern']
                    T = {   'tbl'           :   compare_tbl,
                            'concat_col'    :   ''.join(["concat_ws(' ',",
                                                         ",".join(compare_col),
                                                         ")"]),
                            'not_null_cols' :   ' is not null and '.join([it for it in compare_col
                                                                    if important_cols.count(it)>0]) + ' is not null',
                                                         }

                    #plpy.log(T)
                    try:

                        p = "select distinct ##(concat_col)s comparison from ##(tbl)s where ##(not_null_cols)s;" ## T
                        res = plpy.execute(p)
                        if len(res)==0:
                            plpy.log("string_dist_results: NO DATA AVAILABLE FROM ##(tbl)s IN ##(tbl)s" ## T)
                            return
                        else:
                            #plpy.log(res)
                            res = map(lambda s: s['comparison'],res)

                        #plpy.log("about to start")
                        for i in range(len(idx)):
                            #plpy.log("started")
                            _word               =   string_set[i].upper()
                            if not _word:
                                plpy.log(string_set)
                                plpy.log("not word")
                                plpy.log(_word)
                                yield(              None)

                            else:

                                t               =   {   'idx'               :   idx[i],
                                                        'orig_str'          :   _word   }
                                #plpy.log(t)
                                if jaro:
                                    t.update(       dict(zip(['jaro','jaro_b'],
                                                        sorted(map(lambda s: (J.jaro_distance(_word,s),s),res ) )[-1:][0])))
                                if leven:
                                    t.update(       dict(zip(['leven','leven_b'],
                                                        sorted(map(lambda s: (J.levenshtein_distance(_word,s),s),res ) )[0:][0])))
                                if nysiis:
                                    t.update(       {   'nysiis'            :   J.nysiis(_word)                 })

                                if rating_codex:
                                    t.update(       {   'rating_codex'      :   J.match_rating_codex(_word)     })

                                r               =   string_dist_results(t)
                                #plpy.log(t)
                                yield(              r)

                        return

                    except Exception as e:
                        plpy.log(                       tb_format_exc())
                        plpy.log(                       sys_exc_info()[0])
                        plpy.log(                       e)
                        return

                $$ LANGUAGE plpythonu;
            """.replace('##','%')
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return

        def z_update_with_geom_from_coords(self):
            """

            Usage:

                SELECT z_update_with_geom_from_coords(13277,'yelp','uid','latitude','longitude')
                SELECT z_update_with_geom_from_coords(uid_grp[1:5],'yelp','uid','latitude','longitude')

                SELECT z_update_with_geom_from_coords(
                    'where (age(now(),last_updated) < interval ''15 minutes'' and street_name is not null limit 10',
                    'yelp'::text,'uid'::text,'latitude'::text,'longitude'::text)

            """
            cmd="""
                DROP FUNCTION IF EXISTS z_update_with_geom_from_coords(integer,text,text,text,text);

                CREATE OR REPLACE FUNCTION z_update_with_geom_from_coords(  idx         integer,
                                                                            tbl         text,
                                                                            gid_col     text,
                                                                            lat_col     text,
                                                                            lon_col     text)
                RETURNS text AS $$

                    T = {   'idx'       :   str(idx),
                            'tbl'       :   tbl,
                            'gid_col'   :   gid_col,
                            'lat_col'   :   lat_col,
                            'lon_col'   :   lon_col,
                            'search_rad':   0.0175     }

                    p = \"\"\"

                            WITH upd AS (
                                SELECT uid,bbl,geom
                                FROM
                                    (
                                    SELECT  uid,p.bbl bbl,p.geom geom,
                                            ST_Distance_Spheroid(
                                                    p.geom,
                                                    txt_pt,
                                                    'SPHEROID["WGS 84",6378137,298.257223563]')  dist
                                    FROM
                                        pluto p,
                                        (SELECT uid,st_geomfromtext(concat_ws('','POINT (',lon,' ',lat,')'),4326) txt_pt
                                        FROM
                                            (
                                            select ##(gid_col)s uid,##(lat_col)s lat,##(lon_col)s lon
                                            from ##(tbl)s where ##(gid_col)s = ##(idx)s
                                            and ##(lat_col)s is not null
                                            and ##(lon_col)s is not null
                                            ) f2
                                        WHERE lat is not null and lon is not null
                                        ) f3
                                    WHERE st_dwithin(p.geom::geography,txt_pt::geography,##(search_rad)f*1609.34)
                                    ) f4
                                order by dist
                                limit 1
                                )

                            UPDATE ##(tbl)s t SET
                                bbl = u.bbl,
                                geom= pc.geom
                            FROM upd u,pluto_centroids pc
                            WHERE u.uid = t.##(gid_col)s
                            and u.bbl = pc.bbl
                            RETURNING u.uid ##(gid_col)s;

                        \"\"\"

                    res,cnt,stopped = 0,10,False
                    while res==0:
                        res = len(plpy.execute(p ## T))
                        plpy.log(res)
                        T.update({'search_rad':T['search_rad']+0.005})
                        cnt -= 1
                        if res>0 or cnt<=0:
                            stopped = True
                            break

                    if stopped==True:
                        return 'nothing updated'
                    else:
                        return 'ok'

                $$ LANGUAGE plpythonu;

                -- UID ARRAY FUNCTION

                DROP FUNCTION IF EXISTS z_update_with_geom_from_coords(integer[],text,text,text,text);
                DROP FUNCTION IF EXISTS z_update_with_geom_from_coords(text,text,text,text,text);
                CREATE OR REPLACE FUNCTION z_update_with_geom_from_coords(  limitations text default '',
                                                                            tbl         text default '',
                                                                            gid_col     text default '',
                                                                            lat_col     text default '',
                                                                            lon_col     text default '')
                RETURNS text AS $$

                    T = {   'tbl'       :   tbl,
                            'gid_col'   :   gid_col,
                            'lat_col'   :   lat_col,
                            'lon_col'   :   lon_col,
                            'limits'    :   'where ' + limitations.lower().lstrip('where ').replace("''","'"),
                            'search_rad':   0.0175     }

                    p = \"\"\"

                            WITH upd AS (
                                SELECT *
                                FROM
                                    (
                                    SELECT  uid,bbl,geom,dist,
                                            min(dist) over (partition by uid) as min_thing
                                    FROM
                                        (
                                        SELECT  uid,p.bbl bbl,p.geom geom,
                                                ST_Distance_Spheroid(
                                                        p.geom,
                                                        txt_pt,
                                                        'SPHEROID["WGS 84",6378137,298.257223563]')  dist
                                        FROM
                                            pluto p,
                                            (SELECT uid,st_geomfromtext(concat_ws('','POINT (',lon,' ',lat,')'),4326) txt_pt
                                            from
                                                (
                                                select ##(gid_col)s uid,##(lat_col)s lat,##(lon_col)s lon
                                                from ##(tbl)s
                                                ##(limits)s
                                                ) f2
                                            ) f3
                                        WHERE st_dwithin(p.geom::geography,txt_pt::geography,##(search_rad)f*1609.34)
                                        ) f4
                                    ) f5
                                WHERE dist = min_thing
                                )

                            UPDATE ##(tbl)s t SET
                                bbl = u.bbl,
                                geom= pc.geom
                            FROM upd u,pluto_centroids pc
                            WHERE u.uid = t.##(gid_col)s
                            and u.bbl = pc.bbl
                            RETURNING u.uid ##(gid_col)s;

                        \"\"\"

                    cnt = 10
                    while len(idx)>0:
                        res = plpy.execute(p ## T)

                        for it in res:
                            z=idx.pop(  idx.index( it[ '##(gid_col)s' ## T ] )  )

                        cnt -= 1
                        if len(idx)==0 or cnt<=0:
                            break

                        T.update({  'idx_arr'       :   str(idx).replace("u'","'").replace("'",'').strip('[]'),
                                    'search_rad'    :   T['search_rad']+0.005    })


                    return 'ok'

                $$ LANGUAGE plpythonu;
            """.replace('##','%')
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return
        def z_update_with_geom_from_parsed(self):
            cmd="""
                DROP FUNCTION IF EXISTS z_update_with_geom_from_parsed(integer,text,text);

                CREATE OR REPLACE FUNCTION z_update_with_geom_from_parsed(idx integer,tbl text,gid_col text)
                RETURNS text
                AS $$

                    from traceback                      import format_exc       as tb_format_exc
                    from sys                            import exc_info         as sys_exc_info

                    T = {   'idx'       :   str(idx),
                            'tbl'       :   tbl,
                            'gid_col'   :   gid_col,
                            'idx'       :   str(idx),     }

                    p = \"\"\"  WITH upd AS (
                                    SELECT  p.billbbl,f.uid::bigint src_gid
                                    FROM    pad_adr p,
                                            (   select ##(gid_col)s uid,num,concat_ws(' ',predir,street_name,suftype,sufdir ) concat_addr
                                                from ##(tbl)s where ##(gid_col)s = ##(idx)s   ) f
                                    WHERE   concat_ws(' ',p.predir,p.street_name,p.suftype,p.sufdir ) = f.concat_addr
                                        -- street number within range
                                    AND     (
                                            -- <<
                                            -- street number within range
                                            (   (p.min_num is not null AND p.max_num is not null)
                                                AND (p.min_num <= f.num::double precision and f.num::double precision <= p.max_num)
                                                AND p.parity::integer = (case when mod((f.num::double precision)::integer,2)=1 THEN 1 ELSE 2 END)

                                                    -- parity=2 means even, parity=1 means odd
                                            )
                                            OR
                                            -- street number equals min_max num
                                            (   (p.min_num is null OR p.max_num is null)
                                                AND (p.min_num = f.num::double precision OR p.max_num = f.num::double precision)
                                            )
                                            -- >>
                                            )
                                    )

                                UPDATE ##(tbl)s t set
                                        bbl         =   u.billbbl,
                                        geom        =   pc.geom
                                FROM    upd u, pluto_centroids pc
                                WHERE   u.src_gid   =   t.##(gid_col)s::bigint
                                AND     u.billbbl   =   pc.bbl
                                RETURNING u.src_gid uid

                        \"\"\" ## T

                    try:
                        res = plpy.execute(p)
                        if len(res)>0:
                            return 'OK'
                        else:
                            return 'nothing updated'
                    except:
                        plpy.log("f(x) z_update_with_parsed_info FAILED")
                        plpy.log(p)
                        plpy.log(                       tb_format_exc())
                        plpy.log(                       sys_exc_info()[0])
                        return 'ERROR'

                $$ LANGUAGE plpythonu;



                DROP FUNCTION IF EXISTS z_update_with_geom_from_parsed(integer[],text,text);
                CREATE OR REPLACE FUNCTION z_update_with_geom_from_parsed(idx integer[],tbl text,gid_col text)
                RETURNS text
                AS $$

                    from traceback                      import format_exc       as tb_format_exc
                    from sys                            import exc_info         as sys_exc_info

                    T = {   'idx'       :   str(idx),
                            'tbl'       :   tbl,
                            'gid_col'   :   gid_col,
                            'idx_arr'   :   str(idx).replace("u'","'").replace("'",'').strip('[]'),     }

                    p = \"\"\"  WITH upd AS (
                                    SELECT  p.billbbl,f.uid::bigint src_gid
                                    FROM    pad_adr p,
                                            (   select ##(gid_col)s uid,num,concat_ws(' ',predir,street_name,suftype,sufdir ) concat_addr
                                                from ##(tbl)s where ##(gid_col)s = any ( array[##(idx_arr)s] )   ) f
                                    WHERE   concat_ws(' ',p.predir,p.street_name,p.suftype,p.sufdir ) = f.concat_addr
                                        -- street number within range
                                    AND     (
                                            -- <<
                                            -- street number within range
                                            (   (p.min_num is not null AND p.max_num is not null)
                                                AND (p.min_num <= f.num::double precision and f.num::double precision <= p.max_num)
                                                AND p.parity::integer = (case when mod((f.num::double precision)::integer,2)=1 THEN 1 ELSE 2 END)

                                                    -- parity=2 means even, parity=1 means odd
                                            )
                                            OR
                                            -- street number equals min_max num
                                            (   (p.min_num is null OR p.max_num is null)
                                                AND (p.min_num = f.num::double precision OR p.max_num = f.num::double precision)
                                            )
                                            -- >>
                                            )
                                    )

                                UPDATE ##(tbl)s t set
                                        bbl         =   u.billbbl,
                                        geom        =   pc.geom
                                FROM    upd u, pluto_centroids pc
                                WHERE   u.src_gid   =   t.##(gid_col)s::bigint
                                AND     u.billbbl   =   pc.bbl

                        \"\"\" ## T

                    try:
                        plpy.execute(p)
                        return 'ok'
                    except:
                        plpy.log("f(x) z_update_with_parsed_info FAILED")
                        plpy.log(p)
                        plpy.log(                       tb_format_exc())
                        plpy.log(                       sys_exc_info()[0])
                        return 'error'

                $$ LANGUAGE plpythonu;

            """.replace('##','%')
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return

        def z_update_with_geocode_info(self):
            """

            Usage:

                select z_update_with_geocode_info('yelp','uid','address','postal_code')
                select z_update_with_geocode_info('seamless','id','address','zipcode')

            """
            cmd="""
                DROP FUNCTION IF EXISTS z_update_with_geocode_info(text,text,text,text);

                CREATE OR REPLACE FUNCTION z_update_with_geocode_info(  tbl      text,  gid_col text,
                                                                        addr_col text,  zip_col text)
                RETURNS text AS $$

                    T = {   'tbl'       :   tbl,
                            'gid_col'   :   gid_col,
                            'addr_col'  :   addr_col,
                            'zip_col'   :   zip_col,   }

                    p = \"\"\"

                            WITH upd AS (
                                SELECT (z).*  --,arr_uid,arr_addr
                                FROM
                                    (
                                    select z_get_geocode_info(array_agg(uid),array_agg(address)) z
                                                --,array_agg(uid) arr_uid,array_agg(address) arr_addr
                                    from
                                        (
                                        select ##(gid_col)s uid,concat_ws(', ',##(addr_col)s ,'New York, NY',##(zip_col)s) address
                                        from ##(tbl)s
                                        where street_name is null and geom is null and gc_addr is null
                                        and ##(addr_col)s  is not null and address != ''
                                        and ##(zip_col)s  is not null
                                        order by ##(gid_col)s
                                        ) f1
                                    ) f2
                                )
                            UPDATE ##(tbl)s t SET
                                gc_lat = u.lat,
                                gc_lon = u.lon,
                                gc_addr = u.std_addr,
                                gc_zip = u.zipcode,
                                gc_full_addr = u.form_addr
                            FROM upd u
                            WHERE u.addr_valid is true
                            and u.idx = t.##(gid_col)s;

                        \"\"\" ## T

                    #plpy.log(p)
                    plpy.execute(p)
                    return 'ok'

                $$ LANGUAGE plpythonu;
            """.replace('##','%')
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return
        def z_update_yelp_address_from_valid_display_addr(self):
            cmd="""
                DROP FUNCTION IF EXISTS z_update_yelp_address_from_valid_display_addr();

                CREATE OR REPLACE FUNCTION z_update_yelp_address_from_valid_display_addr()
                RETURNS VOID AS $$
                begin

                    WITH upd as (
                        select src_gid uid, orig_addr new_addr
                        from z_parse_NY_addrs('
                            select uid::bigint gid,repl address,postal_code::bigint zipcode from
                                (select
                                    uid,
                                    regexp_replace(trim(leading address||'', '' from display_address),''^([0-9]+[^,]+)(.*)$'',''\\1'',''g'') repl,
                                    regexp_matches(trim(leading address||'', '' from display_address),''^([0-9]+[^,]+)(.*)$'') matches,
                                    postal_code
                                from yelp
                                where street_name is null and geom is null and address is not null and postal_code is not null) f
                            where length(f.repl)>0
                            order by uid
                            ') z
                        where z.num is not null and z.num != '0' and z.num ~ '^([0-9]+|[.][0-9]+|[0-9]+[.][0-9]+)$'
                        and (z.suftype is not null or ( z.name ilike '%broadway%'
                                                        or z.name ilike '%bowery%'
                                                        or z.name ilike '%slip%' )   )

                        )
                    UPDATE yelp y set address = u.new_addr
                    FROM upd u
                    WHERE y.uid = u.uid;

                end;
                $$ LANGUAGE plpgsql;

            """
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return
        def z_update_with_parsed_info(self):
            cmd="""
                DROP FUNCTION IF EXISTS z_update_with_parsed_info(integer,text, text,text, text,text[], boolean);
                CREATE OR REPLACE FUNCTION z_update_with_parsed_info(idx integer,tbl text,
                                                                     gid_col text,addr_col text,
                                                                     zip_col text,
                                                                     update_cols text[] default array['num','predir','street_name','suftype','sufdir'],
                                                                     validity_check boolean default true)
                RETURNS text AS $$

                from traceback                      import format_exc       as tb_format_exc
                from sys                            import exc_info         as sys_exc_info

                T = {   'tbl'       :   tbl,
                        'gid_col'   :   gid_col,
                        'addr_col'  :   addr_col,
                        'zip_col'   :   zip_col,
                        'update'    :   ','.join( ['##s = u.##s' ## (it,it) for it in update_cols] ),
                        'idx'       :   str(idx),
                        'and_valid' :   '',}

                if validity_check:
                    T['and_valid']  =   ' '.join(["AND u.num ~ '^([0-9]+|[.][0-9]+|[0-9]+[.][0-9]+)$'",
                                                  "AND u.num != '0'"
                                                  "AND u.street_name is not null",
                                                  "AND (",
                                                    "u.suftype is not null",
                                                    "or (",
                                                        "u.street_name ilike '####broadway####'",
                                                        "or u.street_name ilike '####bowery####'"
                                                        "or u.street_name ilike '####slip####'",
                                                    ")",
                                                  ")"])

                p = \"\"\"  WITH upd AS (
                                SELECT  src_gid,bldg,box,unit,num,predir,name street_name,suftype,sufdir
                                FROM    z_parse_NY_addrs('
                                                        select
                                                            ##(gid_col)s::bigint gid,
                                                            ##(addr_col)s::text address,
                                                            ##(zip_col)s::bigint zipcode
                                                        FROM ##(tbl)s
                                                        WHERE ##(gid_col)s = ##(idx)s
                                                        ')
                                )

                            UPDATE ##(tbl)s t set
                                ##(update)s
                            FROM  upd u
                            WHERE u.src_gid = t.##(gid_col)s::bigint
                            ##(and_valid)s
                            RETURNING u.src_gid

                    \"\"\" ## T

                try:
                    res = plpy.execute(p)

                    if len(res)>0:
                        if res[0]['src_gid']==idx:
                            return 'OK'
                    else:
                        return None
                    #plpy.log(res)

                # except UndefinedColumn as e:
                #
                #     new_col_q = \"\"\"
                #                     select regexp_replace('"+e+"',
                #                         '(column [[:alnum:]]+[[:period:]])([^%s])([%s][does not exist]',
                #                         '%1')
                #                 \"\"\"
                #     T.update({ 'new_col': plpy.execute(new_col_q) })
                #
                #     ps1 = 'alter table ##(tbl)s add column %(new_col)s %(new_col_info)s' % T
                except:
                    plpy.log(tbl)
                    plpy.log(                       "f(x) z_update_with_parsed_info FAILED")
                    plpy.log(                       tb_format_exc())
                    plpy.log(                       sys_exc_info())
                    return 'WHAT2'
                    # return '\\n\\n'.join([ 'ERROR:'] + **tb_format_exc() + **sys_exc_info() ])


                $$ LANGUAGE plpythonu;

                -- << INTEGER [] >> --
                DROP FUNCTION IF EXISTS z_update_with_parsed_info(integer[],text,text,text,text,text[],boolean);

                CREATE OR REPLACE FUNCTION z_update_with_parsed_info(idx integer[],tbl text,
                                                                     gid_col text,addr_col text,
                                                                     zip_col text, update_cols text[],
                                                                     validity_check boolean default false)
                RETURNS text
                AS $$

                from traceback                      import format_exc       as tb_format_exc
                from sys                            import exc_info         as sys_exc_info

                T = {   'tbl'       :   tbl,
                        'gid_col'   :   gid_col,
                        'addr_col'  :   addr_col,
                        'zip_col'   :   zip_col,
                        'update'    :   ','.join( ['##s = u.##s' ## (it,it) for it in update_cols] ),
                        'idx_arr'   :   str(idx).replace("u'","'").replace("'",'').strip('[]'),
                        'and_valid' :   '',}

                if validity_check:
                    T['and_valid']  =   ' '.join(["AND u.num ~ '^([0-9]+|[.][0-9]+|[0-9]+[.][0-9]+)$'",
                                                  "AND u.num != '0'"
                                                  "AND u.street_name is not null",
                                                  "AND (",
                                                    "u.suftype is not null",
                                                    "or (",
                                                        "u.street_name ilike '####broadway####'",
                                                        "or u.street_name ilike '####bowery####'"
                                                        "or u.street_name ilike '####slip####'",
                                                    ")",
                                                  ")"])

                error_occurred      =   False

                p = \"\"\"  WITH upd AS (
                                SELECT  src_gid,bldg,box,unit,num,predir,name street_name,suftype,sufdir
                                FROM    z_parse_NY_addrs('
                                                        select
                                                            ##(gid_col)s::bigint gid,
                                                            ##(addr_col)s::text address,
                                                            ##(zip_col)s::bigint zipcode
                                                        FROM ##(tbl)s
                                                        WHERE ##(gid_col)s = any ( array[##(idx_arr)s] )
                                                        ')
                                )
                            UPDATE ##(tbl)s t set
                                ##(update)s
                            FROM  upd u
                            WHERE u.src_gid = t.##(gid_col)s::bigint
                            ##(and_valid)s
                            RETURNING u.src_gid

                    \"\"\" ## T

                try:
                    res = plpy.execute(p)
                    #plpy.log(res)
                    #t = str([it['src_gid'] for it in res[0]])
                    #plpy.log(t)

                except:
                    plpy.log(                       "f(x) z_update_with_parsed_info FAILED")
                    #plpy.log(                       "##(gid_col)s =  ##(idx_arr)s" ## T)
                    plpy.log(                       tb_format_exc())
                    plpy.log(                       sys_exc_info())
                    error_occurred = True

                if error_occurred:
                    return 'Finished, but errors logged'
                else:
                    return




                $$ LANGUAGE plpythonu;

            """.replace('##','%')
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return

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

                    from traceback                      import format_exc       as tb_format_exc
                    from sys                            import exc_info         as sys_exc_info

                    query_str = args[0]
                    qs,res = query_str.lower().replace('\\n',' ').replace('####','##').replace("''","'").split(' '),[]
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
                    while stop==False:
                        pt+=1

                        if q_max>0:
                            if q_offset + q_lim > q_max:
                                q_lim = q_max - q_offset

                        q_range = 'OFFSET ##s LIMIT ##s' ## (q_offset,q_lim)

                        query_dict = {   '_QUERY_STR'        :   query_str + ' ' + q_range, }


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
                        #plpy.log(q)
                        try:
                            q_res = plpy.execute(q)
                            #plpy.log(q)

                            res.extend(q_res)

                            if len(q_res)<q_lim or len(res)==q_max:
                                #plpy.log('exit 1623')
                                stop=True
                                break
                            else:
                                q_offset = q_offset + q_lim
                        except:
                            plpy.log(                       "z_parse_NY_addrs FAILED")
                            plpy.log(                       tb_format_exc())
                            plpy.log(                       sys_exc_info()[0])
                            break


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

                    function nocase (s)
                        s = string.gsub(s, "%a", function (c)
                                                    return string.format("[%s%s]", string.lower(c),
                                                                        string.upper(c))
                                    end)
                        return s
                    end

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
                            log("orig_addr: "..orig_addr)
                            log("GID: "..tostring(src_gid))
                            if true then return end
                        end
                        if not orig_addr then
                            log("orig_addr: "..orig_addr)
                            log("GID: "..tostring(src_gid))
                            if true then return end
                        end

                        s2,e2 = orig_addr:find(tmp_pt["name"])

                        if s2==nil then
                            log("orig_addr: "..orig_addr)
                            log("GID: "..tostring(src_gid))
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


                    if tmp_pt["name"] then

                    -- Return Abbreviated Street Names Back to Original Name, e.g., 'W' for West St., 'S' for South St.
                        if #tmp_pt["name"]==1 then
                            if      tmp_pt["name"]=='N' then tmp_pt["name"]='NORTH'
                            elseif  tmp_pt["name"]=='E' then tmp_pt["name"]='EAST'
                            elseif  tmp_pt["name"]=='S' then tmp_pt["name"]='SOUTH'
                            elseif  tmp_pt["name"]=='W' then tmp_pt["name"]='WEST'
                            end
                        end
                    -- Return null result if street name i_contains 'and'
                        local a = tmp_pt["name"]
                        if (   a:find("^(.*)[%s]AND[%s](.*)$")
                            or a:find("^AND[%s].*$")
                            or a:find("^.*[%s]AT[%s].*$")
                            or a:find("^.*[%s]&[%s].*$")
                            or a:find("^[0-9]+.*[%s]+.*[%s]+[0-9]+.*$")
                            ) then
                           return nil
                        end

                    end




                    return tmp_pt

                $$ LANGUAGE plluau;
            """
            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    cmd)
        def z_custom_addr_post_filter_with_iter(self):
            a=0
            # cmd="""
            #
            #     DROP FUNCTION IF EXISTS z_custom_addr_post_filter_with_iter(stdaddr[],text[],integer[]);
            #     CREATE OR REPLACE FUNCTION z_custom_addr_post_filter_with_iter(   res stdaddr[],
            #                                                             orig_addr text[],
            #                                                             src_gid integer[])
            #     RETURNS SETOF parsed_addr AS $$
            #         return _U(res,orig_addr,src_gid)
            #     end
            #     do
            #         _U = function(res,orig_addr,src_gid)
            #
            #         local some_src_cols = {"building","house_num","predir","qual","pretype","name","suftype","sufdir",
            #                                 "city","state","postcode","box","unit",}
            #
            #         local some_dest_cols = {"bldg","num","predir","qual","pretype","name","suftype","sufdir",
            #                                 "city","state","zip","box","unit"}
            #
            #
            #         for i=1, #res do
            #
            #             local tmp = res[i]
            #             local tmp_pt = {}
            #             local tmp_col = ""
            #
            #             for k,v in pairs(some_dest_cols) do
            #                 tmp_col = some_src_cols[k]
            #                 tmp_pt[v]=tmp[tmp_col]
            #             end
            #             tmp_pt["src_gid"] = src_gid[i]
            #             tmp_pt["orig_addr"] = orig_addr[i]
            #             tmp_pt["zip"]=tmp.postcode
            #
            #             -- CLEAN UP TEMP SUBSTITUTION {Qx5 = no space, Qx4 = space} < -- OUTPUT
            #             if tmp_pt["name"] then
            #                 if tmp_pt["name"]:find("QQQQQ") then
            #                     tmp_pt["name"] = tmp_pt["name"]:gsub("(QQQQQ)","")
            #                 end
            #                 if tmp_pt["name"]:find("QQQQ") then
            #                     tmp_pt["name"] = tmp_pt["name"]:gsub("(QQQQ)"," ")
            #                 end
            #                 if tmp_pt["name"]:find("AVENUE OF THE") then
            #                     tmp_pt["suftype"] = "AVE"
            #                 end
            #             end
            #
            #             local t = ""
            #             local s1,e1,s2,e2 = 0,0,0,0
            #
            #             -- DISCARD PRETYPES, MOVE THEM BACK TO 'NAME', UPDATE SUFTYPE
            #             if tmp_pt["pretype"] then
            #                 --log("1702")
            #                 if tmp_pt["num"]==0 then
            #                     s1,e1=0,0
            #                 else
            #                     s1,e1 = orig_addr[i]:find(tmp_pt["num"])
            #                 end
            #
            #                 if e1==nil then
            #                     log(tmp_pt["num"])
            #                     log(tmp_pt["name"])
            #                     log(orig_addr[i])
            #                     log(tmp_pt["pretype"])
            #                     log(src_gid[i])
            #                     if true then return end
            #                 end
            #
            #                 s2,e2 = orig_addr[i]:find(tmp_pt["name"])
            #
            #                 if s2==nil then
            #                     log(tmp_pt["num"])
            #                     log(tmp_pt["name"])
            #                     log(orig_addr[i])
            #                     log(tmp_pt["pretype"])
            #                     log(src_gid[i])
            #                     if true then return end
            #                 end
            #
            #                 t = orig_addr[i]:sub(e1+2,s2-2)
            #
            #                 -- if this string has a space, meaning at least two words, take only last word
            #                 if t:find("[%s]")==nil then
            #                     tmp_pt["name"] = t.." "..tmp_pt["name"]
            #                 else
            #                     t = t:gsub("(.*)%s([a-zA-Z0-9]+)$","%2")
            #                     tmp_pt["name"] = t.." "..tmp_pt["name"]
            #                 end
            #                 tmp_pt["pretype"] = nil
            #
            #                 t = orig_addr[i]:sub(e2+2)
            #
            #                 cmd = string.format([[  select usps_abbr abbr
            #                                         from usps where common_use ilike '%s']],t)
            #
            #                 for row in server.rows(cmd) do
            #                     t = row.abbr
            #                     break
            #                 end
            #
            #                 tmp_pt["suftype"] = t:upper()
            #
            #             end
            #
            #             -- FOR ANY PREDIR NOT 'E' OR 'W', MOVE BACK TO 'NAME'
            #             if tmp_pt["predir"] and (tmp_pt["predir"]~="E" and tmp_pt["predir"]~="W") then
            #                 --log("1742")
            #                 if tmp_pt["predir"]=='N' then t = "NORTH" end
            #                 if tmp_pt["predir"]=='S' then t = "SOUTH" end
            #
            #                 tmp_pt["predir"] = nil
            #                 tmp_pt["name"] = t.." "..tmp_pt["name"]
            #             end
            #
            #             -- WHEN UNIT CONTAINS 'PIER', e.g., 'PIER-15 SOUTH STREET' (filtered as '0 PIER-15 SOUTH STREET')
            #             if tmp_pt["unit"] then
            #                 if tmp_pt["unit"]:find('# 0 PIER') and tmp_pt["bldg"]==nil then
            #                     tmp_pt["bldg"] = "PIER "..tmp_pt["num"]
            #                     tmp_pt["num"] = 0
            #                     tmp_pt["unit"] = nil
            #                 end
            #             end
            #
            #             coroutine.yield(tmp_pt)
            #         end
            #
            #     end
            #
            #     $$ LANGUAGE plluau;
            # """
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

                    local no_num_but_avenue_cnt = addr:find("^([1]?[0-9][A-Z]?[A-Z]?[A-Z]? AVEN?U?E?)(.*)")
                    -- e.g., "5TH AVE CENTRAL PARK S"


                    if ( cnt == 0 or cnt == nil or no_num_cnt == nil or no_num_but_avenue_cnt~=nil ) then
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

        def z_add_geom_through_addr_idx(self):
            a="""
                DROP FUNCTION if exists z_add_geom_through_addr_idx(text,text) cascade;

                CREATE OR REPLACE FUNCTION z_add_geom_through_addr_idx(tbl text,uid_col text)
                RETURNS text AS $funct$

                from traceback                      import format_exc       as tb_format_exc
                from sys                            import exc_info         as sys_exc_info

                try:

                    p = \"\"\"

                        -- COPY BBL VALUE WHERE A MATCH EXISTS AND VALUE OF ADDRESS NUMBER EQUAL/BETWEEN EXISTING DB PTS
                        update %(tbl)s s set bbl = l.bbl
                            from lot_pts l
                            where
                                char_length(l.bbl::text)        >=  10
                                and s.bldg_street_idx is not null
                                and s.num is not null
                                and (
                                    to_number(concat(s.bldg_street_idx,'.',to_char(s.num::integer,'00000')),'00000.00000')
                                    between l.lot_idx_start and l.lot_idx_end
                                    );
                                and s.bbl is null


                        -- COPY BBL VALUE WHERE A MATCH EXISTS BUT THE NEW ADDRESS HAS STREET NUMBER EXCEEDING THE DB IDX
                        with upd as (   select *
                                        from
                                            (
                                            select
                                                %(uid)s,bldg_street_idx,l.bbl,l.lot_idx_end,
                                                max(l.lot_idx_end) over (partition by bldg_street_idx) as max_thing
                                            from    lot_pts l,
                                                    %(tbl)s t
                                            where t.bldg_street_idx is not null
                                                and regexp_replace(lot_idx_end::text,'^([0-9]{1,5})\.([0-9]{1,5})\$',
                                                            '\\1','g')::numeric
                                                            = t.bldg_street_idx::numeric
                                             ) f1
                                        where lot_idx_end = max_thing       )
                        update %(tbl)s t set bbl = d.bbl from upd d where t.%(uid)s = d.%(uid)s;


                        -- COPY OVER LOT COUNTS
                        update %(tbl)s s set lot_cnt = (select count(l.bbl) from %(tbl)s l
                                                             where s.bbl is not null
                                                             and l.bbl is not null
                                                             and l.bbl=s.bbl);


                        -- COPY OVER GEOM FOR MATCHING BBL
                        update %(tbl)s s set geom = pc.geom
                            from pluto_centroids pc
                            where   pc.bbl = s.bbl
                                    and pc.bbl is not null;

                        \"\"\"  ## {"tbl"                       :   tbl,
                                    "uid"                       :   uid_col  }

                    plpy.execute(p)

                except Exception, Err:
                    plpy.log('z_add_geom_through_addr_idx FUNCTION FAILED')
                    plpy.log("table: " + tbl)
                    plpy.log(tb_format_exc())
                    plpy.log(sys_exc_info()[0])
                    return
                return

                $funct$ language "plpythonu";

            """

            cmd                                 =   a.replace("##","%")
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            print cmd
            return
        def z_make_rows_with_alpha_range_lua_not_working(self):
            """
                z_make_rows_with_alpha_range('idx_col','start_range_col','end_range_col')

                EXAMPLE:
                    select z_make_rows_with_alpha_range(array[1,2,3],array['A','A','C'],array['B','C','E']);


                RETURNS:

                        idx_col =  [1           rows_ranges     =  [A,
                                    1,                              B,
                                    2,                              A,
                                    2,                              B,
                                    2,                              C,
                                    3,                              B,
                                    3,                              C,
                                    3,                              D,
                                    3]                              E]
            """
            cmd="""
                drop function if exists z_make_rows_with_alpha_range(int[],text[],text[]) cascade;
                drop function if exists z_make_rows_with_alpha_range(int,text,text) cascade;
                drop type if exists alpha_range_type;
                CREATE TYPE alpha_range_type as (
                    uid int,
                    alpha_range text
                );
                CREATE FUNCTION z_make_rows_with_alpha_range(IN uid int,IN start_r text,IN end_r text,
                                                             OUT uid_r int[], OUT alphas text[])
                AS $$
                    alphas={}
                    uid_r = {}
                    j=0
                    for j=start_r:byte(1), end_r:byte(1) do

                        if not alphas then
                            uid_r[1] = uid
                            alphas[1]=string.char(j,1)
                        else
                            uid_r[#uid_r+1] = uid
                            alphas[#alphas+1] = string.char(j,1)
                        end

                    end
                    log(#uid_r)
                    log(#alphas)
                    res = {}
                    res.uid = uid_r
                    res.alpha_range = alphas
                    --res[1] = uid_r
                    --res[2] = alphas
                    return --{uid_r,alphas}
                $$ LANGUAGE plluau;
            """
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            print cmd
            return
        def z_make_rows_with_numeric_range(self):
            """
                z_make_rows_with_numeric_range('idx_col','start_range_col','end_range_col')

                EXAMPLE:
                    select numeric_range(array[1,2,3],array[8,9,10],array[10,10,10]);


                RETURNS:

                        idx_col =  [1           rows_ranges     =  [8,
                                    1,                              9,
                                    1,                              10,
                                    2,                              9,
                                    2,                              10]
            """
            cmd="""

                drop function if exists z_make_rows_with_numeric_range(int,int,int,boolean) cascade;

                drop type if exists numeric_range_type;

                CREATE TYPE numeric_range_type as (
                    uid int,
                    res_i int
                );

                CREATE OR REPLACE FUNCTION z_make_rows_with_numeric_range(  IN uid integer,
                                                                            IN start_num integer,
                                                                            IN end_num integer,
                                                                            IN w_parity boolean default false)
                RETURNS SETOF numeric_range_type AS $$

                    class numeric_range_type:
                        def __init__(self,uid,res_i):
                            self.uid = uid
                            self.res_i = res_i


                    for j in range(start_num,end_num+1):
                        if w_parity:
                            if ((j % 2==0) == (start_num % 2==0)):
                                yield( numeric_range_type(uid,j) )
                        else:
                            yield( numeric_range_type(uid,j) )

                    return

                $$ LANGUAGE plpythonu;
            """
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return
        def z_make_rows_with_alpha_range(self):
            """
                z_make_rows_with_alpha_range('idx_col','start_range_col','end_range_col')

                z_make_rows_with_alpha_range(uid,base_str,start_r,end_r,first_empty)

                EXAMPLE:
                    select z_make_rows_with_alpha_range(uid,base_str,'A','C',false)

                RETURNS:

                        idx_col =  [1           rows_ranges     =  [A,
                                    1,                              B,
                                    2,                              A,
                                    2,                              B,
                                    2,                              C,
                                    3,                              B,
                                    3,                              C,
                                    3,                              D,
                                    3]                              E]
            """
            cmd="""
                drop function if exists z_make_rows_with_alpha_range(int,text,text,text,boolean) cascade;
                drop type if exists alpha_range_type;
                CREATE TYPE alpha_range_type as (
                    uid int,
                    alpha_range text
                );
                CREATE OR REPLACE FUNCTION z_make_rows_with_alpha_range(uid int,base_str text,start_r text,end_r text,first_empty boolean)
                RETURNS SETOF alpha_range_type AS $$

                    class alpha_range_type:
                        def __init__(self,uid,alpha_range):
                            self.uid = uid
                            self.alpha_range = alpha_range

                    if first_empty:
                        yield ( alpha_range_type(uid,base_str) )


                    for j in range(ord(start_r),ord(end_r)+1):
                        yield ( alpha_range_type(uid,base_str + chr(j) ) )

                $$ LANGUAGE plpythonu;
            """
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return
        def z_update_addr_idx_from_gc_info(self):
            pass

        def z_get_geocode_info(self):
            cmd="""
                DROP TYPE IF EXISTS geocode_results cascade;
                CREATE TYPE geocode_results as (
                    idx integer,
                    addr_valid boolean,
                    partial_match boolean,
                    form_addr text,
                    std_addr text,
                    zipcode bigint,
                    lat double precision,
                    lon double precision

                );

                drop function if exists z_get_geocode_info(text);
                drop function if exists z_get_geocode_info(integer[],text[]);
                CREATE FUNCTION z_get_geocode_info(uids integer [],addr_queries text[])
                RETURNS SETOF geocode_results AS $$

                from os                             import environ as os_environ
                from sys                            import path             as py_path
                py_path.append(                     os_environ['PWD'] +
                                                        '/SERVER2/ipython/ENV/lib/python2.7/site-packages/')
                from pygeocoder                     import Geocoder,GeocoderError
                from traceback                      import format_exc       as tb_format_exc
                from sys                            import exc_info         as sys_exc_info

                class geocode_results:

                    def __init__(self,upd=None):
                        if upd:
                            self.__dict__.update(       upd)


                def get_gc_info(it):

                    try:
                        r                           =   Geocoder.geocode(it)
                        return 'ok',r
                    except GeocoderError as e:
                        return 'failed',[]
                    except:
                        plpy.log(                       tb_format_exc())
                        plpy.log(                       sys_exc_info()[0])
                        plpy.log(                       e)
                        return 'failed',[]

                try:

                    for j in range(len(addr_queries)):
                        idx                         =   uids[j]
                        it                          =   addr_queries[j]
                        status,results              =   get_gc_info(it)
                        _out                        =   None

                        if not results:
                            _out                    =   None

                        elif results.len > 1:

                            found = False
                            for i in range(0,results.len):

                                idx                 =   i
                                res                 =   results[i]

                                if not res.valid_address:
                                    _out            =   None
                                    break


                                else:
                                    r_data          =   res.data[0]
                                    r_data_c        =   r_data['address_components']
                                    component_list  =   map(lambda s: s['types'][0],r_data_c)
                                    found           =   True
                                    t               =   {'idx'                  :   idx,
                                                         'addr_valid'           :   res.valid_address,
                                                         'partial_match'        :   False if not r_data.has_key('partial_match') else True if res.valid_address else r_data['partial_match'],
                                                         'form_addr'            :   res.formatted_address,
                                                         'std_addr'             :   ' '.join([  r_data_c[component_list.index('street_number')]['long_name'],
                                                                                                r_data_c[component_list.index('route')]['long_name'] ]),
                                                         'zipcode'              :   int(r_data_c[component_list.index('postal_code')]['long_name']),
                                                         'lat'                  :   float(res.latitude),
                                                         'lon'                  :   float(res.longitude),
                                                         }

                                    r               =   geocode_results(t)
                                    yield(              r)

                            if not found:
                                _out                =   None



                        else:
                            res                     =   results
                            if not res.valid_address:
                                _out                =   None
                            else:
                                r_data              =   res.data[0]
                                r_data_c            =   r_data['address_components']
                                component_list      =   map(lambda s: s['types'][0],r_data_c)
                                partial_option      =   True if r_data.keys().count('partial_match') != 0 else False
                                t                   =   {'idx'                  :   idx,
                                                         'addr_valid'           :   res.valid_address,
                                                         'partial_match'        :   False if not r_data.has_key('partial_match') else r_data['partial_match'],
                                                         'form_addr'            :   res.formatted_address,
                                                         'std_addr'             :   ' '.join([  r_data_c[component_list.index('street_number')]['long_name'],
                                                                                                r_data_c[component_list.index('route')]['long_name'] ]),
                                                         'zipcode'              :   int(r_data_c[component_list.index('postal_code')]['long_name']),
                                                         'lat'                  :   float(res.latitude),
                                                         'lon'                  :   float(res.longitude),
                                                         }
                                r                   =   geocode_results(t)
                                _out                =   r


                        yield(                          _out)

                except plpy.SPIError, e:
                    plpy.log(                           'GEOCODING FAILED')
                    plpy.log(                           tb_format_exc())
                    plpy.log(                           sys_exc_info()[0])
                    plpy.log(                           e)
                    yield(                              None)



                $$ LANGUAGE plpythonu;
            """
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return


class pgSQL_Triggers:

    def __init__(self,_parent):
        self.T                              =   _parent.T
        self.Create                         =   self.Create(self)
        self.Destroy                        =   self.Destroy(self)
        self.Operate                        =   self.Operate(self)

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
                OR WHEN TAG IN ('CREATE TABLE AS')
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
                    last_table := ( select relname from pg_class
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
                OR WHEN TAG IN ('CREATE TABLE AS')

                EXECUTE PROCEDURE z_auto_add_last_updated_field();
                                            """
            self.T.conn.set_isolation_level(0)
            self.T.cur.execute(c)
        def z_auto_update_timestamp(self,tbl,col):
            a="""
                DROP FUNCTION if exists z_auto_update_timestamp_on_%(tbl)s_in_%(col)s() cascade;
                DROP TRIGGER if exists update_timestamp_on_%(tbl)s_in_%(col)s ON %(tbl)s;

                CREATE OR REPLACE FUNCTION z_auto_update_timestamp_on_%(tbl)s_in_%(col)s()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.last_updated := now();
                    RETURN NEW;
                END;
                $$ language 'plpgsql';

                CREATE TRIGGER update_timestamp_on_%(tbl)s_in_%(col)s
                BEFORE UPDATE OR INSERT ON %(tbl)s
                FOR EACH ROW
                EXECUTE PROCEDURE z_auto_update_timestamp_on_%(tbl)s_in_%(col)s();

            """ % {'tbl':tbl,'col':col}

            self.T.conn.set_isolation_level(       0)
            self.T.cur.execute(                    a)
            return
        def NOT_USING_z_update_with_geom_from_coords(self,tbl,uid_col):
            a="""
                DROP FUNCTION if exists z_update_with_geom_from_coords_on_%(tbl)s() cascade;
                DROP TRIGGER if exists update_with_geom_from_coords_on_%(tbl)s ON %(tbl)s;

                CREATE OR REPLACE FUNCTION z_update_with_geom_from_coords_on_%(tbl)s()
                RETURNS TRIGGER AS $funct$

                from traceback                      import format_exc       as tb_format_exc
                from sys                            import exc_info         as sys_exc_info

                try:
                    if (TD["new"]["trigger_step"] != 'get_geom_from_coords'):
                        return

                    T = TD['new']

                    p = \"\"\"

                        SELECT z_update_with_geom_from_coords(   t.%(uid_col)s,
                                                                '%(tbl)s'::text,
                                                                '%(uid_col)s'::text,
                                                                'latitude'::text,
                                                                'longitude'::text)
                        FROM %(tbl)s t
                        WHERE %(uid_col)s = ##(uid)s

                        \"\"\" ## T

                    plpy.log(p)

                    TD["new"]["trigger_step"] = 'geom_added_via_trigger_get_geom_from_coords'

                    plpy.execute(p)

                except plpy.SPIError:
                    plpy.log('z_update_with_geom_from_coords FAILED')
                    plpy.log("table: " + TD["table_name"] + '; %(uid_col)s:' + str(T["%(uid_col)s"]))
                    plpy.log(tb_format_exc())
                    plpy.log(sys_exc_info()[0])
                    return
                return

                $funct$ language "plpythonu";

                CREATE TRIGGER update_with_geom_from_coords_on_%(tbl)s
                AFTER UPDATE OR INSERT ON %(tbl)s
                FOR EACH ROW
                EXECUTE PROCEDURE z_update_with_geom_from_coords_on_%(tbl)s();

            """ % {"tbl"                        :   tbl,
                   "uid_col"                    :   uid_col}

            cmd                                 =   a.replace("##","%")
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return

        def z_trigger_when_first_parsed(self,tbl,uid_col,addr_col,zip_col):
            cmd="""
                DROP FUNCTION if exists z_trigger_when_first_parsed_on_%(tbl)s_in_%(addr_col)s() cascade;
                DROP TRIGGER if exists trigger_when_first_parsed_on_%(tbl)s_in_%(addr_col)s ON %(tbl)s;

                CREATE OR REPLACE FUNCTION z_trigger_when_first_parsed_on_%(tbl)s_in_%(addr_col)s()
                RETURNS TRIGGER AS $funct$

                from os                             import system           as os_cmd
                from traceback                      import format_exc       as tb_format_exc
                from sys                            import exc_info         as sys_exc_info

                try:
                    T = TD["new"]
                    if (T["%(addr_col)s"] == 'not_provided' or
                        T["%(addr_col)s"] == '' or
                        T["trigger_step"] != 'new_address.1.parsed'):
                        return
                    else:
                        cmd = ''.join([ "curl -X POST ",
                                        "'",
                                        '&'.join([  "http://0.0.0.0:14401?",
                                                    "table=%(tbl)s",
                                                    "trigger=new_address.1.parsed.",
                                                    "uid_col=%(uid_col)s",
                                                    "addr_col=%(addr_col)s",
                                                    "zip_col=%(zip_col)s",
                                                    "idx=##s" ## T['%(uid_col)s'] ]),
                                        "'",
                                        #" > /dev/null 2>&1",
                                        " &",
                                         ])
                        plpy.log(cmd)
                        os_cmd(cmd)
                        plpy.execute("update %(tbl)s set trigger_step = 'new_address.1.parsed.ngx' where %(uid_col)s =##s" ## T['%(uid_col)s'] )
                        return

                except plpy.SPIError:
                    plpy.log('set_trigger_when_new_addr_on_%(tbl)s_in_%(addr_col)s FAILED')
                    plpy.log(tb_format_exc())
                    plpy.log(sys_exc_info()[0])
                    return


                $funct$ language "plpythonu";

                CREATE TRIGGER trigger_when_first_parsed_on_%(tbl)s_in_%(addr_col)s
                AFTER UPDATE OR INSERT ON %(tbl)s
                FOR EACH ROW
                EXECUTE PROCEDURE z_trigger_when_first_parsed_on_%(tbl)s_in_%(addr_col)s();
            """ % { "tbl"                       :   tbl,
                    "uid_col"                   :   uid_col,
                    "addr_col"                  :   addr_col,
                    "zip_col"                   :   zip_col }
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd.replace('##','%'))
            return
        def z_trigger_when_new_addr(self,tbl,uid_col,addr_col,zip_col):
            cmd="""
                DROP FUNCTION if exists z_trigger_when_new_addr_on_%(tbl)s_in_%(addr_col)s() cascade;
                DROP TRIGGER if exists set_trigger_when_new_addr_on_%(tbl)s_in_%(addr_col)s ON %(tbl)s;

                CREATE OR REPLACE FUNCTION z_trigger_when_new_addr_on_%(tbl)s_in_%(addr_col)s()
                RETURNS TRIGGER AS $funct$

                from os                             import system           as os_cmd
                from traceback                      import format_exc       as tb_format_exc
                from sys                            import exc_info         as sys_exc_info

                try:
                    T = TD["new"]
                    if (T["%(addr_col)s"] == 'not_provided' or
                        T["%(addr_col)s"] == '' or
                        T["trigger_step"] != 'new_address.1'):
                        return
                    else:
                        cmd = ''.join([ "curl -X POST ",
                                        "'",
                                        '&'.join([  "http://0.0.0.0:14401?",
                                                    "table=%(tbl)s",
                                                    "trigger=new_address.1",
                                                    "uid_col=%(uid_col)s",
                                                    "addr_col=%(addr_col)s",
                                                    "zip_col=%(zip_col)s",
                                                    "idx=##s" ## T['%(uid_col)s'] ]),
                                        "'",
                                        #" > /dev/null 2>&1",
                                        " &",
                                         ])
                        plpy.log(cmd)
                        os_cmd(cmd)
                        plpy.execute("update %(tbl)s set trigger_step = 'new_address.1.ngx' where %(uid_col)s =##s" ## T['%(uid_col)s'] )
                        return

                except plpy.SPIError:
                    plpy.log('set_trigger_when_new_addr_on_%(tbl)s_in_%(addr_col)s FAILED')
                    plpy.log(tb_format_exc())
                    plpy.log(sys_exc_info()[0])
                    return


                $funct$ language "plpythonu";

                CREATE TRIGGER trigger_when_new_addr_on_%(tbl)s_in_%(addr_col)s
                AFTER UPDATE OR INSERT ON %(tbl)s
                FOR EACH ROW
                EXECUTE PROCEDURE z_trigger_when_new_addr_on_%(tbl)s_in_%(addr_col)s();
            """ % { "tbl"                       :   tbl,
                    "uid_col"                   :   uid_col,
                    "addr_col"                  :   addr_col,
                    "zip_col"                   :   zip_col}
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd.replace('##','%'))
            return

        def z_yelp_set_trigger_on_addr_not_provided(self):
            cmd="""
                DROP FUNCTION if exists z_yelp_set_trigger_on_addr_not_provided() cascade;
                DROP TRIGGER if exists yelp_set_trigger_on_addr_not_provided ON yelp;

                CREATE OR REPLACE FUNCTION z_yelp_set_trigger_on_addr_not_provided()
                RETURNS TRIGGER AS $funct$

                from os                             import system           as os_cmd
                from traceback                      import format_exc       as tb_format_exc
                from sys                            import exc_info         as sys_exc_info

                try:
                    if (TD["new"]["address"] == TD["old"]["address"] or
                        TD["new"]["address"] != 'not_provided'):
                        return
                    else:
                        cmd = ''.join([ "curl 'http://0.0.0.0:14401?table=yelp&trigger=get_geom_from_coords&",
                                        "idx_col=uid&idx=%s'" % TD['new']['uid'],
                                        ])
                        plpy.log(cmd)
                        os_cmd(cmd)
                        return

                except plpy.SPIError:
                    plpy.log('z_yelp_set_trigger_on_addr_not_provided FAILED')
                    plpy.log(tb_format_exc())
                    plpy.log(sys_exc_info()[0])
                    return


                $funct$ language "plpythonu";

                CREATE TRIGGER yelp_set_trigger_on_addr_not_provided
                AFTER UPDATE OR INSERT ON yelp
                FOR EACH ROW
                EXECUTE PROCEDURE z_yelp_set_trigger_on_addr_not_provided();
            """
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            return
        def z_parse_address_on_gid_addr_zip(self,tbl,
                                        gid_col='gid',
                                        addr_col='address',
                                        zip_col='zipcode',
                                        verbose=False):
            """
            alter table tmp_5e244d5
                add column bldg text,
                add column box text,
                add column unit text,
                add column num text,
                add column predir text,
                add column street_name text,
                add column suftype text,
                add column sufdir text,
                add column bldg_street_idx text,
                add column sm integer DEFAULT 0,
                add column ls integer DEFAULT 0,
                add column gc_lat double precision,
                add column gc_lon double precision,
                add column gc_addr text,
                add column ai integer DEFAULT 0,
                add column pa text;
            """
            a="""
                DROP FUNCTION if exists z_parse_address_on_gid_addr_zip_on_%(tbl)s_in_%(addr_col)s() cascade;
                DROP TRIGGER if exists parse_address_on_gid_addr_zip_on_%(tbl)s_in_%(addr_col)s ON %(tbl)s;

                CREATE OR REPLACE FUNCTION z_parse_address_on_gid_addr_zip_on_%(tbl)s_in_%(addr_col)s()
                RETURNS TRIGGER AS $funct$

                #from traceback                      import format_exc       as tb_format_exc
                #from sys                            import exc_info         as sys_exc_info
                #import                                  inspect             as I

                #try:

                def adjust_single_quote(text_var,repl_var):
                    if text_var.count("'")>0:
                        text_var = ''.join(["concat('",
                                                     "',$single_quote$'$single_quote$,'".join(text_var.split("'")),
                                                     "')"])
                        text_var = text_var.replace("'","''")

                    return text_var


                p = \"\"\"  SELECT  z_update_with_parsed_info(  array_agg(t.%(gid_col)s),
                                                                '%(tbl)s',
                                                                '%(gid_col)s','%(addr_col)s',
                                                                '%(zip_col)s',
                                                                array['num','predir','street_name','suftype','sufdir'])
                            FROM    %(tbl)s t
                            WHERE   t.%(addr_col)s is not null
                            AND     t.%(zip_col)s is not null
                            AND     t.bbl is null
                            AND     t.geom is null
                    \"\"\"

                plpy.execute(p)

                return 'ok'

                $funct$ language "plpythonu";

                CREATE TRIGGER parse_address_on_gid_addr_zip_on_%(tbl)s_in_%(addr_col)s
                AFTER UPDATE OR INSERT ON %(tbl)s
                EXECUTE PROCEDURE z_parse_address_on_gid_addr_zip_on_%(tbl)s_in_%(addr_col)s();

            """ % {"tbl"                        :   tbl,
                   "addr_col"                   :   addr_col,
                   "gid_col"                    :   gid_col,
                   "zip_col"                    :   zip_col}

            cmd                                 =   a.replace("##","%")
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            if verbose:                             print cmd
            return
        def z_match_simple(self,tbl,uid_col):
            a="""
                DROP FUNCTION if exists z_match_simple_on_%(tbl)s() cascade;
                DROP TRIGGER if exists match_simple_on_%(tbl)s ON %(tbl)s;

                CREATE OR REPLACE FUNCTION z_match_simple_on_%(tbl)s()
                RETURNS TRIGGER AS $funct$

                #from traceback                      import format_exc       as tb_format_exc
                #from sys                            import exc_info         as sys_exc_info

                try:
                    if (TD["new"]["street_name"] == TD["old"]["street_name"] or
                        TD["new"]["sm"] == 1):
                        return

                    T = TD['new']

                    if not T["street_name"]:
                        T['sm'] = 99
                        return "MODIFY"

                    if not T["predir"]:
                        T["predir"] = ""

                    if not T["suftype"]:
                        T["suftype"] = ""

                    p = \"\"\"
                        SELECT t.%(uid_col)s,a.bldg_street_idx
                        FROM
                            %(tbl)s t,
                            (SELECT regexp_replace(concat(  predir,
                                                            street_name,
                                                            suftype,
                                                            sufdir),'\\s','','g') addr,
                                    bldg_street_idx
                                FROM addr_idx WHERE street_name IS NOT NULL) a
                        WHERE a.bldg_street_idx IS NOT NULL
                        AND a.addr ilike regexp_replace(concat( '##(predir)s',
                                                                '##(street_name)s',
                                                                '##(suftype)s',
                                                                '##(sufdir)s'),'\\s','','g')
                        AND t.%(uid_col)s = ##(%(uid_col)s)s
                        \"\"\" ## T

                    res = plpy.execute(p)
                    if not res:
                        TD['new']['sm'] = 99
                    else:
                        TD['new']['sm'] = 1
                        TD['new']['bldg_street_idx'] = res[0]['bldg_street_idx']
                    return "MODIFY"

                except plpy.SPIError:
                    plpy.log('SIMPLE MATCH TRIGGER FAILED')
                    plpy.log("table: " + TD["table_name"] + '; %(uid_col)s:' + str(T["%(uid_col)s"]))
                    #plpy.log(tb_format_exc())
                    #plpy.log(sys_exc_info()[0])
                    return
                return

                $funct$ language "plpythonu";

                CREATE TRIGGER match_simple_on_%(tbl)s
                BEFORE UPDATE OR INSERT ON %(tbl)s
                FOR EACH ROW
                EXECUTE PROCEDURE z_match_simple_on_%(tbl)s();

            """ % {"tbl"                        :   tbl,
                   "uid_col"                    :   uid_col}

            cmd                                 =   a.replace("##","%")
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            print cmd
            return
        def z_add_geom_through_addr_idx(self,tbl,uid_col):
            a="""
                DROP FUNCTION if exists z_add_geom_through_addr_idx_on_%(tbl)s() cascade;
                DROP TRIGGER if exists add_geom_through_addr_idx_on_%(tbl)s ON %(tbl)s;

                CREATE OR REPLACE FUNCTION z_add_geom_through_addr_idx_on_%(tbl)s()
                RETURNS TRIGGER AS $funct$

                from traceback                      import format_exc       as tb_format_exc
                from sys                            import exc_info         as sys_exc_info

                try:
                    if (TD["new"]["bldg_street_idx"] == TD["old"]["bldg_street_idx"]):
                        return

                    p = "select z_add_geom_through_addr_idx('%(tbl)s','%(uid_col)s');"

                    plpy.execute(p)

                except plpy.SPIError:
                    plpy.log('add_geom_through_addr_idx_on_%(tbl)s TRIGGER FAILED')
                    plpy.log(tb_format_exc())
                    plpy.log(sys_exc_info()[0])
                    return
                return

                $funct$ language "plpythonu";

                CREATE TRIGGER add_geom_through_addr_idx_on_%(tbl)s
                AFTER UPDATE OR INSERT ON %(tbl)s
                FOR EACH ROW
                EXECUTE PROCEDURE z_add_geom_through_addr_idx_on_%(tbl)s();

            """ % {"tbl"                        :   tbl,
                   'uid_col'                    :   uid_col}

            cmd                                 =   a.replace("##","%")
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            print cmd
            return

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

    class Operate:
        def __init__(self,_parent):
            self.T                              =   _parent.T
            self.Operate                        =   self
        def disable(self,tbl,trigger_name):
            cmd = "ALTER TABLE %(tbl)s DISABLE TRIGGER %(trig)s;" % {'tbl':tbl,'trig':trigger_name}
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
        def enable(self,tbl,trigger_name):
            cmd = "ALTER TABLE %(tbl)s ENABLE TRIGGER %(trig)s;" % {'tbl':tbl,'trig':trigger_name}
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)

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
                                                    where address is not null and geom is null
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


            # push data to table 'tmp'
            z                               =   self.T.pd.merge(df,recognized.ix[:, ['addr_set','bldg_street_idx']], on='addr_set',how='outer')
            z                               =   z.drop(['addr_set'],axis=1)
            self.T.conn.set_isolation_level(    0)
            self.T.cur.execute(                 'drop table if exists %(tmp_tbl)s' % self.T)
            z.to_sql(                           self.T.tmp_tbl,self.T.eng,index=False)

            # update table $working_table and delete table 'tmp'
            self.T.conn.set_isolation_level(0)
            self.T.cur.execute("""

                alter table %(tmp_tbl)s
                    add column camis integer,
                    add column bbl integer,
                    add column lot_cnt integer DEFAULT 1,
                    add column geom geometry(Point,4326);


                select z_add_geom_through_addr_idx('%(tmp_tbl)s','%(id_col)s');


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
            from time                           import sleep            as delay
            from pygeocoder                     import Geocoder



            df,T                            =   self.prep_vendor_data_for_adding_geom(
                                                    data_type   =   'db',
                                                    data_set    =   working_tbl,
                                                    purpose     =   'google_geocode')
            self.T.__init__(                    T)
            addr_start_cnt                  =   len(df)

            from ipdb import set_trace as i_trace; i_trace()

            df['zipcode']                   =   df.zipcode.map(lambda s: '' if str(s).lower()=='nan' else str(int(s)))
            df['chk_addr']                  =   df.ix[:,['address','zipcode']].apply(lambda s:
                                                        unicode(s[0]+', New York, NY, '+str(s[1])).strip(),axis=1)
            uniq_addr_start_cnt             =   len(df.chk_addr.unique().tolist())

            # get google geocode results
            all_chk_addr                    =   df.chk_addr.tolist()
            uniq_addr                       =   self.T.pd.DataFrame({'addr':all_chk_addr}).addr.unique().tolist()
            uniq_addr_dict                  =   dict(zip(uniq_addr,range(len(uniq_addr))))
            _iter                           =   self.T.pd.Series(uniq_addr).iterkv()

            # if two vendors have same address: only one id will be associated with address

            y,z                             =   [],[]
            pt,s                            =   0,'Address\tZip\tLat.\tLong.\r'
            #    print '\n"--" means only one result found.\nOtherwise, numbered results will be shown.'
            if print_gps==True: print s
            for k,it in _iter:
                try:
                    results                 =   Geocoder.geocode(it)

                    if results.count > 1:
                        for i in range(0,results.count):

                            res             =   results[i]
                            r_data          =   res.data[0]
                            t               =   {'res_i'                :   i,
                                                 'orig_addr'            :   it.rstrip(),
                                                 'addr_valid'           :   res.valid_address,
                                                 'partial_match'        :   r_data['partial_match']
                                                                                if res.valid_address != True else False,
                                                 'form_addr'            :   res.formatted_address,
                                                 'geometry'             :   r_data['geometry'],
                                                 'res_data'             :   str(r_data),
                                                 }

                            y.append(           t)
                            z.append(           k)
                            a               =   '\t'.join([str(i),str(it.rstrip()),str(res.postal_code),
                                                           str(res.coordinates[0]),str(res.coordinates[1])])
                            s              +=   a+'\r'
                            if print_gps==True: print a

                    else:

                        res                 =   results
                        r_data              =   res.data[0]
                        partial_option      =   True if r_data.keys().count('partial_match') != 0 else False
                        t                   =   {'res_i'                :   -1,
                                                 'orig_addr'            :   it.rstrip(),
                                                 'addr_valid'           :   res.valid_address,
                                                 'partial_match'        :   r_data['partial_match'] if partial_option else False,
                                                 'form_addr'            :   res.formatted_address,
                                                 'geometry'             :   r_data['geometry'],
                                                 'res_data'             :   str(r_data),
                                                 }

                        y.append(               t)
                        z.append(               k)
                        a                   =   '--'+'\t'.join([str(it.rstrip()),str(results.postal_code),
                                                                str(results.coordinates[0]),
                                                                str(results.coordinates[1])])
                        s                  +=   a+'\r'
                        if print_gps==True: print a

                except:
                    pass

                pt+=1
                if pt==5:
                    delay(                      2.6)
                    pt                      =   0

            d                               =   self.T.pd.DataFrame(y)
            d['iter_keys']                  =   z
            d['lat'],d['lon']               =   zip(*d.geometry.map(lambda s: (s['location']['lat'],s['location']['lng'])))
            tbl_dict                        =   dict(zip(df.chk_addr.tolist(),df.id.tolist()))
            d['%(db_tbl)s_id' % self.T]     =   d.orig_addr.map(tbl_dict)

            # push orig_df to pgSQL
            d['geometry']                   =   d.geometry.map(str)
            d['res_data']                   =   d.res_data.map(str)
            self.T.conn.set_isolation_level(    0)
            self.T.cur.execute(                 "drop table if exists %(tmp_tbl)s;" % self.T)
            d.to_sql(                           self.T.tmp_tbl,self.T.eng,index=False)
            self.T.conn.set_isolation_level(    0)

            from ipdb import set_trace as i_trace; i_trace()

            # update 'geocoded' and $tbl
            cmd                             =   """
                                                    alter table %(tmp_tbl)s
                                                        add column to_parse_addr text,
                                                        add column zipcode bigint;

                                                    -- PULL OUT ONLY VALID, NEW YORK ADDRESSES
                                                    update %(tmp_tbl)s t set
                                                        to_parse_addr = regexp_replace( n.address,
                                                                                        '(.*,\\s)([a-zA-Z0-9\\s]*)$',
                                                                                        '\\2'),
                                                        zipcode=n.zipcode::bigint
                                                    from
                                                        (
                                                        select
                                                            t2.uid gid,
                                                            regexp_replace(t2.form_addr,'(.*)(, New York, NY)(.*)',
                                                                            '\\1') address,
                                                            regexp_replace(t2.form_addr,'(.*)([0-9]{5})(.*)',
                                                                            '\\2') zipcode
                                                        from %(tmp_tbl)s t2
                                                        where t2.addr_valid is true
                                                        ) as n
                                                    where length(n.zipcode::text)=5
                                                    and position(n.zipcode in n.address)=0
                                                    and n.gid = t.uid;


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
                                                                from %(tmp_tbl)s t
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
                                                        %(tmp_tbl)s t,
                                                        (select array_agg(f.orig_addr) upd_addrs from upd f) as f1
                                                        where (not upd_addrs && array[t.orig_addr]
                                                                or upd_addrs is null);

                                                    UPDATE %(db_tbl)s t set
                                                            geom = st_setsrid(st_makepoint(g.lon,g.lat),4326)
                                                        FROM geocoded g
                                                        WHERE g.addr_valid is true
                                                        and g.%(db_tbl)s_id = t.%(id_col)s
                                                        and t.geom is null;

                                                """ % self.T
            self.T.conn.set_isolation_level(    0)
            self.T.cur.execute(                 cmd)

            # provide result info
            uniq_search_queries             =   len(d['%(db_tbl)s_id' % self.T].unique().tolist())
            search_query_res_cnt            =   len(d)
            single_res_cnt                  =   len(d[d.res_i==-1])
            remaining_no_addr               =   self.T.pd.read_sql("""  select count(*) c from %(db_tbl)s
                                                                        where geom is null"""%self.T,self.T.eng).c[0]

            print '\tTABLE:',self.T.db_tbl
            print addr_start_cnt,'\t total addresses in %(db_tbl)s without geom' % self.T
            print uniq_addr_start_cnt,'\t unique addresses '
            print uniq_search_queries,'\t # of unique Search Queries'
            print search_query_res_cnt,'\t # of Search Query Results'
            print single_res_cnt,'\t # of Query Results with a Single Result'
            print remaining_no_addr,'\t # of Vendors in %(db_tbl)s still without geom' % self.T
            return

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
                        '([^|]*)%|(AVE?N?U?E?)[%s]+([A-F])[%s]?(.*)',
                        '%1|%3 %2 %4','','0'),

                    -- AVENUE OF THE AMERICAS
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(AVE?N?U?E?[%s]+O?F?)[%s]+[THE]*[%s]*(AMERI?C?A?S?[%s]*)(.*)',
                        '%1|6 AVENUE %4','','0'),

                    -- Qx5 = repl. w/ no space, Qx4 = repl. w/ space

                    -- AVENUE OF THE FINEST
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(AVE[NUE]*[%s]+OF[%s]+)[THE]*[%s]*(FINEST?)[%s]*(.*)',
                        '%1|AVENUEQQQQOFQQQQTHEQQQQFINEST %4','','0'),


                    -- 3 AVENUE --> 0 3 AVENUE  (b/c street num required for parsing)
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(AVE?N?U?E?)[%s]?([a-zA-Z]*)$',
                        '0|%1 %2 %3','','1'),

                    -- special streets where 'EAST' and 'WEST' don't refer to an end of a street
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(WE?S?T?)%s(END)%s(AV)(.*)$',
                        '%1|%2QQQQ%3 %4%5','','1'),
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(EA?S?T?)%s(RIVER)%s(DR)(.*)$',
                        '%1|%2QQQQ%3 %4%5','','1'),

                    -- "ADAM CLAYTON POWELL JR BOULEVARD"
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(AD?A?M?[%s]*C?L?A?Y?T?O?N?[%s]+PO?W?E?L?L?[%s]*J?R?)[%s]+(BO?U?L?E?V?A?R?D?)(.*)$',
                        '%1|7 AVENUE %4','','1'),

                    -- "DR M L KING JR BOULEVARD"
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(DR[%s]+MA?R?T?I?N?[%s]+LU?T?H?E?R?[%s]+KI?N?G?[%s]*J?R?)[%s]+(BO?U?L?E?V?A?R?D?)(.*)$',
                        '%1|DRQQQQMQQQQLQQQQKQQQQJR BOULEVARD %4','','1'),


                    -- b/c PIKE in 'PIKE SLIP' does not refer to a highway
                    ('custom_addr_pre_filter',
                        '([0-9]+)%|(PI)(KE)[%s]+(SLIP)(.*)$',
                        '%1|%2QQQQQ%3 %4%5','','1'),

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

        class NYC:

            def __init__(self,_parent):
                self.T                          =   _parent.T

            def snd(self,table_name='snd',drop_prev=True):
                from f_nyc_data import load_parsed_snd_datafile_into_db
                load_parsed_snd_datafile_into_db(table_name,drop_prev)
                a="""

                delete from snd where primary_name = variation;

                alter table snd
                    add column from_num integer,
                    add column from_predir text,
                    add column from_street_name text,
                    add column from_suftype text,
                    add column from_sufdir text,
                    add column to_num integer,
                    add column to_predir text,
                    add column to_street_name text,
                    add column to_suftype text,
                    add column to_sufdir text;



                delete from snd
                where variation ilike any (array[ '%%NORTHBOUND%%','%%NB%%','%%SOUTHBOUND%%','%%SB%%',
                                                '%%ENTRANCE%%','%% BRDG%%','%% EXIT%%','%% TRAIN%%','RT %%','%% RT%%',
                                                'RTE %%','%% RTE%%','%% US %%','US %%','%% RTE%%','%%INTERSTATE %%',
                                                '%%I-95%%','%%I %% 95%%','%% COMPLEX%%','%% PROJECTS%%','ROUTE %%',
                                                '%%PATH %%','%%PATH-%%','%% HOUSES%%','%% EXTENSION%%']);

                WITH upd AS (
                    SELECT  src_gid,predir,name street_name,suftype,sufdir
                    FROM    z_parse_NY_addrs('
                                            select
                                                uid::bigint gid,
                                                variation::text address,
                                                ''11111''::bigint zipcode
                                            FROM snd
                                            ')
                      )
                UPDATE snd t set
                    from_predir = u.predir,
                    from_street_name = u.street_name,
                    from_suftype = u.suftype,
                    from_sufdir = u.sufdir
                FROM  upd u
                WHERE u.src_gid = t.uid::bigint;


                delete from snd
                where primary_name ilike any (array[ '%%NORTHBOUND%%','%%NB%%','%%SOUTHBOUND%%','%%SB%%',
                                                '%%ENTRANCE%%','%% BRDG%%','%% EXIT%%','%% TRAIN%%','RT %%','%% RT%%',
                                                'RTE %%','%% RTE%%','%% US %%','US %%','%% RTE%%','%%INTERSTATE %%',
                                                '%%I-95%%','%%I %% 95%%','%% COMPLEX%%','%% PROJECTS%%','ROUTE %%',
                                                '%%PATH %%','%%PATH-%%','%% HOUSES%%','%% RECREATION CTR%%',
                                                '%% EXTENSION%%']);

                WITH upd AS (
                    SELECT  src_gid,predir,name street_name,suftype,sufdir
                    FROM    z_parse_NY_addrs('
                                            select
                                                uid::bigint gid,
                                                primary_name::text address,
                                                ''11111''::bigint zipcode
                                            FROM snd
                                            ')
                      )
                UPDATE snd t set
                    to_predir = u.predir,
                    to_street_name = u.street_name,
                    to_suftype = u.suftype,
                    to_sufdir = u.sufdir
                FROM  upd u
                WHERE u.src_gid = t.uid::bigint


                INSERT INTO snd (from_num,from_predir,from_street_name,from_suftype,from_sufdir,
                                to_num,to_predir,to_street_name,to_suftype,to_sufdir)
                VALUES (0,null,'ROCKEFELLER','CTR',null,
                        45,null,'ROCKEFELLER','PLZ',null);

                INSERT INTO snd (from_predir,from_street_name,from_suftype,from_sufdir,
                                to_predir,to_street_name,to_suftype,to_sufdir)
                VALUES (null,'ROCKEFELLER','CTR',null,
                        null,'ROCKEFELLER','PLZ',null);

                INSERT INTO snd (from_predir,from_street_name,from_suftype,from_sufdir,
                                to_predir,to_street_name,to_suftype,to_sufdir)
                VALUES ('W','59','ST',null,
                        null,'CENTRAL','PARK','S');


                """

            def pad(self):
                # CREATE/ADJUST PAD TABLES

                # CLEAN UP TABLE SPACE
                a="""
                drop table if exists pad_adr;
                drop table if exists pad_bbl;
                drop table if exists tmp_addr_idx_pad;
                drop table if exists addr_idx_wl;
                """
                SV.T.conn.set_isolation_level(        0)
                SV.T.cur.execute(                     a)

                # CREATE PAD_BBL
                df2 = SV.T.pd.read_csv(os_path.join(dl_dir,'bobabbl.txt'))
                t=df2.columns.tolist()
                new_cols = [it.replace('"','') for it in t]
                df2.columns = new_cols
                df2[df2.boro==1].to_sql('pad_bbl',SV.T.eng,index=False)
                a="""

                alter table pad_bbl add column lobbl numeric,add column hibbl numeric,add column billbbl numeric;

                update pad_bbl set
                billboro=trim(both ' ' from billboro),
                billblock=trim(both ' ' from billblock),
                billlot=trim(both ' ' from billlot);

                update pad_bbl set billboro=null where billboro='';
                update pad_bbl set billblock=null where billblock='';
                update pad_bbl set billlot=null where billlot='';

                update pad_bbl set
                lobbl =
                regexp_replace( to_char(loboro::integer,'0')||
                                to_char(loblock::integer,'00000')||
                                to_char(lolot::integer,'0000'),'[[:space:]]','','g')::numeric,
                hibbl =
                regexp_replace( to_char(hiboro::integer,'0')||
                                to_char(hiblock::integer,'00000')||
                                to_char(hilot::integer,'0000'),'[[:space:]]','','g')::numeric;


                update pad_bbl set
                billbbl =
                regexp_replace(to_char(billboro::integer,'0')||to_char(billblock::integer,'00000')||to_char(billlot::integer,'0000'),'[[:space:]]','','g')::numeric
                where billboro is not null and billblock is not null and billlot is not null;

                """
                SV.T.conn.set_isolation_level(        0)
                SV.T.cur.execute(                     a)

                # CREATE PAD_ADR AND START CLEAN (I.E., ENSURE ALL ADDRESSES HAVE ZIPCODE)
                df = SV.T.pd.read_csv(os_path.join(dl_dir,'bobaadr.txt'))
                df[df.boro==1].to_sql('pad_adr',SV.T.eng,index=False)
                a="""
                    alter table pad_adr
                        add column bbl numeric,
                        add column billbbl numeric,
                        add column stnum_w_letter boolean default false,
                        add column street_name text;

                    update pad_adr set bbl =
                    regexp_replace(to_char(boro,'0')||to_char(block,'00000')||to_char(lot,'0000'),'[[:space:]]','','g')::numeric,
                    lhnd=trim(both ' ' from lhnd),
                    hhnd=trim(both ' ' from hhnd),
                    stname=trim(both ' ' from stname);

                    delete from pad_adr where lhnd = '' and hhnd = '';
                    delete from pad_adr where lhnd ilike '% AIR%';
                    update pad_adr set stname = regexp_replace(stname,'[[:space:]]{2,}',' ','g');
                    update pad_adr set zipcode = regexp_replace(zipcode,'[[:space:]]{2,}',' ','g');
                    update pad_adr set zipcode = null where zipcode = ' ';

                    update pad_adr p1 set zipcode = f2.zipcode
                    from
                        (select distinct on (p2.bbl) p2.bbl,p2.zipcode from
                            pad_adr p2,
                            (select distinct on (bbl) bbl from pad_adr where zipcode is null) f1
                        where p2.bbl = f1.bbl
                        and p2.zipcode is not null ) f2
                    where p1.zipcode is null
                    and p1.bbl = f2.bbl;

                    update pad_adr p1 set zipcode = f2.zipcode from
                    --select * from pad_adr p1,
                        (select distinct on (p2.bbl) p2.bbl,p2.zipcode from
                            pluto p2,
                            (select distinct on (bbl) bbl from pad_adr where zipcode is null) f1
                        where p2.bbl = f1.bbl
                        and p2.zipcode is not null ) f2
                    where p1.zipcode is null
                    and p1.bbl = f2.bbl;
                    """
                SV.T.conn.set_isolation_level(        0)
                SV.T.cur.execute(                     a)
                assert SV.T.pd.read_sql(""" select count(*)=0 only_known_addr_remaining from pad_adr
                                            where zipcode is null
                                            and not lhnd ilike '## AIR##'
                                            and not bbl = '1002230997' -- 2400 READE STREET
                                         """.replace('##','%%'),SV.T.eng).only_known_addr_remaining[0] == True

                # SEPARATE ADDRESSES WHERE STREET NUMBER HAS LETTERS
                a="""

                    delete from pad_adr where zipcode is null
                    and ( lhnd ilike '## AIR##' );

                    update pad_adr p set stnum_w_letter = true
                    from
                        (select distinct on (lhnd) lhnd,regexp_replace(lhnd,'[0-9]*','','g') repls
                        from pad_adr) f
                    where f.repls != '' and f.lhnd = p.lhnd;

                    update pad_adr p set stnum_w_letter = true
                    from
                        (select distinct on (hhnd) hhnd,regexp_replace(hhnd,'[0-9]*','','g') repls
                        from pad_adr) f
                    where f.repls != '' and f.hhnd = p.hhnd;

                    """.replace('##','%%')
                SV.T.conn.set_isolation_level(        0)
                SV.T.cur.execute(                     a)

                ## PROVE THAT ONLY ADDR REMAINING IN pad_adr ARE VALID TYPES
                assert SV.T.pd.read_sql(""" select count(*)=0 has_only_valid_addr from pad_adr
                                            where addrtype = any (array['B','G','N','X','U'])
                                            or lhnd = ''
                                            or hhnd = ''
                                            or stname is null or stname = ' ' or stname = ''
                                            """,SV.T.eng).has_only_valid_addr[0] == True

                ## PROVE THAT ALL pluto_bbl EXIST IN pad_bbl_billbbl
                assert SV.T.pd.read_sql(""" select count(*)=0 no_pluto_bbl_not_in_pad_bbl_billbbl
                                            from pluto p,
                                            (select array_agg(billbbl) all_pad_billbbl from pad_bbl) f
                                            where not p.bbl = any(all_pad_billbbl)
                                 """,SV.T.eng).no_pluto_bbl_not_in_pad_bbl_billbbl[0] == True

                ## PROVE THAT ALL pad_bbl_billbbl EXIST IN pluto_bbl
                assert SV.T.pd.read_sql(""" select count(*)=0 no_pad_bbl_billbbl_not_in_pluto_bbl
                                            from pad_bbl p,
                                            (select array_agg(bbl) all_pluto_bbl from pluto) f
                                            where not p.billbbl = any(all_pluto_bbl)
                                 """,SV.T.eng).no_pad_bbl_billbbl_not_in_pluto_bbl[0] == True

                ## CLEAN UP PLUTO BBL JUST TO BE SAFE
                reset_pluto_bbl="""
                    update pluto set bbl =
                    regexp_replace( '1'||
                                    to_char(block::integer,'00000')||
                                    to_char(lot::integer,'0000'),'[[:space:]]','','g')::numeric(10)
                    """
                SV.T.conn.set_isolation_level(        0)
                SV.T.cur.execute(                     reset_pluto_bbl)

                # cross_copy_bbl_if_existing_in_pluto

                prepare_to_cross_copy="""

                    update pad_adr set billbbl = null;

                    update pad_adr a set billbbl = a.bbl
                    from (select array_agg(distinct bbl) all_pluto_bbl from pluto where bbl is not null) f
                    where a.billbbl is null and array[a.bbl] && all_pluto_bbl; --59187 rows affected

                    delete from pad_adr p
                    using (select array_agg(block) pluto_blocks from pluto) f1
                    where p.billbbl is null
                    and not p.block = any(pluto_blocks); --577 rows affected, 571 ms execution time.


                    alter table  pad_adr add column tmp boolean default false;
                    update pad_adr set tmp = true where billbbl is null;
                """
                SV.T.conn.set_isolation_level(        0)
                SV.T.cur.execute(                     prepare_to_cross_copy)

                # CROSS MATCH BBL (I.E., WHERE BBL ON ONE ADDRESS HOSTS ADDRESS FOR OTHER SURROUNDING STREETS)
                cross_match_bbls="""
                    update pad_adr p set billbbl = (select billbbl from pad_bbl where lobbl=_bbl or hibbl=_bbl)
                    from
                        (select uid,bbl from pad_adr where billbbl is null) a,
                        (select array_agg(lobbl) all_lo,array_agg(hibbl) all_hi,array_agg(billbbl) all_bill from pad_bbl) b,
                        (
                        select distinct _bbl
                        from
                            (
                            select unnest(array_cat(array_agg(distinct lobbl),
                                                    array_cat(array_agg(distinct hibbl),
                                                    array_agg(distinct billbbl)))) _bbl
                            from
                                (
                                select lobbl,hibbl,billbbl
                                from pad_bbl,
                                (select array_agg(fa1.bbl) null_bbls
                                    from (select bbl from pad_adr
                                            where billbbl is null
                                            order by uid limit 10) fa1) f1
                                where
                                (array[lobbl] && null_bbls
                                or array[hibbl] && null_bbls
                                or array[billbbl] && null_bbls)
                                ) f2
                            ) f3
                        where _bbl is not null
                        ) f5
                    where a.bbl = _bbl
                    and (array[_bbl] && all_lo
                    or array[_bbl] && all_hi
                    or array[_bbl] && all_bill )
                    and p.uid = a.uid;
                    """
                cnt="select count(*) cnt from pad_adr where billbbl is null;"
                pts_left = SV.T.pd.read_sql(cnt,SV.T.eng).cnt[0]
                pt = 0
                while pts_left>0:
                    pts_left_a = SV.T.pd.read_sql(cnt,SV.T.eng).cnt[0]
                    SV.T.conn.set_isolation_level(        0)
                    SV.T.cur.execute(                     cross_match_bbls)
                    pt+=10
                    print pt
                    pts_left_b = SV.T.pd.read_sql(cnt,SV.T.eng).cnt[0]
                    if pts_left_b==0 or pts_left_a==pts_left_b:
                        break

                cross_match_bbls_2="""
                update pad_adr p set billbbl = _bbl
                from
                    (select array_agg(bbl) pluto_bbls from pluto where bbl is not null) f0,
                    (
                    select f1.uid uid,f1.tmp tmp,unnest(  array_cat(array_agg(distinct lobbl),
                                        array_cat(array_agg(distinct hibbl),
                                        array_agg(distinct billbbl)))) _bbl
                    from
                        pad_bbl,
                            (
                            select uid,bbl tmp,array_agg(bbl) null_bbls
                            from (select distinct bbl,uid from pad_adr where billbbl is null order by uid offset %d limit 10) af1
                            group by uid,tmp
                            ) f1
                        where
                        (array[lobbl] && null_bbls
                        or array[hibbl] && null_bbls
                        or array[billbbl] && null_bbls)
                    group by f1.uid,f1.tmp
                    ) f2
                where _bbl!=f2.tmp and _bbl is not null
                and array[_bbl] && pluto_bbls
                and p.uid = f2.uid
                returning f2.uid uid
                """

                cnt="select count(distinct bbl) cnt from pad_adr where billbbl is null;"
                pts_left = SV.T.pd.read_sql(cnt,SV.T.eng).cnt[0]
                pt,_offset = 0,0
                while pts_left>0:
                    pts_left_a = SV.T.pd.read_sql(cnt,SV.T.eng).cnt[0]
                    res = SV.T.pd.read_sql(  cross_match_bbls_2 % _offset  ,SV.T.eng)
                    updates = len(res)
                    if updates==0:
                        _offset += 10
                        if _offset>=pts_left_a:
                            break
                    elif updates<10:
                        _offset += 10-updates
                    print updates
                    pts_left_b = SV.T.pd.read_sql(cnt,SV.T.eng).cnt[0]


                a="""   select * from pad_adr p, (select array_agg(distinct block) bbl_blocks
                        from pad_adr where billbbl is null) f1
                        where array[p.block] && bbl_blocks"""
                df = SV.T.pd.read_sql(a,SV.T.eng)
                df['billbbl'] = df.billbbl.fillna(value=0).astype(int)
                g = df.groupby('block')

                def update_resp_dict(locs,src):
                    D={}
                    _billbbl = 0
                    for it in locs:
                        _uid = src.ix[it,'uid']
                        if it==0:
                            n = range(1,len(src))
                        elif it==src.index.tolist()[-1:]:
                            n = range(len(src)-1)
                            n.reverse()
                        else:
                            n=range(it,len(src)-1)
                        for i in n:
                            if src.ix[i,'billbbl']:
                                _billbbl = src.ix[i,'billbbl']
                                break
                        D.update({ _uid : _billbbl })
                    return D

                D={}
                t=list(g.groups.iteritems())
                for k,v in g.groups.iteritems():
                    grp = g.get_group(k).sort('min_num')
                    odds = grp[grp.parity=='1'].copy().reset_index(drop=True)
                    evens = grp[grp.parity=='2'].copy().reset_index(drop=True)
                    assert len(odds)+len(evens)==len(grp)

                    odd_blanks,even_blanks = list(odds.billbbl==0),list(evens.billbbl==0)

                    pt,i_odd,odd_idx = 0,[],odds.index.tolist()
                    for j in range(odd_blanks.count(True)):
                        pt = odd_blanks.index(True,pt)
                        i_odd.append( pt )
                        pt += 1

                    pt,i_even,even_idx = 0,[],evens.index.tolist()
                    for j in range(even_blanks.count(True)):
                        pt = even_blanks.index(True,pt)
                        i_even.append( pt )
                        pt += 1

                    odd_locs = [odd_idx[it] for it in i_odd]
                    if odd_locs:
                        D.update(update_resp_dict(odd_locs,odds))

                    even_locs = [even_idx[it] for it in i_even]
                    if even_locs:
                        D.update(update_resp_dict(even_locs,evens))

                assert len(D.keys())==len(df[df.billbbl==0])

                ndf = SV.T.pd.DataFrame(columns=['_uid','_billbbl'],data={'_uid':D.keys(),'_billbbl':D.values()})
                ndf.head()
                ndf = ndf[ndf._billbbl!=0].copy().reset_index(drop=True)
                SV.T.conn.set_isolation_level(        0)
                SV.T.cur.execute('drop table if exists tmp')
                ndf.to_sql('tmp',SV.T.eng,index=False)
                SV.T.conn.set_isolation_level(        0)
                SV.T.cur.execute("""update pad_adr p set billbbl = t._billbbl::numeric
                                    from tmp t where p.uid = t._uid;
                                    drop table if exists tmp;""")

                print "Had to look up blocks by hand for remaining 20 BBLs"

                # CREATE TMP_IDX
                a="""

                drop table if exists tmp_addr_idx_pad;

                create table tmp_addr_idx_pad as
                    select
                        predir,
                        name street_name,
                        suftype,
                        sufdir
                    from z_parse_ny_addrs(
                        'select distinct on (stname) uid::bigint gid,''0 ''||stname address, zipcode::bigint from pad_adr
                        where
                        stnum_w_letter is false
                        ');

                select z_make_column_primary_serial_key('tmp_addr_idx_pad','gid',true);

                """
                SV.T.conn.set_isolation_level(        0)
                SV.T.cur.execute(                     a)

                # INSERT PARSED INFO ONTO PAD_ADR
                a="""
                    update pad_adr t set street_name = f1.parsed_addr
                    from
                    (select src_gid,concat_ws(' ',predir,name,suftype,sufdir) parsed_addr
                    from z_parse_ny_addrs('select uid::bigint gid,''0 ''||stname address, zipcode::bigint from pad_adr
                                            where stnum_w_letter is false and street_name is null
                                            ')) f1
                    where f1.src_gid::bigint = t.uid::bigint;
                    """
                SV.T.conn.set_isolation_level(        0)
                SV.T.cur.execute(            a)
                cnt_str = "select count(*) cnt from pad_adr where stnum_w_letter is false and street_name is null"
                cnt = cnt_a = cnt_b = SV.T.pd.read_sql(cnt_str,SV.T.eng).cnt[0]
                while cnt>0 and cnt_a!=cnt_b:
                    cnt_a=SV.T.pd.read_sql(cnt_str,SV.T.eng).cnt[0]
                    SV.T.conn.set_isolation_level(        0)
                    SV.T.cur.execute(            a)
                    cnt = cnt_b = SV.T.pd.read_sql(cnt_str,SV.T.eng).cnt[0]

                assert SV.T.pd.read_sql(""" select count(*)=0 all_addr_in_idx_found_in_pad_adr from
                                            tmp_addr_idx_pad t,
                                            (select array_agg(distinct street_name) all_parsed from pad_adr) f1
                                            where not concat_ws(' ',t.predir,t.street_name,t.suftype,t.sufdir) = any (all_parsed)
                                            """,SV.T.eng).all_addr_in_idx_found_in_pad_adr[0] == True

                # ADD MIN/MAX ADDRESS NUMBERS
                a="""

                update pad_adr set min_num = lhnd::integer where stnum_w_letter is false;
                update pad_adr set max_num = hhnd::integer where stnum_w_letter is false;

                -- UPDATE ALONG lhnd
                update pad_adr set min_num = regexp_replace(lhnd,' 1/3','.33')::double precision
                where stnum_w_letter = true and lhnd ilike '% 1/3%';
                update pad_adr set min_num = regexp_replace(lhnd,' 3/4','.75')::double precision
                where stnum_w_letter = true and lhnd ilike '% 3/4%';
                update pad_adr set min_num = regexp_replace(lhnd,' 1/4','.25')::double precision
                where stnum_w_letter = true and lhnd ilike '% 1/4%';
                update pad_adr set min_num = regexp_replace(lhnd,' 1/2','.5')::double precision
                where stnum_w_letter = true and lhnd ilike '% 1/2%';

                -- UPDATE ALONG hhnd
                update pad_adr set max_num = regexp_replace(hhnd,' 3/4','.75')::double precision
                where stnum_w_letter = true and hhnd ilike '% 3/4%';
                update pad_adr set max_num = regexp_replace(hhnd,' 1/4','.25')::double precision
                where stnum_w_letter = true and hhnd ilike '% 1/4%';
                update pad_adr set max_num = regexp_replace(hhnd,' 1/3','.33')::double precision
                where stnum_w_letter = true and hhnd ilike '% 1/3%';
                update pad_adr set max_num = regexp_replace(hhnd,' 1/2','.5')::double precision
                where stnum_w_letter = true and hhnd ilike '% 1/2%';

                --WHERE '-' in street_num
                update pad_adr set min_num = regexp_replace(lhnd,'-','.','g')::double precision
                where stnum_w_letter = true and lhnd ilike '%%-%%';
                update pad_adr set max_num = regexp_replace(hhnd,'-','.','g')::double precision
                where stnum_w_letter = true and hhnd ilike '%%-%%';

                """
                SV.T.conn.set_isolation_level(          0)
                SV.T.cur.execute(                       a)

                # USE tmp TABLE TO FORMAT ROWS (where stnum_w_letter=True)
                # 1. add rows where lhnd = hhnd
                #
                # 2. ADD ROWS FOR EACH ADDRESS WHERE lhnd and hhnd have street number and one letter, e.g., (304A,304F)
                # 	    make rows for each letter up to and including last letter, e.g., 304A,304B,...304F
                #
                # 3. ADD ROWS WHERE lhnd = hhnd + 'A' , e.g., (304,304A)
                # 	    make row with just number
                # 	    make row with number+A
                #
                # 4. ADD ROWS WHERE lhnd != hhnd and hhnd = # + A, e.g., (300,304A)
                # 	    make row with just number range, e.g., 300...304
                # 	    make row with last number + A, e.g., 304A
                #
                # 5. ADD ROWS WHERE lhnd = hhnd + letter other than 'A' , e.g., (304,304F)
                # 	    make row with just number, e.g., 304
                # 	    make rows for each letter up to and including last letter, e.g., 304A,304B,...304F
                #
                #
                # 6. ADD ROWS WHERE lhnd != hhnd and hhnd = # + letter other than 'A' , e.g., (300,304F)
                # 	    make row with just number range, e.g., 300...304
                # 	    make rows for each letter up to and including last letter, e.g., 304A,304B,...304F
                #
                #
                # 7. ADD ROWS WHERE lhnd+'A' and hhnd, e.g., (4A,6)
                # 	    make row with just letter, e.g., 4A
                # 	    make row with range, e.g., (4,6)
                #
                #
                # 8. ADD ROWS WHERE lhnd!=hhnd,lhnd + word_l,hhnd + word_r,word_l=word_r, e.g., (501 REAR,503 REAR)
                # 	    make row for each number (ALONG PARITY) between lhnd and hhnd
                #
                #
                # 9. REMOVE ROWS ALREADY (and recently done) MANAGED IN pad_adr
                #
                # ### PROVE THAT ALL EXPECTED UID EXIST IN TMP TABLE
                # ### PROVE THAT ALL ROWS IN TMP WHERE min/max_num ARE NULL THEN BOTH min/max_num ARE NULL
                # ### PROVE THAT ONLY ROWS IN tmp WITHOUT min/max_num ARE THOSE ROWS WITH LETTERS
                # # FINISH WITH TMP (update,delete related rows from pad_adr,re-insert rows from tmp,delete tmp)

                one="""
                -- ADD ROWS WHERE lhnd = hhnd
                create table tmp as
                    select * from pad_adr
                    where stnum_w_letter is true
                    and lhnd = hhnd;

                select z_make_column_primary_serial_key('tmp','uid',false);

                alter table tmp add column src_gid integer;
                update tmp set src_gid = uid;
                """
                SV.T.conn.set_isolation_level(          0)
                SV.T.cur.execute(                       one)
                # 2.
                two="""
                -- ADD ROWS FOR EACH ADDRESS WHERE lhnd and hhnd have street number and one letter, e.g., (304A,304F)
                --      make rows for each letter up to and including last letter, e.g., 304A,304B,...304F

                insert into tmp (boro,src_gid,lhnd,hhnd,stname,zipcode,bbl,billbbl)

                select  1 boro,
                        f2.src_gid,
                        (z).alpha_range lhnd,
                        (z).alpha_range hhnd,
                        p.stname,
                        p.zipcode,
                        p.bbl,
                        p.billbbl
                from
                    pad_adr p,
                    (

                    select uid src_gid,uid,regexp_replace(lhnd,no_num_l,'','g') base_str,
                            lhnd,hhnd,no_num_l,no_num_r,z_make_rows_with_alpha_range(uid,only_num_l,no_num_l,no_num_r,false) z
                    from
                        (
                        select uid,lhnd,hhnd,
                            regexp_replace(hhnd,'[^0-9]*','','g') only_num_l,
                            regexp_replace(lhnd,'[0-9]*','','g') no_num_l,
                            regexp_replace(hhnd,'[0-9]*','','g') no_num_r
                        from pad_adr
                        where stnum_w_letter is true
                        and lhnd != hhnd
                        order by stname
                        ) f1
                    where not f1.no_num_l = any (array['','-'])
                    and length(no_num_r)=1

                    ) f2

                where p.uid = f2.uid
                order by p.uid,lhnd;

                """
                SV.T.conn.set_isolation_level(          0)
                SV.T.cur.execute(                       two)
                # 3.
                three="""

                -- ADD ROWS WHERE lhnd =  hhnd + 'A' , e.g., (304,304A)
                --      make row with just number
                --      make row with number+A

                INSERT INTO tmp (boro,src_gid,lhnd,hhnd,stname,zipcode,bbl,billbbl,parity,min_num,max_num)

                select  1,
                        f2.src_gid,
                        f2.lhnd,  --PART 1/2
                        f2.lhnd hhnd,
                        p.stname,
                        p.zipcode,
                        p.bbl,
                        p.billbbl,
                        p.parity,
                        f2.only_num_l::integer min_num,
                        f2.only_num_l::integer max_num
                from
                    pad_adr p,
                    (

                    select uid src_gid,uid,lhnd,hhnd,only_num_l

                    from
                        (
                        select uid src_gid,uid,lhnd,hhnd,
                            regexp_replace(hhnd,'[^0-9]*','','g') only_num_l,
                            regexp_replace(lhnd,'[0-9]*','','g') no_num_l,
                            regexp_replace(hhnd,'[0-9]*','','g') no_num_r
                        from pad_adr
                        where stnum_w_letter is true
                        and lhnd != hhnd
                        order by stname
                        ) f1
                    where f1.no_num_l = any (array['','-'])
                    and no_num_r='A'
                    and lhnd=trim(trailing 'A' from hhnd)


                    ) f2
                where p.uid = f2.uid
                order by p.uid;


                INSERT INTO tmp (boro,src_gid,lhnd,hhnd,stname,zipcode,bbl,billbbl)
                select  1,
                        f2.src_gid,
                        f2.hhnd lhnd,  --PART 2/2
                        f2.hhnd,
                        p.stname,
                        p.zipcode,
                        p.bbl,
                        p.billbbl
                from
                    pad_adr p,
                    (

                    select uid src_gid,uid,lhnd,hhnd

                    from
                        (
                        select uid src_gid,uid,lhnd,hhnd,
                            regexp_replace(hhnd,'[^0-9]*','','g') only_num_l,
                            regexp_replace(lhnd,'[0-9]*','','g') no_num_l,
                            regexp_replace(hhnd,'[0-9]*','','g') no_num_r
                        from pad_adr
                        where stnum_w_letter is true
                        and lhnd != hhnd
                        order by stname
                        ) f1
                    where f1.no_num_l = any (array['','-'])
                    and no_num_r='A'
                    and lhnd=trim(trailing 'A' from hhnd)


                    ) f2
                where p.uid = f2.uid
                order by p.uid;

                """
                SV.T.conn.set_isolation_level(          0)
                SV.T.cur.execute(                       three)
                # 4.
                four="""

                -- ADD ROWS WHERE lhnd != hhnd and hhnd = # + A, e.g., (300,304A)
                --    make row with just number range, e.g., 300...304
                --    make row with last number + A, e.g., 304A


                insert into tmp (boro,src_gid,stname,zipcode,bbl,billbbl,parity,min_num,max_num)

                --PART 1/2
                select  1,
                        f2.src_gid,
                        p.stname,
                        p.zipcode,
                        p.bbl,
                        p.billbbl,
                        p.parity,
                        only_num_l::integer min_num,
                        only_num_r::integer max_num
                from
                    pad_adr p,
                    (
                    select uid src_gid,uid,
                        lhnd,hhnd,
                        only_num_l,only_num_r,
                        no_num_l,no_num_r
                    from
                        (
                        select uid,lhnd,hhnd,
                            regexp_replace(lhnd,'[^0-9]*','','g') only_num_l,
                            regexp_replace(hhnd,'[^0-9]*','','g') only_num_r,
                            regexp_replace(lhnd,'[0-9]*','','g') no_num_l,
                            regexp_replace(hhnd,'[0-9]*','','g') no_num_r
                        from pad_adr
                        where stnum_w_letter is true
                        and lhnd != hhnd
                        order by stname
                        ) f1
                    where f1.no_num_l = any (array['','-'])
                    and no_num_r='A'
                    and not lhnd=trim(trailing 'A' from hhnd)
                    ) f2

                where p.uid = f2.uid
                order by p.uid;


                select  1,
                        f2.src_gid,
                        --f2.lhnd real_lhnd,
                        f2.hhnd lhnd,
                        f2.hhnd,
                        p.stname,
                        p.zipcode,
                        p.bbl,
                        p.billbbl
                from
                    pad_adr p,
                    (

                    select uid src_gid,uid,
                        lhnd,hhnd,
                        only_num_l,only_num_r,
                        no_num_l,no_num_r
                    from
                        (
                        select uid,lhnd,hhnd,
                            regexp_replace(lhnd,'[^0-9]*','','g') only_num_l,
                            regexp_replace(hhnd,'[^0-9]*','','g') only_num_r,
                            regexp_replace(lhnd,'[0-9]*','','g') no_num_l,
                            regexp_replace(hhnd,'[0-9]*','','g') no_num_r
                        from pad_adr
                        where stnum_w_letter is true
                        and lhnd != hhnd
                        order by stname
                        ) f1
                    where f1.no_num_l = any (array['','-'])
                    and no_num_r='A'
                    and not lhnd=trim(trailing 'A' from hhnd)


                    ) f2
                where p.uid = f2.uid
                order by p.uid;


                --PART 2/2
                insert into tmp (boro,src_gid,lhnd,hhnd,stname,zipcode,bbl,billbbl)
                select  1 boro,
                        f2.src_gid,
                        f2.hhnd lhnd,
                        f2.hhnd,
                        p.stname,
                        p.zipcode,
                        p.bbl,
                        p.billbbl
                from
                    pad_adr p,
                    (

                    select uid src_gid,uid,
                        lhnd,hhnd,
                        only_num_l,only_num_r,
                        no_num_l,no_num_r
                    from
                        (
                        select uid,lhnd,hhnd,
                            regexp_replace(lhnd,'[^0-9]*','','g') only_num_l,
                            regexp_replace(hhnd,'[^0-9]*','','g') only_num_r,
                            regexp_replace(lhnd,'[0-9]*','','g') no_num_l,
                            regexp_replace(hhnd,'[0-9]*','','g') no_num_r
                        from pad_adr
                        where stnum_w_letter is true
                        and lhnd != hhnd
                        order by stname
                        ) f1
                    where f1.no_num_l = any (array['','-'])
                    and no_num_r='A'
                    and not lhnd=trim(trailing 'A' from hhnd)


                    ) f2
                where p.uid = f2.uid
                order by p.uid;

                """
                SV.T.conn.set_isolation_level(          0)
                SV.T.cur.execute(                       four)
                # 5.
                five="""

                -- ADD ROWS WHERE lhnd = hhnd and hhnd = # + letter other than A, e.g., (304,304C)
                --    make rows with just number, e.g., 304
                --    make row with last number + A, e.g., 304A,304B,304C


                -- PART 1/2
                INSERT INTO tmp (boro,src_gid,lhnd,hhnd,stname,zipcode,bbl,billbbl)
                select  1,
                        f2.src_gid,
                        --f2.lhnd,
                        --f2.hhnd,
                        (z).alpha_range lhnd,
                        (z).alpha_range hhnd,
                        --f2.only_num_l,
                        --f2.no_num_l,
                        --f2.no_num_r,
                        p.stname,
                        p.zipcode,
                        p.bbl,
                        p.billbbl
                from
                    pad_adr p,
                    (

                    select uid src_gid,uid,regexp_replace(lhnd,no_num_l,'','g') base_str,
                        lhnd,hhnd,only_num_l,only_num_r,no_num_l,no_num_r
                        ,z_make_rows_with_alpha_range(uid,only_num_l,'A',no_num_r,false) z
                    from
                        (
                        select uid,lhnd,hhnd,
                            regexp_replace(lhnd,'[^0-9]*','','g') only_num_l,
                            regexp_replace(hhnd,'[^0-9]*','','g') only_num_r,
                            regexp_replace(lhnd,'[0-9]*','','g') no_num_l,
                            regexp_replace(hhnd,'[0-9]*','','g') no_num_r
                        from pad_adr
                        where stnum_w_letter is true
                        and lhnd != hhnd
                        order by stname
                        ) f1
                    where
                    f1.no_num_l = ''
                    and f1.no_num_r = any (array['B','C','D','E','F','G','H','I','J','K','L','M'])
                    and only_num_l=only_num_r


                    ) f2
                where p.uid = f2.uid
                order by p.uid;


                -- PART 2/2
                INSERT INTO tmp (boro,src_gid,lhnd,hhnd,stname,zipcode,bbl,billbbl,min_num,max_num)
                select  1 boro,
                        f2.src_gid,
                        f2.lhnd lhnd,
                        f2.lhnd hhnd ,
                        p.stname,
                        p.zipcode,
                        p.bbl,
                        p.billbbl,
                        only_num_l::integer min_num,
                        only_num_r::integer max_num
                from
                    pad_adr p,
                    (

                    select uid src_gid,uid,regexp_replace(lhnd,no_num_l,'','g') base_str,
                        lhnd,hhnd,only_num_l,only_num_r,no_num_l,no_num_r
                        --,z_make_rows_with_alpha_range(uid,only_num_l,'A',no_num_r,false) z
                    from
                        (
                        select uid,lhnd,hhnd,
                            regexp_replace(lhnd,'[^0-9]*','','g') only_num_l,
                            regexp_replace(hhnd,'[^0-9]*','','g') only_num_r,
                            regexp_replace(lhnd,'[0-9]*','','g') no_num_l,
                            regexp_replace(hhnd,'[0-9]*','','g') no_num_r
                        from pad_adr
                        where stnum_w_letter is true
                        and lhnd != hhnd
                        order by stname
                        ) f1
                    where
                    f1.no_num_l = ''
                    and f1.no_num_r = any (array['B','C','D','E','F','G','H','I','J','K','L','M'])
                    and only_num_l=only_num_r


                    ) f2
                where p.uid = f2.uid
                order by p.uid--,lhnd;

                """
                SV.T.conn.set_isolation_level(          0)
                SV.T.cur.execute(                       five)
                # 6.
                six="""

                -- ADD ROWS WHERE lhnd != hhnd and hhnd = # + letter other than A, e.g., (300,304B)
                --    make row with just number range, e.g., 300...304
                --    make row with last number + A, e.g., 304A,304B



                --PART 1/2: row with range
                INSERT INTO tmp (boro,src_gid,lhnd,hhnd,stname,zipcode,bbl,billbbl,parity,min_num,max_num)
                select  1 boro,
                        f2.src_gid,
                        only_num_l lhnd,
                        only_num_r hhnd,
                        p.stname,
                        p.zipcode,
                        p.bbl,
                        p.billbbl,
                        p.parity,
                        only_num_l::integer min_num,
                        only_num_r::integer max_num
                from
                    pad_adr p,
                    (
                    select uid src_gid,uid,
                        lhnd,hhnd,only_num_l,only_num_r,no_num_l,no_num_r
                    from
                        (
                        select uid,lhnd,hhnd,
                            regexp_replace(lhnd,'[^0-9]*','','g') only_num_l,
                            regexp_replace(hhnd,'[^0-9]*','','g') only_num_r,
                            regexp_replace(lhnd,'[0-9]*','','g') no_num_l,
                            regexp_replace(hhnd,'[0-9]*','','g') no_num_r
                        from pad_adr
                        where stnum_w_letter is true
                        and lhnd != hhnd
                        order by stname
                        ) f1
                    where
                    f1.no_num_l = ''
                    and f1.no_num_r = any (array['B','C','D','E','F','G','H','I','J','K','L','M'])
                    and only_num_l!=only_num_r
                    ) f2
                where p.uid = f2.uid
                order by p.uid;



                --PART 2/2: rows with alpha_range
                INSERT INTO tmp (boro,src_gid,lhnd,hhnd,stname,zipcode,bbl,billbbl)
                select  1 boro,
                        f2.src_gid,
                        --f2.lhnd,
                        --f2.hhnd,
                        (z).alpha_range lhnd,
                        (z).alpha_range hhnd,
                        --f2.only_num_l,
                        --f2.no_num_l,
                        --f2.no_num_r,
                        p.stname,
                        p.zipcode,
                        p.bbl,
                        p.billbbl
                from
                    pad_adr p,
                    (

                    select uid src_gid,uid,regexp_replace(lhnd,no_num_l,'','g') base_str,
                        lhnd,hhnd,only_num_l,only_num_r,no_num_l,no_num_r
                        ,z_make_rows_with_alpha_range(uid,only_num_l,'A',no_num_r,false) z
                    from
                        (
                        select uid,lhnd,hhnd,
                            regexp_replace(lhnd,'[^0-9]*','','g') only_num_l,
                            regexp_replace(hhnd,'[^0-9]*','','g') only_num_r,
                            regexp_replace(lhnd,'[0-9]*','','g') no_num_l,
                            regexp_replace(hhnd,'[0-9]*','','g') no_num_r
                        from pad_adr
                        where stnum_w_letter is true
                        and lhnd != hhnd
                        order by stname
                        ) f1
                    where
                    f1.no_num_l = ''
                    and f1.no_num_r = any (array['B','C','D','E','F','G','H','I','J','K','L','M'])
                    and only_num_l!=only_num_r


                    ) f2
                where p.uid = f2.uid
                order by p.uid,lhnd;

                """
                SV.T.conn.set_isolation_level(          0)
                SV.T.cur.execute(                       six)
                # 7.
                seven="""
                --ADD ROWS WHERE lhnd+'A' and hhnd, e.g., (4A,6)
                --    make row with just letter, e.g., 4A
                --    make row with range, e.g., (4,6)

                --PART 1/2
                INSERT INTO tmp (boro,src_gid,lhnd,hhnd,stname,zipcode,bbl,billbbl)
                select  1 boro,
                        f2.src_gid,
                        f2.lhnd lhnd,
                        f2.lhnd hhnd,
                        p.stname,
                        p.zipcode,
                        p.bbl,
                        p.billbbl
                from
                    pad_adr p,
                    (
                    select uid src_gid,uid,
                        lhnd,hhnd,only_num_l,only_num_r,no_num_l,no_num_r
                    from
                        (
                        select uid,lhnd,hhnd,
                            regexp_replace(lhnd,'[^0-9]*','','g') only_num_l,
                            regexp_replace(hhnd,'[^0-9]*','','g') only_num_r,
                            regexp_replace(lhnd,'[0-9]*','','g') no_num_l,
                            regexp_replace(hhnd,'[0-9]*','','g') no_num_r
                        from pad_adr
                        where stnum_w_letter is true
                        and lhnd != hhnd
                        order by stname
                        ) f1
                    where
                    f1.no_num_l = 'A'
                    and f1.no_num_r = ''
                    and only_num_l!=only_num_r
                    ) f2
                where p.uid = f2.uid
                and not
                    (
                        f2.lhnd ilike any (array['%% 1/2%%','%% 3/4%%','%%-%%'])
                        or f2.hhnd ilike any (array['%% 1/2%%','%% 3/4%%','%%-%%'])
                    )
                order by p.uid;


                --PART 2/2
                INSERT INTO tmp (boro,src_gid,lhnd,hhnd,stname,zipcode,bbl,billbbl,parity,min_num,max_num)
                select  1 boro,
                        f2.src_gid,
                        only_num_l lhnd,
                        only_num_r hhnd,
                        p.stname,
                        p.zipcode,
                        p.bbl,
                        p.billbbl,
                        p.parity,
                        only_num_l::integer min_num,
                        only_num_r::integer max_num
                from
                    pad_adr p,
                    (
                    select uid src_gid,uid,
                        lhnd,hhnd,only_num_l,only_num_r,no_num_l,no_num_r
                    from
                        (
                        select uid,lhnd,hhnd,
                            regexp_replace(lhnd,'[^0-9]*','','g') only_num_l,
                            regexp_replace(hhnd,'[^0-9]*','','g') only_num_r,
                            regexp_replace(lhnd,'[0-9]*','','g') no_num_l,
                            regexp_replace(hhnd,'[0-9]*','','g') no_num_r
                        from pad_adr
                        where stnum_w_letter is true
                        and lhnd != hhnd
                        order by stname
                        ) f1
                    where
                    f1.no_num_l = 'A'
                    and f1.no_num_r = ''
                    and only_num_l!=only_num_r
                    ) f2
                where p.uid = f2.uid
                order by p.uid;
                """
                SV.T.conn.set_isolation_level(          0)
                SV.T.cur.execute(                       seven)
                # 8.
                eight="""
                --ADD ROWS WHERE lhnd!=hhnd,lhnd + word_l,hhnd + word_r,word_l=word_r, e.g., (501 REAR,503 REAR)
                --    make row for each number (ALONG PARITY) between lhnd and hhnd
                INSERT INTO tmp (boro,src_gid,lhnd,hhnd,stname,zipcode,bbl,billbbl)
                select  1 boro,
                        f2.src_gid,
                        concat_ws(' ',(z).res_i,no_num_l) lhnd,
                        concat_ws(' ',(z).res_i,no_num_l) hhnd,
                        p.stname,
                        p.zipcode,
                        p.bbl,
                        p.billbbl
                from
                    pad_adr p,
                    (
                    select uid src_gid,uid,
                        lhnd,hhnd,only_num_l,only_num_r,no_num_l,no_num_r
                        ,z_make_rows_with_numeric_range(uid,only_num_l::integer,only_num_r::integer,true) z
                    from
                        (
                        select uid,lhnd,hhnd,
                            regexp_replace(lhnd,'[^0-9]*','','g') only_num_l,
                            regexp_replace(hhnd,'[^0-9]*','','g') only_num_r,
                            regexp_replace(lhnd,'[0-9]*','','g') no_num_l,
                            regexp_replace(hhnd,'[0-9]*','','g') no_num_r
                        from pad_adr
                        where stnum_w_letter is true
                        and lhnd != hhnd
                        order by stname
                        ) f1
                    where
                    f1.no_num_l != ''
                    and f1.no_num_r != ''
                    and ( length(no_num_l)>0 or length(no_num_r)>0 )
                    and only_num_l!=only_num_r
                    and no_num_l=no_num_r
                    ) f2
                where p.uid = f2.uid
                and not
                    (
                        f2.lhnd ilike any (array['%% 1/2%%','%% 3/4%%','%%-%%'])
                        or f2.hhnd ilike any (array['%% 1/2%%','%% 3/4%%','%%-%%'])
                    )
                order by p.uid,(z).res_i;
                """
                SV.T.conn.set_isolation_level(          0)
                SV.T.cur.execute(                       eight)
                # 9.
                nine="""
                -- REMOVE ROWS ALREADY (and recently done) MANAGED IN pad_adr
                delete from tmp
                where   stnum_w_letter = true
                        and (
                        (lhnd ilike '% 3/4%'
                        or lhnd ilike '% 1/4%'
                        or lhnd ilike '% 1/3%'
                        or lhnd ilike '% 1/2%'
                        or lhnd ilike '%-%')
                        or
                        (hhnd ilike '% 3/4%'
                        or hhnd ilike '% 1/4%'
                        or hhnd ilike '% 1/3%'
                        or hhnd ilike '% 1/2%'
                        or hhnd ilike '%-%')
                        );
                """
                SV.T.conn.set_isolation_level(          0)
                SV.T.cur.execute(                       nine)

                ### PROVE THAT ALL EXPECTED UID EXIST IN TMP TABLE
                assert PG.T.pd.read_sql(    """ select count(*)=0 all_expected_uid_from_pad_adr_exist_in_tmp
                                                from
                                                (select distinct on (uid) * from pad_adr
                                                    where stnum_w_letter = true and not
                                                    (
                                                        lhnd ilike any (array['%% 1/2%%','%% 3/4%%','%% 1/4%%','%% 1/3%%','%%-%%'])
                                                        or hhnd ilike any (array['%% 1/2%%','%% 3/4%%','%% 1/4%%','%% 1/3%%','%%-%%'])
                                                    )) p,
                                                (select array_agg(distinct src_gid) all_t_uid from tmp) f2

                                                where not array[p.uid] && all_t_uid
                                            """,PG.T.eng).all_expected_uid_from_pad_adr_exist_in_tmp[0]==True

                ### PROVE THAT ALL ROWS IN TMP WHERE min/max_num ARE NULL THEN BOTH min/max_num ARE NULL
                assert PG.T.pd.read_sql("""
                                            select count(*)=0 min_max_null_or_not_null_equally
                                            from tmp where (min_num is null or max_num is null)
                                            and not (min_num is null and max_num is null)
                                        """,PG.T.eng).min_max_null_or_not_null_equally[0]==True

                ### PROVE THAT ONLY ROWS IN tmp WITHOUT min/max_num ARE THOSE ROWS WITH LETTERS
                assert PG.T.pd.read_sql("""
                                            select count(*)=0 rows_without_letters_and_without_min_max
                                            from tmp where
                                            (min_num is null and not lhnd ~ '[a-zA-z]')
                                            or (max_num is null and not hhnd ~ '[a-zA-z]')
                                        """,PG.T.eng).rows_without_letters_and_without_min_max[0]==True

                # FINISH WITH TMP (update,delete related rows from pad_adr,re-insert rows from tmp,delete tmp)
                finish_up="""

                -- ADD parser_info TO pad_adr WHERE NO STREET_NAME (should be those rows with lhnd or hhnd having '1/2', etc...)
                WITH upd AS (
                    SELECT  src_gid,predir,name street_name,suftype,sufdir
                    FROM    z_parse_NY_addrs('
                                            select
                                                uid::bigint gid,
                                                concat_ws('' '',''0'',stname)::text address,
                                                zipcode::bigint zipcode
                                            FROM pad_adr
                                            WHERE street_name is null
                                            ')
                    )
                UPDATE pad_adr t set
                    predir = u.predir,
                    street_name = u.street_name,
                    suftype = u.suftype,
                    sufdir = u.sufdir
                FROM  upd u
                WHERE u.src_gid = t.uid::bigint;

                -- ADD parser_info TO tmp
                WITH upd AS (
                    SELECT  src_gid,predir,name street_name,suftype,sufdir
                    FROM    z_parse_NY_addrs('
                                            select
                                                uid::bigint gid,
                                                concat_ws('' '',''0'',stname)::text address,
                                                zipcode::bigint zipcode
                                            FROM tmp
                                            ')

                    )
                UPDATE tmp t set
                    predir = u.predir,
                    street_name = u.street_name,
                    suftype = u.suftype,
                    sufdir = u.sufdir
                FROM  upd u
                WHERE u.src_gid = t.uid::bigint;


                -- COPY OVER REMAINING DATA TO tmp
                update tmp t set
                    block = p.block,
                    lot = p.lot,
                    bin = p.bin,
                    lhns = p.lhns,
                    lcontpar = p.lcontpar,
                    lsos = p.lsos,
                    hhns = p.hhns,
                    hcontpar = p.hcontpar,
                    hsos = p.hsos,
                    scboro = p.scboro,
                    sc5 = p.sc5,
                    sclgc = p.sclgc,
                    stname = p.stname,
                    addrtype = p.addrtype,
                    realb7sc = p.realb7sc,
                    validlgcs = p.validlgcs,
                    b10sc = p.b10sc,
                    segid = p.segid
                from pad_adr p
                where t.src_gid = p.uid;

                -- DELETE FROM pad_adr THOSE ROWS ABOUT TO BE RE-INSERTED BACK INTO pad_adr FROM tmp
                delete from pad_adr p
                using (select array_agg(distinct src_gid) all_t_uid from tmp) t
                where array[p.uid] && all_t_uid;


                -- RE-INSERT FORMATTED ROWS FROM TMP
                insert into pad_adr (boro,block,lot,bin,
                    lhnd,lhns,lcontpar,lsos,
                    hhnd,hhns,hcontpar,hsos,
                    scboro,sc5,sclgc,stname,addrtype,realb7sc,validlgcs,parity,b10sc,segid,
                    uid,bbl,stnum_w_letter,
                    predir,street_name,suftype,sufdir,min_num,max_num,billbbl,tmp)
                select
                    boro,block,lot,bin,
                    lhnd,lhns,lcontpar,lsos,
                    hhnd,hhns,hcontpar,hsos,
                    scboro,sc5,sclgc,stname,addrtype,realb7sc,validlgcs,parity,b10sc,segid,
                    uid,bbl,stnum_w_letter,
                    predir,street_name,suftype,sufdir,min_num,max_num,billbbl,tmp
                from tmp;

                -- DROP tmp TABLE
                DROP TABLE tmp;

                """
                SV.T.conn.set_isolation_level(          0)
                SV.T.cur.execute(                       finish_up)

                # TIGHTEN THINGS UP

                # 1. Satisfy/Prove condition:  no_rows_where_only_min_or_max_num_is_null
                t="""   update pad_adr set min_num = lhnd::integer
                        where (min_num is null and max_num is not null);

                        update pad_adr set max_num = hhnd::integer
                        where (max_num is null and min_num is not null);
                """
                SV.T.conn.set_isolation_level(          0)
                SV.T.cur.execute(                       t)
                assert PG.T.pd.read_sql(""" select count(*)=0 no_rows_where_only_min_or_max_num_is_null
                                            from pad_adr where
                                            (min_num is null and max_num is not null)
                                            or
                                            (max_num is null and min_num is not null)
                                        """,PG.T.eng).no_rows_where_only_min_or_max_num_is_null[0]==True

                # 2. Prove that all_rows_where_min_or_max_is_null_have_lhnd_equal_hhnd
                assert PG.T.pd.read_sql(""" select count(*)=0 all_rows_where_min_or_max_is_null_have_lhnd_equal_hhnd
                                            from pad_adr
                                            where (min_num is null or max_num is null) and lhnd != hhnd
                                        """,PG.T.eng).all_rows_where_min_or_max_is_null_have_lhnd_equal_hhnd[0]==True


                # ** BELOW NEEDS TO BE INTEGRATED WITH ABOVE
                a="""
                    -- UPDATE MIN/MAX BLDG NUMBERS
                    update pad_adr set min_num = lhnd::double precision,max_num = hhnd::double precision
                    where stnum_w_letter is false;

                    -- ADD PARSED INFO
                    alter table pad_adr add column tmp_addr text;
                    update pad_adr set tmp_addr = concat_ws(' ',min_num::integer,stname) where stnum_w_letter is false;

                    select z_update_with_parsed_info(array_agg(p.uid),'pad_adr','uid','tmp_addr','zipcode',
                                                        array['street_name','predir','suftype','sufdir'])
                    from pad_adr p where stnum_w_letter is false;

                    alter table pad_adr drop column if exists tmp_addr;

                    -- MAKE LINKAGE B/T pad_adr AND pluto
                    --    (having already asserted all pad_bbl.billbbl exist in pluto)
                    update pad_adr a set billbbl = b.billbbl
                        from pad_bbl b where
                        b.lobbl = a.bbl
                        or b.hibbl = a.bbl
                        or b.billbbl = a.bbl;

                    -- ADD GEOM/BBL BASE ON MATCHES WITH PLUTO
                    select z_update_with_geom_from_parsed(array_agg(p.uid),'pad_adr','uid')
                    from pad_adr p where stnum_w_letter is false;

                """
                SV.T.conn.set_isolation_level(        0)
                SV.T.cur.execute(                     a)

                # ** THIS SHOULD BE AN ASSERTION
                a="""
                    select count(*) from pad_adr where
                    stnum_w_letter is false
                    and
                        (street_name is null
                        or (suftype is null and
                            not (
                                street_name ilike '%broadway%'
                                or street_name ilike '%bowery%'
                                or street_name ilike '%slip%'
                                )
                            )
                        or min_num is null
                        or max_num is null)
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

