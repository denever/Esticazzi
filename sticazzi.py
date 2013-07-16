#!/usr/bin/env python
#
# Eeeesticazzi.
#

import os
import sys
import facebook
import textwrap
import signal
import urllib2
from StringIO import StringIO
from asciiporn import img2txt

BASE0=244
BASE01=240
YELLOW=136
ORANGE=166
RED=160
MAGENTA=125
VIOLET=61
BLUE=33
CYAN=37
GREEN=64

def fetch_user_stream_data(oauth_access_token):
    graph = facebook.GraphAPI(oauth_access_token)
    return graph.get_connections('me', 'home')

def fg256(x, y):
    return u'\033[38;5;%dm%s\033[0m' % (x, y)

def get_picture(url):
    try:
        picture_data = urllib2.urlopen(url).read()
        return img2txt(StringIO(picture_data), scale=3)
    except:
        return url

def print_post(post, show_pictures):
    p = u''
    p += fg256(CYAN, post['from']['name'])

    try: p += ' ' + fg256(BASE0, post['status_type'])
    except KeyError: pass

    try: p += '\n' + post['message']
    except KeyError: pass

    try: p += '\n' + fg256(YELLOW, post['name'])
    except KeyError: pass

    try: p += '\n' + fg256(BASE01, post['description'])
    except KeyError: pass

    try: likes = post['likes']['count']
    except: likes = 0

    try: comments = len(post['comments']['data'])
    except: comments = 0

    p += '\n'

    p += fg256(BASE0, u'Likes: ')
    p += fg256(GREEN, str(likes))
    p += fg256(BASE0, u' - Comments: ')
    p += fg256(GREEN, str(comments))

    if show_pictures and 'picture' in post:
        p += '\n' + get_picture(post['picture'])
        p += '\n' + fg256(BASE0, post['picture'])

    print p + '\n'

def prompt_oauth_access_token():
    oauth_access_token = raw_input('Please insert your oauth access token: ')
    config = ConfigParser.ConfigParser()
    config.add_section('auth')
    config.set('auth','oauth_token', oauth_access_token)

    with open(os.path.expanduser('~/.sticazzi.cfg'), 'wb') as configfile:
        config.write(configfile)
    return oauth_access_token

def graceful_exit(signal, frame):
    print "\nCya!"
    sys.exit(0)

if __name__ == '__main__':
    import ConfigParser

    show_pictures = '-p' in sys.argv

    signal.signal(signal.SIGINT, graceful_exit)

    config = ConfigParser.ConfigParser()

    oauth_access_token = None
    try:
        config.read(os.path.expanduser('~/.sticazzi.cfg'))
        oauth_access_token = config.get('auth', 'oauth_token')
    except:
        oauth_access_token = prompt_oauth_access_token()

    if oauth_access_token is None:
        sys.exit(1)

    news_feed = dict()
    while len(news_feed) == 0:
        try:
            news_feed = fetch_user_stream_data(oauth_access_token)
        except facebook.GraphAPIError, ex:
            print ex
            oauth_access_token = prompt_oauth_access_token()

    if news_feed.has_key('data'):
        for new in news_feed['data']:
            print_post(new, show_pictures)
