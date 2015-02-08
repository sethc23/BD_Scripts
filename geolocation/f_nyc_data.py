import pandas as pd
from re import sub as re_sub  # re_sub('pattern','repl','string','count')
from re import search as re_search # re_search('pattern','string')
from json import dumps as j_dumps

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


SND_NON_S_PATH = '/Users/admin/Projects/GIS/table_data/snd14Bcow_non_s_recs.csv'
SND_S_PATH = '/Users/admin/Projects/GIS/table_data/snd14Bcow_s_recs.csv'

def parse_NYC_snd_datafile(fpath=''):

    f = open(fpath,'r')
    x=f.readlines()
    f.close()
    
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
    df_non_s.to_csv(SND_NON_S_PATH)
    # df_non_s.ix[:300,:]

    p = j_dumps(s)
    df_s=pd.read_json(p)
    df_s = df_s.ix[:,s_cols]
    print '\n',len(df_s),'S-Type records\n'
    print df_s.head()
    df_s.to_csv(SND_S_PATH)
    # df_s.ix[:300,:]
    return 'success'