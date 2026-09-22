import pygame
from pygame.locals import *

from scales import Scales
from constants import Constants
from forcelines import Force_Line
from vectors import Vectors

# need to work on making everything work GENERALLY (not just for 1-dimensional motion and collision)

class Physics_Object(pygame.sprite.Sprite):
    def __init__(self, colour, width, height, mass):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width, height))
        self.image.fill(colour)

        self.rect = self.image.get_rect()

        self.mass = mass
        self.invmass = 1 / mass

        self.width = width
        self.height = height

        self.pos = [0.0, 0.0]
        self.v = [0.0, 0.0]

        self.is_sleeping = False
        self.resting_on = list()

        self.normal = [0.0, -1.0]

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
            Force_Line.initialize_force_lines(self.forces, self.force_lines, self.pos, self.width, self.height, True)

        Force_Line.initialize_force_lines(self.forces, self.force_lines, self.pos, self.width, self.height)

        f = [0.0, 0.0]

        for fx, fy, id in self.forces:
            f[0] += fx
            f[1] += fy

        self.v[0] += f[0] * self.invmass * dt
        self.v[1] += f[1] * self.invmass * dt

        self.move(dt)

        self.forces = list()

    def check_collision(self, physics_objects, dt):
        for o in physics_objects:
            if o is self:
                continue
            elif self.rect.colliderect(o.rect):
                # costheta = Vectors.dotproduct(self.normal, o.normal) / self.normal_magnitude / o.normal_magnitude
                # print("cosine between normal vectors:", costheta)
                if isinstance(o, Immovable_Object) and not self.is_sleeping:
                    # spring force needs to push the object OUT of the ground, whichever direction that is
                    # so by finding the x vector in kx we know that the force is in the opposite 
                    # you 100% know that the x vector is in the same direction as the normal vector of o
                    # then you use a change of base matrix (??)
                    vn, vt = Vectors.matrix_vector_multiplication(self.v, o.mx_standard_to_basis)

                    pn, pt = Vectors.matrix_vector_multiplication(self.pos, o.mx_standard_to_basis)
                    opn, opt = Vectors.matrix_vector_multiplication(o.pos, o.mx_standard_to_basis)
                    whn, wht = Vectors.matrix_vector_multiplication([self.width, self.height], o.mx_standard_to_basis)

                    delta = 0.0

                    if pn > opn:
                        # this means that the ground is underneath the physics object
                        delta = pn + whn / Constants.PIXELS_PER_METER - opn

                    # modelling ground as a spring with a restoring and damping force
                    # delta = [0.0, 0.0]
                    # delta[1] = self.pos[1] + self.height / Constants.PIXELS_PER_METER - o.pos[1]

                    f_restoring = o.k * delta * -1
                    f_damping = o.c * vn * -1

                    f_spring = Vectors.matrix_vector_multiplication([f_restoring + f_damping, 0], o.mx_basis_to_standard)

                    # print(f_restoring, f_damping, f_spring, self.v)

                    # check to see if ball will speed up from hitting the ground because thats impossible in real life (too expensive to compute)

                    # project the velocity vector of self onto the normal vector of o, then get the magnitude
                    if abs(vn) < Constants.VELOCITY_THRESHOLD and delta < 0.1:
                        #snap the position of the object and set velocity to 0 in normal direction somehow
                        self.v = Vectors.matrix_vector_multiplication([0, vt], o.mx_basis_to_standard)
                        self.snap_position(Vectors.matrix_vector_multiplication([opn - whn / Constants.PIXELS_PER_METER, pt], o.mx_basis_to_standard))
                        self.is_sleeping = True
                        self.resting_on.append(o)
                        continue

                    self.forces.append((f_spring[0], f_spring[1], "ground contact force"))

    def normal_force(self):
        # make this general
        if not self.resting_on:
            return
        
        f = [0.0, 0.0]
        normal_force = list()
        for fx, fy, id in self.forces:
            f[0] += fx
            f[1] += fy
        for o in self.resting_on:
            fn, ft = Vectors.matrix_vector_multiplication(f, o.mx_standard_to_basis)
            normal_force = Vectors.scalar_vector_multiplication(o.normal, abs(fn))

        self.forces.append((normal_force[0], normal_force[1], "normal force"))

    def snap_position(self, pos):
        Force_Line.snap_all(self.force_lines, pos, self.pos)

        self.pos = pos

        self.rect.x = int(self.pos[0] * Constants.PIXELS_PER_METER)
        self.rect.y = int(self.pos[1] * Constants.PIXELS_PER_METER)

class Player(Physics_Object):
    def __init__(self, colour, width, height, mass, x, y):
        Physics_Object.__init__(self, colour, width, height, mass)

        self.pos = [x / Constants.PIXELS_PER_METER, y / Constants.PIXELS_PER_METER]    
        self.rect.x = x
        self.rect.y = y

class Immovable_Object(Physics_Object):
    def __init__(self, colour, width, height, mass, x, y, normal = [0, -1]):
        Physics_Object.__init__(self, colour, width, height, mass)

        self.pos = [x / Constants.PIXELS_PER_METER, y / Constants.PIXELS_PER_METER]    
        self.rect.x = x
        self.rect.y = y

        self.k = 40000.0
        self.c = 400.0

        self.normal = normal

        self.mx_basis_to_standard = [self.normal, Vectors.return_perpendicular(self.normal)]
        self.mx_standard_to_basis = Vectors.return_transverse(self.mx_basis_to_standard) # QR Factorization

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

    floor = Immovable_Object((0, 100, 0), 800, 100, 1000, 0, 700, [2**(1/2) / 2, -2**(1/2) / 2])
    # [2**(1/2) / 2, -2**(1/2) / 2]

    objects = [floor,  testball]

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