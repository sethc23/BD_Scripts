

def internet_on():
    import urllib2
    import socket
    socket.setdefaulttimeout(1)
    try:
        response = urllib2.urlopen('http://google.com')
       #x= response
        #print x
        #print 'asda'
        socket.setdefaulttimeout(10)
        return True
    except urllib2.URLError: pass
    return False
