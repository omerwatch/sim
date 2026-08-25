import pygame
from pygame.locals import *
import math

GRAVITY_CONSTANT = 0.1 # units pixels / frame squared

class Physics_Object(pygame.sprite.Sprite):
    def __init__(self, colour, width, height, mass):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width, height))
        self.image.fill(colour)

        self.rect = self.image.get_rect()

        self.mass = mass

        self.v = 0
        self.vtheta = 0

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        self.rect.x += self.v * math.cos(self.vtheta) # angle is measured in radians
        self.rect.y += self.v * math.sin(self.vtheta)

        print(self.v, self.vtheta)
        print("position", self.rect.x, self.rect.y)

    def apply_forces(self, external = ()):
        f = GRAVITY_CONSTANT * self.mass
        theta = math.pi / 2

        vx = self.v * math.cos(self.vtheta) + f * math.cos(theta)
        vy = self.v * math.sin(self.vtheta) + f * math.sin(theta)

        self.v = math.sqrt(vx**2 + vy**2)
        self.vtheta = math.atan2(vy, vx) 

        self.move()



class Player(Physics_Object):
    def __init__(self, colour, width, height, mass):
        Physics_Object.__init__(self, colour, width, height, mass)

        self.left = False
        self.right = False
        self.current = "right"

    # def player_move(self):
    #     if not self.right and not self.left:
    #         return

    #     theta = 0
    #     if self.current == "left" and self.left:
    #         theta = math.pi
    #     if self.current == "right" and self.right:
    #         theta = 0
        
    #     self.move(1, theta)

class Immovable_Object(Physics_Object):
    def __init__(self, colour, width, height, x, y):
        Physics_Object.__init__(self, colour, width, height, 0)

        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.v = 0
        self.vtheta = 0


    

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('RIGID BODY SIMULATOR')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 50, 100))

    CENTERX = background.get_rect().centerx
    CENTERY = background.get_rect().centery

    # floor = pygame.Rect(0, 700, 800, 100)
    # pygame.draw.rect(background, (0, 100, 0), floor)

    floor = Immovable_Object((0, 100, 0), 800, 100, 0, 700)

    testball = Player((0, 0, 0), 50, 50, 1)

    framecounter = 0

    # # Display some text
    # font = pygame.font.Font(None, 36)
    # text = font.render("Hello There", 1, (10, 10, 10))
    # textpos = text.get_rect()
    # textpos.centerx = background.get_rect().centerx
    # background.blit(text, textpos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            # if event.type == KEYDOWN:
            #     if event.key == K_RIGHT:
            #         testball.right = True
            #         testball.current = "right"
            #     if event.key == K_LEFT:
            #         testball.left = True
            #         testball.current = "left"
            # if event.type == KEYUP:
            #     if event.key == K_RIGHT:
            #         testball.right = False
            #         testball.current = "left"
            #     if event.key == K_LEFT:
            #         testball.left = False
            #         testball.current = "right"

        # testball.player_move()
        if framecounter == 10:
            testball.apply_forces()
            floor.apply_forces()
            # make a function that applies forces to all the physics objects inside of a list
            framecounter = -1
        framecounter += 1

        screen.blit(background, (0, 0))
        testball.draw(screen)
        floor.draw(screen)
        pygame.display.flip()


if __name__ == '__main__': main()