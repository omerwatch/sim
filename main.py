import pygame
from pygame.locals import *
import math

from scales import Scales
from constants import Constants
from forcelines import Force_Line

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

        self.pos = [0.0, 0.0]
        self.v = [0.0, 0.0]

        self.v_before_impact = 0.0
        self.impacting = False
        self.is_sleeping = False

        self.normal = [0.0, 1.0]
        self.normal_magnitude = Vectors.magnitude(self.normal)

        self.forces = list()
        self.force_lines = list()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, dt):
        self.pos[0] += self.v[0] * dt
        self.pos[1] += self.v[1] * dt

        self.rect.x = int(self.pos[0] * Constants.PIXELS_PER_METER)
        self.rect.y = int(self.pos[1] * Constants.PIXELS_PER_METER)

        Force_Line.move_all(self.force_lines, self.v, dt)

    def apply_forces(self, dt):
        if isinstance(self, Player):
            self.forces.append((0, Constants.GRAVITY_CONSTANT * self.mass, "gravity"))
        if self.is_sleeping:
            self.normal_force()

        Force_Line.initialize_force_lines(self.forces, self.force_lines, self.pos, self.width, self.height, self.is_sleeping)

        f = [0.0, 0.0]

        for fx, fy, id in self.forces:
            f[0] += fx
            f[1] += fy

        self.v[0] += f[0] / self.mass * dt
        self.v[1] += f[1] / self.mass * dt

        self.move(dt)

        if not self.impacting:
            self.v_before_impact = self.v[1]

        self.forces = list()

    def check_collision(self, physics_objects, dt):
        self.impacting = False
        for o in physics_objects:
            if o is self:
                continue
            elif self.rect.colliderect(o.rect):
                # costheta = Vectors.dotproduct(self.normal, o.normal) / self.normal_magnitude / o.normal_magnitude
                # print("cosine between normal vectors:", costheta)
                if isinstance(o, Immovable_Object) and not self.is_sleeping:
                    # modelling ground as a spring with a restoring and damping force
                    pen = [0.0, 0.0]
                    pen[1] = self.pos[1] + self.height / Constants.PIXELS_PER_METER - o.pos[1]

                    f_restoring = o.k * pen[1] * -1
                    f_damping = o.c * self.v[1] * -1

                    f_spring = f_restoring + f_damping
                    if f_spring > 0:
                        f_spring = 0

                    # check to see if ball will speed up from hitting the ground because thats impossible in real life
                    if self.v[1] + f_spring / self.mass * dt > self.v_before_impact:
                        f_spring = 0

                    # project the velocity vector of self onto the normal vector of o, then get the magnitude
                    if abs(self.v[1]) < Constants.VELOCITY_THRESHOLD and pen[1] < 0.4:
                        #snap the position of the object
                        self.pos[1] = o.pos[1] - self.height / Constants.PIXELS_PER_METER
                        self.v[1] = 0
                        self.is_sleeping = True
                        continue

                    self.impacting = True
                    self.forces.append((0, f_spring, "ground contact force"))

    def normal_force(self):
        self.forces.append((0, -1 * Constants.GRAVITY_CONSTANT * self.mass, "normal force"))

class Player(Physics_Object):
    def __init__(self, colour, width, height, mass, x, y):
        Physics_Object.__init__(self, colour, width, height, mass)

        self.pos = [x / Constants.PIXELS_PER_METER, y / Constants.PIXELS_PER_METER]    
        self.rect.x = x
        self.rect.y = y

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

    testball = Player((0, 0, 0), 10, 10, 10, 0, 0)
    testball2 = Player((250, 250, 250), 10, 10, 10, 400, 0)

    floor = Immovable_Object((0, 100, 0), 800, 100, 1000, 0, 700)

    objects = [floor, testball2, testball]

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
            object.check_collision(objects, dt)
            object.apply_forces(dt)
            object.draw(screen)

            for fl in object.force_lines:
                fl.draw(screen)

        for scale in scales:
            screen.blit(scale.image, (scale.rect.x, scale.rect.y))

        for t, pos in scales_text:
            screen.blit(t, pos)

        pygame.display.flip()


if __name__ == '__main__': main()