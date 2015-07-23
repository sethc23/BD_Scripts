
from ipdb import set_trace as i_trace

class Identity:
    
    def __init__(self):
        from faker                                  import Factory                  as fake_factory
        import us                                                                   as US
        from pyzipcode                              import ZipCodeDatabase
        F                                           =   fake_factory.create()
        Z = ZipCodeDatabase()
        self.F = F
        self.Z = Z
        self.US= US


        import                                  datetime            as dt
        epoch                               =   dt.datetime.now().utcfromtimestamp(0)
        from dateutil                       import parser           as DU
        from re                             import findall          as re_findall
        from re                             import sub              as re_sub           # self.T.re_sub('patt','repl','str','cnt')
        # from re                             import search           as re_search        # re_search('patt','str')
        from subprocess                     import Popen            as sub_popen
        import                                  codecs
        from subprocess                     import PIPE             as sub_PIPE
        import                                  requests
        from types                          import NoneType
        from uuid                           import uuid4            as get_guid
        from os                             import environ          as os_environ
        from sys                            import path             as py_path
        py_path                             =   py_path
        py_path.append(                         os_environ['HOME'] + '/.scripts')
        from System_Control                 import Google
        from py_classes                     import To_Class
        from System_Control                 import System_Admin     as SA
        sys_admin                           =   SA()
        # DB                                  =   'autoposter'
        
        D                                   =   {'exec_cmds'            :   sys_admin.exec_cmds,
                                                 'guid'                 :   str(get_guid().hex)[:7],
                                                 'user'                 :   os_environ['USER'],
                                                 'guid'                 :   str(get_guid().hex)[:7],
                                                 'today'                :   dt.datetime.now(),
                                                 'growl_notice'         :   True,
                                                 'debug'                :   True,}
        D.update(                               {'tmp_tbl'              :   'tmp_' + D['guid'] } )

        self.T                              =   To_Class(D)
        all_imports                         =   locals().keys()
        for k in all_imports:
            if not k=='D':
                self.T.update(                  {k                      :   eval(k) })

    class Create:

        def __init__(self):

            pass

        def gmail_act(self):

            pass

        def ssl_cert(self,email):

        D                                   =   {'_user_name'               :   email[:email.find('@')],
                                                 '_BASE_DIR'                :   self.T.os_environ['SERV_HOME'] + '/autoposter/identities',
                                                 '_user_agent'              :   self.F.user_agent(),
                                                 '_state_abbr'              :   self.F.state_abbr()}
        D.update(                               {'_SAVE_DIR'                :   '%s/%s' % (D['_BASE_DIR'],D['_user_name'])})
        
        cmds                                =   ['mkdir -p %(_SAVE_DIR)s && cd %(_SAVE_DIR)s && rm ./*;' % D]
        
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
                                                 '_email'                   :   email,
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

        return
