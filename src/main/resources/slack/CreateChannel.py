#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
import requests
import urllib2
import re

# Initialize variables & check parameters
response = ''
url = "%s/channels.create" % (server['api'])
token = server['clientToken']
proxyUrl = server['proxyUrl']
if not url.strip():
    print 'Error!'
    print 'Server configuration url undefined\n'
    sys.exit(100)
if not token.strip():
    print 'Error!'
    print 'Server configuration user token undefined\n'
    sys.exit(100)
if not channel.strip():
    print 'Error!'
    print 'Parameter channel undefined\n'
    sys.exit(200)

# Set up proxy
# proxyUrl format: 'http:// username:password@proxyurl:proxyport'
if proxyUrl:
    proxy = urllib2.ProxyHandler({'http': proxyUrl.strip(), 'https': proxyUrl.strip()})
    auth = urllib2.HTTPBasicAuthHandler()
    opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

# Call Slack Incoming WebHook
channel = re.sub("#|@", "", channel)
url = "%s?name=%s&validate=true" % ( url, channel.strip() )
try:
    request = urllib2.Request( url )
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    request.add_header('Authorization', 'Bearer %s' % token)
    myResponse = urllib2.urlopen(request)
    data = json.load(myResponse)
    if( not data['ok'] ):
        print "url = %s\n\n" % url
        print json.dumps(data, indent=4, sort_keys=True)
        print "Error: %s " % data['error']
        sys.exit(100)
    channelId = data['channel']['id']
except urllib2.HTTPError as error:
    print myResponse.info()
    print 'HTTP %s error!' % error.code
    print 'Reason: %s' % error.read()
    print "url = %s" % url
    sys.exit(300)
except urllib2.URLError as error:
    print myResponse.info()
    print 'Network error!'
    print 'Reason: %s' % error.reason
    print "url = %s" % url
    sys.exit(400)

# Print output
print 'Slack channel %s created successfully' % channel
sys.exit(0)
