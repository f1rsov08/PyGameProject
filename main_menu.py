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
