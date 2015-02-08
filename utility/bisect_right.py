def bisect_right(SortedList_in, Right_Value):
    a = SortedList_in
    start = 0
    end = len(a)
    Irange = end - start
    Bisect = int(Irange * 0.5)
    last = 0
    for i in range(0, end):
        # if i == end-1:
            # print 'bisect went to end - most certainly trouble'
        if a[Bisect] == Right_Value:
            Bisect = Bisect - 1
        if a[Bisect] >= Right_Value:
            Bisect = int((Bisect * 0.5))
        else:
            if Bisect == last:
                if a[Bisect + 1] < Right_Value:
                     Bisect = int((Bisect * 0.5) + Bisect - 1)
                     if Bisect > len(a) - 1:
                         Bisect = len(a) - 1
                else:
                    break
            last = Bisect
    if Bisect != 0:
        while a[Bisect] >= Right_Value:
            Bisect = Bisect - 1
    while a[Bisect] < Right_Value:
        Bisect = Bisect + 1
    
    return Bisect
