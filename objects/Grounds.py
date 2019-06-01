# -*- coding: UTF-8 -*-

import pygame

class Grounds(object):
    def __init__(self, renderingSurface, grounds, ratio):
        self.grounds = grounds
        self.renderingSurface = renderingSurface

        self.ratio = ratio

        self.thickness = 1

        self.viewport = [0,0]

    def getCeilingheight(self, object, correction, ceilingHeight = None):
        x = object.x + correction
        #search for ground
        for line in self.grounds:
            if len(line) >= 6 and line[5] == True:
                if line[0] < x < line[0] + line[2] or line[0] < x + object.width < line[0] + line[2]:
                    if line[1] <= object.y:
                        if ceilingHeight:
                            if line[1] > ceilingHeight: 
                                ceilingHeight = line[1]
                        else:
                            ceilingHeight = line[1]
        return ceilingHeight

    def getGroundheight(self, object, correction, groundHeight = None):
        x = object.x + correction
        #search for ground
        for line in self.grounds:
            if line[0] < x < line[0] + line[2] or line[0] < x + object.width < line[0] + line[2]:
                if line[1] >= object.y + object.height:
                    if groundHeight:
                        if line[1] < groundHeight: 
                            groundHeight = line[1]
                    else:
                        groundHeight = line[1]
        return groundHeight

    def getWallPos(self, object, correction, wallinit):
        y = object.y + correction
        #prevent going throw ground
        wall = wallinit
        for line in self.grounds:
            if len(line) <= 4 or line[4] == False:
                if  y + object.height > line[1] > y:
                        if line[0] + line[2] <= object.x and (wall[1] == None or line[0] + line[2] > wall[1]):
                            wall[1] = line[0] + line[2]
                        elif line[0] >= object.x + object.width and (wall[0] == None or line[0] < wall[0]):
                            wall[0] = line[0]
        return wall

    def load(self, data, position):
        for ground in data:
            ground[0] *= self.ratio[1]
            ground[0] += position
            ground[1] *= self.ratio[1]
            ground[2] *= self.ratio[1]

            ground[0] = int(ground[0])
            ground[1] = int(ground[1])
            ground[2] = int(ground[2])

            self.grounds.append(ground)

    def render(self):
        rightx = 0
        outtaview = []
        for line in self.grounds:
            pygame.draw.line(self.renderingSurface, line[3], (line[0]-self.viewport[0],line[1]-self.viewport[1]),(line[0] + line[2]-self.viewport[0],line[1]-self.viewport[1]), self.thickness)
            if line[0] + line[2]-self.viewport[0] < 0:
                outtaview.append(line)
            elif line[0] + line[2] > rightx:
                rightx = line[0] + line[2]
        for entry in outtaview:
            self.grounds.remove(entry)
        return rightx