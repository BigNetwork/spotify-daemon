#!/usr/bin/env python
import sys
sys.path.append("src/");

from configreader import *

############################
## HTTP POSTS
############################
import httplib
from xml.dom import minidom

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

#def getconnection(self,url,handle_redirects=True,headers={}):
#"""Get a httplib connection for the given url.
#    
#    @param url: Should be a relative path for the HTTP request.
#    @type url: string
#    @param handle_redirects: Set this to True if you want to follow redirects (301 and 302). (default)
#    @return: The httplib connection for the specified (or redirected) url."""
#    if url.upper()[:6] == 'HTTPS:':
#        conn = httplib.HTTPSConnection(self.host)
#    else:
#        conn = httplib.HTTPConnection(self.host)
#        conn.connect()
#    if not headers.has_key("User-Agent"):
#        headers["User-Agent"] = self.agent
#    if handle_redirects:
#        # Now we handle 301 and 302 too!
#        conn.request("HEAD", url,headers=headers)
#        responseOb = conn.getresponse() ## Grab HTTPResponse Object
#    if responseOb.status in (301,302,):
#        url = urlparse.urljoin(url, responseOb.getheader('location', ''))
#        conn = self.getconnection(url,True)
#    return conn

def getdata(host, path):
    print "Getting data for URL: http://" + host + "/" + path
    output = ""
    connection = httplib.HTTPConnection(host)
    connection.request("GET", "/" + path)
    response = connection.getresponse()
    if response.status == 200:
    	output = response.read()
    else:
    	if response.status == 302 and response.getheader("Location"):
            output = getdata(host, response.getheader("Location").replace('http://','').replace(host + "/", ""))
        else:
    	    print "Error:", response.status, response.reason
    	    print response.msg
    	    print response.read()
    connection.close()
    return output

http_host = ConfigReader().get("app", "callback_host");
http_port = ConfigReader().get("app", "callback_port");
http_site = ConfigReader().get("app", "callback_site");

output = getdata(http_host + ":" + http_port, http_site)
if output:
    dom = minidom.parseString(output)
    elements = dom.getElementsByTagName("href")
    if len(elements) > 0:
    	print getText(elements[0].childNodes)