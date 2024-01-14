import pygame
import os
import sys
import sqlite3

"""Это класс меню игры"""
pygame.init()


size_monitor = width_monitor, height_monitor = (pygame.display.Info().current_w, pygame.display.Info().current_h)
size_screen = width_screen, height_screen = 1024, 680
screen = pygame.display.set_mode(size_screen)

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
        self.background = pygame.transform.scale(load_image('images/background_list.png'),(width_screen // 2 - 10, height_screen - 100))
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
            account_button = Button((width_screen // 2 - 20, 30), (width_screen // 2 + 5, count),  acc[0],  20, 0)
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
        save = Button((200, 80), (width_screen // 2 - 100, height_screen // 2 + 80),  'Сохранить',  32)
        back = Button((200, 80), (50, height_screen // 2 + 0.25 * height_screen),  'Назад',  40)
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
        create_new_account = Button((200, 80), (50, height_screen // 2 - 0.25 * height_screen),  'Новый аккаунт',  26)
        back = Button((200, 80), (50, height_screen // 2 + 0.25 * height_screen),  'Назад',  40)
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
        self.background = pygame.transform.scale(load_image('images/background_settings.png'), (width_screen, height_screen))
        self.buttons = []

    """Для создания кнопок и других элементов"""

    def create(self):
        full_display = Button((200, 80), (width_screen // 2 - 100, height_screen // 2 - 200),  'Full Screen', 32)
        accounts = Button((200, 80), (width_screen // 2 - 100, height_screen // 2 - 100),  'Аккаунты',  32)
        back = Button((200, 80), (width_screen - 250, height_screen // 2 + 0.25 * height_screen),  'Назад',  40)
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
        play = Button((200, 80), (width_screen // 2 - 100, height_screen // 2 + 30),  'Играть',  40)
        settings = Button((200, 80), (width_screen // 2 - 100, height_screen // 2 + 120),  'Настройки',  40)
        quit = Button((200, 80), (width_screen // 2 - 100, height_screen // 2 + 210),  'Выйти',  40)
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
        self.background = pygame.transform.scale(load_image('images/background_select_level.png'), (width_screen, height_screen))
        self.buttons = []

    """Для создания кнопок и других элементов"""

    def create(self):
        level_1 = Button((200, 200), (0.1 * width_screen, 0.2 * height_screen), 'Уровень 1', 30)
        level_2 = Button((200, 200), (0.1 * width_screen + 220, 0.2 * height_screen), 'Уровень 2',  30)
        level_3 = Button((200, 200), (0.11 * width_screen + 440, 0.2 * height_screen),  'Уровень 3',  30)
        back = Button((200, 80), (width_screen // 2 + 200, height_screen // 2 + 200),  'Назад',  40)
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
        self.auto_font_pos = (self.width // 2 - font.size(self.input_text)[0] // 2, self.height // 2 - font.size(self.input_text)[1] // 2)

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
            if event.unicode != '' and event.unicode != ' ' and event.unicode != '  ' and pygame.key.name(event.key) != 'backspace':
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
