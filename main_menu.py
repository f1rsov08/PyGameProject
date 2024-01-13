import pygame
import os
import sys

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
type = 'Main_Menu'


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
        pass
    def


class Main_Menu:
    def __init__(self):
        self.buttons = []

    def create(self):
        self.background = pygame.transform.scale(load_image('images/background.png'), (width, height))
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
        if self.input_text == 'Играть':
            type = 'Game'
        if self.input_text == 'Настройки':
            type = 'Settings'




clock = pygame.time.Clock()
running = True
screen.fill('green')
main_menu = Main_Menu()
main_menu.create()
settins = Settings()
# but = Button((200, 100), (100, 100), 'black', "Играть", 'white', 40)
# but.create()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if type == 'Main_Menu':
        main_menu.draw()
    if type == 'Settings'
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
