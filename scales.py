import pygame
from pygame.locals import *

from constants import Constants

class Scales(pygame.sprite.Sprite):
    def __init__(self, colour, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((30, 100))
        self.image.fill(colour)

        x = Constants.SCREEN_X - 30

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def initialize():
        intervals = Constants.SCREEN_Y / 100

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

    def scales_text():
        intervals = Constants.SCREEN_Y / 100

        font = pygame.font.Font(None, 24)

        i = 0
        arr = list()
        while i < intervals - 1:
            text = font.render(str((i + 1) * 4) + "m", 1, (200, 200, 200))
            textpos = text.get_rect()
            textpos.centerx = Constants.SCREEN_X  - 60
            textpos.centery = (i + 1) * 100
            arr.append((text, textpos))
            i += 1

        return arr
