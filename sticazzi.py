import facebook
import ConfigParser, os, sys

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
    if new.has_key('caption'):
        print new['from']['name'],'posted a', new['type'], new['caption']
    if new.has_key('message'):
        print new['from']['name'], 'status', new['message']
