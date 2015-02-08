from sys import argv
from gFinance2 import checkCurrentStocks



if __name__ == '__main__':
    try:
        task = argv[1]
        stop = False
    except:
        print 'argument error'
        stop = True

    if stop == False:
        if task == "stockupdates":
            checkCurrentStocks()
