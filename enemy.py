import pygame

class Enemy(pygame.sprite.Sprite):
	def __init__(self, health, animation_list, x, y, speed, flying = False):
		pygame.sprite.Sprite.__init__(self)
		self.alive = True
		self.speed = speed
		self.health = health
		self.animation_list = animation_list
		self.frame_idx = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()

		self.image = self.animation_list[self.action][self.frame_idx]
		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y 

		self.last_attack = 0
		self.attack_cooldown = 1000

	def set_action(self, action):
		if self.action == action:
			return
		if action < len(self.animation_list):
			self.action = action 
		else:
			self.action = 0
		self.frame_idx = 0

	def inc_frame(self):
		self.frame_idx += 1
		if self.frame_idx >= len(self.animation_list[self.action]):
			if self.action == 2:
				self.frame_idx = len(self.animation_list[self.action]) - 1
				self.kill()
			elif self.action == 0:
				self.set_action(1)
			else:
				self.frame_idx = 0
		self.image = self.animation_list[self.action][self.frame_idx]
		self.update_time = pygame.time.get_ticks()




	def update_animation(self):
		animation_cooldown = 100
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.inc_frame()

	def update(self, surface, target, bullets, explosions):
		if self.alive:
			collide_list = pygame.sprite.spritecollide(self, bullets, True)
			if collide_list:
				self.health -= 25
				for b in collide_list:
					explosions.append([b.x, b.y])
		


			if self.rect.right > target.rect.centerx:
				if pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
					target.health -= 10
					if target.health < 0:
						target.health = 0
					self.last_attack = pygame.time.get_ticks()
				self.set_action(0)

			if self.action == 1:
				self.rect.x += self.speed

			if self.health <= 0:
				self.alive = False
				target.coins += 100
				target.score += 100

				self.set_action(2)

		self.update_animation()
		#pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)
		surface.blit(self.image, self.rect)