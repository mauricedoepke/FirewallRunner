# -*- coding: UTF-8 -*-

import glob
import os
import json
import random
import copy

class levelloader(object):

    def __init__(self, path = "part"):
        #this class provides functionality to load new levelparts randomly for the players speed
        self.levelparts = []

        self.leveldefinition = ("grounds", "walls", "decolines", "stumbles", "powerups")


        savedPath = os.getcwd()
        os.chdir(path)
        #read in all level parts in the given directory and save them in a list
        for filename in glob.glob('*.level'):
            levelfile = open(filename, "r")

            self.levelparts.append((json.loads(levelfile.readline()), {}))

            for line in self.leveldefinition:
                self.levelparts[-1][1][line] = json.loads(levelfile.readline())

            levelfile.close()
        os.chdir(savedPath)

        self.lastindex = -1

    def getRandPart(self, speed):
        possible = []
        index = 0
        #checks which level parts are possible to master at the given playerspeed
        for part in self.levelparts:
            if (part[0][0] == -1 or speed >= part[0][0]) and (part[0][1] == -1 or speed <= part[0][1]):
                #prohibits load the same part 2 or more times in sequence
                if not self.lastindex == index:
                    possible.append(index)
            index += 1

        #returns a random part from the possible ones
        count = len(possible)
        if count > 0:
            index = possible[random.randint(0, count - 1)]
            self.lastindex = index
            return copy.deepcopy(self.levelparts[index][1])

        return None
