#!/usr/bin/env python
"""
    This example shows how to build a proxy based on mitmproxy's Flow
    primitives.

    Heads Up: In the majority of cases, you want to use inline scripts.

    Note that request and response messages are not automatically replied to,
    so we need to implement handlers to do this.
"""
import os
from libmproxy import flow, proxy
from libmproxy.proxy.server import ProxyServer


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
