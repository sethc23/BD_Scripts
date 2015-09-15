#!/usr/bin/python
# PYTHON_ARGCOMPLETE_OK
from os                                     import environ                  as os_environ
from sys                                    import path                     as py_path
py_path.append(                             os_environ['HOME'] + '/.scripts')
from system_argparse                        import *


class pb_tools:
    """Provides quick interface for accessing pastebin data"""

    def __init__(self):
        py_path.insert(                 0,'./')
        from pastebin_python            import PastebinPython
        user_name                   =   'mech_coder'
        passw                       =   'Delivery100%'
        dev_key                     =   '4f26d1cb7a08f03b02ab24dae43bc431'
        pb                          =   PastebinPython(api_dev_key=dev_key)
        pb.createAPIUserKey(            user_name,passw)
        self.pb                     =   pb

    @arg('info',nargs='?',default=['ALL'],
            choices=['ALL','params','formats'],
            help='type of info sought')
    def info(self,args):
        """Print out paste parameter info"""
        import urllib2
        from bs4 import BeautifulSoup
        import unicodedata
        import json
        src_page                            =   'http://pastebin.com/api#2'
        src                                 =   urllib2.urlopen(src_page, data=None,timeout=3600)
        h                                   =   BeautifulSoup(src)
        if args.info=='formats' or args.info.lower()=='all':
            formats                         =   h.find('a',attrs={'name':'6'}).previous_sibling.previous_sibling
            uni_formats                     =   formats.decode_contents()
            str_formats                     =   unicodedata.normalize('NFKD',uni_formats).encode('ascii','ignore')
            num_formats                     =   str_formats[str_formats.find('<br/>')+5:].strip(' \n').rstrip('<br/>').split('<br/>')
            dict_formats                    =   {}
            for it in num_formats:
                k,v                         =   it.strip().split(' = ')
                dict_formats.update(            {k:v})
            print '\nFormat Types:'
            print json.dumps(                   dict_formats, sort_keys=True,indent=4, separators=(',', ':\t\t'))
        if args.info=='params' or args.info.lower()=='all':
            params                          =   h.find('a',attrs={'name':'7'}).previous_sibling.previous_sibling
            uni_params                      =   params.decode_contents()
            str_params                      =   unicodedata.normalize('NFKD',uni_params).encode('ascii','ignore')
            num_params                      =   str_params[str_params.find('<br/>')+5:].strip(' \n\t\r').rstrip('<br/>').split('<br/>')
            dict_params                     =   {}
            for it in num_params:
                k,v                         =   it.strip(' \n\t\r').split(' = ')
                dict_params.update(            {k:v})
            print '\nExpiration Types:'
            print json.dumps(                   dict_params, sort_keys=True,indent=4, separators=(',', ':\t\t'))
            print '\nPublication Types:\n\t\tpublic = 0, unlisted = 1, private = 2'

    @arg('-i','--input',
            help='content to paste \n\tNOTE: content can also be piped, see --usage')
    @arg('-t','--title',default=parse_choices_from_exec('date +%Y.%m.%d').strip('\n'),
            help='title of paste')
    @arg('-f','--format',default='None',
            help='syntacical format of content')
    @arg('-p','--privacy',default='Public',
            help='how public or private the paste should be')
    @arg('-e','--expires',default='1H',
            help='when the paste should expire')
    @arg('--usage',
        help='\n'.join(['$ ls | ./filein.py          # Prints a directory listing to stdout',
                        '$ ./filein.py /etc/passwd   # Reads /etc/passwd to stdout.',
                        '$ ./filein.py < /etc/passwd # Reads /etc/passwd to stdout.']))
    @arg('---',default=[],dest='input')
    def create(self,args):
        """Create new paste"""


        i_trace()
        print self.pb.createPaste(args.content, api_paste_name=args.title,
               api_paste_format=args.format, api_paste_private=args.privacy,
               api_paste_expire_date=args.expiration)

    @arg('paste_key',nargs='?')
    def get(self,args):
        """Print raw output for a paste"""
        i_trace()
        print self.pb.getPasteRawOutput(args.paste_key)

    @arg()
    def list(self,args):
        """List title-unique pastes, sorted by provided criteria"""
        import pandas as pd

        res                                 =   self.pb.listUserPastes(api_results_limit=500)

        cols                                =   res[0].keys()
        df                                  =   pd.DataFrame(columns=cols)
        for it in res:
            df                              =   df.append(it,ignore_index=True)
        df['paste_date']                    =   df.paste_date.map(lambda s:
                                                    pd.to_datetime(time.strftime('%Y-%m-%d %H:%M:%S',
                                                    time.localtime(float(s)))))
        df['paste_expire_date']             =   df.paste_expire_date.map(lambda s:
                                                    pd.to_datetime(time.strftime('%Y-%m-%d %H:%M:%S',
                                                    time.localtime(float(s)))))
        print len(df),'total pastes (query limit is 500)'
        all_titles                          =   df.paste_title.tolist()
        ndf                                 =   pd.DataFrame(data={'uniq_title':df.paste_title.unique().tolist()})
        ndf['title_cnt']                    =   ndf.uniq_title.map(lambda s: all_titles.count(s))
        ndf['oldest']                       =   ndf.uniq_title.map(lambda s: df[df.paste_title==s].paste_date.min())
        ndf['latest']                       =   ndf.uniq_title.map(lambda s: df[df.paste_title==s].paste_date.max())
        ndf['expire_next']                  =   ndf.uniq_title.map(lambda s: df[df.paste_title==s].paste_expire_date.min())
        ndf['expire_last']                  =   ndf.uniq_title.map(lambda s: df[df.paste_title==s].paste_expire_date.max())
        print ndf

    @arg('-pk','--paste-key',help='delete paste using provided paste-key')
    @arg('-RT','--re-title',action='append',help='delete pastes matching regex title(s)')
    @arg('-RC','--re-content',action='append',help='delete pastes matching regex content(s)')
    @arg('-D','--dry-run',help='list paste(s) that will be deleted')
    @arg('-U','--non-unique',help='delete all pastes with duplicate titles except the most recent duplicate')
    def delete(self,args):
        """Delete pastes matching one or several criteria"""
        if args.match=='re':
            to_delete_errors                =   df[df.paste_title.isin(other_errors)].paste_key.tolist()
            for it in to_delete_errors:
                pb.deletePaste(                 it)

        if args.match--'unique':
            delete_idx                      =   []
            for _,it in ndf.iterrows():
                if it.title_cnt>1:
                    delete_idx.extend(          df[(df.paste_title==it.uniq_title)&(df.paste_date!=it.latest)].index.tolist() )
            to_delete_pastes                =   df[df.index.isin(delete_idx)].paste_key.tolist()
            assert len(df)-len(ndf)        ==   len(to_delete_pastes)
            for it in to_delete_pastes:
                pb.deletePaste(                 it)

import sys
if __name__ == '__main__':

    if not sys.stdin.isatty():
        global input_text
        import fileinput

        fd_stdin,input_text                     =   fileinput.input('-'),[]
        while True:
            f_descr_1                           =   fd_stdin.fileno()
            line                                =   ''.join([seg for seg in fd_stdin.readline()])
            f_descr_2                           =   fd_stdin.fileno()
            if f_descr_1==f_descr_2==-1 or fd_stdin.lineno()==0:
                break
            if line:
                # print line
                input_text.append(                  line)
        input_text                              =   ''.join(input_text).strip('\n')
        run_custom_argparse({'input_text':input_text})
    else:
        run_custom_argparse()

# TODO: add feature for saving collected 'info' for local queries and choice selection
# TODO: add feature for receiving content via stdin
# TODO: add feature for locally storing titles,links for 500 pastes (for quick retrieval)
# TODO: add feature for saving defaults (or from last used options)
# TODO: add feature for sorting list results
# TODO: add examples of create --usage

