#!/usr/bin/env python
import sys
sys.path.append("src/");

from config_manager import ConfigManager

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

http_host = ConfigManager.get("app", "callback_host");
http_site = ConfigManager.get("app", "callback_site");

connection = httplib.HTTPConnection(http_host)
connection.request("GET", "/" + http_site)
response = connection.getresponse()
if response.status == 200:
	data = response.read()
	dom = minidom.parseString(data)
	elements = dom.getElementsByTagName("href")
	if len(elements) > 0:
		print getText(elements[0].childNodes)
else:
	print "ErrorCode: %d", response.status
	
connection.close()
