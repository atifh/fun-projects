# class MainPage(webapp.RequestHandler):
#   def get(self):
#     self.response.out.write('<html><title>Arbit News</title><body>')
#     user = users.get_current_user()
#     if not user:
#         return self.redirect(users.create_login_url(self.request.uri))

#     self.response.out.write('<h3>Hello, ' + user.nickname() + '. Start shouting atleast Atif will listen. ;)</h3>')
#     # Write the submission form and the footer of the page
#     self.response.out.write("""
#           <form action="/sign" method="post">
#             <div><textarea name="content" rows="3" cols="60"></textarea></div>
#             <div><input type="submit" value="Submit"></div>
#           </form>
#         </body>
#       </html>""")

#     greetings = db.GqlQuery("SELECT * FROM Greeting ORDER BY date DESC LIMIT 10")

#     for greeting in greetings:
#       if greeting.author:
#         self.response.out.write('<b>%s</b> wrote:' % greeting.author.nickname())
#       else:
#         self.response.out.write('An anonymous person wrote:')
#       self.response.out.write('<blockquote>%s</blockquote>' %
#                               cgi.escape(greeting.content))


class Guestbook(webapp.RequestHandler):
  def post(self):
    greeting = Greeting()

    if users.get_current_user():
      greeting.author = users.get_current_user()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook)],
                                     debug=True)
# from google.appengine.api import users
# from google.appengine.ext import webapp
# from google.appengine.ext.webapp.util import run_wsgi_app

# class MainPage(webapp.RequestHandler):
#   def get(self):
#     user = users.get_current_user()

#     if user:
#       self.response.headers['Content-Type'] = 'text/plain'
#       self.response.out.write('Hello, ' + user.nickname() + '. Soon Atif will add few things')
#     else:
#       self.redirect(users.create_login_url(self.request.uri))

# application = webapp.WSGIApplication(
#                                      [('/', MainPage)],
#                                      debug=True)

# def main():
#   run_wsgi_app(application)

# if __name__ == "__main__":
#   main()


# print 'Content-Type: text/plain'
# print ''
# print 'Hello, world!'
