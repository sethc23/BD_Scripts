##################################################
# eBay.py
# Python wrapper classes for eBay API.
# API calls implemented by this module:
#  - GeteBayOfficialTime
#  - GetSearchResults
#  - GetUser
#  - GetCategories (heavy call only)
#  - AddItem
#  - GetSellerList (one page of 200 items max only)
#  - GetFinanceOffers (works in production, not in sandbox)
#  - ValidateTestUserRegistration
#  - GetFeedback
#  - GetToken (works in sandbox, not in production)
#
# Calls on the to-do list:
#  - GetCategory2FinanceOffer
#  - RelistItem, VerifyAddItem
#  - GetSellerEvents
#  - AddToItemDescription
#  - ReviseItem
#  - GetItem
#  - GetItemTransactions
#  - GetSellerTransactions
#  - GetHighBidders, GetBidderList
#  - GetCategoryListings
#  - AddSecondChanceItem, VerifySecondChanceItem
#  - GetAccount
#  - LeaveFeedback
#  - GetCategory2CS, GetAttributesCS, GetAttributesXSL
#  - GetProductSearchPage, GetProductFinder, GetProductFinderXSL
#  - GetProductSearchResults, GetProductFamilyMembers, GetProductSellingPages
#  - FetchToken
##################################################

import httplib, ConfigParser, urlparse
from xml.dom.minidom import parse, parseString


########## Session
class Session:
    # Plug the following values into ebay.ini (not here)
    Developer = "7e2484e2-f568-4558-a4a8-d90cd37067ac"
    Application = "SansPape-5f33-4902-a9fc-953dfc895c66"
    Certificate = "073072fd-1022-4a6e-92d3-2e16961d53ad"
    Token = "AgAAAA**AQAAAA**aAAAAA**QoUqUA**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wGmIGpDJOHpwWdj6x9nY+seQ**aZIBAA**AAMAAA**cYRy0XJ/4+wEG93cu1wTBeSjTeu3FD0H5TeCcRBGr1nFVXNbnoABpePZSlx0InuIOF1A5ZZ/D9xiXOErM+dLVzmWpkc9wXCBsLmY+uIgOdbIb8l0zvw8d05xoO5Y2kOhJxbZWpPvv5JCs+mop7E3nlqXOOY+kXNWNXw1DpcO1HmFjg97Az7GUV9xzxTCQ9/ViT/SZH3D41e0WkKEi0SJ69r8NMs+EAG/JG+Me/6pzGlbNXGkXUtrhVHSD+TueUSnSo8cXFGiv3F15ELTzKU0UoV0KOVhvs1uyT81vkg3sMZNccOLXoqfLY5Puw2Ra0GzY+rB4XaOf7H6E8WV7mw/e5Xr7vo/6wLEcBlPP0z+ACMFA00s3RcN30aN/0Dlberz+uwbpFOvFn7Bvqihg26WXJJOCH1JFs6DaKxmJ1zUPSB5OLJlq30VOzwo0caGFSxhvR0romXwLTvh7POD5zG5QZh7pY5Tf4w4F/vGm+SGCYJETZq/UM9N6ek8eP5xToKDcBcxHGjaDvH3r0rYwO02Nvn32m2ecDYK7ErGc0HuTg8CjCg3gJxGSL2H753ij3tQ7NeLmU1blcD6wcCAbvRqn2eJNVqJxWNVQCKdpdTGS2nZHviT9HyZLjj4ruLH4WhnPmvBzTn3YeUvlIik9JF2xdPpg4ieVUF0AjaPY/yjI+5s/9Namh/wxNEUnew/v/+mW0pNY2VDUKkCYnpdkkIcxmiRoMa9AvmOFsv5Y3qJ32HHCdCfa9nq5NPlxu1FDNE2"
    ServerURL = "https://api.sandbox.ebay.com/ws/api.dll"
    
    def Initialize(self):
        config = ConfigParser.ConfigParser()
        config.read("ebay.ini")
        self.Developer = config.get("Developer Keys", "Developer")
        self.Application = config.get("Developer Keys", "Application")
        self.Certificate = config.get("Developer Keys", "Certificate")
        self.Token = config.get("Authentication", "Token")
        self.ServerURL = config.get("Server", "URL")
        urldat = urlparse.urlparse(self.ServerURL)
        self.Server = urldat[1]  # e.g., api.sandbox.ebay.com
        self.Command = urldat[2]  # e.g., /ws/api.dll

########## REST Token retrieval
class RESTToken:
    """ Retrieves a REST token when a conventional token is available.
    Getting a REST token in this way has the advantage of (cough) not invalidating a conventional token if you have one. """
    Session = Session()
    
    def __init__(self):
        self.Session.Initialize()
        
    def Get(self):
        api = Call()
        api.Session = self.Session
        api.DetailLevel = "128"
        api.RequestData = """<?xml version='1.0' encoding='iso-8859-1'?>
<request>
    <RequestToken>%(token)s</RequestToken>
    <DetailLevel>%(detail)s</DetailLevel>
    <ErrorLevel>1</ErrorLevel>
    <SiteId>0</SiteId>
    <Verb>GetUser</Verb>
    <UserId></UserId>
</request>"""
        api.RequestData = api.RequestData % { 'token': self.Session.Token,
                                              'detail': api.DetailLevel}
        self.Xml = api.MakeCall("GetUser")
        self.Token = self.Xml.getElementsByTagName('RestToken')[0].childNodes[0].data
        
    def Save(self, filename):
        # TODO: If Xml property is blank then it's an exception
        if self.Xml != "":
            f = open(filename, 'w')
            s = self.Token
            f.write(s)
            f.close()

########## Feedback
class Feedback:
    Session = Session()
    
    def __init__(self):
        self.Session.Initialize()
        
    def Get(self, UserID):
        api = Call()
        api.Session = self.Session
        api.DetailLevel = "1"
        api.RequestData = """<?xml version='1.0' encoding='iso-8859-1'?>
<request>
    <RequestToken>%(token)s</RequestToken>
    <DetailLevel>%(detail)s</DetailLevel>
    <ErrorLevel>1</ErrorLevel>
    <SiteId>0</SiteId>
    <Verb>GetFeedback</Verb>
    <UserId>%(userid)s</UserId>
</request>"""
        api.RequestData = api.RequestData % { 'token': self.Session.Token,
                                              'detail': api.DetailLevel,
                                              'userid': UserID }
        self.Xml = api.MakeCall("GetFeedback")
        self.UserID = UserID
        # TODO: Parse into FeedbackDetail objects
        
    def Save(self, filename):
        # TODO: If Xml property is blank then it's an exception
        if self.Xml != "":
            f = open(filename, 'w')
            s = self.Xml.toprettyxml().encode('utf-8')
            f.write(s)
            f.close()        


########## Finance Offers
class FinanceOffers:
    Session = Session()
    
    def __init__(self):
        self.Session.Initialize()
        
    def Get(self):
        api = Call()
        api.Session = self.Session
        api.DetailLevel = "1"
        api.RequestData = """<?xml version='1.0' encoding='iso-8859-1'?>
<request>
    <RequestToken>%(token)s</RequestToken>
    <DetailLevel>%(detail)s</DetailLevel>
    <ErrorLevel>1</ErrorLevel>
    <SiteId>0</SiteId>
    <Verb>GetFinanceOffers</Verb>
    <LastModifiedDate>2004-01-01 12:00:00</LastModifiedDate>
</request>"""
        api.RequestData = api.RequestData % { 'token': self.Session.Token,
                                              'detail': api.DetailLevel }
        self.Xml = api.MakeCall("GetFinanceOffers")
        
        # TODO: Populate this dictionary with data from the xml
        self.Offers = dict()
        self.Offers['6060842'] = 'Im waiting for you'

    def Save(self, filename):
        # TODO: If Xml property is blank then it's an exception
        if self.Xml != "":
            f = open(filename, 'w')
            s = self.Xml.toprettyxml().encode('utf-8')
            f.write(s)
            f.close()

class FinanceOffer:
    # TODO: Assign XML to object and have it parse out all the data
    # TODO: Strip out stupid stupid HTML formatting from seller/buyer terms
    Xml = "<xml />"
    SellerTerms = ""
    BuyerTerms = ""
    Priority = 0
    StartDate = "1900-01-01 1:01:00"
    MinimumAmount = 0
    RateFactor = 0.00
    LastModifiedDate = "1900-01-01 1:01:00"

########## GetToken
class Token:
    Session = Session()
    
    def __init__(self):
        self.Session.Initialize()
        self.RequestUserId = 'USER_ID'
        self.RequestPassword = 'PASSWORD'
        
    def Get(self):
        api = Call()
        api.Session = self.Session
        api.DetailLevel = "0" 
        api.RequestData = """<?xml version='1.0' encoding='iso-8859-1'?>
<request>
    <RequestToken></RequestToken>
    <RequestUserId>%(userid)s</RequestUserId>
    <RequestPassword>%(password)s</RequestPassword>    
    <DetailLevel>%(detail)s</DetailLevel>
    <ErrorLevel>1</ErrorLevel>
    <SiteId>0</SiteId>
    <Verb>GetToken</Verb>
</request>"""
        api.RequestData = api.RequestData % { 'detail': api.DetailLevel,
                                              'userid': self.RequestUserId,
                                              'password': self.RequestPassword}
        print api.RequestData
        self.Xml = api.MakeCall("GetToken")
    

########## SellerList
class SellerList:
    Session = Session()
    
    def __init__(self):
        self.Session.Initialize()
        
    def Get(self, SellerUserName):
        api = Call()
        api.Session = self.Session
        api.DetailLevel = "2"  # 16 is minimal data but returns all IDs
        api.RequestData = """<?xml version='1.0' encoding='iso-8859-1'?>
<request>
    <RequestToken>%(token)s</RequestToken>
    <DetailLevel>%(detail)s</DetailLevel>
    <ErrorLevel>1</ErrorLevel>
    <SiteId>0</SiteId>
    <Verb>GetSellerList</Verb>
    <ItemsPerPage>200</ItemsPerPage>
    <PageNumber>1</PageNumber>
    <StartTimeFrom>2004-01-01</StartTimeFrom>
    <StartTimeTo>2004-12-31</StartTimeTo>
</request>"""
        api.RequestData = api.RequestData % { 'token': self.Session.Token,
                                              'detail': api.DetailLevel }
        self.Xml = api.MakeCall("GetSellerList")


########## Item
class Item:
    # TODO: Implement finance offers by:
    #   1) Downloading all offers using GetFinanceOffers
    #   2) Seeing which offers are available for a category using GetCategory2FinanceOffer (always use detail level 1 for this)
    #   3) Assigning a chosen finance offer by assigning its ID to the item's <FinanceOfferId> node
    Session = Session()
    Category = "14111"  # eBay Test topic
    Country = "us"  # TODO: Enumerate/validate country table as found in http://developer.ebay.com/DevZone/docs/API_Doc/Appendixes/AppendixL.htm
    Currency = "1"  # TODO: Since currency is a function of site ID, it should be possible to auto-map between siteIDs and currency IDs (see http://developer.ebay.com/DevZone/docs/API_Doc/Functions/Tables/CurrencyIdTable.htm)
    Description = "This auction was listed with pyeBay."
    Duration = "7"  # TODO: Provide validation (auctions can be 1, 3, 5, 7, 10 etc.)
    Location = "A town near you"
    MinimumBid = "0.99"
    PayPalEmailAddress = "jeffreyp@well.com"  # TODO: If no PP address provided, set PayPalAccepted to 0
    Quantity = "1"
    Region = "60"  # TODO: Enumerate/validate region codes *or* provide for download and lookup of region tables using GeteBayDetails call
    Title = "My Listing Created by pyeBay"
    
    def __init__(self):
        pass
        # self.Session.Initialize()   # must init an Item object manually at least for now

    def Add(self):
        api = Call()
        api.Session = self.Session
        api.RequestData = """<?xml version='1.0' encoding='iso-8859-1'?>
<request>
    <RequestToken>%(token)s</RequestToken>
    <DetailLevel>0</DetailLevel>
    <ErrorLevel>1</ErrorLevel>
    <SiteId>0</SiteId>
    <Verb>AddItem</Verb>
    <Category>%(category)s</Category>
    <CheckoutDetailsSpecified>0</CheckoutDetailsSpecified>
    <Country>%(country)s</Country>
    <Currency>%(currency)s</Currency>
    <Description>%(description)s</Description>
    <Duration>%(duration)s</Duration>
    <Location>%(location)s</Location>
    <MinimumBid>%(minimumbid)s</MinimumBid>
    <PayPalAccepted>1</PayPalAccepted>
    <PayPalEmailAddress>%(paypaladdress)s</PayPalEmailAddress>
    <Quantity>%(quantity)s</Quantity>
    <Region>%(region)s</Region>
    <Title>%(title)s</Title>
</request>""" 
        api.RequestData = api.RequestData % { 'token': self.Session.Token,
                                              'category': self.Category,
                                              'country': self.Country,
                                              'currency': self.Currency,
                                              'description': self.Description,
                                              'duration': self.Duration,
                                              'location': self.Location,
                                              'minimumbid': self.MinimumBid,
                                              'paypaladdress': self.PayPalEmailAddress,
                                              'quantity': self.Quantity,
                                              'region': self.Region,
                                              'title': self.Title }
        self.Xml = api.MakeCall("AddItem")
        self.ID = self.Xml.getElementsByTagName('Id')[0].childNodes[0].data
        self.ListingFee = self.Xml.getElementsByTagName('ListingFee')[0].childNodes[0].data
        # TODO: Make this do the right thing for production as well
        self.URL = "http://cgi.sandbox.ebay.com/ws/eBayISAPI.dll?ViewItem&item=" + self.ID
        
    def Dispose(self):
        self.Xml.unlink()
        

########## Categories

class Categories:
    Session = Session()
    
    def __init__(self):
        self.Session.Initialize()
    
    # TODO: Need to add the lightweight version of this call 
    # (detail level 0) to check version only -- maybe call it GetVersion()
    def Get(self):
        api = Call()
        api.Session = self.Session
        api.DetailLevel = "1"
        api.RequestData = """<?xml version='1.0' encoding='iso-8859-1'?>
<request>
    <RequestToken>%(token)s</RequestToken>
    <DetailLevel>%(detail)s</DetailLevel>
    <ErrorLevel>1</ErrorLevel>
    <SiteId>0</SiteId>
    <Verb>GetCategories</Verb>
    <ViewAllNodes>1</ViewAllNodes>
</request>"""
        api.RequestData = api.RequestData % { 'token': self.Session.Token,
                                              'detail': api.DetailLevel }
        self.Xml = api.MakeCall("GetCategories")

    def Save(self, filename):
        # TODO: If Xml property is blank then it's an exception
        if self.Xml != "":
            f = open(filename, 'w')
            s = self.Xml.toprettyxml().encode('utf-8')
            f.write(s)
            f.close()
    
    def Dispose(self):
        self.Xml.unlink()
        
        
########## User

class User:
    Session = Session()
    ID = ""
    
    def __init__(self):
        self.Session.Initialize()
        
    def Get(self):
        api = Call()
        api.Session = self.Session
        api.RequestData = """<?xml version='1.0' encoding='iso-8859-1'?>
<request>
   <RequestToken>%(token)s</RequestToken>
   <ErrorLevel>1</ErrorLevel>
   <DetailLevel>%(detail)s</DetailLevel>
   <Verb>GetUser</Verb>
   <SiteId>0</SiteId>
   <UserId>%(userid)s</UserId>
</request>"""
        api.RequestData = api.RequestData % { 'userid': self.ID,
                                              'token': self.Session.Token,
                                              'detail': api.DetailLevel }
        
        self.Xml = api.MakeCall("GetUser")
        # TODO: Map more of the XML to properties of the object
        self.Feedback = self.Xml.getElementsByTagName('Score')[0].childNodes[0].data

    def Validate(self):
        # maps to ValidateTestUserRegistration
        api = Call()
        api.Session = self.Session
        api.RequestData = """<?xml version='1.0' encoding='iso-8859-1'?>
<request>
   <RequestToken>%(token)s</RequestToken>
   <ErrorLevel>1</ErrorLevel>
   <DetailLevel>0</DetailLevel>
   <Verb>ValidateTestUserRegistration</Verb>
   <SiteId>0</SiteId>
</request>"""
        api.RequestData = api.RequestData % { 'token': self.Session.Token }  
        self.Xml = api.MakeCall("ValidateTestUserRegistration")  
        
    def Dispose(self):
        self.Xml.unlink()
    

########## Search

class Search:
    Session = Session()
    DetailLevel = "0"
    Query = ""
    
    def __init__(self):
        self.Session.Initialize()

    
    def Get(self, Query):
        # TODO: Change this so it returns a list of
        # Item objects (instead of raw xml)
        api = Call()
        api.Session = self.Session
        api.RequestData = """<?xml version='1.0' encoding='iso-8859-1'?>
<request>
    <RequestToken>%(token)s</RequestToken>
    <ErrorLevel>1</ErrorLevel>
    <DetailLevel>%(detail)s</DetailLevel>
    <Query>%(query)s</Query>
    <Verb>GetSearchResults</Verb>
    <SiteId>0</SiteId>
</request>"""
        api.RequestData = api.RequestData % { 'query': Query,
                                              'token': self.Session.Token,
                                              'detail': api.DetailLevel }
        print api.RequestData                                              
        self.Xml = api.MakeCall("GetSearchResults")

    def Dispose(self):
        self.Xml.unlink()
        

########## GeteBayOfficialTime

class eBayTime:
    Session = Session()
    
    def __init__(self):
        self.Session.Initialize()
    
    def Get(self):   
        api = Call()
        api.Session = self.Session
        api.RequestData = """<?xml version='1.0' encoding='iso-8859-1'?>
<request>
    <RequestToken>%(token)s</RequestToken>
    <ErrorLevel>1</ErrorLevel>
    <DetailLevel>0</DetailLevel>
    <Verb>GeteBayOfficialTime</Verb>
    <SiteId>0</SiteId>
</request>"""
        api.RequestData = api.RequestData % { 'token': self.Session.Token,
                                              'detail': api.DetailLevel }

        responseDOM = api.MakeCall("GeteBayOfficialTime")
         
        # check for the <EBayTime> tag and return results
        timeElement = responseDOM.getElementsByTagName('EBayTime')
        if (timeElement != []):
            return timeElement[0].childNodes[0].data
         
        # force garbage collection of the DOM object
        responseDOM.unlink()

########## Call        

class Call:
    RequestData = "<xml />"  # just a stub
    DetailLevel = "0"
    SiteID = "0"
    
    def MakeCall(self, CallName):
        # specify the connection to the eBay Sandbox environment
        # TODO: Make this configurable in eBay.ini (sandbox/production)
        conn = httplib.HTTPSConnection(self.Session.Server)

        # specify a POST with the results of generateHeaders and generateRequest
        conn.request("POST", self.Session.Command, self.RequestData, self.GenerateHeaders(self.Session, CallName))
        response = conn.getresponse()
        
        # TODO: When you add logging to this, change the
        # following to log statements
        # print "Response status:", response.status
        # print "Response reason:", response.reason
        
        # store the response data and close the connection
        data = response.read()
        conn.close()
        
        responseDOM = parseString(data)
        
        # check for any <Error> tags and print
        # TODO: Return a real exception and log when this happens
        tag = responseDOM.getElementsByTagName('Error')
        if (tag.count != 0):
            for error in tag:
                print "\n", error.toprettyxml("  ")
                
        return responseDOM
        
    def GenerateHeaders(self, Session, CallName):
        headers = {"X-EBAY-API-COMPATIBILITY-LEVEL": "349",
                   "X-EBAY-API-SESSION-CERTIFICATE": Session.Developer + ";" + Session.Application + ";" + Session.Certificate,
                   "X-EBAY-API-DEV-NAME": Session.Developer,
                   "X-EBAY-API-APP-NAME": Session.Application,
                   "X-EBAY-API-CERT-NAME": Session.Certificate,
                   "X-EBAY-API-CALL-NAME": CallName,
                   "X-EBAY-API-SITEID": self.SiteID,
                   "X-EBAY-API-DETAIL-LEVEL": self.DetailLevel,
                   "Content-Type": "text/xml"}
        return headers
