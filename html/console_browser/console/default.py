
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
                                                ,'notes_idx_col'    :   'page_notes'
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
        self.path_history                   =   []

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
        def change_path():
            pass
        def iter_loop():
            if   len(res)==0:   pass
            elif len(res)==1:
                if   res=='q':  return False
                elif res=='m':
                    if self._path:
                        with open(self.notes_fpath,'a') as f:        f.write(self._path+'\n')
                        if debug:   print(          'marked '+self.notes_fpath)
                elif res=='P':
                    self.jump_uid           =   None
                    z                       =   idx_list.index(self._idx) - 1
                    if z < 0:
                        print(                  "This is the First RECORD.")
                    else:
                        self._idx           =   idx_list[ z ]
                        RUN                 =   gen_and_goto_pg(path_history='remove')
                        new_page            =   True
                        if debug:               print(self._path)
                elif res=='N':
                    if self.mark_skipped:
                        with open(self.notes_fpath,'a') as f:    f.write(self._path+'\n')
                    self.jump_uid           =   None
                    z                       =   idx_list.index(self._idx) + 1
                    if z >= len(idx_list):
                        print(                  "This is the Last RECORD.")
                    else:
                        self._idx           =   idx_list[ z ]
                        RUN                 =   gen_and_goto_pg(path_history='add')
                        new_page            =   True
                        if debug:               print(self._path)

                elif res=='p':
                    self.pgnum              =   self.exts.goto_prev_page()
                    self.path_history.append(   {'path':self._path,'page':self.pgnum})
                elif res=='n':
                    self.pgnum              =   self.exts.goto_next_page()
                    self.path_history.append(   {'path':self._path,'page':self.pgnum})
                elif res=='e':
                    self.pgnum              =   self.exts.goto_last_page()
                    self.path_history.append(   {'path':self._path,'page':self.pgnum})
                elif res=='f':
                    self.pgnum              =   self.exts.goto_first_page()
                    self.path_history.append(   {'path':self._path,'page':1})
                elif res=='L':
                    rotation                =   self.exts.set_rotation('left')
                    update(                     'rotation=%d'%rotation,is_prop=True)
                elif res=='R':
                    rotation                =   self.exts.set_rotation('right')
                    update(                     'rotation=%d'%rotation,is_prop=True)
                elif res=='r':
                    update(                     -1,is_repeat=True)
                elif res=='?':
                    print(                      ' ')
                    print(                      sorted_dict_str(RECORD.to_dict(),level=1))
                    # print(                      qry)
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
                    #             RUN             =  gen_and_goto_pg(path_history='add')
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
                    RUN                     =   gen_and_goto_pg(path_history='add')
                    new_page                =   True

                elif res[0]=='i':
                    update(                 _val,is_note=True)

        def gen_and_goto_pg(path_history='add'):
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
                self._attr                  =   self.RECORD[attr_col]
                self._path                  =   self.RECORD[url_col]
                br.open_page(                   self._path)
                if path_history=='add':
                    self.path_history.append(   {'path':self._path,'page':1})
                elif path_history=='remove':
                    self.path_history.pop(      -1)

            return
        def sorted_dict_str(_dict,max_key_str_len=0,level=0):
            if type(_dict)==str:
                _dict                           =   json.loads(_dict)
            if max_key_str_len:
                k_v_str                         =   '%-'+str(max_key_str_len+4)+'s : %s'
            else:
                k_v_str                         =   '%-'+str(max([len(k) for k in _dict.keys()])+4)+'s : %s'
            res                                 =   ['\n']
            for k,v in sorted(_dict.items()):
                if type(v)==dict:
                    res.append(                     k_v_str%(k,sorted_dict_str(v,level=level+1)))
                elif type(v)==str:
                    try:
                        json.loads(                 v)
                        res.append(                 k_v_str%(k,sorted_dict_str(v,level=level+1)))
                    except:
                        res.append(                 k_v_str%(k,v))
                else:
                    res.append(                     k_v_str%(k,v))
            indent_level                        =   str('\t' * level)
            indent_level_new_line               =   '\n%s' % indent_level
            _return                             =   indent_level_new_line.join(res) + indent_level + '\n'
            return _return
        def update(_val,**kwargs):
            if not _val:                    return
            is_note                     =   False if not kwargs.has_key('is_note') else kwargs['is_note']
            is_prop                     =   False if not kwargs.has_key('is_prop') else kwargs['is_prop']
            is_repeat                   =   False if not kwargs.has_key('is_repeat') else kwargs['is_repeat']

            self._attr                  =   self.RECORD[attr_col] if not hasattr(self,'_attr') else self._attr
            self._attr                  =   {} if not self._attr else self._attr
            self._attr                  =   self._attr if type(self._attr)==dict else json.loads( self._attr )
            pg_num                      =   self.exts.get_page_num()
            pg_key                      =   'page%05d' % pg_num
            self.pg_notes               =   {} if not self._attr.has_key(notes_idx_col) else self._attr[notes_idx_col]
            self.pg_notes               =   self.pg_notes if type(self.pg_notes)==dict else json.loads( self.pg_notes )
            self.this_pg_notes          =   [] if not self.pg_notes.has_key(pg_key) else self.pg_notes[pg_key]
            try:
                self.this_pg_notes      =   self.this_pg_notes if type(self.this_pg_notes)==list else eval( self.this_pg_notes )
            except:
                self.this_pg_notes      =   []

            if is_note:
                pass
            elif is_prop or str(_val).count('='):
                k,v                     =   _val.split('=')
                idx                     =   -1
                for i in range(len(self.this_pg_notes)):
                    it                  =   self.this_pg_notes[i]
                    if it.count('='):
                        _k,_v=it.split('=')
                        if k==_k:
                            self.this_pg_notes.pop( i)
                            break
            elif is_repeat:

                is_repeat_idx           =   _val if _val!=-1 else pg_num-1
                _pg_key                 =   'page%05d' % is_repeat_idx
                assert self.pg_notes.has_key(_pg_key)
                for it in self.pg_notes[_pg_key]:
                    update(                 it)
                return

            if not self.this_pg_notes.count(_val):
                self.this_pg_notes.append(  _val)
            self.pg_notes[pg_key]       =   self.this_pg_notes
            self._attr[notes_idx_col]   =   self.pg_notes

            if type(self._attr)==dict:
                self._attr              =   json.dumps( self._attr, indent=4, sort_keys=True)
            upd_qry                     =   '\n' + '\n'.join([
                                                self.qry_start.lstrip(' ')
                                                ,"_attr='" + self._attr + "'::json"
                                                ,"WHERE uid=%s;" % self.RECORD[uid_col]
                                            ]) + '\n'
            print '\n'.join(                ['\t'+it for it in upd_qry.split('\n')])
            self.T.to_sql(                  upd_qry )
            self.df.set_value(              self._idx, self.attr_col, self._attr)
            self.RECORD                 =   self.df.ix[self._idx,:]
            self._attr                  =   self.RECORD[attr_col]

        def sig_int(signal, frame):
            self.RUN_LOOP                   =   False
        self.T.signal.signal(                   self.T.signal.SIGINT, sig_int)

        locals().update(                        **self.__dict__)
        globals().update(                       **self.__dict__)
        locals().update(                        **self.T.__dict__)
        globals().update(                       **self.T.__dict__)

        self._load_dataframe()

        idx_list                            =   df.index.astype(int).tolist()
        col_list                            =   df.columns.astype(str).tolist()
        uid_list                            =   df[ uid_col ].astype(str).tolist()
        path_list                           =   df[ url_col ].astype(str).tolist()
        attr_list                           =   df[ attr_col ].tolist()
        self.path_uid_dict                  =   dict(zip(path_list,uid_list))
        self.path_idx_dict                  =   dict(zip(path_list,idx_list))
        self.path_attr_dict                 =   dict(zip(path_list,attr_list))


        current                             =   self.exts.get_page_path()
        self._idx                           =   df.first_valid_index().tolist() if not path_list.count(current) else path_list.index(current)
        self.RECORD                         =   df.ix[self._idx,:]
        self._attr                          =   self.RECORD[attr_col]
        # self._path                          =   path_list[self._idx]

        self.qry_clean                      =   self.T.re.sub(r'[\s\n\t][\s\t\n]+',' ',self.select_query.lower())
        self.tbl_name                       =   self.T.re.sub(r'(.*) from ([^ ]+)(.*)','\\2',self.qry_clean)
        self.qry_start                      =   " UPDATE " + self.tbl_name + " SET "
        self.jump_query                     =   self.select_query + ' AND uid = %d ; ' if not hasattr(self,'jump_query') or not self.jump_query else self.jump_query
        self.jump_uid                       =   None
        RUN                                 =   gen_and_goto_pg(path_history='add')
        get_ipython().system(                   u'%(shell)s -c "cd %(script_dir)s; date --iso-8601=seconds >> %(notes_fpath)s"' % self.__dict__)

        # signal.pause()

        self.RUN_LOOP                       =   True
        new_page                            =   True
        print('\n\nStarting Loop.\n')
        while self.RUN_LOOP==True:

            print(                          sorted_dict_str(self.RECORD.to_dict(),level=1))

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
                                                'L'         : 'rotate 90 left (counter-clockwise)',
                                                'R'         : 'rotate 90 right (clockwise)',
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

            if res.count(':'):
                idx                         =   res[res.find(':')+1:]
                res                         =   res[:len(res)-len(idx)-1]
                idx                         =   idx.split(':')
                if len(idx)==1:
                    idx.append(                 self.exts.get_page_count())
                idx                         =   [int(it) for it in idx]

                orig_res = res
                for _loop in range(idx[0],idx[1]+1):
                    print '_loop:',_loop
                    res = orig_res
                    LOOP                    =   iter_loop()
                    if LOOP==False:             return
                    res = 'n'
                    LOOP                    =   iter_loop()
                    if LOOP==False:             return


                print idx
                raise SystemError

            else:


                LOOP = iter_loop()
                if LOOP==False:                 return



            if debug:           print           qry

