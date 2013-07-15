import os
import sys
import facebook
import textwrap

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

def fg256(x, y):
    return u'\033[38;5;%dm%s\033[0m' % (x, y)

def print_post(post):
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

    print p + '\n'

if __name__ == '__main__':
    import ConfigParser

    config = ConfigParser.ConfigParser()
    oauth_access_token = None

    try:
        config.read(os.path.expanduser('~/.sticazzi.cfg'))
        oauth_access_token = config.get('auth', 'oauth_token')
    except:
        oauth_access_token = raw_input('Please insert your oauth access token:')
        config = ConfigParser.ConfigParser()
        config.add_section('auth')
        config.set('auth','oauth_token', oauth_access_token)

        with open(os.path.expanduser('~/.sticazzi.cfg'), 'wb') as configfile:
            config.write(configfile)

    if oauth_access_token is None:
        sys.exit(1)

    graph = facebook.GraphAPI(oauth_access_token)
    news_feed = graph.get_connections("me", "home")
    for new in news_feed['data']:
        print_post(new)
