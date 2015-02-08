from google.appengine.ext import db
import newDB

q = newDB.CLposts.all()
a = q.fetch(1)

w = newDB.Locations.all()
b = w.fetch(1)

p = newDB.Categories.all()
c = p.fetch(1)

print a[0].Locations.location
print b[0].location

print a[0].category.name
print b[0].category.name

print b[0].category.title
print c[0].title

print a[0].category.title
print b[0].category.title

####--------------------------------
# #  RESULT
"""
boston
boston
wanted
wanted
Double Jogger wanted -
Double Jogger wanted -
Double Jogger wanted -
Double Jogger wanted -
"""
####--------------------------------
