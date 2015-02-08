import os
from time import sleep
from sys import argv, path
path.append('/Users/admin/SERVER2/BD_Scripts/appscript')
from skimAPI import activate, setSkimWindow
from SystemEventsAPI import keys
path.append('/Users/admin/SERVER2/BD_Scripts/files_folders')
# from API_system import getMouseSpot

def getMousePos():
    p = os.popen('/usr/bin/cliclick -q')
    s = p.read()
    p.close()
    x, y = s.split(',')
    x = eval(x.strip())
    y = eval(y.strip())
    return x, y


def movePage(seconds, w):
    delay = seconds / 60
    pause = False
    for i in range(0, 60):
        x, y = getMousePos()
        # print w[2],'>=',x,'>=',w[0]
        # print w[3],'>=',y,'>=',w[1]
        if (w[2] >= x >= w[0]) and (w[3] >= y >= w[1]): pause = True
        else: pause = False
        
        while pause == True:
            sleep(.5)
            x, y = getMousePos()
            if (w[2] >= x >= w[0]) and (w[3] >= y >= w[1]): pause = True
            else: pause = False
        sleep(delay - .1)
        keys('keycode', 125)


if __name__ == '__main__':
    pages = eval(str(argv[1]))
    minutes = eval(str(argv[2]))
    
    window = [176, 22, 1111, 632]
    setSkimWindow(window)

    activate()
    seconds = (minutes / pages) * 60
    for i in range(0, pages):
        movePage(seconds, window)




    
    
    
    
    
    
