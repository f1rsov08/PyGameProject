import os
import sys
import math
import pygame
import random

pygame.init()
size = width, height = 600, 600
MAPS = ['data/map1.txt']
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
tanks = pygame.sprite.Group()
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


def blit_rotate(surf, image, pos, originPos, angle):
    '''
    Поворот спрайтов относительно центра
    '''
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    rotated_offset = offset_center_to_pivot.rotate(-angle)

    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    rotated_image = pygame.transform.rotate(image, angle)

    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    surf.blit(rotated_image, rotated_image_rect)


def distance(x1, y1, x2, y2):
    '''
    Расчет расстояния между точками
    '''
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


class Camera:
    '''
    Камера
    '''

    def __init__(self, x, y, attached_entity=None):
        # Координаты камеры
        self.x, self.y = x, y
        # Привязанная сущность
        # Камера будет "следить" за ней
        self.attached_entity = attached_entity

    def update(self):
        '''
        Обновление камеры
        '''
        if self.attached_entity is not None:
            self.x, self.y = self.attached_entity.x, self.attached_entity.y

    def draw(self, screen, objs):
        '''
        Рисование объектов
        '''
        for obj in objs:
            obj.draw(screen, self)


class Entity(pygame.sprite.Sprite):
    '''
    Сущность
    '''

    def __init__(self, x, y, direction=0, health=100, *groups):
        super().__init__(all_sprites, *groups)
        # Положение в пространстве
        self.x, self.y = x, y
        self.direction = direction
        # Характеристики
        self.health = health

    def coords(self):
        '''
        Функция возвращает координаты сущности
        '''
        return self.x, self.y


class Tank(Entity):
    '''
    Танк
    '''

    def __init__(self, x, y, direction=0, health=100, speed=1.5, ai='player'):
        super().__init__(x, y, direction, health, tanks)
        # Загрузка изображений
        self.image_track = pygame.transform.scale(load_image("tank_track.png"), (128, 128))
        self.image_turret = pygame.transform.scale(load_image("tank_turret.png"), (128, 128))
        self.rect = self.image_track.get_rect()
        self.mask = pygame.mask.from_surface(self.image_track)
        # Задаем координаты танка
        self.rect.x = self.x
        self.rect.y = self.y
        # Задаем направление башни танка
        self.turret_direction = direction
        # Скорость танка
        self.speed = speed
        # ИИ
        self.ai = ai

    def move(self, multiplier=1):
        '''
        Перемещение танка
        '''
        self.x += math.cos(math.radians(self.direction)) * self.speed * multiplier
        self.y += math.sin(math.radians(self.direction)) * self.speed * multiplier
        self.rect.x = self.x
        self.rect.y = self.y

    def turn(self, angle):
        '''
        Поворот танка
        '''
        self.direction += angle

    def draw(self, screen, camera):
        '''
        Рисование танка
        '''
        # Вычисляем координаты танка на экране при центре в (0, 0)
        x = (camera.x - self.x) * -1
        y = (camera.y - self.y) * -1
        # Получаем направление к цели
        target_angle = self.get_target(camera)
        # Рисуем
        blit_rotate(screen, self.image_track, (x + width // 2, y + height // 2), (64, 64),
                    self.direction * -1)
        blit_rotate(screen, self.image_turret, (x + width // 2, y + height // 2), (64, 64),
                    target_angle * -1)

    def get_target(self, camera=None):
        '''
        Получаем цель танка
        '''
        if self.ai == 'player':
            # Если танком управляет игрок, то функция возвращает координаты мыши
            x, y = pygame.mouse.get_pos()
            target_x, target_y = x + camera.x - width // 2, y + camera.y - height // 2
        elif self.ai == 'enemy':
            # Если танком управляет враг, то функция возвращает координаты ближайшего игрока
            players = \
                sorted(filter(lambda sprite: type(sprite) is Tank and sprite.ai == 'player', all_sprites),
                       key=lambda sprite: distance(self.x, self.y, sprite.x, sprite.y))
            if players:
                target_x, target_y = players[0].coords()
            else:
                target_x, target_y = 0, 0
        else:
            # Если кто-то другой, то 0, 0
            target_x, target_y = 0, 0
        # Вычисляем координаты цели относительно танка
        target_x, target_y = target_x - self.x, target_y - self.y
        try:
            # Пробуем вычислить угол поворота башни танка
            target_angle = math.degrees(math.atan(target_y / target_x))
        except ZeroDivisionError:
            # И если x оказался равен 0, то сами подставляем значения
            if target_y > 0:
                target_angle = 90
            elif target_y < 0:
                target_angle = 270
            else:
                target_angle = 0
        else:
            # А если нам удалось вычислить угол, то поворачиваем его на 180 градусов, если цель с другой стороны
            if target_x < 0:
                target_angle += 180
        return target_angle

    def shoot(self, camera=None):
        all_sprites.add(Bullet(self.x,
                               self.y, self.get_target(camera)))

    def update(self):
        if self.health <= 0:
            self.kill()


class Box(Entity):
    '''
    Коробка
    '''

    def __init__(self, x, y, direction=0):
        super().__init__(x, y, direction, 25)
        self.box = pygame.transform.scale(load_image("box.png"), (128, 128))
        self.rect = self.box.get_rect()
        self.mask = pygame.mask.from_surface(self.box)
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen, camera):
        '''
        Рисование коробки
        '''
        # Вычисляем координаты коробки на экране при центре в (0, 0)
        x = (camera.x - self.x) * -1
        y = (camera.y - self.y) * -1
        # Рисуем
        blit_rotate(screen, self.box, (x + width // 2, y + height // 2), (64, 64),
                    self.direction * -1)

    def update(self):
        if self.health <= 0:
            self.kill()


class Bullet(Entity):
    '''
    Снаряд
    '''

    def __init__(self, x, y, direction=0):
        super().__init__(x, y, direction, -1)
        self.bullet = pygame.transform.scale(load_image("bullet.png"), (128, 128))
        self.rect = self.bullet.get_rect()
        self.mask = pygame.mask.from_surface(self.bullet)
        self.rect.x = self.x
        self.rect.y = self.y
        self.distance = 0

    def draw(self, screen, camera):
        '''
        Рисование снаряда
        '''
        # Вычисляем координаты снаряда на экране при центре в (0, 0)
        x = (camera.x - self.x) * -1
        y = (camera.y - self.y) * -1
        # Рисуем
        blit_rotate(screen, self.bullet, (x + width // 2, y + height // 2), (64, 64),
                    self.direction * -1)

    def update(self):
        '''
        Перемещение снарядаa
        '''
        self.x += math.cos(math.radians(self.direction)) * 3
        self.y += math.sin(math.radians(self.direction)) * 3
        self.rect.x = self.x
        self.rect.y = self.y
        self.distance += 3
        if self.distance > 600:
            self.kill()
        for i in all_sprites:
            if pygame.sprite.collide_mask(self, i) and i != self and not (type(i) is Tank and i.ai == 'player'):
                i.health -= 25
                self.kill()

class Maps:
    def __init__(self, main_screen):
        self.screen = main_screen
        self.obj_size = 100

    def create_obj(self, x, y, image, can_break):
        Obstacle(x, y, image, self.cell_size, can_break)

    # obj = pygame.sprite.Sprite(obstacles)
    # obj.image = image
    # obj.rect = obj.image.get_rect()
    # obj.rect.x = x * self.cell_size
    # obj.rect.y = y * self.cell_size

    def update(self, coords):
        self.screen.blit(self.field, (-coords[0], -coords[1]))

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
                    self.create_obj(x, y, self.barrier, 0)
                if self.map[y][x] == 'L':
                    self.fill_ground_png(x, y)
                    self.create_obj(x, y, self.light_box, 1)
                if self.map[y][x] == 'W':
                    self.fill_ground_png(x, y)
                    self.create_obj(x, y, self.bush, 0)
                if self.map[y][x] == 'D':
                    self.fill_ground_png(x, y)
                    self.create_obj(x, y, self.dark_box, 1)
                    # self.field.blit(self.dark_box, (x * self.cell_size, y * self.cell_size))
                    # self.field.blit(self.box, (x * self.cell_size, y * self.cell_size))
                if self.map[y][x] == '0':
                    self.field.blit(self.sand_ground, (x * self.cell_size, y * self.cell_size))
                if self.map[y][x] == '1':
                    self.field.blit(self.grass_ground, (x * self.cell_size, y * self.cell_size))
                if self.map[y][x] == '2':
                    self.field.blit(self.stone_ground, (x * self.cell_size, y * self.cell_size))
                if self.map[y][x] == '3':
                    self.field.blit(self.wood_ground, (x * self.cell_size, y * self.cell_size))
                if self.map[y][x] == '+':
                    self.fill_ground_png(x, y)
                    self.create_obj(x, y, self.stone_wall, 0)
                if self.map[y][x] == '-':
                    self.fill_ground_png(x, y)
                    self.create_obj(x, y, self.sandstone_wall, 0)
                if self.map[y][x] == '=':
                    self.fill_ground_png(x, y)
                    self.create_obj(x, y, self.wood_wall, 1)


    def fill_ground_png(self, x, y):
        list_of_number_plates = sorted([(self.textures.count('0'), self.sand_ground),
                                        (self.textures.count('1'), self.grass_ground),
                                        (self.textures.count('2'), self.stone_ground),
                                        (self.textures.count('3'), self.wood_ground)], key=lambda x: x[0])
        self.field.blit(list_of_number_plates[-1][1], (x * self.cell_size, y * self.cell_size))


if __name__ == '__main__':

    # Травяной цвет)
    #screen.fill((93, 161, 48))
    # Создаем 10 коробок, чтобы видеть перемещения танка
    #for i in range(10):
    #    box = Box(random.randint(-300, 300), random.randint(-300, 300))
    #    all_sprites.add(box)
    #    box.name = f'Коробка {i}'

    # Создаем танк игрока
    player = Tank(0, 0)
    player.name = 'Игрок'
    # Создаем танк врага
    enemy_tank = Tank(40, 40, ai='enemy')
    enemy_tank.name = 'Враг'

    # Создаем камеру
    camera = Camera(0, 0, player)

    # Добавляем танки во группу спрайтов

    # Часы
    clock = pygame.time.Clock()

    # Основной цикл
    running = True
    while running:
        # Проходимся по ивентам
        for event in pygame.event.get():
            # Если окно закрыли, то завершаем цикл
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot(camera)

        # Получаем кнопки, которые нажаты
        keys = pygame.key.get_pressed()
        # Управление на WASD
        if keys[pygame.K_w]:
            player.move()
        if keys[pygame.K_s]:
            player.move(-1)
        if keys[pygame.K_a]:
            player.turn(-1.5)
        if keys[pygame.K_d]:
            player.turn(1.5)

        # Обновляем камеру
        all_sprites.update()
        camera.update()

        # Рисуем все что надо
        screen.fill((93, 161, 48))
        camera.draw(screen, all_sprites)

        # Обновляем экран
        pygame.display.flip()

        # Ждем следующий кадр
        clock.tick(60)
pygame.quit()