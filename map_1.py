import pygame
import sys
import os

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


class Map_1:
    def __init__(self, screen):
        self.screen = screen
        self.barrier = pygame.transform.scale(load_image("barrier.png"), (80, 80))
        self.box= pygame.transform.scale(load_image("light_box.png"), (80, 80))

    def render(self):
        pass

    def create_board(self):
        self.width = 10
        self.height = 10
        self.board = [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                      [3, 1, 1, 1, 1, 1, 1, 1, 2, 3],
                      [3, 1, 1, 2, 1, 1, 1, 2, 1, 3],
                      [3, 1, 1, 2, 1, 1, 1, 1, 1, 3],
                      [3, 1, 1, 2, 1, 1, 1, 1, 1, 3],
                      [3, 1, 1, 1, 1, 1, 1, 1, 1, 3],
                      [3, 1, 1, 2, 1, 1, 1, 2, 1, 3],
                      [3, 1, 1, 1, 1, 1, 1, 1, 1, 3],
                      [3, 2, 1, 1, 1, 1, 1, 1, 1, 3],
                      [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 80
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.board[x][y] == 3:
                    self.screen.blit(self.barrier, (x * self.cell_size, y * self.cell_size))
                if self.board[x][y] == 2:
                    self.screen.blit(self.box, (x * self.cell_size, y * self.cell_size))
                if self.board[x][y] == 1:
                    pygame.draw.rect(self.screen, 'gray', (x * self.cell_size, y * self.cell_size,
                                                            self.cell_size, self.cell_size), 0)

                pygame.draw.rect(self.screen, 'white', (x * self.cell_size, y * self.cell_size,
                                                        self.cell_size, self.cell_size), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        # self.on_click(cell)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= x < self.width and 0 <= y < self.height:
            print((x, y))
        else:
            print(None)

    def getboard(self):
        return self.board
