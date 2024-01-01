import os
import sys
import math
import pygame
import random
from mapgenerating import Maps, obstacles

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()


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
            obj.draw(screen, self.x, self.y)


class Entity(pygame.sprite.Sprite):
    '''
    Сущность
    '''

    def __init__(self, x, y, direction=0, health=100):
        super().__init__(all_sprites)
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
        super().__init__(x, y, direction, health)
        # Загрузка изображений
        self.image_track = pygame.transform.scale(load_image("tank_track.png"), (128, 128))
        self.image_turret = pygame.transform.scale(load_image("tank_turret.png"), (128, 128))
        self.rect = self.image_track.get_rect()
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

    def get_tank_obj(self):
        return self.image_track

    def turn(self, angle):
        '''
        Поворот танка
        '''
        self.direction += angle

    def getcoords(self):
        return (self.x, self.y)

    def draw(self, screen, camera_x, camera_y):
        '''
        Рисование танка
        '''
        # Вычисляем координаты танка на экране при центре в (0, 0)
        x = (camera_x - self.x) * -1
        y = (camera_y - self.y) * -1
        # Получаем координаты цели
        target_x, target_y = self.get_target()
        # Вычисляем координаты цели относительно танка
        target_x, target_y = target_x - x, target_y - y
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
        # Рисуем
        blit_rotate(screen, self.image_track, (x + width // 2, y + height // 2), (64, 64),
                    self.direction * -1)
        blit_rotate(screen, self.image_turret, (x + width // 2, y + height // 2), (64, 64),
                    target_angle * -1)

    def get_target(self):
        '''
        Получаем цель танка
        '''
        if self.ai == 'player':
            # Если танком управляет игрок, то функция возвращает координаты мыши
            x, y = pygame.mouse.get_pos()
            return x - width // 2, y - height // 2
        elif self.ai == 'enemy':
            # Если танком управляет враг, то функция возвращает координаты ближайшего игрока
            return sorted(filter(lambda sprite: type(sprite) is Tank and sprite.ai == 'player', all_sprites),
                          key=lambda sprite: distance(self.x, self.y, sprite.x, sprite.y))[0].coords()
        else:
            # Если кто-то другой, то 0, 0
            return 0, 0



if __name__ == '__main__':
    map = Maps(screen) #передается главный экран где будут отображаться все объекты
    map.select(1) #это для выбора карты или можно map.select(номер карты по счету) ---- 1 - песчаная карта, 2 - травяная карта
    map.generate() #для создания мапы

    # Создаем танк игрока
    tank = Tank(0, 0)
    # Создаем танк врага
    enemy_tank = Tank(40, 40, ai='enemy')

    # Создаем камеру
    camera = Camera(0, 0, tank)

    # Добавляем танки во группу спрайтов

    all_sprites.add(tank)
    all_sprites.add(enemy_tank)

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

        # Получаем кнопки, которые нажаты
        keys = pygame.key.get_pressed()
        # Управление на WASD
        if keys[pygame.K_w]:
            #print((tank.x + 200) // map.obj_size + 1, (tank.y + 200) // map.obj_size + 1, map.map)
            #if map.map[int((tank.y + 200) // map.obj_size + 1)][int((tank.x + 200) // map.obj_size + 1)] == '.':
            tank.move()
        if keys[pygame.K_s]:
            #if map.map[int((tank.y + 200) // map.obj_size + 1)][int((tank.x + 200) // map.obj_size + 1)] == '.':
            tank.move(-1)
        if keys[pygame.K_a]:
            tank.turn(-1.5)
        if keys[pygame.K_d]:
            tank.turn(1.5)
        map.update(tank.getcoords(), all_sprites)
        camera.update()

        # Рисуем все что надо
        camera.draw(screen, all_sprites)

        # Обновляем экран
        pygame.display.flip()

        # Ждем следующий кадр
        clock.tick(60)
pygame.quit()
