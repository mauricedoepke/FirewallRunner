# -*- coding: UTF-8 -*-

import pygame
import random

class Stumbles(object):
    def __init__(self ,renderingSurface, stumbles, ratio, player):
        self.stumbles = stumbles
        self.renderingSurface = renderingSurface

        self.ratio = ratio
        self.thickness = 3

        self.player = player


        self.viewport = [0,0]

        self.image = pygame.image.load("graphic/olddata/1.png").convert()
        rect = self.image.get_rect()
        self.image_size = int(rect.width * self.ratio[1]), int(rect.height * self.ratio[1])
        self.image = pygame.transform.scale(self.image, (self.image_size[0], self.image_size[1]))
        self.image.set_colorkey((255,255,255))
    def stumbled(self):
        for stumble in self.stumbles: 
            r1 = pygame.Rect((stumble[0], stumble[1]), (self.image_size[0], self.image_size[1])).colliderect(self.player.rect)

            if r1:
                self.stumbles.remove(stumble)
                return True
        return False

    def load(self, data, position):
        for stumble in data:
            if random.randint(1,stumble[2]) == 1 and self.player.speed >= 3:
                stumble[0] *= self.ratio[1]
                stumble[0] += position
                stumble[1] *= self.ratio[1]
                stumble[1] -= self.image_size[1]
                self.stumbles.append(stumble)

    def render(self):
        outtaview = []
        for stumble in self.stumbles:

            self.renderingSurface.blit(self.image, (stumble[0] - self.viewport[0], stumble[1]))

            if stumble[0] + 20 - self.viewport[0] < 0:
                outtaview.append(stumble)
        for entry in outtaview:
            self.stumbles.remove(entry)