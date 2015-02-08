from sys import argv


try:
    arg_list = []
    for arg in argv:
        arg_list.append(arg)
    start = True
except:
    start = False


if start == True:
    if arg_list[1][:9] == 'skimClick':
        window, mouse = arg_list[2].split(':')
        x1, y1 = window.split(',')  # skim coord
        # print 'x1,y1',x1,y1
        x2, y2 = mouse.split(',')  # screen coord
        # print 'x2,y2',x2,y2
        x3, y3 = (eval(x2) - eval(x1)), (eval(y2) - eval(y1))  # mouse in skim coord
        # print 'x3,y3',x3,y3
        color_sq = ((514 - 338) // 9) - (((514 - 338) // 9) // 2)
        f = open('/Users/admin/SERVER2/BD_Scripts/AS_vars.txt', 'r')
        x = f.read()
        f.close()
        
        if x == '':  # if var is blank
            high = 2
            under = 7
        else:
            high, under = x.split('\n')
            high, under = eval(high), eval(under)

        if ((338 <= x3) and (x3 <= 514)) and ((26 <= y3) and (y3 <= 49)):  # if click is in color picker bar...
            if arg_list[1][9:] == 'Highlight':
                # high=str(eval(x1)+x3)+' '+str(eval(y1)+y3)
                # click=high
                click = str(eval(x1) + x3) + ' ' + str(eval(y1) + y3)
                high = int(round((x3 - 338) / 19.0))
            elif arg_list[1][9:] == 'Underline':
                # under=str(eval(x1)+x3)+' '+str(eval(y1)+y3)
                # click=under
                click = str(eval(x1) + x3) + ' ' + str(eval(y1) + y3)
                under = int(round((x3 - 338) / 19.0))
            # print 'in box'
        else:
            if arg_list[1][9:] == 'Highlight':
                # click=high
                click = str(eval(x1) + 338 - 10 + (((514 - 338) // 9) * high)) + ' ' + str(eval(y1) + 37)
            elif arg_list[1][9:] == 'Underline':
                # click=under
                click = str(eval(x1) + 338 - 10 + (((514 - 338) // 9) * under)) + ' ' + str(eval(y1) + 37)
            # print 'not in box'

        f = open('/Users/admin/SERVER2/BD_Scripts/AS_vars.txt', 'w')
        high = str(high) + '\n'
        under = str(under)
        f.write(high + under)
        f.close()

        print click
        
