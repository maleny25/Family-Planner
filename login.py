import webapp2

# from google.appengine.api import users
from google.appengine.ext import ndb

class User(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  email = ndb.StringProperty()

class Family (ndb.Model):
    members= ndb.KeyProperty(User, repeated=True)
