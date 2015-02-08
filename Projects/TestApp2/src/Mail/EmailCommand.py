import web2email

def send(subject):
    sender = "moneypress.1@gmail.com"
    # account="moneypress.1"
    to = "moneytrain.1000@gmail.com"
    # subject="Test"
    message = " "
    content_type = "text/plain"
    user = "moneypress.1@gmail.com"
    pw = "muchmoney"
    if web2email.mail(send_from=sender,
                            send_to=to,
                            subject=subject,
                            text=message,
                            content_type=content_type,
                            files=[],
                            server="smtp.gmail.com",
                            port=25,
                            username=user,
                            password=pw):
        return "command sent"
    else:
        return "error sending command"

