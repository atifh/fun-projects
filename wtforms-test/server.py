#! /usr/bin/env python
## Author : Atif Haider <mail@atifhaider.com>

import tornado.httpserver
import tornado.ioloop
import tornado.web

from forms import RegistrationForm

class RegistrationHandler(tornado.web.RequestHandler):
    """A handler for user registration
    """
    def get(self):
        form = RegistrationForm()
        self.render("register.html", form=form)

    def post(self):
        data = dict((k,v) for (k, [v]) in self.request.arguments.iteritems())
        # FIXME - Is this the only way to pass data?
        form = RegistrationForm(**data)
        if form.validate():
            self.write("<h2>Form validates</h2>")
        self.render("register.html", form=form)


application = tornado.web.Application([
    (r"/", RegistrationHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    print "Server started at http://localhost:8000/"
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

