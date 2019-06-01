# -*- coding: UTF-8 -*-

import pygame

class Walls(object):
    def __init__(self, renderingSurface, walls, ratio):
        self.walls = walls
        self.renderingSurface = renderingSurface

        self.ratio = ratio

        self.thickness = 1

        self.viewport = [0,0]

    def getGroundheight(self, object, correction, groundHeight = None):
        x = object.x + correction
        #search for ground
        for line in self.walls:
            if x < line[0] < x + object.width:
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
        if object.living:
            for line in self.walls:
                if line[1] < y < line[1] + line[2] or line[1] < y + object.height < line[1] + line[2] or y < line[1] < y + object.height or y < line[1] + line [2]< y + object.height:
                    if line[0] <= object.x and (wall[1] == None or line[0] > wall[1]):
                        wall[1] = line[0]
                    elif line[0] >= object.x + object.width and (wall[0] == None or line[0] < wall[0]):
                        wall[0] = line[0]
        return wall

    def getCeilingheight(self, object, correction, ceilingHeight = None):
        x = object.x + correction
        for line in self.walls:
            if x < line[0] < x + object.width:
                if line[1] <= object.y:
                    if ceilingHeight is None or ceilingHeight < line[1] + line[2]:
                        ceilingHeight = line[1] + line[2]
        return ceilingHeight

    def load(self, data, position):
        for wall in data:
            wall[0] *= self.ratio[1]
            wall[0] += position 
            wall[1] *= self.ratio[1]
            wall[2] *= self.ratio[1]

            wall[0] = int(wall[0])
            wall[1] = int(wall[1])
            wall[2] = int(wall[2])

            self.walls.append(wall)

    def render(self):
        rightx = 0
        outtaview = []
        for line in self.walls:
            pygame.draw.line(self.renderingSurface, line[3], (line[0]-self.viewport[0],line[1]-self.viewport[1]),(line[0] - self.viewport[0],line[1] + line[2] - self.viewport[1]), self.thickness)
            if line[0] - self.viewport[0] < 0:
                outtaview.append(line)
            elif line[0] > rightx:
                rightx = line[0]
        for entry in outtaview:
            self.walls.remove(entry)
        return rightx