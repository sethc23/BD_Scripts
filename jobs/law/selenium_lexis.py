from selenium import selenium
import unittest, time, re

class selenium_lexis(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*firefox", "http://www.lexisnexis.com/")
        self.selenium.start()
    
    def test_selenium_lexis(self):
        sel = self.selenium
        sel.open("/lawschool/login.aspx")
        sel.wait_for_page_to_load("30000")
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
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
