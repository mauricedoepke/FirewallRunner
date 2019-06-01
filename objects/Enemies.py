# -*- coding: UTF-8 -*-

import pygame
# are not fully integrated, yet
class Enemies(object):
    def __init__(self, renderingSurface, worldclass, enemies):
        self.enemies = []
        self.renderingSurface = renderingSurface
        self.worldclass = worldclass

        for enemie in enemies:
            enemie = Enemie(self.renderingSurface, enemie[0],enemie[1], color = enemie[2])
            self.enemies.append(enemie)

        self.thickness = 3

        self.viewport = [0,0]

    def render(self):
        for object in self.enemies:
            self.worldclass.calcGravity(object)
            object.render()
            if object.x + object.width + object.viewport[0] < 0:
                self.enemies.remove(object)
            
class Enemie(object):

    def __init__(self, renderingSurface, x = 30, y = 0, width = 40, height = 40, color = (0,0,0),life = 1, speed =0, thickness = 3):
        #init variables
        self.renderingSurface = renderingSurface

        self.offset = 5
        self.thickness = thickness

        self.player = False
        self.living = True
        self.life  = life

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.viewport = [0, 0]

        self.speed = speed
        self.moving = [0,0]

        self.jumpEnergy = 13
        self.affectedByGravity = True

        self.color = color

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.set_colorkey((255,0,255))
        self.surface.fill((255,0,255))
        ##### just a test drawing...
        pygame.draw.line(self.surface, self.color, (self.offset,38),(self.offset+30,38), self.thickness)
        pygame.draw.line(self.surface, self.color, (self.offset+15,0),(self.offset+30,38), self.thickness)
        pygame.draw.line(self.surface, self.color, (self.offset+15,0),(self.offset,38), self.thickness)

        #calc variables
        self.jumping = False
        self.onGround = False
        self.standOnGround = False

        self.jumpTime = 0
    def render(self):
        self.renderingSurface.blit(self.surface,(self.x - self.viewport[0],self.y - self.viewport[1]))