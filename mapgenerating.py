import random
import pygame
import os
import sys

"""# - brick_barrier
   . - floor
   X - box"""

MAPS = ['data/map1.txt']


def load_image(name, colorkey=None):
    '''
    Функция для загрузки изображений
    '''
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Maps:
    def __init__(self, main_screen):
        self.screen = main_screen

    def update(self, coords):
        self.screen.blit(self.field, (-coords[0], -coords[1]))

    def select_random(self):
        choiced_map_txt = random.choice(MAPS)
        with open(choiced_map_txt, 'r', encoding='utf-8') as map:
            reading_map = map.readlines()
            self.textures = reading_map[-1].split(';')
            self.map = [line.strip('\n\r') for line in reading_map[:-1]]
            self.width_in_tiles = len(self.map[0])
            self.height_in_tiles = len(self.map)
            self.create_size_map()

    def create_size_map(self):
        self.cell_size = 100
        width_field, height_field = self.cell_size * self.width_in_tiles, self.cell_size * self.height_in_tiles
        self.field = pygame.Surface((width_field, height_field))

    def generate(self):
        self.load_textures()
        self.draw_field()

    def load_textures(self):
        if 'box.png' in self.textures:
            self.box = pygame.transform.scale(load_image("box.png"), (100, 100))
        if 'sandfloor.png' in self.textures:
            self.sandfloor = pygame.transform.scale(load_image("sandfloor.png"), (100, 100))
        if 'brick_barrier.png' in self.textures:
            self.barrier = pygame.transform.scale(load_image("brick_barrier.png"), (100, 100))

    def draw_field(self):
        for x in range(0, self.width_in_tiles):
            for y in range(0, self.height_in_tiles):
                if self.map[y][x] == '#':
                    self.field.blit(self.barrier, (x * self.cell_size, y * self.cell_size))
                if self.map[y][x] == 'X':
                    self.field.blit(self.box, (x * self.cell_size, y * self.cell_size))
                if self.map[y][x] == '.':
                    self.field.blit(self.sandfloor, (x * self.cell_size, y * self.cell_size))
