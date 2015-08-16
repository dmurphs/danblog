import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

MAIN_PLATFORM_RECT = (10,90,95,95)

def get_rect_dimensions(rect):
	return rect[2], rect[3]

def load_image(name, colorkey=None):
    fullname = name
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

class PyManMain:
    
    def __init__(self, width=640,height=480):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width
                                               , self.height))

    def LoadSprites(self):
        self.hero = Hero()
        self.hero_sprite = pygame.sprite.RenderPlain((self.hero))

        self.platform = Platform()
        self.platform_sprites = pygame.sprite.Group()
        xdim, ydim = get_rect_dimensions(MAIN_PLATFORM_RECT)

        self.shot_sprites = pygame.sprite.Group()

        for x in range(20):
            self.platform_sprites.add(Platform(pygame.Rect(x*xdim, 385, xdim, ydim)))

        for x in range(22,30):
            self.platform_sprites.add(Platform(pygame.Rect(x*xdim, 385, xdim, ydim)))

    def MainLoop(self):
        self.LoadSprites();

        screen = pygame.display.set_mode((640, 480))

        background = pygame.Surface(screen.get_size())
        background.fill((0, 0, 0))

        while 1:
            dist = 1

            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                for platform in self.platform_sprites:
                    platform.rect.x += dist
            if keys[K_RIGHT]:
                for platform in self.platform_sprites:
                    platform.rect.x -= dist

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        s = Shot(self.hero.rect.x, self.hero.rect.y)
                        self.shot_sprites.add(s)

            if not self.hero.check_hero_vertical(self.platform_sprites):
                self.hero.fall()
            else:
                self.hero.yvel = 0
                if keys[K_SPACE]:
                    self.hero.jump()

            for shot in self.shot_sprites:
                if shot.rect.x > 700 or shot.rect.x < 0:
                    shot.kill()
                else:
                    shot.update()

            self.hero.update_vertical()
            self.platform_sprites.clear(screen, background)
            self.shot_sprites.clear(screen, background)
            self.hero_sprite.clear(screen, background)
            self.hero_sprite.draw(self.screen)
            self.platform_sprites.draw(self.screen)
            self.shot_sprites.draw(self.screen)
            pygame.display.flip()

class Hero(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ss = Spritesheet('player.png')
        image = ss.image_at((0,0,20,20))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.y = 0
        self.xvel = 0
        self.yvel = 0

    def fall(self):
        self.yvel += 0.01

    def jump(self):
        self.yvel = -1

    def update_vertical(self):
        self.rect.y += self.yvel

    def check_hero_vertical(self, platform_list):
		hero_x_range = (self.rect[0], self.rect[0] + self.rect[2])
		hero_bottom = self.rect[1] + self.rect[3]

		filter_func = lambda plat: plat.rect[0] <= hero_x_range[1] and (plat.rect[0] + plat.rect[2]) >= hero_x_range[0] and hero_bottom >= plat.rect[1]

		return len(filter(filter_func, platform_list)) > 0

    def check_hero_horizontal(self, platform_list):
        pass

class Shot(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        ss = Spritesheet('items.png')
        self.image = ss.image_at((0,37, 15, 10))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.direction = 'right'

    def update(self):
        self.rect.x += 2

class Platform(pygame.sprite.Sprite):
	def __init__(self, rect=None):
		pygame.sprite.Sprite.__init__(self)
		ss = Spritesheet('spap1_0.png')
		image = ss.image_at(MAIN_PLATFORM_RECT)
		self.image, self.rect = image, rect

if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()