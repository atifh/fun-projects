#! /usr/bin/env python
## Author : Atif Haider <mail@atifhaider.com>
## Time-stamp: "2009-06-08 16:58:08 atif"

import cgi
import os
import twitter
from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class TweetInfo(db.Model):
  """A simple class to hold the twitter users information"""

  username = db.StringProperty()
  password = db.StringProperty()
  mobile_number = db.IntegerProperty()
  
class Greeting(db.Model):
  """A simple class to hold the greetings."""

  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


class MainPage(webapp.RequestHandler):
  def get(self):
    greetings_query = Greeting.all().order('-date')
    greetings = greetings_query.fetch(30)

    user = users.get_current_user()

    if not user:
        return self.redirect(users.create_login_url(self.request.uri))

    url = users.create_logout_url(self.request.uri)
    url_linktext = 'Logout'

    template_values = {
      'greetings': greetings,
      'url': url,
      'url_linktext': url_linktext,
      'user': user,
      }

    path = os.path.join(os.path.dirname('templates/'), 'index.html')
    self.response.out.write(template.render(path, template_values))

class Friendsbook(webapp.RequestHandler):
  def post(self):
    greeting = Greeting()

    if users.get_current_user():
      greeting.author = users.get_current_user()

    content =  self.request.get('content')
    if content:
      greeting.content = content
      greeting.put()
      self.redirect('/')
    return self.redirect('/')

def send_tweet(username, passwd, message):
  """Login to the given username passd and sends
  update."""
  t_api = twitter.Api(username, passwd)
  t_api.PostUpdate(message)
  

def save_tweet_info_obj(username, password, mobile):
  """Saves tweet info obj in DB."""
  tweet_info = TweetInfo()
  tweet_info.username = username
  tweet_info.password = password
  tweet_info.mobile_number = int(mobile)
  tweet_info.put()
  return tweet_info

class RegisterTwitterUser(webapp.RequestHandler):
  # While rendering form handle all these form data in post method
  def get(self):
    path = os.path.join(os.path.dirname('templates/'), 'register.html')
    self.response.out.write(template.render(path, {}))

  def post(self):
    username = self.request.get("username")
    password = self.request.get("password")
    mobile = self.request.get("mobile")

    if username and password and mobile:
      # user = TweetInfo.get_by_key_name(username)
      query = TweetInfo.all()
      user = query.filter('username = ', username)
      user = user.fetch(1)
      if not user:
        tweet_info = save_tweet_info_obj(username, password, mobile)
        return self.response.out.write("%s is registered with the mobile number: %d" % (tweet_info.username,
                                                                                        tweet_info.mobile_number))
      else:
        return self.response.out.write("%s is already registered" % username)
    return self.redirect('/tweetalert/register/')

class TweetAlert(webapp.RequestHandler):
  def get(self):
    subject = "Someone just used the TweetAlert service"
    sender_address = "gmail.com Help <aatif.haider@gmail.com>"
    user_address = "mail@atifhaider.com"

    mobile_number = self.request.get("msisdn") 
    content = self.request.get("content")
    
    if mobile_number and content:
      query = TweetInfo.all()
      user = query.filter('mobile_number = ', int(mobile_number))
      user = user.fetch(1)
      # user = TweetInfo.get_by_key_name(mobile_number) # user object 
      if user:
        user = user[0]
        send_tweet(user.username, user.password, content[6:])
        body = "%s has sent a tweet(%s) from the mobile num  %s" % (user.username,
                                                                    content,
                                                                    mobile_number)
        mail.send_mail(sender_address, user_address, subject, body)
        response_message = "Hi, %s! you twitter status has been updated. Have a nice day." % (user.username)
        json_data = simplejson.dumps([{"msisdn": mobile_number, "content": response_message}])
        return self.response.out.write(json_data)

      return self.redirect('/tweetalert/register/')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Friendsbook),
                                      ('/tweetalert/', TweetAlert),
                                      ('/tweetalert/register/', RegisterTwitterUser)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

