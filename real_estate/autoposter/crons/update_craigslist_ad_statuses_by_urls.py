#!/home/ub2/.scripts/ENV/bin/python

from os                                     import environ          as os_environ
from sys                                    import path             as py_path
py_path.append(                                 os_environ['HOME'] + '/BD_Scripts/html')
from preview_autopost 				        import Auto_Poster
x 									        = 	Auto_Poster()

from os                                     import getpid           as os_getpid
from inspect                                import stack            as i_stack
_this_file                                  =   i_stack()[0][1]

co_processes                                =   x.T.exec_cmds([' '.join(["ps -eo pid,args",
                                                                         "| grep 'python %s'" % _this_file,
                                                                         "| grep -v '%s'" % os_getpid(),
                                                                         "| grep -v grep"])])[0].split('\n')
if not co_processes or not co_processes[0]:
    x.PP.update_ads_from_urls(				    'craigslist')
