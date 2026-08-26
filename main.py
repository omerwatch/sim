import pygame
from pygame.locals import *
import math

GRAVITY_CONSTANT = 200

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

        self.cidx = -1

        self.normal = [0.0, 1.0]
        self.normal_magnitude = Vectors.magnitude(self.normal)

        self.forces = list()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, dt):
        self.pos[0] += self.v[0] * dt
        self.pos[1] += self.v[1] * dt

        self.rect.x = int(self.pos[0])
        self.rect.y = int(self.pos[1])

    def apply_forces(self, dt):
        f = [0.0, 0.0]

        for fx, fy in self.forces:
            f[0] += fx
            f[1] += fy

        self.v[0] += f[0] / self.mass * dt
        self.v[1] += f[1] / self.mass * dt

        self.forces = self.forces[0:self.cidx]

        self.move(dt)

    def check_collision(self, physics_objects, dt):
        self.cidx = len(self.forces)
        for o in physics_objects:
            if o is self:
                continue
            elif self.rect.colliderect(o.rect):
                # costheta = Vectors.dotproduct(self.normal, o.normal) / self.normal_magnitude / o.normal_magnitude
                # print("cosine between normal vectors:", costheta)
                if isinstance(o, Immovable_Object):
                    # colliding with the ground so reaction force from IMPULSE (integral of F dt but assuming F is constant for now)
                    f = [self.mass * self.v[0] / dt, self.mass * self.v[1] / dt]
                    self.forces.append(f)
                    print(f)


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

    objects = [testball, floor]

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

        screen.blit(background, (0, 0))

        for object in objects:
            object.check_collision(objects, dt)
            object.apply_forces(dt)
            object.draw(screen)

        pygame.display.flip()


if __name__ == '__main__': main()