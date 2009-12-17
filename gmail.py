#! /usr/bin/env python
## Author : Atif Haider <mail@atifhaider.com>

"""
A python script which notifies(sends a tweet) when there is a new 
email in your gmail inbox.
"""

import time
import twitter
import imaplib, re

# You need to have an alternate twitter id which 
# will be used to tweet you.
T_USER = YOUR_ALTERNATE_TWITTER_ID
T_PASS = YOUR_ALTERNATE_TWITTER_PASSWORD

def get_unread_mails(username, password):
    """Returns number of unread mails from google.
    """
    conn = imaplib.IMAP4_SSL("imap.gmail.com")
    conn.login(username, password)
    unreadCount = re.search("UNSEEN (\d+)", conn.status("INBOX", "(UNSEEN)")[1][0]).group(1)
    conn.logout()
    return unreadCount

def send_tweet(user, passwd, to, num_of_mails):
    """Sends a tweet to the given 'to' user
    """
    t_api = twitter.Api(user, passwd)
    t_api.PostUpdate("@%s Mail Alert! You have %s new mails." % (to, num_of_mails))

def mailalert(username, password):
    """Alerts the user if there is any new mail.
    """
    mails = get_unread_mails(username, password)
    if int(mails) != 0:
        # YOUR_TWITTER_ID: Where you want to be notified.
        send_tweet(T_USER, T_PASS, YOUR_TWITTER_ID, mails)
    else:
        print "No new Emails"
    # 1 hour sleep
    time.sleep(60*60)
    mailalert(username, password)

if __name__ == '__main__':
    from getpass import getpass
    while True:
        username = raw_input('Username: ')
        password = getpass()
        try:
            mailalert(username, password)
        except:
            print "Authentication failed. Try again!"
