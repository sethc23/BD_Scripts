
from os                             import environ          as os_environ
from uuid                           import uuid4            as get_guid
from os                             import path             as os_path
from sys                            import path             as py_path

import                                  pandas              as pd
np                                  =   pd.np
from re                             import sub              as re_sub  # re_sub('pattern','repl','string','count')
from re                             import search           as re_search # re_search('pattern','string')


BASE_SAVE_PATH                      =   os_path.join(os_environ['BD'],'geolocation/NYC/snd15a/')
src_fpath                           =   BASE_SAVE_PATH+'snd15Acow.txt'
base_path                           =   src_fpath.rstrip('.txt')
SND_NON_S_PATH                      =   base_path + '_non_s_recs.csv'
SND_S_PATH                          =   base_path + '_s_recs.csv'


def create_numbered_streets(a='numbered_streets_from_lots',street_column='addr'):

    w = a[a[street_column].str.contains('^(w)\s[0-9]+')==True]
    w['street_num'] = w[street_column].map(lambda s: eval(s[2:-3]))
    # w['street'] = w.uniq_st_orig.map(lambda s: s[2:])
    # print len(w.index),'west'
    
    e = a[a[street_column].str.contains('^(e)\s[0-9]+')==True]
    e['street_num'] = e[street_column].map(lambda s: eval(s[2:-3]))
    # e['street'] = e.uniq_st_orig.map(lambda s: s[2:])
    # print len(e.index),'east'
    
    a = numbered_street = []
    # n = numbered_streets = a.ix[a.index-w.index-e.index,:]
    # nn = non_numbered_streets = a.ix[a.index-n.index,:]
    # print 'check\t',len(a),' == ',len(n)+len(nn)
    
    w_below_59 = map(lambda s: 'w '+str(s)+' st',range(1,60))
    e_below_59 = map(lambda s: 'e '+str(s)+' st',range(1,60))
    below_59 = map(lambda s: str(s)+' st',range(1,60))
    # print len(below_59),'below_59\t\tx3'
    a.extend(w_below_59)
    a.extend(e_below_59)
    a.extend(below_59)
    
    w_between_59_110 = map(lambda s: 'w '+str(s)+' st',range(60,110))
    e_between_59_110 = map(lambda s: 'e '+str(s)+' st',range(60,110))
    a.extend(w_between_59_110)
    a.extend(e_between_59_110)
    # print len(w_between_59_110),'between_59_110\tx2'
    
    #print w.street_num.max(),'west max number'
    #print e.street_num.max(),'east max number'
    
    w_between_109_139 = map(lambda s: 'w '+str(s)+' st',range(110,139))
    e_between_109_139 = map(lambda s: 'e '+str(s)+' st',range(110,139))
    between_109_139 = map(lambda s: str(s)+' st',range(110,139))
    a.extend(w_between_109_139)
    a.extend(e_between_109_139)
    a.extend(between_109_139)
    # print len(between_109_139),'between_109_139\tx3'
    
    w_above_138 = map(lambda s: 'w '+str(s)+' st',range(139,int(w.street_num.max())+1))
    above_138 = map(lambda s: str(s)+' st',range(139,int(w.street_num.max())+1))
    a.extend(w_above_138)
    a.extend(above_138)
    # print len(above_138),'above_138\t\tx2'
    
    avenues = map(lambda s: str(s)+' ave',range(1,13))
    a.extend(avenues)
    
    numbered_streets = pd.DataFrame({street_column:a}).reset_index(drop=True)
    # print len(a)
    # a.head()
    return numbered_streets


def parse_NYC_snd_datafile(fpath='',with_regex=True):

    from json import dumps as j_dumps
    from os.path import isfile as os_path_isfile

    f                                   =   open(src_fpath,'r')
    x                                   =   f.readlines()
    f.close(                                )


    print '\n',SND_NON_S_PATH,'\n',SND_S_PATH,'\n'

    # Characters Allowed:  [a-z0-9A-Z],[-&'/]

    # Borough:
        # 1 = MN
        # 2 = Bronx
        # 3 = Brooklyn
        # 4 = Queens
        # 5 = Staten Island

    ## GFT:
        # blank None of the below, e.g., either a name of a street that has no hyphenated house numbers
            # and no part of which is within
            # Edgewater Park, or a name of a tunnel, etc
        # A Addressable place name
        # B Name of bridge
        # C Business Improvement Districts
        # D Duplicate Address Pseudo-Street name (DAPS)
        # E Street is entirely within Edgewater Park
        # F Street is partially within Edgewater Park
        # G Non-Addressable Place name (NAP) of a complex
        # H All house numbers on this street are hyphenated
        # I Intersection Name
        # J Non-Physical Boundary Features
        # M Some house numbers on this street are hyphenated, some are not
        # N NAP of a 'stand-alone' geographic feature (not a complex
            # or a constituent entity of a complex)
        # O Shore Line
        # P Pseudo-street name (BEND, CITY LIMIT, DEAD END and their aliases)
        # R Rail line
        # S Front-truncated street name
        # T Tunnel
        # U Miscellaneous Structures
        # X NAP of a constituent entity of a complex Z Ramp

        ## ignore B,G,N,O,R,T
        ## watch H,M


    def get_snd_non_s(x):
        # non-type 'S' / size 34
        a = {
    #             'rec_type':x[0:1],
                'boro':x[1:2],                # (see "boro" below)
                'stname':x[2:34].strip(),               # full street name
                'primary_flag':x[34:35].strip(),        # P(=primary) or V(=non-primary)
                'principal_flag':x[35:36].strip(),      # F or S
                'boro':x[36:37].strip(),                # 1,2,3,4,5
                'sc5':x[36:42].strip(),
                'lgc':x[42:44].strip(),                 # Local Group Code
                'spv':x[44:47].strip(),                 # Spelling Variation
        #         filler = x[47:49]
                'numeric_ind':x[49:50].strip(),         # Numeric Name Indicator
                'GFT':x[50:51].strip(),                 # (see description above)
    #             'len_full_name':x[51:53].strip(),
                'full_stname':x[53:85].strip(),
                'min_SNL':x[85:87].strip(),
                'stn20':x[87:107].strip(),
                'ht_name_type_code':x[107:108].strip(), # blank or R(= roadbed), G(= generic), U(= undivided)
        #         filler = x[109:200]
            }
        return a

    def get_snd_s(x):
        a = {
    #             filler = x[0:1]           # always '1'
    #             'rectype':x[0:1],
                'boro':x[1:2].strip(),              # only 1 or 2 (MN and BX)
                'stname':x[2:34].strip(),           # front truncated name
        #         filler = x[34:49]         # P or V
                'numeric_ind':x[49:50].strip(),     # blank or N
                'GFT':x[50:51],             # always 'S'
    #             'len_full_name':x[51:53].strip(),
                'num_of_progens':x[53:54].strip(),  # either 1 or 2 ?
                'progen_word_1':x[54:55].strip(),   # E or W
                'progen_gft_1':x[55:56].strip(),
                'progen_b10sc_1':x[56:67].strip(),
                'sc5_1':x[56:62].strip(),
        #         filler = x[67:70]
                'progen_word_2':x[70:71].strip(),   # E or W
                'progen_gft_2':x[71:72].strip(),
                'progen_b10sc_2':x[72:83].strip(),
                'sc5_2':x[72:78].strip(),
        #         filler = x[83:86]
        #         filler = x[86:200]
            }
        return a

    non_s,s,xlen=[],[],len(x)

    for i in range(1,xlen):
        rec = re_sub(r'(\r\n)$',r'',x[i])
        if rec[34]=='P' or rec[34]=='V':    # non-'S'
            r = get_snd_non_s(rec)
            r['source_ln_num'] = i
            non_s.append(r)
        else:
            r = get_snd_s(rec)
            r['source_ln_num'] = i
            s.append(r)

    # print len(non_s),'rows of non-type S'
    # print len(s),'rows of S-type'
    # print xlen,'total rows in data'
    assert len(non_s)+len(s)==xlen-1

    # TESTING:
    # print x[1] # for non s-type
    # non_s[0]
    # --for s-type
    # print x[11]
    # s[0]

    p = j_dumps(non_s)
    df_non_s=pd.read_json(p)
    ns_cols = sorted(get_snd_non_s('').keys())
    df_non_s = df_non_s.ix[:,ns_cols]

    # -  Remove Blank Columns
    remove_cols = []
    # ---- PROVE THAT OK TO REMOVE 'min_SNL' b/c NO VALUES EXIST
    test_col='min_SNL'
    t=df_non_s[test_col].unique().tolist()
    assert True == (len(t)==1) == (t[0]=='')
    remove_cols.append(test_col)
    # ---- PROVE THAT OK TO REMOVE 'stn20' b/c NO VALUES EXIST
    test_col='stn20'
    t=df_non_s[test_col].unique().tolist()
    assert True == (len(t)==1) == (t[0]=='')
    remove_cols.append(test_col)
    # --
    df_non_s = df_non_s.drop(remove_cols,axis=1)



    print '\n',len(df_non_s),'non-S-Type records\n'
    # print df_non_s.head()
    assert False==os_path_isfile(SND_NON_S_PATH)
    df_non_s.to_csv(SND_NON_S_PATH)
    assert True==os_path_isfile(SND_NON_S_PATH)


    p = j_dumps(s)
    df_s=pd.read_json(p)
    s_cols = sorted(get_snd_s('').keys())
    df_s = df_s.ix[:,s_cols]
    l_funct = lambda s: 0 if len(str(s).strip())==0 else int(s)
    df_s['progen_b10sc_2'] = df_s.progen_b10sc_2.map(l_funct)
    df_s['sc5_2'] = df_s.sc5_2.map(l_funct)

    # -  Remove Blank Columns
    remove_cols = []
    # ---- PROVE THAT OK TO REMOVE 'min_SNL' b/c NO VALUES EXIST
    test_col='progen_gft_2'
    t=df_s[test_col].unique().tolist()
    assert True == (len(t)==1) == (t[0]=='')
    remove_cols.append(test_col)
    # --
    df_s = df_s.drop(remove_cols,axis=1)


    print '\n',len(df_s),'S-Type records\n'
    # print df_s.head()
    assert False==os_path_isfile(SND_S_PATH)
    df_s.to_csv(SND_S_PATH)
    assert True==os_path_isfile(SND_S_PATH)
    return 'success'

def load_parsed_snd_datafile_into_db(table_name='snd',drop_prev=True):
    py_path.append(os_path.join(os_environ['BD'],'html'))
    from scrape_vendors             import Scrape_Vendors,conn,cur,routing_eng
    SV                              =   Scrape_Vendors()
    T                               =   SV.T

    def push_first_part_to_sql(streets,table_name,drop_prev):
        """

            SOME OF THE ADJUSTMENT MADE WERE IN REGARD TO:
                --WEST 49 STREET
                --avenue b vs. b avenue
                --WEST 160 STREET
                --BENNETT AVENUE
                --WADSWORTH TERRACE
                --75 PARK TERRACE EAST
                --MARGINAL STREET
                --AVENUE OF THE AMER
                --8 LITTLE WEST 12 ST
                --74 PIKE SLIP

            Do anything about?
                CENTRAL PARK WEST -- Central Park W or Central Pk W
                NORTH END AVE -- N End Ave. or North End Ave.


            NEED 'cust_snd' FOR THE FOLLOWING

                PLCE --> PLACE		"WASHINGTON PLCE"
                S --> SOUTH ST
                W --> WEST ST
                FREDERICK DOUGLASS B --> F.D. BLVD

        """


        if drop_prev:
            conn.set_isolation_level(   0)
            cur.execute(                'drop table if exists %s;' % table_name)

        grps = streets.groupby('sc5')
        df_cols = ['primary_name','variation','full_variation']
        df = pd.DataFrame(columns=df_cols)
        for k,v in grps.groups.iteritems():
            t = grps.get_group(k)
            non_primary_idx = t[t.primary_flag!='P'].index.tolist()
            primary_idx = t[t.index.isin(non_primary_idx)==False].index.tolist()
            tdf = pd.DataFrame()
            tdf['variation'] = t.ix[non_primary_idx,'stname'].tolist()
            tdf['full_variation'] = t.ix[non_primary_idx,'full_stname'].tolist()
            tdf['primary_name'] = t.ix[primary_idx,'full_stname'].tolist()[0]
            tdf['sc5'] = t.ix[primary_idx,'sc5'].tolist()[0]
            assert t.ix[v,'sc5'].unique().tolist()
            df = df.append(tdf,ignore_index=True)

        df.to_sql(table_name,routing_eng,index=False)
        return True


    # I.  NON S-TYPE RECORDS
    d = pd.read_csv(SND_NON_S_PATH,index_col=0)
    drop_idx = d[d.boro!=1].index.tolist()
    d = d.drop(drop_idx,axis=0)

    #   1. PROVE ONLY MN STREETS ARE CONSIDERED
    assert len(d.boro.unique().tolist())==1
    assert d.boro.unique().tolist()[0]==1
    #   2. Remove non-essential Geographic Feature Types (GFT)
    remove_gft_features = ['B','C','J','O','R']
    rem_idx = d[d.GFT.isin(remove_gft_features)].index.tolist()
    d = d.drop(rem_idx,axis=0)
    assert len(d[d.GFT.isin(remove_gft_features)])==0
    #   3. PROVE ALL STREET NAMES ARE UPPER CASE
    d['stname'] = d['stname'].map(lambda s: s.upper())
    assert len(d[d.stname.str.match('[a-z]+')])==0
    #   4. Remove Roadbeds (Horizontal Typology Type Code (ht_name_type_code='R')
    rem_idx = d[d.ht_name_type_code=='R'].index.tolist()
    d = d.drop(rem_idx,axis=0)
    assert len(d[d.ht_name_type_code=='R'])==0



    # II. S-TYPE RECORDS
    dd = pd.read_csv(SND_S_PATH,index_col=0)
    drop_idx = dd[dd.boro!=1].index.tolist()
    dd = dd.drop(drop_idx,axis=0)


    #   1. PROVE ONLY MN STREETS ARE CONSIDERED
    assert len(dd.boro.unique().tolist())==1
    assert dd.boro.unique().tolist()[0]==1
    #   2. Remove non-essential Geographic Feature Types (GFT)
    remove_features = ['B','C','J','O','R']
    rem_idx = dd[dd.GFT.isin(['B','C','J','O','R'])].index.tolist()
    dd = dd.drop(rem_idx,axis=0)
    assert len(dd[dd.GFT.isin(['B','C','J','O','R'])])==0
    #   3. PROVE ALL STREET NAMES ARE UPPER CASE
    dd['stname'] = dd['stname'].map(lambda s: s.upper())
    assert len(dd[dd.stname.str.match('[a-z]+')])==0
    #   4. Remove non-essential Geographic Feature Types (GFT) from progenitors [progen_gft_1=='Z']
    remove_gft_features = ['Z']
    rem_idx = dd[dd.progen_gft_1=='Z'].index.tolist()
    dd = dd.drop(rem_idx,axis=0)
    assert len(dd[dd.progen_gft_1=='Z'])==0

    ##
    # START STREET DATAFRAME
    ##

    # 1. Take First Part of Data from non-type-S records
    streets = d.copy()
    # PROVE ALL NAP'S WERE REMOVED
    rem_idx = streets[streets.GFT.isin(['N','X'])].index.tolist()
    streets = streets.drop(rem_idx,axis=0)
    assert len(streets[streets.GFT.isin(['N','X'])])==0

    # print len(dd),'initial rows from S-Type records'
    # 2. Supplement with Data from type-S records
    uniq_street_sc5 = streets.sc5.unique().tolist()
    nd = dd[(dd.sc5_1.isin(uniq_street_sc5))|(dd.sc5_1.isin(uniq_street_sc5))].index.tolist()
    ndf = dd.ix[nd,:].copy()
    # print len(ndf),'remaining rows from S-Type records after taking only matching sc5'


    # -  Remove Blank Columns from Supplemental Data
    remove_cols = []
    # ---- PROVE THAT OK TO REMOVE 'progen_gft_1' b/c NO VALUES EXIST
    test_col='progen_gft_1'
    t=ndf[test_col].unique().tolist()
    assert True == (len(t)==1) == (np.float(t[0]).is_integer()==False)
    remove_cols.append(test_col)
    # --
    ndf = ndf.drop(remove_cols,axis=1)

    # print len(ndf),'remaining rows before push'
    ##
    # PUSH TO SQL
    ##

    push_first_part_to_sql(streets,table_name,drop_prev)
    if drop_prev:
        conn.set_isolation_level(       0)
        cur.execute(                    'drop table if exists %(tmp_tbl)s;' % {'tmp_tbl' :   table_name+'_tmp'})
    ndf.to_sql(                     table_name+'_tmp',routing_eng,index=False)

    return
    # PG SQL CMDS...
    cmd =   """

            alter table snd
                add column east boolean default false,
                add column south boolean default false,
                add column west boolean default false,
                add column north boolean default false,
                add column sc5_2 bigint,
                add column stname_grp text[];

            -- 276 distinct sc5_1 in _tmp
            -- 221 rows for below (276 without regex exclusions)

            update snd _orig set stname_grp = name_grp
            from

            (select array_agg(t.stname) name_grp,f2.s_sc5 s_sc5
                from
                    (select array_agg(distinct a.variation) orig_variations from snd a) as f3,
                    snd_tmp t,
                    (select distinct s.sc5_1 s_sc5 from snd_tmp s) as f2
                where t.sc5_1 = f2.s_sc5
                and not (orig_variations && array[t.stname] )
                and not (t.stname ilike '%roadbed%' or t.stname ilike '%EXTENSION%'
                    or t.stname ilike '%PEDESTRIAN%' or t.stname ilike '%SIDE HW%' )

                group by f2.s_sc5) as f1
            where s_sc5 = _orig.sc5::bigint;

            -- 454 rows in snd with non-null stname_grp

            insert into snd (variation,primary_name,sc5)
            select variation,primary_name,sc5
            from
                (select distinct unnest(n.stname_grp) variation,
                    n.primary_name primary_name,
                    n.sc5 sc5 from snd n) as f1,

                (select array_agg(full_variation) all_full_varies,
                    array_agg(variation) all_varies,
                    array_agg(primary_name) all_primaries from snd t) as f2
            where not (all_full_varies && array[variation] OR all_varies && array[variation] OR all_primaries && array[variation]);

            -- ASSERT -- res==True
            --select all_vars=uniq_vars res
            --from
            --    (select count(n1.variation) all_vars from snd n1 where n1.variation is not null or n1.variation !='') as f1,
            --    (select count(distinct n2.variation) uniq_vars from snd n2 where n2.variation is not null or n2.variation !='') as f2;

            update snd n set east = true
            from
                (select t.progen_word_1 t_progen_word_1,
                    t.progen_word_2 t_progen_word_2,
                    t.sc5_1 t_sc5_1,
                    t.sc5_2 t_sc5_2
                from snd_tmp t) as f1
            where ( (n.sc5 = t_sc5_1 or n.sc5 = t_sc5_2) OR  (n.sc5_2 = t_sc5_1 or n.sc5_2 = t_sc5_2) )
            and (t_progen_word_1 = 'E' or t_progen_word_2 = 'E');


            update snd n set west = true
            from
                (select t.progen_word_1 t_progen_word_1,
                    t.progen_word_2 t_progen_word_2,
                    t.sc5_1 t_sc5_1,
                    t.sc5_2 t_sc5_2
                from snd_tmp t) as f1
            where ( (n.sc5 = t_sc5_1 or n.sc5 = t_sc5_2) OR  (n.sc5_2 = t_sc5_1 or n.sc5_2 = t_sc5_2) )
            and (t_progen_word_1 = 'W' or t_progen_word_2 = 'W');

            -- ASSERT -- len({below}) == 0
            --select progen_word_1 from snd_tmp where progen_word_1 ilike 'w';

            -- ASSERT -- len({below}) == 0
            --select progen_word_2 from snd_tmp where progen_word_2 ilike 'e';


            update snd set primary_name = regexp_replace(primary_name,
                '^(EAST|WEST)([\s]+)([0-9]+)\s(.*)$','\\1 \\3 \\4','g');
            update snd set full_variation = regexp_replace(full_variation,
                '^(EAST|WEST)([\s]+)([0-9]+)\s(.*)$','\\1 \\3 \\4','g');
            update snd set variation = regexp_replace(variation,
                '^(EAST|WEST)([\s]+)([0-9]+)\s(.*)$','\\1 \\3 \\4','g');
            update snd set full_variation = regexp_replace(full_variation,
                '^(TRANSVRS|CPE|CPW|DOUGLASS|RIIS|RISS|NY|PATH|VLADECK|NEW)([\s]+)([0-9]+)\s(.*)$','\\1 \\3 \\4','g');
            update snd set variation = regexp_replace(variation,
                '^(TRANSVRS|CPE|CPW|DOUGLASS|RIIS|RISS|NY|PATH|VLADECK|NEW)([\s]+)([0-9]+)\s(.*)$','\\1 \\3 \\4','g');

            update snd set primary_name = 'FDR DRIVE' where primary_name = 'F D R DRIVE';

            -- ASSERT -- len({below}) == 0
            --select count(*)=0 res from snd where variation!=full_variation;
            alter table snd drop column if exists full_variation;

            --PROVE ALL STREETNAMES AND STREET IDS ARE FOUND IN 'snd'
            -- ASSERT -- res==True
            --select count(*)=0 res from
            --    snd_tmp t,
            --    (select array_agg(n.sc5) all_sc5 from snd n) as f1,
            --    (select array_agg(n2.sc5_2) all_sc5_2 from snd n2) as f2,
            --    (select array_agg(n3.variation) all_names from snd n3) as f3
            --where NOT ( t.sc5_1::bigint = ANY (all_sc5) OR t.sc5_1::bigint = ANY (all_sc5_2) )
            --and NOT ( t.sc5_2::bigint = ANY (all_sc5) OR t.sc5_2::bigint = ANY (all_sc5_2) )
            --and NOT ( t.stname = ANY (all_names) );
            drop table if exists snd_tmp;

            -- ASSERT
            --select count(distinct sc5_2)=0 res from snd
            alter table snd drop column sc5_2;


            update snd set last_updated = 'now'::timestamp with time zone;

            update snd s set primary_name = regexp_replace(s.primary_name,
                '([a-zA-Z0-9])[\s\s]+([a-zA-Z0-9]*)','\\1 \\2','g')

            drop table if exists tmp_snd;

            insert into snd (variation,sc5,west,east)
            select distinct on (s1.primary_name) s1.primary_name variation,s1.sc5 sc5,s1.west west,s1.east east
            from
                snd s1,
                (select array_agg(s2.variation) all_variations from snd s2) as f1
            where not s1.primary_name = ANY (all_variations);

            --PROVE THAT ALL stname_grp NAMES ARE IN VARIATION COLUMN
            --select count(*)=0 res from
            --    (select unnest(s.stname_grp) all_grp_names from snd s where s.stname_grp is not null) as f1,
            --    (select array_agg(n3.variation) all_names from snd n3) as f3
            --where NOT ( all_grp_names = ANY (all_names) );
            alter table snd drop column stname_grp;

            alter table snd add column tmp bigint;
            update snd set tmp = sc5::bigint;
            alter table snd drop column sc5;
            alter table snd rename column tmp to sc5;

            -- ASSERT


            """
    conn.set_isolation_level(           0)
    cur.execute(                        cmd)

    d = pd.read_sql("select * from snd",routing_eng)
    d = d.sort('primary_name').reset_index(drop=True)
    l_funct = lambda s: 0 if len(str(s).strip())==0 else int(s)
    d['sc5']=d.sc5.map(l_funct)


    cols = ['pattern','repl','_flags']
    ndf = pd.DataFrame(columns=cols)
    grp = d.groupby('primary_name')
    for k,v in grp.groups.iteritems():
        patt = '('+' | '.join(d.ix[v,'variation'].tolist()) + ')'
        ndf = ndf.append(dict(zip(cols,[patt,k,'g'])),ignore_index=True)

    ndf['repl'] = ndf.repl.str.replace(r'([a-zA-Z0-9]*)([\s\s]+)([a-zA-Z0-9]*)',r'\g<1> \g<3>')
    ndf.to_sql('tmp_snd',routing_eng,index=False)

    a="""

        select s.variation,s.primary_name
        from snd s,(select array_agg(t.address) all_addr from pluto p where p.geom is null) as f1
        where s.variation = ANY (all_addr);

        select sl_addr
        from
        (select array_agg(s.variation) all_variations from snd s) as f1,
        (select sl.address sl_addr from seamless sl where geom is null) as f2
        where sl_addr = ANY (all_variations);

    """

    # LOTS OF COMMANDS SHOULD BE HERE (FROM TAIL PART OF LONGSTRING ABOVE)
    # PROVE THAT TABLE IS IN ORIGINAL CONDITION
    saved_col_type_d_snd = {u'east': u'boolean',
                             u'last_updated': u'timestamp with time zone',
                             u'primary_name': u'text',
                             u'sc5': u'bigint',
                             u'uid': u'integer',
                             u'variation': u'text',
                             u'west': u'boolean'}
    x=pd.read_sql("""   select column_name, data_type
                        from INFORMATION_SCHEMA.COLUMNS
                        where table_name = 'snd'""",routing_eng)
    col_type_d = dict(zip(x.column_name.tolist(),x.data_type.tolist()))
    assert col_type_d==saved_col_type_d_snd

    return

class NYC_Tables:
    def __init__(self):
        py_path.append(                     os_path.join(os_environ['BD'],'html'))
        from scrape_vendors         import Scrape_Vendors,conn,cur,routing_eng
        SV                              =   Scrape_Vendors()
        self.SV                         =   SV
        self.T                          =   SV.T
        self.conn                       =   conn
        self.cur                        =   cur
        self.routing_eng                =   routing_eng


    def prep_data(self,data_type,data_set,purpose,args=None):
        """
        This is a custom function for preparing data in a particular way.

        Uses:

            df = prep_data(data_type='db',data_set='seamless',purpose='get_bldg_street_idx')

            df = prep_data(data_type='db',data_set='mnv',purpose='get_bldg_street_idx')

            df = prep_data(data_type='db',data_set='yelp',purpose='google_geocode')


        """
        py_path.append(os_path.join(os_environ['BD'],'geolocation'))
        from f_vendor_postgre       import get_bldg_street_idx
        from f_postgres             import clean_street_names
        from pygeocoder             import Geocoder
        from time                   import sleep            as delay
        conn                        =   self.conn
        cur                         =   self.cur
        routing_eng                 =   self.routing_eng

        def format_db(db,purpose,args):

            # ------------------
            # ------------------
            if   (db=='seamless' or db=='seamless_geom_error'):
                T = {'db_tbl'     : db,
                     'id_col'     :'vend_id',
                     'vend_name'  :'vend_name',
                     'address_col':'address',
                     'zip_col'    :'zipcode',
                    }
            elif (db=='yelp' or db=='yelp_geom_error'):
                T = {'db_tbl'     : db,
                     'id_col'     :'gid',
                     'vend_name'  :'vend_name',
                     'address_col':'address',
                     'zip_col'    :'postal_code',
                        }
            elif db=='mnv':
                T = {'db_tbl'     : db,
                     'id_col'     :'id',
                     'vend_name'  :'vend_name',
                     'address_col':'address',
                     'zip_col'    :'zipcode',
                        }
            # ------------------
            # ------------------

            if purpose=='google_geocode':
                cmd = """
                        select %(id_col)s id,%(vend_name)s vend_name,%(address_col)s address,%(zip_col)s zipcode
                        from %(db_tbl)s
                        where address is not null
                        and (char_length(bbl::text)!=10 or bbl is null)
                      """%T
                df = pd.read_sql(cmd,self.routing_eng)
                return df,T

            if purpose=='get_bldg_street_idx':
                cmd = """
                        select %(id_col)s id,%(address_col)s address,%(zip_col)s zipcode
                        from %(db_tbl)s
                        where address is not null
                        and (bbl::text='NaN' or bbl is null or char_length(bbl::text)<10)
                      """%T
                df = pd.read_sql(cmd,self.routing_eng)
                # df = clean_street_names(df,'address','address')
                self.SV.SF.clean_street_names(df,'address','address')
                df['address'] = df.address.map(lambda s: s.decode('ascii','ignore').encode('utf-8','ignore'))
                df['bldg_num'] = df.address.map(lambda s: s.split(' ')[0])
                df['clean_bldg_num'] = df.bldg_num.map(lambda s: None if ''==''.join([it for it in str(s) if str(s).isdigit()])
                                                      else int(''.join([it for it in str(s) if str(s).isdigit()])) )
                df = df[df.clean_bldg_num.map(lambda s: True if str(s)[0].isdigit() else False)].reset_index(drop=True)
                df['bldg_street'] = df.address.map(lambda s: ' '.join(s.split(' ')[1:]))
                df['clean_bldg_num'] = df.clean_bldg_num.map(int)
                df['zipcode'] = df.zipcode.map(int)
                df['addr_set'] = map(lambda s: ' '.join(map(str,s.tolist())),df.ix[:,['clean_bldg_num','bldg_street']].as_matrix())
                df.rename(columns={'clean_bldg_num':'addr_num',
                                  'bldg_street':'addr_street'},inplace=True)
                return df,T


        if data_type=='db':
            return format_db(data_set,purpose,args)
    def add_geom_using_address(self,working_table):
        """

        Usages:

            working_table = 'seamless' | 'yelp' | 'seamless_geom_error' | 'mnv'

        """

        py_path.append(os_path.join(os_environ['BD'],'geolocation'))
        from f_vendor_postgre       import get_bldg_street_idx

        conn                        =   self.conn
        cur                         =   self.cur
        routing_eng                 =   self.routing_eng

        # 1. load NYC TABLE -- Libraries & F(x)s
        # 2. format data for and run 'get_bldg_street_idx' function
        df,T = self.prep_data(data_type='db',data_set=working_table,purpose='get_bldg_street_idx')
        recognized,not_recog,to_check_later = get_bldg_street_idx(   df,
                                                                     addr_set_col='addr_set',
                                                                     addr_num_col='addr_num',
                                                                     addr_street_col='addr_street',
                                                                     zipcode_col='zipcode',
                                                                     show_info=False  )
        addr_tot = pd.read_sql('select count(*) u from %s'%working_table,self.routing_eng).u[0]
        addr_uniq = len(df.addr_set.unique().tolist())
        addr_recog = len(recognized)
        addr_unrecog = len(not_recog)
        addr_TCL = len(to_check_later)

        # 3. push data to table 'tmp'
        recognized['addr_set'] = map(lambda s: ' '.join(map(str,s.tolist())),
                                  recognized.ix[:,['addr_num','addr_street']].as_matrix())
        z=pd.merge(df,recognized.ix[:,['addr_set','bldg_street_idx']],on='addr_set',how='outer')
        conn.set_isolation_level(0)
        cur.execute('drop table if exists tmp')
        z.to_sql('tmp',self.routing_eng)
        conn.set_isolation_level(0)
        cur.execute("""
        alter table tmp drop column if exists "index";
        alter table tmp add column gid serial primary key;
        update tmp set gid = nextval(pg_get_serial_sequence('tmp','gid'));
        """)
        tmp_rows = len(z)

        # 4. add necessary columns if not exist to $working_table
        cmd = """   select column_name cols, data_type
                    from INFORMATION_SCHEMA.COLUMNS
                    where table_name = '%s'"""%working_table
        tbl_info = pd.read_sql(cmd,self.routing_eng)
        tbl_cols = map(str,tbl_info.cols.tolist())
        cols_needed = {'camis':'integer',
                       'bbl':'integer',
                       'lot_cnt':'integer DEFAULT 1',
                       'geom':'geometry(Point,4326)'}
        for k,v in cols_needed.iteritems():
            if tbl_cols.count(k)==0:
                conn.set_isolation_level(0)
                cur.execute('alter table %(tbl)s add column %(k)s %(v)s'%{'tbl':working_table,'k':k,'v':v})

        # 5. update table $working_table and delete table 'tmp'
        conn.set_isolation_level(0)
        cur.execute("""

        update %(db_tbl)s s set bbl = l.bbl
            from tmp t,lot_pts l
            where
                char_length(l.bbl::text)>=10
                and t.bldg_street_idx::text != 'NaN'
                and t.addr_num::text != 'NaN'
                and t.id=s.%(id_col)s
                and (
                    to_number(concat(t.bldg_street_idx,'.',to_char(t.addr_num,'00000')),'00000.00000')
                    between l.lot_idx_start and l.lot_idx_end
                    );

        update %(db_tbl)s s set lot_cnt = (select count(l.bbl) from %(db_tbl)s l
                                         where s.bbl is not null
                                         and l.bbl is not null
                                         and l.bbl=s.bbl);

        update %(db_tbl)s s set geom = pc.geom
            from pluto_centroids pc
            where
                pc.bbl = s.bbl
                and pc.bbl is not null;

        drop table if exists tmp;

        """%T)

        no_geoms = pd.read_sql('select count(*) c from %(db_tbl)s where geom is null'%T,self.routing_eng).c[0]

        # 6. provide result info
        print '\tTABLE:',working_table
        print addr_tot,'\t\ttotal addresses in %s'%working_table
        print addr_uniq,'\t\tunique addresses in %s'%working_table
        print addr_recog,'\t\t\trecognized'
        print addr_unrecog,'\t\t\tnot_recog'
        print addr_TCL,'\t\t\tto_check_later'
        print tmp_rows,'\t\trows in tmp'
        print no_geoms,'\t\trows without geoms'
    def add_geom_using_geocoding(self,working_tbl,print_gps=True):
        """

        Usages:

             add_geom_using_geocoding(self,working_tbl=('seamless' | 'yelp' | 'mnv'))

        """


        tbl                         =   working_tbl
        print_gps                   =   False

        conn                        =   self.conn
        cur                         =   self.cur
        routing_eng                 =   self.routing_eng

        df,T = self.prep_data(data_type='db',data_set=tbl,purpose='google_geocode')
        addr_start_cnt = len(df)
        df['zipcode'] = df.zipcode.map(lambda s: '' if str(s).lower()=='nan' else str(int(s)))
        df['chk_addr'] = df.ix[:,['address','zipcode']].apply(lambda s: str(s[0]+', New York, NY, '+str(s[1])).strip(),axis=1)
        uniq_addr_start_cnt = len(df.chk_addr.unique().tolist())

        # get google geocode results
        all_chk_addr = df.chk_addr.tolist()
        uniq_addr = pd.DataFrame({'addr':all_chk_addr}).addr.unique().tolist()
        uniq_addr_dict = dict(zip(uniq_addr,range(len(uniq_addr))))
        _iter = pd.Series(uniq_addr).iterkv()

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

        d = pd.DataFrame(y)
        d['iter_keys'] = z
        d['lat'],d['lon'] = zip(*d.geometry.map(lambda s: (s['location']['lat'],s['location']['lng'])))
        tbl_dict = dict(zip(df.chk_addr.tolist(),df.id.tolist()))
        d['%s_id'%tbl] = d.orig_addr.map(tbl_dict)

        # push orig_df to pgSQL
        d['geometry'] = d.geometry.map(str)
        d['res_data'] = d.res_data.map(str)
        conn.set_isolation_level(0)
        cur.execute( """drop table if exists tmp;""")
        d.to_sql('tmp',self.routing_eng)
        conn.set_isolation_level(0)
        cur.execute("""
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
        conn.set_isolation_level(0)
        cur.execute(cmd)

        # provide result info
        uniq_search_queries = len(d['%s_id'%tbl].unique().tolist())
        search_query_res_cnt = len(d)
        single_res_cnt = len(d[d.res_i==-1])
        remaining_no_addr = pd.read_sql('select count(*) c from %s where geom is null'%tbl,self.routing_eng).c[0]

        print '\tTABLE:',tbl
        print addr_start_cnt,'\t total addresses in %s'%tbl
        print uniq_addr_start_cnt,'\t unique addresses in %s'%tbl
        print uniq_search_queries,'\t # of unique Search Queries'
        print search_query_res_cnt,'\t # of Search Query Results'
        print single_res_cnt,'\t # of Query Results with a Single Result'
        print remaining_no_addr,'\t # of Vendors in %s still without geom'%tbl