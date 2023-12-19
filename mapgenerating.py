import random
from map_1 import Map_1
from main import Entity
import math

class Maps:
    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self.screen = screen
        maps = [Map_1(self.screen)]
        self.map = random.choice(maps)


    def render_selected_map(self):
        self.map.create_board()

    def navigation(self, screen, coords):
        s = screen
        s.blit(self.screen, (-coords[0], -coords[1]))

    def getb(self):
        return self.map


class Floor(Entity):
    pass














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
