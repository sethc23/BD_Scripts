from selenium import selenium
import unittest, time, re
from appscript import *


def waitForPage():
    app(u'Firefox').activate()
    app(u'System Events').processes[u'Firefox'].menu_bars[1].menu_bar_items[u'View'].click()
    x = app(u'System Events').processes[u'Firefox'].menu_bars[1].menu_bar_items[u'View'].menus[1].menu_items[u'Reload'].attributes[u'AXEnabled'].value.get()
    while x != True:
        app(u'System Events').processes[u'Firefox'].menu_bars[1].menu_bar_items[u'View'].click()
        x = app(u'System Events').processes[u'Firefox'].menu_bars[1].menu_bar_items[u'View'].menus[1].menu_items[u'Reload'].attributes[u'AXEnabled'].value.get()

sel = selenium("localhost", 4444, "*firefox", "http://www.lexisnexis.com/")
sel.start()
sel.open("/lawschool/login.aspx")
waitForPage()
sel.wait_for_page_to_load("90000")
sel.type("txtPassword", "ferrari1")
sel.click("cmdSignOn")
sel.wait_for_page_to_load("30000")
sel.click("link=> Research Now")
sel.wait_for_page_to_load("30000")
sel.select_frame("targWindow")
sel.click("Go")
sel.wait_for_page_to_load("30000")
sel.click("free_formToTocLink")
sel.wait_for_page_to_load("30000")
sel.click("//img[@alt='Expand']")
sel.wait_for_page_to_load("30000")
