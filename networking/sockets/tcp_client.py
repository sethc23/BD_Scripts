#! ENV/bin/python
# PYTHON_ARGCOMPLETE_OK

from ipdb import set_trace as i_trace

import socket as S
t_host                                      =   'www.google.com'
t_port                                      =   80
c                                           =   S.socket(S.AF_INET,S.SOCK_STREAM)
c.connect(                                      ('10.0.1.52',11111))
c.send(                                         "GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
r                                           =   c.recv(4896)
print r