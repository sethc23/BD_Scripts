#! env python
# PYTHON_ARGCOMPLETE_OK

import os,sys,time,StringIO,json
import socket,getopt,threading

from subprocess                             import Popen            as sub_popen
from subprocess                             import PIPE             as sub_PIPE
from ipdb                                   import set_trace        as i_trace
from types                                  import NoneType

# define some global variables
listen                                      =   False
target                                      =   ""
port                                        =   11111
stdin                                       =   False
verbose                                     =   True

def usage():
    print "BHP Net Tool"
    print
    print "Usage: %s -t target_host -p port" % __file__
    print "-l --listen                      -   listen on [host]:[port] for"
    print "                                     incoming connections"
    print "                                           AND"
    print "                                     initialize a command shell"
    print "-n --no-stdin                    -   skip over logic configured"
    print "                                     to accept stdin pipe"
    print "-v --verbose                     -   print status updates"
    print
    print
    print "Examples: "
    print "     bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
    print "     bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "     bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "     echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
    sys.exit(                                   0)

def client_sender(buffer):
    client                                  =   socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # connect to our target host
        client.connect(                         (target,port))
        if len(buffer):                         client.send(buffer)
        while True:

            # now wait for data back and print
            recv_len                        =   1
            response                        =   ""
            while recv_len:

                data                        =   client.recv(4096)
                recv_len                    =   len(data)
                response                   +=   data
                if recv_len < 4096:             break

            print response + "\n"

            # wait for more input
            buffer                          =   raw_input("")
            buffer                         +=   "\n"

            # send it off
            client.send(                        buffer)
    except:
        if verbose:                             print "[*] Exception! Exiting."
        # tear down the connection
        client.close(                           )

def client_handler(client_socket):
    sent_data = False
    while True:
        # show a simple prompt
        if not sent_data:
            client_socket.send(                 "$.py: ")
            sent_data                       =   True

        # now we receive until we see a linefeed (enter key)
        cmd_buffer                          =   ""
        try:
            while "\n" not in cmd_buffer:
                cmd_buffer                 +=   client_socket.recv(1024)
        except Exception as e:
            print "ERROR:"
            print type(e)                       # the exception instance
            print e.args                        # arguments stored in .args
            print e                             # __str__ allows args to be printed directly

        # create file-like string to capture output
        exec_out                            =   StringIO.StringIO()
        exec_err                            =   StringIO.StringIO()

        # capture output and errors
        sys.stdout                          =   exec_out
        sys.stderr                          =   exec_err

        exec(                                   cmd_buffer.rstrip())

        # restore stdout and stderr
        sys.stdout                          =   sys.__stdout__
        sys.stderr                          =   sys.__stderr__

        # send back the output if any
        _out,_err                           =   exec_out.getvalue(),exec_err.getvalue()
        _out,_err                           =   _out.rstrip(' \n'),_err.rstrip(' \n')
        if _out:
            client_socket.send(                 'OUT: ' + _out)
            sent_data                       =   True
        if _err:
            client_socket.send(                 'ERR: ' + _err)
            sent_data                       =   True
        
        if not _out and not _err:
            sent_data                       =   False
        else:
            client_socket.send(                 '\n')
            

def server_loop():
    global target,verbose

    # if no target is defined, we listen on all interfaces
    if not len(target):         target      =   "0.0.0.0"
    server                                  =   socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(                                (target,port))
    except:
        i_trace()
    server.listen(                              5)
    if verbose:                                 print "[*] Listening on %s:%d"          %   (target,port)

    while True:
        client_socket, addr                 =   server.accept()
        if verbose:                             print "[*] Accepted connection from: %s:%d" % (addr[0],addr[1])

        # spin off a thread to handle our new client
        client_thread                       =   threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start(                    )

def main(*args,**kwargs):
    global listen,port
    global target,stdin
    global verbose

    if kwargs:
        for k,v in kwargs.iteritems():          locals().update({k:v})

    if args and args[0]:            opts    =   list(*args)
    else:

        params                              =   sys.argv[1:]

        if not len(params):                     usage()

        # read the commandline options
        try:
            opts, args                      =   getopt.getopt(params,"hlt:p:nv",
                                                              ["help","listen","target","port","no-stdin","verbose"])
        except getopt.GetoptError as err:
            print '\nPARSING ERROR\n\n'
            print str(err)
            i_trace()
            usage()

    for o,a in opts:
        if o in   ("-h","--help"):
            usage(                              )
        elif o in ("-l","--listen"):
            listen                          =   True
        elif o in ("-t", "--target"):
            target                          =   a
        elif o in ("-p", "--port"):
            port                            =   int(a)
        elif o in ("-n", "--no_stdin"):
            stdin                           =   False
        elif o in ("-v", "--verbose"):
            verbose                         =   True
        else:
            assert False,"Unhandled Option"

    if port and listen:
        # cmd                                 =   'fuser -k %s/tcp' % port
        cmd = """[[ -n "$(lsof -i tcp:%(port)s)" ]] && lsof -i tcp:%(port)s + kill -9""" % {'port':port}
        proc                                =   sub_popen(cmd, stdout=sub_PIPE, shell=True)
        (_out, _err)                        =   proc.communicate()
        assert not _out and type(_err)==NoneType, "_out: %s, _err: %s" % (_out,_err)

    # are we going to listen or just send data from stdin?
    if stdin or (
        not listen and
        len(target) and
        port > 0
        ):

        if verbose:                             print "running client_sender"

        # make initial connection
        client_sender(                          '')
        print 'moving from sender'

    # we are going to listen and drop a shell back
    if listen:                              server_loop()

if __name__ == '__main__':
    # in first terminal:  ./tcp-py-console.py -l -p 11111 -v
    # in second terminal: ./tcp-py-console.py -t 0.0.0.0 -p 11111 -n -v
    main()