
try:
    from ipdb import set_trace as i_trace   # i_trace()
    # ALSO:  from IPython import embed_kernel as embed; embed()
except:
    pass

class Google:

    def __init__(self):
        from os                             import environ                  as os_environ
        from sys                            import path                     as py_path
        py_path.append(                         os_environ['HOME'] + '/.scripts')
        from System_Control                 import System_Lib
        self.T                              =   System_Lib().T
        # self.Google                         =   self
        # self.Voice                          =   self.Voice(self)
        self.Gmail                          =   self.Gmail(self)

    class Voice:

        def __init__(self,_parent):
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
            self.T                          =   _parent.T
            for k in kwargs.keys():
                if k in ['username','pw']:
                    self.T.update(              {k: kwargs[k]})

            self.username                   =   'seth.t.chase@gmail.com' if not self.T.has_key('username') else self.T.username
            self.pw                         =   'meyqleanjtdfczpl' if not self.T.has_key('pw') else self.T.pw

            from os.path                    import getsize                  as os_getsize
            import                              datetime                    as DT
            import                              time
            import                              gmail_client                as GC
            from os.path                    import exists as os_path_exists

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

        def create_account(self,user_name,pw,**kwargs):
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
                for k,v in kwargs.iteritems():
                    assert account_info_keys.count(k)
                    T.update(                   {account_info_dict[k]       :   v})

                # FILL IN ANY MISSING INFO
                from faker                  import Factory                  as fake_factory
                F                           =   fake_factory.create()

                if not T.has_key('FirstName') or not T.has_key('LastName'):
                    g                       =   randrange(0,2)
                    name                    =   F.name_female() if g==0 else F.name_male()
                    while len(name.split())!=2:
                        name                =   F.name_female() if g==0 else F.name_male()
                    first,last              =   name.split()
                    T.update(                   {'FirstName':first,'LastName':last,'gender_num':g})

                if not T.has_key('GmailAddress'):
                    g                       =   str(self.T.get_guid().hex)[:10]
                    T.update(                   {'GmailAddress':g,'Passwd':g,'PasswdAgain':g})

                T.update(                       {'birth_month'              :   randrange(1,13),
                                                 'BirthDay'                 :   randrange(1,29),
                                                 'BirthYear'                :   randrange(1925,1990)})

                if not T.has_key('RecoveryPhoneNumber'):
                    T.update(                   {'RecoveryPhoneNumber'      :   '6174295700'})

                if not T.has_key('RecoveryEmailAddress'):
                    T.update(                   {'RecoveryEmailAddress'     :   'seth.t.chase@gmail.com'})

                return T

            self.T.py_path.append(              self.T.os_environ['BD'] + '/html')
            from HTML_API                   import getTagsByAttr,google,safe_url,getSoup
            from webpage_scrape             import scraper
            from time                       import sleep                    as delay
            from random                     import randrange

            T                               =   setup_account_info()

            self.T.scraper                  =   scraper
            self.T.br                       =   self.T.scraper('chrome',**self.T.__dict__).browser

            start_page                      =   ''.join(['https://accounts.google.com/SignUp?',
                                                         'continue=https%3A%2F%2Fwww.google.com%2F%3Fgws_rd%3Dssl&hl=en'])
            self.T.br.open_page(                start_page)
            delay(                              10)
            min_wait                        =   4
            Actions                         =   self.T.br.Actions(self.T.br.window)

            form_parts                      =   ['FirstName','LastName','GmailAddress','Passwd','PasswdAgain']
            for it in form_parts:
                pt                          =   self.T.br.window.find_element_by_id(it)
                Actions.move_to_element(pt).click().perform()
                delay(                          randrange(min_wait,11))
                self.T.br.randomize_keystrokes( self.T.br.window,T[it],pt)
                delay(                          randrange(min_wait,10))

            self.T.br.window.find_element_by_xpath('//*[@id=":0"]').click()
            delay(                              randrange(min_wait,7))
            self.T.br.window.find_element_by_xpath('//*[@id=":%(birth_month)s"]' % T).click()
            delay(                              randrange(min_wait,9))

            i_trace()

            form_parts                      =   ['BirthDay','BirthYear']
            for it in form_parts:
                pt                          =   self.T.br.window.find_element_by_id(it)
                Actions.move_to_element(pt).click().perform()
                delay(                          randrange(min_wait,9))
                pt.send_keys(                   T[it])
                delay(                          randrange(min_wait,10))

            # Gender
            self.T.br.window.find_element_by_xpath('//*[@id=":d"]').click()        # Menu
            if T['gender_num']==0:
                self.T.br.window.find_element_by_xpath('//*[@id=":e"]').click()    # Female
            else:
                self.T.br.window.find_element_by_xpath('//*[@id=":f"]').click()    # Male

            # Phone // Current Email
            form_parts                      =   ['RecoveryPhoneNumber','RecoveryEmailAddress']
            for it in form_parts:
                pt                          =   self.T.br.window.find_element_by_id(it)
                Actions.move_to_element(pt).click().perform()
                delay(                          randrange(min_wait,8))
                pt.send_keys(                   T[it])
                delay(                          randrange(min_wait,10))


            # i_trace()
            #
            # # CAPTCHA
            # ['recaptcha_challenge_image']
            # ['recaptcha_response_field']

            K                               =   self.T.br.window.find_element_by_id('recaptcha_challenge_image')
            start_location                  =   self.T.br.window.get_window_position()
            start_size                      =   self.T.br.window.get_window_size()
            tmp_location                    =   K.location_once_scrolled_into_view
            tmp_size                        =   K.size
            self.T.br.window.set_window_position(tmp_location['x'],tmp_location['y'])
            self.T.br.window.set_window_size(   tmp_size['width'],tmp_size['height'])
            self.T.br.post_screenshot(          br)
            self.T.br.window.set_window_position   =   start_location
            self.T.br.window.set_window_size       =   start_size

            self.T.update(                      {'line_no'                  :   self.T.I.currentframe().f_back.f_lineno})
            self.T.SYS_r._growl(                '%(line_no)s SL@%(user)s<%(guid)s>: NEED CAPTCHA' % self.T,
                                                'http://demo.aporodelivery.com/phantomjs.html' )
            captcha_input                   =   get_input("Captcha code?\n")
            br.window.find_element_by_id("captcha").send_keys(captcha_input)
            br.window.find_element_by_name("submit").click()
            z                               =   br.get_url()


            i_trace()
            # VERIFY INFORMATION

            # Policy Agreement // Submit Button
            form_parts                      =   ['TermsOfService','submitbutton']
            for it in form_parts:
                pt                          =   self.T.br.window.find_element_by_id(it)
                pt.click(                       )
                delay(                          randrange(min_wait,8))
                pt.send_keys(                   T[it])
                delay(                          randrange(min_wait,10))



            return T


