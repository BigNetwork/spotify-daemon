import cmd
import readline
import sys
import traceback
import time
import threading

from spotify.manager import SpotifySessionManager
try:
    from spotify.alsahelper import AlsaController
except ImportError:
    from spotify.osshelper import OssController as AlsaController
from spotify import Link

import httplib
from xml.dom import minidom
from configreader import *

class HTTPRequests(threading.Thread):
	
	def __init__(self, session):
			threading.Thread.__init__(self)
			self.session = session
			
			http_host = ConfigReader().get("app", "callback_host")
			http_port = ConfigReader().get("app", "callback_port")
			http_site = ConfigReader().get("app", "callback_site")
			self.http = HTTPManager(http_host, http_port, http_site)


	def run(self):
		while True:
			if self.session.playing == False:
				link = self.get_tracklink()
				if link != None:
					self.play_track(link)
				else:
					self.session.terminate()
			else:
				time.sleep(1)
				
	def get_tracklink(self):
		response = self.http.connect()
		data = self.http.contents(response)
		if data == None:
			return None
		
		track = self.http.parse_href_xml(data)
		self.http.close()
		return track

	def play_track(self, link):
		link = Link.from_string(link)
		track = link.as_track()
			
		self.session.load_track(track)
		self.session.play()


class HTTPManager():
	
	def __init__(self, host, port, site):
		self.http_host = host
		self.http_port = port
		self.http_site = site

	def connect(self):
		self.connection = httplib.HTTPConnection(self.http_host, self.http_port)
		self.connection.request("GET", "/" + self.http_site)
		response = self.connection.getresponse()
		if response.status == 302:
		    self.http_site = response.getheader("Location").replace('http://','').replace(self.http_host + ":" + self.http_port + "/", "").replace(self.http_host, '')
		    response = self.connect()
		return response
		
	def contents(self, response):
		if response.status == 200:
			return response.read()
		else:
			return None
			
	def close(self):
		self.connection.close()		
	
	def parse_xml(self, data):
		return minidom.parseString(data)
		
	def parse_href_xml(self, data):
		dom = minidom.parseString(data)
		elements = dom.getElementsByTagName("href")
		if len(elements) > 0:
			return self.get_xml_text(elements[0].childNodes)
		else:
			return None
		
	def get_xml_text(self, nodelist):
		rc = []
		for node in nodelist:
			if node.nodeType == node.TEXT_NODE:
				rc.append(node.data)
		return ''.join(rc)
