#!/home/ub2/.scripts/ENV/bin/python
####!ENV/bin/python
# PYTHON_ARGCOMPLETE_OK
from os                                     import environ          as os_environ
from sys                                    import path as py_path
py_path.append(                                 os_environ['HOME'] + '/.scripts/ENV/lib/python2.7/site-packages')
import time
py_path.append(                                 os_environ['HOME'] + '/.scripts')

from ipdb                                   import set_trace as i_trace

from subprocess                             import Popen            as sub_popen
from subprocess                             import PIPE             as sub_PIPE

from libmproxy.protocol.http                import HTTPRequest,HTTPHandler
from libmproxy.protocol.tcp                 import TCPHandler
from libmproxy.proxy.server                 import ConnectionHandler
from libmproxy.protocol.http                import send_connect_request
from libmproxy                              import flow, proxy

py_path.append(                                 '../sockets')
from pseudo_netcat                          import main             as sockets_main

first                                       =   True

def logger(log_msg):
    cmd                         =   'echo "%s" >> /var/sockets/tmp' % log_msg
    proc                        =   sub_popen(cmd, stdout=sub_PIPE, shell=True)
    (_out, _err)                =   proc.communicate()
    assert _out==''
    assert _err==None


def start(context, argv):
    logger(                                     'start')
    HTTPRequest._headers_to_strip_off.remove(   "Connection")
    HTTPRequest._headers_to_strip_off.remove(   "Upgrade")
    stop_this                               =   False
    # i_trace()
    if stop_this:
        raise SystemExit

def clientconnect(context, cxt_handler):
    logger(                                     'clientconnect')
    stop_this                               =   False
    # i_trace()
    if stop_this:
        raise SystemExit


def serverconnect(context, cxt_handler):
    logger(                                     'serverconnect')
    stop_this                               =   False
    # i_trace()
    if stop_this:
        raise SystemExit

def request(context, flow):

    # global first
    logger(                                     'request')
    stop_this                               =   False
    # print("handle request: %s%s"            %   (flow.request.host, flow.request.path))
    # if first:                       first   =   False
    # else:                                       time.sleep(10000)

    # f                                       =   flow.FlowMaster.handle_request(f)
    # if f:                                       f.reply()


    # print("start  request: %s%s"            %   (flow.request.host, flow.request.path))


    # flow.client_conn.send(flow.response.assemble())
    # x=HTTPHandler(flow.live.c)
    # x.handle_messages()
    # send_connect_request(
    #             flow.live.c.server_conn,
    #             flow.request.host,
    #             flow.request.port)


    # THIS SUCCESSFULLY & QUIETLY PUSH CONNECTION INFO TO FILE
    #       BUT, can't connect for some reason...
    # from os import environ as os_environ
    # print os_environ['VIRTUAL_ENV']
    # I.start_kernel(                             argv=["console","--profile=nbserver"])

    # sockets_main(                               [('--listen',True),
    #                                              ('--port',11111),
    #                                              ('-c',True),])
    #
    # i_trace()



    # flow.client_conn.send(flow.response.assemble())
    # ...and then delegate to tcp passthrough.
    # TCPHandler(flow.live.c, log=False).handle_messages()
    # flow.reply()


    # time.sleep(1000)
    #print("start  request: %s%s" % (flow.request.host, flow.request.path))
    if stop_this:
        raise SystemExit
    # return f

def responseheaders(context, flow):
    logger(                                     'responseheaders')
    stop_this                               =   False
    # i_trace()
    if stop_this:
        raise SystemExit

def response(context, flow):
    logger(                                     'response')

    # flow.response.headers["newheader"] = ["foo"]
    # f                                       =   flow.FlowMaster.handle_response(f)
    # if f:                                       f.reply()
    pass

def error(context, flow):
    logger(                                     'error')


def done(context):
    logger(                                     'done')
