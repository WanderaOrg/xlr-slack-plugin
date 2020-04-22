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
import urllib

def addUserIdToChannel(server, channel, userId):
    response = {'status': -1}
    try:
        query_args = {'channel': channel, "user": userId}
        url = "%s/channels.invite" % ( server['api'] )
        encoded_args = urllib.urlencode(query_args)
        url = "%s?%s" % (url, encoded_args)
        token = server['clientToken']
        request = urllib2.Request( url )
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        request.add_header('Authorization', 'Bearer %s' % token)
        myResponse = urllib2.urlopen(request)
        data = json.load(myResponse)
        if( not data['ok'] ):
            if( data['error'] == "cant_invite_self" ):
                print "Oops,  Invited myself"
                return {'status': 0 }
            if( data['error'] == "already_in_channel" ):
                print "Oops,  User is already in the channel"
                return {'status': 0 }
            if( data['error'] == "user_not_found" ):
                print "Oops,  User not found"
                return {'status': 0 }
            print "url = %s\n\n" % url
            #print json.dumps(data, indent=4, sort_keys=True)
            print "Error: %s " % data['error']
            return {'status': 100 }
    except urllib2.HTTPError as error:
        print myResponse.info()
        print 'HTTP %s error!' % error.code
        print 'Reason: %s' % error.read()
        print "url = %s" % url
        return {'status': 300 }
    except urllib2.URLError as error:
        print myResponse.info()
        print 'Network error!'
        print 'Reason: %s' % error.reason
        print "url = %s" % url
        return {'status': 400 }
    return {'status': 0 }

def getUserIdByEmail(server, userEmail):
    try:
        query_args = {'email': userEmail}
        url = "%s/users.lookupByEmail" % ( server['api'] )
        encoded_args = urllib.urlencode(query_args)
        url = "%s?%s" % (url, encoded_args)
        #url = "%s/users.lookupByEmail?user=%s" % (server['api'], userEmail)
        token = server['clientToken']
        request = urllib2.Request( url )
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        request.add_header('Authorization', 'Bearer %s' % token)

        myResponse = urllib2.urlopen(request)
        data = json.load(myResponse)
        #print json.dumps(data, indent=4, sort_keys=True)
        if( not data['ok'] ):
            print "url = %s\n\n" % url
            print "Error: %s for userEmail %s\n" % (data['error'], userEmail)
            return {'status': 100, 'userId': 0 }
    except urllib2.HTTPError as error:
        print myResponse.info()
        print 'HTTP %s error!' % error.code
        print 'Reason: %s' % error.read()
        print "url = %s" % url
        return {'status': 300, 'userId': 0 }
    except urllib2.URLError as error:
        print myResponse.info()
        print 'Network error!'
        print 'Reason: %s' % error.reason
        print "url = %s" % url
        return {'status': 400, 'userId': 0 }
    return {'status': 0, 'userId': data['user']['id'] }

# Initialize variables & check parameters
response = ''
url = "%s/channels.invite" % (server['api'])
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
#channel = re.sub("#|@", "", channel)
for user in users:
    results = getUserIdByEmail(server, user)
    if ( results['status'] > 0 ):
        #print "ERROR = %s " % results['error']
        print "ERROR getUserIdByEmail for %s\n" % user
    else:
        results = addUserIdToChannel(server, channel, results['userId'])
        if ( results['status'] > 0 ):
            print "ERROR = %s " % results['error']
            sys.exit(results['status'])

sys.exit(0)
