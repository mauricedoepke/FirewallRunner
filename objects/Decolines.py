# -*- coding: UTF-8 -*-

import pygame

class Decolines(object):
    def __init__(self, renderingSurface, decolines, ratio):
        #it is a class to managa all decolines
        #decolines are lines to improve the look of the game and do not interact with the gam physics in any way
        self.decolines = decolines
        self.renderingSurface = renderingSurface

        self.ratio = ratio

        self.thickness = 3

        self.viewport = [0,0]

    def load(self, data, position):
        #loads decolines from a list (their storage format in the level files)
        #resizes them an correct their position to get appended after the levelpart before
        for decoline in data:
            decoline[0] *= self.ratio[1]
            decoline[0] += position

            decoline[1] *= self.ratio[1]

            decoline[2] *= self.ratio[1]
            decoline[2] += position

            decoline[3] *= self.ratio[1]
            decoline[5] *= self.ratio[1] * 2

            decoline[0] = int(decoline[0])
            decoline[1] = int(decoline[1])
            decoline[2] = int(decoline[2])
            decoline[3] = int(decoline[3])
            decoline[5] = int(decoline[5])

            self.decolines.append(decoline)  

    def render(self, z):
        #render the given layer of decolines
        #there are different 3 layers
        #---decolines that are overpainted by everything else
        #---decolines that overpaint every other lines but not the player or other game objects
        #---decolines that overpaint everything
        for line in self.decolines:
            if line[4] == z:
                pygame.draw.line(self.renderingSurface, line[6], (line[0]-self.viewport[0], line[1]-self.viewport[1]), (line[2]-self.viewport[0], line[3]-self.viewport[1]), line[5]) 