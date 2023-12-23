import random
import pygame
from map_1 import Map_1
from Test import load_image
"""# - brick_barrier
   . - floor
   X - box"""

MAP_SIZE = width_field, height_field = 1600, 900
COEF = 50
MAPS = ['data/map1.txt']

class Maps:
    def __init__(self):
        self.field = pygame.Surface((width_field, height_field))
        self.width = 10
        self.height = 10
        self.cell_size = 100
       # self.x = 0
       # self.y = 0
       # self.screen = screen
       # maps = [Map_1(self.screen)]
       # self.map = random.choice(maps)

#

    def render_selected_map(self):
        self.map.create_board()

    def navigation(self, screen, coords):
        s = screen
        s.blit(self.screen, (-coords[0], -coords[1]))

    def getb(self):
        return self.map

    def select_random(self):
        choiced_map_txt = random.choice(MAPS)
        with open(choiced_map_txt, 'r', encoding='utf-8') as map:
            reading_map = map.readlines()
            self.textures = reading_map[-1].split(';')
            self.map = [line.strip('\n\r') for line in reading_map[:-1]]
           # print(reading_map)
           # print(self.map)
           # print(self.textures)
    def generate(self):
        self.load_textures()


    def load_textures(self):
        if 'box.png' in self.textures:
            self.box = pygame.transform.scale(load_image("box.png"), (100, 100))
        if 'sandfloor.png' in self.textures:
            self.sandfloor = pygame.transform.scale(load_image("sandfloor.png"), (80, 100))
        if 'brick_barrier.png' in self.textures:
            self.barrier = pygame.transform.scale(load_image("brick_barrier.png"), (100, 100))














#import pygame
#import os
#import sys
#
#class Board:
#    # создание поля
#    def __init__(self, width, height):
#        self.width = width
#        self.height = height
#        self.board = [[0] * width for _ in range(height)]
#        # значения по умолчанию
#        self.left = 25
#        self.top = 25
#        self.cell_size = 40
#
#    # настройка внешнего вида
#    def set_view(self, left, top, cell_size):
#        self.left = left
#        self.top = top
#        self.cell_size = cell_size
#
#    def render(self, name_screen):
#        for x in range(0, self.width):
#            for y in range(0, self.height):
#                pygame.draw.rect(name_screen, 'white', (self.left + x * self.cell_size, self.top + y * self.cell_size,
#                                                        self.cell_size, self.cell_size), 1)
#
#
#if __name__ == '__main__':
#    pygame.init()
#    size = width, height = 600, 600
#    screen = pygame.display.set_mode(size)
#
#    running = True
#    board = Board(14, 14)
#    while running:
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                running = False
#        screen.fill((0, 0, 0))
#        board.render(screen)
#        all_sprites.draw(screen)
#        pygame.display.flip()
#    pygame.quit()
