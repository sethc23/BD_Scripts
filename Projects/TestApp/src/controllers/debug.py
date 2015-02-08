from google.appengine.ext import db
from controllers.DBclasses import *
import getData
import pdb

_DEBUG = True


def getData():
    url = "http://geo.craigslist.org/iso/us"
    city = "boston"
    top_category = "for sale"
    sub_category = "wanted"
    sendVariables = url, city, top_category, sub_category
    pdb.set_trace()
    # pdb.run('getData.PostData(sendVariables)')
    result1 = getData.PostData(url, city, top_category, sub_category)
