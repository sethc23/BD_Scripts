from google.appengine.ext import db
import logging
import hashlib
import math

class UserInfo(db.Model):
  user = db.UserProperty(required=True)


class Mapping(db.Model):
  site = db.StringProperty()
  category = db.StringProperty()
  title = db.StringProperty()
  link = db.StringProperty()
  created = db.DateTimeProperty(auto_now_add=True)

  @classmethod
  def get_key_name(cls, user, host):
    return "_" + hashlib.sha1("%s@%s" % (user, host)).hexdigest()

  @classmethod
  def get_by_address(cls, user, host):
    return cls.get_by_key_name(cls.get_key_name(user, host))
  
  def get_name(self):
    if self.user:
      return "%s@%s" % (self.user, self.host)
    else:
      return self.host


class SmtpServer(db.Model):
  hostname = db.StringProperty(required=True)
  # The name to display in the list of MXen.
  mxname = db.StringProperty(required=True)
  secret_key = db.TextProperty(required=True)


class LogEntry(db.Model):
  mapping = db.ReferenceProperty(Mapping, required=True)
  server = db.ReferenceProperty(SmtpServer, required=True)
  ts = db.DateTimeProperty(required=True, auto_now_add=True)
  sender = db.EmailProperty(required=True)
  recipient = db.EmailProperty(required=True)
  length = db.IntegerProperty(required=True)
  message = db.TextProperty()
  is_error = db.BooleanProperty(required=True, default=False)
  is_warning = db.BooleanProperty(required=True, default=False)

  def human_size(self):
    return "%d kb" % math.ceil(self.length / 1024.0)
