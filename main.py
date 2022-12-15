'Kaden Can'
'https://www.youtube.com/watch?v=VUFvY349ess&t=2093s'

import pygame, sys, time
from settings import *
from sprites import BG, Ground


class Game:
    def init(self):

        # setup
        pygame.init()
        # creates a display surface
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # sprite group
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor
        # divides height of window by height of image to find scale value
        bg_height = pygame.image.load('background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground(self.all_sprites,self.scale_factor)

    def run(self):
        last_time = time.time()
        while True:

            # delta time
            # source - https://www.youtube.com/watch?v=rWtfClpWSb8&t=0s
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()
            self.clock.tick(FRAMERATE)

running = True
while running:
    Game().run()