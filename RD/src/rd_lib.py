# import sys
# reload(sys)
# sys.setdefaultencoding('UTF8')
from sys import path as py_path
from random import randint,random
from collections import OrderedDict as OD
from itertools import combinations
from time import time
from types import NoneType
from os import getcwd
this_cwd = getcwd()+'/'

from numpy.lib.scimath import sqrt
import pandas as pd
pd.set_option('expand_frame_repr',False)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width',180)
np = pd.np
np.set_printoptions(linewidth=200,threshold=np.nan)
import geopandas as gd
from os.path import isfile

#from os.path import abspath
#py_path.append(abspath(this_cwd+'../../geolocation'))
#from pg_fxs import geom_inside_street_box,make_column_primary_serial_key
from sqlalchemy import create_engine
engine = create_engine(r'postgresql://postgres:postgres@192.168.2.50:8800/routing',
                       encoding='utf-8',
                       echo=False)

# engine = create_engine(r'postgresql://postgres:postgres@localhost/routing',
#                        encoding='utf-8',
#                        echo=False)

way_t,vert_t,vert_g = 'lws','lws_vertices_pgr','the_geom'

ord_q_cols_types    =  OD([ ('order_time'        ,float),
                            ('deliv_id'          ,int),
                            ('dg_id'             ,int),
                            ('dg_node'           ,int),
                            ('travel_time_to_loc',float),
                            ('start_node'        ,int),
                            ('start_time'        ,float),
                            ('travel_time'       ,float),
                            ('end_time'          ,float),
                            ('end_node'          ,int),
                            ('total_order_time'  ,float),
                            ('status'            ,object),
                        ])
MODEL_order_q = pd.DataFrame( columns=ord_q_cols_types.keys())
for k,v in ord_q_cols_types.iteritems():
    MODEL_order_q[k]=MODEL_order_q[k].astype(v)


dg_q_cols_types     = OD([  ('dg_id'            ,int),
                            ('pta'              ,int),
                            ('ptb'              ,int),
                            ('pta-t'            ,float),
                            ('ptb-t'            ,float),
                            ('deliv_id'         ,int),
                            ('mock_pt'          ,int)
                        ])
MODEL_dg_q  = pd.DataFrame(columns=dg_q_cols_types.keys())
for k,v in dg_q_cols_types.iteritems():
    MODEL_dg_q[k] = MODEL_dg_q[k].astype(v)


dg_pool_cols_types  = OD([  ('dg_id'            ,int),
                            ('dg_node'          ,int),
                            ('dest_node'        ,int),
                            ('total_delivered'  ,int),
                            ('current_deliveries',int)
                        ])
MODEL_dg_pool  = pd.DataFrame(columns=dg_pool_cols_types.keys())
for k,v in dg_pool_cols_types.iteritems():
    MODEL_dg_pool[k] = MODEL_dg_pool[k].astype(v)
