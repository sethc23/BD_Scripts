from google.appengine.api import mail

def Send(to, subject, body):

    message = mail.EmailMessage(sender="MoneyPress.1@gmail.com")
    message.to = to
    message.subject = subject
    message.body = body

    x = message.check_initialized()
    # print x
    y = message.is_initialized()
    # print y
    z = message.send()
    # print z
    return y
