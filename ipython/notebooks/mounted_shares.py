
#         FOLDER             SOURCE
L   =   {'BD_Scripts'   :   'mb:/Users/admin/SERVER2/BD_Scripts',
         'gDrive'       :   'mb:/Users/admin/gDrive',
         'GIS'          :   'mb:/Users/admin/Projects/GIS',
         '.ipython'     :   'mb:/Users/admin/.ipython',
         'Reference'    :   'mb:/Users/admin/Reference',
         'SERVER1'      :   'mbp1:/Users/admin/SERVER1',
         'SERVER2'      :   'mb:/Users/admin/SERVER2',
         'SERVER3'      :   'mbp2:/Users/admin/SERVER3',
         'SERVER4'      :   'ec2:/home/SERVER4',
         'mbp1'         :   'mbp1:/',
         'Macbook'      :   'mb:/',
         'mbp2'         :   'mbp2:/',
         'ec2'          :   'ec2:/home/ec2-user',}

R   =   {}
for k,v in R.iteritems():
    if v[0]=='m':   R.update({k:v.replace(':','_remote:')})
    else:           R.update({k:v})

share_list  = L.keys()
s1_always   = ['Macbook']
s2_always   = ['mbp2']
s3_always   = ['Macbook','mbp1']

def mnt_shares(folders=['all'],local=True):
    from subprocess import Popen as sub_popen
    from subprocess import PIPE as sub_PIPE
    from time import sleep as delay

    if local   == True:     T = L
    else:                   T = R

    if folders == ['all']:  folders = T.keys()
    for it in folders:

        cmd             =   'ps -A | grep ssh | grep -v grep | awk '+"'{print $5}'"
        p               =   sub_popen([cmd], stdout=sub_PIPE, shell=True)
        (t, err)        =   p.communicate()
        chk             =   t.split('\n')

        if chk.count(T[it])==0:
            cmd         =   ['mkdir -p /Volumes/'+it,
                             '; /opt/local/bin/sshfs '+T[it],
                             ' /Volumes/'+it+' -ovolname='+it+' &']
            proc        =   sub_popen([''.join(cmd)], stdout=sub_PIPE, shell=True)
            (t, err)    =   proc.communicate()
            delay(3)

    return True

from sys import argv
if __name__ == '__main__':
    if   argv[1]=='mnt_all':            mnt_shares()
    elif share_list.count(argv[1])>0:   mnt_shares([argv[1]])
    elif argv[1]=='mnt_s1_always':      mnt_shares(s1_always)
    elif argv[1]=='mnt_s2_always':      mnt_shares(s2_always)
    elif argv[1]=='mnt_s3_always':      mnt_shares(s3_always)
    elif argv[1]=='mnt_check':          mnt_shares([argv[2]])
    elif argv[1]=='test':               mnt_shares(['mbp1'])
