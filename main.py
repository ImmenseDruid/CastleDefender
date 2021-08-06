
import pygame, os, math, random, ui, spriteSheet, audio

from enemy import Enemy

from pygame.locals import *


pygame.init()
pygame.font.init()

scale = 5
width = 272 * scale
height = 160 * scale
clock = pygame.time.Clock()
fps = 60

#this is a new thing

font = pygame.font.SysFont('Times New Roman', 30)
font_60 = pygame.font.SysFont('Times New Roman', 60)


#Colors

WHITE = (255, 255, 255)
GREY = (100, 100, 100)

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


high_score = 0

#music
tracks = ['Music/1-Dark Fantasy Studio- The ceremonial (seamless).wav', 'Music/2-Dark Fantasy Studio- Demon\'s cage (seamless).wav', 'Music/3-Dark Fantasy Studio- Creepy doll (seamless).wav', 'Music/4-Dark Fantasy Studio- Dread (seamless).wav', 'Music/5-Dark Fantasy Studio- Lullaby (seamless).wav',
	'Music/6-Dark Fantasy Studio- A death embrace (seamless).wav',	'Music/9-Dark Fantasy Studio- Dark echoes (seamless).wav',	'Music/10-Dark Fantasy Studio- The mirror (seamless).wav',	'Music/11-Dark Fantasy Studio- Silent night (seamless).wav']

audioMixer = audio.Mixer(tracks)
pygame.mixer.music.set_endevent(USEREVENT + 1)

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


wave = 1
wave_difficulty = 0
target_difficulty = 1000
difficulty_multiplier = 1.1
game_over = False 
next_level = False 
enemies_alive = 0
explosion_group = pygame.sprite.Group()
explosions_to_create = []

tower_cost = 5000
towers_positions = [
[width - 290, height - 240],
[width - 150, height - 240],
[width - 290, height - 322],
[width - 150, height - 322]
]




def tiledImage(width, height, img):
	surf = pygame.Surface((width, height))
	x = 0
	y = 0
	while x < width:
		surf.blit(img, (x, y))
		x += img.get_width()
	surf.set_colorkey((0,0,0))
	return surf

def extract_img(img, width, height, x, y):
	surf = pygame.Surface((width, height))
	surf.blit(img, (-x * width, -y * height))
	surf.set_colorkey((0,0,0))
	return surf

def extract_img_precise(img, width, height, x, y):
	surf = pygame.Surface((width, height))
	surf.fill((200, 20, 200))
	surf.blit(img, (-x, -y))
	surf.set_colorkey((200, 20, 200))
	return surf

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))

#Button Imgs
repair_img = extract_img(pygame.image.load('images/icons.png').convert_alpha(), 32, 32, 4, 4)
armour_img = extract_img(pygame.image.load('images/icons.png').convert_alpha(), 32, 32, 7, 7)

tower_button_img = extract_img(pygame.image.load('images/icons.png').convert_alpha(), 32, 32, 3, 6)



#Tower Imgs
tower_img = extract_img_precise(pygame.image.load('images/Castle Tileset.png').convert_alpha(), 32, 32, 80, 0)


#Castle_imgs

house_img = extract_img_precise(pygame.image.load('images/Castle Tileset.png').convert_alpha(), 80, 32, 0, 0)
#house_img.set_colorkey((200, 20, 200))


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


def show_info():
	draw_text(f'Money : {house.coins}', font, GREY, 100, 20)
	draw_text(f'Score : {house.score}', font, GREY, 350, 20)
	draw_text(f'HighScore : {high_score}', font, GREY, 350, 50)
	draw_text(f'Level : {wave}', font, GREY, width // 2, 20)
	draw_text(f'Health : {house.health} / {house.max_health}', font, GREY, width - 200, height - 20)
	draw_text(f'1000', font, GREY, width - 220, 70)
	draw_text(f'500', font, GREY, width - 75, 70)
	draw_text(f'5000', font, GREY, width - 150, 70)

def lerp(x,y,z):
	if z < 0:
		z = 0 
	elif z > 1:
		z = 1

	v = ((1 - z) * x) + (z * y)
	return v

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

	def repair(self):
		if self.coins >= 1000 and self.health < self.max_health:
			self.health += 500
			if self.health > self.max_health:
				self.health = self.max_health
			self.coins -= 1000

	def fortify(self):
		if self.coins >= 500:
			self.max_health += 250
			self.coins -= 500

	def draw(self):
		self.image = self.image100
		screen.blit(self.image, self.rect)

class Tower(pygame.sprite.Sprite):
	def __init__(self, image100, x, y, scale):
		pygame.sprite.Sprite.__init__(self)

		width = image100.get_width()
		height = image100.get_height()

		self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
		self.rect = self.image100.get_rect()
		self.rect.x = x 
		self.rect.y = y 

		self.target_acquired = False
		self.angle = 0
		self.fired = False
		self.fire_cooldown = 1000
		self.fired_last = 0

		self.image = self.image100

	def update(self, enemy_group):
		self.target_acquired = False
		for e in enemy_group:
			if e.alive:
				target_x, target_y = e.rect.midbottom
				self.target_acquired = True
				break
		if self.target_acquired and pygame.time.get_ticks() - self.fired_last > self.fire_cooldown:
			pos = (target_x, target_y)
			
			x_dist = pos[0] - self.rect.midleft[0]
			y_dist = -(pos[1] - self.rect.midleft[1])
			self.angle = math.degrees(math.atan2(y_dist, x_dist))
			
			bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
			bullet_group.add(bullet)
			
			self.fired_last = pygame.time.get_ticks()

	def draw(self, screen):
		self.image = self.image100
		screen.blit(self.image, self.rect)

class Crosshair():
	def __init__(self, scale):
		image = icons_sheet.get_sprite(8, 6, 2)
		width = image.get_width()
		height = image.get_height()

		self.image = pygame.transform.flip(pygame.transform.scale(image, (int(width * scale), int(height * scale))), True, False)
		#print(self.image.get_colorkey())
		self.rect = self.image.get_rect()

		#hide mouse
		pygame.mouse.set_visible(False)

	def draw(self):
		mx, my = pygame.mouse.get_pos()
		self.rect.topleft = (mx, my)

		screen.blit(self.image, self.rect)


house = Castle(house_img, width - 50 - house_img.get_width() * 3, height - house_img.get_height() * 3 - grassTile.get_height() + 35, 3)


crosshair = Crosshair(0.5)

tower_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

pygame.display.set_caption('Castle Defender')



def main():
	panel = ui.Panel(0, 0, screen)

	start_label = ui.Label(width // 2, 2 * height // 3, 'Press any key to begin', size = 32)


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
			if event.type == audioMixer.getEndEvent():
				audioMixer.play()
			if event.type == KEYDOWN:
				game()
				run = False

		if pygame.mouse.get_pressed()[0] == 1:
			
			
			game()
			run = False

		start_label.draw(panel)
		crosshair.draw()
		pygame.display.update()


def game():

	global game_over
	run = True

	repair_button = ui.Button_No_Panel(width - 245, 10, (25, 25), (0,0,0), repair_img, 3)
	armour_button = ui.Button_No_Panel(width - 100, 10, (25, 25), (0,0,0), armour_img, 3)
	tower_button =  ui.Button_No_Panel(width - 170, 10, (25, 25), (0,0,0), tower_button_img, 3)
	update_time = pygame.time.get_ticks()
	#pygame.mixer.music.queue('Music/2-Dark Fantasy Studio- Demon\'s cage (seamless).wav')
	#pygame.mixer.music.fadeout(3000)

	audioMixer.play()
	global wave_difficulty, target_difficulty, next_level, wave

	while run:
		clock.tick(fps)

		screen.blit(bg, (0,0))
		screen.blit(tiledImage(width, mountains.get_height(), mountains), (0, height - mountains.get_height()))
		screen.blit(graveyard, (0, height - graveyard.get_height()))
		screen.blit(tiledImage(width, grassTile.get_height(), grassTile), (0, height - grassTile.get_height()))
		

		for t in reversed(list(tower_group)):
			t.draw(screen)
		tower_group.update(enemy_group)
		house.draw()

		

		bullet_group.draw(screen)
		bullet_group.update()
		#Add lighting

		for bullet in bullet_group:
			light = pygame.Surface((bullet.rect.width * 2, bullet.rect.height * 2 ))
			pygame.draw.circle(light, (10, 5, 5), (bullet.rect.width, bullet.rect.height), bullet.rect.size[0])
			light.set_colorkey((0,0,0))
			screen.blit(light, (bullet.rect.x - bullet.rect.width // 2, bullet.rect.y - bullet.rect.height // 2), special_flags = BLEND_RGB_ADD)


		if repair_button.draw(screen):
			house.repair()
		if tower_button.draw(screen):
			if house.coins >= tower_cost and len(tower_group) < len(towers_positions):
				tower = Tower(tower_img, towers_positions[len(tower_group)][0], towers_positions[len(tower_group)][1], 3)
				tower_group.add(tower)
				house.coins -= tower_cost
		if armour_button.draw(screen):
			house.fortify()


		show_info()
		crosshair.draw()
		
		if wave_difficulty < target_difficulty:
			delay = lerp(2000, 500, pygame.time.get_ticks() / 180000)
			if pygame.time.get_ticks() - update_time > delay:
				i = random.randrange(len(enemy_types))
				enemy_group.add(Enemy(enemy_health[i], enemy_animations[i], 200 + random.randrange(0, 200) - 100, height - 110, 2))
				update_time = pygame.time.get_ticks()
				wave_difficulty += enemy_health[i]
		#		print(delay)
		#		print(pygame.time.get_ticks() / 120000)


		#check if all enemies have been spawned
		if wave_difficulty >= target_difficulty:
			#count how many are still alive
			enemies_alive = 0
			for e in enemy_group:
				if e.alive:
					enemies_alive += 1

			if enemies_alive == 0 and not next_level:
				next_level = True
				level_reset_time = pygame.time.get_ticks()


		#move onto the next level
		if next_level:
			draw_text('Level Complete', font_60, WHITE, width // 2, height // 2)
			if pygame.time.get_ticks() - level_reset_time > 1500:
				# TODO : Go to shop
				next_level = False
				wave += 1
				
				last_enemy = pygame.time.get_ticks()
				target_difficulty *= difficulty_multiplier
				wave_difficulty = 0
				enemy_group.empty()


		if house.health <= 0:
			game_over = True
			draw_text('Game Over', font_60, WHITE, width // 2, height // 2)


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
			if event.type == audioMixer.getEndEvent():
				audioMixer.play()


		if pygame.mouse.get_pressed()[0] == 1 and not house.fired and pygame.mouse.get_pos()[1] > 100 and not game_over:	
			house.shoot()

		if pygame.mouse.get_pressed()[0] == 0:
			house.fired = False

		

		pygame.display.update()

def options():
	run = True
	panel = ui.Panel(0, 0, screen)
	music_slider = ui.Slider(width // 2 - 50, height // 2 - 25, (100, 50))
	music_slider.p = audioMixer.getVolume()
	backtogame_button = ui.Button(width // 2 - 50, height // 2 - 25 + 100, (100, 50), (255, 255, 255), None)

	music_label = ui.Label(width // 3, height // 2, 'Music Volume')


	while run:
		clock.tick(30)
		screen.blit(bg, (0,0))
		screen.blit(big_graveyard, (0, big_graveyard.get_height() - 300))



		for event in pygame.event.get():
			if event.type == QUIT:
				run = False
			if event.type == audioMixer.getEndEvent():
				audioMixer.play()


		if backtogame_button.draw(panel):
			run = False




		pygame.mixer.music.set_volume(music_slider.draw(panel))
		music_label.draw(panel)

		crosshair.draw()
		pygame.display.update()


main()

pygame.quit()