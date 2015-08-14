
from subprocess                             import Popen            as sub_popen
from subprocess                             import PIPE             as sub_PIPE

cmd                         =   "socat -d -d pty,raw,echo=1 pty,raw,echo=1"
proc                        =   sub_popen(cmd, stdout=sub_PIPE, shell=True)
(_out, _err)                =   proc.poll() ## ??? proc.communicate()
assert _err==None
# Example _out:
#   2015/07/31 09:47:29 socat[5961] N PTY is /dev/pts/6
#   2015/07/31 09:47:29 socat[5961] N PTY is /dev/pts/7
#   2015/07/31 09:47:29 socat[5961] N starting data transfer loop with FDs [3,3] and [5,5]


# TERMINAL #1
from serial                                 import Serial
r                                           =   S.Serial('/dev/pts/6')
r.readline()
# ... wait for #2 to write()


# TERMINAL #2
from serial                                 import Serial
w                                           =   S.Serial('/dev/pts/7')
w.write("testing this")