import os
from time import sleep
from sys import argv, path
path.append('/Users/admin/SERVER2/BD_Scripts/appscript')
from Word_API import activate, setWordWindow
from SystemEventsAPI import keys
# path.append('/Users/admin/SERVER2/BD_Scripts/files_folders')
# from API_system import getCapsLock

def getMousePos():
    p = os.popen('/usr/bin/cliclick -q')
    s = p.read()
    p.close()
    x, y = s.split(',')
    x = eval(x.strip())
    y = eval(y.strip())
    return x, y

def getCapsLock():
    p = os.popen('xset q | grep LED')
    s = p.read()
    p.close()
    x = s[65]
    if x == '0': return 'off'
    if x == '1': return 'on'

def movePage(seconds, w):
    delay = seconds / 60
    pause = False
    for i in range(0, 40):  # length of page
        x = getCapsLock()
        if x == 'on': pause = False
        if x == 'off': pause = True
        while pause == True:
            sleep(.5)
            x = getCapsLock()
            if x == 'on': pause = False
            if x == 'off': pause = True
        sleep(delay - .1)
        keys('keycode', 125)
        
        """
        x,y=getMousePos()
        #print w[2],'>=',x,'>=',w[0]
        #print w[3],'>=',y,'>=',w[1]
        if (w[2]>=x>=w[0]) and (w[3]>=y>=w[1]): pause=True
        else: pause= False
        
        while pause == True:
            sleep(.5)
            x,y=getMousePos()
            if (w[2]>=x>=w[0]) and (w[3]>=y>=w[1]): pause=True
            else: pause= False
        sleep(delay-.1)
        keys('keycode',125)
        """

if __name__ == '__main__':
    try:
        pages = eval(str(argv[1]))
        minutes = eval(str(argv[2]))
    except:
        pass
    
    w = [221, 22, 1080, 376]
    setWordWindow(w)

    activate()
    seconds = (minutes / pages) * 60
    for i in range(0, pages):

        movePage(seconds, w)




    
    
    
    
    
    
