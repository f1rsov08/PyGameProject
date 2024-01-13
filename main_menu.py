import pygame

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)


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
        self.auto_font_pos = (self.width // 2 - self.font.size(self.text)[0] // 2, self.height // 2 - self.font.size(self.text)[1] // 2)

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
                print('НАЖАЛ')
        else:
            self.not_aimed_button_color()


clock = pygame.time.Clock()
running = True
screen.fill('green')
#but = Button((200, 100), (100, 100), 'black', "Играть", 'white', 40)
#but.create()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #but.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
