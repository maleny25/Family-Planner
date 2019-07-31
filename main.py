import webapp2
import jinja2
import os
from google.appengine.api import users
from login import User
from login import Family
import time

the_jinja_env= jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def load_family_by_email (email):
    current_user=User.query().filter(User.email==email).fetch()[0]
    family = Family.query(Family.members ==current_user.key).fetch()[0]
    return family




class MainHandler(webapp2.RequestHandler):
  def get(self):
    colors=["Pink", "Purple", "Red", "Green", "Orange", "Gray","Yellow"]
    current_user = users.get_current_user()
    if current_user:
      signout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/'))
      email_address = current_user.email()
      user = User.query().filter(User.email == email_address).get()
      if user:
        self.redirect("/calendar")
        # self.response.write(signout_link_html)
        # calendar_template= the_jinja_env.get_template('templates/calendar.html')
        # first_name=user.first_name
        # family= load_family_by_email(users.get_current_user().email())
        # calendar_dict={
        # "first_name":first_name,
        # "family": family
        # }

        # self.response.write(calendar_template.render(calendar_dict))
      else:
        user_color=""
        for color in colors:
            user_color+='<option value="'+color+'">'+color+'</option>'
        self.response.write('''
            Welcome to our site, %s!  Please sign up! <br>
            <form method="post" action="/profile">
            First Name: <input type="text" name="first_name"> <br>
            Last Name: <input type="text" name="last_name"> <br>
            <input type="submit">
            </form><br> %s <br>
            ''' % (email_address, signout_link_html))

    else:
      login_url = users.create_login_url('/')
      login_html_element = '<a href="%s">Sign in</a>' % login_url
      self.response.write('Please log in.<br>' + login_html_element)


  def post(self):
    current_user = users.get_current_user()
    result=User.query().filter(User.email==current_user.email()).fetch()
    user_color="Blue"
    #if result:
        #user_color=result[0].color()
    user = User(
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        email=current_user.email(),
        color=user_color)
    user_key=user.put()
    family=Family(
        members=[user_key]
    )
    family.put()
    profile_template= the_jinja_env.get_template('templates/profile.html')
    profile_dict={
    "last_name": user.last_name,
    "family":family
    }
    self.response.write(profile_template.render(profile_dict))

class Calendar(webapp2.RequestHandler):
    def get(self):
        signout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/'))
        self.response.write(signout_link_html)
        calendar_template=the_jinja_env.get_template('templates/calendar.html')
        user=users.get_current_user()
        signout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/'))
        family= load_family_by_email(users.get_current_user().email())
        calendar_dict={
        "family": family,
        }
        self.response.write(calendar_template.render(calendar_dict))
        # self.response.write(signout_link_html)
        # self.response.write(calendar_template.render())
    def post(self):
        calendar_template=the_jinja_env.get_template('templates/calendar.html')
        user=users.get_current_user()
        signout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/'))
        family= load_family_by_email(users.get_current_user().email())
        calendar_dict={
        "family": family,
        }
        self.response.write(signout_link_html)
        self.response.write(calendar_template.render(calendar_dict))

class Profile(webapp2.RequestHandler):
    def get(self):
        colors=["Pink", "Purple", "Red", "Green", "Orange", "Gray","Yellow"]
        user1 = users.get_current_user().email()
        user = User.query().filter(User.email== user1).get()
        last_name=user.last_name
        family= load_family_by_email(users.get_current_user().email())
        profile_template= the_jinja_env.get_template('templates/profile.html')
        profile_dict={
        "family":family,
        "last_name": last_name,
        "colors":colors,
        }
        self.response.write(profile_template.render(profile_dict))

    def post(self):
        user = User(
            first_name=self.request.get('Firstname'),
            last_name=self.request.get('Lastname'),
            email=self.request.get('email'),
            color=self.request.get('color'))

        member=user.put()
        family= load_family_by_email(users.get_current_user().email())
        #adding user to family FamilyMembers
        family.members.append(member)
        #put the Family
        family.put()
        time.sleep(0.1)

        profile_template= the_jinja_env.get_template('templates/profile.html')
        profile_dict={
        "last_name": user.last_name,
        "first_name":user.first_name,
        "email":user.email,
        "color":user.color,
        "family":family,
        }
        self.response.write(profile_template.render(profile_dict))
        return webapp2.redirect("/profile")

class Planner (webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello")

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/calendar', Calendar),
  ('/profile', Profile),
], debug=True)
