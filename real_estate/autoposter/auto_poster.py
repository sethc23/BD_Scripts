#! /usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
# _ARC_DEBUG
"""

Manages Advertisement Syndication

"""

from os                             import environ          as os_environ
from sys                            import path             as py_path
py_path.append(                         os_environ['HOME'] + '/.scripts')
from system_argparse import *

# from IPython import embed_kernel as embed; embed()
try:
    from ipdb import set_trace as i_trace
except:
    pass
#i_trace()



class PP_Functions:
    """Functions for Managing Preview Boston Real Estate Properties"""

    def __init__(self,_parent,**kwargs):

        self.AP                             =   _parent
        self.T                              =   _parent.T
        # locals().update(                        self.T.__getdict__())
        self.PP                             =   self
        self.T.py_path.append(                  self.T.os_environ['BD'] + '/html')
        from HTML_API                           import getTagsByAttr,google,safe_url,getSoup
        import re
        from random                             import randrange
        
        all_imports                         =   locals().keys()
        for k in all_imports:
            if not self.T.has_key(k) and not k=='self':
                self.T.update(                  {k                      :   eval(k) })
        globals().update(                       self.T.__getdict__())

    def login(self):
        url                                 =   'http://previewbostonrealty.com/admin/login.php'
        self.T.br.open_page(                      url)
        uname                               =   self.T.br.window.find_element_by_name("ap_username")
        if uname.is_displayed():
            uname.send_keys('schase')
            self.T.br.window.find_element_by_name("ap_password").send_keys('B*_Realty')
            self.T.br.window.find_element_by_name("Submit").click()
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
        h                                   =   self.T.codecs.encode(self.T.br.source(),'utf8','ignore')
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
        if not self.T.br.get_url()==self.T.BASE_URL:
            self.T.br.open_page(self.T.BASE_URL)
        h                                       =   self.T.getSoup(self.T.br.source())
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

    def update_ads_from_account(self,account_type):
        def craigslist(self):

            login_page                      =   'https://accounts.craigslist.org/'
            now                             =   self.T.dt.datetime.now()
            # keep scraping last month and this month for the first week
            now                             =   now if now.day>7 else now+self.T.DU.relativedelta(months=-1)
            postings_link                   =   ''.join(['https://accounts.craigslist.org/login/home?',
                                                         'viewProfile=0&viewAccount=0',
                                                         'filter_page=%s',
                                                         '&filter_cat=0',
                                                         '&filter_active=0',
                                                         # '&filter_active=active',
                                                         #'&filter_active=inactive',
                                                         '&filter_date=%s-%s' % (now.year,"%02d" % now.month),
                                                         '&show_tab=postings'])

            self.T.br.window.get(                 login_page)
            try:
                self.T.br.window.find_element_by_id("inputEmailHandle").send_keys('seth.chase.boston@gmail.com')
                self.T.br.window.find_element_by_id("inputPassword").send_keys('B*_Realty')
                self.T.br.window.find_element_by_id("inputPassword").send_keys(self.T.br.keys.ENTER)
            except:
                pass

            self.T.br.window.get(                 postings_link % 1)

            while True:
                h                           =   self.T.getSoup(self.T.br.source())
                # Get Page/Paging Info
                postings_info               =   h.find_all('small')[0].text
                pages                       =   h.find_all('legend',attrs={'id':'paginator1'})[0]
                seg_start,seg_end,total_posts   =   [int(it) for it in self.T.re_findall(r'\d+',postings_info)]
                
                post_tbl                    =   h.find_all('table',attrs={'class':'accthp_postings'})[0]
                t                           =   ''.join([it.decode() for it in post_tbl.contents]
                                                            ).replace('tbody','table')
                tbl_rows                    =   post_tbl.find_all('tr')

                if not locals().keys().count('df'):
                    df                      =   self.T.pd.read_html(t,header=0)[0]
                    df.columns              =   ['_'+it.lstrip('_').lower().replace(' ','_') for it in df.columns.tolist()]
                    df['_posted_date']      =   df._posted_date.map(lambda d: self.T.DU.parse(d))
                    df['_manage']           =   [it.find_all('td')[1].decode() for it in tbl_rows[1:]]
                    df['_post_link']        =   map(lambda r: None if not r.a else None if not r.a.has_attr('href') else r.a.get('href'), [it.find_all('td')[2] for it in tbl_rows[1:]])
                else:
                    n_df                    =   self.T.pd.read_html(t,header=0)[0]
                    n_df.columns            =   ['_'+it.lstrip('_').lower().replace(' ','_') for it in n_df.columns.tolist()]
                    n_df['_posted_date']    =   n_df._posted_date.map(lambda d: self.T.DU.parse(d))
                    n_df['_post_link']      =   map(lambda r: None if not r.a else None if not r.a.has_attr('href') else r.a.get('href'), [it.find_all('td')[2] for it in tbl_rows[1:]])
                    n_df['_manage']         =   [it.find_all('td')[1].decode() for it in tbl_rows[1:]]
                    df                      =   df.append(n_df,ignore_index=True)

                for it in pages.descendants:
                    if it.name and str(it.text).count('postings'):
                        break
                    if it.name=='a' and it.text.isdigit():
                        last_page_link      =   int(it.text)
                    if it.name=='b' and it.text.isdigit():
                        current_page        =   int(it.text)
                
                if current_page>last_page_link:
                    break
                else:                   
                    self.T.br.window.find_element_by_link_text(str(current_page+1)).click()

            assert len(df)                 ==   total_posts
            df['_post_title']               =   df._posting_title
            df['_post_date']                =   df._posted_date
            

            # df['_url_display']              =   df._manage.map(lambda r: None if (len(r.find_all('form'))==1 
            #                                                                         and not r.input 
            #                                                                         and not r.input.has_attr('value')) 
            #                                                                     else r.input.get('value'))
            # df['_url_delete']               =   df._manage.map(lambda r: None if (len(r.find_all('form'))==3
            #                                                                         and not all([it.input for it in r.find_all('form')])
            #                                                                         and not all([it.input.has_attr('value') for it in r.find_all('form')]))
            #                                                                     else r.find_all('form')[0].input.get('value'))
            # df['_url_edit']                 =   df._manage.map(lambda r: None if (len(r.find_all('form'))==3
            #                                                                         and not all([it.input for it in r.find_all('form')])
            #                                                                         and not all([it.input.has_attr('value') for it in r.find_all('form')])) 
            #                                                                     else r.find_all('form')[1].input.get('value'))
            # df['_url_renew']                =   df._manage.map(lambda r: None if (len(r.find_all('form'))==3
            #                                                                         and not all([it.input for it in r.find_all('form')])
            #                                                                         and not all([it.input.has_attr('value') for it in r.find_all('form')])) 
            #                                                                     else r.find_all('form')[2].input.get('value'))

            df                                  =   df.ix[:,['_status','_post_title','_post_link','_post_date','_id','_manage']]
            
            upd_set                             =   ','.join(['%s = t.%s' % (it,it) for it in df.columns])
            ins_cols                            =   ','.join(df.columns)
            sel_cols                            =   ','.join(['t.%s' % it for it in df.columns])

            self.T.update(                          {'upd_set'              :   upd_set,
                                                     'ins_cols'             :   ins_cols,
                                                     'sel_cols'             :   sel_cols,})

            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     'drop table if exists %(tmp_tbl)s' % self.T)
            df.to_sql(                              self.T['tmp_tbl'],self.T.eng)
            
            # upsert to craigslist
            cmd                                 =   """
                                                    with upd as (
                                                        update craigslist p
                                                        set
                                                            %(upd_set)s
                                                        from %(tmp_tbl)s t
                                                        where p._id     =   t._id
                                                        returning t._id _id
                                                    )
                                                    insert into craigslist ( %(ins_cols)s )
                                                    select
                                                        %(sel_cols)s
                                                    from
                                                        %(tmp_tbl)s t,
                                                        (select array_agg(f._id) upd_ids from upd f) as f1
                                                    where (not upd_ids && array[t._id]
                                                        or upd_ids is null);

                                                    DROP TABLE %(tmp_tbl)s;
                                                    """ % self.T

            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     cmd)
            self.T.conn.set_isolation_level(        0)
            self.T.cur.execute(                     'drop table if exists %(tmp_tbl)s' % self.T)

            return

        def postlets(self):
            pass
        
        account_type                            =   account_type if type(account_type)==list else [account_type]
        if account_type.count('craigslist'):        craigslist(self)
        if account_type.count('postlets'):          postlets(self)

        return

    def update_ads_from_urls(self,chk_cnt='All'):
        """assumption is that this function will run on hourly crons. THIS TRIGGERS 'update_properties_by_cl_status'"""
        
        qry                                 =   """
                                                    with prop_data as (
                                                        select 
                                                            uid,url,last_craigslist_id
                                                            --posts,_keys,entries,entry_keys,
                                                            --post_data,
                                                            --url,last_craigslist_id
                                                        from (
                                                            select
                                                                uid,posts,_keys,entries,entry_keys,
                                                                entries::json->>entry_keys post_data,
                                                                (entries::json->>entry_keys)::json->>'url' url,
                                                                last_craigslist_id
                                                            from (
                                                                select 
                                                                    uid,posts,_keys,entries,
                                                                    json_object_keys(entries::json) entry_keys,
                                                                    last_craigslist_id
                                                                from (
                                                                    select 
                                                                        uid,posts,_keys,posts->>_keys entries,
                                                                        last_craigslist_id
                                                                    from (
                                                                        select 
                                                                            uid,posts,json_object_keys(posts::json) _keys,
                                                                            last_craigslist_id
                                                                        from properties
                                                                        where last_craigslist_id is not null
                                                                    ) f1
                                                                ) f2
                                                            ) f3
                                                        ) f4
                                                        where entry_keys ~* '^craigs'
                                                        and url ~* last_craigslist_id::text
                                                    )
                                                    SELECT c.uid cl_uid,p.url cl_url
                                                    FROM craigslist c,prop_data p
                                                    WHERE c._id = p.last_craigslist_id
                                                    AND c._status = 'Active'
                                                """
        df                                  =   self.T.pd.read_sql(qry,self.T.eng)
        chk_cnt                             =   len(df) if chk_cnt=='All' else chk_cnt
        df['idx']                           =   df.cl_uid.map(lambda s: self.T.randrange(0,len(df)*3))
        df                                  =   df.sort('idx').reset_index(drop=True).ix[:chk_cnt,:]
        start_time                          =   int((self.T.dt.datetime.now()-self.T.epoch).total_seconds())
        # endtime based on checking 100 ads / 40 min
        end_time                            =   start_time + ( int(round(len(df)/100.00,0)) * (60*40) )
        all_urls                            =   df.cl_url.tolist()
        self.T.update(                          {'proxy'                    :   self.AP.Config.get_proxy()})
        for i in range(0,len(all_urls)):

            self.T.update(                      {'try_loop_start'           :   int((self.T.dt.datetime.now()-self.T.epoch).total_seconds())})
            while True:
                try:
                    cmd                     =   ' '.join(
                                                    ['curl -s',
                                                     # '-x "%s"' % self.T.proxy,
                                                     '--max-time %s' % self.T.page_timeout,
                                                     '-H "Proxy-Connection:"',
                                                     '-A "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3"',
                                                     '"%s"' % all_urls[i],
                                                     '2>&1 || exit 9',
                                                     "| grep 'Seth Chase' | wc -l"]
                                                 )
                
                    (_out,_err) = self.T.exec_cmds([cmd])
                    assert _out.count('Timeout was reached')==0
                    assert _err is None
                    break
                except:
                    if int((self.T.dt.datetime.now()-self.T.epoch).total_seconds()) - self.T.try_loop_start > self.T.try_loop_max_time:
                        raise SystemError
                        break
                    else:
                        self.T.update(          {'proxy'                    :   self.AP.Config.get_proxy()})
            self.T.update(                      {'try_loop_start'           :   0})

            if not _out.strip('\n ') or _out.strip('\n ')=='0':
                self.T.conn.set_isolation_level(0)
                self.T.cur.execute(             """
                                                with upd as (
                                                    UPDATE craigslist SET _status='Deleted' WHERE uid = %s
                                                    RETURNING _property_id
                                                    )
                                                UPDATE properties SET cl_last_deleted=now() 
                                                FROM upd u
                                                WHERE _property_id = u._property_id;
                                                """ %  df.ix[i,'cl_uid'])

            delay_max = int( ( end_time - int((self.T.dt.datetime.now()-self.T.epoch).total_seconds()) ) /  (len(all_urls)-i) ) - 3 # 3 is transaction time buffer
            
            if delay_max>0:
                this_delay                  =   self.T.randrange(0,delay_max)
                # print i,_out.strip('\n '),this_delay,delay_max
                self.T.delay(                   this_delay)
            else:
                #print i,_out.strip('\n '),'no delay'
                pass

            if int((self.T.dt.datetime.now()-self.T.epoch).total_seconds())>end_time:
                # print 'finishing early? -- %s of %s' % (i,len(df))
                break
            
        # print int((self.T.dt.datetime.now()-self.T.epoch).total_seconds()),'finished'
        return

    def get_property_info(self,pd_row):
        self.T.br.open_page(                 'http://previewbostonrealty.com/admin/property_index.php')
        prop_field                      =   self.T.br.window.find_element_by_name("searchproperty_IDs")
        if prop_field.is_displayed():
            prop_field.send_keys(           pd_row['_property_id'])
            prop_field.send_keys(           self.T.br.keys.ENTER)
        return

    def post_ad(self,post_type):
        """Post ads on Craigslist or Postlets"""

        def update_pgsql_with_post_data(self,prop,D,src):
            # UPDATE PGSQL
            chk = ', pl_checked_out = null' if src=='postlets' else ', cl_checked_out = null'
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
                    uname                       =   self.T.br.window.find_element_by_id('username')
                    if uname.is_displayed():
                        uname.send_keys(            'seth.chase.boston@gmail.com')
                        self.T.br.window.find_element_by_id('password').send_keys('B*_Realty')
                        self.T.br.window.find_element_by_id('password').send_keys(self.T.br.keys.ENTER)
                except:
                    pass

            items                               =   self.T.pd.read_sql("""                  
                                                        UPDATE properties p1 SET pl_checked_out = '%s'
                                                        FROM 
                                                        (
                                                        SELECT * FROM properties p2
                                                        where 
                                                            p2.last_postlets is null
                                                            AND p2._beds >= 1
                                                            --AND length(p2._photos)>0
                                                            AND pl_checked_out is null
                                                        order by 
                                                            p2._rent DESC,p2._walk_score DESC,
                                                            p2._beds DESC,p2._avail_date ASC
                                                        limit 5
                                                        ) f1
                                                        WHERE p1.uid=f1.uid
                                                        returning p1.*;""" % self.T.guid,self.T.eng)
            if not len(items):                      return
            for idx,prop in items.iterrows():
                D                               =   {} if prop.posts is None else prop.posts                
                goto_url                        =   self.T.BASE_URL + "postlets.php?property_ID=%s" % prop['_property_id']
                self.T.br.open_page(                  goto_url)
                self.T.br.window.find_element_by_name("titlegen").click()
                self.T.br.window.find_element_by_name("make_postlet").click()

                # i_trace()
                # IF POSTLETS LOGIN HERE: re-init webdriver/login/post

                
                # GET PAGE POST INFO
                src                             =   self.T.br.source()
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

                # ACTIVATE AD
                self.T.br.window.find_element_by_partial_link_text('Activate Postlet').click()

                # LOGIN INTO POSTLETS IF NECESSARY
                login_postlets(                     self)

                # CONFIRMED POST
                self.T.br.window.find_element_by_class_name("closer").click()
                h                               =   self.T.getSoup(self.T.br.source())
                res                             =   h.findAll('div',attrs={'id':'activated-dialog'})
                try:
                    assert len(res)>0

                    post_url                    =   self.T.br.window.find_element_by_class_name('hdp-url').text
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
                self.T.br.window.find_element_by_id("inputEmailHandle").send_keys('seth.chase.boston@gmail.com')
                self.T.br.window.find_element_by_id("inputPassword").send_keys('B*_Realty')
                self.T.br.window.find_element_by_id("inputPassword").send_keys(self.T.br.keys.ENTER)

            items                               =   self.T.pd.read_sql("""                  
                                                        UPDATE properties p1 SET cl_checked_out = '%s'
                                                        FROM 
                                                        (
                                                        SELECT * FROM properties p2
                                                        where 
                                                            p2.last_craigslist_id is null
                                                            AND p2.cl_post_cnt < 2
                                                            AND p2._beds >= 1
                                                            AND length(p2._photos)>0
                                                            AND cl_checked_out is null
                                                        order by 
                                                            p2._rent DESC,p2._walk_score DESC,
                                                            p2._beds DESC,p2._avail_date ASC
                                                        limit 10
                                                        ) f1
                                                        WHERE p1.uid=f1.uid
                                                        returning p1.*;
                                                        """%  self.T.guid,self.T.eng)

            if not len(items):                      return
            
            h                                       =   self.T.getSoup(self.T.br.source())
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
                select_tag                      =   self.T.br.window.find_element_by_xpath(select_path)
                to_name                         =   select_tag.get_attribute('name').replace(str(res_id),str(prop['_property_id']))
                self.T.br.window.execute_script(      "arguments[0].setAttribute('name', arguments[1])", select_tag, to_name)
                to_id                           =   select_tag.get_attribute('id').replace(str(res_id),str(prop['_property_id']))
                self.T.br.window.execute_script(      "arguments[0].setAttribute('id', arguments[1])", select_tag, to_id)
                # Change value of first option
                option_1_path                   =   select_path + "/option[1]"
                option_1_tag                    =   self.T.br.window.find_element_by_xpath(option_1_path)
                self.T.br.window.execute_script(      "arguments[0].setAttribute('value', arguments[1])", option_1_tag, goto_url)
                # Change name and onclick for submit button
                button_path                     =   first_row_path + "/input"
                button_tag                      =   self.T.br.window.find_element_by_xpath(button_path)
                to_name                         =   button_tag.get_attribute('name').replace(str(res_id),str(prop['_property_id']))
                self.T.br.window.execute_script(      "arguments[0].setAttribute('name', arguments[1])", button_tag, to_name)
                to_onclick                      =   button_tag.get_attribute('onclick').replace(str(res_id),str(prop['_property_id']))
                self.T.br.window.execute_script(      "arguments[0].setAttribute('onclick', arguments[1])", button_tag, to_onclick)
                # Update Replace Marker
                res_id                          =   str(prop['_property_id'])
                button_tag.click(                   )

                # Move to new window
                self.T.delay(                       2)
                self.T.br.wait_for_page(              )
                assert self.T.br.window_count()   ==  2
                orig_window                     =   self.T.br.window.current_window_handle
                new_window                      =   [it for it in self.T.br.window.window_handles if it!=orig_window][0]
                self.T.br.window.switch_to_window(    new_window)
                
                # Check for Errors
                if self.T.br.source().find('posting aborted')!=-1:
                    x                           =   self.T.br.source()
                    b                           =   x.find('posting aborted')
                    a                           =   x[:b].rfind('<br')+3
                    msg                         =   x[a:b].strip('/ <>\n-').replace("'","")
                    tuid                        =   int((self.T.dt.datetime.now()-self.T.epoch).total_seconds())
                    D.update({                      tuid                :       {post_type     :   """ERROR: %s""" % msg} })
                    
                    update_pgsql_with_post_data(    self,prop,D,'craigslist')
                    self.T.br.window.close(           )
                    self.T.br.window.switch_to_window(orig_window)

                else:

                    # Make title for ad
                    for i in range(3):
                        self.T.br.window.find_element_by_name("titlegen").click()
                    self.T.delay(                       2)
                    self.T.br.wait_for_page(              )
                    ad_title                =   str(self.T.br.window.find_element_by_id('title').get_attribute('value')).replace("'","''")
                    assert ad_title        is   not None
                    
                    # Submit PP page for CL
                    self.T.br.window.find_element_by_id("submitbutton").click()
                    self.T.delay(                2)
                    self.T.br.wait_for_page(     )

                    # ...page runs a script and finally shows a windowed CL page
                    
                    # Submit CL pictures
                    self.T.br.window.find_element_by_name("go").click()
                    self.T.delay(                2)
                    self.T.br.wait_for_page(     )

                    try:
                        self.T.br.window.find_element_by_partial_link_text('log in to your account').click()
                        self.T.delay(            2)
                        login_craigslist(        self)
                    except:
                        pass              
                    
                    # Option to Change/Re-Order pictures (click bottom button) [ Scroll to Bottom...]
                    a                       =   self.br.window.execute_script('return document.body.scrollHeight;')
                    self.br.window.execute_script("window.scrollTo(%s, document.body.scrollHeight);" % str(a))
                    # self.T.br.window.find_elements_by_tag_name('button')[-1].click()
                    self.br.window.find_element_by_class_name('done bigbutton').click()
                    self.T.delay(                       2)
                    self.T.br.wait_for_page(              )

                    # Click to publish ad
                    self.T.br.window.find_elements_by_tag_name('button')[0].click()
                    self.T.delay(                       2)
                    self.T.br.wait_for_page(              )

                    try:
                        h                   =   self.T.getSoup(self.T.br.source())
                        post_url            =   h.findAll(href=self.T.re.compile('\.html'))[0].get('href')
                    except:
                        post_url            =   "ERROR: couldn''t obtain link"
                    tuid                    =   int((self.T.dt.datetime.now()-self.T.epoch).total_seconds())
                    D.update({                          tuid                :       {post_type     :   {'url':post_url,'ad_title':ad_title} } })
                    
                    update_pgsql_with_post_data(self,prop,D,'craigslist')
                    self.T.br.window.close(          )
                    self.T.br.window.switch_to_window(    orig_window)

                self.T.delay(                   2*60)

            return

        if not hasattr(self,'logged_in'):
            self.logged_in                  =   self.login()

        self.post_settings                  =   eval(self.T.pd.read_sql("""
                                                        select _value r 
                                                        from pp_settings 
                                                        where _setting = 'post_urls'
                                                        """,self.T.eng).r.tolist()[0])

        post_type                           =   post_type if type(post_type)==list else [post_type]
        if post_type.count('postlets'):             postlets(self)
        if post_type.count('craigslist'):           craigslist(self)

        return

    def run_search(self,**kwargs):
        if not hasattr(self,'logged_in'):
            self.logged_in                      =   self.login()
        self.T.br.open_page(                          self.T.SEARCH_URL)

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
        h                                   =   self.T.re_sub(r'[^\x00-\x7F]+',' ',self.T.codecs.encode(self.T.br.source(),'utf8','ignore'))
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

        self.T.br.quit()

class Auto_Poster:
    """Main Class for Initiating & Managing AutoPoster

        Examples:
            Auto_Poster('chrome',no_identity=True)
    """

    def __init__(self,browser_type=None,**kwargs):
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
        import                                  requests
        from json                           import dumps            as j_dump
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
        py_path.append(                         os_environ['HOME'] + '/.scripts')
        from System_Control                 import Google
        from py_classes                     import To_Class
        from System_Control                 import System_Admin
        
        DB                                  =   'autoposter'
        D                                   =   {'exec_cmds'            :   System_Admin().exec_cmds,
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
        for k,v in kwargs.iteritems():
            self.T.update(                      { 'kw_' + k             :   v})
        all_imports                         =   locals().keys() #+ globals().keys()
        for k in all_imports:
            if not k=='D' and not k=='self':
                self.T.update(                  {k                      :   eval(k) })
        globals().update(                       self.T.__getdict__())
        self.pgSQL                          =   self.pgSQL(self)
        self.Config                         =   self.Config(self)
        self.Maintenance                    =   self.Maintenance(self)
        self.Identity                       =   self.Identity(self)
        self.VPN                            =   self.VPN(self)
        self.PP                             =   PP_Functions(self,**kwargs)
        self.gmail                          =   Google.Gmail(_parent=self,kwargs={'username'    :   'seth.chase.boston@gmail.com',
                                                                                  'pw'          :   'uwejjozvkkcahgrj'})
        self.logged_in                      =   False

        # if not hasattr(self.T,'kw_no_identity'):
        self.T.id                           =   self.Identity.get()
        browser_class                       =   self.Browser(self)
        self.T.br                           =   browser_class.build()

        globals().update(                       self.T.__getdict__())

        # all_imports                         =   locals().keys()
        # for k in all_imports:
        #     if not k=='D':
        #         self.T.update(                  {k                      :   eval(k) })

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
                                                uid,to_timestamp(times::double precision) at time zone 'utc' post_time,json_object_keys( posts::json -> times ) post_type,
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
                    a="""
                        DROP FUNCTION if exists z_keep_recent_craigslist() cascade;
                        DROP TRIGGER if exists update_last_craigslist ON properties;

                        CREATE OR REPLACE FUNCTION z_keep_recent_craigslist()
                        RETURNS TRIGGER AS $funct$

                        from os                             import system           as os_cmd
                        from traceback                      import format_exc       as tb_format_exc
                        from sys                            import exc_info         as sys_exc_info
                        #import                                  datetime            as dt
                        #epoch                               =   dt.datetime.now().utcfromtimestamp(0)
                        #from dateutil                       import parser           as DU
                        #import pytz

                        try:

                            CL_cols                             =   [ it for it in TD["new"] if it.find('last_craigslist_')==0 and TD["new"][it] is not None ]
                            trigger_depth                       =   plpy.execute('select pg_trigger_depth() res')[0]['res']
                            
                            if (not TD["old"]
                                or TD["new"]["last_craigslist"]==TD["old"]["last_craigslist"]
                                or trigger_depth>1
                                ):               return "OK"

                            for k,v in TD["new"].iteritems():
                                
                                if (TD["old"][k]!=v 
                                    and CL_cols.count(k)>0 
                                    and v):
                                                                        
                                    TD["new"]["last_craigslist"]    =   v
                                    
                                    D                               =   eval(TD["new"]["posts"])
                                    latest                          =   sorted(D.keys(),reverse=True)
                                    for it in latest:
                                        if D[it].keys()[0].count('craigslist'):
                                            post_link               =   D[it][D[it].keys()[0]]
                                            break

                                    TD["new"]["last_craigslist_id"] =   int(post_link[post_link.rfind('/')+1:-5])

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
                def update_properties_by_cl_status(self):
                    """When 'craiglist' table updated with _status='Deleted', with 'properties': update 'posts' with 'deleted'
                    clear 'last_craigslist_id', (NOT CLEARING 'last_craigslist'). """
                    a="""
                        DROP FUNCTION if exists z_update_properties_by_cl_status() cascade;
                        DROP TRIGGER if exists update_properties_by_cl_status ON craigslist;

                        CREATE OR REPLACE FUNCTION z_update_properties_by_cl_status()
                        RETURNS TRIGGER AS $funct$

                        from os                             import system           as os_cmd
                        from traceback                      import format_exc       as tb_format_exc
                        from sys                            import exc_info         as sys_exc_info

                        try:

                            trigger_depth               =   plpy.execute('select pg_trigger_depth() res')[0]['res']
                            
                            if (not TD["old"]
                                or TD["old"]["_status"]==TD["new"]["_status"]
                                or trigger_depth>1):        return "OK"

                            if TD["new"]["_status"]=='Deleted':
                                P = \"\"\"
                                    
                                    WITH upd as (

                                        select
                                            json_update(
                                                posts::json,
                                                    concat(
                                                    '{"',
                                                    _keys,
                                                    '": ',

                                                        concat(
                                                        '{"',
                                                        entry_keys,
                                                        '": ',
                                                        json_append(post_data::json,concat('{"Deleted":"',(select now())::text,'"}')::json),
                                                        '}'),

                                                    '}')::json
                                                ) updated_post,
                                            uid,posts,_keys,entries,entry_keys,post_data,url
                                        from (
                                         select
                                            uid,posts,_keys,entries,entry_keys,
                                            entries::json->>entry_keys post_data,
                                            (entries::json->>entry_keys)::json->>'url' url
                                            --,json_object_keys( (entries::json->>entry_keys)::json ) post_data_keys
                                         from (
                                             select uid,posts,_keys,entries,
                                             json_object_keys(entries::json) entry_keys
                                             from (
                                                 select uid,posts,_keys,posts->>_keys entries
                                                 from (
                                                     select uid,posts,json_object_keys(posts::json) _keys
                                                     from properties
                                                     where last_craigslist_id = ##(_id)s
                                                ) f1
                                             ) f2
                                         ) f3
                                         
                                        ) f4
                                        where entry_keys ~* '^craigs' and url ~* '##(_id)s.html$'
                                    )

                                    UPDATE properties p SET 
                                        posts = u.updated_post::jsonb,
                                        last_craigslist_id = NULL
                                        --,last_craigslist = NULL
                                    FROM upd u
                                    WHERE p.uid=u.uid
                                    
                                    \"\"\" ## {'_id':TD["new"]["_id"]}
                                plpy.execute(P)

                            return "OK"                             # means unmodified

                        except plpy.SPIError:
                            plpy.log('update_properties_by_cl_status FAILED')
                            plpy.log(tb_format_exc())
                            plpy.log(sys_exc_info()[0])
                            return

                        $funct$ language "plpythonu";

                        CREATE TRIGGER update_properties_by_cl_status
                        BEFORE UPDATE or INSERT ON craigslist
                        FOR EACH ROW
                        EXECUTE PROCEDURE z_update_properties_by_cl_status();

                    """

                    self.T.conn.set_isolation_level(       0)
                    self.T.cur.execute(                    a.replace('####','%%').replace('##','%'))
                    return
    
    class Config:

        def __init__(self,_parent):
            self.AP                         =   _parent
            self.T                          =   _parent.T
            
            self.T.update(                      {'page_timeout'             :   30,
                                                 'try_loop_max_time'        :   2*60})
            self.Config                     =   self

        def update_proxies(self):
            cmd                             =   ' '.join(['python elite_proxy_finder.py -s 25',
                                                '| grep "^[[:digit:]]"',
                                                "| sed -E 's/ .*//g';"])
            (_out,_err)                     =   self.T.exec_cmds([cmd])
            self.T["proxies"]               =   ['http://'+it for it in _out.strip('\n').split('\n')]
            self.T.conn.set_isolation_level(    0)
            self.T.cur.execute(                 "UPDATE pp_settings SET _list=array%(proxies)s" % self.T)
            return

        def get_proxies(self,_parent):
            if not hasattr(_parent.T,'proxies'):
                _parent.T['proxies']        =   _parent.T.pd.read_sql("""SELECT _list l 
                                                                      FROM pp_settings 
                                                                      WHERE _setting='working_proxies'
                                                                      """,_parent.T.eng).l[0]
            if len(_parent.T['proxies'])==0:
                _parent.update_proxies(         )
            
            _parent.T['proxy']              =   _parent.T['proxies'].pop(0)
            return _parent

        def get_proxy(self,new=True,timeout=5):
            df                              =   self.T.pd.read_sql("select _setting,_list from pp_settings where _setting = any(array['working_proxies','failed_proxies'])",self.T.eng)
            if new or len(df[df._setting=='working_proxies']._list.iloc[0])>25:
                known_proxies               =   df._list[0] + df._list[1]
                failed_proxies              =   []
                user_id                     =   str(self.T.get_guid().hex)
                url                         =   'http://gimmeproxy.com/api/get/%s/?timeout=%s'%(user_id,timeout)
                cmd                         =   ' '.join(["curl -s '%s'" % url])
                self.T.update(                  {'try_loop_start'           :   int((self.T.dt.datetime.now()-self.T.epoch).total_seconds())})
                while True:
                    res                     =   self.T.exec_cmds([cmd])[0]
                    res                     =   eval(res)
                    proxies                 =   {'http':res['curl']}

                    try:
                        assert known_proxies.count(proxies['http'])==0
                        req                 =   self.T.requests.get('https://accounts.craigslist.org/login/home',timeout=timeout,proxies=proxies)
                        assert req.ok      ==   True
                        assert req.content.count('<title>craigslist: account log in</title>')>0
                        # i_trace()
                        break
                    except:
                        failed_proxies.append(  proxies['http'])
                        if int((self.T.dt.datetime.now()-self.T.epoch).total_seconds()) - self.T.try_loop_start > self.T.try_loop_max_time:
                            raise SystemError
                            break
                        else:
                            pass
                    # except self.T.requests.exceptions.ConnectionError as e:
                    #     if e.message.reason.args[0]=='Cannot connect to proxy.':
                    #         failed_proxies.append(proxies['http'])
                    #         print 'failed',i
                    # except self.T.requests.exceptions.Timeout as e:
                    #     print 'timeout'
                    #     failed_proxies.append(  proxies['http'])
                    # except AssertionError:
                    #     print 'some request error'
                self.T.update(                  {'try_loop_start'           :   0})
                if failed_proxies:
                    cmd                     =   """
                        WITH upd AS (
                            UPDATE pp_settings set _list = array_cat(_list,array%(proxy)s)
                            WHERE _setting = 'failed_proxies'
                            RETURNING uid
                            )
                        INSERT INTO pp_settings (_setting,_list)
                        SELECT 'failed_proxies',array%(proxy)s
                        FROM (select array_agg(uid) all_uids from upd) f1
                        WHERE all_uids is null
                                                """ % {'proxy':str(failed_proxies)}

                    self.T.conn.set_isolation_level(0)
                    self.T.cur.execute(          cmd)

                if not locals().keys().count('req'):
                    raise SystemExit
                    return False

                if req.ok:
                    cmd                             =   """
                        WITH upd AS (
                            UPDATE pp_settings set _list = array_cat(_list,array%(proxy)s)
                            WHERE _setting = 'working_proxies'
                            RETURNING uid
                            )
                        INSERT INTO pp_settings (_setting,_list)
                        SELECT 'working_proxies',array%(proxy)s
                        FROM (select array_agg(uid) all_uids from upd) f1
                        WHERE all_uids is null
                                                        """ % {'proxy':str([proxies['http']])}

                    self.T.conn.set_isolation_level(0)
                    self.T.cur.execute(         cmd)
                    return proxies['http']
                    # self.T.update(              {'proxy'                    :   proxies['http']})
            else:
                working_proxies             =   df[df._setting=='working_proxies']._list.iloc[0]
                random_proxy                =   working_proxies[self.T.randrange(0,len(working_proxies))]
                # self.T.update(                  {'proxy'                    :   proxies['http']})
                return random_proxy
            
            return False

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

        def check_cl_connection(self):
            
            i_trace()

    class VPN:

        def __init__(self,_parent):
            # for attr, value in _parent.__dict__.iteritems():
            #     setattr(self,attr,value)
            self._parent                    =   _parent
            self.T                          =   _parent.T
            self.vpn_cfg_path               =   '/etc/openvpn/hma'
            self.vpn_exec_path              =   '%s/vpns'                   %   os_environ['PWD']
            self.credentials                =   '%s/.vpnpass'               %   self.T.os_environ['HOME']

        def check_config(self):
            #files exist:
            chk_files = ['%s/.vpnpass' % self.T.os_environ['HOME'],
                         '/etc/openvpn/update-resolv-conf.sh',
                         '/etc/openvpn/hma/']

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
            df['_server']                       =   df._local.map(lambda s: self.T.re_sub(r'(LOC[0-9]+)(S[0-9]+)',r'\2',s))
            df['_local']                        =   df._local.map(lambda s: self.T.re_sub(r'(LOC[0-9]+)(S[0-9]+)',r'\1',s))

            ndf                                 =   df[(df._local.isnull()==False)&(df._country=='USA')].reset_index(drop=True)
            ndf['_state_abbr']                  =   ndf._state.map(lambda s: self.T.US.states.lookup(s).abbr)
            ndf['_city']                        =   ndf._city.map(lambda s: s if not s or not s.count('_') else s[:s.find('_')])
            ndf['_file']                        =   ndf._file.map(lambda s: info_path + '/%s' % s)

            self.results                        =   ndf
            self.upsert_to_pgsql(                   )
            
            return True

        def find_cl_compatible_vpn(self,_parent=None):
            # CONFIRM NO EXISTING VPN ACTIVE
            # cmd                             =   ['%s/hma_vpn.sh -s' %   self.vpn_exec_path,]
            # (_out,_err)                     =   self.T.exec_cmds(cmd,root=True)
            # assert _out.count('Connected to')==0

            if not hasattr(self.T,'id'):
                self.T.id                   =   self._parent.Identity.get()
            if _parent and hasattr(_parent.T,'id'):
                self.T.id                   =   _parent.T.id

            vpns                            =   self.T.pd.read_sql("""
                                                                   select * from vpns where _state_abbr='%(state_abbr)s'
                                                                   """      %   self.T.id.details,self.T.eng)
            chk_page                        =   'https://accounts.craigslist.org/'

            ## ---------  TEST BROWSER CONFIG ---------

            # for idx,row in vpns.iterrows():
            #
            #     # START SERVER
            #     cmd                         =   [' '.join([
            #                                         'sudo %s/hma_vpn.sh'    %   self.vpn_exec_path,
            #                                         '-d -c ~/.vpnpass -p tcp %(_state)s.*%(_city)s.*%(_local)s %(_server)s' % row])]
            #     (_out,_err)                 =   self.T.exec_cmds(cmd,root=True)
            #     assert _err is None
            #     assert _out.count('Connecting to')>0
            #
            #     # WAIT FOR CONNECTION OR ERROR
            #     wait_time                   =   3*60 # 3 minute wait
            #     end_time                    =   self.T.time.time() + wait_time
            #     while True:
            #
            #         if self.T.time.time()>end_time:
            #             self.T.id.ip_addr   =   ''
            #             break
            #
            #         cmd                     =   ['%s/hma_vpn.sh -s' %   self.vpn_exec_path,]
            #         (_out,_err)             =   self.T.exec_cmds(cmd,root=True)
            #         assert _err is None
            #
            #         if _out.count('Connected to')>0:
            #             (_out,_err)         =   self.T.exec_cmds(['bash -l -i -c "get_my_ip_ext 2>&1"'])
            #             assert _err is None
            #             self.T.id.ip_addr   =   _out.rstrip('\n')
            #             break
            #         else:
            #             self.T.delay(           5)
            #
            #     nbr                         =   self._parent._parent.Browser(self).build()
            #
            # ---------  TEST BROWSER CONFIG ---------

            self.T.browser_type='chrome'
            nbr                             =   self._parent._parent.Browser(self).build()
            nbr.open_page(                      'https://panopticlick.eff.org/index.php?action=log&js=yes')
            i_trace()

            return self.T.id.details.vpn

    class Identity:
        
        def __init__(self,_parent):
            self._parent                    =   _parent
            self.T                          =   _parent.T
            from faker                      import Factory                  as fake_factory
            import us                                                       as US
            from pyzipcode                  import ZipCodeDatabase
            F                               =   fake_factory.create()
            Z                               =   ZipCodeDatabase()
            US                              =   US
            self.Create                     =   self.Create(self)
            self.identity_path              =   self.T.os_environ['BD']     +   '/real_estate/autoposter/identities'
            self.VPN                        =   self._parent.VPN(self)

            all_imports                     =   locals().keys()
            for k in all_imports:
                if not k=='D' and not k=='self':
                    self.T.update(              {k                      :   eval(k) })
            globals().update(                   self.T.__getdict__())

        def get(self):
            if (
                #not self.T.browser_type
                not hasattr(self.T,'kw_identity')
                and not hasattr(self.T,'id')
                ):
                return

            D                               =   self.T.pd.read_sql("""  select * from identities 
                                                                        where guid='%s'""" % self.T.kw_identity,
                                                                        self.T.eng).iloc[0,:].to_dict()
            
            self.T.id                       =   self.T.To_Class({}) if not hasattr(self.T,'id') else self.T.id
            for k,v in D.iteritems():
                if ['guid','email','pw','details'].count(k):
                    setattr(                    self.T.id,k,v)

            D                               =   self.T.id.details
            self.T.id.details               =   self.T.To_Class({})
            for k,v in D.iteritems():
                setattr(                        self.T.id.details,k.lstrip('_'),v)

            assert hasattr(self.T.id,'cookie')


            if not hasattr(self.T.id.details,'vpn') or not self.T.id.details.vpn:
                self.T.id.details.vpn       =   self._parent.VPN.find_cl_compatible_vpn(self)

            return self.T.id

        class Create:

            def __init__(self,_parent):
                # self = self.T.To_Cass(_parent.__dict__)
                self._parent                =   _parent
                self.T                      =   _parent.T
                # for attr, value in _parent.__dict__.iteritems():
                    # setattr(self,attr,value)

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
                self.T.py_path.append(          self.T.os_environ['BD']+'/google')
                from google_main            import Google
                g                           =   Google(self)
                g.Gmail.create_account(         )
                i_trace()
                return '34744f6@gmail.com'

            def user_profile(self):
                def make_user_details():
                    D                       =   {#'_user_name'               :   self.email[:self.email.find('@')],
                                                 '_BASE_DIR'                :   self.T.os_environ['SERV_HOME'] + '/autoposter/identities',
                                                 '_user_agent'              :   self.T.F.user_agent().replace("'",'')}
                    D.update(                   {'_SAVE_DIR'                :   '%s/%s' % (D['_BASE_DIR'],self.T.id.guid)})
                    vpns                    =   self.T.pd.read_sql("select * from vpns where _type='TCP'",self.T.eng)
                    avail_states            =   map(lambda s: self.T.re_sub(r'([A-Z][a-z]+)([A-Z][a-z]+)',r'\1 \2',s),
                                                                            map(lambda s: s.replace(' ',''),vpns._state_abbr.unique().tolist()))
                    # Get State Where a Server Exists
                    while True:
                        _state_abbr         =   self.T.F.state_abbr()
                        if avail_states.count(_state_abbr):
                            break
                    D.update(                   {'_state_abbr'              :   _state_abbr })

                    # Get Zipcode within State
                    while True:
                        z                   =   self.T.F.zipcode()
                        chk                 =   self.T.Z.get(z)
                        if chk and chk[0].state==D['_state_abbr']:
                            break

                    D.update(                   {'_country'                 :   'US',
                                                 '_state'                   :   self.T.US.states.lookup(D['_state_abbr']).name,
                                                 '_city'                    :   self.T.Z.get(z)[0].city.replace('/','\/').replace("'",''),
                                                 '_org'                     :   self.T.F.company().replace('/','\/').replace("'",''),
                                                 '_org_unit'                :   self.T.F.job().replace('/','\/').replace("'",''),
                                                })
                    g                       =   self.T.randrange(0,2)
                    name                    =   self.T.F.name_female() if g==0 else self.T.F.name_male()
                    while len(name.split())!=2:
                        name                =   self.T.F.name_female() if g==0 else self.T.F.name_male()
                    first,last              =   name.replace("'",'').split()
                    D.update(                   {'_first_name'              :   first,
                                                 '_last_name'               :   last,
                                                 '_name'                    :   ' '.join([first,last])})
                    return D
                def update_pgsql_with_details(D=None):
                    if not D:
                        D                   =   self.T.id.details
                    cmd                     =   """
                                                    WITH
                                                        upd_new_details as (
                                                            UPDATE identities
                                                            SET details = '%(details)s'::jsonb
                                                            WHERE guid = '%(guid)s'::text
                                                            AND details is null
                                                            RETURNING guid
                                                        ),
                                                        upd_existing_details as (
                                                            SELECT
                                                                json_merge(i.details::json,'%(details)s'::json),
                                                                '%(guid)s'::text guid
                                                            FROM identities i
                                                            WHERE guid = '%(guid)s'::text
                                                            AND details is not null
                                                        )
                                                    INSERT  INTO identities(guid,details)
                                                    SELECT  f.guid,f.details
                                                    FROM    (SELECT  '%(guid)s'::text guid,'%(details)s'::jsonb details) f
                                                    WHERE   NOT f.guid in (select guid from upd_new_details)
                                                    AND     NOT f.guid in (select guid from upd_existing_details)
                                                """ % {'details':self.T.j_dump(D),'guid':self.T.id.guid}
                    self.T.conn.set_isolation_level(    0)
                    self.T.cur.execute(                 cmd)

                self.T['id']                =   self.T.To_Class({})

                if hasattr(self.T,'kw_identity'):
                    self.T.id.guid          =   self.T.kw_identity
                    self.T.id.email         =   '%s@gmail.com'%self.T.kw_identity
                    ids                     =   self.T.pd.read_sql("select * from identities where guid='%(kw_identity)s'"%self.T,self.T.eng)
                else:
                    self.T.id.guid          =   str(self.T.get_guid().hex)[:7]
                    self.T.id.email         =   '%s@gmail.com'%self.T.id.guid
                    self.T.id.details       =   make_user_details()
                    update_pgsql_with_details(  )
                    ids                     =   self.T.pd.read_sql("select * from identities where guid='%(guid)s'"%self.T.id,self.T.eng)

                if not ids.details[0]:
                    D                       =   make_user_details()
                    update_pgsql_with_details(  )
                else:
                    D                       =   ids.details[0]

                self.T.id.details           =   self.T.To_Class({})
                for k,v in D.iteritems():
                    self.T.id.details.update(   {k.lstrip('_')              :   v})

                return self.T.id

            def cookie(self):
                f_path                      =   '%s/%s/%s/%s.cookie' % (self.T.os_environ['BD'],
                                                                         'real_estate/autoposter/identities',
                                                                         self.T.id.guid,
                                                                         self.T.id.guid)
                cmds                        =   ['mkdir -p %s;' % f_path[:f_path.rfind('/')],
                                                 ':> %s;' % f_path]
                (_out,_err)                 =   self.T.exec_cmds(cmds)
                assert not _out
                assert _err is None
                self.T.id.cookie            =   self.T.To_Class({})
                self.T.id.cookie.f_path     =   f_path
                self.T.id.cookie.content    =   {}
                return self.T.id.cookie

            def ssl_cert(self):
                self.T.id.details.update(       {'email'                    :   self.T.id.email})
                cmds                        =   ['mkdir -p %(SAVE_DIR)s && cd %(SAVE_DIR)s && rm -f ./*;' % self.T.id.details,
                                                 'openssl genrsa -out %(guid)s.key 4096 > /dev/null 2>&1;' % self.T.id,
                                                 ' '.join(['openssl req -x509 -new -nodes',
                                                         '-key %(guid)s.key -days 1024' % self.T.id,
                                                         '-out %(guid)s.pem' % self.T.id,
                                                         '-subj "/C=%(country)s/ST=%(state)s/L=%(city)s/O=%(org)s/OU=%(org_unit)s/CN=%(name)s/emailAddress=%(email)s";' % self.T.id.details])
                                                ]
                (_out,_err)                 =   self.T.exec_cmds(cmds)
                assert not _out
                assert _err                 is  None
                return '%s/%s.pem'          %   (self.T.id.details.SAVE_DIR,self.T.id.guid)

            def vpn_connection(self):
                self._parent.VPN.find_cl_compatible_vpn(self)

            def new(self):
                self.T.id                   =   self.user_profile()

                # self.guid                       =   str(self.T.get_guid().hex)[:7]
                # self.T.conn.set_isolation_level(    0)
                # self.T.cur.execute(                 "INSERT INTO identities (guid) VALUES ('%s');" % self.guid)
                # self.id.guid='e3e1ed2'
                # self.id.details={"_org": "Ratke Inc", 
                #             "_city": "Tillamook", 
                #             "_name": "Ms. Theodora Lemke PhD", 
                #             "_email": "e3e1ed2@gmail.com", 
                #             "_state": "Oregon", 
                #             "_country": "US", 
                #             "_BASE_DIR": "/home/ub1/SERVER1/autoposter/identities", 
                #             "_SAVE_DIR": "/home/ub1/SERVER1/autoposter/identities/e3e1ed2", 
                #             "_org_unit": "Theme park manager", 
                #             "_user_name": "e3e1ed2", 
                #             "_state_abbr": "OR", 
                #             "_user_agent": "Mozilla/5.0 (Windows CE) AppleWebKit/5312 (KHTML, like Gecko) Chrome/15.0.874.0 Safari/5312"}

                self.T.id.cookie            =   self.cookie()
                self.T.id.ssl_cert          =   self.ssl_cert()
                self.id.vpn                 =   self.vpn_connection()
                self.email                  =   self.gmail_act()
                self.cl                     =   self.craigslist_act()

                return self

    class Browser:

        def __init__(self,_parent):
            self.T                          =   _parent.T
            from webpage_scrape                 import scraper
            self.T.scraper                  =   scraper

        def build(self,**kwargs):
            def chrome():
                return self.T.scraper('chrome',**self.T.__dict__).browser

            def phantom():
                self.T['br']                =   self.T.To_Class({})
                if not self.T.id:
                    self.T.br.user_agent        =   self.T._parent.Identity.F.user_agent()
                    self.T.br['service_args']   =   self.T.To_Class({})
                else:
                    self.T.br.user_agent        =   self.T.id.details.user_agent
                    self.T.br['service_args']   =   self.T.To_Class(
                                                        {'ignore_ssl_errors'        :   True,
                                                         'load_images'              :   True,
                                                         #'debugger_port'            :   9901,
                                                         'wd_log_level'             :   'DEBUG',
                                                         'ssl_cert_path'            :   '%s/%s.pem' % (self.T.id.details.SAVE_DIR,
                                                                                                       self.T.id.guid),
                                                         'cookie_file'              :   '%s/%s.cookie' % (self.T.id.details.SAVE_DIR,
                                                                                                          self.T.id.guid),})

                self.T.br['capabilities']       =   ['applicationCacheEnabled',
                                                     'databaseEnabled',
                                                     'webStorageEnabled',
                                                     'acceptSslCerts',
                                                     'browserConnectionEnabled',
                                                     'rotatable']

                self.T.br['browser_config']     =   {'window_size'              :   (300,300),
                                                     'implicitly_wait'          :   120,
                                                     'page_load_timeout'        :   150}

                self.T.br                       =   self.T.scraper('phantom',**self.T.__dict__).browser
                return self.T.br

            for k,v in kwargs.iteritems():
                self.T.update(                  {k                  :   v})

            # CASE WHERE browser_type != ''
            if not self.T.browser_type:         return None

            else:
                
                if not hasattr(self.T,'id'):
                    if hasattr(self.T,'kw_identity'):
                        D                       =   self.T.pd.read_sql("""select * from identities 
                                                                      where guid='%(kw_identity)s'"""%self.T,
                                                                   self.T.eng).ix[0,:].to_dict()
                        self.T.id               =   self.T.To_Class({})
                        for it in ['guid','email','pw','details']:
                            setattr(                self.T.id,it,D[it])
                    else:
                        self.AP.Identity.Create.new()


            if self.T.browser_type=='phantom':                              return phantom()
            if self.T.browser_type=='chrome':                               return chrome()
            #
            # if self.T.browser_type=='phantom':
            #     self.T.br                   =   phantom()
            #
            # return self.T.br
                


if __name__ == '__main__':
    
    # run_custom_argparse()
    
    x                                       =   Auto_Poster('phantom',identity='34744f6')
    x.VPN.find_cl_compatible_vpn()
    
    # x                                       =   Auto_Poster()
    # from webpage_scrape import Nginx
    # N = Nginx(x)
    # N.reload()
    i_trace()
    