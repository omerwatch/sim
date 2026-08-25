import pygame
from pygame.locals import *
import math

GRAVITY_CONSTANT = 200

class Physics_Object(pygame.sprite.Sprite):
    def __init__(self, colour, width, height, mass):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width, height))
        self.image.fill(colour)

        self.rect = self.image.get_rect()

        self.mass = mass

        self.pos = [0.0, 0.0]
        self.v = [0.0, 0.0]

        self.forces = list()

    def draw(self, screen):
        self.rect.x = int(self.pos[0])
        self.rect.y = int(self.pos[1])

        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, dt):
        self.pos[0] += self.v[0] * dt
        self.pos[1] += self.v[1] * dt

    def apply_forces(self, dt):
        f = [0.0, 0.0]

        for fx, fy in self.forces:
            f[0] += fx
            f[1] += fy

        self.v[0] += f[0] / self.mass * dt
        self.v[1] += f[1] / self.mass * dt

        self.move(dt)

class Player(Physics_Object):
    def __init__(self, colour, width, height, mass):
        Physics_Object.__init__(self, colour, width, height, mass)

        self.forces.append((0, GRAVITY_CONSTANT * self.mass))

class Immovable_Object(Physics_Object):
    def __init__(self, colour, width, height, mass, x, y):
        Physics_Object.__init__(self, colour, width, height, mass)

        self.pos = [x, y]    

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('RIGID BODY SIMULATOR')

    clock = pygame.time.Clock()

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 50, 100))

    CENTERX = background.get_rect().centerx
    CENTERY = background.get_rect().centery

    # floor = pygame.Rect(0, 700, 800, 100)
    # pygame.draw.rect(background, (0, 100, 0), floor)

    testball = Player((0, 0, 0), 50, 50, 10)

    floor = Immovable_Object((0, 100, 0), 800, 100, 1000, 0, 700)

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
        dt = clock.tick() / 1000

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        testball.apply_forces(dt)
        floor.apply_forces(dt)

        screen.blit(background, (0, 0))
        testball.draw(screen)
        floor.draw(screen)

        pygame.display.flip()


if __name__ == '__main__': main()