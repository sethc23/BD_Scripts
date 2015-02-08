# Libraries
import sys
import codecs
reload(sys)
sys.setdefaultencoding('UTF8')
from uuid import getnode as get_mac
from os import system as os_cmd
from os.path import abspath
from subprocess import Popen as sub_popen
from subprocess import PIPE as sub_PIPE
from time import sleep as delay
from datetime import datetime as dt

import pandas as pd
pd.set_option('expand_frame_repr',False)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width',180)
np = pd.np
np.set_printoptions(linewidth=200,threshold=np.nan)
from sqlalchemy import create_engine
engine = create_engine(r'postgresql://postgres:postgres@192.168.3.52:8800/routing',
                       encoding='utf-8',
                       echo=False)
import psycopg2
conn = psycopg2.connect("dbname='routing' user='postgres' host='192.168.3.52' password='' port=8800");
cur = conn.cursor()

class PasteBin:
    """
    Module:             http://pythonhosted.org/pastebin_python/code.html

    Expiration Format:  (see http://pastebin.com/api#6)
        Input     Description
        'N'       Never
        '10M'     10 minutes
        '1H'      1 hour
        '1D'      1 day
        '1W'      1 week
        '2W'      2 weeks
        '1M'      1 month

    Publication Format:  public = 0, unlisted = 1, private = 2
    """
    def __init__(self):
        from pastebin_python import PastebinPython
        user_name       =   'mech_coder'
        passw           =   'Delivery100%'
        dev_key         =   '4f26d1cb7a08f03b02ab24dae43bc431'
        pb              =   PastebinPython(api_dev_key=dev_key)
        pb.createAPIUserKey(user_name,passw)
        self.pastebin   =   pb

class System_Databases:

    def __init__(self):
        self.databases  =   pd.read_sql('select * from databases where active is True',engine)

class System_Servers:


    def __init__(self):
        L   =   {'BD_Scripts'   :   'mb:/Users/admin/SERVER2/BD_Scripts',
         'gDrive'       :   'mb:/Users/admin/gDrive',
         'GIS'          :   'mb:/Users/admin/GIS',
         '.ipython'     :   'mb:/Users/admin/.ipython',
         'Reference'    :   'mb:/Users/admin/Reference',
         'SERVER1'      :   'mbp1:/Users/admin/SERVER1',
         'SERVER2'      :   'mb:/Users/admin/SERVER2',
         'SERVER3'      :   'mbp2:/Users/admin/SERVER3',
         'SERVER4'      :   'ec2:/home/SERVER4',
         'mbp1'         :   'mbp1:/',
         'mb'           :   'mb:/',
         'mbp2'         :   'mbp2:/',
         'ec2'          :   'ec2:/',
         'ms1'          :   'ms1:/',
         'ubuntu'       :   'S5:/',}

        R   =   {}
        for k,v in R.iteritems():
            if v[0]=='m':   R.update({k:v.replace(':','_remote:')})
            else:           R.update({k:v})
        self.L          =   L
        self.R          =   R
        s               =   pd.read_sql('select * from servers where production_usage is not null',engine)
        self.servers    =   s
        server_dir_dict =   dict(zip(s.tag.tolist(),s.home_dir.tolist()))
        mac             =   [int(str(get_mac()))]
        worker          =   s[s.mac.isin(mac)].iloc[0].to_dict()
        self.worker     =   worker['server']
        self.base_dir   =   worker['home_dir']
        self.server_idx =   worker['server_idx']
        rank            =   {'high':3,'medium':2,'low':1,'none':0}
        s['ranking']    =   s.production_usage.map(rank)
        self.priority   =   dict(zip(s.tag.tolist(),s.ranking.tolist()))
        local           =   True
        if local   == True:
            self.T      =   self.L


    def mnt_shares(self,folders=[''],local=True):

        if local   == False:
            self.T      =   self.R

        if   folders    ==  ['all']:            folders = T.keys()
        elif folders    ==  ['']:               folders = [self.worker]

        if   folders==['ubuntu']:               folders = ['mb','mbp2']
        elif folders==['mb']:                   folders = ['mbp2','ubuntu']
        elif folders==['mbp2']:                 folders = ['mb','ubuntu']

        folders             =   [it for it in folders if it!=self.worker]
        for it in folders:

            cmd             =   'ps -A | grep ssh | grep -v grep | awk '+"'{print $5}'"
            p               =   sub_popen([cmd], stdout=sub_PIPE, shell=True)
            (t, err)        =   p.communicate()
            chk             =   t.split('\n')

            if chk.count(self.T[it])==0:
                cmd         =   ['mkdir -p /Volumes/'+it,
                                 '; /opt/local/bin/sshfs '+self.T[it],
                                 ' /Volumes/'+it+' -ovolname='+it+' &']
                try:
                    proc        =   sub_popen([''.join(cmd)], stdout=sub_PIPE, shell=True)
                    (t, err)    =   proc.communicate()
                    delay(3)
                except:
                    cmd         =   ['rmdir /Volumes/%s'%(it,it)]
                    proc        =   sub_popen(cmd, stdout=sub_PIPE, shell=True)
                    (t, err)    =   proc.communicate()

        return True
    def umnt_shares(self,folders=['all'],local=True):

        if folders  == ['all']:                 folders = self.T.keys()
        elif folders==['mnt_s1_always']:        folders = ['mb','mbp2']
        elif folders==['mnt_s2_always']:        folders = ['mbp2','ubuntu']
        elif folders==['mnt_s3_always']:        folders = ['mb','ubuntu']

        folders             =   [it for it in folders if it!=self.worker]
        for it in folders:

            cmd             =   'ps -A | grep ssh | grep -v grep | awk '+"'{print $5}'"
            p               =   sub_popen([cmd], stdout=sub_PIPE, shell=True)
            (t, err)        =   p.communicate()
            chk             =   t.split('\n')

            if chk.count(self.T[it])!=0:
                cmd         =   ['umount /Volumes/%s && rmdir /Volumes/%s'%(it,it)]
                proc        =   sub_popen(cmd, stdout=sub_PIPE, shell=True)
                (t, err)    =   proc.communicate()
                delay(3)

        return True

class System_Admin:

    def __init__(self):
        s                   =   System_Servers()
        self.servers        =   s.servers
        self.worker         =   s.worker
        self.base_dir       =   s.base_dir
        self.priority       =   s.priority
        self.ready          =   s.mnt_shares(['mb','mbp1','ec2'])
        self.cfg            =   self.get_cfg()
        self.params         =   {}
        # self.dry_run        =   True
        self.dry_run        =   False
        pb                  =   PasteBin()
        self.pastebin       =   pb.pastebin

    def get_cfg(self):
        base            = self.base_dir if self.worker=='mb' else '/Volumes/mb'+self.base_dir
        cfg_fpath       = base + '/SERVER2/BD_Scripts/files_folders/rsync/backup_system_config.xlsx'
        cfg             = pd.read_excel(cfg_fpath, na_values ='', keep_default_na=False, convert_float=False)
        cols            = cfg.columns.tolist()
        cols_lower      = [str(it).lower() for it in cols]
        cfg.columns     = [cols_lower]
        for it in cols_lower:
            cfg[it]     = cfg[it].map(lambda s: '' if str(s).lower()=='nan' else s)
        tbl             = 'config_rsync'
        conn.set_isolation_level(0)
        cur.execute('drop table if exists %s'%tbl)
        cfg.to_sql(tbl,engine,index=False)
        return cfg

    def add_options(self):
        options         = [ 'verbose','verbose','recursive','archive','update','one-file-system',
                            'compress','prune-empty-dirs','itemize-changes']
                            #,"filter='dir-merge /.rsync-filter'"]
			    # ,'delete-before'
        if self.dry_run==True:      options.append('dry-run')
        self.params.update( { 'options'     :   map(lambda s: '--%s'%s,options) })

    def add_exclusions(self):
        exclude         = self.cfg.exclude.map(lambda s: '--exclude='+str(s)).tolist()
        if len(exclude)!=0:
            self.params.update( { 'exclusions':   exclude, })

    def add_inclusions(self):
        include         = self.cfg.include.map(lambda s: '--include='+str(s)).tolist()
        if len(include)!=0:
            self.params.update( { 'inclusions':   include, })

    def add_logging(self):
        self.params.update( { 'logging'     :   ['--outbuf=L'], })

    def backup_ipython(self,params=''):
        self.process    = 'backup_ipython'
        self.process_start = dt.isoformat(dt.now())
        self.add_options()
        self.add_exclusions()
        from_dir        = '/Users/admin/SERVER2/BD_Scripts/ipython'
        to_dir          = '/Users/admin/SERVER2'
        src             = from_dir if self.worker=='mb' else '/Volumes/mb'+from_dir
        dest            = to_dir   if self.worker=='mb' else '/Volumes/mb'+to_dir
        self.params.update( {'src_dir'      :   src,
                             'dest_dir'     :   dest,
                             'operation'    :   '%s: %s'%(self.worker,self.process)})
        self.run_rsync()
        self.process_end = dt.isoformat(dt.now())
        return self.to_pastebin()

    def backup_databases(self,params=''):
        self.process        =   'backup_databases'
        self.process_start  = dt.isoformat(dt.now())
        T                   =   {'operation'    :   '%s: %s'%(self.worker,self.process)}
        d                   =   System_Databases()
        self.databases      =   d.databases
        self.database_names =   self.databases.db_name.tolist()
        for i in range(len(self.databases)):
            db_info         =   self.databases.ix[i,['backup_path','db_server','db_name','backup_cmd']].map(str)
            fpath           =   '%s/%s_%s_%s.sql'%tuple(db_info[:-1].tolist() + [dt.strftime(dt.now(),'%Y_%m_%d')])
            fname           =   fpath[fpath.rfind('/')+1:]
            cmd             =   """%s -d %s -h 0.0.0.0 -p 8800 --username=postgres > %s
                                """.replace('\n','').replace('\t','').strip()%(db_info['backup_cmd'],db_info['db_name'],fpath)
            if db_info['db_server']!=self.worker:
                cmd         =   "ssh %s '"%db_info['db_server'] + cmd + "'"
            T.update(           {'started'      :   dt.isoformat(dt.now()),
                                 'parameters'   :   cmd.replace("'","''"),} )
            proc            =   sub_popen([cmd], stdout=sub_PIPE, shell=True)
            (t, err)        =   proc.communicate()
            T.update(           {'stout'        :   t,
                                 'sterr'        :   err,
                                 'ended'        :   dt.isoformat(dt.now())} )
            c               =   """insert into system_log values ('%(operation)s','%(started)s',
                                                          '%(parameters)s','%(stout)s',
                                                          '%(sterr)s','%(ended)s')"""%T
            conn.set_isolation_level(0)
            cur.execute(c)

        self.process_end = dt.isoformat(dt.now())
        return self.to_pastebin(params='\n'.join(self.database_names))

    def backup_system(self,params=''):
        self.process    =   'backup_system'
        self.process_start = dt.isoformat(dt.now())
        self.add_options()
        self.add_exclusions()           # DON'T ADD INCLUSIONS -- see sync_items below
        cfg             =   self.cfg
        cols            =   cfg.columns.map(str).tolist()
        t_cols          =   [it for it in cols if it[0].isdigit()]

        grps,pt         =   [],0
        for i in range(len(t_cols)/2):
            x           =   cfg[[t_cols[pt],t_cols[pt+1],'include']].apply(lambda s: [str(s[0])+'-'+str(s[1]),str(s[2])],axis=1).tolist()
            grps.extend(x)
            pt+=2
        res             =   [it for it in grps if (str(it).find("['-',")==-1 and str(it).find("'']")==-1) ]
        d               =   pd.DataFrame({ 'server_pair':map(lambda s: s[0],res),
                                         'transfer_files':map(lambda s: s[1],res)})
        _iters          =   d.server_pair.unique().tolist()
        for pair in _iters:
            sync_items  =   d[d.server_pair==pair].transfer_files
            incl        =   sync_items.map(lambda s: ' --include='+s).tolist()
            a,b         =   pair.split('-')
            a_serv,b_serv = map(lambda s: str(self.servers[self.servers.tag==s].server.iloc[0]),pair.split('-'))
            a_dir,b_dir =   map(lambda s: str(self.servers[self.servers.tag==s].home_dir.iloc[0]),pair.split('-'))
            # _host     =    b if priority[a]>priority[b] else a
            src         =   a_dir if a_serv==self.worker else '/Volumes/'+a_serv+a_dir
            dest        =   b_dir if b_serv==self.worker else '/Volumes/'+b_serv+b_dir
            for it in sync_items:
                self.params.update( {'src_dir'      :   src+'/'+it.lstrip('/'),
                                     'dest_dir'     :   dest+'/',
                                     'operation'    :   '%s: %s -- %s -- %s'%(self.worker,self.process,pair,it)})
                self.run_rsync()
        self.process_end = dt.isoformat(dt.now())
        return self.to_pastebin()

    def to_pastebin(self,params=''):
        if self.dry_run==True:      return True
        else:

            condition       =   """
                                    operation ilike '%s: %s%s'
                                    and started >=  '%s'::timestamp with time zone
                                    and ended   <  '%s'::timestamp with time zone
                                """%(self.worker,self.process,'%%',self.process_start,self.process_end)
            df              =   pd.read_sql("select * from system_log where %s"%(condition),engine)
            T               =   df.iloc[0].to_dict()
            T['operation']  =   '%s: %s'%(self.worker,self.process)
            pb_url          =   self.pastebin.createPaste(df.to_html(), api_paste_name = T['operation'],
                                                      api_paste_format = 'html5', api_paste_private = '1',
                                                      api_paste_expire_date = '2W')
            T['stout']      =   pb_url
            T['ended']      =   dt.isoformat(dt.now())
            T['parameters'] =   '\n\n'.join(df.parameters.tolist()).replace("'","''")
            c               =   """insert into system_log values ('%(operation)s','%(started)s',
                                                              '%(parameters)s','%(stout)s',
                                                              '%(sterr)s','%(ended)s')"""%T
            conn.set_isolation_level(0)
            cur.execute(c)

            conn.set_isolation_level(0)
            cur.execute("delete from system_log where %s "%(condition))
            return True

    def run_rsync(self):
        c,keys    =   ['rsync'],self.params.keys()
        if keys.count('options'):               c.extend(self.params['options'])
        if keys.count('inclusions'):            c.extend(self.params['inclusions'])
        if keys.count('exclusions'):            c.extend(self.params['exclusions'])
        if keys.count('logging'):               c.extend(self.params['logging'])

        c.extend([      self.params['src_dir'], self.params['dest_dir'] ])
        cmd         =   ' '.join(c)
        start_ts    =   dt.isoformat(dt.now())
        proc        =   sub_popen([cmd], stdout=sub_PIPE, shell=True)
        (t, err)    =   proc.communicate()
        c           =   "insert into system_log values ('%s','%s','%s','%s','%s','%s')"%(
                            self.params['operation'],start_ts,
                            '%s %s'%(self.params['src_dir'],self.params['dest_dir']),
                            unicode(t).replace("'","''"), unicode(err).replace("'","''"), dt.isoformat(dt.now()))
        conn.set_isolation_level(0)
        cur.execute(c)
        return True

from sys import argv
if __name__ == '__main__':
    if len(argv)>1:

        SYS = System_Admin()
        if (len(argv)>2 and argv[2]=='dry-run'):
            SYS.dry_run = True

        if  argv[1]=='backup_all':
            SYS.backup_ipython()
            SYS.backup_databases()
            SYS.backup_system()

        elif  argv[1]=='backup_ipython':     SYS.backup_ipython()
        elif  argv[1]=='backup_databases':   SYS.backup_databases()
        elif  argv[1]=='backup_system':      SYS.backup_system()           
            
        elif argv[1]=='test':
            # SYS.backup_system()
            pass