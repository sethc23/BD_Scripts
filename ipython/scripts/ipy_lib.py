def ib_k(a='get_ipython()'):
    from os import system as os_cmd
    from subprocess import Popen as sub_popen
    from subprocess import PIPE as sub_PIPE
    from os.path import isdir
    from os.path import abspath
    from sys import path as py_path
    py_path.append('/Users/admin/SERVER2/scripts')
    from mounted_shares import mnt_shares
    
    # 1. get info about kernel
    a=get_ipython()
    fpath = a.kernel.config['IPKernelApp']['connection_file']
    fpath_shared = fpath[fpath.find('.ipython'):]
    fpath_in_mnt = '/Volumes/mb/Users/admin/'+fpath_shared
    proc = sub_popen(["cat "+fpath], stdout=sub_PIPE, shell=True)
    (t, err) = proc.communicate()
    k_info = eval(t)

    # 2. confirm access from REMOTE
    if not isdir('/Volumes/mbp2/Users'):      
        parts = ['/Users/admin/SERVER2/BD_Scripts/ipython/ENV/bin/python',
                          '/Users/admin/.scripts/mounted_shares.py']
        proc = sub_popen([' '.join(parts)], stdout=sub_PIPE, shell=True)
        (t, err) = proc.communicate()
        mnt_shares(['mbp2'])


    if not isdir('/Volumes/mbp2/Volumes/mb'):
        cmd  = "ssh mbp2 'python /Users/admin/.scripts/mounted_shares.py'"
        proc = sub_popen([cmd], stdout=sub_PIPE, shell=True)
        (t, err) = proc.communicate()

    # 3. create script on REMOTE for execution

    # ---- add cmds for opening proper ports
    cmds = []
    for k,v in k_info.iteritems():
        if k.find('_port')!=-1:
            cmds.append('ssh mb -X -f -N -L '+str(v)+':localhost:'+str(v)+';')

    # ---- add cmd for opening proper connection
    cmds.append("/Users/admin/SERVER3/ipython/ENV/bin/ipython qtconsole --profile=nbserver --existing %s"%fpath_in_mnt+";")
    
    # ---- add cmds for closing connection
    for k,v in k_info.iteritems():
        if k.find('_port')!=-1:
            cmds.append("kill `ps -A | grep "+str(v)+":localhost:"+str(v)+" | grep -v grep | awk '{print $1}'`"+'; ')

    # ---- push cmds to REMOTE
    f = open('/Volumes/mbp2/Users/admin/.scripts/k.sh','w')
    for it in cmds: f.write(it+'\n')
    f.close()

    # 4. send ssh cmd for REMOTE execution of script
    cmd = "ssh mbp2 '~/.scripts/k.sh' &"
    os_cmd(cmd)

    return