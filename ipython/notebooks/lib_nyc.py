
# coding: utf-8

## TODO:

### Turn Stile Data:

#### GOAL -- For Dates A to B and Times C to D, how many people per station?

# 1. consolidate scp's per remote/booth
# 
#     Thoughts:
#         - each scp has its own range of timestamps and register values
#         - some scp.s have multiple datasets for same time period
#         - timestamps exists for all times of the day
#         
#     Method:
#         - create new table with:
#             - date column
#             - 24 columns for each hour filled with register-change values
#                 - need 24 or just use single time col?
#             - index # from sub_turn_stiles
#             
#         
# 
# 2. consolidate remote/booth per station

# In[ ]:

get_ipython().run_cell_magic(u'sql', u'postgres@routing', u'select distinct extract(hour from datetime1) s\nfrom sub_turn_stiles\norder by s')


# In[ ]:

### Using PostgresSQL Server [ db1.public.routing ]:

from sys import path as sys_path
from re import search as re_search # re_search('pattern','string')
from re import sub as re_sub  # re_sub('pattern','repl','string','count')

import pandas as pd
pd.set_option('expand_frame_repr',False)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width',180)
np = pd.np
np.set_printoptions(linewidth=400,threshold=np.nan)
import geopandas as gd
from types import NoneType
from time import sleep as delay
from sqlalchemy import create_engine
from logging import getLogger
from logging import INFO as logging_info
getLogger('sqlalchemy.dialects.postgresql').setLevel(logging_info)

engine = create_engine(r'postgresql://postgres:postgres@localhost:8800/routing',
                       encoding='utf-8',
                       echo=False)

get_ipython().magic(u'load_ext sql')
get_ipython().magic(u'sql postgresql://postgres:postgres@localhost/routing')


# In[ ]:

### add restaurant data
import requests, zipfile, StringIO
from f_postgres import geoparse
z = requests.get('https://data.cityofnewyork.us/download/4vkw-7nck/ZIP')
r = zipfile.ZipFile(StringIO.StringIO(z.content))
v = pd.read_csv(r.open('WebExtract.txt'))
v.columns = [ str(it).lower() for it in v.columns.tolist() ]

m = v[v.boro==1].copy()
m['inspdate'] = pd.to_datetime(m.inspdate)
m = m.sort('inspdate',ascending=False).reset_index(drop=True)
z = m.groupby('camis')
grps = z.groups.keys()
takeCols = ['dba','cuisinecode','building','street','zipcode','phone','inspdate'] # and 'camis' which is the grps[i]
mv = pd.DataFrame(columns=['camis']+takeCols)
g_cnt = len(grps)
for i in range(g_cnt):
    vend_id = grps[i]
    x = z.get_group(vend_id).reset_index(drop=True).ix[0,takeCols]
    x['camis'] = vend_id
    mv = mv.append(x)
mv = geoparse(mv,'dba','clean_name')
mv = geoparse(mv,'street','clean_street')
mv['dba'] = mv.dba.map(lambda s: s.decode('ascii','ignore').encode('utf-8','ignore'))
engine.execute('drop table if exists mn_vendors')
mv.to_sql('mn_vendors',engine,index=False)
engine.execute("""
    alter table mn_vendors add column id serial;
    update mn_vendors set id = nextval(pg_get_serial_sequence('mn_vendors','id'));
    alter table mn_vendors add primary key (id);
    """)
engine.execute("""alter table mn_vendors add column recog_street boolean;
                  update mn_vendors set recog_street = False;""")
engine.execute("""  update mn_vendors set recog_street = True
                    where exists (
                        select 1 from address_idx a
                        where a.street = clean_street
                    )""")


# In[ ]:

### add subway entrances to map
url = 'http://web.mta.info/developers/data/nyct/subway/StationEntrances.csv'
s = pd.read_csv(url)
s.columns = [it.lower().strip() for it in s.columns.tolist()]
engine.execute('drop table if exists sub_stat_entr')
s.to_sql('sub_stat_entr',engine)
engine.execute('alter table sub_stat_entr add column geom geometry(Point,4326)')
engine.execute("""UPDATE sub_stat_entr set geom = ST_SetSRID(ST_MakePoint(station_longitude,station_latitude),4326)""")
engine.execute(""" DELETE FROM sub_stat_entr 
                WHERE NOT (geom && (
                    SELECT ST_Buffer(ST_ConvexHull((ST_Collect(f.the_geom))), .0005) as geom 
                    FROM ( SELECT *, (ST_Dump(geom)).geom As the_geom 
                    FROM pluto) As f))""")
engine.execute("""
    alter table sub_stat_entr add column id serial;
    update sub_stat_entr set index = nextval(pg_get_serial_sequence('sub_stat_entr','id'));
    alter table sub_stat_entr add primary key (id);
    """)


# In[ ]:

### add subway stops to map, add turn stile data to subway stops
import requests, zipfile, StringIO
r = requests.get('http://web.mta.info/developers/data/nyct/subway/google_transit.zip')
z = zipfile.ZipFile(StringIO.StringIO(r.content))
sub_stops = pd.read_csv(z.open('stops.txt'))
sub_stops.to_sql('sub_stops',engine)
engine.execute('alter table sub_stops add column geom geometry(Point,4326)')
engine.execute("""UPDATE sub_stops set geom = ST_SetSRID(ST_MakePoint(stop_lon,stop_lat),4326)""")
engine.execute(""" DELETE FROM sub_stops 
                WHERE NOT (geom && (
                    SELECT ST_Buffer(ST_ConvexHull((ST_Collect(f.the_geom))), .0005) as geom 
                    FROM ( SELECT *, (ST_Dump(geom)).geom As the_geom 
                    FROM pluto) As f))""")
engine.execute("""
    alter table sub_stops add column id serial;
    update sub_stops set index = nextval(pg_get_serial_sequence('sub_stops','id'));
    alter table sub_stops add primary key (id);
    """)
# NOTE:  also then deleted more by hand


# In[ ]:

### add turn_stile_key to pgsql
ts_key = pd.read_excel('http://web.mta.info/developers/resources/nyct/turnstile/Remote-Booth-Station.xls')
ts_key.columns = [str(it).lower().replace(' ','_') for it in ts_key.columns.tolist()]
ts_key['line_name'] = ts_key['line_name'].map(lambda s: ''.join(sorted([str(it) for it in s])) if type(s)!=int else str(s))
ts_key['clean'] = ts_key.station.map(lambda s: s.lower())
engine.execute("drop table if exists ts_key")
ts_key.to_sql('ts_key',engine)


# In[ ]:

### add turn stile data to pgsql
# General Source for Turn Stiles: http://web.mta.info/developers/turnstile.html
#     - field description: http://web.mta.info/developers/resources/nyct/turnstile/ts_Field%20Description.txt
#     - data key: http://web.mta.info/developers/resources/nyct/turnstile/Remote-Booth-Station.xls
#         --> this is the provides the Remote Unit/Control Area/Station Name Key
# Need coords for "UNIT"
# Remote and Station Name here:
#      'http://web.mta.info/developers/resources/nyct/turnstile/Remote-Booth-Station.xls'
# Station Names and Coords here:
#      'http://web.mta.info/developers/data/nyct/subway/StationEntrances.csv'
#     - Relevant stations were added to pgsql as 'sub_stat_entr'


cols = ['C/A','UNIT','SCP','DATE1','TIME1','DESC1','ENTRIES1','EXITS1',
        'DATE2','TIME2','DESC2','ENTRIES2','EXITS2','DATE3','TIME3','DESC3','ENTRIES3',
        'EXITS3','DATE4','TIME4','DESC4','ENTRIES4','EXITS4','DATE5','TIME5','DESC5',
        'ENTRIES5','EXITS5','DATE6','TIME6','DESC6','ENTRIES6',
        'EXITS6','DATE7','TIME7','DESC7','ENTRIES7','EXITS7','DATE8',
        'TIME8','DESC8','ENTRIES8','EXITS8']
cols = [str(it).lower().replace('/','_') for it in cols]
url = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_141004.txt'
p = pd.read_csv(url,names=cols)
idx = p[p.unit.str.contains('R')==False].index
p = p.drop(idx,axis=0).reset_index(drop=True)
# ts_key = pd.read_excel('http://web.mta.info/developers/resources/nyct/turnstile/Remote-Booth-Station.xls')
# ts_key.columns = [str(it).lower().replace(' ','_') for it in ts_key.columns.tolist()]

dropCols = []
for it in cols:
    if it.find('exit')==0 or it.find('entries')==0:
        p[it] = p[it].map(float)
    if it.find('date')==0:
        date_pt,time_pt,datetime_pt = it,'time'+it[4:],'datetime'+it[4:]
        p[datetime_pt] = pd.to_datetime(p[date_pt] + ' ' + p[time_pt],format='%m-%d-%y %H:%M:%S',coerce=False)
        p[datetime_pt] = p[datetime_pt].map(lambda s: None if str(s)=='NaT' else str(s))
        dropCols.extend([date_pt,time_pt])
p = p.drop(dropCols,axis=1)
cols = p.columns.tolist()

# END GOAL conform 'station_names' to 'mn_stations'
mn_stations = pd.read_sql("""select * from sub_stat_entr""",engine)

# Limit NYC key to MN
mn_div_list = mn_stations.division.unique().tolist()
ts_key = ts_key.drop(ts_key[ts_key.division.isin(mn_div_list)==False].index,axis=0)

# Create and Sort Route List for each station
mn_cols = mn_stations.columns.tolist()
s_pt,e_pt = mn_cols.index('route_1'),mn_cols.index('route_11')+1
mn_stations['all_lines'] = mn_stations.ix[:,s_pt:e_pt].apply(lambda s: ''.join([str(it) for it in s if str(it)!='NaN']).replace('nan','').replace('.0',''),axis=1)
mn_stations['all_lines'] = mn_stations.all_lines.map(lambda s: ''.join(sorted(s)))
# ts_key['line_name'] = ts_key['line_name'].map(lambda s: ''.join(sorted([str(it) for it in s])) if type(s)!=int else str(s))

# clean up many but small differences between station names
mn_stations['clean'] = mn_stations.station_name.map(lambda s: s.lower())
# ts_key['clean'] = ts_key.station.map(lambda s: s.lower())
repl_dict = {   r'(1st|first)'          :r'1',
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
                r'\s(street)'           :r' st',
                r'\s(square)'           :r' sq',
                r'\s(center)'           :r' ctr',
                r'\s(av)':r' ave'}
for k,v in repl_dict.iteritems():
    mn_stations['clean'] = mn_stations.clean.str.replace(k,v)
    
repl_dict = {   r'\Aunion sq':r'14 st-union sq',
                r'cathedral parkway-110 st':r'110 st-cathedrl',
                r'163 st - amsterdam ave':r'163 st-amsterdm',
                r'81 st - museum of natural history':r'81 st-museum',
                r'47-50 sts rockefeller ctr':r'47-50 st-rock',
                r'137 st-city college':r'137 st-city col',
                r'broadway-lafayette st':r'broadway/lafay',
                r'west 4 st':r'w 4 st-wash sq' ,
                r'110 st-central park north':r'110 st-cpn',
                r'116 st-columbia university':r'116 st-columbia',
                r'168 st - washington heights':r'168 st-broadway',
#                 r'168 st-broadway - washington heights':r'168 st-broadway',
                r'49 st':r'49 st-7 ave',
                r'168 st\Z':r'168 st-broadway',
                r'59 st-columbus circle':r'59 st-columbus',
                r'66 st-lincoln ctr':r'66 st-lincoln',
                r'68 st-hunter college':r'68st-hunter col',
                # r'astor pl':'astor place',
                r'brooklyn bridge-city hall':r'brooklyn bridge',
                r'dyckman st-200 st':r'dyckman-200 st',
                r'grand central-42 st':r'42 st-grd cntrl',
                r'inwood - 207 st':r'inwood-207 st',
                r'lexington av-53 st':r'lexington-53 st',
                r'prince st':r"prince st-b'way",
                r'\Atimes sq\Z':r'42 st-times sq',
                r'times sq-42 st':r'42 st-times sq',
                r'van cortlandt park-242 st':r'242 st',
                r'marble hill-225 st':r'225 st',
                r'lexington ave-53 st':r'lexington-53 st',
                r'harlem-148 st':r'148 st-lenox',
                r'\Agrand central\Z':r'42 st-grd cntrl',
                r'\Acanal st (ul)\Z':r'canal st',}
for k,v in repl_dict.iteritems():
    mn_stations['clean'] = mn_stations.clean.str.replace(k,v)

station_names = ts_key.clean.tolist()
#print len(mn_stations[mn_stations.clean.isin(station_names)==False]), 'stations not mapped'
# mn_stations[mn_stations.clean.isin(station_names)==False].ix[:,['division','line','station_name','all_lines','clean']].sort('clean')
# mn_stations.head()

# push to [ sub_stat_entr,ts_key,p(turn stiles) ] to pgsql for comparison and unificiation
engine.execute('drop table if exists sub_stat_entr')
engine.execute('drop table if exists ts_key')
engine.execute('drop table if exists sub_turn_stiles')
delay(1)

mn_stations.drop(['id','index'],axis=1).to_sql('sub_stat_entr',engine)
engine.execute("""
    alter table sub_stat_entr add column id serial;
    update sub_stat_entr set index = nextval(pg_get_serial_sequence('sub_stat_entr','id'));
    alter table sub_stat_entr add primary key (id);
    """)
engine.execute("""UPDATE sub_stat_entr set geom = ST_SetSRID(ST_MakePoint(station_longitude,station_latitude),4326)""")

# ts_key.to_sql('ts_key',engine)
engine.execute("""
    alter table ts_key add column lat double precision;
    alter table ts_key add column lon double precision;
    alter table ts_key add column id serial;
    update ts_key set index = nextval(pg_get_serial_sequence('ts_key','id'));
    alter table ts_key add primary key (id);
    """)

p.to_sql('sub_turn_stiles',engine)
engine.execute("""
    alter table sub_turn_stiles add column station text;
    alter table sub_turn_stiles add column lat double precision;
    alter table sub_turn_stiles add column lon double precision;
    alter table sub_turn_stiles add column id serial;
    update sub_turn_stiles set index = nextval(pg_get_serial_sequence('sub_turn_stiles','id'));
    alter table sub_turn_stiles add primary key (id);
    """)

# 1. Copy coords from station_entrances to turnstile_key
engine.execute( """
                UPDATE ts_key t
                SET lat = s.station_latitude,lon = s.station_longitude
                FROM sub_stat_entr s
                WHERE s.clean=t.clean
                AND s.all_lines=t.line_name;
                """)
#print pd.read_sql('select count(*) c from ts_key where lon is null',engine).c[0],'null'
#print pd.read_sql('select count(*) c from ts_key where lon is not null',engine).c[0],'not null'

# 2. Copy matching ts_key table data to turn_stiles table
engine.execute( """
                UPDATE sub_turn_stiles
                SET lat = t.lat,lon=t.lon,station=t.station
                FROM ts_key t
                WHERE t.remote = unit
                AND t.booth = c_a;
                """)
engine.execute('alter table sub_turn_stiles add column geom geometry(Point,4326)')
engine.execute("""UPDATE sub_turn_stiles set geom = ST_SetSRID(ST_MakePoint(lon,lat),4326)""")

# 3. Attempt to match leftovers (non-matching) b/t ts_key/sub_stat_entr using wildcards
leftovers = pd.read_sql("select * from ts_key where lon is null and division = any(array['IRT','IND','BMT'])",engine)
for i in range(0,len(leftovers)):
    row = leftovers.ix[i,:]
    chk = row['clean'].find('-')
    if chk != -1:
        a,b = '%%'+str(row['clean'].split('-')[0])+'%%',row['line_name']
        tmp = pd.read_sql(  """ 
                            SELECT station_latitude lat,station_longitude lon
                            FROM sub_stat_entr s
                            WHERE s.clean ilike '%s'
                            AND s.all_lines='%s';
                            """%(a,b),engine)
        if (len(tmp.lat.unique())==len(tmp.lat.unique())==1):
            a,b,c = tmp.lat[0],tmp.lon[0],row['id']
            engine.execute( """
                                UPDATE ts_key set lat=%f,lon=%f
                                WHERE id = %d
                            """%(a,b,c),engine)
            
# 4. Attempt to match leftover by:
        # starting with lines,division, 
            # if one result go with it, 
            # else if only one result and it's a partial match, go with it?
leftovers = pd.read_sql("select * from ts_key where lon is null and division = any(array['IRT','IND','BMT'])",engine)
for i in range(0,len(leftovers)):
    row = leftovers.ix[i,:]
    a,b,c = '%%'+str(row['clean'].split('-')[0])+'%%',row['line_name'],row['division']
    tmp = pd.read_sql(  """ 
                        SELECT station_latitude lat,station_longitude lon,clean
                        FROM sub_stat_entr s
                        WHERE s.division='%s'
                        AND s.all_lines='%s';
                        """%(c,b),engine)
    if (len(tmp.lat.unique())==len(tmp.lat.unique())==1):
        a,b,c = tmp.lat[0],tmp.lon[0],row['id']
        engine.execute( """
                            UPDATE ts_key set lat=%f,lon=%f
                            WHERE id = %d
                        """%(a,b,c),engine)
    else:
        z=tmp[tmp.clean.str.contains(a)]
        if (len(z.lat.unique())==len(z.lat.unique())==1):
            a,b,c = tmp.lat[0],tmp.lon[0],row['id']
            engine.execute( """
                                UPDATE ts_key set lat=%f,lon=%f
                                WHERE id = %d
                            """%(a,b,c),engine)


# In[ ]:

# TURN STILE CONT'D convert text to timestamp

engine.execute("""  

    DROP TABLE if exists tmp;

    CREATE TABLE tmp (
        gid serial primary key,
        datetime1 timestamp with time zone,
        datetime2 timestamp with time zone,
        datetime3 timestamp with time zone,
        datetime4 timestamp with time zone,
        datetime5 timestamp with time zone,
        datetime6 timestamp with time zone,
        datetime7 timestamp with time zone,
        datetime8 timestamp with time zone
        );

    UPDATE tmp SET gid = nextval(pg_get_serial_sequence('tmp','gid'));

    INSERT INTO tmp (
        datetime1,
        datetime2,
        datetime3,
        datetime4,
        datetime5,
        datetime6,
        datetime7,
        datetime8)
    SELECT 
        to_timestamp(s.datetime1,'YYYY-MM-DD HH24:MI:SS'),
        to_timestamp(s.datetime2,'YYYY-MM-DD HH24:MI:SS'),
        to_timestamp(s.datetime3,'YYYY-MM-DD HH24:MI:SS'),
        to_timestamp(s.datetime4,'YYYY-MM-DD HH24:MI:SS'),
        to_timestamp(s.datetime5,'YYYY-MM-DD HH24:MI:SS'),
        to_timestamp(s.datetime6,'YYYY-MM-DD HH24:MI:SS'),
        to_timestamp(s.datetime7,'YYYY-MM-DD HH24:MI:SS'),
        to_timestamp(s.datetime8,'YYYY-MM-DD HH24:MI:SS')
    FROM sub_turn_stiles s;

    ALTER TABLE sub_turn_stiles 
    DROP COLUMN datetime1,
    DROP COLUMN datetime2,
    DROP COLUMN datetime3,
    DROP COLUMN datetime4,
    DROP COLUMN datetime5,
    DROP COLUMN datetime6,
    DROP COLUMN datetime7,
    DROP COLUMN datetime8,
    ADD COLUMN datetime1 timestamp with time zone,
    ADD COLUMN datetime2 timestamp with time zone,
    ADD COLUMN datetime3 timestamp with time zone,
    ADD COLUMN datetime4 timestamp with time zone,
    ADD COLUMN datetime5 timestamp with time zone,
    ADD COLUMN datetime6 timestamp with time zone,
    ADD COLUMN datetime7 timestamp with time zone,
    ADD COLUMN datetime8 timestamp with time zone;

    UPDATE sub_turn_stiles s
    SET 
        datetime1 = t.datetime1,
        datetime2 = t.datetime2,
        datetime3 = t.datetime3,
        datetime4 = t.datetime4,
        datetime5 = t.datetime5,
        datetime6 = t.datetime6,
        datetime7 = t.datetime7,
        datetime8 = t.datetime8
    FROM tmp t
    where t.gid = s.id;

               """)


# In[ ]:

# TURN STILE CONT'D calc. register differences
engine.execute("""
alter table sub_turn_stiles 
add column out1 double precision,
add column out2 double precision,
add column out3 double precision,
add column out4 double precision,
add column out5 double precision,
add column out6 double precision,
add column out7 double precision,
add column in1 double precision,
add column in2 double precision,
add column in3 double precision,
add column in4 double precision,
add column in5 double precision,
add column in6 double precision,
add column in7 double precision;


update sub_turn_stiles
set out1 = exits2-exits1
where exits1 != 'NaN'::float
and exits2 != 'NaN'::float;

update sub_turn_stiles
set out2 = exits3-exits2
where exits2 != 'NaN'::float
and exits3 != 'NaN'::float;

update sub_turn_stiles
set out3 = exits4-exits3
where exits3 != 'NaN'::float
and exits4 != 'NaN'::float;

update sub_turn_stiles
set out4 = exits5-exits4
where exits4 != 'NaN'::float
and exits5 != 'NaN'::float;

update sub_turn_stiles
set out5 = exits6-exits5
where exits5 != 'NaN'::float
and exits6 != 'NaN'::float;

update sub_turn_stiles
set out6 = exits7-exits6
where exits6 != 'NaN'::float
and exits7 != 'NaN'::float;

update sub_turn_stiles
set out7 = exits8-exits7
where exits7 != 'NaN'::float
and exits8 != 'NaN'::float;


update sub_turn_stiles
set in1 = entries2-entries1
where entries1 != 'NaN'::float
and entries2 != 'NaN'::float;

update sub_turn_stiles
set in2 = entries3-entries2
where entries2 != 'NaN'::float
and entries3 != 'NaN'::float;

update sub_turn_stiles
set in3 = entries4-entries3
where entries3 != 'NaN'::float
and entries4 != 'NaN'::float;

update sub_turn_stiles
set in4 = entries5-entries4
where entries4 != 'NaN'::float
and entries5 != 'NaN'::float;

update sub_turn_stiles
set in5 = entries6-entries5
where entries5 != 'NaN'::float
and entries6 != 'NaN'::float;

update sub_turn_stiles
set in6 = entries7-entries6
where entries6 != 'NaN'::float
and entries7 != 'NaN'::float;

update sub_turn_stiles
set in7 = entries8-entries7
where entries7 != 'NaN'::float
and entries8 != 'NaN'::float;


alter table sub_turn_stiles 
    add column in_all double precision,
    add column out_all double precision;
update sub_turn_stiles
set in_all = (select sum(s) from unnest(array[in1,in2,in3,in4,in5,in6,in7]) s);
update sub_turn_stiles
set out_all = (select sum(s) from unnest(array[out1,out2,out3,out4,out5,out6,out7]) s);
""")


# In[ ]:

# NEED to consolidate turn_stile data


# In[ ]:

# turn_stile data with missing station name -- SMALL ADJUSTMENTS NEEDED
cmd=""" select distinct unit,c_a from sub_turn_stiles 
        where station is null order by unit;"""
pd.read_sql(cmd,engine)


# In[ ]:

# turn_stile data analysis:

# general data used herein
datetime_cols = ['datetime'+str(i) for i in range(1,9)]
desc_cols = ['desc'+str(i) for i in range(1,9)]
entry_cols = ['entries'+str(i) for i in range(1,9)]
exit_cols = ['exits'+str(i) for i in range(1,9)]
in_cols = ['in'+str(i) for i in range(1,9)]
out_cols = ['out'+str(i) for i in range(1,9)]
agg_cols = ['in_all','out_all']
other_cols = ['index','lat','lon','id','geom']

# 1. this shows there are multiple entries per station, i.e., multiple turn stiles
cmd =   """
        select * from sub_turn_stiles 
        where out_all is not null
        and station = '34 ST-HERALD SQ'
        AND extract(hour from datetime1) = 4
        AND extract(day from datetime1) = 29
        order by out_all desc;
        """

# 2. this shows there are multiple rows even when {c_a,unit,scp,datetime1} are same
cmd =   """
        select * from sub_turn_stiles 
        where out_all is not null
        and station = '34 ST-HERALD SQ'
        AND scp = '00-00-00'
        order by c_a,unit,datetime1 asc;
        """
dropCols = desc_cols + entry_cols + exit_cols + in_cols + out_cols + other_cols


# In[ ]:

# 3. this shows the door is open for people leaving during rush hour... (see datetime6-7)
#        and possibly explains why multiple rows
cmd =   """
        select * from sub_turn_stiles 
        where out_all is not null
        and station = '34 ST-HERALD SQ'
        AND scp = '00-00-00'
        AND datetime1 = '2014-09-28 09:00:00-04:00';
        """
# dropCols = desc_cols + entry_cols + exit_cols + in_cols + out_cols + other_cols
pd.read_sql(cmd,engine)#.drop(dropCols,axis=1)

