from datetime import datetime

def roman_numerals():
    return ['I', 'II', 'III', 'IV', 'V', 'VI',
            'VII', 'VIII', 'IX', 'X', 'XI', 'XII',
            'XIII', 'XIV', 'XV', 'XVI', 'XVII',
            'XVIII', 'XIX', 'XX', 'XXI', 'XXII',
            'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII',
            'XXVIII', 'XXIX', 'XXX', 'XXXI', 'XXXII',
            'XXXIII', 'XXXIV', 'XXXV', 'XXXVI',
            'XXXVII', 'XXXVIII', 'XXXIX', 'XL',
            'XLI', 'XLII', 'XLIII', 'XLIV', 'XLV',
            'XLVI', 'XLVII', 'XLVIII', 'XLIX', 'L',
            'LI', 'LII', 'LIII', 'LIV', 'LV', 'LVI',
            'LVII', 'LVIII', 'LIX', 'LX', 'LXI',
            'LXII', 'LXIII', 'LXIV', 'LXV', 'LXVI',
            'LXVII', 'LXVIII', 'LXIX', 'LXX',
            'LXXI', 'LXXII', 'LXXIII', 'LXXIV',
            'LXXV', 'LXXVI', 'LXXVII', 'LXXVIII',
            'LXXIX', 'LXXX', 'LXXXI', 'LXXXII',
            'LXXXIII', 'LXXXIV', 'LXXXV', 'LXXXVI',
            'LXXXVII', 'LXXXVIII', 'LXXXIX', 'XC',
            'XCI', 'XCII', 'XCIII', 'XCIV', 'XCV',
            'XCVI', 'XCVII', 'XCVIII', 'XCIX', 'C']

def change_date(str_or_list, fromFormat, toFormat):
    fromFormat_var, toFormat_var = '', ''
    for letter in fromFormat: 
        if letter.isalpha(): fromFormat_var += '%' + letter
        else: fromFormat_var += letter
    for letter in toFormat: 
        if letter.isalpha(): toFormat_var += '%' + letter
        else: toFormat_var += letter  # really, add what is not a letter
    '''
    % | meaning
    - | --------
    d   day of month as dec. [01,31]
    a   abbr. weekday
    A   full weekday
    
    b   abbr. month
    B   -full
    m   month as dec.

    y   year without century as dec. [00,99]
    Y   year with century as dec.

    M   minute as dec.
    H   24-hour as dec.
    I   12-hour as dec.
    p   AM or PM
    S   second as dec.

    w   weekday as dec.
    U   week number (Sun. as first day)
    W   week number (Mon. as first day)
    j   day of the year as dec.
    '''
    if type(str_or_list) == str: x = [str_or_list]
    elif type(str_or_list) == list: x = str_or_list
    else: print asdgsd
    a = []
    for it in x:
        try:
            date_var = datetime.strptime(it, fromFormat_var)
            a.append(date_var.strftime(toFormat_var))
        except:
            print it
            print it[:-3]
            print 'len:', len(it)
            date_var = datetime.strptime(it, fromFormat_var)
            a.append(date_var.strftime(toFormat_var))
            print date_var
            print sfg
    
    if len(a) == 1: return a[0]
    else: return a
