
from ipdb import set_trace as i_trace

class VPN:

    def __init__(self,_parent):
        for attr, value in _parent.__dict__.iteritems():
            setattr(self,attr,value)
        self.credentials                    =   self.T.os_environ['HOME'] + '/.vpnpass'

    def upsert_to_pgsql(self):
        self.T.conn.set_isolation_level(        0)
        self.T.cur.execute(                     'DROP TABLE IF EXISTS %(tmp_tbl)s;' % self.T)
        self.results.to_sql(                    self.T['tmp_tbl'],self.T.eng)

        upd_set                             =   ','.join(['%s = t.%s' % (it,it) for it in self.results.columns])
        ins_cols                            =   ','.join(self.results.columns)
        sel_cols                            =   ','.join(['t.%s' % it for it in self.results.columns])

        self.T.update(                          {'upd_set'              :   upd_set,
                                                 'ins_cols'             :   ins_cols,
                                                 'sel_cols'             :   sel_cols,})
        # upsert to properties
        cmd                                 =   """
                                                with upd as (
                                                    update vpns p
                                                    set
                                                        %(upd_set)s
                                                    from %(tmp_tbl)s t
                                                    where p._file     =   t._file
                                                    returning t._file _file
                                                )
                                                insert into vpns ( %(ins_cols)s )
                                                select
                                                    %(sel_cols)s
                                                from
                                                    %(tmp_tbl)s t,
                                                    (select array_agg(f._file) upd_files from upd f) as f1
                                                where (not upd_files && array[t._file]
                                                    or upd_files is null);

                                                DROP TABLE %(tmp_tbl)s;
                                                """ % self.T
        self.T.conn.set_isolation_level(        0)
        self.T.cur.execute(                     cmd)

    def update_db_with_server_info(self):
        
        import us                                                           as US
        from os                             import listdir                  as os_listdir
        info_path                           =   '/etc/openvpn/hma'
        _files                              =   os_listdir(info_path)

        df                                  =   self.T.pd.DataFrame(data={'_file':_files})
        df['_type']                         =   df._file.map(lambda s: s[:-5][-3:])
        df['_country']                      =   df._file.map(lambda s: s[:s.find('.')])
        df['_state']                        =   df._file.map(lambda s: self.T.re_sub(r'([A-Z][a-z]+)([A-Z][a-z]+)',r'\1 \2',s.split('.')[1]) )
        df['_city']                         =   df._file.map(lambda s: None if not len(s.split('.'))>=5 else s.split('.')[2])
        df['_local']                        =   df._city.map(lambda s: None if not s or len(s.split('_'))<2 else s.split('_')[1])

        ndf                                 =   df[(df._local.isnull()==False)&(df._country=='USA')].reset_index(drop=True)
        ndf['_state_abbr']                  =   ndf._state.map(lambda s: self.T.US.states.lookup('New Jersey').abbr)
        ndf['_city']                        =   ndf._city.map(lambda s: s if not s or not s.count('_') else s[:s.find('_')])
        ndf['_file']                        =   ndf._file.map(lambda s: info_path + '/%s' % s)

        self.results                        =   ndf
        self.upsert_to_pgsql(                   )
        
        return True



class Identity:
    
    def __init__(self,_parent):
        self.T                              =   _parent.T
        from faker                          import Factory                  as fake_factory
        import us                                                           as US
        from pyzipcode                      import ZipCodeDatabase
        F                                   =   fake_factory.create()
        Z                                   =   ZipCodeDatabase()
        self.F                              =   F
        self.Z                              =   Z
        self.US                             =   US
        self.Create                         =   self.Create(self)
        self.VPN                            =   VPN(self)

        all_imports                         =   locals().keys()
        for k in all_imports:
            if not k=='D':
                self.T.update(                  {k                      :   eval(k) })

    class Create:

        def __init__(self,_parent):
            for attr, value in _parent.__dict__.iteritems():
                setattr(self,attr,value)
                
        def update_db(self):
            cmd                             =   """ CREATE TABLE IF NOT EXISTS identities (
                                                    guid                                    text,
                                                    email                                   text,
                                                    pw                                      text,
                                                    details                                 jsonb
                                                    );
                                                    

                                                    
                                                """
            self.T.conn.set_isolation_level(    0)
            self.T.cur.execute(                 cmd)

        def gmail_act(self):

            
            return 'e3e1ed2@gmail.com'

        def ssl_cert(self):

            
            D                                   =   {'_user_name'               :   self.email[:self.email.find('@')],
                                                     '_BASE_DIR'                :   self.T.os_environ['SERV_HOME'] + '/autoposter/identities',
                                                     '_user_agent'              :   self.F.user_agent()}
            D.update(                               {'_SAVE_DIR'                :   '%s/%s' % (D['_BASE_DIR'],D['_user_name'])})
            
            cmds                                =   ['mkdir -p %(_SAVE_DIR)s && cd %(_SAVE_DIR)s && rm ./*;' % D]
            vpns                                =   self.T.pd.read_sql("select * from vpns where _type='TCP'",self.T.eng)
            avail_states                        =   map(lambda s: self.T.re_sub(r'([A-Z][a-z]+)([A-Z][a-z]+)',r'\1 \2',s),
                                                                    map(lambda s: s.replace(' ',''),vpns._state_abbr.unique().tolist()))
            # Get State Where a Server Exists
            while True:
                _state_abbr                 =   self.F.state_abbr()
                if avail_states.count(_state_abbr):
                    break
            D.update(                           {'_state_abbr'              :   self.F.state_abbr() })

            # Get Zipcode within State
            while True:
                z                               =   self.F.zipcode()
                chk                             =   self.Z.get(z)
                if chk and chk[0].state==D['_state_abbr']:
                    break

            D.update(                               {'_country'                 :   'US',
                                                     '_state'                   :   self.US.states.lookup(D['_state_abbr']).name,
                                                     '_city'                    :   self.Z.get(z)[0].city.replace('/','\/'),
                                                     '_org'                     :   self.F.company().replace('/','\/'),
                                                     '_org_unit'                :   self.F.job().replace('/','\/'),
                                                     '_name'                    :   self.F.name().replace('/','\/'),
                                                     '_email'                   :   self.email,
                                                     })
            

            cmds.extend(                            ['openssl genrsa -out %(_user_name)s.key 4096 > /dev/null 2>&1;' % D,
                                                     ' '.join(['openssl req -x509 -new -nodes',
                                                             '-key %(_user_name)s.key -days 1024' % D,
                                                             '-out %(_user_name)s.pem' % D,
                                                             '-subj "/C=%(_country)s/ST=%(_state)s/L=%(_city)s/O=%(_org)s/OU=%(_org_unit)s/CN=%(_name)s/emailAddress=%(_email)s";' % D])
                                                     ])
            (_out,_err)                         =   self.T.exec_cmds(cmds)
            assert not _out
            assert _err is None

            cmd                             =   """
                                                    UPDATE identities SET details = '%s'::jsonb
                                                    WHERE email = '%s';
                                                """ % (self.T.j_dump(D),self.email)

            self.T.conn.set_isolation_level(    0)
            self.T.cur.execute(                 cmd)

            return '%s/%s.pem' % (D['_SAVE_DIR'],D['_user_name'])

        def cookie(self):
            f_path                          =   '%s/%s/%s/%s.cookie' % (self.T.os_environ['BD'],
                                                                         'real_estate/autoposter/identities',
                                                                         self.guid,
                                                                         self.guid)
            cmd                             =   [':> %s;' % f_path]
            (_out,_err)                     =   self.T.exec_cmds(cmd)
            assert not _out
            assert _err is None
            return f_path

        def vpn_connection(self):
            self.vpn                        =   VPN(self)

            i_trace()

        def new(self):


            
            # self.guid                       =   str(self.T.get_guid().hex)[:7]
            # self.T.conn.set_isolation_level(    0)
            # self.T.cur.execute(                 "INSERT INTO identities (guid) VALUES ('%s');" % self.guid)
            self.guid='e3e1ed2'


            #self.email                      =   self.gmail_act()
            #self.cookie                     =   self.cookie()
            #self.ssl_cert                   =   self.ssl_cert()
            self.vpn                        =   self.vpn_connection()
            return self
