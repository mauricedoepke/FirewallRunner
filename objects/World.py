# -*- coding: UTF-8 -*-

#standart lib
import pygame

#game objects
from Player import Player
from Decolines import Decolines
from Grounds import Grounds
from Walls import Walls
from Stumbles import Stumbles
from PowerUps import PowerUp, PowerUps
from Enemies import Enemie, Enemies
from animatedPng import animatedPng
from levelloader import levelloader

class World(object):

    def __init__(self,renderingSurface,bgcolor = (0, 0, 0), size = (1280,720),thickness = 3, autoscroll = [2,0], ratio = (1, 1), successound = None):
        self.renderingSurface = renderingSurface
        self.surface = pygame.Surface(size)
        self.ratio = ratio
        self.bgcolor = bgcolor

        self.spawnpoint = 600 * ratio[1] , 200 * ratio[1]

        self.player = Player(self.surface, x = self.spawnpoint[0], y = self.spawnpoint[1], speed = autoscroll[0], ratio = self.ratio)
        self.flamewall = animatedPng(self.renderingSurface, "./graphic/flamewall", 50, (40, size[1]))
        self.raspberry = pygame.image.load("graphic/raspberry.png").convert()
        self.raspberry = pygame.transform.scale(self.raspberry, (int(100*ratio[1]),int(126*ratio[1])))
        self.raspberry.set_colorkey((255,255,255))

        #self.ground = (x,y,length,(r,b,g))
        #self.walls = (x,y,height,(r,b,g)) height nach unten gerichtet
        #self.decolines = [x1, y1, x2, y2, z, thickness,(r,g,b)]
        #self.texts = [x,y, "text", size, [r,g,b]]
        #self.coins = (x,y,(r,b,g), wert)

        self.ground = [[1, 600 * self.ratio[1] , 800, [64, 169, 64]]]
        self.stumble = []

        self.walls = []
        self.decolines = []
        self.powerups = []#[[1200,500,"random"], [1400,500,"random"], [1800,500,"random"]]
        self.enemies = []

        self.groundManager = Grounds(self.surface, self.ground, self.ratio)
        self.wallManager = Walls(self.surface, self.walls, self.ratio)
        self.decolineManager = Decolines(self.surface, self.decolines, self.ratio)
        self.PowerUpManager = PowerUps(self.surface, self, self.powerups, self.ratio, successound)
        self.enemieManager = Enemies(self.surface, self,self.enemies) # are not fully integrated, yet
        self.stumbleManager = Stumbles(self.surface, self.stumble, self.ratio, self.player)

        self.partloader = levelloader()

        self.gravity = 0.3
        self.thickness = thickness

        self.viewport = [0,0]
        self.speedlencounter = self.viewport[0]
        self.autoscroll = autoscroll
        self.size = size

        self.genHeight = 200
        self.genWide = 80
        self.points = 0
        self.pointmultiplier = 1

        self.maxSpeedPoints = 40000
        self.speedStep = 10000
        self.timer = 1 

    def setTimer(self, timer):
        self.timer = timer
        self.player.timer = timer

    def calcYmoving(self, object, correction = 0):
        possibleMoving = [None, None]
        moving = 0

        #get groundheights
        groundHeight = self.groundManager.getGroundheight(object, correction)
        groundHeight = self.wallManager.getGroundheight(object, correction, groundHeight)

        if groundHeight != None:
            possibleMoving[0] = groundHeight - (object.y + object.height)
        else:
            possibleMoving[0] = None

        #search for ceiling
        ceilingHeight = self.wallManager.getCeilingheight(object, correction)
        ceilingHeight = self.groundManager.getCeilingheight(object, correction, ceilingHeight)

        if ceilingHeight != None:
            possibleMoving[1] = -(object.y - ceilingHeight)
        else:
            possibleMoving[1] = None


        #calc real y moving
        if object.moving[1] > 0:
            if possibleMoving[0] == None or object.moving[1] < possibleMoving[0]:
                moving = object.moving[1]
            else:
                moving = possibleMoving[0]
        else:
            if possibleMoving[1] == None or object.moving[1] > possibleMoving[1]:
                moving = object.moving[1]
            else:
                moving = possibleMoving[1]

        return moving, possibleMoving

    def calcXmoving(self, object, correction = 0):
        possibleMoving = [None, None]
        moving = 0

        #calc possbile x moving
        wallpos = self.wallManager.getWallPos(object, correction,[None, None])
        wallpos = self.groundManager.getWallPos(object, correction, wallpos)

        if wallpos[0] != None:
            possibleMoving[0] = wallpos[0] - (object.x + object.width)
        if wallpos[1] != None:
            possibleMoving[1] = -(object.x - wallpos[1])


        #calc real x moving
        if object.moving[0] > 0:
            if possibleMoving[0] == None or object.moving[0] < possibleMoving[0]:
                moving = object.moving[0]
            else:
                moving = possibleMoving[0]
        else:
            if possibleMoving[0][1] == None or object.moving[0] > possibleMoving[1]:
                moving = object.moving[0]
            else:
                moving = possibleMoving[1] 

        return moving, possibleMoving

    def calcGravity(self, object, list = None):
        #calc all movings
        if object.jumping: #jumping
            object.specMoving.append((0, self.ratio[1] * 2 * (-(object.jumpEnergy + (object.superjumpEnergy if object.superJump else 0)))))

        if object.affectedByGravity and not object.standOnGround: #gravity
            object.specMoving.append((0, self.ratio[1] * 2 * (self.gravity * object.jumpTime *self.timer)))
            object.jumpTime += 1

        object.calcMoving()



        #calc possible moving
        #calc possbile y moving
        possibleMoving = [0,0]
        moving = [0, 0]


        if abs(object.moving[0]) > abs(object.moving[1]):
            moving[0], possibleMoving[0] = self.calcXmoving(object)
            moving[1], possibleMoving[1] = self.calcYmoving(object, moving[0])#y berechnung anpassen
        else:
            moving[1], possibleMoving[1] = self.calcYmoving(object) 
            moving[0], possibleMoving[0] = self.calcXmoving(object, moving[1])#x berechnung anpassen
      

        #check if stands on Ground
        if possibleMoving[1][0] == moving[1]:
            object.standOnGround = True
            object.jumping = False
            object.superJump = False
            object.jumpTime = 0
            object.jumpEnergy = object.minJumpEnergy
        elif possibleMoving[1][1] == moving[1] and object.moving[1] < 0: #check if hangs under ceiling
            object.jumping = False
            object.superJump = False
            object.jumpTime = 0
            object.standOnGround = False
            object.jumpEnergy = object.minJumpEnergy
        else:
            object.standOnGround = False

        #do real moving
        object.y += moving[1]
        object.x += moving[0]

        #fallen down
        if object.y > self.size[1]:
            if not object.player:
                list.remove(object)

        if object.player:
            #prevent walking outside at left side
            if object.x  - self.viewport[0] < 25 or object.y > self.size[1]:
                object.life = False
            self.autoscroll[0] = 2 + (float(self.speedlencounter) / float(self.speedStep))
            object.speed = self.autoscroll[0]
            #get Coins
            self.PowerUpManager.power()
            self.PowerUpManager.collectPowerUps()

            if self.stumbleManager.stumbled():
                self.speedlencounter = self.speedlencounter - self.speedStep if not self.speedlencounter < self.speedStep else 0
                self.player.jumpTime = 0
                superbuffer = self.player.superJumpenabled
                self.player.superJump = False
                self.player.superJumpenabled = False
                self.player.jump()
                self.player.turn()
                self.player.superJumpenabled = superbuffer

            self.player.rect.left = object.x
            self.player.rect.top = object.y




        #update viewports
        object.viewport = self.viewport
        self.wallManager.viewport = self.viewport
        self.groundManager.viewport = self.viewport
        self.PowerUpManager.viewport = self.viewport
        self.decolineManager.viewport = self.viewport
        self.stumbleManager.viewport = self.viewport
        


    def render(self):
        self.surface.fill(self.bgcolor)
        #do autoscroll
        self.viewport[0] += self.timer * self.autoscroll[0] * self.ratio[1] * 2
        self.viewport[1] += self.timer * self.autoscroll[1] * self.ratio[1] * 2
        self.speedlencounter = self.speedlencounter + self.timer * self.autoscroll[0] if self.speedlencounter + self.timer * self.autoscroll[0] <= self.maxSpeedPoints  else self.maxSpeedPoints

        #render gameobjects
        self.decolineManager.render(0)
        position = self.groundManager.render()
        posbuffer = self.wallManager.render()
        self.PowerUpManager.render()
        self.PowerUpManager.renderBar()
        self.decolineManager.render(1)

        self.calcGravity(self.player)
        self.player.render()

        self.stumbleManager.render()
        self.decolineManager.render(2)
        self.renderingSurface.blit(self.surface,(0,0))

        self.renderingSurface.blit(self.raspberry, (50, 0))
        self.flamewall.render(0, 0)

        if posbuffer > position:
            position = posbuffer
        self.generateWorld(position)
        self.points += self.pointmultiplier * self.timer * (self.player.speed/2) ** 2

    def generateWorld(self, position):
        if self.viewport[0] + self.size[0] + 200 > position:
            partbuffer = self.partloader.getRandPart(self.player.speed)

            self.groundManager.load(partbuffer["grounds"], position)
            self.wallManager.load(partbuffer["walls"], position)
            self.decolineManager.load(partbuffer["decolines"], position)
            self.stumbleManager.load(partbuffer["stumbles"], position)
            self.PowerUpManager.load(partbuffer["powerups"], position)

            """for enemie in json.loads(file.readline()):
                enemie[0] *= ratio[0]
                enemie[0] += position
                enemie[1] *= ratio[1]
                enemie[2] *= ratio[0]

                enemie[0] = int(enemie[0])
                enemie[1] = int(enemie[1])
                enemie[2] = int(enemie[2])

                self.enemieManager.enemies.append(enemie)"""           