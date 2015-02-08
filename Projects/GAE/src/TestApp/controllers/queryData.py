from google.appengine.ext import db
from controllers.DBclasses import *

_DEBUG = True

def sendData(site, category, titles, links, postId, postDate, postNumber):
    try:
        line = "Start-"
        for i in range(0, postNumber):  # len(titles)):
            line = line + "entry-"
            sub_entry = Categories()
            line = line + " value: " + site
            sub_entry.location = str(site)
            line = line + " value: " + category
            sub_entry.name = str(category)
            line = line + " value: " + titles[i]
            sub_entry.title = str(titles[i])
            line = line + " value: " + links[i]
            sub_entry.link = str(links[i])
            line = line + " values: " + postId[i] + ' - ' + str(int(postId[i]))
            sub_entry.postId = int(postId[i])
            line = line + " values: " + postDate[i] + ' - ' + str(int(postDate[i]))
            sub_entry.postDate = int(postDate[i])
            try:
                line = line + "put-sub"
                sub_entry.put()
                # line = line+"put-entry"
                # entry = Locations(location=site,category=sub_entry.key())
                # entry.put()
                # line = line+"put-top"
                # top_entry = CLposts(location=entry.key(),category=sub_entry.key())
                # top_entry.put()
            except:
                line = line + "encode-"
                text = titles[i].encode('ASCII', 'elinks')
                line = line + "entry-"
                sub_entry = Categories()
                line = line + " value: " + site
                sub_entry.location = str(site)
                line = line + " value: " + category
                sub_entry.name = str(category)
                line = line + " value: " + titles[i]
                sub_entry.title = str(titles[i])
                line = line + " value: " + links[i]
                sub_entry.link = str(links[i])
                line = line + " values: " + postId[i] + ' - ' + str(int(postId[i]))
                sub_entry.postId = int(postId[i])
                line = line + " values: " + postDate[i] + ' - ' + str(int(postDate[i]))
                sub_entry.postDate = int(postDate[i])
                line = line + "put-sub"
                sub_entry.put()
                # line = line+"put-entry"
                # entry = Locations(location=site,category=sub_entry.key())
                # entry.put()
                # line = line+"put-top"
                # top_entry = CLposts(location=entry.key(),category=sub_entry.key())
                # top_entry.put()
            line = line + "iteration-"
        line = "end"
        return "success"
    except:
        receivedData = site, category, titles, links, postId, postDate, postNumber
        line = str(receivedData) + "    ----    " + line
        return "sendData failure: " + line

def checkQueryPosts(postId):
    repeatPosts = []
    if len(postId) == 0:
        return repeatPosts
    else:
        oldpostId = postId[:]
        newpostId = postId[:]
        newpostId.sort()
        small = eval(newpostId[0])
        big = eval(newpostId[len(newpostId) - 1])
        postIdQuery = Categories.gql("WHERE postId >= :1 AND postId <= :2 ORDER BY postId DESC", small, big)
        try:
            x = postIdQuery.get()
        except:
            return repeatPosts
        if postIdQuery.count() == 0:
            return repeatPosts
        postQlist = list(post.postId for post in postIdQuery)
        # print "postQlist[0] is ",postQlist[0]," is type ",str(type(str(postQlist[0])))
        # print "oldpostId[0] is ",oldpostId[0]," is type ",str(type(long(oldpostId[0])))
        for i in range(0, len(oldpostId)):
            try:
                a = postQlist.index(long(oldpostId[i]))
                repeatPosts.append(str(postQlist[a]))
            except ValueError:
                pass
        # print len(repeatPosts)
        return repeatPosts
