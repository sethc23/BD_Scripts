
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
import controllers
from time import time

import gdata.docs
import gdata.docs.service
import gdata.service
import gdata.alt.appengine
import gdata.spreadsheet.text_db
import cgi
from google.appengine.api import users
import wsgiref.handlers

_DEBUG = True  # Set to true if we want to have our webapp print stack traces

class GetNewData(webapp.RequestHandler):  ######----Get and Put Data into Datastore
  def get(self):
    controllers.data.GetDataApp(self)
    self.redirect('/')
  def post(self):
    controllers.data.GetDataApp(self)
    self.redirect('/')

class ShowData(webapp.RequestHandler):  ######----Show data on first page
  def get(self):
    location = "boston"
    category = "wanted"
    controllers.data.ShowDataApp(self, location, category)
    
class SortData(webapp.RequestHandler):
  def post(self):
    controllers.data.SortDataApp(self)
    
class GetPostCount(webapp.RequestHandler):
    def post(self):
        self.redirect('/getpostcount', permanent=True)
    def get(self):
        action = self.request.get('action')
        result = controllers.research.GetPostCountApp(self, action)
        if str(action) == "senderror":
            action = ""
        if str(result) == "run again":
            # self.response.out.write("next step  - return was: "+str(result))
            fromapp = "fromapp=getpostcount"
            BounceBack(self, fromapp, action)
        elif str(result).find("print") == 0:
            self.response.out.write(str(result))
        elif str(result).find("error") == 0:
            self.response.out.write(str(result))
        elif str(result).find("redirect") == 0:
            redirect = result[9:]
            self.redirect(redirect, permanent=True)
        else:
            self.response.out.write("error: " + str(result))

class ShowPostCount(webapp.RequestHandler):
  def get(self):
    location = "boston"
    controllers.research.ShowPostCountApp(self, location, "")

class MakeQuery(webapp.RequestHandler):  ######----Show data on first page
    def get(self):
        specific = self.request.get('specific')
        controllers.data.MakeQueryApp(self, "get", specific)
    def post(self):
        specific = self.request.get('specific')
        controllers.data.MakeQueryApp(self, "post", specific)
    
class SendEmail(webapp.RequestHandler):
  def get(self):
    to = self.request.get('to')
    controllers.email.SendEmailApp(self, to)
    
class SetHierarchy(webapp.RequestHandler):
  def post(self):
    postUrl = "/sethierarchy?"
    action = self.request.get('action')
    if action != "":
        postUrl = postUrl + "action=" + action
    specific = self.request.get('specific')
    if specific != "":
        postUrl = postUrl + "&specific=" + specific
    self.redirect(postUrl, permanent=True)
  def get(self):
    action = self.request.get('action')
    specific = self.request.get('specific')
    if str(action):
        now = int(time())
        end = now + (15)
        # attempts = 10
        #================
        #    maximize time to run process
        #================ 
        while end >= now:  # and attempts != 0:
            result = controllers.research.SetHierarchyApp(self, action, specific)
            now = int(time())
            if str(result) == 'run again':
                result = controllers.research.SetHierarchyApp(self, action, specific)
            if str(result).find('run again') != 0:
                break
            now = int(time())
            # attempts = attempts - 1    
        if str(result) == "run again":
            fromapp = "fromapp=sethierarchy"
            if str(specific):
                action = action + "&specific=" + specific
            BounceBack(self, fromapp, action)
        elif str(result).find("print") == 0:
            self.response.out.write(str(result))
        elif str(result).find("error") == 0:
            self.response.out.write(str(result))
        elif str(result).find("redirect") == 0:
            redirect = result[9:]
            self.redirect(redirect, permanent=True)
        else:
            self.response.out.write(str(result))

class Bounce(webapp.RequestHandler):
  def get(self):
      frommachine = self.request.get('frommachine')
      tomachine = self.request.get('tomachine')
      action = self.request.get('action')
      fromapp = self.request.get('fromapp')
      specific = self.request.get('specific')
      if specific == "":
          redirect = (str(frommachine) + "/" + str(fromapp) + "?action=" + str(action))
      else:
          redirect = (str(frommachine) + "/" + str(fromapp) + "?action=" + str(action) + 
                        "&specific=" + str(specific))
      self.redirect(redirect, permanent=True)

class GetWebPage(webapp.RequestHandler):  ######----Get and Put Data into Datastore
  def get(self):
    controllers.data.GetWebPageApp(self)
    
class DBcenter(webapp.RequestHandler):
    def post(self):
        submit = self.request.get('app')
        specific = self.request.get('specific')
        if str(submit) == "Query":
            postUrl = "/makequery?specific=" + specific
            self.redirect(postUrl, permanent=True)
        else:
            action = self.request.get('action')
            postUrl = "/dbcenter?action=" + action + "&specific=" + specific
            self.redirect(postUrl, permanent=True)
    def get(self):
        submit = self.request.get('app')
        specific = self.request.get('specific')
        if str(submit) == "Query":
            postUrl = "/makequery?specific=" + specific
            self.redirect(postUrl, permanent=True)
        else:
            action = self.request.get('action')
            result = controllers.DBhome.DBdataApp(self, action, specific)
            if str(result).find("run again") == 0:
                fromapp = "fromapp=dbcenter"
                postUrl = action + "&specific=" + specific
                BounceBack(self, fromapp, postUrl)
            elif str(result).find("error:") == 0:
                self.response.out.write(str(result))
            elif type(eval(str(result))) == int:
                redirect = "/?count_result=" + str(result)
                self.redirect(redirect, permanent=True)
            else:
                self.response.out.write(str(result))

class Gdata(webapp.RequestHandler):
    def post(self):
        action = self.request.get('action')
        self.response.out.write(":" + str(action))
        self.redirect('/gdata?action=' + action, permanent=True)
    def get(self):
        action = self.request.get('action')
        self.response.out.write(":" + str(action))
        result = controllers.gdataApp.ManageDataApp(self, action)
        if str(result) == "run again":
            fromapp = "fromapp=gdata"
            postUrl = action
            BounceBack(self, fromapp, postUrl)
        elif str(result).find("print") == 0:
            self.response.out.write(str(result))
        elif str(result).find("error") == 0:
            self.response.out.write(str(result))
        elif str(result).find("redirect") == 0:
            redirect = result[9:]
            self.redirect(redirect, permanent=True)
        else:
            self.response.out.write("error: " + str(result))

class TestPage(webapp.RequestHandler):
  def get(self):
      pass

def BounceBack(self, fromapp, action):
    # TODO: change bounce back to global references
    # frommachine = "frommachine=http://money-press.appspot.com"
    # tomachine = "tomachine=http://money-train.appspot.com"
    frommachine = "frommachine=http://localhost:8102"
    tomachine = "tomachine=http://localhost:8103"
    commands = (str(frommachine) + "&" + str(tomachine) + "&" + 
                        str(fromapp) + "&action=" + str(action))
    redirect = "/bounce?" + commands
    self.redirect(redirect)


def main():
  application = webapp.WSGIApplication([
  ('/', ShowData), ('/getdata', GetNewData),
  ('/sortdata', SortData), ('/sendemail', SendEmail),
  ('/getpostcount', GetPostCount), ('/showpostcount', ShowPostCount),  # TODO: look at ShowPostCount
  ('/sethierarchy', SetHierarchy), ('/bounce', Bounce),
  ('/getwebpage', GetWebPage), ('/dbcenter', DBcenter),
  ('/makequery', MakeQuery), ('/gdata', Gdata),
  ('/testpage', TestPage)], debug=True)  

  run_wsgi_app(application)
  
  
if __name__ == '__main__':
  main()
