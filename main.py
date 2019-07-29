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
        calendar_template= the_jinja_env.get_template('/calendar.html')
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
    profile_template= the_jinja_env.get_template('profile.html')
    #self.response.write('Thanks for signing up, %s! <br><a href="/">Home</a>' %
        #cssi_user.first_name)
    self.response.write(profile_template.render())

class Calendar(webapp2.RequestHandler):
    def get(self):
        self.response.write('hello')

class Profile(webapp2.RequestHandler):
    def get(self):
        self.response.write('hello')


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/calendar', Calendar),
  ('/profile', Profile),
], debug=True)
