import geopandas as gd
import pandas as pd
from sqlalchemy import create_engine
from re import sub as re_sub  # re_sub('pattern','repl','string','count')
from sys import path as sys_path

from f_postgres import clean_street_names,routing_eng #,ST_PREFIX_DICT,ST_SUFFIX_DICT
#from f_postgres import update_address_idx_matches

# engine = create_engine(r'postgresql://postgres:postgres@192.168.3.52:8800/routing')
# BASE_SAVE_PATH = '/Users/admin/Projects/GIS/table_data/'

def find_address_idx_matches(addr_list):
    cmd = ('select * from address_idx '+
           'where addr = any(array'+str(addr_list)+')')
    return pd.read_sql_query(cmd,routing_eng)

def explode_addresses(df='cols = addr,norm_addr'):
    
    pre_re_s = re_search_string = r'^('+"|".join(ST_PREFIX_DICT.values())+r')'
    alp  = a_less_prefix = pd.DataFrame({'norm_addr_body':df.norm_addr.map(lambda s: re_sub(pre_re_s,'',s.strip()).strip()),
                                        'orig_addr':df.addr.tolist()})
    
    suf_re_s = re_search_string = r'('+r'|'.join(ST_SUFFIX_DICT.values())+r')$'
    als  = a_less_suffix = pd.DataFrame({'norm_addr_body':df.norm_addr.map(lambda s: re_sub(suf_re_s,'',s.strip()).strip()),
                                        'orig_addr':df.addr.tolist()})
    
    alps = a_less_prefix_less_suffix = pd.DataFrame({'norm_addr_body':alp.norm_addr_body.map(lambda s: re_sub(suf_re_s,'',s.strip()).strip()),
                                                    'orig_addr':df.addr.tolist()})
    
    all_a = alp.append(als,ignore_index=True).append(alps,ignore_index=True).reset_index(drop=True)
    all_a = all_a[all_a.norm_addr_body!='']
    j,k = all_a.norm_addr_body.tolist(),df.norm_addr.tolist()
    all_unique_addr_list = dict(zip(j+k,range(0,len(j)+len(k)))).keys()
    all_a['cnt'] = all_a.norm_addr_body.map(lambda s: all_unique_addr_list.count(s))
    
    x = all_a[all_a.cnt==1].reset_index(drop=True)
    x.drop(['cnt'],axis=1,inplace=True)
    return x

def get_show_info(r,df,show_info=False):
    if show_info==True: print len(r),'remaining addresses\t\t',str(round(float((len(df)-len(r))/float(len(df)))*100,2))+'% overall recognition\n'

def get_addr_body(r,from_label='norm_addr'):
    pre_re_s = re_search_string = r'^('+"|".join(ST_PREFIX_DICT.values())+r')\s'
    suf_re_s = re_search_string = r'\s('+r'|'.join(ST_SUFFIX_DICT.values())+r')$'
    r['body'] = r[from_label].map(lambda s: re_sub(pre_re_s,r'',s).strip()
                                  if ST_SUFFIX_DICT.values().count(  # this extra is to prevent a "st" result
                                                                   re_sub(pre_re_s,r'',s).strip()
                                                                   ) == 0 else ''
                                  ).map(lambda s: re_sub(suf_re_s,r'',s).strip()
                                        if ST_SUFFIX_DICT.values().count(  # this extra is to prevent a "w" result
                                                                         re_sub(suf_re_s,r'',s).strip()
                                                                         ) == 0 else s)
    return r

def update_with_idx_matches(ur,r,dbm='database_matches',input_addr_col='from_label',result_idx_col='idx'):
    addr_idx_map = dict(zip(dbm[input_addr_col].tolist(),dbm[result_idx_col].tolist()))
    dbm_addr = addr_idx_map.keys()
    recog_idx = r[r[input_addr_col].isin(dbm_addr)==True].index
    tmp = r.ix[recog_idx,:]
    tmp['bldg_street_idx'] = tmp[input_addr_col].map(addr_idx_map)
    if type(ur) is str:
        ur = tmp
        r = remaining_addr = r[r.index.isin(recog_idx)==False].reset_index(drop=True)
    else:
        ur = ur.append(tmp,ignore_index=True)
        r = r[r.index.isin(recog_idx)==False].reset_index(drop=True)
    return ur,r

def match_levenshtein_series(ur='user_recognized_addr',r='remaining_addr',df='source_df',from_label='body',show_info=False):
    #  levenshtein(text source, text target, int insert_cost, int delete_cost, int substitution_cost)
    
    if show_info==True: print '\n\n\t-- SEARCH lev-variant1 --\n'
    T = { '1':from_label, '2':'idx', '3':str(r[from_label].tolist()) }
    cmd = """
        SELECT %(1)s,a.bldg_street_idx %(2)s,a.street,levenshtein(a.street,%(1)s,1,0,4)
        from address_idx a,unnest(array[%(3)s]) %(1)s
        where soundex(a.street) = any(select soundex(x) from regexp_split_to_table(%(1)s,E'\s+') x)
        and a.one_word is true
        order by levenshtein(a.street,%(1)s,1,0,4)
        """.replace('\n',' ') % T
    dbm = db_matches = pd.read_sql_query(cmd,routing_eng)
    dbm = dbm[dbm.levenshtein<=3]
    ur,r = update_with_idx_matches(ur,r,dbm,input_addr_col=T['1'],result_idx_col=T['2'])
    get_show_info(r,df,show_info)
    
    if show_info==True: print '\n\n\t-- SEARCH lev-variant2 --\n'
    T = { '1':from_label, '2':'idx', '3':str(r[from_label].tolist()) }
    cmd = """
        SELECT %(1)s,a.bldg_street_idx %(2)s,a.street,levenshtein(a.street,%(1)s,1,1,4) lev,difference(a.street,%(1)s) diff
        from address_idx a
        inner join unnest(array[%(3)s]) %(1)s
        on levenshtein(a.street,%(1)s,1,1,4)<=1
        and a.one_word is true
        order by a.street
        """.replace('\n',' ') % T
    dbm = db_matches = pd.read_sql_query(cmd,routing_eng)
    ur,r = update_with_idx_matches(ur,r,dbm,input_addr_col=T['1'],result_idx_col=T['2'])
    get_show_info(r,df,show_info)
    
    if show_info==True: print '\n\n\t-- SEARCH lev-variant3 --\n'
    T = { '1':from_label, '2':'idx', '3':str(r[from_label].tolist()) }
    cmd = """SELECT a.bldg_street_idx %(2)s,a.street,levenshtein(a.street,%(1)s,1,0,4) lev,%(1)s
        from address_idx a
        inner join unnest(array[%(3)s]) %(1)s
        on levenshtein(a.street,%(1)s,1,1,4)<=1""".replace('\n',' ') % T
    dbm = db_matches = pd.read_sql_query(cmd,routing_eng)
    ur,r = update_with_idx_matches(ur,r,dbm,input_addr_col=T['1'],result_idx_col=T['2'])
    get_show_info(r,df,show_info)
    
    if show_info==True: print '\n\n\t-- SEARCH lev-variant4 --\n'
    T = { '1':from_label, '2':'idx', '3':str(r[from_label].tolist()) }
    cmd = """SELECT %(1)s,a.bldg_street_idx %(2)s,a.street
        from address_idx a
        inner join unnest(array[%(3)s]) %(1)s
        on street ~* %(1)s
        """.replace('\n',' ') % T
    dbm = db_matches = pd.read_sql_query(cmd,routing_eng)
    ur,r = update_with_idx_matches(ur,r,dbm,input_addr_col=T['1'],result_idx_col=T['2'])
    get_show_info(r,df,show_info)

    return ur,r

def match_simple_regex(ur='user_recognized_addr',r='remaining_addr',df='source_df',from_label='norm_addr',show_info=False):
    T = {   '1' : from_label,
            '2' : str(r[from_label].map(lambda s: str(s)).tolist())
        }
    cmd = """
        SELECT %(1)s,a.bldg_street_idx idx,a.street
        from address_idx a
        inner join unnest(array[%(2)s]) %(1)s
        on a.street ~* %(1)s
        where one_word is true
        """.replace('\n',' ') % T
    dbm = db_matches = pd.read_sql_query(cmd,routing_eng)
    ur,r = update_with_idx_matches(ur,r,dbm,input_addr_col=from_label,result_idx_col='idx')
    get_show_info(r,df,show_info)
    return ur,r

def match_simple(ur='user_recognized_addr',r='remaining_addr',df='source_df',from_label='addr_street',show_info=False):
    if type(r) is str: x=df
    else: x=r
    T = { '1':from_label, '2':'idx', '3':x[from_label].map(str).tolist() }
    cmd = """
        SELECT %(1)s,a.bldg_street_idx %(2)s,a.street
        from address_idx a
        inner join unnest(array[%(3)s]) %(1)s
        on a.street = %(1)s
        """.replace('\n',' ') % T
    dbm = db_matches = pd.read_sql_query(cmd,routing_eng)
    ur,r = update_with_idx_matches(ur,x,dbm,input_addr_col=T['1'],result_idx_col=T['2'])
    get_show_info(r,x,show_info)
    return ur,r

def pagc_normalize_address(r,from_label='full_address',to_label='norm_addr'):
    
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
    T = {'arr':str(r[from_label].map(str).tolist()),
         'to_label':to_label}
    cmd = """
        select r,lower(pprint_addy(pagc_normalize_address(r))) %(to_label)s
        from unnest(array[%(arr)s]) r
        """.replace('\n','') % T

    n = pd.read_sql_query(cmd,routing_eng)
    n_map = dict(zip(n.r.tolist(),n[to_label].tolist()))
    r[to_label+'_num'] = r[from_label].map(lambda s: n_map[s].split(',')[0].split(' ')[0])
    r[to_label] = r[from_label].map(lambda s: str(' '.join(n_map[s].split(',')[0].split(' ')[1:])))
    return r

def get_bldg_street_idx(df,addr_set_col='addr_set',addr_num_col='addr_num',addr_street_col='addr_street',zipcode_col='zipcode',show_info=False):
    # cols = [u'seam_id', u'addr_num', u'addr_street', u'zipcode']

    #df.rename(columns={addr_num_col:'addr_num',addr_street_col:'addr_street'},inplace=True)

    all_cols = df.columns.tolist()
    num_col_i = all_cols.index(addr_num_col)
    str_col_i = all_cols.index(addr_street_col)
    zip_col_i = all_cols.index(zipcode_col)
    
    # ur = user/comp recognized
    # r = remaining_addr
    # TCL = to-check-later ... the addr.s not normalized
    
    uniq_idx = dict(zip(df[addr_set_col].tolist(),df.index.tolist()))
    d = df[df.index.isin(uniq_idx.values())].reset_index(drop=True)
    d['full_address'] = d.apply(lambda s: str(s[num_col_i])+' '+str(s[str_col_i])+', New York, NY '+str(s[zip_col_i]),axis=1)
    d['norm_addr_num'] = d.index.map(lambda s: None)
    d['norm_addr'] = d.index.map(lambda s: None)
    d['body'] = d.index.map(lambda s: None)
    d['bldg_street_idx'] = d.index.map(lambda s: None)
    if show_info==True: print len(d),'total uniq addresses\n',d.head()

    if show_info==True: print '\n\n\t-- SEARCH #1 AFTER geoparse --\n'
    ur,r = match_simple(ur='',r='',df=d,from_label=addr_street_col)
    if show_info==True: print len(r),'remaining addresses\t\t',str(round(float((len(d)-len(r))/float(len(d)))*100,2))+'% overall recognition\n'
    if show_info==True: print len(d),'=',len(r)+len(ur),'True?'
    
    r = pagc_normalize_address(r,from_label='full_address',to_label='norm_addr')
    r = clean_street_names(r,'norm_addr','norm_addr')
    
    ### getting base ("body") of address, if address='e 45 st', body='45'
    # r = get_addr_body(r,from_label='norm_addr')
    
    ### create seperate list for addresses with malformed norm_addr
    TCL = to_check_later = r[r[addr_num_col].map(lambda s: len(re_sub(r'^[0-9]+$',r'',str(s)))!=0)].copy()
    r = r[r.index.isin(TCL.index)==False].reset_index(drop=True)
    TCL = TCL.reset_index(drop=True)
    if show_info==True: print '\n',len(TCL),'issue addresses ("TCL")\n'
    
    if show_info==True: print '\n\n\n\t-- SEARCH #2 ./PAGC normalization,body --\n'
    # ur,r = match_simple(ur=ur,r=r,df='',from_label='body')
    ur,r = match_simple(ur=ur,r=r,df='',from_label='norm_addr')
    if show_info==True: print len(r),'remaining addresses\t\t',str(round(float((len(d)-len(r))/float(len(d)))*100,2))+'% overall recognition\n'   
    
    if show_info==True: print '\n\n\n\t-- SEARCH #3 ./match simple regex --\n'
    ur,r = match_simple_regex(ur,r,from_label='norm_addr')
    if show_info==True: print len(r),'remaining addresses\t\t',str(round(float((len(d)-len(r))/float(len(d)))*100,2))+'% overall recognition\n'

    # ur,r = match_levenshtein_series(ur=ur,r=r,df=d,from_label='body',show_info=False)
    ur,r = match_levenshtein_series(ur=ur,r=r,df=d,from_label='norm_addr',show_info=False)

    
    return ur,r,TCL