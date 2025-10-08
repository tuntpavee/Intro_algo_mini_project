import pygame
import math
from queue import PriorityQueue

#Setup
Width = 500
Height = 500

map = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("A* search Map")
