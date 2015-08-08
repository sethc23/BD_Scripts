
try:
    from ipdb import set_trace as i_trace   # i_trace()
    # ALSO:  from IPython import embed_kernel as embed; embed()
except:
    pass

class Google:

    def __init__(self,_parent=None):
        from os                             import environ                  as os_environ
        from sys                            import path                     as py_path
        py_path.append(                         os_environ['HOME'] + '/.scripts')
        if _parent:            self._parent =   _parent
        if not _parent or not hasattr(_parent,'T'):
            from System_Control                 import System_Lib
            self.T                          =   System_Lib().T
        else:
            self.T                          =   _parent.T
            from System_Control                 import System_Reporter
            self.Reporter                   =   System_Reporter(self)
        locals().update(                        self.T.__getdict__())
        # self.Google                         =   self
        # self.Voice                          =   self.Voice(self)
        self.Gmail                          =   self.Gmail(self)

    class Voice:

        def __init__(self,_parent):
            self._parent                    =   _parent
            self.T                          =   _parent.T
            # self.Voice                      =   self
            from googlevoice                import Voice
            from googlevoice.util           import input
            self.Voice                      =   Voice()
            self.Voice.login(                   'aporodeliveryllc@gmail.com',
                                                '100%delivery')

        def _msg(self,phone_num,msg):
            # _out                        =   self.Voice.send_sms(phone_num, msg)
            # assert _out==None
            return

    class Gmail:

        def __init__(self,_parent,**kwargs):
            self._parent                    =   _parent
            self.T                          =   _parent.T

            for k in kwargs.keys():
                if k in ['username','pw']:
                    self.T.update(              {k: kwargs[k]})

            self.username                   =   'seth.t.chase@gmail.com' if not self.T.has_key('username') else self.T.username
            self.pw                         =   'meyqleanjtdfczpl' if not self.T.has_key('pw') else self.T.pw

            from os.path                    import getsize                  as os_getsize
            from os.path                    import exists as os_path_exists
            import                              datetime                    as DT
            import                              time
            import                              gmail_client                as GC
            self.T.py_path.append(              self.T.os_environ['BD'] + '/files_folders')
            from API_system                 import get_input

            attachments_path                =   self.T.os_environ['HOME'] + '/.gmail/attachments/'
            if not os_path_exists(              attachments_path):
                self.T.os_mkdir(                attachments_path)

            all_imports                     =   locals().keys()
            excludes                        =   ['self','_parent']
            for k in all_imports:
                if not excludes.count(k):
                    self.T.update(              {k                          :   eval(k) })
            globals().update(                   self.T.__getdict__())

        def _make_pgsql_tbl(self):
            cmd = """
                DROP TABLE IF EXISTS gmail;
                CREATE TABLE gmail
                    (
                        orig_msg jsonb,
                        all_mail_uid bigint,
                        g_msg_id bigint,
                        msg_id text
                    );
                """
            self.T.conn.set_isolation_level(0)
            self.T.cur.execute(cmd)
        def _unix_time(self,dt):
            epoch                       =   self.T.DT.datetime.utcfromtimestamp(0)
            delta                       =   dt - epoch
            return delta.total_seconds()
        def _fetch_msg_grp(self,msgs,grp_size):
            pt                          =   0
            while pt < len(msgs):
                msg_grp                 =   msgs[pt:pt+grp_size]
                res                     =   map(lambda m: m.fetch(),msg_grp)
                yield msg_grp
                pt                     +=   grp_size
        def _get_msg_ids(self,msg):
            if msg['headers'].has_key('Message-ID'):
                return msg['headers']['Message-ID']
            else:
                K                       =   msg['headers'].keys()
                dict_for_lower          =   dict(zip([it.lower() for it in K],K))
                if dict_for_lower.has_key('message-id'):
                    return msg['headers'][dict_for_lower['message-id']]
                else:
                    return 'None'
        def _msg_to_json(self,msg):
            """Cleaning/Adjusting msg contents to fit into JSON serializable"""

            D                           =   msg.__dict__

            D['body']                   =   self.T.codecs.encode(
                                                self.T.codecs.decode(D['body'],'ascii','ignore'),
                                                'ascii','ignore')
            D['html']                   =   self.T.codecs.encode(
                                                self.T.codecs.decode(D['html'],'ascii','ignore'),
                                                'ascii','ignore')

            if D.has_key('attachments'):
                attachment_json         =   []
                for A in msg.attachments:

                    attach_id           =   str(self.T.get_guid().hex)[:7]
                    AD                  =   dict({  attach_id       : {'name'           :   A.name,
                                                                       'size_in_kb'     :   A.size,
                                                                       'content_type'   :   A.content_type}})
                    attachment_json.append(AD)
                    if A.size > 0:
                        f_path          =   self.T.attachments_path + attach_id
                        A.save(             f_path)
                        saved_size      =   self.T.os_getsize(f_path)
                        assert saved_size==A.size

                D['attachments']        =   attachment_json
            else:
                del D['attachments']

            items_to_delete             =   ['mailbox','gmail','message']
            for it in items_to_delete:
                if D.has_key(it):
                    del D[it]
            D['sent_at']                =   D['sent_at'] if type(D['sent_at'])==int else int(self._unix_time(msg.sent_at))
            D['_labels']                =   list(D['_labels'])
            D['_flags']                 =   list(D['_flags'])

            ## Confirm all elements of msg object are expected (and will fit into JSON)
        #     for k,v in msg.iteritems():
        #         if ["<type 'str'>","<type 'int'>","<type 'list'>","<type 'dict'>","<type 'NoneType'>"].count(str(type(v)))==0:
        #             print 'unexpected data type in msg class'
        #             raise SystemError

            return self.T.j_dump(           D, ensure_ascii=False)

        def misc_queries(self):
            a="""
                select *
                from (
                    select
                    --  trim('"' from (orig_msg::json->'uid')::text)::integer _uid,
                    --  trim('"' from (orig_msg::json->'message_id')::text)::bigint _gmail_id,
                    --  to_timestamp((orig_msg::json->'sent_at')::text::double precision) _sent,
                    --  trim('"' from (orig_msg::json->'to'::text)::text) _to,
                    --  trim('"' from (orig_msg::json->'cc'::text)::text) _cc,
                    --  trim('"' from (orig_msg::json->'fr'::text)::text) _fr,
                    --  trim('"' from (orig_msg::json->'subject')::text) _subject,
                    --  orig_msg::json->'attachments' _attachments,
                        orig_msg::json->'_labels' _labels,
                        orig_msg::json->'_flags' _flags,
                        orig_msg
                    from gmail
                ) f1
                --where _sent < date 'May 1, 2007'
                --order by _sent
                limit 5
            """

        def all_mail(self):
            """Copy all messages to pgsql@system:gmail"""

            start                       =   self.T.time.time()

            g                           =   self.T.GC.login(self.username, self.pw)
            all_mail                    =   g.all_mail().mail()

            # CONFIRM gmail table exists
            qry                         =   """ select count(*)>0 c from information_schema.tables
                                                WHERE table_name = 'gmail'
                                            """
            if not self.T.pd.read_sql(qry,self.T.eng).c[0]==True:
                self._make_pgsql_tbl(       )


            # START PROCESSING FROM WHERE PREVIOUS PROCESSING ENDED
            df                          =   self.T.pd.DataFrame(data={'msg':all_mail})
            df['g_uid']                 =   df.msg.map(lambda m: int(m.uid))

            qry                         =   "select all_mail_uid from gmail"
            pdf                         =   self.T.pd.read_sql(qry,self.T.eng)
            pg_all_mail_uids            =   pdf.all_mail_uid.tolist()

            df['skip']                  =   df.g_uid.isin(pg_all_mail_uids)

            remaining_msgs              =   df[df.skip==False].msg.tolist()

            m                           =   self._fetch_msg_grp(remaining_msgs,25)

            while True:
                try:
                    msg_grp                 =   m.next()
                except StopIteration:
                    break
                msg_num                 =   len(msg_grp)
                msgs_as_dict            =   map(lambda m: m.__dict__,msg_grp)
                all_mail_uids           =   map(lambda m: m.uid, msg_grp)
                g_msg_ids               =   map(lambda m: int(m['message_id']),msgs_as_dict)
                msg_ids                 =   map(lambda m: self._get_msg_ids(m),msgs_as_dict)
                msgs_as_json            =   map(lambda m: self._msg_to_json(m),msg_grp)

                cmd                     =   unicode("",encoding='utf8',errors='ignore')
                for i in range(msg_num):
                    D                   =   {'orig_msg'     :   msgs_as_json[i].replace("'","''"),
                                             'all_mail_uid' :   all_mail_uids[i],
                                             'g_msg_id'     :   g_msg_ids[i],
                                             'msg_id'       :   msg_ids[i]}
                    upsert              =   """
                        INSERT into gmail (
                            orig_msg,
                            all_mail_uid,
                            g_msg_id,
                            msg_id
                            )
                        SELECT '%(orig_msg)s'::jsonb,%(all_mail_uid)s,%(g_msg_id)s,'%(msg_id)s'
                        FROM
                            (
                            SELECT array_agg(all_mail_uid) all_uids FROM gmail
                            ) as f1,
                            (
                            SELECT array_agg(g_msg_id) all_g_m_ids FROM gmail
                            ) as f2
                            -- msg_id ignored as sampling showed such value was not unique to each msg
                            -- (
                            -- SELECT array_agg(msg_id) all_m_ids FROM gmail
                            -- ) as f3
                        WHERE
                            (
                                not all_uids @> array['%(all_mail_uid)s'::bigint]
                            AND not all_g_m_ids @> array['%(g_msg_id)s'::bigint]
                            --AND not all_m_ids @> array['%(msg_id)s'::text]
                            )
                        OR
                            (
                               all_uids is null
                            OR all_g_m_ids is null
                            --OR all_m_ids is null
                            )
                        ;
                        """%D

                    # cmd                +=   unicode(self.T.codecs.encode(upsert,'ascii','ignore'),errors='ignore')
                    cmd                +=   unicode(upsert,errors='ignore') if type(upsert) is not unicode else upsert

                self.T.conn.set_isolation_level(0)
                self.T.cur.execute(         cmd)

            end                         =   self.T.time.time()
            print 'total time (seconds):',end-start

        def create_account(self,**kwargs):
            """ Keyword Args:
                    first_name,last_name,
                    user_name,password,
                    recovery_phone,recovery_email
            """

            def setup_account_info():
                # SETUP VARS WITH ACCOUNT INFO
                account_info_dict           =   {'first_name'               :   'FirstName',
                                                 'last_name'                :   'LastName',
                                                 'user_name'                :   'GmailAddress',
                                                 'password'                 :   'Passwd',
                                                 'recovery_phone'           :   'RecoveryPhoneNumber',
                                                 'recovery_email'           :   'RecoveryEmailAddress'}
                account_info_keys           =   account_info_dict.keys()
                T                           =   {}

                if hasattr(self.T,'id') and hasattr(self.T.id,'details'):
                    for k,v in self.T.id.details.__dict__.iteritems():
                        T.update(               {k.strip('_')               :   v})
                        kwargs.update(          {k.strip('_')               :   v})

                for k,v in kwargs.iteritems():
                    if account_info_keys.count(k):
                        T.update(               {account_info_dict[k]       :   v})

                # FILL IN ANY MISSING INFO

                if not T.has_key('FirstName') or not T.has_key('LastName'):
                    g                       =   self.T.randrange(0,2)
                    gender                  =   'Female' if g==0 else 'Male'
                    name                    =   self.T.Identity.F.name_female() if g==0 else self.T.Identity.F.name_male()
                    while len(name.split())!=2:
                        name                =   self.T.Identity.F.name_female() if g==0 else self.T.Identity.F.name_male()
                    first,last              =   name.split()
                    T.update(                   {'FirstName':first,'LastName':last,'gender_num':g,'gender':gender})

                if not T.has_key('GmailAddress'):
                    _user                   =   str(self.T.get_guid().hex)[:10]
                    _pw                     =   str(self.T.get_guid().hex)
                    T.update(                   {'GmailAddress':_user,'Passwd':_pw,'PasswdAgain':_pw})

                T.update(                       {'birth_month'              :   self.T.randrange(1,13),
                                                 'BirthDay'                 :   self.T.randrange(1,29),
                                                 'BirthYear'                :   self.T.randrange(1925,1990)})
                birth_month_dict            =   {10:'a',11:'b',12:'c'}
                if birth_month_dict.keys().count(T['birth_month']):
                    T['birth_month']        =   birth_month_dict[ T['birth_month'] ]

                if not T.has_key('RecoveryPhoneNumber'):
                    T.update(                   {'RecoveryPhoneNumber'      :   '6174295700'})

                if not T.has_key('RecoveryEmailAddress'):
                    T.update(                   {'RecoveryEmailAddress'     :   'seth.t.chase@gmail.com'})

                return T

            if not hasattr(self,'T'):
                self.T.py_path.append(          self.T.os_environ['BD'] + '/real_estate/autoposter')
                from auto_poster            import Auto_Poster
                AP                          =   Auto_Poster(None,no_identity=True)
                self.T.update(                  {'Identity'             :   AP.Identity})
                self.T.update(                  AP.T.__getdict__())

            T                               =   setup_account_info()

            self.T.br                       =   self.T.scraper('chrome',dict=self.T).browser

            start_page                      =   ''.join(['https://accounts.google.com/SignUp?',
                                                         'continue=https%3A%2F%2Fwww.google.com%2F%3Fgws_rd%3Dssl&hl=en'])
            self.T.br.open_page(                start_page)
            min_wait                        =   4
            Actions                         =   self.T.br.Actions(self.T.br.window)

            form_parts                      =   ['FirstName','LastName','GmailAddress','Passwd','PasswdAgain']
            for it in form_parts:
                self.T.br.set_element_val(      it,T[it],str)
                self.T.delay(                   self.T.randrange(min_wait,10))

            self.T.br.window.find_element_by_xpath('//*[@id=":0"]').click()
            self.T.delay(                       self.T.randrange(min_wait+3,min_wait+9))
            self.T.br.window.find_element_by_xpath('//*[@id=":%(birth_month)s"]' % T).click()
            self.T.delay(                       self.T.randrange(min_wait,9))

            form_parts                      =   ['BirthDay','BirthYear']
            for it in form_parts:
                self.T.br.set_element_val(      it,T[it],int)
                self.T.delay(                   self.T.randrange(min_wait,10))

            # Gender
            self.T.br.window.find_element_by_xpath('//*[@id=":d"]').click()        # Menu
            if T['gender_num']==0:
                self.T.br.window.find_element_by_xpath('//*[@id=":e"]').click()    # Female
            else:
                self.T.br.window.find_element_by_xpath('//*[@id=":f"]').click()    # Male

            # Phone // Current Email
            self.T.br.set_element_val(          'RecoveryPhoneNumber',T['RecoveryPhoneNumber'],int)
            self.T.delay(                       self.T.randrange(min_wait,10))
            it                              =   'RecoveryEmailAddress'
            self.T.br.set_element_val(          'RecoveryEmailAddress',T['RecoveryEmailAddress'],str)
            self.T.delay(                       self.T.randrange(min_wait,10))

            # CAPTCHA
            K                               =   self.T.br.window.find_element_by_id('recaptcha_challenge_image')
            start_location                  =   self.T.br.window.get_window_position()
            start_size                      =   self.T.br.window.get_window_size()
            self.T.br.zoom(                     '200%')
            self.T.br.window.set_window_size(   630,280)
            self.T.br.scroll_to_element(        "recaptcha_challenge_image")
            self.T.br.post_screenshot(          )
            self.T.br.zoom(                     '100%')
            self.T.br.window.set_window_size(   start_size['width'],start_size['height'])

            # Communicate CAPTCHA
            self.T.update(                      {'line_no'                  :   self.T.I.currentframe().f_back.f_lineno})
            self._parent.Reporter._growl(       '%(line_no)s GOOG@%(user)s<%(guid)s>: NEED CAPTCHA' % self.T,
                                                'http://sys.sanspaper.com/tmp/phantomjs.html' )

            # Receive & Enter Input
            captcha_input                   =   get_input("Captcha code?\n")
            self.T.br.scroll_to_element(        "recaptcha_response_field")
            self.T.br.set_element_val(          'recaptcha_response_field',captcha_input,str)

            # VERIFY INFORMATIONse
            most_vars_inputted              =   ['FirstName','LastName','GmailAddress',
                                                 'BirthDay','BirthYear','RecoveryPhoneNumber','RecoveryEmailAddress']
            for it in most_vars_inputted:
                assert self.T.br.execute('return document.getElementById("%s").value;' % it) == str(T[it])
            month_dict                      =   {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',
                                                 7:'July',8:'August',9:'September','a':'October','b':'November','c':'December'}
            assert self.T.br.window.find_element_by_xpath('//*[@id=":0"]').text == month_dict[ T['birth_month'] ]
            gender_dict                     =   { 0:'Female',1:'Male'}
            assert self.T.br.window.find_element_by_xpath('//*[@id=":d"]').text == gender_dict[ T['gender_num'] ]

            self.T.br.scroll_to_element(        "TermsOfService")
            self.T.br.window.execute_script(    'document.getElementById("TermsOfService").checked = true;')
            self.T.br.window.execute_script(    'document.getElementById("createaccount").submit();')

            T['guid']                       =   T['GmailAddress']
            T['email']                      =   T['GmailAddress'] + '@gmail.com'
            T['pw']                         =   T.pop('Passwd')
            details                         =   {'_name'                :   '%s %s' % (T['FirstName'],T['LastName']),}
            details.update(                     {'_recovery_phone'      :   T['RecoveryPhoneNumber'],})
            details.update(                     {'_recovery_email'      :   T['RecoveryEmailAddress'],})
            details.update(                     {'_birthday'            :   '%04d.%02d.%02d' % (int(T['BirthYear']),
                                                                                                int(T['birth_month']),
                                                                                                int(T['BirthDay'])),})
            details.update(                     {'_gender'              :   gender_dict[ T['gender_num'] ],})
            T['details']                    =   self.T.j_dump(details)

            qry                             =   """ INSERT INTO identities (guid,email,pw,details)
                                                    VALUES ('%(guid)s','%(email)s','%(pw)s','%(details)s'::jsonb) """ % T
            self.T.conn.set_isolation_level(    0)
            self.T.cur.execute(                 qry)

            i_trace()



