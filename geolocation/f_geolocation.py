
# from ipdb import set_trace as i_trace; i_trace()



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

    def update(self,upd):
        return self.__init__(upd)

    def has_key(self,key):
        return self.__dict__.has_key(key)



class Geocoding:

    def __init__(self,_parent):
        self.SV                             =   _parent
        self.T                              =   _parent.T
        self.GeoCoding                      =   self
        from pygeocoder                         import Geocoder  # sudo port select python python26
        self.T.update(                          {'Geocoder'           :   Geocoder })
        # generally             --
        # java version          -- https://developers.google.com/maps/documentation/javascript/geocoding
        # java limits           -- https://developers.google.com/maps/documentation/geocoding/#Limits
        # also, consider geopy  -- https://pypi.python.org/pypi/geopy


    def getGPScoord(self,all_addr,printGPS=True,savePath='tmp_results.txt'):

        if type(all_addr) is list:
            z=all_addr
        else:
            f=open(R,'r')
            x=f.read()
            f.close()
            z=x.split('\r')

        d = self.T.pd.DataFrame({'addr':z})
        _iter = self.T.pd.Series(d.addr.unique().tolist()).iterkv()

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

        d = self.T.pd.DataFrame(y)
        d['lat'],d['lon'] = zip(*d.geometry.map(lambda s: (s['location']['lat'],s['location']['lng'])))
        if savePath!='': d.to_csv(savePath)
        return d

    def get_reverse_geo(self,fileWithCoords):
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

    def getArcLenBtCoords(self,lat1, long1, lat2, long2):
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

    def getTriCoorLocations(self):
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



class Addr_Parsing:

    def __init__(self):
        from types                              import NoneType
        from re                                 import sub              as re_sub
        import                                  pandas                  as pd
        pd.set_option(                          'expand_frame_repr', False)
        pd.set_option(                          'display.max_columns', None)
        pd.set_option(                          'display.max_rows', 1000)
        pd.set_option(                          'display.width', 180)
        np                                  =   pd.np
        np.set_printoptions(                    linewidth=200,threshold=np.nan)
        from os                                 import environ          as os_environ
        from uuid                               import uuid4            as get_guid
        from sys                                import path             as py_path
        py_path                             =   py_path
        py_path.append(                         os_environ['HOME'] + '/.scripts')
        from system_settings                    import DB_HOST,DB_PORT
        from sqlalchemy                         import create_engine
        from logging                            import getLogger
        from logging                            import INFO             as logging_info
        getLogger(                              'sqlalchemy.dialects.postgresql').setLevel(logging_info)
        eng                                 =   create_engine(r'postgresql://postgres:postgres@%s:%s/%s'
                                                          %(DB_HOST,DB_PORT,'routing'),
                                                          encoding='utf-8',
                                                          echo=False)
        D                                   =   {'NoneType'         :   NoneType,
                                                 're_sub'           :   re_sub,
                                                 'pd'               :   pd,
                                                 'np'               :   np,
                                                 'eng'              :   eng,
                                                 'guid'             :   str(get_guid().hex)[:7]}
        self.T                              =   To_Class(D)
        self.ST_Parts                       =   self.ST_Parts(self)


    class ST_Parts:

        def __init__(self,_parent):

            ST_STRIP_BEFORE_DICT            =   {
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


    def find_addr_idx_matches(self,addr_list):
        cmd = ('select * from addr_idx '+
               'where addr = any(array'+str(addr_list)+')')
        return self.T.pd.read_sql(cmd,self.T.eng)

    def explode_addresses(self,df='cols = addr,norm_addr'):

        pre_re_s = re_search_string = r'^('+"|".join(ST_PREFIX_DICT.values())+r')'
        alp  = a_less_prefix = self.T.pd.DataFrame({'norm_addr_body':df.norm_addr.map(lambda s: self.T.re_sub(pre_re_s,'',s.strip()).strip()),
                                            'orig_addr':df.addr.tolist()})

        suf_re_s = re_search_string = r'('+r'|'.join(ST_SUFFIX_DICT.values())+r')$'
        als  = a_less_suffix = self.T.pd.DataFrame({'norm_addr_body':df.norm_addr.map(lambda s: self.T.re_sub(suf_re_s,'',s.strip()).strip()),
                                            'orig_addr':df.addr.tolist()})

        alps = a_less_prefix_less_suffix = self.T.pd.DataFrame({'norm_addr_body':alp.norm_addr_body.map(lambda s: self.T.re_sub(suf_re_s,'',s.strip()).strip()),
                                                        'orig_addr':df.addr.tolist()})

        all_a = alp.append(als,ignore_index=True).append(alps,ignore_index=True).reset_index(drop=True)
        all_a = all_a[all_a.norm_addr_body!='']
        j,k = all_a.norm_addr_body.tolist(),df.norm_addr.tolist()
        all_unique_addr_list = dict(zip(j+k,range(0,len(j)+len(k)))).keys()
        all_a['cnt'] = all_a.norm_addr_body.map(lambda s: all_unique_addr_list.count(s))

        x = all_a[all_a.cnt==1].reset_index(drop=True)
        x.drop(['cnt'],axis=1,inplace=True)
        return x

    def get_show_info(self,r,df,show_info=False):
        if show_info==True: print len(r),'remaining addresses\t\t',str(round(float((len(df)-len(r))/float(len(df)))*100,2))+'% overall recognition\n'

    def get_addr_body(self,r,from_label='norm_addr'):
        pre_re_s = re_search_string = r'^('+"|".join(ST_PREFIX_DICT.values())+r')\s'
        suf_re_s = re_search_string = r'\s('+r'|'.join(ST_SUFFIX_DICT.values())+r')$'
        r['body'] = r[from_label].map(lambda s: self.T.re_sub(pre_re_s,r'',s).strip()
                                      if ST_SUFFIX_DICT.values().count(  # this extra is to prevent a "st" result
                                                                       self.T.re_sub(pre_re_s,r'',s).strip()
                                                                       ) == 0 else ''
                                      ).map(lambda s: self.T.re_sub(suf_re_s,r'',s).strip()
                                            if ST_SUFFIX_DICT.values().count(  # this extra is to prevent a "w" result
                                                                             self.T.re_sub(suf_re_s,r'',s).strip()
                                                                             ) == 0 else s)
        return r

    def update_with_idx_matches(self,ur,r,dbm='database_matches',input_addr_col='from_label',
                                result_idx_col='idx'):

        addr_idx_map                        =   dict(zip(dbm[input_addr_col].tolist(),dbm[result_idx_col].tolist()))
        dbm_addr                            =   addr_idx_map.keys()
        recog_idx                           =   r[r[input_addr_col].isin(dbm_addr)==True].index
        tmp                                 =   r.ix[recog_idx,:]
        tmp['bldg_street_idx']              =   tmp[input_addr_col].map(addr_idx_map)
        if type(ur) is str:
            ur                              =   tmp
            r = remaining_addr              =   r[r.index.isin(recog_idx)==False].reset_index(drop=True)
        else:
            ur                              =   ur.append(tmp,ignore_index=True)
            r                               =   r[r.index.isin(recog_idx)==False].reset_index(drop=True)
        return ur,r

    def match_levenshtein_series(self,ur='user_recognized_addr',r='remaining_addr',df='source_df',
                                 from_label='body',show_info=False):
        #  levenshtein(text source, text target, int insert_cost, int delete_cost, int substitution_cost)

        if show_info==True: print '\n\n\t-- SEARCH lev-variant1 --\n'
        T = { '1':from_label, '2':'idx', '3':str(r[from_label].tolist()) }
        cmd = """
            SELECT %(1)s,a.bldg_street_idx %(2)s,a.street,levenshtein(a.street,%(1)s,1,0,4)
            from addr_idx a,unnest(array[%(3)s]) %(1)s
            where soundex(a.street) = any(select soundex(x) from regexp_split_to_table(%(1)s,E'\s+') x)
            and a.one_word is true
            and a.bldg_street_idx is not null
            order by levenshtein(a.street,%(1)s,1,0,4)
            """.replace('\n',' ') % T
        dbm = db_matches = self.T.pd.read_sql(cmd,self.T.eng)
        dbm = dbm[dbm.levenshtein<=3]
        ur,r = self.update_with_idx_matches(ur,r,dbm,input_addr_col=T['1'],result_idx_col=T['2'])
        self.get_show_info(r,df,show_info)

        # DIFFERENCE SHOULD ONLY BE MEASURED IN LETTERS
        # 0 DIFF --> MATCH
        # 1 DIFF,ONLY LETTERS --> MATCH
        if show_info==True: print '\n\n\t-- SEARCH lev-variant2 --\n'
        T = { '1':from_label, '2':'idx', '3':str(r[from_label].tolist()) }
        cmd = """
            SELECT %(1)s,a.bldg_street_idx %(2)s,a.street,levenshtein(a.street,%(1)s,1,1,4) lev,difference(a.street,%(1)s) diff
            from addr_idx a
            inner join unnest(array[%(3)s]) %(1)s
            on levenshtein(a.street,%(1)s,1,1,4)<=1
            and a.one_word is true
            and a.bldg_street_idx is not null
            order by a.street
            """.replace('\n',' ') % T
        dbm = db_matches = self.T.pd.read_sql(cmd,self.T.eng)
        ur,r = self.update_with_idx_matches(ur,r,dbm,input_addr_col=T['1'],result_idx_col=T['2'])
        self.get_show_info(r,df,show_info)

        if show_info==True: print '\n\n\t-- SEARCH lev-variant3 --\n'
        T = { '1':from_label, '2':'idx', '3':str(r[from_label].tolist()) }
        cmd = """SELECT a.bldg_street_idx %(2)s,a.street,levenshtein(a.street,%(1)s,1,0,4) lev,%(1)s
            from addr_idx a
            inner join unnest(array[%(3)s]) %(1)s
            on levenshtein(a.street,%(1)s,1,1,4)<=1
            where a.bldg_street_idx is not null""".replace('\n',' ') % T
        dbm = db_matches = self.T.pd.read_sql(cmd,self.T.eng)
        ur,r = self.update_with_idx_matches(ur,r,dbm,input_addr_col=T['1'],result_idx_col=T['2'])
        self.get_show_info(r,df,show_info)

        if show_info==True: print '\n\n\t-- SEARCH lev-variant4 --\n'
        T = { '1':from_label, '2':'idx', '3':str(r[from_label].tolist()) }
        cmd = """SELECT %(1)s,a.bldg_street_idx %(2)s,a.street
            from addr_idx a
            inner join unnest(array[%(3)s]) %(1)s
            on street ~* %(1)s
            where a.bldg_street_idx is not null
            """.replace('\n',' ') % T
        dbm = db_matches = self.T.pd.read_sql(cmd,self.T.eng)
        ur,r = self.update_with_idx_matches(ur,r,dbm,input_addr_col=T['1'],result_idx_col=T['2'])
        self.get_show_info(r,df,show_info)

        return ur,r

    def match_simple_regex(self,ur='user_recognized_addr',r='remaining_addr',df='source_df',
                           from_label='norm_addr',show_info=False):
        T = {   '1' : from_label,
                '2' : str(r[from_label].map(lambda s: str(s)).tolist())
            }
        cmd = """
            SELECT %(1)s,a.bldg_street_idx idx,a.street
            from addr_idx a
            inner join unnest(array[%(2)s]) %(1)s
            on a.street ~* %(1)s
            where one_word is true
            and bldg_street_idx is not null
            """.replace('\n',' ') % T
        dbm = db_matches = self.T.pd.read_sql(cmd,self.T.eng)
        ur,r = self.update_with_idx_matches(ur,r,dbm,input_addr_col=from_label,result_idx_col='idx')
        self.get_show_info(r,df,show_info)
        return ur,r

    def match_simple(self,ur='user_recognized_addr',r='remaining_addr',df='source_df',
                     from_label='addr_street',show_info=False):
        if type(r) is str:  x               =   df
        else:               x               =   r
        T = { '1':from_label, '2':'idx', '3':x[from_label].map(str).tolist() }
        cmd = """
            SELECT %(1)s,a.bldg_street_idx %(2)s,a.street
            from addr_idx a
            inner join unnest(array[%(3)s]) %(1)s
            on a.street = %(1)s
            where bldg_street_idx is not null
            """.replace('\n',' ') % T
        dbm = db_matches = self.T.pd.read_sql(cmd,self.T.eng)
        ur,r = self.update_with_idx_matches(ur,x,dbm,input_addr_col=T['1'],result_idx_col=T['2'])
        self.get_show_info(r,x,show_info)
        return ur,r

    def pagc_normalize_address(self,r,from_label='full_address',to_label='norm_street'):

        # see /Users/admin/Reference/Python/READ--PAGC.pdf

        #    house_num,predir, name, suftype, sufdir, unit, city, state, postcode

            #    address is an integer: The street number
            #    predirAbbrev is varchar: Directional prefix of road such as N, S, E, W etc. These are controlled using the direction_lookup table.
            #    streetName varchar
            #    streetTypeAbbrev varchar abbreviated version of street type: e.g. St, Ave, Cir. These are controlled using the street_type_lookup table.
            #    postdirAbbrev varchar abbreviated directional suffice of road N, S, E, W etc. These are controlled using the direction_lookup table.
            #    internal varchar internal address such as an apartment or suite number.
            #    location varchar usually a city or governing province.
            #    stateAbbrev varchar two character US State. e.g MA, NY, MI. These are controlled by the state_lookup table.
            #    zip varchar 5-digit zipcode. e.g. 02109.
            #    parsed boolean - denotes if addess was formed from normalize process. The normalize_address function sets this to true before returning the address.

        ### normalizing addresses

        arr                                 =   r[from_label].map(str).tolist()
        addr                                =   r[from_label].map(lambda s: s[:s.find(',')].upper())
        zips                                =   r[from_label].map(lambda s: int(s[s.rfind(' ')+1:]))
        mock_gids                           =   range(len(arr))

        T                                   =   {'gids'             :   str(mock_gids),
                                                 'addr'             :   str(addr.tolist()).replace("'","''"),
                                                 'zips'             :   str(zips.tolist()),
                                                 'to_label'         :   to_label}
        # cmd                                 =   """
        #     select r,lower(pprint_addy(pagc_normalize_address(r))) %(to_label)s
        #     from unnest(array[%(arr)s]) r
        #                                         """.replace('\n','') % T
        cmd = """
            select * from z_parse_NY_addrs('
                select  unnest(array[%(gids)s]) gid,
                        unnest(array[%(addr)s]) address,
                        unnest(array[%(zips)s]) zipcode
                                            ')
                """.replace('\n','') % T

        n = self.T.pd.read_sql(cmd,self.T.eng)

        lc = lambda s: "" if s==None else s
        collect_cols = ['predir','name','suftype','sufdir']
        for it in collect_cols:
            n[it] = n[it].map(lc)
        n['addr'] = n[collect_cols].apply(lambda s: str(' '.join(s).lower()),axis=1)

        # assert len( n[(n.bldg.isnull())&(n.box.isnull())&(n.unit.isnull())&(n.pretype.isnull())& (n.qual.isnull())] ) == 0
        # n[(n.bldg.isnull()==False)|(n.box.isnull()==False)|(n.pretype.isnull()==False)|(n.qual.isnull()==False)]

        # n_map = dict(zip(n.r.tolist(),n[to_label].tolist()))

        r[to_label+'_num'] = n.num.tolist()
        r[to_label] = n['addr']
        return r

    def get_bldg_street_idx(self,df,addr_set_col='addr_set',addr_num_col='addr_num',
                            addr_street_col='addr_street',zipcode_col='zipcode',show_info=False):
        # cols = [u'seam_id', u'addr_num', u'addr_street', u'zipcode']

        #df.rename(columns={addr_num_col:'addr_num',addr_street_col:'addr_street'},inplace=True)

        all_cols                            =   df.columns.tolist()
        num_col_i                           =   all_cols.index(addr_num_col)
        str_col_i                           =   all_cols.index(addr_street_col)
        zip_col_i                           =   all_cols.index(zipcode_col)

        # ur = user/comp recognized
        # r = remaining_addr
        # TCL = to-check-later ... the addr.s not normalized

        uniq_idx                            =   dict(zip(df[addr_set_col].tolist(),df.index.tolist()))
        d                                   =   df[df.index.isin(uniq_idx.values())].reset_index(drop=True)
        d['full_address']                   =   d.apply(lambda s: str(s[num_col_i])+' '+str(s[str_col_i]) +
                                                                  ', NEW YORK, NY, '+str(s[zip_col_i]),axis=1)
        d['norm_addr_num']                  =   d.index.map(lambda s: None)
        d['norm_addr']                      =   d.index.map(lambda s: None)
        d['body']                           =   d.index.map(lambda s: None)
        d['bldg_street_idx']                =   d.index.map(lambda s: None)
        if show_info==True:                     print len(d),'total uniq addresses\n',d.head()

        if show_info==True:                     print '\n\n\t-- SEARCH #1 AFTER geoparse --\n'
        ur,r                                =   self.match_simple(ur='',r='',df=d,from_label=addr_street_col)
        if show_info==True:                     print len(r),'remaining addresses\t\t',str(round(float((len(d)-len(r))/float(len(d)))*100,2))+'% overall recognition\n'
        if show_info==True:                     print len(d),'=',len(r)+len(ur),'True?'

        r                                   =   self.pagc_normalize_address(r,from_label='full_address',to_label='norm_street')
        r                                   =   self.clean_street_names(r,'norm_street','norm_street')

        # from ipdb import set_trace as i_trace; i_trace()

        ### getting base ("body") of address, if address='e 45 st', body='45'
        # r = get_addr_body(r,from_label='norm_addr')

        ### create seperate list for addresses with malformed norm_addr
        TCL = to_check_later = r[r[addr_num_col].map(lambda s: len(self.T.re_sub(r'^[0-9]+$',r'',str(s)))!=0)].copy()
        r = r[r.index.isin(TCL.index)==False].reset_index(drop=True)
        TCL = TCL.reset_index(drop=True)
        if show_info==True:                     print '\n',len(TCL),'issue addresses ("TCL")\n'

        if show_info==True:                     print '\n\n\n\t-- SEARCH #2 ./PAGC normalization,body --\n'
        # ur,r = self.match_simple(ur=ur,r=r,df='',from_label='body')
        ur,r = self.match_simple(ur=ur,r=r,df='',from_label='norm_street')
        if show_info==True:                     print len(r),'remaining addresses\t\t',str(round(float((len(d)-len(r))/float(len(d)))*100,2))+'% overall recognition\n'

        if show_info==True:                     print '\n\n\n\t-- SEARCH #3 ./match simple regex --\n'
        ur,r = self.match_simple_regex(ur,r,from_label='norm_street')
        if show_info==True:                     print len(r),'remaining addresses\t\t',str(round(float((len(d)-len(r))/float(len(d)))*100,2))+'% overall recognition\n'

        # ur,r = match_levenshtein_series(ur=ur,r=r,df=d,from_label='body',show_info=False)
        ur,r = self.match_levenshtein_series(ur=ur,r=r,df=d,from_label='norm_street',show_info=False)


        return ur,r,TCL

    def clean_street_names(self,df,from_label,to_label):

        def remove_non_ascii(text):
            return self.T.re_sub(r'[^\x00-\x7F]+',' ', text)

        df_ignore                       =   df[df[from_label].map(lambda s: type(s))==self.T.NoneType]
        df_ignore_idx                   =   df_ignore.index.tolist()
        if len(df_ignore_idx)>0:
            df                          =   df.ix[df[df.index.isin(df_ignore_idx)==False].index,:]

        df[to_label]                    =   df[from_label].map(lambda s: s.lower().strip())
        df[to_label]                    =   df[to_label].map(remove_non_ascii)

        # st_strip_before
        for k,v in self.ST_Parts.ST_STRIP_BEFORE_DICT.iteritems():
            df[to_label]                =   df[to_label].map(lambda s: self.T.re_sub(k,v,s))

        # st_prefix
        for k,v in self.ST_Parts.ST_PREFIX_DICT.iteritems():
            df[to_label]                =   df[to_label].map(lambda s: self.T.re_sub(r'^('+k+r')\s',v+r' ',s)
                                                if self.ST_Parts.ST_SUFFIX_DICT.values().count(
                                                self.T.re_sub(r'^('+k+r')\s',v+r' ',s)
                                                ) == 0 else s)

        # st_suffix
        for k,v in self.ST_Parts.ST_SUFFIX_DICT.iteritems():
            df[to_label]                =   df[to_label].map(lambda s: self.T.re_sub(r'\s('+k+r')$'   ,r' '+v,s))

        # st_body
        for k,v in self.ST_Parts.ST_BODY_DICT.iteritems():
            df[to_label]                =   df[to_label].map(lambda s: self.T.re_sub(k,v,s))

        # st_strip_after
        for k,v in self.ST_Parts.ST_STRIP_AFTER_DICT.iteritems():
            df[to_label]                =   df[to_label].map(lambda s: self.T.re_sub(k,v,s))

        return df.append(                   df_ignore)

class GeoLocation:

    def __init__(self):

        from re                             import sub              as re_sub           # re_sub('patt','repl','str','cnt')
        from os                             import environ          as os_environ
        from uuid                           import uuid4            as get_guid
        from sys                            import path             as py_path
        py_path                             =   py_path
        py_path.append(                         os_environ['HOME'] + '/.scripts')
        from system_settings                import DB_HOST,DB_PORT
        import                                  pandas          as pd
        # from pandas.io.sql                import execute              as sql_cmd
        self.T.pd.set_option(                              'expand_frame_repr', False)
        self.T.pd.set_option(                              'display.max_columns', None)
        self.T.pd.set_option(                              'display.max_rows', 1000)
        self.T.pd.set_option(                              'display.width', 180)
        np                                  =   self.T.pd.np
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
        all_imports                         =   locals().keys()
        D                                   =   {'pd'           :   pd,
                                                 'np'           :   np,
                                                 'gd'           :   gd,
                                                 'conn'         :   conn,
                                                 'cur'          :   cur,
                                                 'eng'          :   eng,
                                                 'os_environ'   :   os_environ,
                                                 'py_path'      :   py_path,
                                                 'guid'         :   str(get_guid().hex)[:7]}
        for k in all_imports:
            if not D.has_key(k):
                D.update(                       {k                      :   eval(k) })
        self.T                              =   To_Class(D)
        self.Addr_Parsing                   =   Addr_Parsing()
        self.GeoCoding                      =   Geocoding()


        # BASE_SAVE_PATH = '/Users/admin/Projects/GIS/table_data/'


if __name__ == '__main__':

    gc = Geocoding()
    gc.fileWithAddresses = '/Users/admin/Desktop/work_locations.txt'
    gc.getGPScoord(fileWithAddresses,printGPS=True,save=False,reverse=False)
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