import pygame
from pygame.locals import *
import os
import math

from constants import Constants
from vectors import Vectors

# make this entire class general for all forces

class Force_Line(pygame.sprite.Sprite):
    def __init__(self, id, pos, width, height, fx, fy):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join("img", "forcearrow.png"))

        # if fy > 0:
        #     self.image = pygame.transform.flip(self.image, False, True)

        self.f = [fx, fy]

        self.pos = pos[:]
        self.pos[0] += (width / 2 - 5) / Constants.PIXELS_PER_METER
        self.pos[1] += height / 2 / Constants.PIXELS_PER_METER

        self.set_initial_position()

        self.rect = self.image.get_rect()

        self.rect.x = self.pos[0] * Constants.PIXELS_PER_METER
        self.rect.y = self.pos[1] * Constants.PIXELS_PER_METER

        self.font = pygame.font.Font(None, 24)
        self.text = self.font.render(str(round(Vectors.magnitude(self.f), 2)) + " N", 1, (200, 200, 200))
        self.textpos = self.text.get_rect()

        self.id = id

    def initialize_force_lines(forces, force_lines, pos, width, height, normal = False):
        # forces is a list of tuples (x component, y component, id)
        # this function takes this list of tuples and and the 'force lines' list for a physics object and ensures that the list is completely updated

        if len(forces) > len(force_lines):
            id_arr = list() # list of all the forces present in force_lines
            for fx, fy, id in forces:
                for fl in force_lines:
                    if id == fl.id:
                        id_arr.append(id)

            for fx, fy, id in forces:
                if not id in id_arr:
                    force_lines.append(Force_Line(id, pos, width, height, fx, fy))

        if len(forces) < len(force_lines) or normal:
            # delete items in force_lines array
            id_arr = list()
            for fx, fy, id in forces:
                id_arr.append(id)

            # need to get rid of the element whose id is not in id_arr
            i = 0
            while i < len(force_lines):
                if not force_lines[i].id in id_arr:
                    force_lines.pop(i)
                else:
                    i += 1

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # add text here showing the magnitude of the force
        self.textpos.centerx = self.rect.x + 75
        self.textpos.centery = self.rect.y + 25

        screen.blit(self.text, self.textpos)

    def move_all(force_lines, v, dt):
        # takes in a list of Force_Line objects and moves them according to the velocity of the object its attached to
        for fl in force_lines:
            fl.pos[0] += v[0] * dt
            fl.pos[1] += v[1] * dt

            fl.rect.x = int(fl.pos[0] * Constants.PIXELS_PER_METER)
            fl.rect.y = int(fl.pos[1] * Constants.PIXELS_PER_METER)

    def snap_all(force_lines, newp, ogp):
        delta = [newp[0] - ogp[0], newp[1] - ogp[1]]
        for fl in force_lines:
            fl.pos[0] += delta[0]
            fl.pos[1] += delta[1]

        Force_Line.move_all(force_lines, [0.0, 0.0], 0)

    def set_initial_position(self):
        if self.f[1] < 0:
            self.pos[1] -= 49 / Constants.PIXELS_PER_METER

        # TO DO FOR THIS FUNCTION MAKE SURE THE ARROWS ARE IN THE RIGHT POSITION NO MATTER WHICH DIRECTION IT IS IN

        theta = math.atan2(-1 * self.f[1], self.f[0]) * 180 / math.pi - 90
        # multiplying by 180/pi to change to degrees and then adding 90 to correct the angle from how the image is loaded

        self.image = pygame.transform.rotate(self.image, theta)