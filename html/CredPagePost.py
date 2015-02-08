 #!/usr/bin/env python 
import urllib 
import httplib2
from httplib2 import Http

formhead = """<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Quick HTML Form</title>
<style type="text/css">
<!--.style1 {
	font-size: 12px;
	font-style: italic;
            }-->
</style>
</head>
<body>"""

formbody = """
<form name="listing" method="post" action="HTMLAction.cfm">
<input name="image" type="text" id="image" size="63"/>
<input name="unit" type="text" id="unit" size="10"/>
<input name="street" type="text" id="address3" size="63"/>
<input name="city" type="text" id="address4" size="63" />
<input name="state" type="text" id="address5" size="4" maxlength="2" />
<input name="price" type="text" id="state8" size="10" maxlength="15" />
<input name="bed" type="text" id="zip6" size="10" maxlength="15" />
<input name="bath" type="text" id="bath" size="10" maxlength="15" />
<input name="footage" type="text" id="state7" size="10" maxlength="15" />
<input name="parking" type="text" id="zip5" size="63" />
<input name="pets" type="text" id="state6" size="63" />
<input name="deposit" type="text" id="deposit" size="63" />
<textarea name="title" cols="60" rows="3" id="title"></textarea>
<textarea name="geograph" cols="60" rows="7" id="geograph"></textarea>
<textarea name="description" cols="60" rows="7" id="description"></textarea>
<input name="pic1" type="text" id="pic1" size="63" />
<input name="pic2" type="text" id="image3" size="63" />
<input name="pic3" type="text" id="image4" size="63" />
<input name="pic4" type="text" id="image5" size="63" />
<input name="pic5" type="text" id="image6" size="63" />
<input name="pic6" type="text" id="image7" size="63" />
<input name="pic7" type="text" id="image13" size="63" />
input name="pic8" type="text" id="image12" size="63" />
<input name="pic9" type="text" id="image11" size="63" />
<input name="pic10" type="text" id="image10" size="63" />
<input name="pic11" type="text" id="image9" size="63" />
<input name="pic12" type="text" id="image8" size="63" />
<input name="pic13" type="text" id="image19" size="63" />
<input name="pic14" type="text" id="image18" size="63" />
<input name="pic15" type="text" id="image17" size="63" />
<input name="pic16" type="text" id="image16" size="63" />
<input name="pic17" type="text" id="image15" size="63" />
<input name="pic18" type="text" id="image14" size="63" />
<input name="submit" type="submit" id="submit" value="Create Listing" />
<input name="reset" type="reset" id="reset" value="Clear Form" />
</form>"""

formfoot = "</body></html>"

postURL = formhead + formbody + formfoot
# print postURL
# print "break"


http = httplib2.Http() 
url = 'http://credentials.designforeman.com/HTML%20Form/HTMLForm.cfm'
# body = {'USERNAME': 'foo','PASSWORD': 'bar'}
# headers = {'Content-type': 'application/x-www-form-urlencoded'}
h = Http()
resp, content = h.request(url, "POST", postURL)

resp
{'status': '200', 'transfer-encoding': 'chunked', 'vary': 'Accept-Encoding,User-Agent',
 'server': 'Apache', 'connection': 'close', 'date': 'Tue, 31 Jul 2007 15:29:52 GMT',
 'content-type': 'text/html'}

content = http.request(url, 'POST')
print content
# goodContent=resp.urllib2.urlopen(content)
goodContent = resp.urllib2.urlopen(content)
print goodContent
