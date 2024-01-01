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
        self.other = 80

    def create_obj(self, x, y, image):
        Obj_obstacle(x, y, image, self.cell_size)

    # obj = pygame.sprite.Sprite(obstacles)
    # obj.image = image
    # obj.rect = obj.image.get_rect()
    # obj.rect.x = x * self.cell_size
    # obj.rect.y = y * self.cell_size

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
            self.map = [line.strip('\n\r') for line in reading_map]
            self.textures = ''.join(self.map)
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
        """# - brick_barrier - барьерная стена
           0 - sand_ground - песочный пол
           L - light_box - светлая коробка
           D - dark_box - темная коробка
           1 - grass_ground - травянистый пол
           2 - stone_ground - каменный пол
           3 - wood_ground - деревянный пол
           + - stone_wall - каменная стена
           - - sandstone_wall - песчаная стена
           = -  wood_wall - деревянная стена
           W - bush - кусты"""
        if 'L' in self.textures:
            self.light_box = pygame.transform.scale(load_image("light_box.png"), (self.obj_size, self.obj_size))
        if '0' in self.textures:
            self.sand_ground = pygame.transform.scale(load_image("sand_ground.png"), (self.obj_size, self.obj_size))
        if '#' in self.textures:
            self.barrier = pygame.transform.scale(load_image("brick_barrier.png"), (self.obj_size, self.obj_size))
        if 'D' in self.textures:
            self.dark_box = pygame.transform.scale(load_image("dark_box.png"), (self.obj_size, self.obj_size))
        if '1' in self.textures:
            self.grass_ground = pygame.transform.scale(load_image("grass_ground.png"), (self.obj_size, self.obj_size))
        if '2' in self.textures:
            self.stone_ground = pygame.transform.scale(load_image("stone_ground.png"), (self.obj_size, self.obj_size))
        if '3' in self.textures:
            self.wood_ground = pygame.transform.scale(load_image("wood_ground.png"), (self.obj_size, self.obj_size))
        if '-' in self.textures:
            self.sandstone_wall = pygame.transform.scale(load_image("sandstone_wall.png"),
                                                         (self.obj_size, self.obj_size))
        if '+' in self.textures:
            self.stone_wall = pygame.transform.scale(load_image("stone_wall.png"), (self.obj_size, self.obj_size))
        if '=' in self.textures:
            self.wood_wall = pygame.transform.scale(load_image("wood_wall.png"), (self.obj_size, self.obj_size))
        if 'W' in self.textures:
            self.bush = pygame.transform.scale(load_image("bush.png"), (self.obj_size, self.obj_size))

    def draw_field(self):
        for x in range(0, self.width_in_tiles):
            for y in range(0, self.height_in_tiles):
                if self.map[y][x] == '#':
                    # self.field.blit(sprite, (x * self.cell_size, y * self.cell_size))
                    self.create_obj(x, y, self.barrier)
                if self.map[y][x] == 'L':
                    self.fill_ground_png(x, y)
                    self.create_obj(x, y, self.light_box)
                if self.map[y][x] == 'W':
                    self.fill_ground_png(x, y)
                    self.create_obj(x, y, self.bush)
                if self.map[y][x] == 'D':
                    self.fill_ground_png(x, y)
                    self.create_obj(x, y, self.dark_box)
                    # self.field.blit(self.dark_box, (x * self.cell_size, y * self.cell_size))
                    # self.field.blit(self.box, (x * self.cell_size, y * self.cell_size))
                if self.map[y][x] == '0':
                    self.field.blit(self.sand_ground, (x * self.cell_size, y * self.cell_size))
                if self.map[y][x] == '1':
                    self.field.blit(self.grass_ground, (x * self.cell_size, y * self.cell_size))
                if self.map[y][x] == '2':
                    self.create_obj(x, y, self.stone_ground)
                if self.map[y][x] == '3':
                    self.create_obj(x, y, self.wood_ground)
                if self.map[y][x] == '+':
                    self.create_obj(x, y, self.stone_wall)
                if self.map[y][x] == '-':
                    self.create_obj(x, y, self.sandstone_wall)
                if self.map[y][x] == '=':
                    self.create_obj(x, y, self.wood_wall)


    def fill_ground_png(self, x, y):
        list_of_number_plates = sorted([(self.textures.count('0'), self.sand_ground),
                                        (self.textures.count('1'), self.grass_ground),
                                        (self.textures.count('2'), self.stone_ground),
                                        (self.textures.count('3'), self.wood_ground)], key=lambda x: x[0])
        self.create_obj(x, y, list_of_number_plates[-1][1])
