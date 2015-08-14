#!/home/ub2/.scripts/ENV/bin/python

import os
from libmproxy                              import flow, proxy
from libmproxy.proxy.server                 import ProxyServer

from os                                     import environ          as os_environ
from sys                                    import path as py_path
py_path.append(                                 os_environ['HOME'] + '/.scripts/ENV/lib/python2.7/site-packages')
py_path.append(                                 os_environ['HOME'] + '/.scripts')
from ipdb                                   import set_trace as i_trace


class MyMaster(flow.FlowMaster):
    def run(self):
        try:
            flow.FlowMaster.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_request(self, f):
        f = flow.FlowMaster.handle_request(self, f)
        if f:
            f.reply()
        i_trace()
        return f

    def handle_response(self, f):
        f = flow.FlowMaster.handle_response(self, f)
        if f:
            f.reply()
        print(f)
        return f

config                                      =   proxy.ProxyConfig(
                                                    # host                            =   '',
                                                    port                            =   10052,
                                                    # server_version                  =   version.NAMEVERSION,
                                                    ### use ~/.mitmproxy/mitmproxy-ca.pem as default CA file.
                                                    cadir                           =   "~/.mitmproxy/",
                                                    # clientcerts                     =   None,
                                                    # no_upstream_cert                =   False,
                                                    # body_size_limit                 =   None,
                                                    ### Opts: transparent,socks5,reverse,upstream,spoof,sslspoof,'' {=regular}
                                                    mode                            =   "transparent",
                                                    # upstream_server                 =   None,
                                                    # http_form_in                    =   None,
                                                    # http_form_out                   =   None,
                                                    # authenticator                   =   None,
                                                    # ignore_hosts                    =   [],
                                                    # tcp_hosts                       =   [],
                                                    # ciphers_client                  =   None,
                                                    # ciphers_server                  =   None,
                                                    # certs                           =   [],
                                                    # ssl_version_client              =   tcp.SSL_DEFAULT_METHOD,
                                                    # ssl_version_server              =   tcp.SSL_DEFAULT_METHOD,
                                                    ### Default: TRANSPARENT_SSL_PORTS=   [443, 8443]
                                                    # ssl_ports                       =   TRANSPARENT_SSL_PORTS,
                                                    # spoofed_ssl_port                =   None,
                                                    # ssl_verify_upstream_cert        =   False,
                                                    # ssl_upstream_trusted_cadir      =   None,
                                                    # ssl_upstream_trusted_ca         =   None
                                                    )
state                                       =   flow.State()
server                                      =   ProxyServer(config)
m                                           =   MyMaster(server, state)
m.run(                                          )


