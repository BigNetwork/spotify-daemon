import os
import random
import pygame
import pygame.mixer as mixer

FREQ = 44100
BITSIZE = -16
CHANNELS = 2
BUFFER = 1024
FRAMERATE = 30
ADS_DIR = 'ads/'
FORMATS = ["mp3"]

class AdsPlayer():

	list = []
	current = 0

	def __init__(self):
		mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)
		self.load_ads(ADS_DIR)
		random.shuffle(self.list)

	def load_ads(self, dir = '.'):
		self.list = []
		directory = os.listdir(dir)
		for file in directory:
			path = dir + file
			if file[-3:] in FORMATS:
				self.list.append(path)

	def play(self, wait = False):
		if self.current >= len(self.list):
			random.shuffle(self.list)
			self.current = 0
			
		print "Playing %s" % self.list[self.current]
		mixer.music.load(self.list[self.current])
		mixer.music.play()
		
		if wait:
			self.wait()
		
		self.current += 1
		
	def is_playing(self):
		return mixer.music.get_busy()

	def wait(self):
		while mixer.music.get_busy():
			pygame.time.Clock().tick(FRAMERATE)
		
	def loop(self):
		while True:
			self.play()
			self.wait()
			
player = AdsPlayer()
player.loop()
