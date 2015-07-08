# add encoding?
#   see SL_previously_closed_vendors

from ipdb import set_trace as i_trace
#; i_trace()


class PP_Functions:

    def __init__(self,_parent):
        self.SV                             =   _parent
        self.T                              =   _parent.T
        self.SF                             =   self
        from HTML_API                           import getTagsByAttr,google,safe_url,getSoup
        all_imports                         =   locals().keys()
        for k in all_imports:
            if not self.T.has_key(k):
                self.T.update(                  {k                      :   eval(k) })
        from webpage_scrape                     import scraper
        self.br                             =   scraper(self.T.browser_type).browser
        self.logged_in                      =   self.login()

    def login(self):
        url                                 =   'http://previewbostonrealty.com/admin/login.php'
        self.br.open_page(                      url)
        uname                               =   self.br.window.find_element_by_name("ap_username")
        if uname.is_displayed():
            uname.send_keys('schase')
            self.br.window.find_element_by_name("ap_password").send_keys('B*_Realty')
            self.br.window.find_element_by_name("Submit").click()
        return True

    def _clean_cols(self,pd_table_from_html,key_items):
        A                                   =   pd_table_from_html
        A.columns                           =   map(lambda s: '_'+s.lower().replace(' ','_'),A.columns.tolist())
        A['_keys']                          =   map(lambda t: '' if t.img is None else t.img.get('src'),key_items)
        A['_property_id']                   =   A._property_id.map(int)
        A['_photos']                        =   A._photos.map(lambda s: '' if s=='No Photos' else s)
        A['_rent']                          =   A._rent.map(lambda d: float(d.strip('$')))
        A['_beds']                          =   A._rent.map(int)
        date_cols                           =   [ it for it in A.columns.tolist() if it.rfind('_date')==len(it)-5 ]
        for it in date_cols:
            A[it]                           =   A[it].map(lambda d: self.T.DU.parse(d))
        return A

    def recent_modified(self):
        h                                   =   self.T.codecs_enc(self.br.source(),'utf8','ignore')
        tbls                                =   self.T.getTagsByAttr(h,'table',{'class':'added_table'},contents=False)
        
        drop_cols                           =   ['Link']

        # GET ADDED TABLE
        added                               =   tbls[0]#.decode_contents(formatter='html')

        A                                   =   self.T.pd.read_html(self.T.re_sub(r'[^\x00-\x7F]+',' ', '<table>'+added.renderContents()+'</table>'),header=1)[0]
        A_idx                               =   [(n*2) for n in range(len(A))]
        A                                   =   A[A.index.isin(A_idx)].reset_index(drop=True).drop(drop_cols,axis=1)

        A_key_items                         =   [it.findAll('td')[1] for it in added.findAll('tr') if len(it.findAll('td'))==11][1:]
        A                                   =   self._clean_cols(A,A_key_items)


        # GET RECENTS TABLE
        recents                             =   tbls[1]#.decode_contents(formatter='html')

        R                                   =   self.T.pd.read_html(self.T.re_sub(r'[^\x00-\x7F]+',' ', '<table>'+recents.renderContents()+'</table>'),header=1)[0]
        R_idx                               =   [(n*2) for n in range(len(R))]
        R                                   =   R[R.index.isin(R_idx)].reset_index(drop=True).drop(drop_cols,axis=1)

        R_key_items                         =   [it.findAll('td')[1] for it in recents.findAll('tr') if len(it.findAll('td'))==11][1:]
        R                                   =   self._clean_cols(R,R_key_items)

        return added,A,recents,R

    def update_from_homepage(self):
        added,A,recents,R = self.recent_modified()
        i_trace()

class Browser:
    """Main class for initiating AutoPoster"""

    def __init__(self,browser_type='phantom'):
        import                                  datetime            as dt
        from dateutil                       import parser           as DU
        from urllib                         import quote_plus,unquote
        from re                             import findall          as re_findall
        from re                             import sub              as re_sub           # self.T.re_sub('patt','repl','str','cnt')
        # from re                             import search           as re_search        # re_search('patt','str')
        from subprocess                     import Popen            as sub_popen
        from codecs                         import encode           as codecs_enc
        from subprocess                     import PIPE             as sub_PIPE
        from traceback                      import format_exc       as tb_format_exc
        from sys                            import exc_info         as sys_exc_info
        import                                  inspect             as I
        from types                          import NoneType
        from time                           import sleep            as delay
        from os                             import environ          as os_environ
        from uuid                           import uuid4            as get_guid
        from sys                            import path             as py_path
        py_path                             =   py_path
        py_path.append(                         os_environ['HOME'] + '/.scripts')
        from system_settings                import DB_HOST,DB_PORT
        # from System_Control                 import System_Reporter
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
        conn                                =   pg_connect("dbname='routing' "+"user='postgres' "+"host='%s' password='' port=8800" % DB_HOST)
        cur                                 =   conn.cursor()
        D                                   =   {'browser_type'         :   browser_type,
                                                 'guid'                 :   str(get_guid().hex)[:7],
                                                 'user'                 :   os_environ['USER'],
                                                 'guid'                 :   str(get_guid().hex)[:7],
                                                 'today'                :   dt.datetime.now(),
                                                 # 'oldest_comments'      :   str(9*30),                      # in days
                                                 # 'transaction_cnt'      :   '100',
                                                 'growl_notice'         :   True,
                                                 'debug'                :   True,}
        D.update(                               {'tmp_tbl'              :   'tmp_' + D['guid'] } )

        self.T                              =   To_Class(D)
        self.PP                             =   PP_Functions(self)
        self.B                              =   self

        self.logged_in                      =   False


        all_imports                         =   locals().keys()
        for k in all_imports:
            if not k=='D':
                self.T.update(                  {k                      :   eval(k) })

    def post_screenshot(self,br):
        fpath                           =   '/home/ub2/SERVER2/aprinto/static/phantom_shot'
        if THIS_PC=='ub2':
            br.screenshot(                  fpath )
        else:
            br.screenshot(                  '/tmp/phantom_shot' )
            cmds                        =   ['scp /tmp/phantom_shot %(host)s@%(serv)s:%(fpath)s;'
                                             % ({ 'host'                :   'ub2',
                                                  'serv'                :   'ub2',
                                                  'fpath'               :   fpath }),
                                             'rm -f /tmp/phantom_shot;']
            p                           =   self.T.sub_popen(cmds,stdout=self.T.sub_PIPE,shell=True)
            (_out,_err)                 =   p.communicate()
            assert _out                ==   ''
            assert _err                ==   None
        return

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



from sys import argv
if __name__ == '__main__':


    if   len(argv)>1:
        SV                              =   Scrape_Vendors()
        query_str                       =   '' if len(argv)<4 else argv[3]
        msg                             =   ''


        if   argv[1]=='sl':

            if   ['1','search_results'].count(argv[2])>0:
                SV.SL.scrape_sl_1_search_results(query_str)

            elif ['2','prev_closed_v'].count(argv[2])>0:
                SV.SL.scrape_sl_2_previously_closed_vendors(query_str)

            elif ['3','v_pgs'].count(argv[2])>0:
                SV.SL.scrape_sl_3_known_vendor_pages(query_str)

            else:
                msg                     =   'UNKNOWN COMMAND LINE ARGUMENTS'


        elif argv[1]=='y':

            if   ['0','search_results'].count(argv[2])>0:
                SV.Yelp.scrape_yelp_0_search_results(query_str)

            elif ['1','api'].count(argv[2])>0:
                SV.Yelp.scrape_yelp_1_api(query_str)

            elif ['2','v_pgs'].count(argv[2])>0:
                SV.Yelp.scrape_yelp_2_vendor_pages(query_str)

            else:
                msg                     =   'UNKNOWN COMMAND LINE ARGUMENTS'

        else:
            msg                         =   'UNKNOWN COMMAND LINE ARGUMENTS'


        if msg:
            print msg