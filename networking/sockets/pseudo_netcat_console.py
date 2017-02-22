#!/home/ub2/.virtualenvs/fileserver/bin/python 
# PYTHON_ARGCOMPLETE_OK

from os                                     import environ          as os_environ
from sys                                    import path             as py_path
py_path.append(                                 os_environ['HOME'] + '/.scripts/ENV/lib/python2.7/site-packages')
import time
py_path.append(                                 os_environ['HOME'] + '/.scripts')
from sysparse                        import *
from system_settings                        import *

from ipdb                                   import set_trace        as i_trace

from subprocess                             import Popen            as sub_popen
from subprocess                             import PIPE             as sub_PIPE

import sys,socket,getopt,threading,subprocess
from multiprocessing import Process


# define some global variables
listen                                      =   False
command                                     =   False
upload                                      =   False
execute                                     =   ""
target                                      =   ""
upload_destination                          =   ""
port                                        =   11111
stdin                                       =   False
verbose                                     =   True
server                                      =   ''
server_thread                               =   ''

def usage():
    print "BHP Net Tool"
    print
    print "Usage: bhpnet.py -t target_host -p port"
    print "-l --listen                      -   listen on [host]:[port] for"
    print "                                     incoming connections"
    print "-e --execute=file_to_run         -   execute the given file upon"
    print "                                     receiving a connection"
    print "-c --command                     -   initialize a command shell"
    print "-u --upload=destination          -   upon receiving connection,"
    print "                                     upload a file and write to [dest]"
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

def client_sender(buffer=''):
    global server_thread,server
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

            print response

            try:
                # wait for more input
                buffer                          =   raw_input("")
                buffer                         +=   "\n"
            except KeyboardInterrupt:
                break

            # send it off
            client.send(                        buffer)

        if verbose:                             print "Exiting."
        client.close(                           )
        server_thread.terminate()
        

    except Exception as e:
        print "ERROR:"
        print type(e)     # the exception instance
        print e.args      # arguments stored in .args
        print e           # __str__ allows args to be printed directly

        if verbose:                             print "[*] Exception! Exiting."
        # tear down the connection
        client.close(                           )
        server_thread.terminate()

def run_command(command):
    # trim the newline
    command                                 =   command.rstrip()

    # run the command and get the output back
    try:
        proc                                =   sub_popen(  command, 
                                                            stdout=sub_PIPE, 
                                                            shell=False
                                                            #,executable='/bin/zsh'
                                                            )
        (_out, _err)                        =   proc.communicate()
        assert _err==None
    except:
        _out                                =   "Failed to execute command.\r\n"

    # send the output back to the client
    return _out

def client_handler(client_socket):
    global upload,execute,command

    # check for upload
    if len(upload_destination):

        # read in all of the bytes and write to our destination
        file_buffer                         =   ""

        # keep reading data until none is available
        while True:
            data                            =   client_socket.recv(1024)
            if not data:                        break
            else:           file_buffer    +=   data

        # now we take these bytes and try to write them out
        try:
            file_descriptor                 =   open(upload_destination,"wb")
            file_descriptor.write(              file_buffer)
            file_descriptor.close(              )

            # acknowledge that we wrote the file out
            client_socket.send(                 "Successfully saved file to %s\r\n"
                                                % upload_destination)

        except:
            client_socket.send(                 "Failed to save file to %s\r\n"
                                                % upload_destination)

    # check for command execution
    if len(execute):

        # run the command
        output                              =   run_command(execute)
        client_socket.send(                     output)

    # now we go into another loop if a command shell was requested
    if command:

        while True:
            # show a simple prompt
            client_socket.send(                 "<GO:#> ")

            # now we receive until we see a linefeed (enter key)
            cmd_buffer                      =   ""
            try:
                while "\n" not in cmd_buffer:
                    cmd_buffer             +=   client_socket.recv(1024)
            except Exception as e:
                print "ERROR:"
                print type(e)     # the exception instance
                print e.args      # arguments stored in .args
                print e           # __str__ allows args to be printed directly

            # send back the command output
            response                        =   run_command(cmd_buffer)

            # send back the response
            client_socket.send(                 response)

def server_loop():
    global target,verbose,status,server

    # if no target is defined, we listen on all interfaces
    if not len(target):         target  =   "0.0.0.0"

    server                              =   socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(                      socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    status                              =   'server started'
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
    # print args,list(*args)
    # print kwargs
    # print sys.argv[1:]
    # raise SystemError
    global listen,port,execute,command
    global upload_destination,target,stdin
    global verbose

    if kwargs:
        for k,v in kwargs.iteritems():          locals().update({k:v})
    


    if args and args[0]:            
        pass
    else:
        params                              =   sys.argv[1:]
        if not len(params):                     usage()

    # read the commandline options
    try:
        opts, args                      =   getopt.getopt(args,"hlnve:t:p:cu:",["help","listen","no-stdin","verbose","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print '\nPARSING ERROR\n\n'
        print str(err)
        i_trace()
        usage()

    for o,a in opts:
        if o in ("-h","--help"):
            usage(                              )
        elif o in ("-l","--listen"):
            listen                          =   True
        elif o in ("-e", "--execute"):
            execute                         =   a
        elif o in ("-c", "--shell"):
            command                         =   True
        elif o in ("-u", "--upload"):
            upload_destination              =   a
        elif o in ("-t", "--target"):
            target                          =   a
        elif o in ("-p", "--port"):
            port                            =   int(a)
        elif o in ("-n", "--no_stdin"):
            stdin                           =   False
        elif o in ("-v", "--verbose"):
            verbose                         =   True
        else:
            assert False,"Unhandled Option: '%s' '%s'" % (o,a)

    if port and listen:
        cmd                                 =   'fuser -k %s/tcp' % port
        proc                                =   sub_popen(cmd, stdout=sub_PIPE, shell=True)
        (_out, _err)                        =   proc.communicate()
        assert not _out and _err is None


    # are we going to listen or just send data from stdin?
    if (#stdin and
        not listen and
        len(target) and
        port > 0):

        if verbose:                             print "running client_sender"

        # make initial connection
        client_sender(                          '')
        print 'moving from sender'

    # we are going to listen and potentially
    # upload things, execute commands, and drop a shell back
    # depending on our command line options above
    if listen:                              server_loop()

def console():
    global status,server_thread
    status = 'starting server'
    cmd = '/home/ub2/SERVER2/file_server/console/pseudo_netcat.py -l -p 11111 -c -v'
    # server_thread = threading.Thread(target=main,args=cmd.split()[1:] + [status])
    # server_thread = KThread(target=main,args=cmd.split()[1:] + [status])
    server_thread = Process(target=main,args=cmd.split()[1:] + [status])
    server_thread.start()
    max_wait = 15
    while status=='starting server':
        time.sleep(1)
        max_wait-=1
        if max_wait==0:
            print 'waited max_time for server to start'
            break
    client_sender()



if __name__ == '__main__':
    # in first terminal:  ./pseudo_netcat.py -l -p 11111 -c -v
    # in second terminal: ./pseudo_netcat.py -t 0.0.0.0 -p 11111 -n -v
    main()