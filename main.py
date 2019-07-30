import webapp2
import jinja2
import os
from google.appengine.api import users
from login import CssiUser
import urllib

the_jinja_env= jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      signout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/'))
      email_address = user.nickname()
      cssi_user = CssiUser.query().filter(CssiUser.email == email_address).get()
      if cssi_user:
        self.response.write(signout_link_html)
        calendar_template= the_jinja_env.get_template('templates/calendar.html')
        first_name=cssi_user.first_name
        calendar_dict={
        "first_name":first_name
        }
        self.response.write(calendar_template.render(calendar_dict))
      else:
        self.response.write('''
            Welcome to our site, %s!  Please sign up! <br>
            <form method="post" action="/">
            First Name: <input type="text" name="first_name">
            Last Name: <input type="text" name="last_name">
            <input type="submit">
            </form><br> %s <br>
            ''' % (email_address, signout_link_html))
    else:
      login_url = users.create_login_url('/')
      login_html_element = '<a href="%s">Sign in</a>' % login_url
      self.response.write('Please log in.<br>' + login_html_element)


  def post(self):
    user = users.get_current_user()
    cssi_user = CssiUser(
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        email=user.nickname())
    cssi_user.put()
    profile_template= the_jinja_env.get_template('templates/profile.html')
    profile_dict={
    "last_name": cssi_user.last_name
    }
    self.response.write(profile_template.render(profile_dict))

class Calendar(webapp2.RequestHandler):
    def get(self):
        calendar_template=the_jinja_env.get_template('templates/calendar.html')
        self.response.write(calendar_template.render())
    def post(self):
        calendar_template=the_jinja_env.get_template('templates/calendar.html')
        user=users.get_current_user()
        self.response.write(calendar_template.render())

class Profile(webapp2.RequestHandler):
    def get(self):
        user1 = users.get_current_user().nickname()
        user = CssiUser.query().filter(CssiUser.email== user1).get()
        last_name=user.get_current_user().last_name()
        profile_template= the_jinja_env.get_template('templates/profile.html')
        profile_dict={
        "last_name": last_name,
        }
        self.response.write(profile_template.render(profile_dict))

    def post(self):
        cssi_user = CssiUser(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            email=user.nickname())
        cssi_user.put()
        profile_template= the_jinja_env.get_template('templates/profile.html')
        profile_dict={
        "last_name": cssi_user.last_name
        }
        self.response.write(profile_template.render(profile_dict))

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/calendar', Calendar),
  ('/profile', Profile),
], debug=True)
