import pygame
from pygame.locals import *
import os

from constants import Constants

class Force_Line(pygame.sprite.Sprite):
    def __init__(self, id, pos, width, height, fx, fy):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join("img", "forcearrow.png"))

        if fy > 0:
            self.image = pygame.transform.flip(self.image, False, True)

        self.rect = self.image.get_rect()

        self.pos = pos[:]
        self.pos[0] += (width / 2 - 5) / Constants.PIXELS_PER_METER
        self.pos[1] += height / 2 / Constants.PIXELS_PER_METER

        if fy < 0:
            self.pos[1] -= 49 / Constants.PIXELS_PER_METER

        self.rect.x = self.pos[0] * Constants.PIXELS_PER_METER
        self.rect.y = self.pos[1] * Constants.PIXELS_PER_METER

        self.fx = fx
        self.fy = fy

        

        self.id = id

    def initialize_force_lines(forces, force_lines, pos, width, height, is_sleeping):
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

        if len(forces) < len(force_lines) or is_sleeping:
            # delete items in force_lines array
            # print()
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
        font = pygame.font.Font(None, 24)
        text = font.render(str(round(self.fy, 2)) + " N", 1, (200, 200, 200))
        textpos = text.get_rect()
        textpos.centerx = self.rect.x + 75
        textpos.centery = self.rect.y + 25

        screen.blit(text, textpos)

    def move_all(force_lines, v, dt):
        # takes in a list of Force_Line objects and moves them according to the velocity of the object its attached to
        for fl in force_lines:
            fl.pos[0] += v[0] * dt
            fl.pos[1] += v[1] * dt

            fl.rect.x = int(fl.pos[0] * Constants.PIXELS_PER_METER)
            fl.rect.y = int(fl.pos[1] * Constants.PIXELS_PER_METER)

