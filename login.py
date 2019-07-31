import webapp2

# from google.appengine.api import users
from google.appengine.ext import ndb

class User(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  email = ndb.StringProperty()
  color = ndb.StringProperty()
  # add colors

class Family (ndb.Model):
    members= ndb.KeyProperty(User, repeated=True)

class Event (ndb.Model):
    owner = ndb.KeyProperty(User)
    # maybe fix
class ToDo(ndb.Model):
    owner=ndb.KeyProperty(User)
    task=ndb.StringProperty()
