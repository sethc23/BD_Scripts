
from os                             import environ          as os_environ
from uuid                           import uuid4            as get_guid
from os                             import path             as os_path
from sys                            import path             as py_path
from os.path                        import isfile           as os_path_isfile

import                                  pandas              as pd
from re                             import sub              as re_sub  # re_sub('pattern','repl','string','count')
from re                             import search           as re_search # re_search('pattern','string')
from json                           import dumps            as j_dumps


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


def parse_NYC_snd_datafile(fpath=''):

    f                                   =   open(fpath,'r')
    x                                   =   f.readlines()
    f.close(                                )

    base_path                           =   fpath.rstrip('.txt')
    SND_NON_S_PATH                      =   base_path + '_non_s_recs.csv'
    SND_S_PATH                          =   base_path + '_s_recs.csv'

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
    #             'boro':x[1:2],                # (see "boro" below)
                'stname':x[2:34],               # full street name
                'primary_flag':x[34:35],        # P(=primary) or V(=non-primary)
                'principal_flag':x[35:36],      # F or S
                'boro':x[36:37],                # 1,2,3,4,5
                'sc5':x[37:42],
                'lgc':x[42:44],                 # Local Group Code
                'spv':x[44:47],                 # Spelling Variation
        #         filler = x[47:49]
                'numeric_ind':x[49:50],         # Numeric Name Indicator
                'GFT':x[50:51],                 # (see description above)
                'len_full_name':x[51:53],
                'full_stname':x[53:85],
                'min_SNL':x[85:87],
                'stn20':x[87:107],
                'ht_name_type_code':x[107:108], # blank or R(= roadbed), G(= generic), U(= undivided)
        #         filler = x[109:200]
            }
        return a

    def get_snd_s(x):
        a = {
    #             filler = x[0:1]           # always '1'
    #             'rectype':x[0:1],            
                'boro':x[1:2],              # only 1 or 2 (MN and BX)
                'stname':x[2:34],           # front truncated name
        #         filler = x[34:49]         # P or V    
                'numeric_ind':x[49:50],     # blank or N
                'GFT':x[50:51],             # always 'S'    
                'len_full_name':x[51:53],
                'num_of_progens':x[53:54],  # either 1 or 2 ?
                'progen_word_1':x[54:55],   # E or W
                'progen_gft_1':x[55:56],
                'progen_b10sc_1':x[56:67],
        #         filler = x[67:70]
                'progen_word_2':x[70:71],   # E or W
                'progen_gft_2':x[71:72],
                'progen_b10sc_2':x[72:83],
        #         filler = x[83:86]
        #         filler = x[86:200]
            }
        return a

    ns_cols = ['stname','primary_flag','principal_flag','boro','sc5','lgc','spv',
               'numeric_ind','GFT','len_full_name','full_stname','min_SNL','stn20',
               'ht_name_type_code']

    s_cols = ['boro','stname','numeric_ind','GFT','len_full_name','num_of_progens',
              'progen_word_1','progen_gft_1','progen_b10sc_1',  
              'progen_word_2','progen_gft_2','progen_b10sc_2']

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

    print xlen,'rows in data'

    p = j_dumps(non_s)
    df_non_s=pd.read_json(p)
    df_non_s = df_non_s.ix[:,ns_cols]
    print '\n',len(df_non_s),'non-S-Type records\n'
    print df_non_s.head()
    assert False==os_path_isfile(SND_NON_S_PATH)
    df_non_s.to_csv(SND_NON_S_PATH)
    # df_non_s.ix[:300,:]

    p = j_dumps(s)
    df_s=pd.read_json(p)
    df_s = df_s.ix[:,s_cols]
    print '\n',len(df_s),'S-Type records\n'
    print df_s.head()
    assert False==os_path_isfile(SND_S_PATH)
    df_s.to_csv(SND_S_PATH)
    # df_s.ix[:300,:]
    return 'success'

def load_parsed_snd_datafile_into_db():
    py_path.append(os_path.join(os_environ['BD'],'html'))
    from scrape_vendors import *
    SV = Scrape_Vendors()
    T                               =   SV.T

    d = pd.read_csv(SND_NON_S_PATH,index_col=0)
    d = d[d.boro==1].drop(['len_full_name','min_SNL','stn20'],axis=1)
    for it in d.columns.tolist():
        d[it] = d[it].map(lambda s: s if type(s)!=str else s.strip())

    # 1. PROVE ONLY MN STREETS ARE CONSIDERED
    assert len(d.boro.unique().tolist())==1
    assert d.boro.unique().tolist()[0]==1
    # 2. Remove non-essential Geographic Feature Types (GFT)
    remove_gft_features = ['B','C','J','O','R']
    rem_idx = d[d.GFT.isin(remove_gft_features)].index.tolist()
    d = d.drop(rem_idx,axis=0)
    assert len(d[d.GFT.isin(remove_gft_features)])==0
    # 3. PROVE ALL STREET NAMES ARE UPPER CASE
    d['stname'] = d['stname'].map(lambda s: s.upper())
    assert len(d[d.stname.str.match('[a-z]+')])==0
    # 4. Remove Roadbeds (Horizontal Typology Type Code (ht_name_type_code='R')
    rem_idx = d[d.ht_name_type_code=='R'].index.tolist()
    d = d.drop(rem_idx,axis=0)
    assert len(d[d.ht_name_type_code=='R'])==0

    dd = pd.read_csv(SND_S_PATH,index_col=0)
    l_funct = lambda s: 0 if len(str(s).strip())==0 else int(s)
    dd['progen_b10sc_1'] = dd.progen_b10sc_1.map(l_funct)
    dd['progen_b10sc_1'] = dd.progen_b10sc_1.astype(int)
    dd['progen_b10sc_2'] = dd.progen_b10sc_2.map(l_funct)
    dd['progen_b10sc_2'] = dd.progen_b10sc_2.astype(int)
    dd['sc5_1'] = dd.progen_b10sc_1.map(lambda s: 0 if len(str(s).strip())==0
                                        else 0 if str(s)[1:6]=='' else int(str(s)[1:6]))
    dd['sc5_2'] = dd.progen_b10sc_2.map(lambda s: 0 if len(str(s).strip())==0
                                        else 0 if str(s)[1:6]=='' else int(str(s)[1:6]))
    dd['sc7_1'] = dd.progen_b10sc_1.map(lambda s: 0 if len(str(s).strip())==0
                                        else 0 if str(s)[1:8]=='' else int(str(s)[1:8]))
    dd['sc7_2'] = dd.progen_b10sc_2.map(lambda s: 0 if len(str(s).strip())==0
                                        else 0 if str(s)[1:8]=='' else int(str(s)[1:8]))
    dd['scL3_1'] = dd.progen_b10sc_1.map(lambda s: 0 if len(str(s).strip())==0
                                         else 0 if str(s)[8:]=='' else int(str(s)[8:]))
    dd['scL3_2'] = dd.progen_b10sc_2.map(lambda s: 0 if len(str(s).strip())==0
                                         else 0 if str(s)[8:]=='' else int(str(s)[8:]))

    dd = dd[dd.boro==1].drop(['numeric_ind','len_full_name'],axis=1)
    for it in dd.columns.tolist():
        dd[it] = dd[it].map(lambda s: s if type(s)!=str else s.strip())

    # 1. PROVE ONLY MN STREETS ARE CONSIDERED
    assert len(dd.boro.unique().tolist())==1
    assert dd.boro.unique().tolist()[0]==1
    # 2. Remove non-essential Geographic Feature Types (GFT)
    remove_features = ['B','C','J','O','R']
    rem_idx = dd[dd.GFT.isin(['B','C','J','O','R'])].index.tolist()
    dd = dd.drop(rem_idx,axis=0)
    assert len(dd[dd.GFT.isin(['B','C','J','O','R'])])==0
    # 3. PROVE ALL STREET NAMES ARE UPPER CASE
    dd['stname'] = dd['stname'].map(lambda s: s.upper())
    assert len(dd[dd.stname.str.match('[a-z]+')])==0

    ##
    # START STREET DATAFRAME
    ##

    streets = d.copy()
    # PROVE ALL NAP'S WERE REMOVED
    rem_idx = streets[streets.GFT.isin(['N','X'])].index.tolist()
    streets = streets.drop(rem_idx,axis=0)
    assert len(streets[streets.GFT.isin(['N','X'])])==0

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
        df = df.append(tdf,ignore_index=True)

    df.to_sql('nyc_snd',routing_eng,index=False)