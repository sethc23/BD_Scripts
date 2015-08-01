#! ENV/bin/python
# PYTHON_ARGCOMPLETE_OK

import socket
import threading

bind_ip                                     =   "10.0.1.52"
bind_port                                   =   11111

server                                      =   socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(                                    (bind_ip,bind_port))
server.connect(                                    (bind_ip,bind_port))
server.listen(                                  5)
print "[*] Listening on %s:%d" % (bind_ip,bind_port)

# this is our client-handling thread
def handle_client(client_socket):
    # print out what the client sends
    request                                 =   client_socket.recv(4096)
    print "[*] Received: %s"                %   request
    # send back a packet
    client_socket.send(                          "ACK!")
    client_socket.close(                        )

while True:
    client,addr                             =   server.accept()
    print "[*] Accepted connection from: %s:%d" % (addr[0],addr[1])
    # spin up our client thread to handle incoming data
    client_handler                          =   threading.Thread(target=handle_client,args=(client,))
    client_handler.start(                       )