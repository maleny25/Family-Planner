import webapp2
import jinja2
import os
import time
import datetime
from google.appengine.api import users
from google.appengine.ext import ndb
from login import User
from login import Family
from login import Event

the_jinja_env= jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def load_family_by_email (email):
    current_user=User.query().filter(User.email==email).fetch()[0]
    family = Family.query(Family.members ==current_user.key).fetch()[0]
    return family

def get_date(event):
    return event.event_date

def load_event (email):
    event=[]
    family= load_family_by_email(email)
    for member in family.members:
        user=member.get()
        if user:
            event.extend(Event.query().filter(Event.owner==user.key).filter(Event.event_date>=datetime.datetime.today()))
    event.sort(key=get_date)
    #sort list by date
    return event


class MainHandler(webapp2.RequestHandler):
  def get(self):
    colors=["Blue", "Brown", "Cyan", "Gold", "Gray", "Green", "Lavendar", "Lime", "Magenta", "Navy", "Orange", "Pink", "Purple","Turquoise", "Red", "Yellow"]
    current_user = users.get_current_user()
    if current_user:
      signout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/'))
      email_address = current_user.email()
      user = User.query().filter(User.email == email_address).get()
      if user:
        self.redirect("/calendar")
      else:
        colors=["Blue", "Brown", "Cyan", "Gold", "Gray", "Green", "Lavendar", "Lime", "Magenta", "Navy", "Orange", "Pink", "Purple","Turquoise", "Red", "Yellow"]
        current_user = users.get_current_user()
        # user_color=""
        # for color in colors:
        #     user_color+='<option value="'+color+'">'+color+'</option>'
        self.response.write('''
            Welcome to our site, %s!  Please sign up! <br>
            <form method="post" action="/">
            First Name: <input type="text" name="first_name"> <br>
            Last Name: <input type="text" name="last_name"> <br>
            Color: <select class="" name="color">
            <br> %s <br>
            ''' % (email_address, signout_link_html))
        for color in colors:
            self.response.write('''
                <option value="%s">%s</option>'''% (color, color))
        self.response.write('''</select><br><input type="submit"></form>''')


    else:
      login_url = users.create_login_url('/')
      login_html_element = '<a href="%s">Sign in</a>' % login_url
      self.response.write('Please log in.<br>' + login_html_element)


  def post(self):
    current_user = users.get_current_user()
    user_color=self.request.get('color')
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
    time.sleep(0.1)
    self.redirect("/profile")

class Calendar(webapp2.RequestHandler):
    def get(self):
        signout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/'))
        self.response.write(signout_link_html)
        calendar_template=the_jinja_env.get_template('templates/calendar.html')
        user=users.get_current_user()
        family= load_family_by_email(users.get_current_user().email())
        # all_members = bool(self.request.get("all_members"))

        calendar_dict={
        "family": family,
        "event": load_event(users.get_current_user().email()),
        # "all_members": all_members,
        }
        self.response.write(calendar_template.render(calendar_dict))
    def post(self):
        family= load_family_by_email(users.get_current_user().email())
        event_user=self.request.get('family')
        for member in family.members:
            user=member.get()
            if user.first_name==event_user:
                user_key=member
                color=member.get().color

        event_date=datetime.date(int(self.request.get('cal1-yr')), int(self.request.get('cal1-mth')), int(self.request.get('cal1-day')))
        event_end=datetime.date(int(self.request.get('cal2-yr')), int(self.request.get('cal2-mth')), int(self.request.get('cal2-day')))
        event = Event(
            owner=user_key,
            event_name = self.request.get('event_name'),
            event_date= event_date,
            event_end=event_end,
            color=color,
            #all_members= all_members,
        )
        calevent=event.put()
        time.sleep(0.1)
        calendar_template=the_jinja_env.get_template('templates/calendar.html')
        user=users.get_current_user()
        signout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/'))
        name=self.request.get('family')
        calendar_dict={
        "family": family,
        "event": load_event(users.get_current_user().email()),
        }
        self.response.write(signout_link_html)
        self.response.write(calendar_template.render(calendar_dict))

class Profile(webapp2.RequestHandler):
    def get(self):
        colors=["Blue", "Brown", "Cyan", "Gold", "Gray", "Green", "Lavendar", "Lime", "Magenta", "Navy", "Orange", "Pink", "Purple","Turquoise", "Red", "Yellow"]
        current_user = users.get_current_user()
        user1 = users.get_current_user().email()
        user = User.query().filter(User.email== user1).get()
        family= load_family_by_email(users.get_current_user().email())
        profile_template= the_jinja_env.get_template('templates/profile.html')
        profile_dict={
        "family":family,
        "last_name": user.last_name,
        "colors":colors,
        }
        self.response.write(profile_template.render(profile_dict))

    def post(self):
        user = User(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
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

#class Planner(webapp2.RequestHandler):
    #def get(self):
    #def post(self):


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/calendar', Calendar),
  ('/profile', Profile),
 # ('/planner', Planner)
], debug=True)
