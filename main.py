import os
import sys
import math
import pygame
import random
import sqlite3

pygame.init()
size = WIDTH, HEIGHT = 1024, 680
MAPS = ['data/maps/map1.txt', 'data/maps/mines.txt', 'data/maps/maze.txt']
size_monitor = width_monitor, height_monitor = (pygame.display.Info().current_w, pygame.display.Info().current_h)
size_screen = width_screen, height_screen = 1024, 680
screen = pygame.display.set_mode(size_screen)
all_sprites = pygame.sprite.Group()
tanks = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
CAMERA_X, CAMERA_Y = 0, 0




aimed_button_sound = pygame.mixer.Sound('data/sounds/aimed_button_sound.ogg')
clicked_button_sound = pygame.mixer.Sound("data/sounds/clicked_button_sound.ogg")
clicked_button_sound.set_volume(0.1)
aimed_button_sound.set_volume(0.5)

is_full_screen = False
current_type_tab = 'Main_Menu'
input_name = ''
basedata = 'data/basedata/basedata.db'


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


def check_actived_accounts():
    """Это функция для проверки последнего выюранного аккаунта"""

    con = sqlite3.connect(basedata)
    list_for_enter = con.cursor().execute("""SELECT account_names FROM accounts WHERE actived=1""").fetchall()
    if list_for_enter:
        con.commit()
        con.close()
        return list_for_enter[0][0]
    con.commit()
    con.close()
    return ''


def full_screen():
    """Это функция для создания полноэкранного режима в игре"""

    global screen, width_screen, height_screen, size_screen, width_monitor, height_monitor, is_full_screen
    if not is_full_screen:
        size_screen = width_screen, height_screen = width_monitor, height_monitor
        screen = pygame.display.set_mode(size_monitor, pygame.FULLSCREEN)
        is_full_screen = True
    else:
        size_screen = width_screen, height_screen = 1024, 680
        screen = pygame.display.set_mode(size_screen)
        is_full_screen = False
    update_window()


def update_window():
    """Это функция для обновления всех вкладок"""

    tabs = [main_menu, settings, select_lvl, acc_list, acc_create, acc]
    for tab in tabs:
        tab.__init__()
        tab.create()


def reset_all_input_text():
    """Это функция для очищения всех полей с вводом"""

    global input_name
    acc_create.create_font('')
    input_name = ''


def back_to_menu():
    """Это функция для возвращения к предыдущей вкладке"""

    global current_type_tab
    if current_type_tab == 'Account_Create':
        current_type_tab = 'Accounts'
        acc.__init__()
        acc.create()
    elif current_type_tab == 'Accounts':
        current_type_tab = 'Settings'
        settings.__init__()
        settings.create()
    else:
        current_type_tab = 'Main_Menu'
        main_menu.__init__()
        main_menu.create()
    reset_all_input_text()


def quit():
    """Это функция для выхода из игры"""

    global running
    running = False


def add_account():
    """Это функция для создания аккаунта"""

    global current_type_tab, input_name, current_name_user
    con = sqlite3.connect(basedata)

    check_quantity_exec = """SELECT id FROM accounts"""
    check_quantity = con.cursor().execute(check_quantity_exec).fetchall()
    if len(check_quantity) + 1 > 15:
        print('Нельзя иметь больше 15 аккаунтов')
        con.commit()
        con.close()
        return None
    if not input_name:
        print('Имя не может быть пустым')
        con.commit()
        con.close()
        return None
    add_account_exec = f"""INSERT INTO accounts(id, account_names, actived) VALUES({check_quantity[-1][0] + 1 if check_quantity else 1}, "{input_name}", 1);"""
    con.cursor().execute(add_account_exec).fetchall()
    con.commit()
    con.close()

    current_type_tab = 'Accounts'
    reset_all_input_text()

    acc_list.__init__()
    acc_list.create()


def save():
    """Это функция делает аккаунт активным"""

    con = sqlite3.connect(basedata)
    con.cursor().execute("""UPDATE accounts SET actived=0""").fetchall()
    con.cursor().execute(f"""UPDATE accounts SET actived=1 WHERE account_names='{current_name_user}'""").fetchall()
    con.commit()
    con.close()


def delete_account(name):
    """Это функция удаляет аккаунт"""

    global current_name_user
    con = sqlite3.connect(basedata)
    con.cursor().execute(f"""DELETE FROM accounts WHERE account_names='{name}'""").fetchall()
    if name == current_name_user:
        current_name_user = ''
    con.commit()
    con.close()

    acc_list.__init__()
    acc_list.create()
    settings.__init__()
    settings.create()


def create_buttons_in_tab(list):
    """Это функция создает кнопки"""

    for button in list:
        button.create()


def update_buttons_in_tab(list):
    """Это функция обновляет кнопки"""

    for button in list:
        button.update()


class Account_List:
    """Класс списка аккаунтов"""

    """Для инициализации текстур"""

    def __init__(self):
        self.background = pygame.transform.scale(load_image('images/background_list.png'),
                                                 (width_screen // 2 - 10, height_screen - 100))
        pygame.draw.rect(self.background, 'black', (0, 0, width_screen // 2 - 10, height_screen - 100), 5)

    """Для создания списка с аккаунтами и кнопок"""

    def create(self):
        self.accounts = []
        count = 50
        con = sqlite3.connect(basedata)
        list_accounts = con.cursor().execute("""SELECT account_names FROM accounts""").fetchall()
        con.commit()
        con.close()

        for acc in list_accounts:
            count += 40
            account_button = Button((width_screen // 2 - 20, 30), (width_screen // 2 + 5, count), acc[0], 20, 0)
            account_button.create()
            self.accounts.append(account_button)

    """Для отрисовки элементов"""

    def draw(self):
        screen.blit(self.background, (width_screen // 2, 50))
        update_buttons_in_tab(self.accounts)


class Account_Create:
    """Класс вкладки для создания аккаунтов"""

    """Для инициализации текстур"""

    def __init__(self):
        self.background = pygame.transform.scale(load_image('images/background_reg.png'), (width_screen, height_screen))
        self.field_input = pygame.surface.Surface((250, 50))
        pygame.draw.rect(self.field_input, 'white', (0, 0, 250, 50), 1)

    """Для создания кнопок и других элементов"""

    def create(self):
        save = Button((200, 80), (width_screen // 2 - 100, height_screen // 2 + 80), 'Сохранить', 32)
        back = Button((200, 80), (50, height_screen // 2 + 0.25 * height_screen), 'Назад', 40)
        self.buttons = [save, back]
        create_buttons_in_tab(self.buttons)
        reset_all_input_text()

    """Для создания кнопок и поля ввода с текстом"""

    def create_font(self, input_name_account):
        font = pygame.font.Font('data/fonts/TunnelFront.ttf', 28)
        self.ready_text = font.render(input_name_account, True, 'white')

    """Для отрисовки элементов"""

    def draw(self):
        screen.blit(self.background, (0, 0))
        screen.blit(self.field_input, (width_screen // 2 - 125, height_screen // 2))
        screen.blit(self.ready_text, (width_screen // 2 - 115, height_screen // 2 + 5))
        update_buttons_in_tab(self.buttons)


class Accounts:
    """Класс вкладки с аккаунтами"""

    """Для инициализации текстур"""

    def __init__(self):
        self.background = pygame.transform.scale(load_image('images/background_acc.png'), (width_screen, height_screen))

    """Для создания кнопок и других элементов"""

    def create(self):
        create_new_account = Button((200, 80), (50, height_screen // 2 - 0.25 * height_screen), 'Новый аккаунт', 26)
        back = Button((200, 80), (50, height_screen // 2 + 0.25 * height_screen), 'Назад', 40)
        self.buttons = [back, create_new_account]
        create_buttons_in_tab(self.buttons)

    """Для отрисовки элементов"""

    def draw(self):
        screen.blit(self.background, (0, 0))
        update_buttons_in_tab(self.buttons)


class Settings:
    """Класс вкладки с настройками"""

    """Для инициализации текстур"""

    def __init__(self):
        self.background = pygame.transform.scale(load_image('images/background_settings.png'),
                                                 (width_screen, height_screen))
        self.buttons = []

    """Для создания кнопок и других элементов"""

    def create(self):
        full_display = Button((200, 80), (width_screen // 2 - 100, height_screen // 2 - 200), 'Full Screen', 32)
        accounts = Button((200, 80), (width_screen // 2 - 100, height_screen // 2 - 100), 'Аккаунты', 32)
        back = Button((200, 80), (width_screen - 250, height_screen // 2 + 0.25 * height_screen), 'Назад', 40)
        self.buttons = [full_display, accounts, back]
        create_buttons_in_tab(self.buttons)
        self.create_text_user()

    """Для создания текста с  текущем пользователем и кнопок"""

    def create_text_user(self):
        global current_name_user
        font = pygame.font.Font('data/fonts/TunnelFront.ttf', 28)
        self.output_text = font.render("Текущий пользователь:" + current_name_user, True, 'black')

    """Для отрисовки элементов"""

    def draw(self):
        screen.blit(self.background, (0, 0))
        screen.blit(self.output_text, (50, 50))
        update_buttons_in_tab(self.buttons)


class Main_Menu:
    """Класс главного меню"""

    """Для инициализации текстур"""

    def __init__(self):
        self.background = pygame.transform.scale(load_image('images/background.png'), (width_screen, height_screen))

    """Для создания кнопок и других элементов"""

    def create(self):
        play = Button((200, 80), (width_screen // 2 - 100, height_screen // 2 + 30), 'Играть', 40)
        settings = Button((200, 80), (width_screen // 2 - 100, height_screen // 2 + 120), 'Настройки', 40)
        quit = Button((200, 80), (width_screen // 2 - 100, height_screen // 2 + 210), 'Выйти', 40)
        self.buttons = [play, settings, quit]
        create_buttons_in_tab(self.buttons)

    """Для отрисовки элементов"""

    def draw(self):
        screen.blit(self.background, (0, 0))
        update_buttons_in_tab(self.buttons)


class Select_Level:
    """Класс вкладки с выбором уровней"""

    """Для инициализации текстур"""

    def __init__(self):
        self.background = pygame.transform.scale(load_image('images/background_select_level.png'),
                                                 (width_screen, height_screen))
        self.buttons = []

    """Для создания кнопок и других элементов"""

    def create(self):
        level_1 = Button((200, 200), (0.1 * width_screen, 0.2 * height_screen), 'Уровень 1', 30)
        level_2 = Button((200, 200), (0.1 * width_screen + 220, 0.2 * height_screen), 'Уровень 2', 30)
        level_3 = Button((200, 200), (0.11 * width_screen + 440, 0.2 * height_screen), 'Уровень 3', 30)
        back = Button((200, 80), (width_screen // 2 + 200, height_screen // 2 + 200), 'Назад', 40)
        self.buttons = [level_1, level_2, level_3, back]
        create_buttons_in_tab(self.buttons)

    """Для отрисовки элементов"""

    def draw(self):
        screen.blit(self.background, (0, 0))
        update_buttons_in_tab(self.buttons)


class Button:
    """Класс кнопки"""

    """Для инициализации параметров кнопки"""

    def __init__(self, size, pos, text, size_font, button=1):
        self.check_button = button
        self.input_text = text
        self.width = size[0]
        self.height = size[1]
        self.font_size = size_font
        self.x = pos[0]
        self.y = pos[1]
        self.played = False

    """Для создания кнопки"""

    def create(self):
        self.create_field_button()
        self.create_font_and_text()

    """Для изменения цвета кнопки при наведении"""

    def aimed_button_color(self):

        self.button.fill((10, 10, 10))
        if not self.played:
            aimed_button_sound.play()
            self.played = True
        pygame.draw.rect(self.button, (250, 250, 250), (0, 0, self.width, self.height), 4)
        self.button.blit(self.output_text, self.auto_font_pos)

    """Для изменения цвета кнопки при наведении"""

    def not_aimed_button_color(self):
        self.played = False
        self.button.fill('black')
        pygame.draw.rect(self.button, 'white', (0, 0, self.width, self.height), 2)
        self.button.blit(self.output_text, self.auto_font_pos)

    """Для создания текста на кнопке"""

    def create_font_and_text(self):
        font = pygame.font.Font('data/fonts/TunnelFront.ttf', self.font_size)
        self.output_text = font.render(self.input_text, True, 'white')
        self.auto_font_pos = (
            self.width // 2 - font.size(self.input_text)[0] // 2, self.height // 2 - font.size(self.input_text)[1] // 2)

    """Для создания поля кнопки"""

    def create_field_button(self):
        self.button = pygame.surface.Surface((self.width, self.height))
        self.button.fill('black')
        pygame.draw.rect(self.button, 'white', (0, 0, self.width, self.height), 2)

    """Для обновления кнопки"""

    def update(self):
        screen.blit(self.button, (self.x, self.y))
        self.button.blit(self.output_text, self.auto_font_pos)
        self.draw()

    """Для отрисовки кнопки"""

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            self.aimed_button_color()
            if click[0] == 1:
                self.pressed()
            elif click[2] and not self.check_button:
                delete_account(self.input_text)
        else:
            self.not_aimed_button_color()

    """Для отслеэивания нажатой кнопки"""

    def pressed(self):
        global current_type_tab, current_name_user
        clicked_button_sound.play()
        if self.check_button:
            if self.input_text == 'Играть':
                current_type_tab = 'Select_level'
            if self.input_text == 'Настройки':
                current_type_tab = 'Settings'
            if self.input_text == 'Новый аккаунт':
                current_type_tab = 'Account_Create'
            if self.input_text == 'Аккаунты':
                current_type_tab = 'Accounts'
                acc_list.create()
            if self.input_text == 'Full Screen':
                full_screen()
            if self.input_text == 'Назад':
                back_to_menu()
            if self.input_text == 'Выйти':
                quit()
            if self.input_text == 'Сохранить':
                add_account()
        else:
            current_name_user = self.input_text
            save()
            update_window()


clock = pygame.time.Clock()

running = True

main_menu = Main_Menu()
main_menu.create()

current_name_user = check_actived_accounts()

settings = Settings()
settings.create()

acc_list = Account_List()

select_lvl = Select_Level()
select_lvl.create()

acc = Accounts()
acc.create()

acc_create = Account_Create()
acc_create.create()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == 27:
            current_type_tab = 'Main_Menu'
            update_window()
        if event.type == pygame.KEYDOWN and current_type_tab == 'Account_Create':
            if event.unicode != '' and event.unicode != ' ' and event.unicode != '  ' and pygame.key.name(
                    event.key) != 'backspace':
                if len(input_name) <= 15:
                    input_name += event.unicode
                    acc_create.create_font(input_name)
                else:
                    print('Длина имени не может больше 15 симовлов')
            if pygame.key.name(event.key) == 'backspace' and input_name:
                input_name = input_name[0:-1]
                acc_create.create_font(input_name)

    if current_type_tab == 'Main_Menu':
        main_menu.draw()
    if current_type_tab == 'Settings':
        settings.draw()
    if current_type_tab == 'Select_level':
        select_lvl.draw()
    if current_type_tab == 'Accounts':
        acc.draw()
        acc_list.draw()
    if current_type_tab == 'Account_Create':
        acc_create.draw()
    pygame.display.flip()
    clock.tick(60)

save()
pygame.quit()

fwef
wf
wfwef
wef
wf
we



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
        image_track_left = pygame.transform.scale(load_image("images/tank_track_left.png"), (192, 64))
        tank_track_right = pygame.transform.scale(load_image("images/tank_track_right.png"), (192, 64))
        self.image_turret = pygame.transform.scale(load_image("images/tank_turret.png"), (128, 128))
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.frames_left = []
        self.frames_right = []
        for i in range(3):
            frame_location = (64 * i, 0)
            self.frames_left.append(image_track_left.subsurface(pygame.Rect(
                frame_location, self.rect.size)))
            self.frames_right.append(tank_track_right.subsurface(pygame.Rect(
                frame_location, self.rect.size)))
        self.image_track_left = self.frames_left[0]
        self.image_track_right = self.frames_right[0]

        self.shoot_sound = pygame.mixer.Sound('data/sounds/tank_shoot.wav')
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

        self.turning = 0
        self.moving = 0

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
        self.moving = multiplier / abs(multiplier)

    def turn(self, angle):
        '''
        Поворот танка
        '''
        self.direction += angle
        self.turning = angle / abs(angle)

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
        if self.moving == 1:
            self.image_track_left = self.frames_left[frame // 5 % 3]
            self.image_track_right = self.frames_right[frame // 5 % 3]
        elif self.moving == -1:
            self.image_track_left = self.frames_left[(frame // 5 % 3 + 1) * -1]
            self.image_track_right = self.frames_right[(frame // 5 % 3 + 1) * -1]
        elif self.turning == -1:
            self.image_track_left = self.frames_left[(frame // 5 % 3 + 1) * -1]
            self.image_track_right = self.frames_right[frame // 5 % 3]
        elif self.turning == 1:
            self.image_track_left = self.frames_left[frame // 5 % 3]
            self.image_track_right = self.frames_right[(frame // 5 % 3 + 1) * -1]
        blit_rotate(screen, self.image_track_left, (x + width // 2, y + height // 2), (32, 32),
                    self.direction * -1)
        blit_rotate(screen, self.image_track_right, (x + width // 2, y + height // 2), (32, 32),
                    self.direction * -1)
        blit_rotate(screen, self.image_turret, (x + width // 2, y + height // 2), (64, 64),
                    target_angle * -1 - 90)
        self.turning = 0
        self.moving = 0

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
            self.shoot_sound.set_volume((1 - distance(self.x, self.y, CAMERA_X, CAMERA_Y) / 1080) / 2)
            self.shoot_sound.play()
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

        self.shoot_sounds = [pygame.mixer.Sound(f'data/sounds/turret_shoot_{i}.wav') for i in range(1, 7)]
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
            shoot_sound = self.shoot_sounds[random.randint(0, 5)]
            shoot_sound.set_volume((1 - distance(self.x, self.y, CAMERA_X, CAMERA_Y) / 3000) / 2)
            shoot_sound.play()
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

    def __init__(self, x, y, image, cell, can_break=0, skips_bullets=0, have_loot=0):
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
        self.have_loot = have_loot
        self.break_sound = pygame.mixer.Sound(f'data/sounds/obstacle_break.wav')

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

    def update(self):
        if self.health <= 0:
            if self.have_loot and random.randint(0, 1):
                Bonus(self.x, self.y, random.randint(0, 1))
            self.break_sound.set_volume((1 - distance(self.x, self.y, CAMERA_X, CAMERA_Y) / 3000) / 2)
            self.break_sound.play()
            self.kill()


class Bonus(Entity):
    def __init__(self, x, y, type):
        super().__init__(x, y, random.randint(0, 359), 25, all_sprites)
        if type == 0:
            self.image = pygame.transform.scale(load_image(f"images/medecine.png"), (64, 64))
        elif type == 1:
            self.image = pygame.transform.scale(load_image(f"images/shield.png"), (64, 64))
        self.rect = self.image.get_rect()
        self.bonus_type = type
        self.x = x
        self.y = y
        self.rect.x = self.x + 32
        self.rect.y = self.y + 32
        self.take_sound = pygame.mixer.Sound(f'data/sounds/bonus_take.wav')

    def draw(self, screen, camera, frame):
        '''
        Рисование коробки
        '''
        width, height = screen.get_width(), screen.get_height()
        x = (camera.x - self.x) * -1
        y = (camera.y - self.y) * -1
        # Рисуем
        screen.blit(self.image, (x + width // 2, y + height // 2))

    def update(self):
        if self.health <= 0:
            self.kill()
        for i in pygame.sprite.spritecollide(self, all_sprites, False):
            if type(i) is Tank:
                if self.bonus_type == 0:
                    if i.health <= 75:
                        i.health += 25
                    else:
                        i.health = 100
                if self.bonus_type == 1:
                    Shield(i)
                self.take_sound.set_volume((1 - distance(self.x, self.y, CAMERA_X, CAMERA_Y) / 3000) / 2)
                self.take_sound.play()
                self.kill()


class Shield(Entity):
    def __init__(self, attached_entity):
        super().__init__(attached_entity.x, attached_entity.y, 0, 25, all_sprites)
        self.rect = pygame.Rect(attached_entity.x - 72, attached_entity.y - 72, 144, 144)
        self.x = attached_entity.x - 72
        self.y = attached_entity.y - 72
        self.attached_entity = attached_entity
        self.team = attached_entity.team

    def draw(self, screen, camera, frame):
        '''
        Рисование коробки
        '''
        width, height = screen.get_width(), screen.get_height()
        x = (camera.x - self.x) * -1
        y = (camera.y - self.y) * -1
        # Рисуем
        shield_surface = pygame.Surface((1000, 750), pygame.SRCALPHA)
        pygame.draw.ellipse(shield_surface, (0, 191, 255), pygame.Rect(0, 0, 144, 144))
        shield_surface.set_alpha(50)
        screen.blit(shield_surface, (x + width // 2, y + height // 2))
        pygame.draw.ellipse(screen, (0, 191, 255), pygame.Rect(x + width // 2, y + height // 2, 144, 144), width=2)

    def update(self):
        if self.health <= 0:
            self.kill()
        self.x = self.attached_entity.x - 72
        self.y = self.attached_entity.y - 72
        self.rect.x = self.attached_entity.x - 72
        self.rect.y = self.attached_entity.y - 72
        for i in pygame.sprite.spritecollide(self, all_sprites, False):
            if i != self and type(i) is Shield and i.attached_entity == self.attached_entity:
                i.health += 25
                self.kill()


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
        for i in pygame.sprite.spritecollide(self, all_sprites, False):
            if i != self and not (
                    type(i) in [Tank, Turret, Shield] and i.team == self.team) and type(i) is not Bullet and not (
                    type(i) is Obstacle and i.skips_bullets):
                i.health -= self.damage
                self.kill()


class Maps:
    """КЛАСС КАРТ"""

    def __init__(self, main_screen):
        self.screen = main_screen
        self.cell_size = 96

    """создание объектов на карте"""

    def create_obj(self, x, y, image, can_break, skips_bullets=0, have_loot=0):
        Obstacle(x, y, image, self.cell_size, can_break, skips_bullets, have_loot)

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
                    self.create_obj(x, y, self.light_box, 1, have_loot=1)
                if self.map[y][x] == 'W':
                    self.fill_ground_png(x, y)
                    self.create_obj(x, y, self.bush, 0)
                if self.map[y][x] == 'D':
                    self.fill_ground_png(x, y)
                    self.create_obj(x, y, self.dark_box, 1, have_loot=1)
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
    # передается главный экран где будут отображаться все объекты
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

    # Часы
    clock = pygame.time.Clock()
    frame = 0
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
        CAMERA_X, CAMERA_Y = camera.x, camera.y
        # Рисуем все что надо
        s = max(WIDTH, HEIGHT) * 1.42  # Типа корень из двух
        test_screen = pygame.Surface((s, s))
        map.draw(test_screen, camera)
        camera.draw(test_screen, all_sprites, frame)
        blit_rotate(screen, test_screen, (WIDTH // 2, HEIGHT // 2), (s // 2, s // 2), camera.angle)

        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 10, player.health * 2, 50), width=0)
        pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(10 + player.health * 2, 10, 200 - player.health * 2, 50),
                         width=0)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 10, 200, 50), width=2)
        # Обновляем экран
        pygame.display.flip()

        frame += 1
        # Ждем следующий кадр
        clock.tick(60)
pygame.quit()