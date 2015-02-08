
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
from webob import Request
import controllers

_DEBUG = True  # Set to true if we want to have our webapp print stack traces

class GetNewData(webapp.RequestHandler):  ######----Get and Put Data into Datastore
  def get(self):
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
  def get(self):  
    controllers.research.GetPostCountApp(self)

class ShowPostCount(webapp.RequestHandler):
  def get(self):
    location = "boston"
    controllers.research.ShowPostCountApp(self, location, "")
    
class SendEmail(webapp.RequestHandler):
  def get(self):
    controllers.email.SendEmailApp(self)
    
class SetHierarchy(webapp.RequestHandler):
  def get(self):
    action = self.request.get('action')
    specific = self.request.get('specific')
    if str(action):
        result = controllers.research.SetHierarchyApp(self, action, specific)
        if str(action) == "categories" and str(result) == "success":
            fromapp = "sethierarchy"
            redirect = "/bounce?fromapp=" + str(fromapp) + "&action=" + str(action)
            self.redirect(redirect)
        else:
            self.response.out.write(str(result))

class Bounce(webapp.RequestHandler):
    def get(self):          
        frommachine = self.request.get('frommachine')
        tomachine = self.request.get('tomachine')
        action = self.request.get('action')
        fromapp = self.request.get('fromapp')
        specific = self.request.get('specific')
        if database == "":
            redirect = (str(frommachine) + "/" + str(fromapp) + "?action=" + str(action))
        else:
            redirect = (str(frommachine) + "/" + str(fromapp) + "?action=" + str(action) + 
                        "&specific=" + str(specific))
        self.redirect(redirect, permanent=True)
    
class TestPage(webapp.RequestHandler):
  def get(self):
    # controllers.data.TestPageApp(self)
    controllers.research.TestPageApp(self)
 
def main():
  application = webapp.WSGIApplication([
  ('/', ShowData), ('/getdata', GetNewData),
  ('/sortdata', SortData), ('/sendemail', SendEmail),
  ('/getpostcount', GetPostCount), ('/showpostcount', ShowPostCount),  # TODO: look at GetPostCount
  ('/sethierarchy', SetHierarchy), ('/bounce', Bounce),
  ('/testpage', TestPage)], debug=True)  

  run_wsgi_app(application)
  
  
if __name__ == '__main__':
  main()
