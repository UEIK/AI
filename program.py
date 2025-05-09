import pygame, sys
from pygame.locals import *
from enum import Enum
pygame.init()
WINDOW_WIDTH = 732
WINDOW_HEIGHT = 780
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
FONT = pygame.font.SysFont("cambria", 30, bold= True)
MENU_BG = pygame.image.load('img/menu.jpg')
ICON_O = pygame.transform.scale(pygame.image.load('img/O.png'),(70, 70))
ICON_X = pygame.transform.scale(pygame.image.load('img/X.png'),(70, 70))

class Screen(Enum):
    MENUINTRO = 1
    MENUSIZEHUMAN = 2
    MENUAI = 3
    SELECT_AIGO = 4
    SELECT_SIZE = 5 
    GAMING = 6       
    GAMINGHUMAN = 7

SCREEN = Screen.MENUINTRO

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
PINK  = (255,  20, 147)
BABY_PINK = (255, 195, 208)

BOARD_SIZE = 3 