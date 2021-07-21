import pygame


class SpriteSheet():
	def __init__(self, img, size = (32, 32)):
		self.sheet = img
		self.size = size

	def get_sprite(self, x, y, scale):
		 surf = pygame.Surface(self.size).convert_alpha()
		 surf.fill((200, 20, 200))
		 surf.blit(self.sheet, (0,0), ((x * self.size[0]), (y * self.size[1]), self.size[0], self.size[1]))
		 surf = pygame.transform.scale(surf, (int(self.size[0] * scale), int(self.size[1] * scale)))
		 surf.set_colorkey((200, 20, 200))
		 return surf.convert_alpha()
