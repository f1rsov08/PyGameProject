import os
import sys
import math
import pygame
import random

pygame.init()
size11 = WIDTH, HEIGHT = 800, 600
MAPS = ['data/maps/map1.txt', 'data/maps/mines.txt']
disp = pygame.display.Info()
size_full_screen = width1, height1 = (disp.current_w, disp.current_h)
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
tanks = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
full_screen_coef = 1
current_type_tab = 'Main_Menu'


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

def full_screen():
    global screen, width, height,size, width1, height1, full_screen_coef
    if full_screen_coef:
        size = width, height = width1, height1
        screen = pygame.display.set_mode(size_full_screen, pygame.FULLSCREEN)
        full_screen_coef = 0
        update_after_change_size_screen()
    else:
        size = width, height = 800, 600
        screen = pygame.display.set_mode(size)
        update_after_change_size_screen()
        full_screen_coef = 1

def update_after_change_size_screen():
    settings.__init__()
    settings.create()
    select_lvl.__init__()
    select_lvl.create()

def back():
    global current_type_tab
    current_type_tab = 'Main_Menu'
    main_menu.__init__()
    main_menu.create()

def quit():
    global running
    running = False



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

class Settings:
    def __init__(self):
        self.background = pygame.transform.scale(load_image('images/background_settings.png'), (width, height))
        self.buttons = []

    def create(self):
        self.full_display = Button((200, 80), (width // 2 - 100, height // 2 - 200), 'black', 'Полноэкранный режим', 'white', 20)
        self.back = Button((200, 80), (width // 2 + 200, height // 2 + 200), 'black', 'Назад', 'white', 40)
        self.buttons.extend([self.full_display, self.back])
        for i in self.buttons:
            i.create()

    def draw(self):
        screen.blit(self.background, (0, 0))
        for i in self.buttons:
            i.update()



class Main_Menu:
    def __init__(self):
        self.background = pygame.transform.scale(load_image('images/background.png'), (width, height))
        self.buttons = []

    def create(self):
        self.play = Button((200, 80), (width // 2 - 100, height // 2 + 30), 'black', 'Играть', 'white', 40)
        self.settings = Button((200, 80), (width // 2 - 100, height // 2 + 120), 'black', 'Настройки', 'white', 40)
        self.quit = Button((200, 80), (width // 2 - 100, height // 2 + 210), 'black', 'Выйти', 'white', 40)
        self.buttons.extend([self.play, self.settings, self.quit])
        for i in self.buttons:
            i.create()

    def draw(self):
        screen.blit(self.background, (0, 0))
        for i in self.buttons:
            i.update()

class Select_Level:
    def __init__(self):
        self.background = pygame.transform.scale(load_image('images/background_select_level.png'), (width, height))
        self.buttons = []

    def create(self):
        self.level_1 = Button((200, 200), (0.1 * width, 0.2 * height), 'black', 'Уровень 1', 'white', 30)
        self.level_2 = Button((200, 200), (0.1 * width + 220, 0.2 * height), 'black', 'Уровень 2', 'white', 30)
        self.level_3 = Button((200, 200), (0.11 * width + 440, 0.2 * height), 'black', 'Уровень 3', 'white', 30)
        self.back = Button((200, 80), (width // 2 + 200, height // 2 + 200), 'black', 'Назад', 'white', 40)
        self.buttons.extend([self.level_1, self.level_2, self.level_3, self.back])
        for i in self.buttons:
            i.create()

    def draw(self):
        screen.blit(self.background, (0, 0))
        for i in self.buttons:
            i.update()


class Button:
    def __init__(self, size, pos, color, text, color_text, size_font):
        self.text = text
        self.color_text = color_text
        self.input_text = text
        self.color = color
        self.width = size[0]
        self.height = size[1]
        self.font_size = size_font
        self.x = pos[0]
        self.y = pos[1]

    def create(self):
        self.create_field_button()
        self.create_font()

    def aimed_button_color(self):
        self.button.fill((10, 10, 10))
        pygame.draw.rect(self.button, (250, 250, 250), (0, 0, self.width, self.height), 3)
        self.button.blit(self.output_text, self.auto_font_pos)

    def create(self):
        self.create_field_button()
        self.create_font()

    def aimed_button_color(self):
        self.button.fill((10, 10, 10))
        pygame.draw.rect(self.button, (250, 250, 250), (0, 0, self.width, self.height), 3)
        self.button.blit(self.output_text, self.auto_font_pos)

    def not_aimed_button_color(self):
        self.button.fill('black')
        pygame.draw.rect(self.button, 'white', (0, 0, self.width, self.height), 2)
        self.button.blit(self.output_text, self.auto_font_pos)

    def create_font(self):
        self.font = pygame.font.Font('data/fonts/TunnelFront.ttf', self.font_size)
        self.output_text = self.font.render(self.text, True, self.color_text)
        self.auto_font_pos = (
        self.width // 2 - self.font.size(self.text)[0] // 2, self.height // 2 - self.font.size(self.text)[1] // 2)

    def create_field_button(self):
        self.button = pygame.surface.Surface((self.width, self.height))
        self.button.fill(self.color)
        pygame.draw.rect(self.button, 'white', (0, 0, self.width, self.height), 2)

    def update(self):
        screen.blit(self.button, (self.x, self.y))
        self.button.blit(self.output_text, self.auto_font_pos)
        self.draw()

    def draw(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        if self.x <= self.mouse_pos[0] <= self.x + self.width and self.y <= self.mouse_pos[1] <= self.y + self.height:
            self.aimed_button_color()
            if self.click[0] == 1:
                self.pressed()

        else:
            self.not_aimed_button_color()

    def pressed(self):
        global current_type_tab
        if self.input_text == 'Играть':
            current_type_tab = 'Select_level'
        if self.input_text == 'Настройки':
            current_type_tab = 'Settings'
        if self.input_text == 'Полноэкранный режим':
            full_screen()
        if self.input_text == 'Назад':
            back()
        if self.input_text == 'Выйти':
            quit()
        if self.input_text == 'Уровень 1':
            current_type_tab = 'Game'
            map.select(2)
            ## # для создания карты
            map.generate()
        if self.input_text == 'Уровень 2':
            current_type_tab = 'Game'
            map.select(1)
            map.generate()

            ##


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

    def draw(self, screen, objs, frame):
        '''
        Рисование объектов
        '''
        width, height = screen.get_width(), screen.get_height()
        sx, ex = self.x - width // 2 - 136, self.x + width // 2 + 136
        sy, ey = self.y - height // 2 - 136, self.y + height // 2 + 136
        for obj in objs:
            if sx < obj.x < ex and sy < obj.y < ey:
                obj.draw(screen, self, frame)

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

    def draw(self, screen, camera, frame):
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
            all_sprites.add(Bullet(self.x, self.y, self.get_target(camera), 25, 'big', self.team))
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


class Turret(Entity):
    '''
    Турель
    '''

    def __init__(self, x, y, direction=0, health=100, reload_time=250, ai='enemy', team='enemy'):
        super().__init__(x, y, direction, health, tanks)
        # Загрузка изображений
        self.image_track = pygame.transform.scale(load_image("images/turret_track.png"), (64, 64))
        self.image_turret = pygame.transform.scale(load_image("images/turret_turret.png"), (128, 128))
        self.rect = self.image_track.get_rect()
        # Задаем координаты турели
        self.rect.x = self.x
        self.rect.y = self.y
        # Задаем направление башни турели
        self.turret_direction = direction
        # Время перезарядки
        self.reload_time = reload_time
        self.last_shot_time = 0
        # ИИ
        self.ai = ai
        self.team = team

    def draw(self, screen, camera, frame):
        '''
        Рисование танка
        '''
        width, height = screen.get_width(), screen.get_height()
        # Вычисляем координаты танка на экране при центре в (0, 0)
        x = (camera.x - self.x) * -1
        y = (camera.y - self.y) * -1
        # Получаем направление к цели
        target_angle = self.get_target()
        if target_angle is None:
            target_angle = self.direction - 90
        # Рисуем
        blit_rotate(screen, self.image_track, (x + width // 2, y + height // 2), (32, 32),
                    self.direction * -1)
        blit_rotate(screen, self.image_turret, (x + width // 2, y + height // 2), (64, 64),
                    target_angle * -1 - 90)

    def get_target(self):
        '''
        Получаем цель танка
        '''
        if self.ai == 'enemy':
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
        return target_angle

    def shoot(self):
        if pygame.time.get_ticks() - self.last_shot_time >= self.reload_time:
            all_sprites.add(Bullet(self.x, self.y, self.get_target(), 10, 'small', self.team))
            self.last_shot_time = pygame.time.get_ticks()

    def update(self):
        super().update()
        if self.ai == 'enemy':
            if self.get_target():
                self.shoot()


class Obstacle(Entity):
    '''
    Препятсвтие
    '''

    def __init__(self, x, y, image, cell, can_break=0, skips_bullets=0):
        super().__init__(x, y, 0, [float('inf'), 25][can_break], obstacles)
        self.rect = pygame.Rect(0, 0, cell, cell)
        rect = image.get_rect()
        self.frames = []
        for i in range(rect.w // cell):
            frame_location = (cell * i, 0)
            self.frames.append(image.subsurface(pygame.Rect(
                frame_location, self.rect.size)))
        self.image = self.frames[0]
        self.x = x * cell - 256
        self.y = y * cell - 256
        self.rect.x = self.x
        self.rect.y = self.y
        self.skips_bullets = skips_bullets

    def draw(self, screen, camera, frame):
        '''
        Рисование коробки
        '''
        width, height = screen.get_width(), screen.get_height()
        # Вычисляем координаты коробки на экране при центре в (0, 0)
        x = (camera.x - self.x) * -1 - 32
        y = (camera.y - self.y) * -1 - 32
        # Рисуем
        screen.blit(self.image, (x + width // 2, y + height // 2))
        self.image = self.frames[frame // 60 % len(self.frames)]


class Bullet(Entity):
    '''
    Снаряд
    '''

    def __init__(self, x, y, direction=0, damage=25, size='big', team='player'):
        super().__init__(x, y, direction, float('inf'))
        if size == 'big':
            self.bullet = pygame.transform.scale(load_image(f"images/big_bullet.png"), (28, 8))
        elif size == 'small':
            self.bullet = pygame.transform.scale(load_image(f"images/small_bullet.png"), (8, 8))
        self.rect = pygame.Rect(self.x, self.y, 8, 8)
        self.distance = 0
        self.damage = damage
        self.team = team

    def draw(self, screen, camera, frame):
        '''
        Рисование снаряда
        '''
        width, height = screen.get_width(), screen.get_height()
        # Вычисляем координаты снаряда на экране при центре в (0, 0)
        x = (camera.x - self.x) * -1
        y = (camera.y - self.y) * -1
        # Рисуем
        blit_rotate(screen, self.bullet, (x + width // 2, y + height // 2), (4, 4),
                    self.direction * -1)

    def update(self):
        '''
        Перемещение снаряда
        '''
        self.x += math.cos(math.radians(self.direction)) * 5
        self.y += math.sin(math.radians(self.direction)) * 5
        self.rect.x = self.x + 32
        self.rect.y = self.y + 32
        self.distance += 5
        if self.distance > 500:
            self.kill()
        for i in all_sprites:
            if pygame.sprite.collide_rect(self, i) and i != self and not (
                    type(i) in [Tank, Turret, Bullet] and i.team == self.team) and type(i) is not Bullet and not (
                    type(i) is Obstacle and i.skips_bullets):
                i.health -= self.damage
                self.kill()


class Maps:
    """КЛАСС КАРТ"""

    def __init__(self, main_screen):
        self.screen = main_screen
        self.cell_size = 96

    """создание объектов на карте"""

    def create_obj(self, x, y, image, can_break, skips_bullets=0):
        Obstacle(x, y, image, self.cell_size, can_break, skips_bullets)

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
                                                (self.cell_size * 2, self.cell_size))
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
                    self.create_obj(x, y, self.water, 0, 1)

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
    main_menu = Main_Menu()
    main_menu.create()
    settings = Settings()
    settings.create()
    select_lvl = Select_Level()
    select_lvl.create()
    map = Maps(screen)
    # это для выбора карты или можно map.selectrandod)
    map.select(2)
    # для создания карты
    map.generate()
    # Создаем танк игрока
    player = Tank(5 * 96 - 288 + 48, 5 * 96 - 288 + 48)

    # Создаем танк врага
    enemies.add(Tank(96 - 288 + 48, 96 - 288 + 48, ai='enemy', team='enemy'))
    enemies.add(Turret(9 * 96 - 288 + 48, 9 * 96 - 288 + 48))

    # Создаем камеру
    camera = Camera(5 * 96 - 288 + 48, 5 * 96 - 288 + 48, 0, player)
   # Добавляем танки во группу спрайтов
#
    ## Часы
    clock = pygame.time.Clock()
    frame = 0

    # Основной цикл
    running = True
    while running:
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


        if current_type_tab == 'Main_Menu':
            main_menu.draw()
        if current_type_tab == 'Settings':
            settings.draw()
        if current_type_tab == 'Select_level':
            select_lvl.draw()
        if current_type_tab == 'Game':
            screen.fill((0, 0, 0))
            # Обновляем
            all_sprites.update()
            camera.update()

            # Рисуем все что надо
            s = max(WIDTH, HEIGHT) * 1.42  # Типа корень из двух
            test_screen = pygame.Surface((s, s))
            map.draw(test_screen, camera)
            camera.draw(test_screen, all_sprites, frame)
            blit_rotate(screen, test_screen, (WIDTH // 2, HEIGHT // 2), (s // 2, s // 2), camera.angle)
            # Обновляем экран
            pygame.display.flip()

            frame += 1
            # Ждем следующий кадр

        # Обновляем экран
        pygame.display.flip()

        # Ждем следующий кадр
        clock.tick(60)
pygame.quit()
