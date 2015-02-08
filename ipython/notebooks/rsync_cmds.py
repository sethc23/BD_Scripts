
from os import system as os_cmd
from os.path import abspath
from subprocess import Popen as sub_popen
from subprocess import PIPE as sub_PIPE
from mounted_shares import mnt_shares
from datetime import datetime as dt

# INITIAL SETUP
f               = __file__
this_dir        = f[:f.rfind('/')-1]
mnt_shares(['Macbook','mbp1','ec2'])
rsync_options   = [ 'verbose','verbose','recursive','archive','update','one-file-system',
                    'compress','prune-empty-dirs','itemize-changes']

def get_rsync_cmd(T):
    c,T_keys    =   ['rsync'],T.keys()
    if T_keys.count('options'):               [ c.append('--'+it) for it in T['options'] ]
    rsync_cmd   =   [' '.join(c)]
    if T_keys.count('excl_pattern'):          rsync_cmd.append('--exclude-from=%(excl_file)s'%T)
    if T_keys.count('incl_pattern'):          rsync_cmd.append('--include-from=%(incl_file)s'%T)
    if T_keys.count('file_list_txt'):         rsync_cmd.append('--files-from=%(file_list_txt)s'%T)
    if T_keys.count('log_txt'):               rsync_cmd.append('--log-file=%(log_txt)s'%T)
    rsync_cmd.extend([  '--outbuf=L',
                        '%(src_dir)s'%T,
                        '%(dest_dir)s'%T])
    return ' '.join([it for it in rsync_cmd if it!=''])

def pg_dump_s3_and_ec2_into_s3():
    server_cmds     =   {'mbp2' : '/opt/local/lib/postgresql93/bin/pg_dump',
                         'ec2'  : '/usr/bin/pg_dump', }
    server_dbs      =   {'mbp2' : [ 'routing', ],
                         'ec2'  : [ 'aprinto', ], }
    dump_paths      =   {'mbp2' : '/Users/admin/.pg_dump',
                         'ec2'  : '/home/ec2-user/.pg_dump', }
    for k,v in server_cmds.iteritems():
        dump_files = []
        for db in server_dbs[k]:
            fpath       =   '%s/%s_%s_%s.sql'%(dump_paths[k],k,db,dt.strftime(dt.now(),'%Y_%m_%d'))
            fname       =   fpath[fpath.rfind('/')+1:]
            cmd         =   """%s -d %s -h 0.0.0.0 -p 8800 --username=postgres > %s;
                            """.replace('\n','').replace('\t','').strip()%(v,db,fpath)
            if k=='ec2':    cmd = "ssh ec2 '"+cmd[:-1]+"'"
            proc        =   sub_popen([cmd], stdout=sub_PIPE, shell=True)
            (t, err)    =   proc.communicate()

            dump_files.append(fname)

        if k!='mbp2':
            T   =   {'options'      :   rsync_options,
                     'sync_items'   :   dump_files,
                     'file_list_txt':   abspath(this_dir+'/../rsync/file_list.txt'),
                     'log_txt'      :   abspath(this_dir+'/../rsync/pg_dump_s3_and_ec2_into_s3.log'),
                     'src_dir'      :   '/Volumes/ec2/.pg_dump',
                     'dest_dir'     :   dump_paths['mbp2'],}
            os_cmd('rm %(file_list_txt)s'%T)
            with open('%(file_list_txt)s'%T, 'a') as f:     f.write('\n'.join(T['sync_items']))
            rsync_cmd   =   get_rsync_cmd(T)
            proc        =   sub_popen([rsync_cmd], stdout=sub_PIPE, shell=True)
            (t, err)    =   proc.communicate()
    return True
def rsync_s1_to_s3():
    T           =   {'options'      :   rsync_options,
                     'sync_items'   :   [ '/SERVER1','.alias_s1' ],
                     'file_list_txt':   abspath(this_dir+'/../rsync/file_list.txt'),
                     'log_txt'      :   abspath(this_dir+'/../rsync/rsync_s1.log'),
                     'src_dir'      :   '/Volumes/mbp1/Users/admin',
                     'dest_dir'     :   '/Users/admin'}

    os_cmd('rm %(file_list_txt)s'%T)
    with open('%(file_list_txt)s'%T, 'a') as f:
        f.write('\n'.join(T['sync_items']))
    rsync_cmd   =   get_rsync_cmd(T)
    proc        =   sub_popen([rsync_cmd], stdout=sub_PIPE, shell=True)
    (t, err)    =   proc.communicate()
    return True
def rsync_ipy2_in_s2():
    """
    Copies all ipython notebooks into /Volumes/Macbook/Users/admin/SERVER2/ipython/notebooks
    """

    T           =   {'options'      :   rsync_options,
                     'sync_items'   :   [ '/ipython', ],
                     'file_list_txt':   abspath(this_dir+'/../rsync/file_list.txt'),
                     'excl_pattern' :   [ '*.DS_Store*','ipython/ipython*','ENV/*','.ipynb_checkpoints*','ipython/examples*' ],
                     'excl_file'    :   abspath(this_dir+'/../rsync/rsync_excl.txt'),
                     'log_txt'      :   abspath(this_dir+'/../rsync/rsync_ipy2_in_s2.log'),
                     'src_dir'      :   '/Volumes/Macbook/Users/admin/SERVER2/BD_Scripts',
                     'dest_dir'     :   '/Volumes/Macbook/Users/admin/SERVER2'}

    os_cmd('rm %(excl_file)s %(file_list_txt)s'%T)
    with open('%(excl_file)s'%T, 'a') as f:
        f.write('\n'.join(T['excl_pattern']))
    with open('%(file_list_txt)s'%T, 'a') as f:
        f.write('\n'.join(T['sync_items']))
    rsync_cmd   =   get_rsync_cmd(T)
    proc        =   sub_popen([rsync_cmd], stdout=sub_PIPE, shell=True)
    (t, err)    =   proc.communicate()
    return True
def rsync_s2_to_s3():
    """
    Pull from Macbook onto mbp2
    """

    T           =   {'options'      :   rsync_options,
                     'sync_items'   :   [ '/SERVER2','.alias_s2','/.ipython/profile_nbserver', ],
                     'file_list_txt':   abspath(this_dir+'/../rsync/file_list.txt'),
                     'excl_pattern' :   [ '*.DS_Store*', '*.pid',
                                          'profile_nbserver/log*','profile_nbserver/pid*',
                                          'profile_nbserver/security*'],
                     'excl_file'    :   abspath(this_dir+'/../rsync/rsync_excl.txt'),
                     'log_txt'      :   abspath(this_dir+'/../rsync/rsync_s2_to_s3.log'),
                     'src_dir'      :   '/Volumes/Macbook/Users/admin',
                     'dest_dir'     :   '/Users/admin'}
    os_cmd('rm %(excl_file)s %(file_list_txt)s'%T)
    with open('%(excl_file)s'%T, 'a') as f:         f.write('\n'.join(T['excl_pattern']))
    with open('%(file_list_txt)s'%T, 'a') as f:     f.write('\n'.join(T['sync_items']))
    rsync_cmd   =   get_rsync_cmd(T)
    proc        =   sub_popen([rsync_cmd], stdout=sub_PIPE, shell=True)
    (t, err)    =   proc.communicate()
    return True
def rsync_s4_to_s3():
    """ Pull ec2 to mbp2. """

    T           =   {'options'      :   rsync_options,
                     'sync_items'   :   [ '.alias_s4','/SERVER4','/aprinto','/aporo', ],
                     'file_list_txt':   abspath(this_dir+'/../rsync/file_list.txt'),
                     'excl_pattern' :   [ '*.DS_Store*','*.sock','*.pid','ENV*','.git*' ],
                     'excl_file'    :   abspath(this_dir+'/../rsync/rsync_excl.txt'),
                     'log_txt'      :   abspath(this_dir+'/../rsync/rsync_s4_to_s3.log'),
                     'src_dir'      :   '/Volumes/ec2',
                     'dest_dir'     :   '/Users/admin'}
    os_cmd('rm %(file_list_txt)s %(excl_file)s'%T)
    with open('%(file_list_txt)s'%T, 'a') as f:     f.write('\n'.join(T['sync_items']))
    with open('%(excl_file)s'%T, 'a') as f:         f.write('\n'.join(T['excl_pattern']))
    rsync_cmd   =   get_rsync_cmd(T)
    proc        =   sub_popen([rsync_cmd], stdout=sub_PIPE, shell=True)
    (t, err)    =   proc.communicate()
    return True
def rsync_s3_to_s1_and_s2():
    T           =   {'options'      :   rsync_options,
                     'sync_items'   :   [ '/SERVER1','.alias_s1',
                                          '/SERVER2','.alias_s2',
                                          '/SERVER3','.alias_s3',
                                          '/SERVER4','.alias_s4',
                                          '/aprinto','/aporo',],
                     'file_list_txt':   abspath(this_dir+'/../rsync/file_list.txt'),
                     'excl_pattern' :   [ '*.DS_Store*','*.sock','*.pid','pagc-code-361-branches-sew-refactor2',
                                          'aprinto/ENV*','aporo/ENV*' ],
                     'excl_file'    :   abspath(this_dir+'/../rsync/rsync_excl.txt'),
                     'log_txt'      :   abspath(this_dir+'/../rsync/rsync_s3_to_s1_and_s2.log'),
                     'src_dir'      :   '/Users/admin',}
    os_cmd('rm %(file_list_txt)s %(excl_file)s'%T)
    with open('%(file_list_txt)s'%T, 'a') as f:     f.write('\n'.join(T['sync_items']))
    with open('%(excl_file)s'%T, 'a') as f:         f.write('\n'.join(T['excl_pattern']))
    for share in ['Macbook','mbp1']:
        T.update({    'log_txt'     :   abspath(this_dir+'/../rsync/rsync_all_to_%s.log'%share),
                      'dest_dir'    :   '/Volumes/%s/Users/admin'%share })
        rsync_cmd   =   get_rsync_cmd(T)
        proc        =   sub_popen([rsync_cmd], stdout=sub_PIPE, shell=True)
        (t, err)    =   proc.communicate()
    return True
def rsync_s2_to_ext_hd():

    T           =   {'options'      :   rsync_options,
                     'sync_items'   :   [ '/SERVER1','.alias_s1','/SERVER2','.alias_s2',
                                          '/SERVER3','.alias_s3','/SERVER4','.alias_s4',
                                          '/aprinto','/aporo','/.pg_dump', '/BD_Scripts',
                                          '/GIS','/.ipython','/qgis2/shortcuts.xml',
                                          '/.ssh','/.ssl','/Reference', ],
                     'file_list_txt':   abspath(this_dir+'/../rsync/file_list.txt'),
                     'excl_pattern' :   [ '*.DS_Store*','*.sock','*.pid','pagc-code-361-branches-sew-refactor2',
                                          'aprinto/ENV*','aporo/ENV*' ],
                     'excl_file'    :   abspath(this_dir+'/../rsync/rsync_excl.txt'),
                     'log_txt'      :   abspath(this_dir+'/../rsync/rsync_s2_to_ext_hd.log'),
                     'src_dir'      :   '/Volumes/Macbook/Users/admin',
                     'dest_dir'     :   '/Volumes/Macbook/Volumes/EXT_HD'}
    os_cmd('rm %(file_list_txt)s'%T)
    with open('%(file_list_txt)s'%T, 'a') as f:     f.write('\n'.join(T['sync_items']))
    rsync_cmd   =   get_rsync_cmd(T)
    proc        =   sub_popen([rsync_cmd], stdout=sub_PIPE, shell=True)
    (t, err)    =   proc.communicate()
    return True


from sys import argv
if __name__ == '__main__':

    if  argv[1]=='all':
        pg_dump_s3_and_ec2_into_s3()
        rsync_s1_to_s3()
        rsync_ipy2_in_s2()
        rsync_s2_to_s3()
        rsync_s4_to_s3()
        rsync_s3_to_s1_and_s2()
        rsync_s2_to_ext_hd()

    elif argv[1]=='test':
        # pg_dump_s3_and_ec2_into_s3()
        # rsync_s1()
        # rsync_ipy2_in_s2()
        # rsync_s2()
        # rsync_s4()
        # rsync_s3_to_s1_and_s2()
        # rsync_s2_with_ext_hd()
        pass