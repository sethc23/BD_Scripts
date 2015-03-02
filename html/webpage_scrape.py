
from time                       import sleep
from sys                        import argv, path
path.append(                    '../appscript')
path.append(                    '..')
# import                             Safari_API
from handle_cookies             import getFirefoxCookie,set_cookies_from_text
import mechanize
from time                       import time             as TIME
from time                       import sleep            as delay


class Mechanize():
    
    def __init__(self,browser,cookies):
        from mechanize import Browser
        br = Browser()
        # Cookie Jar
        if cookies == "firefox": cj = getFirefoxCookie()
        else: cj=set_cookies_from_text(cookies)
        br.set_cookiejar(cj)
        # Browser options 
        br.set_handle_equiv(True) 
        #br.set_handle_gzip(True) 
        br.set_handle_redirect(True) 
        br.set_handle_referer(True) 
        br.set_handle_robots(False)
        # Debug Options
        #br.set_debug_http(True) 
        #br.set_debug_redirects(True) 
        #br.set_debug_responses(True)
        # Follows refresh 0 but not hangs on refresh > 0 
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        # User-Agent
        br.addheaders = [('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.45 Safari/537.36'),
        ('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')]
        self.browser = br
        self.browserType = 'mechanize'

    def get_page(self, gotoUrl):
        br=self.browser
        br.open(gotoUrl)
        return br.response().read()

    def get_file(self,filePath,savePath):
        self.browser.retrieve(filePath, savePath,timeout=3600)[0]

class Webdriver():

    def __init__(self,browser,cookies):
        self.browser=''
        self.type=browser
        self.cookies=''
        if browser == 'firefox': self.set_firefox(cookies)
        if browser == 'phantom': self.set_phantom(cookies)
        if browser == 'chrome': self.set_chrome(cookies)
        self.window=self.browser
    
    def set_firefox(self,cookies,with_profile=False):
        from selenium import webdriver
        if with_profile==True:
            profile = webdriver.firefox.firefox_profile.FirefoxProfile()
            profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ('application/pdf'))
            profile.set_preference('browser.helperApps.neverAsk.saveToDisk','application/pdf,application/x-pdf')
            profile.set_preference('browser.download.folderList', 2)
            profile.set_preference('browser.download.dir', '/Users/admin/Desktop')
            profile.set_preference('browser.download.manager.showWhenStarting', False)
            profile.set_preference('extensions.blocklist.enabled', False)
            profile.set_preference('pdfjs.disabled', True)
            self.browser = webdriver.Firefox(firefox_profile=profile)
        else:
            # profile = webdriver.firefox.firefox_profile.FirefoxProfile()
            self.browser = webdriver.Firefox()

    def set_chrome(self,cookies,with_profile=False):
        from selenium import webdriver
        profile = webdriver.Chrome()
    
    def set_phantom(self,cookies):
        from selenium import webdriver
        driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        #driver.Remote.current_url(self)
        driver.set_window_position(0, 0)
        driver.set_window_size(300, 300)
        driver.desired_capabilities['applicationCacheEnabled'] = True
        driver.desired_capabilities['locationContextEnabled'] = True
        driver.desired_capabilities['databaseEnabled'] = True
        driver.desired_capabilities['webStorageEnabled'] = True
        driver.desired_capabilities['JavascriptEnabled'] = True
        driver.desired_capabilities['acceptSslCerts'] = True
        driver.desired_capabilities['browserConnectionEnabled'] = True
        driver.desired_capabilities['rotatable'] = True
        driver.implicitly_wait(120)
        self.browser = driver

    def open_page(self, gotoUrl):
        self.browser.get(gotoUrl)
        #sleep(10)
    
    def source(self):
        return self.browser.page_source

    def get_cookies(self):
        self.cookies=self.browser.get_cookies()
    
    def get_url(self):
        return self.browser.current_url

    def execute(self,script,*args):
        return self.browser.execute(script,*args)

    def wait_for_page(self,timeout_seconds=45):
        end                     =   TIME() + timeout_seconds
        while TIME()<end:
            status              =   self.browser.execute_script("return document.readyState")
            if status=='complete':
                return
            else:
                delay(2)

    def window_count(self):
        return len(self.browser.window_handles)
    
    def frame_count(self):
        return self.browser.frame_attr()

    def reset_frames(self):
        return self.window.switch_to_window(self.window.current_window_handle)
    
    def screenshot(self,save_path='/Volumes/mbp2/Users/admin/Desktop/screen.png'):
        self.browser.save_screenshot(save_path)
    
    def quit(self):
        self.browser.quit()


#     jcode="document.title;"
#     a=br.execute_script(jcode)
#     br.find_element_by_name("uid").send_keys(usr)
#     br.find_element_by_name("upass").send_keys(pw)
#     br.find_element_by_name("continueButtonExisting").click()
#     br.find_element_by_xpath("//a[contains(@href,'"+it+"')]").click()  
#     br.get_window_size('current')
#     br.switch_to_window(br.window_handles[0])
#     from selenium.webdriver.common.action_chains import ActionChains
#     action_chains = ActionChains(br)
#     q=action_chains.context_click(p).perform()
#     br.save_screenshot('/Users/admin/Desktop/screen.png')

class Urllib2():

    def __init__(self,browser,cookies):
        import urllib2
        self.browser=urllib2
        if cookies != '':
            cj=set_cookies_from_text(cookies)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            self.browser.install_opener(opener)
        
    def get_page(self, gotoUrl):
        return self.browser.urlopen(gotoUrl, data=None,timeout=3600)

class EXTRAS():
    """
    Usage:
        from html.webpage_scrape import EXTRAS
        Select                  =   EXTRAS()._select

    """

    def __init__(self):
        pass

    def _alert(self):
        from selenium.webdriver.common.alert import Alert
        self._alert             =   Alert

    def _select(self,element):
        """
        Example:

        time_element            =   br.browser.find_element_by_id('deliveryTime')
        time_str                =   "1:00 PM"
        _select                 =   Select(time_element)
        _select.select_by_value(    time_str)
        assert time_element.get_attribute("value")==time_str

        ALSO:

        addresses               =   br.window.find_element_by_xpath("//select[@id='Address']")
        last_option             =   len(addresses.find_elements_by_tag_name('option'))-1
        addresses.find_elements_by_tag_name('option')[last_option].click()

        """
        from selenium.webdriver.support.select import Select
        self._select            =   Select(element)


class scraper():

    def __init__(self,browser,cookies=''):
        if browser == 'mechanize':
            t = Mechanize(self,cookies)
            self.browser,self.browserType = t.browser,t.browserType
        if browser == 'firefox' or browser == 'phantom' or browser == 'chrome':
            self.browser=Webdriver(browser,cookies)
        if browser == 'urllib2': self.browser = Urllib2(self,cookies)

    


        #self.browser.type=browser
        #self.browser.cookies=cookies


    
    # request = mechanize.Request("http://example.com/", data)
    # txt=br.response().read()
    # print txt
    
    # txt=getUrl(gotoUrl)
    # print txt#txt[txt.find('style21'):txt.find('style21')+1000]
    
    # import spynner
    # from spynner import browser
    # import pyquery
    # import private
    # import pynotify
    # import time
    '''
    cj = getFirefoxCookie()
    #opener=spynner.get_opener(cj)
    #.HTTPCookieProcessor(cookielib.CookieJar()))
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:17.0) Gecko/20100101 Firefox/17.0'),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Language', 'en-gb,en;q=0.5'),
        ('Accept-Encoding', 'gzip,deflate'),
        ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
        ('Keep-Alive', '115'),
        ('Connection', 'keep-alive'),
        ('Cache-Control', 'max-age=0'),
        ('Referer', 'http://iapps.courts.state.ny.us/iscroll/'),
    ]
    '''
    
    '''
    agent = browser.Browser()
    agent.manager.setCookieJar(cj)
    #agent.get_mozilla_cookies()
    agent.load(gotoUrl)
    agent.wait(3)
    agent.create_webview(True)
    agent.show()
    '''
    
    # g=getOneElement(txt,'class','style21')
    # print g
    
    # class="style21"
    # span class="style21"
    '''
    import urllib2
    import cookielib
    from sqlite3 import dbapi2
    
    host = 'iapps.courts.state.ny.us'
    ff_cookie_file= '/Users/admin/Library/Application Support/Firefox/Profiles/nvoog4xy.default/cookies.sqlite'
    
    file = open("cookie.txt", "w")
    file.write("#LWP-Cookies-2.0\n")
    match = '%%%s%%' % host
    
    con = dbapi2.connect(ff_cookie_file)
    cur = con.cursor()
    cur.execute("select name, value, path, host from moz_cookies where host like ?", [match])
    for item in cur.fetchall():
        cookie = "Set-Cookie3: %s=\"%s\"; path=\"%s\";  \
        domain=\"%s\"; expires=\"2038-01-01 00:00:00Z\"; version=0\n" % (
        item[0], item[1], item[2], item[3],
        )
    file.write(cookie)
    file.close()
    cj = cookielib.LWPCookieJar()
    cj.load("cookie.txt")
    
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:17.0) Gecko/20100101 Firefox/17.0'),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Language', 'en-gb,en;q=0.5'),
        ('Accept-Encoding', 'gzip,deflate'),
        ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
        ('Keep-Alive', '115'),
        ('Connection', 'keep-alive'),
        ('Cache-Control', 'max-age=0'),
        ('Referer', 'http://iapps.courts.state.ny.us/iscroll/'),
    ]
    urllib2.install_opener(opener)
    
    #urllib2.install_opener(opener)
    
    
    #req = urllib2.Request(gotoUrl)
    res = urllib2.urlopen(gotoUrl)
    print res.read()
    '''
#     pass
# 
# def setup_browser():
#     import mechanize
#     br = mechanize.Browser()
#     # Cookie Jar
#     # cj = cookielib.LWPCookieJar()
#     cj = getFirefoxCookie()
#     br.set_cookiejar(cj)
#     # Browser options 
#     br.set_handle_equiv(True) 
#     br.set_handle_gzip(True) 
#     br.set_handle_redirect(True) 
#     br.set_handle_referer(True) 
#     br.set_handle_robots(False)
#     # Debug Options
#     br.set_debug_http(True) 
#     br.set_debug_redirects(True) 
#     br.set_debug_responses(True)
#     # Follows refresh 0 but not hangs on refresh > 0 
#     br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
#     # User-Agent
#     br.addheaders = [('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:17.0) Gecko/20100101 Firefox/17.0'),
#     ('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
#     return br
# 
# def addFormVars(_type, _name, _value):
#     #------------LOGIN
#     startUrl = 'https://store.law.com/Registration/Login.aspx?source=' + today_url
#     # print startUrl
#     br.open(startUrl)
#     # print br.forms
#     br.select_form(nr=0)
# 
#     br.new_control("text", "uid", {'value': usr})
#     br.new_control("password", "upass", {'value': pw})
#     # br.new_control("password", "upass", {pw})
#     br.form.fixup()
#     # control = br.form.find_control("action")
#     # control.readonly = False
#     # br["action"] = "login"
#      
#     # form = br.form
#     # print form
#     # form['uid'] = usr
#     # form['upass'] = pw
#     # form.set_value("schase@cozen.com","uid")
#     # form.set_value("ferrarif50","upass")
#     print br.form
#     br.submit()  # submit current form
# 
# 
# def getUrl(url):
#     return urllib2.urlopen(url).read()
# 
# def runLinks(links, start=0):
#     a = links
#     for i in range(0, len(a)):
#         gotoUrl = 'http://iapps.courts.state.ny.us/iscroll/CaseCap.jsp?IndexNo=' + a[i]
#         Safari_API.openUrl(gotoUrl)
#         sleep(5)
#         try:
#             Safari_API.saveHTML(saveBase + a[i] + '_status' + '.html', findStr=['table', 'width', '300'])
#         except:    
#             Safari_API.saveHTML(saveBase + a[i] + '_status' + '.html', findStr=['div', 'class', 'style21'])
#         
#         Safari_API.saveHTML(saveBase + a[i] + '_names' + '.html', findStr=['table', 'width', '97%'])
#         sleep(10)
# 
# def runLink(link, linkID, saveBase):
#     Safari_API.openUrl(link)
#     sleep(5)
#     try:
#         Safari_API.saveHTML(saveBase + linkID + '_status' + '.html', findStr=['table', 'width', '300'])
#     except:    
#         Safari_API.saveHTML(saveBase + linkID + '_status' + '.html', findStr=['div', 'class', 'style21'])
#     
#     Safari_API.saveHTML(saveBase + linkID + '_names' + '.html', findStr=['table', 'width', '97%'])
#     sleep(10)


# f=open('/Users/admin/Desktop/case_check.txt','r')
# x=f.readlines()
# f.close()
#
# a=[]
# for it in x:
#     #print it[7]
#     #break
#     it=it.rstrip('\r')
#     it=it.rstrip('\n')
#     it=it[:-1]
#     if it[7]=='9': b=it[:6]+'-19'+it[7:]
#     else: b=it[:6]+'-20'+it[7:]
#     if a.count(b)==0: a.append(b)
#
#
#
# baseUrl='http://iapps.courts.state.ny.us/iscroll/CaseCap.jsp?IndexNo='
# saveBase='/Users/admin/Desktop/HB/'
#
# #runLinks(a)



# gotoUrl = SEARCH_URL_0
# html_hard_coding(gotoUrl)
# scraper(browser='mechanize',cookies='')