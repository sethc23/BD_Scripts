
"""

"""

from extensions import *

class Console:
    """
        Debug Logs:

            /home/kali/BD_Scripts/html/webdrivers/chrome/profiles/default/chromedriver.log
            /home/kali/BD_Scripts/html/webdrivers/chrome/profiles/default/chrome_debug.log
            /home/kali/BD_Scripts/html/webdrivers/chrome/profiles/default/net-log.log


            /home/kali/BD_Scripts/html/webdrivers/chrome/profiles/default'

            /home/kali/BD_Scripts/html/webdrivers/chrome/profiles/default/net-log.log'
            --log-path=/home/kali/BD_Scripts/html/webdrivers/chrome/profiles/default/chromedriver.log'
            'load-extension=/home/kali/BD_Scripts/html/webdrivers/chrome/extensions/custom_js/poakhlngfciodnhlhhgnaaelnpjljija/2.1.40_0',

            br.webdriver_config.dc['chromeOptions']['prefs']['download.default_directory']
                'savefile.default_directory': '/home/kali/BD_Scripts/html/webdrivers/chrome/profiles/default/DOWNLOADS'
            br.webdriver_config.dc['chromeOptions']['prefs']['savefile.default_directory']
                '/home/kali/BD_Scripts/html/webdrivers/chrome/profiles/default/DOWNLOADS'

        check_args = ['user-data-dir','log-net-log']
        for it in br.webdriver_config.dc['chromeOptions']['args']:
            try:
                k,v = it.split('=')
                if check_args.count(k):
                    print '%s = %s' % (k.strip('- '),v.strip('- '))
            except:
                pass

    """

    def __init__(self,_parent,kwargs={}):
        self                                =   _parent.T.To_Sub_Classes(self,_parent)
        T = self.T                          =   _parent.T

        config_defaults                     =   {
                                                'notes_fpath'       :   T.os.path.abspath(T.os.path.join(
                                                                            T.os.path.dirname(__file__)
                                                                            ,'../logs/console_notes'))
                                                ,'select_query'     :   ''
                                                ,'update_query'     :   ''
                                                ,'sort_select_by'   :   'uid'
                                                ,'date_format'      :   '%m/%d/%y'
                                                ,'skip_marked'      :   True
                                                ,'mark_skipped'     :   True
                                                ,'uid_col'          :   'uid'
                                                ,'attr_col'         :   '_attr'
                                                ,'url_col'          :   'fpath'
                                                ,'url_substitution' :   ('/home/ub2/ARCHIVE','http://10.0.0.52:14382/files')
                                                ,'npages_col'       :   'npages'
                                                ,'regex_fpath'      :   ''
                                                ,'val_dict'         :   {}
                                                ,'_path'            :   ''
                                                ,'jump_uid'         :   ''
                                                }
        console_config                      =   {} if not hasattr(self.T,'console_config') else self.T['console_config']
        if type(console_config)==dict:
            config_defaults.update(             console_config)
        elif hasattr(console_config,'__dict__'):
            config_defaults.update(             console_config.__dict__)
        else:
            print(                              'Unrecognized format of "console_config":',str(console_config))
        ALL_CONFIG_PARAMS                   =   config_defaults
        self._config(                           ALL_CONFIG_PARAMS)
        self.exts                           =   PDF_Viewer(self)

    def __update__(self,upd_dict):
        for k,v in upd_dict.iteritems():
            self.__dict__.update(               {k:v})

    def _load_dataframe(self):
        assert self.select_query,'Missing value for "select_query":' + self.select_query
        #assert self.update_query,'Missing value for "update_query":' + self.update_query
        df                                  =   self.T.pd.read_sql(self.select_query,self.T.eng)
        if self.sort_select_by:    df       =   df.sort_values(self.sort_select_by).reset_index(drop=True)

        df[self.url_col]                    =   df[self.url_col].map(lambda s: s.replace(*self.url_substitution))
        df[self.attr_col]                   =   df[self.attr_col].map(lambda d:
                                                    None if not d else self.T.json.dumps(d,indent=4,sort_keys=True)).tolist()
        # df['effective_date']                = df.effective_date.map(lambda s: None if s.__class__.__name__=='NaTType' else s.strftime('%m/%d/%y'))

        if self.skip_marked and self.T.os.path.exists(self.notes_fpath):
            print('\nskipping files marked in %s\n' % self.notes_fpath)
            fpath_list,idx_list             =   df[self.url_col].tolist(),[]
            with open(self.notes_fpath,'r') as f:
                x                           =   f.read().split('\n')
            for l in x:
                try:
                    if l[0]=='/' and fpath_list.count(l)!=0:
                        _idx                =   fpath_list.index(l)
                        if idx_list.count(_idx)==0:
                            idx_list.append(    _idx)
                except:
                    pass
            df                              =   df[df.index.isin(idx_list)==False].reset_index(drop=True)
        if self.sort_select_by:    df       =   df.sort_values(self.sort_select_by).reset_index(drop=True)
        self.df                             =   df

    def _config(self,kwargs):
        self.__update__(                        kwargs)
        locals().update(                        **self.__dict__)
        globals().update(                       **self.__dict__)
        locals().update(                        **self.T.__dict__)
        globals().update(                       **self.T.__dict__)

        self.shell                          =   self.T.run_cmd('which zsh')
        self.script_dir                     =   __file__[:__file__.rfind('/')]

        self._load_dataframe()

        if regex_fpath:
            with open(regex_fpath,'r') as f:
                self.regex_list             =   f.read().split('\n')
        self.T.br.window.implicitly_wait(       2)

    def reset_console(self,browser_class_obj):
        browser_class_obj.cs.__init__(browser_class_obj)

    def run_review(self,debug=False):
        # def get_ocr(pg_num):
        #     self.pg_num                     =   pg_num
        #     c                               =   ';\n'.join([
        #                                                 'cd /home/kali/PROJECTS/INTARCIA/scripts',
        #                                                 'pdftotext \
        #                                                     -f %(pg_num)s \
        #                                                     -l %(pg_num)s \
        #                                                     review/tmp.pdf - 2>&1' % self.__dict__,
        #                                             ])
        #     ocr_content                     =   ' '.join(get_ipython().getoutput(
        #                                                  u'%(shell)s -c "' % self.__dict__ + c + '"'))
        #     return                              ocr_content
        def gen_and_goto_pg():

            if hasattr(self,'jump_uid') and self.jump_uid:
                nf                          =   pd.read_sql(self.jump_query % self.jump_uid,eng)
                nf[self.url_col]            =   nf.fpath.map(lambda s: s.replace(*self.url_substitution))
                self.RECORD                 =   nf.ix[idx_list[0],:]
                self.new_path               =   self.RECORD[ self.url_col ]
            elif self._idx>=len(path_list):
                print(                          "END OF FILES")
                return
            else:
                self.new_path               =   path_list[self._idx]

            if self._path!=self.new_path:
                self.RECORD                 =   df.ix[self.path_idx_dict[self.new_path],:]
                br.open_page(                   self.RECORD[url_col])
                self._path                  =   self.new_path
                # self._attr                  =   r[attr_col]

            return
        def update():
            pass
        def sig_int(signal, frame):
            self.RUN_LOOP                   =   False
        self.T.signal.signal(                   self.T.signal.SIGINT, sig_int)

        locals().update(                        **self.__dict__)
        globals().update(                       **self.__dict__)
        locals().update(                        **self.T.__dict__)
        globals().update(                       **self.T.__dict__)

        idx_list                            =   df.index.astype(int).tolist()
        col_list                            =   df.columns.astype(str).tolist()
        uid_list                            =   df[ uid_col ].astype(str).tolist()
        path_list                           =   df[ url_col ].astype(str).tolist()
        attr_list                           =   df[ attr_col ].tolist()
        self.path_uid_dict                  =   dict(zip(path_list,uid_list))
        self.path_idx_dict                  =   dict(zip(path_list,idx_list))
        self.path_attr_dict                 =   dict(zip(path_list,attr_list))

        self.RECORD                         =   df.ix[idx_list[0],:]

        self._idx                           =   df.first_valid_index().tolist()
        self._path                          =   path_list[self._idx]
        # self._attr                          =   self.path_attr_dict[self._path]

        self.qry_clean                      =   self.T.re.sub(r'[\s\n\t][\s\t\n]+',' ',self.select_query.lower())
        self.tbl_name                       =   self.T.re.sub(r'(.*) from ([^ ]+)(.*)','\\2',self.qry_clean)
        self.qry_start                      =   " UPDATE " + self.tbl_name + " SET "
        self.jump_query                     =   self.select_query + ' AND uid = %d ; ' if not hasattr(self,'jump_query') or not self.jump_query else self.jump_query
        self.jump_uid                       =   None
        RUN                                 =   gen_and_goto_pg()
        get_ipython().system(                   u'%(shell)s -c "cd %(script_dir)s; date --iso-8601=seconds >> %(notes_fpath)s"' % self.__dict__)

        # signal.pause()

        self.RUN_LOOP                       =   True
        new_page                            =   True
        print('\n\nStarting Loop.\n')
        while self.RUN_LOOP==True:

            if new_page:
                print( self.T.json.dumps(       self.RECORD.to_dict(), indent=4, sort_keys=True) )
                print ''
                new_page                    = False

            # _update                         =   self.T.json.dumps({'pg_notes' : '; '.join(self.pg_notes)})
            # self.jump_query                 =   '\n\t' + '\n\t'.join([
            #                                         self.qry_start
            #                                         ,"_attr=json_append('" + _update + "'::json,_attr::json)"
            #                                         ,"WHERE uid=%s;" % self.path_uid_dict[self._path]
            #                                     ])
            # upd_qry                         =   '\n\t' + '\n\t'.join([
            #                                         self.qry_start
            #                                         ,"_attr='" + self._attr + "'::json"
            #                                         ,"WHERE uid=%s;" % self.path_uid_dict[self._path]
            #                                     ])

            res                             =   raw_input(' ')
            print(                              ' ')
            OPTS                            =   {

                                                'q'         : 'quit',
                                                'm'         : 'mark file (append filepath to save file)',
                                                'P'         : 'goto previous file',
                                                'N'         : 'goto next file',
                                                'p'         : 'goto previous page in file',
                                                'n'         : 'goto next page in file',
                                                'f'         : 'goto first page of file',
                                                'e'         : 'goto last page of file',
                                                '?'         : 'show info about file and update query',
                                                'o'         : 'print OCR of file',
                                                'D'         : 'execute update query and goto next file',

                                                're [str]'  : 'test,save,edit,remove regex queries re: OCR text',
                                                '! [str]'   : 'execute ipython command in this namespace',
                                                'j [int]'   : 'jump to file having input uid',

                                                }
                                                #
                                                # ? CREATE FUNCTION FOR CUSTOMIZING SHORT-HANDS ON-THE-GO ?
                                                #   list
                                                #   new
                                                #   edit
                                                #   del
                                                #
                                                # 't [str]'   : 'set contract type',
                                                # 'd [str]'   : 'set contract department',
                                                # 's [str]'   : 'set contract status',
                                                # 'n [str]'   : 'set contract title',
                                                # 'd [str]'   : 'set effective date',
                                                # 'v [str]'   : 'set vendor name',
                                                # 'a [str]'   : 'set address',
                                                # 'x [str]'   : 'set expiration',
                                                # 'r [str]'   : 'set requestor',
                                                # 'i [str]'   : 'append/set notes',

            if   len(res)==0:   pass
            elif len(res)==1:
                if   res=='q':  break
                elif res=='m':
                    if self._path:
                        with open(self.notes_fpath,'a') as f:        f.write(self._path+'\n')
                        if debug:   print(          'marked '+self.notes_fpath)
                elif res=='P':
                    self.jump_uid           =   None
                    z                       =   idx_list.index(self._idx) - 1
                    if z < 0:
                        pass
                    else:
                        self._idx           =   idx_list[ z ]
                        self.RECORD         =   df.ix[self._idx,:]
                        RUN                 =   gen_and_goto_pg()
                        new_page            =   True
                        if debug:               print(self._path)
                elif res=='N':
                    if self.mark_skipped:
                        with open(self.notes_fpath,'a') as f:    f.write(self._path+'\n')
                    self.jump_uid           =   None
                    z                       =   idx_list.index(self._idx) + 1
                    if z >= len(idx_list):
                        pass
                    else:
                        self._idx           =   idx_list[ z ]
                        self.RECORD         =   df.ix[self._idx,:]
                        RUN                 =   gen_and_goto_pg()
                        new_page            =   True
                        if debug:               print(self._path)

                elif res=='p':                  self.exts.goto_prev_page()
                elif res=='n':                  self.exts.goto_next_page()
                elif res=='e':                  self.exts.goto_last_page(   )
                elif res=='f':                  self.exts.goto_first_page()
                elif res=='?':
                    print(                      ' ')
                    print(                      qry)
                    print(                      ' ')
                elif res=='o':  print(          self.exts.get_page_text_content())
                # elif res=='D':
                    # print                       qry
                    # if self.pg_notes:
                    #     if debug:   print(          qry)
                    #     else:
                    #         try:
                    #             print               qry
                    #             to_sql(             qry)
                    #             print(              'DB updated')
                    #             self.pg_notes   =   []
                    #             self.jump_uid   =   None
                    #             self._idx  +=   1
                    #             self.pg_num     =   1
                    #             RUN             =  gen_and_goto_pg()
                    #         except:
                    #             print(              '\nQRY FAILED: %s\n' % qry)

            # elif res[:3]=='re ':
                #     """
                #         test single
                #         test all
                #         append regex
                #         edit regex

                #     """
                #     print(                          ' ')
                #     r                           =   res[3:]
                #     if   r    =='?':
                #         for it in regex_list:
                #             print(                  re.search(r'%s' % it,OCR))
                #     elif r[:2]=='l ':
                #         pt                      =   0
                #         for it in regex_list:
                #             print(                  '%s: %s' % (str(pt),it))
                #             pt                 +=   1
                #     elif r[:2]=='a ':
                #         _regex                  =   r[2:]
                #         regex_list.append(          _regex)
                #         with open(regex_fpath,'w') as f:        f.write('\n'.join(regex_list))
                #         print(                      'regex appended')
                #     elif r[:2]=='d ':
                #         _idx                    =   int(r[2:])
                #         z                       =   regex_list.pop(_idx)
                #         with open(regex_fpath,'w') as f:        f.write('\n'.join(regex_list))
                #         print(                      'dropped regex: %s' % z)
                #     elif r[:2]=='t ':
                #         _regex                  =   r[2:]
                #         print(                      re.search(r'%s' % _regex,OCR))

            elif res[0]=='!':
                try:
                    print                           '\n'
                    exec res[1:] in globals(),locals()
                    print                           '\n'
                except Exception as e:
                    print "ERROR:"
                    print type(e)       # the exception instance
                    print e.args        # arguments stored in .args
                    print e             # __str__ allows args to be printed directly
                    print '\n'

            elif res[1]==' ' \
                and res[2:].strip(' '):
                _val                        =   res[2:]

                if   res[0]=='j':
                    self.jump_uid           =   _val if not _val.isdigit() else int(_val)
                    RUN                     =   gen_and_goto_pg()
                    new_page                =   True

                elif res[0]=='i':
                    pg_key                  =   'page%05d' % self.exts.get_page_num()
                    if self._attr:
                        if type( self._attr )!=dict:
                            self._attr      =   json.loads( self._attr )
                        self.pg_notes       =   [] if not self._attr.has_key(pg_key) else self._attr[pg_key]
                        self.pg_notes.append(   _val)
                        self._attr[pg_key]  =   self.pg_notes
                    else:
                        self._attr          =   {pg_key:[_val]}

                    if type(self._attr)==dict:
                        self._attr          =   json.dumps( self._attr, indent=4, sort_keys=True)
                    upd_qry                 =   '\n' + '\n'.join([
                                                    self.qry_start.lstrip(' ')
                                                    ,"_attr='" + self._attr + "'::json"
                                                    ,"WHERE uid=%s;" % self.path_uid_dict[self._path]
                                                ]) + '\n'
                    print '\n'.join(['\t'+it for it in upd_qry.split('\n')])
                    # self.T.to_sql(              upd_qry )
                    df.set_value(self._idx, self.attr_col, self._attr)


            if debug:           print           qry

