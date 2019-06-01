# -*- coding: UTF-8 -*-

#standart lib
import pygame
import sys

#game objects
sys.path.append('objects')
from Menu import Menu

def main():
    #Create an instance of Menuclass which does all necessary jobs to run the game
    game = Menu()

if __name__ == '__main__':
    main()
    