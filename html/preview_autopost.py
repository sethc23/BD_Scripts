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
        # self.logged_in                      =   self.login()

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
        added,A,recents,R                   =   self.recent_modified()
        i_trace()

class Auto_Poster:
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
        from py_classes                     import To_Class
        from System_Control                 import System_Admin     as SA
        sys_admin                           =   SA()
        DB                                  =   'autoposter'
        
        D                                   =   {'exec_cmds'            :   sys_admin.exec_cmds,
                                                 'exec_root_cmds'       :   sys_admin.exec_root_cmds,
                                                 'browser_type'         :   browser_type,
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
        all_imports                         =   locals().keys()
        for k in all_imports:
            if not k=='D':
                self.T.update(                  {k                      :   eval(k) })
        globals().update(                       self.T.__getdict__())
        self.pgSQL                          =   self.pgSQL(self)
        self.Config                         =   self.Config(self)
        self.Maintenance                    =   self.Maintenance(self)
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

    class pgSQL:

        def __init__(self,_parent):
            self.AP                         =   _parent
            self.T                          =   _parent.T
            self.pgSQL                      =   self
            import                              pandas              as pd
            # from pandas.io.sql                  import execute          as sql_cmd
            pd.set_option(                      'expand_frame_repr', False)
            pd.set_option(                      'display.max_columns', None)
            pd.set_option(                      'display.max_rows', 1000)
            pd.set_option(                      'display.width', 180)
            np                              =   pd.np
            np.set_printoptions(                linewidth=200,threshold=np.nan)
            import                              geopandas       as gd
            from sqlalchemy                     import create_engine
            from logging                        import getLogger
            from logging                        import INFO             as logging_info
            getLogger(                          'sqlalchemy.dialects.postgresql').setLevel(logging_info)
            from psycopg2                       import connect          as pg_connect
            from psycopg2                       import OperationalError,InterfaceError
            from system_settings                import THIS_PC,DB_HOST,DB_PORT
            # from System_Control                 import System_Reporter
            # SYS_r                               =   System_Reporter()
            try:
                eng                         =   create_engine(r'postgresql://postgres:postgres@%s:%s/%s'
                                                                  %(DB_HOST,DB_PORT,self.T.DB),
                                                                  encoding='utf-8',
                                                                  echo=False)

                conn                        =   pg_connect("dbname='%s' " % self.T.DB +
                                                                   "user='postgres' "+
                                                                   "host='%s' password='' port=%s" % (DB_HOST,
                                                                                                      DB_PORT))
                cur                         =   conn.cursor()
            except OperationalError:
                print 'NO DB CONNECTED'
                pass

            all_imports                     =   locals().keys()
            excludes = ['self', '_parent']
            for k in all_imports:
                if not excludes.count(k):
                    self.T.update(              {k                      :   eval(k) })
            self.Functions                  =   self.Functions(self.pgSQL)
            self.Triggers                   =   self.Triggers(self.pgSQL)

        def _initial_build(self):
            
            pass

        class Functions:

            def __init__(self,_parent):
                self.T                      =   _parent.T
                self.Create                 =   self.Create(self)

            class Create:

                def __init__(self,_parent):
                    self.T                  =   _parent.T
                    self.Create             =   self

        class Triggers:

            def __init__(self,_parent):
                self.T                      =   _parent.T
                self.Create                 =   self.Create(self)

            class Create:

                def __init__(self,_parent):
                    self.T                  =   _parent.T
                    self.Create             =   self

    class Config:

        def __init__(self,_parent):
            self.AP                         =   _parent
            self.T                          =   _parent.T
            self.Config                     =   self

        def update_build_files(self):
            def make_dir_path(d_path,base_dir):
                dirs_in_path                =   d_path.replace(base_dir,'').lstrip('/').split('/')
                for d in dirs_in_path:
                    base_dir                =   '/'.join([base_dir,d])
                    if not os_path.isdir(base_dir):
                        os_mkdir(               base_dir)

            from_dir                        =   os_environ['APORO']
            to_dir                          =   os_environ['SERV_HOME'] + '/BUILD/files/aporo/src'

            specific_paths                  =   {os_environ['SERV_HOME']+'/.scripts/pgsql_functions.sql':
                                                 to_dir.replace('/src','/setup')}


            for k,v in specific_paths.items():
                cmd                         =   'cp -R %s %s' % (k,v)
                p                           =   sub_popen(cmd,stdout=sub_PIPE,shell=True)
                (_out,_err)                 =   p.communicate()
                assert _out                ==   ''
                assert _err                ==   None

            # COPY FILES TO DESTINATION
            excludes                        =   ['.pyc','ENV']
            src_files                       =   []
            for root, sub_dir, files in os_walk(from_dir):
                for f in files:
                    f_path                  =   os_path.join(root,f)
                    if not sum([f_path.count(it) for it in excludes]):
                        new_f_path          =   f_path.replace(from_dir,to_dir)
                        src_files.append(       new_f_path)
                        new_dir_path        =   new_f_path[:new_f_path.rfind('/')]
                        if not os_path.isdir(new_dir_path):
                            make_dir_path(      new_dir_path,to_dir)
                        cmd                 =   'cp -R %s %s' % (f_path,new_f_path)
                        p                   =   sub_popen(cmd,stdout=sub_PIPE,shell=True)
                        (_out,_err)         =   p.communicate()
                        assert _out        ==   ''
                        assert _err        ==   None

            # REMOVE FILES FROM DESTINATION NOT IN SOURCE
            for root, sub_dir, files in os_walk(from_dir):
                for f in files:
                    f_path                  =   os_path.join(root,f)
                    if src_files.count(f_path):
                        t                   =   src_files.pop(src_files.index(f_path))
            for it in src_files:
                cmd                         =   'rm -fR %s' % it
                p                           =   sub_popen(cmd,stdout=sub_PIPE,shell=True)
                (_out,_err)                 =   p.communicate()
                assert _out                ==   ''
                assert _err                ==   None

            return

        def build_db(self):
            cmd                             =   ''.join(["sudo -u postgres psql postgres -h 0.0.0.0",
                                                        " --port %s -l | grep %s | wc -l;"%(self.T.DB_PORT,self.T.DB)])

            # cmds                            =   ['echo "money" | sudo -S --prompt=\'\' ',
            #                                      'script -qc \"bash -i -l -c \'',
            #                                      cmd,
            #                                      '\'\";',
            #                                      'rm -f typescript;'
            #                                     ]
            args                            =   self.T.To_Class({       'cmd'       :   cmd,
                                                                        'tag'       :   'autoposter_chk_db',
                                                                        'cmd_host'  :   'ub2',
                                                                        'results'   :   'print',
                                                                        'errors'    :   'print'})
            (_out,_err)                     =   self.T.exec_root_cmds(args)
            print _out
            print _err
            assert _err==None
            for it in _out.split('\n'):
                if it.lower().count('error')>0:
                    print it
                else:
                    print it

            return

        def destroy_db(self):
            psql_cmd    = ['script -aqc "echo \"money\" | sudo -S -k --prompt=\'\'',
                           ' sudo su postgres -c \\\"',
                                'psql --host=0.0.0.0 --port=8800 --username=postgres -c \'',
                                '\\i $TMP;',
                           '\' \\\" ";',
                           'rm typescript;']
            cmd1        = [ 'echo "UPDATE pg_database set datallowconn = \'false\' where datname = \'aporo\';" > tmp;',
                            'echo "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = \'aporo\';" >> tmp;',
                            'echo "DROP DATABASE IF EXISTS aporo;" >> tmp;']
            cmd2        = [ 'TMP="`pwd`/tmp";',
                            ''.join(psql_cmd),]
            cmd3        = [ 'TMP="`pwd`/tmp";',
                            'rm $TMP;',
                            'unset TMP;']
            (_out,_err)                     =   self.exec_cmds(cmd1,'ub2','ub2')
            assert _err==None
            (_out,_err)                     =   self.exec_cmds(cmd2,'ub2','ub2')
            assert _err==None
            (_out,_err)                     =   self.exec_cmds(cmd3,'ub2','ub2')
            assert _err==None
            return

    class Maintenance:

        def __init__(self,_parent):

            self.AP                         =   _parent
            self.T                          =   _parent.T
            self.Maintenance                =   self
            py_path.append(                     '/home/ub2/SERVER2/ipython/ENV/' +
                                                'local/lib/python2.7/site-packages/matplotlib')
            from matplotlib.pyplot          import bar
            from time                       import tzname           as t_tzname
            THIS_TZ                         =   list(t_tzname)[-1]
            all_imports                     =   locals().keys()
            excludes = ['self', '_parent']
            for k in all_imports:
                if not excludes.count(k):
                    self.T.update(                {k                      :   eval(k) })


from sys import argv
if __name__ == '__main__':
    pass