from google.appengine.ext import webapp
import email
 
class EmailHandler(webapp.RequestHandler):
  def post(self):
    sender = self.request.GET.get("from", "")
    recipient = self.request.GET.get("to", "")
    message = email.message_from_string(self.request.body)
    # Do stuff with the email message
