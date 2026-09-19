import pygame
from pygame.locals import *
import math

from scales import Scales
from constants import Constants

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

        self.width = width
        self.height = height

        self.is_sleeping = False
        self.allowed_sleep = False
        self.kinetic_energy = list()

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

        self.rect.x = int(self.pos[0] * Constants.PIXELS_PER_METER)
        self.rect.y = int(self.pos[1] * Constants.PIXELS_PER_METER)

    def apply_forces(self, dt):
        if isinstance(self, Player):
            self.forces.append((0, Constants.GRAVITY_CONSTANT * self.mass, "gravity"))

        f = [0.0, 0.0]

        for fx, fy, id in self.forces:
            f[0] += fx
            f[1] += fy

        self.v[0] += f[0] / self.mass * dt
        self.v[1] += f[1] / self.mass * dt

        if self.is_sleeping:
            self.v[0] = 0
            self.v[1] = 0

        self.kinetic_energy.append(0.5 * self.mass * Vectors.magnitude(self.v) ** 2)
        if len(self.kinetic_energy) > 10:
            self.kinetic_energy.pop(0)

        self.move(dt)

        self.forces = list()

    def check_collision(self, physics_objects):
        for o in physics_objects:
            if o is self:
                continue
            elif self.rect.colliderect(o.rect):
                # costheta = Vectors.dotproduct(self.normal, o.normal) / self.normal_magnitude / o.normal_magnitude
                # print("cosine between normal vectors:", costheta)
                if isinstance(o, Immovable_Object):
                    # modelling ground as a spring with a restoring and damping force
                    pen = [0.0, 0.0]
                    pen[1] = self.pos[1] + self.height / Constants.PIXELS_PER_METER - o.pos[1]

                    f_restoring = o.k * pen[1] * -1
                    f_damping = o.c * self.v[1] * -1

                    f_spring = f_restoring + f_damping
                    if f_spring > 0:
                        f_spring = 0

                    self.allowed_sleep = True
                    self.check_kinetic_energy()

                    # i = 0
                    # first_frame = True
                    # for fx, fy, id in self.forces:
                    #     if id == "ground contact force":
                    #         first_frame = False
                    #         self.forces[i] = ((0, f_spring), "ground contact force")
                    #     i += 1

                    # if first_frame:
                    self.forces.append((0, f_spring, "ground contact force"))

    def check_kinetic_energy(self):
        if not self.allowed_sleep:
            return

        for e in self.kinetic_energy:
            if e > Constants.KINETIC_ENERGY_THRESHOLD:
                self.is_sleeping = False
                print(e)
                return

        self.is_sleeping = True

                    

class Player(Physics_Object):
    def __init__(self, colour, width, height, mass):
        Physics_Object.__init__(self, colour, width, height, mass)

class Immovable_Object(Physics_Object):
    def __init__(self, colour, width, height, mass, x, y):
        Physics_Object.__init__(self, colour, width, height, mass)

        self.pos = [x / Constants.PIXELS_PER_METER, y / Constants.PIXELS_PER_METER]    
        self.rect.x = x
        self.rect.y = y

        self.k = 40000.0
        self.c = 400.0

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((Constants.SCREEN_X, Constants.SCREEN_Y))
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

    testball = Player((0, 0, 0), 50, 100, 10)

    floor = Immovable_Object((0, 100, 0), 800, 100, 1000, 0, 700)

    objects = [testball, floor]

    scales = Scales.initialize()
    scales_text = Scales.scales_text()

    # Display some text
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
        dt = clock.tick(120) / 1000

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        screen.blit(background, (0, 0))

        for object in objects:
            if not object.is_sleeping:
                object.check_collision(objects)
                object.apply_forces(dt)
            object.draw(screen)

        for scale in scales:
            screen.blit(scale.image, (scale.rect.x, scale.rect.y))

        for t, pos in scales_text:
            screen.blit(t, pos)

        pygame.display.flip()


if __name__ == '__main__': main()