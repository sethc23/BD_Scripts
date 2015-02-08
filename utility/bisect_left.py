def bisect_left(SortedList_in, Left_Value):
    a = SortedList_in
    start = 0
    end = len(a)
    Irange = end - start
    Bisect = int(Irange * 0.5)
    last = 0
    for i in range(0, end):
        # if i == end-1:
            # print 'bisect went to end - most certainly trouble'
            # print 'or bisect went all the way to (end - 1)'
        if a[Bisect] == Left_Value:
            Bisect = Bisect - 1
            if Bisect > len(a) - 1:
                Bisect = len(a) - 1
        if a[Bisect - 1] < Left_Value:
            Bisect = int((Bisect * 0.5) + Bisect - 1)
            if Bisect > len(a) - 1:
                Bisect = len(a) - 1
        else:
            if Bisect == last:
                if a[Bisect] <= Left_Value:
                     Bisect = int((Bisect * 0.5))
                     if Bisect > len(a) - 1:
                        Bisect = len(a) - 1
                else:
                    break
            last = Bisect
    if Bisect != Left_Value:
        while a[Bisect] <= Left_Value:
            Bisect = Bisect + 1
    while a[Bisect] > Left_Value:
        Bisect = Bisect - 1
    
    return Bisect
