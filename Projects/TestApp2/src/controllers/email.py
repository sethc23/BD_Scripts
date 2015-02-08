import GAppSendMail

def SendEmailApp(self, to):
  subject = "works!"
  body = "body here"
  email = GAppSendMail.Send(to, subject, body)
  
####--------Receive Email (doesn't work)
# #    username = "seth.t.chase@gmail.com"
# #    inbox = GAppRecieveMail.Recieve(username)
# #    self.response.out.write(inbox)
# #    self.response.out.write("finished-\r\n")
####################################################
