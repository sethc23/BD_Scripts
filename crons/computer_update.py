from os import system
from sys import path, argv
# path.append('/Users/admin/SERVER2/BD_Scripts/utility')
# from var_checks import internet_on


if __name__ == '__main__':
    # print str(time.localtime()[3])+':'+str(time.localtime()[4])

    try:
        script = argv[1]
        stop = False
    except:
        print 'argument error'
        stop = True

    if stop == False:
        if script == 'macport':
            system('echo "money" | sudo port upgrade outdated')


