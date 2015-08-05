
from sys                                    import argv, path
path.append(                                    '../appscript')
path.append(                                    '..')
# import                                    Safari_API
from handle_cookies                         import getFirefoxCookie,set_cookies_from_text
import mechanize
from selenium.webdriver.common.keys         import Keys
from time                                   import time                     as TIME
from time                                   import sleep                    as delay
from ipdb                                   import set_trace                as i_trace
from random                                 import randrange

class Mechanize:
    
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

class Browsermob_Proxy:
    
    def __init__(self,package_type='server'):
        if package_type=='server':
            self                            =   self.Server()
        elif package_type=='client':
            self                            =   self.Client()
        
    def Server(self):
        from browsermobproxy                import Server
        self                                =   Server("/usr/local/bin/browsermob-proxy",options={'port':11001})

    def Client(self):
        from browsermobproxy                import Client
        self                                =   Client('%(scheme)s://%(remote_ip)s:%(remote_port)s' % self.prox_client_data)

class Nginx:
    def __init__(self,_parent):
        self.T                              =   _parent.T
    def reload(self):
        (_out,_err)                         =   self.T.exec_cmds(           ['bash -i -l -c "ng_reload"'],
                                                                            root=True)
        assert not _out and _err is None

class Webdriver:

    def __init__(self,browser,**kwargs):
        self.browser            =   '  '
        self.type               =   browser
        
        # for k,v in kwargs.iteritems():
        #     setattr(self,k,v)

        if browser == 'firefox':    
            self.window                     =   self.set_firefox(**kwargs)
        if browser == 'phantom':    
            self.window                     =   self.set_phantom(**kwargs)
        if browser == 'chrome':    
            self.window                     =   self.set_chrome(**kwargs)
        # self.window             =   self.browser
        from selenium.webdriver.common.keys import Keys 
        self.keys               =   Keys
    
    def set_firefox(self,with_profile=False,**kwargs):
        from selenium           import webdriver
        if with_profile==True:
            p                   =   webdriver.firefox.firefox_profile.FirefoxProfile()
            p.set_preference(       'browser.helperApps.neverAsk.saveToDisk', ('application/pdf'))
            p.set_preference(       'browser.helperApps.neverAsk.saveToDisk','application/pdf,application/x-pdf')
            p.set_preference(       'browser.download.folderList', 2)
            p.set_preference(       'browser.download.dir', '/Users/admin/Desktop')
            p.set_preference(       'browser.download.manager.showWhenStarting', False)
            p.set_preference(       'extensions.blocklist.enabled', False)
            p.set_preference(       'pdfjs.disabled', True)
            self.browser        =   webdriver.Firefox(firefox_profile=profile)
        else:
            # profile = webdriver.firefox.firefox_profile.FirefoxProfile()
            self.browser        =   webdriver.Firefox()

    def set_chrome(self,with_profile=False,**kwargs):
        from selenium                       import webdriver
        self.T                              =   kwargs['To_Class'](kwargs)
        opts                                =   webdriver.ChromeOptions()
        if hasattr(self.T,'proxy'):
            opts.add_argument(                  '--proxy-server=%s'%proxy)
        attempts                            =   0
        while True:
            try:
                d                           =   webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',
                                                                 chrome_options=opts)
                init_d_cap = {'browserName':'{android|chrome|firefox|htmlunit|internet explorer|iPhone|iPad|opera|safari}',
                              'version':'',
                              'platform':'{WINDOWS|XP|VISTA|MAC|LINUX|UNIX|ANDROID|ANY}'}
                user_d_cap = {'javascriptEnabled':'',
                              'databaseEnabled':'',
                              'locationContextEnabled':'',
                              'applicationCacheEnabled':'',
                              'browserConnectionEnabled':'',
                              'webStorageEnabled':'',
                              'acceptSslCerts':'',
                              'rotatable':'',
                              'nativeEvents':'',
                              'proxy':'proxy pbject',
                              'unexpectedAlertBehaviour':'string',
                              'elementScrollBehavior':'integer',
                              '':'',}
                d.add_cookie(                   self.T.id.cookie.contents)
                break
            except:
                attempts                   +=   1
            if attempts>=5:
                raise SystemError
                break
        return d
    
    def set_phantom(self,**kwargs):
        from selenium                       import webdriver
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

        if not hasattr(self,'T'):               return webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        try:
            self.T                          =   kwargs['To_Class'](kwargs)
        except:
            return                              webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')

        # CAPABILITIES
        dcap                                =   dict(DesiredCapabilities.PHANTOMJS)
        
        if not hasattr(self.T.br.user_agent,'user_agent'):
            self.T.br.user_agent            =   ("Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1")
        dcap["phantomjs.page.settings.userAgent"] = self.T.br.user_agent
        

        # SERVICE ARGS
        service_args                        =   []
        if hasattr(self.T.br.service_args,'cookie_file'):
            service_args.extend(                ['--cookies-file=%s'        % self.T.br.service_args.cookie_file])
        if hasattr(self.T.br.service_args,'debug'):
            service_args.extend(                ['--debug=%s'               % str(self.T.br.service_args.debug).lower()])
        if hasattr(self.T.br.service_args,'ignore_ssl_errors'):
            service_args.extend(                ['--ignore-ssl-errors=%s'   % str(self.T.br.service_args.ignore_ssl_errors).lower()])
        if hasattr(self.T.br.service_args,'load_images'):
            service_args.extend(                ['--load-images=%s'         % str(self.T.br.service_args.load_images).lower()])
        if hasattr(self.T.br.service_args,'local_remote_access'):
            service_args.extend(                ['--local-to-remote-url-access=%s' % str(self.T.br.service_args.local_remote_access).lower()])
        if hasattr(self.T.br.service_args,'debugger_port'):
            service_args.extend(                ['--remote-debugger-port=%s'% self.T.br.service_args.debugger_port])
        if hasattr(self.T.br.service_args,'proxy'):
            service_args.extend(                ['--proxy=%s'               % self.T.br.service_args.proxy[:7]
                                                                                if self.T.br.service_args.proxy.find('http://')==0
                                                                                else self.T.br.service_args.proxy,
                                                 '--proxy-type=http'])
        if hasattr(self.T.br.service_args,'ssl_cert_path'):
            service_args.extend(                ['--ssl-certificates-path=%s'% self.T.br.service_args.ssl_cert_path])
        if hasattr(self.T.br.service_args,'wd_log_level'):
            service_args.extend(                ['--webdriver-loglevel=%s'  % self.T.br.service_args.wd_log_level])

        # INITIATE WEB DRIVER
        d                                   =   webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs',
                                                                    desired_capabilities=dcap,
                                                                    service_args=service_args)
        # CAPABILITY CONFIG
        known_capabilities                  =   ['applicationCacheEnabled',
                                                 'locationContextEnabled',
                                                 'databaseEnabled',
                                                 'webStorageEnabled',
                                                 'javascriptEnabled',
                                                 'acceptSslCerts',
                                                 'browserConnectionEnabled',
                                                 'rotatable']
        selected_capabilities               =   [] if not hasattr(self.T.br,'capabilities') else self.T.br.capabilities
        for it in known_capabilities:
            d.capabilities[it]              =   True if selected_capabilities.count(it) else False
        
        # BROWSER CONFIG
        if hasattr(self.T.br.browser_config,'window_position'):
            d.set_window_position(              self.T.br.browser_config.window_position)

        if hasattr(self.T.br.browser_config,'window_size'):
            d.set_window_position(              self.T.br.browser_config.window_size)
        else:
            d.set_window_position(              300,300)
        
        if hasattr(self.T.br.browser_config,'maximize_window') and self.T.br.browser_config.maximize_window:
            d.maximize_window(                  )
        
        if hasattr(self.T.br.browser_config,'implicitly_wait'):
            d.implicitly_wait(                  self.T.br.browser_config.implicitly_wait)
        else:
            d.implicitly_wait(                  120)

        if hasattr(self.T.br.browser_config,'page_load_timeout'):
            d.set_page_load_timeout(            self.T.br.browser_config.page_load_timeout)
        else:
            d.set_page_load_timeout(            150)

        return d

    def Select(self,element):
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
        return Select(element)

    def Actions(self,browser):
        """See here: https://selenium-python.readthedocs.org/api.html#module-selenium.webdriver.common.action_chains """
        from selenium.webdriver.common.action_chains import ActionChains
        # Example: action_chains.context_click(p).perform()
        return ActionChains(browser)

    def execute(self,script,*args):
        return self.window.execute_script(script,*args)

    def frame_count(self):
        return self.window.frame_attr()

    def get_cookies(self):
        self.cookies=self.window.get_cookies()

    def get_url(self):
        return self.window.current_url

    def open_page(self, gotoUrl):
        self.window.get(gotoUrl)
        #sleep(10)

    def post_screenshot(self):
        fpath                               =   '/home/ub2/.scripts/tmp/phantom_shot'
        if self.T.THIS_PC=='ub2':
            self.screenshot(                      fpath )
        else:
            self.screenshot(                    '/tmp/phantom_shot' )
            cmds                            =   ['scp /tmp/phantom_shot %(host)s@%(serv)s:%(fpath)s;'
                                                 % ({ 'host'                :   'ub2',
                                                      'serv'                :   'ub2',
                                                      'fpath'               :   fpath }),
                                                 'rm -f /tmp/phantom_shot;']
            p                               =   self.T.sub_popen(cmds,stdout=self.T.sub_PIPE,shell=True)
            (_out,_err)                     =   p.communicate()
            assert _out                    ==   ''
            assert _err                    ==   None
        return

    def quit(self):
        self.window.quit()

    def randomize_keystrokes(self,keys,element,**kwargs):
        T                                   =   {'shortest_delay_ms'        :   500,
                                                 'longest_delay_ms'         :   1200,
                                                }
        for k,v in kwargs:
            T.update(                           { k                         :   v })
        pauses                              =   map(lambda s: randrange(
                                                    T['shortest_delay_ms'],
                                                    T['longest_delay_ms'])//float(100),keys)

        for i in range(len(keys)):
            action_chain                    =   self.Actions(self.window)
            action_chain.send_keys_to_element(  element,keys[i]).perform()
            delay(                              pauses[i])
        return True

    def reset_frames(self):
        return self.window.switch_to_window(self.window.current_window_handle)

    def screenshot(self,save_path='/Volumes/mbp2/Users/admin/Desktop/screen.png'):
        self.window.save_screenshot(save_path)

    def scroll_to_element(self,element):
        return self.window.execute_script('document.getElementById("%s").scrollIntoView(true)'%element)

    def set_element_val(self,element,val,val_type):
        _str_sub                            =   '"%s"' % val if val_type is str else '%s' % val
        _script                             =   'var elem = document.getElementById("%s"); elem.value = %s;' % (element,_str_sub)
        return self.window.execute_script( _script)

    def source(self):
        return self.window.page_source

    def wait_for_condition(self,condition,param1,param2,invert=False,timeout_seconds=45,poll_frequency=0.5):
        """

            NOTE -- UNTESTED

            Usage:

                br.wait_for_condition('presence_of_element_located','id','some_tag_id_value',
                                    invert=False,timeout_seconds=45,poll_frequency=1.0)


            WebDriverWait(self, driver, timeout, poll_frequency=0.5, ignored_exceptions=None)

        """
        def element_types(element_type):
            global By
            from selenium.webdriver.common.by import By
            element_types           =  {'class_name'            :By.CLASS_NAME,
                                        'id'                    :By.ID,
                                        'link_text'             :By.LINK_TEXT,
                                        'name'                  :By.NAME,
                                        'partial_link_text'     :By.PARTIAL_LINK_TEXT,
                                        'tag_name'              :By.TAG_NAME,
                                        'xpath'                 :By.XPATH}
            assert element_types.keys().count(element_type)>0
            return element_types[element_type]
        def expected_conditions(condition,*params):
            global EC
            from selenium.webdriver.support import expected_conditions as EC
            expected_conditions     =  {"title_is"                                  :   EC.title_is,
                                        "title_contains"                            :   EC.title_contains,
                                        "presence_of_element_located"               :   EC.presence_of_element_located,
                                        "visibility_of_element_located"             :   EC.visibility_of_element_located,
                                        "visibility_of"                             :   EC.visibility_of,
                                        "presence_of_all_elements_located"          :   EC.presence_of_all_elements_located,
                                        "text_to_be_present_in_element"             :   EC.text_to_be_present_in_element,
                                        "text_to_be_present_in_element_value"       :   EC.text_to_be_present_in_element_value,
                                        "frame_to_be_available_and_switch_to_it"    :   EC.frame_to_be_available_and_switch_to_it,
                                        "invisibility_of_element_located"           :   EC.invisibility_of_element_located,
                                        "element_to_be_clickable"                   :   EC.element_to_be_clickable,
                                        "staleness_of"                              :   EC.staleness_of,
                                        "element_to_be_selected"                    :   EC.element_to_be_selected,
                                        "element_located_to_be_selected"            :   EC.element_located_to_be_selected,
                                        "element_selection_state_to_be"             :   EC.element_selection_state_to_be,
                                        "element_located_selection_state_to_be"     :   EC.element_located_selection_state_to_be,
                                        "alert_is_present"                          :   EC.alert_is_present}
            assert expected_conditions.keys().count(condition)>0
            if condition=='presence_of_element_located':
                expected_res        =   (element_types(params[0]), params[1])
                condition_res       =   expected_conditions[condition](expected_res)
            else:
                assert True=='DEVELOPMENT INCOMPLETE'
            return condition_res


        global WebDriverWait
        from selenium.webdriver.support.ui import WebDriverWait


        if not invert:
            WebDriverWait(self.window, timeout_seconds,poll_frequency).until(
                expected_conditions(condition,param1,param2))
        else:
            WebDriverWait(self.window, timeout_seconds,poll_frequency).until_not(
                expected_conditions(condition,param1,param2))

    def wait_for_page(self,timeout_seconds=45):
        """
        Include start page to confirm change started ??
        """
        end                     =   TIME() + timeout_seconds
        delay(                      1)
        while TIME()<end:
            status              =   self.window.execute_script("return document.readyState")
            if status=='complete':
                return
            else:
                delay(              2)

    def window_count(self):
        return len(self.window.window_handles)

    def zoom(self,percentage):
        self.window.execute_script('document.body.style.zoom = "%s";' % percentage)

    def misc_code():
        #     jcode="document.title;"
        #     a=br.execute_script(jcode)
        #     br.find_element_by_name("uid").send_keys(usr)
        #     br.find_element_by_name("upass").send_keys(pw)
        #     br.find_element_by_name("continueButtonExisting").click()
        #     br.find_element_by_xpath("//a[contains(@href,'"+it+"')]").click()  
        #     br.get_window_size('current')
        #     br.switch_to_window(br.window_handles[0])
        pass

class Urllib2:

    def __init__(self,browser,cookies):
        import urllib2
        self.browser                        =   urllib2
        if cookies != '':
            cj                              =   set_cookies_from_text(cookies)
            opener                          =   urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            self.browser.install_opener(        opener)
        
    def get_page(self, gotoUrl):
        return self.browser.urlopen(gotoUrl, data=None,timeout=3600)

class EXTRAS:
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

class scraper:

    def __init__(self,browser,**kwargs):
        # if proxy:
        #     self.proxy_server               =   Browsermob_Proxy('server')
        #     self.proxy_server.start(            )
        #     self.proxy                      =   self.proxy_server.create_proxy()
            
        #     self.proxy_client               =   Browsermob_Proxy('client')

        if browser == 'mechanize':
            t                               =   Mechanize(self)
            self.browser,self.browserType   =   t.browser,t.browserType
        
        if ['firefox','phantom','chrome'].count(browser):
            self.browser                    =   Webdriver(browser,**kwargs)
        
        if browser == 'urllib2': 
            self.browser                    =   Urllib2(self)

    


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