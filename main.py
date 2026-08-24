import pygame
from pygame.locals import *
import math

class Physics_Object(pygame.sprite.Sprite):
    def __init__(self, colour, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width, height))
        self.image.fill(colour)

        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, v, theta):
        self.rect.x += v * math.cos(theta) # angle is measured in radians
        self.rect.y += v * math.sin(theta) * -1 # always multiply y value by negative 1 because coordinate axis is flipped

class Player(Physics_Object):
    def __init__(self, colour, width, height, x, y):
        Physics_Object.__init__(self, colour, width, height)

        self.rect.x = x
        self.rect.y = y

    def player_move(self, walking):
        if walking == 0:
            return
        
        theta = 0
        if walking == -1:
            theta = math.pi
        self.move(4, theta)


    

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('RIGID BODY SIMULATOR')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 50, 100))

    CENTERX = background.get_rect().centerx
    CENTERY = background.get_rect().centery

    floor = pygame.Rect(0, 400, 500, 100)
    pygame.draw.rect(background, (0, 100, 0), floor)

    testball = Player((0, 0, 0), 50, 50, CENTERX, CENTERY)

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
        walking = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    walking = 1
                elif event.key == K_LEFT:
                    walking = -1
            elif event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_LEFT:
                    walking = 0

        testball.player_move(walking)

        screen.blit(background, (0, 0))
        testball.draw(screen)
        pygame.display.flip()


if __name__ == '__main__': main()