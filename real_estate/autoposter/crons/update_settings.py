#!/home/ub2/.scripts/ENV/bin/python

from os                             import environ          as os_environ
from sys                            import path             as py_path
py_path.append(                         os_environ['HOME'] + '/BD_Scripts/html')
from preview_autopost 				import Auto_Poster
x 								= 	Auto_Poster('phantom')
x.PP.update_post_settings(			)
x.PP.close_browser(					)
