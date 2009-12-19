#! /usr/bin/env python
## Author : Atif Haider <mail@atifhaider.com>

import os

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from mechanize import Browser

# API_KEY = '2338efee7656a7906224421771903d11'
# SECRET_KEY = '0efe5b27e215dbad59eb1ea732891c51'

class FacebookInfo(db.Model):
  """A simple class to hold the facebook users information"""

  email = db.EmailProperty()
  password = db.StringProperty()
  mobile_number = db.IntegerProperty()

def update_fb_status(email, password, message):
    """Takes the message and update facebook status.
    """
    browser_obj = Browser()
    browser_obj.open( "http://lite.facebook.com/" )
    browser_obj.select_form(nr=0)
    browser_obj.form['email'] = email
    browser_obj.form['password'] = password
    browser_obj.submit()
    # Update status
    browser_obj.select_form(nr=1)
    browser_obj.form['message'] = message
    browser_obj.submit()

def save_fb_info_obj(username, password, mobile):
  """Saves facebook info obj in DB."""
  fb_info = FacebookInfo()
  fb_info.email = username
  fb_info.password = password
  fb_info.mobile_number = int(mobile)
  fb_info.put()
  return fb_info

class RegisterFacebookUser(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname('templates/'), 'register.html')
    self.response.out.write(template.render(path, {'type': 'Facebook'}))

  def post(self):
    username = self.request.get("username")
    password = self.request.get("password")
    mobile = self.request.get("mobile")

    if username and password and mobile:
      # user = TweetInfo.get_by_key_name(username)
      query = FacebookInfo.all()
      user = query.filter('email = ', username)
      user = user.fetch(1)
      if not user:
        fb_info = save_fb_info_obj(username, password, mobile)
        return self.response.out.write("%s is registered with the mobile number: %d" % (fb_info.email,
                                                                                        fb_info.mobile_number))
      else:
        return self.response.out.write("%s is already registered" % username)
    return self.redirect('/tweetalert/register/facebook/')


if __name__ == '__main__':
    from getpass import getpass
    email = raw_input('FaceBook Email: ')
    password = getpass()
    br = authenticate(email, password)
    print "Authenticated"
    message = raw_input('Update Status: ')
    update_fb_status(br, message)

