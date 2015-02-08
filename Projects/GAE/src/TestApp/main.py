
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
import controllers

_DEBUG = True  # Set to true if we want to have our webapp print stack traces

class GetNewData(webapp.RequestHandler):  ######----Get and Put Data into Datastore
  def get(self):
    controllers.data.GetDataApp(self)

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

class PostCount(webapp.RequestHandler):
  def get(self):
    controllers.research.PostCountApp(self)

class SendEmail(webapp.RequestHandler):
  def get(self):
    controllers.email.SendEmailApp(self)
    
class TestPage(webapp.RequestHandler):
  def get(self):
    controllers.data.TestPageApp(self)
 
def main():
  application = webapp.WSGIApplication([
  ('/', ShowData), ('/getdata', GetNewData), ('/testpage', TestPage),
  ('/sortdata', SortData), ('/sendemail', SendEmail),
  ('/countdata', GetPostCount), ('/countdata', PostCount)], debug=True)  

  run_wsgi_app(application)
  
  
if __name__ == '__main__':
  main()
