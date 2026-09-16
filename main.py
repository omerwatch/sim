import pygame
from pygame.locals import *
import math
# from scale import Scale

GRAVITY_CONSTANT = 9.81
PIXELS_PER_METER = 25
SCREEN_X = 800
SCREEN_Y = 800

class Scales(pygame.sprite.Sprite):
    def __init__(self, colour, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((30, 100))
        self.image.fill(colour)

        x = SCREEN_X - 30

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def initialize():
        intervals = SCREEN_Y / 100

        i = 0
        arr = list()
        while i < intervals:
            c = list()
            if i % 3 == 0:
                c = tuple([170, 0, 0])
            if i % 3 == 1:
                c = tuple([0, 170, 0])
            if i % 3 == 2:
                c = tuple([0, 0, 170])

            s = Scales(c, 100 * i)
            arr.append(s)

            i += 1

        return arr 

class Vectors():
    def dotproduct(v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]

    def magnitude(v):
        return math.sqrt(v[0]**2 + v[1]**2)

class Physics_Object(pygame.sprite.Sprite):
    def __init__(self, colour, width, height, mass):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width, height))
        self.image.fill(colour)

        self.rect = self.image.get_rect()

        self.mass = mass

        self.pos = [0.0, 0.0]
        self.v = [0.0, 0.0]

        self.normal = [0.0, 1.0]
        self.normal_magnitude = Vectors.magnitude(self.normal)

        self.forces = list()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, dt):
        self.pos[0] += self.v[0] * dt
        self.pos[1] += self.v[1] * dt

        self.rect.x = int(self.pos[0] * PIXELS_PER_METER)
        self.rect.y = int(self.pos[1] * PIXELS_PER_METER)

    def apply_forces(self, dt):
        f = [0.0, 0.0]

        for fx, fy in self.forces:
            f[0] += fx
            f[1] += fy

        self.v[0] += f[0] / self.mass * dt
        self.v[1] += f[1] / self.mass * dt

        self.move(dt)

    def check_collision(self, physics_objects, dt):
        for o in physics_objects:
            if o is self:
                continue
            elif self.rect.colliderect(o.rect):
                # costheta = Vectors.dotproduct(self.normal, o.normal) / self.normal_magnitude / o.normal_magnitude
                # print("cosine between normal vectors:", costheta)
                if isinstance(o, Immovable_Object):
                    # ASSUME ELASTIC COLLISION SO NO KINETIC ENERGY LOST
                    self.v[1] = self.v[1] * -1

                    self.pos[1] = o.pos[1] - self.rect.height
                    self.rect.y = self.pos[1]

class Player(Physics_Object):
    def __init__(self, colour, width, height, mass):
        Physics_Object.__init__(self, colour, width, height, mass)

        self.forces.append((0, GRAVITY_CONSTANT * self.mass))

class Immovable_Object(Physics_Object):
    def __init__(self, colour, width, height, mass, x, y):
        Physics_Object.__init__(self, colour, width, height, mass)

        self.pos = [x / PIXELS_PER_METER, y / PIXELS_PER_METER]    
        self.rect.x = x
        self.rect.y = y

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
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

    objects = [testball, floor]

    scales = Scales.initialize()

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
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        screen.blit(background, (0, 0))

        for object in objects:
            # object.check_collision(objects, dt)
            object.apply_forces(dt)
            object.draw(screen)

        for scale in scales:
            screen.blit(scale.image, (scale.rect.x, scale.rect.y))

        pygame.display.flip()


if __name__ == '__main__': main()