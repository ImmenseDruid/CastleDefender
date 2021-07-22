import pygame, random

class Mixer():
	def __init__(self, tracks):
		self.tracks = tracks
		self.looping = False 

	def play(self):
		if not pygame.mixer.music.get_busy():
			pygame.mixer.music.stop()
			pygame.mixer.music.load(random.choice(self.tracks))
			pygame.mixer.music.play()

	def setVolume(self, vol):
		pygame.mixer.music.set_volume(vol)

	def getVolume(self):
		return pygame.mixer.music.get_volume()

	def getEndEvent(self):
		return pygame.mixer.music.get_endevent()