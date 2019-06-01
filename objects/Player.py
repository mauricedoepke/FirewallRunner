# -*- coding: UTF-8 -*-

import pygame

class Player(object):


    def __init__(self, renderingSurface, x = 30, y = 0, width = 40, height = 90, color = (64, 169, 64),life = True, speed = 5, thickness = 3, ratio = (1, 1)):
        #init variables
        self.renderingSurface = renderingSurface

        self.offset = 5
        self.thickness = thickness

        self.player = True
        self.living = True
        self.life  = life

        self.coins = 0

        self.x = x
        self.y = y
        self.ratio = ratio
        self.width = int(round(ratio[1] * width))
        self.height = int(round(ratio[1] * height))
        self.viewport = [0, 0]

        self.speed = speed
        self.maxStepwide = 12
        self.moving = [0,0]
        self.specMoving = []
        self.mode = "run"

        self.jumpEnergy = 5 
        self.minJumpEnergy = 5
        self.maxJumpEnergy = 6.5
        self.superjumpEnergy = 5
        self.affectedByGravity = True

        self.color = color

        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey((255,0,255))

        #calc variables
        self.actualStepwide = 0
        self.stepwideFactor = self.speed

        self.jumping = False
        self.superJump = False
        self.turning = False
        self.onGround = False
        self.standOnGround = False
        self.superJumpenabled = False

        self.jumpTime = 0
        self.turningAngle = 360

        self.timer = 1

        self.rect = pygame.Rect((self.x,self.y),(self.width,self.height))

    def turn(self):
        if not self.turning:
            self.turningAngle = 360
            self.turning = True

    def jump(self, sound = None):
        if not self.jumping and self.standOnGround:
            self.jumping = True
            if sound != None:
                sound.play()
        elif self.jumping and not self.standOnGround and not self.superJump and self.superJumpenabled:
            self.superJump = True
            if sound != None:
                sound.play()

    def goForward(self):
        self.speed = abs(self.speed)
        self.mode = "run"

    def goBackward(self):
        self.speed = -abs(self.speed)
        self.mode = "run"

    def stop(self):
        self.moving[0] = 0
        self.mode = None

    def calcMoving(self):
        self.moving = [0, 0]
        if self.mode == "run":
            self.moving[0] += self.timer * self.speed * self.ratio[1] * 2

        for move in self.specMoving:
            self.moving[0] += self.timer * move[0]
            self.moving[1] += self.timer * move[1]

        self.specMoving = []

    #from http://www.pygame.org/wiki/RotateCenter
    def rot_center(self, image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

    def render(self):
        self.surface.fill((255,0,255))

        #leg movement
        self.stepwideFactor = self.speed if self.stepwideFactor > 0 else -self.speed
        if self.mode == "run":
            self.actualStepwide -= self.timer * self.stepwideFactor
            if self.actualStepwide <= 0:
                self.actualStepwide = 0
                self.stepwideFactor *= -1
            elif self.actualStepwide >= self.maxStepwide:
                self.actualStepwide = self.maxStepwide
                self.stepwideFactor *= -1
        else:
            self.actualStepwide = 0

        #arme
        pygame.draw.line(self.surface, self.color, (self.offset+self.maxStepwide - int(round(self.actualStepwide)),60),(self.offset+self.maxStepwide,40), self.thickness)
        pygame.draw.line(self.surface, self.color, (self.offset+self.maxStepwide + int(round(self.actualStepwide)),60),(self.offset+self.maxStepwide,40), self.thickness)
        #beine
        pygame.draw.line(self.surface, self.color, (self.offset+int(round(self.actualStepwide)),90),(self.offset+self.maxStepwide,65), self.thickness)
        pygame.draw.line(self.surface, self.color, (self.offset+self.maxStepwide*2-int(round(self.actualStepwide)),90),(self.offset+self.maxStepwide,65), self.thickness)
        #lörper
        pygame.draw.line(self.surface, self.color, (self.offset+self.maxStepwide,65),(self.offset+self.maxStepwide,30), self.thickness)
        #kopf
        pygame.draw.circle(self.surface, self.color, (self.offset+self.maxStepwide,15),15,self.thickness)

        #scaling
        surfacebuffer = pygame.transform.scale(self.surface, (self.width,self.height))

        #turning
        rect = None
        if self.turning:
            surfacebuffer, rect = self.rot_center(surfacebuffer, pygame.Rect((self.x - self.viewport[0],self.y - self.viewport[1]), (self.width,self.height)), self.turningAngle)#pygame.transform.rotate(surfacebuffer, self.turningAngle)
            self.turningAngle -= self.timer * 10
            if self.turningAngle <= 0:
                self.turning = False

        self.renderingSurface.blit(surfacebuffer,rect if not rect == None else (self.x - self.viewport[0],self.y - self.viewport[1]))