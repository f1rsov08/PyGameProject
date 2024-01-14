import pygame
import os
import sys
import sqlite3

pygame.init()
disp = pygame.display.Info()
size_full_screen = width1, height1 = (disp.current_w, disp.current_h)
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
full_screen_coef = 1
current_type_tab = 'Main_Menu'
current_name_user = ''


def account_list():
    back_surface = pygame.surface.Surface()


def check_accs():
    print(1)
    basedata = 'basedata.db'
    con = sqlite3.connect(basedata)
    cur = con.cursor()
    for_enter = cur.execute("""SELECT account_names FROM accounts WHERE actived=1""").fetchall()
    print(for_enter)
    # for_spisok = cur.execute("""SELECT account_names FROM accounts""").fetchall()
    con.close()
    return for_enter[0][0]

def full_screen():
    global screen, width, height, size, width1, height1, full_screen_coef
    if full_screen_coef:
        size = width, height = width1, height1
        screen = pygame.display.set_mode(size_full_screen, pygame.FULLSCREEN)
        full_screen_coef = 0
        update_after_change_size_screen()
    else:
        size = width, height = 800, 800
        screen = pygame.display.set_mode(size)
        update_after_change_size_screen()
        full_screen_coef = 1


def update_after_change_size_screen():
    settings.__init__()
    settings.create()
    select_lvl.__init__()
    select_lvl.create()
    acc.__init__()
    acc.create()
    text.__init__()
    text.create()


def back():
    global current_type_tab
    current_type_tab = 'Main_Menu'
    main_menu.__init__()
    main_menu.create()
    text.create_font('')


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


def save():
    global current_type_tab, input_name, current_name_user
    basedata = 'basedata.db'
    con = sqlite3.connect(basedata)
    cur = con.cursor()
    # for_enter = cur.execute("""SELECT account_names FROM accounts WHERE actived=1""").fetchall()
    # for_spisok = cur.execute("""SELECT account_names FROM accounts""").fetchall()
    exec2 = """SELECT id FROM accounts"""
    for_id = cur.execute(exec2).fetchall()
    if not for_id:
        exec1 = f"""INSERT INTO accounts(id, account_names, actived) VALUES(1, "{input_name}", 1);"""
        for_add1 = cur.execute(exec1).fetchall()
    else:
        exec3 = f"""INSERT INTO accounts(id, account_names, actived) VALUES({for_id[-1][0] + 1}, "{input_name}", 0);"""
        for_add2 = cur.execute(exec3).fetchall()
    current_type_tab = 'Accounts'
    current_name_user = input_name
    input_name = ''
    con.commit()
    con.close()
    text.create_font('')
    main_menu.__init__()
    main_menu.create()
    settings.__init__()
    settings.create()


def before_quit():
    basedata = 'basedata.db'
    con = sqlite3.connect(basedata)

    # Создание курсора
    cur = con.cursor()

    # Выполнение запроса и получение всех результатов
   # for_enter = cur.execute("""SELECT account_names FROM accounts WHERE actived=1""").fetchall()
    for_spisok = cur.execute("""UPDATE accounts SET actived=0""").fetchall()
    # for_add = cur.execute("""INSERT INTO accounts(account_names) VALUES(?)""", (input_name,).fetchall()
    print(current_name_user)
    for_actived_last = cur.execute(f"""UPDATE accounts SET actived=1 WHERE account_names='{current_name_user}'""").fetchall()

    con.commit()
    con.close()

#def before_enter():
#    global current_name_user
#    basedata = 'basedata.db'
#    con = sqlite3.connect(basedata)
#
#    cur = con.cursor()
#
#    # Выполнение запроса и получение всех результатов
#    # for_enter = cur.execute("""SELECT account_names FROM accounts WHERE actived=1""").fetchall()
#    for_spisok = cur.execute("""SELECT accounts SET actived=0""").fetchall()
#    # for_add = cur.execute("""INSERT INTO accounts(account_names) VALUES(?)""", (input_name,).fetchall()
#    print(for_spisok)
#    for_actived_last = f"""UPDATE accounts SET actived=1 WHERE account_names="{current_name_user}")"""
#
#    con.commit()
#    con.close()


class Input_Text:
    def __init__(self):
        self.background = pygame.transform.scale(load_image('images/background_reg.png'), (width, height))
        self.buttons = []

    def create(self):
        self.field_input = pygame.surface.Surface((250, 50))
        self.save = Button((200, 80), (0, height // 2), 'black', 'Сохранить', 'white', 20)
        self.back = Button((200, 80), (0, height // 2 + 200), 'black', 'Назад', 'white', 20)
        self.back.create()
        self.save.create()
        self.create_font('')

    def create_font(self, text):
        self.font = pygame.font.Font('data/fonts/TunnelFront.ttf', 28)
        self.output_text = self.font.render(text, True, 'white')

    def draw(self):
        screen.blit(self.background, (0, 0))
        screen.blit(self.field_input, (width // 2 - 125, height // 2))
        screen.blit(self.output_text, (width // 2 - 115, height // 2 + 5))
        self.save.update()
        self.back.update()


class Accounts:
    def __init__(self):
        self.background = pygame.transform.scale(load_image('images/background_acc.png'), (width, height))
        self.list_acc = pygame.surface.Surface((width // 2 - 10, height - 100))
        # pygame.draw.rect(self.background, (255, 255, 255, 0.1), (0, 0, width, height))

        self.buttons = []

    def create(self):
        self.new_acc = Button((200, 80), (50, height // 2 - 200), 'black', 'Новый аккаунт', 'white', 20)
        self.back = Button((200, 80), (50, height // 2 + 200), 'black', 'Назад', 'white', 40)
        self.buttons.extend([self.new_acc, self.back])
        for i in self.buttons:
            i.create()


    def draw(self):
        screen.blit(self.background, (0, 0))
        screen.blit(self.list_acc, (width // 2, 20))
        for i in self.buttons:
            i.update()


class Settings:
    def __init__(self):
        self.background = pygame.transform.scale(load_image('images/background_settings.png'), (width, height))
        self.buttons = []

    def create(self):
        self.full_display = Button((200, 80), (width // 2 - 100, height // 2 - 200), 'black', 'Полноэкранный режим',
                                   'white', 20)
        self.accounts = Button((200, 80), (width // 2 - 100, height // 2 - 100), 'black', 'Аккаунты', 'white', 30)
        self.back = Button((200, 80), (width // 2 + 200, height // 2 + 200), 'black', 'Назад', 'white', 40)

        self.buttons.extend([self.full_display, self.back, self.accounts])
        self.create_font()
        for i in self.buttons:
            i.create()

    def create_font(self):
        global current_name_user
        print(current_name_user, 13123213)
        self.font = pygame.font.Font('data/fonts/TunnelFront.ttf', 28)
        self.output_text = self.font.render("Текущий пользователь:" + current_name_user, True, 'black')

    def draw(self):
        screen.blit(self.background, (0, 0))
        screen.blit(self.output_text, (50, 50))
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
        print(width, height)
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
        if self.input_text == 'Аккаунты':
            current_type_tab = 'Accounts'
        if self.input_text == 'Сохранить':
            save()
        if self.input_text == 'Новый аккаунт':
            current_type_tab = 'Input_Text'


clock = pygame.time.Clock()
running = True
screen.fill('green')
input_name = ''
main_menu = Main_Menu()
main_menu.create()
current_name_user = check_accs()
settings = Settings()
settings.create()
select_lvl = Select_Level()
select_lvl.create()
acc = Accounts()
acc.create()
text = Input_Text()
text.create()
print(current_name_user)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and current_type_tab == 'Input_Text':
            if event.unicode != '' and event.unicode != ' ' and pygame.key.name(event.key) != 'backspace' and len(input_name) <= 15:
                input_name += event.unicode
                text.create_font(input_name)
            if pygame.key.name(event.key) == 'backspace' and input_name:
                input_name = input_name[0:-1]
                text.create_font(input_name)
    if current_type_tab == 'Main_Menu':
        main_menu.draw()
    if current_type_tab == 'Settings':
        settings.draw()
    if current_type_tab == 'Select_level':
        select_lvl.draw()
    if current_type_tab == 'Accounts':
        acc.draw()
    if current_type_tab == 'Input_Text':
        text.draw()
    pygame.display.flip()
    clock.tick(60)

before_quit()
pygame.quit()
