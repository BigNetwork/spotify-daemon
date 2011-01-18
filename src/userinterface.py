import cmd
import readline
import sys
import traceback
import time
import threading

from spotify.manager import SpotifySessionManager
#try:
#    from spotify.alsahelper import AlsaController
#except ImportError:
#    from spotify.osshelper import OssController as AlsaController
from spotify import Link

class JukeboxUI(cmd.Cmd, threading.Thread):

    prompt = "spotify> "

    def __init__(self, jukebox):
        cmd.Cmd.__init__(self)
        threading.Thread.__init__(self)
        self.jukebox = jukebox
        self.playlist = None
        self.track = None
        self.results = False

    def run(self):
        self.cmdloop()

    def do_quit(self, line):
		link = Link.from_string("spotify:track:5sCCUyrCF2u9LerPMUsmlY")
		track = link.as_track()
		while(track.is_loaded() != 1):
			pass
			
		self.jukebox.load_track(track)
		self.jukebox.play()
		
        #print "Goodbye!"
        #self.jukebox.terminate()
        #return True

    def do_list(self, line):
        """ List the playlists, or the contents of a playlist """
        if not line:
            for i, p in enumerate(self.jukebox.ctr):
                if p.is_loaded():
					print "%3d %s" % (i, p.name())
                else:
                    print "%3d %s" % (i, "loading...")
        else:
            try:
                p = int(line)
            except ValueError:
                print "that's not a number!"
                return
            if p < 0 or p > len(self.jukebox.ctr):
                print "That's out of range!"
                return
            print "Listing playlist #%d" % p
            for i, t in enumerate(self.jukebox.ctr[p]):
                if t.is_loaded():
                    print "%3d %s" % (i, t.name())
                else:
                    print "%3d %s" % (i, "loading...")

    def do_play(self, line):
        if not line:
            self.jukebox.play()
            return
        if line.startswith("spotify:"):
            # spotify url
            l = Link.from_string(line)
            if not l.type() == Link.LINK_TRACK:
                print "You can only play tracks!"
                return
            self.jukebox.load_track(l.as_track())
        else:
            try:
                playlist, track = map(int, line.split(' ', 1))
            except ValueError:
                print "Usage: play [track_link] | [playlist] [track]"
                return
            self.jukebox.load(playlist, track)
        self.jukebox.play()

    def do_search(self, line):
        if not line:
            if self.results is False:
                print "No search is in progress"
            elif self.results is None:
                print "Searching is in progress"
            else:
                print "Artists:"
                for a in self.results.artists():
                    print "    ", Link.from_artist(a), a.name()
                print "Albums:"
                for a in self.results.albums():
                    print "    ", Link.from_album(a), a.name()
                print "Tracks:"
                for a in self.results.tracks():
                    print "    ", Link.from_track(a, 0), a.name()
                print self.results.total_tracks() - len(self.results.tracks()), "Tracks not shown"
                self.results = False
        else:
            self.results = None
            def _(results, userdata):
                print "\nSearch results received"
                self.results = results
            self.jukebox.search(line, _)

    def do_queue(self, line):
        if not line:
            for playlist, track in self.jukebox._queue:
                print playlist, track
            return
        try:
            playlist, track = map(int, line.split(' ', 1))
        except ValueError:
            print "Usage: play playlist track"
            return
        self.jukebox.queue(playlist, track)

    def do_stop(self, line):
        self.jukebox.stop()

    def do_next(self, line):
        self.jukebox.next()

    def emptyline(self):
        pass

    do_ls = do_list
    do_EOF = do_quit
