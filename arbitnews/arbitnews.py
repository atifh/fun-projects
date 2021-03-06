#! /usr/bin/env python
## Author : Atif Haider <mail@atifhaider.com>
## Time-stamp: "2009-06-08 16:58:08 atif"

import os
import cgi
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from facebook import RegisterFacebookUser
from tweetalert import RegisterTwitterUser, TweetAlert

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


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Friendsbook),
                                      ('/tweetalert/', TweetAlert),
                                      ('/tweetalert/register/', RegisterTwitterUser),
                                      ('/tweetalert/register/facebook/', RegisterFacebookUser)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

