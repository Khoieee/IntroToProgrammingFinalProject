import pygame
from settings import *
from random import choice, randint

class BG(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)
        # loading image for background
        bg_image = pygame.image.load('background.png').convert()

        # scaling the height and the width to neatly fit the display surface
        full_height = bg_image.get_height() * scale_factor
        full_width = bg_image.get_width() * scale_factor
        full_sized_image = pygame.transform.scale(bg_image,(full_width,full_height))

        # making the image double the width to help with scrolling
        self.image = pygame.Surface((full_width * 2,full_height))
        # centers the background
        self.image.blit(full_sized_image,(0,0))
        self.image.blit(full_sized_image,(full_width,0))

        # sets the coords of the background making it cover the whole display surface.
        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)
    # makes the background scroll past at a certain speed. If the center is less that zero it will repeat
    def update(self,dt):
        self.pos.x -= 300 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

# makes ground the sprite type ground
# setting up ground class
class Ground(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)
        self.sprite_type = 'ground'

        # image
        # loads image for ground sprite
        # convert alpha to get rid of transparent background
        ground_surf = pygame.image.load('ground.png').convert_alpha()
        self.image = pygame.transform.scale(ground_surf,pygame.math.Vector2(ground_surf.get_size()) * scale_factor)

        #position
        # sets the position of the ground at the bottom
        self.rect = self.image.get_rect(bottomleft = (0,WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # mask
        # masking the ground image so you can actually go into the crevices
        self.mask = pygame.mask.from_surface(self.image)
    # method for updating the ground
    # makes the ground scroll past at a certain speed
    # makes it loop if it reaches it
    def update(self,dt):
        self.pos.x -= 360 * dt
        if self.rect.centerx <= 0:
            self.pos.x =0

        self.rect.x = round(self.pos.x)
# plane class 
class Plane(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)

        # image
        # helps setup the image animation
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # rect
        # sets the position of the plane on the displane surface
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # movement
        # sets the gravity of the plane and the direction pulling it
        self.gravity = 600
        self.direction = 0

        # mask
        # masking the plane so it doesn't clip on the transparent edges
        self.mask = pygame.mask.from_surface(self.image)

    def import_frames(self, scale_factor):
        self.frames = []
        for i in range(3):
            # loads the three images for the plane so it seems as if the propelors are spinning
            surf = pygame.image.load(f'red{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size())* scale_factor)
            self.frames.append(scaled_surface)

    #applying gravity to the plane
    def apply_gravity(self,dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    # makes the plane jump
    def jump(self):
        self.direction = - 400

    # makes the images rotate in specific order to make it animated
    def animate(self,dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    # rotates the plane as it goes in a downward direction
    def rotate(self,dt):
        rotated_plane = pygame.transform.rotozoom(self.image,-self.direction * 0.05,1)
        self.image = rotated_plane
        self.mask = pygame.mask.from_surface(self.image)

    # updates that constantly apply gravity, animations, and rotations
    def update(self,dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate(dt)
# obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)
        # setting sprite type for colllisions
        self.sprite_type = 'obstacle'

        # sets the spikes either at the top or the bottom
        orientation = choice(('up','down'))
        # chooses between variant of spike and removes transparent background of image
        surf = pygame.image.load(f'{choice((0,1))}.png').convert_alpha()
        # sets the size of the images
        self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size())* scale_factor)
        
        x = WINDOW_WIDTH + randint(40,100)
        # oreination if on the top side
        if orientation == 'up':
            y = WINDOW_HEIGHT + randint(10,50)
            self.rect = self.image.get_rect(midbottom = (x,y))
        else:
            # orientation if on the bottom side
            y = randint(-50,-10)
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect = self.image.get_rect(midtop = (x,y))

        self.pos = pygame.math.Vector2(self.rect.topleft)

        # mask
        # masking the spikes so plane doesn't clip the transparent edges
        self.mask = pygame.mask.from_surface(self.image)

    # updates the obstacles so they can move acorss the screen
    # once they are on the left side of the screen they are killed
    def update(self,dt):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()
