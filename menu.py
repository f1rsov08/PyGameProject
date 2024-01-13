import pygame
import os
import sys

pygame.init()
disp = pygame.display.Info()
size_full_screen = width1, height1 = (disp.current_w, disp.current_h)
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
full_screen_coef = 1
current_type_tab = 'Main_Menu'


def full_screen():
    global screen, width, height,size, width1, height1, full_screen_coef
    if full_screen_coef:
        size = width, height = width1, height1
        screen = pygame.display.set_mode(size_full_screen, pygame.FULLSCREEN)
        settings.__init__()
        settings.create()
        select_lvl.__init__()
        select_lvl.create()
        full_screen_coef = 0
    else:
        size = width, height = 800, 600
        screen = pygame.display.set_mode(size)
        settings.__init__()
        settings.create()
        select_lvl.__init__()
        select_lvl.create()
        full_screen_coef = 1

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
            current_type_tab = 'Game'
        if self.input_text == 'Настройки':
            current_type_tab = 'Settings'
        if self.input_text == 'Полноэкранный режим':
            full_screen()
        if self.input_text == 'Назад':
            back()
        if self.input_text == 'Выйти':
            quit()





clock = pygame.time.Clock()
running = True
screen.fill('green')
main_menu = Main_Menu()
main_menu.create()
settings = Settings()
settings.create()
select_lvl = Select_Level()
select_lvl.create()
# but = Button((200, 100), (100, 100), 'black', "Играть", 'white', 40)
# but.create()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if current_type_tab == 'Main_Menu':
        main_menu.draw()
    if current_type_tab == 'Settings':
        settings.draw()
    if current_type_tab == 'Game':
        select_lvl.draw()
    print(current_type_tab)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
