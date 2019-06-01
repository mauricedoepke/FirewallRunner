# -*- coding: UTF-8 -*-

import pygame
import datetime
import random

from animatedPng import animatedPng

class PowerUps(object):
    def __init__(self, renderingSurface, worldclass, powerups, ratio, successound):
        #this ist the powerup manager, it provides all necessery functions to use them in the game
        self.powerUps = []
        self.renderingSurface = renderingSurface
        self.worldclass = worldclass
        self.successound = successound

        self.types = { "multiplier" : Multiplier, "forwarder" : Forwarder, "superjump" : Superjump}
        self.type_keys = self.types.keys()
        self.actives = []

        self.ratio = ratio

        self.load(powerups, 0)

        self.thickness = 3
        self.viewport = [0,0] 

        self.pause = False  
        self.pausetime = None   

    def load(self, data, position):
        count = len(self.type_keys) -1
        for powerUp in data: 
            if random.randint(1,powerUp[3]) == 1:
                if powerUp[2] == "random":
                    powerUp[2] = self.type_keys[random.randint(0, count)]
                powerUp = self.types[powerUp[2]](self.renderingSurface, self.worldclass, powerUp[0] * self.ratio[1] + position, powerUp[1] * self.ratio[1] , self.ratio)
                self.powerUps.append(powerUp)

    def power(self):
        delete = []
        for active in self.actives:
            if active.active:
                active.power()
            else:
                delete.append(active)
        for inactive in delete:
            self.actives.remove(inactive)

    def collectPowerUps(self):
        #checks if the player collides with a power up and activates it 
        for powerUp in self.powerUps:
            doubled = False
            if self.worldclass.player.rect.colliderect(powerUp.rect):
                for active in self.actives:
                    if isinstance(active,powerUp.__class__):
                        doubled = True
                if doubled:
                    #adds the runtime of the collected power up to the actual active one if there is already one of the type active
                    active.duration += powerUp.duration
                else:
                    powerUp.powerStart()
                    self.actives.append(powerUp)
                self.successound.play()
                self.powerUps.remove(powerUp)

    def setPause(self):
        if self.pause:
            for active in self.actives:
                active.starttime += datetime.datetime.now() - self.pausetime
            self.pause = False
        else:
            self.pausetime = datetime.datetime.now()
            self.pause = True

    def renderBar(self):
        #renders the powerup Bar which is centered on top of the screen and shows the active powerups
        # + let them blink 1 second before they expire
        barwidth = 0
        for active in self.actives:
            barwidth += active.image.size[0]

        startx = float(self.worldclass.size[0]) / 2 - float(barwidth) / 2 - (len(self.actives)-1) * 10
        self.actives.sort(key=lambda x: x.last)

        for active in self.actives:
            if active.last < datetime.timedelta(seconds = 1) and datetime.datetime.now() - active.flickering >= datetime.timedelta(milliseconds = 200):
                active.visible = not active.visible
                active.flickering = datetime.datetime.now()

            if active.visible:
                active.image.render(startx, 15)
            startx += active.image.size[0] + 10

    def render(self):
        #renders all loaded powerups on the renderingsurface
        for powerUp in self.powerUps:
            powerUp.viewport = self.viewport
            powerUp.render()
            #delete powerups which are not anymore in the viewport
            if powerUp.rect.left + powerUp.rect.width - powerUp.viewport[0] < 0:
                self.powerUps.remove(powerUp)

class PowerUp(object):
    def __init__(self, renderingSurface, worldclass, x, y, duration = None):
        self.renderingSurface = renderingSurface
        self.worldclass = worldclass

        self.rect = None
        self.viewport = [0, 0]

        if duration != None:
            self.duration = datetime.timedelta(seconds = duration)
        else:
            self.duration = None

        self.active = False
        self.last = self.duration

        self.flickering = datetime.datetime.now()
        self.visible = True

    def powerStart(self):
        self.active = True
        self.starttime = datetime.datetime.now()

    def power(self):
        pass

    def powerStop(self):
        self.active = False

    def isFinished(self):
        if self.duration != None:
            if datetime.datetime.now() - self.starttime >= self.duration:
                return True
            else:
                self.last = self.duration - (datetime.datetime.now() - self.starttime)
                return False
        else:
            return False

    def render(self):
        self.image.render(self.rect.left - self.viewport[0], self.rect.top)

class Multiplier(PowerUp):
    def __init__(self, renderingSurface, worldclass, x, y, ratio):
        PowerUp.__init__(self, renderingSurface, worldclass, x, y, 10)

        self.image = animatedPng(self.renderingSurface, "graphic/multiplier", 400, ratio = ratio, colorkey = (255,255,255))
        self.rect = pygame.Rect((x, y), self.image.size)

        self.value = 2

    def powerStart(self):
        PowerUp.powerStart(self)
        self.worldclass.pointmultiplier += self.value

    def power(self):
        if self.isFinished():
            self.powerStop()

    def powerStop(self):
        PowerUp.powerStop(self)
        self.worldclass.pointmultiplier -= self.value

    def render(self):
        PowerUp.render(self)

class Forwarder(PowerUp):
    def __init__(self, renderingSurface, worldclass, x, y, ratio):
        PowerUp.__init__(self, renderingSurface, worldclass, x, y, 5)

        self.image = animatedPng(self.renderingSurface, "graphic/forward", 200, ratio = ratio, colorkey = (255,255,255))
        self.rect = pygame.Rect((x, y), self.image.size)

        self.value = 200 * ratio[1]

    def powerStart(self):
        PowerUp.powerStart(self)

    def power(self):
        self.worldclass.viewport[0] -= self.worldclass.timer * self.value / (60 *  self.duration.seconds)
        if self.isFinished():
            self.powerStop()

    def powerStop(self):
        PowerUp.powerStop(self)

    def render(self):
        PowerUp.render(self)

class Superjump(PowerUp):
    def __init__(self, renderingSurface, worldclass, x, y, ratio):
        PowerUp.__init__(self, renderingSurface, worldclass, x, y, 20)

        self.image = animatedPng(self.renderingSurface, "graphic/jump", 200, ratio = ratio, colorkey = (255,255,255))
        self.rect = pygame.Rect((x, y), self.image.size)

        self.value = True

    def powerStart(self):
        PowerUp.powerStart(self)
        self.worldclass.player.superJumpenabled = self.value

    def power(self):
        self.worldclass.player.superJumpenabled = self.value
        if self.isFinished():
            self.powerStop()

    def powerStop(self):
        PowerUp.powerStop(self)
        self.worldclass.player.superJumpenabled = not self.value

    def render(self):
        PowerUp.render(self)
