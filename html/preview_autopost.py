# add encoding?
#   see SL_previously_closed_vendors

from ipdb import set_trace as i_trace
#; i_trace()


class PP_Functions:

    def __init__(self,_parent):
        self.AP                             =   _parent
        self.T                              =   _parent.T
        self.PP                             =   self
        from HTML_API                           import getTagsByAttr,google,safe_url,getSoup
        from json                               import dumps                as j_dump
        import re
        from random                             import randrange
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
        if A.columns.tolist().count('_date'):
            A['_avail_date']                =   A._date
            A                               =   A.drop(['_date'],axis=1)
        A['_keys']                          =   map(lambda t: '' if t.img is None else t.img.get('src'),key_items)
        A['_property_id']                   =   A._property_id.map(int)
        A['_photos']                        =   A._photos.map(lambda s: '' if s=='No Photos' else s)
        A['_rent']                          =   A._rent.map(lambda d: None if self.T.pd.isnull(d) else float(d.strip('$')))
        A['_beds']                          =   A._beds.map(lambda s: 0 if (s=='Studio' or type(s)==float) else int(s))
        date_cols                           =   [ it for it in A.columns.tolist() if (it.rfind('_date')==len(it)-5 or it.find('_date_')==0) ]
        for it in date_cols:
            A[it]                           =   A[it].map(lambda d: self.T.DU.parse(d))
        return A

    def recent_modified(self):
        if not hasattr(self,'logged_in'):
            self.logged_in                  =   self.login()
        h                                   =   self.T.codecs.encode(self.br.source(),'utf8','ignore')
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

        return A,R

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
                                                    update properties p
                                                    set
                                                        %(upd_set)s
                                                    from %(tmp_tbl)s t
                                                    where p._property_id     =   t._property_id
                                                    returning t._property_id _property_id
                                                )
                                                insert into properties ( %(ins_cols)s )
                                                select
                                                    %(sel_cols)s
                                                from
                                                    %(tmp_tbl)s t,
                                                    (select array_agg(f._property_id) upd_property_ids from upd f) as f1
                                                where (not upd_property_ids && array[t._property_id]
                                                    or upd_property_ids is null);

                                                DROP TABLE %(tmp_tbl)s;
                                                """ % self.T
        self.T.conn.set_isolation_level(        0)
        self.T.cur.execute(                     cmd)

    def update_pgsql_from_homepage(self):
        added,recents                       =   self.recent_modified()
        if len(added):
            self.results                    =   added
            self.upsert_to_pgsql(               )
        if len(recents):
            self.results                    =   recents
            self.upsert_to_pgsql(               )

    def update_post_settings(self):
        """updates pgSQL with current url destinations for 'Post Ad' feature"""
        if not hasattr(self,'logged_in'):
            self.logged_in                      =   self.login()
        if not self.br.get_url()==self.T.BASE_URL:
            self.br.open_page(self.T.BASE_URL)
        h                                       =   self.T.getSoup(self.br.source())
        res                                     =   h.findAll('td',attrs={'class':'testimonials'})
        assert len(res)>0
        res                                     =   res[1]
        res_id                                  =   res.parent.findAll('select')[0].get('id').strip('ad-')
        opts                                    =   res.findAll('option')
        df                                      =   self.T.pd.DataFrame(data={                  
                                                        'post_type'         :   map(lambda s: s.text.lower().replace(' ','_'),opts),
                                                        'post_link'         :   map(lambda s: s.get('value').replace(str(res_id),'%(_property_id)s'),opts),
                                                        })
        ndf                                     =   self.T.pd.DataFrame(columns=['_setting','_value'])
        D                                       =   {'_setting'             :   'post_urls',
                                                     '_value'               :   self.T.j_dump(dict(zip(df.post_type.tolist(),df.post_link.tolist())))}
        ndf                                     =   ndf.append(D,ignore_index=True)
        self.T.conn.set_isolation_level(           0)
        self.T.cur.execute(                        'drop table if exists %(tmp_tbl)s' % self.T)
        ndf.to_sql(                                 self.T.tmp_tbl,self.T.eng)
        cmd                                     =   """
                                                    with upd as (
                                                        UPDATE pp_settings p SET _value = t._value
                                                        FROM %(tmp_tbl)s t
                                                        WHERE p._setting = t._setting
                                                        RETURNING p._setting _setting
                                                        )
                                                    INSERT into pp_settings
                                                        (_setting,_value)
                                                    SELECT 
                                                        t._setting,t._value
                                                    FROM 
                                                        %(tmp_tbl)s t,
                                                        (select array_agg(u._setting) upd_setting from upd u) f1
                                                    WHERE (not upd_setting && array[t._setting]
                                                    or upd_setting is null);
                                                    """ % self.T
        self.T.conn.set_isolation_level(           0)
        self.T.cur.execute(                        cmd)
        self.T.conn.set_isolation_level(           0)
        self.T.cur.execute(                        'drop table if exists %(tmp_tbl)s' % self.T)

        # Check if any new types of post_type exist
        prop_tbl_cols                           =   self.T.pd.read_sql("select * from properties",self.T.eng).columns.astype(str).tolist()
        post_types                              =   eval(D['_value']).keys()
        # 1. Ensure columns exist for all post types
        missing_post_type_cols                  =   ['last_%s' % it for it in post_types if prop_tbl_cols.count('last_%s' % it)==0]
        for it in missing_post_type_cols:
            cmd                                 =   "ALTER TABLE properties add column %s TIMESTAMP with time zone" % it
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
        # 2. Create Triggers for checking 'posts' col/log and Updating Col values
        c                                       =   """ select replace(proname,'z_copy_latest_post_type_','') post_types
                                                        from (pg_trigger join pg_class on tgrelid=pg_class.oid)
                                                        join pg_proc on (tgfoid=pg_proc.oid)
                                                        where relname='properties'
                                                        AND position('copy_latest_post_type' in proname)>0
                                                    """
        current_post_type_triggers              =   self.T.pd.read_sql(c,self.T.eng).post_types.tolist()
        for it in post_types:
            if not current_post_type_triggers.count(it):
                self.AP.pgSQL.Triggers.Create.copy_latest_post_type(self.T.re_sub(r'^last_','',it)) 

        return

    def update_ads_from_email(self):
        cmd                                     =   """
                SELECT 
                    postlets,craiglist,body,orig_msg
                FROM
                    (
                        select 
                            CASE    WHEN position('postlets' in lower(_fr))>0 THEN true else FALSE END postlets,
                            CASE    WHEN position('craiglist' in lower(_fr))>0 THEN true else FALSE END craiglist,
                            CASE    WHEN length(body)>0 THEN body
                                    WHEN length(body)=0 THEN html END body,
                            orig_msg
                        from (
                            select
                                trim('"' from (orig_msg::json->'uid')::text)::integer _uid,
                                --trim('"' from (orig_msg::json->'message_id')::text)::bigint _gmail_id,
                                to_timestamp((orig_msg::json->'sent_at')::text::double precision) _sent,
                                --trim('"' from (orig_msg::json->'to'::text)::text) _to,
                                --trim('"' from (orig_msg::json->'cc'::text)::text) _cc,
                                trim('"' from (orig_msg::json->'fr'::text)::text) _fr,
                                trim('"' from (orig_msg::json->'subject')::text) _subject,
                                trim('"' from (orig_msg::json->'body')::TEXT) body,
                                trim('"' from (orig_msg::json->'html')::TEXT) html,
                                orig_msg::json->'_labels' _labels,
                                --orig_msg::json->'_flags' _flags,
                                orig_msg
                            from gmail
                        ) f1
                    ) f2
                WHERE postlets is true or craiglist is true
        """
        df                                      =   self.T.pd.read_sql(cmd,self.T.eng)

        

        i_trace()

    def get_property_info(self,pd_row):
        self.br.open_page(                 'http://previewbostonrealty.com/admin/property_index.php')
        prop_field                      =   self.br.window.find_element_by_name("searchproperty_IDs")
        if prop_field.is_displayed():
            prop_field.send_keys(           pd_row['_property_id'])
            prop_field.send_keys(           self.br.keys.ENTER)
        return

    def post_ad(self,post_type):

        def update_pgsql_with_post_data(self,prop,D,src):
            # UPDATE PGSQL
            chk = ', pl_checked_out = false' if src=='postlets' else ', cl_checked_out = false'
            cmd                                 =   """
                                                        UPDATE properties SET
                                                        posts            =   '%s'
                                                        %s
                                                        WHERE _property_id = '%s'
                                                    """ % (self.T.j_dump(D),chk,prop._property_id)

            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd   )
        def postlets(self):
            def login_postlets(self):
                try:
                    uname                       =   self.br.window.find_element_by_id('username')
                    if uname.is_displayed():
                        uname.send_keys(            'seth.chase.boston@gmail.com')
                        self.br.window.find_element_by_id('password').send_keys('B*_Realty')
                        self.br.window.find_element_by_id('password').send_keys(self.br.keys.ENTER)
                except:
                    pass

            items                               =   self.T.pd.read_sql("""                  
                                                        UPDATE properties p1 SET pl_checked_out = true
                                                        FROM 
                                                        (
                                                        SELECT * FROM properties p2
                                                        where 
                                                            p2.last_postlets is null
                                                            AND p2._beds >= 1
                                                            AND length(p2._photos)>0
                                                            AND pl_checked_out is false
                                                        order by 
                                                            p2._rent DESC,p2._walk_score DESC,
                                                            p2._beds DESC,p2._avail_date ASC
                                                        limit 5
                                                        ) f1
                                                        WHERE p1.uid=f1.uid
                                                        returning p1.*;""",self.T.eng)
            if not len(items):                      return
            for idx,prop in items.iterrows():
                D                               =   {} if prop.posts is None else prop.posts                
                goto_url                        =   self.T.BASE_URL + "postlets.php?property_ID=%s" % prop['_property_id']
                self.br.open_page(                  goto_url)
                self.br.window.find_element_by_name("titlegen").click()
                self.br.window.find_element_by_name("make_postlet").click()

                # i_trace()
                # IF POSTLETS LOGIN HERE: re-init webdriver/login/post

                
                # GET PAGE POST INFO
                src                             =   self.br.source()
                a                               =   src.find('<body')
                b                               =   src.find('>',a) + 1
                c                               =   src.find('<!--',b)
                cmts                            =   src[b:c].strip('\n')
                splitter                        =   '<br />' if cmts.count('<br />') else '<br>'
                cmts                            =   cmts.split(splitter)[:-1]
                try:
                    assert cmts[-1]            ==   'We _might_ review page...'
                except:
                    tuid                        =   int((self.T.dt.datetime.now()-self.T.epoch).total_seconds())
                    D.update({                      tuid                :       {'postlets'     :   'ERROR_1'} })
                    break
                
                i_trace()

                # ACTIVATE AD
                activate_postlet_xpath          =   """/html/body[@class='controller-ad view-main browser-ie']/div[@id='main']/div[@class='tablet-margins']/div[@id='postlet-main']/div[@class='postlet-content']/div[@id='postlet_review_form']/a[@class='button button_main']"""
                self.br.window.find_element_by_xpath(activate_postlet_xpath).click()

                # LOGIN INTO POSTLETS IF NECESSARY
                login_postlets(                     self)

                # CONFIRMED POST
                h                               =   self.T.getSoup(self.br.source())
                res                             =   h.findAll('div',attrs={'id':'activated-dialog'})
                try:
                    assert len(res)>0
                    self.br.window.find_element_by_class_name("closer").click()

                    post_url                    =   self.br.window.find_element_by_class_name('hdp-url').text
                    tuid                        =   int((self.T.dt.datetime.now()-self.T.epoch).total_seconds())
                    D.update({                      tuid                :       {'postlets'     :   post_url} })
                except:
                    tuid                        =   int((self.T.dt.datetime.now()-self.T.epoch).total_seconds())
                    D.update({                      tuid                :       {'postlets'     :   'ERROR_2'} })
                    break
                update_pgsql_with_post_data(self,prop,D,'postlets')
            return
        def craigslist(self):
            def login_craigslist(self):
                self.br.window.find_element_by_id("inputEmailHandle").send_keys('seth.chase.boston@gmail.com')
                self.br.window.find_element_by_id("inputPassword").send_keys('B*_Realty')
                self.br.window.find_element_by_id("inputPassword").send_keys(self.br.keys.ENTER)

            items                               =   self.T.pd.read_sql("""                  
                                                        UPDATE properties p1 SET cl_checked_out = true
                                                        FROM 
                                                        (
                                                        SELECT * FROM properties p2
                                                        where 
                                                            p2.last_craigslist is null
                                                            AND p2._beds >= 1
                                                            AND length(p2._photos)>0
                                                            AND cl_checked_out is false
                                                        order by 
                                                            p2._rent DESC,p2._walk_score DESC,
                                                            p2._beds DESC,p2._avail_date ASC
                                                        limit 5
                                                        ) f1
                                                        WHERE p1.uid=f1.uid
                                                        returning p1.*;
                                                        """,self.T.eng)
            if not len(items):                      return
            h                                       =   self.T.getSoup(self.br.source())
            res                                     =   h.findAll('td',attrs={'class':'testimonials'})
            assert                      len(res)    >   0
            res                                     =   res[1]
            res_id                                  =   res.parent.findAll('select')[0].get('id').strip('ad-')

            for idx,prop in items.iterrows():
                D                               =   {} if prop.posts is None else prop.posts

                # SET DESTINATION FOR FORM SUBMISSION
                cl_cols                         =   [ it for it in prop.axes[0].tolist() 
                                                        if it.find('last_craigslist_')==0 ]
                # post_type                       =   self.T.re_sub(r'^last_','',cl_cols[self.T.randrange(0,len(cl_cols))])
                post_type                       =   self.T.re_sub(r'^last_','',cl_cols[0])
                goto_url                        =   self.post_settings[post_type] % prop

                # CHANGE VALUE OF FIRST POST_AD FORM
                # Get First Row
                first_row_path                  =   ''.join([   "/html/body/div[@id='admin-container']",
                                                                "/div[@id='admin-center']",
                                                                "/table[@class='added_table'][1]",
                                                                "/tbody/tr[4]/td[@class='testimonials']"])
                # Change name and id of select tag
                select_path                     =   first_row_path + "/select"
                select_tag                      =   self.br.window.find_element_by_xpath(select_path)
                to_name                         =   select_tag.get_attribute('name').replace(str(res_id),str(prop['_property_id']))
                self.br.window.execute_script(      "arguments[0].setAttribute('name', arguments[1])", select_tag, to_name)
                to_id                           =   select_tag.get_attribute('id').replace(str(res_id),str(prop['_property_id']))
                self.br.window.execute_script(      "arguments[0].setAttribute('id', arguments[1])", select_tag, to_id)
                # Change value of first option
                option_1_path                   =   select_path + "/option[1]"
                option_1_tag                    =   self.br.window.find_element_by_xpath(option_1_path)
                self.br.window.execute_script(      "arguments[0].setAttribute('value', arguments[1])", option_1_tag, goto_url)
                # Change name and onclick for submit button
                button_path                     =   first_row_path + "/input"
                button_tag                      =   self.br.window.find_element_by_xpath(button_path)
                to_name                         =   button_tag.get_attribute('name').replace(str(res_id),str(prop['_property_id']))
                self.br.window.execute_script(      "arguments[0].setAttribute('name', arguments[1])", button_tag, to_name)
                to_onclick                      =   button_tag.get_attribute('onclick').replace(str(res_id),str(prop['_property_id']))
                self.br.window.execute_script(      "arguments[0].setAttribute('onclick', arguments[1])", button_tag, to_onclick)
                # Update Replace Marker
                res_id                          =   str(prop['_property_id'])
                button_tag.click(                   )

                # Move to new window
                self.T.delay(                       2)
                self.br.wait_for_page(              )
                assert self.br.window_count()   ==  2
                orig_window                     =   self.br.window.current_window_handle
                new_window                      =   [it for it in self.br.window.window_handles if it!=orig_window][0]
                self.br.window.switch_to_window(    new_window)
                
                # Check for Errors
                if self.br.source().find('posting aborted')!=-1:
                    x                           =   self.br.source()
                    b                           =   x.find('posting aborted')
                    a                           =   x[:b].rfind('<br')+3
                    msg                         =   x[a:b].strip('/ <>\n-').replace("'","")
                    tuid                        =   int((self.T.dt.datetime.now()-self.T.epoch).total_seconds())
                    D.update({                      tuid                :       {post_type     :   """ERROR: %s""" % msg} })
                    
                    update_pgsql_with_post_data(    self,prop,D,'craigslist')
                    self.br.window.close(           )
                    self.br.window.switch_to_window(orig_window)

                else:

                    # Make title for ad
                    for i in range(3):
                        self.br.window.find_element_by_name("titlegen").click()
                    self.T.delay(                       2)
                    self.br.wait_for_page(              )
                    assert self.br.window.find_element_by_id('title').get_attribute('value') is not None
                    
                    # Submit PP page for CL
                    self.br.window.find_element_by_id("submitbutton").click()
                    self.T.delay(                       2)
                    self.br.wait_for_page(              )

                    # ...page runs a script and finally shows a windowed CL page
                    
                    # Submit CL pictures
                    self.br.window.find_element_by_name("go").click()
                    self.T.delay(                       2)
                    self.br.wait_for_page(              )

                    try:
                        self.br.window.find_element_by_partial_link_text('log in to your account').click()
                        self.T.delay(                   2)
                        login_craigslist(               self)
                    except:
                        pass              
                    
                    # Option to Change/Re-Order pictures (click bottom button)
                    self.br.window.find_elements_by_tag_name('button')[-1].click()
                    self.T.delay(                       2)
                    self.br.wait_for_page(              )

                    # Click to publish ad
                    self.br.window.find_elements_by_tag_name('button')[0].click()
                    self.T.delay(                       2)
                    self.br.wait_for_page(              )

                    try:
                        h                               =   self.T.getSoup(self.br.source())
                        post_url                        =   h.findAll(href=self.T.re.compile('\.html'))[0].get('href')
                    except:
                        post_url                    =   "ERROR: couldn't obtain link"
                    tuid                            =   int((self.T.dt.datetime.now()-self.T.epoch).total_seconds())
                    D.update({                          tuid                :       {post_type     :   post_url} })
                    
                    update_pgsql_with_post_data(        self,prop,D,'craigslist')
                    self.br.window.close(               )
                    self.br.window.switch_to_window(    orig_window)

            return

        if not hasattr(self,'logged_in'):
            self.logged_in                      =   self.login()

        self.post_settings                      =   eval(self.T.pd.read_sql("""
                                                        select _value r 
                                                        from pp_settings 
                                                        where _setting = 'post_urls'
                                                        """,self.T.eng).r.tolist()[0])

        post_type                               =   post_type if type(post_type)==list else [post_type]
        if post_type.count('postlets'):             postlets(self)
        if post_type.count('craigslist'):           craigslist(self)

        return

    def run_search(self,**kwargs):
        if not hasattr(self,'logged_in'):
            self.logged_in                      =   self.login()
        self.br.open_page(                          self.T.SEARCH_URL)

        i_trace()

        self.get_search_results(                    )

        # # Make Query
        # --active, with photos, in boston, 5000 results
        # --active, without photos, with keys, in boston, 5000 results

        # D={
        # 'prop_id'  : {'name':'searchproperty_IDs'},
        # 'street' : {'name':'property_StreetName'},

        # 'bed_min': {'name':'min_bedrooms'},
        # 'bed_max': {'name':'max_bedrooms'},
        # 'bath_min': {'name':'min_bathooms'},
        # 'bath_max': {'name':'max_bathrooms'},
        # 'price_min': {'name':'price_min'},
        # 'price_max': {'name':'price_max'},

        # 'avail_now': {'name':'property_AvailableNow'},
        # 'avail_day': {'name':'property_AvailableDay'},
        # 'avail_month': {'name':'property_Available'},
        # 'avail_year': {'name':'property_AvailableYear'},

        # 'loc1': {'name':'loc1'},
        # 'loc2': {'name':'loc2'},

        # 'w_photo': {'name':'property_NumPhotos'},
        # 'wo_photo': {'name':'property_NoPhotos'},
        # 'w_keys': {'name':'property_Key'},
        # 'rented': {'id':'ap_SearchStatus2'},
        # 'pending': {'id':'ap_SearchStatus3'},
        # }

    def get_search_results(self):
        # Pull Results
        h                                   =   self.T.re_sub(r'[^\x00-\x7F]+',' ',self.T.codecs.encode(self.br.source(),'utf8','ignore'))
        tbls                                =   self.T.getTagsByAttr(h,'table',{'cellpadding':'4'},contents=False)
        try:
            tbl                             =   tbls[0]
        except:
            return
        
        header                              =   map(lambda t: t.text,tbl.find_all('tr')[3].find_all('td')) # 2 and 3 have worked worked (3 when next button at top)
        header                              =   dict(zip(header,range(len(header))))

        pop_list                            =   []
        for k,v in header.iteritems():
            if not unicode(k).isalpha():
                pop_list.append(k)
                
        for it in pop_list:
            del header[it]

        header                              =   dict(zip(['_'+it.lstrip('_').lower().replace(' ','_') for it in header.keys()],header.values()))
        header.update({                         '_keys'             :   1,
                                                '_photos'           :   1,
                                                '_apt_num'          :   6,
                                                '_property_id'      :   11})
        df                                  =   self.T.pd.DataFrame(columns=header.keys())
        df['ROWS']                          =   map(lambda s: s,tbl.find_all('tr',attrs={'valign':'top'}))
        for k,v in header.iteritems():
            df[k]                           =   df.ROWS.map(lambda t: t.find_all('td')[v].text)

        df['_property_id']                  =   df._updated.str.extract(r'#([0-9]+)').map(int)
        df['_walk_score']                   =   df._updated.str.extract(r'[s][c][o][r][e][:][\s]([0-9.]+)').map(float)
        df['_updated_date']                 =   df._updated.str.extract(r'\s([0-9]{2}\.[0-9]{2}\.[0-9]{2})')
        df['_price']                        =   df._price.str.replace(r'[^\d]','').map(lambda d: None if self.T.pd.isnull(d) else float(d))
        df['_beds']                         =   df._beds.str.replace(r'[^\d]','').map(lambda s: 0 if (type(s)==float or s=='Studio' or not s) else int(s))
        df['_status']                       =   df._status.map(lambda s: s.split('\n')[0])
        df['_avail_date']                   =   df._avail.map(lambda s: s.split('\t')[0])

        df['_address']                      =   df.ROWS.map(lambda r: r.find_all('td')[header['_address']].contents[0])
        df['tmp']                           =   df.ROWS.map(lambda r: r.find_all('td')[header['_keys']].find('img',attrs={'src':self.T.re.compile("key")}))
        df['_keys']                         =   df.tmp.map(lambda t: None if t is None or not t.has_key('src') else t.get('src'))
        df['tmp']                           =   df.ROWS.map(lambda r: r.find_all('td')[header['_photos']].find('img',attrs={'src':self.T.re.compile("photo")}))
        df['_photos']                       =   df.tmp.map(lambda t: None if t is None or not t.has_key('src') else t.get('src'))
        df['_city']                         =   df.ROWS.map(lambda t: [ self.T.re_sub(r'[^a-zA-Z0-9 ]+','',it) for it in list(t.find_all('td')[header['_city']].contents) if ( type(it).__name__!='Tag' and self.T.re_sub(r'[^a-zA-Z0-9 ]+','',it) is not None) ] )
        df['_apt_num']                      =   df.ROWS.map(lambda t: self.T.re_sub('\t|\n','',t.find_all('td')[header['_apt_num']].text))
        df['_address']                      =   df[['_address','_apt_num']].apply(lambda t: '%s, Apt. %s' % (t[0],t[1]),axis=1)

        df                                  =   df.drop(['_actions','_updated','_avail','_apt_num','ROWS'],axis=1)
        df                                  =   df.rename(columns={ '_city'             :       '_town',
                                                                    '_price'            :       '_rent'})

        col_ord                             =   ['_property_id','_updated_date','_walk_score','_keys','_photos','_status','_beds',
                                                '_avail_date','_address','_town','_rent']
        df                                  =   df.ix[:,col_ord].reset_index(drop=True)

        date_cols                           =   [ it for it in df.columns.tolist() if (it.rfind('_date')==len(it)-5 or it.find('_date_')==0) ]
        for it in date_cols:
            df[it]                          =   df[it].map(lambda d: self.T.DU.parse(d))
        
        self.results                        =   df
        self.upsert_to_pgsql(                   )

        return


    def close_browser(self):

        self.br.quit()

class Auto_Poster:
    """Main class for initiating AutoPoster"""

    def __init__(self,browser_type='phantom'):
        import                                  datetime            as dt
        epoch                               =   dt.datetime.now().utcfromtimestamp(0)
        from dateutil                       import parser           as DU
        from urllib                         import quote_plus,unquote
        from re                             import findall          as re_findall
        from re                             import sub              as re_sub           # self.T.re_sub('patt','repl','str','cnt')
        # from re                             import search           as re_search        # re_search('patt','str')
        from subprocess                     import Popen            as sub_popen
        import                                  codecs
        from subprocess                     import PIPE             as sub_PIPE
        from traceback                      import format_exc       as tb_format_exc
        from sys                            import exc_info         as sys_exc_info
        import                                  inspect             as I
        from types                          import NoneType
        from time                           import sleep            as delay
        from os                             import environ          as os_environ
        from os.path                        import exists           as os_path_exists
        from os                             import makedirs         as os_makedirs
        from uuid                           import uuid4            as get_guid
        from sys                            import path             as py_path
        py_path                             =   py_path
        py_path.append(                         os_environ['HOME'] + '/.scripts')
        from System_Control                 import Google
        from py_classes                     import To_Class
        # from System_Control                 import System_Admin     as SA
        # sys_admin                           =   SA()
        DB                                  =   'autoposter'
        
        D                                   =   {#'exec_cmds'            :   sys_admin.exec_cmds,
                                                 #'exec_root_cmds'       :   sys_admin.exec_root_cmds,
                                                 'browser_type'         :   browser_type,
                                                 'guid'                 :   str(get_guid().hex)[:7],
                                                 'user'                 :   os_environ['USER'],
                                                 'guid'                 :   str(get_guid().hex)[:7],
                                                 'today'                :   dt.datetime.now(),
                                                 # 'oldest_comments'      :   str(9*30),                      # in days
                                                 # 'transaction_cnt'      :   '100',
                                                 'growl_notice'         :   True,
                                                 'debug'                :   True,
                                                 'BASE_URL'             :   'http://previewbostonrealty.com/admin/',
                                                 'MODDED_URL'           :   'http://previewbostonrealty.com/admin/recent_modified.php',
                                                 'SEARCH_URL'           :   'http://previewbostonrealty.com/admin/property_index.php'}
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
        self.gmail                          =   Google.Gmail(_parent=self,kwargs={'username'    :   'seth.chase.boston@gmail.com',
                                                                                  'pw'          :   'uwejjozvkkcahgrj'})
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
            import logging
            logging.basicConfig()
            logging.getLogger(                  'sqlalchemy.engine').setLevel(logging.WARNING)
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

                def copy_latest_post_type(self,post_type):
                    # def z_auto_update_timestamp(self,tbl,col):
                    a="""
                        DROP FUNCTION if exists z_copy_latest_post_type_%(post_type)s() cascade;
                        DROP TRIGGER if exists update_last_%(post_type)s ON properties;

                        CREATE OR REPLACE FUNCTION z_copy_latest_post_type_%(post_type)s()
                        RETURNS TRIGGER AS $funct$

                        from os                             import system           as os_cmd
                        from traceback                      import format_exc       as tb_format_exc
                        from sys                            import exc_info         as sys_exc_info

                        try:

                            T                           =   TD["new"]
                            T.update({                      'post_type'             :   '%(post_type)s' })
                            trigger_depth               =   plpy.execute('select pg_trigger_depth() res')[0]['res']
                            
                            if (T["posts"] == None
                                or TD["new"]["posts"]==TD["old"]["posts"]
                                or trigger_depth>1):        return
                            else:

                                p = \"\"\"
                                    with res as 
                                        (
                                        select 
                                            uid,to_timestamp(times::double precision) post_time,json_object_keys( posts::json -> times ) post_type,
                                            ROW_NUMBER() OVER(PARTITION BY f2.uid,f2.post_type ORDER BY times DESC) as rk
                                        from
                                            (
                                            select 
                                                uid,_property_id,json_object_keys( posts::json ) times,posts,
                                                json_object_keys( posts::json -> json_object_keys( posts::json ) ) post_type
                                            from ( 
                                                select 
                                                    ##(uid)s uid,
                                                    ##(_property_id)s _property_id,
                                                    '##(posts)s'::jsonb posts
                                                ) f1
                                            ) f2
                                            where post_type = '%(post_type)s'
                                        )
                                    UPDATE properties p SET last_%(post_type)s = s.post_time
                                    FROM res s
                                    WHERE s.rk=1 AND p.uid=s.uid
                                    \"\"\" ## T

                                # plpy.log(p)
                                plpy.execute(p)
                                return

                        except plpy.SPIError:
                            plpy.log('z_copy_latest_post_type_%(post_type)s FAILED')
                            plpy.log(tb_format_exc())
                            plpy.log(sys_exc_info()[0])
                            return


                        $funct$ language "plpythonu";

                        CREATE TRIGGER update_last_%(post_type)s
                        AFTER UPDATE or INSERT ON properties
                        FOR EACH ROW
                        EXECUTE PROCEDURE z_copy_latest_post_type_%(post_type)s();

                    """ % {'post_type':post_type}

                    self.T.conn.set_isolation_level(       0)
                    self.T.cur.execute(                    a.replace('##','%'))
                    return

                def keep_recent_craigslist(self):
                    # def z_auto_update_timestamp(self,tbl,col):
                    a="""
                        DROP FUNCTION if exists z_keep_recent_craigslist() cascade;
                        DROP TRIGGER if exists update_last_craigslist ON properties;

                        CREATE OR REPLACE FUNCTION z_keep_recent_craigslist()
                        RETURNS TRIGGER AS $funct$

                        from os                             import system           as os_cmd
                        from traceback                      import format_exc       as tb_format_exc
                        from sys                            import exc_info         as sys_exc_info

                        try:

                            CL_cols                     =   [ it for it in TD["new"] if it.find('last_craigslist_')==0 and TD["new"][it] is not None ]
                            trigger_depth               =   plpy.execute('select pg_trigger_depth() res')[0]['res']
                            
                            if not TD["old"]:               return "OK"

                            for k,v in TD["new"].iteritems():
                                
                                if (TD["old"][k]!=v 
                                    and CL_cols.count(k)>0 
                                    and v):
                                                                        
                                    TD["new"]["last_craigslist"] = v
                                    return "MODIFY"

                            return "OK"                             # means unmodified

                        except plpy.SPIError:
                            plpy.log('z_keep_recent_craigslist FAILED')
                            plpy.log(tb_format_exc())
                            plpy.log(sys_exc_info()[0])
                            return


                        $funct$ language "plpythonu";

                        CREATE TRIGGER update_last_craigslist
                        BEFORE UPDATE or INSERT ON properties
                        FOR EACH ROW
                        EXECUTE PROCEDURE z_keep_recent_craigslist();

                    """

                    self.T.conn.set_isolation_level(       0)
                    self.T.cur.execute(                    a.replace('##','%'))
                    return
                    
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