# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.

import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
    assert type(send_to) == list
    assert type(files) == list

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f, "rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    # smtp = smtplib.SMTP(server)
    smtp = smtplib.SMTP()
    smtp.connect('smtp.gmail.com:587')
    smtp.ehlo()
    smtp.starttls()
    smtp.login('seth.t.chase', 'F*rrari1')
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()



# send_mail('seth.t.chase@gmail.com', ['seth.t.chase@gmail.com'], 'NYLJ', 'today', files=['/Users/admin/SERVER2/BD_Scripts/crons/NYLJ/NYLJtuesdayA.pdf'], server="localhost")

'''

# Define these once; use them twice!
strFrom = 'seth.t.chase@gmail.com'
strTo = strFrom

# Create the root message and fill in the from, to, and subject headers
msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = "Today's NYLJ"
msgRoot['From'] = strFrom
msgRoot['To'] = strTo
msgRoot.preamble = 'This is a multi-part message in MIME format.'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

# We reference the image in the IMG SRC attribute by the ID we give it below
msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
msgAlternative.attach(msgText)

# This example assumes the image is in the current directory
#fp = open('/Users/admin/SERVER2/BD_Scripts/crons/NYLJ/NYLJtuesdayA.pdf', 'rb')
#msgImage = MIMEImage(fp.read())
#fp.close()



# Define the image's ID as referenced above
#msgImage.add_header('Content-ID', 'NYLJtuesdayA.pdf')
#msgRoot.attach(msgImage)
'''
'''
strFrom = 'seth.t.chase@gmail.com'
strTo = strFrom

msg = MIMEMultipart()
fp = open("/Users/admin/SERVER2/BD_Scripts/crons/NYLJ/NYLJtuesdayA.pdf", 'rb')
msg.attach(MIMEText(fp.read()))
fp.close()

# Send the email (this example assumes SMTP authentication is required)
import smtplib
smtp = smtplib.SMTP()

smtp.connect('smtp.gmail.com:587')
smtp.ehlo()
smtp.starttls()
smtp.login('seth.t.chase', 'F*rrari1')
smtp.sendmail(strFrom, strTo, msg.as_string())
smtp.quit()
'''
