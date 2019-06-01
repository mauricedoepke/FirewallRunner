# -*- coding: UTF-8 -*-

import pygame
import glob
import datetime
import os

class animatedPng(object):
    def __init__(self, renderingSurface, folderpath, pause, resize = None, ratio = None, colorkey = (0,0,0)):
        #a class to animate sets of png's
        self.images = []

        savedPath = os.getcwd()
        os.chdir(folderpath)
        #gets all pngs's in the given path, converts, resizes and saves them in self.images
        for filename in glob.glob('*.png'):
            buffer = pygame.image.load(filename).convert()
        
            if resize != None:
                buffer = pygame.transform.scale(buffer, resize)
                rect = pygame.Rect((0,0), resize)
            elif ratio != None:
                rect = buffer.get_rect()
                rect.width *= ratio[1]
                rect.height *= ratio[1]

                rect.height = int(rect.height)
                rect.width = int(rect.width)

                buffer = pygame.transform.scale(buffer, (rect.width, rect.height))

            buffer.set_colorkey(colorkey)
            self.images.append(buffer)
        os.chdir(savedPath)

        self.renderingSurface = renderingSurface

        self.pause = datetime.timedelta(milliseconds = pause)
        self.lastshown = datetime.datetime.now() #time of last picture change

        self.index = 0
        self.count = len(self.images)

        self.size = rect.width, rect.height

    def render(self, x, y):
        #if the last picture in list is reaged then start over
        if self.index == self.count:
            self.index = 0
        #blits the image on the renderingsurface at the given coordinates
        self.renderingSurface.blit(self.images[self.index], (x, y))

        #jump to the next image in list, when the pause is equal or higher the given one between to images
        now = datetime.datetime.now()
        if now - self.lastshown >= self.pause:
            self.index += 1
            self.lastshown = now