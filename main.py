import os
import sys
import math
import pygame
import random

pygame.init()
size = WIDTH, HEIGHT = 1000, 800
MAPS = ['data/maps/map1.txt', 'data/maps/mines.txt', 'data/maps/maze.txt']
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
tanks = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemies = pygame.sprite.Group()


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


def blit_rotate(surf, image, pos, origin_pos, angle):
    '''
    Поворот спрайтов относительно центра
    '''
    image_rect = image.get_rect(topleft=(pos[0] - origin_pos[0], pos[1] - origin_pos[1]))
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

    def __init__(self, x, y, angle=0, attached_entity=None):
        # Координаты камеры
        self.x, self.y = x, y
        self.angle = angle
        # Привязанная сущность
        # Камера будет "следить" за ней
        self.attached_entity = attached_entity

    def update(self):
        '''
        Обновление камеры
        '''
        if self.attached_entity is not None and self.attached_entity.alive():
            self.x, self.y = self.attached_entity.x, self.attached_entity.y
            self.angle = self.attached_entity.direction

    def draw(self, screen, objs):
        '''
        Рисование объектов
        '''
        width, height = screen.get_width(), screen.get_height()
        sx, ex = self.x - width // 2 - 136, self.x + width // 2 + 136
        sy, ey = self.y - height // 2 - 136, self.y + height // 2 + 136
        for obj in objs:
            if sx < obj.x < ex and sy < obj.y < ey:
                obj.draw(screen, self)

    def move(self, x, y):
        self.x += math.cos(math.radians(self.angle)) * x
        self.y += math.sin(math.radians(self.angle)) * x
        self.x += math.cos(math.radians(self.angle + 90)) * y
        self.y += math.sin(math.radians(self.angle + 90)) * y


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

    def update(self):
        if self.health <= 0:
            self.kill()


class Tank(Entity):
    '''
    Танк
    '''

    def __init__(self, x, y, direction=0, health=100, speed=1.5, reload_time=1000, ai='player', team='player'):
        super().__init__(x, y, direction, health, tanks)
        # Загрузка изображений
        self.image_track = pygame.transform.scale(load_image("images/tank_track.png"), (64, 64))
        self.image_turret = pygame.transform.scale(load_image("images/tank_turret.png"), (128, 128))
        self.rect = self.image_track.get_rect()
        # Задаем координаты танка
        self.rect.x = self.x
        self.rect.y = self.y
        # Задаем направление башни танка
        self.turret_direction = direction
        # Скорость танка
        self.speed = speed
        # Время перезарядки
        self.reload_time = reload_time
        self.last_shot_time = 0
        # ИИ
        self.ai = ai
        self.team = team

    def move(self, multiplier=1):
        '''
        Перемещение танка
        '''
        x = math.cos(math.radians(self.direction - 90)) * self.speed * multiplier
        y = math.sin(math.radians(self.direction - 90)) * self.speed * multiplier
        self.x += x
        self.rect.x = self.x
        if pygame.sprite.spritecollideany(self, obstacles):
            self.x -= x
            self.rect.x = self.x
        self.y += y
        self.rect.y = self.y
        if pygame.sprite.spritecollideany(self, obstacles):
            self.y -= y
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
        width, height = screen.get_width(), screen.get_height()
        # Вычисляем координаты танка на экране при центре в (0, 0)
        x = (camera.x - self.x) * -1
        y = (camera.y - self.y) * -1
        # Получаем направление к цели
        target_angle = self.get_target(camera)
        if target_angle is None:
            target_angle = self.direction - 90
        # Рисуем
        blit_rotate(screen, self.image_track, (x + width // 2, y + height // 2), (32, 32),
                    self.direction * -1)
        blit_rotate(screen, self.image_turret, (x + width // 2, y + height // 2), (64, 64),
                    target_angle * -1 - 90)

    def get_target(self, camera=None):
        '''
        Получаем цель танка
        '''
        addition = 0
        if self.ai == 'player':
            # Если танком управляет игрок, то функция возвращает координаты мыши
            x, y = pygame.mouse.get_pos()
            target_x, target_y = x - WIDTH // 2, y - HEIGHT // 2
            addition = camera.angle
        elif self.ai == 'enemy':
            # Если танком управляет враг, то функция возвращает координаты ближайшего игрока
            players = \
                sorted(filter(lambda sprite: type(sprite) is Tank and sprite.team == 'player', all_sprites),
                       key=lambda sprite: distance(self.x, self.y, sprite.x, sprite.y))
            if players:
                target_x, target_y = players[0].coords()
                target_x, target_y = target_x - self.x, target_y - self.y
            else:
                return None
        else:
            # Если кто-то другой, то 0, 0
            target_x, target_y = 0, 0
        try:
            target_angle = math.degrees(math.atan(target_y / target_x))
        except ZeroDivisionError:
            if target_y > 0:
                target_angle = 90
            elif target_y < 0:
                target_angle = 270
            else:
                target_angle = 0
        else:
            if target_x < 0:
                target_angle += 180
        return target_angle + addition

    def shoot(self, camera=None):
        if pygame.time.get_ticks() - self.last_shot_time >= self.reload_time:
            all_sprites.add(Bullet(self.x, self.y, self.get_target(camera), self.team))
            self.last_shot_time = pygame.time.get_ticks()

    def update(self):
        super().update()
        if self.ai == 'enemy':
            target = self.get_target()
            if target:
                self.direction = target + 90
                self.move()
                self.shoot()
            else:
                self.turn(5)


class Obstacle(Entity):
    '''
    Препятсвтие
    '''

    def __init__(self, x, y, image, cell, can_break=0):
        super().__init__(x, y, 0, [float('inf'), 25][can_break], obstacles)
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x * cell - 256
        self.y = y * cell - 256
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen, camera):
        '''
        Рисование коробки
        '''
        width, height = screen.get_width(), screen.get_height()
        # Вычисляем координаты коробки на экране при центре в (0, 0)
        x = (camera.x - self.x) * -1 - 32
        y = (camera.y - self.y) * -1 - 32
        # Рисуем
        screen.blit(self.image, (x + width // 2, y + height // 2))


class Bullet(Entity):
    '''
    Снаряд
    '''

    def __init__(self, x, y, direction=0, team='player'):
        super().__init__(x, y, direction, -1)
        self.bullet = pygame.transform.scale(load_image("images/bullet.png"), (28, 8))
        self.rect = self.bullet.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.distance = 0
        self.team = team

    def draw(self, screen, camera):
        '''
        Рисование снаряда
        '''
        width, height = screen.get_width(), screen.get_height()
        # Вычисляем координаты снаряда на экране при центре в (0, 0)
        x = (camera.x - self.x) * -1
        y = (camera.y - self.y) * -1
        # Рисуем
        blit_rotate(screen, self.bullet, (x + width // 2, y + height // 2), (14, 4),
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
        if self.distance > 1200:
            self.kill()
        for i in all_sprites:
            if pygame.sprite.collide_rect(self, i) and i != self and not (type(i) is Tank and i.team == self.team):
                i.health -= 25
                self.kill()


class Maps:
    """КЛАСС КАРТ"""

    def __init__(self, main_screen):
        self.screen = main_screen
        self.cell_size = 96

    """создание объектов на карте"""

    def create_obj(self, x, y, image, can_break):
        Obstacle(x, y, image, self.cell_size, can_break)

    """обновление карты"""

    def draw(self, screen, camera):
        width, height = screen.get_width(), screen.get_height()
        x = -camera.x - 288
        y = -camera.y - 288
        # Рисуем
        screen.blit(self.field, (x + width // 2, y + height // 2))

    """загрузка карты из txt формата"""

    def load_map_from_txt(self):
        with open(self.choiced_map_txt, 'r', encoding='utf-8') as map:
            reading_map = map.readlines()
            self.map = [line.strip('\n\r') for line in reading_map]
            self.textures = ''.join(self.map)
            self.width_in_tiles = len(self.map[0])
            self.height_in_tiles = len(self.map)
            self.create_size_map()

    """выбор карты на рандом"""

    def select_random(self):
        self.choiced_map_txt = random.choice(MAPS)
        self.load_map_from_txt()

    """выбор карты"""

    def select(self, number_of_map):
        count_maps = len(MAPS)
        if 1 <= number_of_map <= count_maps:
            self.choiced_map_txt = MAPS[number_of_map - 1]
            self.load_map_from_txt()
        else:
            return 'Введите правильный номер карты'

    """создание размеров карты"""

    def create_size_map(self):
        width_field, height_field = self.cell_size * self.width_in_tiles, self.cell_size * self.height_in_tiles
        self.field = pygame.Surface((width_field, height_field))

    """генерация или создание карты"""

    def generate(self):
        self.load_textures()
        self.draw_field()

    """загрузка текстур"""

    def load_textures(self):
        """# - brick_barrier - барьерная стена
           0 - sand_ground - песчаный пол
           L - light_box - светлая коробка
           D - dark_box - темная коробка
           1 - grass_ground - травянистый пол
           2 - stone_ground - каменный пол
           3 - wood_ground - деревянный пол
           4 - snow_ground - снежный пол
           + - stone_wall - каменная стена
           - - sandstone_wall - песчаная стена
           = -  wood_wall - деревянная стена
           ~ -  water - вода
           W - bush - кусты"""
        if 'L' in self.textures:
            self.light_box = pygame.transform.scale(load_image("images/light_box.png"),
                                                    (self.cell_size, self.cell_size))
        if '0' in self.textures:
            self.sand_ground = pygame.transform.scale(load_image("images/sand_ground.png"),
                                                      (self.cell_size, self.cell_size))
        if '#' in self.textures:
            self.barrier = pygame.transform.scale(load_image("images/brick_barrier.png"),
                                                  (self.cell_size, self.cell_size))
        if 'D' in self.textures:
            self.dark_box = pygame.transform.scale(load_image("images/dark_box.png"),
                                                   (self.cell_size, self.cell_size))
        if '1' in self.textures:
            self.grass_ground = pygame.transform.scale(load_image("images/grass_ground.png"),
                                                       (self.cell_size, self.cell_size))
        if '2' in self.textures:
            self.stone_ground = pygame.transform.scale(load_image("images/stone_ground.png"),
                                                       (self.cell_size, self.cell_size))
        if '3' in self.textures:
            self.wood_ground = pygame.transform.scale(load_image("images/wood_ground.png"),
                                                      (self.cell_size, self.cell_size))
        if '4' in self.textures:
            self.snow_ground = pygame.transform.scale(load_image("images/snow_ground.png"),
                                                      (self.cell_size, self.cell_size))
        if '-' in self.textures:
            self.sandstone_wall = pygame.transform.scale(load_image("images/sandstone_wall.png"),
                                                         (self.cell_size, self.cell_size))
        if '+' in self.textures:
            self.stone_wall = pygame.transform.scale(load_image("images/stone_wall.png"),
                                                     (self.cell_size, self.cell_size))
        if '=' in self.textures:
            self.wood_wall = pygame.transform.scale(load_image("images/wood_wall.png"),
                                                    (self.cell_size, self.cell_size))
        if '~' in self.textures:
            self.water = pygame.transform.scale(load_image("images/water.png"),
                                                (self.cell_size, self.cell_size))
        if 'W' in self.textures:
            self.bush = pygame.transform.scale(load_image("images/bush.png"),
                                               (self.cell_size, self.cell_size))

    """рисование поля"""

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
                if self.map[y][x] == '4':
                    self.field.blit(self.snow_ground, (x * self.cell_size, y * self.cell_size))
                if self.map[y][x] == '+':
                    self.fill_ground_png(x, y)
                    self.create_obj(x, y, self.stone_wall, 0)
                if self.map[y][x] == '-':
                    self.fill_ground_png(x, y)
                    self.create_obj(x, y, self.sandstone_wall, 0)
                if self.map[y][x] == '=':
                    self.fill_ground_png(x, y)
                    self.create_obj(x, y, self.wood_wall, 1)
                if self.map[y][x] == '~':
                    self.fill_ground_png(x, y)
                    self.create_obj(x, y, self.water, 0)

    """Для заполения пола у ломающихся и не полностью заполненных объектов"""

    def fill_ground_png(self, x, y):
        list_of_number_plates = sorted(
            [(self.textures.count('0'), pygame.transform.scale(load_image("images/sand_ground.png"),
                                                               (self.cell_size, self.cell_size))),
             (self.textures.count('1'), pygame.transform.scale(load_image("images/grass_ground.png"),
                                                               (self.cell_size, self.cell_size))),
             (self.textures.count('2'), pygame.transform.scale(load_image("images/stone_ground.png"),
                                                               (self.cell_size, self.cell_size))),
             (self.textures.count('3'), pygame.transform.scale(load_image("images/wood_ground.png"),
                                                               (self.cell_size, self.cell_size))),
             (self.textures.count('4'), pygame.transform.scale(load_image("images/snow_ground.png"),
                                                               (self.cell_size, self.cell_size)))], key=lambda x: x[0])
        self.field.blit(list_of_number_plates[-1][1], (x * self.cell_size, y * self.cell_size))


if __name__ == '__main__':
    # передается главный экран где будут отображаться все объекты
    map = Maps(screen)
    # это для выбора карты или можно map.selectrandod)
    map.select(3)
    # для создания карты
    map.generate()
    # Создаем танк игрока
    player = Tank(230, 230)

    # Создаем танк врага
    enemies.add(Tank(96 - 288 + 48, 96 - 288 + 48, ai='enemy', team='enemy'))

    # Создаем камеру
    camera = Camera(0, 0, 0, player)

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and player.alive():
                    player.shoot(camera)

        # Получаем кнопки, которые нажаты
        keys = pygame.key.get_pressed()
        # Управление на WASD
        if player.alive():
            if keys[pygame.K_w]:
                player.move(2)
            if keys[pygame.K_s]:
                player.move(-2)
            if keys[pygame.K_a]:
                player.turn(-1.5)
            if keys[pygame.K_d]:
                player.turn(1.5)
        else:
            if keys[pygame.K_w]:
                camera.move(0, -20)
            if keys[pygame.K_s]:
                camera.move(0, 20)
            if keys[pygame.K_a]:
                camera.move(-20, 0)
            if keys[pygame.K_d]:
                camera.move(20, 0)
            if keys[pygame.K_q]:
                camera.angle -= 1.5
            if keys[pygame.K_e]:
                camera.angle += 1.5

        screen.fill((0, 0, 0))
        # Обновляем
        all_sprites.update()
        camera.update()

        # Рисуем все что надо
        s = max(WIDTH, HEIGHT) * 1.42  # Типа корень из двух
        test_screen = pygame.Surface((s, s))
        map.draw(test_screen, camera)
        camera.draw(test_screen, all_sprites)
        blit_rotate(screen, test_screen, (WIDTH // 2, HEIGHT // 2), (s // 2, s // 2), camera.angle)
        # Обновляем экран
        pygame.display.flip()

        # Ждем следующий кадр
        clock.tick(60)
pygame.quit()
