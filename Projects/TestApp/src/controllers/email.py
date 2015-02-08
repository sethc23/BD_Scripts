import GAppSendMail

def SendEmailApp(self, to):
  # to = "apallaria1@gmail.com"
  subject = "works!"
  body = "email sent and received"
  email = GAppSendMail.Send(to, subject, body)
  
####--------Receive Email (doesn't work)
# #    username = "seth.t.chase@gmail.com"
# #    inbox = GAppRecieveMail.Recieve(username)
# #    self.response.out.write(inbox)
# #    self.response.out.write("finished-\r\n")
####################################################
