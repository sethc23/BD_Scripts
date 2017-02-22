#!env python

"""
    from relativity import *
    R=Relativity()
    R.start()
    T=R.T
    br=R.br
    PG=R.pg.PG
    E=br.execute
    self=R


    # Get/Check Current Tags
    tdf=T.pd.DataFrame(E("return create_code_tag_arr();"))
    if len(tdf[(tdf.tag_selected==True) & (df.tag_text=='Non-Responsive')]):
        E("save_next();")


    # DOC DATA
    df = T.pd.DataFrame(E("return get_doc_data();"))


    # BATCH DATA

    R.run_batch_code(select_type=None,js_on_select='none_save_next();',js_on_else='next_doc();',invert=False,ctrl_num_list=ctrl_num_list)

    R.open_batches()
    R.cfg.set_docs_per_page(1000)
    d=R.data.get_extracted_text(doc_data)

    # DATA EXTRACTION
    R.cfg.config_page('queue',{'category':'Batch Review - In Progress','count':1000})
    d=R.data.get_extracted_text(doc_data)

    tail -n 0 -f net-log.log | while read line; do
        echo $line | grep headers | sed 's/,$//' | jq '.'
    done

    save_list = []
    uniq_subj = df['Subject'].map(lambda s: re.sub(r'(?iLmsux)^((fw|re)[:\s]*)+','',s)).unique().tolist()

    R.run_batch_code(None,ctrl_num_list=ctrl_num_list)

    Failed to connect to localhost (error -102)


    import re
    save_list.extend(df[df['Subject'].str.contains('capital',flags=re.IGNORECASE)]['Control Number'].tolist())
    drop_idx=df[df['Control Number'].isin(save_list)==True].index.tolist()



    REV00798394  
        https://relativity.trustpointintl.com/Relativity/Controls/DocumentReview/DocumentIdentifierFrame.aspx?&AppID=3209893&ArtifactID=2323535&IsRenderedInPopup=False&IsFromReviewTool=False#
        The attached document is a Special



    file:///Users/admin/Desktop/MGM_Law/project_sites.jpg
    file:///Users/admin/Desktop/MGM_Law/completion_chart.png
"""


from selenium.common.exceptions import WebDriverException
import signal, os
def handler(signum, frame):
    raise SystemError
signal.signal(signal.SIGALRM, handler)

class Hud:
    
    def __init__(self):
        make_display=True

        from os import environ as os_environ
        from os import path as os_path
        from sys import path as py_path
        py_path.append(os_path.join(os_environ['G'],'browser_hud'))

        # from browser_hud import *
        # from linkedin_hud import *

        urls = """
            https://www.linkedin.com/in/jaywthomas
            https://www.linkedin.com/in/andrewnallen
            https://www.linkedin.com/pub/steve-mardenfeld/43/367/709
            https://www.linkedin.com/in/jackzhou999
            https://www.linkedin.com/pub/stephen-tsai/39/490/364
            https://www.linkedin.com/pub/mark-wilhelm/86/75a/b94
            https://www.linkedin.com/in/mrxinyi
            https://www.linkedin.com/in/markstokan
            https://www.linkedin.com/pub/tammy-soo/7/770/60
            https://www.linkedin.com/pub/peter-lau/25/578/83
            https://www.linkedin.com/in/srilathak
            https://www.linkedin.com/in/jmogielnicki
            https://www.linkedin.com/pub/frank-wierzbicki/3/559/380
            """
        urls = [it.strip() for it in urls.split('\n') if it.strip()]


        try:
            display_type
        except NameError:
            display_type = 'float'
        else:
            display_type = 'float' if display_type=='pager' else 'pager'
        display_type='pager'
            
        try:
            bh
        except NameError:
            bh = browser_hud(display_type).start_hud(make_display=make_display)
        else:
            bh.close_widget() 
            bh = browser_hud(display_type).start_hud(make_display=make_display)

        def close_all():
            get_ipython().run_cell_magic(u'javascript', u'',u"$('div.start_button_container').remove();")
            get_ipython().run_cell_magic(u'javascript', u'',u"$('div.inspector').remove();")

    class relativity_hud:

        def __init__(self,hud=None):
            
            self.bh = hud

            from os import environ as os_environ
            from os import path as os_path
            from sys import path as py_path
            py_path.append(os_path.join(os_environ['GIT_REPOS'],'emt/src'))

            from emt import EMT
            self.x = EMT()
            self.x.pg.check_db_config()
            self.x.web.initiate_web_session(linkedin_user)
            self.pg = self.x.pg
            self.T = self.pg.T

        def load_data(self):
            _html,_info = self.x.web.collect_and_save_data(self.current_url)
            for tag in _html.find_all('div',{'id':'profile'}):
                tag.attrs['style'] = "width: 100%"
            self.html = _html.renderContents()
            
        def integrate(self,urls=[]):
            self.urls = urls
            self.current_url = self.urls[0]
            
            def general_page():
                opts = self.T.pd.read_sql("select trait from general_traits",
                                          self.T.eng).trait.tolist()
                fresh_opts = sorted([it.replace('_',' ').title() for it in opts])
                widget_component = self.bh.widget.components['General_category']
                current_list = list(widget_component.options)
                new_list = fresh_opts
                new_list.insert(0,current_list[0])
                new_list.extend(current_list[1:])
                widget_component.options=tuple(new_list)  
            def trait_pages():

                def get_work_df():
                    qry = """
                        select 
                            company, t_company.rank company_rank,
                            job_title,  t_job_title.rank job_title_rank
                        from (
                            select 
                                entries->>'company' company,
                                entries->>'title' job_title
                            from 
                                (
                                select jsonb_array_elements((json_info->>'work')::jsonb) entries
                                from candidates 
                                where json_info->>'url'='%s'
                                ) f1
                        ) f2
                        inner join traits t_company on t_company.trait=company
                        inner join traits t_job_title  on t_job_title.trait=job_title
                        """ % self.current_url
                    opts=self.T.pd.read_sql(qry,self.T.eng)

                    hud_df = self.T.pd.DataFrame(columns=['trait','score'])
                    for t in ['company','job_title']:
                        x = opts.ix[:,[t,'%s_rank' % t]].rename(columns={t:'trait','%s_rank' % t:'score'})
                        hud_df=hud_df.append(x,ignore_index=True)
                    return hud_df
                def get_school_df():
                    qry = """
                        select 
                            school, t_school.rank school_rank,
                            major,  t_major.rank major_rank,
                            degree, t_degree.rank degree_rank
                        from (
                            select 
                                entries->>'institution' school,
                                entries->>'major' major,
                                entries->>'degree' degree
                            from 
                                (
                                select jsonb_array_elements((json_info->>'school')::jsonb) entries
                                from candidates 
                                where json_info->>'url'='%s'
                                ) f1
                        ) f2
                        inner join traits t_school on t_school.trait=school
                        inner join traits t_major  on t_major.trait=major
                        inner join traits t_degree on t_degree.trait=degree
                        """ % self.current_url
                    opts=self.T.pd.read_sql(qry,self.T.eng)

                    hud_df = self.T.pd.DataFrame(columns=['trait','score'])
                    for t in ['school','major','degree']:
                        x = opts.ix[:,[t,'%s_rank' % t]].rename(columns={t:'trait','%s_rank' % t:'score'})
                        hud_df=hud_df.append(x,ignore_index=True)
                    return hud_df

                def push_data_to_hud(hud_df,hud_page=''):
                    new_traits = hud_df[hud_df.score.isnull()].apply(lambda a: self.T.json.dumps({'trait':a.trait}),axis=1).tolist()
                    scored_traits = hud_df[hud_df.score.isnull()==False].copy()
                    scored_traits['score'] = scored_traits.score.map(int)
                    scored_traits = scored_traits.apply(lambda a: self.T.json.dumps(a.to_dict()),axis=1).tolist()

                    self.bh.widget.components['%s_new_traits' % hud_page].options = new_traits
                    self.bh.widget.components['%s_scored_traits' % hud_page].options = scored_traits

                hud_df = get_work_df()
                push_data_to_hud(hud_df,hud_page='Work')
                
                hud_df = get_school_df()
                push_data_to_hud(hud_df,hud_page='School')
            
            general_page()
            trait_pages()
            
        def load_url(self,position=''):
            
            def check_button_style():
                if self.current_url==self.urls[0]:
                    _prev,_next,_exit = bh.menu_bar.children
                    _prev._dom_classes = ['faded']
                    _next._dom_classes = ()
                elif self.current_url==self.urls[-1]:
                    _prev,_next,_exit = bh.menu_bar.children
                    _prev._dom_classes = ()
                    _next._dom_classes = ['faded']
                else:
                    _prev,_next,_exit = bh.menu_bar.children
                    _prev._dom_classes = ()
                    _next._dom_classes = ()
                bh.set_css()
            
            if not position:
                self.current_url = self.urls[0]
            elif position=='prev':
                if self.urls.index(self.current_url)==0:
                    return
                self.current_url = self.urls[ self.urls.index(self.current_url)-1 ]
            elif position=='next':
                if self.urls.index(self.current_url)==len(self.urls)-1:
                    return
                self.current_url = self.urls[ self.urls.index(self.current_url)+1 ]


            check_button_style()
            clear_output()
            get_ipython().run_cell_magic(u'html', u'',self.html)

class Postgres:
    
    def __init__(self,_parent):
        self                                =   _parent.T.To_Sub_Classes(self,_parent)
        self.T.__dict__.update(                 dict(zip(
                                                    ['DB_NAME','DB_HOST','DB_PORT','DB_USER','DB_PW'],
                                                    ['mgm', 
                                                    # '0.0.0.0', 
                                                    # 'elm.sanspaper.com', 
                                                    '10.0.0.52', 
                                                    '8800', 'postgres', ''])))
        # self.T.pgsql_home                   =   self.T.os.environ['BD'] + '/pgsql'
        self.T.pgsql_home                   =   '/home/ub2/BD_Scripts/pgsql'
        self.T.sys.path.append(                 self.T.os.environ['BD'] + '/pgsql')
        from pgsql_classes                      import pgSQL
        self.PG                             =   pgSQL(**self.T.__dict__)
        self.T.update(                          self.PG.T.__dict__)
    
    def build(self):
        self.PG.F.functions_run_confirm_extensions()
        self.PG.C.Functions_Create.from_command_line(one_directory=self.T.pgsql_home + '/sql_files/admin')
        self.PG.C.Functions_Create.from_command_line(one_directory=self.T.pgsql_home + '/sql_files/json')
        self.PG.T.to_sql("""
            DROP TABLE IF EXISTS batch_info;
            CREATE TABLE batch_info (
                updates JSONB
            );

            DROP TABLE IF EXISTS doc_data;
            CREATE TABLE doc_data (
                updates JSONB
            );

            CREATE OR REPLACE FUNCTION get_extracted_text_from_uid(integer) RETURNS text AS '
            #!/bin/bash
                UUID=$(uuidgen);
                ASCII="$UUID"_ascii
                LYNX="$UUID"_lynx
                CONTENT=$(psql -At -c "select extracted_text_base64 from doc_data where uid=$1")
                echo "$CONTENT" | base64 -d | iconv -c -f windows-1252 -t ascii > /tmp/$ASCII
                lynx -dump /tmp/$ASCII > /tmp/$LYNX
                RES=$(cat /tmp/$LYNX)
                rm /tmp/$ASCII /tmp/$LYNX
                echo "$RES"
            ' LANGUAGE plshu;

            """)
        return True

    def update_batch_info_from_file(self,fpath='mgm_batch_updates'):
        with open(fpath,'r') as f: x=f.read()
        z = eval(x)
        for k in z.keys():
            qry="""INSERT INTO batch_info (updates) VALUES ('{"%s":%s}'::JSONB);"""%(k,self.PG.T.json.dumps(z[k]))
            self.PG.T.to_sql(qry)
        return True

    def update_batch_info_from_dict(self,updates={}):
        k = self.PG.T.re.sub(r'[.][0-9]*$','',self.PG.T.DT.datetime.now().isoformat()).replace('T',' ')
        qry="""INSERT INTO batch_info (updates) VALUES ('{"%s":%s}'::JSONB);"""%(k,self.PG.T.json.dumps(updates))
        self.PG.T.to_sql(qry)
        return True

    def confirm_doc_data_fields_and_type(self,df={}):
        assert str(type(df).__name__)=='DataFrame'
        # Get table info and create dict for comparison
        tbl_info = self.PG.F.tables_get_info('doc_data')
        tbl_cols = tbl_info.column_name.astype(str).tolist()
        tbl_types = tbl_info.data_type.astype(str).tolist()
        col_type_dict = dict(zip(tbl_cols,tbl_types))

        # Create data_dict for comparison
        data_cols = df.columns.astype(str).tolist()
        data_type = df.dtypes.astype(str).tolist()
        data_dict = dict(zip(data_cols,data_type))
        # ASSUMMING FIELDS WITH SAME NAME HAVE SAME/UNCHANGED TYPES
        # Remove existings fields from analysis
        del_list = []
        for it in data_dict.keys():
            if tbl_cols.count(it):
                del_list.append(it)
        for it in del_list:
            del data_dict[it]

        if not data_dict:
            return tbl_info

        first_row=df.ix[0,:]
        change_dict={}
        for k,v in data_dict.iteritems():
            if v=='object':
                try:
                    new_type=type(eval(first_row[k]))
                    if new_type==list:
                        change_dict.update({k:'text[]'})
                except:
                    change_dict.update({k:'text'})
            elif v=='int64':
                change_dict.update({k:'integer'})
            elif v.count('datetime'):
                change_dict.update({k:'timestamp without time zone'})
        # Make query
        alter_tbl_qry = "alter table doc_data %s ;"
        add_col = 'add column "%s" %s'
        # ASSUMMING FIELDS WITH SAME NAME HAVE SAME/UNCHANGED TYPES
        new_cols = []
        for k,v in change_dict.iteritems():
            data_dict[k] = v
            new_cols.append(add_col % (k,v))
        qry = alter_tbl_qry % ', '.join(sorted(new_cols))
        self.PG.T.to_sql(qry)
        return self.PG.F.tables_get_info('doc_data')

    def update_doc_data_from_df(self,df={}):
        tbl_info = self.confirm_doc_data_fields_and_type( df )
        tbl_dict = dict(zip(
                        tbl_info.column_name.astype(str).tolist(),
                        tbl_info.data_type.astype(str).tolist()))
        self.PG.T.to_sql("DROP TABLE IF EXISTS %s;"%self.T.tmp_tbl)
        df.to_sql(self.T.tmp_tbl,self.T.eng)

        sanitize_qry_text = """UPDATE %(tmp_tbl)s SET "%(field)s"=NULL WHERE "%(field)s"=''"""
        sanitize_qry_array_null = """UPDATE %(tmp_tbl)s SET "%(field)s"=NULL WHERE length("%(field)s")=2"""
        sanitize_qry_array_format = """UPDATE %(tmp_tbl)s SET "%(field)s"=REGEXP_SPLIT_TO_ARRAY(REGEXP_REPLACE("%(field)s",E'\\\\[|\\]|\\\'','','mig'),',','mi')::TEXT[] WHERE NOT "%(field)s" IS NULL"""
        update_qry_templ = """
            WITH uuid_arr AS (
                SELECT array_agg("Control_Number") _arr FROM doc_data
            ),
            upd AS (
                SELECT 
                    %(in_cols)s from %(tmp_tbl)s,
                    (select * from uuid_arr) as _arr
                WHERE _arr && ARRAY["Control_Number"]
            )
            UPDATE doc_data d
            SET %(upd_cols)s
            FROM upd u
            WHERE u."Control_Number" = d."Control_Number"
            """
        insert_qry_templ = """
            WITH uuid_arr AS (
                SELECT array_agg("Control_Number") _arr FROM doc_data
            ),
            ins AS (
                SELECT 
                    %(in_cols)s from %(tmp_tbl)s t,
                    (select _arr from uuid_arr) as A
                WHERE 
                    (NOT ARRAY[t."Control_Number"] && A._arr)
                    OR A._arr IS NULL
            )
            INSERT INTO doc_data (%(out_cols)s)
            SELECT * FROM ins
            """
        
        update_cols = []
        in_cols = []
        out_cols = []

        sanitize_qry_pts = []
        for c in sorted(df.columns.astype(str).tolist()):
            col_type = tbl_dict[c]
            if col_type=='text':
                self.T.field = c
                sanitize_qry_pts.append(sanitize_qry_text % self.T)
                in_cols.append('"%(field)s"'%self.T)
                if c!="Control_Number":
                    update_cols.append('"%(field)s"=u."%(field)s"'%self.T)
            elif col_type=='ARRAY':
                self.T.field = c
                sanitize_qry_pts.append(sanitize_qry_array_null % self.T)
                sanitize_qry_pts.append(sanitize_qry_array_format % self.T)
                in_cols.append('"%(field)s"::text[]'%self.T)
                if c!="Control_Number":
                    update_cols.append('"%(field)s"=u."%(field)s"::text[]'%self.T)
            else:
                self.T.field = c
                in_cols.append('"%(field)s"'%self.T)
                if c!="Control_Number":
                    update_cols.append('"%(field)s"=u."%(field)s"'%self.T)
            out_cols.append('"%(field)s"'%self.T)

        sanitize_qry = ';\n'.join(sanitize_qry_pts)
        update_qry = update_qry_templ % {
                    'in_cols' : ', '.join(in_cols),
                    'out_cols' : ', '.join(out_cols),
                    'upd_cols' : ', '.join(update_cols),
                    'tmp_tbl' : self.T.tmp_tbl,
                    }
        insert_qry = insert_qry_templ % {
                    'in_cols' : ', '.join(in_cols),
                    'out_cols' : ', '.join(out_cols),
                    'tmp_tbl' : self.T.tmp_tbl,
                    }
        add_decoded_extracted_text_qry = """
            UPDATE doc_data SET 
                extracted_text=get_extracted_text_from_uid(uid) 
            WHERE extracted_text IS NULL
            """
        qry = '; \n'.join([
                sanitize_qry,
                update_qry,
                insert_qry,
                add_decoded_extracted_text_qry
                ])
        self.PG.T.to_sql(qry)
        self.PG.T.to_sql("DROP TABLE IF EXISTS %s;"%self.T.tmp_tbl)
        return True

    def upload_extracted_text(self,df={}):
        c = self._parent.run_cmd('cat /Users/admin/BD_Scripts/jobs/law/relativity/docs/00037499_Return_Receipt_dxl.base64')
        pass

class Config:

    """
        R.cfg.set_conditions([{'cond_str':'FileExtension','oper_str':'is not','val_str':'pdf'}])

        R.cfg.set_conditions(conditions=[
            {'cond_str':'FileExtension','oper_str':'is not','val_str':'pdf'},
            {'cond_str':'RESPONSIVENESS','oper_str':'is not set'}]
            ])
        R.cfg.set_conditions(conditions=[{'cond_str':'RESPONSIVENESS','oper_str':'is not set'}])
        R.cfg.set_conditions(conditions=[{'cond_str':'RESPONSIVENESS','oper_str':'any of these','val_str':'Responsive'}])
        
        
        R.cfg.set_batch_category(batch_category='Batch Review - In Progress')
        R.cfg.set_batch_category(batch_category='Batch Review - To Be Reviewed')
        
        if not R.cfg.set_docs_per_page(1000):
            R.T.delay(3)


        R.cfg.set_document_grouping(group_type='No Related Items')
        R.cfg.set_document_grouping(group_type='FamilyID')

        R.cfg.swap_review()
        R.cfg.set_viewer()

    """

    def __init__(self,_parent):
        # self                                =   _parent
        self                                =   _parent.T.To_Sub_Classes(self,_parent)
        self.br                             =   _parent.br

    def add_encoding(self):
        reload(sys)
        sys.setdefaultencoding('UTF8')
    def drop_encoding(self):
        reload(sys)
        sys.setdefaultencoding('ascii')

    def set_batch_category(self,batch_category='Batch Review - In Progress'):
        self.br.window.switch_to.parent_frame()
        current_view = self.br.execute("""return $('#_externalPage').contents().find('select[name="viewMenu"] option:selected').text();""")
        try:
            if current_view==batch_category:
                return True
        except WebDriverException:
            pass

        self._parent.switch_to_active_frame()

        el = self.br.window.find_elements_by_name('viewMenu')[0]
        _select = self.br.Select(el)
        _select.select_by_visible_text( batch_category )
        return True 
    def set_document_grouping(self,group_type='No Related Items'):
        """relationalMenu"""
        group_type = '+ '+group_type
        self.br.window.switch_to.parent_frame()
        current_view = self.br.execute("""return $('#_externalPage').contents().find('select[name="relationalMenu"] option:selected').text();""")
        try:
            if current_view==group_type:
                return True
        except WebDriverException:
            pass

        self._parent.switch_to_active_frame()

        el = self.br.window.find_elements_by_name('relationalMenu')[0]
        _select = self.br.Select(el)
        _select.select_by_visible_text( group_type )
        return True        
    def set_docs_per_page(self,doc_num=10):
        doc_num = str(doc_num)
        # cnt = str(self.br.execute("""return $('#_externalPage').contents().find('.items-per-page>select option:selected').text();"""))
        cnt = str(self.br.execute("""return $('.items-per-page>select option:selected').text();"""))
        if not cnt:
            self._parent.switch_to_active_frame()
            cnt = str(self.br.execute("""return $('.items-per-page>select option:selected').text();"""))
        if cnt!=doc_num:
            doc_num_element = self.br.window.find_element_by_class_name('page-size-options')
            _select = self.br.Select(doc_num_element)
            _select.select_by_visible_text( doc_num )
            return False
            
            # R.br.window.implicitly_wait(5)
            # doc_num_element = self.br.execute("""return $('#_externalPage').contents().find('.page-size-options')[0];""")
            # self.br.execute("""$('#_externalPage').contents().find('.items-per-page>select>select')""")
            
            # try:
            #     self.br.window.find_element_by_class_name('items-per-page').click()
            # except WebDriverException:
            #     pass
        else:
            return True
    def sort_by_date(self,direction='desc'):
        '''

            while True:
                asc_sort = E("""return $('th[title="MasterDateTime"]').find('span[sort="asc"]').attr('class');""")
                desc_sort = E("""return $('th[title="MasterDateTime"]').find('span[sort="desc"]').attr('class');""")
                if direction=='asc' and not asc_sort.count('off'):
                    break
                elif direction=='desc' and not desc_sort.count('off'):
                    break
                else:
                    # toggle sorting
                    E("""return $('th[title="MasterDateTime"]').find('.s-ico')[0].click();""")
                    T.delay(3)

        '''
        E = self.br.execute
        while True:
            asc_sort = E("""return $('th[title="MasterDateTime"]').find('span[sort="asc"]').attr('class');""")
            desc_sort = E("""return $('th[title="MasterDateTime"]').find('span[sort="desc"]').attr('class');""")
            if not asc_sort or not desc_sort:
                self._parent.switch_to_active_frame()
                self.T.delay(3)
            elif direction=='asc'  and not asc_sort.count('off'):
                break
            elif direction=='desc' and not desc_sort.count('off'):
                break
            else:
                # toggle sorting
                E("""return $('th[title="MasterDateTime"]').find('.s-ico')[0].click();""")
                self.T.delay(3)
        return True
        # self._parent.switch_to_active_frame()
        # asc_class = self.br.execute("""return $('.ui-jqgrid-sortable:contains("MasterDateTime")').parent().find('span[sort="asc"]').attr('class');""")
        # if direction=='desc' and asc_class.count('asc off'):
        #     return True
        # elif direction=='asc' and asc_class.count('asc') and not asc_class.count('asc off'):
        #     return True
        # else:
        #     self.br.execute("""return $('.ui-jqgrid-sortable:contains("MasterDateTime")')[0];""").click()
        #     return False
            # for it in z:
            #     if it.text=='MasterDateTime':
            #         it.click()
            #         self.br.execute('return $(\'span[sort="asc"]\');')
            # if not asc_class.count('off') and direction=='desc':
            # self.br.execute('return $(\'.ui-jqgrid-sortable:contains("MasterDateTime")\')[0];').click()

    def config_page(self,page='queue',kwargs={}):
        """

            page = 'queue' or 'batches'

        """
        orig_wait = self.br.window_cfg['defaults']['browser_config']['implicitly_wait']
        self.br.window.implicitly_wait(2)
        self._parent.switch_to_active_frame()       # works for sorting changes
        # self.br.window.switch_to_window(self.br.window.window_handles[0])
        # self.br.window.switch_to_window(self.br.window.current_window_handle)
        
        # DEFAULTS
        opts = {
            # 'category':'Batch Review - In Progress',
            'category':'Batch Review - To Be Reviewed',
            'grp':'No Related Items',
            'count':10,
            'direction':'desc'
            }
        
        for k,v in kwargs.iteritems():
            opts[k] = v

        max_attempts = 5
        attempts = 0
        while True:
            attempts += 1
            success=False
            while True:
                if page=='queue':
                    if not self.set_batch_category(opts['category']):
                        break
                    if not self.set_document_grouping(opts['grp']):
                        break
                    if not self.sort_by_date(opts['direction']):
                        break
                if page=='batches':
                    pass
                if not self.set_docs_per_page(opts['count']):
                    break
                success=True
                break
            if success:
                break
            else:
                self.T.delay(5)
                self._parent.switch_to_active_frame()
            if attempts>=max_attempts:
                success=False
                break

        self.br.window.implicitly_wait(orig_wait)
        return success
    
    def not_working_set_document_grouping(self,group_type='No Related Items'):
        # group_type='FamilyID';
        group_type='FamilyID';
        js = '\n'.join([
            "group_type = '+ %s';" % group_type,
            """
            //batch error:
            //    $('widget-container-state')[0].innerText == "The query has errored."
            //    $('widget-container-state')[0].attributes.loading.value == "loading"


            //$(document).find("select[name=\"relationalMenu\"] option:selected").text()
            current_opt = $('#_externalPage').contents().find('select[name="relationalMenu"] option:selected')[0].text;
            if(current_opt==group_type){
                var doc_groups = $('#_externalPage').contents().find('select[name="relationalMenu"]');
                doc_groups.find('option').each(function(k,v){
                    console.log('k: '+k);
                    if(v.label==group_type){
                        console.log('condition met');
                        console.log('v.value: '+v.value);
                        doc_groups.val(v.value).change();
                        return false;
                    }
                });
            }
            return true;
            """,
        ])
        return self.br.execute(js)
    def not_working_set_items_per_page(self,input_val=10):
        # ON FAIL --> self.switch_to_active_frame()
        js = '\n'.join([
            "input_val = '%s';" % input_val,
            """
            //batch error:
            //    $('widget-container-state')[0].innerText == "The query has errored."
            //    $('widget-container-state')[0].attributes.loading.value == "loading"
            
            var select_element = $(document).find('.items-per-page select');
            current_opt = select_element.find('option:selected')[0].text;
            if(current_opt!=input_val){
                select_element.find('option').each(function(k,v){
                    if(v.label==input_val){
                        select_element.val(v.value).change();
                        return false;
                    }
                });
            }
            return true;
            """,
            ])
        return self.br.execute(js)
    def not_working_sort_by_date(self,direction='desc'):
        self.br.window.switch_to_default_content()
        self.br.window.switch_to_frame(self.br.window.find_elements_by_xpath('//iframe')[3])
        js = '\n'.join([
            "input_val = '%s';" % direction,
            """
            //batch error:
            //    $('widget-container-state')[0].innerText == "The query has errored."
            //    $('widget-container-state')[0].attributes.loading.value == "loading"
            
            var column_header = $('.ui-jqgrid-sortable:contains("MasterDateTime")');
            if(input_val=='desc'){
                var class_info = column_header.parent().find('span[sort="asc"]').attr('class');
                var match = class_info.match(/asc off/);
            } else if(input_val=='asc') {
                var class_info = column_header.parent().find('span[sort="desc"]').attr('class');
                var match = class_info.match(/desc off/);
            }

            if( match==null){             // opposite not off --> keep clicking
                column_header[0].click();
                return false;
            } else {
                return true;
            }
            """,
            ])
        return self.br.execute(js)
    
    # REVIEW CONFIGS
    def swap_review(self,display_side='left'):
        swapped = "true" if display_side=="left" else "false"
        js = '\n'.join([
            "swapped_val = %s;" % swapped,
            """
            if(swapped!=swapped_val){
                toggleSwapped();
            }
            """,
            ])
        return self.br.execute(js)
    def set_viewer(self,viewer_name='Long Text'):
        js = '\n'.join([
            "viewer_set = '%s';" % viewer_name,
            """
            current_viewer = GetCurrentViewer();
            if(viewer_set!=current_viewer){
                SetDocumentViewer(viewer_set);
            }
            """,
            ])
        return self.br.execute(js)

    def _toggle_conditions_panel(self,direction="'expand' or 'collapse'"):
        if not self.br.execute("return $('#_externalPage');"):
            self.br.window.switch_to.parent_frame()
        frame_cnt = self.br.execute("return frames.length;")
        if frame_cnt>0:
            self.br.window.switch_to.frame(frame_cnt-1)
        if direction=='expand':
            if not self.br.execute("return $('.options-inside')[0];").is_displayed():
                self.br.execute("""$('button[title="Expand Search Panel"]').get(0).click();""")
        elif direction=='collapse':
            self.br.execute("""$('div:visible[title="Collapse Search Panel"]').get(0).click();""")
    def set_conditions(self,conditions=[{'cond_str':'FileExtension','oper_str':'is not','val_str':'pdf'}]):
        def set_filter():
            if not hasattr(self,'all_conditions'):
                all_conds = E("""var res=[]; $('div[title="Add Condition"]:visible').find('select[name="newFilterMenu"]:visible option').each(function(k,v){ res.push(v.attributes.label.value); }); return res""")
                self.all_conditions = T.To_Class(dict(zip([str(it) for it in all_conds],[[] for it in all_conds])))

            assert hasattr(self.all_conditions,_cond.cond_str),"Unknown filter condition: "+_cond.cond_str
            cond_element            =   E("""return $('div[title="Add Condition"]:visible').find('select[name="newFilterMenu"][meta-data="newFilterData"]')[0];""")
            _select                 =   self.br.Select(cond_element)
            _select.select_by_visible_text(    _cond.cond_str)
        def set_operator():
            if not self.all_conditions[_cond.cond_str]:
                all_oper = E("""var res=[]; $('div[class*="modal-content"]').find('select[title="Filter operator"]:visible option').each(function(k,v){ res.push(v.attributes.label.value); }); return res""")
                self.all_conditions[_cond.cond_str] = [str(it) for it in all_oper]
            
            assert self.all_conditions[_cond.cond_str].count(_cond.oper_str), "Unexpected condition operator: " + _cond.oper_str
            oper_element            =   E("""return $('div[class*="modal-content"]').find('select[title="Filter operator"]:visible')[0];""")
            _select                 =   self.br.Select(oper_element)
            _select.select_by_visible_text(    _cond.oper_str)
            assert _cond.oper_str==E("""return $('div[class*="modal-content"]').find('select[title="Filter operator"]:visible option:selected')[0].text;"""), "Condition operator value was not set."
        def set_value():
            _textarea = E("return $('textarea:visible')[0];")
            if _textarea:
                Actions = br.Actions(br.window)
                Actions.send_keys_to_element(E("return $('textarea:visible')[0];"),
                                             _cond.val_str)
                Actions.perform()
                return
            _list_items = E("return $('.list-items-container:visible');")
            if _list_items:
                if len(_list_items[0].parent.find_elements_by_class_name('state-disabled')):
                    return
                elif len(_list_items)==2:
                    if not hasattr(_cond,'val_list') and hasattr(_cond,'val_str'):
                        _cond['val_list']=[ _cond.val_str ]
                        delattr(_cond,'val_str')
                    elif hasattr(_cond,'val_list') and hasattr(_cond,'val_str'):
                        if type(_cond.val_list)==list and type(_cond.val_str)==str:
                            _cond['val_list'].append(_cond.val_str)
                            delattr(_cond,'val_str')
                    uniq_list = []
                    for it in _cond.val_list:
                        if not uniq_list.count(it):
                            uniq_list.append(it)
                    delattr(_cond,'val_list')
                    _cond['val_list'] = uniq_list
                    for it in _cond.val_list:
                        it='Non-Responsive'
                        E("""$('.list-items-container:visible li:contains("%s")').get(0).click()"""% it)
                        E("""$('button:visible[title="Select One"]').get(0).click()""")
                    return
                else:
                    assert False, "Unknown error in Config:set_conditions:set_value:_list_items"
            assert False, "Further devel of Config:set_conditions:set_value is needed.  Value type not currently recognized: "+C.__dict__
        def add_condition():
            # ----
            E("""$('button:visible[title="Add condition"]')[0].click()""")

        T = self.T
        br = self.br
        E = br.execute

        self._toggle_conditions_panel('expand')
        
        # CHECK FOR EXISTING CONDITIONS

        if not type(conditions)==list:
            conditions = [conditions]

        for C in conditions:

            if not C.__class__.__name__=='To_Class':
                _cond = T.To_Class(C)
            else:
                _cond = C

            set_filter()

            if hasattr(_cond,'oper_str'):
                set_operator()
                set_value()
                E("""$('button:visible:contains("Apply")')[0].click();""")
            elif hasattr(_cond,'oper_list'):
                assert False, "NEED TO DEVELOP FURTHER"
                # add_condition()
                # E("""$('button:visible:contains("Apply")')[0].click();""")

        E("""$('button:visible:contains("Run Search")').get(0).click();""")
        # T.delay(2)
        self._toggle_conditions_panel('collapse')
        
        return
    def get_conditions(self):
        self._toggle_conditions_panel('expand')
        res = self.br.execute("""
            res=[]; 
            $('.grouped-filter:visible')
                .find('div[name="userEquation"] .item')
                .each(function(k,v){ 
                    d={}; 
                    d['filter']=$(v).find('.card-title').text().replace(/^\\s*/mig,'').replace(/\\s*$/mig,'').replace(/\\n\\r/mig,'').replace(/[.]\\n/mig,'. ');
                    d['content']=$(v).find('.card-text').text().replace(/^\\s*/mig,'').replace(/\\s*$/mig,'').replace(/\\n\\r/mig,'').replace(/[.]\\n/mig,'. ');
                    if( $(v).find('.filter-enable>input:checked').length>0 ){ d['enabled']=true; } else { d['enabled']=false; }
                    res.push(d); 
                    }
                );
            return res;
            """)
        self._toggle_conditions_panel('collapse')
        return res
    def clear_conditions(self):
        if self.get_conditions():
            self._toggle_conditions_panel('expand')
            self.br.execute("""$('button:visible:contains("Clear All Conditions")').get(0).click();""")
            self.br.execute("""$('button:visible:contains("Run Search")').get(0).click();""")
            self._toggle_conditions_panel('collapse')
        return True

class Data:

    def __init__(self,_parent):
        self                                =   _parent.T.To_Sub_Classes(self,_parent)
        self.br                             =   _parent.br
        self.T                              =   _parent.T
        self.docs                           =   None
        self.batches                        =   None
        self.cookie_fpath                   =   self.T.os.environ['BD'] + "/jobs/law/relativity/cookiefile"
        self.extracted_store                =   self.T.os.environ['BD'] + "/jobs/law/relativity/docs"

    def log(self,msg=None,prefix_caller=True):
        I = self.T.I
        D = {      
            'dt' : self.T.DT.datetime.now().isoformat().replace('T',' '),
            'fx' : I.getouterframes(I.currentframe(),2)[1][3],
            'msg' : '' if not msg else str(msg),
            }
        log_path = 'relativity-py.log'
        with open(log_path,'a') as f:
            f.write( '%(dt)s  %(fx)s: %(msg)s\n' % D )
        return True

    def get_data(self):
        def sanitize_doc_data(df):
            df.drop(['','undefined'],axis=1,inplace=True)
            df.rename(columns={'#':'idx'},inplace=True)
            df.columns = df.columns.astype(str).tolist()
            data_cols = df.columns.tolist()
            rename_dict = {}
            for c in data_cols:
                new_c = self.T.re.sub(r'[^a-zA-Z0-9_]','_',c)
                if c!=new_c:
                    rename_dict.update({c:new_c})
            if rename_dict:
                df.rename(columns=rename_dict,inplace=True)
            data_cols = df.columns.tolist()
            to_int_fields = ['idx','AppID','ArtifactID','long_id']
            to_str_fields = ['2nd_Level_Review','Attorney_Notes','Author','BegAttach',
                'Control_Number','Custodian','DocumentType','FileExtension','FileName',
                'From','HOT','Production__Begin_Bates','RESPONSIVENESS',
                'RelativePath','RelativePathParent','Subject',
                'Title','family_beg','family_end','input_checkbox','url']
            to_str_list_fields = ['Attachments','BCC','CC','ISSUES','Project_Code','To']
            to_datetime_fields = ['MasterDateTime']            
            
            conditional_to_str_fields = ['CONFIDENTIALITY']
            for f in conditional_to_str_fields:
                if data_cols.count(f):
                    to_str_fields.append(f)

            conditional_to_str_list_fields = ['Privilege']
            for f in conditional_to_str_list_fields:
                if data_cols.count(f):
                    to_str_list_fields.append(f)

            df[to_int_fields] = df[to_int_fields].astype(int)
            # import ipdb as I; I.set_trace()
            # df[to_str_fields] = df[to_str_fields].apply(lambda s: self.T.re.sub(r'[^\x00-\x7F]+','',s),axis=1).astype(str)
            for c in to_datetime_fields:
                df[ c ] = df[ c ].map(lambda d: self.T.DU.parse(d))
            for c in to_str_list_fields:
                df[ c ] = df[ c ].map(lambda s: s if not type(s)==list and not len(s)>1 else str([str(it) for it in s]))
                df[ c ] = df[ c ].map(lambda s: s if not type(s)==list and not len(s)==1 else str([ str(s)[0] ]))
                df[ c ] = df[ c ].map(lambda s: str([]) if ["[u'']","['']"].count(str(s)) else s)
            return df

        # START IN REVIEW QUEUE
        if self._parent.status!='documents':
            self._parent.open_page('documents')

        self.br.window.switch_to.parent_frame()
        self.br.execute("data_store('clear','doc_data');")
        self.T.delay(2)
        df = self.T.pd.DataFrame(self.br.execute("return get_doc_data();"))
        
        self._parent.switch_to_active_frame()
        h = self.T.BS(self.br.source())

        # col_j = df.columns.tolist().index('url')
        ctrl_num_dict = dict(zip(
                             df['Control Number'].tolist(),
                             df.index.tolist()  ))
        res = h.find_all('a',text=self.T.re.compile(r'^(REV[0-9]+)'))
        url_base = 'https://relativity.trustpointintl.com'

        update_info = []
        for link in res:
            url = link.get('href')
            url_dict = {
                'url':str(url_base + link.get('href')),
                'Control Number':str(link.text),
                'idx':ctrl_num_dict[link.text],
                }
            url_dict.update( self.T.urlparse.parse_qs(self.T.re.sub(r'^[^\?]+\?(.*)$',r'\1',url)) )
            for it in ['AppID','ArtifactID','ArtifactTypeID']:
                url_dict[it] = str(url_dict[it][0])
            for it in ['SelectedTab','profilerMode','ArtifactTypeID']:
                del url_dict[it]
            update_info.append(url_dict)

        df.sort_index(by='Control Number',ascending=True,inplace=True)
        udf = self.T.pd.DataFrame(update_info)
        udf.sort_index(by='Control Number',ascending=True,inplace=True)
        assert udf['Control Number'].astype(str).tolist()==df['Control Number'].astype(str).tolist()

        cols = ['AppID','ArtifactID','url']
        for c in cols:
            df[ c ] = udf[ c ].tolist()

        df['extracted_text_base64'] = unicode('')
        df['extracted_text'] = unicode('')
        df['fname'] = df['FileName'].map(lambda s: unicode(self.T.re.sub(r'[^a-zA-Z0-9_]','_',str(s)) + '.base64'))

        # MOVE TO DOCUMENT PAGE
        self._parent.open_page('review')
        self._parent.T.delay(5)
        long_id = self.br.execute("return parseInt(JSON.parse(documentViewer.MetricTimestamps.metricsForTextViewer.documentViewerService_retrieveLongTextContentEnd_supplementalMetricData.stringifiedPayload).LongTextFieldArtifactID);")
        df['long_id'] = long_id

        df = sanitize_doc_data(df)
        self.docs = df
        return df

    def store_batch_data(self):
        self.br.window.switch_to.parent_frame()
        self.br.execute("data_store('clear','doc_data'); delete doc_data;")
        k = str(self.T.DT.datetime.now().isoformat()).replace('T',' ')
        v = self.T.json.dumps( { k : self.br.execute("return get_doc_data();") } )
        q=  """
            INSERT INTO batch_info (updates,collected) 
            VALUES ('%(upd)s'::jsonb,'%(timestamp)s'::timestamp without time zone)
            """ % {'upd':v,'timestamp':k}
        self.T.to_sql(q)
        return True

    def export_cookies(self,fpath=''):
        fpath = fpath if fpath else self.cookie_fpath
        cookies = self.br.window.get_cookies()
        df = self.T.pd.DataFrame(cookies)
        df.rename(columns={'expiry':'expiration'},inplace=True)
        take_cols=['domain','flag','path','secure','expiration','name','value']
        df = df.ix[:,take_cols].copy()
        df['flag'] = df.flag.map(lambda s: "FALSE" if self.T.pd.isnull(s) else "TRUE").astype(str)
        df['secure'] = df.secure.map(lambda s: "FALSE" if not s else "TRUE").astype(str)
        df['expiration'] = df.expiration.map(lambda n: 0 if self.T.pd.isnull(n) else n).astype(int)
        csv = df.to_csv(header=False,index=False)
        file_header="# HTTP Cookie File"
        out_str = '\n'.join([file_header,csv.replace(',','\t').rstrip(' \n\r')])
        with open(fpath,'w') as f: f.write(out_str)
        return fpath

    def get_extracted_text(self,doc_data=[],store_dir=''):
        if not type(doc_data).__name__=='DataFrame':
            if self.docs:
                doc_data = self.docs
            else:
                doc_data = self.get_data()
        cookiefile = self.export_cookies()
        store_dir = store_dir if store_dir else self.extracted_store
        current_files = self.T.os.listdir(store_dir)
        empty_text_fnames = self.T.pd.read_sql("SELECT fname FROM doc_data WHERE extracted_text IS NULL;",self.T.eng).fname.tolist()

        D = {
            'user_agent' : "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
            'cookiefile' : cookiefile,
            'store_dir'  : store_dir,
            }
        for r in doc_data.iterrows():
            d = r[1].to_dict()
            D.update(d)
            delay = False
            if not current_files.count(d['fname']):
                # ?? CONVERT DATA TO JSON AND ADD TO EXTRACTED TEXT ??
                # import ipdb as I; I.set_trace()
                # d.update({'d_json':self.T.json.dumps(d)})
                cmd = """ \
                    wget \
                        --quiet \
                        --output-document=- \
                        --trust-server-names \
                        --load-cookie %(cookiefile)s \
                        --keep-session-cookies \
                        --save-cookies=%(cookiefile)s \
                        --user-agent='%(user_agent)s' \
                        --save-headers \
                        --local-encoding=$LANG \
                        "https://relativity.trustpointintl.com/Relativity.Distributed/Download.aspx?AppID=%(AppID)s&ArtifactID=%(ArtifactID)s&LongTextFieldArtifactID=%(long_id)s&ExtractedText=True" | \
                    base64 >> %(store_dir)s/%(fname)s && echo true; \
                    """ % D
                self._parent.run_cmd(cmd)
                delay = True
            if empty_text_fnames.count(d['fname']):
                cmd_base64 = "cat %(store_dir)s/%(fname)s;" % D
                cmd_utf8= "cat %(store_dir)s/%(fname)s|base64 --decode;" % D
                text_base64 = self._parent.run_cmd(cmd_base64)
                text_utf8 = self._parent.run_cmd(cmd_utf8)
                self.T.to_sql("""
                         UPDATE doc_data SET extracted_text_base64='%(base64)s' WHERE fname='%(fname)s';
                         """%{  'base64':text_base64,
                                'fname':d['fname'],
                            })
                # self.T.to_sql("""
                #          UPDATE doc_data SET extracted_text_base64='%(base64)s' WHERE fname='%(fname)s';
                #          UPDATE doc_data SET extracted_text='%(utf8)s' WHERE fname='%(fname)s';
                #          """%{  'base64':text_base64,
                #                 'utf8':text_utf8,
                #                 'fname':d['fname'],
                #             })
            if delay:
                if r[0]!=len(doc_data)-1:
                    self.T.delay( self.T.randint(0,10) )

        return True

class Relativity:

    def __init__(self,configs={}):
        import                                  datetime            as DT
        from dateutil                           import parser       as DU               # e.g., DU.parse('some date as str') --> obj(datetime.datetime)
        from urllib                         import quote_plus,unquote
        import                                  urlparse
        from subprocess                     import Popen            as sub_popen
        from subprocess                     import PIPE             as sub_PIPE
        from codecs                         import encode           as codecs_enc
        from traceback                      import format_exc       as tb_format_exc
        from sys                            import exc_info         as sys_exc_info
        import                                  inspect             as I
        from types                          import NoneType
        from time                           import sleep            as delay
        from uuid                           import uuid4            as get_guid
        from random                         import randint
        from selenium.webdriver.common.by   import By
        import                                  os,sys,base64,re
        sys.path.append(                        os.path.join(os.environ['HOME'],'.scripts'))
        sys.path.append(                        os.path.join(os.environ['BD'],'html'))
        from webpage_scrape                 import scraper
        from py_classes                     import To_Class,To_Class_Dict,To_Sub_Classes
        from bs4                            import BeautifulSoup    as BS
        from syscontrol                     import sys_reporter
        SYS_r                               =   sys_reporter
        import                                  pandas              as pd
        # from pandas.io.sql                import execute              as sql_cmd
        pd.set_option(                         'expand_frame_repr', False)
        pd.set_option(                          'display.max_columns', None)
        pd.set_option(                          'display.max_rows', 1000)
        pd.set_option(                          'display.width', 180)
        np                                  =   pd.np
        np.set_printoptions(                    linewidth=200,threshold=np.nan)

        D                                   =   {'guid'                 :   str(get_guid().hex)[:7],
                                                 'user'                 :   os.environ['USER'],
                                                 'guid'                 :   str(get_guid().hex)[:7],
                                                 'today'                :   DT.datetime.now(),
                                                 'growl_notice'         :   True,
                                                 'debug'                :   True,}
        
        # self.T                              =   To_Class(D)

        self.T                              =   To_Class_Dict(  self,
                                                                dict_list=[D,locals()],
                                                                update_globals=True)

        self.T.defaults                     =   self._chromedriver_defaults()
        if configs:
            self.T.update(configs)
            for k,v in configs.iteritems():
                if self.T.defaults.has_key(k):
                    self.T.defaults[k]      =   v

        self.T.configs                      =   {
                                                'window_position': {'x':111, 'y':23, 'windowHandle':'current'},
                                                'window_size': {'height':710,'width':1750},
                                                }
        self.sh                             =   self.run_cmd
        self.br                             =   self.T.scraper(browser='chrome', kwargs=self.T).browser
        self.E                              =   self.br.execute
        import                                  secrets             as S
        self.login_name                     =   S.relativity['username']
        self.login_pw                       =   S.relativity['pw']
        self.cfg                            =   Config(self)
        self.pg                             =   Postgres(self)
        self.data                           =   Data(self)
        self.project_name                   =   'Manion - Eversource'

        #   js_list = ['project','review','batches','documents']
        self.js_page_dict                   =   pd.DataFrame([
                                                {'key' : 'project'   , 'value' : self.project_name,'DOM' : 'parent'},
                                                {'key' : 'review'    , 'value' : 'Edit','DOM' : 'frame'},
                                                {'key' : 'batches'   , 'value' : 'Review Batches','DOM' : 'parent'},
                                                {'key' : 'documents' , 'value' : 'Documents','DOM' : 'parent'},
                                                ])
        self.status                         =   'initiated'
              
    def _chromedriver_defaults(self):
        """
            ----------------------------------------------------------
            CURRENT FINGERPRINT (https://panopticlick.eff.org/tracker)

                one in 66772.5 browsers have the same fingerprint
                16.03 bits of identifying information

            ----------------------------------------------------------
        """
        self.BASE_DIR = self.T.os.path.join(self.T.os.environ['BD'],'html/webdrivers/chrome/profiles/relativity')
        # self.DOWNLOAD_DIR = self.T.os.path.join(self.T.os.environ['HOME'],'Desktop')
        self.DOWNLOAD_DIR = self.BASE_DIR + '/DOWNLOADS'
        self.EXTENSIONS_DIR = self.T.os.path.join(self.T.os.environ['BD'],'html/webdrivers/chrome/extensions')
        _extensions_dict_val =   {
            "settings": {
                "poakhlngfciodnhlhhgnaaelnpjljija": {
                    "active_permissions": {
                    "api": [
                    "storage",
                    "tabs",
                    "management",
                    "system.display",
                    "system.storage",
                    "system.cpu",
                    "system.memory",
                    "system.network"
                    ],
                    "explicit_host": [
                    "http://*/*",
                    "https://*/*"
                    ],
                    "manifest_permissions": [],
                    "scriptable_host": [
                    "<all_urls>"
                    ]
                    },
                    "extension_can_script_all_urls": True,
                    "granted_permissions": {
                    "api": [
                        "storage",
                        "tabs"
                        ],
                    "explicit_host": [
                        "http://*/*",
                        "https://*/*"
                        ],
                    "manifest_permissions": [
                        "webstorePrivate",
                        "management",
                        "system.cpu",
                        "system.display",
                        "system.memory",
                        "system.network",
                        "system.storage"
                        ],
                    "scriptable_host": [
                    "<all_urls>"
                    ]
                    },
                    "incognito": True,
                    "location": 8,
                    "newAllowFileAccess": True,
                    "path": self.EXTENSIONS_DIR + "/custom_js/poakhlngfciodnhlhhgnaaelnpjljija/2.1.40_0",
                }
            }
          }
            # ,"dpplabbmogkhghncfbfdeeokoefdjegm": {
                #     "active_permissions": {
                #     "api": [
                #       "proxy",
                #       "tabs"
                #     ],
                #     "explicit_host": [
                #       "<all_urls>",
                #       "chrome://favicon/*",
                #       "ftp://*/*",
                #       "http://*/*",
                #       "https://*/*"
                #     ],
                #     "manifest_permissions": []
                #     },
                #     "extension_can_script_all_urls": True,
                #     "granted_permissions": {
                #         "api": [
                #           "proxy",
                #           "tabs"
                #         ],
                #     "explicit_host": [
                #       "<all_urls>",
                #       "chrome://favicon/*",
                #       "ftp://*/*",
                #       "http://*/*",
                #       "https://*/*"
                #     ],
                #     "manifest_permissions": []
                #     },
                #     "has_set_script_all_urls": True,
                #     "incognito": True,
                #     "initial_keybindings_set": True,
                #     "location": 4,
                #     "newAllowFileAccess": True,
                #     "path": self.EXTENSIONS_DIR + "/proxy-switchysharp",
                # }
             #}
             #}
                                    # 'load-extension=%s'                     %   (EXTENSIONS_DIR + '/proxy-switchysharp'),
        return {    'user-data-dir'                                 :   self.BASE_DIR,
                    'profile-directory'                             :   'Profile',
                    'log_path'                                      :   self.BASE_DIR + '/chromedriver.log',
                    'bin_path'                                      :   '/usr/local/bin/chromedriver',
                    'port'                                          :   15010,
                    'user-agent'                                    :   "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36", # 10.88 bits, 1 in 1880.59
                    # 'user-agent'                                    :   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",  # 11.86 bits // 1 in 3708.89
                    # 'user-agent'                                    :   "Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1",
                    #               1 in 1788 per panopticlick !!
                    'no_java'                                       :   False,
                    'no_plugins'                                    :   False,
                    'net-log-capture-mode'                          :   'IncludeCookiesAndCredentials',
                    'log-level'                                     :   0,
                    'cookie_content'                                :   {},
                    'capabilities'                                  :
                        {   'acceptSslCerts'                        :   True,
                            'databaseEnabled'                       :   True,
                            'unexpectedAlertBehaviour'              :   "accept",
                            'applicationCacheEnabled'               :   True,
                            'webStorageEnabled'                     :   True,
                            'browserConnectionEnabled'              :   True,
                            'locationContextEnabled'                :   False,
                        },
                    'prefs'                                         :
                        {   
                            "autofill.enabled"                      :   False,
                            "download.default_directory"            :   self.DOWNLOAD_DIR,
                            "download.prompt_for_download"          :   False,
                            "download.directory_upgrade"            :   True,
                            "enable_do_not_track"                   :   True,
                            "extensions"                            :   _extensions_dict_val,
                            "local_discovery.notifications_enabled" :   False,
                            "net.network_prediction_options"        :   2,
                            "partition"                             :   {
                                                                        "default_zoom_level": {
                                                                            "11160318154034397263": -2.2293886449264093
                                                                            },
                                                                        "per_host_zoom_levels": {
                                                                            "11160318154034397263": {}
                                                                            }
                                                                        },
                            "password_manager.keychain_migration"   :   1,
                            "plugins.plugins_disabled"              :   [
                                                                        {"enabled":False,"name":"Chromoting Viewer"},
                                                                        {"enabled":False,"name":"Chrome PDF Viewer"},
                                                                        ],
                            "profile.default_content_setting_values":   { "automatic_downloads": 1 },
                            "profile.password_manager_enabled"      :   False,
                            "savefile.default_directory"            :   self.DOWNLOAD_DIR,
                            "search.suggest_enabled"                :   False,
                            "translate.enabled"                     :   False,
                        },
                    # 'detach'                                        :   True,
                    'extensions_dir'                                :   self.EXTENSIONS_DIR,
                    'extensions'                                    :
                        [
                            # "custom_javascript.crx",
                            # "proxy-switchysharp.crx",
                        ],
                    'session.startup_urls'                          :
                        [
                            'file:///Users/admin/Desktop/MGM_Law/project_sites.jpg',
                            'https://relativity.trustpointintl.com/Relativity/Identity/login',
                            'file:///Users/admin/Desktop/MGM_Law/completion_chart.png',
                        ],
                    'loggingPrefs'                                  :
                        {   "driver"                                :   "ALL",
                            "server"                                :   "ALL",
                            "browser"                               :   "ALL"},
                    'add_opts'                                      :
                        {
                            'log-net-log=%s'                        %   (self.BASE_DIR + '/net-log.log'),
                            'load-extension=%s'                     %   (self.EXTENSIONS_DIR + '/custom_js/poakhlngfciodnhlhhgnaaelnpjljija/2.1.40_0'),
                            'session.restore_on_startup=4',
                        },
                    'true_opts'                                     :
                        [   
                            'allow-cross-origin-auth-prompt',
                            'allow-external-pages',
                            'allow-file-access',
                            'allow-file-access-from-files',
                            'allow-http-background-page',
                            'ash-copy-host-background-at-boot',
                            # 'auto-open-devtools-for-tabs',
                            'disable-core-animation-plugins',
                            # 'disable-extensions',
                            'disable-extensions-http-throttling',
                            # 'disable-file-system',                  # dont enable
                            'disable-plugins',
                            'disable-plugins-discovery',
                            'disable-remote-fonts',
                            'disable-site-engagement-service',
                            'disable-web-security',
                            'disable-webusb-security',

                            'embedded-extension-options',
                            'enable-account-consistency',
                            'enable-devtools-experiments',
                            
                            'enable-logging',
                            'enable-net-benchmarking',
                            'enable-network-information',
                            'enable-network-portal-notification',
                            'enable-offline-auto-reload',
                            'enable-profiling',

                            # 'enable-strict-site-isolation',
                            'enable-tab-switcher',
                            'enable-tcp-fastopen',
                            'enable-web-bluetooth',
                            'incognito',                            
                            'keep-alive-for-test',
                            'mark-non-secure-as',
                            'restore-last-session',
                            'scripts-require-action',
                            'system-developer-mode',
                            'unlimited-storage',
                            'unsafely-treat-insecure-origin-as-secure',
                            # 'use-mobile-user-agent',                # disable
                        ],
                    'false_opts'                                    :
                        [
                            'disable-text-input-focus-manager',
                            # 'enable-profiling',
                        ],
                    # 'value_opts'                                    :
                    #     [
                    #         'load-and-launch-app',
                    #         'load-apps',
                    #         'load-extension',
                    #         'oauth2-client-id',
                    #         'oauth2-client-secret',
                    #     ],
                    'browser_config'                                :
                        {
                            'window_position'                       :   {'x': 135,      'y': 30,
                                                                         'windowHandle':'start'},
                            'window_size'                           :   {'height':746,'width':1718},
                            'implicitly_wait'                       :   2,
                            'page_load_timeout'                     :   25,
                        },
                     }

    def run_cmd(self,cmd,shell=None):
        if not shell or shell=='bash':
            SHELL='/bin/bash'
            cmd = 'source ~/.bashrc; ' + cmd
        elif shell=='zsh':
            SHELL='/bin/zsh'
            cmd = 'source ~/.zshrc; ' + cmd
        p = self.T.sub_popen(cmd,stdout=self.T.sub_PIPE,
                      shell=True,
                      executable=SHELL)
        (_out,_err) = p.communicate()
        assert _err is None
        return _out.rstrip('\n')

    def run_sql(self,qry):
        qry = qry.replace('"','\\\\\\\"')
        pcmd="psql --host=0.0.0.0 --port=8800 --username=postgres --dbname=mgm -c \\\""+qry+"\\\""
        cmd="ssh %(DB_USER)s@%(DB_HOST)s -p 9202" % self.T.__dict__ + "\"" + pcmd + "\""
        return self.run_cmd(cmd,shell='bash')

    def open_login(self):
        start_url = 'https://relativity.trustpointintl.com/Relativity/Identity/login?signin=66ebf8407a887ee7d9745d524f5b8f29'
        self.br.open_page(start_url)
        self.br.wait_for_page()
        self.status = 'login page'

    def identify_page(self,compare_to=None):
        try:
            page_id = self.br.execute("return identify_page();")
        except WebDriverException:
            self.br.window.switch_to.parent_frame()
            page_id = self.br.execute("return identify_page();")
        return page_id if not compare_to else compare_to==page_id

    def login(self):
        self.data.log()
        self.br.scroll_and_click_id('_email')
        self.br.click_element_id_and_type('_email',self.login_name)
        self.br.execute("""$('button:contains("Continue")').click();""")
        self.br.wait_for_page()
        self.br.scroll_and_click_id('_password__password_TextBox')
        self.br.click_element_id_and_type('_password__password_TextBox',self.login_pw)
        self.br.execute("""$('button:contains("Login")').click();""")
        # self.br.scroll_and_click_id('_login')
        self.br.wait_for_page()
        self.status = 'logged in'

    def logout(self):
        self.data.log()
        self.br.window.switch_to_window(self.br.window.current_window_handle)
        self.br.window.execute_script("""
            $('span[title="User Dropdown Menu"]').find('img[alt="Dropdown Menu"]')[0].click();
            """)
        self.br.T.delay(1)
        self.br.window.execute_script("""
            $('a[title="Logout"]')[0].click();
            """)
        self.br.wait_for_page()
        self.status = 'logged out'

    def quit(self):
        self.data.log()
        self.logout()
        self.br.quit()
        self.run_cmd( 'rm -fr %(d)s; mkdir -p %(d)s'%{'d':self.DOWNLOAD_DIR} )

    def load_js(self):
        cmd = """ssh ub2 "cat /home/ub2/GIT_REPOS/relativity/relativity.js | base64";"""
        code_content = self.run_cmd(cmd,shell='bash').replace('\n','')
        c = self.T.base64.b64decode(code_content)
        code_content = self.T.base64.b64encode(c.replace('top.',''))
        self.br.window.execute_script( """
            code_base64 = '"""+code_content+"""';
            ext = {
                config: {
                    enable: true,
                    include: '',
                    extra: ''
                },
                source: ''
            }
            ext.source = 'data:text\/javascript;base64,' + code_base64; //btoa(script_stored)
            localStorage['customjs'] = JSON.stringify(ext);
            """)
        self.br.window.refresh()

    def load_cookies(self,cookie_list=[]):
        if not cookie_list:
            # GET COOKIE FROM ... (pastebin?)
            return False
        for c in cookie_list:
            self.br.add_cookie(c)
        return True

    def run_js(self,js):
        if not hasattr(self,'js_base'):
            self.load_js()
        if not hasattr(self.br,'handle'):
            self.br.handle = self.br.window.current_window_handle
        self.br.window.switch_to_window(self.br.handle)
        self.switch_to_active_frame()
        self.br.window.switch_to_active_element()
        # self.br.window.switch_to_default_content()
        return self.br.window.execute_script(js)

    def open_project(self,project_name_text=''):
        if not project_name_text:
            project_name_text = self.project_name
        self.br.window.execute_script("""
            c = $('#_form').find('#Table1').find('#_main').find('#ListTemplateFrame').contents();
            c.find('a[class="itemListPrimaryLink"]:contains("%s")')[0].click();
            """ % project_name_text)
        self.br.wait_for_page()
        self.status = self.identify_page()
        assert self.status=='documents'
    
    def open_page(self,page_id):
        """
            STATUSES
                initiated
                login
                logged in
                logged out
                project
                documents
                review
                batches
            
            PAGE IDS
                project
                documents
                review
                batches
        """
        
        def goto():
            if not self.identify_page(page_id):
                if d.DOM=='parent':
                    self.br.window.switch_to.parent_frame()
                elif d.DOM=='frame':
                    self.switch_to_active_frame()
                self.br.execute("""return $('a:contains("%s")').first()[0].click();"""%d.value)
                self.br.wait_for_page()
                self.T.delay(3)
                self.status = self.identify_page()
                assert self.status==page_id
        
        df = self.js_page_dict
        d = df.ix[df[df.key==page_id].first_valid_index(),:]
        
        try:
            # print('goto page_id: %s, js_page_dict: %s, identify_page: %s'%(page_id,d.value,self.identify_page()))
            goto()
            return True
        except WebDriverException:
            # print('error fixing')
            self.error_fix()
            goto()
            return True

    def switch_review_tab(self,tab_link_text=None):
        """
            Opens 'Documents' or 'Review Batches' tabs
        """
        current_url = self.br.get_url()
        tabs = ['Documents','Review Batches']
        if tab_link_text:
            assert tabs.count(tab_link_text),'Unknown review tab: %s' % tab_link_text
        idx = 1 if not current_url.count('ViewId=') else 0
        switch_to_tab = tabs[idx]
        if tab_link_text == switch_to_tab:
            pass
        else:
            self.br.window.execute_script("""
                $('#_form').find('#Table1').find('a:contains("%s"):visible')[0].click();
                """ % switch_to_tab)
            self.br.wait_for_page()

    def is_loading_error(self):
        error_conditions = [
            ['An error has occurred in Relativity.','Return to Home'],
            ['The query has errored.']
        ]
        is_err,body_text = False,self.br.get_body_text()
        for errs in error_conditions:
            e_cnt = len(errs)
            cnt = 0
            for e in errs:
                if body_text.count(e):
                    cnt+=1
            if cnt==e_cnt:
                is_err = True
                break
        if is_err and body_text.count("Return to Home"):
            self.br.window.execute_script("""return $('a:contains("Return to Home"):visible')[0].click();""")
            self.br.wait_for_page()
            return True
        if is_err and body_text.count('The query has errored.'):
            self.br.window.refresh()
        return False

    def wait_for_frames_to_load(self,element_to_wait_for):
        # signal.alarm(2)
        # try:
        #     self.br.window.find_elements_by_xpath('//iframe')[2].find_elements(by='class name',value='jqgfirstrow')
        # except:
        #     print('no results')
        # signal.alarm(0)          # Disable the alarm
        orig_wait = self.br.window_cfg['defaults']['browser_config']['implicitly_wait']
        self.br.window.implicitly_wait(2)

        # workspace -> $('#_form').find('#Table1').find('#_main').find('#ListTemplateFrame').contents()
        # main_list,batch_list -> $('#_externalPage').contents()
        # review_queue -> $('#_form').find('#_main').find('#_tableViewFrameDocked').contents();

        self.br.window.implicitly_wait(orig_wait)

    def switch_to_active_frame(self):
        orig_wait = self.br.window_cfg['defaults']['browser_config']['implicitly_wait']
        self.br.window.implicitly_wait(2)

        if int(self.br.execute("return frames.length;"))>0:
            last_frame = self.br.execute("return frames.length;") - 1
            self.br.window.switch_to.frame(last_frame)


        # instance: Browser
        # self.reset_browser(targets=['window'])
        # self.br.window.switch_to_default_content()
        # self.br.window.switch_to_active_element()
        # self.br.window.find_elements_by_xpath('//iframe')[3].is_displayed() # == True
        # z=br.window.find_elements_by_xpath('//iframe')[3]


        # br.window.find_elements_by_xpath('//iframe')
        # br.window.switch_to_default_content()
        # frames = self.br.window.find_elements_by_xpath('//iframe')
        # for it in frames:
        #     if it.is_displayed():
        #         self.br.window.switch_to_frame(frames.index(it))
        #         break
        
        # # Iterate frames and switching to active frame
        # frames = self.br.window.find_elements_by_xpath('//iframe')
        # active_dict={}
        # pt=-1
        # for it in frames:
        #     pt+=1
        #     if it.is_displayed():
        #         active_dict.update({it.size['height'] * it.size['width']:pt})
        # if active_dict:
        #     idx = active_dict[ sorted(active_dict.keys())[-1] ]
        #     self.br.window.switch_to_frame( idx )
        #     return True
        # else:
        #     return False

        self.br.window.implicitly_wait(orig_wait)

    def reset_browser(self,targets=['all']):
        if type(targets)==str: targets=[targets]
        if targets==['all']:
            self.br.window.switch_to_window(self.br.handle)
            self.switch_to_active_frame()
            self.br.window.switch_to_active_element()
        else:
            if targets.count('window'):
                self.br.window.switch_to_window(self.br.handle)
            if targets.count('frame'):
                # self.switch_to_active_frame()
                self.switch_to_active_frame()
            if targets.count('element'):
                self.br.window.switch_to_active_element()

    def check_batch(self,direction,batch_name=None):
        """ Directions: in,out,pending,completed """
        R = self
        T = R.T
        br = R.br
        PG = R.pg.PG
        E = br.execute

        self.data.log(batch_name)
        if batch_name:
            R.switch_to_active_frame()
            E("""$('tr:contains(\"""" + batch_name + """\")').find('a:contains("Edit")')[0].click();""")
            T.delay(2)
            br.window.switch_to.window(br.window.window_handles[1])
        else:
            # IDENTIFY CURRENT BATCH AND SET BATCH_NAME
            pass

        direction=direction.lower()
        if direction=='in' or direction=='completed':
            check_name = "Check In As Completed"
        elif direction=='pending':
            check_name = "Check In As Pending"
        elif direction=='out':
            check_name = "Check Out"

        E("$('a:contains(\"%s\")')[0].click()"%check_name)

        br.window.switch_to.window(br.window.window_handles[0])
        R.switch_to_active_frame()
        T.delay(4)
        return True

    def checkin_batch_and_checkout_next_in_set(self):
        """
            On completing analysis,
                run this function (checkin_batch_and_checkout_next_in_set),
                consider then running function: initial_analysis_prep
        """
        R = self
        T = R.T
        br = R.br
        PG = R.pg.PG
        E = br.execute

        if not R.open_page('batches'):
            T.delay(4)
        if not R.cfg.set_docs_per_page(1000):
            T.delay(3)
        R.br.window.switch_to.parent_frame()
        df = T.pd.DataFrame(E("return get_doc_data();"))

        current_batch = df[ (df['Batch Status']=='In Progress') & (df['Assigned To']=='Chase, Seth') ]['Batch'].astype(str).tolist()[0]
        self.check_batch('completed',current_batch)

        current_set = str(df[ (df['Batch']==current_batch) ]['Batch Set'].tolist()[0])
        remaining_batches_in_set = df[ (df['Batch Set']==current_set) & (df['Batch Status']==u'')]
        if not len(remaining_batches_in_set):
            return False
        else:
            idx = remaining_batches_in_set.first_valid_index()
            self.check_batch('out',str(df.ix[idx,'Batch']))
            return True
    
    def start(self):
        self.data.log()
        self.br.window.implicitly_wait(5)
        self.br.window.set_script_timeout(20)
        self.br.window.set_page_load_timeout(20)
        self.br.window.switch_to_active_element() 
        self.open_login()
        self.load_js()
        self.login()
        self.T.delay(3)
        self.open_project()
        assert self.identify_page()=='documents'

    def error_fix(self):
        self.data.log()
        R = self
        T = R.T
        br = R.br
        E = br.execute

        br.window.execute_script("top.set_options('autopilot'); top.toggle_autopilot('stop');")

        error_script = """
            function error_check(){
                // METHODS
                //  -RELOAD
                //  -SELECT LINKS, i.e., Documents

                if( $('a[title="Return to Home"]')!=null ){
                    // error('relativity load error')
                    console.log('relativity load error');
                    $('a[title="Return to Home"]')[0].click();
                    return true;
                } else if( document.getElementsByTagName("a").length==1 ){
                    // error('logged out')  --> ''
                    console.log('logged out');
                    // logged_out_url='https://relativity.trustpointintl.com/Relativity/Identity/logout?id=cb5d5c99cff5b0a841786fdc078dbaa9'
                    link = document.getElementsByTagName("a")[0];
                    if(link.text=='log in.'){ 
                        console.log('logging in');
                        link.click(); 
                        return true; 
                    }
                } else if( element_attrs('data_store').length==1 ){
                    // error('relativity load error (data_store)')
                    console.log('error:data_store');
                    location.reload();
                } else if( $('widget-container-state')[0].innerText == "The query has errored." ){
                    // error('relativity review queue loading error')
                    console.log('error:review queue loading');
                    location.reload();
                }


                $('widget-container-state')[0].innerText == "The query has errored."
                };
            error_check();
            """

        try:
            E(error_script)
            T.delay(8)
        except WebDriverException:
            br.window.refresh()
            T.delay(8)

        br.window.switch_to.parent_frame()
        if self.identify_page()=='review':
            br.window.execute_script("top.set_options('autopilot'); top.toggle_autopilot('start');")
            return

        if self.identify_page()=='project':
            self.open_project()
            T.delay(3)

        br.window.switch_to.parent_frame()
        if self.identify_page()!='documents':
            self.open_page('documents')
            T.delay(3)

        R.switch_to_active_frame()
        if not E("return document.getElementById('select2--container');").text.count('Batch Review -'):
            print('NEED TO SET ANY CONDITIONS, i.e., no PDFs?')
            self.cfg.config_page('queue',{'category':'Batch Review - To Be Reviewed','count':10})

        br.window.switch_to.parent_frame()
        self.open_page('review')
        self.cfg.swap_review()

        br.window.execute_script("top.set_options('autopilot'); top.toggle_autopilot('start');")

    def initial_analysis_prep(self):
        """
            NEEDS TO END AT 'documents' WITH ALL DOCS VISIBLE (e.g., 1000)

        """
        self.data.log()
        R = self
        T = R.T
        br = R.br
        PG = R.pg.PG
        E = br.execute

        br.window.switch_to.parent_frame()

        if not self.identify_page()=='documents':
            R.open_page('documents')
        if not R.cfg.set_batch_category(batch_category='Batch Review - To Be Reviewed'):
            R.T.delay(1)
        if not R.cfg.set_document_grouping(group_type='No Related Items'):
            R.T.delay(1)
        if not R.cfg.set_docs_per_page(1000):
            R.T.delay(3)
        R.cfg.sort_by_date('desc')
        R.cfg.clear_conditions()
        R.T.delay(3)

    def run_analysis(self,skip_pdfs=True):
        """

        """
        msg = ','.join([
                       'skip_pdfs=%s' % str(skip_pdfs),
                       ])
        self.data.log('START - %s' % msg)
        R = self
        T = R.T
        br = R.br
        PG = R.pg.PG
        E = br.execute

        br.window.switch_to.parent_frame()

        if not self.identify_page()=='documents':
            R.open_page('documents')
        if not R.cfg.set_docs_per_page(1000):
            R.T.delay(3)
        if not R.cfg.set_batch_category(batch_category='Batch Review - To Be Reviewed'):
            R.T.delay(1)
        if not R.cfg.set_document_grouping(group_type='No Related Items'):
            R.T.delay(1)

        R.cfg.clear_conditions()
        conditions=[{'cond_str':'RESPONSIVENESS','oper_str':'is not set'}]
        if skip_pdfs:
            conditions.append({'cond_str':'FileExtension','oper_str':'is not','val_str':'pdf'})
        R.cfg.set_conditions(conditions)
        R.T.delay(3)

        _out = R.data.get_data()
        df = R.data.docs

        T.delay(3)

        # if self.identify_page()!='review':

        br.window.switch_to.parent_frame()

        if not self.identify_page()=='documents':
            R.open_page('documents')
        if not R.cfg.set_docs_per_page(10):
            R.T.delay(3)                
        if not R.cfg.set_batch_category(batch_category='Batch Review - To Be Reviewed'):
            R.T.delay(1)
        if not R.cfg.set_document_grouping(group_type='No Related Items'):
            R.T.delay(1)

        R.cfg.sort_by_date('asc')
        R.open_page('review')
        R.cfg.swap_review()
        R.cfg.set_viewer()

        orig_data_store = { 
            'highlight_only'                    : E("data_store('get','highlight_only');"),
            'auto_next_doc_if_non_responsive'   : E("data_store('get','auto_next_doc_if_non_responsive');"),
            }

        E("""data_store('set',{
            'auto_next_doc_if_non_responsive'   :   true,
            'highlight_only'                    :   true,
            });""")

        total_docs = int(E("""return $('.documentNavigatorNonButtonCell').find('span').last().text().replace(/[^0-9]*/mig,'');"""))
        while True:
            try:
                for i in range(40):
                    if not self.identify_page()=='review':
                        break
                    # based on above data_store:auto_next_doc_if_non_responsive setting, responsive if page unchanged
                    doc_num = int(E("""return $('#_documentNavigator_currentArtifactTextBox_textBox').attr('value');"""))
                    R.br.window.execute_script("top.set_options(); top.run_analysis();")
                    R.T.delay(2)
                    doc_num_chk = int(E("""return $('#_documentNavigator_currentArtifactTextBox_textBox').attr('value');"""))
                    if doc_num==doc_num_chk:
                        # fetch extracted content if responsive
                        ctrl_num = str(E("return get_doc_records();")['ctrl_number'])
                        assert R.data.get_extracted_text(doc_data=df[df.Control_Number==ctrl_num])
                        E("toggle_skip_doc();")
                    if doc_num==total_docs:
                        break
                    R.T.delay(2)
                if doc_num==total_docs:
                    break
                self.br.window.refresh()
                self.T.delay(10)
            except WebDriverException:
                pass
        self.data.log('END -- last doc_num: %s'%doc_num)
        return True

    def run_batch_code(self,select_type,js_on_select='none_save_next();',js_on_else='next_doc();',invert=False,ctrl_num_list=None):
        """

            select_types: all,checked,unchecked
            js_on_select: 'none_save_next();'
            js_on_else: 'next_doc();'

        """
        msg = ','.join([
                       'select_type=%s' % str(select_type),
                       'js_on_select=%s' % str(js_on_select),
                       'js_on_else=%s' % str(js_on_else),
                       'invert=%s' % str(invert),
                       ])
        self.data.log('START - %s' % msg)
        R = self
        T = R.T
        br = R.br
        PG = R.pg.PG
        E = br.execute
        self.df = T.pd.DataFrame(E("return get_doc_data();"))
        df = self.df

        if ctrl_num_list:
            do_list = ctrl_num_list
        else:
            if select_type=='all':
                do_list = df['Control Number'].tolist()
            elif select_type=='checked':
                do_list = df[df['input_checkbox']=='checked']['Control Number'].tolist()
            elif select_type=='unchecked':
                do_list = df[df['input_checkbox']!='checked']['Control Number'].tolist()
        
        if self.identify_page()!='review':

            if not R.cfg.set_batch_category(batch_category='Batch Review - To Be Reviewed'):
                R.T.delay(3)
            if not R.cfg.set_docs_per_page(10):
                R.T.delay(3)
            if not R.cfg.set_document_grouping(group_type='No Related Items'):
                R.T.delay(3)

            R.cfg.clear_conditions()
            R.cfg.set_conditions(conditions=[{'cond_str':'RESPONSIVENESS','oper_str':'is not set'}])
            R.T.delay(2)
            R.cfg.sort_by_date('desc')

            R.open_page('review')
        
        R.cfg.swap_review()
        R.cfg.set_viewer()

        total_docs = int(E("""return $('.documentNavigatorNonButtonCell').find('span').last().text().replace(/[^0-9]*/mig,'');"""))
        try:
            while True:
                try:
                    for i in range(40):
                        doc_num = int(E("""return $('#_documentNavigator_currentArtifactTextBox_textBox').attr('value');"""))
                        
                        if invert:
                            if not do_list.count(E("return get_doc_records();")['ctrl_number']):
                                E(js_on_select)
                            else:
                                E(js_on_else)
                        else:
                            if do_list.count(E("return get_doc_records();")['ctrl_number']):
                                E(js_on_select)
                            else:
                                E(js_on_else)

                        if doc_num==total_docs:
                            break
                    if doc_num==total_docs:
                        break
                    self.br.window.refresh()
                    self.T.delay(10)
                except WebDriverException:
                    pass
        except KeyboardInterrupt:
            self.data.log('END')
            return False
        self.data.log('END')
        return True

    def check_tagging(self):
        R = self
        T = R.T
        br = R.br
        PG = R.pg.PG
        E = br.execute
        
        R.open_page('documents')
        R.cfg.clear_conditions()
        if not R.cfg.set_batch_category(batch_category='Batch Review - In Progress'):
            T.delay(3)
        if not R.cfg.set_document_grouping(group_type='FamilyID'):
            T.delay(3)
        if not R.cfg.set_docs_per_page(1000):
            T.delay(3)
        R.br.window.switch_to.parent_frame()


        # COMPARE SUBJECTS:
        print('Comparing Email Subject Lines')
        df = T.pd.DataFrame(E("return get_doc_data();"))
        df['subj_clean']=df['Subject'].map(lambda s: T.re.sub(r'(?iLmsux)^((fw|re)[:\s]*)+','',s))
        # assert len(df[df['subj_clean'].isin(save_list)]) and len(df[df['subj_clean'].isin(save_list)])<len(df)
        uniq_subjs = sorted(df[df['subj_clean']!=u'']['subj_clean'].unique().tolist())

        chk_cols = [u'RESPONSIVENESS',u'Privilege',u'CONFIDENTIALITY',u'HOT',u'ISSUES']
        for it in uniq_subjs:
            cp = df[df['subj_clean']==it].copy().reset_index(drop=True)
            for chk in chk_cols:
                cp[chk] = cp[chk].map(lambda t: None if type(t)==list else t)
                tf = cp[cp[chk]!=None].copy().reset_index(drop=True)
                if len(tf[chk].unique().tolist())>1:
                    print 'doc #: %s -- Different %s with subj: %s' % (str(tf.ix[:,'#'].tolist()),str(chk),it)
        print('Comparing Email Subject Lines-DONE')

        print(E("var dd=get_doc_data(); return check_coding_quality(dd,true);"))
        return True


# javascript:parent.documentViewer.SwitchViewer(false);
#   
#   
#   $(".loading:hidden").length>0  -->  content loaded 
#   $(".loading:visible").length>0  -->  content NOT loaded (and currently loading)
#
#   window.top.location.reload()
#   .is(':checked')
#
#   getDocument(currentViewer, true, true/false)
#
#   window.frames.isLoaded
#
# z = documentViewer.GetData().ExtractedTextURL
# extr_url = z.ExtractedTextURL.replace(/LongTextFieldArtifactID=\{1\}[&]/,'')
# extr_url = extr_url.replace(/(ArtifactID)=(\{0\})/,'$1='+z.ArtifactID).replace(/LongTextFieldArtifactID=\{1\}[&]/,'')
# window.open(extr_url,'_blank')
#
#   https://relativity.trustpointintl.com/Relativity/Case/Document/Review.aspx?AppID=3209893&ArtifactID=2323320&profilerMode=Edit&ArtifactTypeID=10&SelectedTab=null


# from selenium.webdriver.common.by import By


# loading batches -- signal for errors , signal for loaded
# loading documents -- signal for errors , signal for loaded
