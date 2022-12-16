'Kaden Can, Period 3, Intro To Programming'
'https://www.youtube.com/watch?v=VUFvY349ess'
'https://www.youtube.com/watch?v=rWtfClpWSb8&t=0s - Delta Time'
'https://www.youtube.com/watch?v=uW3Fhe-Vkx4&t=0s - Masks'



import pygame, sys, time
from settings import *
from sprites import *
 
class Game:
    def __init__(self):
        
        # setup
        pygame.init()
        #creates a display surface for the game
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        # names the display Flappy Bird
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        # track the status of the game (see if running)
        self.active = True

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor
        # gets the height of the window and divides it by the height of the image to find the scale factor needed to stretch the image
        bg_height = pygame.image.load('background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprite setup
        BG(self.all_sprites,self.scale_factor)
        # ground is part of the collision sprites and kills plane if touched
        Ground([self.all_sprites,self.collision_sprites],self.scale_factor)
        # divide scale factor by two to make the plane smaller
        self.plane = Plane(self.all_sprites,self.scale_factor/ 2)

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        # starts the timer 1400ms is how many times it should run
        pygame.time.set_timer(self.obstacle_timer,1400)

        # text
        # uses the font BD Cartoon Shout size 30
        # sets the starting score to 0
        # sets the offset score to 0 when restarting game
        self.font = pygame.font.Font('BD_Cartoon_Shout.ttf',30)
        self.score = 0
        self.start_offset = 0

        # menu
        # loads the menu image
        # sets the menu image in the middle of the display surface
        self.menu_surf = pygame.image.load('menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

    # method for collisions
    def collisions(self):
        # check if there is any collision between plan and obstacles
         if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False,pygame.sprite.collide_mask)\
        or self.plane.rect.top <= 0: #makes sure the plane cant go throught the top of the display
        # checking if obstacle that collides with plane is part of sprite_type obstacle
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            # when plane collides with obstacle turns off the status of the game class
            self.active = False
            # when plane collides with obstacle kill plane
            self.plane.kill()
    # method for displaying score 
    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            # once you die put the score under neath the menu
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

        # creating surface of score
        score_surf = self.font.render(str(self.score),True,'black')
        # puts the score in the topcenter
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2,y))
        # blitting onto the screen
        self.display_surface.blit(score_surf,score_rect)

    # run method
    def run(self):
        last_time = time.time()
        # updating pygame
        while True:
            
            # delta time - there to account for different framerates
            dt = time.time() - last_time
            last_time = time.time()
 
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    # when mouse button is pressed the plane 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        # plane jumps
                        self.plane.jump()
                    else:
                        # looping status of game and clock
                        self.plane = Plane(self.all_sprites,self.scale_factor/ 2)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()

                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor/1.7)
            
            # game logic
            # fill the space around background as black
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            # while game is active set collisions true
            if self.active:
                self.collisions()
            else:
                # if game is over start menu screen
                self.display_surface.blit(self.menu_surf,self.menu_rect)

            pygame.display.update()
            # updates the framerate
            self.clock.tick(FRAMERATE)

 # checking if current file is main file
if __name__ == '__main__':
    # creating one instance of the game class
    game = Game()
    # calling game.run()
    game.run()