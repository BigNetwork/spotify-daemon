import cmd
import readline
import sys
import traceback
import time
import threading

from userinterface import *
from httprequests import *
from spotify.manager import SpotifySessionManager
#try:
#    from spotify.alsahelper import AlsaController
#except ImportError:
#    from spotify.osshelper import OssController as AlsaController
from spotify import Link

class SessionManager(SpotifySessionManager):

    queued = False
    playlist = 2
    track = 0
    username = ""

    def __init__(self, *a, **kw):
        SpotifySessionManager.__init__(self, *a, **kw)
        #self.audio = AlsaController()
        self.ui = HTTPRequests(self)
        self.ctr = None
        self.playing = False
        self.username = a[0]
        self._queue = []
        print "Trying to log in as " + a[0] + ", please wait..."

    def logged_in(self, session, error):
        self.session = session
        try:
            self.ctr = session.playlist_container()
            print "Successfully logged in as " + self.username
            self.ui.start()    
        except:
            traceback.print_exc()

    def load_track(self, track):
		if self.playing:
			self.stop()

		while(track.is_loaded() != 1):
			pass

		self.session.load(track)
		print "Loading %s" % track.name()

    def load(self, playlist, track):
        if self.playing:
            self.stop()
            
        print type(self.ctr[playlist][track])
        self.session.load(self.ctr[playlist][track])
        print "Loading %s from %s" % (self.ctr[playlist][track].name(), self.ctr[playlist].name())

    def queue(self, playlist, track):
        if self.playing:
            self._queue.append((playlist, track))
        else:
            self.load(playlist, track)
            self.play()

    def play(self):
        self.session.play(1)
        self.playing = True
        print "Playing"

    def stop(self):
        self.session.play(0)
        self.playing = False
        print "Stopping"

    def music_delivery(self, *a, **kw):
        return self.audio.music_delivery(*a, **kw)

    def next(self):
        self.stop()
        if self._queue:
            t = self._queue.pop()
            self.load(*t)
            self.play()
        else:
            self.stop()

    def end_of_track(self, sess):
        #self.next()
        self.playing = False
        print "Track ends"

    def search(self, query, callback):
        self.session.search(query, callback)
