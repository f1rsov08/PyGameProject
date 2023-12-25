import random
import pygame
import os
import sys

"""# - brick_barrier
   . - sandfloor
   X - box
   D - dark_box
   , - grassfloor"""

MAPS = ['data/map1.txt', 'data/map2.txt']
obstacles = pygame.sprite.Group()


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

class Obj_obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image, cell_size):
        super().__init__()
        obj = pygame.sprite.Sprite(obstacles)
        obj.image = image
        obj.rect = obj.image.get_rect()
        obj.rect.x = x * cell_size
        obj.rect.y = y * cell_size


class Maps:
    def __init__(self, main_screen):
        self.screen = main_screen
        self.obj_size = 100

    def create_obj(self, x, y, image):
        Obj_obstacle(x, y, image, self.cell_size)
      #obj = pygame.sprite.Sprite(obstacles)
      #obj.image = image
      #obj.rect = obj.image.get_rect()
      #obj.rect.x = x * self.cell_size
      #obj.rect.y = y * self.cell_size

    def update(self, coords, entity):
        self.screen.blit(self.field, (-coords[0], -coords[1]))
        obstacles.draw(self.field)

    # object1_mask = pygame.mask.from_surface(tank)
    # object2_mask = pygame.mask.from_surface(self.box)
    # if object1_mask.collide(object2_mask):
    #    print(11)
    ## Оба объекта пересекаются

    def load_map_from_txt(self):
        with open(self.choiced_map_txt, 'r', encoding='utf-8') as map:
            reading_map = map.readlines()
            self.textures = reading_map[-1].split(';')
            self.map = [line.strip('\n\r') for line in reading_map[:-1]]
            self.width_in_tiles = len(self.map[0])
            self.height_in_tiles = len(self.map)
            self.create_size_map()

    def select_random(self):
        self.choiced_map_txt = random.choice(MAPS)
        self.load_map_from_txt()

    def select(self, number_of_map):
        count_maps = len(MAPS)
        if 1 <= number_of_map <= count_maps:
            self.choiced_map_txt = MAPS[number_of_map - 1]
            self.load_map_from_txt()
        else:
            return 'Введите правильный номер карты'

    def create_size_map(self):
        self.cell_size = 100
        width_field, height_field = self.cell_size * self.width_in_tiles, self.cell_size * self.height_in_tiles
        self.field = pygame.Surface((width_field, height_field))

    def generate(self):
        self.load_textures()
        self.draw_field()

    def load_textures(self):
        if 'box.png' in self.textures:
            self.box = pygame.transform.scale(load_image("box.png"), (self.obj_size, self.obj_size))
        if 'sandfloor.png' in self.textures:
            self.sandfloor = pygame.transform.scale(load_image("sandfloor.png"), (self.obj_size, self.obj_size))
        if 'brick_barrier.png' in self.textures:
            self.barrier = pygame.transform.scale(load_image("brick_barrier.png"), (self.obj_size, self.obj_size))
        if 'dark_box.png' in self.textures:
            self.dark_box = pygame.transform.scale(load_image("dark_box.png"), (self.obj_size, self.obj_size))
        if 'grassfloor.png' in self.textures:
            self.grassfloor = pygame.transform.scale(load_image("grassfloor.png"), (self.obj_size, self.obj_size))

    def draw_field(self):
        for x in range(0, self.width_in_tiles):
            for y in range(0, self.height_in_tiles):
                if self.map[y][x] == '#':
                    # self.field.blit(sprite, (x * self.cell_size, y * self.cell_size))
                    self.create_obj(x, y, self.barrier)
                if self.map[y][x] == 'X':
                    self.create_obj(x, y, self.box)
                    # self.field.blit(self.box, (x * self.cell_size, y * self.cell_size))
                if self.map[y][x] == '.':
                    self.field.blit(self.sandfloor, (x * self.cell_size, y * self.cell_size))
                if self.map[y][x] == ',':
                    self.field.blit(self.grassfloor, (x * self.cell_size, y * self.cell_size))
                if self.map[y][x] == 'D':
                    self.create_obj(x, y, self.dark_box)
                    # self.field.blit(self.dark_box, (x * self.cell_size, y * self.cell_size))
