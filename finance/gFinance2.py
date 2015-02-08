import urllib2
import re
import datetime
from appscript import *
from os import system, listdir, getcwd
from time import sleep
# from listFout import listFout
# from listFin import listFin


def activateSafari():
    app(u'Safari').activate()

def runScript(script):
    return app(u'Safari').documents[1].do_JavaScript(script)

def gotoUrl(url):
    activateSafari()
    orig_url = app(u'Safari').documents[1].URL.get()
    app(u'Safari').windows[1].tabs[1].properties.set({k.URL: url})
    if orig_url != url:
        checkLoaded(orig_url, url)

def getSource():
    activateSafari()
    x = app(u'Safari').windows[1].tabs[1].source.get()
    return x

def getPage():
    activateSafari()
    data = app(u'Safari').documents[1].text.get()
    return data

def checkLoaded(orig_url, url):
    current = (app(u'Safari').documents[1].URL.get()).replace('%20', ' ')
    if current == url:
        next = True
    else:
        next = False
    if current == orig_url:
        stop, iter_num = False, 30
        while stop == False or iter_num != 0:
            sleep(2)
            current = (app(u'Safari').documents[1].URL.get()).replace('%20', ' ')
            if current == url:
                next = True
                stop = True
                break
            else:
                check = runScript('document.readyState')
                if check == 'complete':
                    return True
                else:
                    iter_num = iter_num - 1
        if iter_num == 0:
            return False
    current = (app(u'Safari').documents[1].URL.get()).replace('%20', ' ')   
    if current == url or next == True:
        check = runScript('document.readyState')
        if check == 'complete':
            return True
        else:
            stop, iter_num = False, 60
            while stop == False or iter_num != 0:
                sleep(1)
                check = runScript('document.readyState')
                if check == 'complete':
                    return True
                else:
                    iter_num = iter_num - 1
            if iter_num == 0:
                return False

def getScreenerUrl(varList):
    (startNum, resultNum, MarketCap, PE, Price52WkPercChange, High52Wk, Low52Wk,
         QuotePercChange, QuoteLast, Price13WkPercChange, Price26WkPercChange,
         Volume, AvgVolume, DividendYield, BookValuePerShare,
         CurrentRatio, TotalDebtToAssetsQtr, NetProfitMarginPerc,
         GrossMargin, ReturnOnInvestment, ReturnOnAssets, ReturnOnEquity) = varList

    url = (
    'http://www.google.com/finance?start=' + 
    startNum + 
    '&num=' + 
    resultNum + 
    '&gl=us&' + 
    'hl=en&' + 
    'q=((exchange%3ANYSE)%20OR%20(exchange%3ANASDAQ)%20OR%20(exchange%3AAMEX))%20%5B')

    varUrl = ''
    if MarketCap:
        varUrl = varUrl + (
        '(MarketCap%20%3E%20' + 
        MarketCap[0] + 
        '%20%7C%20MarketCap%20%3D%20' + 
        MarketCap[0] + 
        ')%20%26%20(MarketCap%20%3C%20' + 
        MarketCap[1] + 
        '%20%7C%20MarketCap%20%3D%20' + 
        MarketCap[1] + 
        ')%20%26%20')
    if PE:
        varUrl = varUrl + ('(PE%20%3E%20' + 
        PE[0] + 
        '%20%7C%20PE%20%3D%20' + 
        PE[0] + 
        ')%20%26%20(PE%20%3C%20' + 
        PE[1] + 
        '%20%7C%20PE%20%3D%20' + 
        PE[1] + 
        ')%20%26%20')

    if Price52WkPercChange:
        varUrl = varUrl + ('(Price52WeekPercChange%20%3E%20' + 
        Price52WkPercChange[0] + 
        '%20%7C%20Price52WeekPercChange%20%3D%20' + 
        Price52WkPercChange[0] + 
        ')%20%26%20(Price52WeekPercChange%20%3C%20' + 
        Price52WkPercChange[1] + 
        '%20%7C%20Price52WeekPercChange%20%3D%20' + 
        Price52WkPercChange[1] + 
        ')%20%26%20')

    if High52Wk: 
        varUrl = varUrl + ('(High52Week%20%3E%20' + 
        High52Wk[0] + 
        '%20%7C%20High52Week%20%3D%20' + 
        High52Wk[0] + 
        ')%20%26%20(High52Week%20%3C%20' + 
        High52Wk[1] + 
        '%20%7C%20High52Week%20%3D%20' + 
        High52Wk[1] + 
        ')%20%26%20')

    if Low52Wk:     
        varUrl = varUrl + ('(Low52Week%20%3E%20' + 
        Low52Wk[0] + 
        '%20%7C%20Low52Week%20%3D%20' + 
        Low52Wk[0] + 
        ')%20%26%20(Low52Week%20%3C%20' + 
        Low52Wk[1] + 
        '%20%7C%20Low52Week%20%3D%20' + 
        Low52Wk[1] + 
        ')%20%26%20')

    if QuotePercChange:      
        varUrl = varUrl + ('(QuotePercChange%20%3E%20' + 
        QuotePercChange[0] + 
        '%20%7C%20QuotePercChange%20%3D%20' + 
        QuotePercChange[0] + 
        ')%20%26%20(QuotePercChange%20%3C%20' + 
        QuotePercChange[1] + 
        '%20%7C%20QuotePercChange%20%3D%20' + 
        QuotePercChange[1] + 
        ')%20%26%20')
        
    if QuoteLast:      
        varUrl = varUrl + ('(QuoteLast%20%3E%20' + 
        QuoteLast[0] + 
        '%20%7C%20QuoteLast%20%3D%20' + 
        QuoteLast[0] + 
        ')%20%26%20(QuoteLast%20%3C%20' + 
        QuoteLast[1] + 
        '%20%7C%20QuoteLast%20%3D%20' + 
        QuoteLast[1] + 
        ')%20%26%20')

    if Price13WkPercChange:       
        varUrl = varUrl + ('(Price13WeekPercChange%20%3E%20' + 
        Price13WkPercChange[0] + 
        '%20%7C%20Price13WeekPercChange%20%3D%20' + 
        Price13WkPercChange[0] + 
        ')%20%26%20(Price13WeekPercChange%20%3C%20' + 
        Price13WkPercChange[1] + 
        '%20%7C%20Price13WeekPercChange%20%3D%20' + 
        Price13WkPercChange[1] + 
        ')%20%26%20')

    if Price26WkPercChange:        
        varUrl = varUrl + ('(Price26WeekPercChange%20%3E%20' + 
        Price26WkPercChange[0] + 
        '%20%7C%20Price26WeekPercChange%20%3D%20' + 
        Price26WkPercChange[0] + 
        ')%20%26%20(Price26WeekPercChange%20%3C%20' + 
        Price26WkPercChange[1] + 
        '%20%7C%20Price26WeekPercChange%20%3D%20' + 
        Price26WkPercChange[1] + 
        ')%20%26%20')

    if Volume:        
        varUrl = varUrl + ('(Volume%20%3E%20' + 
        Volume[0] + 
        '%20%7C%20Volume%20%3D%20' + 
        Volume[0] + 
        ')%20%26%20(Volume%20%3C%20' + 
        Volume[1] + 
        '%20%7C%20Volume%20%3D%20' + 
        Volume[1] + 
        ')%20%26%20')

    if AvgVolume:       
        varUrl = varUrl + ('(AverageVolume%20%3E%20' + 
        AvgVolume[0] + 
        '%20%7C%20AverageVolume%20%3D%20' + 
        AvgVolume[0] + 
        ')%20%26%20(AverageVolume%20%3C%20' + 
        AvgVolume[1] + 
        '%20%7C%20AverageVolume%20%3D%20' + 
        AvgVolume[1] + 
        ')%20%26%20')

    if DividendYield:       
        varUrl = varUrl + ('(DividendYield%20%3E%20' + 
        DividendYield[0] + 
        '%20%7C%20DividendYield%20%3D%20' + 
        DividendYield[0] + 
        ')%20%26%20(DividendYield%20%3C%20' + 
        DividendYield[1] + 
        '%20%7C%20DividendYield%20%3D%20' + 
        DividendYield[1] + 
        ')%20%26%20')

    if BookValuePerShare:       
        varUrl = varUrl + ('(BookValuePerShareYear%20%3E%20' + 
        BookValuePerShare[0] + 
        '%20%7C%20BookValuePerShareYear%20%3D%20' + 
        BookValuePerShare[0] + 
        ')%20%26%20(BookValuePerShareYear%20%3C%20' + 
        BookValuePerShare[1] + 
        '%20%7C%20BookValuePerShareYear%20%3D%20' + 
        BookValuePerShare[1] + 
        ')%20%26%20')

    if CurrentRatio:       
        varUrl = varUrl + ('(CurrentRatioYear%20%3E%20' + 
        CurrentRatio[0] + 
        '%20%7C%20CurrentRatioYear%20%3D%20' + 
        CurrentRatio[0] + 
        ')%20%26%20(CurrentRatioYear%20%3C%20' + 
        CurrentRatio[1] + 
        '%20%7C%20CurrentRatioYear%20%3D%20' + 
        CurrentRatio[1] + 
        ')%20%26%20')

    if TotalDebtToAssetsQtr:       
        varUrl = varUrl + ('(TotalDebtToAssetsQuarter%20%3E%20' + 
        TotalDebtToAssetsQtr[0] + 
        '%20%7C%20TotalDebtToAssetsQuarter%20%3D%20' + 
        TotalDebtToAssetsQtr[0] + 
        ')%20%26%20(TotalDebtToAssetsQuarter%20%3C%20' + 
        TotalDebtToAssetsQtr[1] + 
        '%20%7C%20TotalDebtToAssetsQuarter%20%3D%20' + 
        TotalDebtToAssetsQtr[1] + 
        ')%20%26%20')

    if NetProfitMarginPerc:       
        varUrl = varUrl + ('(NetProfitMarginPercent%20%3E%20' + 
        NetProfitMarginPerc[0] + 
        '%20%7C%20NetProfitMarginPercent%20%3D%20' + 
        NetProfitMarginPerc[0] + 
        ')%20%26%20(NetProfitMarginPercent%20%3C%20' + 
        NetProfitMarginPerc[1] + 
        '%20%7C%20NetProfitMarginPercent%20%3D%20' + 
        NetProfitMarginPerc[1] + 
        ')%20%26%20')

    if GrossMargin:       
        varUrl = varUrl + ('(GrossMargin%20%3E%20' + 
        GrossMargin[0] + 
        '%20%7C%20GrossMargin%20%3D%20' + 
        GrossMargin[0] + 
        ')%20%26%20(GrossMargin%20%3C%20' + 
        GrossMargin[1] + 
        '%20%7C%20GrossMargin%20%3D%20' + 
        GrossMargin[1] + 
        ')%20%26%20')

    if ReturnOnInvestment:       
        varUrl = varUrl + ('(ReturnOnInvestmentTTM%20%3E%20' + 
        ReturnOnInvestment[0] + 
        '%20%7C%20ReturnOnInvestmentTTM%20%3D%20' + 
        ReturnOnInvestment[0] + 
        ')%20%26%20(ReturnOnInvestmentTTM%20%3C%20' + 
        ReturnOnInvestment[1] + 
        '%20%7C%20ReturnOnInvestmentTTM%20%3D%20' + 
        ReturnOnInvestment[1] + 
        ')%20%26%20')

    if ReturnOnAssets:       
        varUrl = varUrl + ('(ReturnOnAssetsTTM%20%3E%20' + 
        ReturnOnAssets[0] + 
        '%20%7C%20ReturnOnAssetsTTM%20%3D%20' + 
        ReturnOnAssets[0] + 
        ')%20%26%20(ReturnOnAssetsTTM%20%3C%20' + 
        ReturnOnAssets[1] + 
        '%20%7C%20ReturnOnAssetsTTM%20%3D%20' + 
        ReturnOnAssets[1] + 
        ')%20%26%20')

    if ReturnOnEquity:       
        varUrl = varUrl + ('(ReturnOnEquityTTM%20%3E%20' + 
        ReturnOnEquity[0] + 
        '%20%7C%20ReturnOnEquityTTM%20%3D%20' + 
        ReturnOnEquity[0] + 
        ')%20%26%20(ReturnOnEquityTTM%20%3C%20' + 
        ReturnOnEquity[1] + 
        '%20%7C%20ReturnOnEquityTTM%20%3D%20' + 
        ReturnOnEquity[1] + 
        ')%20%26%20')

    varUrl = varUrl.rstrip('%20%26%20')
    
    url = url + varUrl + (
    '%5D&' + 
    'restype=company&' + 
    'output=json&' + 
    'noIL=1')

    return url

def get_finance(exchange, ticker):
    url = 'http://www.google.com/finance/historical?q=' + exchange + '%3A' + ticker + '&output=csv'
    try:
        csv = urllib2.urlopen(url).read()
    except:
        workDir = '/Users/admin/Desktop'
        file_name = 'data.csv.xls'
        x_1 = listdir(workDir)
        if x_1.count(file_name) != 0:
            cmd = 'rm ' + workDir + '/' + file_name
            system(cmd)
            x_1 = listdir(workDir)
        gotoUrl(url)
        x = listdir(workDir)
        if len(x) == len(x_1):
            stop = False
            iter_num = 10
            while (stop == False or iter_num != 0):
                iter_num = iter_num - 1
                x = listdir(workDir)
                if len(x) == len(x_1) + 1:
                    stop = True
                    break
                else:
                    sleep(1)
        f = open(file_name, 'r')
        csv = f.read()
        f.close()
        cmd = 'rm ' + workDir + '/' + file_name
        system(cmd)
    csv = csv[csv.find('Date'):]
    data = []
    csvDays = csv.split('\n')
    for day in csvDays:
        data.append(day.split(','))
    return data


def getTechAnalysisStocks(data, count):
    # compare stocks 52 wk high low range and last price, 
    # where stocks ranked higher if last price closer to low number
    # where stocks have increasing price changes over last 3 days
    change_3_day, range_price_ratio, yest_prices = [], [], []
    for i in range(0, len(data)):
        # print data[i]['title']
        x = get_finance(data[i]['exchange'], data[i]['ticker'])
        high, low = [], []
        ############# 2:-1
        for it in x[1:-1]:
            high.append(eval(it[2]))
            low.append(eval(it[3]))
        high.sort()
        low.sort()
        ############# x[1][4]
        last_price = eval(x[1][4])
        # yest_prices.append(str(last_price))
        range_52_wk = high[len(high) - 1] - low[0]
        range_price_ratio.append((high[len(high) - 1] - last_price) / range_52_wk)
        temp_3_day_change = 0
        ############# x[1:4]
        for it in x[1:4]:
            open_ = eval(it[1])
            close_ = eval(it[4])
            temp_3_day_change = temp_3_day_change + ((close_ - open_) / open_)
        change_3_day.append(temp_3_day_change)

    a = range_price_ratio[:]
    a.sort()
    b = change_3_day[:]
    b.sort()

    ranking = [], []  # result,data (= ratio_rank + change_rank
    for i in range(0, len(data)):
        ratio_rank = (a.index(range_price_ratio[i]) + 1) / float(len(range_price_ratio))
        change_rank = (b.index(change_3_day[i]) + 1) / float(len(change_3_day))
        ranking[0].append(ratio_rank + change_rank)
        ranking[1].append(str(ratio_rank) + ' + ' + str(change_rank))

    c = ranking[0][:]
    c.sort()
    c.reverse()

    price_column = ''
    stockPicks, used = [], []
    for i in range(0, count):
        indexNum = ranking[0].index(c[i])
        if used.count(indexNum) == 0:
            used.append(indexNum)
        else:
            start = True
            while start == True:
                indexNum = ranking[0].index(c[i], indexNum + 1)
                if used.count(indexNum) == 0:
                    used.append(indexNum)
                    start = False
                    break
        
        stockName = data[indexNum]['title']
        ticker = data[indexNum]['exchange'] + ':' + data[indexNum]['ticker']
        if price_column == '':
            for it in data[indexNum]['columns']:
                if it['field'] == 'QuoteLast':
                    price_column = data[indexNum]['columns'].index(it)
        price = data[indexNum]['columns'][price_column]['value']
        # price=yest_prices[indexNum]
        ############################
        
        a = data[indexNum]['ticker'] + ' -- ' + data[indexNum]['title']
        b = 'range_ratio= ' + str(range_price_ratio[indexNum]) + ' -- 3 day change= ' + str(change_3_day[indexNum])
        print a
        print b
        stockPicks.append([stockName, ticker, price])
    return stockPicks

def TestTechAnalysisStocks(data, count):
    # compare stocks 52 wk high low range and last price, 
    # where stocks ranked higher if last price closer to low number
    # where stocks have increasing price changes over last 3 days
    testRange = [2, 12]  # test whether 7 days ago, would this algorithm work, how about 6 days etc...
    percentChanges = []

    '''
    
    for each company
        for each 3 day increase
            X1_ = mean of all 3 day total price change
            X2_ = mean of all 3 day average price change
            X3_ = mean of all 3 day average(day_high-close_price)
            X4_ = mean of all 3 day average(close_price-day_low)
            X5_ = mean of all 3 day average_change(day_high-close_price)
            X6_ = mean of all 3 day average_change(close_price-day_low)
            X7_ = mean of all 3 day change(day_high-close_price)
            X8_ = mean of all 3 day change(close_price-day_low)
            X9_ = mean of all P/E
            X10_= mean of all volume
            X11_= mean of all average volume
            X12_= mean of all market cap
            X13_= mean of range ratio
            X14_= mean of 13 wk change
            X15_= mean of 26 wk change
            Y_ = mean of next day increase
    
categorical percent/day changes
categorical dollar/day changees
quarter net income change & quarter percent changes
quarter net income change & quarter dollar changes
    '''

    change_3_day, range_price_ratio, picked_prices, test_prices = [], [], [], []

    for i in range(0, len(data)):
        # print data[i]['title']
        x = data[i]['financials']

        # print "testDay= ", x[daysBack][0]
        high, low = [], []
        ############# 2:-1
        for it in x[daysBack:-1]:
            high.append(eval(it[2]))
            low.append(eval(it[3]))
        high.sort()
        low.sort()
        ############# x[1][4]
        
        last_price = eval(x[daysBack][4])
        picked_prices. append(last_price)
        test_prices.append(eval(x[daysBack - 1][4]))
        range_52_wk = high[len(high) - 1] - low[0]
        range_price_ratio.append((high[len(high) - 1] - last_price) / range_52_wk)
        temp_3_day_change = 0
        ############# x[1:4]
        for it in x[daysBack:daysBack + 3]:
            # print 'one of 3 days= ',it[0]
            open_ = eval(it[1])
            close_ = eval(it[4])
            temp_3_day_change = temp_3_day_change + ((close_ - open_) / open_)
        change_3_day.append(temp_3_day_change)
        # return

    for j in range(testRange[0], testRange[1]):
        daysBack = j  # this is the number of days when stock would be predicted, then tested against next day
        # print j
        
        a = range_price_ratio[:]
        a.sort()
        b = change_3_day[:]
        b.sort()

        ranking = [], []  # result,data (= ratio_rank + change_rank
        for i in range(0, len(data)):
            ratio_rank = (a.index(range_price_ratio[i]) + 1) / float(len(range_price_ratio))
            change_rank = (b.index(change_3_day[i]) + 1) / float(len(change_3_day))
            ranking[0].append((ratio_rank * 1.8) + (change_rank * 1))
            ranking[1].append(str(ratio_rank) + ' + ' + str(change_rank))

        c = ranking[0][:]
        c.sort()
        c.reverse()

        price_column = ''
        stockPicks, used, testMoney = [], [], 200000
        for i in range(0, count):
            indexNum = ranking[0].index(c[i])
            if used.count(indexNum) == 0:
                used.append(indexNum)
            else:
                start = True
                while start == True:
                    indexNum = ranking[0].index(c[i], indexNum + 1)
                    if used.count(indexNum) == 0:
                        used.append(indexNum)
                        start = False
                        break
            
            stockName = data[indexNum]['title']
            ticker = data[indexNum]['exchange'] + ':' + data[indexNum]['ticker']
            if price_column == '':
                for it in data[indexNum]['columns']:
                    if it['field'] == 'QuoteLast':
                        price_column = data[indexNum]['columns'].index(it)
            price = data[indexNum]['columns'][price_column]['value']
            # price=yest_prices[indexNum]
            ############################
            
            a = data[indexNum]['ticker'] + ' -- ' + data[indexNum]['title']
            b = 'range_ratio= ' + str(range_price_ratio[indexNum]) + ' -- 3 day change= ' + str(change_3_day[indexNum])
            # print a
            # print b
            old = picked_prices[indexNum]
            new = test_prices[indexNum]
            check = ((new - old) / old)
            # print check
            testMoney = testMoney + ((testMoney / count) * check)
            stockPicks.append([stockName, ticker, price])
        percentChanges.append(((testMoney - 200000) / 200000.0))
        print testMoney
        print ''
    print percentChanges
    x = 0
    for it in percentChanges:
        x = x + it
    print x * 200000
    return stockPicks

def addBuyTrans(ticker, shares, shareprice, total, timestamp):
    buyTrans = (
    '<BUYSTOCK>\n' + 
    '<INVBUY>\n' + 
    '<INVTRAN>\n' + 
    '<FITID>1\n' + 
    '<DTTRADE>' + timestamp[:8] + '000000.000\n' + 
    '</INVTRAN>\n' + 
    '<SECID>\n' + 
    '<UNIQUEID>' + ticker + '\n' + 
    '<UNIQUEIDTYPE>TICKER\n' + 
    '</SECID>\n' + 
    '<UNITS>' + shares + '\n' + 
    '<UNITPRICE>' + shareprice + '\n' + 
    '<TOTAL>-' + total + '\n' + 
    '<SUBACCTSEC>CASH\n' + 
    '<SUBACCTFUND>CASH\n' + 
    '</INVBUY>\n' + 
    '<BUYTYPE>BUY\n' + 
    '</BUYSTOCK>\n')
    return buyTrans

def addStockInfo(stockName, ticker):
    stockInfo = (
    '<STOCKINFO>\n' + 
    '<SECINFO>\n' + 
    '<SECID>\n' + 
    '<UNIQUEID>' + ticker + '\n' + 
    '<UNIQUEIDTYPE>TICKER\n' + 
    '</SECID>\n' + 
    '<SECNAME>' + stockName + '\n' + 
    '<TICKER>' + ticker[ticker.find(':') + 1:] + '\n' + 
    '</SECINFO>\n' + 
    '</STOCKINFO>')
    return stockInfo

def makePortfolioFile(stockData):
    t = datetime.datetime.today()
    a = str(t.strftime("%Y%m%d"))
    ###############    ###############
    a = '20110309'
    b = str(eval(str(t.hour)) + 5)
    c = str(t.minute)
    d = str(t.second) + '.000'
    timestamp = a + b + c + d
    buyTransData, stockInfoData = [], []
    for item in stockData:
        stockName, ticker, shares, shareprice, total = item
        buyTransData.append(addBuyTrans(ticker, shares, shareprice, total, timestamp))
        stockInfoData.append(addStockInfo(stockName, ticker))

    folioText = (
    'OFXHEADER:100\n' + 
    'DATA:OFXSGML\n' + 
    'VERSION:102\n' + 
    'SECURITY:NONE\n' + 
    'ENCODING:USASCII\n' + 
    'CHARSET:1252\n' + 
    'COMPRESSION:NONE\n' + 
    'OLDFILEUID:NONE\n' + 
    'NEWFILEUID:NONE\n\n' + 
    '<OFX>\n' + 
    '<SIGNONMSGSRSV1>\n' + 
    '<SONRS>\n' + 
    '<STATUS>\n' + 
    '<CODE>0\n' + 
    '<SEVERITY>INFO\n' + 
    '</STATUS>\n' + 
    '<DTSERVER>' + timestamp + '\n' + 
    '<LANGUAGE>ENG\n' + 
    '</SONRS>\n' + 
    '</SIGNONMSGSRSV1>\n' + 
    '<INVSTMTMSGSRSV1>\n' + 
    '<INVSTMTTRNRS>\n' + 
    '<TRNUID>1001\n' + 
    '<STATUS>\n' + 
    '<CODE>0\n' + 
    '<SEVERITY>INFO\n' + 
    '</STATUS>\n' + 
    '<INVSTMTRS>\n' + 
    '<DTASOF>' + timestamp + '\n' + 
    '<CURDEF>USD\n' + 
    '<INVACCTFROM>\n' + 
    '<BROKERID>google.com\n' + 
    '<ACCTID>test\n' + 
    '</INVACCTFROM>\n' + 
    '<INVTRANLIST>\n' + 
    '<DTSTART>20110218000000.000\n' + 
    '<DTEND>' + timestamp[:8] + '000000.000\n')
    
    for entry in buyTransData:
        for it in entry.split('\n'):
            folioText = folioText + it + '\n'

    folioText = folioText + (
    '</INVTRANLIST>\n' + 
    '</INVSTMTRS>\n' + 
    '</INVSTMTTRNRS>\n' + 
    '</INVSTMTMSGSRSV1>\n' + 
    '<SECLISTMSGSRSV1>\n' + 
    '<SECLIST>')

    for entry in stockInfoData:
        for it in entry.split('\n'):
            folioText = folioText + it + '\n'

    folioText = folioText + (
    '</SECLIST>\n' + 
    '</SECLISTMSGSRSV1>\n' + 
    '</OFX>')
    return folioText

def runAnalysis(varList):
    url = getScreenerUrl(varList)
    try:
        content = urllib2.urlopen(url).read()
    except:
        gotoUrl(url)
        content = getPage()
    x = dict(eval(content))
    if x['num_company_results'] == '':
        print 'no results'
    else:
        data = []
        data.extend(x['searchresults'])
        resultCount = eval(x['num_company_results'])
        print resultCount
        print ''

        if resultCount > eval(resultNum):
            iterNum = resultCount // eval(resultNum)
            for i in range(0, iterNum):
                startNum = str(eval(resultNum) + eval(resultNum) * i)
                varList = (startNum, resultNum, MarketCap, PE, '', '', '',
                         '', '', Price13WkPercChange, Price26WkPercChange,
                         Volume, AvgVolume, '', BookValuePerShare,
                         CurrentRatio, TotalDebtToAssetsQtr, NetProfitMarginPerc,
                         '', '', '', '')
                url = getScreenerUrl(varList)
                try:
                    content = urllib2.urlopen(url).read()
                except:
                    gotoUrl(url)
                    content = getPage()
                x = dict(eval(content))
                data.extend(x['searchresults'])

        financeFolder = '/Users/admin/Stocks/History'
        saved_finance_data = listdir(financeFolder)

        for i in range(0, len(data)):
            fileName = 'HIS_' + data[i]['exchange'] + '_' + data[i]['ticker'] + '.txt'
            if saved_finance_data.count(fileName) == 0:
                data[i]['financials'] = get_finance(data[i]['exchange'], data[i]['ticker'])
                listFout(data[i]['financials'], financeFolder + '/' + fileName)
            else:
                data[i]['financials'] = listFin(financeFolder + '/' + fileName)



        # compare stocks 52 wk high low range and last price, 
        # where stocks ranked higher if last price closer to low number
        # where stocks have increasing price changes over last 3 days
        # count=20
        # investment=200000
        # stockPicks = TestTechAnalysisStocks(data,count)
    '''
        stockPicks = getTechAnalysisStocks(data,count) #stockName,ticker,price
        stockData=[]
        for it in stockPicks:
            stockName,ticker,price=it
            shares=str(round((investment/float(count))/eval(price)))[:-2]
            total=str(eval(shares)*eval(price))
            stockData.append([stockName,ticker,shares,price,total])

        folioText=makePortfolioFile(stockData)

        f=open('/Users/admin/Desktop/new_data.ofx','w')
        f.write(folioText)
        f.close()
    '''

def checkCurrentStocks():
    # workDir=getcwd()
    workDir = '/Users/admin/SERVER2/BD_Scripts/finance/'
    stocks_file = 'stocks.txt'
    f = open(workDir + '/' + stocks_file, 'r')
    stocks = f.readlines()
    f.close()
    info = []
    for it in stocks:
        if it[0].isdigit() == True:
            ticker = it.split('	')[1]
            target = eval(it.split('	')[2])
            a = ''
            b = ticker
            data = get_finance(a, b)
            if len(info) == 0:
                info.append(data[1][0])
            price = eval(data[1][4])
            # ##
            # for it in data:
            #    print it
            #    return
            # ##
            text = str(price) + '\t' + b + '\t' + str(target)
            if target - price < 2:
                text = text + '\t' + 'SELL??'
            info.append(text)
        else:
            a = ''
            b = it
            data = get_finance(a, b)
            if len(info) == 0:
                info.append(data[1][0])
            price = eval(data[1][4])
            text = str(price) + '\t' + b
            info.append(text)

    for it in info:
        print it

    # desktopFile='/Users/admin/Desktop/stockUpdate.txt'
    # f=open(desktopFile,'w')
    # for it in info:
    #    f.write(it+'\n')
    # f.close()

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

startNum = '0'
resultNum = '20'
MarketCap = ['100000000', '403540000000']
PE = ['0', '5000']
Price52WkPercChange = ['-1000', '1000']
High52Wk = ['0.0', '500000']
Low52Wk = ['0.0', '500000']
QuotePercChange = ['1', '100']
QuoteLast = ['0', '500000']
Price13WkPercChange = ['0', '5000']
Price26WkPercChange = ['-100', '5000']
Volume = ['10000', '500000000']
AvgVolume = ['0', '500000000']

DividendYield = ['0', '50']
BookValuePerShare = ['-500', '200000']
CurrentRatio = ['0', '500']
TotalDebtToAssetsQtr = ['0', '5000']
NetProfitMarginPerc = ['-500000', '100000000']
GrossMargin = ['-50000', '100']
ReturnOnInvestment = ['-10000', '50000']
ReturnOnAssets = ['250000', '5000']
ReturnOnEquity = ['-500,000', '50000']


'''
varList=(startNum,resultNum,MarketCap,PE,Price52WkPercChange,High52Wk,Low52Wk,
         QuotePercChange,QuoteLast,Price13WkPercChange,Price26WkPercChange,
         Volume,AvgVolume, DividendYield, BookValuePerShare,
         CurrentRatio, TotalDebtToAssetsQtr, NetProfitMarginPerc,
         GrossMargin, ReturnOnInvestment, ReturnOnAssets, ReturnOnEquity)
'''
'''
varList=(startNum,resultNum,MarketCap,PE,'','','',
         '','',Price13WkPercChange,Price26WkPercChange,
         Volume,AvgVolume, '', BookValuePerShare,
         CurrentRatio, TotalDebtToAssetsQtr, NetProfitMarginPerc,
         '', '', '', '')
'''
varList = (startNum, resultNum, MarketCap, PE, '', '', '',
         '', '', Price13WkPercChange, Price26WkPercChange,
         Volume, AvgVolume, '', BookValuePerShare,
         CurrentRatio, TotalDebtToAssetsQtr, NetProfitMarginPerc,
         '', '', '', '')


# runAnalysis(varList)
checkCurrentStocks()


    

