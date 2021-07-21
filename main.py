
import pygame, os, math, random, ui, spriteSheet

from enemy import Enemy

from pygame.locals import *


pygame.init()

scale = 5
width = 272 * scale
height = 160 * scale
clock = pygame.time.Clock()
fps = 60



screen = pygame.display.set_mode((width, height))

bg = pygame.image.load('images/Environment/background.png')
bg = pygame.transform.scale(bg, (width, height)).convert_alpha()
graveyard = pygame.image.load('images/Environment/graveyard.png')
big_graveyard = pygame.transform.scale(graveyard, (width, graveyard.get_height() * 5)).convert_alpha()
graveyard = pygame.transform.scale(graveyard, (width, height // 2)).convert_alpha()
mountains = pygame.image.load('images/Environment/mountains.png')
mountains = pygame.transform.scale(mountains, (mountains.get_width() * scale, mountains.get_height() * 3)).convert_alpha()
grassTile = pygame.image.load('images/Environment/grassTile.png')
grassTile = pygame.transform.scale(grassTile, (grassTile.get_width() * 2, grassTile.get_height() * 2)).convert_alpha()

house_img =  pygame.transform.flip(pygame.image.load('images/house-a.png'), True, False)

fireball_sheet = spriteSheet.SpriteSheet(pygame.transform.flip(pygame.image.load('images/FireBall_2_64x64.png'), True, False).convert_alpha(), (64, 64))
explosion_sheet = spriteSheet.SpriteSheet(pygame.transform.flip(pygame.image.load('images/Explosion_2_64x64.png'), True, False).convert_alpha(), (64, 64))

bullet_img = pygame.image.load('images/37.png')
bullet_img = pygame.transform.flip(pygame.transform.scale(bullet_img, (int(bullet_img.get_width() * 0.1), int(bullet_img.get_height()* 0.1))), True, False).convert_alpha()

icons_sheet = spriteSheet.SpriteSheet(pygame.image.load('images/icons.png'))

enemy_animations = []
enemy_types = ['skeleton', 'skeleton-clothed']
enemy_health = [75, 150]
enemy_canFly = [False, False]

animation_types = ['rise', 'walk']

#music
tracks = ['Music/1-Dark Fantasy Studio- The ceremonial (seamless).wav', 'Music/2-Dark Fantasy Studio- Demon\'s cage (seamless).wav', 'Music/3-Dark Fantasy Studio- Creepy doll (seamless).wav', 'Music/4-Dark Fantasy Studio- Dread (seamless).wav', 'Music/5-Dark Fantasy Studio- Lullaby (seamless).wav',
	'Music/6-Dark Fantasy Studio- A death embrace (seamless).wav',	'Music/9-Dark Fantasy Studio- Dark echoes (seamless)',	'Music/10-Dark Fantasy Studio- The mirror (seamless)',	'Music/11-Dark Fantasy Studio- Silent night (seamless)']

for enemy in enemy_types:
	animation_list = []
	for i, animation in enumerate(animation_types):
		temp_list = []
		num_of_frames = [6, 8]
		for j in range(num_of_frames[i]):
			print(f'images/Sprites/{enemy}/{animation}/{enemy}-{j + 1}.png')
			
			img = pygame.image.load(f'images/Sprites/{enemy}/{animation}/{enemy}-{j + 1}.png')
			img = pygame.transform.flip(img, True, False)
			e_w = img.get_width()
			e_h = img.get_height()
			img = pygame.transform.scale(img, (int(e_w * 1), int(e_h * 1)))
			temp_list.append(img)
		animation_list.append(temp_list)
	temp_list = []
	for j in range(5):
		img = pygame.image.load(f'images/Sprites/enemy-death/enemy-death-{j + 1}.png')
		img = pygame.transform.flip(img, True, False)
		e_w = img.get_width()
		e_h = img.get_height()
		img = pygame.transform.scale(img, (int(e_w * 1), int(e_h * 1)))
		temp_list.append(img)
	animation_list.append(temp_list)
	enemy_animations.append(animation_list)

enemy_1 = Enemy(enemy_health[0], enemy_animations[0], 200, height - 110, 2, enemy_canFly[0])
enemy_group = pygame.sprite.Group()

enemy_group.add(enemy_1)
explosion_group = pygame.sprite.Group()
explosions_to_create = []

def tiledImage(width, height, img):
	surf = pygame.Surface((width, height))
	x = 0
	y = 0
	while x < width:
		surf.blit(img, (x, y))
		x += img.get_width()
	surf.set_colorkey((0,0,0))
	return surf


class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.x = x 
		self.y = y
		self.frame_idx = 0
		self.frames = 2816 // 64
		self.animation_frames = []
		self.animation_cooldown = 5
		self.update_time = 0
		for i in range(self.frames):
			self.animation_frames.append(explosion_sheet.get_sprite(i, 0, 1))
		self.animation_frames = list(reversed(self.animation_frames))
		self.img = self.animation_frames[0]

	def update(self):
		if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_idx += 1
			if self.frame_idx >= len(self.animation_frames):
				self.kill()
				return
			self.img = self.animation_frames[self.frame_idx]
		screen.blit(self.img, (self.x - self.img.get_width() // 2, self.y - self.img.get_height() // 2))

class Bullet(pygame.sprite.Sprite):
	def __init__(self, img, x, y, angle):
		pygame.sprite.Sprite.__init__(self)
		self.image = fireball_sheet
		
		self.x = x 
		self.y = y
		self.angle = math.radians(angle)
		self.speed = 10 
		#print(self.angle)
		self.dx = math.cos(self.angle) * self.speed
		self.dy = -(math.sin(self.angle) * self.speed)

		#self.image = pygame.transform.rotate(self.image, angle - 180)

		self.animation_frames = []
		self.animation_cooldown = 5
		self.update_time = 0
		self.frame_idx = 0
		self.frames = self.image.sheet.get_width() // 64
		#self.update_time = 0


		for i in range(self.frames):
			self.animation_frames.append(fireball_sheet.get_sprite(i, 0, .5))
		self.animation_frames = list(reversed(self.animation_frames))
		self.image = self.animation_frames[0]


		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y 

	def update(self):
		if self.rect.right < 0 or self.rect.left > width or self.rect.bottom < 0 or self.rect.top > height - 70:
			explosion_group.add(Explosion(self.x, self.y))
			self.kill()

		if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_idx += 1
			if self.frame_idx >= len(self.animation_frames):
				self.frame_idx = 0
			self.image = self.animation_frames[self.frame_idx]
			self.image = pygame.transform.rotate(pygame.transform.flip(self.image, True, False), math.degrees(self.angle))

		self.x += self.dx
		self.y += self.dy

		self.rect.x = self.x
		self.rect.y = self.y


	def draw(self, screen):
		screen.blit(self.image, screen)



class Castle():
	def __init__(self, image100, x, y, scale):
		self.health = 1000
		self.max_health = self.health
		self.fired = False
		width = image100.get_width()
		height = image100.get_height()

		self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
		self.rect = self.image100.get_rect()
		self.rect.x = x 
		self.rect.y = y 

		self.coins = 0
		self.score = 0

	def shoot(self):
		pos = pygame.mouse.get_pos()
		#pygame.draw.line(screen, (255, 255, 255), (self.rect.midleft[0], self.rect.midleft[1]), (pos))
		x_dist = pos[0] - self.rect.midleft[0]
		y_dist = -(pos[1] - self.rect.midleft[1])
		self.angle = math.degrees(math.atan2(y_dist, x_dist))
		#print(self.angle)
		bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
		bullet_group.add(bullet)
		self.fired = True

	def draw(self):
		self.image = self.image100
		screen.blit(self.image, self.rect)


class Crosshair():
	def __init__(self, scale):
		image = icons_sheet.get_sprite(8, 6, 2)
		width = image.get_width()
		height = image.get_height()

		self.image = pygame.transform.flip(pygame.transform.scale(image, (int(width * scale), int(height * scale))), True, False)
		print(self.image.get_colorkey())
		self.rect = self.image.get_rect()

		#hide mouse
		pygame.mouse.set_visible(False)

	def draw(self):
		mx, my = pygame.mouse.get_pos()
		self.rect.topleft = (mx, my)

		screen.blit(self.image, self.rect)


house = Castle(house_img, width - 50 - house_img.get_width(), height - house_img.get_height() - grassTile.get_height() + 35, 1)

crosshair = Crosshair(0.5)

bullet_group = pygame.sprite.Group()

pygame.display.set_caption('Castle Defender')



def main():

	run = True
	pygame.mixer.music.load(tracks[0])
	pygame.mixer.music.play()
	while run:
		clock.tick(fps)

		screen.blit(bg, (0,0))
		#screen.blit(mountains, (0, 0))
		screen.blit(big_graveyard, (0, big_graveyard.get_height() - 300))
		

		

		for event in pygame.event.get():
			if event.type == QUIT:
				run = False

		if pygame.mouse.get_pressed()[0] == 1:
			
			
			game()
			run = False

		crosshair.draw()
		pygame.display.update()


def game():
	run = True

	
	update_time = pygame.time.get_ticks()
	#pygame.mixer.music.queue('Music/2-Dark Fantasy Studio- Demon\'s cage (seamless).wav')
	#pygame.mixer.music.fadeout(3000)

	pygame.mixer.music.load(tracks[1])
	pygame.mixer.music.play()

	while run:
		clock.tick(fps)

		screen.blit(bg, (0,0))
		screen.blit(tiledImage(width, mountains.get_height(), mountains), (0, height - mountains.get_height()))
		screen.blit(graveyard, (0, height - graveyard.get_height()))
		screen.blit(tiledImage(width, grassTile.get_height(), grassTile), (0, height - grassTile.get_height()))
		

		house.draw()

		crosshair.draw()

		bullet_group.draw(screen)
		bullet_group.update()

		if pygame.time.get_ticks() - update_time > 2000:
			i = random.randrange(len(enemy_types))
			enemy_group.add(Enemy(enemy_health[i], enemy_animations[i], 200 + random.randrange(0, 200) - 100, height - 110, 2))
			update_time = pygame.time.get_ticks()
		enemy_group.update(screen, house, bullet_group, explosions_to_create)


		for i, e in reversed(list(enumerate(explosions_to_create))):
			explosion_group.add(Explosion(e[0], e[1]))
			explosions_to_create.remove(explosions_to_create[i])

		explosion_group.update()

		for event in pygame.event.get():
			if event.type == QUIT:
				run = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					options()


		if pygame.mouse.get_pressed()[0] == 1 and not house.fired:
			house.shoot()

		if pygame.mouse.get_pressed()[0] == 0:
			house.fired = False



		pygame.display.update()

def options():
	run = True
	panel = ui.Panel(0, 0, screen)
	music_slider = ui.Slider(width // 2 - 50, height // 2 - 25, (100, 50))
	music_slider.p = 1
	backtogame_button = ui.Button(width // 2 - 50, height // 2 - 25 + 100, (100, 50), (255, 255, 255), None)

	while run:
		clock.tick(30)
		screen.blit(bg, (0,0))
		screen.blit(big_graveyard, (0, big_graveyard.get_height() - 300))



		for event in pygame.event.get():
			if event.type == QUIT:
				run = False


		if backtogame_button.draw(panel):
			run = False




		pygame.mixer.music.set_volume(music_slider.draw(panel))

		crosshair.draw()
		pygame.display.update()


main()

pygame.quit()