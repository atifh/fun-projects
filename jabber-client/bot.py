#! /usr/bin/env python
## Author : Atif Haider <mail@atifhaider.com>
## Time-stamp: "2009-06-08 16:58:08 atif"

import xmpp
import logging

from eliza import *
from getpass import getpass


logging.basicConfig(filename='/home/atif/tmp/chatter-bot.log',
                    level=logging.INFO)

class ChatterBot(object):
    """A simple class for testing jabber bot
    """

    JABBER_SERVER = "talk.google.com"
    CLIENT = "gmail.com"
    JABBER_PORT = 5223
    JABBER_RESOURCE = "Google"

    def __init__(self, username, password):
        """
        
        Arguments:
        - `self`:
        - `username`:
        - `password`:
        """
        self.email = username + "@" + ChatterBot.CLIENT
        self.server = ChatterBot.JABBER_SERVER
        self.port = ChatterBot.JABBER_PORT
        self.jid = xmpp.protocol.JID(self.email)
        self.password = password

    def iterate(self, conn):
        """
        """
        try:
            conn.Process(1)
        except KeyboardInterrupt:
            return 0
        return 1

    def communicate(self, sess, mess):
        """Communicate with the user
        """
        user = mess.getFrom()
        nick = mess.getFrom().getResource()
        text = mess.getBody()
        logging.info("From: %s-- Message: %s" % (user, text))
        therapist = eliza()
        reply = therapist.respond(text)
        sess.send(xmpp.Message(mess.getFrom(), reply))

    def run(self):
        """Runs the jabber client
        """
        cb = xmpp.Client(ChatterBot.CLIENT)
        cb.connect((self.server, self.port))
        cb.RegisterHandler("message", self.communicate)
        cb.auth(self.jid.getNode(),self.password)
        cb.sendInitPresence()
        while self.iterate(cb):
            pass

if __name__ == "__main__":
    username = raw_input('GMail Username: ')
    password = getpass()
    bot = ChatterBot(username, password)
    bot.run()

