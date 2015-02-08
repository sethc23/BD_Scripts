import imaplib
import email


def Recieve(username):
    c = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    if username is "seth.t.chase@gmail.com":
        c.login(username, 'F*rrari1')
    if username is "moneypress.1@gmail.com" or username is "moneytrain.1000@gmail.com":
        c.login(username, 'muchmoney')
    inbox = []
    try:
        status, msgs = c.select('INBOX', readonly=True)
        # print msgs[0]
        for msg in range(1, int(msgs[0]) + 1):
            typ, msg_data = c.fetch(msg, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    for header in [ 'date', 'from', 'subject']:
                        inbox.append('%s -:-' % (msg[header]))

                    # for header in [ 'subject', 'to', 'from' ]:
                     #   print '%-8s: %s' % (header.upper(), msg[header])

    finally:
        try:
            c.close()
        except:
            pass
        c.logout()
        return inbox
