#!env python

""" USAGE:

jupyter console -i --pdb -c "$(
cat <<-'EOF'

import sys,os
sys.path.append(os.environ["BD"] + "/html/console_browser")
from browser_base import *

kwargs = {
        "chromedriver_input_defaults":{
            "incognito":False
            ,"disable-plugins":False
        }
        ,"console_config":{
            "config_name"       :   "default"
            ,"select_query"     :   "                                           \
                                    SELECT                                      \
                                        uid                                     \
                                        ,_attr                                  \
                                        ,_metadata->>'fpath' fpath              \
                                        ,_metadata->>'pg_notes' pg_notes        \
                                    FROM file_idx                               \
                                    WHERE (_metadata->>'fpath')::TEXT ~* 'pdf$' \
                                    "
            ,"update_query"     :   ""
            ,"jump_query"       :   ""
            ,"sort_select_by"   :   ""
            ,"skip_marked"      :   True
            ,"mark_skipped"     :   True
            }
        ,"db_config":{
            "DB_NAME"           :   "fileserver"
            ,"DB_HOST"          :   "10.0.0.52"
            ,"DB_PORT"          :   "8800"
            ,"DB_USER"          :   "postgres"
            ,"DB_PW"            :   ""
            }
        }

br      = Browser(kwargs)
br.T.update(br.cs.T.__dict__)
T       = br.T
df      = br.cs.df
E       = br.execute
print 'Console Browser Loaded.'
self    = br.cs
Exts    = br.cs.exts
RUN     = br.cs.run_review
br.cs.run_review()

EOF
)"



"""


"""

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
        self.T.pgsql_home                   =   self.T.os.environ['HOME_ENV'] + '/BD_Scripts/pgsql'
        self.T.sys.path.append(                 self.T.pgsql_home)
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

class Browser:

    def __init__(self,configs={}):
        import                                  os,sys,base64,re
        import                                  datetime            as DT
        from dateutil                           import parser       as DU               # e.g., DU.parse('some date as str') --> obj(datetime.datetime)
        from urllib                         import quote_plus,unquote
        import                                  urlparse
        

        from subprocess                     import Popen            as sub_popen
        from subprocess                     import PIPE             as sub_PIPE
        from codecs                         import encode           as codecs_enc
        from traceback                      import format_exc       as tb_format_exc
        from sys                            import exc_info         as sys_exc_info
        from importlib                      import import_module
        import                                  inspect             as I
        from types                          import NoneType
        from time                           import sleep            as delay
        from uuid                           import uuid4            as get_guid
        from random                         import randint
        from selenium.webdriver.common.by   import By
        sys.path.append(                        os.path.join(os.environ['HOME'],'.scripts'))
        sys.path.append(                        os.path.join(os.environ['BD'],'html'))
        from webpage_scrape                 import scraper
        from py_classes                     import To_Class,To_Class_Dict,To_Sub_Classes
        from bs4                            import BeautifulSoup    as BS
        from selenium.common.exceptions     import WebDriverException
        import                                  signal
        def sig_alrm(signum, frame):        raise SystemError
        signal.signal(                      signal.SIGALRM, sig_alrm)
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
        
        self.T                              =   To_Class_Dict(  self,
                                                                dict_list=[D,locals()],
                                                                update_globals=True)

        chromedriver_input_defaults         =   {} if not configs.has_key('chromedriver_input_defaults') else configs['chromedriver_input_defaults']
        if type(chromedriver_input_defaults)==list:
            chromedriver_input_defaults     =   {'chromedriver_input_defaults':chromedriver_input_defaults}

        self.T.defaults                     =   self._chromedriver_defaults(chromedriver_input_defaults)

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
        br                                  =   self.T.scraper(browser='chrome', kwargs=self.T).browser
        self.T.br                           =   br
        self.E                              =   br.execute

        if configs.has_key('db_config'):
            db_config                       =   configs['db_config']
        else:
            db_config                       =   dict(zip(
                                                        ['DB_NAME','DB_HOST','DB_PORT','DB_USER','DB_PW'],
                                                        ['system', 
                                                        # '0.0.0.0', 
                                                        # 'elm.sanspaper.com', 
                                                        '10.0.0.52', 
                                                        '8800', 'postgres', '']
                                                        ))
        self.T.__dict__.update(                 db_config)

        # import                                  secrets             as S
        # self.cfg                            =   Config(self)
        self.pg                             =   Postgres(self)
        # self.data                           =   Data(self)
        # self.project_name                   =   'Manion - Eversource'
        
        
        self.T.console_config               =   {} if not configs.has_key('console_config') else configs['console_config']
        self.T.console_config['config_name']=   'default' if not configs.has_key('console_config') else self.T.console_config['config_name']
        cfg_mod                             =   import_module("console." + self.T.console_config['config_name'])
        self.cs                             =   cfg_mod.Console(self)

        excl_attrs_regex                    =   '^(__|_parent|T)'
        for _attr in dir(br):
            if not hasattr(re.search(excl_attrs_regex,_attr),'groups'):
                if not hasattr(self,_attr):
                    setattr(self,_attr,getattr(br,_attr))

        #   js_list = ['project','review','batches','documents']
        # self.js_page_dict                   =   pd.DataFrame([
        #                                         {'key' : 'project'   , 'value' : self.project_name,'DOM' : 'parent'},
        #                                         {'key' : 'review'    , 'value' : 'Edit','DOM' : 'frame'},
        #                                         {'key' : 'batches'   , 'value' : 'Review Batches','DOM' : 'parent'},
        #                                         {'key' : 'documents' , 'value' : 'Documents','DOM' : 'parent'},
        #                                         ])
        # self.status                         =   'initiated'
              
    def _chromedriver_defaults(self,args={}):
        """
            ----------------------------------------------------------
            CURRENT FINGERPRINT (https://panopticlick.eff.org/tracker)

                one in 66772.5 browsers have the same fingerprint
                16.03 bits of identifying information

            ----------------------------------------------------------
        """
        self.BASE_DIR = self.T.os.path.join(self.T.os.environ['BD'],'html/webdrivers/chrome/profiles/default')
        # self.DOWNLOAD_DIR = self.T.os.path.join(self.T.os.environ['HOME'],'Desktop')
        self.DOWNLOAD_DIR = self.BASE_DIR + '/DOWNLOADS'
        self.EXTENSIONS_DIR = self.T.os.path.join(self.T.os.environ['BD'],'html/webdrivers/chrome/extensions')

        ext_custom_js =   {
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
                        "scriptable_host": ["<all_urls>"]
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
                        "scriptable_host": ["<all_urls>"]
                    },
                    "incognito": True,
                    "location": 8,
                    "newAllowFileAccess": True,
                    "path": self.EXTENSIONS_DIR + "/custom_js/poakhlngfciodnhlhhgnaaelnpjljija/2.1.40_0",
                }
            }
          }
        ext_proxy_switch =   {
                "dpplabbmogkhghncfbfdeeokoefdjegm": 
                    {
                        "active_permissions": {
                        "api": [
                          "proxy",
                          "tabs"
                        ],
                        "explicit_host": [
                          "<all_urls>",
                          "chrome://favicon/*",
                          "ftp://*/*",
                          "http://*/*",
                          "https://*/*"
                        ],
                        "manifest_permissions": []
                        },
                        "extension_can_script_all_urls": True,
                        "granted_permissions": {
                            "api": [
                              "proxy",
                              "tabs"
                            ],
                        "explicit_host": [
                          "<all_urls>",
                          "chrome://favicon/*",
                          "ftp://*/*",
                          "http://*/*",
                          "https://*/*"
                        ],
                        "manifest_permissions": []
                        },
                        "has_set_script_all_urls": True,
                        "incognito": True,
                        "initial_keybindings_set": True,
                        "location": 4,
                        "newAllowFileAccess": True,
                        "path": self.EXTENSIONS_DIR + "/proxy-switchysharp",
                    }
                }
        ext_pdf_viewer =   {
            "oemmndcbldboiebfnladdacbdfmadadm": 
                {
                    "active_permissions": {
                        "api": [
                            "management"
                            ,"proxy"
                            ,"storage"
                            ,"system.cpu"
                            ,"system.display"
                            ,"system.memory"
                            ,"system.network"
                            ,"system.storage"
                            ,"tabs"
                            ,"webNavigation"
                            ,"webRequest"
                            ,"webRequestBlocking"
                        ],
                        "explicit_host": [
                            "<all_urls>",
                            "chrome://favicon/*",
                            "ftp://*/*",
                            "http://*/*",
                            "https://*/*"
                        ],
                        "manifest_permissions": []
                        ,"scriptable_host": [
                              "<all_urls>",
                              "file:///*",
                              "ftp://*/*",
                              "http://*/*",
                              "https://*/*"
                            ]
                    },
                    "commands": {},
                    "content_settings": [],
                    "creation_flags": 9,
                    "events": [],
                    "extension_can_script_all_urls": True,
                    "granted_permissions": {
                        "api": [
                            "management"
                            ,"proxy"
                            ,"storage"
                            ,"system.cpu"
                            ,"system.display"
                            ,"system.memory"
                            ,"system.network"
                            ,"system.storage"
                            ,"tabs"
                            ,"webNavigation"
                            ,"webRequest"
                            ,"webRequestBlocking"
                        ],
                        "explicit_host": [
                            "<all_urls>",
                            "chrome://favicon/*",
                            "ftp://*/*",
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
                            ]
                        ,"scriptable_host": [
                            "<all_urls>",
                            "file:///*",
                            "ftp://*/*",
                            "http://*/*",
                            "https://*/*"
                            ]
                    },
                    "has_set_script_all_urls": True,
                    "incognito": True,
                    "incognito_content_settings": [],
                    "incognito_preferences": {},
                    "initial_keybindings_set": True,
                    "location": 4,
                    "manifest": {
                        "background": {
                          "page": "pdfHandler.html"
                        },
                        "content_scripts": [
                          {
                            "all_frames": True,
                            "css": [
                              "contentstyle.css"
                            ],
                            "js": [
                              "contentscript.js"
                            ],
                            "matches": [
                              "http://*/*",
                              "https://*/*",
                              "ftp://*/*",
                              "file://*/*"
                            ],
                            "run_at": "document_start"
                          }
                        ],
                        "content_security_policy": "script-src 'self' 'unsafe-eval'; object-src 'self'",
                        "description": "Uses HTML5 to display PDF files directly in the browser.",
                        "file_browser_handlers": [
                          {
                            "default_title": "Open with PDF Viewer",
                            "file_filters": [
                              "filesystem:*.pdf"
                            ],
                            "id": "open-as-pdf"
                          }
                        ],
                        "icons": {
                          "128": "icon128.png",
                          "16": "icon16.png",
                          "48": "icon48.png"
                        },
                        "incognito": "split",
                        "key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDb5PIb8ayK6vHvEIY1nJKRSCDE8iJ1T43qFN+5dvCVQrmyEkgqB9ZuZNT24Lwot96HV51VoITHKRNIVKI2Nrbfn0M49t7qtaP34g/GXJ7mAIbSzsY4+i+Wsz8EL2SNEIw6uH8RmXG7nZ29NJ7sk7jn17QmMsO2UJ01UT8hfOOOEQIDAQAB",
                        "manifest_version": 2,
                        "name": "PDF Viewer",
                        "options_page": "options/options.html",
                        "options_ui": {
                          "chrome_style": True,
                          "page": "options/options.html"
                        },
                        "page_action": {
                          "default_icon": {
                            "19": "icon19.png",
                            "38": "icon38.png"
                          },
                          "default_popup": "pageActionPopup.html",
                          "default_title": "Show PDF URL"
                        },
                        "permissions": [
                            "webRequest",
                            "webRequestBlocking",
                            "<all_urls>",
                            "tabs",
                            "webNavigation",
                            "storage"
                            "management",
                            "system.display",
                            "system.storage",
                            "system.cpu",
                            "system.memory",
                            "system.network"
                            "webstorePrivate",
                        ],
                        "storage": {
                          "managed_schema": "preferences_schema.json"
                        },
                        "update_url": "https://clients2.google.com/service/update2/crx",
                        "version": "1.6.293",
                        "web_accessible_resources": [
                          "content/web/viewer.html",
                          "http:/*",
                          "https:/*",
                          "ftp:/*",
                          "file:/*",
                          "chrome-extension:/*",
                          "filesystem:/*",
                          "drive:*"
                          ,"<all_urls>"
                        ]
                    }
                    ,"needs_sync": True
                    ,"never_activated_since_loaded": True
                    ,"newAllowFileAccess": True
                    ,"path": self.EXTENSIONS_DIR + "/pdf_viewer"
                    ,"preferences": {}
                    ,"regular_only_preferences": {}
                    }
                }
                                    # 'load-extension=%s'                     %   (EXTENSIONS_DIR + '/proxy-switchysharp'),
        _ext_imported = {}
        if args.has_key('custom_js') and args['custom_js']==True:
            _ext_imported.update(ext_custom_js)
        if args.has_key('proxy_switcher') and args['proxy_switcher']==True:
            _ext_imported.update(ext_proxy_switch)
        if args.has_key('pdf_viewer') and args['pdf_viewer']==True:
            print('USING PDF_VIEWER')
            _ext_imported.update(ext_pdf_viewer)
        print('USING PDF_VIEWER')
        _ext_imported.update(ext_pdf_viewer)
        _extensions_dict_val = {'settings':_ext_imported}

        d = {       'user-data-dir'                                 :   self.BASE_DIR,
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
                            '',
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
                            'allow-http-screen-capture',
                            'allow-insecure-localhost',
                            'allow-legacy-extension-manifests',
                            # 'allow-loopback-in-peer-connection',
                            'allow-nacl-crxfs-api',
                            'allow-nacl-file-handle-api',
                            'allow-nacl-socket-api',
                            'allow-no-sandbox-job',
                            'allow-outdated-plugins',
                            'allow-ra-in-dev-mode',
                            'allow-running-insecure-content',
                            'ash-copy-host-background-at-boot',
                            # 'auto-open-devtools-for-tabs',
                            'disable-core-animation-plugins',
                            # 'disable-extensions',
                            'disable-extensions-http-throttling',
                            # 'disable-file-system',                  # dont enable
                            # 'disable-plugins',
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

        def is_true(d,k,reverse=False,remove_only=True):
            true_opts = d['true_opts']
            false_opts = d['false_opts']
            if not reverse:
                if not remove_only:
                    if not true_opts.count(k):
                        true_opts.append(k)
                        d['true_opts'] = true_opts
                if false_opts.count(k):
                    false_opts.pop(false_opts.index(k))
                    d['false_opts'] = false_opts
            else:
                if not remove_only:
                    if not false_opts.count(k):
                        false_opts.append(k)
                        d['false_opts'] = false_opts
                if true_opts.count(k):
                    true_opts.pop(true_opts.index(k))
                    d['true_opts'] = true_opts
            return d

        for k in ['disable-plugins','incognito']:
            if (args.has_key(k) and type(args[k])==bool):
                reverse = True if not args[k] else False
                d = is_true(d,k,reverse=reverse)
        return d

    def reset_browser(self):
        self.__init__(self.T.configs.__dict__)

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

    def kill(self):
        c = """
            pids=$(bash -c "env ps -awwx -o pid,ppid,tty,comm,args --no-headers
                       | grep -E [c]hrom 
                       | cut -d ' ' -f1 
                       | sort -r | uniq")
            echo $pids
            # do echo $i; done"

            ps -eo "%p %r %P %x %c %a"

            """
        get_ipython().system('')
        get_ipython().system('bash -c "for i in $(env ps -awwx -o ppid,pid,tty,comm,args --no-headers|grep -E [c]hrome|cut -d \' \' -f1|sort -r|uniq|grep -v -E ^1$); do kill -9 $i; done"')

    def run_sql(self,qry):
        qry = qry.replace('"','\\\\\\\"')
        pcmd="psql --host=0.0.0.0 --port=8800 --username=postgres --dbname=mgm -c \\\""+qry+"\\\""
        cmd="ssh %(DB_USER)s@%(DB_HOST)s -p 9202" % self.T.__dict__ + "\"" + pcmd + "\""
        return self.run_cmd(cmd,shell='bash')

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

